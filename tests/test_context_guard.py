"""Context guard (plan step U1.5, UP-D03): a response whose counters fill num_ctx fails validation."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator.common import canonical, read
from aimediator.config import defaults
from aimediator.fixture_transport import FixtureTransport
from aimediator.operations import analyze
from aimediator.resources import asset_path
from aimediator.runner import Runner


class RunnerContextTests(unittest.TestCase):
    def generate(self, **counters):
        with tempfile.TemporaryDirectory() as temp:
            def chat(base, payload, partial):
                content = '{"decisions": ["related"]}'
                return {'done': True, 'done_reason': 'stop', 'message': {'content': content}, **counters}
            runner = Runner('http://fixture.invalid', Path(temp), {'relevance': {'en': 'Review relevance'}},
                            chat_transport=chat)
            data = {'comments': [{'comment_id': 'c1', 'text': 'Ryu is too strong', 'retrieved_topics': []}]}
            parsed, meta = runner.generate('llama3.1:latest', 'en', 'relevance', data, ['c1'])
            request = read(next(Path(temp).rglob('request.json')))
            validation = read(next(Path(temp).rglob('validation.json')))
        self.assertEqual(request['options']['num_ctx'], 8192)
        self.assertEqual(validation['errors'], meta['errors'])
        return parsed, meta['errors']

    def test_counters_at_or_above_num_ctx_fail(self):
        for prompt, output in ((8000, 192), (8191, 1), (9000, 0), (4096, 4096)):
            parsed, errors = self.generate(prompt_eval_count=prompt, eval_count=output)
            self.assertIsNone(parsed)
            self.assertEqual(errors, ['Context window reached'])

    def test_counters_below_num_ctx_or_missing_pass(self):
        for counters in ({'prompt_eval_count': 8000, 'eval_count': 191}, {}, {'prompt_eval_count': 9000},
                         {'eval_count': 9000}, {'prompt_eval_count': None, 'eval_count': 9000},
                         {'prompt_eval_count': '8000', 'eval_count': 9000}, {'prompt_eval_count': True, 'eval_count': 8192}):
            parsed, errors = self.generate(**counters)
            self.assertEqual(errors, [], counters)
            self.assertIsNotNone(parsed)


class PipelineContextTests(unittest.TestCase):
    """The existing failure handling applies: extraction batches split, quality retries."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        cases = read(asset_path('fixtures/cases.json'))
        self.input = self.root / 'input.jsonl'
        self.input.write_bytes(b''.join(canonical(c['source']) + b'\n' for c in cases))

    def run_with(self, mode, full):
        """Run the fixture analysis; ``full(stage, data, payload)`` marks responses whose counters fill num_ctx."""
        cfg = defaults()
        cfg.update(evidence_quality=mode, base_url='http://fixture.invalid')
        transport = FixtureTransport(cfg)
        original = transport.chat

        def chat(base, payload, partial):
            result = original(base, payload, partial)
            stage = 'quality' if 'segments' in payload['format']['properties'] else \
                'extract' if 'assessments' in payload['format']['properties'] else 'other'
            if full(stage, json.loads(payload['messages'][1]['content']), payload):
                result = {**result, 'prompt_eval_count': payload['options']['num_ctx'] - 100, 'eval_count': 100}
            else:
                result = {**result, 'prompt_eval_count': 1000, 'eval_count': 100}
            return result
        transport.chat = chat
        run = self.root / mode
        with contextlib.redirect_stderr(io.StringIO()):
            analyze(self.input, run, cfg, transport=transport, quiet=True)
        return run, read(run / 'request-trace.json')

    def test_full_extraction_batch_splits(self):
        run, trace = self.run_with('off', lambda stage, data, payload: stage == 'extract' and len(data['comments']) > 1)
        extract = [entry for entry in trace if entry['stage'] == 'extract']
        failed = [entry for entry in extract if entry['errors']]
        self.assertTrue(failed)
        self.assertTrue(all(entry['errors'] == ['Context window reached'] for entry in failed))
        batches = {entry['request_id']: len(json.loads(read(run / 'requests/extract' / entry['request_id'] /
                   'request.json')['messages'][1]['content'])['comments']) for entry in extract}
        self.assertTrue(all(batches[entry['request_id']] > 1 for entry in failed))
        singles = [entry for entry in extract if batches[entry['request_id']] == 1]
        self.assertEqual(sum(batches[entry['request_id']] for entry in failed), len(singles))
        self.assertTrue(all(not entry['errors'] for entry in singles))
        coverage = read(run / 'full-pipeline-coverage.json')
        self.assertFalse([r for r in coverage if (r.get('extraction') or {}).get('disposition') == 'generation_failed'])

    def test_full_quality_attempt_is_retried(self):
        target = 'synthetic:numeric_request:zh'
        run, trace = self.run_with('shadow', lambda stage, data, payload: stage == 'quality'
                                   and 'previous_attempt_errors' not in data
                                   and data['comments'][0]['comment_id'].startswith(target))
        quality = [entry for entry in trace if entry['stage'] == 'quality' and entry['comment_id'].startswith(target)]
        self.assertEqual([(entry['attempt'], entry['errors']) for entry in quality],
                         [(1, ['Context window reached']), (2, [])])
        others = [entry for entry in trace if entry['stage'] == 'quality' and not entry['comment_id'].startswith(target)]
        self.assertTrue(others and all(entry['attempt'] == 1 and not entry['errors'] for entry in others))


if __name__ == '__main__':
    unittest.main()
