"""Per-stage request data, options, response schemas, response normalization and item coverage checks."""
from __future__ import annotations

from collections import Counter
import copy
import re
from typing import Any

from . import evidence_quality as quality
from .balance_policy import attributed_candidates
from .evidence import CLAIM, character_candidates, character_reference, numeric_tokens
from .schema import arr, obj

# Pipeline upgrade plan 4.1 (LNK-01): per stage, the keys a request view may
# hold, at its top level and in each of its comments[] entries. Runner adds
# response_schema to the user message; everything else in the request data
# is program context that the model never sees.
MODEL_VISIBLE = {
    'relevance': {'top': frozenset({'comments'}),
                  'comments': frozenset({'comment_id', 'text', 'retrieved_topics'})},
    'retrieval_review': {'top': frozenset({'comments'}),
                         'comments': frozenset({'comment_id', 'text', 'retrieved_topics'})},
    'quality': {'top': frozenset({'comments', 'language', 'character_normalization_reference',
                                  'previous_attempt_errors'}),
                'comments': frozenset({'comment_id', 'units'})},
    'extract': {'top': frozenset({'comments', 'character_normalization_reference'}),
                'comments': frozenset({'comment_id', 'units', 'allowed_quality_points'})},
    'verify': {'top': frozenset({'original_evidence', 'proposed_claim', 'naming_reference', 'claim_id',
                                 'selected_source_segments', 'selected_source_points'}),
               'comments': frozenset()},
}


def schema_for(stage: str, ids: list[str], data: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return the response schema of a stage request; for extract, the request data narrows it per comment."""
    identity = {'type': 'string', 'enum': ids}
    if stage in ('relevance', 'retrieval_review'):
        return obj({'decisions': {**arr({'enum': ['related', 'unrelated', 'uncertain']}),
                                  'minItems': len(ids), 'maxItems': len(ids)}})
    if stage == 'quality':
        return quality.annotation_schema(ids)
    if stage == 'extract':
        records = {r['comment_id']: r for r in data['comments']} if data else {}
        properties = {}
        for record_id in ids:
            claim = copy.deepcopy(CLAIM)
            claims = arr(claim)
            if data and 'allowed_quality_points' in records[record_id]:
                allowed_points = records[record_id]['allowed_quality_points']
                claim['properties']['quality_point_ids'] = {**arr({'type': 'string',
                    'enum': [r['point_id'] for r in allowed_points]}), 'minItems': 1, 'maxItems': 1}
                claim['required'].append('quality_point_ids')
                if not allowed_points:
                    claims['maxItems'] = 0
            if data:
                text = '\n'.join(u['text'] for u in records[record_id]['units'])
                unit_ids = [u['evidence_id'] for u in records[record_id]['units']]
                parameters = claim['properties']['parameters']['items']['properties']
                numeric_values = list(dict.fromkeys(numeric_tokens(text) + re.findall(r'[一二三四五六七八九十百千万]+', text)))
                deltas = re.findall(r'\bby\s+([+-]?\d+(?:\.\d+)?%?)|(?:加|减|增加|减少|降低|提高)\s*([+-]?\d+(?:\.\d+)?%?|[一二三四五六七八九十百千万]+)', text, re.I)
                delta_values = list(dict.fromkeys(value for pair in deltas for value in pair if value))
                units = list(dict.fromkeys(re.findall(r'(?:\d+(?:\.\d+)?|[一二三四五六七八九十百千万]+)\s*(frames?\b|points?\b|seconds?\b|bars?\b|%|帧|点|秒|格)', text, re.I)))
                for key in ('current', 'proposed'):
                    parameters[key] = {'type': ['string', 'null'], 'enum': [None] + numeric_values}
                parameters['delta'] = {'type': ['string', 'null'], 'enum': [None] + delta_values}
                parameters['unit'] = {'type': ['string', 'null'], 'enum': [None] + units}
                # No legal requested value or delta means no valid numerical
                # parameter can exist; do not let decoding emit null-only ones.
                if not numeric_values and not delta_values:
                    claim['properties']['specificity'] = {'enum': ['qualitative_only']}
                    claim['properties']['parameters']['maxItems'] = 0
                if unit_ids:
                    evidence_property = {'type': 'string', 'enum': unit_ids}
                    claim['properties']['evidence_ids'] = {**arr(evidence_property), 'minItems': 1}
                    claim['properties']['parameters']['items']['properties']['evidence_id'] = evidence_property
                allowed = character_candidates(text, data['character_normalization_reference'])
                allowed, _ = attributed_candidates(text, data['character_normalization_reference'], allowed)
                if allowed:
                    claim['properties']['character'] = {'type': 'string', 'enum': allowed}
                else:
                    claims['maxItems'] = 0
            properties[record_id] = obj({'claims': claims})
        return obj({'assessments': obj(properties)})
    if len(ids) != 1:
        raise ValueError('Semantic audits require exactly one proposal')
    return obj({'support': {'type': 'string', 'enum': ['supported', 'unsupported', 'uncertain']}})


def exact_coverage(rows: list[dict[str, Any]], key: str, expected: list[str]) -> bool:
    """Return whether the key values of the rows are exactly the expected IDs, each as often."""
    return Counter(r[key] for r in rows) == Counter(expected)


def view(stage: str, data: dict[str, Any], ids: list[str]) -> dict[str, Any]:
    """Return the model-visible view of the request data of a stage (keys in MODEL_VISIBLE); data stays the context.

    The audit view for verify; the quality view (plan 4.1, UP-D04) for quality; the extraction view
    (plan 4.1, UP-D05) for extract; for relevance and retrieval review, the comments with the IDs and
    rounded cosines of their retrieved topics, whose texts are in the system prompt (plan 4.4, UP-D07).
    """
    if stage == 'quality':
        return _quality_view(data)
    if stage == 'extract':
        return _extract_view(data)
    if stage in ('relevance', 'retrieval_review'):
        return {'comments': [{'comment_id': c['comment_id'], 'text': c['text'], 'retrieved_topics': [
            {'topic_id': t['topic_id'], 'cosine': round(t['cosine'], 4)} for t in c['retrieved_topics']]}
            for c in data['comments']]}
    if stage != 'verify':
        return data
    entry = data['claims'][0]
    proposal = entry['claim']
    original = data.get('original_comment') or '\n'.join(u['text'] for u in proposal['evidence'])
    reference = character_reference(original)
    candidates = character_candidates(original, reference)
    # Confidence flags, model names and source URLs are not premises for
    # entailment. Keep the original text separate from the proposal.
    qualification = proposal.get('evidence_quality')
    data = {'original_evidence': original,
        'proposed_claim': {key: proposal[key] for key in ('character', 'target', 'direction', 'recommendation')},
        'naming_reference': [e for e in reference if e['canonical_name'] in candidates],
        'claim_id': ids[0]}
    data['proposed_claim']['parameters'] = [
        {key: parameter[key] for key in ('metric', 'current', 'proposed', 'delta', 'unit')}
        for parameter in proposal['parameters']]
    if qualification:
        # Show source spans and original annotation semantics, never a
        # passed-quality flag, emotion ratio or model confidence.
        data['selected_source_segments'] = [{k: s[k] for k in
            ('evidence_id', 'start', 'end', 'quote')} for s in qualification['selected_segments']]
        data['selected_source_points'] = [{k: p[k] for k in
            ('point_id', 'segment_ids', 'character_literal', 'mechanic_literal', 'stance', 'direction')}
            for p in qualification['selected_points']]
    return data


def _quality_view(data: dict[str, Any]) -> dict[str, Any]:
    """Return the comment units, the language and the reference entries of the comment's character candidates.

    The source row, the quality contract and the attempt number stay in the context. After a failed attempt,
    data['previous_attempt'] ({'errors', 'transport_failure'}) adds previous_attempt_errors: at most 20
    errors, each cut to 300 characters, or the single entry 'transport failure' without remote text.
    """
    reference = data['character_normalization_reference']
    candidates = character_candidates(data['source']['text_original'], reference)
    result = {'comments': [{'comment_id': c['comment_id'], 'units': [
                  {key: u[key] for key in ('evidence_id', 'text', 'start', 'end')} for u in c['units']]}
                  for c in data['comments']],
              'language': data['language'],
              'character_normalization_reference': [e for e in reference if e['canonical_name'] in candidates]}
    previous = data.get('previous_attempt')
    if previous is not None:
        result['previous_attempt_errors'] = (['transport failure'] if previous['transport_failure']
                                             else [str(error)[:300] for error in previous['errors'][:20]])
    return result


def _extract_view(data: dict[str, Any]) -> dict[str, Any]:
    """Return units without offsets, trimmed allowed quality points and the reference entries of the batch's candidates.

    The candidates of a comment are found in its joined unit texts, as schema_for finds its allowed characters.
    """
    reference = data['character_normalization_reference']
    candidates, comments = set(), []
    for comment in data['comments']:
        candidates.update(character_candidates('\n'.join(u['text'] for u in comment['units']), reference))
        entry = {'comment_id': comment['comment_id'],
                 'units': [{'evidence_id': u['evidence_id'], 'text': u['text']} for u in comment['units']]}
        if 'allowed_quality_points' in comment:
            entry['allowed_quality_points'] = [_allowed_point(r) for r in comment['allowed_quality_points']]
        comments.append(entry)
    return {'comments': comments,
            'character_normalization_reference': [e for e in reference if e['canonical_name'] in candidates]}


def _allowed_point(routed: dict[str, Any]) -> dict[str, Any]:
    """Return the model-visible fields of a mechanism-evidence routing entry; quotes come from its selected segments."""
    point = routed['point']
    return {'point_id': routed['point_id'],
            'evidence_ids': list(dict.fromkeys(s['evidence_id'] for s in routed['segments'])),
            'quotes': [s['quote'] for s in routed['segments']],
            **{key: point[key] for key in ('scope', 'detail_level', 'stance', 'direction',
                                           'character_literal', 'mechanic_literal')}}


def options(stage: str, quality_policy: dict[str, Any] | None) -> dict[str, Any]:
    """Return the inference options of a stage request; Runner applies its runtime options afterwards."""
    result = {'temperature': 0, 'seed': 42, 'num_ctx': 8192,
              'num_predict': 4096 if stage == 'extract' else 256}
    if stage == 'quality':
        policy = quality_policy or quality.load_policy()
        result.update(num_predict=policy['num_predict'], num_ctx=policy['num_ctx'])
    return result


def normalize(stage: str, parsed: dict[str, Any], ids: list[str],
              data: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    """Turn a schema-valid response into the stage result; return (parsed or None, errors)."""
    errors = []
    if stage in ('relevance', 'retrieval_review'):
        parsed = {'decisions': [{'comment_id': identity, 'related': status == 'related',
            'uncertain': status == 'uncertain', 'reason': 'Ordered model status: ' + status}
            for identity, status in zip(ids, parsed['decisions'])]}
    elif stage == 'quality':
        errors.extend(quality.validate_annotation(parsed, data['source'], data['comments'][0]['units']))
    elif stage == 'verify':
        status = parsed['support']
        parsed = {'verdicts': [{'claim_id': ids[0], 'supported': status == 'supported',
            'support_status': status, 'scope': 'selected_quality_segments_with_original_context' if data.get('selected_source_segments') else 'full_original_comment',
            'reason': 'Model source-support status: ' + status}]}
    else:
        parsed = {'assessments': [{'comment_id': identity, **assessment,
            'disposition': 'extracted' if assessment['claims'] else 'no_supported_character_claim'}
            for identity, assessment in parsed['assessments'].items()]}
        if not exact_coverage(parsed['assessments'], 'comment_id', ids):
            errors.append('Missing or duplicated item IDs')
    return (parsed if not errors else None), errors
