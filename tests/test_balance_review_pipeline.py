"""Regression boundaries from the full-corpus source review and evaluation split."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import run_balance_analysis as m
from balance_policy import numeric_request_supported,triage_retrieval,direction_action_conflicts,attributed_candidates
from evaluate_balance_review import read_labels,calibrate,relevance_metrics
from prepare_balance_design import prepare_briefs,validate_move_data
from run_balance_regression_live import CASES
from export_balance_review_followups import followups

ROOT=Path(__file__).resolve().parents[1]

def proposal():
    return {'character':'Ryu','target':'Hadoken damage','direction':'nerf','recommendation':'Reduce Hadoken damage from 600 to 500.',
        'specificity':'source_numeric','parameters':[{'metric':'damage','current':'600','proposed':'500','delta':None,'unit':None,'evidence_id':'E1'}],
        'evidence_ids':['E1'],'uncertain':False}

class ReviewPipelineTests(unittest.TestCase):
    def test_cosmetic_scope_exclusion_does_not_hide_a_real_buff_request(self):
        for text,expected in [('Drive Impact is unfair. Elena looks great; where is Makoto?',[]),
                              ('Elena looks great; please buff Elena.',['Elena'])]:
            reference=m.character_reference(text);raw=m.character_candidates(text,reference)
            allowed,_=attributed_candidates(text,reference,raw)
            self.assertEqual(allowed,expected)

    def test_explicit_victim_exclusion_preserves_independent_victim_feedback(self):
        for text,expected in [('你阿俊一招给我老桑打半管白血。',['Arjun']),
                              ('你阿俊一招给我老桑打半管白血。加强老桑。',['Zangief','Arjun'])]:
            reference=m.character_reference(text);raw=m.character_candidates(text,reference)
            allowed,_=attributed_candidates(text,reference,raw)
            self.assertEqual(allowed,expected)

    def test_live_manifest_cases_survive_json_round_trip_for_resume(self):
        self.assertEqual(json.loads(json.dumps(CASES)),CASES)
        labels=[json.loads(line) for line in (ROOT/'data/evaluation/balance-silver-v1/labels.jsonl').read_text().splitlines()]
        development={r['comment_id'] for r in labels if r['split']=='development'}
        self.assertTrue({c['comment_id'] for c in CASES}<=development)

    def test_nationality_alone_never_resolves_dhalsim(self):
        for text in ['印度人怎么这么赖','阿三不削我就退游','三哥白血太强了','Indian guy is too strong']:
            self.assertNotIn('Dhalsim',m.character_candidates(text,m.character_reference(text)))
        text='达尔西姆太强了，印度人';self.assertIn('Dhalsim',m.character_candidates(text,m.character_reference(text)))

    def test_source_literal_kept_without_official_identity_or_grouping(self):
        text='阿俊不削等着所有人退游吧';c=proposal();c.update(character='Arjun',target=None,recommendation='降低阿俊整体强度。',specificity='qualitative_only',parameters=[])
        errors,enriched=m.ground_claim(c,{'record_id':'fixture','text_original':text}, {'Arjun'})
        self.assertFalse(errors);self.assertIsNone(enriched['character_identity']['canonical_name'])
        self.assertEqual(enriched['character_identity']['source_literal'],'阿俊')
        self.assertEqual(m.aggregate([{**enriched,'comment_id':'fixture'}]),[])

    def test_wrong_dhalsim_assignment_blocked_in_named_arjun_source(self):
        c=proposal();c.update(character='Dhalsim',recommendation='Nerf Dhalsim.',specificity='qualitative_only',parameters=[])
        errors,_=m.ground_claim(c,{'record_id':'fixture','text_original':'阿俊的白血太强，阿三重做吧。'}, {'Dhalsim'})
        self.assertTrue(any('identity' in e for e in errors))

    def test_numeric_coincidence_fails_both_languages(self):
        for text in ["Ryu's Hadoken deals 600 damage; Ken's Hadoken deals 500 damage.",'隆的波动拳伤害为600，肯的波动拳伤害为500。']:
            self.assertFalse(numeric_request_supported(text,proposal()['parameters'][0]))

    def test_generation_schema_cannot_invent_derived_delta_or_unstated_units(self):
        text="Please reduce Ryu's Hadoken damage from 600 to 500."
        data={'comments':[{'comment_id':'a','units':m.evidence_units(text)}],
              'character_normalization_reference':m.character_reference(text)}
        schema=m.schema_for('extract',['a'],data)
        properties=schema['properties']['assessments']['properties']['a']['properties']['claims']['items']['properties']['parameters']['items']['properties']
        self.assertEqual(properties['delta']['enum'],[None]);self.assertEqual(properties['unit']['enum'],[None])
        self.assertEqual(properties['proposed']['enum'],[None,'600','500'])
        text='请将隆的伤害降低100点。'
        data['comments'][0]['units']=m.evidence_units(text)
        p=m.schema_for('extract',['a'],data)['properties']['assessments']['properties']['a']['properties']['claims']['items']['properties']['parameters']['items']['properties']
        self.assertIn('100',p['delta']['enum']);self.assertIn('点',p['unit']['enum'])

    def test_explicit_requests_survive_without_inventing_values(self):
        for text in ['Please reduce Ryu Hadoken damage from 600 to 500.','请将隆的波动拳伤害从600降到500。']:
            self.assertTrue(numeric_request_supported(text,proposal()['parameters'][0]))
        self.assertTrue(numeric_request_supported('给一键指令加5帧发生时间更合理。',{'proposed':None,'delta':'5'}))

    def test_past_patch_and_negated_numeric_actions_require_review(self):
        for text in ['Last patch we reduced Ryu from 600 to 500.','不要把隆的伤害从600降低到500。','上个版本已经将隆伤害从600改为500。']:
            self.assertFalse(numeric_request_supported(text,proposal()['parameters'][0]))

    def test_far_negative_explicit_request_is_only_queued(self):
        row={'positive_score':.1,'negative_score':.9,'retrieval_related':False}
        status,reasons=triage_retrieval(row,'请给一键指令加5帧发生。',.08)
        self.assertEqual(status,'review_queue');self.assertIn('explicit_numeric_request',reasons)
        row['retrieval_triage']=status;review={'related':True,'uncertain':False}
        self.assertFalse(m.relevance_agrees(row,review))
        row.update(retrieval_review_related=True,retrieval_review_uncertain=False)
        self.assertTrue(m.relevance_agrees(row,review))
        self.assertFalse(m.relevance_agrees(row,{'related':True,'uncertain':True}))

    def test_borderline_nomination_does_not_count_as_admission(self):
        row={'positive_score':.49,'negative_score':.50,'retrieval_related':False}
        self.assertEqual(triage_retrieval(row,'Nice costumes.',.02)[0],'review_queue')
        self.assertFalse(m.relevance_agrees(row,{'related':True,'uncertain':False}))

    def test_disagreement_export_preserves_source_without_overriding_admission(self):
        sources=[{'record_id':'a','text_original':'Drive Rush is unfair.'},
                 {'record_id':'b','text_original':'Nice music.'},
                 {'record_id':'c','text_original':'阿俊太强了。'}]
        decisions=[{'comment_id':'a','agreement':False,'retrieval_related':True,'model_related':False},
                   {'comment_id':'b','agreement':False,'retrieval_related':False,'retrieval_triage':'unrelated'},
                   {'comment_id':'c','agreement':True,'retrieval_related':True,'model_related':True}]
        out=followups(decisions,sources);self.assertEqual(out['total'],2)
        self.assertFalse(out['decision_overrides']);a,c=out['items']
        self.assertEqual(a['review_scope'],['relevance']);self.assertFalse(a['admitted_for_extraction'])
        self.assertEqual(a['original_text'],sources[0]['text_original'])
        self.assertEqual(c['review_scope'],['identity']);self.assertTrue(c['admitted_for_extraction'])

    def test_metrics_count_missing_and_exclude_uncertain(self):
        labels=[{'comment_id':'a','relevance':'related'},{'comment_id':'b','relevance':'unrelated'},{'comment_id':'c','relevance':'uncertain'}]
        result=relevance_metrics(labels,{'b':True})
        self.assertEqual(result['missing_predictions'],1);self.assertEqual(result['false_negative'],1)
        self.assertEqual(result['false_positive'],1);self.assertEqual(result['excluded_uncertain'],1)

    def test_calibration_does_not_read_holdout_labels(self):
        labels=[{'comment_id':'a','split':'development','relevance':'related'},{'comment_id':'b','split':'holdout','relevance':'related'}]
        retrieval=[{'comment_id':'a','positive_score':.49,'negative_score':.5},{'comment_id':'b','positive_score':.1,'negative_score':.9}]
        sources=[{'record_id':'a','text_original':'balance bad'},{'record_id':'b','text_original':'price bad'}]
        before=calibrate(labels,retrieval,sources);labels[1]['relevance']='unrelated'
        self.assertEqual(before,calibrate(labels,retrieval,sources));self.assertFalse(before['holdout_used'])
        self.assertEqual(before['development_comment_ids'],['a'])

    def test_silver_set_is_frozen_and_disjoint(self):
        folder=ROOT/'data/evaluation/balance-silver-v1';manifest=json.loads((folder/'manifest.json').read_text())
        raw=(folder/'labels.jsonl').read_bytes();self.assertEqual(m.digest(raw),manifest['labels_sha256'])
        labels=[json.loads(s) for s in raw.decode().splitlines()]
        dev={r['comment_id'] for r in labels if r['split']=='development'};hold={r['comment_id'] for r in labels if r['split']=='holdout'}
        self.assertEqual((len(dev),len(hold)),(70,30));self.assertFalse(dev&hold)
        self.assertTrue(all(r['reviewer_type']=='agent' and r['reason'] for r in labels))
        self.assertFalse(manifest['independent_human_gold'])

    def test_regression_fixtures_keep_exact_original_hash_bindings(self):
        folder=ROOT/'data/evaluation/balance-regressions-v1'
        raw=(folder/'cases.json').read_bytes();cases=json.loads(raw)
        manifest=json.loads((folder/'manifest.json').read_text())
        self.assertEqual(m.digest(raw),manifest['cases_sha256'])
        for case in cases:
            self.assertEqual(m.digest(case['source']['text_original'].encode()),manifest['source_hashes'][case['case_id']])
        self.assertEqual(len(cases),12);self.assertEqual(len({c['case_id'] for c in cases}),12)
        self.assertTrue(all(c['reviewer_type']=='agent' and c['expected_original_supported'] is False for c in cases))
        categories={c['category'] for c in cases}
        self.assertTrue({'attacker_victim_reversal','universal_system_scope','numeric_example_leak','direction_action_contradiction'}<=categories)

    def test_direction_action_reversals_blocked_without_guessing_frame_effects(self):
        c=proposal();c.update(recommendation='Strengthen Ryu.',direction='nerf')
        self.assertTrue(direction_action_conflicts(c))
        c.update(recommendation='加强隆。',direction='nerf');self.assertTrue(direction_action_conflicts(c))
        c.update(recommendation='Reduce uppercut startup from 8 to 6 frames.',direction='buff')
        self.assertFalse(direction_action_conflicts(c))

    def test_design_never_manufactures_missing_move_data(self):
        c={**proposal(),'claim_id':'a:1','comment_id':'a','source_review':{'decision':'accept'}}
        out=prepare_briefs([c]);self.assertEqual(out['summary']['blocked'],1)
        b=out['briefs'][0];self.assertIn('target_patch_required',b['blockers'])
        self.assertEqual(b['engineering_hypotheses'],[]);self.assertEqual(b['source_request'],c)

    def test_addressee_only_text_is_not_an_engineering_action(self):
        c={**proposal(),'recommendation':'Capcom','claim_id':'a:1','comment_id':'a','source_review':{'decision':'accept'}}
        self.assertIn('engineering_action_text_required',prepare_briefs([c])['briefs'][0]['blockers'])

    def test_known_label_disputes_block_design(self):
        c={**proposal(),'claim_id':'a:1','comment_id':'a','source_review':{'decision':'accept'}}
        self.assertIn('source_annotation_adjudication_required',prepare_briefs([c],pending_adjudication_ids={'a'})['briefs'][0]['blockers'])

    def test_versioned_design_matching_and_source_review_are_both_required(self):
        c={**proposal(),'claim_id':'a:1','comment_id':'a','source_review':{'decision':'accept'}}
        data=[{'character':'Ryu','target':'Hadoken damage','patch_version':'synthetic-patch','metric':'damage','current':'600','unit':'points','source_url':'https://example.test/fixture','verified':True}]
        out=prepare_briefs([c],data,'synthetic-patch');self.assertEqual(out['summary']['ready'],1)
        self.assertEqual(out['briefs'][0]['release_status'],'not_approved_for_game_changes')
        self.assertEqual(prepare_briefs([c],data,'other-patch')['summary']['ready'],0)
        del c['source_review'];self.assertEqual(prepare_briefs([c],data,'synthetic-patch')['summary']['ready'],0)

    def test_move_data_requires_verification_provenance_and_unique_key(self):
        with self.assertRaises(ValueError):validate_move_data([{'current':'600'}])
        data={'character':'Ryu','target':'damage','patch_version':'fixture','metric':'damage','current':'600','unit':'points','source_url':'https://example.test','verified':True}
        with self.assertRaises(ValueError):validate_move_data([data,data])
        data['verified']=False
        with self.assertRaises(ValueError):validate_move_data([data])


if __name__=='__main__':unittest.main()
