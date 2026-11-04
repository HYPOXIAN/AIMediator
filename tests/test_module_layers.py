"""Intra-package imports follow the dependency table of the restructuring plan, section 4.2."""
import ast
from pathlib import Path
import unittest

PACKAGE = Path(__file__).resolve().parents[1] / 'src/aimediator'

# Plan section 4.2, copied row by row. Rows for modules that do not exist yet
# stay. A table change needs a decision in the change record and an update of
# this copy in the same commit.
TABLE = [
    (('common', 'schema', 'design_briefs'), ()),
    (('resources',), ('common',)),
    (('config',), ('common', 'resources')),
    (('balance_policy',), ('resources',)),
    (('glossary_vectors',), ('common', 'config', 'resources')),
    (('evidence',), ('common', 'resources', 'schema', 'balance_policy')),
    (('evidence_quality',), ('resources', 'schema', 'balance_policy', 'evidence')),
    (('stages',), ('schema', 'evidence', 'evidence_quality', 'balance_policy')),
    (('inference',), ('common', 'glossary_vectors')),
    (('runner',), ('common', 'stages', 'inference', 'evidence', 'evidence_quality')),
    (('retrieval',), ('common', 'resources', 'inference', 'glossary_vectors')),
    (('pipeline',), ('common', 'resources', 'balance_policy', 'evidence', 'evidence_quality', 'runner',
                     'retrieval')),
    (('run_store',), ('common', 'resources')),
    (('fixture_transport',), ('common', 'resources', 'inference', 'evidence')),
    (('operations',), ('common', 'config', 'resources', 'inference', 'run_store', 'pipeline', 'runner',
                       'retrieval', 'evidence_quality', 'balance_policy', 'fixture_transport')),
    (('legacy_review',), ('common', 'schema', 'evidence', 'evidence_quality', 'pipeline')),
    (('review',), ('common', 'schema', 'evidence', 'evidence_quality', 'balance_policy', 'legacy_review')),
    (('reporting',), ('common', 'evidence', 'evidence_quality', 'review')),
    (('quality_scoring',), ('common', 'evidence_quality')),
    (('evaluation',), ('common', 'schema', 'evidence', 'evidence_quality', 'quality_scoring', 'review')),
    (('demo',), ('common', 'config', 'resources', 'fixture_transport', 'operations', 'review', 'reporting')),
    (('cli',), ('common', 'config', 'operations', 'review', 'reporting', 'evaluation', 'demo')),
    (('presentation',), ('common', 'cli')),
    (('__main__',), ('cli',)),
    (('engine',), ('common', 'resources', 'balance_policy', 'evidence', 'evidence_quality', 'glossary_vectors',
                   'inference', 'runner', 'retrieval', 'pipeline')),
    (('diagnostics',), ('evidence', 'evidence_quality', 'runner')),
    (('collection.*',), ('common', 'resources', 'collection.*')),
]
ALLOWED = {module: frozenset(imports) for modules, imports in TABLE for module in modules}
# Every module may import aimediator.__version__ (plan 4.2).
EVERYWHERE = frozenset({'__version__'})

# __init__.py is the package itself, the source of __version__, and has no
# row: it may not import from the package at all (change record, decision
# found in B2.10).
PACKAGE_INIT = '__init__'


def imported_modules(source):
    """Return (line, target) for every intra-package import in the source, function bodies included."""
    edges = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom):
            if node.level >= 1:
                module = node.module
            elif node.module == 'aimediator' or (node.module or '').startswith('aimediator.'):
                module = node.module.partition('.')[2] or None
            else:
                continue
            if module:
                edges.append((node.lineno, module.split('.')[0]))
            else:
                edges.extend((node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.Import):
            edges.extend((node.lineno, alias.name.split('.')[1]) for alias in node.names
                         if alias.name.startswith('aimediator.'))
    return edges


def package_imports():
    return {path.stem: imported_modules(path.read_text(encoding='utf-8'))
            for path in sorted(PACKAGE.glob('*.py'))}


def allowed(module, target):
    return target in EVERYWHERE or target in ALLOWED.get(module, ())


class ModuleLayers(unittest.TestCase):
    def test_scanner_finds_every_import_form(self):
        source = '\n'.join([
            'import json',
            'from . import __version__',
            'from . import evidence_quality as quality, run_store',
            'from .common import sha as digest',
            'import aimediator.config',
            'from aimediator.schema import obj',
            'from aimediator import resources',
            'from collections import Counter',
            'def late():',
            '    from .fixture_transport import FixtureTransport',
        ])
        self.assertEqual(sorted(imported_modules(source)), [
            (2, '__version__'), (3, 'evidence_quality'), (3, 'run_store'), (4, 'common'), (5, 'config'),
            (6, 'schema'), (7, 'resources'), (10, 'fixture_transport')])

    def test_every_module_file_is_in_the_table(self):
        nested = sorted(p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*.py') if p.parent != PACKAGE)
        self.assertEqual(nested, [], 'Subpackage modules are not covered yet; add them to this test on purpose')
        modules = set(package_imports()) - {PACKAGE_INIT}
        self.assertIn('common', modules)
        self.assertEqual(sorted(modules - set(ALLOWED)), [], 'Add new modules to the table on purpose')

    def test_package_init_imports_nothing_from_the_package(self):
        self.assertEqual(package_imports()[PACKAGE_INIT], [])

    def test_every_import_is_allowed(self):
        violations = [f'{module} -> {target} (line {line})'
                      for module, edges in sorted(package_imports().items()) if module != PACKAGE_INIT
                      for line, target in edges if not allowed(module, target)]
        self.assertEqual(violations, [])

    def test_imports_form_no_cycle(self):
        graph = {module: sorted({target for _, target in edges} - EVERYWHERE)
                 for module, edges in package_imports().items()}
        state, stack = {}, []

        def visit(module):
            state[module] = 'open'
            stack.append(module)
            for target in graph.get(module, ()):
                if state.get(target) == 'open':
                    self.fail('Import cycle: ' + ' -> '.join(stack[stack.index(target):] + [target]))
                if target not in state:
                    visit(target)
            stack.pop()
            state[module] = 'done'

        for module in sorted(graph):
            if module not in state:
                visit(module)


if __name__ == '__main__':
    unittest.main()
