"""End-to-end positive numeric extraction controls; never real community evidence."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.common import sha as digest, strict_json, write as write_json
from aimediator.diagnostics import audit, extract
from aimediator.inference import api
from aimediator.resources import asset_path
from aimediator.run_store import code_manifest
from aimediator.runner import Runner

ASSETS = ('configs/balance-review-policy.json', 'data/glossary.json', 'prompts/summarize-balance.en.txt',
          'prompts/summarize-balance.zh.txt', 'prompts/verify-balance.en.txt', 'prompts/verify-balance.zh.txt')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--base-url',default='http://127.0.0.1:11434');p.add_argument('--num-gpu',type=int);args=p.parse_args()
    prompts={stage:{lang:asset_path(f'prompts/{name}.{lang}.txt').read_text(encoding='utf-8') for lang in ('en','zh')}
        for stage,name in [('extract','summarize-balance'),('verify','verify-balance')]}
    tags=api(args.base_url,'/api/tags')['models'];installed={r['name']:r['digest'] for r in tags}
    identity={'script_sha256':digest(Path(__file__).read_bytes()),'package_code_sha256':code_manifest()['modules'],
        'asset_sha256':{name:digest(asset_path(name).read_bytes()) for name in ASSETS},
        'models':{m:installed[m] for m in ('llama3.1:latest','qwen2.5:7b')},
        'prompts':{s:{l:digest(t.encode()) for l,t in langs.items()} for s,langs in prompts.items()},
        'runtime_options':{'num_gpu':args.num_gpu} if args.num_gpu is not None else {}}
    path=args.out/'manifest.json'
    if path.exists() and strict_json(path.read_text(encoding='utf-8'))!=identity:raise ValueError('Control identity changed; use a new output directory')
    write_json(path,identity);runner=Runner(args.base_url,args.out,prompts,log=lambda text:print(text,flush=True));runner.runtime_options=identity['runtime_options'];results=[]
    for language,model,text in [('en','llama3.1:latest',"Please reduce Ryu's Hadoken damage from 600 to 500."),('zh','qwen2.5:7b','请将隆的波动拳伤害从600降到500。')]:
        record_id='synthetic-extraction-'+language;row={'record_id':record_id,'text_original':text,'source_url':None}
        parsed,meta=extract(runner,model,language,row);checks=[]
        for r in audit(runner,model,language,row,parsed['assessments'][0]['claims'] if parsed else [],{'Ryu'}):
            c=r['claim']
            numeric_ok=c['character']=='Ryu' and c['direction']=='nerf' and c['specificity']=='source_numeric' and any(parameter['current']=='600' and parameter['proposed']=='500' for parameter in c['parameters'])
            checks.append({'claim':r['enriched'] or c,'errors':r['errors'],'audit':r['audit'],'audit_request':r['audit_meta'],'numeric_roles_correct':numeric_ok})
        passed=parsed is not None and len(checks)==1 and all(r['numeric_roles_correct'] and not r['errors'] and (r['audit'] or {}).get('supported') is True for r in checks)
        results.append({'kind':'synthetic_control_not_community_evidence','language':language,'model':model,'source':text,'passed':passed,'checks':checks,'extraction_request':meta})
        write_json(args.out/'progress.json',results)
    write_json(args.out/'results.json',{'kind':'synthetic_end_to_end_numeric_extraction','total':len(results),'passed':sum(r['passed'] for r in results),'cases':results,'limitation':'Two diagnostic positives, not a held-out accuracy benchmark; excluded from community counts.'})
    print('Numeric extraction controls:',sum(r['passed'] for r in results),'/',len(results))


if __name__=='__main__':main()
