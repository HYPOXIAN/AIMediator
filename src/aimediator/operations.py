"""Operational services; new product runs never implicitly resume."""
from pathlib import Path
import sys
from types import SimpleNamespace
from . import balance_policy, evidence_quality, pipeline, resources, retrieval, runner
from .common import Failure, canonical, input_rows, new_path, read, sha, write
from .config import credential, resolve, validate
from .inference import Transport, probe
from .resources import asset_path
from . import run_store as store


def preflight(cfg, input_path=None, out=None):
    validate(cfg)
    for name in store.resource_manifest():
        if not asset_path(name).is_file():
            raise Failure(3, 'Packaged resource unavailable: ' + name)
    evidence_quality.load_policy()
    rows = input_rows(Path(input_path).read_bytes()) if input_path else None
    if out:
        new_path(out)
    return rows


def doctor(cfg, input_path=None, out=None, offline=False, env_file=None):
    rows = preflight(cfg, input_path, out)
    checks = {'dependencies': 'passed', 'resources': 'passed', 'configuration': 'passed',
              'input': 'passed' if rows else 'not_provided', 'output': 'passed' if out else 'not_provided',
              'service_models': 'not_checked', 'embedding_probe': 'not_checked'}
    installed = None
    if not offline:
        installed = probe(cfg, Transport(cfg, credential(cfg, env_file)))
        checks.update(service_models='passed', embedding_probe='passed')
    return {'checks': checks, 'installed_models': installed, 'input_comments': len(rows) if rows else None,
            'remote_digest_verified': cfg['embedding']['provider'] == 'ollama',
            'runtime': {k:v for k,v in store.code_manifest().items() if k != 'modules'}}


prompts_for = resources.prompts


def analyze(input_path=None, out=None, cfg=None, resume=None, env_file=None, transport=None, quiet=False):
    warnings = []
    if resume:
        folder = Path(resume).resolve()
        # All local identity checks precede any write, lock or network probe.
        try:
            manifest, cfg, rows = store.load_resume(folder)
        except Failure as exc:
            if exc.code == 2:
                raise Failure(4, 'Saved resume snapshot is invalid; start a new run') from None
            raise
        except (OSError, ValueError, TypeError, KeyError):
            raise Failure(4, 'Saved resume identity/snapshot is missing or invalid; start a new run') from None
        validate(cfg)
        if transport is None and manifest['execution_provenance'] == 'agent_authored_synthetic_fixture_transports':
            from .fixture_transport import FixtureTransport
            transport = FixtureTransport(cfg)
        current_state = read(folder / 'run-state.json')
        completed = current_state['run_state'] == 'completed'
        key = credential(cfg, env_file, required=not completed)
        transport = transport or Transport(cfg, key)
        installed = probe(cfg, transport, require_embedding=False)
        old = manifest['identity']
        if any(installed.get(m) != d for m, d in old['models'].items()) or (
            cfg['embedding']['provider'] == 'ollama' and installed.get(cfg['embedding']['model']) != old['embedding']['digest']):
            raise Failure(4, 'Installed model identity differs from saved run; start a new run')
        if env_file and cfg['embedding']['provider'] == 'configured':
            warnings.append('Credential file supplies credentials only; saved endpoint/model/configuration remain authoritative')
        if completed:
            if current_state.get('artifact_hashes') != store.snapshot_artifacts(folder):
                raise Failure(4, 'Completed run artifacts changed')
            return folder, status(folder), warnings
    else:
        cfg = cfg or resolve()
        preflight(cfg, input_path, out)
        folder = new_path(out)
        raw = Path(input_path).read_bytes()
        rows = input_rows(raw)
        key = credential(cfg, env_file)
        transport = transport or Transport(cfg, key)
        installed = probe(cfg, transport)
        try:
            store.initialize(folder, raw, rows, cfg, installed, transport.provenance)
        except FileExistsError:
            raise Failure(4, 'Output appeared during preflight; choose a new path') from None
    transport.folder = folder
    with store.lock(folder):
        try:
            store.state(folder, 'running', 'retrieval')
            mode = cfg['evidence_quality']
            prompts = resources.prompts(mode)
            write(folder / 'prompt-snapshot.json', prompts)
            write(folder / 'review-policy-snapshot.json', balance_policy.load_policy())
            policy = evidence_quality.load_policy() if mode != 'off' else None
            write(folder / 'quality-policy-snapshot.json', policy)
            manifest = read(folder / 'manifest.json')
            args = SimpleNamespace(out=folder, base_url=cfg['base_url'], embedding_model=cfg['embedding']['model'],
                evidence_quality=mode, relevance_only=cfg['stop_after'] == 'relevance', quality_only=cfg['stop_after'] == 'quality')
            quality_identity = {'mode': mode, 'policy': policy, 'run_identity': manifest['run_id']}
            engine_identity = {'mode': 'relevance_only' if args.relevance_only else 'quality_only' if args.quality_only else 'full_pipeline',
                               'runtime_options': {'num_gpu': cfg['num_gpu']} if cfg['num_gpu'] is not None else {}}
            def progress(stage, ids, succeeded):
                if succeeded is None:
                    store.state(folder, 'running', stage)
                elif not quiet:
                    unit = 'claims' if stage == 'verify' else 'comments'
                    print(f'{stage}: {len(ids) if succeeded else 0}/{len(ids)} {unit} in request',
                          file=sys.stderr, flush=True)

            def runner_factory(*values):
                return runner.Runner(*values, chat_transport=transport.chat, progress=progress,
                                     journal=lambda relative, completed: store.record_request(folder, relative, completed))

            def retrieve(*values):
                if not quiet:
                    print('retrieval: 0/%d comments' % len(values[0]), file=sys.stderr, flush=True)
                result = retrieval.retrieve(*values, api_transport=transport.api, embed_transport=transport.embed)
                if not quiet:
                    print('retrieval: %d/%d comments' % (len(result),len(values[0])), file=sys.stderr, flush=True)
                return result
            embedding_cfg = {'url': cfg['embedding']['endpoint'], 'model': cfg['embedding']['model']} if cfg['embedding']['provider'] == 'configured' else None
            pipeline.process(args, rows, cfg['routing'], list(cfg['routing']['models']), prompts,
                quality_identity, policy, engine_identity, embedding_cfg, runner_factory, retrieve)
            ledger = store.coverage(folder, rows)
            write(folder / 'full-pipeline-coverage.json', ledger)
            failures = store.technical_failures(folder, ledger)
            store.state(folder, 'partial' if failures else 'completed', cfg['stop_after'],
                        'Technical failures remain' if failures else None)
            state = read(folder / 'run-state.json')
            state.update(artifact_hashes=store.snapshot_artifacts(folder),
                         stage_counters={'input_comments': len(rows), 'coverage_comments': len(ledger),
                                         'technical_failure_units': len(failures)})
            write(folder / 'run-state.json', state)
            if failures:
                raise Failure(5, 'Artifacts saved; requested processing has unresolved technical failures')
        except KeyboardInterrupt:
            store.state(folder, 'interrupted', read(folder / 'run-state.json')['stage'], 'user_interruption')
            write(folder / 'full-pipeline-coverage.json', store.coverage(folder, rows))
            raise Failure(130, 'Interrupted; completed requests and partial streams preserved') from None
        except Failure as exc:
            if exc.code not in (4, 5):
                store.state(folder, 'failed', read(folder / 'run-state.json')['stage'], exc.message)
            elif exc.code == 5:
                store.state(folder, 'partial', read(folder / 'run-state.json')['stage'], exc.message)
                write(folder / 'full-pipeline-coverage.json', store.coverage(folder, rows))
            raise
        except Exception as exc:
            store.state(folder, 'failed', read(folder / 'run-state.json')['stage'], type(exc).__name__)
            write(folder / 'full-pipeline-coverage.json', store.coverage(folder, rows))
            raise Failure(1, 'Internal processing failure; safe diagnostic saved (' + type(exc).__name__ + ')') from None
    return folder, status(folder), warnings


def status(folder):
    folder = Path(folder)
    manifest = read(folder / 'manifest.json')
    if manifest.get('schema_version') != 'aimediator-run-v1':
        raise Failure(2, 'Status requires aimediator-run-v1')
    rows = read(folder / 'source-snapshot.json')
    ledger = store.coverage(folder, rows)
    state = read(folder / 'run-state.json')
    claims = read(folder / 'validated-claims.json') if (folder / 'validated-claims.json').exists() else []
    quarantine = read(folder / 'quarantined-claims.json') if (folder / 'quarantined-claims.json').exists() else []
    failures = store.technical_failures(folder, ledger)
    return {'run_state': state['run_state'], 'stage': state['stage'], 'requested_stop_stage': state['requested_stop_stage'],
            'counts': {'input_comments': len(rows), 'coverage_comments': len(ledger), 'automatically_accepted_claims': len(claims),
                       'quarantined_claims': len(quarantine), 'technical_failure_units': len(failures),
                       'ambiguous_relevance_comments': sum(r.get('relevance_state') == 'ambiguous' for r in ledger),
                       'quality_review_comments': sum('review' in r.get('routes_present', []) and r.get('quality_status') != 'failed' for r in ledger),
                       'valid_zero_claim_comments': sum((r.get('extraction') or {}).get('disposition') == 'no_supported_character_claim' for r in ledger)},
            'has_failures': bool(failures), 'has_pending_review': bool(claims or quarantine),
            'execution_provenance': manifest['execution_provenance'], 'semantic_accuracy': None}
