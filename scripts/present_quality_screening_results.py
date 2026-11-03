"""Verify and present a completed local-model screening experiment without inference."""
import argparse
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
from pathlib import Path

import evidence_quality as q
import run_balance_analysis as m
from run_quality_screening_experiment import classify

NAMES = {'opinion_only': '一般意见统计', 'mechanism_evidence': '角色机制候选',
         'system_evidence': '系统反馈', 'exclude': '剔除', 'review': '待复核'}
REASONS = {'invalid_annotation': '标注未通过校验', 'uncertain_information': '信息或归属存在不确定性',
           'separate_system_scope': '独立的系统平衡反馈', 'missing_character_context': '缺少角色上下文',
           'general_not_mechanism': '一般意见，不构成具体机制证据',
           'concrete_character_information': '包含具体角色信息', 'unresolved_fragment': '片段仍需复核',
           'no_balance_information': '不含可用于平衡分析的信息', 'empty_content': '内容为空',
           'quality_attempts_exhausted': '模型尝试未通过完整性或标注校验'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--canvas', type=Path, required=True)
    args = parser.parse_args()
    folder = args.run.resolve()
    read = lambda name: json.loads((folder / name).read_text())
    rows, summary, manifest = read('all-classifications.json'), read('summary.json'), read('manifest.json')
    sources = {r['record_id']: r for r in read('source-snapshot.json')}
    expected_ids = manifest['identity']['comment_ids']
    assert [r['comment_id'] for r in rows] == expected_ids
    assert len(set(expected_ids)) == len(rows) == summary['input_comments']
    fragment_counts = Counter()
    eligible = []
    for row in rows:
        original = sources[row['comment_id']]['text_original']
        assert row['text_original'] == original
        assert row['content_sha256'] == hashlib.sha256(original.encode()).hexdigest()
        recomputed = classify(sources[row['comment_id']], row['relevance_record'], row.get('quality_record'))
        assert all(row[key] == value for key, value in recomputed.items())
        record = row.get('quality_record')
        if record and record['status'] == 'completed':
            checked = q.qualify(record['annotation'], sources[row['comment_id']], m.evidence_units(original), manifest['identity']['policy'])
            assert checked['errors'] == []
            assert checked['routing'] == record['routing']
            assert checked['emotion_ratio'] == record['emotion_ratio']
        for kind in ('retained_fragments', 'excluded_fragments', 'review_fragments'):
            for fragment in row[kind]:
                fragment_counts[kind] += 1
                for segment in fragment['segments']:
                    assert segment.get('quote', segment.get('text')) == original[segment['start']:segment['end']]
                if kind == 'retained_fragments':
                    assert row['decision'] == 'retained'
                    eligible.append({'comment_id': row['comment_id'], 'language': row['language'],
                        'source_url': row['source_url'], 'content_sha256': row['content_sha256'],
                        'route': fragment['route'], 'reason': fragment['reason'], 'point': fragment.get('point'),
                        'segments': fragment['segments']})
    counts = dict(Counter(r['decision'] for r in rows))
    assert all(counts.get(k, 0) == v for k, v in summary['mutually_exclusive_comment_counts'].items())
    for decision in ('retained', 'excluded', 'review'):
        assert read(decision + '-comments.json') == [r for r in rows if r['decision'] == decision]
    (folder / 'retained-fragments.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in eligible))
    lines = ['# 剔除片段', '', '这里包括保留评论中被单独剔除的内容。整条剔除的数据另见 excluded-comments.md。', '']
    for row in rows:
        for fragment in row['excluded_fragments']:
            lines += ['## ' + row['comment_id'], '', '整条评论状态：' + row['decision'], '',
                      '原因：' + REASONS.get(fragment['reason'], fragment['reason']), '']
            for seg in fragment['segments']:
                lines += [f"原文位置 [{seg['start']},{seg['end']})", '', '> ' + seg.get('quote', seg.get('text', '')).replace('\n', '\n> '), '']
    (folder / 'excluded-fragments.md').write_text('\n'.join(lines) + '\n')
    for filename in ('retained-comments.md', 'excluded-comments.md', 'review-comments.md'):
        path = folder / filename
        rendered = path.read_text()
        for route_name in NAMES.values():
            for code, label in REASONS.items():
                rendered = rendered.replace('\n' + route_name + '；原因：' + code + '\n',
                                            '\n' + route_name + '；原因：' + label + '\n')
        path.write_text(rendered)
    stamp = datetime.now(ZoneInfo('America/Los_Angeles')).isoformat()
    verification = {'verified_at': stamp, 'input_count': len(rows), 'comment_counts': counts,
                    'fragment_item_counts': dict(fragment_counts), 'eligible_fragment_items': len(eligible),
                    'checks': ['exact_id_order_and_unique_coverage', 'original_text_and_sha256_unchanged',
                               'all_fragment_quotes_match_original_offsets', 'exported_groups_match_classifications', 'completed_annotations_and_routing_revalidated',
                               'classifications_recomputed_from_original_source'],
                    'quality_failed_comment_ids': [r['comment_id'] for r in rows if r['quality_status'] == 'failed']}
    (folder / 'delivery-verification.json').write_text(json.dumps(verification, ensure_ascii=False, indent=2) + '\n')
    c = summary['mutually_exclusive_comment_counts']
    report = f'''# 项目既有 100 条评论筛选实验结果

完成时间：{stamp}（America/Los_Angeles）。

本次沿用原实验的 100 条中英文真实评论组及历史相关性筛选结果，使用本地 Llama 3.1（英文）和 Qwen 2.5 7B（中文）补完证据质量筛选。恢复时使用单请求串行运行。

- 保留：{c['retained']} 条。
- 整条剔除：{c['excluded']} 条，其中历史相关性筛选剔除 {summary['inherited_relevance_excluded']} 条，本次质量筛选新增剔除 {summary['new_quality_excluded']} 条。
- 待复核：{c['review']} 条，其中模型尝试未通过校验 {summary['quality_failed_review']} 条。
- 部分保留的评论：{summary['partial_retained_comments']} 条；只有其中的保留片段可用于后续分析。
- 进入质量评估 {summary['quality_assessed']} 条，模型标注通过校验 {summary['quality_completed']} 条。
- 可用保留信息项：{len(eligible)} 项；单独剔除片段项：{summary['excluded_fragment_items']} 项。

## 分别查看数据

- [保留评论及保留片段](retained-comments.md)，原始结构数据见 retained-comments.json / retained-comments.jsonl。
- [整条剔除的数据及原因](excluded-comments.md)，原始结构数据见 excluded-comments.json / excluded-comments.jsonl。
- [单独剔除的片段](excluded-fragments.md)，原始结构数据见 excluded-fragments.json。
- [待复核的数据及原因](review-comments.md)，原始结构数据见 review-comments.json / review-comments.jsonl。
- retained-fragments.jsonl 只包含可用于后续分析的保留信息项及其原文片段，避免把保留评论的完整原文误当作全部合格。

## 解释边界

保留的用途分为一般意见统计、角色机制候选和系统反馈。角色机制候选尚未经过新的事实核验、版本确认或设计审查，不能直接视为机制事实或调整方案。情绪强烈本身不作为剔除条件。

这次是沿用冻结相关性结果的质量筛选实验，并非重新运行完整检索流程。该组是既有分层抽样代理银标组，特意包含历史失败案例，筛选比例不能代表全量语料。银标未用于本次模型判断；没有独立人工真值，因此不报告准确率。待复核数据单独保存，没有计入剔除。

原文和引用位置已逐项核对，100 条输入完整覆盖、无重复、三组互斥，验证记录见 delivery-verification.json。模型请求、原始响应和校验记录保留在 requests/quality/。
'''
    if summary.get('recovery_protocol'):
        report += ('\n## 恢复协议说明\n\n本次使用精简引用标注协议，原有质量校验没有放宽。复用父实验中校验通过的 '
                   + str(summary['imported_quality_completed']) + ' 条标注，其余进入质量阶段的数据通过本地模型重新评估。'
                   + '精简提示词和传输格式与原实验不同；不能视为原模型输出的逐位重现。父实验完整保留，协议和来源详见 manifest.json 与 RECOVERY.md。\n')
    (folder / 'RESULTS.md').write_text(report)
    compact = []
    for r in rows:
        record = r.get('quality_record') or {}
        compact.append({k: r[k] for k in ('comment_id', 'language', 'decision', 'decision_stage', 'reason',
                         'source_url', 'text_original', 'partial', 'quality_status', 'retained_fragments',
                         'excluded_fragments', 'review_fragments')} | {'emotion_ratio': record.get('emotion_ratio'),
                         'errors': record.get('errors', [])})
    for row in compact:
        for key in ('retained_fragments', 'excluded_fragments', 'review_fragments'):
            row[key] = [{'route': f['route'], 'reason': f['reason'], 'segments': [
                {'start': s['start'], 'end': s['end'], 'quote': s.get('quote', s.get('text', ''))}
                for s in f['segments']]} for f in row[key]]
    code = TEMPLATE.replace('__ROWS__', json.dumps(compact, ensure_ascii=False)).replace('__SUMMARY__', json.dumps(summary, ensure_ascii=False)).replace('__REASONS__', json.dumps(REASONS, ensure_ascii=False)).replace('__RUN_NAME__', json.dumps(folder.name, ensure_ascii=False)).replace('__RECOVERY_NOTE__', json.dumps(('精简标注恢复版：沿用原质量校验，复用 '+str(summary.get('imported_quality_completed', 0))+' 条已校验旧标注；其余进入质量阶段的数据由本地模型重新评估。原实验另行保留。') if summary.get('recovery_protocol') else '', ensure_ascii=False))
    args.canvas.write_text(code)
    print(json.dumps(verification, ensure_ascii=False, indent=2))


TEMPLATE = '''import { Stack, Row, H1, H2, H3, Text, Stat, Pill, TextInput, Select, Divider, Callout, Link, useState, useHostTheme } from "cursor/canvas";
type Segment = {start:number;end:number;quote?:string;text?:string};
type Fragment = {route:string;reason:string;segments:Segment[]};
type CommentRow = {comment_id:string;language:string;decision:string;decision_stage:string;reason:string;source_url:string|null;text_original:string;partial:boolean;quality_status:string;retained_fragments:Fragment[];excluded_fragments:Fragment[];review_fragments:Fragment[];emotion_ratio:number|null;errors:string[]};
const rows: CommentRow[] = __ROWS__;
const runName = __RUN_NAME__;
const recoveryNote = __RECOVERY_NOTE__;
const summary = __SUMMARY__;
const reasons: Record<string,string> = __REASONS__;
const names: Record<string,string> = {opinion_only:"一般意见统计", mechanism_evidence:"角色机制候选", system_evidence:"系统反馈", exclude:"剔除", review:"待复核"};
const decisions: Record<string,string> = {retained:"保留",excluded:"整条剔除",review:"待复核"};
export default function ScreeningResults() {
  const theme = useHostTheme();
  const [group,setGroup] = useState("retained");
  const [query,setQuery] = useState("");
  const [language,setLanguage] = useState("all");
  const [selected,setSelected] = useState("");
  const filtered = rows.filter(r => r.decision === group && (language === "all" || r.language === language) && (r.text_original + r.comment_id).toLowerCase().includes(query.toLowerCase()));
  const active = filtered.find(r => r.comment_id === selected) || filtered[0];
  return <Stack gap={20} style={{padding:24,maxWidth:1400,margin:"0 auto",color:theme.text.primary}}>
    <Stack gap={6}><H1>既有评论数据 · 筛选结果</H1><Text>{rows.length===100?"100 / 100 条已完成":"阶段性结果："+rows.length+" / 100 条已归类；其余尚未处理，当前数字并非最终结果。"}</Text><Text>项目既有 100 条中英文评论；冻结历史相关性结果，本地模型补完质量筛选。来源：{runName}。</Text></Stack>
    <Row gap={32} wrap><Stat value={summary.mutually_exclusive_comment_counts.retained} label="保留评论 / 条"/><Stat value={summary.mutually_exclusive_comment_counts.excluded} label="整条剔除 / 条"/><Stat value={summary.mutually_exclusive_comment_counts.review} label="待复核 / 条"/><Stat value={summary.partial_retained_comments} label="其中部分保留 / 条"/></Row>
    <Callout title="保留范围">只有“保留片段”可用于后续分析。机制内容仍是候选；待复核内容没有计入剔除。情绪强烈本身不作为剔除条件。</Callout>
    <Row gap={8} wrap>{Object.entries(decisions).map(([key,label])=><div key={key}><Pill active={group===key} onClick={()=>{setGroup(key);setSelected("");}}>{label} · {rows.filter(r=>r.decision===key).length}</Pill></div>)}<Select value={language} onChange={setLanguage} options={[{value:"all",label:"全部语言"},{value:"en",label:"英文"},{value:"zh",label:"中文"}]}/><TextInput value={query} onChange={setQuery} placeholder="搜索评论原文或 ID" style={{minWidth:240}}/></Row>
    {filtered.length > 0 && <div style={{display:"grid",gridTemplateColumns:"minmax(220px, 30%) minmax(0, 1fr)",gap:24,alignItems:"start"}}>
      <Stack gap={0} style={{maxHeight:"75vh",overflow:"auto",borderTop:`1px solid ${theme.stroke.tertiary}`}}>{filtered.map(r=><button key={r.comment_id} onClick={()=>setSelected(r.comment_id)} style={{textAlign:"left",padding:"12px 10px",border:0,borderBottom:`1px solid ${theme.stroke.tertiary}`,background:active?.comment_id===r.comment_id?theme.fill.secondary:"transparent",color:theme.text.primary,cursor:"pointer"}}><div style={{fontSize:12,color:theme.text.secondary,marginBottom:6}}>{r.comment_id} · {r.language.toUpperCase()}{r.partial?" · 部分保留":""}</div><div style={{fontSize:13,lineHeight:1.6}}>{r.text_original.slice(0,110)}{r.text_original.length>110?"…":""}</div></button>)}</Stack>
      {active && <Stack gap={14}>
        <H2>{active.comment_id}</H2><Text>{decisions[active.decision]} · {active.decision_stage === "quality"?"质量筛选":"历史相关性筛选"} · {active.reason}</Text>
        {active.source_url && <Link href={active.source_url}>查看来源</Link>}
        <H3>完整原文</H3><div style={{whiteSpace:"pre-wrap",lineHeight:1.8,fontSize:14,padding:16,background:theme.fill.tertiary,overflowWrap:"anywhere"}}>{active.text_original}</div>
        {typeof active.emotion_ratio === "number" && <Text>纯情绪篇幅：{(active.emotion_ratio*100).toFixed(1)}%（按原文有效字符权重计算，仅作诊断，不决定证据权重）</Text>}
        {([ ["retained_fragments","保留片段"],["excluded_fragments","剔除片段"],["review_fragments","待复核片段"] ] as const).map(([key,title])=>active[key].length>0 && <div key={key} style={{display:"flex",flexDirection:"column",gap:10}}><Divider/><H3>{title}</H3>{active[key].map((f,index)=><div key={index} style={{display:"flex",flexDirection:"column",gap:6}}><Text>{names[f.route]} · {reasons[f.reason]||f.reason}</Text>{f.segments.map((s,i)=><div key={i} style={{borderLeft:`2px solid ${key==="retained_fragments"?theme.accent.primary:theme.stroke.primary}`,paddingLeft:12,whiteSpace:"pre-wrap",lineHeight:1.75,fontSize:14,overflowWrap:"anywhere"}}><div style={{fontSize:11,color:theme.text.tertiary}}>[{s.start}, {s.end})</div>{"quote" in s?s.quote:("text" in s?s.text:"")}</div>)}</div>)}</div>)}
        {active.errors.length>0 && <Callout title="模型校验未通过">{active.errors.join("；")}</Callout>}
      </Stack>}
    </div>}
    {recoveryNote && <Text>{recoveryNote}</Text>}
    <Divider/><Text>本地模型：英文 Llama 3.1，中文 Qwen 2.5 7B。质量评估 {summary.quality_assessed} 条；标注通过 {summary.quality_completed} 条；未通过 {summary.quality_failed_review} 条。历史相关性剔除 {summary.inherited_relevance_excluded} 条；本次质量筛选新增剔除 {summary.new_quality_excluded} 条。本组分层抽样且包含历史失败案例，比例不代表全量语料；未进行人工真值准确率评估。</Text>
  </Stack>;
}
'''

if __name__ == '__main__':
    main()
