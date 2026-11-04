"""Evidence primitives: source units, numeric tokens, character references and source binding."""
import copy
import re

from .balance_policy import (attributed_candidates, direction_action_conflicts, identity_alias_allowed,
                             load_policy, numeric_request_supported, term_matches)
from .resources import glossary
from .schema import BOOL, NULL_STRING, STRING, arr, obj

PARAMETER = obj({k: v for k, v in [
    ('metric', STRING), ('current', NULL_STRING), ('proposed', NULL_STRING),
    ('delta', NULL_STRING), ('unit', NULL_STRING), ('evidence_id', STRING)]})
CLAIM = obj({'character': STRING, 'target': NULL_STRING,
             'direction': {'enum': ['buff', 'nerf', 'keep', 'unclear']},
             'recommendation': STRING, 'specificity': {'enum': ['qualitative_only', 'source_numeric']},
             'parameters': arr(PARAMETER), 'evidence_ids': arr(STRING), 'uncertain': BOOL})


def evidence_units(text):
    # Keep decimal values (e.g. 1.5) and move notation intact. Offsets are Unicode
    # code-point indices in the immutable original, not byte or UTF-16 offsets.
    units, start = [], 0
    for match in list(re.finditer(r'\r?\n+|[。！？!?]+|\.(?=\s|$)', text)) + [None]:
        end = len(text) if match is None else (match.start() if '\n' in match.group() else match.end())
        raw = text[start:end]
        left, right = start + len(raw) - len(raw.lstrip()), end - len(raw) + len(raw.rstrip())
        if left < right:
            units.append({'evidence_id': 'E' + str(len(units) + 1),
                          'text': text[left:right], 'start': left, 'end': right})
        start = len(text) if match is None else match.end()
    return units


def character_reference(text=''):
    reference = [{'canonical_name': e['canonical_name'], 'chinese_label': e.get('chinese_label'),
             'aliases': [{k: a[k] for k in ('text', 'candidate_only', 'requires_context', 'context_note') if k in a}
                         for a in e['aliases'] if term_matches(a['text'], text) and identity_alias_allowed(a['text'])]}
            for e in glossary()['entries'] if e['category'] == 'character']
    reference.extend(copy.deepcopy(load_policy()['source_literal_characters']))
    return reference


def character_candidates(text, reference):
    return [entry['canonical_name'] for entry in reference if any(term_matches(term, text) for term in
        [entry['canonical_name'], entry.get('chinese_label')] + [a['text'] for a in entry['aliases']])]


def numeric_tokens(text):
    return re.findall(r'[+-]?\d+(?:\.\d+)?%?', text)


def ground_claim(claim, row, characters):
    """Check identity-bound spans and numeric presence; entailment is audited later."""
    units = {u['evidence_id']: u for u in evidence_units(row['text_original'])}
    errors = []
    refs = claim['evidence_ids']
    if not refs or len(refs) != len(set(refs)) or any(r not in units for r in refs):
        return ['Missing, duplicated or foreign evidence IDs'], None
    selected = [units[r] for r in refs]
    source = '\n'.join(u['text'] for u in selected)
    if claim['character'] is not None and claim['character'] not in characters:
        errors.append('Unknown canonical character')
    candidates = character_candidates(row['text_original'], character_reference(row['text_original']))
    if claim['character'] is not None and claim['character'] not in candidates:
        errors.append('Character identity has no permitted source name')
    attributed, exclusions = attributed_candidates(row['text_original'], character_reference(row['text_original']), candidates)
    if claim['character'] in exclusions:
        errors.append('Source attribution excludes character: ' + exclusions[claim['character']])
    if claim['character'] is None and not claim['uncertain']:
        errors.append('Unresolved character must be uncertain')
    if bool(claim['parameters']) != (claim['specificity'] == 'source_numeric'):
        errors.append('Inconsistent numeric specificity')
    if direction_action_conflicts(claim):
        errors.append('Explicit engineering action contradicts direction tag')
    prose = ' '.join(str(claim.get(k) or '') for k in ['target', 'recommendation'])
    # Match complete signed numeric tokens, not substring 5 in 50 or +2 in -2.
    if any(n not in numeric_tokens(source) for n in numeric_tokens(prose)):
        errors.append('Unsupported number in recommendation or target')
    for parameter in claim['parameters']:
        unit = units.get(parameter['evidence_id'])
        if unit is None or parameter['evidence_id'] not in refs:
            errors.append('Parameter evidence not selected')
            continue
        if parameter['proposed'] is None and parameter['delta'] is None:
            errors.append('Parameter lacks requested target or delta')
        if not numeric_request_supported(unit['text'], parameter):
            errors.append('Numerical adjustment intent absent or ambiguous; review required')
        for key in ['current', 'proposed', 'delta', 'unit']:
            value = parameter[key]
            if value is not None and (not value or value not in unit['text']):
                errors.append('Parameter ' + key + ' absent from its original span')
            if value and any(n not in numeric_tokens(unit['text']) for n in numeric_tokens(value)):
                errors.append('Parameter ' + key + ' numeric token mismatch')
        if any(n not in numeric_tokens(unit['text']) for n in numeric_tokens(parameter['metric'])):
            errors.append('Unsupported number in parameter metric')
    enriched = {**claim, 'evidence': [{**u, 'comment_id': row['record_id'],
        'source_url': row.get('source_url')} for u in selected]}
    enriched['source_review_required'] = True
    entry = next((e for e in character_reference(row['text_original'])
                  if e['canonical_name'] == claim['character']), None)
    if entry:
        literal = next((t for t in [entry.get('chinese_label'), entry['canonical_name']]
                        + [a['text'] for a in entry['aliases']] if term_matches(t, row['text_original'])), None)
        unverified = entry.get('normalization_status') == 'source_literal_unverified'
        enriched['character_identity'] = {'source_literal': literal,
            'canonical_name': None if unverified else claim['character'],
            'normalization_status': 'source_literal_unverified' if unverified else 'glossary_reference',
            'glossary_target_patch': glossary().get('target_patch')}
    for item in enriched['evidence']:
        if item['text'] != row['text_original'][item['start']:item['end']]:
            raise AssertionError('Evidence span differs from the original text')
    return errors, enriched
