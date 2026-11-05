# Handoff U7: Acceptance and documents

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-04
- Applies to: [pipeline upgrade plan](../pipeline-upgrade.md) batch U7; entry tag `upgrade-u6`

Work order for batch U7. The steps are defined in plan section 7 (U7). The
batch runs the full 600-comment set and the holdout checks once, brings the
documents and `RULES.md` up to date, records the final acceptance and,
after the owner's final review, freezes the record and archives the plan.

## 1. Mission

- Full live runs in the three quality modes with the adopted configuration
  (U7.1).
- The single holdout and test runs of the project (U7.2).
- Documents that describe the code (U7.3).
- `RULES.md` v1.5 with the new test floor (U7.4, UP-D16).
- Final acceptance (U7.5) and closure (U7.6).

## 2. Entry conditions

- Tag `upgrade-u6` exists. Clean tree, no `WIP Step` stash, the gates pass.
- The owner has fixed the configuration for U7.1: `max_parallel_requests`,
  `cache_dir` (a new empty directory, so that every request is fresh), and
  `second_audit`. U7-L copies it into the change record.
- UP-D16 is answered (U7.4).

## 3. Responsibility boundary

Allowed paths:

```text
^(README\.md$|RULES\.md$|CLAUDE\.md$|docs/|reports/[0-9]{8}-upgrade-acceptance/|scripts/maintenance/check_rules\.py$|tests/test_check_rules\.py$)
```

- **Allowed**: documents under `docs/`, including the new validation record,
  the index, and in U7.6 the moves into `docs/archive/`; the root README;
  `CLAUDE.md` in U7.4 (its `Applies to` line) and U7.6 (its pointer to the
  plan); `RULES.md` in U7.4 only; the rule check and its test only if the
  P4 baseline parser needs the new wording; one curated report.
- **Not allowed**: package code, tests other than the rule-check test,
  assets, data, earlier reports, frozen records. A defect found here becomes
  an escalation, not a fix in U7.
- **Decisions in force**: UP-D16 (U7.4).
- **Owner actions**: fix the U7.1 configuration; run or authorize U7-L;
  approve the `RULES.md` wording; give the final review.

## 4. Sessions

### U7-L (live): steps U7.1 and U7.2

```text
You are session U7-L (live) of the AIMediator pipeline upgrade, steps U7.1
and U7.2. You run on the owner's machine with the local model service.
Read: RULES.md; this work order; the plan, sections 1, 5 and 8.6 and the U7
part of section 7; the change record.
Task: check the environment, run the U7.1 and U7.2 runs at the U7 entry
tag, measure and score them, archive the full runs, and record the results
in the change record and in reports/<YYYYMMDD>-upgrade-acceptance/, with
"Step: U7.1" and "Step: U7.2" in separate commits.
Rules: never open, print or copy .env. If the environment differs from the
U0.6 record in anything the owner did not set for U7.1, or doctor fails,
stop and report. Each holdout or test split is run once. Never add
attribution.
Finish with a session-log entry; your final message repeats it.
```

Runs:

- **U7.1**: `u7-full-off`, `u7-full-shadow`, `u7-full-enforce` on
  `data/raw/feedback/20261027-balanced/screened/records.jsonl`. Compare
  `u7-full-off` with the archived `off` run (stages, tokens, time, claim
  outcomes, coverage) and all three with the U0.6 benchmark baseline scaled
  per comment. Every input row must have one coverage record.
- **U7.2**: the `balance-silver-v1` holdout (relevance and character
  expectations) and the `extraction-precision-v1` test split, once each,
  in `off`. Compare the test split with U5.5.

### U7-1 (implementation): steps U7.3 to U7.5

```text
You are session U7-1 (implementation) of the AIMediator pipeline upgrade,
steps U7.3 to U7.5.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/pipeline-upgrade-handoffs/u7-acceptance-and-documents.md); the
plan docs/plans/pipeline-upgrade.md, sections 1, 5, 7, 12 and 13; every
design document, the CLI guide, the README; the change record.
Task: execute your steps in order, inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates after every commit.
- One kind of operation per commit, with "Step: U7.x" in the body and
  "Decision: UP-D16" for U7.4. The RULES.md wording waits for the owner's
  approval.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **U7.3**
  - design/cli.md: sections 5 (modules, layers, contracts), 6
    (configuration keys), 7 (identity, cache, request index) and 8 (report
    schema `aimediator-report-v2`), checked against the code.
  - balance-analysis.md, evidence-quality.md and
    emotion-quantification-and-evidence-isolation.md: the request views,
    quality v2, extraction v2 and the measured limits.
  - guides/cli-usage.md: options, configuration keys, cache directory,
    second audit, resume refusals.
  - README: the "Current engineering work" lines point at the record of
    U7.3 instead of the plan once U7.6 runs; until then, keep them.
  - `docs/records/<YYYYMMDD>-pipeline-upgrade-validation.md`: the U7.1 and
    U7.2 results with denominators and intervals, the targets of plan 5.5
    with measured values, and the limitations (agent silver labels,
    same-model audit unless the second audit is adopted, sample sizes).
- **U7.4** (UP-D16): `RULES.md` v1.5: the P4 baseline sentence names the
  final count and date; a revision-log entry states the reason; the
  `Applies to` line of `CLAUDE.md` names v1.5. Run the rule check: it must
  parse the new baseline.
- **U7.5**: under "Batch results" in the change record, a table with every
  completion criterion of plan section 13 and every target of 5.5 with its
  measured value; open items go to "Deferred".

### U7-V (verification)

```text
You are session U7-V (verification) of the AIMediator pipeline upgrade. You
did not implement batch U7. Change nothing except the change record.
Read: RULES.md; this work order; the plan, sections 1, 5, 8, 10 and 13 and
the U7 part of section 7; the change record.
Task: run every item of the U7-V checklist on HEAD, and append a
verification note committed with "Session: U7-V". If every item passes, tag
that commit upgrade-u7-review and stop for the owner's final review.
Otherwise record fix-up steps U7.F1 and so on and stop without tagging.
Never add attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary and commit hygiene from `upgrade-u6` (plan 8.8); no package
   code changed in U7.
2. Gates, foreign directory and wheel acceptance pass; the test count is at
   least the new P4 floor.
3. The U7.1 coverage accounts for all 600 inputs in each mode.
4. The holdout and the test split appear exactly once each in U7.2 (and the
   test split once in U5.5).
5. Every completion criterion of plan section 13 except item 9 is met or
   explained in "Deferred".
6. Spot-check the design documents against the code: every module of the
   layering table appears in design/cli.md section 5, every configuration
   key in section 6, and every new artifact name in section 7 or 8.

### U7-2 (closure): step U7.6, after the owner's final review

```text
You are session U7-2 (closure) of the AIMediator pipeline upgrade, step
U7.6. The owner has given the final review: <outcome>.
Read: RULES.md; this work order; the plan, sections 1, 10 and 13; the
change record.
Task: record the review outcome; if items were rejected, turn them into
fix-up steps and stop. Otherwise freeze the change record (Status stays
Active only until this commit; the file is final afterwards, D3), move
docs/plans/pipeline-upgrade.md and docs/plans/pipeline-upgrade-handoffs/
into docs/archive/ with their names kept, set their Status to Archived,
update every inbound link (D5), the index, the README and CLAUDE.md, and
tag upgrade-done. Commit with "Step: U7.6". Never add attribution.
Finish with a session-log entry; your final message repeats it.
```

## 5. Exit and handoff out

- Review tag `upgrade-u7-review` (U7-V); after the final review U7-2 sets
  `upgrade-done`.
- The upgrade is finished; later work starts a new plan.

## 6. Escalation triggers

- A full run leaves technical failures or an unaccounted input.
- A holdout or test result is much worse than the development results (a
  sign of overfitting): record it, do not tune.
- A document cannot be made to match the code without a code change.
- The rule check cannot parse the new P4 sentence.
