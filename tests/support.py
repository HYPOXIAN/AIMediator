"""Shared test fixtures: the synthetic evidence-quality cases and their qualified records."""
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import evidence_quality
from aimediator.evidence import evidence_units
from aimediator.resources import asset_path

CASES = json.loads(asset_path('fixtures/cases.json').read_text(encoding='utf-8'))


def case(category, language='en'):
    """Return a copy of the synthetic case with this category and language."""
    return copy.deepcopy(next(c for c in CASES if c['category'] == category and c['source']['language'] == language))


def qualified(c):
    """Return the deterministic quality record of a synthetic case."""
    return evidence_quality.qualify(c['annotation'], c['source'], evidence_units(c['source']['text_original']))
