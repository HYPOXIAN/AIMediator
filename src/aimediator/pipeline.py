"""Shared analysis orchestration: relevance, evidence quality, extraction, source audit and report."""
from collections import Counter
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


def process(args, rows, routing, models, prompts, quality_identity, quality_policy,
            identity, embedding_config=None, runner_factory=Runner, retrieval_service=retrieve):
    """Shared orchestration with explicit inputs and injected inference boundaries."""
    folder, routes = args.out.resolve(), routing['models']
    quality_mode = args.evidence_quality
    by_id = {r['record_id']: r for r in rows}
    eligible = [r for r in rows if any(routes[m]['language'] == r['language'] for m in models)]
    retrieval = retrieval_service(eligible, args.base_url, folder, args.embedding_model, embedding_config)
    runner = runner_factory(args.base_url, folder, prompts, quality_identity, quality_policy)
    runner.runtime_options = identity.get('runtime_options', {})
    quality_records = {}
    trace, claims, quarantine, coverage = [], [], [], []
    decisions = {d['comment_id']: {**d, 'model_related': None, 'agreement': False} for d in retrieval}
    for decision in decisions.values():
        status, reasons = triage_retrieval(decision, by_id[decision['comment_id']]['text_original'],
                                           load_policy()['retrieval_borderline_margin'])
        decision.update(retrieval_triage=status, retrieval_triage_reasons=reasons)
    reference = character_reference()
    characters = {e['canonical_name'] for e in reference}
    for model in models:
        language = routes[model]['language']
        language_rows = [d for d in decisions.values() if d['language'] == language]
        queued = [d for d in language_rows if d['retrieval_triage'] == 'review_queue']
        cached = runner.cached_single_ids(model, language, 'retrieval_review')
        review_batches = [[d] for d in queued if d['comment_id'] in cached]
        review_batches += list(batches([d for d in queued if d['comment_id'] not in cached], count=8, chars=10000))
        for batch in review_batches:
            data = {'comments': [{'comment_id': d['comment_id'], 'text': by_id[d['comment_id']]['text_original'],
                                  'retrieved_topics': d['references']} for d in batch]}
            parsed, meta = runner.generate(model, language, 'retrieval_review', data, [d['comment_id'] for d in batch])
            trace.append({'model': model, 'stage': 'retrieval_review', **meta})
            reviewed = {d['comment_id']: d for d in parsed['decisions']} if parsed else {}
            for decision in batch:
                item = reviewed.get(decision['comment_id'], {})
                decision.update(retrieval_review_related=item.get('related'),
                                retrieval_review_uncertain=item.get('uncertain', True),
                                initial_retrieval_review_related=item.get('related'),
                                initial_retrieval_review_uncertain=item.get('uncertain', True))
                if len(batch) > 1 and (item.get('related') is not True or item.get('uncertain') is not False):
                    record_id = decision['comment_id']
                    single = {'comments': [{'comment_id': record_id, 'text': by_id[record_id]['text_original'],
                                            'retrieved_topics': decision['references']}]}
                    retry, meta = runner.generate(model, language, 'retrieval_review', single, [record_id])
                    trace.append({'model': model, 'stage': 'retrieval_review', 'refinement': True, **meta})
                    result = retry['decisions'][0] if retry else {}
                    decision.update(retrieval_review_related=result.get('related'),
                                    retrieval_review_uncertain=result.get('uncertain', True))
        candidates = [d for d in language_rows if d['retrieval_related'] or (
            d.get('retrieval_review_related') is True and d.get('retrieval_review_uncertain') is False)]
        for batch in batches(candidates, count=8, chars=10000):
            data = {'comments': [{'comment_id': d['comment_id'],
                'text': by_id[d['comment_id']]['text_original'], 'retrieved_topics': d['references']} for d in batch]}
            parsed, meta = runner.generate(model, language, 'relevance', data, [d['comment_id'] for d in batch])
            trace.append({'model': model, 'stage': 'relevance', **meta})
            if parsed:
                for item in parsed['decisions']:
                    decisions[item['comment_id']].update(model_related=item['related'],
                        model_uncertain=item['uncertain'], model_reason=item['reason'],
                        agreement=relevance_agrees(decisions[item['comment_id']], item))
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
            data = {'comments': [{'comment_id': record_id, 'text': by_id[record_id]['text_original'],
                                  'retrieved_topics': decision['references']}]}
            parsed, meta = runner.generate(model, language, 'relevance', data, [record_id])
            trace.append({'model': model, 'stage': 'relevance_refinement', **meta})
            if parsed:
                item = parsed['decisions'][0]
                decision.update(model_related=item['related'], model_uncertain=item['uncertain'],
                    model_reason=item['reason'], agreement=relevance_agrees(decision, item))
        write_json(folder / 'relevance.json', list(decisions.values()))
        write_json(folder / 'review-queue.json', [d for d in decisions.values()
                   if d['retrieval_triage'] == 'review_queue' and not d['agreement']])
        if getattr(args, 'relevance_only', False):
            continue
        selected = [by_id[d['comment_id']] for d in decisions.values()
                    if d['language'] == language and d['agreement']]
        # Evidence units contain the entire original text in order. Do not send
        # a second copy of the full text, which wastes context and GPU memory.
        write_json(folder / 'full-pipeline-coverage.json', build_full_coverage(rows, decisions, routes, models, quality_records, coverage, [], quarantine, quality_mode, args))
        if quality_mode != 'off':
            for row in selected:
                record_id = row['record_id']
                units = evidence_units(row['text_original'])
                attempts = []
                result = None
                for attempt in range(quality_policy['max_attempts']):
                    data = {'comments': [{'comment_id': record_id, 'units': units}],
                        'source': row, 'language': language,
                        'character_normalization_reference': character_reference(row['text_original']),
                        'quality_contract': quality_identity, 'attempt': attempt + 1}
                    # A retry is a new request/cache identity. Failed cached
                    # attempt 1 cannot masquerade as a fresh attempt 2.
                    parsed, meta = runner.generate(model, language, 'quality', data, [record_id])
                    trace.append({'model': model, 'stage': 'quality', 'comment_id': record_id,
                                  'attempt': attempt + 1, **meta})
                    if parsed is not None:
                        result = quality.qualify(parsed, row, units, quality_policy)
                        if result['errors']:
                            meta = {**meta, 'errors': result['errors']}
                        else:
                            attempts.append(meta)
                            break
                    attempts.append(meta)
                    result = None
                record = result or quality.failed_record(row, units, attempts, quality_policy)
                record.update(attempts=attempts, model=model, observation_only=quality_mode == 'shadow')
                quality_records[record_id] = record
                write_json(folder / 'evidence-quality.json', list(quality_records.values()))
                write_json(folder / 'full-pipeline-coverage.json', build_full_coverage(rows, decisions, routes, models, quality_records, coverage, [], quarantine, quality_mode, args))
                write_json(folder / 'request-trace.json', trace)
            if getattr(args, 'quality_only', False):
                continue
        prepared = [{'comment_id': r['record_id'], 'units': evidence_units(r['text_original'])}
                    for r in selected]
        if quality_mode == 'enforce':
            prepared = [{**r, 'allowed_quality_points': quality.allowed_points(quality_records[r['comment_id']])}
                        for r in prepared if quality.allowed_points(quality_records[r['comment_id']])]
        extraction_queue = list(batches(prepared, count=4, chars=9000 if language == 'en' else 4000))
        while extraction_queue:
            batch = extraction_queue.pop(0)
            parsed, meta = runner.generate(model, language, 'extract',
                {'comments': batch, 'character_normalization_reference': character_reference('\n'.join(by_id[r['comment_id']]['text_original'] for r in batch))},
                [r['comment_id'] for r in batch])
            trace.append({'model': model, 'stage': 'extract', **meta})
            if not parsed:
                if len(batch) > 1:
                    extraction_queue[0:0] = [[item] for item in batch]
                    continue
                coverage.extend({'comment_id': r['comment_id'], 'model': model,
                                 'disposition': 'generation_failed', 'claims_generated': 0} for r in batch)
                continue
            for assessment in parsed['assessments']:
                record_id = assessment['comment_id']
                coverage.append({'comment_id': record_id, 'model': model,
                    'disposition': assessment['disposition'], 'claims_generated': len(assessment['claims'])})
                consistent = (assessment['disposition'] == 'extracted') == bool(assessment['claims'])
                for i, claim in enumerate(assessment['claims']):
                    errors, enriched = ground_claim(claim, by_id[record_id], characters)
                    if quality_mode == 'enforce':
                        quality_errors, qualification = quality.bind_claim(claim, quality_records[record_id],
                            character_reference(by_id[record_id]['text_original']))
                        errors.extend(quality_errors)
                        if enriched is not None:
                            enriched['evidence_quality'] = qualification
                    if not consistent:
                        errors.append('Disposition and claims disagree')
                    envelope = {'claim_id': record_id + ':' + str(i + 1), 'comment_id': record_id,
                                'model': model, 'claim': enriched or claim}
                    if errors:
                        quarantine.append({**envelope, 'stage': 'source_binding', 'errors': errors})
                    else:
                        claims.append(envelope)
            write_json(folder / 'extraction-coverage.json', coverage)
            write_json(folder / 'claims-before-audit.json', claims)
            write_json(folder / 'quarantined-claims.json', quarantine)
        # Audit in a separate context, with original spans, never the generator's rationale.
        pending = [c for c in claims if c['model'] == model]
        for batch in batches(pending, count=1):
            parsed, meta = runner.generate(model, language, 'verify',
                {'claims': batch, 'original_comment': by_id[batch[0]['comment_id']]['text_original']},
                                           [c['claim_id'] for c in batch])
            trace.append({'model': model, 'stage': 'verify', **meta})
            verdicts = {v['claim_id']: v for v in parsed['verdicts']} if parsed else {}
            for entry in batch:
                verdict = verdicts.get(entry['claim_id'])
                entry['audit'] = verdict
                if verdict is None or not verdict['supported']:
                    quarantine.append({**entry, 'stage': 'semantic_audit',
                        'errors': [verdict['reason'] if verdict else 'Audit failed; fail closed']})
            write_json(folder / 'audit-progress.json', claims)
            write_json(folder / 'quarantined-claims.json', quarantine)
    accepted = [{**e['claim'], 'claim_id': e['claim_id'], 'comment_id': e['comment_id'],
                 'model': e['model'], 'semantic_audit': e['audit']} for e in claims
                if (e.get('audit') or {}).get('supported')]
    summary = {'version': VERSION, 'input_comments': len(rows),
        'mode': identity['mode'],
        'input_languages': dict(Counter(r['language'] for r in rows)),
        'routed_comments': len(eligible), 'unsupported_or_unselected_language': len(rows) - len(eligible),
        'retrieval_related': sum(d['retrieval_related'] for d in decisions.values()),
        'retrieval_review_queued': sum(d['retrieval_triage'] == 'review_queue' for d in decisions.values()),
        'retrieval_review_rescues': sum(d['agreement'] and not d['retrieval_related'] for d in decisions.values()),
        'agreement_related': sum(d['agreement'] for d in decisions.values()),
        'relevance_refinements': sum(d.get('refinement_performed', False) for d in decisions.values()),
        'relevance_refinement_rescues': sum(d.get('refinement_performed', False) and d['agreement'] for d in decisions.values()),
        'assessed_comments': len(coverage), 'generated_claims': sum(c['claims_generated'] for c in coverage),
        'accepted_claims': len(accepted), 'quarantined_claims': len(quarantine),
        'source_numeric_accepted': sum(c['specificity'] == 'source_numeric' for c in accepted),
        'qualitative_only_accepted': sum(c['specificity'] == 'qualitative_only' for c in accepted),
        'failed_requests': sum(bool(t['errors']) for t in trace),
        'final_generation_failed_comments': sum(c['disposition'] == 'generation_failed' for c in coverage),
        'by_language': {lang: {'input': sum(r['language'] == lang for r in rows),
            'retrieval_related': sum(d['language'] == lang and d['retrieval_related'] for d in decisions.values()),
            'agreement_related': sum(d['language'] == lang and d['agreement'] for d in decisions.values()),
            'accepted_claims': sum(by_id[c['comment_id']]['language'] == lang for c in accepted)} for lang in ('en', 'zh')},
        'limitations': ['Automated semantic audit uses the same language-routed model in a separate context; not human ground truth.',
            'Retrieval prototypes and threshold are reused from the earlier experiment; no held-out relevance labels exist for the full corpus.',
            'Source binding proves quotation provenance, not gameplay truth or patch applicability.',
            'Semantic audit reads the full original comment; selected citations can still need additional context.',
            'Coverage accounts for every admitted comment; completeness of individual concerns still requires human review.',
            'No numerical targets are invented; qualitative comments cannot supply exact engineering values.']}
    unsupported = [{'comment_id': r['record_id'], 'language': r['language'],
                    'reason': 'No configured language route'} for r in rows if r not in eligible]
    report = {'summary': summary, 'character_adjustments': aggregate(accepted, quality_mode == 'enforce'),
        'release_status': 'requires_source_review_and_versioned_game_data',
        'unresolved_identity_claims': [c for c in accepted if c.get('character_identity', {}).get('normalization_status') == 'source_literal_unverified'],
        'other_supported_claims': [c for c in accepted if c['character'] is None or c['direction'] not in ('buff', 'nerf')],
        'coverage': coverage, 'unsupported_languages': unsupported}
    report['report_schema_version'] = 'balance-report-v3' if quality_mode == 'enforce' else VERSION
    report['evidence_quality_mode'] = quality_mode
    report['quality_assessment'] = 'enforced' if quality_mode == 'enforce' else 'observation_only' if quality_mode == 'shadow' else 'quality_not_assessed'
    full_coverage = build_full_coverage(rows, decisions, routes, models, quality_records, coverage,
                                        accepted, quarantine, quality_mode, args)
    write_json(folder / 'full-pipeline-coverage.json', full_coverage)
    report['full_pipeline_coverage'] = full_coverage
    if quality_mode != 'off':
        records = list(quality_records.values())
        routed = [{**r, 'source_url': q['source_url'], 'content_sha256': q['content_sha256'],
                   'quality_status': q['status'], 'language': q['language'], 'model': q.get('model'),
                   'policy_version': q['policy_version'], 'errors': q['errors'],
                   'quality_request_ids': [a['request_id'] for a in q.get('attempts', [])],
                   'observation_only': quality_mode == 'shadow'}
                  for q in records for r in q['routing']]
        opinions = quality.summarize_opinions(records, character_reference('\n'.join(r['text_original'] for r in rows)))
        systems = [r for r in routed if r['route'] == 'system_evidence']
        review = [r for r in routed if r['route'] == 'review']
        exclusions = [r for r in routed if r['route'] == 'exclude']
        quality_summary = {'mode': quality_mode, 'comments_assessed': len(records),
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
            write_json(folder / (name + '.json'), value)
        if quality_mode == 'enforce':
            report.update(opinion_summary=opinions, system_feedback=systems,
                          quality_review_queue=review, quality_exclusions=exclusions)
        else:
            report['quality_observation_artifacts'] = ['quality-summary.json', 'opinion-summary.json', 'system-feedback.json']
    write_json(folder / 'relevance.json', list(decisions.values()))
    write_json(folder / 'validated-claims.json', accepted)
    write_json(folder / 'quarantined-claims.json', quarantine)
    write_json(folder / 'request-trace.json', trace)
    write_json(folder / 'summary.json', summary)
    write_json(folder / 'balance-report.json', report)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return report
