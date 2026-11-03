"""Bind explicit agent audit decisions to immutable feedback and saved model outputs.

This exporter does not label with keywords, call inference, or alter screening.
Labels are a non-blind agent audit, not independent human ground truth.
"""
import argparse
from collections import Counter
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import evidence_quality as quality
import run_balance_analysis as balance
from run_quality_screening_experiment import classify

ROUTES = {'M': '角色机制候选', 'S': '系统反馈候选', 'G': '仅一般意见',
          'U': '待上下文/身份复核', 'X': '整条无关，应排除', 'L': '语言未支持，隔离'}
GROUPS = {'candidate': '有角色/系统候选', 'general': '仅一般意见',
          'review': '待复核', 'exclude': '整条排除', 'unsupported': '语言隔离'}
OUTCOMES = {'kept_relevant': '相关性放行合理，仍需质量分流',
            'missed_relevant': '含相关信息但未放行',
            'accepted_irrelevant': '无关评论误放行',
            'rejected_irrelevant': '无关评论未放行，合理',
            'ambiguous_accepted': '语义待复核，已被相关性放行',
            'ambiguous_held': '语义待复核，相关性未放行',
            'language_isolation': '葡语未支持，不计筛选对错'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def tsv(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


def group(routes):
    return ('candidate' if {'M', 'S'} & set(routes) else 'general' if 'G' in routes else
            'review' if 'U' in routes else 'exclude' if 'X' in routes else 'unsupported')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'reports/screening-audit-20261027')
    args = parser.parse_args()
    out = args.out.resolve()
    source = ROOT / 'data/raw/feedback/20261015-expanded/screened/records.jsonl'
    relevance_dir = ROOT / 'reports/balance-review-v2/relevance'
    quality_dir = ROOT / 'reports/quality-screening-existing-100-recovered-v2'
    raw = [json.loads(line) for line in source.read_text().splitlines() if line.strip()]
    labels = tsv(out / 'review-labels.tsv')
    assert len(labels) == len(raw) == 321
    assert [int(a['index']) for a in labels] == list(range(1, 322))
    assert len({r['record_id'] for r in raw}) == 321
    relevance = {r['comment_id']: r for r in read(relevance_dir / 'relevance.json')}
    frozen_sources = {r['record_id']: r for r in read(relevance_dir / 'source-snapshot.json')}
    saved_quality = read(quality_dir / 'screening-progress.json')
    quality_records = {r['comment_id']: r for r in saved_quality}
    quality_sources = {r['record_id']: r for r in read(quality_dir / 'source-snapshot.json')}
    quality_audits = {int(r['index']): r for r in tsv(out / 'quality-comment-reviews.tsv')}
    point_audits = {(int(r['index']), r['point_id']): r for r in tsv(out / 'quality-point-reviews.tsv')}
    relevance_overrides = {int(r['index']): r for r in tsv(out / 'relevance-overrides.tsv')}
    identity = read(quality_dir / 'manifest.json')['identity']
    replay = read(out / 'admission-replay/replay-results.json')
    assert replay['all_admission_decisions_unchanged'] and replay['fresh_inference_calls'] == 0
    assert replay['current_runner_sha256'] == sha((ROOT / 'scripts/run_balance_analysis.py').read_bytes())
    assert replay['current_policy_module_sha256'] == sha((ROOT / 'scripts/balance_policy.py').read_bytes())
    rows, checked_points = [], set()
    checked_annotations, checked_segments, attempted = 0, 0, 0
    for i, (r, a) in enumerate(zip(raw, labels), 1):
        text = r['text_original']
        assert a['evidence'] in text, ('Audit quote mismatch', i)
        routes = a['routes'].split(',')
        assert set(routes) <= set(ROUTES)
        d = relevance.get(r['record_id'])
        if d:
            assert frozen_sources[r['record_id']]['text_original'] == text
            assert d['language'] == r['language']
        q = quality_records.get(r['record_id'])
        if q:
            assert q['text_original'] == quality_sources[r['record_id']]['text_original'] == text
            assert q['content_sha256'] == sha(text.encode())
            assert q['relevance_record'] == d
            recomputed = classify(r, d, q.get('quality_record'))
            assert all(q[key] == value for key, value in recomputed.items())
        g = group(routes)
        relevance_label = relevance_overrides.get(i, {}).get('relevance',
            'related' if g in ('candidate', 'general') else 'unrelated' if g == 'exclude' else 'uncertain')
        related = relevance_label == 'related'
        if not d:
            assert r['language'] == 'pt'
            stage = '语言不支持'
            outcome = 'language_isolation'
        elif d['agreement']:
            stage = '相关性放行'
            outcome = 'kept_relevant' if related else 'accepted_irrelevant' if g == 'exclude' else 'ambiguous_accepted'
        else:
            stage = ('检索复核不确定，尚未放行' if d.get('retrieval_review_uncertain') or d.get('model_uncertain')
                     else '向量检索未通过' if d.get('retrieval_triage') == 'unrelated'
                     else '相关性复核未通过')
            outcome = 'missed_relevant' if related else 'rejected_irrelevant' if g == 'exclude' else 'ambiguous_held'
        qr = q.get('quality_record') if q else None
        quality_status = qr['status'] if qr else 'not_run' if d and d['agreement'] else 'not_applicable'
        points = []
        if qr:
            attempted += 1
            assert i in quality_audits
            if qr['status'] == 'completed':
                recalculated = quality.qualify(qr['annotation'], r, balance.evidence_units(text), identity['policy'])
                assert recalculated['status'] == 'completed' and not recalculated['errors']
                assert recalculated['routing'] == qr['routing']
                assert recalculated['emotion_ratio'] == qr['emotion_ratio']
                checked_annotations += 1
                for route in qr['routing']:
                    for s in route['segments']:
                        assert s['quote'] == text[s['start']:s['end']]
                        checked_segments += 1
                    if route['point_id'] is not None:
                        key = (i, route['point_id'])
                        assert key in point_audits
                        checked_points.add(key)
                        points.append({'model_point': route, 'audit': point_audits[key]})
        start = text.index(a['evidence'])
        rows.append({'index': i, 'comment_id': r['record_id'], 'language': r['language'],
                     'source_url': r['source_url'], 'text_original': text,
                     'source_sha256': sha(text.encode()), 'patch_context': r.get('target_patch_context'),
                     'coarse_decision': r['coarse_screening']['decision'],
                     'coarse_reason': r['coarse_screening']['reason'], 'group': g, 'routes': routes,
                     'relevance_label': relevance_label,
                     'relevance_label_reason': relevance_overrides.get(i, {}).get('reason', a['reason']),
                     'tone': a['tone'], 'confidence': a['confidence'], 'audit_reason': a['reason'],
                     'audit_evidence': {'quote': a['evidence'], 'start': start, 'end': start + len(a['evidence'])},
                     'relevance_stage': stage, 'relevance_record': d, 'relevance_audit': outcome,
                     'quality_status': quality_status, 'saved_experiment_decision': q['decision'] if q else None,
                     'quality_comment_audit': quality_audits.get(i), 'quality_points': points,
                     'quality_record': qr, 'reviewer_type': 'agent_nonblind', 'human_review': None})
    assert checked_points == set(point_audits)
    assert attempted == len(quality_audits) == 22
    assert len(relevance) == 320 and len(quality_records) == 38
    # Counts below are conditional on this preselected corpus and explicit audit policy.
    counts = Counter(r['group'] for r in rows)
    outcomes = Counter(r['relevance_audit'] for r in rows)
    tp, fn = outcomes['kept_relevant'], outcomes['missed_relevant']
    fp, tn = outcomes['accepted_irrelevant'], outcomes['rejected_irrelevant']
    retained_points = [p for r in rows for p in r['quality_points'] if p['model_point']['route'] in
                       ('mechanism_evidence', 'system_evidence', 'opinion_only')]
    stat = {'date': '2026-10-27', 'timezone': 'America/Los_Angeles', 'input': len(rows),
            'languages': dict(Counter(r['language'] for r in rows)), 'groups': dict(counts),
            'routes_overlapping': dict(Counter(k for r in rows for k in r['routes'])),
            'relevance_outcomes': dict(outcomes), 'binary_confusion': {'tp': tp, 'fn': fn, 'fp': fp, 'tn': tn},
            'binary_denominator': tp + fn + fp + tn,
            'topic_relevance_labels': dict(Counter(r['relevance_label'] for r in rows if r['language'] in ('en', 'zh'))),
            'relevance_precision': {'numerator': tp, 'denominator': tp + fp},
            'relevance_recall_within_screened': {'numerator': tp, 'denominator': tp + fn},
            'false_acceptance_among_labeled_admitted': {'numerator': fp, 'denominator': tp + fp},
            'quality_experiment_classified': 38, 'quality_attempted': attempted,
            'quality_completed': checked_annotations, 'quality_failed': attempted - checked_annotations,
            'quality_not_run_among_admitted': sum(r['quality_status'] == 'not_run' for r in rows),
            'quality_attempted_by_language': dict(Counter(r['language'] for r in rows if r['quality_record'])),
            'quality_points_reviewed': len(checked_points), 'retained_quality_points': len(retained_points),
            'retained_quality_point_routes': dict(Counter(p['model_point']['route'] for p in retained_points)),
            'quality_point_verdicts': dict(Counter(p['audit']['verdict'] for r in rows for p in r['quality_points'])),
            'by_language': {lang: {'groups': dict(Counter(r['group'] for r in rows if r['language'] == lang)),
                                 'outcomes': dict(Counter(r['relevance_audit'] for r in rows if r['language'] == lang))}
                            for lang in ('en', 'zh', 'pt')},
            'human_ground_truth': False, 'fresh_model_calls': 0,
            'independent_test': False, 'all_quality_annotations_completed': False,
            'emotion_causal_bias_measured': False, 'quality_model_success_rate_claimed': False}
    silver = [json.loads(line) for line in (ROOT / 'data/evaluation/balance-silver-v1/labels.jsonl').read_text().splitlines() if line.strip()]
    by_id = {r['comment_id']: r for r in rows}
    disagreements = []
    for old in silver:
        current = by_id[old['comment_id']]
        current['historical_silver'] = {'relevance': old['relevance'], 'reason': old['reason'],
                                       'split': old['split'], 'reviewer_type': old['reviewer_type']}
        expected = current['relevance_label']
        if expected != old['relevance']:
            disagreements.append({'index': current['index'], 'comment_id': current['comment_id'],
                                  'historical_silver_relevance': old['relevance'],
                                  'historical_silver_reason': old['reason'], 'new_audit_relevance': expected,
                                  'new_audit_reason': current['audit_reason'], 'resolution': 'independent_adjudication_pending'})
    write(out / 'historical-silver-disagreements.json', disagreements)
    manifest = {'created_at': datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),
                'reviewer': 'Codex agent, non-blind single-pass semantic review with consistency checks',
                'scope': 'All 321 retained coarse-screened records; 320 supported en/zh plus one pt',
                'label_procedure': 'All source comments read in full; explicit per-comment judgments, not keyword scoring. Quality outputs reviewed separately. Boundary consistency checked against prompts and prior silver, retaining documented disagreements; no frozen labels or human fields changed.',
                'limitations': ['Non-blind single-agent silver audit; not human ground truth or an independent benchmark.',
                                'Only coarse-retained records: cannot estimate losses in the original rejected corpus.',
                                'Quality outputs from a partial selected 100-comment experiment; 22 attempted, all English.',
                                'No fresh LLM, embedding or full extraction run; saved requests replayed with current code.',
                                'Patch applicability, identities and factual gameplay/numeric claims remain unverified.',
                                'Emotion labels describe tone, not proof of cognitive bias. No real neutral/emotional matched inference experiment.'],
                'source_files_sha256': {}, 'analysis_policy': ROUTES,
                'comment_group_priority': 'M or S -> candidate; else G -> general; else U -> review; else X -> exclude; else L -> unsupported',
                'relevance_metric_scope': 'Topic relevance is separate from evidence readiness. M/S/G are related, X unrelated; explicit per-source overrides mark 19 review-only records topic-related despite uncertain identity/stance. Eight remaining ambiguous topics and pt excluded. Routes within a comment may overlap.',
                'historical_silver_consulted_for_boundary_consistency': True,
                'historical_silver_disagreement_count': len(disagreements), 'frozen_replay': replay}
    snapshot = out / 'snapshots'
    snapshot.mkdir(exist_ok=True)
    sources = {'source-records.jsonl': source, 'frozen-relevance.json': relevance_dir / 'relevance.json',
               'quality-progress.json': quality_dir / 'screening-progress.json',
               'quality-manifest.json': quality_dir / 'manifest.json',
               'current-evidence-quality-policy.json': ROOT / 'configs/evidence-quality-policy.json',
               'current-balance-review-policy.json': ROOT / 'configs/balance-review-policy.json',
               'current-evidence-quality.py': ROOT / 'scripts/evidence_quality.py',
               'current-quality-en.txt': ROOT / 'prompts/evidence-quality.en.txt',
               'current-quality-zh.txt': ROOT / 'prompts/evidence-quality.zh.txt',
               'historical-silver-labels.jsonl': ROOT / 'data/evaluation/balance-silver-v1/labels.jsonl',
               'historical-silver-errata.json': ROOT / 'data/evaluation/balance-silver-v1/errata.json',
               'relevance-overrides.tsv': out / 'relevance-overrides.tsv',
               'review-labels.tsv': out / 'review-labels.tsv',
               'quality-point-reviews.tsv': out / 'quality-point-reviews.tsv',
               'quality-comment-reviews.tsv': out / 'quality-comment-reviews.tsv'}
    for name, path in sources.items():
        content = path.read_bytes()
        (snapshot / name).write_bytes(content)
        manifest['source_files_sha256'][str(path.relative_to(ROOT))] = sha(content)
    write(out / 'manifest.json', manifest)
    write(out / 'summary.json', stat)
    (out / 'comment-audits.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
    write(out / 'audit-data.json', {'summary': stat, 'rows': rows})
    point_rows = [{'index': r['index'], 'comment_id': r['comment_id'], **p} for r in rows for p in r['quality_points']]
    write(out / 'model-point-audits.json', point_rows)
    verification = {'source_comments': len(raw), 'audit_rows': len(rows), 'unique_ids': len({r['comment_id'] for r in rows}),
                    'audit_quotes_exact': len(rows), 'frozen_relevance_source_bindings': len(relevance),
                    'quality_source_bindings': len(quality_records), 'revalidated_annotations': checked_annotations,
                    'revalidated_routing_segments': checked_segments, 'reviewed_information_points': len(checked_points),
                    'all_existing_information_points_audited': True,
                    'saved_comment_classifications_recomputed': len(quality_records),
                    'all_input_and_historical_output_files_preserved': True,
                    'current_admission_replay_verified_requests': replay['verified_requests']}
    write(out / 'verification.json', verification)
    write_markdown(out, rows, stat)
    print(json.dumps({'summary': stat, 'verification': verification}, ensure_ascii=False, indent=2))


def write_markdown(out, rows, s):
    tp, fn, fp, tn = (s['binary_confusion'][k] for k in ('tp', 'fn', 'fp', 'tn'))
    related, irrelevant, uncertain = tp + fn, fp + tn, s['topic_relevance_labels']['uncertain']
    report = f'''# 现有筛选机制审核 · 2026-10-27

结论：现有结果不足以认定筛选机制能精确清除情绪干扰和无关内容。已发现具体信息被挡住、无关内容误放行、纯负评态度进入系统证据、一般意见升级为角色机制，以及角色请求错归系统。格式校验通过不能证明这些语义正确。

## 本次覆盖和结果

- 全部 321 条逐条审核：207 英文、113 中文、1 葡语。
- 互斥主分类：{s['groups']['candidate']} 条含角色/系统候选，{s['groups']['general']} 条仅一般意见，{s['groups']['review']} 条待复核，{s['groups']['exclude']} 条整条无关，1 条葡语隔离。
- 单条可同时含一般意见、机制、系统反馈与待核部分；重叠路由数不能相加当评论总数。候选仍需核对身份、版本、事实与来源，不能直接调参。
- 最新冻结相关性：320 条中英文，275 条放行，45 条未放行；161 份请求经当前代码重放全部一致，无新推理调用。45 条中含检索拒绝、复核拒绝和不确定状态，不把未放行全叫模型否定。
- 本次银标认为相关的 {related} 条中，{tp} 条放行、{fn} 条未放行。{irrelevant} 条无关中，{fp} 条误放行、{tn} 条未放行。
- 相关性条件 precision = {tp}/{tp+fp} = {tp/(tp+fp):.1%}；在当前粗筛保留集内的条件 recall = {tp}/{tp+fn} = {tp/(tp+fn):.1%}。仅对 {s['binary_denominator']} 条有明确主题二元标签的评论计算，{uncertain} 条主题仍不确定及1条葡语不进分母。27条用途待复核中，19条主题其实明确相关，只是身份/方向/事实未决，不能混为主题不相关；逐条依据见relevance-overrides.tsv。一般意见也算相关，这不是“具体机制证据准确率”。
- 粗筛已保留的320条中英文中仍有{irrelevant}条无关（{irrelevant}/320 = {irrelevant/320:.1%}）；这只描述保留集残留，不是粗筛完整precision/recall。原始已拒绝语料未审核。

## 质量阶段不能按38条都已审核成功理解

既有100条诊断实验只归类38条，其中16条沿用上游未放行结果；实际质量尝试22条，全部英文。15条结构校验通过，7条失败转复核。其余253条已获相关性放行的评论尚无本次实验的质量结果，中文质量效果尤其未被该实验验证。15/22只表示结构校验通过比例，不是正确率；复核不是剔除成功或提取成功。

已审核全部16个已发布信息点，其中7个进入保留路由：2个角色机制点、5个系统点。两个角色机制点均把一般抱怨/更新观察错误升格；5个系统点分别有混入无关内容、纯负评态度泄漏、角色错归系统或请求/观察分类错误。它们来自刻意含历史问题的诊断子集，不能外推全量错误率。

## 可直接核对的失败样例

- #14 steam:236856267：DI抱怨与Ryu“war crimes”夸张抱怨合成Ryu机制证据。应降为一般意见，不能给Ryu绑定DI属性。
- #23 steam:236222206：Drive-rush corner-carry / 50-50的具体反馈被排除；叹气却进复核。是片段误删，不因整条review就算保护了信息。
- #63 steam:233481207：讽刺“another year of Ryu buffs”被当Ryu具体机制，buffs还被当机制名；更新观察不能冒充作者支持加强。
- #94 steam:232518681：动作、画面可读性赞美被相关性放行；全文没有角色强弱或战斗调整主张。
- #163 youtube:UgzJYtb-vEd9Z3T9GQh4AaABAg：长文最后明确请求修复100%解摔输入BUG，却在相关性阶段未放行。
- #185 steam:231963988：带条件的绿冲3格、移除投循环、招架-1帧请求没有释放为系统信息，全留复核。
- #220 steam:229094178：buff manon被误作系统反馈，Manon字面名丢失、明确请求误作强度评价。
- #233 steam:228172110：“and this review will be negative”被保留为系统证据；JP削弱请求又被错归系统。

## emotional bias的审核口径

本次检查的是“情绪是否代替信息”“是否误删带情绪的有效信息”“是否把纯发泄/无关片段混入证据”“是否因切分或角色归属扭曲意见”。措辞愤怒不证明认知偏差，也不证明信息错误；没有真人双标、真实等义情绪/中性对照推理或玩家背景，本次不能测量心理偏差或证明某种语气导致错误。

“balance sux”“加强JP”等是政策允许的一般意见，只能统计，不能出具体机制或数值方案。命名机制但仅表示厌恶也不自动具备机制资格。纯感叹、辱骂、外貌、价格、网络、作弊、剧情、登场阵容喜好等应从战斗平衡证据中移除；混合评论保留有效部分，不能整条一刀切。

代码中的情绪比例0.70仅作诊断，不能删除或改权重；默认quality模式off，shadow只观察，enforce才约束下游。此次重放与现有单元检查说明确定性控制可重现，不证明本地模型真实分段与语义已达标。

## 建议修复顺序

1. 优先修复信息点的范围、角色归属、具体性与请求/观察区分，先阻断一般意见升格及情绪片段进入证据。
2. 用上述实际失败项检查混合长文、末尾有效句、反讽、正向反馈、一般总体意见和分段上下文；不能只靠增删关键词。
3. 保留review独立状态并提供实际释放流程；未提取应记录为损失，不能包装成筛除成功。
4. 以独立人工双标和裁决确认这些AI银标，再在未参与修复的粗筛前样本测量完整流程。现阶段不足以把enforce当成可靠的自动审核替代品。

## 查看全部结论

全部321条见 ALL-REVIEWS.md / comment-audits.jsonl；16个模型信息点及逐点评语见 MODEL-POINT-REVIEWS.md / model-point-audits.json。每条含完整原文、来源、引用位置、审核理由、置信度、原粗筛判断、最新相关性状态与可用的质量输出。

本审核由单个AI非盲评完成，属于agent silver，不是独立人工真值；审核者先前已见部分历史失败例。初审后参照现有提示词和历史银标核对了纯学习、匹配偏好及更新频率等边界，历史银标没有被改写；分歧逐条存于historical-silver-disagreements.json，均待独立裁决。尤其#82的高水平随机性、#163的解摔BUG和#319的正向系统观察存在口径分歧，应结合原文核查，不能把新旧任一AI标签当人工答案。

未改动任何原文、历史模型结果或筛选规则，未重新调用本地模型，未验证实际版本、官方身份、帧数、伤害及平衡效果。所有原文校验值、快照和验证记录均在本目录。
'''
    (out / 'REPORT.zh.md').write_text(report)
    lines = ['# 全部321条逐条审核', '', 'AI非盲银标；不是独立人工真值。候选不等于机制事实。索引顺序与原始保留集一致。', '']
    for r in rows:
        lines += [f"## #{r['index']:03d} · {r['comment_id']}", '',
                  f"语言：{r['language']}；主结论：{GROUPS[r['group']]}；用途：{'、'.join(ROUTES[k] for k in r['routes'])}；置信度：{r['confidence']}。", '',
                  '审核理由：' + r['audit_reason'], '',
                  '主题相关性：' + r['relevance_label'] + '；' + r['relevance_label_reason'], '',
                  f"依据 [{r['audit_evidence']['start']}, {r['audit_evidence']['end']})：", '',
                  '> ' + r['audit_evidence']['quote'].replace('\n', '\n> '), '',
                  f"原粗筛：保留（{r['coarse_reason']}）。最新相关性：{r['relevance_stage']}。审核：{OUTCOMES[r['relevance_audit']]}。", '',
                  '质量状态：' + r['quality_status'] + '。']
        if r['quality_comment_audit']:
            lines += ['', '既有质量结果审核：' + r['quality_comment_audit']['reason']]
        for p in r['quality_points']:
            lines += ['', p['model_point']['point_id'] + ' → ' + p['model_point']['route'] + '：' + p['audit']['reason']]
        lines += ['', '[原始来源](' + r['source_url'] + ')', '', '完整原文：', '',
                  '> ' + r['text_original'].replace('\n', '\n> '), '', '原文SHA256：' + r['source_sha256'], '']
    (out / 'ALL-REVIEWS.md').write_text('\n'.join(lines) + '\n')
    lines = ['# 既有模型全部16个信息点审核', '', '来源：部分100条诊断实验，15条结构校验通过的评论；不代表全量语料。', '']
    for r in rows:
        for p in r['quality_points']:
            q, a = p['model_point'], p['audit']
            lines += [f"## #{r['index']} {r['comment_id']} / {q['point_id']}", '',
                      '模型路由：' + q['route'], '', '模型点：' + json.dumps(q['point'], ensure_ascii=False), '',
                      '原文支持片段：', '', *['> ' + seg['quote'].replace('\n', '\n> ') for seg in q['segments']], '',
                      '审核：' + a['verdict'] + '；应属：' + '、'.join(ROUTES[k] for k in a['expected'].split(',')), '', a['reason'], '']
    (out / 'MODEL-POINT-REVIEWS.md').write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
