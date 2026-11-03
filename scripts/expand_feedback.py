import argparse
import collections
import copy
import fcntl
import hashlib
import json
from pathlib import Path
import time

import collect_feedback as collector
import screen_feedback as screener

ROOT=Path(__file__).resolve().parents[1]


def kept_counts(store, overrides):
    counts=collections.Counter()
    for row in store.rows:
        if screener.classify(row,overrides)[0]=='keep':
            counts[row['language']]+=1
    return counts


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base',type=Path,default=ROOT/'data/raw/feedback/20261015-initial')
    parser.add_argument('--output',type=Path,default=ROOT/'data/raw/feedback/20261015-expanded')
    parser.add_argument('--english',type=int,default=220)
    parser.add_argument('--chinese',type=int,default=120)
    args=parser.parse_args()
    if args.base.resolve()==args.output.resolve():
        parser.error('Expansion must use a separate directory')
    lock=(ROOT/'data/raw/feedback-collector.lock').open('a')
    try:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        parser.error('Another collector is running')
    config=json.loads((ROOT/'configs/feedback-collection.json').read_text())
    config['steam']['targets']={'en':3000,'zh':1500}
    config['steam']['max_requests']=35
    config['screening_keep_goals']={'en':args.english,'zh':args.chinese}
    config['expansion_base']=str(args.base)
    config['bluesky']['enabled']=False
    config['youtube']['enabled']=False
    store=collector.Store(args.output,config)
    if not store.rows:
        store.rows=[json.loads(line) for line in (args.base/'records.jsonl').read_text().splitlines()]
        store.ids={row['record_id'] for row in store.rows}
        base_state=json.loads((args.base/'checkpoint.json').read_text())
        store.state['streams']=copy.deepcopy(base_state['streams'])
        store.state['base_source_sha256']=hashlib.sha256((args.base/'records.jsonl').read_bytes()).hexdigest()
        store.state['seed_record_count']=len(store.rows)
        store.save()
    overrides={r['record_id']:r for r in json.loads((ROOT/'configs/feedback-screening-overrides.json').read_text())['entries']}
    client=collector.Client(ROOT/'data/raw/feedback-http-state.json')
    settings=config['steam']
    statuses={'steam':'not_started','youtube':'inherited_from_base; no new request','bluesky':'previous_access_denied; no request'}
    try:
        for lang,goal in config['screening_keep_goals'].items():
            while kept_counts(store,overrides)[lang]<goal:
                previous_raw=store.count('steam',lang)
                if previous_raw>=settings['targets'][lang]:
                    raise collector.Halt('Raw-language safety cap reached')
                stream=store.state['streams'].get('steam:'+lang,{})
                if stream.get('done'):
                    raise collector.Halt('Steam language stream exhausted or made no progress')
                one_page_settings={**settings,'targets':{lang:min(previous_raw+100,settings['targets'][lang])}}
                collector.steam(client,store,one_page_settings)
                if store.count('steam',lang)==previous_raw:
                    raise collector.Halt('Steam did not add new records')
                counts=kept_counts(store,overrides)
                print(json.dumps({'screened_kept_so_far':dict(counts),'raw_total':len(store.rows),'requests':dict(client.calls)}),flush=True)
            statuses['steam']='screened_goals_reached'
    except collector.Halt as error:
        statuses['steam']=str(error)
        print('Expansion stopped: '+str(error),flush=True)
    except KeyboardInterrupt:
        statuses['steam']='interrupted; resume the same expansion directory'
    finally:
        store.save()
        collector.export(store,statuses,client)
        counts=kept_counts(store,overrides)
        report={'base':str(args.base),'output':str(args.output),'screening_version':'coarse-v1','goals':config['screening_keep_goals'],'screened_keep_counts':dict(counts),'targets_reached':all(counts[lang]>=goal for lang,goal in config['screening_keep_goals'].items()),'raw_total':len(store.rows),'seed_record_count':store.state['seed_record_count'],'new_records':len(store.rows)-store.state['seed_record_count'],'requests_this_invocation':dict(client.calls),'statuses':statuses}
        collector.write_json(args.output/'expansion.json',report)
    return 0 if report['targets_reached'] else 2


if __name__=='__main__':
    raise SystemExit(main())
