"""Frozen evaluation sets keep the bytes their manifests record."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC = ROOT / 'data/evaluation/evidence-quality-synthetic-v1'
FIXTURE = ROOT / 'src/aimediator/assets/fixtures/cases.json'


class EvaluationSets(unittest.TestCase):
    def test_synthetic_cases_link_to_the_fixture_and_match_the_manifest(self):
        # The packaged fixture is the single file; the set path is a
        # registered link to it (RULES.md G2, P1 freeze).
        cases = SYNTHETIC / 'cases.json'
        self.assertTrue(cases.is_symlink())
        self.assertEqual(cases.resolve(), FIXTURE.resolve())
        manifest = json.loads((SYNTHETIC / 'manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(hashlib.sha256(cases.read_bytes()).hexdigest(),
                         manifest['cases_sha256'])
        self.assertEqual(len(json.loads(cases.read_text(encoding='utf-8'))),
                         manifest['cases'])


if __name__ == '__main__':
    unittest.main()
