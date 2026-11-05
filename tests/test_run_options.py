"""RunOptions: the typed run settings of pipeline.process (pipeline upgrade U6.7, LNK-05)."""
import dataclasses
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT / 'src'))

from aimediator import pipeline  # noqa: E402


class RunOptionsTest(unittest.TestCase):
    def test_fields_and_defaults(self):
        names = [f.name for f in dataclasses.fields(pipeline.RunOptions)]
        self.assertEqual(names, ['out', 'base_url', 'embedding_model', 'quality_mode', 'relevance_only',
                                 'quality_only', 'max_parallel_requests'])
        options = pipeline.RunOptions(out=pathlib.Path('x'), base_url='http://b', embedding_model='e')
        self.assertEqual((options.quality_mode, options.relevance_only, options.quality_only,
                          options.max_parallel_requests), ('off', False, False, 1))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            options.quality_mode = 'enforce'

    def capture(self):
        seen = []
        original = pipeline.process

        def wrapper(options, *values, **named):
            seen.append(options)
            return original(options, *values, **named)
        return seen, wrapper

    def test_analyze_passes_run_options(self):
        from aimediator.demo import demo
        seen, wrapper = self.capture()
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(pipeline, 'process', wrapper):
            demo(pathlib.Path(tmp) / 'demo', quiet=True)
            self.assertEqual([type(o) for o in seen], [pipeline.RunOptions] * 3)
            self.assertEqual([o.quality_mode for o in seen], ['off', 'shadow', 'enforce'])
            self.assertEqual({(o.base_url, o.relevance_only, o.quality_only, o.max_parallel_requests) for o in seen},
                             {('http://fixture.invalid', False, False, 1)})
            self.assertEqual([o.out.name for o in seen], ['off', 'shadow', 'enforce'])

    def test_engine_builds_run_options_from_its_namespace(self):
        import behavior_lock
        from aimediator import engine
        seen, wrapper = self.capture()
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(engine, 'process', wrapper):
            root = pathlib.Path(tmp)
            behavior_lock.run_legacy(root, behavior_lock.legacy_dataset(root), 'shadow')
        self.assertEqual(len(seen), 1)
        options = seen[0]
        self.assertIsInstance(options, pipeline.RunOptions)
        self.assertEqual((options.quality_mode, options.base_url, options.embedding_model, options.relevance_only,
                          options.quality_only, options.max_parallel_requests),
                         ('shadow', 'http://fixture.invalid', 'qwen3-embedding:8b', False, False, 1))
        self.assertTrue(options.out.is_absolute())


if __name__ == '__main__':
    unittest.main()
