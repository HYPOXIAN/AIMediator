import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts/collect'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts/experiments'))
import evidence_quality as q
import run_balance_analysis as m
from evaluate_evidence_quality import evaluate,proportion,prepare_dataset
from support import case,qualified


def label(c,provenance='silver'):
    record=qualified(c)
    return {'comment_id':c['source']['record_id'],'language':c['source']['language'],
        'text_original':c['source']['text_original'],'content_sha256':record['content_sha256'],
        'cluster_id':c['cluster_id'],'split':'development','source_stage':'raw_pre_screen',
        'reviewer_type':provenance,'relevance':'related','segments':c['annotation']['segments'],
        'points':[dict(point_id=r['point_id'],route=r['route'],segment_ids=r['point']['segment_ids']) for r in record['routing'] if r['point_id']],
        'point_matches':[{'gold_point_id':r['point_id'],'predicted_point_id':r['point_id']} for r in record['routing'] if r['point_id']],
        'equivalence_group':None}


class QualityEvaluationTests(unittest.TestCase):
    def test_no_denominator_is_null_never_full_accuracy(self):
        self.assertIsNone(proportion(0,0)['value'])
        l=label(case('general'));score=evaluate([l],[qualified(case('general'))])['groups']['silver:development']['all']
        self.assertIsNone(score['mechanism_precision']['value'])
        self.assertIsNone(score['human_emotion_ratio_mae'])
        self.assertIsNone(score['human_emotion_span_recall']['value'])

    def test_missing_review_and_exclusion_are_recall_losses(self):
        c=case('numeric_request');l=label(c);l['point_matches']=[];r=qualified(c)
        for prediction in (None,{**r,'status':'failed','routes_present':['review'],'routing':[]}):
            out=evaluate([l],[prediction] if prediction else [])['groups']['silver:development']['all']
            self.assertEqual(out['mechanism_recall']['value'],0)
        r['routing']=[{'route':'exclude','point_id':None,'segments':c['annotation']['segments']}]
        out=evaluate([l],[r])['groups']['silver:development']['all']
        self.assertEqual(out['valid_mechanism_exclusion_rate']['value'],1)

    def test_spurious_mechanism_and_general_upgrades_penalized(self):
        c=case('general');l=label(c);r=qualified(c);r['routing'][0]['route']='mechanism_evidence'
        score=evaluate([l],[r])['groups']['silver:development']['all']
        self.assertEqual(score['mechanism_precision']['value'],0)
        self.assertEqual(score['general_opinion_upgrade_rate']['value'],1)
        self.assertEqual(score['mechanism_precision']['denominator'],1)
        self.assertIsNotNone(score['mechanism_precision']['wilson95'])

    def test_human_span_metrics_require_human_provenance_and_source_binding(self):
        c=case('high_emotion');l=label(c,'human');r=qualified(c)
        score=evaluate([l],[r])['groups']['human:development']['all']
        self.assertEqual(score['human_emotion_span_precision']['value'],1)
        self.assertEqual(score['human_emotion_ratio_mae'],0)
        l['segments'][0]['quote']='forged'
        with self.assertRaisesRegex(ValueError,'gold span'):evaluate([l],[r])

    def test_split_leak_and_source_hash_mismatch_rejected(self):
        a=label(case('general'));b=label(case('general','zh'));b['split']='test'
        with self.assertRaisesRegex(ValueError,'crosses'):evaluate([a,b],[])
        b=label(case('general','zh'));b['content_sha256']='wrong'
        with self.assertRaisesRegex(ValueError,'hash'):evaluate([b],[])

    def test_prepare_cluster_split_and_inspected_sources_forced_development(self):
        rows=[{'record_id':'a','text_original':'Ken is strong!','language':'en'},
              {'record_id':'b','text_original':'Ken is strong.','language':'en'},
              {'record_id':'c','text_original':'隆太强','language':'zh'}]
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'new'
            labels=prepare_dataset(rows,'raw_pre_screen',out,300,['a'])
            self.assertEqual(labels[0]['reviewer_type'],'unlabeled')
            duplicate=[l for l in labels if l['comment_id'] in ('a','b')]
            self.assertEqual({l['split'] for l in duplicate},{'development'})
            self.assertEqual(len({l['cluster_id'] for l in duplicate}),1)
            self.assertTrue(all(l['point_matches'] is None for l in labels))
            with self.assertRaises(ValueError):prepare_dataset(rows,'raw_pre_screen',out)


if __name__=='__main__':unittest.main()
