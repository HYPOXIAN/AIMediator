"""Authoritative redistributable resources, independent of the checkout."""
from __future__ import annotations

import functools
from importlib.resources import files
import json
from pathlib import Path
from typing import Any


def asset_path(name: str = '') -> Path:
    """Return the path of a packaged asset, or of the asset directory when name is empty."""
    # Linux wheels install unpacked; resource lookup always starts at the package.
    return Path(str(files('aimediator').joinpath('assets', name)))


@functools.lru_cache(maxsize=1)
def anchors() -> tuple[list[str], list[str]]:
    """Return the packaged positive and negative retrieval anchors, loaded once per process; callers never mutate them."""
    value = json.loads(asset_path('retrieval-anchors.json').read_text(encoding='utf-8'))
    return value['POS'], value['NEG']


@functools.lru_cache(maxsize=1)
def glossary() -> dict[str, Any]:
    """Return the parsed packaged glossary, loaded once per process; callers never mutate it."""
    return json.loads(asset_path('data/glossary.json').read_text(encoding='utf-8'))


def module_path(name: str) -> Path:
    """Return the path of a module file inside the package."""
    return Path(str(files('aimediator').joinpath(name)))


def prompts(mode: str) -> dict[str, dict[str, str]]:
    """Return the stage prompts for an evidence-quality mode, keyed by stage, then language.

    The relevance and retrieval-review prompts end with the topic list: one line per anchor, P1 to N10.
    """
    names = {'relevance': 'relevance', 'retrieval_review': 'retrieval-review',
             'extract': 'summarize-balance', 'verify': 'verify-balance'}
    if mode != 'off':
        names['quality'] = 'evidence-quality'
    result = {stage: {lang: asset_path('prompts/%s.%s.txt' % (name, lang)).read_text(encoding='utf-8')
                      for lang in ('en', 'zh')} for stage, name in names.items()}
    # The anchors keep one source (retrieval-anchors.json); requests cite them by topic_id (plan 4.4, UP-D07).
    topics = ''.join('%s%d: %s\n' % (prefix, index, text) for prefix, texts in zip('PN', anchors())
                     for index, text in enumerate(texts, 1))
    for stage in ('relevance', 'retrieval_review'):
        for lang in ('en', 'zh'):
            result[stage][lang] += topics
    if mode == 'enforce':
        for stage, name in (('extract', 'quality-extract'), ('verify', 'quality-verify')):
            for lang in ('en', 'zh'):
                result[stage][lang] += '\n' + asset_path('prompts/%s.%s.txt' % (name, lang)).read_text(encoding='utf-8')
    return result


def _workspace_root(candidate: Path) -> Path:
    """Return candidate when it holds RULES.md and pyproject.toml, otherwise the working directory."""
    if (candidate / 'RULES.md').exists() and (candidate / 'pyproject.toml').exists():
        return candidate
    return Path.cwd()


def workspace_root() -> Path:
    """Return the checkout root when the package is imported from a checkout, otherwise the working directory."""
    return _workspace_root(Path(__file__).resolve().parents[2])
