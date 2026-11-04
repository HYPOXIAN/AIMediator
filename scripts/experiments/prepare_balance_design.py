"""Separate player evidence from engineering design prerequisites and hypotheses.

No current move data, target values or causal effects are fabricated. Matching
versioned inputs can make a brief ready for an engineer, never release a patch.
"""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.common import sha as digest, strict_json, write as write_json
from aimediator.design_briefs import prepare_briefs
from aimediator.resources import workspace_root

ROOT = workspace_root()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--claims',type=Path,required=True)
    p.add_argument('--quality-mode',choices=['auto','enforce'],default='auto',help='Use enforce for v3 claim lists to reject missing quality metadata')
    p.add_argument('--move-data',type=Path)
    p.add_argument('--target-patch')
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--adjudications',type=Path,default=ROOT/'data/evaluation/balance-silver-v1/errata.json')
    args=p.parse_args()
    claims=strict_json(args.claims.read_text(encoding='utf-8'))
    moves=strict_json(args.move_data.read_text(encoding='utf-8')) if args.move_data else []
    quality_mode = 'enforce' if args.quality_mode == 'enforce' else None
    if isinstance(claims, dict):
        if claims.get('evidence_quality_mode') == 'enforce' or claims.get('report_schema_version') == 'balance-report-v3':
            quality_mode = 'enforce'
        if 'claims' in claims:
            claims = claims['claims']
        else:
            claims = [c for g in claims.get('character_adjustments', []) for c in g['recommendations']]
    pending=[]
    if args.adjudications.exists():
        pending=[r['comment_id'] for r in strict_json(args.adjudications.read_text(encoding='utf-8'))['entries']]
    result=prepare_briefs(claims,moves,args.target_patch,pending,quality_mode)
    result['adjudication_source_sha256']=digest(args.adjudications.read_bytes()) if args.adjudications.exists() else None
    write_json(args.out,result)
    print(json.dumps(result['summary']))


if __name__=='__main__':
    main()
