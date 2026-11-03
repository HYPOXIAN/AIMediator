"""Apply fingerprinted agent/human decisions to live regression proposals.

Keeps the raw model results unchanged and never substitutes review for model scores.
"""
import argparse
from pathlib import Path
import sys
sys.path.insert(1, str(Path(__file__).resolve().parents[1]))  # scripts/ holds the registered forwarding shells
from run_balance_analysis import strict_json,write_json,character_reference,aggregate,digest
from review_balance_sources import apply_review
from prepare_balance_design import prepare_briefs


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--live-run',type=Path,required=True)
    p.add_argument('--admission-run',type=Path,required=True);p.add_argument('--decisions',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    raw=strict_json((args.live_run/'results.json').read_text());review=strict_json(args.decisions.read_text())
    if review['reviewer_type'] not in ('agent','human'):raise ValueError('Explicit reviewer provenance required')
    admitted={r['comment_id'] for r in strict_json((args.admission_run/'relevance.json').read_text()) if r['agreement']}
    sources={c['comment_id']:c['source'] for c in raw['cases'] if c.get('source')};proposals={}
    for case in raw['cases']:
        for index,item in enumerate(case.get('claims',[]),1):
            identity=case['comment_id']+':'+str(index)
            proposals[identity]={'comment_id':case['comment_id'],'model':case['model'],'claim':item['claim']}
    accepted,excluded=apply_review(proposals,review['decisions'],sources,admitted,{e['canonical_name'] for e in character_reference()})
    output={'reviewer_type':review['reviewer_type'],'kind':'separate_source_review_not_model_accuracy',
        'raw_model_report_sha256':digest((args.live_run/'results.json').read_bytes()),'complete_proposals_reviewed':len(proposals),
        'accepted':len(accepted),'excluded':len(excluded),'character_adjustments':aggregate(accepted),
        'unresolved_identity_claims':[c for c in accepted if c.get('character_identity',{}).get('normalization_status')=='source_literal_unverified'],
        'exclusions':excluded,'release_status':'requires_official_identity_patch_data_and_engineering_validation'}
    write_json(args.out/'source-reviewed-report.json',output);write_json(args.out/'source-reviewed-claims.json',accepted)
    write_json(args.out/'design-briefs.json',prepare_briefs(accepted))
    print({k:output[k] for k in ('reviewer_type','complete_proposals_reviewed','accepted','excluded')})


if __name__=='__main__':main()
