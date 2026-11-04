"""Live bilingual meaning controls; synthetic inputs never enter community counts."""
import argparse
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.common import sha as digest, strict_json, write as write_json
from aimediator.evidence import character_reference, evidence_units, ground_claim
from aimediator.inference import api
from aimediator.resources import asset_path
from aimediator.run_store import code_manifest
from aimediator.runner import Runner

ASSETS = ('configs/balance-review-policy.json', 'data/glossary.json', 'prompts/summarize-balance.en.txt',
          'prompts/summarize-balance.zh.txt', 'prompts/verify-balance.en.txt', 'prompts/verify-balance.zh.txt')

FIXTURES = [
    ('en', 'negated_nerf', 'Do not nerf Ken.', [('Ken','keep')]),
    ('en', 'conditional_nerf', 'If Ryu is not nerfed, I will quit.', [('Ryu','nerf')]),
    ('en', 'attacker_not_victim', 'Ken hits Ryu too hard. Please nerf Ken.', [('Ken','nerf')]),
    ('en', 'system_not_roster', 'Drive Rush needs a nerf. Elena looks great.', []),
    ('zh', 'negated_nerf', '不要削弱肯。', [('Ken','keep')]),
    ('zh', 'conditional_nerf', '隆不削弱我就退游。', [('Ryu','nerf')]),
    ('zh', 'attacker_not_victim', '肯打隆太痛了，请削弱肯。', [('Ken','nerf')]),
    ('zh', 'system_not_roster', '绿冲需要削弱，艾莲娜很好看。', []),
]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--base-url',default='http://127.0.0.1:11434')
    p.add_argument('--num-gpu',type=int,default=99)
    args=p.parse_args()
    prompts={s:{l:asset_path(f'prompts/{name}.{l}.txt').read_text(encoding='utf-8') for l in ('en','zh')}
        for s,name in [('extract','summarize-balance'),('verify','verify-balance')]}
    models={'en':'llama3.1:latest','zh':'qwen2.5:7b'}
    tags={r['name']:r['digest'] for r in api(args.base_url,'/api/tags')['models']}
    identity={'kind':'synthetic_semantic_controls_not_community_evidence','fixtures':FIXTURES,
        'script_sha256':digest(Path(__file__).read_bytes()),'package_code_sha256':code_manifest()['modules'],
        'asset_sha256':{name:digest(asset_path(name).read_bytes()) for name in ASSETS},
        'models':{n:tags[n] for n in models.values()},'prompts':prompts,'runtime_options':{'num_gpu':args.num_gpu}}
    path=args.out/'manifest.json'
    if path.exists() and strict_json(path.read_text(encoding='utf-8')) != json.loads(json.dumps(identity)):
        raise ValueError('Control identity changed; use a new output directory')
    write_json(path,identity)
    runner=Runner(args.base_url,args.out,prompts);runner.runtime_options=identity['runtime_options']
    results=[];characters={e['canonical_name'] for e in character_reference()}
    for lang,category,text,expected in FIXTURES:
        cid='synthetic-'+lang+'-'+category;model=models[lang]
        source={'record_id':cid,'text_original':text,'source_url':None}
        data={'comments':[{'comment_id':cid,'units':evidence_units(text)}],
            'character_normalization_reference':character_reference(text)}
        parsed,meta=runner.generate(model,lang,'extract',data,[cid]);checks=[]
        for i,claim in enumerate(parsed['assessments'][0]['claims'] if parsed else [],1):
            errors,enriched=ground_claim(claim,source,characters)
            audit=None;verify_request=None
            if not errors:
                item={'claim_id':cid+':'+str(i),'comment_id':cid,'claim':enriched}
                verdict,verify_request=runner.generate(model,lang,'verify',{'claims':[item],'original_comment':text},[item['claim_id']])
                audit=verdict['verdicts'][0] if verdict else None
            checks.append({'claim':enriched or claim,'source_errors':errors,'audit':audit,'verify_request':verify_request})
        observed={(c['claim']['character'],c['claim']['direction']) for c in checks}
        passed=parsed is not None and observed==set(expected) and all(not c['source_errors'] and (c['audit'] or {}).get('supported') and c['claim']['parameters']==[] and c['claim']['specificity']=='qualitative_only' for c in checks)
        results.append({'kind':'synthetic_control_not_community_evidence','language':lang,'category':category,
            'text_original':text,'expected_pairs':expected,'passed':passed,'claims':checks,'extract_request':meta})
        write_json(args.out/'progress.json',results)
    report={'kind':'eight_synthetic_semantic_controls_not_accuracy','passed':sum(r['passed'] for r in results),'total':len(results),'cases':results,
        'limitation':'Eight deliberately constructed diagnostics, not independent real-source accuracy; excluded from community counts.'}
    write_json(args.out/'results.json',report)
    print(f"Semantic controls: {report['passed']}/{report['total']}",flush=True)


if __name__=='__main__':main()
