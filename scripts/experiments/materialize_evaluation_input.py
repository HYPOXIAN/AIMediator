"""Entry point for the input JSONL of an evaluation set (aimediator.measurement).

The output holds the raw dataset rows unchanged, so it is JSONL bytes and not a
JSON document; it is written through a temporary file and replaced atomically.
"""
import argparse
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.measurement import materialize


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--set', type=Path, required=True, help='evaluation set directory under data/evaluation/')
    parser.add_argument('--dataset', type=Path, required=True, help='raw dataset JSONL the set was drawn from')
    parser.add_argument('--split', help='only the rows of this split')
    parser.add_argument('--out', type=Path, required=True, help='JSONL output file')
    args = parser.parse_args(argv)
    data = materialize(args.set, args.dataset, args.split)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    temp = args.out.with_name(args.out.name + '.tmp')
    with temp.open('wb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    temp.replace(args.out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
