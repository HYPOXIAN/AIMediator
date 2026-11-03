"""Replay authored synthetic annotations into deterministic example artifacts.

This demonstration makes no model calls and measures no semantic accuracy.
"""
import argparse
from unittest.mock import patch
import json
from pathlib import Path
import sys
sys.path.insert(1, str(Path(__file__).resolve().parents[1]))  # scripts/ holds the registered forwarding shells
import evidence_quality as q
import run_balance_analysis as m


def mock_pipeline(folder, cases, dataset):
    annotations={c['source']['record_id']:c['annotation'] for c in cases}
    originals={c['source']['record_id']:c['source'] for c in cases}
    def retrieval(rows, base, out, model):
        result=[{'comment_id':r['record_id'],'language':r['language'], 'positive_score':.9,
                 'negative_score':.1,'retrieval_related':True,'references':[]} for r in rows]
        m.write_json(out/'retrieval.json',result)
        return result
    def transport(base,payload,path):
        data=json.loads(payload['messages'][1]['content']);props=payload['format']['properties']
        if 'segments' in props:result=annotations[data['comments'][0]['comment_id']]
        elif 'decisions' in props:result={'decisions':['related']*len(data['comments'])}
        elif 'support' in props:result={'support':'supported'}
        else:
            assessments={}
            for row in data['comments']:
                cid=row['comment_id'];claims=[];a=annotations[cid]
                for point in a['information_points']:
                    if point['scope']!='character_balance' or not point['character_literal'] or point['stance']=='uncertain':continue
                    if 'allowed_quality_points' in row and point['point_id'] not in {p['point_id'] for p in row['allowed_quality_points']}:continue
                    selected=[s for s in a['segments'] if s['segment_id'] in point['segment_ids']]
                    names=m.character_candidates(point['character_literal'],m.character_reference(originals[cid]['text_original']))
                    if len(names)!=1:continue
                    claim={'character':names[0],'target':point['mechanic_literal'],'direction':point['direction'],
                        'recommendation':' '.join(s['quote'] for s in selected),'specificity':'qualitative_only',
                        'parameters':[],'evidence_ids':list(dict.fromkeys(s['evidence_id'] for s in selected)), 'uncertain':False}
                    if 'numeric_request' in cid:
                        claim['specificity']='source_numeric'
                        claim['parameters']=[{'metric':'damage','current':'600','proposed':'500','delta':None,
                                              'unit':None,'evidence_id':selected[0]['evidence_id']}]
                    if 'allowed_quality_points' in row:claim['quality_point_ids']=[point['point_id']]
                    claims.append(claim)
                assessments[cid]={'claims':claims}
            result={'assessments':assessments}
        return {'done':True,'done_reason':'stop','mock_fixture':True,'message':{'content':json.dumps(result,ensure_ascii=False)}}
    tags={'models':[{'name':name,'digest':'MOCK-NOT-A-REAL-MODEL'} for name in ('llama3.1:latest','qwen2.5:7b','qwen3-embedding:8b')]}
    for mode in ('off','shadow','enforce'):
        args=argparse.Namespace(out=folder/mode,dataset=dataset,model=None,embedding_model='qwen3-embedding:8b',
            base_url='http://mock.invalid',evidence_quality=mode,quality_only=False,relevance_only=False)
        with patch.object(m,'api',return_value=tags),patch.object(m,'retrieve',side_effect=retrieval),patch.object(m,'streamed_chat',side_effect=transport):
            m.run(args)
        m.write_json(folder/mode/'execution-provenance.json',{'execution':'mock_models_and_retrieval',
            'source':'agent_authored_synthetic','all_admitted_by_mock':True,'semantic_accuracy':None})


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mock-pipeline',action='store_true',help='Also run all three modes with mocked retrieval/models')
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();folder=args.out
    if folder.exists():raise ValueError('Choose a new example output directory')
    cases_path=m.ROOT/'data/evaluation/evidence-quality-synthetic-v1/cases.json'
    cases=json.loads(cases_path.read_text());policy=q.load_policy();records=[]
    for c in cases:
        row=c['source'];record=q.qualify(c['annotation'],row,m.evidence_units(row['text_original']),policy)
        record['annotation_origin']='agent_authored_synthetic_fixture'
        record['attempts']=[];records.append(record)
    routed=[r for record in records for r in record['routing']]
    m.write_json(folder/'manifest.json',{'mode':'synthetic_annotation_replay_no_inference',
        'cases_sha256':m.digest(cases_path.read_bytes()),'policy':policy,
        'module_sha256':m.digest((m.ROOT/'scripts/evidence_quality.py').read_bytes()),
        'accuracy_established':False})
    m.write_json(folder/'evidence-quality.json',records)
    m.write_json(folder/'quality-routing.json',routed)
    m.write_json(folder/'quality-review-queue.json',[r for r in routed if r['route']=='review'])
    m.write_json(folder/'quality-exclusions.json',[r for r in routed if r['route']=='exclude'])
    m.write_json(folder/'system-feedback.json',[r for r in routed if r['route']=='system_evidence'])
    m.write_json(folder/'opinion-summary.json',q.summarize_opinions(records,m.character_reference('\n'.join(c['source']['text_original'] for c in cases))))
    m.write_json(folder/'mixed-comment-examples.json',[r for r in records if len(r['routes_present'])>1])
    if args.mock_pipeline:
        mock_pipeline(folder/'mock-pipeline',cases,m.ROOT/'data/evaluation/evidence-quality-synthetic-v1/records.jsonl')
    print(json.dumps({'comments':len(records),'failed':sum(r['status']=='failed' for r in records),
                      'output':str(folder.resolve()),'semantic_accuracy':None}))


if __name__=='__main__':main()
