"""Legacy console text of ``engine.run`` (plan step B1.5), pinned for B5.7.

The behavior lock's L2 producer runs the legacy runner in ``enforce`` mode on
the packaged fixture sources. Its stdout holds no time, path or hash, so the
lines are compared exactly, without normalization.
"""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import behavior_lock as lock

# (stage, items) for every request one model makes, in order.
REQUESTS = ([('relevance', 8), ('relevance', 8), ('relevance', 3)] + [('quality', 1)] * 19
            + [('extract', 4), ('extract', 4), ('extract', 1)] + [('verify', 1)] * 10)

SUMMARY = '''{
  "version": "balance-evidence-v2",
  "input_comments": 38,
  "mode": "full_pipeline",
  "input_languages": {
    "zh": 19,
    "en": 19
  },
  "routed_comments": 38,
  "unsupported_or_unselected_language": 0,
  "retrieval_related": 38,
  "retrieval_review_queued": 0,
  "retrieval_review_rescues": 0,
  "agreement_related": 38,
  "relevance_refinements": 0,
  "relevance_refinement_rescues": 0,
  "assessed_comments": 18,
  "generated_claims": 20,
  "accepted_claims": 20,
  "quarantined_claims": 0,
  "source_numeric_accepted": 2,
  "qualitative_only_accepted": 18,
  "failed_requests": 0,
  "final_generation_failed_comments": 0,
  "by_language": {
    "en": {
      "input": 19,
      "retrieval_related": 19,
      "agreement_related": 19,
      "accepted_claims": 10
    },
    "zh": {
      "input": 19,
      "retrieval_related": 19,
      "agreement_related": 19,
      "accepted_claims": 10
    }
  },
  "limitations": [
    "Automated semantic audit uses the same language-routed model in a separate context; not human ground truth.",
    "Retrieval prototypes and threshold are reused from the earlier experiment; no held-out relevance labels exist for the full corpus.",
    "Source binding proves quotation provenance, not gameplay truth or patch applicability.",
    "Semantic audit reads the full original comment; selected citations can still need additional context.",
    "Coverage accounts for every admitted comment; completeness of individual concerns still requires human review.",
    "No numerical targets are invented; qualitative comments cannot supply exact engineering values."
  ]
}'''


def expected_lines():
    # Step U3.4: one record per text, the missing texts embedded in batches of 32.
    embedding = ['Embedding %d/58' % n for n in (32, 58)]
    requests = ['%s: %s, %d items' % (stage, model, items)
                for model in ('llama3.1:latest', 'qwen2.5:7b') for stage, items in REQUESTS]
    return embedding + requests + SUMMARY.split('\n')


class LegacyConsoleOutputTests(unittest.TestCase):
    def test_enforce_run_prints_progress_and_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = lock.run_legacy(root, lock.legacy_dataset(root), 'enforce')
        self.assertTrue(output.endswith('}\n'))
        self.assertEqual(output.split('\n')[:-1], expected_lines())


if __name__ == '__main__':
    unittest.main()
