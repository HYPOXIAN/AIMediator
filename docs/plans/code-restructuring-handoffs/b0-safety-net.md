# Handoff B0: Safety net and baseline

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-03
- Applies to: [code restructuring plan](../code-restructuring.md) batch B0; entry tag `restructure-plan`

Work order for batch B0. The steps are defined in plan section 7 (B0).
Roles, the session protocol and the standards are in the
[blueprint](../code-restructuring-blueprint.md). This sheet adds the
boundary, the session split, notes and checks.

## 1. Mission

Build the safety net before any production code changes:

- the change record;
- the fix for the one test that depends on the working directory (F-04);
- the behavior lock (targets L1 to L4) with its self-test;
- fresh baseline measurements.

Nothing under `src/` or `scripts/` changes in this batch.

## 2. Entry conditions

- Tag `restructure-plan` exists. HEAD is that commit or a later `docs`
  commit. It contains the plan (Status Active), the blueprint, the eight
  handoffs and their index entries.
- `git status --short` prints nothing, and `git stash list` has no
  `WIP Step` entry.
- `python3 -m unittest discover -s tests -q` passes 222 tests.
  `python3 scripts/maintenance/check_rules.py` reports `Total: 0`.

## 3. Responsibility boundary

Allowed paths (boundary check, blueprint section 7.2):

```text
^(tests/|docs/README\.md$|docs/records/[0-9]{8}-code-restructuring\.md$)
```

- **Allowed**:
  - new: `tests/behavior_lock.py`, `tests/test_behavior_lock.py`,
    `tests/fixtures/behavior-lock.json`, and the change record;
  - edit: `tests/test_balance_analysis.py` (one line, B0.2) and
    `docs/README.md` (one index row).
- **Not allowed**:
  - anything under `src/`, `scripts/`, `configs/`, `data/` or `reports/`;
  - any other document. A problem in the plan, the blueprint or a handoff
    is reported as an escalation, never fixed inside the batch.
- **Decisions in force**: B0 records all twelve (blueprint section 1.1). No
  step of B0 depends on one.
- **Owner actions**: none.

## 4. Sessions

### B0-1 (implementation): steps B0.1 to B0.4

```text
You are session B0-1 (implementation) of the AIMediator code restructuring.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/code-restructuring-handoffs/b0-safety-net.md); the blueprint
docs/plans/code-restructuring-blueprint.md, sections 1, 4, 5 and 6; the plan
docs/plans/code-restructuring.md, sections 1, 2, 5, 8 and the B0 part of
section 7.
Task: execute steps B0.1 to B0.4 as this work order describes, inside its
boundary.
Rules:
- Start with the plan's resume procedure. Run the gates after every step.
- One kind of operation per commit, with "Step: B0.x" in the body.
- Never add Co-Authored-By, "Generated with" or any other attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry in the
change record. Your final message repeats that entry.
```

Step notes:

- **B0.1** Name the file `docs/records/<today as YYYYMMDD>-code-restructuring.md`.
  - Copy the skeleton from plan section 10.
  - "Owner decisions" gets twelve rows: answer `adopt`, date `2026-11-03`,
    note "plan section 9". The CR-D06 row adds "includes confirmation that
    no experiment output must be resumed under its old identity".
  - Add an index row in `docs/README.md` under Records: type `Record`,
    status `Active`, description "Change record of the code restructuring:
    decisions, progress, session log, verification notes and archives."
  - Commit `docs: open the code restructuring change record`.
- **B0.2** At `tests/test_balance_analysis.py` line 194, read the prompt with
  `asset_path('prompts/verify-balance.en.txt').read_text(encoding='utf-8')`.
  - Import `asset_path` with `from aimediator.resources import asset_path`,
    placed after the existing `import run_balance_analysis as m` (that
    forwarder puts `src/` on the path).
  - Plan 8.5 must then report no failure.
  - Commit `chore: read the verify prompt from the package assets in a test`.
- **B0.3** Behavior lock (plan section 5). Build it as follows.
  - **Layout**: `tests/behavior_lock.py` holds no test classes. It defines
    one producer per target, a normalizer, and `--write`, which rewrites the
    fixture with sorted keys. `tests/test_behavior_lock.py` holds one
    `TestCase` that compares the produced digests with the fixture and
    prints the differing keys.
  - **L1**: run `aimediator.demo.demo(<tmp>/demo, quiet=True)`, with stderr
    captured.
  - **L3**: in `<tmp>/demo/review-template/decisions.json`, set
    `reviewer_type` to `agent` and `reviewer_id` to `behavior-lock`. Then
    call `import_review` into `<tmp>/overlay`, and `export_report` for
    `<tmp>/demo/enforce` with that overlay. This mirrors
    `scripts/maintenance/verify_cli_install.py` lines 52 to 59.
  - **L2**: run `aimediator.engine.run(args)` for `off`, `shadow` and
    `enforce`.
    - Dataset: the fixture sources written as `demo` writes
      `synthetic-input.jsonl`.
    - Arguments: `model=None`, `embedding_model='qwen3-embedding:8b'`,
      `base_url='http://fixture.invalid'`, `quality_only=False`,
      `relevance_only=False`.
    - Until B2.2, patch `aimediator.engine.api` with a dispatcher. For
      `/api/tags` it returns `FixtureTransport(defaults()).tags()`; for any
      other endpoint it returns `FixtureTransport.api(base, endpoint,
      payload)`.
    - Patch `aimediator.engine.streamed_chat` with `FixtureTransport.chat`,
      and redirect stdout.
  - **L4**: load `scripts/collect/screen_feedback.py` with `importlib`, as
    `tests/test_screen_feedback.py` does.
    - Inputs: every `text_original` in
      `data/evaluation/balance-regressions-v1/cases.json` (12, under
      `source`), `data/evaluation/evidence-quality-real-v1/annotation-template.json`
      (300) and `data/evaluation/evidence-quality-synthetic-v1/records.jsonl`
      (38).
    - Digest the JSON list of `classify_rules` results.
  - **Normalization**: find the volatile values with the procedure in plan
    section 5.3; do not guess them. Values you can expect to find volatile:
    - times and durations: `created_at_utc`, `updated_at_utc`,
      `elapsed_seconds`;
    - absolute paths: the legacy manifest's `dataset`;
    - run and request identities: `run_id`, `run_sha256`, request
      directory names, `request_id`, `quality_request_ids`,
      `completed_request_identities`;
    - code hashes: `code`, `modules`, `runner_sha256`,
      `shared_code_sha256`, `module_sha256`, `policy_module_sha256`,
      `script_sha256`;
    - `artifact_hashes`;
    - `run_identity` inside quality request contents, and fingerprints
      derived from all of the above.
  - **Code-only files**: `*-snapshot.py` and `code-manifest.json` contain
    only code or code hashes. The lock checks that they exist and replaces
    their content digest with a placeholder. List them as the only content
    exemption besides `.writer.lock`.
  - **Self-test** (plan 5.4). Make each temporary edit at the location
    given, then restore the file with `git checkout -- <file>` before you
    commit:
    - must fail:
      - append a space to `src/aimediator/assets/prompts/summarize-balance.en.txt`;
      - swap `'recommendation'` and `'specificity'` in `CLAIM` (`engine.py`
        lines 110 to 113);
      - change `count=4` to `count=3` at `engine.py` line 773;
      - change one word of `'# SF6 collected-sample feedback'`
        (`reporting.py` line 125);
      - change `'general_not_mechanism'` (`evidence_quality.py` line 182);
    - must pass: append `# lock probe` to `src/aimediator/common.py`, and
      a plain rerun.
  - **Record** under "Behavior lock (B0.3)": the volatile keys, the
    exemptions and a table of the self-test results.
  - The suite takes about 50 s longer until B1.1.
  - Commit `chore: add the behavior lock`.
- **B0.4** Measure every plan section 0 item again, plus the blueprint 7.3
  metric and the plan 8.7 grep counts. Record them under "Baseline
  measurements".
  - Include the wheel acceptance (plan 8.2) and the foreign-directory run
    (plan 8.5).
  - Commit `docs: record the baseline measurements`, together with the
    session-log entry.

Expected test count after B0: 222 plus the lock tests.

### B0-V (verification)

```text
You are session B0-V (verification) of the AIMediator code restructuring.
You did not implement batch B0. Change nothing except the change record.
Read: RULES.md; this work order; the blueprint, sections 3.7, 5, 6.6 and 7;
the plan, sections 5 and 8; the change record.
Task: run every item of the B0-V checklist in this work order on HEAD, and
append a verification note (blueprint 6.6) committed with "Session: B0-V" in
the body. If every item passes, tag that commit restructure-b0. Otherwise
record the findings as fix-up steps B0.F1, B0.F2 and so on, and stop
without tagging.
Never add attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary check from `restructure-plan`, and commit hygiene (blueprint
   7.2).
2. Plan 8.1 gates. The count is 222 plus the lock tests.
3. Plan 8.5 passes (F-04 fixed).
4. Lock independence:
   1. The lock is green twice in a row.
   2. One temporary failing edit (a prompt byte) turns it red; restoring the
      file turns it green again.
   3. The `# lock probe` edit leaves it green.
   4. Restore everything afterwards.
5. The fixture holds only 64-character hex digests and placeholders, never
   corpus text.
6. The change record has twelve decision rows, a complete lock section and
   the baseline measurements.
7. Wheel acceptance (plan 8.2).

## 5. Exit and handoff out

- Exit tag: `restructure-b0`, set by B0-V.
- The next work order is [B1](b1-defects-and-hot-spots.md). Its first
  session reads the B0-V note and the baseline measurements.

## 6. Escalation triggers

- A lock target still differs between two runs after V1 and V2
  normalization (nondeterminism in the product).
- The self-test cannot make a required case fail (the lock is too weak).
- The lock can only be made deterministic by changing code outside
  `tests/`.
