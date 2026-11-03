"""Small live bilingual prompt regression on real, relevance-admitted sources.

This is a known-case regression, never a model accuracy estimate. Synthetic
numeric controls are run separately and never enter community counts.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
sys.path.insert(1, str(Path(__file__).resolve().parents[1]))  # scripts/ holds the registered forwarding shells
from run_balance_analysis import (ROOT,Runner,api,strict_json,write_json,digest,
    evidence_units,character_reference,ground_claim)

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
    p.add_argument('--prompt-dir',type=Path,default=ROOT/'prompts');args=p.parse_args()
    snapshots=strict_json((args.admission_run/'source-snapshot.json').read_text());sources={r['record_id']:r for r in snapshots}
    admitted={r['comment_id'] for r in strict_json((args.admission_run/'relevance.json').read_text()) if r['agreement']}
    prompts={stage:{lang:(args.prompt_dir/f'{name}.{lang}.txt').read_text() for lang in ('en','zh')}
        for stage,name in [('extract','summarize-balance'),('verify','verify-balance')]}
    tags=api(args.base_url,'/api/tags')['models'];installed={r['name']:r['digest'] for r in tags}
    identity={'script_sha256':digest(Path(__file__).read_bytes()),'runner_sha256':digest((ROOT/'scripts/run_balance_analysis.py').read_bytes()),
        'policy_module_sha256':digest((ROOT/'scripts/balance_policy.py').read_bytes()),'policy_sha256':digest((ROOT/'configs/balance-review-policy.json').read_bytes()),
        'admission_manifest_sha256':digest((args.admission_run/'manifest.json').read_bytes()),
        'prompts':{s:{l:digest(t.encode()) for l,t in langs.items()} for s,langs in prompts.items()},
        'models':{model:installed[model] for model in ('llama3.1:latest','qwen2.5:7b')},'cases':CASES,
        'runtime_options':{'num_gpu':args.num_gpu} if args.num_gpu is not None else {}}
    path=args.out/'manifest.json'
    if path.exists() and strict_json(path.read_text())!=identity:raise ValueError('Live run identity changed; choose a new directory')
    write_json(path,identity);write_json(args.out/'prompt-snapshot.json',prompts)
    runner=Runner(args.base_url,args.out,prompts);runner.runtime_options=identity['runtime_options'];characters={r['canonical_name'] for r in character_reference()};results=[]
    for case in CASES:
        record_id=case['comment_id'];source=sources[record_id];language=source['language'];model='llama3.1:latest' if language=='en' else 'qwen2.5:7b'
        if record_id not in admitted:
            results.append({**case,'passed':False,'status':'not_admitted_no_extraction','comment_id':record_id});continue
        data={'comments':[{'comment_id':record_id,'units':evidence_units(source['text_original'])}],
              'character_normalization_reference':character_reference(source['text_original'])}
        parsed,meta=runner.generate(model,language,'extract',data,[record_id]);checks=[]
        for index,c in enumerate(parsed['assessments'][0]['claims'] if parsed else [],1):
            errors,enriched=ground_claim(c,source,characters);audit=None;audit_meta=None
            if not errors:
                envelope={'claim_id':record_id+':'+str(index),'comment_id':record_id,'model':model,'claim':enriched}
                verdict,audit_meta=runner.generate(model,language,'verify',{'claims':[envelope],'original_comment':source['text_original']},[envelope['claim_id']])
                audit=verdict['verdicts'][0] if verdict else None
            checks.append({'claim':enriched or c,'source_errors':errors,'audit':audit,'audit_request':audit_meta})
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
