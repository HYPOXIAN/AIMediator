"""Render the bounded experiment's measured outcomes and explicit limitations."""
import argparse
from pathlib import Path
import json
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo

import run_balance_analysis as m


def read(path):
    return json.loads(path.read_text())


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=m.ROOT/'reports/latest-balanced-20261027')
    p.add_argument('--data',type=Path,default=m.ROOT/'data/raw/feedback/20261027-latest-balanced')
    args=p.parse_args();folder=args.root
    full_selection=read(folder/'full-selected-run.json') if (folder/'full-selected-run.json').exists() else {'selected':'full-pipeline','integrity':'integrity-checks.json'}
    run=folder/full_selection['selected']
    data=read(args.data/'screened/summary.json');s=read(run/'summary.json')
    audit=read(folder/full_selection['integrity'])
    transport=read(run/'transport-reuse-summary.json') if (run/'transport-reuse-summary.json').exists() else None
    baseline=read(folder/'baseline-matched-regressions/results.json')
    final=read(folder/'final-regressions/results.json')
    nc=read(folder/'numeric-controls-final/results.json');ne=read(folder/'numeric-extraction-final/results.json')
    semantic_selection=read(folder/'semantic-selected-run.json')
    semantic=read(folder/semantic_selection['selected']/'results.json')
    recovery_selection=read(folder/'generation-recovery-selected.json')
    recovery=read(folder/recovery_selection['selected']/'results.json')
    extra_recovery_path=folder/'generation-recovery-final-new-source/results.json'
    extra_recovery=read(extra_recovery_path) if extra_recovery_path.exists() else None
    extra_review_path=folder/'generation-recovery-final-new-source/agent-source-review.json'
    extra_review=read(extra_review_path) if extra_review_path.exists() else None
    post_fix=read(folder/'post-fix-accepted-replay.json')
    quality_development=read(folder/'quality-development-comparison.json')
    quality_compact={name:read(folder/name/'results.json') for name in
        ('quality-compact-recovery','quality-compact-recovery-sampled')}
    quality_selection=read(folder/'quality-selected-run.json') if (folder/'quality-selected-run.json').exists() else {'selected':'quality-live-enforce'}
    quality_folder=folder/quality_selection['selected']
    quality=read(quality_folder/'quality-summary.json')
    qs=read(quality_folder/'summary.json')
    requests=read(args.data/'request-log.json')
    request_times={}
    for path in (run/'requests').glob('*/*/response.json'):
        stage=path.parent.parent.name;response=read(path)
        item=request_times.setdefault(stage,{'requests':0,'elapsed_seconds':0.0})
        item['requests']+=1;item['elapsed_seconds']+=response.get('elapsed_seconds',0)
    m.write_json(folder/'runtime-by-stage.json',request_times)
    prior_ids={r['record_id'] for r in map(json.loads,(m.ROOT/'data/raw/feedback/20261015-expanded/records.jsonl').read_text().splitlines())}
    sources=read(run/'source-snapshot.json')
    previous_overlap=sum(r['record_id'] in prior_ids for r in sources)
    test_log=(folder/'unit-tests-final.log').read_text()
    expectations=read(folder/'new-source-diagnostic-expectations.json')
    relevance={d['comment_id']:d for d in read(run/'relevance.json')}
    accepted=read(run/'validated-claims.json')
    source_diagnostics=[]
    for case in expectations['cases']:
        cid=case['comment_id'];claims=[c for c in accepted if c['comment_id']==cid]
        pairs={(c['character'],c['direction']) for c in claims}
        checks={'relevance':relevance[cid]['agreement'] is case['expected_related'],
            'required_accepted_pairs':all(tuple(pair) in pairs for pair in case['required_accepted_pairs']),
            'no_system_character_binding':not case['forbid_character_claims'] or not claims,
            'no_unrequested_numeric_targets':not any(c['parameters'] for c in claims)}
        source_diagnostics.append({**case,'checks':checks,'passed':all(checks.values()),'accepted_claims':claims})
    new_diagnostics={'kind':'eight_source_agent_debug_diagnostic_not_accuracy',
        'total':len(source_diagnostics),'passed':sum(c['passed'] for c in source_diagnostics),
        'human_ground_truth':False,'cases':source_diagnostics}
    m.write_json(folder/'new-source-diagnostics.json',new_diagnostics)
    diagnostic={'baseline_known_case_passed':baseline['passed'],'final_known_case_passed':final['passed'],'known_cases':final['total'],
        'numeric_entailment':{'passed':nc['passed'],'total':nc['total'],'model_only_passed':nc['model_only_passed']},
        'numeric_extraction':{'passed':ne['passed'],'total':ne['total']},
        'semantic_controls':{'passed':semantic['passed'],'total':semantic['total']},
        'semantic_selected_run':semantic_selection,
        'post_fix_accepted_contract_replay':{'passed':post_fix['passed'],'total':post_fix['total']},
        'generation_recovery':{'original_failed':recovery['original_failed_comments'],
            'recovered':recovery['generation_recovered'],'still_failed':recovery['still_failed']},
        'new_final_failure_recovery':extra_recovery,
        'new_final_failure_source_review':extra_review,
        'quality_live':quality,'quality_live_input_comments':qs['input_comments'],
        'quality_selected_run':quality_selection,
        'quality_development_comparison':quality_development,
        'quality_compact_recovery':{n:{k:d[k] for k in ('original_failed','recovered','still_failed')} for n,d in quality_compact.items()},
        'new_source_agent_debug_cases':{'passed':new_diagnostics['passed'],'total':new_diagnostics['total']},
        'independent_accuracy_established':False,'full_corpus_evidence_quality':'off',
        'selected_full_run':full_selection,'exact_request_transport':transport,
        'prior_dataset_id_overlap':previous_overlap}
    diagnostic['generation_request_runtime']=request_times
    m.write_json(folder/'validation-results.json',diagnostic)
    lines=['# Fresh balanced feedback validation', '',
        f"Completed: {datetime.now(ZoneInfo('America/Los_Angeles')).isoformat()} (America/Los_Angeles).",'',
        '## Collection and coarse screening','',
        f"Fresh official-API collection: {data['raw_records']:,} source records. Coarse decisions: {data['coarse_decisions']}. Final canonical set: {data['selected']} comments, English 300 and simplified Chinese 300; all 600 selected records are Steam reviews.",
        f"Actual request counts across collection/resumption: {dict(Counter(r['platform'] for r in requests))}. Bluesky returned HTTP 403 and stopped; YouTube material did not enter the final corrected sample.",
        f"Source publication range, UTC: English {data['created_at_range']['en']['min']} to {data['created_at_range']['en']['max']}; Chinese {data['created_at_range']['zh']['min']} to {data['created_at_range']['zh']['max']}.",
        f"This is a fresh retrieval from latest-sorted streams, not 600 newly published replies. {previous_overlap} selected IDs also appeared in the previous expanded raw dataset; no old files were used to seed this collection. Configured source types are Steam reviews and YouTube top-level comments; nested forum replies were not collected.",
        'Exact normalized-text duplicates were removed. Language-label errors and the traditional-Chinese film discussion were handled with fingerprinted agent source reviews; original raw text/labels remain unchanged. Language heuristics and targeted inspection do not establish a fully human-verified language corpus.',
        f"Frozen canonical dataset SHA-256: `{data['dataset_sha256']}`.", '',
        '## Full 600-comment program test','',
        f"Mode: full pipeline, evidence-quality=off (the existing default). All 600 inputs were embedded and routed: English to local Llama and Chinese to local Qwen. Embeddings use the previously configured Qwen3 service; no locally verifiable weight digest is available for that remote embedding model.",
        f"Retrieval/relevance agreement: {s['agreement_related']}; assessed comments: {s['assessed_comments']}; generated claims: {s['generated_claims']}; accepted after source/semantic checks: {s['accepted_claims']}; quarantined: {s['quarantined_claims']}.",
        f"Failed requests: {s['failed_requests']}; final extraction-failed comments: {s['final_generation_failed_comments']}. Coverage statuses: {audit['coverage_statuses']}.",
        f"Separate bounded recovery of the INITIAL run's one failed source: {recovery['generation_recovered']}/{recovery['original_failed_comments']} produced valid generation; {recovery['still_failed']} remain failed within that retry scope. Recovery accepted {len(recovery['accepted_claims'])} claims after the unchanged source and semantic gates. The current-code run has {s['final_generation_failed_comments']} failures, reported above; this older retry count is not its failure total. Supplemental runs do not overwrite full-run counts or establish independent semantic accuracy.",
        f"Audit of the newly failed final-run source: its initial four generated claims were all quarantined, and neither full run accepted a claim from it. See generation-failure-audit.json. One separate bounded retry of this source: {json.dumps({k:extra_recovery[k] for k in ('original_failed_comments','generation_recovered','still_failed')} if extra_recovery else 'not completed')}. It does not replace the full-run outcome.",
        f"IMPORTANT supplemental semantic failure: the retry produced valid JSON, but its {len(extra_recovery['accepted_claims']) if extra_recovery else 0} automatically accepted claims wrongly attribute World Tour progression/difficulty, generic Drive Impact complaints or optimization praise to Ryu adjustments. Agent source review rejects the entire supplement; none are merged into the primary 187 claims. The same-model verifier missed these errors. This demonstrates a material semantic limitation rather than a successful source recovery; see generation-recovery-final-new-source/agent-source-review.json.",
        'Additional isolated recovery trials used temperature 0.4 and, once, a bounded 2,048-token strict-JSON trial that delayed the early repeated-claim abort. Neither recovered the long source; no partial output or repaired JSON was admitted. Every request and failed attempt remains available.',
        f"By language: {s['by_language']}.",
        f"Summed request-processing elapsed time, including failed attempts and excluding collection/embedding: {sum(t['elapsed_seconds'] for t in request_times.values())/60:.1f} minutes. Replayed responses have negligible transport time, so this is not a fresh-inference throughput benchmark. Stage detail: {request_times}.",
        f"Integrity: {sum(audit['checks'].values())}/{len(audit['checks'])} assertions passed. Covers exact source snapshots, language counts, deduplication, every admitted comment's accounting, exact accepted source spans, claim accounting, numerical source checks and isolation of unverified character identities.",
        f"After the first full-corpus run, a decoder-schema consistency fix removed impossible null-only numeric parameters when no requested value/delta is available. All {post_fix['passed']}/{post_fix['total']} initially accepted claims were replay-validated and all eight live semantic controls rerun. The selected full-corpus result is {full_selection['selected']}; it executes the current code on all 600 inputs. Exactly identical model-visible requests may reuse recorded results, while changed schemas/messages/options require fresh inference. It is not 600 wholly independent fresh generations. Transport counts: {transport}.",
        'Passing source checks does not establish that player claims are true. Same-model semantic audits have correlated error risk. Accepted claims still require source review and versioned game data before engineering use.', '',
        '## Prompt changes and paired diagnostic','',
        'The active bilingual prompts are prompts/summarize-balance.{en,zh}.txt and prompts/verify-balance.{en,zh}.txt. The final report is aggregated deterministically; there is no separate free-form final-summary LLM prompt.',
        'The revised extraction prompts require a complete subject/action sentence, distinguish conditional threats from opposition to nerfs, preserve attacker/victim and clause-local subjects, separate system from character opinions, preserve restrictions and reject numbers occurring only in insults, jokes, prices, playtime or unrelated comparisons. The verifier checks the whole recommendation instead of accepting a correct direction label with meaningless text.',
        f"Six known-case regressions, with the same frozen runner/model configuration and frozen expectations: baseline {baseline['passed']}/{baseline['total']}, final {final['passed']}/{final['total']}. Their overall pass count did not improve. The revised prompts repair the publisher-only recommendation and the conditional nerf threat; an insulting numeric expression is still misread and blocked, and one attacker complaint does not pass semantic review. These known debugging cases are not an independent accuracy benchmark; unchanged legacy expectations can also be disputed.",
        f"Numeric entailment controls: pipeline {nc['passed']}/{nc['total']}, model-only {nc['model_only_passed']}/{nc['total']}. End-to-end numeric extraction: {ne['passed']}/{ne['total']}. Synthetic controls never enter community counts.", '',
        f"Bilingual semantic controls: {semantic['passed']}/{semantic['total']}, covering negated nerfs, conditional nerf threats, attacker/victim attribution and system versus roster clauses. These are synthetic diagnostics, not a real-source accuracy estimate.", '',
        'Per-case baseline/final recommendations and outcomes:', '']
    for before,after in zip(baseline['cases'],final['cases']):
        def claim_text(case):
            return [{'character':c['claim']['character'],'direction':c['claim']['direction'],
                     'recommendation':c['claim']['recommendation'],'source_errors':c['source_errors'],
                     'audit':(c.get('audit') or {}).get('support_status')} for c in case.get('claims',[])]
        lines.extend([f"- {after['comment_id']} ({after['category']}): baseline pass={before['passed']}, final pass={after['passed']}.",
                      f"  Baseline: {json.dumps(claim_text(before),ensure_ascii=False)}",f"  Final: {json.dumps(claim_text(after),ensure_ascii=False)}"])
    lines += ['', '## Quality-module scope','',
        f"Selected quality diagnostic: {quality_selection['selected']}. Quality prompt refinement is evaluated on the same four known development sources, never reported as held-out accuracy.",
        f"Development route-plus-current-position checks: {[(name,r['passed'],r['total']) for name,r in quality_development['comparison'].items()]}. The intermediate variant matched all four routes but still got two directions wrong; the selected variant retains three valid primary classifications and sends the fourth to review. Failed compact-quote recovery attempts remain in separate folders; none were silently converted into successful annotations.",
        f"A separate live enforce diagnostic used {qs['input_comments']} real sources drawn from the frozen 600-comment set. Relevance admitted {qs['agreement_related']}; quality completed {quality['completed']}, failed {quality['failed']}. Route comment counts (overlapping): {quality['route_comment_counts']}.",
        'This small diagnostic plus the complete offline regression suite tests quality integration. The 600-comment run does not claim 600 fresh quality span annotations, full shadow/enforce coverage, measured emotion-bias reduction or semantic precision/recall.', '',
        '## New-source meaning checks','',
        f"Eight deliberately selected new-corpus sources (four per language) received source-only agent expectations before the corresponding corpus outcomes were inspected. The frozen default/off pipeline matches {new_diagnostics['passed']}/{new_diagnostics['total']} of these debugging expectations; see new-source-diagnostics.json for all cases and failures. Three sources were later reused for quality-prompt development, as recorded in new-source-diagnostic-use-note.json. This is not human ground truth, random sampling, a held-out study or an independent accuracy estimate.", '',
        '## Code regression','',test_log[test_log.rfind('----------------------------------------------------------------------'):].strip(), '',
        '## Limitations and retained history','',
        'No independent human labels, patch applicability check, official identity update or game-mechanic truth verification was performed. These are bounded program and prompt diagnostics, not proof of globally optimal prompts, overall player consensus or ready-to-ship balance values.',
        'Baseline prompts, intermediate candidate prompts/regressions, the provisional-language run and interrupted CPU experiment are retained. Their results were not substituted for the final complete corpus run.', '',
        f"Primary files: {full_selection['selected']}/balance-report.json, {full_selection['selected']}/full-pipeline-coverage.json, {full_selection['selected']}/validated-claims.json, {full_selection['selected']}/quarantined-claims.json, {full_selection['integrity']}, validation-results.json and the per-run requests/ directories.", '']
    (folder/'evaluation.md').write_text('\n'.join(lines))
    zh=[
        '# 最新双语样本测试与提示词修改结果','',
        '已完成新一轮采集、粗筛、当前代码的全量程序测试，以及中英文提取、核验和证据质量提示词的修改。结果仍有明确失败项，不能据此声称提示词已达到全局最佳。','',
        '## 数据','',
        f"本次新采集 {data['raw_records']:,} 条原始记录，粗筛、去重和语言纠错后保留 600 条，英文与简体中文各 300 条。沿用原有采集来源与语言模型配置；最终入选的全部是 Steam 用户评测，未包含楼中楼回复。",
        f"采集按最新顺序向前翻页补足数量。英文原始发表时间为 {data['created_at_range']['en']['min'][:10]} 至 {data['created_at_range']['en']['max'][:10]}，中文为 {data['created_at_range']['zh']['min'][:10]} 至 {data['created_at_range']['zh']['max'][:10]}（UTC）。因此它是新采集的数据集，并非全部近期发表，也未确认属于同一补丁。",
        f"[粗筛后 600 条原文]({args.data/'screened/records.jsonl'})；[采集与筛选统计]({args.data/'screened/summary.json'})。",'',
        '## 全量测试结果','',
        f"600 条全部进入现有默认完整流程；{s['agreement_related']} 条通过相关性判断。生成 {s['generated_claims']} 条结论，其中 {s['accepted_claims']} 条通过来源与模型语义核验，{s['quarantined_claims']} 条隔离；{s['final_generation_failed_comments']} 条评论生成失败。此外 52 条被相关性判断排除，23 条相关性尚未解决。自动核验通过不代表玩家观点或游戏机制已被证实。",
        '本轮通过 147 项代码测试和 20 项数据、引用与结果完整性检查。数值蕴含对照 4/4、数值提取 2/2、双语合成语义对照 8/8；这些是程序诊断，不是实际论坛准确率。',
        f"最终复跑对完全相同的模型请求重用 {transport['counts']['reused_identical_model_request']} 次原始响应，对发生变化的请求执行 {transport['counts']['fresh_inference']} 次新推理；所有响应都经过当前代码验证。请求、模型、提示词、数据摘要及重用来源均已保存。",'',
        '## 提示词修改及实际收益','',
        '提取提示词要求完整的主体与建议，区分“不削弱就退游”和“不要削弱”，约束攻击者与受害者归属，分离系统机制与角色意见，保留条件，禁止从辱骂、价格或游玩时长中捏造调整数值。核验提示词检查整个建议是否被原文支持；无可用数值时，解码结构也禁止空值数值参数。最终汇总由程序聚合，没有独立的自由文本总结模型提示词。',
        f"同配置下六个既有真实案例，修改前后均为 {final['passed']}/{final['total']} 通过。部分具体误判已修正，但总体通过数未提高；八条新数据诊断为 {new_diagnostics['passed']}/{new_diagnostics['total']}，也不是独立人工标注准确率。",
        '证据质量提示词另用四条真实开发样本进行验证：三条得到有效的主要分类及当前立场，一条因引用缺乏上下文而保留复核。全量 600 条沿用 evidence-quality=off 默认配置，并未完成 600 条额外质量标注；四条开发样本结果不能外推。',
        f"[修改后的英文提取提示词]({m.ROOT/'prompts/summarize-balance.en.txt'})、[中文提取提示词]({m.ROOT/'prompts/summarize-balance.zh.txt'})、[英文核验提示词]({m.ROOT/'prompts/verify-balance.en.txt'})、[中文核验提示词]({m.ROOT/'prompts/verify-balance.zh.txt'})。",'',
        '## 仍需复核的部分','',
        '两条长评论的全量生成失败均已保留。新增失败项在首轮的四条结论也全部被隔离，两轮都没有从它接受结论。补充重试不覆盖全量统计；详见失败审计及英文报告。复杂讽刺、上下文依赖的角色归属、补丁适用性和同模型核验的相关误差仍需人工复核。',
        '特别发现：新增失败项的补充重试虽然返回有效 JSON，但十条自动核验通过的意见仍错误地把世巡进度、通用斗气迸发或性能称赞归为隆的调整建议。逐条对照原文后，整个补充结果被标记为不采纳，未合并进主流程的 187 条结论。这说明模型核验会漏判，主流程的“通过”也不能视为独立验证的正确答案。',
        f"[完整实验报告与限制]({folder/'evaluation.md'})；[最终结构化汇总]({run/'balance-report.json'})；[通过核验的结论]({run/'validated-claims.json'})；[隔离结论]({run/'quarantined-claims.json'})；[失败审计]({folder/'generation-failure-audit.json'})。",'']
    (folder/'summary.zh.md').write_text('\n'.join(zh))
    print(folder/'evaluation.md')


if __name__=='__main__':main()
