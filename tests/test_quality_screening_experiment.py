"""Offline partition/export checks; live experiment results are not test labels."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts/experiments'))
from aimediator import evidence, evidence_quality as q
from run_quality_screening_experiment import classify,export_results
from support import case,qualified


class ScreeningExperimentTests(unittest.TestCase):
    def test_frozen_rejection_and_uncertainty_are_separate(self):
        c=case('general');row=c['source']
        excluded=classify(row,{'agreement':False,'model_uncertain':False})
        review=classify(row,{'agreement':False,'model_uncertain':True})
        self.assertEqual(excluded['decision'],'excluded')
        self.assertEqual(review['decision'],'review')
        self.assertEqual(excluded['text_original'],row['text_original'])
        self.assertIsNone(excluded['quality_record'])

    def test_mixed_comment_retains_information_and_lists_removed_spans(self):
        c=case('price_and_opinion');result=classify(c['source'],{'agreement':True},qualified(c))
        self.assertEqual(result['decision'],'retained');self.assertTrue(result['partial'])
        self.assertEqual(len(result['retained_fragments']),1)
        self.assertEqual(len(result['excluded_fragments']),1)
        self.assertEqual(result['text_original'],c['source']['text_original'])
        self.assertEqual(result['retained_fragments'][0]['route'],'opinion_only')

    def test_failed_annotation_is_review_not_exclusion(self):
        c=case('numeric_request');r=q.failed_record(c['source'],evidence.evidence_units(c['source']['text_original']),
            [{'request_id':'failure','errors':['timeout']}])
        result=classify(c['source'],{'agreement':True},r)
        self.assertEqual(result['decision'],'review');self.assertEqual(result['quality_status'],'failed')

    def test_partition_counts_exactly_cover_inputs_and_fragments_remain_bound(self):
        cases=[case(cat) for cat in ('general','venting','me_too','price_and_opinion')]
        rows=[classify(c['source'],{'agreement':True},qualified(c)) for c in cases]
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);summary=export_results(folder,rows)
            self.assertEqual(summary['mutually_exclusive_comment_counts'],{'retained':2,'excluded':1,'review':1})
            saved=json.loads((folder/'retained-comments.json').read_text(encoding='utf-8'))
            self.assertEqual(len(saved),2)
            for row in saved:
                for item in row['retained_fragments']:
                    for s in item['segments']:
                        self.assertEqual(s['quote'],row['text_original'][s['start']:s['end']])
            self.assertTrue((folder/'retained-comments.md').exists())
            self.assertEqual(sum(1 for line in (folder/'retained-comments.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()),2)


if __name__=='__main__':unittest.main()
