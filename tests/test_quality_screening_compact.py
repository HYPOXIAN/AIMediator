"""Compact transport must reconstruct identical source-bound annotations or fail."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts/collect'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts/experiments'))
import evidence_quality as q
import run_balance_analysis as m
import run_quality_screening_recovery as recovery
from test_evidence_quality import CASES, case


def compact(annotation):
    grouped={}
    for s in annotation['segments']:
        grouped.setdefault(s['evidence_id'],[]).append({'id':s['segment_id'],'q':s['quote'],'s':s['scope'],
                        'k':s['content_kind'],'t':s['emotional_tone'],'r':s['reason_code']})
    return {'segments':grouped,
            'points':[{'i':p['segment_ids'],'s':p['scope'],'l':p['detail_level'],'a':p['stance'],
                       'd':p['direction'],'c':p['character_literal'],'m':p['mechanic_literal']} for p in annotation['information_points']]}


class CompactTests(unittest.TestCase):
    def test_bilingual_contract_roundtrips_preserve_routes_measurement_and_offsets(self):
        for c in CASES:
            with self.subTest(c=c['case_id']):
                units=m.evidence_units(c['source']['text_original'])
                expanded,errors=recovery.expand(compact(c['annotation']),c['source'],units)
                self.assertEqual(errors,[])
                expected=q.qualify(c['annotation'],c['source'],units)
                actual=q.qualify(expanded,c['source'],units)
                self.assertEqual(actual['routes_present'],expected['routes_present'])
                self.assertEqual(actual['emotion_ratio'],expected['emotion_ratio'])
                self.assertEqual(expanded['segments'],c['annotation']['segments'])

    def test_rewritten_quote_is_rejected(self):
        c=case('general');data=compact(c['annotation']);next(iter(data['segments'].values()))[0]['q']+=' invented'
        _,errors=recovery.expand(data,c['source'],m.evidence_units(c['source']['text_original']))
        self.assertTrue(errors)

    def test_ambiguous_quote_is_rejected(self):
        row={'record_id':'repeat','text_original':'Ryu Ryu'};units=m.evidence_units(row['text_original'])
        data={'segments':{units[0]['evidence_id']:[{'id':'S1','q':'Ryu','s':'uncertain','k':'uncertain','t':False,'r':'missing_context'}]},'points':[]}
        _,errors=recovery.expand(data,row,units)
        self.assertTrue(any('ambiguous' in e for e in errors))

    def test_missing_coverage_and_mismatched_point_types_remain_rejected(self):
        c=case('general');data=compact(c['annotation']);units=m.evidence_units(c['source']['text_original'])
        data['segments']={}
        self.assertTrue(recovery.expand(data,c['source'],units)[1])
        data=compact(c['annotation']);data['points'][0]['l']='concrete'
        self.assertTrue(any('detail conflict' in e for e in recovery.expand(data,c['source'],units)[1]))


if __name__=='__main__':unittest.main()
