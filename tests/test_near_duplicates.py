"""Near-duplicate clusters of comment vectors (pipeline upgrade U6.5, plan 4.9, ALG-05, UP-D14)."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import quality_scoring  # noqa: E402
from aimediator.common import read  # noqa: E402
from aimediator.demo import demo  # noqa: E402
from aimediator.reporting import export_report  # noqa: E402
from aimediator.resources import asset_path  # noqa: E402
from aimediator.retrieval import near_duplicate_clusters  # noqa: E402


def unit(angle):
    return [np.cos(angle), np.sin(angle)]


class ClusterTest(unittest.TestCase):
    def test_single_linkage_threshold_and_maxima(self):
        # Angles chosen so a-b and b-c pass 0.9 but a-c does not; d is alone; e equals f.
        angles = {'a': 0.0, 'b': 0.4, 'c': 0.8, 'd': 2.0, 'e': 3.0, 'f': 3.0}
        ids = list(angles)
        vectors = np.asarray([unit(angles[i]) for i in ids], dtype=np.float64)
        clusters = near_duplicate_clusters(ids, vectors, 0.9, block=2)
        ab = round(float(np.cos(0.4)), 6)
        self.assertEqual([c['cluster_id'] for c in clusters], ['D1', 'D2'])
        self.assertEqual(clusters[0]['comment_ids'], ['a', 'b', 'c'])
        self.assertEqual(clusters[0]['pairs'], [{'comment_ids': ['a', 'b'], 'cosine': ab},
                                                {'comment_ids': ['b', 'c'], 'cosine': ab}])
        self.assertEqual(clusters[0]['members'], [{'comment_id': i, 'max_cosine': ab} for i in 'abc'])
        self.assertEqual(clusters[0]['max_cosine'], ab)
        self.assertEqual(clusters[1]['comment_ids'], ['e', 'f'])
        self.assertEqual(clusters[1]['max_cosine'], 1.0)
        # A threshold equal to the cosine still links (at or above).
        exact = min(float(vectors[0] @ vectors[1]), float(vectors[1] @ vectors[2]))
        self.assertEqual(len(near_duplicate_clusters(ids, vectors, exact, block=4)[0]['comment_ids']), 3)
        self.assertEqual(len(near_duplicate_clusters(ids, vectors, np.nextafter(exact, 2), block=4)[0]['comment_ids']), 2)
        self.assertEqual(near_duplicate_clusters(ids, vectors, 1.01), [])
        self.assertEqual(near_duplicate_clusters([], np.zeros((0, 2)), 0.9), [])

    def test_policy_key(self):
        policy = json.loads(asset_path('configs/balance-review-policy.json').read_text(encoding='utf-8'))
        self.assertEqual(policy['version'], 'balance-review-policy-v3')
        self.assertEqual(policy['near_duplicate_cosine'], 0.9)
        self.assertEqual(policy['calibration']['label_set'], 'balance-silver-v1')


class RunAndReportTest(unittest.TestCase):
    def test_demo_writes_clusters_and_the_report_annotates_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'demo'
            demo(root, quiet=True)
            near = read(root / 'enforce' / 'near-duplicates.json')
            self.assertEqual((near['schema_version'], near['policy_version'], near['near_duplicate_cosine'],
                              near['linkage']), ('near-duplicates-v1', 'balance-review-policy-v3', 0.9, 'single'))
            self.assertEqual(near['comments'], len(read(root / 'enforce' / 'retrieval.json')))
            report = read(export_report(root / 'enforce', Path(tmp) / 'report')[0] / 'report.json')
            self.assertEqual(report['near_duplicate_clusters']['clusters'], near['clusters'])
            self.assertIn('no count changes', report['near_duplicate_clusters']['note'])
            # A run folder without the file (an earlier run) reports null.
            (root / 'off' / 'near-duplicates.json').unlink()
            report = read(export_report(root / 'off', Path(tmp) / 'report-off')[0] / 'report.json')
            self.assertIsNone(report['near_duplicate_clusters'])


class SplitTest(unittest.TestCase):
    def test_prepare_dataset_keeps_near_duplicates_in_one_split(self):
        rows = [{'record_id': 'r%d' % i, 'language': 'en', 'text_original': 'comment number %d' % i}
                for i in range(40)]
        with tempfile.TemporaryDirectory() as tmp:
            plain = quality_scoring.prepare_dataset(rows, 'screened', Path(tmp) / 'a', limit=100)
            split = {r['comment_id']: r['split'] for r in plain}
            # Pick a development and a test comment and declare them near-duplicates.
            dev = next(i for i, s in split.items() if s == 'development')
            test = next(i for i, s in split.items() if s == 'test')
            merged = quality_scoring.prepare_dataset(rows, 'screened', Path(tmp) / 'b', limit=100,
                                                     near_duplicates=[{'comment_ids': [dev, test, 'absent']}])
            by_id = {r['comment_id']: r for r in merged}
            self.assertEqual(by_id[dev]['split'], by_id[test]['split'])
            self.assertEqual(by_id[dev]['cluster_id'], by_id[test]['cluster_id'])
            self.assertEqual(len(merged), 40)
            others = {i for i in split if i not in (dev, test)}
            self.assertEqual({i: by_id[i]['split'] for i in others}, {i: split[i] for i in others})
            self.assertIn('near-duplicate', read(Path(tmp) / 'b' / 'manifest.json')['split_rule'])
            self.assertNotIn('near-duplicate', read(Path(tmp) / 'a' / 'manifest.json')['split_rule'])


if __name__ == '__main__':
    unittest.main()
