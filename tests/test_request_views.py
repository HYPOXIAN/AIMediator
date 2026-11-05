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
from aimediator.common import read, sha
from aimediator.demo import demo
from aimediator.runner import Runner

# Keys a view holds only on some requests, which the offline demo does not send.
OCCASIONAL = {}


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
