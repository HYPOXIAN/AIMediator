"""Glossary references of claim targets (pipeline upgrade plan 4.8, LNK-02, UP-D12).

The index holds every glossary entry except the `character` category, with its canonical name, its
Chinese label and its aliases. Only exact terms resolve: a term matches when `balance_policy.term_matches`
finds it in the target literal (whole-word and case-free for terms with a Latin letter, substring
otherwise). Aliases flagged `candidate_only` or `requires_context` only ever yield candidates, and an
entry scoped to a character matches only claims about that character. No fuzzy or semantic rule applies.
"""
from __future__ import annotations

import functools
from typing import Any

from .balance_policy import term_matches
from .resources import glossary

STATUSES = ('resolved', 'candidate', 'unmatched')


@functools.lru_cache(maxsize=1)
def _index() -> tuple[tuple[str, str, tuple[tuple[str, bool], ...]], ...]:
    """Return (entry ID, scope, ((term, resolves), ...)) per non-character entry, built once per process."""
    entries = []
    for entry in glossary()['entries']:
        if entry['category'] == 'character':
            continue
        terms = {}
        for text in (entry.get('canonical_name'), entry.get('chinese_label')):
            if isinstance(text, str) and text.strip():
                terms[text] = True
        for alias in entry.get('aliases', ()):
            text = alias.get('text')
            if not isinstance(text, str) or not text.strip() or terms.get(text):
                continue
            terms[text] = not (alias.get('candidate_only') or alias.get('requires_context'))
        entries.append((entry['id'], entry.get('scope') or 'universal', tuple(terms.items())))
    return tuple(entries)


def _shadowed(term: str, others: list[str]) -> bool:
    """Return whether term is a proper part of a longer matched term, so the longer one decides."""
    folded = term.casefold()
    return any(len(other) > len(term) and folded in other.casefold() for other in others)


def target_reference(target: Any, character: Any) -> dict[str, Any]:
    """Return the glossary reference of a claim target literal for the claim's character.

    The result holds `glossary_ids` (sorted), `status` (`resolved`, `candidate` or `unmatched`) and
    `matched_alias` (the longest matched term, or None). Matched terms inside a longer matched term
    (flagged or not) are dropped first. A target resolves only when the remaining terms that resolve
    name exactly one entry; several entries, or only flagged aliases, give a candidate, which never
    merges report groups.
    """
    if not isinstance(target, str) or not target.strip():
        return {'glossary_ids': [], 'status': 'unmatched', 'matched_alias': None}
    resolving, flagged = [], []
    for entry_id, scope, terms in _index():
        if scope != 'universal' and scope != character:
            continue
        for term, resolves in terms:
            if term_matches(term, target):
                (resolving if resolves else flagged).append((entry_id, term))
    texts = [term for _, term in resolving + flagged]
    for found, status in ((resolving, 'resolved'), (resolving + flagged, 'candidate')):
        kept = [(entry_id, term) for entry_id, term in found if not _shadowed(term, texts)]
        if not kept:
            continue
        ids = sorted({entry_id for entry_id, _ in kept})
        alias = sorted(kept, key=lambda pair: (-len(pair[1]), pair[0], pair[1]))[0][1]
        if status == 'resolved' and len(ids) != 1:
            status = 'candidate'
        return {'glossary_ids': ids, 'status': status, 'matched_alias': alias}
    return {'glossary_ids': [], 'status': 'unmatched', 'matched_alias': None}
