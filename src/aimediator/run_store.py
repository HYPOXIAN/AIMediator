"""Portable run identity, snapshots, advisory locking and lifecycle state."""
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
from importlib.resources import files
import os
from pathlib import Path
import platform
import numpy as np
from . import __version__
from .common import Failure, canonical, input_rows, read, sha, write
from .resources import asset_path


def now():
    return datetime.now(timezone.utc).isoformat()


def code_manifest():
    root = Path(str(files('aimediator')))
    return {'package_version': __version__, 'python': platform.python_version(), 'numpy': np.__version__,
            'modules': {p.name: sha(p.read_bytes()) for p in sorted(root.glob('*.py'))}}


def resource_manifest():
    root = asset_path()
    return {str(p.relative_to(root)): sha(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file()}


def identity(raw, rows, cfg, installed):
    return {'input_sha256': sha(raw), 'sources_sha256': sha(canonical(rows)),
            'config_sha256': sha(canonical(cfg)), 'resources': resource_manifest(),
            'code': code_manifest(), 'models': {m: installed[m] for m in cfg['routing']['models']},
            'embedding': {'provider': cfg['embedding']['provider'], 'model': cfg['embedding']['model'],
                          'endpoint': cfg['embedding']['endpoint'] if cfg['embedding']['provider'] == 'configured' else cfg['base_url'],
                          'digest': None if cfg['embedding']['provider'] == 'configured' else installed[cfg['embedding']['model']],
                          'digest_verified': cfg['embedding']['provider'] == 'ollama'}}


@contextmanager
def lock(folder):
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


def initialize(folder, raw, rows, cfg, installed, provenance):
    folder.mkdir(parents=True, exist_ok=False)
    ident = identity(raw, rows, cfg, installed)
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
    state(folder, 'created', 'preflight')


# Validation files already read by _completed_requests, for the last run folder
# only: path -> (stat signature, sort key, request directory, completed).
_validations = {}


def _completed_requests(folder):
    """Return the request directories whose validation.json has no errors, reading only new or changed files."""
    known = _validations.pop(str(folder), {})
    _validations.clear()
    entries = []
    for path in (folder / 'requests').rglob('validation.json'):
        info = os.stat(path)
        # Writers replace files (common.write), so a rewrite also changes the inode.
        signature = (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)
        entry = known.get(str(path))
        if entry is None or entry[0] != signature:
            relative = path.relative_to(folder)
            entry = (signature, relative.parts, str(relative.parent), not read(path).get('errors'))
        entries.append((str(path), entry))
    _validations[str(folder)] = dict(entries)
    # The paths share the folder prefix, so ordering by parts is the order of sorted paths.
    return [entry[2] for _, entry in sorted(entries, key=lambda item: item[1][1]) if entry[3]]


def state(folder, status, stage, reason=None):
    previous = read(folder / 'run-state.json') if (folder / 'run-state.json').exists() else {}
    completed = _completed_requests(folder)
    write(folder / 'run-state.json', {**previous, 'schema_version': 'aimediator-state-v1',
          'run_state': status, 'stage': stage, 'updated_at_utc': now(), 'reason': reason,
          'requested_stop_stage': read(folder / 'resolved-config.json')['stop_after'],
          'completed_request_identities': completed})


def load_resume(folder):
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


def coverage(folder, rows):
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


def technical_failures(folder, ledger):
    decisions = {r['comment_id']: r for r in read(folder / 'relevance.json')} if (folder / 'relevance.json').exists() else {}
    failures = [r['comment_id'] for r in ledger if r['status'] in (
        'pending', 'quality_pending', 'quality_failed', 'extraction_failed', 'extraction_pending')
        or r['status'] == 'relevance_pending_or_failed' and decisions.get(r['comment_id'], {}).get('model_related') is None]
    quarantine = read(folder / 'quarantined-claims.json') if (folder / 'quarantined-claims.json').exists() else []
    failures.extend(q['claim_id'] for q in quarantine if q.get('stage') == 'semantic_audit' and not q.get('audit'))
    return sorted(set(failures))


def snapshot_artifacts(folder):
    # Completion replay also verifies artifact bytes, not just the existence of a directory.
    names = ['retrieval.json', 'relevance.json', 'full-pipeline-coverage.json', 'validated-claims.json',
             'quarantined-claims.json', 'balance-report.json', 'summary.json', 'evidence-quality.json']
    return {name: sha((folder / name).read_bytes()) for name in names if (folder / name).exists()}
