"""Entry point for the request metrics and claim outcomes of a run (aimediator.measurement)."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.common import write
from aimediator.measurement import claim_outcomes, request_metrics


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True, help='CLI, legacy or archived run folder (read only)')
    parser.add_argument('--out', type=Path, required=True, help='JSON output file')
    args = parser.parse_args(argv)
    if not (args.run / 'requests').is_dir():
        parser.error('Run folder has no requests directory')
    write(args.out, {'request_metrics': request_metrics(args.run), 'claim_outcomes': claim_outcomes(args.run)})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
