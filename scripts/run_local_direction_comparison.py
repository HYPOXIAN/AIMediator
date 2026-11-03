"""Compatibility entry point for the full-corpus, evidence-audited balance pipeline.

Replaces the historical 32-comment character-name-only experiment. Original
reports are not modified. New runs use bilingual prompts and all routed records.
"""
import argparse
from pathlib import Path
from run_balance_analysis import ROOT, run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', choices=['qwen2.5:7b', 'llama3.1:latest'])
    parser.add_argument('--run-name', default='local-direction-comparison')
    parser.add_argument('--dataset', type=Path, default=ROOT / 'data/raw/feedback/20261015-expanded/screened/records.jsonl')
    parser.add_argument('--base-url', default='http://127.0.0.1:11434')
    parser.add_argument('--embedding-model', default='qwen3-embedding:8b')
    args = parser.parse_args()
    if Path(args.run_name).name != args.run_name or args.run_name in ('.', '..'):
        parser.error('Invalid run name')
    args.out = ROOT / 'runs' / args.run_name
    run(args)


if __name__ == '__main__':
    main()
