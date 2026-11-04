"""Shared analysis orchestration: relevance, evidence quality, extraction, source audit and report."""
from collections import Counter
from dataclasses import dataclass, field
import json

from . import evidence_quality as quality
from .balance_policy import load_policy, retrieval_review_agrees, triage_retrieval
from .common import write as write_json
from .evidence import character_reference, evidence_units, ground_claim
from .retrieval import retrieve
from .runner import Runner
VERSION = 'balance-evidence-v2'


def relevance_agrees(retrieved, review):
    return retrieval_review_agrees(retrieved, review)


def batches(rows, count=12, chars=18000):
    batch, size = [], 0
    for row in rows:
        length = len(json.dumps(row, ensure_ascii=False))
        if batch and (len(batch) >= count or size + length > chars):
            yield batch
            batch, size = [], 0
        batch.append(row)
        size += length
    if batch:
        yield batch


def aggregate(claims, quality_enforced=False):
    grouped = {}
    for claim in claims:
        if quality_enforced and ((claim.get('evidence_quality') or {}).get('mode') != 'enforce'
                or (claim.get('evidence_quality') or {}).get('route') != 'mechanism_evidence'
                or not (claim.get('semantic_audit') or {}).get('supported')):
            continue
        if claim['character'] is None or claim['direction'] not in (('buff', 'nerf', 'keep', 'unclear') if quality_enforced else ('buff', 'nerf')):
            continue
        if claim.get('character_identity', {}).get('normalization_status') == 'source_literal_unverified':
            continue
        # Preserve nuanced recommendations instead of performing an unverified model merge.
        key = (claim['character'], claim['direction'], claim.get('target')) if quality_enforced else (claim['character'], claim['direction'])
        group = grouped.setdefault(key, {'character': key[0], 'direction': key[1],
                                         'comment_ids': set(), 'recommendations': []})
        if quality_enforced:
            group['topic'] = key[2]
        group['comment_ids'].add(claim['comment_id'])
        group['recommendations'].append(claim)
    result = []
    for key in sorted(grouped, key=lambda k: tuple(v or '' for v in k)):
        group = grouped[key]
        group['comment_ids'] = sorted(group['comment_ids'])
        group['supporting_comment_count'] = len(group['comment_ids'])
        result.append(group)
    return result


def quality_source_counts(records, accepted):
    """Unique source sets, including overlap; no player identity is inferred."""
    general = {q['comment_id'] for q in records if any(r['route'] == 'opinion_only' for r in q['routing'])}
    concrete = {c['comment_id'] for c in accepted if (c.get('evidence_quality') or {}).get('mode') == 'enforce'}
    return {'opinion_comment_ids': sorted(general), 'audited_mechanism_comment_ids': sorted(concrete),
            'union_comment_ids': sorted(general | concrete), 'union_count': len(general | concrete),
            'overlap_comment_ids': sorted(general & concrete), 'categories_overlap': True}


def build_full_coverage(rows, decisions, routes, models, quality_records, coverage,
                        accepted, quarantine, quality_mode, args):
    extraction = {c['comment_id']: c for c in coverage}
    all_languages = {route['language'] for route in routes.values()}
    selected_languages = {routes[m]['language'] for m in models}
    result = []
    for row in rows:
        cid, lang = row['record_id'], row['language']
        d, q, e = decisions.get(cid), quality_records.get(cid), extraction.get(cid)
        if lang not in all_languages:
            status = 'unsupported_language'
        elif lang not in selected_languages:
            status = 'unselected_language'
        elif not d or not d['agreement']:
            status = 'relevance_pending_or_failed' if not d or d['model_related'] is None or d.get('model_uncertain') else 'relevance_rejected'
            if d and d.get('retrieval_triage') == 'unrelated':
                status = 'relevance_rejected'
        elif getattr(args, 'relevance_only', False):
            status = 'relevance_only_complete'
        elif quality_mode != 'off' and not q:
            status = 'quality_pending'
        elif getattr(args, 'quality_only', False):
            status = 'quality_failed' if q['status'] == 'failed' else 'quality_completed'
        elif e:
            status = 'extraction_failed' if e['disposition'] == 'generation_failed' else 'extraction_completed'
        elif q and quality_mode == 'enforce':
            status = 'quality_failed' if q['status'] == 'failed' else 'quality_routed_without_extraction'
        else:
            status = 'extraction_pending'
        result.append({'comment_id': cid, 'language': lang, 'status': status,
            'relevance': 'admitted' if d and d['agreement'] else 'not_admitted',
            'quality_status': q['status'] if q else 'not_assessed' if quality_mode == 'off' else 'pending' if d and d['agreement'] else 'not_applicable',
            'routes_present': q['routes_present'] if q else [],
            'extraction': e, 'audited_accepted_claims': sum(c['comment_id'] == cid for c in accepted),
            'quarantined_claims': sum(c['comment_id'] == cid for c in quarantine),
            'source_review': 'pending_external_review' if any(c['comment_id'] == cid for c in accepted) else 'not_applicable'})
    return result


def validate_modes(args):
    mode = getattr(args, 'evidence_quality', 'off')
    if getattr(args, 'relevance_only', False) and (mode != 'off' or getattr(args, 'quality_only', False)):
        raise ValueError('--relevance-only requires --evidence-quality off and cannot use --quality-only')
    if getattr(args, 'quality_only', False) and mode == 'off':
        raise ValueError('--quality-only requires --evidence-quality shadow or enforce')
    return mode


@dataclass
class RunState:
    """The inputs, the runner and the accumulated results that the stages of one run share."""
    args: object
    rows: list
    models: list
    quality_identity: object
    quality_policy: object
    identity: dict
    folder: object
    routes: dict
    quality_mode: str
    by_id: dict = None
    eligible: list = None
    runner: object = None
    decisions: dict = None
    characters: set = None
    quality_records: dict = field(default_factory=dict)
    trace: list = field(default_factory=list)
    claims: list = field(default_factory=list)
    quarantine: list = field(default_factory=list)
    coverage: list = field(default_factory=list)


def triage(state, retrieval):
    """Start one relevance decision per retrieved comment and triage it by its retrieval scores."""
    state.decisions = {d['comment_id']: {**d, 'model_related': None, 'agreement': False} for d in retrieval}
    for decision in state.decisions.values():
        status, reasons = triage_retrieval(decision, state.by_id[decision['comment_id']]['text_original'],
                                           load_policy()['retrieval_borderline_margin'])
        decision.update(retrieval_triage=status, retrieval_triage_reasons=reasons)


def review_retrieval(state, model, language, language_rows):
    """Review the borderline comments queued by triage, rechecking failed or uncertain batch items alone."""
    queued = [d for d in language_rows if d['retrieval_triage'] == 'review_queue']
    cached = state.runner.cached_single_ids(model, language, 'retrieval_review')
    review_batches = [[d] for d in queued if d['comment_id'] in cached]
    review_batches += list(batches([d for d in queued if d['comment_id'] not in cached], count=8, chars=10000))
    for batch in review_batches:
        data = {'comments': [{'comment_id': d['comment_id'], 'text': state.by_id[d['comment_id']]['text_original'],
                              'retrieved_topics': d['references']} for d in batch]}
        parsed, meta = state.runner.generate(model, language, 'retrieval_review', data, [d['comment_id'] for d in batch])
        state.trace.append({'model': model, 'stage': 'retrieval_review', **meta})
        reviewed = {d['comment_id']: d for d in parsed['decisions']} if parsed else {}
        for decision in batch:
            item = reviewed.get(decision['comment_id'], {})
            decision.update(retrieval_review_related=item.get('related'),
                            retrieval_review_uncertain=item.get('uncertain', True),
                            initial_retrieval_review_related=item.get('related'),
                            initial_retrieval_review_uncertain=item.get('uncertain', True))
            if len(batch) > 1 and (item.get('related') is not True or item.get('uncertain') is not False):
                record_id = decision['comment_id']
                single = {'comments': [{'comment_id': record_id, 'text': state.by_id[record_id]['text_original'],
                                        'retrieved_topics': decision['references']}]}
                retry, meta = state.runner.generate(model, language, 'retrieval_review', single, [record_id])
                state.trace.append({'model': model, 'stage': 'retrieval_review', 'refinement': True, **meta})
                result = retry['decisions'][0] if retry else {}
                decision.update(retrieval_review_related=result.get('related'),
                                retrieval_review_uncertain=result.get('uncertain', True))


def admit_relevance(state, model, language, language_rows):
    """Check relevance in batches, recheck each disagreement alone, then write relevance.json and review-queue.json."""
    candidates = [d for d in language_rows if d['retrieval_related'] or (
        d.get('retrieval_review_related') is True and d.get('retrieval_review_uncertain') is False)]
    for batch in batches(candidates, count=8, chars=10000):
        data = {'comments': [{'comment_id': d['comment_id'],
            'text': state.by_id[d['comment_id']]['text_original'], 'retrieved_topics': d['references']} for d in batch]}
        parsed, meta = state.runner.generate(model, language, 'relevance', data, [d['comment_id'] for d in batch])
        state.trace.append({'model': model, 'stage': 'relevance', **meta})
        if parsed:
            for item in parsed['decisions']:
                state.decisions[item['comment_id']].update(model_related=item['related'],
                    model_uncertain=item['uncertain'], model_reason=item['reason'],
                    agreement=relevance_agrees(state.decisions[item['comment_id']], item))
    # Recheck every rejection alone: short ordered arrays can still drift
    # semantically across comments. Preserve the initial result for review.
    for decision in candidates:
        decision['initial_model_related'] = decision['model_related']
        decision['initial_model_uncertain'] = decision.get('model_uncertain')
        decision['refinement_performed'] = False
        if decision['agreement']:
            continue
        decision['refinement_performed'] = True
        record_id = decision['comment_id']
        data = {'comments': [{'comment_id': record_id, 'text': state.by_id[record_id]['text_original'],
                              'retrieved_topics': decision['references']}]}
        parsed, meta = state.runner.generate(model, language, 'relevance', data, [record_id])
        state.trace.append({'model': model, 'stage': 'relevance_refinement', **meta})
        if parsed:
            item = parsed['decisions'][0]
            decision.update(model_related=item['related'], model_uncertain=item['uncertain'],
                model_reason=item['reason'], agreement=relevance_agrees(decision, item))
    write_json(state.folder / 'relevance.json', list(state.decisions.values()))
    write_json(state.folder / 'review-queue.json', [d for d in state.decisions.values()
               if d['retrieval_triage'] == 'review_queue' and not d['agreement']])


def assess_quality(state, model, language, selected):
    """Annotate the evidence quality of each admitted comment and write the quality progress after each record."""
    for row in selected:
        record_id = row['record_id']
        units = evidence_units(row['text_original'])
        attempts = []
        result = None
        for attempt in range(state.quality_policy['max_attempts']):
            data = {'comments': [{'comment_id': record_id, 'units': units}],
                'source': row, 'language': language,
                'character_normalization_reference': character_reference(row['text_original']),
                'quality_contract': state.quality_identity, 'attempt': attempt + 1}
            # A retry is a new request/cache identity. Failed cached
            # attempt 1 cannot masquerade as a fresh attempt 2.
            parsed, meta = state.runner.generate(model, language, 'quality', data, [record_id])
            state.trace.append({'model': model, 'stage': 'quality', 'comment_id': record_id,
                                'attempt': attempt + 1, **meta})
            if parsed is not None:
                result = quality.qualify(parsed, row, units, state.quality_policy)
                if result['errors']:
                    meta = {**meta, 'errors': result['errors']}
                else:
                    attempts.append(meta)
                    break
            attempts.append(meta)
            result = None
        record = result or quality.failed_record(row, units, attempts, state.quality_policy)
        record.update(attempts=attempts, model=model, observation_only=state.quality_mode == 'shadow')
        state.quality_records[record_id] = record
        write_json(state.folder / 'evidence-quality.json', list(state.quality_records.values()))
        write_json(state.folder / 'full-pipeline-coverage.json', build_full_coverage(
            state.rows, state.decisions, state.routes, state.models, state.quality_records, state.coverage, [],
            state.quarantine, state.quality_mode, state.args))
        write_json(state.folder / 'request-trace.json', state.trace)


def extract_claims(state, model, language, selected):
    """Extract claims and bind them to their sources, splitting failed batches; write the progress after each batch."""
    # Evidence units contain the entire original text in order. Do not send
    # a second copy of the full text, which wastes context and GPU memory.
    prepared = [{'comment_id': r['record_id'], 'units': evidence_units(r['text_original'])}
                for r in selected]
    if state.quality_mode == 'enforce':
        prepared = [{**r, 'allowed_quality_points': quality.allowed_points(state.quality_records[r['comment_id']])}
                    for r in prepared if quality.allowed_points(state.quality_records[r['comment_id']])]
    extraction_queue = list(batches(prepared, count=4, chars=9000 if language == 'en' else 4000))
    while extraction_queue:
        batch = extraction_queue.pop(0)
        parsed, meta = state.runner.generate(model, language, 'extract',
            {'comments': batch, 'character_normalization_reference': character_reference('\n'.join(state.by_id[r['comment_id']]['text_original'] for r in batch))},
            [r['comment_id'] for r in batch])
        state.trace.append({'model': model, 'stage': 'extract', **meta})
        if not parsed:
            if len(batch) > 1:
                extraction_queue[0:0] = [[item] for item in batch]
                continue
            state.coverage.extend({'comment_id': r['comment_id'], 'model': model,
                                   'disposition': 'generation_failed', 'claims_generated': 0} for r in batch)
            continue
        for assessment in parsed['assessments']:
            record_id = assessment['comment_id']
            state.coverage.append({'comment_id': record_id, 'model': model,
                'disposition': assessment['disposition'], 'claims_generated': len(assessment['claims'])})
            consistent = (assessment['disposition'] == 'extracted') == bool(assessment['claims'])
            for i, claim in enumerate(assessment['claims']):
                errors, enriched = ground_claim(claim, state.by_id[record_id], state.characters)
                if state.quality_mode == 'enforce':
                    quality_errors, qualification = quality.bind_claim(claim, state.quality_records[record_id],
                        character_reference(state.by_id[record_id]['text_original']))
                    errors.extend(quality_errors)
                    if enriched is not None:
                        enriched['evidence_quality'] = qualification
                if not consistent:
                    errors.append('Disposition and claims disagree')
                envelope = {'claim_id': record_id + ':' + str(i + 1), 'comment_id': record_id,
                            'model': model, 'claim': enriched or claim}
                if errors:
                    state.quarantine.append({**envelope, 'stage': 'source_binding', 'errors': errors})
                else:
                    state.claims.append(envelope)
        write_json(state.folder / 'extraction-coverage.json', state.coverage)
        write_json(state.folder / 'claims-before-audit.json', state.claims)
        write_json(state.folder / 'quarantined-claims.json', state.quarantine)


def audit_claims(state, model, language):
    """Audit each claim of the model alone and quarantine unsupported ones; write the progress after each audit."""
    # Audit in a separate context, with original spans, never the generator's rationale.
    pending = [c for c in state.claims if c['model'] == model]
    for batch in batches(pending, count=1):
        parsed, meta = state.runner.generate(model, language, 'verify',
            {'claims': batch, 'original_comment': state.by_id[batch[0]['comment_id']]['text_original']},
                                             [c['claim_id'] for c in batch])
        state.trace.append({'model': model, 'stage': 'verify', **meta})
        verdicts = {v['claim_id']: v for v in parsed['verdicts']} if parsed else {}
        for entry in batch:
            verdict = verdicts.get(entry['claim_id'])
            entry['audit'] = verdict
            if verdict is None or not verdict['supported']:
                state.quarantine.append({**entry, 'stage': 'semantic_audit',
                    'errors': [verdict['reason'] if verdict else 'Audit failed; fail closed']})
        write_json(state.folder / 'audit-progress.json', state.claims)
        write_json(state.folder / 'quarantined-claims.json', state.quarantine)


def summarize(state, accepted):
    """Return the run summary: counts per stage and language, and the limitations of the method."""
    return {'version': VERSION, 'input_comments': len(state.rows),
        'mode': state.identity['mode'],
        'input_languages': dict(Counter(r['language'] for r in state.rows)),
        'routed_comments': len(state.eligible), 'unsupported_or_unselected_language': len(state.rows) - len(state.eligible),
        'retrieval_related': sum(d['retrieval_related'] for d in state.decisions.values()),
        'retrieval_review_queued': sum(d['retrieval_triage'] == 'review_queue' for d in state.decisions.values()),
        'retrieval_review_rescues': sum(d['agreement'] and not d['retrieval_related'] for d in state.decisions.values()),
        'agreement_related': sum(d['agreement'] for d in state.decisions.values()),
        'relevance_refinements': sum(d.get('refinement_performed', False) for d in state.decisions.values()),
        'relevance_refinement_rescues': sum(d.get('refinement_performed', False) and d['agreement'] for d in state.decisions.values()),
        'assessed_comments': len(state.coverage), 'generated_claims': sum(c['claims_generated'] for c in state.coverage),
        'accepted_claims': len(accepted), 'quarantined_claims': len(state.quarantine),
        'source_numeric_accepted': sum(c['specificity'] == 'source_numeric' for c in accepted),
        'qualitative_only_accepted': sum(c['specificity'] == 'qualitative_only' for c in accepted),
        'failed_requests': sum(bool(t['errors']) for t in state.trace),
        'final_generation_failed_comments': sum(c['disposition'] == 'generation_failed' for c in state.coverage),
        'by_language': {lang: {'input': sum(r['language'] == lang for r in state.rows),
            'retrieval_related': sum(d['language'] == lang and d['retrieval_related'] for d in state.decisions.values()),
            'agreement_related': sum(d['language'] == lang and d['agreement'] for d in state.decisions.values()),
            'accepted_claims': sum(state.by_id[c['comment_id']]['language'] == lang for c in accepted)} for lang in ('en', 'zh')},
        'limitations': ['Automated semantic audit uses the same language-routed model in a separate context; not human ground truth.',
            'Retrieval prototypes and threshold are reused from the earlier experiment; no held-out relevance labels exist for the full corpus.',
            'Source binding proves quotation provenance, not gameplay truth or patch applicability.',
            'Semantic audit reads the full original comment; selected citations can still need additional context.',
            'Coverage accounts for every admitted comment; completeness of individual concerns still requires human review.',
            'No numerical targets are invented; qualitative comments cannot supply exact engineering values.']}


def report_quality(state, accepted, report):
    """Write the shadow or enforce quality artifacts and add them to the report."""
    records = list(state.quality_records.values())
    routed = [{**r, 'source_url': q['source_url'], 'content_sha256': q['content_sha256'],
               'quality_status': q['status'], 'language': q['language'], 'model': q.get('model'),
               'policy_version': q['policy_version'], 'errors': q['errors'],
               'quality_request_ids': [a['request_id'] for a in q.get('attempts', [])],
               'observation_only': state.quality_mode == 'shadow'}
              for q in records for r in q['routing']]
    opinions = quality.summarize_opinions(records, character_reference('\n'.join(r['text_original'] for r in state.rows)))
    systems = [r for r in routed if r['route'] == 'system_evidence']
    review = [r for r in routed if r['route'] == 'review']
    exclusions = [r for r in routed if r['route'] == 'exclude']
    quality_summary = {'mode': state.quality_mode, 'comments_assessed': len(records),
        'completed': sum(q['status'] == 'completed' for q in records),
        'failed': sum(q['status'] == 'failed' for q in records),
        'route_comment_counts': {route: len({r['comment_id'] for r in routed if r['route'] == route}) for route in quality.ROUTES},
        'route_item_counts': dict(Counter(r['route'] for r in routed)),
        'counting_note': 'Mixed comments overlap across routes; never sum groups as players.',
        'source_counts': quality_source_counts(records, accepted),
        'accuracy_validation': 'not_established; deterministic checks are not semantic accuracy'}
    for name, value in [('evidence-quality', records), ('quality-routing', routed),
            ('quality-review-queue', review), ('quality-summary', quality_summary),
            ('opinion-summary', opinions), ('system-feedback', systems), ('quality-exclusions', exclusions)]:
        write_json(state.folder / (name + '.json'), value)
    if state.quality_mode == 'enforce':
        report.update(opinion_summary=opinions, system_feedback=systems,
                      quality_review_queue=review, quality_exclusions=exclusions)
    else:
        report['quality_observation_artifacts'] = ['quality-summary.json', 'opinion-summary.json', 'system-feedback.json']


def assemble(state, log=None):
    """Build the summary and the report, write the final artifacts, log the summary text and return the report."""
    accepted = [{**e['claim'], 'claim_id': e['claim_id'], 'comment_id': e['comment_id'],
                 'model': e['model'], 'semantic_audit': e['audit']} for e in state.claims
                if (e.get('audit') or {}).get('supported')]
    summary = summarize(state, accepted)
    unsupported = [{'comment_id': r['record_id'], 'language': r['language'],
                    'reason': 'No configured language route'} for r in state.rows if r not in state.eligible]
    report = {'summary': summary, 'character_adjustments': aggregate(accepted, state.quality_mode == 'enforce'),
        'release_status': 'requires_source_review_and_versioned_game_data',
        'unresolved_identity_claims': [c for c in accepted if c.get('character_identity', {}).get('normalization_status') == 'source_literal_unverified'],
        'other_supported_claims': [c for c in accepted if c['character'] is None or c['direction'] not in ('buff', 'nerf')],
        'coverage': state.coverage, 'unsupported_languages': unsupported}
    report['report_schema_version'] = 'balance-report-v3' if state.quality_mode == 'enforce' else VERSION
    report['evidence_quality_mode'] = state.quality_mode
    report['quality_assessment'] = 'enforced' if state.quality_mode == 'enforce' else 'observation_only' if state.quality_mode == 'shadow' else 'quality_not_assessed'
    full_coverage = build_full_coverage(state.rows, state.decisions, state.routes, state.models, state.quality_records,
                                        state.coverage, accepted, state.quarantine, state.quality_mode, state.args)
    write_json(state.folder / 'full-pipeline-coverage.json', full_coverage)
    report['full_pipeline_coverage'] = full_coverage
    if state.quality_mode != 'off':
        report_quality(state, accepted, report)
    write_json(state.folder / 'relevance.json', list(state.decisions.values()))
    write_json(state.folder / 'validated-claims.json', accepted)
    write_json(state.folder / 'quarantined-claims.json', state.quarantine)
    write_json(state.folder / 'request-trace.json', state.trace)
    write_json(state.folder / 'summary.json', summary)
    write_json(state.folder / 'balance-report.json', report)
    if log is not None:
        log(json.dumps(summary, ensure_ascii=False, indent=2))
    return report


def process(args, rows, routing, models, prompts, quality_identity, quality_policy,
            identity, embedding_config=None, runner_factory=Runner, retrieval_service=retrieve, log=None):
    """Shared orchestration with explicit inputs and injected inference boundaries; log receives the summary text."""
    state = RunState(args, rows, models, quality_identity, quality_policy, identity,
                     folder=args.out.resolve(), routes=routing['models'], quality_mode=args.evidence_quality)
    state.by_id = {r['record_id']: r for r in state.rows}
    state.eligible = [r for r in state.rows if any(state.routes[m]['language'] == r['language'] for m in state.models)]
    retrieval = retrieval_service(state.eligible, state.args.base_url, state.folder, state.args.embedding_model,
                                  embedding_config)
    state.runner = runner_factory(state.args.base_url, state.folder, prompts, state.quality_identity,
                                  state.quality_policy)
    state.runner.runtime_options = state.identity.get('runtime_options', {})
    triage(state, retrieval)
    reference = character_reference()
    state.characters = {e['canonical_name'] for e in reference}
    for model in state.models:
        language = state.routes[model]['language']
        language_rows = [d for d in state.decisions.values() if d['language'] == language]
        review_retrieval(state, model, language, language_rows)
        admit_relevance(state, model, language, language_rows)
        if getattr(state.args, 'relevance_only', False):
            continue
        selected = [state.by_id[d['comment_id']] for d in state.decisions.values()
                    if d['language'] == language and d['agreement']]
        write_json(state.folder / 'full-pipeline-coverage.json', build_full_coverage(
            state.rows, state.decisions, state.routes, state.models, state.quality_records, state.coverage, [],
            state.quarantine, state.quality_mode, state.args))
        if state.quality_mode != 'off':
            assess_quality(state, model, language, selected)
            if getattr(state.args, 'quality_only', False):
                continue
        extract_claims(state, model, language, selected)
        audit_claims(state, model, language)
    return assemble(state, log)
