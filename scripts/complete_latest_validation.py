"""Complete the final sequential diagnostics and render this experiment report."""
import json
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'reports/latest-balanced-20261027'
while not (folder/'validation-jobs-completed.json').exists():
    time.sleep(10)
for name,script,extra in [
    ('semantic-controls','test_balance_semantic_controls.py',[]),
    ('generation-recovery','recover_latest_failures.py',['--run',str(folder/'full-pipeline')]),
]:
    print('Running '+name,flush=True)
    with (folder/(name+'.log')).open('a') as log:
        subprocess.run([sys.executable,str(ROOT/'scripts'/script),'--out',str(folder/name),*extra],stdout=log,stderr=subprocess.STDOUT,check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/render_latest_validation_report.py')],check=True)
result={'steps_executed':True,'completed_at_local':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),
        'report':str(folder/'evaluation.md'),'note':'Experimental steps finished; test failures and uncertainty remain explicitly recorded in the report.'}
(folder/'all-validation-completed.json').write_text(json.dumps(result,indent=2)+'\n')
state=json.loads((folder/'work-state.json').read_text());state['status']='validation_steps_finished_pending_final_review';state['remaining']=['Inspect final test, recovery and quality results; verify evaluation.md; open report and deliver the Chinese final.']
(folder/'work-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
print('Final diagnostics and report finished',flush=True)
