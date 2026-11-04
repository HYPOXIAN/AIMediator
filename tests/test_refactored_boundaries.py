"""Contracts for shared modules, progress reporting and failure boundaries."""
import copy
import importlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'scripts'))  # the forwarders, for the identity test until B4.2
from aimediator import evidence
from aimediator.config import defaults, embedding_endpoint, env_values
from aimediator.inference import Transport
from aimediator.runner import Runner


class RefactoredBoundaries(unittest.TestCase):
    def test_compatibility_imports_share_package_state(self):
        for script, package in {
            'run_balance_analysis': 'engine',
            'evidence_quality': 'evidence_quality',
            'balance_policy': 'balance_policy',
            'glossary_vectors': 'glossary_vectors',
            'evaluate_evidence_quality': 'quality_scoring',
            'review_balance_sources': 'legacy_review',
        }.items():
            with self.subTest(script=script):
                self.assertIs(importlib.import_module(script),
                              importlib.import_module('aimediator.' + package))

    def test_character_reference_returns_new_objects(self):
        expected = copy.deepcopy(evidence.character_reference('Ryu'))
        self.assertIn({'text': 'Ryu'}, next(e for e in expected if e['canonical_name'] == 'Ryu')['aliases'])
        reference = evidence.character_reference('Ryu')
        for entry in reference:
            for alias in entry['aliases']:
                alias['text'] = 'mutated'
            entry['aliases'].append({'text': 'mutated'})
            entry['canonical_name'] = 'mutated'
        reference.clear()
        self.assertEqual(evidence.character_reference('Ryu'), expected)

    def test_progress_brackets_generation(self):
        events = []
        runner = Runner('', Path('.'), {}, progress=lambda *event: events.append(event))
        with patch.object(runner, '_generate', return_value=({'ok': True}, {})):
            self.assertEqual(runner.generate('model', 'en', 'quality', {}, ['a']),
                             ({'ok': True}, {}))
        self.assertEqual(events, [('quality', ['a'], None), ('quality', ['a'], True)])

    def test_programming_errors_are_not_retried(self):
        calls = []
        def broken():
            calls.append(True)
            raise AssertionError('programming error')
        with tempfile.TemporaryDirectory() as folder:
            transport = Transport(defaults())
            with self.assertRaisesRegex(AssertionError, 'programming error'):
                transport._durable(Path(folder), {}, broken, attempts=4)
        self.assertEqual(len(calls), 1)

    def test_shared_embedding_endpoint(self):
        for suffix in ('', '/embeddings', '/chat/completions'):
            self.assertEqual(embedding_endpoint('https://example.test/v1' + suffix),
                             'https://example.test/v1/embeddings')

    def test_env_preserves_unmatched_quotes(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / '.env'
            path.write_text('export A="value"\nB=value\'\n', encoding='utf-8')
            self.assertEqual(env_values(path), {'A': 'value', 'B': "value'"})
