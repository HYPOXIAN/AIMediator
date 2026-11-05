"""Portable run identity, snapshots, advisory locking and lifecycle state."""
from __future__ import annotations

import bisect
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
from importlib.resources import files
from pathlib import Path
import platform
from typing import Any, Iterator
import numpy as np
from . import __version__
from .common import Failure, canonical, input_rows, read, sha, write
from .resources import asset_path


def now() -> str:
    """Return the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def code_manifest() -> dict[str, Any]:
    """Return the package, Python and NumPy versions and the SHA-256 of every top-level package module."""
    root = Path(str(files('aimediator')))
    return {'package_version': __version__, 'python': platform.python_version(), 'numpy': np.__version__,
            'modules': {p.name: sha(p.read_bytes()) for p in sorted(root.glob('*.py'))}}


def resource_manifest() -> dict[str, str]:
    """Return the SHA-256 of every packaged asset file, keyed by its path inside the asset directory."""
    root = asset_path()
    return {str(p.relative_to(root)): sha(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file()}


def identity(raw: bytes, rows: list[dict[str, Any]], cfg: dict[str, Any], installed: dict[str, str],
             service_version: str | None) -> dict[str, Any]:
    """Return the run identity: input, source, configuration, resource, code, model, service and embedding fingerprints."""
    return {'input_sha256': sha(raw), 'sources_sha256': sha(canonical(rows)),
            'config_sha256': sha(canonical(cfg)), 'resources': resource_manifest(),
            'code': code_manifest(), 'models': {m: installed[m] for m in cfg['routing']['models']},
            'service': {'ollama_version': service_version},
            'embedding': {'provider': cfg['embedding']['provider'], 'model': cfg['embedding']['model'],
                          'endpoint': cfg['embedding']['endpoint'] if cfg['embedding']['provider'] == 'configured' else cfg['base_url'],
                          'digest': None if cfg['embedding']['provider'] == 'configured' else installed[cfg['embedding']['model']],
                          'digest_verified': cfg['embedding']['provider'] == 'ollama'}}


@contextmanager
def lock(folder: Path) -> Iterator[None]:
    """Hold the exclusive writer lock of a run folder, or raise Failure(4) when another writer holds it."""
    # Existing files are never truncated. flock ownership is released by the OS.
    with (folder / '.writer.lock').open('a', encoding='utf-8') as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Failure(4, 'Another writer owns the run lock') from None
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def initialize(folder: Path, raw: bytes, rows: list[dict[str, Any]], cfg: dict[str, Any], installed: dict[str, str],
               provenance: str, service_version: str | None) -> None:
    """Create a run folder with its manifest and its configuration, input, source, code and resource snapshots."""
    folder.mkdir(parents=True, exist_ok=False)
    ident = identity(raw, rows, cfg, installed, service_version)
    write(folder / 'manifest.json', {'schema_version': 'aimediator-run-v1', 'identity': ident,
          'run_id': sha(canonical(ident)), 'created_at_utc': now(), 'execution_provenance': provenance,
          'remote_identity_limitation': 'Configured remote weights cannot be locally verified' if cfg['embedding']['provider'] == 'configured' else None})
    write(folder / 'resolved-config.json', cfg)
    (folder / 'input-snapshot.jsonl').write_bytes(raw)
    write(folder / 'source-snapshot.json', rows)
    write(folder / 'code-manifest.json', ident['code'])
    for name in ident['resources']:
        target = folder / 'resource-snapshot' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(asset_path(name).read_bytes())
    # The folder is new, so its request index is known to be empty.
    _requests.clear()
    _requests[str(folder)] = ({}, [])
    state(folder, 'created', 'preflight')


# Request index of the last run folder only: run folder -> (completed flag by
# request directory relative to the run folder, [(sort key, request directory)]
# kept sorted). The sort key is the relative path parts of the request's
# validation.json, so the order is that of the sorted validation paths.
_requests = {}


def record_request(folder: Path, relative: Path | str, completed: bool) -> None:
    """Record that a request's validation.json was written, with or without errors, in the folder's index.

    The runner's journal callback. A folder without an index is ignored: the next
    ``state`` call lists its validation files, this one included.
    """
    index = _requests.get(str(folder))
    if index is not None:
        flags, order = index
        relative = Path(relative)
        directory = str(relative)
        if directory not in flags:
            bisect.insort(order, ((relative / 'validation.json').parts, directory))
        flags[directory] = completed


def _completed_requests(folder: Path) -> list[str]:
    """Return the request directories whose validation.json has no errors.

    The first call for a folder in a process lists and reads every validation file
    (a new or resumed run); later calls use the index that ``record_request`` keeps.
    """
    index = _requests.get(str(folder))
    if index is None:
        flags, order = {}, []
        for path in (folder / 'requests').rglob('validation.json'):
            relative = path.relative_to(folder)
            flags[str(relative.parent)] = not read(path).get('errors')
            order.append((relative.parts, str(relative.parent)))
        # The paths share the folder prefix, so ordering by parts is the order of sorted paths.
        order.sort()
        index = flags, order
        _requests.clear()
        _requests[str(folder)] = index
    flags, order = index
    return [directory for _, directory in order if flags[directory]]


def state(folder: Path, status: str, stage: str, reason: str | None = None) -> None:
    """Update run-state.json with the status, stage and reason, and the completed request identities."""
    previous = read(folder / 'run-state.json') if (folder / 'run-state.json').exists() else {}
    if status in ('interrupted', 'failed'):
        # The interruption or error may fall between a validation.json write and its journal call.
        _requests.pop(str(folder), None)
    completed = _completed_requests(folder)
    write(folder / 'run-state.json', {**previous, 'schema_version': 'aimediator-state-v1',
          'run_state': status, 'stage': stage, 'updated_at_utc': now(), 'reason': reason,
          'requested_stop_stage': read(folder / 'resolved-config.json')['stop_after'],
          'completed_request_identities': completed})


def load_resume(folder: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    """Return the manifest, configuration and rows of a run whose recorded identity still holds, or raise Failure(4)."""
    # A resume lists the request directories again, also within one process.
    _requests.pop(str(folder), None)
    manifest = read(folder / 'manifest.json')
    if manifest.get('schema_version') != 'aimediator-run-v1':
        raise Failure(4, 'Only aimediator-run-v1 runs can be resumed')
    cfg = read(folder / 'resolved-config.json')
    raw = (folder / 'input-snapshot.jsonl').read_bytes()
    rows = input_rows(raw)
    saved = manifest['identity']
    checks = [sha(raw) == saved['input_sha256'], sha(canonical(rows)) == saved['sources_sha256'],
              sha(canonical(read(folder / 'source-snapshot.json'))) == saved['sources_sha256'],
              sha(canonical(cfg)) == saved['config_sha256'], code_manifest() == saved['code'],
              read(folder / 'code-manifest.json') == saved['code'], resource_manifest() == saved['resources'],
              sha(canonical(saved)) == manifest['run_id']]
    for name, expected in saved['resources'].items():
        p = folder / 'resource-snapshot' / name
        checks.append(p.is_file() and sha(p.read_bytes()) == expected)
    if not all(checks):
        raise Failure(4, 'Run input/configuration/code/resource identity mismatch; start a new run')
    return manifest, cfg, rows


def coverage(folder: Path, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the coverage ledger: one aimediator-coverage-v1 record per source row."""
    path = folder / 'full-pipeline-coverage.json'
    records = read(path) if path.exists() else []
    by_id = {r['comment_id']: r for r in records}
    if len(by_id) != len(records) or set(by_id) - {r['record_id'] for r in rows}:
        raise Failure(2, 'Coverage has duplicate or foreign source IDs')
    decisions = {r['comment_id']: r for r in read(folder / 'relevance.json')} if (folder / 'relevance.json').exists() else {}
    claims = read(folder / 'validated-claims.json') if (folder / 'validated-claims.json').exists() else []
    quarantined = read(folder / 'quarantined-claims.json') if (folder / 'quarantined-claims.json').exists() else []
    accepted = Counter(claim['comment_id'] for claim in claims)
    rejected = Counter(claim['comment_id'] for claim in quarantined)
    result = []
    for source in rows:
        cid = source['record_id']
        row = dict(by_id.get(cid, {'comment_id': cid, 'language': source['language'],
            'status': 'pending', 'relevance': 'pending', 'quality_status': 'pending',
            'extraction': None, 'source_review': 'not_assessed'}))
        decision = decisions.get(cid, {})
        relevance = ('admitted' if decision.get('agreement') else
                     'ambiguous' if decision.get('model_uncertain') and decision.get('model_related') is not None else
                     'technical_failure_or_pending' if row['status'] == 'relevance_pending_or_failed' else
                     'rejected' if row['status'] == 'relevance_rejected' else row.get('relevance', 'pending'))
        accepted_count = accepted[cid]
        rejected_count = rejected[cid]
        row.update(schema_version='aimediator-coverage-v1', relevance_state=relevance,
                   language_state='supported' if source['language'] in ('en', 'zh') else 'unsupported',
                   automatic_audit={'accepted_claims': accepted_count, 'quarantined_claims': rejected_count,
                                    'state': 'recorded_outcomes' if accepted_count or rejected_count else 'not_assessed'})
        if accepted_count or rejected_count:
            row['source_review'] = 'pending_external_review'
        result.append(row)
    return result


def technical_failures(folder: Path, ledger: list[dict[str, Any]]) -> list[str]:
    """Return the sorted comment and claim IDs that a technical failure left unfinished."""
    decisions = {r['comment_id']: r for r in read(folder / 'relevance.json')} if (folder / 'relevance.json').exists() else {}
    failures = [r['comment_id'] for r in ledger if r['status'] in (
        'pending', 'quality_pending', 'quality_failed', 'extraction_failed', 'extraction_pending')
        or r['status'] == 'relevance_pending_or_failed' and decisions.get(r['comment_id'], {}).get('model_related') is None]
    quarantine = read(folder / 'quarantined-claims.json') if (folder / 'quarantined-claims.json').exists() else []
    failures.extend(q['claim_id'] for q in quarantine if q.get('stage') == 'semantic_audit' and not q.get('audit'))
    return sorted(set(failures))


def snapshot_artifacts(folder: Path) -> dict[str, str]:
    """Return the SHA-256 of each existing main run artifact, keyed by file name."""
    # Completion replay also verifies artifact bytes, not just the existence of a directory.
    names = ['retrieval.json', 'relevance.json', 'full-pipeline-coverage.json', 'validated-claims.json',
             'quarantined-claims.json', 'balance-report.json', 'summary.json', 'evidence-quality.json']
    return {name: sha((folder / name).read_bytes()) for name in names if (folder / name).exists()}
