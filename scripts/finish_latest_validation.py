"""Finish this bounded local validation after the full corpus report is written."""
import argparse
from pathlib import Path
import json
import subprocess
import sys
import time

import run_balance_analysis as m
from validate_latest_run import audit


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=m.ROOT/'reports/latest-balanced-20261027')
    p.add_argument('--data',type=Path,default=m.ROOT/'data/raw/feedback/20261027-latest-balanced')
    args=p.parse_args();folder=args.root.resolve();run=folder/'full-pipeline'
    while not (run/'balance-report.json').exists():
        time.sleep(10)
    checked=audit(args.data,run)
    m.write_json(folder/'integrity-checks.json',checked)
    if not checked['complete'] or not checked['all_checks_pass']:
        raise ValueError('Full-corpus integrity checks failed; inspect integrity-checks.json')
    tasks=[
        ('numeric-controls-final','test_balance_controls.py',[]),
        ('numeric-extraction-final','test_balance_numeric_extraction.py',[]),
        ('final-regressions','run_balance_regression_live.py',['--admission-run',str(m.ROOT/'reports/balance-review-v2/relevance')]),
        ('baseline-matched-regressions','run_balance_regression_live.py',['--admission-run',str(m.ROOT/'reports/balance-review-v2/relevance'),'--prompt-dir',str(folder/'prompt-baseline')]),
    ]
    for name,script,extra in tasks:
        print('Running '+name,flush=True)
        with (folder/(name+'.log')).open('a') as log:
            subprocess.run([sys.executable,str(m.ROOT/'scripts'/script),'--num-gpu','99','--out',str(folder/name),*extra],stdout=log,stderr=subprocess.STDOUT,check=True)
    rows=json.loads((run/'source-snapshot.json').read_text())
    selected_ids={'steam:233430759','steam:225016184','steam:232744105','steam:238468626'}
    subset=[r for r in rows if r['record_id'] in selected_ids]
    if len(subset)!=4:
        raise ValueError('Expected diagnostic sources are absent')
    path=folder/'quality-live-sources.jsonl'
    path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in subset))
    print('Running four-source live enforce diagnostic',flush=True)
    with (folder/'quality-live-enforce.log').open('a') as log:
        subprocess.run([sys.executable,str(m.ROOT/'scripts/run_balance_analysis.py'),'--dataset',str(path),
            '--embedding-provider','configured','--num-gpu','99','--evidence-quality','enforce','--out',str(folder/'quality-live-enforce')],stdout=log,stderr=subprocess.STDOUT,check=True)
    m.write_json(folder/'validation-jobs-completed.json',{'completed_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
        'full_corpus':600,'quality_live_diagnostic':4,'control_runs':[t[0] for t in tasks],
        'note':'Job completion is not a claim that every semantic control passed; read each results.json.'})
    print('All bounded validation jobs finished',flush=True)


if __name__=='__main__':
    main()
