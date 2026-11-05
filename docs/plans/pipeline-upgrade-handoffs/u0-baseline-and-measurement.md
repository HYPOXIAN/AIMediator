# Handoff U0: Baseline, measurement tool and evaluation sets

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-04
- Applies to: [pipeline upgrade plan](../pipeline-upgrade.md) batch U0; entry tag `upgrade-plan`

Work order for batch U0. The steps are defined in plan section 7 (U0). This
batch changes no pipeline behavior. It builds what every later batch is
measured with: the change record, the measurement tool, two evaluation sets
and the offline, archived and live baselines.

## 1. Mission

- Open the change record (U0.1).
- Add the measurement module and its three scripts (U0.2).
- Freeze `latency-benchmark-v1` (U0.3) and `extraction-precision-v1`
  (U0.5).
- Measure the offline baseline and the archived run with the committed tool
  (U0.4).
- Record the live environment and the live reference runs (U0.6).
- Freeze the smaller samples of UP-D17 (U0.7) and run the sample reference
  runs (U0.8).

## 2. Entry conditions

- Tags `restructure-done` and `upgrade-plan` exist. If either is missing,
  stop: the restructuring closure and the review corrections of the plan
  come first (plan, entry condition).
- Clean tree, no `WIP Step` stash, the gates pass.
- UP-D01 and UP-D02 are answered (U0.2 needs UP-D01; U0.3 and U0.5 need
  UP-D02).
- Read-only inputs exist locally: the archive
  `~/Archives/AIMediator/reports/latest-balanced-20261027/` (U0.4, U0.5) and
  `data/raw/feedback/20261027-balanced/` whose files match the SHA-256
  values in its `manifest.json` (U0.3, U0.5). If one is missing, stop and
  report.

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/measurement\.py$|tests/|scripts/experiments/(measure_run_requests|materialize_evaluation_input|score_extraction)\.py$|data/evaluation/(latency-benchmark-v1|extraction-precision-v1|upgrade-samples-v1)/|reports/[0-9]{8}-upgrade-baseline(-samples)?/|docs/records/[0-9]{8}-pipeline-upgrade\.md$|docs/README\.md$|docs/design/cli\.md$)
```

- **Allowed**:
  - the new module `measurement` and its tests;
  - the `measurement` row of the layering table, and the module table and
    contracts of design/cli.md section 5;
  - the lock fixture, only to add the three existence-only keys of the new
    module (plan rule 1.3), in the U0.2 commit;
  - the two new evaluation sets, each in its own `data` commit, and the
    samples of U0.7 in a third;
  - one curated report directory from U0.6 and one from U0.8.
- **Not allowed**: any other package module, any asset, any request byte,
  any existing evaluation set or report, the archive (read only), `.env`.
- **Owner amendment**: the `docs` commit with `Decision: UP-D17` changes
  the plan and the work orders outside this pattern, by the owner's
  decision of 2026-11-04. Checklist item 1 names it and does not count it
  as a boundary violation.
- **Decisions in force**: UP-D01 (U0.2), UP-D02 (U0.3, U0.5), UP-D17
  (U0.7, U0.8).
- **Owner actions**: answer UP-D01 and UP-D02; provide the live environment
  for U0-L or run it; set the embedding keys of the live configuration.

## 4. Sessions

### U0-1 (implementation): steps U0.1 to U0.4

```text
You are session U0-1 (implementation) of the AIMediator pipeline upgrade,
steps U0.1 to U0.4.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/pipeline-upgrade-handoffs/u0-baseline-and-measurement.md); the
plan docs/plans/pipeline-upgrade.md, sections 0 to 6, the U0 part of
section 7, and sections 8, 10 and 11; design/cli.md section 5.
Task: execute your steps in order, inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates after every commit.
- One kind of operation per commit, with "Step: U0.x" in the body and
  "Decision: UP-Dnn" where the step names one.
- Never add any attribution. Never open, print or copy .env or a credential.
- The archive under ~/Archives/AIMediator/ is read only.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **U0.1**
  - Copy plan section 11. `Applies to` names the commit tagged
    `upgrade-plan`.
  - Fill "Owner decisions" with the sixteen answers and their dates; a
    decision without an answer gets the row `pending`.
  - Add the index row to `docs/README.md` (Records) in the same commit.
- **U0.2**
  - Functions and outputs as in plan 5.2. Standard library and `common`
    only, plus `quality_scoring.proportion` for the intervals. No network,
    no model, and no import of `inference` or `runner`.
  - Request walk: `requests/<stage>/<id>/` for the stages `relevance`,
    `retrieval_review`, `quality`, `extract` and `verify`. Skip
    `requests/embedding/` and nested `transport-attempts/`.
  - Reuse: a request is reused when its `transport-provenance.json` has a
    `kind` other than `fresh_inference` (the archived format), or when a
    `reuse-provenance.json` exists (the U3.3 format, not written yet).
    Otherwise it is fresh.
  - Counters (`prompt_eval_count`, `prompt_eval_cached_count`,
    `eval_count`, the three durations in nanoseconds) are optional; missing
    values give `null`, never zero.
  - Composition: mean characters of the system prompt, of `format`, of
    every top-level key of the user message and of the nested parts
    `comments[].units[].text`, `comments[].text` and
    `comments[].retrieved_topics`.
  - `materialize` reads three label formats: `ids.json` (`record_id`,
    `content_sha256`), `labels.jsonl` with `content_sha256` (this project's
    sets) and `labels.jsonl` with `source_sha256` (`balance-silver-v1`). It
    writes the dataset rows unchanged, in the set's order, and raises when
    a row is missing or a hash differs.
  - `score_positions`: a claim is correct when its `character` and
    `direction` equal one labeled position of its comment. Precision over
    accepted claims and over all generated claims (validated plus
    quarantined claims with a claim object); recall over all labeled
    positions and over positions of admitted comments (`relevance.json`
    `agreement`); comments labeled `uncertain` are excluded from both and
    counted apart. Several claims on one position count once for recall.
  - Scripts: the docstring `Entry point for ... (aimediator.measurement).`,
    the bootstrap the other experiment scripts use, `argparse`, and
    `common.write` for the output.
  - Tests: synthetic run folders in a temporary directory (with and without
    counters, the archived provenance format), a demo run end to end
    (counters `null`), a hash mismatch in `materialize`, and hand-computed
    precision and recall.
  - Layering: add `(('measurement',), ('common', 'quality_scoring'))` to the
    table, citing UP-D01 in the commit body.
  - Lock: run the lock. If it fails only at
    `L2:<off|shadow|enforce>/code-snapshot/measurement.py`, run
    `python3 tests/behavior_lock.py --write` and list the three keys in the
    body. Any other difference is a stop condition.
- **U0.3**
  - Read `data/raw/feedback/20261027-balanced/screened/records.jsonl`.
  - Terciles by `len(text_original)`, per language, with the cut points
    recorded in the manifest. Within each language and tercile, sort by
    SHA-256 of `latency-benchmark-v1:<record_id>` and take the first 10.
  - `ids.json`: `record_id`, `language`, `content_sha256`,
    `length_tercile`. No source text, no URL.
  - `manifest.json`: version, purpose ("latency and outcome counts; not an
    accuracy set"), source dataset path and SHA-256, selection rule, cut
    points, counts, `ids_sha256`, `reviewer_type` `none`.
  - The commit body states the decision and that the set is frozen.
- **U0.4**
  - Run plan 8.1, 8.2, 8.4 and 8.5, and record the results under "Baseline
    measurements (U0.4)".
  - Run plan 8.7 and record the per-stage table and the composition table.
    They must agree with plan section 0.2 within rounding; a larger
    difference is a finding for the record, not a reason to edit the plan.

### U0-A (annotation): step U0.5

```text
You are session U0-A (annotation) of the AIMediator pipeline upgrade, step
U0.5. Work in the AIMediator checkout on branch main.
Read: RULES.md; this work order; the plan docs/plans/pipeline-upgrade.md,
sections 1, 5.3 and the U0 part of section 7; the change record;
data/evaluation/balance-silver-v1/manifest.json as the model of a silver
set.
Task: build data/evaluation/extraction-precision-v1/ as the step notes
describe, label every comment from its original text only, and commit the
set in one data commit with "Step: U0.5" and "Decision: UP-D02".
Rules: you never look at model claims, quarantined claims or audit results
of the comments you label. Never add attribution. The archive is read only.
Finish with a session-log entry; your final message repeats it.
```

Step notes:

- **Selection**, from the archive's `full-pipeline-final/extraction-coverage.json`:
  the 251 comments with `claims_generated` above 0, and the first 50
  comments, in the order of SHA-256 of `extraction-precision-v1:<record_id>`,
  with `claims_generated` 0 and a disposition other than
  `generation_failed`.
  Read only the IDs from the archive; take the text from the raw dataset
  with `materialize` or an equivalent hash-checked read.
- **Split**: development when the first 8 hexadecimal digits of SHA-256 of
  `extraction-precision-v1:<record_id>`, as an integer, modulo 10 are below
  7, or when the ID is in `latency-benchmark-v1`; test otherwise.
- **Label per comment** (`labels.jsonl`): `comment_id`, `language`,
  `content_sha256`, `split`, `positions` (a list of `character` and
  `direction`), `exhaustive` true, `uncertain` (true when the author's
  position cannot be resolved), `reason` (one or two sentences in English,
  quoting the source where needed), `reviewer_type` `agent`.
  - A position is a fighter whose balance the author takes a stance on:
    `buff`, `nerf`, `keep` or `unclear`, with the meanings of the extraction
    prompt. A mention, a comparison, a victim, roster or cosmetic praise is
    not a position.
  - `character` uses the glossary canonical name. A name outside the
    glossary keeps its source literal and is flagged in `reason`; a
    nationality-only nickname never establishes identity.
  - System-only feedback gives `positions` [] with that reason.
- **Manifest**: version, `reviewer_type` `agent`,
  `independent_human_gold` false, source dataset path and SHA-256, archived
  run name, selection and split rules, counts by split and language,
  `labels_sha256`, and the statement that labels were written without model
  outputs.
- **Size**: about 300 comments. If the session cannot finish, it stops
  between comments with nothing committed, stashes the partial file as
  `WIP Step U0.5`, and the next annotation session continues. The set is
  committed only when complete.

### U0-L (live): step U0.6

```text
You are session U0-L (live) of the AIMediator pipeline upgrade, step U0.6.
You run on the owner's machine with the local model service.
Read: RULES.md; this work order; the plan docs/plans/pipeline-upgrade.md,
sections 1, 5.4 and 8.6 and the U0 part of section 7; the change record.
Task: record the environment and the live configuration, run the reference
runs of U0.6, measure and score them, archive the full runs, commit a
curated report and the change-record entries with "Step: U0.6".
Rules: never open, print or copy .env; pass it by path only when the
configuration uses the configured embedding provider. If doctor fails,
stop and report. Never add attribution.
Finish with a session-log entry; your final message repeats it.
```

Step notes:

- Environment record: the output of `/api/version`, the server settings of
  plan 5.4 as the owner states them, GPU model and memory, and the model
  digests from `python3 -m aimediator doctor --config <cfg>`.
- Reference runs (plan 7, U0.6), each in its own run directory:
  `u0-benchmark-off`, `u0-benchmark-shadow`,
  `u0-extraction-development-off`, `u0-silver-development-relevance`,
  `u0-quality-synthetic-shadow`. Time each with the measurement tool's wall
  time.
- Inputs: the benchmark and the two development splits are materialized
  (plan 8.6); the synthetic run reads
  `data/evaluation/evidence-quality-synthetic-v1/records.jsonl` as is (38
  authored rows, no raw data).
- The curated report `reports/<YYYYMMDD>-upgrade-baseline/` holds
  `manifest.json` (P2: record document, datasets, code version, retention
  reason, archive path) and `summary/` with the metrics and scores JSON,
  no source text.
- Full runs go to `~/Archives/AIMediator/reports/<YYYYMMDD>-upgrade-baseline/`
  with `SHA256SUMS`.
- Fill the "Live evaluations" table with one row per run. These rows are
  the full-set baseline; for the sampled sets, U0.8 gives the reference of
  U2 (UP-D17).

### U0-L2 (live): step U0.8

Step U0.7 (the samples) is committed by the owner's amendment before this
session starts.

```text
You are session U0-L2 (live) of the AIMediator pipeline upgrade, step
U0.8. You run on the owner's machine with the local model service.
Read: RULES.md; this work order; the plan docs/plans/pipeline-upgrade.md,
sections 1, 5.3, 5.4 and 8.6 and the U0 part of section 7; the change
record, especially the U0.6 sections.
Task: check the environment against the U0.6 record, materialize the
samples, run the four sample reference runs of U0.8 at HEAD, measure and
score them, archive the full runs, commit a curated report and the
change-record entries with "Step: U0.8".
Rules: never open, print or copy .env. If the environment differs from the
U0.6 record or doctor fails, stop and report. Never add attribution.
Finish with a session-log entry; your final message repeats it.
```

Step notes:

- Environment: checked as in U0.6; `runs/upgrade/live-config.json`
  unchanged.
- Inputs: materialize all four samples with the command in each sample's
  manifest (`full-balanced` too, for U7.1); check the row counts 30, 114,
  19 and 120 and record each file's SHA-256.
- Runs, each in its own run directory and process session, with the U0.6
  commands: `u0s-benchmark-off`, `u0s-benchmark-shadow`,
  `u0s-extraction-development-off`, `u0s-quality-synthetic-shadow`
  (`--stop-after quality`). Time each with the measurement tool's wall
  time.
- Scores: `score_extraction.py` with the labels of
  `extraction-precision-v1`, split development; route agreement with the
  one-off scorer of D-4 over the 19 sample cases only (give it a copy of
  `cases.json` filtered to the sample's IDs, written under
  `runs/upgrade/inputs/`).
- Record: one "Live evaluations" row per run, the set named
  `upgrade-samples-v1/<sample>` with its size; the plan 5.5 baselines T1
  to T7 on the samples beside the U0.6 values; a comparison of each sample
  row with its U0.6 row, where a difference beyond the intervals is a
  finding, not a stop.
- The curated report `reports/<YYYYMMDD>-upgrade-baseline-samples/` holds
  `manifest.json` (P2) and `summary/`, no source text; the U0.6 report is
  not changed. Full runs go to
  `~/Archives/AIMediator/reports/<YYYYMMDD>-upgrade-baseline-samples/`
  with `SHA256SUMS`.

### U0-V (verification)

```text
You are session U0-V (verification) of the AIMediator pipeline upgrade. You
did not implement batch U0. Change nothing except the change record.
Read: RULES.md; this work order; the plan, sections 1, 5, 8 and 10 and the
U0 part of section 7; the change record.
Task: run every item of the U0-V checklist on HEAD, and append a
verification note committed with "Session: U0-V". If every item passes, tag
that commit upgrade-u0. Otherwise record the findings as fix-up steps U0.F1
and so on, and stop without tagging. Never add attribution. Your final
message repeats the verification note.
```

Checklist:

1. Boundary and commit hygiene from `upgrade-plan` (plan 8.8).
2. The lock fixture changed only in the U0.2 commit, only by the three
   existence-only `measurement.py` keys.
3. Gates, foreign directory and wheel acceptance pass; the test count is at
   least 241.
4. Recompute `ids_sha256` and `labels_sha256` of both sets; rerun the U0.3
   selection rule and compare the IDs; check the split rule on
   `extraction-precision-v1`. Recompute the four `ids_sha256` of
   `upgrade-samples-v1`, rerun their rules from the manifests and compare
   the IDs.
5. Rerun plan 8.7 and compare with the U0.4 entry.
6. The U0.6 and U0.8 report manifests name their archive paths, and their
   `SHA256SUMS` files exist; the "Live evaluations" table has the five
   reference rows of U0.6 and the four sample rows of U0.8.

## 5. Exit and handoff out

- Exit tag: `upgrade-u0`, set by U0-V.
- The next work order is [U1](u1-neutral-performance.md).

## 6. Escalation triggers

- The archive or the raw dataset is missing or differs from its manifest.
- The lock differs at any key other than the three `measurement.py` keys.
- The measured archived numbers differ from plan section 0.2 by more than
  rounding and the difference changes a baseline of plan 5.5. Other
  differences are findings for the record (U0.4) and do not stop the
  session.
- The annotation session would need model outputs to decide a label.
- `aimediator doctor` fails in the live environment.
