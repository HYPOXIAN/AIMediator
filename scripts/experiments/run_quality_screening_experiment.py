"""Screen an existing comment group with frozen relevance and live quality models.

No extraction or design is performed. Retained means eligible for the specified
analysis use, never verified mechanism truth or engineering approval.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import time

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator import evidence_quality as q
from aimediator.common import sha as digest, strict_json, write as write_json
from aimediator.evidence import evidence_units
from aimediator.inference import api
from aimediator.pipeline import quality_request
from aimediator.resources import asset_path, module_path, workspace_root
from aimediator.run_store import code_manifest
from aimediator.runner import Runner

ROOT = workspace_root()
ASSETS = ('configs/balance-review-policy.json', 'configs/evidence-quality-policy.json',
          'configs/local-language-routing.json', 'data/glossary.json', 'prompts/evidence-quality.en.txt',
          'prompts/evidence-quality.zh.txt')

RETAINED_ROUTES = {'opinion_only', 'mechanism_evidence', 'system_evidence'}
NAMES = {'opinion_only': '一般意见统计', 'mechanism_evidence': '角色机制候选',
         'system_evidence': '系统反馈', 'exclude': '剔除', 'review': '待复核'}


def classify(row, relevance, quality_record=None):
    original = row['text_original']
    common = {'comment_id': row['record_id'], 'language': row['language'],
              'source_url': row.get('source_url'), 'text_original': original,
              'content_sha256': digest(original.encode()), 'relevance_record': relevance}
    if not relevance['agreement']:
        pending = (relevance.get('model_uncertain') is True or
                   relevance.get('retrieval_review_uncertain') is True)
        return {**common, 'decision': 'review' if pending else 'excluded',
                'decision_stage': 'frozen_relevance', 'routes_present': ['review' if pending else 'exclude'],
                'reason': '历史相关性结果不确定' if pending else '历史检索/相关性复核未放行',
                'retained_fragments': [], 'excluded_fragments': [], 'review_fragments': [],
                'quality_status': 'not_applicable', 'quality_record': None, 'partial': False}
    if quality_record is None:
        raise ValueError('Every admitted comment needs a quality record')
    routed = quality_record['routing']
    kept = [r for r in routed if r['route'] in RETAINED_ROUTES]
    excluded = [r for r in routed if r['route'] == 'exclude']
    reviews = [r for r in routed if r['route'] == 'review']
    decision = 'retained' if kept else 'review' if reviews else 'excluded'
    return {**common, 'decision': decision, 'decision_stage': 'quality',
        'routes_present': quality_record['routes_present'], 'quality_status': quality_record['status'],
        'reason': '；'.join(NAMES[route] for route in quality_record['routes_present']),
        'retained_fragments': kept, 'excluded_fragments': excluded, 'review_fragments': reviews,
        'quality_record': quality_record, 'partial': bool(kept and (excluded or reviews))}


def jsonl(path, rows):
    path.write_text(''.join(json.dumps(row, ensure_ascii=False, allow_nan=False)+'\n' for row in rows), encoding='utf-8')


def export_results(folder, rows):
    if len({r['comment_id'] for r in rows}) != len(rows):
        raise ValueError('Duplicate classification IDs')
    groups = {key: [r for r in rows if r['decision'] == key] for key in ('retained','excluded','review')}
    assert sum(map(len, groups.values())) == len(rows)
    for key, group in groups.items():
        write_json(folder/(key+'-comments.json'), group)
        jsonl(folder/(key+'-comments.jsonl'), group)
        heading = {'retained':'保留的数据','excluded':'整条剔除的数据','review':'待复核的数据'}[key]
        lines = ['# '+heading, '', '本实验只筛选证据用途，不证明机制真实或适合任何版本。原文未改写。', '']
        for row in group:
            lines += ['## '+row['comment_id'], '',
                      '语言：'+row['language']+'；阶段：'+row['decision_stage']+'；结果：'+row['reason'], '',
                      '原文：', '', *['> '+line for line in row['text_original'].splitlines()], '']
            if row.get('source_url'):
                lines += ['[来源]('+row['source_url']+')','']
            for kind,label in [('retained_fragments','保留片段'),('excluded_fragments','剔除片段'),('review_fragments','待复核片段')]:
                if not row[kind]:
                    continue
                lines += ['### '+label, '']
                for item in row[kind]:
                    lines += [NAMES[item['route']]+'；原因：'+item['reason'], '']
                    for s in item['segments']:
                        lines += [f"{s['evidence_id']} [{s['start']},{s['end']})", '',
                                  '> '+s.get('quote',s.get('text','')).replace('\n','\n> '), '']
        (folder/(key+'-comments.md')).write_text('\n'.join(lines)+'\n', encoding='utf-8')
    # Removed portions of mixed comments remain separate from wholly removed rows.
    portions = [{ 'comment_id': r['comment_id'], 'source_url':r['source_url'],
                 'whole_comment_decision':r['decision'], 'fragment': p}
                for r in rows for p in r['excluded_fragments']]
    write_json(folder/'excluded-fragments.json', portions)
    write_json(folder/'all-classifications.json', rows)
    records = [r['quality_record'] for r in rows if r['quality_record']]
    write_json(folder/'evidence-quality.json', records)
    summary = {'input_comments':len(rows), 'mutually_exclusive_comment_counts':{key:len(value) for key,value in groups.items()},
        'partial_retained_comments':sum(r['partial'] for r in rows),
        'quality_assessed':len(records), 'quality_completed':sum(r['status']=='completed' for r in records),
        'quality_failed_review':sum(r['status']=='failed' for r in records),
        'inherited_relevance_excluded':sum(r['decision']=='excluded' and r['decision_stage']=='frozen_relevance' for r in rows),
        'new_quality_excluded':sum(r['decision']=='excluded' and r['decision_stage']=='quality' for r in rows),
        'review_fragments_in_retained_comments':sum(bool(r['review_fragments']) and r['decision']=='retained' for r in rows),
        'route_comment_counts':{route:sum(route in r['routes_present'] for r in rows) for route in q.ROUTES},
        'excluded_fragment_items':len(portions),
        'by_language':{lang:dict(Counter(r['decision'] for r in rows if r['language']==lang)) for lang in sorted({r['language'] for r in rows})},
        'retained_definition':'Contains at least one opinion_only, mechanism_evidence or system_evidence point. Only retained fragments are eligible, not the entire text.',
        'mechanism_status':'Candidates only; no new extraction, claim audit, source review, official identity or version verification.',
        'scope':'Existing 100-comment bilingual group; frozen prior relevance, fresh live quality; not a fresh full RAG run.',
        'accuracy':None, 'human_ground_truth':False}
    write_json(folder/'summary.json', summary)
    return summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--group',type=Path,default=ROOT/'data/evaluation/balance-silver-v1/labels.jsonl')
    p.add_argument('--from-run',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--base-url',default='http://127.0.0.1:11434')
    p.add_argument('--workers',type=int,default=3)
    args=p.parse_args()
    folder=args.out.resolve()
    if not 1<=args.workers<=4:
        raise ValueError('workers must be in [1,4]')
    group_bytes=args.group.read_bytes()
    # Use membership only. Never send old relevance/stance expectations to models.
    ids=[strict_json(line)['comment_id'] for line in group_bytes.decode().splitlines() if line.strip()]
    if len(ids)!=len(set(ids)):
        raise ValueError('Duplicate group IDs')
    source_bytes=(args.from_run/'source-snapshot.json').read_bytes()
    relevance_bytes=(args.from_run/'relevance.json').read_bytes()
    sources={r['record_id']:r for r in json.loads(source_bytes)}
    decisions={r['comment_id']:r for r in json.loads(relevance_bytes)}
    if not set(ids)<=set(sources) or not set(ids)<=set(decisions):
        raise ValueError('Incomplete frozen source/relevance coverage')
    rows=[sources[cid] for cid in ids]
    routing=json.loads(asset_path('configs/local-language-routing.json').read_text(encoding='utf-8'))
    models={v['language']:name for name,v in routing['models'].items()}
    tags={r['name']:r['digest'] for r in api(args.base_url,'/api/tags')['models']}
    if any(models.get(r['language']) not in tags for r in rows):
        raise ValueError('A required local language model is missing')
    policy=q.load_policy()
    prompts={'quality':{lang:asset_path(f'prompts/evidence-quality.{lang}.txt').read_text(encoding='utf-8') for lang in ('en','zh')}}
    identity={'version':'existing-group-quality-screen-v1','group_sha256':digest(group_bytes),
        'source_sha256':digest(source_bytes),'relevance_sha256':digest(relevance_bytes),
        'comment_ids':ids,'policy':policy,'prompts':prompts,
        'script_sha256':digest(Path(__file__).read_bytes()),'package_code_sha256':code_manifest()['modules'],
        'asset_sha256':{name:digest(asset_path(name).read_bytes()) for name in ASSETS},
        'models':{models[lang]:tags[models[lang]] for lang in {r['language'] for r in rows}},
        'mode':'quality_only_using_frozen_relevance'}
    folder.mkdir(parents=True,exist_ok=True)
    manifest=folder/'manifest.json'
    if manifest.exists():
        if json.loads(manifest.read_text(encoding='utf-8'))['identity']!=identity:
            raise ValueError('Changed inputs/code: choose a new output directory')
    else:
        write_json(manifest,{'identity':identity,'created_at_utc':datetime.now(timezone.utc).isoformat(),
            'group_path':str(args.group.resolve()),'frozen_relevance_run':str(args.from_run.resolve()),
            'labels_used_for_model_decisions':False,'workers':args.workers,
            'limits':'Not independent accuracy evaluation. No retrieval, extraction or engineering design.'})
        write_json(folder/'source-snapshot.json',rows)
        write_json(folder/'relevance.json',[decisions[cid] for cid in ids])
        (folder/('snapshot-'+Path(__file__).name)).write_bytes(Path(__file__).read_bytes())
        for name in ('configs/evidence-quality-policy.json','configs/balance-review-policy.json','data/glossary.json'):
            (folder/('snapshot-'+Path(name).name)).write_bytes(asset_path(name).read_bytes())
        snapshot=folder/'code-snapshot'
        snapshot.mkdir(exist_ok=True)
        for name in identity['package_code_sha256']:
            (snapshot/name).write_bytes(module_path(name).read_bytes())
    runner=Runner(args.base_url,folder,prompts,identity,policy,log=lambda text:print(text,flush=True))
    def process(row):
        cid=row['record_id']
        decision=decisions[cid]
        if not decision['agreement']:
            return classify(row,decision)
        units=evidence_units(row['text_original'])
        attempts=[]
        record=None
        for attempt in range(policy['max_attempts']):
            data,context=quality_request(runner,row,units,row['language'],identity,attempts)
            parsed,meta=runner.generate(models[row['language']],row['language'],'quality',data,[cid],request_context=context)
            attempts.append(meta)
            if parsed is not None:
                record=q.qualify_v2(parsed,row,units,data['segments'],policy)
                if not record['errors']:
                    break
                record=None
        record=record or q.failed_record(row,units,attempts,policy)
        record.update(attempts=attempts,model=models[row['language']],observation_only=False)
        return classify(row,decision,record)
    completed={}
    start=time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures={pool.submit(process,row):row['record_id'] for row in rows}
        for future in as_completed(futures):
            result=future.result()
            completed[result['comment_id']]=result
            write_json(folder/'progress.json',{'completed':len(completed),'input':len(rows),
                'elapsed_seconds':time.monotonic()-start,'decisions':dict(Counter(r['decision'] for r in completed.values()))})
            write_json(folder/'screening-progress.json',[completed[cid] for cid in ids if cid in completed])
            print(json.dumps({'completed':len(completed),'input':len(rows),'comment_id':result['comment_id'],
                'decision':result['decision'],'quality_status':result['quality_status']},ensure_ascii=False),flush=True)
    summary=export_results(folder,[completed[cid] for cid in ids])
    summary['elapsed_seconds']=time.monotonic()-start
    write_json(folder/'summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':
    main()
