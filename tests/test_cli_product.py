"""Product gates: immutable evidence, durable attempts and portable workflows."""
import contextlib
import copy
import fcntl
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from aimediator import evidence
from aimediator.cli import main
from aimediator.common import Failure, canonical, input_rows, read, sha, write
from aimediator.config import defaults, credential, resolve
from aimediator.demo import FixtureTransport
from aimediator.inference import Transport
from aimediator.operations import analyze, doctor, status
from aimediator.review import export_review, import_review, load_run
from aimediator.reporting import export_report, groups_for
from aimediator.evaluation import evaluate_quality
from aimediator.resources import asset_path
from aimediator import run_store


class ProductTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.cases=read(asset_path('fixtures/cases.json'))
        self.cases=[c for c in self.cases if 'numeric_request' in c['source']['record_id']]
        self.input=self.root/'input with spaces.jsonl'
        self.input.write_bytes(b''.join(canonical(c['source'])+b'\n' for c in self.cases))
        self.cfg=defaults();self.cfg['base_url']='http://fixture.invalid';self.cfg['evidence_quality']='enforce'
        self.transport=FixtureTransport(self.cfg)

    def run_fixture(self, name='run', cfg=None, transport=None):
        out=self.root/name
        analyze(self.input,out,cfg or self.cfg,transport=transport or self.transport,quiet=True)
        return out

    def review_decisions(self,run):
        template,_=export_review(run,self.root/'template')
        path=template/'decisions.json';decisions=read(path)
        decisions.update(reviewer_type='agent',reviewer_id='synthetic-test-reviewer')
        return path,decisions

    def expect_failure(self,code,func,*args,**kwargs):
        with self.assertRaises(Failure) as result:func(*args,**kwargs)
        self.assertEqual(result.exception.code,code)

    def test_strict_input_preflight_no_calls(self):
        invalid=[b'',b'{"record_id":"a","record_id":"a"}',b'{"record_id":"a","text_original":"x","language":"en","x":1e999}',
            b'{"record_id":3,"text_original":"x","language":"en"}',b'{"record_id":"a","text_original":"x","language":"fr"}']
        for raw in invalid:
            self.input.write_bytes(raw)
            self.expect_failure(2,analyze,self.input,self.root/'bad',self.cfg,transport=self.transport)
            self.assertFalse((self.root/'bad').exists())
        self.assertEqual(self.transport.calls,[])

    def test_source_snapshot_unsupported_unicode_and_extra_metadata(self):
        rows=[c['source'] for c in self.cases]
        rows.append({'record_id':'emoji','text_original':'😀 Ryu!','language':'fr','extra':{'keep':True}})
        self.input.write_bytes(b''.join(canonical(r)+b'\n' for r in rows))
        raw=self.input.read_bytes();run=self.run_fixture()
        self.assertEqual((run/'input-snapshot.jsonl').read_bytes(),raw)
        self.assertEqual(read(run/'source-snapshot.json')[-1]['extra'],{'keep':True})
        ledger=read(run/'full-pipeline-coverage.json')
        self.assertEqual({r['comment_id'] for r in ledger},{r['record_id'] for r in rows})
        self.assertEqual(ledger[-1]['status'],'unsupported_language')
        text='😀 Ryu. 龙！';units=evidence.evidence_units(text)
        for unit in units:self.assertEqual(text[unit['start']:unit['end']],unit['text'])

    def test_completed_resume_relocation_no_generation(self):
        run=self.run_fixture();self.input.unlink()
        before=len(self.transport.calls)
        relocated=self.root/'relocated';run.rename(relocated)
        analyze(resume=relocated,transport=self.transport,quiet=True)
        self.assertEqual(len(self.transport.calls),before)
        self.assertEqual(status(relocated)['run_state'],'completed')

    def test_resume_identity_mismatch_no_mutation_or_calls(self):
        run=self.run_fixture();cfg=read(run/'resolved-config.json');cfg['num_gpu']=0;write(run/'resolved-config.json',cfg)
        before={str(p.relative_to(run)):p.read_bytes() for p in run.rglob('*') if p.is_file()}
        calls=len(self.transport.calls)
        self.expect_failure(4,analyze,resume=run,transport=self.transport)
        self.assertEqual(len(self.transport.calls),calls)
        self.assertEqual(before,{str(p.relative_to(run)):p.read_bytes() for p in run.rglob('*') if p.is_file()})

    def test_model_mismatch_before_mutation(self):
        run=self.run_fixture();before=(run/'run-state.json').read_bytes()
        with patch.object(self.transport,'tags',return_value={'models':[{'name':m,'digest':'changed'} for m in list(self.cfg['routing']['models'])+[self.cfg['embedding']['model']]]}):
            self.expect_failure(4,analyze,resume=run,transport=self.transport)
        self.assertEqual(before,(run/'run-state.json').read_bytes())

    def test_new_output_never_implicitly_resumes(self):
        run=self.run_fixture();calls=len(self.transport.calls)
        self.expect_failure(4,analyze,self.input,run,self.cfg,transport=self.transport)
        self.assertEqual(len(self.transport.calls),calls)

    def test_offline_doctor_invalid_modes_and_output_do_not_call_network(self):
        with patch('urllib.request.urlopen',side_effect=AssertionError('network')):
            result=doctor(defaults(),self.input,self.root/'prospective',offline=True)
        self.assertEqual(result['checks']['service_models'],'not_checked');self.assertFalse((self.root/'prospective').exists())
        for mode,stop in [('off','quality'),('shadow','relevance'),('enforce','relevance')]:
            cfg=copy.deepcopy(self.cfg);cfg.update(evidence_quality=mode,stop_after=stop)
            self.expect_failure(2,analyze,self.input,self.root/'bad',cfg,transport=self.transport)
        self.assertEqual(self.transport.calls,[])

    def test_quality_failure_budget_survives_repeated_resume(self):
        original=self.transport.chat
        calls=[]
        def chat(base,payload,partial):
            if 'segments' in payload['format']['properties']:
                calls.append(payload)
                return {'done':True,'done_reason':'stop','message':{'content':'{}'}}
            return original(base,payload,partial)
        self.transport.chat=chat
        run=self.root/'run'
        self.expect_failure(5,analyze,self.input,run,self.cfg,transport=self.transport,quiet=True)
        attempts=len(calls);self.assertEqual(attempts,2*len(self.cases))
        for _ in range(2):self.expect_failure(5,analyze,resume=run,transport=self.transport,quiet=True)
        self.assertEqual(len(calls),attempts)
        self.assertTrue(status(run)['has_failures'])

    def test_transport_crash_consumes_attempt_without_reissuing(self):
        transport=Transport(self.cfg,folder=self.root/'store')
        directory=self.root/'attempt';count=[]
        def crash():count.append(1);raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):transport._durable(directory,{'test':True},crash)
        self.expect_failure(5,transport._durable,directory,{'test':True},lambda:count.append(1))
        self.assertEqual(len(count),1)
        self.assertEqual(read(directory/'attempt-1.json')['state'],'interrupted')

    def test_quality_interruption_resumes_remaining_attempt(self):
        calls=[];original=self.transport.chat
        def chat(base,payload,partial):
            if 'segments' in payload['format']['properties']:
                calls.append(1)
                if len(calls)==1:
                    partial.write_text('{"partial":',encoding='utf-8');raise KeyboardInterrupt()
            return original(base,payload,partial)
        # Fixture transport bypasses durable production transport intentionally;
        # use production durability around the fixture chat to test crash recovery.
        durable=Transport(self.cfg)
        def wrapped(base,payload,partial):
            try:return durable._durable(partial.parent/'transport-attempts',payload,lambda:chat(base,payload,partial))
            except Failure:return {'done':False,'done_reason':'exhausted','message':{'content':''}}
        self.transport.chat=wrapped
        run=self.root/'run'
        self.expect_failure(130,analyze,self.input,run,self.cfg,transport=self.transport,quiet=True)
        self.assertEqual(status(run)['run_state'],'interrupted')
        analyze(resume=run,transport=self.transport,quiet=True)
        self.assertEqual(status(run)['run_state'],'completed')
        self.assertTrue(list(run.rglob('interrupted-partial-*.txt')))

    def test_writer_lock_conflict(self):
        run=self.run_fixture();state=read(run/'run-state.json');state['run_state']='interrupted';write(run/'run-state.json',state)
        before=(run/'run-state.json').read_bytes()
        with run_store.lock(run):self.expect_failure(4,analyze,resume=run,transport=self.transport)
        self.assertEqual(before,(run/'run-state.json').read_bytes())

    def test_untouched_template_accepts_nothing(self):
        run=self.run_fixture();path,decisions=self.review_decisions(run)
        self.expect_failure(2,import_review,run,path,self.root/'invalid')
        write(path,decisions)
        overlay,counts=import_review(run,path,self.root/'overlay')
        self.assertEqual(counts['source_accepted_claims'],0)
        exported,_=export_report(run,self.root/'report',overlay)
        report=read(exported/'report.json');self.assertEqual(report['counts']['formal_claims'],0)
        self.assertTrue(report['source_review_queue'])

    def test_correction_loses_audit_and_never_mutates_run(self):
        run=self.run_fixture();path,decisions=self.review_decisions(run)
        before={str(p):p.read_bytes() for p in run.rglob('*') if p.is_file()}
        claim_id=next(iter(decisions['decisions']))
        decisions['decisions'][claim_id].update(decision='accept',reason='synthetic context correction',recommendation='Ryu needs a change.')
        write(path,decisions);overlay,_=import_review(run,path,self.root/'overlay')
        claim=read(overlay/'source-reviewed-claims.json')[0]
        self.assertIsNone(claim['semantic_audit']);self.assertEqual(claim['audit_status'],'pending_reaudit');self.assertFalse(claim['formal_eligible'])
        out,_=export_report(run,self.root/'report',overlay);report=read(out/'report.json')
        self.assertEqual(report['counts']['formal_claims'],0);self.assertEqual(report['counts']['review_appendix_claims'],1)
        self.assertEqual(before,{str(p):p.read_bytes() for p in run.rglob('*') if p.is_file()})

    def test_review_fingerprint_exact_coverage_and_no_bypass(self):
        run=self.run_fixture();path,decisions=self.review_decisions(run)
        bad=copy.deepcopy(decisions);bad['source_sha256']='wrong';write(path,bad)
        self.expect_failure(4,import_review,run,path,self.root/'bad')
        bad=copy.deepcopy(decisions);bad['decisions'].pop(next(iter(bad['decisions'])));write(path,bad)
        self.expect_failure(2,import_review,run,path,self.root/'bad')
        bad=copy.deepcopy(decisions);item=next(iter(bad['decisions'].values()));item.update(decision='accept',corrected_direction='buff',reason='cannot bypass point direction');write(path,bad)
        self.expect_failure(2,import_review,run,path,self.root/'bad')

    def test_quarantined_source_acceptance_retains_automatic_failure(self):
        original=self.transport.chat
        def chat(base,payload,partial):
            if 'support' in payload['format']['properties']:
                return {'done':True,'done_reason':'stop','message':{'content':'{"support":"unsupported"}'}}
            return original(base,payload,partial)
        self.transport.chat=chat;run=self.run_fixture();path,decisions=self.review_decisions(run)
        for item in decisions['decisions'].values():item.update(decision='accept',reason='synthetic source review')
        write(path,decisions);overlay,counts=import_review(run,path,self.root/'overlay')
        self.assertGreater(counts['source_accepted_claims'],0);self.assertEqual(counts['formal_eligible_claims'],0)
        for claim in read(overlay/'source-reviewed-claims.json'):
            self.assertTrue(claim['automatic_errors']);self.assertFalse(claim['semantic_audit']['supported'])

    def test_report_deterministic_distinct_comments_and_conflicts(self):
        run=self.run_fixture()
        a,_=export_report(run,self.root/'report-a');b,_=export_report(run,self.root/'report-b')
        for name in ('report.md','report.json'):self.assertEqual((a/name).read_bytes(),(b/name).read_bytes())
        data=load_run(run);claim=next(iter(data['proposals'].values()))['claim'];cid=claim['comment_id']
        copies=[{**claim,'claim_id':str(i),'comment_id':cid,'direction':d} for i,d in enumerate(('buff','buff','nerf','keep','unclear'))]
        groups,_=groups_for(copies,data['sources']);g=groups[0]
        self.assertEqual(g['union_comment_count'],1);self.assertEqual(g['directions']['buff']['supporting_comment_count'],1)
        self.assertEqual(g['direction_overlap_comment_ids'],[cid])

    def test_legacy_allowlist_and_missing_quality(self):
        run=self.run_fixture();(run/'manifest.json').unlink()
        self.assertTrue(load_run(run)['legacy'])
        raw=read(run/'balance-report.json');raw['report_schema_version']='unknown';write(run/'balance-report.json',raw)
        self.expect_failure(2,load_run,run)
        raw['report_schema_version']='balance-report-v3';write(run/'balance-report.json',raw);(run/'evidence-quality.json').unlink()
        self.expect_failure(2,load_run,run)

    def test_overlay_tampering_is_rejected(self):
        run=self.run_fixture();path,decisions=self.review_decisions(run)
        for item in decisions['decisions'].values():item.update(decision='accept',reason='synthetic review')
        write(path,decisions);overlay,_=import_review(run,path,self.root/'overlay')
        claims=read(overlay/'source-reviewed-claims.json');claims[0]['recommendation']='injected';write(overlay/'source-reviewed-claims.json',claims)
        self.expect_failure(4,export_report,run,self.root/'report',overlay)

    def test_no_derived_output_inside_run(self):
        run=self.run_fixture()
        self.expect_failure(4,export_report,run,run/'report')
        self.expect_failure(4,export_review,run,run/'review')

    def test_structured_errors_are_one_json_document(self):
        for args,expected in [(['analyze','--json'],2),(['status','--json'],2),(['report','--run',str(self.root/'missing'),'--out',str(self.root/'out'),'--json'],2)]:
            output=io.StringIO()
            with contextlib.redirect_stdout(output):code=main(args)
            self.assertEqual(code,expected);result=json.loads(output.getvalue())
            self.assertEqual(result['status'],'error');self.assertIsNotNone(result['error_code']);self.assertIsInstance(result['warnings'],list)

    def test_env_only_and_resume_credential_does_not_override_identity(self):
        cfg=defaults();cfg['embedding'].update(provider='configured',endpoint='https://example.invalid/embeddings')
        with patch.dict('os.environ',{'EMBEDDING_API_KEY':'SECRET'}):self.assertEqual(credential(cfg),'SECRET')
        cfg['embedding']['model']='frozen-model'
        env=self.root/'credentials.env';env.write_text('EMBEDDING_API_KEY=NEW_SECRET\nEMBEDDING_API_URL=https://different.invalid\nEMBEDDING_MODEL=different\n', encoding='utf-8')
        self.assertEqual(credential(cfg,env),'NEW_SECRET');self.assertEqual(cfg['embedding']['model'],'frozen-model')
        resolved=resolve(overrides={'embedding_provider':'configured','embedding_model':'explicit'},env_file=env)
        self.assertEqual(resolved['embedding']['model'],'explicit')
        env.write_text('EMBEDDING_API_KEY=NEW_SECRET\nEMBEDDING_API_URL=https://example.invalid/v1/chat/completions\n', encoding='utf-8')
        resolved=resolve(overrides={'embedding_provider':'configured','embedding_model':'explicit'},env_file=env)
        self.assertEqual(resolved['embedding']['endpoint'],'https://example.invalid/v1/embeddings')

    def test_partial_report_and_null_quality_denominator(self):
        run=self.run_fixture();state=read(run/'run-state.json');state['run_state']='partial';write(run/'run-state.json',state)
        out,_=export_report(run,self.root/'report');self.assertTrue(read(out/'report.json')['partial'])
        labels=[]
        for c in self.cases:
            r=c['source'];labels.append({'comment_id':r['record_id'],'text_original':r['text_original'],'language':r['language'],
                'content_sha256':sha(r['text_original'].encode()),'cluster_id':r['record_id'],'split':'development',
                'reviewer_type':'agent_authored_synthetic','source_stage':'fixed_admission','points':[],'point_matches':[]})
        path=self.root/'labels.json';write(path,labels)
        out,_=evaluate_quality(run,path,self.root/'evaluation')
        metrics=read(out/'evaluation.json')['groups']['agent_authored_synthetic:development']['all']
        self.assertIsNone(metrics['mechanism_recall']['value'])
        labels[0]['text_original']='changed';write(path,labels)
        self.expect_failure(4,evaluate_quality,run,path,self.root/'bad')

    def test_actual_configured_resume_credentials_and_secret_redaction(self):
        cfg=copy.deepcopy(self.cfg)
        cfg['embedding'].update(provider='configured',model='frozen-remote',endpoint='https://embedding.invalid/v1/embeddings')
        transport=FixtureTransport(cfg)
        env=self.root/'secret.env'
        env.write_text('EMBEDDING_API_KEY=FIRST_SECRET_SENTINEL\n', encoding='utf-8')
        run=self.root/'run'
        with patch.dict('os.environ',{},clear=True):
            analyze(self.input,run,cfg,env_file=env,transport=transport,quiet=True)
        state=read(run/'run-state.json');state['run_state']='interrupted';write(run/'run-state.json',state)
        before=(run/'run-state.json').read_bytes()
        calls=len(transport.calls)
        with patch.dict('os.environ',{},clear=True):
            self.expect_failure(3,analyze,resume=run,transport=transport,quiet=True)
        self.assertEqual(before,(run/'run-state.json').read_bytes());self.assertEqual(calls,len(transport.calls))
        env.write_text('EMBEDDING_API_KEY=SECOND_SECRET_SENTINEL\nEMBEDDING_MODEL=wrong\nEMBEDDING_API_URL=https://wrong.invalid\n', encoding='utf-8')
        with patch.dict('os.environ',{},clear=True):
            _,_,warnings=analyze(resume=run,env_file=env,transport=transport,quiet=True)
        self.assertTrue(warnings)
        saved=read(run/'resolved-config.json')
        self.assertEqual(saved['embedding']['model'],'frozen-remote');self.assertEqual(saved['embedding']['endpoint'],cfg['embedding']['endpoint'])
        for p in run.rglob('*'):
            if p.is_file():
                self.assertNotIn(b'SECRET_SENTINEL',p.read_bytes())

    def test_ambiguity_is_not_a_technical_failure(self):
        original=self.transport.chat
        def chat(base,payload,partial):
            if 'decisions' in payload['format']['properties']:
                data=json.loads(payload['messages'][1]['content'])
                return {'done':True,'done_reason':'stop','message':{'content':json.dumps({'decisions':['uncertain']*len(data['comments'])})}}
            return original(base,payload,partial)
        self.transport.chat=chat
        run=self.run_fixture()
        self.assertEqual(status(run)['run_state'],'completed');self.assertFalse(status(run)['has_failures'])
        self.assertTrue(all(r['status']=='relevance_pending_or_failed' for r in read(run/'full-pipeline-coverage.json')))

    def test_resource_snapshot_and_code_identity_reject_before_writes(self):
        run=self.run_fixture();before=(run/'run-state.json').read_bytes()
        with patch('aimediator.run_store.code_manifest',return_value={'changed':True}):
            self.expect_failure(4,analyze,resume=run,transport=self.transport)
        snapshot=run/'resource-snapshot/configs/evidence-quality-policy.json'
        snapshot.write_text('{}', encoding='utf-8')
        self.expect_failure(4,analyze,resume=run,transport=self.transport)
        self.assertEqual(before,(run/'run-state.json').read_bytes())

    def test_enforce_cannot_be_downgraded_by_report_mode(self):
        run=self.run_fixture();report=read(run/'balance-report.json')
        report.update(evidence_quality_mode='off',report_schema_version='balance-evidence-v2');write(run/'balance-report.json',report)
        self.expect_failure(4,load_run,run)

    def test_completed_artifact_tampering_rejects_resume(self):
        run=self.run_fixture();write(run/'validated-claims.json',[])
        self.expect_failure(4,analyze,resume=run,transport=self.transport)

    def test_offline_demo_no_network_with_unrelated_environment(self):
        # Full three-mode demo is also exercised by the installed-wheel gate;
        # a bounded subset here tests the injected seam without network access.
        with patch('socket.socket.connect',side_effect=AssertionError('network')), patch.dict('os.environ',{'EMBEDDING_API_KEY':'UNRELATED_SECRET'}):
            self.run_fixture()

    def test_existing_script_and_package_use_same_prompt_bytes(self):
        from aimediator.operations import prompts_for
        for lang in ('en','zh'):
            self.assertEqual(prompts_for('off')['extract'][lang],asset_path('prompts/summarize-balance.'+lang+'.txt').read_text(encoding='utf-8'))

    def test_interrupted_audit_exports_complete_pending_proposals(self):
        original=self.transport.chat
        def chat(base,payload,partial):
            if 'support' in payload['format']['properties']:raise KeyboardInterrupt()
            return original(base,payload,partial)
        self.transport.chat=chat;run=self.root/'run'
        self.expect_failure(130,analyze,self.input,run,self.cfg,transport=self.transport,quiet=True)
        template,count=export_review(run,self.root/'template')
        self.assertGreater(count,0)
        proposals=read(template/'proposals.json')
        self.assertTrue(all(not e['automatic_accepted'] for e in proposals.values()))
        self.assertTrue(all(e['audit'] is None for e in proposals.values()))
        out,_=export_report(run,self.root/'report');self.assertTrue(read(out/'report.json')['partial'])

    def test_corrupt_resume_snapshot_is_incompatible_before_mutation(self):
        run=self.run_fixture();before=(run/'run-state.json').read_bytes()
        (run/'input-snapshot.jsonl').write_bytes(b'invalid JSON')
        self.expect_failure(4,analyze,resume=run,transport=self.transport)
        self.assertEqual(before,(run/'run-state.json').read_bytes())

    def test_individual_proposal_hash_mismatch_is_exit_four(self):
        run=self.run_fixture();path,decisions=self.review_decisions(run)
        next(iter(decisions['decisions'].values()))['proposal_sha256']='wrong'
        write(path,decisions)
        self.expect_failure(4,import_review,run,path,self.root/'bad')

    def test_legacy_failed_quality_cannot_supply_mechanism_eligibility(self):
        run=self.run_fixture();(run/'manifest.json').unlink()
        records=read(run/'evidence-quality.json');records[0]['status']='failed';records[0]['errors']=['failed']
        write(run/'evidence-quality.json',records)
        self.expect_failure(2,load_run,run)

    def test_saved_admission_requires_both_retrieval_and_model_agreement(self):
        run=self.run_fixture();records=read(run/'relevance.json');records[0]['model_related']=False;write(run/'relevance.json',records)
        self.expect_failure(2,load_run,run)

    def test_quality_labels_reject_foreign_point_segments(self):
        run=self.run_fixture();c=self.cases[0];r=c['source']
        labels=[{'comment_id':r['record_id'],'language':r['language'],'text_original':r['text_original'],
            'content_sha256':sha(r['text_original'].encode()),'cluster_id':r['record_id'],
            'split':'development','source_stage':'fixed_admission','reviewer_type':'agent_authored_synthetic',
            'segments':c['annotation']['segments'],
            'points':[{'point_id':'G1','route':'mechanism_evidence','segment_ids':['foreign']}], 'point_matches':[]}]
        path=self.root/'labels.json';write(path,labels)
        self.expect_failure(2,evaluate_quality,run,path,self.root/'evaluation')
        self.assertFalse((self.root/'evaluation').exists())


if __name__=='__main__':unittest.main()
