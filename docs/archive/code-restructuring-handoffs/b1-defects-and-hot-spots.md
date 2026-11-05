# Handoff B1: Confirmed defects, the main hot spot, archives

- Type: Agent handoff
- Status: Archived
- Updated: 2026-11-04
- Applies to: [code restructuring plan](../code-restructuring.md) batch B1; entry tag `restructure-b0`
- Archived 2026-11-04 when the code restructuring was completed (tag `restructure-done`).

Work order for batch B1. The steps are defined in plan section 7 (B1).
Roles, the session protocol and the standards are in the
[blueprint](../code-restructuring-blueprint.md).

## 1. Mission

This batch:

- removes the glossary hot spot (P-01);
- fixes F-05, F-06 and F-07;
- pins the legacy console text for B5.7;
- archives the six scripts named by CR-D03 and CR-D04, which also resolves
  F-01, F-02 and R-02.

The behavior lock stays green at every step, and its fixture does not change.
The batch ends at an owner review point.

## 2. Entry conditions

- Tag `restructure-b0` exists, and the B0-V note says "accepted".
- Clean tree, no `WIP Step` stash. The gates pass.

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/|scripts/|tests/|docs/reference/compatibility-layers\.md$|docs/design/(balance-analysis|cli)\.md$|docs/records/[0-9]{8}-code-restructuring\.md$)
```

- **Allowed**:
  - `src/aimediator/resources.py` and `engine.py` (B1.1, B1.2);
  - encoding-only edits anywhere in `src/`, `scripts/` and `tests/` (B1.3);
  - the collectors (B1.4);
  - new tests (B1.1, B1.4, B1.5);
  - deletions of the six archived scripts and two test files (B1.6, B1.7);
  - the register rows and change log for those deletions;
  - the two design-document mentions (B1.7).
- **Not allowed**:
  - any other change to `src/` or `scripts/`;
  - the assets;
  - the lock fixture;
  - any other document.
- **Decisions in force**:
  - CR-D03: archive four scripts and nine tests;
  - CR-D04: archive the two broken scripts and do not fix them. Ignore the
    plan's "if rejected" text.
- **Owner actions**: review after B1-V (section 5).

## 4. Sessions

### B1-1 (implementation): steps B1.1 to B1.7

```text
You are session B1-1 (implementation) of the AIMediator code restructuring.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/code-restructuring-handoffs/b1-defects-and-hot-spots.md); the
blueprint docs/plans/code-restructuring-blueprint.md, sections 1, 3.3
(resources, evidence), 4, 5 and 6; the plan docs/plans/code-restructuring.md,
sections 1, 2, 3.2, 3.3, 8 and the B1 part of section 7; the change record.
Task: execute steps B1.1 to B1.7 as this work order describes, inside its
boundary.
Rules:
- Start with the plan's resume procedure. Run the gates after every step.
- One kind of operation per commit, with "Step: B1.x" and, where it applies,
  "Decision: CR-D0x" in the body.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **B1.1** In `resources.py`, add `glossary()` decorated with
  `functools.lru_cache(maxsize=1)`. It returns
  `json.loads(asset_path('data/glossary.json').read_text(encoding='utf-8'))`.
  - Use it in `engine.character_reference` (line 403) and for
    `glossary_target_patch` in `ground_claim` (line 477).
  - Leave the `glossary_sha256` values in `engine.run` alone: they hash file
    bytes, not the parsed object.
  - New test: mutate an entry returned by `character_reference('Ryu')`, call
    the function again, and assert the result equals a fresh expected value.
  - Measure with plan 8.4 and record the numbers. The cumulative time of
    `character_reference` must be under 1 s and the demo under 10 s; if not,
    escalate.
- **B1.2** Replace the `assert` at `engine.py` lines 478 and 479 with a loop
  that raises `AssertionError('Evidence span differs from the original
  text')` on a mismatch. The exception type stays, so the CLI exit code
  stays 1.
- **B1.3** Add `encoding='utf-8'` to every text-mode `read_text`,
  `write_text`, `open` and `Path.open` in `src/`, `scripts/` and `tests/`.
  - Binary I/O and `json.load` on HTTP responses stay as they are.
  - Find the `open` calls with `git grep -nE "open\(" -- src scripts tests`,
    then inspect every hit that has no `encoding=`, no binary mode and is
    not `urlopen`, `os.open` or `opener.open`.
  - The plan 8.7 encoding grep must print nothing. Lock unchanged.
  - One commit.
- **B1.4** `collect_balanced_feedback.py` lines 65 and 66: catch
  `BlockingIOError` and call
  `parser.error('Another collector is running in this project')`.
  - In all three collectors, keep the lock handle and close it in a
    `finally` block at the end of `main` (closing releases `flock`).
  - A test for the message is recommended; record it if you add one.
- **B1.5** New test (for example `tests/test_console_output.py`). It runs the
  lock's L2 producer for `enforce` and asserts the exact stdout lines:
  - the `<stage>: <model>, <n> items` lines;
  - the `Embedding <n>/<total>` lines;
  - the summary JSON.

  Confirm first that these lines contain no volatile value. If one does,
  normalize it the way the lock does.
- **B1.6** Archive (plan section 1, item 9):
  - Copy `present_quality_screening_results.py`,
    `protect_quality_screening_checkpoint.py`,
    `resume_quality_screening_local.py` and `run_quality_screening_recovery.py`
    (from `scripts/experiments/`), plus `tests/test_quality_screening_compact.py`
    and `tests/test_quality_screening_recovery.py`, to
    `~/Archives/AIMediator/scripts/<YYYYMMDD>-quality-screening/`.
  - Write `SHA256SUMS` there, check it with `sha256sum -c SHA256SUMS`, then
    `git rm` the six files.
  - In the register, remove these scripts from the "Used by" cells of
    `configs/local-language-routing.json`, `scripts/evidence_quality.py` and
    `scripts/run_balance_analysis.py`, and add a change-log line.
  - Add six rows under "Archive and deletions". Test count −9.
- **B1.7** Archive `scripts/run_local_direction_comparison.py` and
  `scripts/experiments/demo_evidence_quality.py` to
  `~/Archives/AIMediator/scripts/<YYYYMMDD>-broken-entry-points/`, with
  `SHA256SUMS`. Do all of the following in the **same commit**, otherwise
  G2 reports "registered layer no longer exists":
  - remove the register row of the wrapper (R3);
  - remove both scripts from the "Used by" cells of
    `scripts/run_balance_analysis.py`, `scripts/evidence_quality.py` and the
    `cases.json` symlink row;
  - add a change-log line.
  - In `docs/design/balance-analysis.md` (line 45) and
    `docs/design/cli.md` (line 90), add a dated note: "archived on <date>,
    code restructuring step B1.7; it had stopped working when the
    evidence-quality stage was added".

After B1.6 and B1.7, this grep must print nothing:
`git grep -nE 'present_quality_screening_results|protect_quality_screening_checkpoint|resume_quality_screening_local|run_quality_screening_recovery|run_local_direction_comparison|demo_evidence_quality' -- src scripts tests README.md docs/guides docs/reference`.
The design documents may keep the dated notes, and the planning documents
may still name the files.

Expected test count after B1: B0 count + 1 (B1.1) + 1 (B1.5) − 9, plus one
if you added the B1.4 test.

### B1-V (verification)

```text
You are session B1-V (verification) of the AIMediator code restructuring.
You did not implement batch B1. Change nothing except the change record.
Read: RULES.md; this work order; the blueprint, sections 3.3, 4, 5, 6.6 and
7; the plan, sections 2, 5, 8 and the B1 part of section 7; the change record.
Task: run every item of the B1-V checklist in this work order on HEAD, and
append a verification note committed with "Session: B1-V". If every item
passes, tag that commit restructure-b1-review and list the owner review
items from section 5 of this work order in the note. Otherwise record the
findings as fix-up steps B1.F1 and so on, and stop without tagging.
Never add attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary check from `restructure-b0`, and commit hygiene.
2. Diff review: `git diff restructure-b0..HEAD -- src` changes only
   `resources.py` and `engine.py`, plus encoding-only lines elsewhere.
3. Gates. The test count matches the expectation above.
4. `git diff restructure-b0..HEAD -- tests/fixtures/` prints nothing, and the
   lock is green.
5. `sha256sum -c SHA256SUMS` passes in both archive directories, and the
   change record lists all eight deletions.
6. The B1.7 grep and the plan 8.7 encoding grep print nothing. G2 and P3
   report 0.
7. Timing: demo at most 10 s; record the suite time.
8. Wheel acceptance (plan 8.2) and the foreign directory check (plan 8.5).

## 5. Exit, owner review and handoff out

- B1-V sets `restructure-b1-review`.
- Owner review items: the archived files and their locations; the demo and
  suite timings; any decisions found during execution or escalations.
- After the review, a closure session (blueprint 6.4) records the outcome
  and sets `restructure-b1`.
- The next work order is [B2](b2-engine-split.md).

## 6. Escalation triggers

- The demo stays above 10 s after B1.1.
- Any B1 step turns the lock red.
- An archived file is still used by code or tests.
- An encoding change would alter output bytes under a UTF-8 locale.
