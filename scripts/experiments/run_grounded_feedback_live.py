import argparse
import collections
import copy
import csv
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.request

ROOT=Path(__file__).resolve().parents[2]
FIELDS={'comment_id','language','claims','emotional_tone'}
CLAIM_FIELDS={'character','mechanic','direction','reason','evidence_id','uncertain'}
CASE_SPECS=[
 ('steam:235935329','en','explicit_buff',{'characters':['Ingrid'],'directions':['buff'],'must_have_claim':True}),
 ('steam:237737379','en','strength_complaint',{'characters':['Ryu'],'directions':['nerf','unclear'],'must_have_claim':True}),
 ('steam:237615221','en','positive_balance',{'characters':[],'directions':['keep','unclear'],'must_have_claim':True}),
 ('steam:237661313','en','ambiguous_possible_sarcasm',{'characters':[],'directions':['unclear'],'must_have_claim':True,'must_mark_uncertain':True}),
 ('steam:235736413','en','multiple_mechanics',{'characters':[],'directions':['nerf','unclear'],'must_have_claim':True}),
 ('steam:235469922','zh','explicit_buff',{'characters':['Ingrid'],'directions':['buff'],'must_have_claim':True}),
 ('steam:237118886','zh','do_not_nerf',{'characters':['Mai'],'directions':['keep'],'must_have_claim':True}),
 ('steam:235098360','zh','positive_balance',{'characters':[],'directions':['keep','unclear'],'must_have_claim':True}),
 ('steam:237272538','zh','existing_damage_penalty',{'characters':[],'directions':['buff','unclear'],'must_have_claim':True}),
 ('steam:237749034','zh','unnamed_character_multiple_mechanics',{'characters':[],'directions':['nerf','unclear'],'must_have_claim':True,'must_mark_uncertain':True}),
]


def sha(value):
    return hashlib.sha256(value).hexdigest()


def save_json(path, obj):
    temporary=path.with_name(path.name+'.tmp')
    with temporary.open('w',encoding='utf-8') as stream:
        json.dump(obj,stream,ensure_ascii=False,indent=2)
        stream.write('\n');stream.flush();os.fsync(stream.fileno())
    temporary.replace(path)


def local_request(path,payload=None,timeout=300):
    body=None if payload is None else json.dumps(payload).encode()
    request=urllib.request.Request('http://127.0.0.1:11434'+path,data=body,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=timeout) as response:
        return json.load(response)


def evidence_units(text):
    units=[]
    for match in re.finditer(r'[^\n。！？.!?]+(?:[。！？.!?]+|(?=\n|$))',text):
        raw=match.group();start=match.start()+len(raw)-len(raw.lstrip());end=match.end()-len(raw)+len(raw.rstrip())
        if start<end:
            units.append({'evidence_id':'E'+str(len(units)+1),'text':text[start:end],'start':start,'end':end})
    return units


def schema_for(case):
    evidence_property={'type':'string'}
    if case['units']:
        evidence_property['enum']=[u['evidence_id'] for u in case['units']]
    properties={
      'comment_id':{'type':'string','enum':[case['comment_id']]},
      'language':{'type':'string','enum':[case['language']]},
      'claims':{'type':'array','maxItems':3,'items':{'type':'object','additionalProperties':False,'properties':{
        'character':{'enum':case['character_candidates']+[None]},
        'mechanic':{'type':['string','null']},
        'direction':{'type':'string','enum':['buff','nerf','keep','unclear']},
        'reason':{'type':'string','maxLength':180},
        'evidence_id':evidence_property,
        'uncertain':{'type':'boolean'}},'required':sorted(CLAIM_FIELDS)}},
      'emotional_tone':{'type':'string','enum':['neutral','emotional','unclear']}}
    return {'type':'object','additionalProperties':False,'properties':properties,'required':sorted(FIELDS)}


def validate(output,case,done=True):
    checks={'json_valid':False,'schema_valid':False,'identity_matches':False,'evidence_references_valid':False,'character_candidates_valid':False,'numbers_supported_by_evidence':False,'empty_input_abstention':None if case['kind']=='real_review' else False,'generation_complete':done is True,'accepted_for_human_review':False}
    try:
        obj=json.loads(output)
    except (TypeError,ValueError):
        return checks,None,None
    checks['json_valid']=True
    if not isinstance(obj,dict):
        return checks,obj,None
    checks['identity_matches']=obj.get('comment_id')==case['comment_id'] and obj.get('language')==case['language']
    claims=obj.get('claims')
    structure=set(obj)==FIELDS and isinstance(obj.get('comment_id'),str) and obj.get('language') in ['en','zh','other'] and obj.get('emotional_tone') in ['neutral','emotional','unclear'] and isinstance(claims,list) and len(claims)<=3
    if not isinstance(claims,list):
        return checks,obj,None
    for claim in claims:
        structure=structure and isinstance(claim,dict) and set(claim)==CLAIM_FIELDS
        if not isinstance(claim,dict) or not CLAIM_FIELDS<=set(claim):
            structure=False;continue
        structure=structure and (claim['character'] is None or isinstance(claim['character'],str)) and (claim['mechanic'] is None or isinstance(claim['mechanic'],str)) and claim['direction'] in ['buff','nerf','keep','unclear'] and isinstance(claim['reason'],str) and 0<len(claim['reason'])<=180 and isinstance(claim['evidence_id'],str) and type(claim['uncertain']) is bool
    checks['schema_valid']=bool(structure)
    units={u['evidence_id']:u for u in case['units']}
    refs=all(isinstance(c,dict) and isinstance(c.get('evidence_id'),str) and c['evidence_id'] in units for c in claims)
    checks['evidence_references_valid']=refs
    checks['character_candidates_valid']=all(isinstance(c,dict) and c.get('character') in case['character_candidates']+[None] for c in claims)
    checks['numbers_supported_by_evidence']=refs and all(all(number in units[c['evidence_id']]['text'] for number in re.findall(r'\d+(?:\.\d+)?%?',str(c.get('reason',''))+' '+str(c.get('mechanic') or ''))) for c in claims)
    if case['kind']!='real_review':
        checks['empty_input_abstention']=claims==[]
    required=[v for k,v in checks.items() if k!='accepted_for_human_review' and v is not None]
    checks['accepted_for_human_review']=all(v is True for v in required)
    if not checks['accepted_for_human_review']:
        return checks,obj,None
    enriched=copy.deepcopy(obj)
    for claim in enriched['claims']:
        unit=units[claim['evidence_id']]
        claim.update(evidence=unit['text'],evidence_start=unit['start'],evidence_end=unit['end'])
        assert claim['evidence']==case['text'][claim['evidence_start']:claim['evidence_end']]
    return checks,obj,enriched


def semantic_checks(parsed,case):
    if not isinstance(parsed,dict) or not isinstance(parsed.get('claims'),list):
        return {'provisional_expectations_met':False}
    claims=parsed['claims'];expected=case['expectations'];checks={}
    checks['required_claim_present']=(bool(claims) if expected['must_have_claim'] else not claims)
    if claims:
        checks['directions_within_provisional_expectation']=all(isinstance(c,dict) and c.get('direction') in expected['directions'] for c in claims)
        if expected['characters']:
            checks['expected_character_mentioned']=any(isinstance(c,dict) and c.get('character') in expected['characters'] for c in claims)
        if expected.get('must_mark_uncertain'):
            checks['ambiguity_marked']=all(isinstance(c,dict) and c.get('uncertain') is True for c in claims)
    checks['provisional_expectations_met']=all(checks.values())
    return checks


def prepare_cases(dataset):
    records=[json.loads(line) for line in dataset.read_text().splitlines()]
    rows={r['record_id']:r for r in records};cases=[]
    for identity,language,category,expectations in CASE_SPECS:
        row=rows[identity]
        if row['language']!=language or row.get('coarse_screening',{}).get('decision')!='keep':
            raise ValueError('Case is not a retained record of the expected language: '+identity)
        cases.append({'comment_id':identity,'language':language,'text':row['text_original'],'kind':'real_review','category':category,'character_candidates':expectations['characters'],'units':evidence_units(row['text_original']),'source_url':row['source_url'],'source_record_sha256':sha(json.dumps(row,sort_keys=True,ensure_ascii=False).encode()),'expectations':expectations})
    for language in ['en','zh']:
        cases.append({'comment_id':'empty-control-'+language,'language':language,'text':'','kind':'empty_control','category':'no_evidence_no_claims','character_candidates':[],'units':[],'source_url':None,'expectations':{'characters':[],'directions':[],'must_have_claim':False}})
    return cases


def render_prompt(template,case,schema):
    substitutions={'review_json':{'comment_id':case['comment_id'],'language':case['language'],'text':case['text']},'units_json':case['units'],'characters_json':case['character_candidates'],'schema_json':schema}
    for key,value in substitutions.items():
        template=template.replace('{{'+key+'}}',json.dumps(value,ensure_ascii=False))
    return template


def export(folder,results,cases,models):
    summary={}
    for model in models:
        rows=[r for r in results if r['model']==model];real=[r for r in rows if r['kind']=='real_review'];controls=[r for r in rows if r['kind']=='empty_control']
        summary[model]={'responses':len(rows),'real_reviews':len(real),'empty_controls':len(controls)}
        for key in ['json_valid','schema_valid','identity_matches','evidence_references_valid','character_candidates_valid','numbers_supported_by_evidence','generation_complete','accepted_for_human_review']:
            summary[model][key]={'passed':sum(r.get('checks',{}).get(key) is True for r in rows),'total':len(rows)}
        summary[model]['empty_input_abstention']={'passed':sum(r.get('checks',{}).get('empty_input_abstention') is True for r in controls),'total':len(controls)}
        summary[model]['provisional_semantic_expectations']={'passed':sum(r.get('semantic_checks',{}).get('provisional_expectations_met') is True for r in real),'total':len(real)}
    save_json(folder/'results.json',results);save_json(folder/'summary.json',{'models':summary,'limitations':['Non-random diagnostic sample: ten real reviews plus two separately labeled empty controls per model.','IDs, candidate character values, and evidence reference choices are constrained by JSON schema, not independent tests of unconstrained model reliability.','Exact source quotation and identity checks prevent fabricated review references in accepted outputs; they do not prove paraphrase entailment or complete extraction.','Provisional semantic expectations are agent-authored checks and are not human gold labels.','No historical patch applicability or factual correctness of reviewer assertions was established.','CPU wall time is not a controlled performance benchmark.']})
    with (folder/'validated.jsonl').open('w',encoding='utf-8') as good,(folder/'quarantined.jsonl').open('w',encoding='utf-8') as bad:
        for result in results:
            envelope={'model':result['model'],'kind':result['kind'],'comment_id':result['comment_id'],'needs_human_semantic_review':True,'output':result.get('validated_output'),'checks':result.get('checks',{})}
            if result.get('checks',{}).get('accepted_for_human_review'):
                good.write(json.dumps(envelope,ensure_ascii=False)+'\n')
            else:
                envelope['error']=result.get('error');bad.write(json.dumps(envelope,ensure_ascii=False)+'\n')
    with (folder/'review.csv').open('w',encoding='utf-8',newline='') as stream:
        columns=['model','comment_id','kind','automatic_gate_pass','reason_supported','character_correct','direction_correct','uncertainty_correct','omissions','reviewer','notes'];writer=csv.DictWriter(stream,fieldnames=columns);writer.writeheader()
        for row in results:
            writer.writerow({'model':row['model'],'comment_id':row['comment_id'],'kind':row['kind'],'automatic_gate_pass':row.get('checks',{}).get('accepted_for_human_review')})
    lines=['# Grounded Real-Feedback Pilot','','Ten real retained source reviews (five English, five Chinese) and two separately labeled empty-input controls per model. This is not a full-corpus evaluation or an independent held-out benchmark.','','JSON schema constrains source identity and evidence reference IDs. Quotation text is reconstructed from immutable original spans. No model-written quote is trusted. Automatic acceptance means eligible for human review, not semantically verified.','','## Automatic results','']
    for model,stats in summary.items():
        lines += [f'### {model}','',json.dumps(stats,ensure_ascii=False,indent=2),'']
    lines+=['## Human review','','Reviewer:','Decision:','Notes:','','Exact original evidence does not prove that a generated reason or direction is entailed by it. Review every retained claim before using it as a consensus input.','']
    for row in results:
        case=next(c for c in cases if c['comment_id']==row['comment_id']);lines += [f"## {row['model']} / {row['comment_id']}",'',f"Case kind: {case['kind']}; category: {case['category']}",'',f"Source: {case.get('source_url')}",'','Original text:','']+['> '+x for x in case['text'].splitlines()]+['','Raw response:','','```text',row.get('response',{}).get('response',row.get('error','')),'```','',f"Automatic checks: {json.dumps(row.get('checks',{}),ensure_ascii=False)}",'',f"Provisional checks: {json.dumps(row.get('semantic_checks',{}),ensure_ascii=False)}",'','Reviewer:','Reason supported:','Direction correct:','Notes:','']
    (folder/'review.md').write_text('\n'.join(lines)+'\n')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--dataset',type=Path,default=ROOT/'data/raw/feedback/20261015-expanded/screened/records.jsonl');parser.add_argument('--models',nargs='+',default=['qwen2.5:7b','llama3.1:latest']);parser.add_argument('--output',type=Path);parser.add_argument('--resume',type=Path);args=parser.parse_args()
    folder=args.resume or args.output or ROOT/'runs'/('grounded-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    tags=local_request('/api/tags');digests={m['name']:m['digest'] for m in tags['models']}
    if any(model not in digests for model in args.models):
        raise ValueError('Requested installed model is missing; no model downloads are attempted')
    if args.resume:
        metadata=json.loads((folder/'metadata.json').read_text());cases=json.loads((folder/'cases.json').read_text());template=(folder/'prompt.txt').read_text()
        if args.models!=metadata['models'] or any(digests[m]!=metadata['model_digests'][m] for m in args.models):
            raise ValueError('Model selection/digest differs from frozen run')
        if sha(template.encode())!=metadata['prompt_sha256'] or sha((folder/'cases.json').read_bytes())!=metadata['cases_sha256']:
            raise ValueError('Frozen prompt or cases changed')
    else:
        folder.mkdir(parents=True,exist_ok=False);cases=prepare_cases(args.dataset);template=(ROOT/'src/aimediator/assets/prompts/extract-grounded-feedback.txt').read_text();save_json(folder/'cases.json',cases);(folder/'prompt.txt').write_text(template);(folder/'runner.py').write_text(Path(__file__).read_text())
        metadata={'started_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'models':args.models,'model_digests':{m:digests[m] for m in args.models},'ollama_version':local_request('/api/version'),'dataset_path':str(args.dataset),'dataset_sha256':sha(args.dataset.read_bytes()),'cases_sha256':sha((folder/'cases.json').read_bytes()),'prompt_sha256':sha(template.encode()),'options':{'temperature':0,'seed':42,'num_ctx':4096,'num_predict':520,'num_gpu':0,'num_thread':min(8,os.cpu_count() or 4)},'generation_mode':'local structured JSON schema plus evidence references','case_count':len(cases),'real_reviews':10,'empty_controls':2,'selection':'Purposive initial diagnostics, not random or held-out; expectations are not included in the model request.','hardware_note':'CPU explicitly selected after earlier GPU backend failures; no speed comparison claimed.'};save_json(folder/'metadata.json',metadata)
    results=[]
    for model in args.models:
        for case in cases:
            filename=model.replace(':','-').replace('/','-')+'-'+case['comment_id'].replace(':','-')+'.json';path=folder/filename
            if args.resume and path.exists():
                previous=json.loads(path.read_text())
                if previous.get('response',{}).get('done') is True:
                    results.append(previous);continue
                archive=folder/'interrupted-attempts';archive.mkdir(exist_ok=True);path.rename(archive/(str(time.time_ns())+'-'+filename))
            schema=schema_for(case);payload={'model':model,'prompt':render_prompt(template,case,schema),'format':schema,'stream':False,'options':metadata['options'],'keep_alive':'2m'};record={'model':model,'comment_id':case['comment_id'],'kind':case['kind'],'request':payload,'started_at_utc':dt.datetime.now(dt.timezone.utc).isoformat()};save_json(path,record);start=time.monotonic()
            try:
                response=local_request('/api/generate',payload);record['response']=response;record['checks'],record['parsed_output'],record['validated_output']=validate(response.get('response',''),case,response.get('done') is True and response.get('done_reason')!='length');record['semantic_checks']=semantic_checks(record['parsed_output'],case)
            except Exception as error:
                record['error']=type(error).__name__+': '+str(error);record['checks']={}
            record['wall_seconds']=round(time.monotonic()-start,3);save_json(path,record);results.append(record);export(folder,results,cases,args.models)
            print(json.dumps({'model':model,'comment_id':case['comment_id'],'seconds':record['wall_seconds'],'checks':record['checks'],'provisional':record.get('semantic_checks')}),flush=True)
        local_request('/api/generate',{'model':model,'keep_alive':0},timeout=30)
    export(folder,results,cases,args.models);print('Saved run: '+str(folder),flush=True)


if __name__=='__main__':
    main()
