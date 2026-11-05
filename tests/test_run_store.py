"""Run lifecycle state: ``run_store.state`` and its request index (plan steps B5.8 and U1.1).

``state`` lists ``requests/**/validation.json`` on its first call for a run
folder in a process; afterwards the runner's journal callback
(``run_store.record_request``) keeps the index. The harness below checks, at
every write of ``run-state.json`` in CLI fixture runs with interruptions and
resumes, that the content equals what a full scan of the validation files
gives (the code before U1.1, ``updated_at_utc`` aside).
"""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import run_store
from aimediator.common import Failure, canonical, read, write
from aimediator.config import defaults
from aimediator.fixture_transport import FixtureTransport
from aimediator.operations import analyze
from aimediator.resources import asset_path
from aimediator.runner import Runner

READ_TEXT = Path.read_text
RGLOB = Path.rglob


def full_scan(folder):
    """The completed request directories as the code before U1.1 lists them: every validation file, read."""
    entries = []
    for path in RGLOB(folder / 'requests', 'validation.json'):
        relative = path.relative_to(folder)
        entries.append((relative.parts, str(relative.parent), not read(path).get('errors')))
    return [directory for _, directory, completed in sorted(entries) if completed]


class RunStateTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name) / 'run'
        write(self.folder / 'resolved-config.json', {'stop_after': 'full'})

    def request(self, stage, number, errors=(), journal=True):
        """Write the validation file of one request directory, journal it, and return its path."""
        path = self.folder / 'requests' / stage / ('%064x' % number) / 'validation.json'
        write(path, {'errors': list(errors), 'schema': {}})
        if journal:
            run_store.record_request(self.folder, path.parent.relative_to(self.folder), not errors)
        return path

    def state(self, status='running'):
        """Call ``state`` once; return its validation reads, its listings and the completed identities it wrote."""
        reads, listings = [], []

        def counting_read(path, *args, **kwargs):
            if path.name == 'validation.json':
                reads.append(path)
            return READ_TEXT(path, *args, **kwargs)

        def counting_rglob(path, *args, **kwargs):
            listings.append(path)
            return RGLOB(path, *args, **kwargs)
        with patch.object(Path, 'read_text', autospec=True, side_effect=counting_read), \
                patch.object(Path, 'rglob', autospec=True, side_effect=counting_rglob):
            run_store.state(self.folder, status, 'extract')
        return len(reads), len(listings), read(self.folder / 'run-state.json')['completed_request_identities']

    def test_state_lists_once_then_follows_the_journal(self):
        paths = [self.request(stage, number, ['failed'] if number % 7 == 0 else ())
                 for number in range(40) for stage in ('extract', 'quality')]
        self.assertEqual(self.state(), (80, 1, full_scan(self.folder)))
        for _ in range(3):
            self.assertEqual(self.state(), (0, 0, full_scan(self.folder)))
        self.request('verify', 1)
        self.request('relevance', 2, ['failed'])
        self.request('extract-x', 3)
        self.assertEqual(self.state(), (0, 0, full_scan(self.folder)))
        write(paths[0], {'errors': [], 'schema': {}})
        run_store.record_request(self.folder, paths[0].parent.relative_to(self.folder), True)
        write(paths[2], {'errors': ['changed'], 'schema': {}})
        run_store.record_request(self.folder, str(paths[2].parent.relative_to(self.folder)), False)
        count, listings, completed = self.state()
        self.assertEqual((count, listings, completed), (0, 0, full_scan(self.folder)))
        self.assertIn(str(paths[0].parent.relative_to(self.folder)), completed)
        self.assertNotIn(str(paths[2].parent.relative_to(self.folder)), completed)
        self.assertEqual(len(completed), 70)
        # A file written without the journal is found by the next listing only: on resume.
        self.request('verify', 4, journal=False)
        self.assertNotIn(str(Path('requests/verify') / ('%064x' % 4)), self.state()[2])
        run_store._requests.clear()  # a new process, as on resume
        self.assertEqual(self.state(), (84, 1, full_scan(self.folder)))
        # An interruption or failure may fall between a validation write and its journal call.
        self.request('verify', 5, journal=False)
        for status in ('interrupted', 'failed'):
            self.assertEqual(self.state(status), (85, 1, full_scan(self.folder)))
        self.assertEqual(self.state(), (0, 0, full_scan(self.folder)))

    def test_fifty_state_calls_list_the_requests_once(self):
        for number in range(30):
            self.request('extract', number)
        listings = 0
        for number in range(50):
            self.request('verify', number, ['failed'] if number % 3 == 0 else ())
            listings += self.state()[1]
        self.assertEqual(listings, 1)
        self.assertEqual(read(self.folder / 'run-state.json')['completed_request_identities'], full_scan(self.folder))

    def test_journal_before_the_first_listing_is_not_the_index(self):
        self.request('extract', 1, journal=False)
        self.request('extract', 2)
        self.assertEqual(self.state(), (2, 1, full_scan(self.folder)))

    def test_runner_journals_each_validation(self):
        events = []

        def chat(base, payload, partial):
            content = '{"decisions": ["related"]}'
            return {'done': True, 'done_reason': 'stop', 'message': {'content': content}}
        runner = Runner('http://fixture.invalid', self.folder, {'relevance': {'en': 'Review relevance'}},
                        chat_transport=chat, journal=lambda *event: events.append(event))
        data = {'comments': [{'comment_id': 'c1', 'text': 'Ryu is too strong', 'retrieved_topics': []}]}
        parsed, meta = runner.generate('llama3.1:latest', 'en', 'relevance', data, ['c1'])
        self.assertEqual((events, meta['errors']), ([(Path('requests/relevance') / meta['request_id'], True)], []))
        self.assertTrue((self.folder / events[0][0] / 'validation.json').is_file())


class RunStateHarnessTests(unittest.TestCase):
    """Reduced form of the U1.1 contract harness: CLI fixture runs in three modes, interrupted and resumed."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        cases = read(asset_path('fixtures/cases.json'))[::3]  # 13 of the 38 cases, both languages
        self.input = self.root / 'input.jsonl'
        self.input.write_bytes(b''.join(canonical(c['source']) + b'\n' for c in cases))
        self.writes = 0
        real = run_store.state

        def checked(folder, status, stage, reason=None):
            path = folder / 'run-state.json'
            previous = read(path) if path.exists() else {}
            real(folder, status, stage, reason)
            written = read(path)
            expected = {**previous, 'schema_version': 'aimediator-state-v1', 'run_state': status, 'stage': stage,
                        'updated_at_utc': written['updated_at_utc'], 'reason': reason,
                        'requested_stop_stage': read(folder / 'resolved-config.json')['stop_after'],
                        'completed_request_identities': full_scan(folder)}
            self.assertEqual(list(written.items()), list(expected.items()))
            self.writes += 1
        patcher = patch.object(run_store, 'state', checked)
        patcher.start()
        self.addCleanup(patcher.stop)

    def transport(self, mode, interrupt_at=None, invalid_every=None):
        cfg = defaults()
        cfg.update(evidence_quality=mode, base_url='http://fixture.invalid')
        transport = FixtureTransport(cfg)
        original, calls = transport.chat, []

        def chat(base, payload, partial):
            calls.append(1)
            if interrupt_at is not None and len(calls) == interrupt_at:
                raise KeyboardInterrupt()
            if invalid_every and len(calls) % invalid_every == 0:
                return {'done': True, 'done_reason': 'stop', 'message': {'content': '{}'}}
            return original(base, payload, partial)
        transport.chat = chat
        return cfg, transport

    def analyze(self, *args, **kwargs):
        with contextlib.redirect_stderr(io.StringIO()):
            try:
                analyze(*args, quiet=True, **kwargs)
            except Failure as exc:
                return exc.code
        return 0

    def test_state_content_equals_a_full_scan_at_every_write(self):
        for mode in ('off', 'shadow', 'enforce'):
            with self.subTest(mode=mode):
                run = self.root / ('interrupted-' + mode)
                cfg, transport = self.transport(mode, interrupt_at=9)
                self.assertEqual(self.analyze(self.input, run, cfg, transport=transport), 130)
                self.assertEqual(self.analyze(resume=run, transport=self.transport(mode, interrupt_at=6)[1]), 130)
                self.assertEqual(self.analyze(resume=run, transport=self.transport(mode)[1]), 0)
                self.assertEqual(read(run / 'run-state.json')['run_state'], 'completed')
        run = self.root / 'invalid-shadow'
        cfg, transport = self.transport('shadow', invalid_every=5)
        self.assertEqual(self.analyze(self.input, run, cfg, transport=transport), 5)
        self.assertEqual(self.analyze(resume=run, transport=self.transport('shadow', invalid_every=5)[1]), 5)
        self.assertGreater(self.writes, 150)


if __name__ == '__main__':
    unittest.main()
