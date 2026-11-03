"""Replay reviewed original errors through deterministic gates and frozen audits.

This is regression replay of old proposals, not a fresh model accuracy benchmark.
"""
import argparse
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(1, str(Path(__file__).resolve().parents[1]))  # scripts/ holds the registered forwarding shells
from run_balance_analysis import ROOT,strict_json,write_json,ground_claim,character_reference,digest
from prepare_balance_design import prepare_briefs
from review_balance_sources import proposal_hash, apply_review


def replay(cases, prior_claims):
    characters={e['canonical_name'] for e in character_reference()};results=[]
    for case in cases:
        errors,enriched=ground_claim(case['proposed_claim'],case['source'],characters)
        old=prior_claims.get(case['case_id']);old_support=(old or {}).get('supported')
        brief=prepare_briefs([{**case['proposed_claim'],'claim_id':case['case_id'],
                              'comment_id':case['source']['record_id']}])['briefs'][0]
        results.append({'case_id':case['case_id'],'category':case['category'],
            'expected_supported':False,'source_gate_errors':errors,
            'previous_model_support':old_support,
            'combined_supported':not errors and old_support is True,
            'passed':bool(errors) or old_support is False,
            'engineering_design_blocked':brief['readiness']=='blocked',
            'engineering_blockers':brief['blockers'],
            'review_reason':case['review_reason']})
    return {'kind':'old_proposal_and_audit_replay_not_fresh_generation','total':len(results),
        'blocked_by_source_gate':sum(bool(r['source_gate_errors']) for r in results),
        'still_requires_semantic_review':sum(not r['passed'] for r in results),
        'passed':sum(r['passed'] for r in results),'cases':results}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',type=Path,default=ROOT/'reports/balance-engineering-20261022-final-review')
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();fixture=ROOT/'data/evaluation/balance-regressions-v1/cases.json'
    cases=strict_json(fixture.read_text());audit={r['claim_id']:r.get('audit') for r in strict_json((args.baseline/'audit-progress.json').read_text())}
    output=replay(cases,audit);output['fixtures_sha256']=digest(fixture.read_bytes());write_json(args.out,output)
    reviews=strict_json((args.baseline/'source-review-decisions.json').read_text())
    selected={c['case_id']:reviews['decisions'][c['case_id']] for c in cases}
    proposals={c['case_id']:{'comment_id':c['source']['record_id'],'claim':c['proposed_claim'],'model':'prior-model-fixture'} for c in cases}
    sources={c['source']['record_id']:c['source'] for c in cases}
    admitted={r['comment_id'] for r in strict_json((args.baseline/'relevance.json').read_text()) if r['agreement']}
    accepted,excluded=apply_review(proposals,selected,sources,admitted,{r['canonical_name'] for r in character_reference()})
    unresolved=[c['claim_id'] for c in accepted if not c['source_review']['direction_changed']]
    output['fingerprinted_review_workflow']={'reviewer_type':reviews['reviewer_type'],
        'rejected_or_uncertain':len(excluded),'explicit_direction_corrections':len(accepted)-len(unresolved),
        'unresolved_original_errors':unresolved,'all_known_original_errors_handled':not unresolved,
        'note':'Replays frozen agent review decisions; not new model success or independent human gold.'}
    output['engineering_design_blocked']=sum(r['engineering_design_blocked'] for r in output['cases'])
    write_json(args.out,output)
    print({k:v for k,v in output.items() if k!='cases'})


if __name__=='__main__':main()
