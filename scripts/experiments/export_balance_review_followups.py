"""Make unresolved relevance disagreements and source-only identities reviewable.

This export never overrides agreement or sends unresolved comments to extraction.
"""
import argparse
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.balance_policy import attributed_candidates, load_policy, term_matches
from aimediator.common import sha as digest, strict_json, write as write_json
from aimediator.evidence import character_candidates, character_reference, character_terms


def followups(decisions,sources):
    by_id={r['record_id']:r for r in sources}
    rows=[]
    attribution=[]
    for decision in decisions:
        identity=decision['comment_id']
        source=by_id[identity]
        reasons=[]
        scope=[]
        reference=character_reference(source['text_original'])
        candidates=character_candidates(source['text_original'],reference)
        retained,excluded=attributed_candidates(source['text_original'],reference,candidates)
        if excluded:
            attribution.append({'comment_id':identity,'excluded_characters':excluded,
                'retained_candidates':retained,'source_sha256':digest(source['text_original'].encode()),
                'original_text':source['text_original']})
        if not decision['agreement'] and (decision.get('retrieval_related') is True or decision.get('retrieval_triage')=='review_queue'):
            scope.append('relevance')
            reasons.append('retrieval_model_disagreement' if decision.get('retrieval_related') else 'queued_retrieval_not_confirmed')
        names=[]
        if decision['agreement']:
            for entry in load_policy()['source_literal_characters']:
                for term in character_terms(entry):
                    if term_matches(term,source['text_original']):
                        names.append(term)
            if names:
                scope.append('identity')
                reasons.append('source_literal_official_identity_unverified')
        if scope:
            rows.append({'comment_id':identity,'review_scope':scope,'reasons':reasons,
                'admitted_for_extraction':decision['agreement'],'decision_changed':False,
                'unverified_source_names':sorted(set(names)),'original_text':source['text_original'],
                'source_url':source.get('source_url'),'relevance_decision':decision})
    return {'decision_overrides':False,'total':len(rows),'scope_counts':dict(Counter(s for r in rows for s in r['review_scope'])),
        'items':rows,'attribution_exclusions':attribution,
        'rule':'A relevance disagreement remains excluded until affirmative retrieval review and model relevance agree. An identity follow-up never proves an official roster mapping.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',type=Path,required=True)
    p.add_argument('--out',type=Path)
    args=p.parse_args()
    result=followups(strict_json((args.run/'relevance.json').read_text(encoding='utf-8')),strict_json((args.run/'source-snapshot.json').read_text(encoding='utf-8')))
    write_json(args.out or args.run/'review-followups.json',result)
    print({'total':result['total'],'scope_counts':result['scope_counts'],
           'attribution_exclusion_count':len(result['attribution_exclusions']),'decision_overrides':False})


if __name__=='__main__':
    main()
