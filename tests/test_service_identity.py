"""Service identity of runs (plan step U1.4, UP-D03): /api/version in the run identity; resume refuses a change."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import urllib.request
from urllib.error import HTTPError, URLError
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aimediator import inference
from aimediator.common import Failure, canonical, read, sha
from aimediator.config import defaults
from aimediator.fixture_transport import FixtureTransport
from aimediator.inference import Transport, service_version
from aimediator.operations import analyze
from aimediator.resources import asset_path
import behavior_lock


class Answer(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class VersionTests(unittest.TestCase):
    def setUp(self):
        self.cfg = defaults()
        self.cfg.update(base_url='http://service.invalid', connection_timeout=7, request_timeout=99)

    def call(self, effect):
        seen = []

        def urlopen(request, timeout):
            seen.append((request.full_url, request.get_method(), timeout))
            if isinstance(effect, Exception):
                raise effect
            return Answer(effect)
        with patch.object(urllib.request, 'urlopen', side_effect=urlopen):
            try:
                return Transport(self.cfg).version(), seen
            except Failure as exc:
                return exc, seen

    def test_version_reads_the_endpoint_with_the_connection_timeout(self):
        answer, seen = self.call(b'{"version": "0.34.2"}')
        self.assertEqual(answer, {'version': '0.34.2'})
        self.assertEqual(seen, [('http://service.invalid/api/version', 'GET', 7)])

    def test_missing_endpoint_is_unavailable_and_other_failures_follow_probe(self):
        self.assertIsNone(self.call(HTTPError('http://service.invalid/api/version', 404, 'Not Found', {}, None))[0])
        for effect, message in ((HTTPError('u', 500, 'Server Error', {}, None), 'HTTP 500'),
                                (URLError('refused'), 'URLError'), (TimeoutError(), 'TimeoutError'),
                                (b'not json', 'JSONDecodeError')):
            failure = self.call(effect)[0]
            self.assertIsInstance(failure, Failure)
            self.assertEqual((failure.code, failure.message), (3, 'Service/model probe unavailable (%s)' % message))

    def test_service_version_string(self):
        class Fake:
            def __init__(self, answer):
                self.answer = answer

            def version(self):
                return self.answer
        self.assertEqual(service_version(Fake({'version': '0.34.2', 'extra': 1})), '0.34.2')
        self.assertIsNone(service_version(Fake(None)))
        self.assertEqual(service_version(FixtureTransport(self.cfg)), 'fixture-not-a-service')
        for invalid in ({}, {'version': 3}, ['0.34.2'], '0.34.2'):
            with self.assertRaises(Failure) as caught:
                service_version(Fake(invalid))
            self.assertEqual(caught.exception.code, 3)


class RunIdentityTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        cases = [c for c in read(asset_path('fixtures/cases.json')) if 'numeric_request' in c['source']['record_id']]
        self.input = self.root / 'input.jsonl'
        self.input.write_bytes(b''.join(canonical(c['source']) + b'\n' for c in cases))
        self.cfg = defaults()
        self.cfg.update(base_url='http://fixture.invalid', evidence_quality='shadow')

    def transport(self, version):
        transport = FixtureTransport(self.cfg)
        transport.version = lambda: version
        return transport

    def test_identity_records_the_service_version(self):
        run = self.root / 'run'
        analyze(self.input, run, self.cfg, transport=FixtureTransport(self.cfg), quiet=True)
        manifest = read(run / 'manifest.json')
        self.assertEqual(manifest['identity']['service'], {'ollama_version': 'fixture-not-a-service'})
        self.assertEqual(manifest['run_id'], sha(canonical(manifest['identity'])))
        unavailable = self.root / 'unavailable'
        analyze(self.input, unavailable, self.cfg, transport=self.transport(None), quiet=True)
        self.assertEqual(read(unavailable / 'manifest.json')['identity']['service'], {'ollama_version': None})

    def test_resume_refuses_a_changed_service_version(self):
        run = self.root / 'run'
        transport = self.transport({'version': '0.34.2'})
        original = transport.chat
        calls = []

        def interrupted(base, payload, partial):
            calls.append(1)
            if len(calls) == 3:
                raise KeyboardInterrupt()
            return original(base, payload, partial)
        transport.chat = interrupted
        with self.assertRaises(Failure) as caught:
            analyze(self.input, run, self.cfg, transport=transport, quiet=True)
        self.assertEqual(caught.exception.code, 130)
        before = {p: p.read_bytes() for p in sorted(run.rglob('*')) if p.is_file()}
        for version in ({'version': '0.35.0'}, None):
            changed = self.transport(version)
            with self.assertRaises(Failure) as caught:
                analyze(resume=run, transport=changed, quiet=True)
            self.assertEqual((caught.exception.code, caught.exception.message),
                             (4, 'Service version differs from saved run; start a new run'))
            self.assertEqual(changed.calls, [])
        self.assertEqual({p: p.read_bytes() for p in sorted(run.rglob('*')) if p.is_file()}, before)
        with contextlib.redirect_stderr(io.StringIO()):
            analyze(resume=run, transport=self.transport({'version': '0.34.2'}), quiet=True)
        self.assertEqual(read(run / 'run-state.json')['run_state'], 'completed')

    def test_legacy_runner_records_the_service_version(self):
        dataset = behavior_lock.legacy_dataset(self.root)
        behavior_lock.run_legacy(self.root, dataset, 'off')
        self.assertEqual(read(self.root / 'off/manifest.json')['identity']['service_version'], 'fixture-not-a-service')
        from aimediator import engine
        from types import SimpleNamespace
        transport = FixtureTransport(defaults())
        api = behavior_lock.fixture_api(transport)

        def without_version(base, endpoint, payload=None):
            if endpoint == '/api/version':
                raise HTTPError(base + endpoint, 404, 'Not Found', {}, None)
            return api(base, endpoint, payload)
        args = SimpleNamespace(dataset=dataset, out=self.root / 'no-version', model=None,
                               embedding_model='qwen3-embedding:8b', base_url='http://fixture.invalid',
                               evidence_quality='off', quality_only=False, relevance_only=False)
        engine.run(args, api_transport=without_version, chat_transport=transport.chat)
        self.assertIsNone(json.loads((self.root / 'no-version/manifest.json').read_text())['identity']['service_version'])


if __name__ == '__main__':
    unittest.main()
