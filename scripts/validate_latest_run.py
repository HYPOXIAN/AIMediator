"""Audit dataset/run accounting without inventing semantic reference labels."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

import run_balance_analysis as m


def audit(data_folder, run_folder):
    dataset = data_folder/'screened/records.jsonl'
    rows = [json.loads(x) for x in dataset.read_text().splitlines() if x.strip()]
    raw = {r['record_id']:r for r in map(json.loads, (data_folder/'records.jsonl').read_text().splitlines())}
    expected = {r['record_id']:r for r in rows}
    checks = {}
    checks['six_hundred_comments'] = len(rows) == 600
    checks['equal_languages'] = Counter(r['language'] for r in rows) == {'en':300,'zh':300}
    checks['unique_ids'] = len(expected) == len(rows)
    checks['unique_normalized_text'] = len({' '.join(r['text_original'].split()).casefold() for r in rows}) == len(rows)
    checks['original_text_preserved'] = all(raw[r['record_id']]['text_original'] == r['text_original'] for r in rows)
    checks['all_coarse_kept'] = all(r['coarse_screening']['decision'] == 'keep' for r in rows)
    manifest = json.loads((run_folder/'manifest.json').read_text())
    checks['dataset_matches_run_manifest'] = manifest['identity']['dataset_sha256'] == hashlib.sha256(dataset.read_bytes()).hexdigest()
    snapshot = json.loads((run_folder/'source-snapshot.json').read_text())
    checks['exact_source_snapshot'] = snapshot == rows
    summary_path = run_folder/'summary.json'
    if not summary_path.exists():
        return {'complete':False,'checks':checks,'all_checks_pass':all(checks.values()),'reason':'Full inference is still running; no completion or semantic accuracy claimed.'}
    summary = json.loads(summary_path.read_text())
    report = json.loads((run_folder/'balance-report.json').read_text())
    coverage = json.loads((run_folder/'full-pipeline-coverage.json').read_text())
    relevance = json.loads((run_folder/'relevance.json').read_text())
    accepted = json.loads((run_folder/'validated-claims.json').read_text())
    quarantine = json.loads((run_folder/'quarantined-claims.json').read_text())
    admitted = {d['comment_id'] for d in relevance if d['agreement']}
    assessed = {c['comment_id'] for c in report['coverage']}
    checks['all_input_coverage'] = len(coverage) == len(rows) and {c['comment_id'] for c in coverage} == set(expected)
    checks['every_admitted_comment_accounted_for'] = admitted == assessed
    checks['accepted_claim_count'] = summary['accepted_claims'] == len(accepted)
    checks['quarantine_count'] = summary['quarantined_claims'] == len(quarantine)
    checks['claim_accounting'] = summary['generated_claims'] == len(accepted)+len(quarantine)
    checks['accepted_sources_admitted'] = all(c['comment_id'] in admitted for c in accepted)
    checks['accepted_semantic_audit'] = all(c['semantic_audit']['supported'] is True for c in accepted)
    checks['exact_accepted_quotes'] = all(e['comment_id'] == c['comment_id'] and e['text'] == expected[c['comment_id']]['text_original'][e['start']:e['end']] for c in accepted for e in c['evidence'])
    checks['accepted_deterministic_checks'] = all(not m.ground_claim(c, expected[c['comment_id']], {x['canonical_name'] for x in m.character_reference()})[0] for c in accepted)
    checks['unverified_names_isolated'] = all(c.get('character_identity',{}).get('normalization_status') != 'source_literal_unverified' for group in report['character_adjustments'] for c in group['recommendations'])
    checks['unique_source_counts_per_group'] = all(g['supporting_comment_count'] == len(set(g['comment_ids'])) for g in report['character_adjustments'])
    statuses = Counter(c['status'] for c in coverage)
    checks['no_extraction_pending'] = not statuses['extraction_pending']
    return {'complete':True, 'checks':checks,'all_checks_pass':all(checks.values()),
        'input_comments':len(rows),'input_languages':dict(Counter(r['language'] for r in rows)),
        'coverage_statuses':dict(statuses),'summary':summary,
        'evidence_quality_mode':report['evidence_quality_mode'],
        'limitations':['Completion includes explicit failures and unresolved relevance, reported separately.',
            'No independent semantic ground truth or population-representative accuracy is inferred.',
            'The default full pipeline uses evidence-quality=off; shadow/enforce were covered by offline regression, not by 600 fresh quality annotations.']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',type=Path,required=True)
    p.add_argument('--run',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    result=audit(args.data,args.run)
    m.write_json(args.out,result)
    print(json.dumps({k:v for k,v in result.items() if k!='summary'},indent=2))
    return 0 if result['complete'] and result['all_checks_pass'] else 2


if __name__=='__main__':
    sys.exit(main())
