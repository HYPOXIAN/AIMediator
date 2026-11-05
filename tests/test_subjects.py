"""Declared subjects of extraction answers and their program gate (plan 4.3, step U5.2, UP-D11)."""
import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import urllib.request
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import evidence, inference, stages
from aimediator.common import canonical, read
from aimediator.config import defaults
from aimediator.fixture_transport import FixtureTransport
from aimediator.operations import analyze
from aimediator.resources import asset_path
from aimediator.schema import schema_errors

GATE = 'Claim character not declared as subject'


def claim(character='Ken', evidence_id='E2'):
    return {'evidence_ids': [evidence_id], 'character': character, 'target': None, 'direction': 'nerf',
            'recommendation': 'Nerf %s.' % character, 'specificity': 'qualitative_only', 'parameters': [],
            'uncertain': False}


class SchemaTests(unittest.TestCase):
    def setUp(self):
        texts = {'one': 'Ken hits Ryu too hard. Please nerf Ken.', 'two': 'The netcode is bad.'}
        self.data = {'comments': [{'comment_id': k, 'units': evidence.evidence_units(t)} for k, t in texts.items()],
                     'character_normalization_reference': evidence.character_reference('\n'.join(texts.values()))}
        self.schema = stages.schema_for('extract', ['one', 'two'], self.data)

    def test_subjects_come_before_claims_and_list_the_allowed_characters(self):
        comments = self.schema['properties']['assessments']['properties']
        one, two = comments['one'], comments['two']
        self.assertEqual(list(one['properties']), ['subjects', 'claims'])
        self.assertEqual(one['required'], ['subjects', 'claims'])
        allowed = one['properties']['claims']['items']['properties']['character']['enum']
        self.assertEqual(one['properties']['subjects'], {'type': 'array', 'items': {'type': 'string', 'enum': allowed},
                                                         'uniqueItems': True, 'maxItems': len(allowed)})
        self.assertEqual(two['properties']['subjects']['maxItems'], 0)
        self.assertEqual(two['properties']['claims']['maxItems'], 0)
        bare = stages.schema_for('extract', ['one'])['properties']['assessments']['properties']['one']
        self.assertEqual(bare['properties']['subjects'], {'type': 'array', 'items': {'type': 'string'},
                                                          'uniqueItems': True})

    def test_schema_refuses_repeated_unknown_and_missing_subjects(self):
        def answer(subjects, claims=()):
            return {'assessments': {'one': {'subjects': subjects, 'claims': list(claims)},
                                    'two': {'subjects': [], 'claims': []}}}
        self.assertEqual(schema_errors(answer(['Ken'], [claim()]), self.schema), [])
        self.assertEqual(schema_errors(answer([]), self.schema), [])
        self.assertTrue(schema_errors(answer(['Ken', 'Ken'], [claim()]), self.schema))
        self.assertTrue(schema_errors(answer(['Guile']), self.schema))
        missing = answer(['Ken'])
        del missing['assessments']['one']['subjects']
        self.assertTrue(schema_errors(missing, self.schema))
        other = answer([])
        other['assessments']['two']['subjects'] = ['Ken']
        self.assertTrue(schema_errors(other, self.schema))

    def test_normalize_keeps_subjects(self):
        response = {'assessments': {'one': {'subjects': ['Ken'], 'claims': [claim()]},
                                    'two': {'subjects': [], 'claims': []}}}
        parsed, errors = stages.normalize('extract', copy.deepcopy(response), ['one', 'two'], self.data)
        self.assertEqual(errors, [])
        self.assertEqual([(a['comment_id'], a['subjects']) for a in parsed['assessments']],
                         [('one', ['Ken']), ('two', [])])


class LoopGuardTests(unittest.TestCase):
    """The loop guards still find the comment keys and the claims inside {subjects, claims}."""

    def stream(self, output, size=7):
        lines = [{'message': {'content': output[i:i + size]}, 'done': False} for i in range(0, len(output), size)]
        lines.append({'message': {'content': ''}, 'done': True, 'done_reason': 'stop'})
        ids = ['steam:1', 'steam:2']
        payload = {'model': 'fake', 'messages': [], 'stream': True, 'format': stages.schema_for('extract', ids)}
        body = io.BytesIO(b''.join(json.dumps(line).encode() + b'\n' for line in lines))
        with tempfile.TemporaryDirectory() as temp, patch.object(urllib.request, 'urlopen', return_value=body):
            return inference.streamed_chat('http://fixture.invalid', payload, Path(temp) / 'partial.txt')

    def test_guards_inside_subjects_and_claims(self):
        def output(one, two_key='steam:2'):
            return json.dumps({'assessments': {'steam:1': {'subjects': ['Ken'], 'claims': one}}})[:-2] + \
                ', "%s": {"subjects": [], "claims": []}}}' % two_key
        self.assertEqual(self.stream(output([claim(), claim('Ken', 'E3')]))['done_reason'], 'stop')
        self.assertEqual(self.stream(output([claim(), claim()]))['done_reason'], 'duplicate_claim_loop')
        self.assertEqual(self.stream(output([claim()], 'steam:1'))['done_reason'], 'duplicate_comment_loop')
        same = json.dumps({'assessments': {'steam:1': {'subjects': ['Ken'], 'claims': [claim()]},
                                           'steam:2': {'subjects': ['Ken'], 'claims': [claim()]}}})
        self.assertEqual(self.stream(same)['done_reason'], 'stop')


class PipelineGateTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        cases = read(asset_path('fixtures/cases.json'))
        self.input = self.root / 'input.jsonl'
        self.input.write_bytes(b''.join(canonical(c['source']) + b'\n' for c in cases))

    def run_with(self, mode, edit=None):
        cfg = defaults()
        cfg.update(evidence_quality=mode, base_url='http://fixture.invalid')
        transport = FixtureTransport(cfg)
        original, answers = transport.chat, []

        def chat(base, payload, partial):
            result = original(base, payload, partial)
            if 'assessments' in payload['format']['properties']:
                answer = json.loads(result['message']['content'])
                answers.append(answer)
                if edit:
                    edit(answer)
                    result = {**result, 'message': {'content': json.dumps(answer, ensure_ascii=False)}}
            return result
        transport.chat = chat
        run = self.root / (mode + ('-edited' if edit else ''))
        with contextlib.redirect_stderr(io.StringIO()):
            analyze(self.input, run, cfg, transport=transport, quiet=True)
        return run, answers

    def test_fixture_subjects_are_the_characters_of_its_claims(self):
        for mode in ('off', 'enforce'):
            run, answers = self.run_with(mode)
            assessments = [a for answer in answers for a in answer['assessments'].values()]
            self.assertTrue(any(a['claims'] for a in assessments))
            for a in assessments:
                self.assertEqual(a['subjects'], list(dict.fromkeys(c['character'] for c in a['claims'])))
            self.assertFalse([q for q in read(run / 'quarantined-claims.json') if GATE in q.get('errors', [])])

    def test_undeclared_character_is_quarantined_at_source_binding(self):
        dropped = []

        def edit(answer):
            for cid, a in answer['assessments'].items():
                if a['claims'] and not dropped:
                    dropped.append((cid, a['claims'][0]['character']))
                    a['subjects'] = [s for s in a['subjects'] if s != a['claims'][0]['character']]
        run, _ = self.run_with('off', edit)
        cid, character = dropped[0]
        gated = [q for q in read(run / 'quarantined-claims.json') if GATE in q.get('errors', [])]
        self.assertTrue(gated)
        self.assertTrue(all(q['stage'] == 'source_binding' and q['comment_id'] == cid
                            and q['claim']['character'] == character for q in gated))
        self.assertFalse([c for c in read(run / 'claims-before-audit.json')
                          if c['comment_id'] == cid and c['claim']['character'] == character])


if __name__ == '__main__':
    unittest.main()
