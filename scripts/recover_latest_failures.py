"""Bounded retry of final generation failures, preserving the original experiment."""
import argparse
import json
from pathlib import Path

import run_balance_analysis as m


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--base-url',default='http://127.0.0.1:11434')
    p.add_argument('--retry-temperature',type=float,default=0)
    p.add_argument('--allow-exact-duplicates',action='store_true',help='Bounded recovery only: finish strict JSON before removing identical claim objects')
    p.add_argument('--max-attempts',type=int,choices=[1,2],default=2)
    p.add_argument('--num-predict',type=int,default=4096)
    p.add_argument('--comment-id',action='append',help='Retry only these failed source IDs; never add new sources')
    args=p.parse_args()
    report=m.strict_json((args.run/'balance-report.json').read_text())
    manifest=m.strict_json((args.run/'manifest.json').read_text())
    prompts=m.strict_json((args.run/'prompt-snapshot.json').read_text())
    sources={r['record_id']:r for r in m.strict_json((args.run/'source-snapshot.json').read_text())}
    ids=[c['comment_id'] for c in report['coverage'] if c['disposition']=='generation_failed']
    if args.comment_id:
        if set(args.comment_id)-set(ids):raise ValueError('Requested source is not a generation failure in this run')
        ids=[cid for cid in ids if cid in args.comment_id]
    tags={r['name']:r['digest'] for r in m.api(args.base_url,'/api/tags')['models']}
    if any(tags.get(n)!=d for n,d in manifest['identity']['models'].items()):
        raise ValueError('Original local model weights changed')
    identity={'kind':'bounded_generation_recovery_separate_from_original','original_manifest_sha256':m.digest((args.run/'manifest.json').read_bytes()),
        'script_sha256':m.digest(Path(__file__).read_bytes()),'runner_sha256':m.digest((m.ROOT/'scripts/run_balance_analysis.py').read_bytes()),
        'original_failed_ids':ids,'models':manifest['identity']['models'],'prompts':prompts,
        'max_attempts':args.max_attempts,'seeds':[42,43][:args.max_attempts],'num_gpu':99,'retry_temperature':args.retry_temperature,
        'allow_exact_duplicates':args.allow_exact_duplicates,'num_predict':args.num_predict,
        'method':'Full original source, same extraction/verifier prompts and gates; explicit deduplication reminder in separately recorded retry metadata. No repaired or truncated model output.'}
    path=args.out/'manifest.json'
    if path.exists() and m.strict_json(path.read_text())!=identity:raise ValueError('Recovery identity changed')
    m.write_json(path,identity);runner=m.Runner(args.base_url,args.out,prompts)
    if args.allow_exact_duplicates:
        # Keep token limits, duplicate comment-ID checks, strict JSON and every
        # source/semantic gate. Only the early repeated-claim transport abort is
        # disabled for this isolated recovery; raw output remains unchanged.
        m.repeated_claim = lambda output, allowed_ids: False
    characters={e['canonical_name'] for e in m.character_reference()};results=[];accepted=[];quarantine=[]
    for cid in ids:
        row=sources[cid];lang=row['language'];model='llama3.1:latest' if lang=='en' else 'qwen2.5:7b'
        attempts=[];parsed=None
        for attempt,seed in enumerate((42,43)[:args.max_attempts],1):
            runner.runtime_options={'num_gpu':99,'seed':seed,'temperature':args.retry_temperature,'num_predict':args.num_predict}
            data={'comments':[{'comment_id':cid,'units':m.evidence_units(row['text_original'])}],
                'character_normalization_reference':m.character_reference(row['text_original']),
                'generation_retry':{'attempt':attempt,'instruction':'Return each DISTINCT supported concern ONCE. Never repeat an identical claim. Close the claims array after the unique supported concerns. No supported character concern means claims=[]. Keep all original conditions and source gates.'}}
            parsed,meta=runner.generate(model,lang,'extract',data,[cid]);attempts.append(meta)
            if parsed is not None:break
        generated=parsed['assessments'][0]['claims'] if parsed else []
        distinct=[];seen=set()
        for claim in generated:
            signature=json.dumps(claim,sort_keys=True,ensure_ascii=False)
            if args.allow_exact_duplicates and signature in seen:continue
            seen.add(signature);distinct.append(claim)
        m.write_json(args.out/(cid.replace(':','-')+'-normalization.json'),{
            'original_claims':len(generated),'distinct_claims':len(distinct),
            'exact_duplicate_objects_removed':len(generated)-len(distinct),
            'method':'Only identical complete JSON claim objects; no wording, evidence, values or directions repaired.'})
        checked=[]
        for i,claim in enumerate(distinct,1):
            errors,enriched=m.ground_claim(claim,row,characters)
            item={'claim_id':cid+':recovery:'+str(i),'comment_id':cid,'model':model,'claim':enriched or claim}
            audit=None;audit_meta=None
            if not errors:
                runner.runtime_options={'num_gpu':99,'seed':42}
                verdict,audit_meta=runner.generate(model,lang,'verify',{'claims':[item],'original_comment':row['text_original']},[item['claim_id']])
                audit=verdict['verdicts'][0] if verdict else None
            checked.append({**item,'source_errors':errors,'audit':audit,'audit_request':audit_meta})
            if not errors and (audit or {}).get('supported'):
                accepted.append({**item['claim'],'claim_id':item['claim_id'],'comment_id':cid,'model':model,'semantic_audit':audit,'recovery_provenance':'separate_bounded_retry'})
            else:quarantine.append(checked[-1])
        results.append({'comment_id':cid,'language':lang,'generation_recovered':parsed is not None,'attempts':attempts,'claims':checked,
            'exact_duplicate_objects_removed':len(generated)-len(distinct)})
        m.write_json(args.out/'progress.json',results)
    output={'original_failed_comments':len(ids),'generation_recovered':sum(r['generation_recovered'] for r in results),
        'still_failed':sum(not r['generation_recovered'] for r in results),'accepted_claims':accepted,'quarantined_claims':quarantine,'cases':results,
        'original_run_unchanged':True,'limitation':'Recovery of valid generation does not prove completeness of concerns or semantic accuracy; original first-pass failures remain reported.'}
    m.write_json(args.out/'results.json',output)
    print('Recovered generation:',output['generation_recovered'],'/',len(ids),flush=True)


if __name__=='__main__':main()
