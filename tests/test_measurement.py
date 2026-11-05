"""The measurement tool (aimediator.measurement) on synthetic run folders, a demo run and synthetic evaluation sets."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from aimediator.common import read
from aimediator.demo import demo
from aimediator.measurement import claim_outcomes, materialize, request_metrics, score_positions
from aimediator.quality_scoring import proportion

EMPTY = {'count': 0, 'sum': None, 'mean': None, 'median': None, 'max': None}
COUNTED = ('prompt_tokens', 'cached_tokens', 'uncached_tokens', 'output_tokens', 'prefill_seconds',
           'decode_seconds', 'load_seconds')


def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def counters(prompt, cached, output, prefill, decode, load=0.1):
    return {'prompt_eval_count': prompt, 'prompt_eval_cached_count': cached, 'eval_count': output,
            'prompt_eval_duration': int(prefill * 1e9), 'eval_duration': int(decode * 1e9),
            'load_duration': int(load * 1e9)}


def add_request(run, stage, name, model, user, result=None, elapsed=1.0, errors=None, provenance=None, reuse=False,
                system='S' * 10):
    folder = run / 'requests' / stage / name
    put(folder / 'request.json', {'model': model, 'messages': [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': json.dumps(user, ensure_ascii=False)}],
        'format': {'type': 'object'}, 'stream': True, 'keep_alive': '10m', 'options': {}})
    if result is not None:
        put(folder / 'response.json', {'elapsed_seconds': elapsed, 'response': result})
    if errors is not None:
        put(folder / 'validation.json', {'errors': errors, 'schema': {}})
    if provenance is not None:
        put(folder / 'transport-provenance.json', {'kind': provenance})
    if reuse:
        put(folder / 'reuse-provenance.json', {'source': 'cache', 'elapsed_seconds': 4.0})
    return folder


def stop(**extra):
    return {'done': True, 'done_reason': 'stop', 'message': {'content': '{}'}, **extra}


EXTRACT_USER = {'comments': [{'comment_id': 'c1', 'units': [
    {'evidence_id': 'E1', 'text': 'Ryu 强', 'start': 0, 'end': 5},
    {'evidence_id': 'E2', 'text': 'nerf', 'start': 6, 'end': 10}]}],
    'character_normalization_reference': [{'canonical': 'Ryu'}], 'response_schema': {'type': 'object'}}


class RequestMetricsTests(unittest.TestCase):
    def build(self, run):
        add_request(run, 'extract', 'a', 'm1', EXTRACT_USER, stop(**counters(1000, 200, 100, 2.0, 1.0)),
                    elapsed=3.0, errors=[])
        add_request(run, 'extract', 'b', 'm1', EXTRACT_USER, stop(**counters(3000, 400, 300, 4.0, 3.0)),
                    elapsed=5.0, errors=['$.assessments: missing keys'], provenance='fresh_inference')
        # The archived format of a reused request: original counters, almost no elapsed time.
        add_request(run, 'extract', 'c', 'm1', EXTRACT_USER, stop(**counters(500, 100, 50, 1.0, 0.5)),
                    elapsed=0.001, errors=[], provenance='reused_identical_model_request')
        # A loop guard stopped this one: no counters, which must give None and never zero.
        add_request(run, 'extract', 'd', 'm2', {'comments': [], 'response_schema': {}},
                    {'done': False, 'done_reason': 'duplicate_claim_loop', 'message': {'content': ''}},
                    elapsed=7.0, errors=['Incomplete generation'])
        # The U3.3 format of a reused request.
        add_request(run, 'extract', 'e', 'm2', {'comments': [], 'response_schema': {}}, stop(), elapsed=0,
                    errors=[], reuse=True)
        # Neither a nested transport attempt nor an embedding request is a chat request.
        put(run / 'requests' / 'extract' / 'a' / 'transport-attempts' / 'x' / 'request.json', {'model': 'm1'})
        add_request(run, 'embedding', 'z', 'm3', {}, stop(**counters(9, 9, 9, 9, 9)), errors=[])
        # Interrupted before its response: no response and no validation.
        add_request(run, 'verify', 'f', 'm1', {'claims': [], 'original_comment': 'Ryu', 'response_schema': {}})

    def test_counts_reuse_and_statistics_of_a_synthetic_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / 'run'
            self.build(run)
            metrics = request_metrics(run)
        self.assertEqual(list(metrics['stages']), ['extract', 'verify'])
        extract = metrics['stages']['extract']
        self.assertEqual((extract['all']['requests'], extract['all']['fresh'], extract['all']['reused']), (5, 3, 2))
        self.assertEqual(extract['all']['done_reason'], {'duplicate_claim_loop': 1, 'stop': 4})
        self.assertEqual(extract['all']['with_validation_errors'], 2)
        self.assertEqual(list(extract['models']), ['m1', 'm2'])
        m1, m2 = extract['models']['m1'], extract['models']['m2']
        self.assertEqual(m1['fresh_metrics']['prompt_tokens'],
                         {'count': 2, 'sum': 4000, 'mean': 2000, 'median': 2000.0, 'max': 3000})
        self.assertEqual(m1['fresh_metrics']['uncached_tokens']['mean'], 1700)
        self.assertEqual(m1['fresh_metrics']['prefill_seconds']['mean'], 3.0)
        self.assertEqual(m1['fresh_metrics']['decode_seconds']['max'], 3.0)
        self.assertAlmostEqual(m1['fresh_metrics']['load_seconds']['mean'], 0.1)
        self.assertEqual(m1['fresh_metrics']['elapsed_seconds']['mean'], 4.0)
        self.assertEqual(m1['reused_metrics']['prompt_tokens']['mean'], 500)
        self.assertEqual(m1['reused_metrics']['elapsed_seconds']['mean'], 0.001)
        for name in COUNTED:
            self.assertEqual(m2['fresh_metrics'][name], EMPTY, name)
            self.assertEqual(m2['reused_metrics'][name], EMPTY, name)
        self.assertEqual(m2['fresh_metrics']['elapsed_seconds']['mean'], 7.0)
        composition = m1['composition']
        user = json.dumps(EXTRACT_USER, ensure_ascii=False)
        self.assertEqual(composition['requests'], 3)
        self.assertEqual(composition['system_prompt'], 10)
        self.assertEqual(composition['format'], len('{"type": "object"}'))
        self.assertEqual(composition['user_message'], len(user))
        self.assertEqual(list(composition['user_keys']),
                         ['comments', 'character_normalization_reference', 'response_schema'])
        self.assertEqual(composition['user_keys']['comments'],
                         {'requests': 3, 'mean': len(json.dumps(EXTRACT_USER['comments'], ensure_ascii=False))})
        self.assertEqual(composition['nested'], {'comments[].units[].text': 9, 'comments[].text': 0,
                                                 'comments[].retrieved_topics': 0})
        verify = metrics['stages']['verify']['all']
        self.assertEqual((verify['done_reason'], verify['without_validation']), ({'no_response': 1}, 1))
        self.assertEqual(verify['fresh_metrics']['elapsed_seconds'], EMPTY)

    def test_wall_time_from_manifest_and_run_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            cli, legacy = Path(tmp) / 'cli', Path(tmp) / 'legacy'
            put(cli / 'manifest.json', {'schema_version': 'aimediator-run-v1',
                                        'created_at_utc': '2026-11-04T10:00:00.000000+00:00'})
            put(cli / 'run-state.json', {'run_state': 'completed', 'stage': 'full',
                                         'updated_at_utc': '2026-11-04T10:02:30.500000+00:00'})
            put(legacy / 'manifest.json', {'identity': {}, 'created_at_utc': '2026-10-28T02:21:13+00:00'})
            cli_run, legacy_run = request_metrics(cli)['run'], request_metrics(legacy)['run']
        self.assertEqual((cli_run['format'], cli_run['run_state'], cli_run['wall_seconds']), ('cli', 'completed', 150.5))
        self.assertEqual((legacy_run['format'], legacy_run['wall_seconds']), ('legacy', None))

    def test_demo_run_end_to_end_has_no_counters(self):
        with tempfile.TemporaryDirectory() as tmp:
            demo(Path(tmp) / 'demo', quiet=True)
            for mode in ('off', 'shadow', 'enforce'):
                run = Path(tmp) / 'demo' / mode
                metrics, outcomes = request_metrics(run), claim_outcomes(run)
                self.assertEqual((metrics['run']['format'], metrics['run']['run_state']), ('cli', 'completed'))
                self.assertGreaterEqual(metrics['run']['wall_seconds'], 0)
                stages = metrics['stages']
                self.assertIn('extract', stages)
                self.assertEqual('quality' in stages, mode != 'off')
                self.assertEqual(sum(s['all']['requests'] for s in stages.values()),
                                 len(read(run / 'run-state.json')['completed_request_identities']))
                for stage in stages.values():
                    self.assertEqual(stage['all']['fresh'], stage['all']['requests'])
                    for name in COUNTED:
                        self.assertEqual(stage['all']['fresh_metrics'][name], EMPTY, name)
                validated = read(run / 'validated-claims.json')
                quarantined = read(run / 'quarantined-claims.json')
                self.assertEqual(outcomes['claims']['accepted'], len(validated))
                self.assertEqual(outcomes['claims']['generated'], len(validated) + len(quarantined))
                self.assertEqual(sum(outcomes['coverage_status'].values()),
                                 len(read(run / 'full-pipeline-coverage.json')))
                quality = read(run / 'evidence-quality.json') if mode != 'off' else []
                self.assertEqual(outcomes['quality']['comments'], len(quality))


def labeled_run(folder):
    """A run with five comments, its relevance decisions, accepted and quarantined claims and quality records."""
    put(folder / 'source-snapshot.json', [{'record_id': c, 'language': l} for c, l in
                                          [('c1', 'en'), ('c2', 'en'), ('c3', 'zh'), ('c4', 'zh'), ('c5', 'en')]])
    put(folder / 'relevance.json', [{'comment_id': c, 'language': l, 'agreement': a} for c, l, a in
                                    [('c1', 'en', True), ('c2', 'en', True), ('c3', 'zh', False),
                                     ('c4', 'zh', True), ('c5', 'en', True)]])
    put(folder / 'validated-claims.json', [{'comment_id': c, 'character': ch, 'direction': d} for c, ch, d in
                                           [('c1', 'Ryu', 'nerf'), ('c1', 'Ryu', 'nerf'), ('c2', 'Ryu', 'buff'),
                                            ('c3', 'JP', 'nerf'), ('c4', 'Ken', 'buff')]])
    put(folder / 'quarantined-claims.json', [
        {'comment_id': 'c1', 'claim': {'character': 'Ken', 'direction': 'buff'}, 'stage': 'source_binding',
         'errors': ['Parameter lacks requested target or delta']},
        {'comment_id': 'c3', 'claim': {'character': 'JP', 'direction': 'buff'}, 'stage': 'semantic_audit',
         'audit': {'support_status': 'unsupported'}, 'errors': ['Model source-support status: unsupported']},
        {'comment_id': 'c3', 'claim': None, 'stage': 'source_binding', 'errors': ['No claim object']}])
    put(folder / 'full-pipeline-coverage.json', [{'comment_id': c, 'language': l, 'status': s} for c, l, s in
                                                 [('c1', 'en', 'extraction_completed'), ('c2', 'en', 'extraction_completed'),
                                                  ('c3', 'zh', 'relevance_rejected'), ('c4', 'zh', 'extraction_completed'),
                                                  ('c5', 'en', 'extraction_failed')]])
    literal = 'Literal absent from selected spans: character_literal'
    put(folder / 'evidence-quality.json', [
        {'comment_id': 'c1', 'status': 'completed', 'attempts': [{'errors': []}],
         'routes_present': ['opinion_only'], 'routing': [{'route': 'opinion_only'}, {'route': 'opinion_only'}]},
        {'comment_id': 'c2', 'status': 'failed', 'attempts': [{'errors': [literal]}, {'errors': [literal]}],
         'routes_present': ['review'], 'routing': [{'route': 'review'}]}])


LABELS = [
    {'comment_id': 'c1', 'language': 'en', 'split': 'development', 'uncertain': False,
     'positions': [{'character': 'Ryu', 'direction': 'nerf'}, {'character': 'Ken', 'direction': 'buff'}]},
    {'comment_id': 'c2', 'language': 'en', 'split': 'development', 'uncertain': False, 'positions': []},
    {'comment_id': 'c3', 'language': 'zh', 'split': 'development', 'uncertain': False,
     'positions': [{'character': 'JP', 'direction': 'nerf'}]},
    {'comment_id': 'c4', 'language': 'zh', 'split': 'development', 'uncertain': True, 'positions': []},
    {'comment_id': 'c5', 'language': 'en', 'split': 'test', 'uncertain': False,
     'positions': [{'character': 'Ryu', 'direction': 'nerf'}]},
    {'comment_id': 'c6', 'language': 'en', 'split': 'development', 'uncertain': False,
     'positions': [{'character': 'Ken', 'direction': 'nerf'}]}]


class OutcomeAndScoreTests(unittest.TestCase):
    def test_claim_outcomes_by_stage_language_and_direction(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / 'run'
            labeled_run(run)
            outcomes = claim_outcomes(run)
        self.assertEqual(outcomes['claims'], {'generated': 7, 'binding_quarantined': 1, 'audited': 6,
                                              'audit_rejected': 1, 'accepted': 5, 'audit_rejection': proportion(1, 6)})
        self.assertEqual(outcomes['binding_errors'], {'Parameter lacks requested target or delta': 1})
        self.assertEqual(outcomes['audit_status'], {'unsupported': 1})
        self.assertEqual({k: v['generated'] for k, v in outcomes['by_language'].items()}, {'en': 4, 'zh': 3})
        zh = outcomes['by_language_direction']['zh']
        self.assertEqual((zh['nerf']['accepted'], zh['buff']['audit_rejected'], zh['buff']['accepted']), (1, 1, 1))
        self.assertEqual(outcomes['coverage_status'], {'extraction_completed': 3, 'extraction_failed': 1,
                                                       'relevance_rejected': 1})
        quality = outcomes['quality']
        self.assertEqual(quality['first_attempt_valid'], proportion(1, 2))
        self.assertEqual(quality['attempts'], {'total': 3, 'per_comment': {'1': 1, '2': 1}})
        self.assertEqual(quality['attempt_errors'], {'Literal absent from selected spans: character_literal': 2})
        self.assertEqual(quality['route_comments'], {'opinion_only': 1, 'review': 1})
        self.assertEqual(quality['route_items'], {'opinion_only': 2, 'review': 1})

    def test_precision_and_recall_computed_by_hand(self):
        with tempfile.TemporaryDirectory() as tmp:
            run, labels = Path(tmp) / 'run', Path(tmp) / 'set'
            labeled_run(run)
            labels.mkdir()
            (labels / 'labels.jsonl').write_text(''.join(json.dumps(l) + '\n' for l in LABELS), encoding='utf-8')
            scores = score_positions(run, labels, 'development')
        self.assertEqual((scores['labels'], scores['split'], scores['labeled_comments'], scores['absent_from_run']),
                         ('set', 'development', 5, 1))
        overall = scores['overall']
        # Scored: c1, c2, c3 (c4 uncertain, c5 test split, c6 absent from the run).
        self.assertEqual((overall['comments'], overall['admitted_comments']), (3, 2))
        # Accepted: c1 Ryu nerf twice (correct), c2 Ryu buff (wrong), c3 JP nerf (correct).
        self.assertEqual(overall['precision_accepted'], proportion(3, 4))
        # Generated adds c1 Ken buff (correct) and c3 JP buff (wrong); the entry without a claim object is skipped.
        self.assertEqual(overall['precision_generated'], proportion(4, 6))
        # Positions c1 Ryu nerf, c1 Ken buff, c3 JP nerf; accepted claims find the first and the third once each.
        self.assertEqual(overall['recall'], proportion(2, 3))
        # c3 is not admitted, so only the two c1 positions count.
        self.assertEqual(overall['recall_admitted'], proportion(1, 2))
        self.assertEqual(overall['uncertain'], {'comments': 1, 'accepted_claims': 1, 'generated_claims': 1})
        en, zh = scores['by_language']['en'], scores['by_language']['zh']
        self.assertEqual((en['precision_accepted'], en['precision_generated'], en['recall'], en['recall_admitted']),
                         (proportion(2, 3), proportion(3, 4), proportion(1, 2), proportion(1, 2)))
        self.assertEqual((zh['precision_accepted'], zh['precision_generated'], zh['recall'], zh['recall_admitted']),
                         (proportion(1, 1), proportion(1, 2), proportion(1, 1), proportion(0, 0)))
        self.assertEqual(zh['uncertain'], {'comments': 1, 'accepted_claims': 1, 'generated_claims': 1})
        self.assertIsNone(zh['recall_admitted']['value'])


ROWS = [{'record_id': 'r1', 'language': 'en', 'text_original': 'Ryu is too strong', 'source_url': 'u1'},
        {'record_id': 'r2', 'language': 'zh', 'text_original': '请加强JP', 'source_url': 'u2'},
        {'record_id': 'r3', 'language': 'en', 'text_original': 'Ken needs a buff', 'source_url': 'u3'}]


class MaterializeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        # Key order and spacing differ from json.dumps defaults, so an unchanged row is visible.
        self.lines = [json.dumps(r, ensure_ascii=False, separators=(',', ':')) for r in ROWS]
        self.dataset = self.root / 'records.jsonl'
        self.dataset.write_text('\n'.join(self.lines) + '\n\n', encoding='utf-8')

    def tearDown(self):
        self.tmp.cleanup()

    def make_set(self, name, ids=None, labels=None, manifest=None):
        folder = self.root / name
        folder.mkdir()
        if ids is not None:
            put(folder / 'ids.json', ids)
        if labels is not None:
            (folder / 'labels.jsonl').write_text(''.join(json.dumps(l, ensure_ascii=False) + '\n' for l in labels),
                                                 encoding='utf-8')
        if manifest is not None:
            put(folder / 'manifest.json', manifest)
        return folder

    def test_three_label_formats_keep_rows_unchanged_in_set_order(self):
        ids = self.make_set('ids', ids=[{'record_id': r['record_id'], 'content_sha256': sha(r['text_original'])}
                                        for r in (ROWS[2], ROWS[0])])
        self.assertEqual(materialize(ids, self.dataset), (self.lines[2] + '\n' + self.lines[0] + '\n').encode())
        content = self.make_set('content', labels=[
            {'comment_id': r['record_id'], 'content_sha256': sha(r['text_original']), 'split': s}
            for r, s in ((ROWS[1], 'development'), (ROWS[0], 'test'), (ROWS[2], 'development'))])
        self.assertEqual(materialize(content, self.dataset, 'development').decode(),
                         self.lines[1] + '\n' + self.lines[2] + '\n')
        self.assertEqual(materialize(content, self.dataset).decode().splitlines(),
                         [self.lines[1], self.lines[0], self.lines[2]])
        silver = self.make_set('silver', labels=[
            {'comment_id': 'r2', 'source_sha256': sha(ROWS[1]['text_original']), 'split': 'holdout'}])
        self.assertEqual(materialize(silver, self.dataset, 'holdout').decode(), self.lines[1] + '\n')

    def test_missing_row_and_hash_mismatch_raise(self):
        missing = self.make_set('missing', ids=[{'record_id': 'r9', 'content_sha256': sha('x')}])
        with self.assertRaisesRegex(ValueError, 'Row missing from dataset: r9'):
            materialize(missing, self.dataset)
        changed = self.make_set('changed', ids=[{'record_id': 'r1', 'content_sha256': sha('Ryu is too weak')}])
        with self.assertRaisesRegex(ValueError, 'Content hash differs: r1'):
            materialize(changed, self.dataset)

    def test_manifest_hashes_are_checked(self):
        ids = [{'record_id': 'r1', 'content_sha256': sha(ROWS[0]['text_original'])}]
        tampered = self.make_set('tampered', ids=ids, manifest={'ids_sha256': sha('other')})
        with self.assertRaisesRegex(ValueError, 'differs from its manifest'):
            materialize(tampered, self.dataset)
        foreign = self.make_set('foreign', ids=ids, manifest={'source_dataset_sha256': sha('other')})
        with self.assertRaisesRegex(ValueError, 'Dataset differs'):
            materialize(foreign, self.dataset)
        file_sha = hashlib.sha256(self.dataset.read_bytes()).hexdigest()
        good = self.make_set('good', ids=ids, manifest={'source_dataset_sha256': file_sha})
        good_ids = hashlib.sha256((good / 'ids.json').read_bytes()).hexdigest()
        put(good / 'manifest.json', {'source_dataset_sha256': file_sha, 'ids_sha256': good_ids})
        self.assertEqual(materialize(good, self.dataset), (self.lines[0] + '\n').encode())
        with self.assertRaisesRegex(ValueError, 'no splits'):
            materialize(good, self.dataset, 'development')


def script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / 'experiments' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ScriptTests(unittest.TestCase):
    def test_scripts_write_the_module_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            run, labels = tmp / 'run', tmp / 'set'
            labeled_run(run)
            add_request(run, 'extract', 'a', 'm1', EXTRACT_USER, stop(), errors=[])
            labels.mkdir()
            (labels / 'labels.jsonl').write_text(''.join(json.dumps({**l, 'content_sha256': sha(l['comment_id'])}) + '\n'
                                                         for l in LABELS), encoding='utf-8')
            self.assertEqual(script('measure_run_requests').main(['--run', str(run), '--out', str(tmp / 'm.json')]), 0)
            self.assertEqual(read(tmp / 'm.json'), {'request_metrics': request_metrics(run),
                                                    'claim_outcomes': claim_outcomes(run)})
            self.assertEqual(script('score_extraction').main(['--run', str(run), '--labels', str(labels),
                                                              '--split', 'development', '--out', str(tmp / 's.json')]), 0)
            self.assertEqual(read(tmp / 's.json'), score_positions(run, labels, 'development'))
            dataset = tmp / 'records.jsonl'
            dataset.write_text(''.join(json.dumps({'record_id': l['comment_id'], 'language': l['language'],
                                                   'text_original': l['comment_id']}) + '\n' for l in LABELS),
                               encoding='utf-8')
            out = tmp / 'inputs' / 'set.jsonl'
            self.assertEqual(script('materialize_evaluation_input').main(
                ['--set', str(labels), '--dataset', str(dataset), '--split', 'test', '--out', str(out)]), 0)
            self.assertEqual(out.read_bytes(), materialize(labels, dataset, 'test'))
            self.assertEqual(sorted(p.name for p in out.parent.iterdir()), ['set.jsonl'])


if __name__ == '__main__':
    unittest.main()
