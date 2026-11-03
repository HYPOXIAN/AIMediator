import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts/collect'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts/experiments'))
import review_balance_sources as r


class SourceReviewTests(unittest.TestCase):
    def setUp(self):
        self.claim = {'character': 'Ryu', 'target': None, 'direction': 'nerf',
            'recommendation': 'Nerf Ryu.', 'specificity': 'qualitative_only',
            'parameters': [], 'evidence_ids': ['E1'], 'uncertain': False}
        self.proposals = {'a:1': {'claim': self.claim, 'comment_id': 'a', 'model': 'fixture'}}
        self.sources = {'a': {'record_id': 'a', 'text_original': 'Ryu is too strong. Reduce his Hadoken damage.'}}
        self.decisions = {'a:1': {'decision': 'accept', 'reason': 'Explicit strength complaint.',
                                 'proposal_sha256': r.proposal_hash(self.claim)}}

    def apply(self):
        return r.apply_review(self.proposals, self.decisions, self.sources, {'a'}, {'Ryu'})

    def test_context_can_be_added_without_changing_raw_model_results(self):
        original = copy.deepcopy(self.proposals)
        self.decisions['a:1'].update(evidence_ids=['E1', 'E2'], target='Hadoken damage',
                                     recommendation="Reduce Ryu's Hadoken damage.")
        accepted, excluded = self.apply()
        self.assertEqual(len(accepted), 1)
        self.assertEqual(excluded, [])
        self.assertTrue(accepted[0]['source_review']['context_changed'])
        self.assertEqual(self.proposals, original)
        self.assertFalse(accepted[0]['source_review_required'])
        for evidence in accepted[0]['evidence']:
            self.assertEqual(evidence['text'], self.sources['a']['text_original'][evidence['start']:evidence['end']])

    def test_direction_cannot_be_silently_corrected(self):
        self.decisions['a:1']['direction'] = 'buff'
        with self.assertRaises(ValueError): self.apply()

    def test_explicit_direction_correction_is_labeled_and_preserves_original(self):
        self.sources['a']['text_original'] = 'Ryu is too weak.'
        self.decisions['a:1'].update(corrected_direction='buff',
            reason='The source explicitly describes weakness; the original nerf direction was inverted.',
            recommendation='Strengthen Ryu.')
        accepted, _ = self.apply()
        self.assertEqual(accepted[0]['direction'], 'buff')
        self.assertTrue(accepted[0]['source_review']['direction_changed'])
        self.assertEqual(accepted[0]['original_model_claim']['direction'], 'nerf')

    def test_invented_number_and_foreign_evidence_remain_blocked(self):
        for key, value in [('recommendation', 'Reduce damage by 40%.'), ('evidence_ids', ['E99'])]:
            decisions = copy.deepcopy(self.decisions)
            self.decisions['a:1'][key] = value
            with self.assertRaises(ValueError): self.apply()
            self.decisions = decisions

    def test_every_proposal_requires_an_explicit_review(self):
        self.decisions = {}
        with self.assertRaises(ValueError): self.apply()

    def test_changed_proposal_cannot_reuse_a_review(self):
        self.claim['direction'] = 'buff'
        with self.assertRaises(ValueError): self.apply()

    def test_non_admitted_comments_cannot_enter_the_reviewed_report(self):
        with self.assertRaises(ValueError):
            r.apply_review(self.proposals, self.decisions, self.sources, set(), {'Ryu'})

    def test_review_preserves_source_only_identity_without_verifying_official_name(self):
        self.claim.update(character='Arjun',recommendation='削弱阿俊。')
        self.sources['a']['text_original']='阿俊不削我就退游。'
        self.decisions['a:1']['proposal_sha256']=r.proposal_hash(self.claim)
        accepted,_=r.apply_review(self.proposals,self.decisions,self.sources,{'a'},
                                 {e['canonical_name'] for e in r.character_reference()})
        self.assertEqual(len(accepted),1)
        self.assertIsNone(accepted[0]['character_identity']['canonical_name'])
        self.assertFalse(accepted[0]['source_review_required'])
        self.assertEqual(r.aggregate(accepted),[])


if __name__ == '__main__':
    unittest.main()
