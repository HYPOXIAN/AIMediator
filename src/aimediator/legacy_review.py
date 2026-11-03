"""Apply an explicit agent/human source review without overwriting model results.

Reviewers may clarify wording and add original context. A direction correction
requires its own explicit field and is labeled; identities cannot change. Every complete proposal needs a
fingerprinted decision. This is a source review, not verification of game facts.
"""
import argparse
import copy
import json
from . import evidence_quality as quality
from pathlib import Path
from .engine import (CLAIM, ROOT, aggregate, digest, ground_claim,
                                 schema_errors, strict_json, write_json, character_reference)


def proposal_hash(claim):
    fields = {key: claim[key] for key in CLAIM['properties']}
    if 'evidence_quality' in claim or 'quality_point_ids' in claim:
        fields['evidence_quality'] = claim.get('evidence_quality')
        fields['quality_point_ids'] = claim.get('quality_point_ids')
    return digest(json.dumps(fields, sort_keys=True, ensure_ascii=False).encode())


def apply_review(proposals, decisions, sources, admitted, characters):
    if set(proposals) != set(decisions):
        raise ValueError('Every complete proposal must have exactly one review decision')
    accepted, excluded = [], []
    allowed = {'decision', 'reason', 'proposal_sha256', 'evidence_ids', 'target', 'recommendation', 'corrected_direction'}
    for identity, envelope in proposals.items():
        decision = decisions[identity]
        if set(decision) - allowed or not {'decision', 'reason', 'proposal_sha256'} <= set(decision):
            raise ValueError('Unexpected or missing review fields: ' + identity)
        if (decision['decision'] not in ('accept', 'reject', 'uncertain')
                or not isinstance(decision['reason'], str) or not decision['reason']):
            raise ValueError('Invalid review decision: ' + identity)
        original = envelope['claim']
        if decision['proposal_sha256'] != proposal_hash(original):
            raise ValueError('Reviewed proposal changed: ' + identity)
        record_id = envelope['comment_id']
        if record_id not in admitted or record_id not in sources:
            raise ValueError('Unadmitted or nonexistent original comment: ' + identity)
        if decision['decision'] != 'accept':
            excluded.append({'claim_id': identity, 'comment_id': record_id,
                'decision': decision['decision'], 'reason': decision['reason'], 'original_model_claim': original})
            continue
        claim = {key: copy.deepcopy(original[key]) for key in CLAIM['properties']}
        for key in ('evidence_ids', 'target', 'recommendation'):
            if key in decision:
                claim[key] = copy.deepcopy(decision[key])
        if 'corrected_direction' in decision:
            claim['direction'] = decision['corrected_direction']
        errors = schema_errors(claim, CLAIM)
        if errors:
            raise ValueError('Reviewed claim has invalid structure: ' + identity)
        errors, enriched = ground_claim(claim, sources[record_id], characters)
        if errors:
            raise ValueError('Reviewed claim fails source binding: ' + identity + ': ' + '; '.join(errors))
        if 'evidence_quality' in original or 'quality_point_ids' in original:
            q = original.get('evidence_quality') or {}
            point_claim = {**claim, 'quality_point_ids': original.get('quality_point_ids', [])}
            record = {'schema_version': q.get('schema_version'), 'comment_id': record_id,
                      'content_sha256': q.get('content_sha256'), 'routing': [
                          {'point_id': p['point_id'], 'route': q.get('route'), 'point': p,
                           'segments': q.get('selected_segments', [])} for p in q.get('selected_points', [])]}
            binding_errors, qualification = quality.bind_claim(point_claim, record,
                character_reference(sources[record_id]['text_original']))
            if binding_errors:
                raise ValueError('Review cannot bypass evidence quality: ' + '; '.join(binding_errors))
            enriched['quality_point_ids'] = point_claim['quality_point_ids']
            enriched['evidence_quality'] = qualification
            changed = any(claim[k] != original[k] for k in CLAIM['properties'])
            enriched['semantic_audit'] = (original.get('semantic_audit') or envelope.get('audit')) if not changed else None
        accepted.append({**enriched, 'claim_id': identity, 'comment_id': record_id, 'model': envelope['model'],
            'source_review_required': False,
            'original_model_claim': {key: original[key] for key in CLAIM['properties']},
            'source_review': {'decision': 'accept', 'reason': decision['reason'],
                'context_changed': claim['evidence_ids'] != original['evidence_ids'],
                'direction_changed': claim['direction'] != original['direction'],
                'original_direction': original['direction'],
                'wording_changed': claim['recommendation'] != original['recommendation'] or claim['target'] != original['target']}})
    return accepted, excluded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--decisions', type=Path, required=True)
    args = parser.parse_args()
    folder = args.run
    raw = json.loads((folder / 'balance-report.json').read_text(encoding='utf-8'))
    sources = {r['record_id']: r for r in json.loads((folder / 'source-snapshot.json').read_text(encoding='utf-8'))}
    relevance = json.loads((folder / 'relevance.json').read_text(encoding='utf-8'))
    admitted = {r['comment_id'] for r in relevance if r['agreement']}
    proposals = {}
    for claim in json.loads((folder / 'validated-claims.json').read_text(encoding='utf-8')):
        proposals[claim['claim_id']] = {'comment_id': claim['comment_id'], 'model': claim['model'], 'claim': claim}
    for row in json.loads((folder / 'quarantined-claims.json').read_text(encoding='utf-8')):
        if row['claim_id'] in proposals:
            raise ValueError('Duplicate proposal identity')
        proposals[row['claim_id']] = row
    review = strict_json(args.decisions.read_text(encoding='utf-8'))
    if review.get('reviewer_type') not in ('agent', 'human'):
        raise ValueError('Review provenance must distinguish agent from human review')
    characters = {e['canonical_name'] for e in character_reference()}
    accepted, excluded = apply_review(proposals, review['decisions'], sources, admitted, characters)
    covered = {c['comment_id'] for c in accepted}
    coverage = {r['comment_id']: r for r in raw['coverage']}
    unassigned = [{'comment_id': identity, 'language': sources[identity]['language'],
        'status': coverage.get(identity, {}).get('disposition', 'quality_routed_without_extraction'), 'original_text': sources[identity]['text_original'],
        'source_url': sources[identity].get('source_url')}
        for identity in sorted(admitted - covered)]
    summary = {'reviewer_type': review['reviewer_type'], 'complete_proposals_reviewed': len(proposals),
        'accepted': len(accepted), 'rejected': sum(e['decision'] == 'reject' for e in excluded),
        'uncertain': sum(e['decision'] == 'uncertain' for e in excluded),
        'context_added_or_changed': sum(c['source_review']['context_changed'] for c in accepted),
        'explicit_direction_corrections': sum(c['source_review']['direction_changed'] for c in accepted),
        'source_numeric': sum(c['specificity'] == 'source_numeric' for c in accepted),
        'unverified_character_identity': sum(c.get('character_identity', {}).get('normalization_status') == 'source_literal_unverified' for c in accepted),
        'unassigned_comments': len(unassigned)}
    report = {'review_summary': summary, 'raw_model_summary': raw['summary'],
        'raw_model_report_sha256': digest((folder / 'balance-report.json').read_bytes()),
        'review_decisions_sha256': digest(args.decisions.read_bytes()),
        'character_adjustments': aggregate(accepted, raw.get('evidence_quality_mode') == 'enforce'),
        'evidence_quality_mode': raw.get('evidence_quality_mode', 'off'),
        'report_schema_version': raw.get('report_schema_version', 'legacy'),
        'unresolved_identity_claims': [c for c in accepted if c.get('character_identity', {}).get('normalization_status') == 'source_literal_unverified'],
        'other_supported_claims': [c for c in accepted if c['direction'] not in ('buff', 'nerf')],
        'unassigned_comments': unassigned,
        'limitations': ['Agent review is not independent human ground truth.',
            'Numerical targets are never supplied without a source request; game facts and patch applicability remain unverified.',
            'Original model results remain unchanged; context additions and wording refinements are labeled.']}
    write_json(folder / 'source-reviewed-claims.json', accepted)
    write_json(folder / 'source-review-exclusions.json', excluded)
    write_json(folder / 'source-reviewed-report.json', report)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
