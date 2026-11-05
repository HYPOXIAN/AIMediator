"""Ordered executor and bounded concurrency of the pipeline (plan 4.5, U3.1 and U3.2)."""
import contextlib
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import threading
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator.cli import main
from aimediator.common import Failure, canonical, read
from aimediator.config import defaults, validate
from aimediator.fixture_transport import FixtureTransport
from aimediator.operations import analyze
from aimediator.pipeline import ordered
from aimediator.resources import asset_path

DIGEST = re.compile(r'[0-9a-f]{64}')
ELAPSED = re.compile(r'"elapsed_seconds": [0-9.e-]+')


class OrderedExecutorTests(unittest.TestCase):
    def test_commits_in_input_order_on_the_calling_thread(self):
        caller = threading.get_ident()
        committed, threads = [], set()

        def work(unit):
            time.sleep(0.02 * (5 - unit % 5))
            return unit * 10

        def commit(unit, result):
            threads.add(threading.get_ident())
            committed.append((unit, result))

        for limit in (1, 2, 4, 8):
            committed.clear()
            ordered(range(12), work, commit, limit)
            self.assertEqual(committed, [(u, u * 10) for u in range(12)])
        self.assertEqual(threads, {caller})

    def test_window_bounds_units_in_flight(self):
        lock, state = threading.Lock(), {'now': 0, 'max': 0}

        def work(unit):
            with lock:
                state['now'] += 1
                state['max'] = max(state['max'], state['now'])
            time.sleep(0.01)
            with lock:
                state['now'] -= 1
            return unit

        for limit in (1, 3):
            state.update(now=0, max=0)
            ordered(range(10), work, lambda u, r: None, limit)
            self.assertEqual(state['max'], limit)

    def test_limit_one_interleaves_as_a_serial_loop(self):
        events = []
        ordered(range(3), lambda u: events.append(('work', u)), lambda u, r: events.append(('commit', u)), 1)
        self.assertEqual(events, [('work', 0), ('commit', 0), ('work', 1), ('commit', 1), ('work', 2), ('commit', 2)])

    def test_interruption_commits_nothing_after_the_failed_unit(self):
        started, committed = [], []

        def work(unit):
            started.append(unit)
            if unit == 2:
                raise KeyboardInterrupt()
            time.sleep(0.01)
            return unit

        with self.assertRaises(KeyboardInterrupt):
            ordered(range(20), work, lambda u, r: committed.append(u), 3)
        self.assertEqual(committed, [0, 1])
        self.assertLessEqual(max(started), 4)


def artifacts(folder):
    """Return the top-level JSON artifacts of a run with digests and elapsed times masked; identity files are left out."""
    skipped = {'manifest.json', 'resolved-config.json', 'run-state.json'}
    return {p.name: ELAPSED.sub('<elapsed>', DIGEST.sub('<digest>', p.read_text(encoding='utf-8')))
            for p in sorted(Path(folder).glob('*.json')) if p.name not in skipped}


class ParallelRunTests(unittest.TestCase):
    """U3.2 (UP-D08): max_parallel_requests bounds the requests in flight and keeps the artifacts of N = 1."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        cases = read(asset_path('fixtures/cases.json'))
        self.input = self.root / 'input.jsonl'
        self.input.write_bytes(b''.join(canonical(c['source']) + b'\n' for c in cases))

    def run_with(self, mode, limit):
        cfg = defaults()
        cfg.update(evidence_quality=mode, base_url='http://fixture.invalid', max_parallel_requests=limit)
        transport = FixtureTransport(cfg)
        original, lock, state = transport.chat, threading.Lock(), {'now': 0, 'max': 0, 'calls': 0}

        def chat(base, payload, partial):
            with lock:
                state['now'] += 1
                state['calls'] += 1
                state['max'] = max(state['max'], state['now'])
            try:
                time.sleep(0.004)
                return original(base, payload, partial)
            finally:
                with lock:
                    state['now'] -= 1
        transport.chat = chat
        run = self.root / ('%s-%d' % (mode, limit))
        with contextlib.redirect_stderr(io.StringIO()):
            analyze(self.input, run, cfg, transport=transport, quiet=True)
        self.assertEqual(read(run / 'resolved-config.json')['max_parallel_requests'], limit)
        return run, state

    def test_parallel_runs_bound_requests_and_equal_the_serial_run(self):
        for mode in ('off', 'shadow', 'enforce'):
            serial, one = self.run_with(mode, 1)
            self.assertEqual(one['max'], 1)
            for limit in (2, 4):
                parallel, many = self.run_with(mode, limit)
                self.assertLessEqual(many['max'], limit)
                self.assertGreater(many['max'], 1, mode)
                self.assertEqual(many['calls'], one['calls'])
                self.assertEqual(artifacts(parallel), artifacts(serial), (mode, limit))
                self.assertEqual(read(parallel / 'run-state.json')['run_state'], 'completed')

    def test_configuration_key_and_option(self):
        self.assertEqual(defaults()['max_parallel_requests'], 1)
        for value in (1, 8):
            validate({**defaults(), 'max_parallel_requests': value})
        for value in (0, 9, 2.0, True, None, '2'):
            with self.assertRaises(Failure) as raised:
                validate({**defaults(), 'max_parallel_requests': value})
            self.assertEqual(raised.exception.code, 2)
        config = self.root / 'config.json'
        config.write_text(json.dumps({k: v for k, v in defaults().items() if k != 'max_parallel_requests'}),
                          encoding='utf-8')
        from aimediator.config import resolve
        self.assertEqual(resolve(config)['max_parallel_requests'], 1)
        self.assertEqual(resolve(config, {'max_parallel_requests': 3})['max_parallel_requests'], 3)
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()):
            code = main(['analyze', '--config', str(config), '--input', str(self.input), '--out',
                         str(self.root / 'refused'), '--max-parallel-requests', '9', '--json'])
        self.assertEqual(code, 2)
        self.assertFalse((self.root / 'refused').exists())


if __name__ == '__main__':
    unittest.main()
