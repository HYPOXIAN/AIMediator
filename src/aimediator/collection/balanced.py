"""Collect fresh feedback using existing sources, then freeze a balanced coarse set."""
import argparse
from collections import Counter
from copy import deepcopy
import fcntl
import hashlib
import json
from pathlib import Path

from ..common import write as write_json
from . import screening as s
from .client import Client, Halt, load_youtube_key, utc_now
from .export import export
from .sources import ROOT, STATE, bluesky, steam, youtube
from .store import Store


def reviewed_rows(rows, reviews=None):
    for row in rows:
        review = (reviews or {}).get(row['record_id'])
        if review:
            if hashlib.sha256(row['text_original'].encode()).hexdigest() != review['text_sha256']:
                raise ValueError('Stale source review: ' + row['record_id'])
            if review.get('exclude'):
                continue
            if review.get('language'):
                row = {**row, 'language': review['language'], 'language_review': review}
        yield row


def retained(rows, reviews=None):
    """No inherited ID-specific overrides: new/edited evidence needs fresh review."""
    return [r for r in reviewed_rows(rows, reviews) if r['language'] in ('en', 'zh') and s.classify(r)[0] == 'keep']


def select_balanced(rows, per_language, reviews=None):
    selected = []
    seen_text = set()
    counts = Counter()
    # Latest first within each language; sampling never depends on model outputs.
    for row in sorted(retained(rows, reviews), key=lambda r: (r.get('created_at_utc') or '', r['record_id']), reverse=True):
        text_key = ' '.join(row['text_original'].split()).casefold()
        if text_key in seen_text or counts[row['language']] >= per_language:
            continue
        seen_text.add(text_key)
        counts[row['language']] += 1
        decision, reason, signals, method = s.classify(row)
        selected.append({**row, 'coarse_screening': {'version': 'coarse-v1',
            'decision': decision, 'reason': reason, 'signals': signals, 'method': method,
            'text_sha256': hashlib.sha256(row['text_original'].encode()).hexdigest(),
            'human_review': 'pending'}})
    return selected, counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT/'configs/feedback-collection-balanced.json')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--per-language', type=int, default=300)
    parser.add_argument('--env-file', type=Path, default=ROOT/'.env')
    parser.add_argument('--review-decisions', type=Path)
    parser.add_argument('--screen-only', action='store_true', help='Reselect from saved raw evidence without network requests')
    args = parser.parse_args(argv)
    if not 250 <= args.per_language <= 350:
        parser.error('Choose 250..350 per language (500..700 total)')
    STATE.mkdir(parents=True, exist_ok=True)
    lock = (STATE/'feedback-collector.lock').open('a', encoding='utf-8')
    try:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error('Another collector is running in this project')
        config = json.loads(args.config.read_text(encoding='utf-8'))
        config['screening_keep_goals'] = {'en': args.per_language, 'zh': args.per_language}
        reviews = {r['record_id']: r for r in json.loads(args.review_decisions.read_text(encoding='utf-8'))['entries']} if args.review_decisions else {}
        store = Store(args.out, config)
        client = Client(STATE/'feedback-http-state.json')
        statuses = json.loads((args.out/'summary.json').read_text(encoding='utf-8'))['statuses'] if args.screen_only else {}
        # Existing source settings, official endpoints, intervals, quota and cooldown.
        for platform, function in ([] if args.screen_only else [('steam', steam), ('bluesky', bluesky), ('youtube', youtube)]):
            settings = deepcopy(config[platform])
            if not settings['enabled']:
                statuses[platform] = 'disabled_in_config'
                continue
            if platform == 'youtube':
                load_youtube_key(args.env_file)
                settings['quota_used'] = store.state.get('youtube_quota_used', 0)
            try:
                function(client, store, settings)
                statuses[platform] = 'initial_pass_completed'
            except Halt as exc:
                statuses[platform] = str(exc)
            finally:
                store.save()
                write_json(store.directory/'source-status.json', statuses)
        # Extend recent Steam streams page by page until coarse-retained goals hold.
        settings = deepcopy(config['steam'])
        try:
            for lang in (() if args.screen_only else ('en', 'zh')):
                while select_balanced(store.rows, args.per_language, reviews)[1][lang] < args.per_language:
                    previous = store.count('steam', lang)
                    cap = config['adaptive_raw_caps'][lang]
                    if previous >= cap:
                        raise Halt('Adaptive raw safety cap reached for ' + lang)
                    if store.state['streams'].get('steam:'+lang, {}).get('done'):
                        raise Halt('Recent Steam stream exhausted for ' + lang)
                    steam(client, store, {**settings, 'targets': {lang: min(previous+100, cap)}})
                    if store.count('steam', lang) == previous:
                        raise Halt('Steam added no new records for ' + lang)
                    print(json.dumps({'raw': len(store.rows), 'coarse_counts': dict(select_balanced(store.rows, args.per_language, reviews)[1]), 'requests': dict(client.calls)}), flush=True)
            statuses['steam'] = 'balanced_screening_goals_reached'
        except Halt as exc:
            statuses['steam'] = str(exc)
        finally:
            store.save()
            export(store, statuses, client)
        selected, counts = select_balanced(store.rows, args.per_language, reviews)
        folder = args.out/'screened'
        folder.mkdir(exist_ok=True)
        s.write_rows(folder/'records.jsonl', selected)
        for lang, name in [('en', 'english'), ('zh', 'chinese')]:
            s.write_rows(folder/(name+'.jsonl'), [r for r in selected if r['language'] == lang])
        decisions = []
        selected_ids = {r['record_id'] for r in selected}
        for row in store.rows:
            decision, reason, signals, method = s.classify(row)
            review = reviews.get(row['record_id'])
            if review and review.get('exclude'):
                decision, reason, method = 'exclude', review['reason'], 'agent_source_review'
            decisions.append({'record_id': row['record_id'], 'language': row['language'],
                'decision': decision, 'reason': reason, 'signals': signals, 'method': method,
                'selected': row['record_id'] in selected_ids,
                'text_sha256': hashlib.sha256(row['text_original'].encode()).hexdigest(), 'source_review': review})
        s.write_rows(folder/'decisions.jsonl', decisions)
        s.write_rows(folder/'needs-review.jsonl', [r for r in store.rows if s.classify(r)[0] == 'review'])
        excluded_ids = {d['record_id'] for d in decisions if d['decision'] == 'exclude'}
        s.write_rows(folder/'excluded.jsonl', [r for r in store.rows if r['record_id'] in excluded_ids])
        s.write_rows(folder/'retained-reserve.jsonl', [r for r in retained(store.rows, reviews) if r['record_id'] not in selected_ids])
        summary = {'created_at_utc': utc_now(), 'raw_records': len(store.rows),
            'coarse_decisions': dict(Counter(d['decision'] for d in decisions)),
            'selected': len(selected), 'selected_by_language': dict(counts),
            'selected_by_platform': dict(Counter(r['platform'] for r in selected)),
            'targets_reached': all(counts[l] == args.per_language for l in ('en', 'zh')),
            'selection': 'Latest created_at within language; exact whitespace/case-normalized text deduplication; fixed equal language quotas; no model outcomes used.',
            'new_collection_no_seed': True, 'source_statuses': statuses,
            'created_at_range': {l: {'min': min((r.get('created_at_utc') or '') for r in selected if r['language']==l), 'max': max((r.get('created_at_utc') or '') for r in selected if r['language']==l)} for l in counts},
            'dataset_sha256': hashlib.sha256((folder/'records.jsonl').read_bytes()).hexdigest(),
            'review_decisions_sha256': hashlib.sha256(args.review_decisions.read_bytes()).hexdigest() if args.review_decisions else None,
            'source_reviews': list(reviews.values()),
            'limitations': ['Latest accessible stream, not all posts published today.', 'Platform/script language labels are provisional.', 'Patch applicability and semantic accuracy unverified.', 'Steam reviews and YouTube top-level comments are the configured source types; nested replies are not collected.']}
        write_json(folder/'summary.json', summary)
        print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
        return 0 if summary['targets_reached'] else 2
    finally:
        lock.close()
