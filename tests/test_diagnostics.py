"""The shared live diagnostic loop (aimediator.diagnostics) with a fake chat transport, offline."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import diagnostics, evidence_quality
from aimediator.evidence import character_reference, evidence_units, ground_claim
from aimediator.runner import Runner
from aimediator.stages import schema_for, view
from support import case, qualified

PROMPTS = {'extract': {'en': 'fixture extract prompt'}, 'verify': {'en': 'fixture verify prompt'}}
TEXT = "Please reduce Ryu's Hadoken damage from 600 to 500."
ROW = {'record_id': 'fixture:1', 'text_original': TEXT, 'source_url': None}


def numeric_claim(**changes):
    claim = {'character': 'Ryu', 'target': 'Hadoken damage', 'direction': 'nerf',
             'recommendation': 'Reduce Hadoken damage from 600 to 500.', 'specificity': 'source_numeric',
             'parameters': [{'metric': 'damage', 'current': '600', 'proposed': '500', 'delta': None,
                             'unit': None, 'evidence_id': 'E1'}],
             'evidence_ids': ['E1'], 'uncertain': False}
    claim.update(changes)
    return claim


class FakeChat:
    """Answer extraction with fixed claims and every audit with "supported"; keep each payload."""

    def __init__(self, claims=()):
        self.claims = list(claims)
        self.payloads = []

    def __call__(self, base, payload, partial_path):
        self.payloads.append(payload)
        data = json.loads(payload['messages'][1]['content'])
        if 'support' in payload['format']['properties']:
            result = {'support': 'supported'}
        else:
            result = {'assessments': {data['comments'][0]['comment_id']: {'subjects': list(dict.fromkeys(c['character'] for c in self.claims)),
                                                                   'claims': self.claims}}}
        return {'done': True, 'done_reason': 'stop', 'message': {'content': json.dumps(result)}}

    def stage_payloads(self, key):
        return [p for p in self.payloads if key in p['format']['properties']]


class DiagnosticsTests(unittest.TestCase):
    def runner(self, chat, prompts=PROMPTS):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        return Runner('http://fixture.invalid', Path(folder.name), prompts, chat_transport=chat)

    def test_extract_sends_the_scripts_request_data(self):
        allowed = evidence_quality.allowed_points(qualified(case('numeric_request')))
        for allowed_points in (None, allowed):
            chat = FakeChat([numeric_claim()])
            parsed, meta = diagnostics.extract(self.runner(chat), 'fixture-model', 'en', ROW,
                                               allowed_points=allowed_points)
            # The data the live scripts built inline, in their key order; the model sees its
            # extraction view (pipeline upgrade step U2.3) and the schema the full data gives.
            comment = {'comment_id': 'fixture:1', 'units': evidence_units(TEXT)}
            if allowed_points is not None:
                comment['allowed_quality_points'] = allowed_points
            data = {'comments': [comment], 'character_normalization_reference': character_reference(TEXT)}
            visible = view('extract', data, ['fixture:1'])
            expected = json.dumps({**visible, 'response_schema': schema_for('extract', ['fixture:1'], data)},
                                  ensure_ascii=False)
            [payload] = chat.payloads
            self.assertEqual(payload['messages'][1]['content'], expected)
            self.assertEqual(visible['comments'][0]['units'], [{'evidence_id': 'E1', 'text': TEXT}])
            self.assertEqual([e['canonical_name'] for e in visible['character_normalization_reference']], ['Ryu'])
            if allowed_points is not None:
                self.assertEqual(list(visible['comments'][0]['allowed_quality_points'][0]),
                                 ['point_id', 'evidence_ids', 'quotes', 'scope', 'detail_level', 'stance',
                                  'direction', 'character_literal', 'mechanic_literal'])
            self.assertEqual(payload['messages'][0]['content'], 'fixture extract prompt')
            self.assertEqual(sorted(meta), ['elapsed_seconds', 'errors', 'request_id'])
            if allowed_points is None:
                self.assertEqual(parsed['assessments'][0]['claims'], [numeric_claim()])
            else:
                # The fake omits quality_point_ids, which the allowed points make required.
                self.assertIsNone(parsed)
                self.assertTrue(meta['errors'])

    def test_audit_verifies_only_claims_without_errors(self):
        chat = FakeChat()
        claims = [numeric_claim(), numeric_claim(recommendation='Reduce Hadoken damage to 999.')]
        records = diagnostics.audit(self.runner(chat), 'fixture-model', 'en', ROW, claims, {'Ryu'})
        self.assertEqual([list(r) for r in records],
                         [['index', 'claim', 'enriched', 'errors', 'audit', 'audit_meta']] * 2)
        good, bad = records
        self.assertEqual((good['index'], bad['index']), (1, 2))
        self.assertIs(good['claim'], claims[0])
        self.assertEqual(good['errors'], [])
        self.assertEqual(good['enriched'], ground_claim(claims[0], ROW, {'Ryu'})[1])
        self.assertEqual(good['audit']['claim_id'], 'fixture:1:1')
        self.assertIs(good['audit']['supported'], True)
        self.assertEqual(sorted(good['audit_meta']), ['elapsed_seconds', 'errors', 'request_id'])
        self.assertIn('Unsupported number in recommendation or target', bad['errors'])
        self.assertIsNotNone(bad['enriched'])
        self.assertIsNone(bad['audit'])
        self.assertIsNone(bad['audit_meta'])
        [payload] = chat.stage_payloads('support')
        sent = json.loads(payload['messages'][1]['content'])
        self.assertEqual((sent['claim_id'], sent['original_evidence']), ('fixture:1:1', TEXT))

    def test_audit_request_bytes_equal_the_inline_envelope(self):
        # The live scripts sent verify envelopes with and without a model key;
        # only the claim, the original comment and the claim ID reach the request.
        chat = FakeChat()
        diagnostics.audit(self.runner(chat), 'fixture-model', 'en', ROW, [numeric_claim()], {'Ryu'})
        enriched = ground_claim(numeric_claim(), ROW, {'Ryu'})[1]
        envelope = {'claim_id': 'fixture:1:1', 'comment_id': 'fixture:1', 'model': 'fixture-model',
                    'claim': enriched}
        inline = FakeChat()
        self.runner(inline).generate('fixture-model', 'en', 'verify',
                                     {'claims': [envelope], 'original_comment': TEXT}, ['fixture:1:1'])
        self.assertEqual(chat.payloads, inline.payloads)

    def test_audit_binds_claims_to_a_quality_record(self):
        c = case('numeric_request')
        row, record = c['source'], qualified(c)
        claims = [numeric_claim(quality_point_ids=['P1']), numeric_claim(quality_point_ids=['P999'])]
        chat = FakeChat()
        records = diagnostics.audit(self.runner(chat), 'fixture-model', 'en', row, copy.deepcopy(claims),
                                    {'Ryu'}, quality_record=record)
        bound, foreign = records
        self.assertEqual(bound['errors'], [])
        self.assertEqual(bound['enriched']['evidence_quality']['route'], 'mechanism_evidence')
        self.assertIs(bound['audit']['supported'], True)
        self.assertTrue(foreign['errors'])
        self.assertIn('evidence_quality', foreign['enriched'])
        self.assertIsNone(foreign['audit'])
        [payload] = chat.stage_payloads('support')
        self.assertIn('selected_source_points', json.loads(payload['messages'][1]['content']))
        # Without a quality record, the same claims are grounded only.
        plain = diagnostics.audit(self.runner(FakeChat()), 'fixture-model', 'en', row, copy.deepcopy(claims),
                                  {'Ryu'})
        self.assertEqual([r['errors'] for r in plain], [[], []])
        self.assertNotIn('evidence_quality', plain[0]['enriched'])


if __name__ == '__main__':
    unittest.main()
