"""Evidence qualification: immutable Unicode spans, diagnostics and routing.

No lexical emotion classifier or semantic truth oracle lives here. Models propose
annotations; deterministic checks reject malformed or unbound proposals.
"""
import copy
import hashlib
import json
from pathlib import Path
import unicodedata

from .resources import asset_path
POLICY_PATH = asset_path('configs/evidence-quality-policy.json')
ROUTES = ('exclude', 'opinion_only', 'mechanism_evidence', 'system_evidence', 'review')
REASONS = ('empty_venting', 'general_strength', 'concrete_mechanic_condition',
           'system_feedback', 'price_cosmetic_network', 'quoted_emotion',
           'missing_context', 'ambiguous_sarcasm', 'unrelated_topic', 'concrete_positive',
           'explicit_request', 'uncertain_attribution')


def load_policy():
    policy = json.loads(POLICY_PATH.read_text(encoding='utf-8'))
    if (policy['max_attempts'] != 2 or policy['request_batch_size'] != 1
            or policy['measurement_version'] != 'unicode-LNMS-codepoint-v1'
            or type(policy['num_predict']) is not int or policy['num_predict'] < 1
            or type(policy['num_ctx']) is not int or policy['num_ctx'] < 1
            or not 0 <= policy['high_emotion_threshold'] <= 1):
        raise ValueError('Unsupported evidence quality policy')
    return policy


def obj(properties):
    return {'type': 'object', 'properties': properties, 'required': list(properties),
            'additionalProperties': False}


def enum(values):
    return {'type': 'string', 'enum': list(values)}


STRING = {'type': 'string', 'minLength': 1}
NULL_STRING = {'type': ['string', 'null'], 'minLength': 1}
SCOPES = ('character_balance', 'system_balance', 'unrelated', 'uncertain')
KINDS = ('pure_emotion', 'general_opinion', 'concrete_feedback', 'other', 'uncertain')


def annotation_schema(ids):
    if len(ids) != 1:
        raise ValueError('Quality annotation requires exactly one comment')
    return obj({'comment_id': enum(ids),
        'segments': {'type': 'array', 'items': obj({
            'segment_id': STRING, 'evidence_id': STRING,
            'start': {'type': 'integer', 'minimum': 0},
            'end': {'type': 'integer', 'minimum': 1}, 'quote': STRING,
            'scope': enum(SCOPES), 'content_kind': enum(KINDS),
            'emotional_tone': {'type': 'boolean'}, 'reason_code': enum(REASONS)})},
        'information_points': {'type': 'array', 'items': obj({
            'point_id': STRING,
            'segment_ids': {'type': 'array', 'items': STRING, 'minItems': 1, 'uniqueItems': True},
            'scope': enum(('character_balance', 'system_balance', 'uncertain')),
            'detail_level': enum(('general', 'concrete', 'uncertain')),
            'stance': enum(('explicit_request', 'strength_assessment', 'observation', 'uncertain')),
            'direction': enum(('buff', 'nerf', 'keep', 'unclear')),
            'character_literal': NULL_STRING, 'mechanic_literal': NULL_STRING})}})


def schema_errors(value, schema, path='$'):
    errors = []
    if 'enum' in schema and value not in schema['enum']:
        errors.append(path + ': value outside enum')
    kind = schema.get('type')
    kinds = kind if isinstance(kind, list) else [kind] if kind else []
    types = {'object': lambda v: isinstance(v, dict), 'array': lambda v: isinstance(v, list),
             'string': lambda v: isinstance(v, str), 'null': lambda v: v is None,
             'boolean': lambda v: type(v) is bool, 'integer': lambda v: type(v) is int,
             'number': lambda v: type(v) in (float, int)}
    if kinds and not any(types[k](value) for k in kinds):
        return errors + [path + ': wrong type']
    if isinstance(value, dict) and kind == 'object':
        properties = schema['properties']
        if set(schema.get('required', [])) - set(value):
            errors.append(path + ': missing keys')
        if schema.get('additionalProperties') is False and set(value) - set(properties):
            errors.append(path + ': extra keys')
        for key in set(value) & set(properties):
            errors.extend(schema_errors(value[key], properties[key], path + '.' + key))
    if isinstance(value, list) and kind == 'array':
        if not schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', float('inf')):
            errors.append(path + ': wrong item count')
        if schema.get('uniqueItems') and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errors.append(path + ': duplicate items')
        for i, item in enumerate(value):
            errors.extend(schema_errors(item, schema['items'], f'{path}[{i}]'))
    if isinstance(value, str) and len(value) < schema.get('minLength', 0):
        errors.append(path + ': empty string')
    if type(value) in (int, float) and not schema.get('minimum', -float('inf')) <= value <= schema.get('maximum', float('inf')):
        errors.append(path + ': outside bounds')
    return errors


def weight(text):
    return sum(unicodedata.category(c)[0] in 'LNMS' for c in text)


def validate_annotation(annotation, row, units):
    errors = schema_errors(annotation, annotation_schema([row['record_id']]))
    if errors:
        return errors
    text = row['text_original']
    unit_map = {u['evidence_id']: u for u in units}
    segments = annotation['segments']
    seg_map = {s['segment_id']: s for s in segments}
    if len(seg_map) != len(segments):
        errors.append('Duplicate segment IDs')
    points = annotation['information_points']
    if len({p['point_id'] for p in points}) != len(points):
        errors.append('Duplicate point IDs')
    previous_end = 0
    covered = set()
    for s in segments:
        start, end = s['start'], s['end']
        unit = unit_map.get(s['evidence_id'])
        if unit is None or not (unit['start'] <= start < end <= unit['end']):
            errors.append('Foreign evidence ID or out-of-unit span: ' + s['segment_id'])
        if start < previous_end:
            errors.append('Overlapping or out-of-order spans')
        previous_end = end
        if not 0 <= start < end <= len(text) or text[start:end] != s['quote']:
            errors.append('Quote/offset mismatch: ' + s['segment_id'])
        covered.update(range(max(0, start), min(len(text), end)))
    expected = {i for u in units for i in range(u['start'], u['end']) if not text[i].isspace()}
    if not expected <= covered:
        errors.append('Uncovered non-whitespace original content')
    for p in points:
        refs = [seg_map.get(s) for s in p['segment_ids']]
        if any(s is None for s in refs):
            errors.append('Foreign segment reference: ' + p['point_id'])
            continue
        if p['scope'] != 'uncertain' and any(s['scope'] not in (p['scope'], 'uncertain') for s in refs):
            errors.append('Point/segment scope conflict: ' + p['point_id'])
        allowed = {'general': {'general_opinion'}, 'concrete': {'concrete_feedback'},
                   'uncertain': set(KINDS)}[p['detail_level']]
        if any(s['content_kind'] not in allowed | {'uncertain'} for s in refs):
            errors.append('Point/segment detail conflict: ' + p['point_id'])
        source = '\n'.join(s['quote'] for s in refs)
        for key in ('character_literal', 'mechanic_literal'):
            if p[key] is not None and not any(p[key] in s['quote'] for s in refs):
                errors.append('Literal absent from selected spans: ' + key)
        if p['scope'] == 'system_balance' and p['character_literal'] is not None:
            errors.append('System point must not bind a character')
    return errors


def qualify(annotation, row, units, policy=None):
    policy = policy or load_policy()
    errors = validate_annotation(annotation, row, units)
    base = {'comment_id': row['record_id'], 'language': row.get('language'),
            'source_url': row.get('source_url'),
            'content_sha256': hashlib.sha256(row['text_original'].encode()).hexdigest(),
            'schema_version': policy['schema_version'], 'policy_version': policy['version'],
            'measurement_version': policy['measurement_version'], 'annotation': annotation}
    if errors:
        return {**base, 'status': 'failed', 'errors': errors, 'routes_present': ['review'],
                'routing': [{'comment_id': row['record_id'], 'route': 'review', 'reason': 'invalid_annotation',
                             'point_id': None, 'segments': copy.deepcopy(units)}]}
    seg_map = {s['segment_id']: s for s in annotation['segments']}
    routed, used = [], set()
    for p in annotation['information_points']:
        selected = [seg_map[s] for s in p['segment_ids']]
        used.update(p['segment_ids'])
        uncertain = (p['scope'] == 'uncertain' or p['detail_level'] == 'uncertain'
                     or p['stance'] == 'uncertain' or any(s['scope'] == 'uncertain'
                     or s['content_kind'] == 'uncertain' or s['reason_code'] in
                     ('quoted_emotion', 'missing_context', 'ambiguous_sarcasm', 'uncertain_attribution') for s in selected))
        if uncertain:
            route, reason = 'review', 'uncertain_information'
        elif p['scope'] == 'system_balance':
            route, reason = 'system_evidence', 'separate_system_scope'
        elif not p['character_literal']:
            route, reason = 'review', 'missing_character_context'
        elif p['detail_level'] == 'general':
            route, reason = 'opinion_only', 'general_not_mechanism'
        else:
            route, reason = 'mechanism_evidence', 'concrete_character_information'
        routed.append({'comment_id': row['record_id'], 'point_id': p['point_id'], 'route': route,
                       'reason': reason, 'point': p, 'segments': selected})
    for s in annotation['segments']:
        if s['segment_id'] in used:
            continue
        uncertain = s['scope'] == 'uncertain' or s['content_kind'] == 'uncertain' or s['reason_code'] in (
            'quoted_emotion', 'missing_context', 'ambiguous_sarcasm', 'uncertain_attribution')
        # Information-bearing fragments omitted from points cannot silently disappear.
        unresolved = s['scope'] != 'unrelated' and s['content_kind'] in ('general_opinion', 'concrete_feedback')
        route = 'review' if uncertain or unresolved else 'exclude'
        routed.append({'comment_id': row['record_id'], 'point_id': None, 'route': route,
                       'reason': 'unresolved_fragment' if route == 'review' else 'no_balance_information',
                       'excluded_use': 'balance_analysis' if route == 'exclude' else None, 'segments': [s]})
    denominator = weight(row['text_original'])
    numerator = sum(weight(s['quote']) for s in annotation['segments'] if s['content_kind'] == 'pure_emotion')
    ratio = numerator / denominator if denominator else None
    counts = {scope: {level + '_point_count': sum(p['scope'] == scope and p['detail_level'] == level
               for p in annotation['information_points']) for level in ('general', 'concrete')}
              for scope in ('character_balance', 'system_balance', 'uncertain')}
    routes = sorted({r['route'] for r in routed})
    if not routed:
        routed = [{'comment_id': row['record_id'], 'point_id': None, 'route': 'exclude',
                   'reason': 'empty_content', 'segments': [], 'excluded_use': 'balance_analysis'}]
        routes = ['exclude']
    return {**base, 'status': 'completed', 'errors': [], 'routing': routed, 'routes_present': routes,
            'emotion_weight': numerator, 'full_weight': denominator, 'emotion_ratio': ratio,
            'empty_measurement': denominator == 0,
            'high_emotion_warning': ratio is not None and ratio >= policy['high_emotion_threshold'],
            'emotion_only': numerator > 0 and not annotation['information_points'] and routes == ['exclude'],
            'point_counts': counts}


def failed_record(row, units, attempts, policy=None):
    record = qualify(None, row, units, policy)
    record.update(attempts=attempts, errors=[e for a in attempts for e in a['errors']])
    record['routing'][0]['reason'] = 'quality_attempts_exhausted'
    return record


def allowed_points(record):
    return [r for r in record['routing'] if r['route'] == 'mechanism_evidence']


def bind_claim(claim, record, reference):
    """Bind a claim to exactly one concrete point, never a comment-wide pass.

    Lexical checks enforce source membership; a separate selected-span semantic
    audit must still establish the relation between the claim and this point.
    """
    from .balance_policy import numeric_request_supported, term_matches
    import re
    errors = []
    ids = claim.get('quality_point_ids', [])
    by_id = {r['point_id']: r for r in allowed_points(record)}
    if len(ids) != 1 or ids[0] not in by_id:
        return ['Claim requires one eligible same-comment mechanism point'], None
    selected = by_id[ids[0]]
    p, spans = selected['point'], selected['segments']
    text = '\n'.join(s['quote'] for s in spans)
    if not claim['evidence_ids'] or set(claim['evidence_ids']) != {s['evidence_id'] for s in spans}:
        errors.append('Claim evidence outside selected quality point')
    identity = next((e for e in reference if e['canonical_name'] == claim['character']), None)
    terms = ([identity['canonical_name'], identity.get('chinese_label')]
             + [a['text'] for a in identity['aliases']]) if identity else []
    if not any(t and term_matches(t, p['character_literal'] or '') for t in terms):
        errors.append('Claim character differs from selected point')
    if claim['direction'] != p['direction']:
        errors.append('Claim direction differs from selected point')
    if claim.get('target') and not (claim['target'] in text or
            p['mechanic_literal'] and p['mechanic_literal'] in claim['target']):
        errors.append('Claim target absent from selected point')
    numbers = lambda t: re.findall(r'[+-]?\d+(?:\.\d+)?%?', t)
    if any(n not in numbers(text) for n in numbers((claim.get('target') or '') + ' ' + claim['recommendation'])):
        errors.append('Claim number absent from selected point')
    for param in claim['parameters']:
        local = '\n'.join(s['quote'] for s in spans if s['evidence_id'] == param['evidence_id'])
        if any(n not in numbers(local) for n in numbers(param['metric'])):
            errors.append('Parameter metric number absent from selected quality spans')
        if p['stance'] != 'explicit_request' or not numeric_request_supported(local, param):
            errors.append('Numeric request not supported by selected point')
        for key in ('current', 'proposed', 'delta', 'unit'):
            if param[key] is not None and (param[key] not in local or any(n not in numbers(local) for n in numbers(param[key]))):
                errors.append('Parameter absent from selected quality spans: ' + key)
    qualification = {'schema_version': record['schema_version'], 'mode': 'enforce',
                     'route': 'mechanism_evidence', 'comment_id': record['comment_id'],
                     'content_sha256': record['content_sha256'], 'point_ids': ids,
                     'selected_points': [copy.deepcopy(p)], 'selected_segments': copy.deepcopy(spans)}
    return errors, qualification


def summarize_opinions(records, reference):
    from .balance_policy import term_matches
    grouped, unresolved = {}, []
    for record in records:
        for routed in record['routing']:
            if routed['route'] != 'opinion_only':
                continue
            p = routed['point']
            matching = [e for e in reference if any(t and term_matches(t, p['character_literal']) for t in
                        [e['canonical_name'], e.get('chinese_label')] + [a['text'] for a in e['aliases']])]
            if len(matching) != 1 or matching[0].get('normalization_status') == 'source_literal_unverified':
                unresolved.append(routed)
                continue
            key = (matching[0]['canonical_name'], p['mechanic_literal'], p['direction'])
            group = grouped.setdefault(key, {'character': key[0], 'topic': key[1], 'direction': key[2],
                'stance_comment_ids': {}, 'comment_ids': set(), 'evidence': []})
            group['comment_ids'].add(record['comment_id'])
            group['stance_comment_ids'].setdefault(p['stance'], set()).add(record['comment_id'])
            group['evidence'].append({**routed, 'source_url': record.get('source_url'),
                'content_sha256': record['content_sha256'], 'language': record.get('language'),
                'policy_version': record['policy_version'],
                'quality_request_ids': [a['request_id'] for a in record.get('attempts', [])]})
    groups = []
    for group in grouped.values():
        group['comment_ids'] = sorted(group['comment_ids'])
        group['supporting_comment_count'] = len(group['comment_ids'])
        group['stance_comment_ids'] = {stance: sorted(ids) for stance, ids in group['stance_comment_ids'].items()}
        group['stance_comment_counts'] = {stance: len(ids) for stance, ids in group['stance_comment_ids'].items()}
        groups.append(group)
    return {'groups': groups, 'unresolved_identity_opinions': unresolved,
            'counting_unit': 'unique_comment_id_per_character_topic_direction',
            'limitation': 'Sample comments, not independent players or population consensus; groups can overlap.'}
