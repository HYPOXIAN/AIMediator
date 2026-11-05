"""Evidence primitives: source units, numeric tokens, character references and source binding."""
from __future__ import annotations

import copy
from functools import lru_cache
import re
from typing import Any
import unicodedata

from .balance_policy import (attributed_candidates, direction_action_conflicts, identity_alias_allowed,
                             load_policy, numeric_request_supported, term_matches)
from .resources import glossary
from .schema import BOOL, NULLABLE_STRING, STRING, arr, obj

PARAMETER = obj({k: v for k, v in [
    ('metric', STRING), ('current', NULLABLE_STRING), ('proposed', NULLABLE_STRING),
    ('delta', NULLABLE_STRING), ('unit', NULLABLE_STRING), ('evidence_id', STRING)]})
# Evidence-first property order (pipeline upgrade plan 4.3, U5.1, UP-D11): the model
# selects the source units before it names the subject. The order reaches the model
# through the response schema; inference derives the claim key of its loop guard
# from that schema.
CLAIM = obj({'evidence_ids': arr(STRING), 'character': STRING, 'target': NULLABLE_STRING,
             'direction': {'enum': ['buff', 'nerf', 'keep', 'unclear']},
             'recommendation': STRING, 'specificity': {'enum': ['qualitative_only', 'source_numeric']},
             'parameters': arr(PARAMETER), 'uncertain': BOOL})


def evidence_units(text: str) -> list[dict[str, Any]]:
    """Split text into evidence units E1, E2, ... with their text and offsets in the original."""
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


SEGMENTATION_VERSION = 'clause-v1'
CLAUSE_PUNCTUATION = frozenset(',;:，；：、')


def clause_segments(units: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Split evidence units into clause segments E<n>.<k> with absolute code-point offsets (clause-v1, plan 4.2).

    A unit splits after a run of clause punctuation (, ; : and their full-width forms, and 、) with the
    combining marks that follow it, unless the characters before and after the run are both decimal digits
    (1,000 and 1:30 stay whole). Punctuation stays with the clause on its left; whitespace at the edges of a
    segment is dropped; a unit without a split point is one segment. The segments of a unit are ordered,
    disjoint and cover every non-whitespace character of the unit; text == original[start:end].
    """
    segments = []
    for unit in units:
        text, base, pieces, left, i = unit['text'], unit['start'], [], 0, 0
        while i < len(text):
            if text[i] not in CLAUSE_PUNCTUATION:
                i += 1
                continue
            run_start = i
            while i < len(text) and text[i] in CLAUSE_PUNCTUATION:
                i += 1
            while i < len(text) and unicodedata.category(text[i]).startswith('M'):
                i += 1
            if i < len(text) and not (run_start > 0 and text[run_start - 1].isdecimal() and text[i].isdecimal()):
                pieces.append((left, i))
                left = i
        pieces.append((left, len(text)))
        for start, end in pieces:
            raw = text[start:end]
            start, end = start + len(raw) - len(raw.lstrip()), end - len(raw) + len(raw.rstrip())
            if start < end:
                count = sum(s['evidence_id'] == unit['evidence_id'] for s in segments)
                segments.append({'segment_id': '%s.%d' % (unit['evidence_id'], count + 1),
                                 'evidence_id': unit['evidence_id'], 'text': text[start:end],
                                 'start': base + start, 'end': base + end})
    return segments


def character_reference(text: str = '') -> list[dict[str, Any]]:
    """Return new character reference entries, keeping only the aliases that occur in text."""
    # Memoized by text; every call returns its own copy, so callers may mutate it.
    return _json_copy(_character_reference(text))


def _json_copy(value: Any) -> Any:
    """Return a copy of JSON-shaped data with a new dict or list at every level (deepcopy without its memo)."""
    if isinstance(value, dict):
        return {key: _json_copy(item) if isinstance(item, (dict, list)) else item for key, item in value.items()}
    if isinstance(value, list):
        return [_json_copy(item) if isinstance(item, (dict, list)) else item for item in value]
    return value


@lru_cache(maxsize=1024)
def _character_reference(text: str) -> list[dict[str, Any]]:
    """Build the character reference of text; the cached value is never handed out."""
    reference = [{'canonical_name': e['canonical_name'], 'chinese_label': e.get('chinese_label'),
             'aliases': [{k: a[k] for k in ('text', 'candidate_only', 'requires_context', 'context_note') if k in a}
                         for a in e['aliases'] if term_matches(a['text'], text) and identity_alias_allowed(a['text'])]}
            for e in glossary()['entries'] if e['category'] == 'character']
    reference.extend(copy.deepcopy(load_policy()['source_literal_characters']))
    return reference


def character_terms(entry: dict[str, Any]) -> list[str | None]:
    """Return the canonical name, Chinese label and alias texts of a reference entry, unfiltered."""
    return [entry['canonical_name'], entry.get('chinese_label')] + [a['text'] for a in entry['aliases']]


def character_candidates(text: str, reference: list[dict[str, Any]]) -> list[str]:
    """Return the canonical names of the reference entries with a term that occurs in text."""
    return [entry['canonical_name'] for entry in reference
            if any(term_matches(term, text) for term in character_terms(entry))]


def numeric_tokens(text: str) -> list[str]:
    """Return the signed numeric tokens of text, with their decimals and percent signs."""
    return re.findall(r'[+-]?\d+(?:\.\d+)?%?', text)


def _character_identity(character: str | None, text: str) -> dict[str, Any] | None:
    """Return the identity record of a claimed character in its source, or None without a reference entry."""
    entry = next((e for e in character_reference(text) if e['canonical_name'] == character), None)
    if not entry:
        return None
    # The Chinese label is tried first here, unlike character_terms; it decides the recorded literal.
    literal = next((t for t in [entry.get('chinese_label'), entry['canonical_name']]
                    + [a['text'] for a in entry['aliases']] if term_matches(t, text)), None)
    unverified = entry.get('normalization_status') == 'source_literal_unverified'
    return {'source_literal': literal,
            'canonical_name': None if unverified else character,
            'normalization_status': 'source_literal_unverified' if unverified else 'glossary_reference',
            'glossary_target_patch': glossary().get('target_patch')}


def ground_claim(claim: dict[str, Any], row: dict[str, Any],
                 characters: set[str]) -> tuple[list[str], dict[str, Any] | None]:
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
    identity = _character_identity(claim['character'], row['text_original'])
    if identity is not None:
        enriched['character_identity'] = identity
    for item in enriched['evidence']:
        if item['text'] != row['text_original'][item['start']:item['end']]:
            raise AssertionError('Evidence span differs from the original text')
    return errors, enriched
