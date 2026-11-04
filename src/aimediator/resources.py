"""Authoritative redistributable resources, independent of the checkout."""
import functools
from importlib.resources import files
import json
from pathlib import Path


def asset_path(name=''):
    # Linux wheels install unpacked; resource lookup always starts at the package.
    return Path(str(files('aimediator').joinpath('assets', name)))


def anchors():
    value = json.loads(asset_path('retrieval-anchors.json').read_text(encoding='utf-8'))
    return value['POS'], value['NEG']


@functools.lru_cache(maxsize=1)
def glossary():
    """Return the parsed packaged glossary, loaded once per process; callers never mutate it."""
    return json.loads(asset_path('data/glossary.json').read_text(encoding='utf-8'))


def module_path(name):
    return Path(str(files('aimediator').joinpath(name)))


def prompts(mode):
    """Return the stage prompts for an evidence-quality mode, keyed by stage, then language."""
    names = {'relevance': 'relevance', 'retrieval_review': 'retrieval-review',
             'extract': 'summarize-balance', 'verify': 'verify-balance'}
    if mode != 'off':
        names['quality'] = 'evidence-quality'
    result = {stage: {lang: asset_path('prompts/%s.%s.txt' % (name, lang)).read_text(encoding='utf-8')
                      for lang in ('en', 'zh')} for stage, name in names.items()}
    if mode == 'enforce':
        for stage, name in (('extract', 'quality-extract'), ('verify', 'quality-verify')):
            for lang in ('en', 'zh'):
                result[stage][lang] += '\n' + asset_path('prompts/%s.%s.txt' % (name, lang)).read_text(encoding='utf-8')
    return result
