"""Prepare a new annotation set or score explicitly aligned quality predictions.

No labels are inferred from predictions. Point alignment is adjudicated separately
because semantic equivalence/deduplication cannot be proven by span arithmetic.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re

from . import evidence_quality as q
from .common import sha as digest, strict_json, write as write_json


def proportion(numerator, denominator):
    if not denominator:
        return {'numerator': numerator, 'denominator': denominator, 'value': None, 'wilson95': None}
    p=numerator/denominator
    z=1.959963984540054
    center=(p+z*z/(2*denominator))/(1+z*z/denominator)
    half=z*math.sqrt(p*(1-p)/denominator+z*z/(4*denominator**2))/(1+z*z/denominator)
    return {'numerator': numerator, 'denominator': denominator, 'value': p,
            'wilson95': [max(0,center-half),min(1,center+half)]}


def prepare_dataset(rows, source_stage, out, limit=300, inspected_ids=()):
    if out.exists():
        raise ValueError('Annotation output must be a new directory')
    if len({r['record_id'] for r in rows}) != len(rows):
        raise ValueError('Duplicate source IDs')
    inspected=set(inspected_ids)
    clusters=defaultdict(list)
    for row in rows:
        normalized=re.sub(r'\W+','',row['text_original'].casefold())
        # This groups exact normalized duplicates, not semantic paraphrases.
        clusters[digest(normalized.encode())].append(row)
    ordered=sorted(clusters, key=lambda c:digest(('quality-v1:'+c).encode()))
    selected=[]
    for cluster in ordered:
        group=clusters[cluster]
        dev=any(r['record_id'] in inspected for r in group)
        split='development' if dev or int(cluster[:8],16)%10<7 else 'test'
        for row in group:
            selected.append({'comment_id': row['record_id'], 'language': row['language'],
                'text_original': row['text_original'], 'source_url': row.get('source_url'),
                'content_sha256': digest(row['text_original'].encode()), 'source_stage': source_stage,
                'cluster_id': cluster, 'split': split, 'reviewer_type': 'unlabeled',
                'relevance': None, 'segments': None, 'points': None, 'point_matches': None,
                'equivalence_group': None, 'reviewer_a': None, 'reviewer_b': None,
                'adjudication': None, 'notes': 'Merge paraphrase clusters before freezing splits.'})
        if len(selected)>=limit:
            break
    out.mkdir(parents=True)
    write_json(out/'annotation-template.json',selected)
    write_json(out/'manifest.json',{'version':'evidence-quality-evaluation-v1',
        'status':'unlabeled_not_ground_truth','sample_count':len(selected),'requested_count':limit,
        'input_comments':len(rows),'source_stage':source_stage,
        'input_sha256':digest(json.dumps(rows,sort_keys=True,ensure_ascii=False).encode()),
        'independent_human_gold':False,'inspected_ids':sorted(inspected),
        'split_rule':'Normalized duplicate clusters; inspected sources forced development. Manually merge semantic variants before freezing.',
        'source_sampling':'Deterministic cluster sample, not population-representative; supply raw_pre_screen input for end-to-end evaluation.'})
    return selected


def score_group(labels, predictions, admission):
    n=Counter()
    span=Counter()
    ratio_errors=[]
    equivalents=defaultdict(list)
    eligible_labels=[]
    for label in labels:
        cid=label['comment_id']
        pred=predictions.get(cid)
        n['total']+=1
        n['missing']+=pred is None
        n['failed']+=pred is not None and pred['status']=='failed'
        n['review']+=pred is not None and 'review' in pred['routes_present']
        if label.get('relevance') in ('related','unrelated') and cid in admission:
            n['admitted']+=admission[cid]
            n['false_accept']+=admission[cid] and label['relevance']=='unrelated'
        if label.get('points') is None or label.get('point_matches') is None:
            continue
        eligible_labels.append(label)
        gold={p['point_id']:p for p in label['points']}
        if len(gold)!=len(label['points']):
            raise ValueError('Duplicate gold point IDs')
        predicted={r['point_id']:r for r in (pred or {}).get('routing',[]) if r.get('point_id')}
        matches=label['point_matches']
        aligned={}
        used=set()
        for match in matches:
            g,p=match['gold_point_id'],match['predicted_point_id']
            if g not in gold or p not in predicted or g in aligned or p in used:
                raise ValueError('Invalid or duplicate adjudicated point alignment: '+cid)
            aligned[g]=p
            used.add(p)
        for gid,g in gold.items():
            route=g['route']
            p=predicted.get(aligned.get(gid))
            actual=p['route'] if p else None
            if not p and pred and g.get('segment_ids') and label.get('segments'):
                gold_spans=[s for s in label['segments'] if s['segment_id'] in g['segment_ids']]
                source_chars={i for s in gold_spans for i in range(s['start'],s['end']) if q.weight(label['text_original'][i])}
                excluded_chars={i for r in pred['routing'] if r['route']=='exclude' for s in r['segments']
                                for i in range(s['start'],s['end'])}
                if source_chars and source_chars<=excluded_chars:
                    actual='exclude'
            if route=='mechanism_evidence':
                n['gold_mechanism']+=1
                n['true_mechanism']+=actual=='mechanism_evidence'
                n['mechanism_excluded']+=actual=='exclude'
                n['mechanism_review_loss']+=actual=='review' or pred is not None and pred['status']=='failed'
            if route=='opinion_only':
                n['gold_general']+=1
                n['general_upgrade']+=actual=='mechanism_evidence'
            if route=='system_evidence':
                n['gold_system']+=1
                n['system_misbind']+=actual in ('mechanism_evidence','opinion_only')
        n['pred_mechanism']+=sum(p['route']=='mechanism_evidence' for p in predicted.values())
        if label.get('equivalence_group'):
            signature=sorted((r['point']['scope'],r['point']['detail_level'],r['point']['direction'],r['route'],1)
                for r in (pred or {}).get('routing',[]) if r.get('point_id'))
            # Failures/missing predictions never count as equivalent success.
            equivalents[label['equivalence_group']].append(signature if pred and pred['status']=='completed' else None)
        if label.get('reviewer_type')=='human' and label.get('segments') is not None:
            text=label['text_original']
            measure={i for i,c in enumerate(text) if q.weight(c)}
            actual={i for s in (pred or {}).get('annotation',{}).get('segments',[]) if s['content_kind']=='pure_emotion'
                    for i in range(s['start'],s['end'])}&measure if pred and pred.get('annotation') else set()
            expected={i for s in label['segments'] if s['content_kind']=='pure_emotion'
                      for i in range(s['start'],s['end'])}&measure
            span['tp']+=len(actual&expected)
            span['pred']+=len(actual)
            span['gold']+=len(expected)
            if measure and pred and pred.get('emotion_ratio') is not None:
                ratio_errors.append(abs(pred['emotion_ratio']-len(expected)/len(measure)))
    n['equivalence_pairs']=sum(len(v)*(len(v)-1)//2 for v in equivalents.values())
    n['consistent_pairs']=sum(a is not None and a==b for v in equivalents.values() for i,a in enumerate(v) for b in v[i+1:])
    return {'comments':n['total'],'point_labeled_comments':len(eligible_labels),'missing_predictions':n['missing'],
        'relevance_false_acceptance':proportion(n['false_accept'],n['admitted']),
        'mechanism_precision':proportion(n['true_mechanism'],n['pred_mechanism']),
        'mechanism_recall':proportion(n['true_mechanism'],n['gold_mechanism']),
        'valid_mechanism_exclusion_rate':proportion(n['mechanism_excluded'],n['gold_mechanism']),
        'mechanism_recall_loss_to_review':proportion(n['mechanism_review_loss'],n['gold_mechanism']),
        'general_opinion_upgrade_rate':proportion(n['general_upgrade'],n['gold_general']),
        'system_character_misbind_rate':proportion(n['system_misbind'],n['gold_system']),
        'review_coverage':proportion(n['review'],n['total']), 'failure_rate':proportion(n['failed'],n['total']),
        'equivalent_qualification_weight_consistency':proportion(n['consistent_pairs'],n['equivalence_pairs']),
        'human_emotion_span_precision':proportion(span['tp'],span['pred']),
        'human_emotion_span_recall':proportion(span['tp'],span['gold']),
        'human_emotion_ratio_mae':sum(ratio_errors)/len(ratio_errors) if ratio_errors else None,
        'human_emotion_ratio_comments':len(ratio_errors)}


def evaluate(labels, records, admission=None):
    if len({r['comment_id'] for r in labels})!=len(labels):
        raise ValueError('Duplicate label IDs')
    if len({r['comment_id'] for r in records})!=len(records):
        raise ValueError('Duplicate prediction IDs')
    predictions={r['comment_id']:r for r in records}
    admission=admission or {}
    cluster_splits=defaultdict(set)
    for label in labels:
        cluster_splits[label['cluster_id']].add(label['split'])
        if label.get('equivalence_group'):
            cluster_splits['equivalent:'+label['equivalence_group']].add(label['split'])
        if label.get('segments') is not None:
            previous=0
            covered=set()
            for span in label['segments']:
                if (type(span.get('start')) is not int or type(span.get('end')) is not int
                        or not previous<=span['start']<span['end']<=len(label['text_original'])
                        or span.get('quote')!=label['text_original'][span['start']:span['end']]):
                    raise ValueError('Invalid gold span binding')
                previous=span['end']
                covered.update(range(span['start'],span['end']))
            if any(not c.isspace() and i not in covered for i,c in enumerate(label['text_original'])):
                raise ValueError('Incomplete gold spans')
        if label.get('points') is not None and any(p.get('route') not in q.ROUTES for p in label['points']):
            raise ValueError('Unknown gold point route')
        if label['content_sha256']!=digest(label['text_original'].encode()):
            raise ValueError('Label source hash mismatch')
        pred=predictions.get(label['comment_id'])
        if pred and pred['content_sha256']!=label['content_sha256']:
            raise ValueError('Prediction source hash mismatch')
    if any(len(v)>1 for v in cluster_splits.values()):
        raise ValueError('Cluster crosses evaluation splits')
    labeled=[l for l in labels if l.get('reviewer_type') in ('human','silver','agent_authored_synthetic')]
    # Do not pool unlike provenance or development/test data as an accuracy claim.
    groups={}
    for provenance in sorted({l['reviewer_type'] for l in labeled}):
        for split in sorted({l['split'] for l in labeled}):
            subset=[l for l in labeled if l['reviewer_type']==provenance and l['split']==split]
            if not subset:
                continue
            groups[provenance+':'+split]={'all':score_group(subset,predictions,admission),
                'by_language':{lang:score_group([l for l in subset if l['language']==lang],predictions,admission)
                               for lang in sorted({l['language'] for l in subset})},
                'by_source_stage':{stage:score_group([l for l in subset if l['source_stage']==stage],predictions,admission)
                                   for stage in sorted({l['source_stage'] for l in subset})},
                'fixed_admission':score_group([l for l in subset if admission.get(l['comment_id'])],predictions,admission)}
    return {'version':'quality-evaluation-v1','labeled_comments':len(labeled),'unlabeled_comments':len(labels)-len(labeled),
        'groups':groups,'independent_effectiveness_established':False,
        'notes':['Human/silver/synthetic and development/test scores remain separate.',
                 'Point matching requires explicit adjudicated one-to-one alignments; unaligned mechanism outputs count against precision.',
                 'Missing predictions are recall losses, review is never successful extraction.',
                 'End-to-end recall requires raw_pre_screen labels and complete upstream admission accounting.',
                 'Wilson intervals treat counted units as binomial trials; within-comment/span dependence limits interpretation.',
                 'No threshold calibration is performed here; use development labels only.']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('prepare')
    a.add_argument('--dataset',type=Path,required=True)
    a.add_argument('--source-stage',choices=['raw_pre_screen','screened','fixed_admission'],required=True)
    a.add_argument('--inspected-labels',type=Path)
    a.add_argument('--limit',type=int,default=300)
    a.add_argument('--out',type=Path,required=True)
    e=sub.add_parser('score')
    e.add_argument('--labels',type=Path,required=True)
    e.add_argument('--run',type=Path,required=True)
    e.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    if args.command=='prepare':
        rows=[strict_json(line) for line in args.dataset.read_text(encoding='utf-8').splitlines() if line.strip()]
        inspected=[strict_json(line)['comment_id'] for line in args.inspected_labels.read_text(encoding='utf-8').splitlines() if line.strip()] if args.inspected_labels else []
        prepare_dataset(rows,args.source_stage,args.out,args.limit,inspected)
    else:
        labels=strict_json(args.labels.read_text(encoding='utf-8'))
        records=strict_json((args.run/'evidence-quality.json').read_text(encoding='utf-8'))
        relevance=args.run/'relevance.json'
        admission={r['comment_id']:r['agreement'] for r in strict_json(relevance.read_text(encoding='utf-8'))} if relevance.exists() else {}
        write_json(args.out,evaluate(labels,records,admission))


if __name__=='__main__':
    main()
