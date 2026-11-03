"""Validate and select the completed current-code corpus rerun."""
from datetime import datetime
from zoneinfo import ZoneInfo
import json
from pathlib import Path
import subprocess
import sys
import time

import run_balance_analysis as m
from validate_latest_run import audit

folder=m.ROOT/'reports/latest-balanced-20261027';run=folder/'full-pipeline-final'
while not (run/'transport-reuse-summary.json').exists():
    time.sleep(10)
checked=audit(m.ROOT/'data/raw/feedback/20261027-latest-balanced',run)
m.write_json(folder/'final-integrity-checks.json',checked)
if not checked['complete'] or not checked['all_checks_pass']:
    raise ValueError('Final current-code corpus checks failed')
old_diagnostics=folder/'new-source-diagnostics.json'
if old_diagnostics.exists() and not (folder/'new-source-diagnostics-before-schema-fix.json').exists():
    (folder/'new-source-diagnostics-before-schema-fix.json').write_bytes(old_diagnostics.read_bytes())
m.write_json(folder/'full-selected-run.json',{'selected':'full-pipeline-final','initial':'full-pipeline',
    'integrity':'final-integrity-checks.json','method':'Current code executes on all 600 inputs; only exactly identical model-visible calls reuse frozen results. Changed calls receive fresh inference.'})
subprocess.run([sys.executable,str(m.ROOT/'scripts/render_latest_validation_report.py')],check=True)
result={'steps_executed':True,'completed_at_local':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),
        'selected_full_run':str(run),'report':str(folder/'evaluation.md'),
        'known_limits':'See final report for generation failures, unresolved relevance and four-case quality development scope. No independent accuracy or global prompt optimality claimed.'}
m.write_json(folder/'all-validation-completed.json',result)
state=json.loads((folder/'work-state.json').read_text());state['status']='experiment_complete_pending_final_read';state['remaining']=['Read final report and actual counts; open the report and deliver the Chinese final.']
m.write_json(folder/'work-state.json',state)
print('Current-code full rerun validated and final report rendered',flush=True)
