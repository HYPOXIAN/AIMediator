"""Run lifecycle state: ``run_store.state`` reads only new or changed validation files (plan step B5.8)."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import run_store
from aimediator.common import read, write

READ_TEXT = Path.read_text


class RunStateTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name) / 'run'
        write(self.folder / 'resolved-config.json', {'stop_after': 'full'})

    def request(self, stage, number, errors=()):
        """Write the validation file of one request directory and return its path."""
        path = self.folder / 'requests' / stage / ('%064x' % number) / 'validation.json'
        write(path, {'errors': list(errors), 'schema': {}})
        return path

    def state(self):
        """Call ``state`` once; return its validation.json reads and the completed identities it wrote."""
        reads = []

        def counting(path, *args, **kwargs):
            if path.name == 'validation.json':
                reads.append(path)
            return READ_TEXT(path, *args, **kwargs)
        with patch.object(Path, 'read_text', autospec=True, side_effect=counting):
            run_store.state(self.folder, 'running', 'extract')
        return len(reads), read(self.folder / 'run-state.json')['completed_request_identities']

    def full_scan(self):
        """The completed identities as a scan that reads every validation file finds them."""
        return [str(path.parent.relative_to(self.folder))
                for path in sorted((self.folder / 'requests').rglob('validation.json')) if not read(path)['errors']]

    def test_state_reads_only_new_or_changed_validation_files(self):
        paths = [self.request(stage, number, ['failed'] if number % 7 == 0 else ())
                 for number in range(40) for stage in ('extract', 'quality')]
        self.assertEqual(self.state(), (80, self.full_scan()))
        for _ in range(3):
            self.assertEqual(self.state(), (0, self.full_scan()))
        self.request('verify', 1)
        self.request('relevance', 2, ['failed'])
        self.assertEqual(self.state(), (2, self.full_scan()))
        write(paths[0], {'errors': [], 'schema': {}})
        write(paths[2], {'errors': ['changed'], 'schema': {}})
        count, completed = self.state()
        self.assertEqual((count, completed), (2, self.full_scan()))
        self.assertIn(str(paths[0].parent.relative_to(self.folder)), completed)
        self.assertNotIn(str(paths[2].parent.relative_to(self.folder)), completed)
        shutil.rmtree(paths[4].parent)
        self.assertEqual(self.state(), (0, self.full_scan()))
        self.assertEqual(len(self.full_scan()), 68)


if __name__ == '__main__':
    unittest.main()
