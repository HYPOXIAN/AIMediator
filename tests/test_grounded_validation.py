import copy
import importlib.util
import json
from pathlib import Path
import unittest

SPEC=importlib.util.spec_from_file_location('grounded',Path(__file__).resolve().parents[1]/'scripts/experiments/test_grounded_feedback.py')
m=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


def case(text='Please buff Ingrid.'):
    return {'comment_id':'steam:fixture','language':'en','text':text,'kind':'real_review','character_candidates':['Ingrid'],'units':m.evidence_units(text),'expectations':{'must_have_claim':True,'characters':['Ingrid'],'directions':['buff']}}


def output():
    return {'comment_id':'steam:fixture','language':'en','claims':[{'character':'Ingrid','mechanic':None,'direction':'buff','reason':'The player requests a buff for Ingrid.','evidence_id':'E1','uncertain':False}],'emotional_tone':'neutral'}


class GroundedExtractionTests(unittest.TestCase):
    def check_rejected(self,obj,source=None):
        checks,parsed,validated=m.validate(json.dumps(obj),source or case())
        self.assertFalse(checks['accepted_for_human_review'])
        self.assertIsNone(validated)
        return checks

    def test_valid_output_quotes_only_original_span(self):
        checks,parsed,validated=m.validate(json.dumps(output()),case())
        self.assertTrue(checks['accepted_for_human_review'])
        claim=validated['claims'][0]
        self.assertEqual(claim['evidence'],case()['text'][claim['evidence_start']:claim['evidence_end']])
        self.assertNotIn('evidence',parsed['claims'][0])

    def test_fabricated_review_id_is_rejected(self):
        obj=output();obj['comment_id']='steam:nonexistent'
        self.assertFalse(self.check_rejected(obj)['identity_matches'])

    def test_extra_invented_review_array_is_rejected(self):
        obj=output();obj['reviews']=[{'text':'invented'}]
        self.assertFalse(self.check_rejected(obj)['schema_valid'])

    def test_model_written_quote_cannot_replace_source_quote(self):
        obj=output();obj['claims'][0]['evidence']='The reviewer never wrote this.'
        self.assertFalse(self.check_rejected(obj)['schema_valid'])

    def test_nonexistent_evidence_reference_is_rejected(self):
        obj=output();obj['claims'][0]['evidence_id']='E999'
        self.assertFalse(self.check_rejected(obj)['evidence_references_valid'])

    def test_unsupported_character_is_rejected(self):
        obj=output();obj['claims'][0]['character']='Ryu'
        self.assertFalse(self.check_rejected(obj)['character_candidates_valid'])

    def test_unsupported_numerical_recommendation_is_rejected(self):
        obj=output();obj['claims'][0]['reason']='Increase her damage by 50%.'
        self.assertFalse(self.check_rejected(obj)['numbers_supported_by_evidence'])

    def test_wrong_scalar_types_are_rejected(self):
        obj=output();obj['claims'][0]['uncertain']='false'
        self.assertFalse(self.check_rejected(obj)['schema_valid'])

    def test_invalid_json_and_markdown_fences_are_rejected(self):
        for raw in ['not JSON','```json\n'+json.dumps(output())+'\n```']:
            checks,parsed,validated=m.validate(raw,case())
            self.assertFalse(checks['json_valid']);self.assertIsNone(validated)

    def test_empty_input_cannot_support_any_claim(self):
        empty=case('');empty['kind']='empty_control'
        self.assertFalse(self.check_rejected(output(),empty)['empty_input_abstention'])
        obj=output();obj['claims']=[]
        checks,parsed,validated=m.validate(json.dumps(obj),empty)
        self.assertTrue(checks['accepted_for_human_review'])

    def test_incomplete_generation_is_quarantined(self):
        checks,parsed,validated=m.validate(json.dumps(output()),case(),done=False)
        self.assertFalse(checks['generation_complete']);self.assertIsNone(validated)

    def test_chinese_and_emoji_offsets_preserve_exact_text(self):
        text=' 太难了！现代模式不应该少了20%的伤害😤\n别削弱火舞了。'
        for unit in m.evidence_units(text):
            self.assertEqual(unit['text'],text[unit['start']:unit['end']])
        self.assertEqual(len(m.evidence_units(text)),3)

    def test_exact_quote_alone_does_not_prove_semantic_entailment(self):
        obj=output();obj['claims'][0]['reason']='Ingrid should receive invulnerability.'
        checks,parsed,validated=m.validate(json.dumps(obj),case())
        self.assertTrue(checks['accepted_for_human_review'])
        self.assertIsNotNone(validated)


if __name__=='__main__':
    unittest.main()
