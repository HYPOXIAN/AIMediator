"""Revalidate every accepted corpus claim after tightening empty numeric options."""
import json
from pathlib import Path
import run_balance_analysis as m

folder=m.ROOT/'reports/latest-balanced-20261027';run=folder/'full-pipeline'
rows={r['record_id']:r for r in m.strict_json((run/'source-snapshot.json').read_text())}
claims=m.strict_json((run/'validated-claims.json').read_text());results=[]
for c in claims:
    row=rows[c['comment_id']];cid=row['record_id']
    data={'comments':[{'comment_id':cid,'units':m.evidence_units(row['text_original'])}],
          'character_normalization_reference':m.character_reference(row['text_original'])}
    payload={k:c[k] for k in m.CLAIM['properties']}
    errors=m.schema_errors({'assessments':{cid:{'claims':[payload]}}},m.schema_for('extract',[cid],data))
    errors+=m.ground_claim(c,row,{e['canonical_name'] for e in m.character_reference()})[0]
    results.append({'claim_id':c['claim_id'],'comment_id':cid,'errors':errors,'passed':not errors})
output={'kind':'accepted_claim_contract_replay_no_new_generation','total':len(results),'passed':sum(r['passed'] for r in results),
        'runner_sha256':m.digest((m.ROOT/'scripts/run_balance_analysis.py').read_bytes()),
        'original_runner_sha256':m.strict_json((run/'manifest.json').read_text())['identity']['script_sha256'],
        'cases':results,'limitation':'This checks compatibility of all previously accepted claims; it is not a fresh full-corpus generation under the tightened decoder schema.'}
m.write_json(folder/'post-fix-accepted-replay.json',output)
print('Accepted claim contract replay:',output['passed'],'/',output['total'])
if output['passed']!=output['total']:raise SystemExit(2)
