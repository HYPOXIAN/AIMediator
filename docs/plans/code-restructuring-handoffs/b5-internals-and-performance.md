# Handoff B5: Internal decomposition and performance

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-03
- Applies to: [code restructuring plan](../code-restructuring.md) batch B5; entry tag `restructure-b4`

Work order for batch B5. The steps are defined in plan section 7 (B5). This
batch rewrites code, so the frozen contracts govern every change:
[blueprint](../code-restructuring-blueprint.md) section 3.3 (interfaces),
section 3.4 (artifact write schedule) and section 3.5 (request
construction).

## 1. Mission

- Unify the duplicated helpers (U-01 to U-04).
- Split `Runner._generate` and `pipeline.process` along the frozen
  contracts.
- Replace library printing with callbacks (F-08).
- Make `run_store.state` incremental (P-02), measure the coverage rebuild
  (P-03), and remove import-time I/O (P-04).
- Add the legacy code snapshots (CR-D12).

The only lock-fixture change allowed in B5 is the B5.11 commit.

## 2. Entry conditions

- Tag `restructure-b4` exists (after the owner review of B4).
- Clean tree, no `WIP Step` stash. The gates pass.

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/|tests/|scripts/experiments/|docs/records/[0-9]{8}-code-restructuring\.md$)
```

- **Allowed**:
  - `src/aimediator/` within the contracts of blueprint section 3;
  - new tests;
  - in `scripts/experiments/`, only passing a `log` printer (B5.7);
  - the lock fixture in the B5.11 commit only.
- **Not allowed**:
  - any change to request bytes, artifact names, contents or write order;
  - an exception type on an existing path;
  - the functions listed in blueprint section 1.2;
  - documents other than the change record.
- **Decisions in force**: CR-D12 (B5.11).
- **Owner actions**: none.

## 4. Sessions

### B5-1 (implementation): steps B5.1 to B5.5

### B5-2 (implementation): step B5.6

### B5-3 (implementation): steps B5.7 to B5.11

All three sessions use this prompt, with their own session ID and step
range:

```text
You are session B5-<k> (implementation) of the AIMediator code restructuring,
steps <first> to <last>.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/code-restructuring-handoffs/b5-internals-and-performance.md); the
blueprint docs/plans/code-restructuring-blueprint.md, sections 3, 4, 5 and
6, and sections 3.4 and 3.5 in full; the plan docs/plans/code-restructuring.md,
sections 1, 2, 5, 8 and the B5 part of section 7; the change record.
Task: execute your steps in order, inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates, including the
  behavior lock, after every commit.
- One kind of operation per commit, with "Step: B5.x" in the body (and
  "Decision: CR-D12" for B5.11). B5.6 is a series of commits.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **B5.1**
  - `resources.prompts(mode)` follows blueprint section 3.3.
  - `engine.run` and `operations.analyze` use it.
  - `operations.prompts_for` stays as a one-line alias.
  - Lock unchanged, including `prompt-snapshot.json` in both the CLI and
    legacy targets.
- **B5.2** `schema.py` holds the builders (`obj`, `quality_obj`, `arr`,
  `enum`), the constants (`STRING`, `NULLABLE_STRING`,
  `NULLABLE_NONEMPTY_STRING`, `BOOL`) and `schema_errors`.
  - `evidence_quality` and `evidence` import from it.
  - Only the archived recovery script used `evidence_quality.obj`, `enum`
    and the like, so those names need no aliases. Check with
    `git grep -nE "evidence_quality\.(obj|enum|STRING|NULL_STRING)|\bq\.(obj|enum|STRING|NULL_STRING)"`.
  - Add a unit test that pins `json.dumps(obj({'a': STRING}))`,
    `json.dumps(quality_obj({'a': STRING}))` and both nullable constants as
    literal strings.
  - Request lock unchanged.
- **B5.3** `evidence.character_terms(entry)` is used at these six sites.
  Keep each site's own filtering:
  - `engine.py` line 414, now `evidence.character_candidates`: no filter,
    since `term_matches(None, ...)` is `False`;
  - lines 471 and 472, now in `ground_claim`: no filter;
  - `balance_policy.attributed_candidates`: `if t and term_matches(...)`;
  - `evidence_quality.bind_claim`: `t and term_matches(...)` inside `any`;
  - `evidence_quality.summarize_opinions`: `t and term_matches(...)`;
  - `scripts/experiments/export_balance_review_followups.py` line 31: no
    filter. This is the only script edit in B5.3, and `scripts/experiments/`
    is in the boundary.
- **B5.4** `bind_claim` replaces its `numbers` lambda with
  `evidence.numeric_tokens`. The regular expressions are identical; confirm
  this before the edit.
- **B5.5** `stages.prepare`, `stages.options` and `stages.normalize` follow
  blueprint section 3.3.
  - `Runner._generate` keeps: the cache identity and journal paths; the
    quality-stage repair of cache, transport and envelope errors; the
    `strict_json`, `schema_errors` and `normalize` `try` block; the
    incomplete-generation check; and `validation.json`.
  - Add unit tests for each stage's `prepare`, `options` and `normalize`.
- **B5.6** Series of commits.
  1. The first commit introduces the `RunState` dataclass and replaces the
     locals of `process` with its fields. It moves no logic.
  2. Each later commit extracts one stage function (blueprint section 3.3,
     `pipeline`).
  3. After every commit, check the write schedule of blueprint section 3.4
     against the diff, then run the lock and the full suite. The resume and
     interruption tests are in `test_cli_product.py` and
     `test_evidence_quality.py`.
  4. Add no `try` block.
  5. Target: no function in `pipeline` over 60 lines (blueprint section
     7.3).
- **B5.7**
  - `Runner`, `retrieve`, `process` and `engine.run` take `log=None`.
    `engine.main` passes `lambda text: print(text, flush=True)`.
  - `operations.analyze` drops `contextlib.redirect_stdout` and the unused
    `io` import.
  - Experiment scripts that build a `Runner` pass the same printer, so their
    console text stays: `diagnose_evidence_quality_live` (two places),
    `run_balance_controls_live`, `run_balance_numeric_extraction_live`,
    `run_balance_regression_live`, `run_balance_semantic_controls_live`,
    `replay_balance_admission` and `run_quality_screening_experiment`.
  - The B1.5 test keeps its expected text. If it now has to pass the
    printer explicitly, the text must not change.
- **B5.8**
  - Contract: `run-state.json` keeps the same content at every write.
  - Approach, chosen by the session: track the request directories already
    scanned in a per-folder cache inside `run_store`, or receive completed
    request IDs from the progress callback.
  - Test: count `validation.json` reads over repeated `state()` calls.
  - Measure 50 `state()` calls on a synthetic folder with 2,000
    `requests/<stage>/<id>/validation.json` files containing
    `{"errors": []}`, before and after, and record the numbers.
- **B5.9** Build a synthetic 600-comment shadow run: copy the fixture cases
  under new IDs, with matching annotations for `FixtureTransport`.
  - Profile it, and change the coverage rebuild only if
    `build_full_coverage` takes more than 10 % of the run.
  - Otherwise record "measured, not needed" with the numbers. Any change
    keeps the write schedule.
- **B5.10**
  - `retrieval` calls `resources.anchors()` inside `retrieve`, and
    `engine.run` calls it for the identity. The function is cached.
  - New test: in a subprocess, import `numpy` and `json`, then patch
    `pathlib.Path.read_text` and `read_bytes` to raise, and import every
    `aimediator` module. The imports must succeed.
- **B5.11** In `engine.run`, where the three snapshot files are written, also
  write `code-snapshot/<module>.py` for every top-level package module,
  sorted.
  - In the same commit, update lock target L2: run
    `python3 tests/behavior_lock.py --write`.
  - The body lists the added paths (contents are presence-only, like the
    other snapshots) and `Decision: CR-D12`.

### B5-V (verification)

```text
You are session B5-V (verification) of the AIMediator code restructuring.
You did not implement batch B5. Change nothing except the change record.
Read: RULES.md; this work order; the blueprint, sections 3 (in full), 4, 5,
6.6 and 7; the plan, sections 2, 5, 8 and the B5 part of section 7; the
change record.
Task: run every item of the B5-V checklist in this work order on HEAD, and
append a verification note committed with "Session: B5-V". If every item
passes, tag that commit restructure-b5. Otherwise record the findings as
fix-up steps B5.F1 and so on, and stop without tagging.
Never add attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary check from `restructure-b4`, and commit hygiene. Every B5.6
   commit names B5.6.
2. `git log --oneline restructure-b4..HEAD -- tests/fixtures/behavior-lock.json`
   lists exactly one commit, the B5.11 commit with `Decision: CR-D12`. Its
   fixture diff touches only L2 snapshot paths. The lock is green.
3. Read the diff of `pipeline.py` against blueprint section 3.4: every write
   point is still present, in order.
4. The function-length metric (blueprint section 7.3) lists nothing in
   `pipeline`, `runner`, `stages`, `evidence` or `retrieval`.
5. The layering test, the import-without-I/O test, the B1.5 console test
   and the B5.8 read-count test pass.
6. The suite time is recorded against the blueprint section 2 target. Gates,
   the foreign directory check and the wheel acceptance pass.

## 5. Exit and handoff out

- Exit tag: `restructure-b5`, set by B5-V.
- The next work order is [B6](b6-research-code.md).

## 6. Escalation triggers

- The lock changes outside the B5.11 commit.
- A stage split needs to move, merge or reorder an artifact write.
- B5.9 crosses the threshold, and the fix would touch the write schedule.
- Removing a `print` changes a script's console text.
