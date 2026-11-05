"""Deterministic offline sample-feedback exports, with escaped source evidence."""
from collections import Counter
import html
from pathlib import Path
import re
from urllib.parse import urlsplit, quote
from . import evidence, evidence_quality
from .common import canonical, new_path, read, sha, write
from .review import glossary_entry, load_run, load_overlay, target_reference


def normalized(text):
    return ' '.join((text or '').split()).casefold()


def escape(value):
    text = html.escape(str(value if value is not None else 'unknown'), quote=True)
    return re.sub(r'([\\`*_{}\[\]()#+.!|>~-])', r'\\\1', text).replace('\r','').replace('\n', '  \n')


def source_link(row, evidence_id=None):
    label = escape(row['record_id'] + (('/' + evidence_id) if evidence_id else ''))
    url = row.get('source_url')
    if isinstance(url, str):
        p = urlsplit(url)
        if p.scheme in ('http','https') and p.hostname and not p.username and not p.password:
            return '[' + label + '](' + quote(url, safe=':/?#=&%') + ')'
    return label


def groups_for(claims, sources):
    """Group formal claims by character and topic (report v2, pipeline upgrade U6.2, UP-D12).

    A target whose glossary reference is resolved groups by (character, glossary ID) across wording and
    language; every other target, candidates included, groups by (character, normalized literal), so
    candidates never merge groups. Each group lists its original literals. The reference is the claim's
    saved one, or recomputed for claims without one (earlier runs, reviewed claims).
    """
    groups, unresolved = {}, []
    for claim in claims:
        identity = claim.get('character_identity') or {}
        if not claim.get('character') or identity.get('normalization_status') != 'glossary_reference' or not claim.get('target'):
            unresolved.append(claim)
            continue
        reference = target_reference(claim)
        if reference['status'] == 'resolved':
            entry = glossary_entry(reference['glossary_ids'][0])
            key = (claim['character'], normalized(entry['canonical_name']), 'glossary', entry['id'])
            topic = {'grouping': 'glossary_id', 'glossary_id': entry['id'],
                     'glossary_entry': {'canonical_name': entry['canonical_name'],
                                        'chinese_label': entry['chinese_label'], 'category': entry['category']}}
        else:
            key = (claim['character'], normalized(claim['target']), 'literal', '')
            topic = {'grouping': 'literal', 'glossary_id': None, 'glossary_entry': None}
        group = groups.setdefault(key, {'character': key[0], 'topic_literal_normalized': key[1], **topic,
            'topic_original_literals': set(), 'target_reference_statuses': set(),
            'directions': {d: [] for d in ('buff','nerf','keep','unclear')}})
        group['topic_original_literals'].add(claim['target'])
        group['target_reference_statuses'].add(reference['status'])
        group['directions'][claim['direction']].append(claim)
    result = []
    for key in sorted(groups):
        group = groups[key]
        group['topic_original_literals'] = sorted(group['topic_original_literals'])
        group['target_reference_statuses'] = sorted(group['target_reference_statuses'])
        all_ids, direction_sets = set(), []
        for direction, entries in group['directions'].items():
            ids = {c['comment_id'] for c in entries}
            all_ids |= ids
            direction_sets.append(ids)
            group['directions'][direction] = {'comment_ids': sorted(ids), 'supporting_comment_count': len(ids),
                'by_language': dict(sorted(Counter(sources[i]['language'] for i in ids).items())),
                'by_platform': dict(sorted(Counter(sources[i].get('platform') or 'unknown' for i in ids).items())),
                'recommendations': sorted(entries, key=lambda c: c['claim_id'])}
        overlap = {i for i in all_ids if sum(i in s for s in direction_sets) > 1}
        group.update(union_comment_ids=sorted(all_ids), union_comment_count=len(all_ids),
                     direction_overlap_comment_ids=sorted(overlap))
        result.append(group)
    return result, unresolved


def export_report(run, out, review=None):
    data = load_run(run)
    sources, mode = data['sources'], data['raw']['evidence_quality_mode']
    reviewer, appendix, review_queue = None, [], []
    if review:
        reviewer, reviewed, exclusions = load_overlay(data, review)
        claims = [c for c in reviewed if c['formal_eligible']]
        appendix = [c for c in reviewed if not c['formal_eligible']]
        review_queue = exclusions
        view = reviewer['reviewer_type'] + '_reviewed'
    else:
        claims = [{**e['claim'], 'claim_id': cid, 'comment_id': e['comment_id']} for cid,e in data['proposals'].items() if cid in data['automatic']]
        view = 'automatic'
        review_queue = list(data['proposals'].values())
    groups, unresolved = groups_for(claims, sources)
    quality = data['quality']
    routed = [r for q in quality for r in q['routing']]
    reference = evidence.character_reference('\n'.join(r['text_original'] for r in sources.values()))
    quality_views = {'opinion_summary': evidence_quality.summarize_opinions(quality, reference),
                     'system_feedback': [r for r in routed if r['route'] == 'system_evidence'],
                     'exclusions': [r for r in routed if r['route'] == 'exclude'],
                     'review_queue': [r for r in routed if r['route'] == 'review']}
    dates = {}
    for key in ('created_at_utc','published_at','timestamp','source_created_at','review_timestamp','timestamp_created','created_at','updated_at','collected_at_utc','published_at_utc'):
        values = sorted({str(r[key]) for r in sources.values() if r.get(key) is not None})
        if values:
            dates[key] = {'minimum': values[0], 'maximum': values[-1], 'observed_comments': sum(r.get(key) is not None for r in sources.values())}
    ledger_path = data['folder'] / 'full-pipeline-coverage.json'
    ledger = read(ledger_path) if ledger_path.exists() else data['raw'].get('full_pipeline_coverage', [])
    partial = data['run_state'] != 'completed'
    quality_ids = {r['route']: sorted({x['comment_id'] for x in routed if x['route'] == r['route']}) for r in routed}
    all_topic_ids = {c['comment_id'] for c in claims}
    statuses = Counter(target_reference(c)['status'] for g in groups for d in g['directions'].values()
                       for c in d['recommendations'])
    literal_groups = {(g['character'], normalized(literal)) for g in groups for d in g['directions'].values()
                      for c in d['recommendations'] for literal in [c['target']]}
    near_path = data['folder'] / 'near-duplicates.json'
    near = read(near_path) if near_path.exists() else None
    report = {'schema_version': 'aimediator-report-v2', 'view': view, 'reviewer_provenance': reviewer,
        'run_fingerprints': data['fingerprints'], 'run_identity': data['run_identity'],
        'execution_provenance': data['provenance'], 'legacy_adapter': data['legacy'],
        'engine_report_schema': data['raw'].get('report_schema_version'), 'run_state': data['run_state'],
        'partial': partial, 'scope': 'collection_sample', 'patch_applicability': 'unknown',
        'observed_source_date_ranges': dates, 'quality_mode': mode,
        'quality_assessment': {'off':'unassessed','shadow':'observation_only','enforce':'enforced'}[mode],
        'denominators': {'input_comments': len(sources),
            'by_language': dict(sorted(Counter(r['language'] for r in sources.values()).items())),
            'by_platform': dict(sorted(Counter(r.get('platform') or 'unknown' for r in sources.values()).items()))},
        'counts': {'formal_claims': len(claims), 'formal_unique_comment_ids': sorted(all_topic_ids),
                   'formal_unique_comments': len(all_topic_ids), 'review_appendix_claims': len(appendix)},
        'topic_grouping': {'rule': 'glossary_id_then_literal',
            'target_reference_status_counts': {k: statuses.get(k, 0) for k in ('resolved', 'candidate', 'unmatched')},
            'groups': len(groups), 'glossary_groups': sum(g['grouping'] == 'glossary_id' for g in groups),
            'literal_groups': sum(g['grouping'] == 'literal' for g in groups),
            'groups_by_literal_only': len(literal_groups)},
        'topics': groups, 'unresolved_identity_or_target_claims': unresolved,
        'near_duplicate_clusters': None if near is None else {
            'near_duplicate_cosine': near['near_duplicate_cosine'], 'policy_version': near['policy_version'],
            'clusters': near['clusters'],
            'note': 'Annotation only: comments in one cluster are counted as before; no count changes.'},
        'source_review_appendix': appendix, 'source_review_queue': review_queue,
        'coverage': ledger, 'processing_summary': data['raw'].get('summary', {}),
        'processing_failures': [r for r in ledger if 'failed' in r.get('status','') or 'pending' in r.get('status','')],
        'automatic_quarantined_proposals': [e for cid,e in data['proposals'].items() if cid not in data['automatic']],
        'quality_view_provenance': 'automatic_quality_annotation_not_source_review',
        'quality_views': quality_views if mode == 'enforce' else None,
        'shadow_diagnostics': quality_views if mode == 'shadow' else None,
        'quality_route_comment_ids': quality_ids, 'sources': list(sources.values()),
        'semantic_accuracy': None,
        'limitations': ['Collected sample comments, not independent players or community-wide consensus.',
            'Comment IDs can overlap across directions/topics/routes; these counts are not additive.',
            'Targets that resolve to exactly one glossary entry are grouped by that entry across wording and language; other targets, glossary candidates included, are grouped by normalized literal and can fragment equivalent topics; no fuzzy or semantic merging.',
            'Emotional intensity never changes the evidence weight of substantive feedback.',
            'Automatic semantic audits use the same routed model and can have correlated attribution errors.',
            'Source review is separate from automatic audit success and verification of game mechanics.',
            'Patch applicability, official game facts, independent human semantic accuracy and engineering tuning remain unverified.']}
    out = new_path(out, run)
    lines = ['# SF6 collected-sample feedback', '', '**PARTIAL / completion unknown**' if partial else 'Processing completed.', '',
        'View: ' + view + '; quality: ' + report['quality_assessment'] + '.',
        'Execution: ' + data['provenance'] + '. Semantic accuracy: not established.',
        'Scope: collection_sample. Patch applicability: unknown.',
        'Input comments: %d. Formal unique comments: %d.' % (len(sources),len(all_topic_ids)), '',
        '## Source and processing coverage', '', escape(dates if dates else 'Source dates unknown'), '',
        'Language denominators: ' + escape(report['denominators']['by_language']),
        'Platform denominators: ' + escape(report['denominators']['by_platform']),
        'Technical failure/pending comments: %d.' % len(report['processing_failures']), '',
        '## Character and topic evidence (glossary entries and literals)', '']
    if reviewer:
        lines += ['Reviewer: ' + escape(reviewer['reviewer_type']) + ' / ' + escape(reviewer['reviewer_id']), '']
    for group in groups:
        if group['grouping'] == 'glossary_id':
            entry = group['glossary_entry']
            lines += ['### ' + escape(group['character']) + ' — ' + escape(entry['canonical_name']) + ' / ' +
                      escape(entry['chinese_label']) + ' (glossary ' + escape(group['glossary_id']) + ')', '',
                      'Literals: ' + '; '.join(escape(t) for t in group['topic_original_literals']), '']
        else:
            lines += ['### ' + escape(group['character']) + ' — ' + escape(group['topic_literal_normalized']), '']
        for direction, entry in group['directions'].items():
            lines += ['**%s**: %d distinct comments' % (direction, entry['supporting_comment_count']), '']
            for claim in entry['recommendations']:
                lines += ['- ' + escape(claim['recommendation']) + ' (' + source_link(sources[claim['comment_id']]) + ')']
                for span in claim['evidence']:
                    lines += ['  - ' + source_link(sources[claim['comment_id']], span['evidence_id']) +
                        ' source Unicode [%d,%d): ' % (span['start'],span['end']) + escape(span['text'])]
            lines += ['']
    lines += ['## Unresolved identity/target and review appendix', '']
    for claim in unresolved + appendix:
        lines += ['- ' + source_link(sources[claim['comment_id']]) + ': ' + escape(claim['recommendation']) +
                  ' — ' + escape(claim.get('audit_status','unresolved_identity_or_target'))]
    lines += ['', '## Quality routes' + (' (observation only)' if mode == 'shadow' else ''), '']
    if mode == 'off':
        lines += ['Quality unassessed. No missing general/system concerns are inferred.']
    else:
        for route in evidence_quality.ROUTES:
            items = [r for r in routed if r['route'] == route]
            lines += ['', '### ' + route, '']
            for item in items:
                lines += ['- ' + source_link(sources[item['comment_id']]) + ': ' + escape(item.get('reason'))]
                for segment in item['segments']:
                    lines += ['  - source Unicode [%d,%d): ' % (segment['start'],segment['end']) + escape(segment.get('quote',segment.get('text')))]
    lines += ['', '## Source review queue', '', '%d pending/rejected/uncertain proposal records; see report.json for original automatic errors and decisions.' % len(review_queue), '', '## Limitations', '']
    lines += ['- ' + text for text in report['limitations']]
    out.mkdir(parents=True)
    write(out / 'report.json', report)
    (out / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return out, report['counts']
