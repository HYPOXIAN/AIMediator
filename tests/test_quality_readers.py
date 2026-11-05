"""Readers accept quality records of both schema versions, each under its own rules (plan 4.2, step U4.5)."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import evidence_quality as quality
from aimediator.common import Failure, read, write
from aimediator.demo import demo
from aimediator.design_briefs import quality_design_errors
from aimediator.evidence import evidence_units
from aimediator.quality_scoring import evaluate
from aimediator.reporting import export_report
from aimediator.resources import asset_path
from aimediator.review import export_review, import_review, load_run

V1_POLICY = {**quality.json.loads(quality.POLICY_PATH.read_text(encoding='utf-8')),
             'version': 'evidence-quality-policy-v1', 'schema_version': quality.SCHEMA_V1}
V1_POLICY.pop('segmentation_version')


def review_and_report(test, run, root):
    """Export the review template, import it as an agent review and export the report with the overlay."""
    template, _ = export_review(run, root / 'template')
    decisions = read(template / 'decisions.json')
    decisions.update(reviewer_type='agent', reviewer_id='synthetic-test-reviewer')
    write(template / 'decisions.json', decisions)
    overlay, _ = import_review(run, template / 'decisions.json', root / 'overlay')
    report, _ = export_report(run, root / 'report', overlay)
    test.assertTrue((Path(report) / 'report.json').exists())


class QualityReaders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        demo(cls.root / 'demo', quiet=True)
        cls.cases = {c['source']['record_id']: c for c in read(asset_path('fixtures/cases.json'))}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def copy_run(self, name, mode='enforce'):
        target = self.root / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(self.root / 'demo' / mode, target)
        return target

    def test_v2_demo_run_is_reviewed_and_reported(self):
        run = self.root / 'demo/enforce'
        records = read(run / 'evidence-quality.json')
        self.assertTrue(records)
        self.assertEqual({r['schema_version'] for r in records}, {quality.SCHEMA_V2})
        completed = [r for r in records if r['status'] == 'completed']
        self.assertTrue(all(isinstance(r['annotation_v2'], dict) for r in completed))
        self.assertEqual(list(completed[0])[list(completed[0]).index('annotation') + 1], 'annotation_v2')
        self.assertEqual(len(load_run(run)['quality']), len(records))
        review_and_report(self, run, self.root / 'v2-review')

    def test_v2_records_are_checked_against_their_own_rules(self):
        for name, change in [
                ('label', lambda r: next(iter(r['annotation_v2']['segment_labels'].values())).update(scope='forged')),
                ('derived', lambda r: r['annotation']['segments'][0].update(reason_code='quoted_emotion')),
                ('missing', lambda r: r.pop('annotation_v2')),
                ('version', lambda r: r.update(schema_version='evidence-quality-v9'))]:
            with self.subTest(name):
                run = self.copy_run('tampered-' + name)
                records = read(run / 'evidence-quality.json')
                change(next(r for r in records if r['status'] == 'completed' and r['annotation']['segments']))
                write(run / 'evidence-quality.json', records)
                with self.assertRaises(Failure) as caught:
                    load_run(run)
                self.assertEqual(caught.exception.code, 2)

    def test_v1_run_folder_is_reviewed_and_reported(self):
        # Tests cannot check out older code: the quality records are v1 records built by qualify from the
        # v1 fixture annotations under the v1 policy, as the code before U4.4 wrote them. The shadow run is
        # used because its claims are not bound to quality points (enforce claims cite the v2 points).
        run = self.copy_run('v1-run', 'shadow')
        records = []
        for record in read(run / 'evidence-quality.json'):
            row = self.cases[record['comment_id']]['source']
            v1 = quality.qualify(self.cases[record['comment_id']]['annotation'], row,
                                 evidence_units(row['text_original']), V1_POLICY)
            v1.update(attempts=record['attempts'], model=record['model'], observation_only=record['observation_only'])
            self.assertNotIn('annotation_v2', v1)
            records.append(v1)
        write(run / 'evidence-quality.json', records)
        self.assertEqual({r['schema_version'] for r in load_run(run)['quality']}, {quality.SCHEMA_V1})
        review_and_report(self, run, self.root / 'v1-review')
        tampered = copy.deepcopy(records)
        target = next(r for r in tampered if r['status'] == 'completed' and r['annotation']['segments'])
        target['annotation']['segments'][0]['quote'] += 'x'
        write(run / 'evidence-quality.json', tampered)
        with self.assertRaises(Failure):
            load_run(run)

    def test_scoring_and_design_briefs_accept_both_versions(self):
        records = read(self.root / 'demo/enforce/evidence-quality.json')
        labels = []
        for r in records:
            c = self.cases[r['comment_id']]
            gold = quality.qualify(c['annotation'], c['source'], evidence_units(c['source']['text_original']), V1_POLICY)
            points = [r2['point_id'] for r2 in gold['routing'] if r2['point_id']]
            labels.append({'comment_id': r['comment_id'], 'language': c['source']['language'],
                           'text_original': c['source']['text_original'], 'content_sha256': r['content_sha256'],
                           'cluster_id': c['cluster_id'], 'split': 'development', 'source_stage': 'raw_pre_screen',
                           'reviewer_type': 'human', 'relevance': 'related', 'segments': c['annotation']['segments'],
                           'points': [{'point_id': g['point_id'], 'route': g['route'],
                                       'segment_ids': g['point']['segment_ids']} for g in gold['routing'] if g['point_id']],
                           'point_matches': [{'gold_point_id': p, 'predicted_point_id': p} for p in points],
                           'equivalence_group': None})
        v2 = evaluate(labels, records)
        v1 = evaluate(labels, [{**r, 'schema_version': quality.SCHEMA_V1} for r in records])
        self.assertEqual(v1, v2)
        with self.assertRaisesRegex(ValueError, 'Unknown quality schema version'):
            evaluate(labels, [{**records[0], 'schema_version': 'evidence-quality-v9'}] + records[1:])
        claims = read(self.root / 'demo/enforce/validated-claims.json')
        claim = next(c for c in claims if c.get('evidence_quality'))
        self.assertEqual(claim['evidence_quality']['schema_version'], quality.SCHEMA_V2)
        self.assertEqual(quality_design_errors(claim), [])
        as_v1 = copy.deepcopy(claim)
        as_v1['evidence_quality']['schema_version'] = quality.SCHEMA_V1
        self.assertEqual(quality_design_errors(as_v1), [])
        as_v1['evidence_quality']['schema_version'] = 'evidence-quality-v9'
        self.assertEqual(quality_design_errors(as_v1), ['mechanism_evidence_qualification_required'])

    def test_legacy_review_accepts_both_versions(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from support import case, qualified
        from test_evidence_quality import numeric_claim
        from aimediator import evidence
        from aimediator.legacy_review import apply_review, proposal_hash
        c = case('numeric_request')
        source = c['source']
        claim = numeric_claim()
        claim['quality_point_ids'] = ['P1']
        for version, accepted in ((quality.SCHEMA_V1, True), (quality.SCHEMA_V2, True), ('evidence-quality-v9', False)):
            with self.subTest(version):
                _, enriched = evidence.ground_claim(claim, source, {'Ryu'})
                _, qualification = quality.bind_claim(claim, qualified(c), evidence.character_reference(source['text_original']))
                qualification['schema_version'] = version
                enriched['evidence_quality'] = qualification
                enriched['semantic_audit'] = {'supported': True}
                proposals = {'a:1': {'comment_id': source['record_id'], 'model': 'fixture', 'claim': enriched}}
                decisions = {'a:1': {'decision': 'accept', 'reason': 'fixture', 'proposal_sha256': proposal_hash(enriched)}}
                arguments = (proposals, decisions, {source['record_id']: source}, {source['record_id']}, {'Ryu'})
                if accepted:
                    self.assertEqual(apply_review(*arguments)[0][0]['evidence_quality']['schema_version'], version)
                else:
                    with self.assertRaisesRegex(ValueError, 'unknown schema version'):
                        apply_review(*arguments)

    def test_stored_annotation_errors_dispatch(self):
        case = self.cases['synthetic:numeric_request:en']
        row = case['source']
        units = evidence_units(row['text_original'])
        v1 = quality.qualify(case['annotation'], row, units, V1_POLICY)
        self.assertEqual(quality.stored_annotation_errors(v1, row, units), [])
        self.assertEqual(quality.stored_annotation_errors({**v1, 'schema_version': None}, row, units), [])
        self.assertEqual(quality.stored_annotation_errors({**v1, 'schema_version': 'x'}, row, units),
                         ['Unknown quality schema version'])
        self.assertTrue(quality.stored_annotation_errors({**v1, 'schema_version': quality.SCHEMA_V2,
                                                          'annotation_v2': None}, row, units))


if __name__ == '__main__':
    unittest.main()
