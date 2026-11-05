"""Entry point for the (character, direction) position scores of a run (aimediator.measurement)."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.common import write
from aimediator.measurement import score_positions


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True, help='run folder (read only)')
    parser.add_argument('--labels', type=Path, required=True, help='evaluation set directory holding labels.jsonl')
    parser.add_argument('--split', help='score only the labels of this split')
    parser.add_argument('--out', type=Path, required=True, help='JSON output file')
    args = parser.parse_args(argv)
    write(args.out, score_positions(args.run, args.labels, args.split))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
