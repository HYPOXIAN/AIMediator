"""Deterministic contracts and mocked end-to-end runs, never semantic accuracy."""
import argparse
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import engine, evidence, evidence_quality as q, pipeline
from aimediator.design_briefs import prepare_briefs
from aimediator.legacy_review import apply_review, proposal_hash
from support import CASES, case, qualified


def numeric_claim():
    return {'character': 'Ryu', 'target': 'Hadoken damage', 'direction': 'nerf',
        'recommendation': 'Reduce Hadoken damage from 600 to 500.', 'specificity': 'source_numeric',
        'parameters': [{'metric': 'damage', 'current': '600', 'proposed': '500', 'delta': None,
                        'unit': None, 'evidence_id': 'E1'}],
        'evidence_ids': ['E1'], 'uncertain': False}


def basic_claim(character='Ken', target=None, direction='nerf'):
    return {'character': character, 'target': target, 'direction': direction,
        'recommendation': 'Nerf ' + character + '.', 'specificity': 'qualitative_only',
        'parameters': [], 'evidence_ids': ['E1'], 'uncertain': False}


class QualityLogicTests(unittest.TestCase):
    def test_bilingual_authored_contracts(self):
        for c in CASES:
            with self.subTest(c=c['case_id']):
                record = qualified(c)
                self.assertEqual(record['errors'], [])
                self.assertEqual(record['routes_present'], sorted(c['expected_routes']))
                for item in record['routing']:
                    self.assertEqual(item['comment_id'], c['source']['record_id'])

    def test_unicode_weights_and_offsets(self):
        text = ' 😤e\u0301中1.5 2MK!\r\n'
        self.assertEqual(q.weight(text), 9)
        row = {'record_id': 'unicode', 'text_original': text}
        units = evidence.evidence_units(text)
        annotation = {'comment_id': 'unicode', 'information_points': [], 'segments': [
            {'segment_id': 'S' + str(i), 'evidence_id': u['evidence_id'], 'start': u['start'],
             'end': u['end'], 'quote': u['text'], 'scope': 'unrelated', 'content_kind': 'pure_emotion',
             'emotional_tone': True, 'reason_code': 'empty_venting'} for i, u in enumerate(units)]}
        result = q.qualify(annotation, row, units)
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['emotion_ratio'], 1)
        self.assertIn('1.5', units[0]['text'])
        for unit in units:
            self.assertEqual(text[unit['start']:unit['end']], unit['text'])

    def test_empty_and_punctuation_measurement(self):
        for text in ('', ' \r\n', '!!!。'):
            row = {'record_id': 'empty', 'text_original': text}
            units = evidence.evidence_units(text)
            ann = {'comment_id': 'empty', 'information_points': [], 'segments': [
                dict(segment_id=f'S{i}', evidence_id=u['evidence_id'], start=u['start'], end=u['end'],
                     quote=u['text'], scope='unrelated', content_kind='other', emotional_tone=False,
                     reason_code='unrelated_topic') for i,u in enumerate(units)]}
            result = q.qualify(ann,row,units)
            self.assertIsNone(result['emotion_ratio'])
            self.assertTrue(result['empty_measurement'])
            self.assertEqual(result['routes_present'], ['exclude'])

    def test_bad_spans_ids_references_and_unknown_fields_fail_closed(self):
        mutations = [lambda a: a.update(comment_id='foreign'),
            lambda a: a['segments'][0].update(evidence_id='E999'),
            lambda a: a['segments'][0].update(start=-1),
            lambda a: a['segments'][0].update(start=True),
            lambda a: a['segments'][0].update(end=100000),
            lambda a: a['segments'][0].update(quote='forged'),
            lambda a: a['segments'][0].update(start=1,quote=a['segments'][0]['quote'][1:]),
            lambda a: a['segments'].append(copy.deepcopy(a['segments'][0])),
            lambda a: a['information_points'].append(copy.deepcopy(a['information_points'][0])),
            lambda a: a['information_points'][0].update(segment_ids=['foreign:S1']),
            lambda a: a['information_points'][0].update(segment_ids=['S1','S1']),
            lambda a: a['segments'][0].update(content_kind='made_up'),
            lambda a: a.update(emotion_ratio=.5),
            lambda a: a['information_points'][0].update(mechanic_literal='invented')]
        for mutate in mutations:
            c = case('numeric_request');mutate(c['annotation'])
            with self.subTest(mutate=mutate):
                record=qualified(c)
                self.assertEqual(record['status'],'failed')
                self.assertEqual(record['routes_present'],['review'])

    def test_out_of_order_nonoverlap_and_missing_points_are_reviewed(self):
        c=case('opposing_mechanics');c['annotation']['segments'].reverse()
        self.assertEqual(qualified(c)['status'],'failed')
        c=case('general');c['annotation']['information_points']=[]
        self.assertEqual(qualified(c)['routes_present'],['review'])

    def test_scope_detail_conflicts_and_emotion_cannot_support_concrete(self):
        for kind,scope in [('pure_emotion','character_balance'),('other','character_balance'),
                           ('concrete_feedback','unrelated'),('general_opinion','character_balance')]:
            c=case('numeric_request');c['annotation']['segments'][0].update(content_kind=kind,scope=scope)
            self.assertEqual(qualified(c)['status'],'failed')

    def test_quoted_emotion_and_sarcasm_do_not_become_authors_stance(self):
        for category in ('quoted_voice','sarcasm','me_too'):
            self.assertEqual(qualified(case(category))['routes_present'],['review'])
        c=case('venting');c['annotation']['segments'][0]['reason_code']='quoted_emotion'
        self.assertEqual(qualified(c)['routes_present'],['review'])

    def test_high_emotion_and_neutral_have_same_qualification_and_weight(self):
        for language in ('zh','en'):
            records=[qualified(case(cat,language)) for cat in ('hostile_concrete','neutral_equivalent','high_emotion')]
            self.assertTrue(records[-1]['high_emotion_warning'])
            self.assertTrue(all(len(q.allowed_points(r))==1 for r in records))
            claims=[{'character':'Ken','target':'Shoryuken','direction':'unclear','comment_id':r['comment_id'], 'evidence_quality':{'mode':'enforce','route':'mechanism_evidence'}, 'semantic_audit':{'supported':True}} for r in records]
            self.assertEqual(pipeline.aggregate(claims,True)[0]['supporting_comment_count'],3)
            self.assertEqual(pipeline.aggregate(claims+claims,True)[0]['supporting_comment_count'],3)

    def test_opinions_keep_stance_negation_and_unverified_identity_isolated(self):
        records=[qualified(case('negation')),qualified(case('general'))]
        out=q.summarize_opinions(records+records,evidence.character_reference('Ken'))
        self.assertEqual({g['direction'] for g in out['groups']},{'keep','nerf'})
        self.assertTrue(all(g['supporting_comment_count']==1 for g in out['groups']))
        c=case('unknown_identity');p=c['annotation']['information_points'][0]
        p['detail_level']='general';c['annotation']['segments'][0]['content_kind']='general_opinion'
        out=q.summarize_opinions([qualified(c)],evidence.character_reference(c['source']['text_original']))
        self.assertEqual(out['groups'],[]);self.assertEqual(len(out['unresolved_identity_opinions']),1)

    def test_claim_requires_own_eligible_point_and_local_numbers(self):
        c=case('numeric_request');r=qualified(c);claim=numeric_claim();claim['quality_point_ids']=['P1']
        errors,qualification=q.bind_claim(claim,r,evidence.character_reference(c['source']['text_original']))
        self.assertEqual(errors,[]);self.assertEqual(qualification['route'],'mechanism_evidence')
        for field,value in [('quality_point_ids',[]),('quality_point_ids',['foreign:P1']),
                            ('character','Ken'),('direction','buff'),('target','Shoryuken'),
                            ('recommendation','Nerf Ryu damage to 100.')]:
            bad=copy.deepcopy(claim);bad[field]=value
            self.assertTrue(q.bind_claim(bad,r,evidence.character_reference(c['source']['text_original']))[0])
        bad=copy.deepcopy(claim);bad['parameters'][0]['metric']='damage at 999 health'
        self.assertTrue(q.bind_claim(bad,r,evidence.character_reference(c['source']['text_original']))[0])
        for category in ('general','system_and_cosmetic','venting'):
            self.assertTrue(q.bind_claim(claim,qualified(case(category)),evidence.character_reference('Ryu'))[0])

    def test_same_evidence_unit_cannot_lend_general_numeric_request(self):
        text='Ryu Hadoken is strong; please nerf Ken damage from 600 to 500.'
        row={'record_id':'mixed','text_original':text};u=evidence.evidence_units(text)[0];cut=text.index(';')+1
        a=case('numeric_request')['annotation'];a['comment_id']='mixed'
        a['segments']=[{**a['segments'][0],'quote':text[:cut],'end':cut},
            {**a['segments'][0],'segment_id':'S2','start':cut,'end':len(text),'quote':text[cut:],
             'content_kind':'general_opinion'}]
        a['information_points']=[{**a['information_points'][0],'character_literal':'Ryu','stance':'strength_assessment'},
            {**a['information_points'][0],'point_id':'P2','segment_ids':['S2'],'detail_level':'general',
             'character_literal':'Ken','mechanic_literal':None}]
        r=q.qualify(a,row,[u]);self.assertEqual(r['errors'],[])
        claim=numeric_claim();claim['quality_point_ids']=['P1']
        self.assertTrue(q.bind_claim(claim,r,evidence.character_reference(text))[0])

    def test_numeric_observations_and_history_cannot_become_requests(self):
        for category in ('damage_comparison','past_patch'):
            c=case(category);claim=numeric_claim();claim['quality_point_ids']=['P1']
            self.assertTrue(q.bind_claim(claim,qualified(c),evidence.character_reference(c['source']['text_original']))[0])

    def test_unresolved_part_does_not_block_independent_point(self):
        c=case('opposing_mechanics');c['annotation']['information_points'][1]['stance']='uncertain'
        r=qualified(c);self.assertEqual(r['routes_present'],['mechanism_evidence','review'])
        self.assertEqual(len(q.allowed_points(r)),1)

    def test_schema_integer_bounds_are_real_checks(self):
        for value in (True,1.5,-1,'1'):
            self.assertTrue(q.schema_errors(value,{'type':'integer','minimum':0}))
        self.assertEqual(q.schema_errors(1,{'type':'integer','minimum':0}),[])

    def test_design_accept_cannot_upgrade_general_or_missing_quality(self):
        c={**numeric_claim(),'claim_id':'a:1','comment_id':'a','source_review':{'decision':'accept'}}
        old=prepare_briefs([c])['briefs'][0]
        self.assertEqual(old['quality_assessment'],'legacy/quality_not_assessed')
        new=prepare_briefs([c],quality_mode='enforce')['briefs'][0]
        self.assertIn('mechanism_evidence_qualification_required',new['blockers'])
        c['evidence_quality']={'mode':'enforce','route':'opinion_only'}
        self.assertIn('mechanism_evidence_qualification_required',prepare_briefs([c])['briefs'][0]['blockers'])

    def test_source_review_preserves_quality_and_fingerprint(self):
        c=case('numeric_request');source=c['source'];claim=numeric_claim();claim['quality_point_ids']=['P1']
        _,enriched=evidence.ground_claim(claim,source,{'Ryu'})
        _,qualification=q.bind_claim(claim,qualified(c),evidence.character_reference(source['text_original']))
        enriched['evidence_quality']=qualification;enriched['semantic_audit']={'supported':True}
        original_hash=proposal_hash(enriched)
        changed=copy.deepcopy(enriched);changed['quality_point_ids']=['P999']
        self.assertNotEqual(proposal_hash(changed),original_hash)
        proposals={'a:1':{'comment_id':source['record_id'],'model':'fixture','claim':enriched}}
        decisions={'a:1':{'decision':'accept','reason':'fixture','proposal_sha256':original_hash}}
        accepted,_=apply_review(proposals,decisions,{source['record_id']:source},{source['record_id']},{'Ryu'})
        self.assertEqual(accepted[0]['evidence_quality'],qualification)
        self.assertEqual(accepted[0]['semantic_audit'],{'supported':True})
        decisions['a:1']['target']='Shoryuken'
        with self.assertRaisesRegex(ValueError,'quality'):
            apply_review(proposals,decisions,{source['record_id']:source},{source['record_id']},{'Ryu'})

    def test_qualified_design_retains_version_and_source_gates(self):
        c=case('numeric_request');source=c['source'];claim=numeric_claim();claim['quality_point_ids']=['P1']
        _,enriched=evidence.ground_claim(claim,source,{'Ryu'})
        _,qualification=q.bind_claim(claim,qualified(c),evidence.character_reference(source['text_original']))
        enriched.update(evidence_quality=qualification,semantic_audit={'supported':True},
                        comment_id=source['record_id'],claim_id='fixture:1',source_review={'decision':'accept'})
        moves=[{'character':'Ryu','target':'Hadoken damage','patch_version':'synthetic-patch',
                'metric':'damage','current':'600','unit':'points','source_url':'https://example.test','verified':True}]
        self.assertEqual(prepare_briefs([enriched],moves,'synthetic-patch')['summary']['ready'],1)
        for field in ('evidence_quality','semantic_audit','character_identity','source_review'):
            bad=copy.deepcopy(enriched);bad.pop(field)
            self.assertEqual(prepare_briefs([bad],moves,'synthetic-patch',quality_mode='enforce')['summary']['blocked'],1)
        self.assertEqual(prepare_briefs([enriched],moves,'other-patch')['summary']['blocked'],1)

    def test_comment_union_counts_overlap_and_stance_counts_do_not_add_weight(self):
        c=case('general');p=copy.deepcopy(c['annotation']['information_points'][0]);p['point_id']='P2';p['stance']='strength_assessment'
        c['annotation']['information_points'].append(p)
        record=qualified(c);opinion=q.summarize_opinions([record],evidence.character_reference('Ken'))
        self.assertEqual(len(opinion['groups']),1)
        group=opinion['groups'][0];self.assertEqual(group['supporting_comment_count'],1)
        self.assertEqual(group['stance_comment_counts'],{'explicit_request':1,'strength_assessment':1})
        counts=pipeline.quality_source_counts([record],[{'comment_id':record['comment_id'],'evidence_quality':{'mode':'enforce'}}])
        self.assertEqual(counts['union_count'],1);self.assertEqual(counts['overlap_comment_ids'],[record['comment_id']])


class MockPipelineTests(unittest.TestCase):
    def setUp(self):
        self.cases=[case(cat) for cat in ('venting','general','system_and_cosmetic','numeric_request','high_emotion')]
        self.rows=[c['source'] for c in self.cases]
        self.rows += [{'record_id':'reject','text_original':'nice music','language':'en'},
                      {'record_id':'unsupported','text_original':'bonjour','language':'fr'},
                      {'record_id':'unselected','text_original':'肯太强','language':'zh'}]
        self.annotations={c['source']['record_id']:c['annotation'] for c in self.cases}
        self.calls=[];self.fail_quality=None;self.inject_bad_claim=False

    def transport(self,base,payload,path):
        data=json.loads(payload['messages'][1]['content']);props=payload['format']['properties']
        stage='quality' if 'segments' in props else 'extract' if 'assessments' in props else 'verify' if 'support' in props else 'relevance'
        self.calls.append((stage,data,payload))
        if stage=='quality':
            if self.fail_quality:
                outcome=self.fail_quality(data)
                if isinstance(outcome,Exception):raise outcome
                if outcome:return outcome
            result=copy.deepcopy(self.annotations[data['comments'][0]['comment_id']])
        elif stage=='relevance':result={'decisions':['related']*len(data['comments'])}
        elif stage=='verify':result={'support':'supported'}
        else:
            assessments={}
            for row in data['comments']:
                cid=row['comment_id'];claims=[]
                if 'numeric_request' in cid:
                    claims=[numeric_claim()]
                    if cid.endswith(':zh'):
                        claims[0].update(target='波动拳伤害',recommendation='将波动拳伤害从600降低到500。')
                if 'general' in cid:claims=[basic_claim()]
                if 'high_emotion' in cid:
                    eid=next(u['evidence_id'] for u in row['units'] if 'Ken' in u['text'])
                    c=basic_claim(target='Shoryuken',direction='unclear');c['evidence_ids']=[eid];c['recommendation']="Ken's Shoryuken keeps pressure on block."
                    claims=[c]
                if 'allowed_quality_points' in row:
                    for c in claims:c['quality_point_ids']=[row['allowed_quality_points'][0]['point_id']]
                    if self.inject_bad_claim and 'numeric_request' in cid:
                        claims.append({**basic_claim('Ryu',direction='buff'),'quality_point_ids':['P1']})
                assessments[cid]={'subjects':list(dict.fromkeys(c['character'] for c in claims)),'claims':claims}
            result={'assessments':assessments}
        return {'done':True,'done_reason':'stop','message':{'content':json.dumps(result)}}

    def run_mock(self,folder,mode='enforce',quality_only=False,model='llama3.1:latest'):
        dataset=folder.parent/'dataset.jsonl';dataset.write_text(''.join(json.dumps(r)+'\n' for r in self.rows), encoding='utf-8')
        args=argparse.Namespace(out=folder,dataset=dataset,model=model,
            base_url='http://local.test',embedding_model='qwen3-embedding:8b',evidence_quality=mode,
            quality_only=quality_only,relevance_only=False)
        tags={'models':[{'name':name,'digest':'fixture:'+name} for name in ('llama3.1:latest','qwen2.5:7b','qwen3-embedding:8b')]}
        def retrieval(rows,*unused):
            return [{'comment_id':r['record_id'],'language':r['language'],'retrieval_related':r['record_id']!='reject',
                     'positive_score':.1 if r['record_id']=='reject' else .9,
                     'negative_score':.9 if r['record_id']=='reject' else .1,'references':[]} for r in rows]
        with patch('sys.stdout',new=io.StringIO()):
            engine.run(args,api_transport=Mock(return_value=tags),chat_transport=self.transport,retrieval_service=retrieval)
        return json.loads((folder/'balance-report.json').read_text(encoding='utf-8'))

    def test_legacy_run_snapshots_every_package_module(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)/'off';self.run_mock(folder,'off')
            package=Path(engine.__file__).parent;modules=sorted(p.name for p in package.glob('*.py'))
            self.assertIn('engine.py',modules)
            self.assertEqual(sorted(p.name for p in (folder/'code-snapshot').iterdir()),modules)
            for name in modules:self.assertEqual((folder/'code-snapshot'/name).read_bytes(),(package/name).read_bytes())

    def test_off_shadow_downstream_identical_enforce_routes_and_resume(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            off=self.run_mock(folder/'off','off');self.assertFalse(any(c[0]=='quality' for c in self.calls))
            shadow=self.run_mock(folder/'shadow','shadow')
            self.assertEqual(off['character_adjustments'],shadow['character_adjustments'])
            self.assertEqual(off['summary'],shadow['summary'])
            enforce=self.run_mock(folder/'enforce')
            self.assertTrue(enforce['opinion_summary']['groups']);self.assertTrue(enforce['system_feedback'])
            accepted=json.loads((folder/'enforce/validated-claims.json').read_text(encoding='utf-8'))
            self.assertEqual(len(accepted),2)
            self.assertTrue(all(c['evidence_quality']['route']=='mechanism_evidence' for c in accepted))
            self.assertTrue(any(g['direction']=='unclear' for g in enforce['character_adjustments']))
            before=len(self.calls);again=self.run_mock(folder/'enforce')
            self.assertEqual(enforce,again);self.assertEqual(len(self.calls),before)
            coverage=again['full_pipeline_coverage'];self.assertEqual(len(coverage),len(self.rows))
            self.assertEqual(len({r['comment_id'] for r in coverage}),len(self.rows))
            statuses={r['comment_id']:r['status'] for r in coverage}
            self.assertEqual(statuses['unsupported'],'unsupported_language')
            self.assertEqual(statuses['unselected'],'unselected_language')
            self.assertEqual(statuses['reject'],'relevance_rejected')
            self.assertEqual(statuses['synthetic:general:en'],'quality_routed_without_extraction')
            self.assertEqual(again['summary']['final_generation_failed_comments'],0)
            verify=[data for stage,data,_ in self.calls if stage=='verify' and 'selected_source_segments' in data]
            self.assertEqual(len(verify),2)
            self.assertNotIn('evidence_quality',verify[0]['proposed_claim'])

    def test_chinese_pipeline_uses_chinese_prompt_and_preserves_routes(self):
        self.cases=[case(cat,'zh') for cat in ('numeric_request','price_and_opinion','system_and_cosmetic')]
        self.rows=[c['source'] for c in self.cases]
        self.annotations={c['source']['record_id']:c['annotation'] for c in self.cases}
        with tempfile.TemporaryDirectory() as temp:
            report=self.run_mock(Path(temp)/'run',model='qwen2.5:7b')
            self.assertEqual(report['summary']['accepted_claims'],1)
            self.assertEqual(len(report['opinion_summary']['groups']),1)
            self.assertEqual(len(report['system_feedback']),1)
            self.assertTrue(all(payload['model']=='qwen2.5:7b' for _,_,payload in self.calls))
            quality_payload=next(payload for stage,_,payload in self.calls if stage=='quality')
            self.assertIn('只标注一条',quality_payload['messages'][0]['content'])

    def test_quality_only_stops_before_generation(self):
        with tempfile.TemporaryDirectory() as temp:
            report=self.run_mock(Path(temp)/'run',quality_only=True)
            self.assertEqual(report['character_adjustments'],[])
            self.assertFalse(any(stage in ('extract','verify') for stage,_,_ in self.calls))
            self.assertEqual(report['summary']['mode'],'quality_only')

    def test_retry_is_fresh_once_and_failure_durable_review(self):
        def fail(data):
            if 'numeric_request' not in data['comments'][0]['comment_id']:return None
            return TimeoutError('fixture timeout')
        self.fail_quality=fail
        with tempfile.TemporaryDirectory() as temp:
            run=Path(temp)/'run';report=self.run_mock(run)
            records=json.loads((run/'evidence-quality.json').read_text(encoding='utf-8'))
            failed=next(r for r in records if 'numeric_request' in r['comment_id'])
            self.assertEqual(failed['status'],'failed');self.assertEqual(failed['routes_present'],['review'])
            self.assertEqual(len(failed['attempts']),2)
            self.assertNotEqual(failed['attempts'][0]['request_id'],failed['attempts'][1]['request_id'])
            self.assertEqual(report['summary']['final_generation_failed_comments'],0)
            before=len(self.calls);again=self.run_mock(run)
            self.assertEqual(len(self.calls),before);self.assertEqual(report,again)

    def test_malformed_truncated_and_structural_failures_retry_then_review(self):
        for mode in ('json','truncated','quote'):
            self.calls=[]
            def fail(data):
                if 'numeric_request' not in data['comments'][0]['comment_id']:return None
                raw='not json'
                if mode=='quote':
                    ann=copy.deepcopy(self.annotations[data['comments'][0]['comment_id']]);ann['segments'][0]['quote']='forged';raw=json.dumps(ann)
                if mode=='truncated':raw=json.dumps(self.annotations[data['comments'][0]['comment_id']])
                return {'done':True,'done_reason':'length' if mode=='truncated' else 'stop','message':{'content':raw}}
            self.fail_quality=fail
            with tempfile.TemporaryDirectory() as temp:
                self.run_mock(Path(temp)/'run',quality_only=True)
                records=json.loads((Path(temp)/'run/evidence-quality.json').read_text(encoding='utf-8'))
                r=next(r for r in records if 'numeric_request' in r['comment_id'])
                self.assertEqual(r['status'],'failed');self.assertEqual(len(r['attempts']),2)

    def test_one_failed_attempt_then_valid_new_request(self):
        self.fail_quality=lambda data: {'done':True,'done_reason':'stop','message':{'content':'{}'}} if 'previous_attempt_errors' not in data else None
        with tempfile.TemporaryDirectory() as temp:
            self.run_mock(Path(temp)/'run',quality_only=True)
            records=json.loads((Path(temp)/'run/evidence-quality.json').read_text(encoding='utf-8'))
            self.assertTrue(all(r['status']=='completed' and len(r['attempts'])==2 for r in records))
            self.assertTrue(all(r['attempts'][0]['errors'] and not r['attempts'][1]['errors'] for r in records))

    def test_enforce_blocks_model_borrowing_even_if_audit_would_accept(self):
        self.inject_bad_claim=True
        with tempfile.TemporaryDirectory() as temp:
            self.run_mock(Path(temp)/'run')
            quarantine=json.loads((Path(temp)/'run/quarantined-claims.json').read_text(encoding='utf-8'))
            self.assertTrue(any(any('selected point' in e for e in c['errors']) for c in quarantine))
            self.assertEqual(len(json.loads((Path(temp)/'run/validated-claims.json').read_text(encoding='utf-8'))),2)

    def test_policy_changes_forbid_directory_resume(self):
        with tempfile.TemporaryDirectory() as temp:
            run=Path(temp)/'run';self.run_mock(run,quality_only=True)
            policy=q.load_policy();policy['high_emotion_threshold']=.75
            with patch.object(q,'load_policy',return_value=policy):
                with self.assertRaisesRegex(ValueError,'new output directory'):self.run_mock(run,quality_only=True)

    def test_mode_argument_validation(self):
        for mode,quality_only,relevance_only in [('off',True,False),('shadow',False,True),('enforce',True,True)]:
            with self.assertRaises(ValueError):pipeline.validate_modes(argparse.Namespace(evidence_quality=mode,quality_only=quality_only,relevance_only=relevance_only))
        self.assertEqual(pipeline.validate_modes(argparse.Namespace()),'off')


if __name__=='__main__':unittest.main()
