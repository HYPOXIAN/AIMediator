"""Model-visible request views (pipeline upgrade plan 4.1, LNK-01): stages.view, MODEL_VISIBLE and the runner."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from support import case
from aimediator import stages
from aimediator.common import canonical, read, sha
from aimediator.config import defaults
from aimediator.demo import demo
from aimediator.evidence import character_candidates, character_reference, evidence_units
from aimediator.fixture_transport import FixtureTransport
from aimediator.operations import analyze
from aimediator.pipeline import quality_request
from aimediator.resources import asset_path
from aimediator.runner import Runner

# Keys a view holds only on some requests, which the offline demo does not send.
OCCASIONAL = {'quality': {'top': {'previous_attempt_errors'}}}


def demo_requests():
    """Return (stage, user message) of every request of the offline demo in its three modes."""
    with tempfile.TemporaryDirectory() as temp:
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            demo(Path(temp) / 'demo', quiet=True)
        return [(path.parent.parent.name, json.loads(read(path)['messages'][1]['content']))
                for path in sorted(Path(temp).glob('demo/*/requests/*/*/request.json'))]


class ModelVisibleKeys(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.requests = demo_requests()

    def test_every_demo_request_holds_only_model_visible_keys(self):
        # The demo's synthetic vectors queue no comment for retrieval review, whose
        # requests the pipeline builds as it builds relevance requests.
        self.assertEqual({stage for stage, _ in self.requests}, set(stages.MODEL_VISIBLE) - {'retrieval_review'})
        self.assertEqual(stages.MODEL_VISIBLE['retrieval_review'], stages.MODEL_VISIBLE['relevance'])
        seen = {stage: {'top': set(), 'comments': set()} for stage in stages.MODEL_VISIBLE}
        seen['retrieval_review'] = seen['relevance']
        for stage, message in self.requests:
            self.assertEqual(list(message)[-1], 'response_schema')
            top = set(message) - {'response_schema'}
            self.assertLessEqual(top, stages.MODEL_VISIBLE[stage]['top'], stage)
            seen[stage]['top'] |= top
            for comment in message.get('comments', []):
                self.assertLessEqual(set(comment), stages.MODEL_VISIBLE[stage]['comments'], stage)
                seen[stage]['comments'] |= set(comment)
        # The table lists no key that no request uses, apart from the occasional ones.
        for stage, keys in stages.MODEL_VISIBLE.items():
            for level in ('top', 'comments'):
                self.assertEqual(seen[stage][level] | OCCASIONAL.get(stage, {}).get(level, set()), keys[level],
                                 (stage, level))


class QualityView(unittest.TestCase):
    """Plan 4.1, UP-D04: no source row, contract or attempt; a repair attempt sees the previous errors."""

    def test_quality_view_keeps_the_comment_language_and_candidate_references(self):
        source = case('numeric_request')['source']
        data, context = quality_request(None, source, evidence_units(source['text_original']), 'en',
                                        {'run_identity': 'run'}, [])
        self.assertEqual(context, {'attempt': 1})
        self.assertEqual((data['source'], data['quality_contract'], data['attempt']), (source, {'run_identity': 'run'}, 1))
        visible = stages.view('quality', data, [source['record_id']])
        self.assertEqual(list(visible), ['comments', 'language', 'character_normalization_reference'])
        self.assertEqual(visible['comments'], [{'comment_id': source['record_id'],
                                                'units': evidence_units(source['text_original'])}])
        self.assertEqual(visible['language'], 'en')
        names = [e['canonical_name'] for e in visible['character_normalization_reference']]
        reference = character_reference(source['text_original'])
        self.assertEqual(names, character_candidates(source['text_original'], reference))
        self.assertTrue(names)
        self.assertLess(len(names), len(reference))
        self.assertEqual(visible['character_normalization_reference'],
                         [e for e in reference if e['canonical_name'] in names])

    def test_previous_attempt_errors(self):
        source = case('numeric_request')['source']
        data, _ = quality_request(None, source, evidence_units(source['text_original']), 'en', None, [])
        errors = ['%02d ' % i + 'x' * 400 for i in range(25)]
        visible = stages.view('quality', {**data, 'previous_attempt': {'errors': errors, 'transport_failure': False}},
                              [source['record_id']])
        self.assertEqual(list(visible)[-1], 'previous_attempt_errors')
        self.assertEqual(visible['previous_attempt_errors'], [e[:300] for e in errors[:20]])
        visible = stages.view('quality', {**data, 'previous_attempt': {'errors': ['URLError: remote text'],
                                                                       'transport_failure': True}},
                              [source['record_id']])
        self.assertEqual(visible['previous_attempt_errors'], ['transport failure'])

    def test_transport_failed_reads_the_journaled_response(self):
        with tempfile.TemporaryDirectory() as temp:
            runner = Runner('http://fixture.invalid', Path(temp), {})
            folder = Path(temp) / 'requests/quality'
            answers = {'model': ({'response': {'done': True, 'message': {'content': '{}'}}}, False),
                       'transport': ({'response': {'done': False, 'done_reason': 'transport_error',
                                                   'message': {'content': ''}, 'error': 'OSError: x'}}, True),
                       'envelope': ({'response': 'text'}, True), 'message': ({'response': {'message': 'x'}}, True)}
            for name, (response, _) in answers.items():
                (folder / name).mkdir(parents=True)
                (folder / name / 'response.json').write_text(json.dumps(response), encoding='utf-8')
            (folder / 'unreadable').mkdir()
            (folder / 'unreadable' / 'response.json').write_text('{', encoding='utf-8')
            for name, (_, failed) in answers.items():
                self.assertIs(runner.transport_failed('quality', name), failed, name)
            self.assertTrue(runner.transport_failed('quality', 'unreadable'))

    def test_repair_attempts_in_a_fixture_run(self):
        """Attempt 2 carries the validation errors of attempt 1, or 'transport failure' without remote text."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cases = read(asset_path('fixtures/cases.json'))
            (root / 'input.jsonl').write_bytes(b''.join(canonical(c['source']) + b'\n' for c in cases))
            cfg = defaults()
            cfg.update(evidence_quality='shadow', base_url='http://fixture.invalid')
            transport = FixtureTransport(cfg)
            original = transport.chat

            def chat(base, payload, partial):
                data = json.loads(payload['messages'][1]['content'])
                if 'segments' in payload['format']['properties'] and 'previous_attempt_errors' not in data:
                    comment = data['comments'][0]['comment_id']
                    if comment == 'synthetic:numeric_request:en':
                        return {'done': True, 'done_reason': 'stop', 'message': {'content': '{"comment_id": 1}'}}
                    if comment == 'synthetic:numeric_request:zh':
                        raise OSError('remote secret text')
                return original(base, payload, partial)
            transport.chat = chat
            with contextlib.redirect_stderr(io.StringIO()):
                analyze(root / 'input.jsonl', root / 'run', cfg, transport=transport, quiet=True)
            trace = [t for t in read(root / 'run/request-trace.json') if t['stage'] == 'quality']
            requests = {}
            for entry in trace:
                folder = root / 'run/requests/quality' / entry['request_id']
                message = json.loads(read(folder / 'request.json')['messages'][1]['content'])
                requests[entry['comment_id'], entry['attempt']] = (entry, message)
                self.assertNotIn('remote secret text', (folder / 'request.json').read_text(encoding='utf-8'))
            self.assertEqual(sorted(key for key in requests if key[1] == 2),
                             [('synthetic:numeric_request:en', 2), ('synthetic:numeric_request:zh', 2)])
            first, _ = requests['synthetic:numeric_request:en', 1]
            _, repair = requests['synthetic:numeric_request:en', 2]
            self.assertTrue(first['errors'])
            self.assertEqual(repair['previous_attempt_errors'], first['errors'])
            first, _ = requests['synthetic:numeric_request:zh', 1]
            entry, repair = requests['synthetic:numeric_request:zh', 2]
            self.assertTrue(any('remote secret text' in e for e in first['errors']))
            self.assertEqual(repair['previous_attempt_errors'], ['transport failure'])
            self.assertEqual(entry['errors'], [])
            for (_, attempt), (entry, message) in requests.items():
                self.assertFalse({'source', 'quality_contract', 'attempt'} & set(message))
                self.assertEqual('previous_attempt_errors' in message, attempt == 2)


class RunnerContext(unittest.TestCase):
    def runner(self, folder, answer, prompts=None):
        def chat(base, payload, partial):
            return {'done': True, 'done_reason': 'stop', 'message': {'content': json.dumps(answer)}}
        return Runner('http://fixture.invalid', folder, prompts or {'relevance': {'en': 'Review relevance'}},
                      chat_transport=chat)

    def test_request_context_enters_only_the_cache_identity(self):
        data = {'comments': [{'comment_id': 'c1', 'text': 'Ryu is too strong', 'retrieved_topics': []}]}
        with tempfile.TemporaryDirectory() as temp:
            runner = self.runner(Path(temp), {'decisions': ['related']})
            _, plain = runner.generate('m', 'en', 'relevance', data, ['c1'])
            _, none = runner.generate('m', 'en', 'relevance', data, ['c1'], request_context=None)
            _, first = runner.generate('m', 'en', 'relevance', data, ['c1'], request_context={'attempt': 1})
            _, second = runner.generate('m', 'en', 'relevance', data, ['c1'], request_context={'attempt': 2})
            request = read(Path(temp) / 'requests/relevance' / plain['request_id'] / 'request.json')
            self.assertEqual(plain['request_id'], none['request_id'])
            self.assertEqual(plain['request_id'], sha(json.dumps({**request, 'stream': False}, sort_keys=True,
                                                                 ensure_ascii=False).encode()))
            self.assertEqual(first['request_id'], sha(json.dumps({**request, 'stream': False,
                'request_context': {'attempt': 1}}, sort_keys=True, ensure_ascii=False).encode()))
            self.assertEqual(len({plain['request_id'], first['request_id'], second['request_id']}), 3)
            for meta in (first, second):
                self.assertEqual(read(Path(temp) / 'requests/relevance' / meta['request_id'] / 'request.json'),
                                 request)

    def test_verify_scope_reads_the_view(self):
        c = case('numeric_request')
        source = c['source']
        segment, point = c['annotation']['segments'][0], c['annotation']['information_points'][0]
        claim = {'character': 'Ryu', 'target': None, 'direction': 'nerf', 'recommendation': 'nerf Ryu',
                 'parameters': [], 'evidence': [{'evidence_id': 'E1', 'text': source['text_original']}],
                 'evidence_quality': {'selected_segments': [segment], 'selected_points': [point]}}
        data = {'claims': [{'claim_id': 'c:1', 'claim': claim}], 'original_comment': source['text_original']}
        with tempfile.TemporaryDirectory() as temp:
            runner = self.runner(Path(temp), {'support': 'supported'}, {'verify': {'en': 'Audit'}})
            parsed, meta = runner.generate('m', 'en', 'verify', data, ['c:1'])
        self.assertEqual(meta['errors'], [])
        self.assertEqual(parsed['verdicts'][0]['scope'], 'selected_quality_segments_with_original_context')


if __name__ == '__main__':
    unittest.main()
