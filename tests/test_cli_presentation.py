"""Exercise presentation through real command dispatch and offline transports."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator.common import canonical, read, write
from aimediator.config import defaults
from aimediator.demo import FixtureTransport
from aimediator.presentation import main
from aimediator.resources import asset_path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = {'提取结果', '相关性测试', '质量测试', '最终结论'}


class PresentationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        cases = read(asset_path('fixtures/cases.json'))
        self.rows = [case['source'] for case in cases if 'numeric_request' in case['source']['record_id']]
        self.input = self.root / 'input.jsonl'
        self.input.write_bytes(b''.join(canonical(row) + b'\n' for row in self.rows))
        cfg = defaults()
        cfg.update(base_url='http://fixture.invalid', evidence_quality='enforce')
        self.config = self.root / 'config.json'
        write(self.config, cfg)
        self.run = self.root / 'run'

    def invoke(self, args):
        output, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = main(args)
        return code, output.getvalue(), errors.getvalue()

    def analyze(self, *extra):
        with patch('aimediator.operations.Transport', FixtureTransport):
            return self.invoke(['analyze', '--input', str(self.input), '--out', str(self.run),
                                '--config', str(self.config), *extra])

    def test_analysis_outputs_only_business_results_with_no_progress(self):
        code, output, errors = self.analyze('--json')
        self.assertEqual((code, errors), (0, ''))
        result = json.loads(output)
        self.assertEqual(set(result), SECTIONS)
        self.assertTrue(result['提取结果'])
        self.assertTrue(result['最终结论']['分析完成'])
        self.assertTrue(result['最终结论']['合成示例'])
        self.assertIsNone(result['质量测试']['准确率'])
        self.assertNotIn('artifacts', output)
        self.assertNotIn('runtime', output)
        self.assertNotIn(str(self.root), output)
        self.assertTrue((self.run / 'request-trace.json').is_file())

    def test_stop_and_interruption_do_not_become_final_conclusions(self):
        code, output, errors = self.analyze('--stop-after', 'quality')
        self.assertEqual((code, errors), (0, ''))
        self.assertFalse(json.loads(output)['最终结论']['分析完成'])
        state = read(self.run / 'run-state.json')
        state['run_state'] = 'interrupted'
        write(self.run / 'run-state.json', state)
        code, output, errors = self.invoke(['report', '--run', str(self.run), '--out', str(self.root / 'partial')])
        self.assertEqual((code, errors), (0, ''))
        self.assertEqual(set(json.loads(output)), {'最终结论'})
        self.assertFalse(json.loads(output)['最终结论']['分析完成'])

    def test_evaluation_preserves_unlabeled_status_and_helpers_are_silent(self):
        self.analyze()
        labels = self.root / 'labels.json'
        helper = subprocess.run([sys.executable, str(ROOT / 'cli-demo/prepare-labels.py'),
                                 str(self.input), str(labels)], capture_output=True, text=True)
        self.assertEqual((helper.returncode, helper.stdout, helper.stderr), (0, '', ''))
        code, output, errors = self.invoke(['evaluate', 'quality', '--run', str(self.run),
            '--labels', str(labels), '--out', str(self.root / 'evaluation'), '--json'])
        self.assertEqual((code, errors), (0, ''))
        result = json.loads(output)['质量测试']
        self.assertEqual(result['unlabeled_comments'], len(self.rows))
        self.assertEqual(result['labeled_comments'], 0)
        self.assertEqual(result['groups'], {})
        self.assertFalse(result['independent_effectiveness_established'])

    def test_setup_status_help_and_version_are_silent_but_errors_keep_exit_codes(self):
        for argv in (['init', '--out', str(self.root / 'new-config.json'), '--json'],
                     ['doctor', '--config', str(self.config), '--input', str(self.input), '--offline', '--json'],
                     ['--version'], ['--help'], ['analyze', '--help']):
            self.assertEqual(self.invoke(argv), (0, '', ''))
        self.analyze()
        self.assertEqual(self.invoke(['status', '--run', str(self.run), '--json']), (0, '', ''))
        code, output, errors = self.invoke(['init', '--out', str(self.config), '--json'])
        self.assertEqual((code, output), (4, ''))
        self.assertIn('Output already exists', errors)

    def test_builtin_demo_retains_three_modes_with_business_only_output(self):
        code, output, errors = self.invoke(['demo', '--out', str(self.root / 'demo'), '--quiet', '--json'])
        self.assertEqual((code, errors), (0, ''))
        result = json.loads(output)
        self.assertEqual(set(result), SECTIONS)
        for values in result.values():
            self.assertEqual(set(values), {'off', 'shadow', 'enforce'})


if __name__ == '__main__':
    unittest.main()
