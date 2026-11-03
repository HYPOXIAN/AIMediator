"""Live shadow/enforce diagnostic on explicitly selected frozen admissions.

No retrieval is rerun, no effectiveness score is inferred, no historical output
is modified. Uses the existing language models and original source snapshots.
"""
import argparse
import json
from pathlib import Path

import sys
sys.path.insert(1, str(Path(__file__).resolve().parents[1]))  # scripts/ holds the registered forwarding shells
import evidence_quality as q
import run_balance_analysis as m


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--admission-run',type=Path,required=True)
    p.add_argument('--comment-id',action='append',required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--base-url',default='http://127.0.0.1:11434')
    args=p.parse_args();folder=args.out.resolve();policy=q.load_policy()
    source_bytes=(args.admission_run/'source-snapshot.json').read_bytes()
    admission_bytes=(args.admission_run/'relevance.json').read_bytes()
    sources={r['record_id']:r for r in json.loads(source_bytes)}
    admitted={r['comment_id'] for r in json.loads(admission_bytes) if r['agreement']}
    if not set(args.comment_id)<=admitted or len(set(args.comment_id))!=len(args.comment_id):
        raise ValueError('Select unique comments from frozen affirmative admissions')
    rows=[sources[cid] for cid in args.comment_id]
    routing=json.loads((m.ROOT/'configs/local-language-routing.json').read_text())['models']
    by_lang={v['language']:model for model,v in routing.items()}
    tags={r['name']:r['digest'] for r in m.api(args.base_url,'/api/tags')['models']}
    prompts={stage:{lang:(m.ROOT/f'prompts/{name}.{lang}.txt').read_text() for lang in ('en','zh')}
        for stage,name in [('quality','evidence-quality'),('extract','summarize-balance'),('verify','verify-balance')]}
    code_paths=['scripts/evidence_quality.py','scripts/run_balance_analysis.py',
                'scripts/balance_policy.py','scripts/experiments/diagnose_evidence_quality_live.py']
    identity={'version':'fixed-admission-quality-live-v1',
        'source_sha256':m.digest(source_bytes),'admission_sha256':m.digest(admission_bytes),
        'comment_ids':args.comment_id,'policy':policy,
        'models':{by_lang[r['language']]:tags[by_lang[r['language']]] for r in rows},
        'code_sha256':{name:m.digest((m.ROOT/name).read_bytes()) for name in code_paths},
        'prompts':prompts,
        'enforce_prompts':{stage:{lang:(m.ROOT/f'prompts/quality-{stage}.{lang}.txt').read_text()
                                 for lang in ('en','zh')} for stage in ('extract','verify')}}
    folder.mkdir(parents=True,exist_ok=True)
    manifest=folder/'manifest.json'
    if manifest.exists() and json.loads(manifest.read_text())['identity']!=identity:
        raise ValueError('Diagnostic identity changed; use a new output directory')
    m.write_json(manifest,{'identity':identity,'scope':'Fixed historical admissions only; no fresh retrieval or human effectiveness validation.'})
    m.write_json(folder/'source-snapshot.json',rows)
    for name in code_paths:(folder/Path(name).name).write_bytes((m.ROOT/name).read_bytes())
    runner=m.Runner(args.base_url,folder,prompts,identity,policy)
    quality_records=[];trace=[];comparison=[]
    for row in rows:
        cid=row['record_id'];lang=row['language'];model=by_lang[lang];units=m.evidence_units(row['text_original']);attempts=[];record=None
        for attempt in range(policy['max_attempts']):
            data={'source':row,'comments':[{'comment_id':cid,'units':units}],
                'language':lang,'character_normalization_reference':m.character_reference(row['text_original']),
                'quality_contract':policy,'attempt':attempt+1}
            annotation,meta=runner.generate(model,lang,'quality',data,[cid]);attempts.append(meta)
            trace.append({'stage':'quality','comment_id':cid,'attempt':attempt+1,**meta})
            if annotation is not None:
                record=q.qualify(annotation,row,units,policy);break
        record=record or q.failed_record(row,units,attempts,policy);record['attempts']=attempts
        quality_records.append(record)
        m.write_json(folder/'evidence-quality.json',quality_records)
        for mode in ('shadow','enforce'):
            allowed=q.allowed_points(record)
            if mode=='enforce' and not allowed:
                comparison.append({'comment_id':cid,'mode':mode,'claims':[], 'status':'quality_routed_without_extraction'})
                continue
            stage_prompts={k:dict(v) for k,v in prompts.items()}
            if mode=='enforce':
                for stage in ('extract','verify'):
                    stage_prompts[stage][lang]+='\n'+identity['enforce_prompts'][stage][lang]
            mode_runner=m.Runner(args.base_url,folder/mode,stage_prompts,{**identity,'mode':mode},policy)
            data={'comments':[{'comment_id':cid,'units':units}],
                  'character_normalization_reference':m.character_reference(row['text_original'])}
            if mode=='enforce':data['comments'][0]['allowed_quality_points']=allowed
            parsed,meta=mode_runner.generate(model,lang,'extract',data,[cid])
            trace.append({'stage':'extract','mode':mode,'comment_id':cid,**meta});claims=[]
            for i,claim in enumerate(parsed['assessments'][0]['claims'] if parsed else []):
                errors,enriched=m.ground_claim(claim,row,{e['canonical_name'] for e in m.character_reference()})
                if mode=='enforce':
                    errs,qualification=q.bind_claim(claim,record,m.character_reference(row['text_original']));errors+=errs
                    if enriched:enriched['evidence_quality']=qualification
                entry={'claim_id':f'{cid}:{i+1}','comment_id':cid,'claim':enriched or claim,'errors':errors}
                if not errors:
                    audited,meta=mode_runner.generate(model,lang,'verify',{'claims':[entry],'original_comment':row['text_original']},[entry['claim_id']])
                    trace.append({'stage':'verify','mode':mode,'comment_id':cid,**meta})
                    entry['audit']=audited['verdicts'][0] if audited else None
                claims.append(entry)
            comparison.append({'comment_id':cid,'mode':mode,'claims':claims,'status':'completed' if parsed else 'generation_failed'})
            m.write_json(folder/'mode-comparison.json',comparison)
            m.write_json(folder/'request-trace.json',trace)
    m.write_json(folder/'mode-comparison.json',comparison)
    m.write_json(folder/'request-trace.json',trace)
    m.write_json(folder/'diagnostic-summary.json',{
        'scope':'Live models on selected fixed historical admissions; not a full fresh RAG run.',
        'comments':len(rows),'quality_completed':sum(r['status']=='completed' for r in quality_records),
        'quality_failed':sum(r['status']=='failed' for r in quality_records),
        'routes':{r['comment_id']:r['routes_present'] for r in quality_records},
        'effectiveness_metrics':None,'independent_human_labels':False,
        'limitations':['No fresh embedding/relevance run.','No semantic accuracy estimate.','Model-proposed spans/points need human review.']})


if __name__=='__main__':main()
