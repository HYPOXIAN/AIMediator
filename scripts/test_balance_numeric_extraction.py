"""End-to-end positive numeric extraction controls; never real community evidence."""
import argparse
from pathlib import Path
from run_balance_analysis import (ROOT,Runner,strict_json,write_json,digest,api,
    evidence_units,character_reference,ground_claim)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--base-url',default='http://127.0.0.1:11434');p.add_argument('--num-gpu',type=int);args=p.parse_args()
    prompts={stage:{lang:(ROOT/f'prompts/{name}.{lang}.txt').read_text() for lang in ('en','zh')}
        for stage,name in [('extract','summarize-balance'),('verify','verify-balance')]}
    tags=api(args.base_url,'/api/tags')['models'];installed={r['name']:r['digest'] for r in tags}
    identity={'script_sha256':digest(Path(__file__).read_bytes()),'runner_sha256':digest((ROOT/'scripts/run_balance_analysis.py').read_bytes()),
        'policy_module_sha256':digest((ROOT/'scripts/balance_policy.py').read_bytes()),
        'models':{m:installed[m] for m in ('llama3.1:latest','qwen2.5:7b')},
        'prompts':{s:{l:digest(t.encode()) for l,t in langs.items()} for s,langs in prompts.items()},
        'runtime_options':{'num_gpu':args.num_gpu} if args.num_gpu is not None else {}}
    path=args.out/'manifest.json'
    if path.exists() and strict_json(path.read_text())!=identity:raise ValueError('Control identity changed; use a new output directory')
    write_json(path,identity);runner=Runner(args.base_url,args.out,prompts);runner.runtime_options=identity['runtime_options'];results=[]
    for language,model,text in [('en','llama3.1:latest',"Please reduce Ryu's Hadoken damage from 600 to 500."),('zh','qwen2.5:7b','请将隆的波动拳伤害从600降到500。')]:
        record_id='synthetic-extraction-'+language;row={'record_id':record_id,'text_original':text,'source_url':None}
        data={'comments':[{'comment_id':record_id,'units':evidence_units(text)}],'character_normalization_reference':character_reference(text)}
        parsed,meta=runner.generate(model,language,'extract',data,[record_id]);checks=[]
        for index,c in enumerate(parsed['assessments'][0]['claims'] if parsed else [],1):
            errors,enriched=ground_claim(c,row,{'Ryu'});audit=None;audit_meta=None
            if not errors:
                envelope={'claim_id':record_id+':'+str(index),'comment_id':record_id,'model':model,'claim':enriched}
                verdict,audit_meta=runner.generate(model,language,'verify',{'claims':[envelope],'original_comment':text},[envelope['claim_id']])
                audit=verdict['verdicts'][0] if verdict else None
            numeric_ok=c['character']=='Ryu' and c['direction']=='nerf' and c['specificity']=='source_numeric' and any(parameter['current']=='600' and parameter['proposed']=='500' for parameter in c['parameters'])
            checks.append({'claim':enriched or c,'errors':errors,'audit':audit,'audit_request':audit_meta,'numeric_roles_correct':numeric_ok})
        passed=parsed is not None and len(checks)==1 and all(r['numeric_roles_correct'] and not r['errors'] and (r['audit'] or {}).get('supported') is True for r in checks)
        results.append({'kind':'synthetic_control_not_community_evidence','language':language,'model':model,'source':text,'passed':passed,'checks':checks,'extraction_request':meta})
        write_json(args.out/'progress.json',results)
    write_json(args.out/'results.json',{'kind':'synthetic_end_to_end_numeric_extraction','total':len(results),'passed':sum(r['passed'] for r in results),'cases':results,'limitation':'Two diagnostic positives, not a held-out accuracy benchmark; excluded from community counts.'})
    print('Numeric extraction controls:',sum(r['passed'] for r in results),'/',len(results))


if __name__=='__main__':main()
