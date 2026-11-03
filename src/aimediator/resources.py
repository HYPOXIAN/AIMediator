"""Authoritative redistributable resources, independent of the checkout."""
from importlib.resources import files
import json
from pathlib import Path


def asset_path(name=''):
    # Linux wheels install unpacked; resource lookup always starts at the package.
    return Path(str(files('aimediator').joinpath('assets', name)))


def anchors():
    value = json.loads(asset_path('retrieval-anchors.json').read_text(encoding='utf-8'))
    return value['POS'], value['NEG']


def module_path(name):
    return Path(str(files('aimediator').joinpath(name)))
