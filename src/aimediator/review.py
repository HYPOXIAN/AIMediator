"""Read-only run adapters and immutable fingerprinted source-review overlays."""
import copy
import csv
from pathlib import Path
from . import balance_policy, evidence, evidence_quality
from .common import Failure, canonical, new_path, read, sha, write
from .legacy_review import apply_review, proposal_hash

REQUIRED = ('source-snapshot.json', 'relevance.json', 'validated-claims.json', 'quarantined-claims.json')


def load_run(folder):
    folder = Path(folder).resolve()
    manifest = read(folder / 'manifest.json') if (folder / 'manifest.json').exists() else {}
    product = manifest.get('schema_version') == 'aimediator-run-v1'
    raw_path = folder / 'balance-report.json'
    if not raw_path.exists() and product:
        raw = {'report_schema_version': None, 'evidence_quality_mode': read(folder / 'resolved-config.json')['evidence_quality'],
               'summary': {}, 'full_pipeline_coverage': []}
    else:
        raw = read(raw_path)
        schema, mode = raw.get('report_schema_version'), raw.get('evidence_quality_mode')
        if schema not in ('balance-evidence-v2', 'balance-report-v3'):
            raise Failure(2, 'Unsupported legacy/engine report schema; only balance-evidence-v2 and balance-report-v3 are allowed')
        if mode not in ('off', 'shadow', 'enforce') or (schema == 'balance-report-v3') != (mode == 'enforce'):
            raise Failure(2, 'Engine report schema and independent quality mode disagree')
    if product:
        cfg = read(folder / 'resolved-config.json')
        if (sha(canonical(cfg)) != manifest['identity']['config_sha256']
                or sha(canonical(manifest['identity'])) != manifest['run_id']
                or cfg['evidence_quality'] != raw['evidence_quality_mode']):
            raise Failure(4, 'Saved configuration/run identity and report quality mode disagree')
    else:
        declared = manifest.get('identity', {}).get('evidence_quality', {})
        if isinstance(declared, dict) and declared.get('mode') is not None and declared['mode'] != raw['evidence_quality_mode']:
            raise Failure(2, 'Legacy manifest and report quality mode disagree')
    values, hashes = {}, {}
    for name in REQUIRED:
        path = folder / name
        if not path.exists():
            if product and name != 'source-snapshot.json':
                values[name] = []
                continue
            raise Failure(2, 'Legacy evidence artifact required: ' + name)
        values[name] = read(path)
        hashes[name] = sha(path.read_bytes())
    sources = {r['record_id']: r for r in values['source-snapshot.json']}
    if len(sources) != len(values['source-snapshot.json']) or not sources:
        raise Failure(2, 'Source snapshot has duplicate IDs or is empty')
    for row in sources.values():
        if not all(isinstance(row.get(k), str) and row[k].strip() for k in ('record_id','text_original','language')):
            raise Failure(2, 'Invalid source snapshot fields')
    if product:
        ident = manifest['identity']
        if sha(canonical(values['source-snapshot.json'])) != ident['sources_sha256']:
            raise Failure(4, 'Source fingerprint mismatch')
        if sha((folder / 'input-snapshot.jsonl').read_bytes()) != ident['input_sha256']:
            raise Failure(4, 'Original-byte source fingerprint mismatch')
    relevance = values['relevance.json']
    if len({r['comment_id'] for r in relevance}) != len(relevance) or any(r['comment_id'] not in sources for r in relevance):
        raise Failure(2, 'Invalid relevance source coverage')
    for row in relevance:
        if row.get('agreement') is True and not balance_policy.retrieval_review_agrees(row, {
                'related': row.get('model_related'), 'uncertain': row.get('model_uncertain')}):
            raise Failure(2, 'Saved relevance admission lacks required retrieval/model agreement')
    admitted = {r['comment_id'] for r in relevance if r.get('agreement') is True}
    qrecords = {}
    if raw['evidence_quality_mode'] != 'off':
        qpath = folder / 'evidence-quality.json'
        if not qpath.exists() and (not product or raw_path.exists()):
            raise Failure(2, 'Quality mode requires evidence-quality.json')
        for q in read(qpath) if qpath.exists() else []:
            cid = q['comment_id']
            if cid not in sources or cid in qrecords or q['content_sha256'] != sha(sources[cid]['text_original'].encode('utf-8')):
                raise Failure(2, 'Quality source binding mismatch')
            if q.get('status') not in ('completed', 'failed'):
                raise Failure(2, 'Unknown quality processing status')
            if q['status'] == 'failed' and (not q.get('errors') or any(r.get('route') != 'review' for r in q.get('routing', []))):
                raise Failure(2, 'Failed quality annotation cannot supply eligible evidence')
            if q['status'] == 'completed':
                # Each record is validated by the rules of its own schema_version (v1 or v2, plan 4.2).
                errors = evidence_quality.stored_annotation_errors(q, sources[cid], evidence.evidence_units(sources[cid]['text_original']))
                recomputed = evidence_quality.qualify(q['annotation'], sources[cid], evidence.evidence_units(sources[cid]['text_original']))
                if errors or q['routing'] != recomputed['routing'] or q.get('routes_present') != recomputed['routes_present']:
                    raise Failure(2, 'Quality annotation/routing is not source-bound')
            qrecords[cid] = q
        if qpath.exists():
            hashes['evidence-quality.json'] = sha(qpath.read_bytes())
    proposals, automatic = {}, set()
    entries = []
    for c in values['validated-claims.json']:
        entries.append({'claim_id': c['claim_id'], 'comment_id': c['comment_id'], 'model': c.get('model'),
                        'claim': c, 'audit': c.get('semantic_audit'), 'errors': []})
        automatic.add(c['claim_id'])
    entries += values['quarantined-claims.json']
    # Partial runs can contain structurally complete, source-bound proposals whose
    # automatic audit has not finished. Keep those reviewable without promoting
    # them to automatically accepted evidence.
    finalized = {e['claim_id'] for e in entries}
    pending = {}
    for name in ('claims-before-audit.json', 'audit-progress.json'):
        path = folder / name
        if path.exists():
            hashes[name] = sha(path.read_bytes())
            for entry in read(path):
                if entry['claim_id'] not in finalized:
                    pending[entry['claim_id']] = entry
    entries += list(pending.values())
    for e in entries:
        c = e.get('claim')
        if not isinstance(c, dict) or not set(evidence.CLAIM['properties']) <= set(c):
            continue  # Malformed generations remain diagnostics, never editable invented claims.
        core = {k: c[k] for k in evidence.CLAIM['properties']}
        if evidence_quality.schema_errors(core, evidence.CLAIM):
            continue
        cid, claim_id = e['comment_id'], e['claim_id']
        if claim_id in proposals or cid not in sources or cid not in admitted:
            raise Failure(2, 'Duplicate, foreign or unadmitted proposal')
        errors, enriched = evidence.ground_claim(core, sources[cid], {r['canonical_name'] for r in evidence.character_reference()})
        if c.get('evidence') is not None and enriched is not None and c['evidence'] != enriched['evidence']:
            errors.append('Saved evidence differs from immutable original source')
        if raw['evidence_quality_mode'] == 'enforce':
            record = qrecords.get(cid)
            if not record:
                raise Failure(2, 'Enforce proposal has no same-comment quality record')
            binding, qualification = evidence_quality.bind_claim(c, record, evidence.character_reference(sources[cid]['text_original']))
            errors += binding
            if not binding and c.get('evidence_quality') != qualification:
                errors.append('Saved quality qualification differs from source-bound annotation')
        if raw['evidence_quality_mode'] != 'enforce' and (c.get('evidence_quality') or {}).get('mode') == 'enforce':
            raise Failure(2, 'Enforced proposal cannot be relabeled as unassessed quality')
        audit = c.get('semantic_audit') or e.get('audit')
        if claim_id in automatic and (errors or not audit or audit.get('supported') is not True):
            raise Failure(2, 'Automatic claim lacks source binding, quality eligibility or supported audit')
        proposals[claim_id] = {**copy.deepcopy(e), 'automatic_errors': list(e.get('errors', [])) + errors,
                               'automatic_accepted': claim_id in automatic, 'audit': audit}
    for name in ('balance-report.json', 'full-pipeline-coverage.json', 'run-state.json'):
        if (folder / name).exists():
            hashes[name] = sha((folder / name).read_bytes())
    fingerprints = {'run_sha256': sha(canonical({'manifest': manifest, 'artifacts': hashes})),
                    'source_sha256': sha(canonical(values['source-snapshot.json'])),
                    'proposal_set_sha256': sha(canonical({k: proposal_hash(v['claim']) for k,v in proposals.items()}))}
    state = read(folder / 'run-state.json')['run_state'] if product else 'legacy_completion_unknown'
    return {'folder': folder, 'raw': raw, 'sources': sources, 'admitted': admitted, 'proposals': proposals,
            'automatic': automatic, 'quality': list(qrecords.values()), 'fingerprints': fingerprints,
            'provenance': manifest.get('execution_provenance', 'legacy_unknown_model_identity'),
            'run_identity': manifest.get('identity') if product else None, 'run_state': state,
            'legacy': not product}


def export_review(run, out):
    data = load_run(run)
    out = new_path(out, run)
    decisions = {cid: {'proposal_sha256': proposal_hash(e['claim']), 'decision': 'uncertain', 'reason': 'pending_review'}
                 for cid,e in sorted(data['proposals'].items())}
    envelope = {'schema_version': 'aimediator-source-review-v1', **data['fingerprints'],
                'reviewer_type': None, 'reviewer_id': None, 'decisions': decisions,
                'execution_provenance': data['provenance']}
    out.mkdir(parents=True)
    write(out / 'decisions.json', envelope)
    write(out / 'proposals.json', data['proposals'])
    def cell(value):
        text = str(value or '')
        return "'" + text if text.lstrip().startswith(('=', '+', '-', '@', '\t', '\r', '\n')) else text
    with (out / 'worksheet.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['claim_id','comment_id','automatic_accepted','automatic_errors','character','target','direction','recommendation','original_source','decision','reason'])
        for cid, e in sorted(data['proposals'].items()):
            c = e['claim']
            writer.writerow([cell(x) for x in (cid,e['comment_id'],e['automatic_accepted'], '; '.join(e['automatic_errors']),
                c['character'],c['target'],c['direction'],c['recommendation'],data['sources'][e['comment_id']]['text_original'], 'uncertain','pending_review')])
    (out / 'README.md').write_text(encoding='utf-8', data='''# Source review

Edit decisions.json; CSV is a reading worksheet only. Set reviewer_type to agent
or human and reviewer_id to your identifier. Inspect the complete original source
in proposals/source run. Keep uninspected items uncertain with a reason. Exact
proposal coverage is required. Allowed corrections: evidence_ids, target,
recommendation, corrected_direction. Identity and source text cannot change.
Changes lose their previous automatic audit and remain pending_reaudit.
Source acceptance does not verify game mechanics, patch applicability or automatic
success. Import and report make no model calls. Synthetic demo reviewers must be
labeled agent; the demo does not establish semantic accuracy.
''')
    return out, len(decisions)


def import_review(run, decisions_path, out):
    data = load_run(run)
    envelope = read(decisions_path)
    expected_keys = {'schema_version','reviewer_type','reviewer_id','decisions','execution_provenance', *data['fingerprints']}
    if not isinstance(envelope, dict) or set(envelope) != expected_keys or envelope.get('schema_version') != 'aimediator-source-review-v1':
        raise Failure(2, 'Unsupported review envelope/schema')
    if any(envelope.get(k) != v for k,v in data['fingerprints'].items()) or envelope['execution_provenance'] != data['provenance']:
        raise Failure(4, 'Review source/run/proposal fingerprint mismatch')
    if envelope['reviewer_type'] not in ('agent','human') or not isinstance(envelope['reviewer_id'], str) or not envelope['reviewer_id'].strip():
        raise Failure(2, 'Set reviewer_type and reviewer_id before importing a review')
    if data['provenance'] == 'agent_authored_synthetic_fixture_transports' and envelope['reviewer_type'] != 'agent':
        raise Failure(2, 'Synthetic demo reviews must retain agent provenance')
    if not isinstance(envelope['decisions'], dict):
        raise Failure(2, 'Review decisions must be keyed by claim ID')
    for claim_id, decision in envelope['decisions'].items():
        if (claim_id in data['proposals'] and isinstance(decision, dict)
                and decision.get('proposal_sha256') != proposal_hash(data['proposals'][claim_id]['claim'])):
            raise Failure(4, 'Reviewed proposal fingerprint mismatch')
    try:
        accepted, excluded = apply_review(data['proposals'], envelope['decisions'], data['sources'], data['admitted'],
                                         {r['canonical_name'] for r in evidence.character_reference()})
    except (ValueError, TypeError, KeyError) as exc:
        raise Failure(2, 'Review validation failed: ' + str(exc)) from None
    accepted = decorate_review(data, accepted)
    out = new_path(out, run)
    out.mkdir(parents=True)
    write(out / 'decisions.json', envelope)
    write(out / 'source-reviewed-claims.json', accepted)
    write(out / 'source-review-exclusions.json', excluded)
    review = {'schema_version': 'aimediator-review-overlay-v1', **data['fingerprints'],
              'reviewer_type': envelope['reviewer_type'], 'reviewer_id': envelope['reviewer_id'],
              'execution_provenance': data['provenance'], 'decisions_sha256': sha(canonical(envelope)),
              'claims_sha256': sha(canonical(accepted)), 'exclusions_sha256': sha(canonical(excluded))}
    write(out / 'review-manifest.json', review)
    return out, {'source_accepted_claims': len(accepted), 'formal_eligible_claims': sum(c['formal_eligible'] for c in accepted),
                 'rejected_claims': sum(c['decision']=='reject' for c in excluded), 'uncertain_claims': sum(c['decision']=='uncertain' for c in excluded)}



def decorate_review(data, accepted):
    for c in accepted:
        original = data['proposals'][c['claim_id']]
        changed = any(c[k] != original['claim'][k] for k in evidence.CLAIM['properties'])
        c['original_model_claim'] = copy.deepcopy(original['claim'])
        c['automatic_errors'] = original['automatic_errors']
        c['automatic_accepted'] = original['automatic_accepted']
        c['semantic_audit'] = None if changed else original['audit']
        c['audit_status'] = 'pending_reaudit' if changed else 'original_automatic_audit'
        c['formal_eligible'] = not changed and original['automatic_accepted'] and not original['automatic_errors'] and bool((c['semantic_audit'] or {}).get('supported'))
    return accepted


def load_overlay(data, path):
    path = Path(path)
    overlay = read(path / 'review-manifest.json')
    if overlay.get('schema_version') != 'aimediator-review-overlay-v1' or any(overlay.get(k) != v for k,v in data['fingerprints'].items()):
        raise Failure(4, 'Review overlay does not match the source run')
    decisions = read(path / 'decisions.json')
    claims = read(path / 'source-reviewed-claims.json')
    exclusions = read(path / 'source-review-exclusions.json')
    if overlay.get('decisions_sha256') != sha(canonical(decisions)) or overlay.get('claims_sha256') != sha(canonical(claims)) or overlay.get('exclusions_sha256') != sha(canonical(exclusions)):
        raise Failure(4, 'Review overlay content fingerprint mismatch')
    if (decisions.get('schema_version') != 'aimediator-source-review-v1'
            or decisions.get('reviewer_type') not in ('agent', 'human')
            or not isinstance(decisions.get('reviewer_id'), str) or not decisions['reviewer_id'].strip()
            or any(decisions.get(k) != v for k, v in data['fingerprints'].items())
            or any(overlay.get(k) != decisions.get(k) for k in ('reviewer_type','reviewer_id','execution_provenance'))
            or decisions.get('execution_provenance') != data['provenance']):
        raise Failure(4, 'Review overlay provenance/envelope mismatch')
    if data['provenance'] == 'agent_authored_synthetic_fixture_transports' and decisions['reviewer_type'] != 'agent':
        raise Failure(2, 'Synthetic review must retain agent provenance')
    # Re-run source/quality validation and reconstruct every derived field, including
    # evidence spans, original proposals and audit eligibility, before export.
    expected, rejected = apply_review(data['proposals'], decisions['decisions'], data['sources'], data['admitted'],
                                     {r['canonical_name'] for r in evidence.character_reference()})
    expected = decorate_review(data, expected)
    if canonical(expected) != canonical(claims) or canonical(rejected) != canonical(exclusions):
        raise Failure(4, 'Review overlay differs from validated source decisions')
    return overlay, claims, exclusions
