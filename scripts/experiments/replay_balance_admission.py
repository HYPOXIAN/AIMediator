"""Validate frozen admission responses with current unchanged relevance prompts.

No fresh inference and no holdout retuning. This preserves inference provenance
when only extraction/audit code changes during a targeted iteration.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.balance_policy import retrieval_review_agrees
from aimediator.common import sha as digest, strict_json, write as write_json
from aimediator.resources import asset_path
from aimediator.run_store import code_manifest
from aimediator.runner import Runner

ASSETS = ('configs/balance-review-policy.json', 'prompts/relevance.en.txt', 'prompts/relevance.zh.txt',
          'prompts/retrieval-review.en.txt', 'prompts/retrieval-review.zh.txt')


def no_inference(*unused):
    raise RuntimeError('Replay cannot run inference')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--from-run',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    old=strict_json((args.from_run/'manifest.json').read_text(encoding='utf-8'))
    sources=strict_json((args.from_run/'source-snapshot.json').read_text(encoding='utf-8'))
    by_id={r['record_id']:r for r in sources}
    if digest(asset_path('configs/balance-review-policy.json').read_bytes())!=old['identity']['review_policy_sha256']:
        raise ValueError('Retrieval policy changed')
    prompts={s:{l:asset_path(f'prompts/{name}.{l}.txt').read_text(encoding='utf-8') for l in ('en','zh')} for s,name in [('relevance','relevance'),('retrieval_review','retrieval-review')]}
    for stage,langs in prompts.items():
        for language,t in langs.items():
            if digest(t.encode())!=old['identity']['prompts'][stage][language]:
                raise ValueError('Relevance prompt changed')
    original=strict_json((args.from_run/'relevance.json').read_text(encoding='utf-8'))
    decisions={r['comment_id']:{**r,'model_related':None,'model_uncertain':True,'agreement':False,'retrieval_review_related':None,'retrieval_review_uncertain':True} for r in original}
    trace=strict_json((args.from_run/'request-trace.json').read_text(encoding='utf-8'))
    runner=Runner('http://no-network.invalid',args.out,prompts,chat_transport=no_inference,log=lambda text:print(text,flush=True))
    verified=[]
    for entry in trace:
        stage='relevance' if entry['stage']=='relevance_refinement' else entry['stage']
        folder=args.from_run/'requests'/stage/entry['request_id']
        target=args.out/'requests'/stage/entry['request_id']
        shutil.copytree(folder,target,dirs_exist_ok=True)
        request=strict_json((folder/'request.json').read_text(encoding='utf-8'))
        data=strict_json(request['messages'][1]['content'])
        ids=[c['comment_id'] for c in data['comments']]
        language='en' if entry['model']=='llama3.1:latest' else 'zh'
        for item in data['comments']:
            if item['text']!=by_id[item['comment_id']]['text_original']:
                raise ValueError('Cached source differs')
        parsed,meta=runner.generate(entry['model'],language,stage,data,ids)
        if meta['request_id']!=entry['request_id'] or meta['errors'] or parsed is None:
            raise ValueError('Cached inference no longer validates')
        for item in parsed['decisions']:
            r=decisions[item['comment_id']]
            if stage=='retrieval_review':
                r.update(retrieval_review_related=item['related'],retrieval_review_uncertain=item['uncertain'])
            else:
                r.update(model_related=item['related'],model_uncertain=item['uncertain'])
        verified.append(entry['request_id'])
    for row in original:
        r=decisions[row['comment_id']]
        actual=retrieval_review_agrees(r,{'related':r['model_related'],'uncertain':r['model_uncertain']})
        if actual!=row['agreement']:
            raise ValueError('Replayed admission differs: '+row['comment_id'])
    output={'kind':'frozen_inference_replay_not_fresh_model_run','verified_requests':len(verified),'comments':len(original),'admitted':sum(r['agreement'] for r in original),'all_admission_decisions_unchanged':True,'fresh_inference_calls':0,
        'frozen_admission_manifest_sha256':digest((args.from_run/'manifest.json').read_bytes()),'package_code_sha256':code_manifest()['modules'],'asset_sha256':{name:digest(asset_path(name).read_bytes()) for name in ASSETS},'frozen_model_digests':old['identity']['models']}
    write_json(args.out/'replay-results.json',output)
    print(json.dumps(output,indent=2))


if __name__=='__main__':
    main()
