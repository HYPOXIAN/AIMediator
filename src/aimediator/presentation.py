"""Business-only output for the demonstration launcher; CLI contracts stay intact."""
from collections import Counter
import contextlib
import io
import json
from pathlib import Path
import sys

from .cli import main as cli_main
from .common import read


def optional(folder, name, default):
    path = folder / name
    return read(path) if path.exists() else default


def claim_view(claim):
    return {key: claim[key] for key in (
        'comment_id', 'character', 'target', 'direction', 'recommendation',
        'specificity', 'parameters', 'evidence') if key in claim}


def run_results(folder):
    folder = Path(folder)
    state = read(folder / 'run-state.json')
    config = read(folder / 'resolved-config.json')
    sources = read(folder / 'source-snapshot.json')
    relevance = optional(folder, 'relevance.json', [])
    quality = optional(folder, 'evidence-quality.json', [])
    claims = optional(folder, 'validated-claims.json', [])
    report = optional(folder, 'balance-report.json', {})
    groups = [{key: group[key] for key in (
        'character', 'direction', 'topic', 'supporting_comment_count', 'comment_ids') if key in group}
        for group in report.get('character_adjustments', [])]
    return {
        '提取结果': [claim_view(claim) for claim in claims],
        '相关性测试': {
            '输入评论': len(sources),
            '语言分布': dict(Counter(row['language'] for row in sources)),
            '已有判定': len(relevance),
            '通过': sum(bool(row.get('agreement')) for row in relevance),
            '未通过或待定': sum(not row.get('agreement') for row in relevance),
            '准确率': None,
        },
        '质量测试': {
            '模式': config['evidence_quality'],
            '已评估': len(quality),
            '完成': sum(row['status'] == 'completed' for row in quality),
            '失败': sum(row['status'] == 'failed' for row in quality),
            '分流评论数': {route: sum(route in row.get('routes_present', []) for row in quality)
                           for route in ('mechanism_evidence', 'opinion_only', 'system_evidence', 'review', 'exclude')},
            '准确率': None,
        },
        '最终结论': {
            '分析完成': state['run_state'] == 'completed' and config['stop_after'] == 'full',
            '运行状态': state['run_state'],
            '已验证主张数': len(claims),
            '调整建议': groups,
            '结果范围': '仅采集样本；自动审核，未建立独立人工准确率，需来源复核。',
            '合成示例': read(folder / 'manifest.json')['execution_provenance'] == 'agent_authored_synthetic_fixture_transports',
        },
    }


def report_results(path):
    report = read(path)
    topics = []
    for group in report['topics']:
        topics.append({
            '角色': group['character'], '主题': group['topic_literal_normalized'],
            '方向': {direction: {
                '支持评论数': data['supporting_comment_count'],
                '建议': [claim_view(claim) for claim in data['recommendations']],
            } for direction, data in group['directions'].items() if data['supporting_comment_count']},
        })
    return {'最终结论': {
        '分析完成': not report['partial'] and report['processing_summary'].get('mode') == 'full_pipeline',
        '运行状态': report['run_state'],
        '正式主张数': report['counts']['formal_claims'], '调整建议': topics,
        '未归并主张': [claim_view(claim) for claim in report['unresolved_identity_or_target_claims']],
        '结果范围': '仅采集样本；自动审核，未建立独立人工准确率，需来源复核。',
        '合成示例': report['execution_provenance'] == 'agent_authored_synthetic_fixture_transports',
    }}


def present(result):
    artifacts = result['artifacts']
    command = result['command']
    if command == 'analyze':
        path = artifacts.get('run') or artifacts.get('saved_output')
        return run_results(path) if path else None
    if command == 'report':
        return report_results(artifacts['json'])
    if command == 'evaluate quality':
        evaluation = read(artifacts['evaluation'])
        return {'质量测试': {key: evaluation[key] for key in (
            'labeled_comments', 'unlabeled_comments', 'groups', 'independent_effectiveness_established')}}
    if command == 'demo':
        results = {mode: run_results(Path(artifacts['demo']) / mode)
                   for mode in ('off', 'shadow', 'enforce')}
        return {section: {mode: value[section] for mode, value in results.items()}
                for section in ('提取结果', '相关性测试', '质量测试', '最终结论')}
    return None


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    # Use the same commands, validation, exit codes and files. Only presentation
    # changes: routine progress, help/version and operational envelopes stay off screen.
    informational = any(flag in argv for flag in ('--help', '-h', '--version'))
    if not informational:
        for flag in ('--quiet', '--json'):
            if flag not in argv:
                argv.append(flag)
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        try:
            code = cli_main(argv)
        except SystemExit as exc:
            return exc.code
    if informational:
        return code
    result = json.loads(output.getvalue())
    if code:
        print('aimediator: ' + result['error_message'], file=sys.stderr)
    # Partial results are useful, but must retain their incomplete status.
    if code in (0, 5, 130):
        value = present(result)
        if value:
            print(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
