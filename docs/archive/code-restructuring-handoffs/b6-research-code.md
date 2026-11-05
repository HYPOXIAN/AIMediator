# Handoff B6: Research code: workspace root, collection, shared helpers

- Type: Agent handoff
- Status: Archived
- Updated: 2026-11-04
- Applies to: [code restructuring plan](../code-restructuring.md) batch B6; entry tag `restructure-b5`
- Archived 2026-11-04 when the code restructuring was completed (tag `restructure-done`).

Work order for batch B6. The steps are defined in plan section 7 (B6). The
contracts (`resources.workspace_root`, `collection`, `design_briefs`,
`diagnostics`) and the research-script rules are in
[blueprint](../code-restructuring-blueprint.md) sections 3.3 and 3.6.

## 1. Mission

- Give the project one root (CR-D09).
- Move the collectors into `aimediator.collection`, leaving thin entry
  scripts (CR-D01).
- Extract the research logic that several scripts and tests share into
  `aimediator.design_briefs` and `aimediator.diagnostics` (CR-D02).

Script flags, defaults, outputs and request bytes stay unchanged.

## 2. Entry conditions

- Tag `restructure-b5` exists, and the B5-V note says "accepted".
- Clean tree, no `WIP Step` stash. The gates pass.

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/|scripts/collect/|scripts/experiments/|tests/|docs/records/[0-9]{8}-code-restructuring\.md$)
```

- **Allowed**:
  - `resources.py`, `engine.py` and `glossary_vectors.py` (root only);
  - the new `collection/` subpackage and the `design_briefs` and
    `diagnostics` modules;
  - the scripts in `collect/` and `experiments/`;
  - tests;
  - the L4 lock harness import (not the fixture).
- **Not allowed**:
  - collector behavior: endpoints, host allowlist, budgets, cooldowns, the
    User-Agent, output files, default paths;
  - the screening rules;
  - experiment output formats;
  - the lock fixture;
  - documents other than the change record;
  - the CLI path modules, except the import of `workspace_root`.
- **Decisions in force**: CR-D01, CR-D02 and CR-D09.
- **Owner actions**: none.

## 4. Sessions

### B6-1 (implementation): steps B6.1 and B6.2

### B6-2 (implementation): steps B6.3 and B6.4

Both sessions use this prompt, with their own session ID and step range:

```text
You are session B6-<k> (implementation) of the AIMediator code restructuring,
steps <first> to <last>.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/code-restructuring-handoffs/b6-research-code.md); the blueprint
docs/plans/code-restructuring-blueprint.md, sections 3.3, 3.6, 4, 5 and 6;
the plan docs/plans/code-restructuring.md, sections 1, 2, 4, 8 and the B6
part of section 7; the change record.
Task: execute your steps in order, inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates after every commit.
- One kind of operation per commit, with "Step: B6.x" and the decision ID
  in the body. B6.2 is a series of commits.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **B6.1** `resources.workspace_root()` follows blueprint section 3.3.
  - For testability, put the marker check in a private helper that takes the
    candidate directory, and test both branches.
  - Users:
    - `engine.ROOT`;
    - `glossary_vectors.ROOT` and `DEFAULT_INDEX`;
    - every `ROOT = Path(__file__).resolve().parents[2]` in
      `scripts/collect/` and `scripts/experiments/`, which keeps its
      bootstrap line;
    - `STATE` in the collectors (`workspace_root() / 'runs/state'`);
    - `run_grounded_feedback_live.py`.
  - Verify from a foreign directory:
    `python3 -c "import sys; sys.path.insert(0, '<checkout>/src'); from aimediator import engine; print(engine.ROOT)"`
    prints the checkout path, and plan 8.5 passes.
  - Plan 8.7, fourth grep, prints nothing.
- **B6.2** Series of commits, one module at a time, in this order:
  `screening`, `client`, `store`, `sources`, `export`, `balanced`,
  `expansion`. Then a commit that makes the scripts thin, then the test
  migration.
  - **Mapping**:
    - `screen_feedback.py` (regular expressions, `classify_rules`,
      `classify`, `load_sources`, `write_rows`, `main`) goes to
      `screening`;
    - `collect_feedback.py`:
      - `HOSTS`, `load_youtube_key`, `utc_now`, `retry_delay`, `Halt`,
        `RestrictedRedirect` and `Client` go to `client`;
      - `Store` goes to `store`;
      - `guess_language`, `timestamp`, `steam`, `bluesky`, `youtube` and
        `main` go to `sources`;
      - `export` goes to `export`;
    - `collect_balanced_feedback.py` (`reviewed_rows`, `retained`,
      `select_balanced`, `main`) goes to `balanced`;
    - `expand_feedback.py` (`kept_counts`, `main`) goes to `expansion`.
  - **Writers**: `write_json` becomes `common.write`. The output bytes are
    the same for finite data: the same indentation, `ensure_ascii=False`,
    and a final newline. Confirm this on a fixture before switching.
  - **Thin scripts**: the docstring begins "Entry point for ...", never
    "Compatibility entry point", which the rule check would flag (G2). Then
    the bootstrap, then `raise SystemExit(main())`.
  - **Meaning change**: the screening summary's `script_sha256` now hashes
    `collection/screening.py`, because `Path(__file__)` moved with the code.
    Record this.
  - **Tests**: `test_collect_feedback`, `test_screen_feedback`,
    `test_balanced_collection` and `test_expand_feedback` import the
    package. Patches of `m.time`, `m.os`, `m.dt` or `m.ZoneInfo` now target
    the module that uses the name (for example
    `aimediator.collection.client.time`).
  - **Lock**: the L4 harness imports `aimediator.collection.screening`, and
    the digest is unchanged.
  - **Wheel**: `python3 -m zipfile -l <wheel>` lists
    `aimediator/collection/` and nothing under `data/raw`.
- **B6.3**
  - Move `validate_move_data`, `quality_design_errors` and `prepare_briefs`
    unchanged. Run the move check (plan 8.6) with the script as the old
    file.
  - `prepare_balance_design.py` keeps `main()`.
  - `check_balance_regressions.py`, `review_balance_live.py`,
    `test_balance_review_pipeline.py` and `test_evidence_quality.py` import
    from `aimediator.design_briefs`.
- **B6.4** `diagnostics.extract` and `diagnostics.audit` follow blueprint
  section 3.3. Each script maps the neutral records to its own existing
  output keys.
  - **Request equivalence**: run this before refactoring each of the four
    `run_balance_*_live.py` scripts, and again after; the SHA-256 lists of
    their `request.json` files must be equal.
    1. Run the script with `runpy.run_path(<script>, run_name='__main__')`
       and a patched `sys.argv`.
    2. Patch `aimediator.inference.api` to return fixture tags.
    3. Patch `aimediator.runner.streamed_chat` with a fake: extraction
       returns one claim built from the first evidence unit, and the audit
       returns `supported`.
    4. For `run_balance_regression_live.py`, give a synthetic admission run
       (`source-snapshot.json` and `relevance.json` with its six case IDs).
    5. Compute the SHA-256 list.

    Record the lists in the change record. The harness is temporary; the
    committed tests cover `diagnostics` with a fake chat transport.
  - `diagnose_evidence_quality_live.py` relies on the offline
    `diagnostics` tests (its inputs are archived runs).
  - Record that live reruns were not performed.

### B6-V (verification)

```text
You are session B6-V (verification) of the AIMediator code restructuring.
You did not implement batch B6. Change nothing except the change record.
Read: RULES.md; this work order; the blueprint, sections 3.3, 3.6, 4, 5, 6.6
and 7; the plan, sections 2, 4, 8 and the B6 part of section 7; the change
record.
Task: run every item of the B6-V checklist in this work order on HEAD, and
append a verification note committed with "Session: B6-V". If every item
passes, tag that commit restructure-b6. Otherwise record the findings as
fix-up steps B6.F1 and so on, and stop without tagging.
Never add attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary check from `restructure-b5`, and commit hygiene.
2. Plan 8.7, fourth grep, prints nothing. The suite passes from a foreign
   directory (plan 8.5).
3. G2 and P3 report 0. No script docstring begins with "Compatibility entry
   point".
4. Every script in `scripts/collect/` and `scripts/experiments/` prints its
   help, and `--help` output is unchanged against `restructure-b5` (compare
   both).
5. The lock fixture is unchanged since B5, and the lock is green.
6. The request-equivalence lists are recorded and equal.
7. The layering test covers `collection.*`, `design_briefs` and
   `diagnostics`.
8. Gates. Wheel acceptance with the wheel listing check of step B6.2.

## 5. Exit and handoff out

- Exit tag: `restructure-b6`, set by B6-V.
- The next work order is [B7](b7-readability-and-acceptance.md).

## 6. Escalation triggers

- A collector default, endpoint or output would change.
- A live script's request bytes differ after B6.4.
- `workspace_root()` resolves differently from the old roots for a
  documented command.
