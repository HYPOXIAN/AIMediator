"""Shared response cache across runs (plan 4.6, U3.3, UP-D09)."""
import contextlib
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator.cache import SharedCache, chat_key, storable
from aimediator.common import Failure, canonical, read
from aimediator.config import defaults, resolve, validate
from aimediator.fixture_transport import FixtureTransport
from aimediator.measurement import request_metrics
from aimediator.operations import analyze
from aimediator.resources import asset_path
from aimediator.runner import Runner

ELAPSED = re.compile(r'"elapsed_seconds": [0-9.e-]+|"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:.]+\+00:00"')
DONE = {'done': True, 'done_reason': 'stop', 'message': {'content': '{"decisions": []}'}}


def artifacts(folder):
    """Return every JSON file of a run except its state and reuse provenance, with elapsed times and timestamps masked."""
    skipped = {'run-state.json', 'reuse-provenance.json'}
    return {str(p.relative_to(folder)): ELAPSED.sub('<elapsed>', p.read_text(encoding='utf-8'))
            for p in sorted(Path(folder).rglob('*.json')) if p.name not in skipped}


class SharedCacheTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        cases = read(asset_path('fixtures/cases.json'))
        self.input = self.root / 'input.jsonl'
        self.input.write_bytes(b''.join(canonical(c['source']) + b'\n' for c in cases))

    def run_with(self, mode, name, cache_dir, limit=1):
        cfg = defaults()
        cfg.update(evidence_quality=mode, base_url='http://fixture.invalid', cache_dir=cache_dir,
                   max_parallel_requests=limit)
        transport = FixtureTransport(cfg)
        run = self.root / name
        with contextlib.redirect_stderr(io.StringIO()):
            analyze(self.input, run, cfg, transport=transport, quiet=True)
        self.embedding_calls = [c for c in transport.calls if c[0] == 'embedding']
        return run, [c for c in transport.calls if c[0] == 'chat']

    def test_second_run_reuses_every_response(self):
        cache_dir = str(self.root / 'cache')
        cold, cold_calls = self.run_with('enforce', 'cold', cache_dir)
        self.assertTrue(cold_calls)
        self.assertFalse(list(cold.rglob('reuse-provenance.json')))
        self.assertTrue(self.embedding_calls)
        warm, warm_calls = self.run_with('enforce', 'warm', cache_dir)
        self.assertEqual(warm_calls, [])
        # Step U3.4: retrieval embeds nothing; the one remaining call is the availability probe of
        # operations.analyze (one text, before the run folder exists).
        self.assertEqual(self.embedding_calls, [('embedding', 1)])
        self.assertFalse((warm / 'requests' / 'embedding').exists())
        self.assertEqual(artifacts(warm), artifacts(cold))
        responses = list((warm / 'requests').glob('*/*/response.json'))
        reused = list(warm.rglob('reuse-provenance.json'))
        self.assertEqual(len(reused), len(cold_calls))
        self.assertEqual(len(responses), len(reused))
        for path in reused:
            provenance = read(path)
            self.assertEqual(set(provenance), {'source', 'key', 'original_elapsed_seconds'})
            self.assertEqual(provenance['source'], 'shared_cache')
            self.assertTrue((Path(cache_dir) / 'chat' / provenance['key'][:2] / provenance['key']).is_dir())
            self.assertEqual(read(path.parent / 'response.json')['elapsed_seconds'], 0)
        metrics = request_metrics(warm)
        self.assertEqual(sum(s['all']['fresh'] for s in metrics['stages'].values()), 0)
        self.assertEqual(sum(s['all']['reused'] for s in metrics['stages'].values()), len(reused))
        # Parallel requests read the same cache.
        parallel, parallel_calls = self.run_with('enforce', 'parallel', cache_dir, limit=3)
        self.assertEqual(parallel_calls, [])
        self.assertEqual(read(parallel / 'run-state.json')['run_state'], 'completed')

    def test_runner_lookup_order_and_storage(self):
        shared = SharedCache(self.root / 'cache')
        calls = []

        def chat(base, payload, partial):
            calls.append(payload)
            return dict(answers.pop(0))
        prompts = {'relevance': {'en': 'Review relevance'}}
        data = {'comments': [{'comment_id': 'c1', 'text': 'Ryu is too strong', 'retrieved_topics': []}]}
        answers = [{'done': False, 'done_reason': 'length', 'message': {'content': ''}},
                   {'done': True, 'done_reason': 'stop', 'message': {'content': '{"decisions": ["related"]}'}}]
        first = Runner('http://fixture.invalid', self.root / 'a', prompts, chat_transport=chat, shared_cache=shared,
                       model_digests={'llama3.1:latest': 'sha256:1'}, service_version='v1')
        first.generate('llama3.1:latest', 'en', 'relevance', data, ['c1'])
        self.assertFalse((self.root / 'cache' / 'chat').exists())  # incomplete answers are not stored
        second = Runner('http://fixture.invalid', self.root / 'b', prompts, chat_transport=chat, shared_cache=shared,
                        model_digests={'llama3.1:latest': 'sha256:1'}, service_version='v1')
        parsed, meta = second.generate('llama3.1:latest', 'en', 'relevance', data, ['c1'])
        self.assertEqual(len(calls), 2)
        self.assertEqual(len(list((self.root / 'cache' / 'chat').glob('*/*/response.json'))), 1)
        # The run journal comes first, then the shared cache; the transport is not called.
        again, _ = second.generate('llama3.1:latest', 'en', 'relevance', data, ['c1'])
        self.assertEqual(again, parsed)
        third = Runner('http://fixture.invalid', self.root / 'c', prompts, chat_transport=chat, shared_cache=shared,
                       model_digests={'llama3.1:latest': 'sha256:1'}, service_version='v1',
                       quality_identity={'run_identity': 'another run'})
        reused, meta = third.generate('llama3.1:latest', 'en', 'relevance', data, ['c1'])
        self.assertEqual((reused, meta['elapsed_seconds'], len(calls)), (parsed, 0, 2))
        # Another model digest, service version or request context misses.
        for kwargs, context in (({'model_digests': {'llama3.1:latest': 'sha256:2'}, 'service_version': 'v1'}, None),
                                ({'model_digests': {'llama3.1:latest': 'sha256:1'}, 'service_version': 'v2'}, None),
                                ({'model_digests': {'llama3.1:latest': 'sha256:1'}, 'service_version': 'v1'},
                                 {'attempt': 2})):
            answers.append(dict(answers and answers[0] or
                                {'done': True, 'done_reason': 'stop', 'message': {'content': '{"decisions": ["related"]}'}}))
            other = Runner('http://fixture.invalid', self.root / ('d%d' % len(calls)), prompts, chat_transport=chat,
                           shared_cache=shared, **kwargs)
            other.generate('llama3.1:latest', 'en', 'relevance', data, ['c1'], request_context=context)
        self.assertEqual(len(calls), 5)

    def test_key_and_storable(self):
        payload = {'model': 'm', 'messages': [], 'stream': True}
        self.assertEqual(chat_key(payload, 'd', 'v'), chat_key({**payload, 'stream': False}, 'd', 'v'))
        self.assertNotEqual(chat_key(payload, 'd', 'v'), chat_key(payload, 'd', 'v', {'attempt': 1}))
        self.assertTrue(storable({'response': DONE}))
        for result in ({**DONE, 'done': False}, {**DONE, 'done_reason': 'length'}, {**DONE, 'error': 'x'},
                       {'done': True, 'done_reason': 'stop'}):
            self.assertFalse(storable({'response': result}))
        shared = SharedCache(self.root / 'cache')
        shared.store('ab' * 32, payload, {'elapsed_seconds': 1.5, 'response': DONE})
        self.assertEqual(shared.lookup('ab' * 32, payload)['elapsed_seconds'], 1.5)
        self.assertIsNone(shared.lookup('ab' * 32, {**payload, 'model': 'other'}))
        self.assertIsNone(shared.lookup('cd' * 32, payload))

    def test_configuration_key_and_option(self):
        self.assertIsNone(defaults()['cache_dir'])
        for value in ('', '  ', 3, True):
            with self.assertRaises(Failure):
                validate({**defaults(), 'cache_dir': value})
        folder = self.root / 'configs'
        folder.mkdir()
        config = folder / 'config.json'
        config.write_text(json.dumps({'cache_dir': 'cache'}), encoding='utf-8')
        self.assertEqual(resolve(config)['cache_dir'], str((folder / 'cache').resolve()))
        self.assertEqual(resolve(config, {'cache_dir': Path('elsewhere')})['cache_dir'], str(Path('elsewhere').resolve()))
        config.write_text(json.dumps({'evidence_quality': 'off'}), encoding='utf-8')
        self.assertIsNone(resolve(config)['cache_dir'])


class EmbeddingCacheTests(unittest.TestCase):
    """U3.4 (UP-D09): one embedding record per text, missing texts only, batches of 32 in input order."""

    def test_records_batches_and_shared_cache(self):
        from aimediator import retrieval
        from aimediator.resources import anchors
        rows = [{'record_id': 'r%d' % i, 'language': 'en', 'text_original': 'comment %d' % (i % 40)}
                for i in range(50)]
        calls = []

        def api(base, endpoint, payload):
            calls.append(list(payload['input']))
            return {'embeddings': [[1.0, float(len(t) % 7) + 0.5] for t in payload['input']]}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shared = SharedCache(root / 'cache')
            first = retrieval.retrieve(rows, 'http://fixture.invalid', root / 'a', 'm', api_transport=api,
                                       shared_cache=shared, model_digest='sha256:1')
            texts = list(dict.fromkeys(sum(anchors(), []) + [retrieval_text(r) for r in rows]))
            self.assertEqual([len(c) for c in calls], [32, 28])  # 20 anchors and 40 distinct comments
            self.assertEqual(sum(calls, []), texts)
            files = sorted((root / 'a' / 'embeddings').glob('*.json'))
            self.assertEqual(len(files), 60)
            record = read(files[0])
            self.assertEqual(set(record), {'model', 'text', 'vector'})
            self.assertEqual(files[0].stem, retrieval.text_identity('m', 'http://fixture.invalid', record['text']))
            self.assertEqual(len(list((root / 'cache' / 'embedding').glob('*/*.json'))), 60)
            # The run's records come first; then the shared cache; a new run asks the service for nothing.
            again = retrieval.retrieve(rows, 'http://fixture.invalid', root / 'a', 'm', api_transport=api)
            warm = retrieval.retrieve(rows, 'http://fixture.invalid', root / 'b', 'm', api_transport=api,
                                      shared_cache=shared, model_digest='sha256:1')
            self.assertEqual(len(calls), 2)
            self.assertEqual(again, first)
            self.assertEqual(warm, first)
            self.assertEqual(set(first[0]), {'comment_id', 'language', 'positive_score', 'negative_score', 'margin',
                                             'retrieval_related', 'references'})
            # Another model digest misses the shared cache.
            retrieval.retrieve(rows[:1], 'http://fixture.invalid', root / 'c', 'm', api_transport=api,
                               shared_cache=shared, model_digest='sha256:2')
            self.assertEqual([len(c) for c in calls[2:]], [21])


def retrieval_text(row):
    return ('Instruct: Retrieve the description matching the topic and intent of this Street Fighter 6 player '
            'comment.\nQuery: ' + row['text_original'])


if __name__ == '__main__':
    unittest.main()
