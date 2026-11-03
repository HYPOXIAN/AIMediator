"""Offline tests for scripts/maintenance/check_rules.py."""
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import textwrap
import unittest
import unittest.mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'check_rules', str(ROOT / 'scripts/maintenance/check_rules.py'))
check_rules = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_rules)

# Built at run time so this tracked file holds no such strings itself.
HOME = '/' + 'home/alice/project'
FAKE_KEY = 'AIza' + 'B' * 35
HEADER = ('- Type: Record\n- Status: Active\n- Updated: 2026-11-03\n'
          '- Applies to: v1\n')
RULES_TEXT = ('suite passing with at least the recorded\n'
              'baseline count (2 on 2026-11-03; a baseline change)\n')


class CheckRulesTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = Path(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, rel, text=''):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text), encoding='utf-8')
        return path

    def violations(self, rule):
        return check_rules.CHECKS[rule](check_rules.Project(self.root))

    def paths(self, rule):
        return sorted(v.path for v in self.violations(rule))

    def messages(self, rule):
        return [v.message for v in self.violations(rule)]


class TestGlobalRules(CheckRulesTestCase):
    def test_g3_flags_entries_outside_allowlist(self):
        for name in ('README.md', 'src', 'docs', 'prompts', '.env', 'notes',
                     'stray.txt'):
            if '.' in name:
                self.write(name)
            else:
                (self.root / name).mkdir()
        self.assertEqual(self.paths('G3'), ['notes', 'stray.txt'])

    def test_g7_flags_home_paths_but_not_prose_placeholders(self):
        self.write('docs/a.md', 'see %s/file\n' % HOME)
        self.write('docs/b.md', 'no `/home/...` paths, grep -r /home/ is empty\n')
        self.assertEqual([(v.path, v.line) for v in self.violations('G7')],
                         [('docs/a.md', 1)])

    def test_g7_flags_dated_or_reports_defaults_only(self):
        # PROJECT stands for the root constant, so this file does not
        # trip the P4 check itself.
        self.write('src/tool.py', textwrap.dedent('''\
            import argparse
            from pathlib import Path
            PROJECT = Path('.')
            p = argparse.ArgumentParser()
            p.add_argument('--out', default=PROJECT / 'reports/run-a')
            p.add_argument('--run-name', default='balance-20261022')
            p.add_argument('--dataset', default=PROJECT / 'data/raw/feedback/20261015-x')
            p.add_argument('--out2', default=PROJECT / 'runs' / 'x')
            def f(out='reports/old'):
                return out
            ''').replace('PROJECT', 'ROOT'))
        self.assertEqual(sorted(v.line for v in self.violations('G7')),
                         [5, 6, 9])

    def test_g8_naming(self):
        names = ['docs/plans/good-name.md', 'src/pkg/good_module.py',
                 'src/pkg/__init__.py', 'data/20261015-dataset/records.jsonl',
                 'prompts/relevance.en.txt', 'README.md', '.gitignore',
                 'scripts/latest_run.py', 'configs/x-20261027.json',
                 'data/set-v1-pending/a.json', 'docs/BadName.md',
                 'scripts/bad-module.py', 'Some_Dir/file.txt']
        for name in names:
            self.write(name)
        self.assertEqual(self.paths('G8'), [
            'Some_Dir/', 'configs/x-20261027.json', 'data/set-v1-pending/',
            'docs/BadName.md', 'scripts/bad-module.py',
            'scripts/latest_run.py'])

    def test_g8_lists_ignored_report_and_dataset_names(self):
        (self.root / 'reports/latest-run').mkdir(parents=True)
        (self.root / 'data/raw/feedback/20261027-final').mkdir(parents=True)
        self.assertEqual(self.paths('G8'), [
            'data/raw/feedback/20261027-final/', 'reports/latest-run/'])

    def test_g9_reports_location_but_never_the_secret(self):
        self.write('src/config.py', 'KEY = "%s"\n' % FAKE_KEY)
        self.write('.env.example', 'A_KEY=\nB_KEY=filled\n')
        out = io.StringIO()
        code = check_rules.main(['--root', str(self.root), '--rule', 'G9'],
                                out=out)
        self.assertEqual(code, 1)
        text = out.getvalue()
        self.assertIn('src/config.py:1: possible Google API key', text)
        self.assertIn('value present for key B_KEY', text)
        self.assertNotIn(FAKE_KEY, text)
        self.assertNotIn('filled', text)

    def test_g9_env_files_are_flagged_without_being_read(self):
        self.write('.env.example', 'A_KEY=\n')
        self.write('sub/.env', 'A_KEY=%s\n' % FAKE_KEY)
        self.write('.env', 'A_KEY=%s\n' % FAKE_KEY)
        project = check_rules.Project(self.root)
        self.assertIsNone(project.text('.env'))
        self.assertEqual(
            [(v.path, v.message) for v in check_rules.check_g9(project)],
            [('.env', 'credential file in the source tree'),
             ('sub/.env', 'credential file in the source tree')])

    def test_g9_package_listing(self):
        self.write('.env.example', 'A_KEY=\n')
        (self.root / 'dist').mkdir()
        with zipfile.ZipFile(str(self.root / 'dist/pkg.zip'), 'w') as archive:
            archive.writestr('ws/data/raw/a.jsonl', '{}')
            archive.writestr('ws/.env', 'x')
            archive.writestr('ws/.env.example', 'x')
            archive.writestr('ws/src/a.py', '')
        self.assertEqual(self.messages('G9'),
                         ['package lists 1 .env and 1 data/raw entries'])

    def test_g2_register_and_duplicates(self):
        (self.root / 'assets').mkdir()
        self.write('assets/a.txt', 'alpha')
        (self.root / 'prompts').mkdir()
        os.symlink('../assets/a.txt', str(self.root / 'prompts/a.txt'))
        os.symlink('../assets/a.txt', str(self.root / 'prompts/b.txt'))
        self.write('scripts/shim.py',
                   '"""Compatibility entry point for :mod:`x`."""\n')
        self.write('scripts/plain.py', '"""Not a shim."""\n')
        self.write('data/one.json', '{"same": 1}')
        self.write('data/two.json', '{"same": 1}')
        self.write(check_rules.REGISTER, '''\
            | Path | Points to |
            | ---- | --------- |
            | `prompts/a.txt` | `../assets/a.txt` |
            | `scripts/gone.py` | x |
            ''')
        found = sorted((v.path, v.message) for v in self.violations('G2'))
        self.assertEqual(found, [
            ('data/one.json', 'identical content in data/two.json'),
            (check_rules.REGISTER,
             'registered layer no longer exists: scripts/gone.py'),
            ('prompts/b.txt', 'symlink not in the compatibility register'),
            ('scripts/shim.py',
             'forwarding script not in the compatibility register'),
        ])

    def test_g2_missing_register(self):
        self.write('scripts/shim.py',
                   '"""Compatibility entry point for :mod:`x`."""\n')
        self.assertEqual(self.paths('G2'),
                         [check_rules.REGISTER, 'scripts/shim.py'])


class TestDocumentationRules(CheckRulesTestCase):
    def test_d1_directories_and_loose_files(self):
        self.write('docs/README.md')
        self.write('docs/plans/a.md')
        self.write('docs/reviews/b.md')
        self.write('docs/loose.md')
        self.assertEqual(self.paths('D1'), ['docs/loose.md', 'docs/reviews/'])

    def test_d2_header(self):
        self.write('docs/records/20261103-ok.md', '# Title\n\n' + HEADER)
        self.write('docs/records/20261103-bold.md',
                   '# T\n\n**Type:** Record\n**Status:** Superseded by x.md\n'
                   '**Updated:** 2026-11-03\n**Applies to:** v1\n')
        self.write('docs/records/20261103-none.md', '# Title\n\nBody\n')
        self.write('docs/records/20261103-bad.md',
                   '# T\n\n' + HEADER.replace('Active', 'Final')
                   .replace('2026-11-03', 'Nov 3'))
        found = {v.path: v.message for v in self.violations('D2')}
        self.assertEqual(sorted(found), ['docs/records/20261103-bad.md',
                                         'docs/records/20261103-none.md'])
        self.assertIn("invalid status 'Final'",
                      found['docs/records/20261103-bad.md'])
        self.assertIn('Updated is not YYYY-MM-DD',
                      found['docs/records/20261103-bad.md'])

    def test_d4_index(self):
        self.write('docs/plans/a.md')
        self.write('docs/plans/b.md')
        self.assertEqual(self.paths('D4'), ['docs/README.md', 'docs/plans/a.md',
                                            'docs/plans/b.md'])
        self.write('docs/README.md', '- [A](plans/a.md) — plan\n')
        self.assertEqual(self.paths('D4'), ['docs/plans/b.md'])

    def test_d5_links_and_manifest(self):
        self.write('docs/plans/a.md')
        self.write('README.md', '''\
            [ok](docs/plans/a.md#part) [web](https://example.org) [top](#x)
            [broken](docs/plans/missing.md) [abs](/etc/hosts)
            [out](../elsewhere.md)
            `[code](not/checked.md)`
            ```
            [fenced](not/checked.md)
            ```
            [ref]: docs/plans/gone.md
            ''')
        self.write('MANIFEST.in', 'include docs/plans/a.md\n'
                                  'include docs/missing.md\n')
        found = [(v.path, v.line, v.message) for v in self.violations('D5')]
        self.assertEqual(found, [
            ('README.md', 2, 'broken link: docs/plans/missing.md'),
            ('README.md', 2, 'absolute link: /etc/hosts'),
            ('README.md', 3, 'link leaves the project: ../elsewhere.md'),
            ('README.md', 8, 'broken link: docs/plans/gone.md'),
            ('MANIFEST.in', 2, 'path does not exist: docs/missing.md'),
        ])

    def test_d6_document_names(self):
        for rel in ('docs/records/20261103-ok.md', 'docs/records/undated.md',
                    'docs/decisions/0001-choice.md', 'docs/decisions/choice.md',
                    'docs/plans/roadmap.md', 'docs/plans/roadmap-v2.md',
                    'docs/guides/setup-20261103.md', 'docs/archive/old-v1.md'):
            self.write(rel)
        self.assertEqual(self.paths('D6'), [
            'docs/decisions/choice.md', 'docs/guides/setup-20261103.md',
            'docs/plans/roadmap-v2.md', 'docs/records/undated.md'])

    def test_d7_json_and_size(self):
        self.write('docs/reference/dump.json', '{}')
        self.write('docs/reference/big.md', 'x' * (100 * 1024 + 1))
        self.write('docs/reference/small.md', 'x' * 100)
        self.assertEqual(self.paths('D7'), ['docs/reference/big.md',
                                            'docs/reference/dump.json'])

    def test_d8_chinese_only_in_corpus_content(self):
        self.write('docs/design/a.md', 'Intro\n中文说明\n`隆` ok\n> 引用语料\n'
                                       '```\n模型输出\n```\n第二行\n')
        self.write('docs/reference/glossary.md', '术语表\n')
        self.write('docs/design/b.md', 'Only `隆的波掌击` in code.\n')
        found = [(v.path, v.line, v.message) for v in self.violations('D8')]
        self.assertEqual(found, [('docs/design/a.md', 2,
                                  'Chinese outside corpus content on 2 line(s)')])


class TestProjectRules(CheckRulesTestCase):
    def test_p1_datasets_and_runtime_state(self):
        self.write('data/raw/feedback/20261015-good/manifest.json', '{}')
        self.write('data/raw/feedback/20261015-nomanifest/records.jsonl')
        self.write('data/raw/feedback/undated/manifest.json', '{}')
        self.write('data/raw/glossary/terms-20261008.json')
        self.write('data/raw/collector.lock')
        self.write('data/raw/http-state.json')
        self.write('data/evaluation/labels-v1/manifest.json', '{}')
        self.write('data/evaluation/labels-v1-pending/manifest.json', '{}')
        self.write('data/evaluation/loose.json')
        found = sorted((v.path, v.message) for v in self.violations('P1'))
        self.assertEqual(found, [
            ('data/evaluation/labels-v1-pending/',
             'annotation set name does not end in -vN'),
            ('data/evaluation/loose.json',
             'annotation file outside a versioned set'),
            ('data/raw/collector.lock', 'runtime state file under data/'),
            ('data/raw/feedback/20261015-nomanifest/',
             'dataset has no manifest.json'),
            ('data/raw/feedback/undated/',
             'dataset directory is not named YYYYMMDD-slug'),
            ('data/raw/glossary/', '1 file(s) outside a dataset directory'),
            ('data/raw/http-state.json', 'runtime state file under data/'),
        ])

    def test_p2_reports_and_dist(self):
        self.write('pyproject.toml', 'name = "my-pkg"\nversion = "1.2"\n')
        self.write('reports/kept/manifest.json', '{}')
        self.write('reports/kept/summary.md')
        self.write('reports/kept/provenance/snapshot.py')
        self.write('reports/raw/run.py')
        self.write('reports/raw/data.zip')
        self.write('reports/raw/backups/a.json')
        self.write('reports/loose.txt')
        self.write('dist/my_pkg-1.2-py3-none-any.whl')
        self.write('dist/my_pkg-1.2.tar.gz')
        self.write('dist/workspace.zip')
        found = sorted((v.path, v.message) for v in self.violations('P2'))
        self.assertEqual(found, [
            ('dist/workspace.zip', 'not the current wheel or sdist'),
            ('reports/loose.txt', 'loose file in reports/'),
            ('reports/raw/', '1 backup or checkpoint entr(ies)'),
            ('reports/raw/', '2 code or archive file(s) outside provenance/'),
            ('reports/raw/', 'report has no manifest.json'),
        ])

    def test_reports_contents_are_never_read(self):
        self.write('.env.example', 'A=\n')
        self.write('reports/run/manifest.json', '{"p": "%s", "k": "%s"}'
                   % (HOME, FAKE_KEY))
        self.write('reports/run/notes.md', '中文 [x](missing.md)\n')
        project = check_rules.Project(self.root)
        self.assertIsNone(project.text('reports/run/manifest.json'))
        results = check_rules.run(project, ['G7', 'G9', 'D5', 'D8'])
        self.assertEqual({rule: v for rule, v in results.items() if v}, {})

    def test_p3_scripts(self):
        self.write(check_rules.REGISTER, '| `scripts/shim.py` | x |\n')
        self.write('scripts/shim.py')
        self.write('scripts/loose_tool.py')
        self.write('scripts/collect/fetch.py')
        self.write('scripts/experiments/test_live.py')
        self.write('scripts/other/tool.py')
        found = sorted((v.path, v.message) for v in self.violations('P3'))
        self.assertEqual([p for p, _ in found], [
            'scripts/experiments/test_live.py', 'scripts/loose_tool.py',
            'scripts/other/'])

    def test_p4_test_count_and_reports_dependency(self):
        self.write('RULES.md', RULES_TEXT)
        self.write('tests/test_a.py', '''\
            import unittest
            class A(unittest.TestCase):
                def test_one(self):
                    pass
                def helper(self):
                    pass
            ''')
        self.assertEqual(self.messages('P4'),
                         ['1 tests, below the baseline of 2'])
        (self.root / 'reports/old-run').mkdir(parents=True)
        self.write('tests/test_b.py', textwrap.dedent('''\
            import unittest
            class B(unittest.TestCase):
                def test_two(self):
                    open(PROJECT / 'reports' / 'x.json')
                    open('reports/old-run/summary.json')
                    open(tmp / 'reports/other/summary.json')
            ''').replace('PROJECT', 'ROOT'))
        self.assertEqual([(v.path, v.line) for v in self.violations('P4')],
                         [('tests/test_b.py', 4), ('tests/test_b.py', 5)])

    def test_p4_missing_baseline(self):
        self.assertEqual(self.messages('P4'),
                         ['recorded test baseline not found'])


class TestCommandLine(CheckRulesTestCase):
    def run_main(self, *args):
        out = io.StringIO()
        code = check_rules.main(['--root', str(self.root)] + list(args),
                                out=out)
        return code, out.getvalue()

    def test_exit_codes_and_summary(self):
        self.write('README.md')
        code, text = self.run_main('--rule', 'G3')
        self.assertEqual(code, 0)
        self.assertIn('  G3  0\nTotal: 0\n', text)
        self.write('stray.txt')
        code, text = self.run_main('--rule', 'g3')
        self.assertEqual(code, 1)
        self.assertIn('G3  stray.txt: top-level entry not in the allowlist',
                      text)

    def test_rule_selection(self):
        code, text = self.run_main('--rule', 'G3,D7', '--rule', 'P3')
        summary = text.split('Violations by rule:\n')[1]
        self.assertEqual([line.split()[0] for line in summary.splitlines()
                          if line.startswith('  ')], ['G3', 'D7', 'P3'])

    def test_unknown_rule_is_a_usage_error(self):
        with self.assertRaises(SystemExit) as raised:
            with unittest.mock.patch('sys.stderr', io.StringIO()):
                self.run_main('--rule', 'Z9')
        self.assertEqual(raised.exception.code, 2)

    def test_list_rules_covers_every_check(self):
        code, text = self.run_main('--list-rules')
        self.assertEqual(code, 0)
        self.assertEqual([line.split()[0] for line in text.splitlines()],
                         list(check_rules.CHECKS))

    def test_failing_check_is_reported_not_raised(self):
        def broken(project):
            raise RuntimeError('boom')
        with unittest.mock.patch.dict(check_rules.CHECKS, {'G3': broken}):
            code, text = self.run_main('--rule', 'G3')
        self.assertEqual(code, 1)
        self.assertIn('check failed: RuntimeError', text)

    @unittest.skipUnless(shutil.which('git'), 'git not installed')
    def test_git_checkout_uses_tracked_and_unignored_files(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.write('.gitignore', 'ignored/\n')
        self.write('ignored/Bad Name.txt')
        self.write('kept/Bad Name.txt')
        self.assertEqual(self.paths('G8'), ['kept/Bad Name.txt'])


if __name__ == '__main__':
    unittest.main()
