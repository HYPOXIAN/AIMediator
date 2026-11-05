"""Glossary target references (pipeline upgrade U6.1, plan 4.8, LNK-02, UP-D12)."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import topics  # noqa: E402
from aimediator.common import Failure, read, write  # noqa: E402
from aimediator.demo import demo  # noqa: E402
from aimediator.review import load_run  # noqa: E402

DEMO = {}


def demo_run():
    if 'root' not in DEMO:
        DEMO['tmp'] = tempfile.TemporaryDirectory()
        DEMO['root'] = Path(DEMO['tmp'].name) / 'demo'
        demo(DEMO['root'], quiet=True)
    return DEMO['root']


def tearDownModule():
    if 'tmp' in DEMO:
        DEMO['tmp'].cleanup()


class TargetReferenceTest(unittest.TestCase):
    def check(self, target, character, ids, status, alias):
        self.assertEqual(topics.target_reference(target, character),
                         {'glossary_ids': ids, 'status': status, 'matched_alias': alias}, (target, character))

    def test_universal_mechanics_in_english_and_chinese(self):
        self.check('Drive Impact', 'Ryu', ['system.drive_impact'], 'resolved', 'Drive Impact')
        self.check('drive impact damage', 'Ken', ['system.drive_impact'], 'resolved', 'Drive Impact')
        self.check('斗气迸放', 'Ken', ['system.drive_impact'], 'resolved', '斗气迸放')
        self.check('Drive Rush', 'Luke', ['system.drive_rush'], 'resolved', 'Drive Rush')
        self.check('绿冲的收益', 'Luke', ['system.drive_rush'], 'resolved', '绿冲')
        self.check('Perfect Parry', 'JP', ['system.perfect_parry'], 'resolved', 'Perfect Parry')
        self.check('完美招架', 'Manon', ['system.perfect_parry'], 'resolved', '完美招架')

    def test_character_moves_in_english_and_chinese(self):
        self.check('Hadoken', 'Ryu', ['ryu.hadoken'], 'resolved', 'Hadoken')
        self.check('波动拳', 'Ryu', ['ryu.hadoken'], 'resolved', '波动拳')
        self.check('Sonic Boom', 'Guile', ['guile.special.sonic_boom'], 'resolved', 'Sonic Boom')
        self.check('Sonic Boom recovery', 'Guile', ['guile.special.sonic_boom', 'mechanic.recovery'], 'candidate',
                   'Sonic Boom')
        self.check('音速手刀', 'Guile', ['guile.special.sonic_boom'], 'resolved', '音速手刀')
        self.check('Shoryuken', 'Ken', ['ken.special.shoryuken'], 'resolved', 'Shoryuken')
        self.check('OD Sonic Cross', 'Guile', ['guile.special.od_sonic_cross'], 'resolved', 'OD Sonic Cross')

    def test_flagged_and_ambiguous_aliases_stay_candidates(self):
        # requires_context / candidate_only aliases never resolve.
        self.check('boom', 'Guile', ['guile.special.sonic_boom'], 'candidate', 'boom')
        self.check('迸', 'Ryu', ['system.drive_impact'], 'candidate', '迸')
        # A resolving term inside a longer flagged alias does not decide: 斗气 (Drive Gauge) in 斗气冲击.
        self.check('斗气冲击', 'Ryu', ['system.drive_impact'], 'candidate', '斗气冲击')
        # One alias of several entries, and a target naming two entries, are candidates.
        self.check('CA', 'Ryu', ['ryu.ca', 'ryu.sa3', 'system.critical_art', 'system.sa3'], 'candidate', 'CA')
        self.check('Drive Rush into Drive Impact', 'Ryu', ['system.drive_impact', 'system.drive_rush'],
                   'candidate', 'Drive Impact')

    def test_other_characters_moves_and_free_text_stay_unmatched(self):
        self.check('Sonic Boom', 'Ken', [], 'unmatched', None)
        self.check('音速手刀', 'Ryu', [], 'unmatched', None)
        self.check('Hadoken', 'Guile', [], 'unmatched', None)
        self.check('overall strength', 'Ryu', [], 'unmatched', None)
        self.check('', 'Ryu', [], 'unmatched', None)
        self.check(None, 'Ryu', [], 'unmatched', None)

    def test_whole_word_matching_for_latin_terms(self):
        # DI is an alias of Drive Impact; it must not match inside another word.
        self.check('DI damage', 'Ken', ['system.drive_impact'], 'resolved', 'DI')
        self.check('Dhalsim spacing', 'Dhalsim', [], 'unmatched', None)

    def test_index_is_built_once_and_skips_characters(self):
        first = topics._index()
        self.assertIs(first, topics._index())
        self.assertFalse(any(entry_id.startswith('character.') for entry_id, _, _ in first))
        self.assertGreater(len(first), 800)


class PipelineAndReviewTest(unittest.TestCase):
    def test_grounded_claims_carry_the_reference(self):
        root = demo_run()
        for mode in ('off', 'shadow', 'enforce'):
            claims = read(root / mode / 'claims-before-audit.json')
            self.assertTrue(claims)
            for entry in claims:
                claim = entry['claim']
                self.assertEqual(claim['target_reference'],
                                 topics.target_reference(claim['target'], claim['character']))
                keys = list(claim)
                self.assertEqual(keys.index('target_reference'), keys.index('source_review_required') + 1
                                 if 'character_identity' not in claim else keys.index('character_identity') + 1)

    def test_review_fails_a_changed_reference(self):
        import shutil
        root = demo_run()
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'off'
            shutil.copytree(root / 'off', folder)
            self.assertTrue(load_run(folder)['automatic'])
            path = folder / 'validated-claims.json'
            claims = read(path)
            self.assertIn('target_reference', claims[0])
            changed = copy.deepcopy(claims)
            changed[0]['target_reference'] = {'glossary_ids': ['system.drive_rush'], 'status': 'resolved',
                                              'matched_alias': 'Drive Rush'}
            write(path, changed)
            # An automatic claim whose saved reference differs fails closed, like the saved evidence check.
            with self.assertRaises(Failure):
                load_run(folder)

            def strip(value):
                if isinstance(value, dict):
                    return {k: strip(v) for k, v in value.items() if k != 'target_reference'}
                if isinstance(value, list):
                    return [strip(v) for v in value]
                return value
            # Runs written before U6.1 have no reference and still load.
            write(path, strip(claims))
            for name in ('quarantined-claims.json', 'claims-before-audit.json', 'audit-progress.json'):
                if (folder / name).exists():
                    write(folder / name, strip(read(folder / name)))
            self.assertEqual(sorted(load_run(folder)['automatic']), sorted(c['claim_id'] for c in claims))

if __name__ == '__main__':
    unittest.main()
