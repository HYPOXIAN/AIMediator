# Handoff B3: Callers leave the facade and the forwarders

- Type: Agent handoff
- Status: Archived
- Updated: 2026-11-04
- Applies to: [code restructuring plan](../code-restructuring.md) batch B3; entry tag `restructure-b2`
- Archived 2026-11-04 when the code restructuring was completed (tag `restructure-done`).

Work order for batch B3. The steps are defined in plan section 7 (B3). The
contracts are in [blueprint](../code-restructuring-blueprint.md) sections 3.3
and 3.6.

## 1. Mission

Every caller imports the new modules directly:

- package modules;
- tests, which also get shared fixtures in `tests/support.py`;
- experiment scripts, whose identities follow CR-D06;
- the screening collector.

After that, the `engine` facade is removed. The forwarders still exist but
nothing imports them; B4 deletes them.

## 2. Entry conditions

- Tag `restructure-b2` exists, and the B2-V note says "accepted".
- Clean tree, no `WIP Step` stash. The gates pass.

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/|tests/|scripts/experiments/|scripts/collect/screen_feedback\.py$|docs/records/[0-9]{8}-code-restructuring\.md$)
```

- **Allowed**:
  - import lines and module-qualified names in `src/aimediator/`;
  - removing the facade from `engine.py`;
  - `tests/` (imports, `support.py`, the layering test);
  - experiment scripts (bootstrap, imports, asset paths, identity fields);
  - `screen_feedback.py` (glossary source only).
- **Not allowed**:
  - logic changes;
  - flags, defaults or output formats of scripts, except the identity
    fields of CR-D06 and the `--prompt-dir` default;
  - the lock fixture;
  - deleting forwarders or symlinks (B4).
- **Decisions in force**:
  - CR-D06: the identity rule is in blueprint section 3.6;
  - CR-D02: `run_grounded_feedback_live.py` gets only bootstrap and
    asset-path changes.
- **Owner actions**: none.

## 4. Sessions

### B3-1 (implementation): steps B3.1 to B3.3

### B3-2 (implementation): steps B3.4 to B3.6

Both sessions use this prompt, with their own session ID and step range:

```text
You are session B3-<k> (implementation) of the AIMediator code restructuring,
steps <first> to <last>.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/code-restructuring-handoffs/b3-callers-and-tests.md); the
blueprint docs/plans/code-restructuring-blueprint.md, sections 3, 4, 5 and
6; the plan docs/plans/code-restructuring.md, sections 1, 2, 4, 8 and the B3
part of section 7; the change record.
Task: execute your steps in order, inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates after every step.
- One kind of operation per commit, with "Step: B3.x" and, for B3.4,
  "Decision: CR-D06" in the body. B3.3 and B3.4 are series of commits.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Name mapping for B3.1, from `engine` to the new import:

| `engine` name | Import instead |
| ------------- | -------------- |
| `relevance_agrees` | `balance_policy.retrieval_review_agrees` (same function) |
| `CLAIM`, `ground_claim`, `character_reference`, `character_candidates`, `evidence_units` | `evidence` |
| `schema_errors` | `evidence_quality.schema_errors` (moves to `schema` in B5.2) |
| `quality` (alias of `evidence_quality`) | `evidence_quality` |
| `load_policy` | `balance_policy.load_policy` |
| `Runner`, `retrieve`, `process`, `aggregate` | `runner`, `retrieval`, `pipeline`, `pipeline` |
| `digest`, `strict_json`, `write_json` | `common.sha`, `common.strict_json`, `common.write`, keeping those aliases |
| `ROOT` in `legacy_review` | delete (unused) |

Step notes:

- **B3.1** Callers by number of `engine` uses: `review.py` (11),
  `operations.py` (6), `evaluation.py` (4), `reporting.py` (3),
  `legacy_review.py` (import line), `fixture_transport.py` (should already
  have none). One commit. Plan 8.7, second grep: only `engine.py` may still
  match.
- **B3.2** `tests/support.py` holds only what two or more test modules use:
  - `CASES`, read through `asset_path('fixtures/cases.json')` rather than
    the evaluation-set symlink;
  - `case`;
  - `qualified`;
  - any claim builders the importers need.

  Currently `test_evidence_quality_evaluation.py` and
  `test_quality_screening_experiment.py` import these from
  `test_evidence_quality.py`. The responder in `test_evidence_quality.py`
  (lines 248 to 286) is **not** a copy of `FixtureTransport.chat`: it
  injects failures and bad claims. Keep it in that test module.
- **B3.3** One commit per area:
  1. evidence and quality: `test_evidence_quality`,
     `test_evidence_quality_evaluation`, `test_quality_screening_experiment`;
  2. balance: `test_balance_analysis`, `test_balance_review_pipeline`,
     `test_balance_source_review` (`review_balance_sources` becomes
     `aimediator.legacy_review`), `test_balanced_collection`;
  3. the rest.

  Keep `scripts/collect` or `scripts/experiments` on `sys.path` only in
  tests that import a script. The tests for collectors, screening, the
  grounded pilot, `evaluate_balance_review`, `prepare_balance_design`,
  `run_balance_regression_live`, `export_balance_review_followups` and
  `run_quality_screening_experiment` do. `test_refactored_boundaries` keeps
  its forwarder-identity test until B4.2. The test count does not change.
- **B3.4** For each experiment script:
  - Add the bootstrap (plan section 4.3) and import `aimediator` modules
    instead of `run_balance_analysis`, `evidence_quality`,
    `balance_policy` and `review_balance_sources`.
  - Replace `ROOT / 'prompts/...'` and `ROOT / 'configs/...'` with
    `asset_path(...)`.
  - Apply the identity rule of blueprint section 3.6.
  - Keep a local
    `ROOT = Path(__file__).resolve().parents[2]` until B6.1.
  - `run_balance_regression_live.py` defaults `--prompt-dir` to
    `asset_path('prompts')`.

  Commit groups:
  1. live: `run_balance_controls_live`, `run_balance_numeric_extraction_live`,
     `run_balance_regression_live`, `run_balance_semantic_controls_live`,
     `diagnose_evidence_quality_live`;
  2. offline research: `check_balance_regressions`,
     `evaluate_balance_review`, `export_balance_review_followups`,
     `prepare_balance_design`, `replay_balance_admission`,
     `review_balance_live`;
  3. `run_quality_screening_experiment` and `run_grounded_feedback_live`.

  For every script, `python3 scripts/experiments/<name>.py --help` exits 0,
  also from a foreign directory. Enter a table of each script's identity
  keys (removed, added) in the change record.
- **B3.5** `screen_feedback.py` loads `G` from
  `asset_path('data/glossary.json')` after the bootstrap. Lock target L4
  unchanged.
- **B3.6**
  - Delete the facade imports and the `schema_errors` wrapper from
    `engine.py`. Keep the imports that `run` and `main` use.
  - Remove the transitional allowance from `tests/test_module_layers.py`.
  - Plan 8.7, first and second greps, must print nothing.

### B3-V (verification)

```text
You are session B3-V (verification) of the AIMediator code restructuring.
You did not implement batch B3. Change nothing except the change record.
Read: RULES.md; this work order; the blueprint, sections 3, 4, 5, 6.6 and 7;
the plan, sections 2, 4, 5, 8 and the B3 part of section 7; the change
record.
Task: run every item of the B3-V checklist in this work order on HEAD, and
append a verification note committed with "Session: B3-V". If every item
passes, tag that commit restructure-b3. Otherwise record the findings as
fix-up steps B3.F1 and so on, and stop without tagging.
Never add attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary check from `restructure-b2`, and commit hygiene. Every B3.4
   commit names CR-D06.
2. Plan 8.7, first and second greps, print nothing. The layering test passes
   without the allowance.
3. The lock fixture is unchanged since `restructure-b0`, and the lock is
   green. The test count is unchanged since `restructure-b2`.
4. Every remaining experiment script prints its help from a foreign
   directory. The identity table is in the change record.
5. Gates, the foreign directory check (plan 8.5) and the wheel acceptance
   (plan 8.2).

## 5. Exit and handoff out

- Exit tag: `restructure-b3`, set by B3-V.
- The next work order is [B4](b4-layer-removal-and-docs.md).

## 6. Escalation triggers

- A script's output must change beyond the CR-D06 identity fields.
- A test or script still needs a facade name that has no home in blueprint
  section 3.3.
- The lock turns red.
