"""Synthetic fixture run at scale: wall time and the profiled share of run_store.state.

Reproduces the setup of the code restructuring's step B5.9 (pipeline upgrade
target T9): the packaged fixture cases are copied under new IDs
(`<record_id>:copy-NN`, with the annotation's `comment_id` set to the same ID)
up to the requested number of comments, a fixture transport answers from
those annotations, and `operations.analyze` runs with `stop_after` `full`, as
the demo runs it. No network and no model. Prints one JSON line.
"""
import argparse
import copy
import cProfile
import json
from pathlib import Path
import pstats
import sys
import tempfile
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.common import Failure, canonical, read
from aimediator.config import defaults
from aimediator.fixture_transport import FixtureTransport
from aimediator.operations import analyze
from aimediator.resources import asset_path


def scaled_cases(count):
    """Return `count` copies of the packaged fixture cases, copy-major, each under a new record ID."""
    cases = read(asset_path('fixtures/cases.json'))
    result = []
    for index in range(count):
        case = copy.deepcopy(cases[index % len(cases)])
        new_id = '%s:copy-%02d' % (case['source']['record_id'], index // len(cases))
        case['source']['record_id'] = new_id
        case['annotation']['comment_id'] = new_id
        result.append(case)
    return result


class ScaledFixtureTransport(FixtureTransport):
    """The packaged fixture transport, answering from the copied cases."""

    def __init__(self, cfg, cases):
        super().__init__(cfg)
        self.cases = cases
        self.annotations = {c['source']['record_id']: c['annotation'] for c in cases}
        self.originals = {c['source']['record_id']: c['source'] for c in cases}


def state_profile(profile):
    """Return the profiled total seconds, and the calls and cumulative seconds of run_store.state."""
    stats = pstats.Stats(profile)
    calls, cumulative = 0, 0.0
    for (filename, _, name), (_, primitive, _, inclusive, _) in stats.stats.items():
        if name == 'state' and Path(filename).name == 'run_store.py':
            calls, cumulative = primitive, inclusive
    return stats.total_tt, calls, cumulative


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--comments', type=int, default=600, help='number of synthetic comments (default 600)')
    parser.add_argument('--mode', choices=['off', 'shadow', 'enforce'], default='shadow')
    parser.add_argument('--out', type=Path, required=True, help='new run folder')
    parser.add_argument('--no-profile', action='store_true', help='measure plain wall time without cProfile')
    args = parser.parse_args(argv)
    if args.comments < 1:
        parser.error('--comments must be positive')
    cases = scaled_cases(args.comments)
    cfg = defaults()
    cfg.update(evidence_quality=args.mode, base_url='http://fixture.invalid')
    transport = ScaledFixtureTransport(cfg, cases)
    profile = None if args.no_profile else cProfile.Profile()
    exit_code = 0
    with tempfile.TemporaryDirectory() as temp:
        dataset = Path(temp) / 'synthetic-input.jsonl'
        dataset.write_bytes(b''.join(canonical(c['source']) + b'\n' for c in cases))
        start = time.perf_counter()
        if profile is not None:
            profile.enable()
        try:
            analyze(dataset, args.out, cfg, transport=transport, quiet=True)
        except Failure as exc:
            exit_code = exc.code
        finally:
            if profile is not None:
                profile.disable()
        wall = time.perf_counter() - start
    requests = {path.name: sum(1 for _ in path.iterdir())
                for path in sorted((args.out / 'requests').iterdir()) if path.is_dir()}
    result = {'comments': args.comments, 'mode': args.mode, 'exit_code': exit_code,
              'run_state': read(args.out / 'run-state.json')['run_state'], 'requests': requests,
              'wall_seconds': round(wall, 3), 'profiled': profile is not None}
    if profile is not None:
        total, calls, cumulative = state_profile(profile)
        result.update(profiled_seconds=round(total, 3), state_calls=calls,
                      state_seconds=round(cumulative, 3), state_share=round(cumulative / total, 4))
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
