"""Failure-boundary checks for relevance gating and source-grounded quantities."""
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import evidence, evidence_quality, inference, pipeline, stages
from aimediator.common import strict_json
from aimediator.resources import asset_path
from aimediator.runner import Runner


def claim():
    return {'character': 'Ryu', 'target': 'Hadoken damage', 'direction': 'nerf',
            'recommendation': 'Reduce Hadoken damage from 600 to 500.',
            'specificity': 'source_numeric', 'parameters': [{'metric': 'damage',
                'current': '600', 'proposed': '500', 'delta': None, 'unit': None,
                'evidence_id': 'E1'}], 'evidence_ids': ['E1'], 'uncertain': False}


def row(text='Nerf Ryu Hadoken damage from 600 to 500.'):
    return {'record_id': 'steam:test', 'text_original': text, 'source_url': 'https://example.test/source'}


class BalanceEvidenceTests(unittest.TestCase):
    def test_two_stage_relevance_agreement_required(self):
        for retrieved in (True, False):
            for related in (True, False):
                for uncertain in (True, False):
                    self.assertEqual(pipeline.relevance_agrees({'retrieval_related': retrieved},
                        {'related': related, 'uncertain': uncertain}), retrieved and related and not uncertain)
        self.assertFalse(pipeline.relevance_agrees({'retrieval_related': True}, {}))

    def test_source_bound_numeric_request(self):
        errors, enriched = evidence.ground_claim(claim(), row(), {'Ryu'})
        self.assertEqual(errors, [])
        span = enriched['evidence'][0]
        self.assertEqual(span['text'], row()['text_original'][span['start']:span['end']])

    def test_decimal_and_chinese_offsets_remain_intact(self):
        text = ' 将隆的倍率从1.5改成1.2。\nKeep 2MK unchanged!😤'
        units = evidence.evidence_units(text)
        self.assertIn('1.5', units[0]['text'])
        self.assertIn('1.2', units[0]['text'])
        for unit in units:
            self.assertEqual(unit['text'], text[unit['start']:unit['end']])

    def test_fabricated_target_and_foreign_quote_are_rejected(self):
        for change in ('number', 'reference', 'character'):
            c = claim()
            if change == 'number': c['parameters'][0]['proposed'] = '450'
            if change == 'reference': c['evidence_ids'] = ['E999']
            if change == 'character': c['character'] = 'NotACharacter'
            self.assertTrue(evidence.ground_claim(c, row(), {'Ryu'})[0])

    def test_digit_substring_and_signed_values_do_not_pass(self):
        c = claim();c['parameters'][0]['proposed'] = '50'
        self.assertTrue(evidence.ground_claim(c, row(), {'Ryu'})[0])
        c = claim();c['recommendation'] = 'Make it +2 on block.'
        self.assertTrue(evidence.ground_claim(c, row('Nerf Ryu from -2 to -3.'), {'Ryu'})[0])

    def test_no_numbers_means_no_numeric_parameters(self):
        c = claim();c.update(target=None, recommendation='Nerf Ryu.', parameters=[], specificity='qualitative_only')
        self.assertEqual(evidence.ground_claim(c, row('Ryu is too strong.'), {'Ryu'})[0], [])
        c['specificity'] = 'source_numeric'
        self.assertTrue(evidence.ground_claim(c, row('Ryu is too strong.'), {'Ryu'})[0])

    def test_strict_json_rejects_duplicate_keys_nonfinite_and_fences(self):
        for raw in ('{"a":1,"a":2}', '{"a":NaN}', '```json\n{}\n```'):
            with self.assertRaises(ValueError): strict_json(raw)

    def test_schema_rejects_extra_fields_and_wrong_boolean(self):
        schema = stages.schema_for('relevance', ['one'])
        good = {'decisions': ['related']}
        self.assertEqual(evidence_quality.schema_errors(good, schema), [])
        bad = copy.deepcopy(good);bad['decisions'][0] = True
        self.assertTrue(evidence_quality.schema_errors(bad, schema))
        bad = copy.deepcopy(good);bad['untrusted_quote'] = 'fabricated'
        self.assertTrue(evidence_quality.schema_errors(bad, schema))

    def test_all_comment_ids_required_without_duplicates(self):
        self.assertFalse(stages.exact_coverage([{'comment_id': 'a'}, {'comment_id': 'a'}], 'comment_id', ['a', 'b']))
        self.assertTrue(stages.exact_coverage([{'comment_id': 'b'}, {'comment_id': 'a'}], 'comment_id', ['a', 'b']))

    def test_model_omission_and_incomplete_generation_fail_closed(self):
        for omit, done_reason in ((True, 'stop'), (False, 'length')):
            decisions = [] if omit else ['related']
            response = {'done': True, 'done_reason': done_reason,
                        'message': {'content': json.dumps({'decisions': decisions})}}
            with tempfile.TemporaryDirectory() as temp:
                runner = Runner('http://local.test', Path(temp), {'relevance': {'en': 'Review relevance'}},
                                  chat_transport=Mock(return_value=response))
                parsed, meta = runner.generate('fixture', 'en', 'relevance', {'comments': []}, ['a'])
                self.assertIsNone(parsed)
                self.assertTrue(meta['errors'])
                request = json.loads(next(Path(temp).rglob('request.json')).read_text(encoding='utf-8'))
                self.assertIn('response_schema', json.loads(request['messages'][1]['content']))

    def test_semantic_support_labels_are_explicit_and_bound_to_one_claim(self):
        source = row('Nerf Ryu Hadoken damage from 600 to 500. Keep the rest unchanged.')
        errors, enriched = evidence.ground_claim(claim(), source, {'Ryu'})
        self.assertEqual(errors, [])
        entry = {'claim_id': 'steam:test:1', 'comment_id': 'steam:test', 'model': 'fixture', 'claim': enriched}
        for status in ('supported', 'unsupported', 'uncertain'):
            response = {'done': True, 'done_reason': 'stop', 'message': {'content': json.dumps({'support': status})}}
            with tempfile.TemporaryDirectory() as temp:
                runner = Runner('http://local.test', Path(temp), {'verify': {'en': 'Assess source support'}},
                                  chat_transport=Mock(return_value=response))
                parsed, meta = runner.generate('fixture', 'en', 'verify',
                    {'claims': [entry], 'original_comment': source['text_original']}, ['steam:test:1'])
                self.assertEqual(meta['errors'], [])
                verdict = parsed['verdicts'][0]
                self.assertEqual(verdict['claim_id'], 'steam:test:1')
                self.assertEqual(verdict['supported'], status == 'supported')
                request = json.loads(next(Path(temp).rglob('request.json')).read_text(encoding='utf-8'))
                supplied = json.loads(request['messages'][1]['content'])
                self.assertEqual(supplied['original_evidence'], source['text_original'])
                self.assertNotIn('uncertain', supplied['proposed_claim'])
                self.assertNotIn('model', supplied['proposed_claim'])

    def test_semantic_audit_rejects_opaque_booleans_and_multiple_claims(self):
        self.assertTrue(evidence_quality.schema_errors({'support': True}, stages.schema_for('verify', ['a'])))
        with self.assertRaises(ValueError): stages.schema_for('verify', ['a', 'b'])

    def test_streaming_duplicate_comment_loop_is_interrupted(self):
        partial = '{"assessments":[{"comment_id":"a"},{"comment_id":"a"}'
        stream = io.BytesIO((json.dumps({'message': {'content': partial}, 'done': False}) + '\n').encode())
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'partial.txt'
            with patch.object(urllib.request, 'urlopen', return_value=stream):
                result = inference.streamed_chat('http://local.test', {'format': {'properties': {'assessments': {}}}}, path)
            self.assertEqual(result['done_reason'], 'duplicate_comment_loop')
            self.assertFalse(result['done'])
            self.assertEqual(path.read_text(encoding='utf-8'), partial)

    def test_streaming_whitespace_loop_is_interrupted(self):
        stream = io.BytesIO((json.dumps({'message': {'content': ' ' * 257}, 'done': False}) + '\n').encode())
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(urllib.request, 'urlopen', return_value=stream):
                result = inference.streamed_chat('http://local.test', {'format': {'properties': {}}}, Path(temp) / 'partial.txt')
        self.assertEqual(result['done_reason'], 'whitespace_loop')

    def test_claim_loop_detection_is_scoped_to_one_original_comment(self):
        same = {'assessments': {'a': {'claims': [claim(), claim()]}}}
        separate = {'assessments': {'a': {'claims': [claim()]}, 'b': {'claims': [claim()]}}}
        self.assertTrue(inference.repeated_claim(json.dumps(same), {'a', 'b'}, 'character'))
        self.assertFalse(inference.repeated_claim(json.dumps(separate), {'a', 'b'}, 'character'))

    def test_extraction_schema_requires_exact_number_of_assessments(self):
        schema = stages.schema_for('extract', ['a', 'b'])
        self.assertTrue(evidence_quality.schema_errors({'assessments': []}, schema))
        empty = {'subjects': [], 'claims': []}
        self.assertEqual(evidence_quality.schema_errors({'assessments': {'a': empty, 'b': empty}}, schema), [])
        self.assertTrue(evidence_quality.schema_errors({'assessments': {'a': empty}}, schema))

    def test_source_specific_character_constraints_block_system_inventions(self):
        reference = [{'canonical_name': 'Ryu', 'chinese_label': '隆', 'aliases': []},
                     {'canonical_name': 'Ken', 'chinese_label': '肯', 'aliases': []}]
        data = {'comments': [{'comment_id': 'a', 'units': evidence.evidence_units('Nerf Ryu.')},
                             {'comment_id': 'b', 'units': evidence.evidence_units('Drive Rush is too strong.')}],
                'character_normalization_reference': reference}
        schema = stages.schema_for('extract', ['a', 'b'], data)
        properties = schema['properties']['assessments']['properties']
        self.assertEqual(properties['a']['properties']['claims']['items']['properties']['character']['enum'], ['Ryu'])
        self.assertEqual(properties['a']['properties']['claims']['items']['properties']['evidence_ids']['items']['enum'], ['E1'])
        self.assertEqual(properties['a']['properties']['claims']['items']['properties']['parameters']['items']['properties']['evidence_id']['enum'], ['E1'])
        self.assertEqual(properties['b']['properties']['claims']['maxItems'], 0)
        self.assertEqual(evidence.character_candidates('taken', reference), [])
        self.assertEqual(evidence.character_candidates('隆太强了', reference), ['Ryu'])

    def test_aggregation_keeps_disagreement_and_unique_source_counts(self):
        claims = [{**claim(), 'comment_id': 'a'}, {**claim(), 'comment_id': 'a'},
                  {**claim(), 'comment_id': 'b', 'direction': 'buff'}]
        groups = pipeline.aggregate(claims)
        self.assertEqual(len(groups), 2)
        self.assertTrue(all(g['supporting_comment_count'] == 1 for g in groups))

    def test_chinese_number_words_preserved_and_checked(self):
        c = claim();c['recommendation'] = '将伤害降低一百。'
        c['parameters'] = [{'metric': '伤害', 'current': None, 'proposed': None,
                            'delta': '一百', 'unit': None, 'evidence_id': 'E1'}]
        self.assertEqual(evidence.ground_claim(c, row('请把隆的波动拳伤害降低一百。'), {'Ryu'})[0], [])
        c['parameters'][0]['delta'] = '两百'
        self.assertTrue(evidence.ground_claim(c, row('请把隆的波动拳伤害降低一百。'), {'Ryu'})[0])

    def test_quote_presence_is_not_a_semantic_truth_test(self):
        # Matching quantities alone now fail the conservative request-intent gate.
        errors, _ = evidence.ground_claim(claim(), row('Ryu did 600 damage; Ken did 500.'), {'Ryu'})
        self.assertTrue(any('intent' in error for error in errors))
        self.assertIn('past patch', asset_path('prompts/verify-balance.en.txt').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
