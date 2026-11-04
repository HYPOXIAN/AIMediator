"""Per-stage model response schemas and item coverage checks."""
from collections import Counter
import copy
import re

from . import evidence_quality as quality
from .balance_policy import attributed_candidates
from .evidence import CLAIM, character_candidates, numeric_tokens
from .schema import arr, obj


def schema_for(stage, ids, data=None):
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


def exact_coverage(rows, key, expected):
    return Counter(r[key] for r in rows) == Counter(expected)
