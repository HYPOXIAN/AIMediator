"""Intra-package imports follow the dependency table of the restructuring plan, section 4.2."""
import ast
from pathlib import Path
import subprocess
import sys
import unittest

PACKAGE = Path(__file__).resolve().parents[1] / 'src/aimediator'

# Run in a fresh interpreter: argv[1] is the source root, the rest are module names.
IMPORT_WITHOUT_READS = '''
import importlib, json, pathlib, sys
import numpy

def refuse(path, *args, **kwargs):
    raise AssertionError('File read at import time: ' + str(path))

pathlib.Path.read_text = refuse
pathlib.Path.read_bytes = refuse
try:
    pathlib.Path(sys.argv[1]).read_bytes()
except AssertionError:
    pass
else:
    raise SystemExit('The read patch is not in effect')
sys.path.insert(0, sys.argv[1])
for name in sys.argv[2:]:
    importlib.import_module(name)
print(len(sys.argv) - 2)
'''

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
    (('cache',), ('common',)),
    (('runner',), ('common', 'stages', 'inference', 'evidence', 'evidence_quality', 'cache')),
    (('retrieval',), ('common', 'resources', 'inference', 'glossary_vectors')),
    (('pipeline',), ('common', 'resources', 'balance_policy', 'evidence', 'evidence_quality', 'runner',
                     'retrieval')),
    (('run_store',), ('common', 'resources')),
    (('fixture_transport',), ('common', 'resources', 'inference', 'evidence')),
    (('operations',), ('common', 'config', 'resources', 'inference', 'run_store', 'pipeline', 'runner',
                       'retrieval', 'evidence_quality', 'balance_policy', 'fixture_transport', 'cache')),
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
    # Pipeline upgrade plan 4.11 (UP-D01).
    (('measurement',), ('common', 'quality_scoring')),
]
ALLOWED = {module: frozenset(imports) for modules, imports in TABLE for module in modules}
# Every module may import aimediator.__version__ (plan 4.2).
EVERYWHERE = frozenset({'__version__'})

# __init__.py is the package itself, the source of __version__, and has no
# row: it may not import from the package at all (change record, decision
# found in B2.10).
PACKAGE_INIT = '__init__'

# Subpackages with a "<name>.*" row. Their modules are named "<name>.<module>",
# and the subpackage's own __init__.py is named "<name>".
SUBPACKAGES = ('collection',)


def target_name(parts):
    """Name an import target given as parts below aimediator: a top-level module or a subpackage module."""
    if parts[0] in SUBPACKAGES and len(parts) > 1:
        return parts[0] + '.' + parts[1]
    return parts[0]


def imported_modules(source, package=()):
    """Return (line, target) for every intra-package import in the source, function bodies included.

    package holds the parts of the subpackage that contains the source; relative imports resolve from it.
    """
    edges = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom):
            if node.level >= 1:
                base = list(package[:len(package) - node.level + 1])
                module = node.module
            elif node.module == 'aimediator' or (node.module or '').startswith('aimediator.'):
                base = []
                module = node.module.partition('.')[2] or None
            else:
                continue
            parts = base + module.split('.') if module else base
            if parts and (len(parts) > 1 or parts[0] not in SUBPACKAGES):
                edges.append((node.lineno, target_name(parts)))
            else:  # the imported names are modules of the package, or of the subpackage that parts name
                edges.extend((node.lineno, target_name(parts + [alias.name])) for alias in node.names)
        elif isinstance(node, ast.Import):
            edges.extend((node.lineno, target_name(alias.name.split('.')[1:])) for alias in node.names
                         if alias.name.startswith('aimediator.'))
    return edges


def module_name(path):
    parts = path.relative_to(PACKAGE).with_suffix('').parts
    return '.'.join(parts[:-1] if len(parts) > 1 and parts[-1] == '__init__' else parts)


def package_imports():
    return {module_name(path): imported_modules(path.read_text(encoding='utf-8'),
                                                path.parent.relative_to(PACKAGE).parts)
            for path in sorted(PACKAGE.rglob('*.py'))}


def row(module):
    """Return the table row of a module: its own name, or "<subpackage>.*"."""
    head = module.split('.')[0]
    return head + '.*' if head in SUBPACKAGES else module


def allowed(module, target):
    return target in EVERYWHERE or row(target) in ALLOWED.get(row(module), ())


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

    def test_scanner_resolves_subpackage_imports(self):
        source = '\n'.join([
            'from . import screening as s',
            'from .client import Halt',
            'from ..common import write as write_json',
            'from .. import __version__, resources',
            'from aimediator.collection.store import Store',
            'import aimediator.collection.export',
            'from aimediator.collection import sources',
        ])
        self.assertEqual(sorted(imported_modules(source, ('collection',))), [
            (1, 'collection.screening'), (2, 'collection.client'), (3, 'common'), (4, '__version__'),
            (4, 'resources'), (5, 'collection.store'), (6, 'collection.export'), (7, 'collection.sources')])
        self.assertEqual(row('collection.client'), 'collection.*')
        self.assertTrue(allowed('collection.balanced', 'collection.screening'))
        self.assertTrue(allowed('collection.client', 'common'))
        self.assertFalse(allowed('collection.client', 'evidence'))
        self.assertFalse(allowed('evidence', 'collection.client'))

    def test_every_module_file_is_in_the_table(self):
        modules = set(package_imports()) - {PACKAGE_INIT}
        self.assertIn('common', modules)
        self.assertEqual(sorted(m for m in modules if row(m) not in ALLOWED), [],
                         'Add new modules to the table on purpose')

    def test_importing_every_module_reads_no_file(self):
        # __main__ is left out: importing it runs the command line.
        names = sorted('.'.join(('aimediator',) + path.relative_to(PACKAGE).with_suffix('').parts).replace('.__init__', '')
                       for path in PACKAGE.rglob('*.py') if path.stem != '__main__')
        self.assertIn('aimediator.retrieval', names)
        result = subprocess.run([sys.executable, '-c', IMPORT_WITHOUT_READS, str(PACKAGE.parent)] + names,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.split(), [str(len(names))])

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
