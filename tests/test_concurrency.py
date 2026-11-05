"""Ordered executor and bounded concurrency of the pipeline (plan 4.5, U3.1 and U3.2)."""
from pathlib import Path
import sys
import threading
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator.pipeline import ordered


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


if __name__ == '__main__':
    unittest.main()
