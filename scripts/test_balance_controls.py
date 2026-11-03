"""Separate synthetic numeric-entailment controls; never community evidence."""
import argparse
from pathlib import Path
from run_balance_analysis import ROOT, Runner, ground_claim, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--base-url', default='http://127.0.0.1:11434')
    parser.add_argument('--num-gpu', type=int)
    args = parser.parse_args()
    prompts = {'verify': {language: (ROOT / f'prompts/verify-balance.{language}.txt').read_text()
                          for language in ('en', 'zh')}}
    runner = Runner(args.base_url, args.out, prompts)
    if args.num_gpu is not None:
        runner.runtime_options = {'num_gpu': args.num_gpu}
    results = []
    fixtures = [
        ('en', 'llama3.1:latest', True, "Please reduce Ryu's Hadoken damage from 600 to 500."),
        ('en', 'llama3.1:latest', False, "Ryu's Hadoken deals 600 damage; Ken's Hadoken deals 500 damage."),
        ('zh', 'qwen2.5:7b', True, '请将隆的波动拳伤害从600降到500。'),
        ('zh', 'qwen2.5:7b', False, '隆的波动拳伤害为600，肯的波动拳伤害为500。'),
    ]
    for i, (language, model, expected, text) in enumerate(fixtures, 1):
        identity = 'synthetic-numeric-control-' + str(i)
        claim = {'character': 'Ryu', 'target': 'Hadoken damage' if language == 'en' else '波动拳伤害',
            'direction': 'nerf', 'recommendation': 'Reduce Hadoken damage from 600 to 500.' if language == 'en' else '将波动拳伤害从600降到500。',
            'specificity': 'source_numeric', 'parameters': [{'metric': 'damage' if language == 'en' else '伤害',
                'current': '600', 'proposed': '500', 'delta': None, 'unit': None, 'evidence_id': 'E1'}],
            'evidence_ids': ['E1'], 'uncertain': False}
        row = {'record_id': identity, 'text_original': text, 'source_url': None}
        errors, enriched = ground_claim(claim, row, {'Ryu'})
        if errors and expected:
            raise ValueError('Control failed deterministic binding: ' + str(errors))
        envelope = {'claim_id': identity + ':1', 'comment_id': identity, 'model': model, 'claim': enriched}
        parsed, meta = runner.generate(model, language, 'verify',
            {'claims': [envelope], 'original_comment': text}, [envelope['claim_id']])
        observed = parsed['verdicts'][0]['supported'] if parsed else None
        support_status = parsed['verdicts'][0]['support_status'] if parsed else None
        expected_status = 'supported' if expected else 'unsupported'
        pipeline_supported = not errors and observed is True
        results.append({'kind': 'synthetic_control_not_community_evidence', 'language': language,
            'model': model, 'source': text, 'claim': enriched, 'expected_supported': expected,
            'observed_supported': observed, 'support_status': support_status,
            'expected_status': expected_status, 'source_gate_errors': errors,
            'pipeline_supported': pipeline_supported,
            'model_only_passed': support_status == expected_status,
            'passed': pipeline_supported is expected, 'request': meta})
    write_json(args.out / 'results.json', {'passed': sum(r['passed'] for r in results),
        'total': len(results), 'model_only_passed': sum(r['model_only_passed'] for r in results), 'cases': results,
        'limitation': 'Small synthetic diagnostic, not an independent accuracy benchmark; excluded from corpus counts.'})
    print(f"Numeric entailment controls: {sum(r['passed'] for r in results)}/{len(results)}", flush=True)


if __name__ == '__main__':
    main()
