"""Live shadow/enforce diagnostic on explicitly selected frozen admissions.

No retrieval is rerun, no effectiveness score is inferred, no historical output
is modified. Uses the existing language models and original source snapshots.
"""
import argparse
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator import evidence_quality as q
from aimediator.common import sha as digest, write as write_json
from aimediator.diagnostics import audit, extract
from aimediator.evidence import character_reference, evidence_units
from aimediator.inference import api
from aimediator.pipeline import quality_request
from aimediator.resources import asset_path, module_path
from aimediator.run_store import code_manifest
from aimediator.runner import Runner

ASSETS = ('configs/balance-review-policy.json', 'configs/evidence-quality-policy.json',
          'configs/local-language-routing.json', 'data/glossary.json', 'prompts/evidence-quality.en.txt',
          'prompts/evidence-quality.zh.txt', 'prompts/quality-extract.en.txt', 'prompts/quality-extract.zh.txt',
          'prompts/quality-verify.en.txt', 'prompts/quality-verify.zh.txt', 'prompts/summarize-balance.en.txt',
          'prompts/summarize-balance.zh.txt', 'prompts/verify-balance.en.txt', 'prompts/verify-balance.zh.txt')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--admission-run',type=Path,required=True)
    p.add_argument('--comment-id',action='append',required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--base-url',default='http://127.0.0.1:11434')
    args=p.parse_args()
    folder=args.out.resolve()
    policy=q.load_policy()
    source_bytes=(args.admission_run/'source-snapshot.json').read_bytes()
    admission_bytes=(args.admission_run/'relevance.json').read_bytes()
    sources={r['record_id']:r for r in json.loads(source_bytes)}
    admitted={r['comment_id'] for r in json.loads(admission_bytes) if r['agreement']}
    if not set(args.comment_id)<=admitted or len(set(args.comment_id))!=len(args.comment_id):
        raise ValueError('Select unique comments from frozen affirmative admissions')
    rows=[sources[cid] for cid in args.comment_id]
    routing=json.loads(asset_path('configs/local-language-routing.json').read_text(encoding='utf-8'))['models']
    by_lang={v['language']:model for model,v in routing.items()}
    tags={r['name']:r['digest'] for r in api(args.base_url,'/api/tags')['models']}
    prompts={stage:{lang:asset_path(f'prompts/{name}.{lang}.txt').read_text(encoding='utf-8') for lang in ('en','zh')}
        for stage,name in [('quality','evidence-quality'),('extract','summarize-balance'),('verify','verify-balance')]}
    identity={'version':'fixed-admission-quality-live-v1',
        'source_sha256':digest(source_bytes),'admission_sha256':digest(admission_bytes),
        'comment_ids':args.comment_id,'policy':policy,
        'models':{by_lang[r['language']]:tags[by_lang[r['language']]] for r in rows},
        'script_sha256':digest(Path(__file__).read_bytes()),'package_code_sha256':code_manifest()['modules'],
        'asset_sha256':{name:digest(asset_path(name).read_bytes()) for name in ASSETS},
        'prompts':prompts,
        'enforce_prompts':{stage:{lang:asset_path(f'prompts/quality-{stage}.{lang}.txt').read_text(encoding='utf-8')
                                 for lang in ('en','zh')} for stage in ('extract','verify')}}
    folder.mkdir(parents=True,exist_ok=True)
    manifest=folder/'manifest.json'
    if manifest.exists() and json.loads(manifest.read_text(encoding='utf-8'))['identity']!=identity:
        raise ValueError('Diagnostic identity changed; use a new output directory')
    write_json(manifest,{'identity':identity,'scope':'Fixed historical admissions only; no fresh retrieval or human effectiveness validation.'})
    write_json(folder/'source-snapshot.json',rows)
    (folder/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    snapshot=folder/'code-snapshot'
    snapshot.mkdir(exist_ok=True)
    for name in identity['package_code_sha256']:
        (snapshot/name).write_bytes(module_path(name).read_bytes())
    runner=Runner(args.base_url,folder,prompts,identity,policy,log=lambda text:print(text,flush=True))
    quality_records=[]
    trace=[]
    comparison=[]
    for row in rows:
        cid=row['record_id']
        lang=row['language']
        model=by_lang[lang]
        units=evidence_units(row['text_original'])
        attempts=[]
        record=None
        for attempt in range(policy['max_attempts']):
            data,context=quality_request(runner,row,units,lang,policy,attempts)
            annotation,meta=runner.generate(model,lang,'quality',data,[cid],request_context=context)
            attempts.append(meta)
            trace.append({'stage':'quality','comment_id':cid,'attempt':attempt+1,**meta})
            if annotation is not None:
                record=q.qualify(annotation,row,units,policy)
                break
        record=record or q.failed_record(row,units,attempts,policy)
        record['attempts']=attempts
        quality_records.append(record)
        write_json(folder/'evidence-quality.json',quality_records)
        for mode in ('shadow','enforce'):
            allowed=q.allowed_points(record)
            if mode=='enforce' and not allowed:
                comparison.append({'comment_id':cid,'mode':mode,'claims':[], 'status':'quality_routed_without_extraction'})
                continue
            stage_prompts={k:dict(v) for k,v in prompts.items()}
            if mode=='enforce':
                for stage in ('extract','verify'):
                    stage_prompts[stage][lang]+='\n'+identity['enforce_prompts'][stage][lang]
            mode_runner=Runner(args.base_url,folder/mode,stage_prompts,{**identity,'mode':mode},policy,log=lambda text:print(text,flush=True))
            parsed,meta=extract(mode_runner,model,lang,row,allowed_points=allowed if mode=='enforce' else None)
            trace.append({'stage':'extract','mode':mode,'comment_id':cid,**meta})
            claims=[]
            for r in audit(mode_runner,model,lang,row,parsed['assessments'][0]['claims'] if parsed else [],
                           {e['canonical_name'] for e in character_reference()},quality_record=record if mode=='enforce' else None):
                entry={'claim_id':f"{cid}:{r['index']}",'comment_id':cid,'claim':r['enriched'] or r['claim'],'errors':r['errors']}
                if not r['errors']:
                    trace.append({'stage':'verify','mode':mode,'comment_id':cid,**r['audit_meta']})
                    entry['audit']=r['audit']
                claims.append(entry)
            comparison.append({'comment_id':cid,'mode':mode,'claims':claims,'status':'completed' if parsed else 'generation_failed'})
            write_json(folder/'mode-comparison.json',comparison)
            write_json(folder/'request-trace.json',trace)
    write_json(folder/'mode-comparison.json',comparison)
    write_json(folder/'request-trace.json',trace)
    write_json(folder/'diagnostic-summary.json',{
        'scope':'Live models on selected fixed historical admissions; not a full fresh RAG run.',
        'comments':len(rows),'quality_completed':sum(r['status']=='completed' for r in quality_records),
        'quality_failed':sum(r['status']=='failed' for r in quality_records),
        'routes':{r['comment_id']:r['routes_present'] for r in quality_records},
        'effectiveness_metrics':None,'independent_human_labels':False,
        'limitations':['No fresh embedding/relevance run.','No semantic accuracy estimate.','Model-proposed spans/points need human review.']})


if __name__=='__main__':
    main()
