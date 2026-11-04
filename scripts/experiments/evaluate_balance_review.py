"""Evaluate recorded predictions against frozen agent silver labels, never gold.

Calibration uses development labels only. Queued is not the same as admitted.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.balance_policy import triage_retrieval
from aimediator.common import sha as digest, strict_json, write as write_json

ROOT = Path(__file__).resolve().parents[2]


def read_labels(folder, source_rows):
    manifest = strict_json((folder / 'manifest.json').read_text(encoding='utf-8'))
    raw = (folder / 'labels.jsonl').read_bytes()
    if digest(raw) != manifest['labels_sha256']:
        raise ValueError('Frozen evaluation labels changed')
    labels = [strict_json(line) for line in raw.decode().splitlines() if line.strip()]
    if len(labels) != manifest['comments'] or len({r['comment_id'] for r in labels}) != len(labels):
        raise ValueError('Duplicate or incomplete evaluation set')
    sources = {r['record_id']: r for r in source_rows}
    for label in labels:
        if digest(sources[label['comment_id']]['text_original'].encode()) != label['source_sha256']:
            raise ValueError('Evaluation source changed')
        if label['reviewer_type'] != 'agent' or label['split'] not in ('development', 'holdout'):
            raise ValueError('Invalid review provenance or split')
    return labels, manifest


def relevance_metrics(labels, predictions):
    counts = Counter(); failures = []
    for label in labels:
        if label['relevance'] == 'uncertain':
            counts['excluded_uncertain'] += 1
            continue
        identity = label['comment_id']
        if identity not in predictions:
            counts['missing_predictions'] += 1
        expected = label['relevance'] == 'related'
        actual = predictions.get(identity) is True
        key = 'true_positive' if expected and actual else 'false_negative' if expected else 'false_positive' if actual else 'true_negative'
        counts[key] += 1
        if expected != actual: failures.append({'comment_id': identity, 'expected': expected, 'actual': actual})
    tp, fp, fn, tn = (counts[k] for k in ('true_positive', 'false_positive', 'false_negative', 'true_negative'))
    return {**{k: counts[k] for k in ('true_positive','false_positive','false_negative','true_negative','excluded_uncertain','missing_predictions')},
        'precision': tp/(tp+fp) if tp+fp else None, 'recall': tp/(tp+fn) if tp+fn else None,
        'specificity': tn/(tn+fp) if tn+fp else None,
        'evaluated': tp+fp+fn+tn, 'errors': failures}


def calibrate(labels, retrieved, sources):
    development = [r for r in labels if r['split'] == 'development']
    by_id = {r['comment_id']: r for r in retrieved}; text = {r['record_id']:r['text_original'] for r in sources}
    options = []
    for margin in (0.0,0.01,0.02,0.03,0.04,0.06,0.08,0.12):
        statuses = {l['comment_id']: triage_retrieval(by_id[l['comment_id']], text[l['comment_id']], margin)[0] for l in development}
        m = relevance_metrics(development, {key:value!='unrelated' for key,value in statuses.items()})
        options.append({'margin':margin,'nominated_recall':m['recall'],
                        'queued':sum(s=='review_queue' for s in statuses.values()),'nomination_metrics':m})
    feasible = [r for r in options if (r['nominated_recall'] or 0)>=0.95]
    selected = min(feasible,key=lambda r:(r['queued'],r['margin'])) if feasible else max(options,key=lambda r:((r['nominated_recall'] or 0),-r['queued'],-r['margin']))
    return {'calibration_split':'development','holdout_used':False,'development_comment_ids':[r['comment_id'] for r in development],
        'objective':'At least 0.95 development related-source nomination recall, then minimize review queue. Nomination is not admission.',
        'selected_margin':selected['margin'],'objective_met':bool(feasible),'candidates':options}


def evaluate(labels, baseline, candidate, candidate_margin, retrieval, sources):
    text={r['record_id']:r['text_original'] for r in sources}
    nominated={r['comment_id']:triage_retrieval(r,text[r['comment_id']],candidate_margin)[0]!='unrelated' for r in retrieval}
    output={}
    for split in ('development','holdout'):
        group=[l for l in labels if l['split']==split]
        output[split]={'baseline_agreement':relevance_metrics(group,{r['comment_id']:r['agreement'] for r in baseline}),
            'candidate_nomination_only':relevance_metrics(group,nominated),
            'candidate_final_agreement':relevance_metrics(group,{r['comment_id']:r['agreement'] for r in candidate}) if candidate is not None else None}
    return output


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--labels',type=Path,default=ROOT/'data/evaluation/balance-silver-v1')
    p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--candidate',type=Path)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();sources=strict_json((args.baseline/'source-snapshot.json').read_text(encoding='utf-8'))
    labels,manifest=read_labels(args.labels,sources);retrieval=strict_json((args.baseline/'retrieval.json').read_text(encoding='utf-8'))
    fit=calibrate(labels,retrieval,sources);write_json(args.out/'calibration.json',fit)
    baseline=strict_json((args.baseline/'relevance.json').read_text(encoding='utf-8'))
    candidate=strict_json((args.candidate/'relevance.json').read_text(encoding='utf-8')) if args.candidate else None
    if args.candidate:
        candidate_manifest=strict_json((args.candidate/'manifest.json').read_text(encoding='utf-8'))
        if candidate_manifest['identity']['dataset_sha256']!=manifest['source_dataset_sha256']:
            raise ValueError('Candidate source dataset differs from frozen evaluation sources')
        read_labels(args.labels,strict_json((args.candidate/'source-snapshot.json').read_text(encoding='utf-8')))
        policy=strict_json((args.candidate/'review-policy-snapshot.json').read_text(encoding='utf-8'))
        if policy['retrieval_borderline_margin']!=fit['selected_margin']:raise ValueError('Candidate did not use development-calibrated margin')
    result={'reviewer_type':'agent','independent_human_gold':False,'label_manifest':manifest,
        'selection_warning':manifest['selection'],'metrics':evaluate(labels,baseline,candidate,fit['selected_margin'],retrieval,sources),
        'limitations':['Same-agent silver review is correlated with previous debugging; this is not independent model accuracy.',
        'Only eight confidently unrelated labels and a stratified sample; precision/prevalence estimates do not generalize.',
        'Nomination recall includes pending review and must never be reported as final admission recall.']}
    write_json(args.out/'evaluation.json',result)
    print(json.dumps({'selected_margin':fit['selected_margin'],'calibration_objective_met':fit['objective_met'],'metrics':result['metrics']},indent=2))


if __name__=='__main__':main()
