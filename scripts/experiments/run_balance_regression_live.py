"""Small live bilingual prompt regression on real, relevance-admitted sources.

This is a known-case regression, never a model accuracy estimate. Synthetic
numeric controls are run separately and never enter community counts.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.common import sha as digest, strict_json, write as write_json
from aimediator.diagnostics import audit, extract
from aimediator.evidence import character_reference
from aimediator.inference import api
from aimediator.resources import asset_path
from aimediator.run_store import code_manifest
from aimediator.runner import Runner

# Prompts come from --prompt-dir and are identified by their content digests.
ASSETS = ('configs/balance-review-policy.json', 'data/glossary.json')

CASES=[
    {'comment_id':'steam:229094178','required':[['Manon','buff']],'forbidden':[],'category':'explicit_buff'},
    {'comment_id':'steam:229292137','required':[],'forbidden':['Elena'],'category':'system_not_roster_praise'},
    {'comment_id':'steam:235001445','required':[['Jamie','buff']],'forbidden':[],'category':'hostile_wording_does_not_reverse_direction'},
    {'comment_id':'steam:237619085','required':[['Arjun','nerf']],'forbidden':['Zangief'],'category':'attacker_not_victim'},
    {'comment_id':'steam:237685225','required':[],'forbidden':['Dhalsim'],'category':'nationality_not_identity'},
    {'comment_id':'steam:237728767','required':[['Arjun','nerf']],'forbidden':[],'category':'source_literal_unknown_official_identity'},
]


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--admission-run',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--base-url',default='http://127.0.0.1:11434');p.add_argument('--num-gpu',type=int)
    p.add_argument('--prompt-dir',type=Path,default=asset_path('prompts'));args=p.parse_args()
    snapshots=strict_json((args.admission_run/'source-snapshot.json').read_text(encoding='utf-8'));sources={r['record_id']:r for r in snapshots}
    admitted={r['comment_id'] for r in strict_json((args.admission_run/'relevance.json').read_text(encoding='utf-8')) if r['agreement']}
    prompts={stage:{lang:(args.prompt_dir/f'{name}.{lang}.txt').read_text(encoding='utf-8') for lang in ('en','zh')}
        for stage,name in [('extract','summarize-balance'),('verify','verify-balance')]}
    tags=api(args.base_url,'/api/tags')['models'];installed={r['name']:r['digest'] for r in tags}
    identity={'script_sha256':digest(Path(__file__).read_bytes()),'package_code_sha256':code_manifest()['modules'],
        'asset_sha256':{name:digest(asset_path(name).read_bytes()) for name in ASSETS},
        'admission_manifest_sha256':digest((args.admission_run/'manifest.json').read_bytes()),
        'prompts':{s:{l:digest(t.encode()) for l,t in langs.items()} for s,langs in prompts.items()},
        'models':{model:installed[model] for model in ('llama3.1:latest','qwen2.5:7b')},'cases':CASES,
        'runtime_options':{'num_gpu':args.num_gpu} if args.num_gpu is not None else {}}
    path=args.out/'manifest.json'
    if path.exists() and strict_json(path.read_text(encoding='utf-8'))!=identity:raise ValueError('Live run identity changed; choose a new directory')
    write_json(path,identity);write_json(args.out/'prompt-snapshot.json',prompts)
    runner=Runner(args.base_url,args.out,prompts,log=lambda text:print(text,flush=True));runner.runtime_options=identity['runtime_options'];characters={r['canonical_name'] for r in character_reference()};results=[]
    for case in CASES:
        record_id=case['comment_id'];source=sources[record_id];language=source['language'];model='llama3.1:latest' if language=='en' else 'qwen2.5:7b'
        if record_id not in admitted:
            results.append({**case,'passed':False,'status':'not_admitted_no_extraction','comment_id':record_id});continue
        parsed,meta=extract(runner,model,language,source)
        checks=[{'claim':r['enriched'] or r['claim'],'source_errors':r['errors'],'audit':r['audit'],'audit_request':r['audit_meta']}
            for r in audit(runner,model,language,source,parsed['assessments'][0]['claims'] if parsed else [],characters)]
        pairs={(r['claim']['character'],r['claim']['direction']) for r in checks}
        missing=[list(pair) for pair in case['required'] if tuple(pair) not in pairs]
        forbidden=[r['claim']['character'] for r in checks if r['claim']['character'] in case['forbidden']]
        numerical=[r for r in checks if r['claim']['parameters']]
        valid=parsed is not None and not missing and not forbidden and not numerical and all(not c['source_errors'] and (c['audit'] or {}).get('supported') is True for c in checks)
        result={**case,'comment_id':record_id,'language':language,'model':model,'admission_verified':True,'passed':valid,
            'status':'complete' if parsed else 'generation_failed','missing_required_pairs':missing,'forbidden_assignments':forbidden,
            'unexpected_numeric_targets':len(numerical),'claims':checks,'extraction_request':meta,'source':source}
        results.append(result);write_json(args.out/'progress.json',results)
    output={'kind':'known_case_live_bilingual_regression_not_accuracy_benchmark','total':len(results),'passed':sum(r['passed'] for r in results),
        'cases':results,'limitations':['Six selected cases, all actual sources must pass relevance agreement before extraction.',
            'Required character/direction pairs are reviewer expectations, not independently adjudicated gold.',
            'Source-literal Arjun feedback remains outside verified engineering character groups.']}
    write_json(args.out/'results.json',output);print(f"Live regressions: {output['passed']}/{output['total']}")


if __name__=='__main__':main()
