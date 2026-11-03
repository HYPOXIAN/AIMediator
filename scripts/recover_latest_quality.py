"""Try the existing compact exact-quote transport on failed quality annotations.

All imported or expanded annotations pass the unchanged full source validator.
This is a supplemental recovery experiment, not repair of old model output.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

import evidence_quality as q
import run_balance_analysis as m
import run_quality_screening_recovery as compact

MAP = '''COMPACT TRANSPORT OVERRIDE: Apply the same information, scope, stance and source rules, but return the compact format instead of absolute offsets. The program derives offsets ONLY from exact quotes uniquely located in their named unit, then performs all original checks. segments contains EVERY unit ID as a required key. Its fragments use id=segment ID, q=exact source quote, s=scope, k=content kind, t=emotional tone, r=reason code. points use i=selected fragment IDs, s=scope, l=detail level, a=stance, d=direction, c=source character literal or null, m=source mechanic literal or null. No extra fields. Every quote must uniquely match its named unit. Cover every unit completely in order. A context-dependent reaction without a new concern belongs to the preceding mechanic point, with the subject-containing fragment also selected; do not create a disconnected new point for it. The CURRENT stance is not the historical patch event direction. Never treat criticism of a past nerf as a request for another nerf.'''


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--from-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--base-url',default='http://127.0.0.1:11434')
    p.add_argument('--retry-temperature',type=float,default=0)
    args=p.parse_args()
    sources={r['record_id']:r for r in m.strict_json((args.from_run/'source-snapshot.json').read_text())}
    records=m.strict_json((args.from_run/'evidence-quality.json').read_text())
    failed=[r for r in records if r['status']=='failed'];policy=q.load_policy()
    tags={r['name']:r['digest'] for r in m.api(args.base_url,'/api/tags')['models']}
    prompts={lang:(m.ROOT/f'prompts/evidence-quality.{lang}.txt').read_text()+'\n'+MAP for lang in ('en','zh')}
    identity={'protocol':'existing_compact_exact_quote_transport_with_current_quality_rules',
        'parent_manifest_sha256':m.digest((args.from_run/'manifest.json').read_bytes()),
        'script_sha256':m.digest(Path(__file__).read_bytes()),'compact_module_sha256':m.digest((m.ROOT/'scripts/run_quality_screening_recovery.py').read_bytes()),
        'policy':policy,'models':tags,'effective_prompts':prompts,'failed_ids':[r['comment_id'] for r in failed],
        'num_gpu':99,'retry_temperature':args.retry_temperature,'max_attempts':2,'original_run_unchanged':True}
    path=args.out/'manifest.json'
    if path.exists() and m.strict_json(path.read_text())!=identity:raise ValueError('Recovery identity changed')
    m.write_json(path,identity);results=[]
    for previous in failed:
        cid=previous['comment_id'];row=sources[cid];lang=row['language'];model='llama3.1:latest' if lang=='en' else 'qwen2.5:7b'
        units=m.evidence_units(row['text_original']);attempts=[];record=None
        references=[]
        for item in m.character_reference(row['text_original']):
            literals=[item.get('chinese_label'),item['canonical_name']]+[a['text'] for a in item.get('aliases',[])]
            references += [t for t in literals if t and m.term_matches(t,row['text_original'])]
        for attempt in range(1,3):
            schema=compact.compact_schema(units)
            payload={'model':model,'messages':[{'role':'system','content':prompts[lang]},
                {'role':'user','content':json.dumps({'units':[{'id':u['evidence_id'],'text':u['text']} for u in units],
                    'source_literal_name_candidates':list(dict.fromkeys(references)),'attempt':attempt},ensure_ascii=False)}],
                'format':schema,'stream':True,'keep_alive':'10m','options':{'num_gpu':99,'temperature':args.retry_temperature,'seed':42+attempt-1,'num_ctx':policy['num_ctx'],'num_predict':policy['num_predict']}}
            rid=m.digest(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode());folder=args.out/'requests'/rid
            m.write_json(folder/'request.json',payload);start=time.monotonic()
            response_path=folder/'response.json'
            if response_path.exists():response=m.strict_json(response_path.read_text())
            else:
                raw=m.streamed_chat(args.base_url,payload,folder/'partial-output.txt');response={'elapsed_seconds':time.monotonic()-start,'response':raw};m.write_json(response_path,response)
            errors=[];annotation=None
            try:
                raw=response['response']
                if raw.get('done') is not True or raw.get('done_reason')!='stop':errors.append('Incomplete generation')
                parsed=m.strict_json(raw['message']['content']);annotation,validation=compact.expand(parsed,row,units);errors+=validation
            except (ValueError,KeyError,TypeError) as exc:errors.append(str(exc))
            m.write_json(folder/'validation.json',{'errors':errors,'schema':schema})
            attempts.append({'request_id':rid,'errors':errors,'elapsed_seconds':response['elapsed_seconds']})
            if not errors:
                record=q.qualify(annotation,row,units,policy);break
        record=record or q.failed_record(row,units,attempts,policy)
        record.update(model=model,attempts=attempts,recovery_protocol=identity['protocol'])
        results.append(record);m.write_json(args.out/'evidence-quality.json',results)
    output={'original_failed':len(failed),'recovered':sum(r['status']=='completed' for r in results),
        'still_failed':sum(r['status']!='completed' for r in results),'records':results,
        'note':'Exact unique quotes determine offsets without guessing; original semantic and coverage validation is unchanged. Structural recovery is not semantic accuracy.'}
    m.write_json(args.out/'results.json',output);print('Compact quality recovery:',output['recovered'],'/',len(failed),flush=True)


if __name__=='__main__':main()
