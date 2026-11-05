"""Request shaping, options and response normalization of every model stage."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from support import case
from aimediator import evidence_quality, stages
from aimediator.evidence import evidence_units

STAGES = ('relevance', 'retrieval_review', 'quality', 'extract', 'verify')


def proposal(qualification=None):
    """Return a grounded-claim envelope for the numeric-request case, with fields the audit must not see."""
    source = case('numeric_request')['source']
    claim = {'character': 'Ryu', 'target': 'Hadoken damage', 'direction': 'nerf',
             'recommendation': 'Reduce Hadoken damage from 600 to 500', 'specificity': 'source_numeric',
             'parameters': [{'metric': 'Hadoken damage', 'current': '600', 'proposed': '500', 'delta': None,
                             'unit': None, 'evidence_id': 'E1'}],
             'evidence_ids': ['E1'], 'uncertain': False, 'source_review_required': True,
             'evidence': [{**u, 'comment_id': source['record_id'], 'source_url': source['source_url']}
                          for u in evidence_units(source['text_original'])]}
    if qualification:
        claim['evidence_quality'] = qualification
    return {'claim_id': source['record_id'] + ':1', 'comment_id': source['record_id'], 'model': 'm', 'claim': claim}


class View(unittest.TestCase):
    def test_returns_data_itself_except_for_verify(self):
        data = {'comments': [{'comment_id': 'a', 'units': []}]}
        for stage in STAGES[:-1]:
            self.assertIs(stages.view(stage, data, ['a']), data)

    def test_builds_the_verify_audit_view(self):
        entry = proposal()
        text = case('numeric_request')['source']['text_original']
        data = {'claims': [entry], 'original_comment': text}
        before = copy.deepcopy(data)
        view = stages.view('verify', data, [entry['claim_id']])
        self.assertEqual(data, before)
        self.assertEqual(list(view), ['original_evidence', 'proposed_claim', 'naming_reference', 'claim_id'])
        self.assertEqual(view['original_evidence'], text)
        self.assertEqual(view['claim_id'], entry['claim_id'])
        self.assertEqual(view['proposed_claim'], {
            'character': 'Ryu', 'target': 'Hadoken damage', 'direction': 'nerf',
            'recommendation': 'Reduce Hadoken damage from 600 to 500',
            'parameters': [{'metric': 'Hadoken damage', 'current': '600', 'proposed': '500', 'delta': None, 'unit': None}]})
        self.assertEqual(list(view['proposed_claim']), ['character', 'target', 'direction', 'recommendation', 'parameters'])
        self.assertEqual([e['canonical_name'] for e in view['naming_reference']], ['Ryu'])
        # Without the original comment, the audit sees the claim's evidence spans.
        spans = stages.view('verify', {'claims': [entry]}, [entry['claim_id']])
        self.assertEqual(spans['original_evidence'], '\n'.join(u['text'] for u in entry['claim']['evidence']))

    def test_adds_the_selected_quality_spans_to_the_verify_view(self):
        c = case('numeric_request')
        segment = c['annotation']['segments'][0]
        point = c['annotation']['information_points'][0]
        entry = proposal({'selected_segments': [segment], 'selected_points': [point],
                          'route': 'mechanism_evidence', 'mode': 'enforce'})
        view = stages.view('verify', {'claims': [entry], 'original_comment': c['source']['text_original']},
                              [entry['claim_id']])
        self.assertEqual(list(view), ['original_evidence', 'proposed_claim', 'naming_reference', 'claim_id',
                                      'selected_source_segments', 'selected_source_points'])
        self.assertEqual(view['selected_source_segments'], [{k: segment[k] for k in ('evidence_id', 'start', 'end', 'quote')}])
        self.assertEqual(list(view['selected_source_points'][0]),
                         ['point_id', 'segment_ids', 'character_literal', 'mechanic_literal', 'stance', 'direction'])
        self.assertEqual(view['selected_source_points'][0]['character_literal'], 'Ryu')


class Options(unittest.TestCase):
    def test_options_per_stage(self):
        small = '{"temperature": 0, "seed": 42, "num_ctx": 8192, "num_predict": 256}'
        for stage in ('relevance', 'retrieval_review', 'verify'):
            self.assertEqual(json.dumps(stages.options(stage, None)), small)
        self.assertEqual(json.dumps(stages.options('extract', {'num_predict': 7, 'num_ctx': 9})),
                         '{"temperature": 0, "seed": 42, "num_ctx": 8192, "num_predict": 4096}')
        self.assertEqual(json.dumps(stages.options('quality', {'num_predict': 7, 'num_ctx': 9})),
                         '{"temperature": 0, "seed": 42, "num_ctx": 9, "num_predict": 7}')
        policy = evidence_quality.load_policy()
        self.assertEqual(stages.options('quality', None), {'temperature': 0, 'seed': 42,
                         'num_ctx': policy['num_ctx'], 'num_predict': policy['num_predict']})
        first = stages.options('extract', None)
        first['num_gpu'] = 0
        self.assertNotIn('num_gpu', stages.options('extract', None))


class Normalize(unittest.TestCase):
    def test_relevance_and_retrieval_review_decisions(self):
        for stage in ('relevance', 'retrieval_review'):
            parsed, errors = stages.normalize(stage, {'decisions': ['related', 'uncertain', 'unrelated']},
                                              ['a', 'b', 'c'], {})
            self.assertEqual(errors, [])
            self.assertEqual(parsed, {'decisions': [
                {'comment_id': 'a', 'related': True, 'uncertain': False, 'reason': 'Ordered model status: related'},
                {'comment_id': 'b', 'related': False, 'uncertain': True, 'reason': 'Ordered model status: uncertain'},
                {'comment_id': 'c', 'related': False, 'uncertain': False, 'reason': 'Ordered model status: unrelated'}]})

    def test_quality_validates_the_annotation_against_the_source(self):
        c = case('numeric_request')
        row = c['source']
        data = {'comments': [{'comment_id': row['record_id'], 'units': evidence_units(row['text_original'])}],
                'source': row}
        annotation = c['annotation']
        parsed, errors = stages.normalize('quality', annotation, [row['record_id']], data)
        self.assertIs(parsed, annotation)
        self.assertEqual(errors, [])
        broken = copy.deepcopy(annotation)
        broken['segments'][0]['quote'] = broken['segments'][0]['quote'][:-1] + '?'
        parsed, errors = stages.normalize('quality', broken, [row['record_id']], data)
        self.assertIsNone(parsed)
        self.assertIn('Quote/offset mismatch: S1', errors)

    def test_verify_verdict_and_scope(self):
        parsed, errors = stages.normalize('verify', {'support': 'supported'}, ['c:1'], {'claim_id': 'c:1'})
        self.assertEqual(errors, [])
        self.assertEqual(parsed, {'verdicts': [{'claim_id': 'c:1', 'supported': True, 'support_status': 'supported',
            'scope': 'full_original_comment', 'reason': 'Model source-support status: supported'}]})
        for status in ('unsupported', 'uncertain'):
            parsed, errors = stages.normalize('verify', {'support': status}, ['c:1'],
                                              {'selected_source_segments': [{'evidence_id': 'E1'}]})
            verdict = parsed['verdicts'][0]
            self.assertEqual((verdict['supported'], verdict['support_status'], verdict['scope']),
                             (False, status, 'selected_quality_segments_with_original_context'))

    def test_extract_assessments_and_coverage(self):
        claim = {'character': 'Ryu'}
        response = {'assessments': {'a': {'claims': []}, 'b': {'claims': [claim]}}}
        parsed, errors = stages.normalize('extract', copy.deepcopy(response), ['a', 'b'], {})
        self.assertEqual(errors, [])
        self.assertEqual(parsed, {'assessments': [
            {'comment_id': 'a', 'claims': [], 'disposition': 'no_supported_character_claim'},
            {'comment_id': 'b', 'claims': [claim], 'disposition': 'extracted'}]})
        self.assertEqual(stages.normalize('extract', copy.deepcopy(response), ['a', 'b', 'c'], {}),
                         (None, ['Missing or duplicated item IDs']))


if __name__ == '__main__':
    unittest.main()
