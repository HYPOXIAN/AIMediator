# Reorganization Change Record

- Type: Record
- Status: Draft
- Updated: 2026-11-03
- Applies to: baseline commit `0d390c4` and later; `RULES.md` v1.0

The single change record for the whole reorganization
([plan](../plans/reorganization.md), section 0, item 4). Every phase appends
to it. Deletions of non-reproducible content are entered here (G6). The
record is frozen when the reorganization is finished (P5).

## P0 Baseline (2026-11-03)

- **Baseline commit**: `0d390c4` on `main`, "chore: baseline snapshot before
  reorganization", 175 tracked files. Large data stays ignored; `.env` is not
  tracked. Before this, `.git/` was an empty directory.
- **Pre-commit checks** run before the baseline commit: a credential pattern
  scan and a comparison of `.env` values against the files to be tracked.
  Neither produced a hit.
- **Backup**: `~/Archives/AIMediator/20261103-baseline/`, containing
  `workspace/` (the full workspace), `SHA256SUMS` (20,989 files), `SYMLINKS.txt`
  (18 symlinks, not in `SHA256SUMS`) and `README.txt`. Excluded: `.env`
  (credentials, G9), `.git`, `build/`, `__pycache__/`, `*.egg-info`
  (reproducible).
- **Backup verification**: compared one by one against the original files at
  creation, with a matching result. Re-verified on 2026-11-03 during batch 1
  with `sha256sum -c --quiet ../SHA256SUMS` run from `workspace/`: all 20,989
  files OK (exit status 0). `SHA256SUMS` has no `.env` entry.
- **Backup limitation**: btrfs reflink copy on the same disk as the project.
  It protects against accidental deletion or overwrite, not against disk
  failure. No off-site copy will be made (plan, section 7, decision 3).
- **Test baseline**: 192 offline tests pass
  (`python3 -m unittest discover -s tests -q`). Recorded in RULES.md P4.
- **Durable planning copies** used by batch 1 before the rules entered the
  project: `~/Archives/AIMediator/planning/` (`RULES.md`,
  `reorganization-plan.zh.md`, `rules-review.zh.md`).

## P1 Rules in place and the check tool (batch 1, 2026-11-03)

Entry check: working tree clean, `HEAD` at `0d390c4`, 192 tests passing.

Batch 1 only adds files; it moves, deletes and renames nothing.

### Changes

- `RULES.md` copied verbatim from the planning copy (byte-identical, checked
  with `cmp`).
- `docs/plans/reorganization.md`: English translation of the approved
  Chinese plan, with a D2 header added. It is the basis for batches 2 to 4.
- `CLAUDE.md`: references `RULES.md`, lists common commands and states that
  agents do not sign their work. No rules of its own (G1).
- `.env.example`: the four key names from `.env`, without values, produced
  from the key column only (G9).
- `.gitignore`: `runs/` added.
- `docs/reference/compatibility-layers.md`: compatibility register (G2).

### Compatibility layer inventory

Measured with `find . -type l` (excluding `.git/`) and a search for the
docstring "Compatibility entry point":

- 18 symlinks, all tracked, matching the plan and the backup's
  `SYMLINKS.txt`: 3 in `configs/`, 1 in `data/`, 14 in `prompts/`, all
  pointing into `src/aimediator/assets/`.
- **7 forwarding scripts, against 6 in the plan.** Six are pure forwarders
  (`balance_policy.py`, `evaluate_evidence_quality.py`, `evidence_quality.py`,
  `glossary_vectors.py`, `review_balance_sources.py`,
  `run_balance_analysis.py`). The seventh,
  `scripts/run_local_direction_comparison.py`, carries the same docstring but
  is a wrapper with its own arguments around `run_balance_analysis.run`. All
  seven are registered, so the register covers 25 layers, not 24.

All layers are registered only; none was removed (decision Q4).
