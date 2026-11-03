"""Behavior lock (plan section 5): the produced digests equal the fixture."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import behavior_lock as lock


class BehaviorLockTests(unittest.TestCase):
    def test_outputs_match_the_fixture(self):
        changed = lock.differences(lock.load_fixture(), lock.compute())
        if changed:
            self.fail('behavior lock differs at %d normalized paths:\n%s'
                      % (len(changed), '\n'.join(changed)))


if __name__ == '__main__':
    unittest.main()
