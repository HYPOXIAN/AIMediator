# Handoff U4: Quality annotation v2

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-04
- Applies to: [pipeline upgrade plan](../pipeline-upgrade.md) batch U4; entry tag `upgrade-u3`

Work order for batch U4. The steps are defined in plan section 7 (U4) and
the target in plan 4.2. The program segments every evidence unit into
clauses; the model only labels the clauses and groups them into
information points. Routing rules do not change: v2 annotations are
converted into the v1 shape and routed by the existing `qualify`. U4 ends at
an owner review.

## 1. Mission

- Deterministic clause segmentation with exact offsets (ALG-01).
- Check that the frozen fixtures can answer v2 requests (U4.2).
- The v2 schema with enumerated IDs and literals, its validation and the
  conversion to v1 (ALG-01, ALG-02).
- v2 requests, policy and prompts in the pipeline; readers that accept both
  versions (UP-D10).
- Measure validity and time against the reference (T4, T5).

## 2. Entry conditions

- Tag `upgrade-u3` exists. Clean tree, no `WIP Step` stash, the gates pass.
- UP-D10 is answered (U4.4 to U4.6).
- U2.1 and U2.2 are in effect (request views; no run identity in quality
  requests).

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/(evidence|evidence_quality|stages|pipeline|runner|fixture_transport|review|reporting|evaluation|quality_scoring|design_briefs|legacy_review|diagnostics|measurement)\.py$|src/aimediator/assets/configs/evidence-quality-policy\.json$|src/aimediator/assets/prompts/(evidence-quality|quality-extract|quality-verify)\.(en|zh)\.txt$|tests/|scripts/experiments/|reports/[0-9]{8}-upgrade-u4-evaluation/|docs/records/[0-9]{8}-pipeline-upgrade\.md$|docs/decisions/0005-[a-z0-9-]+\.md$|docs/design/[a-z0-9-]+\.md$|docs/README\.md$)
```

- **Allowed**: the listed modules; the policy file and the three prompt
  pairs in U4.4 (the policy also in U4.6); the lock fixture in U4.4 to
  U4.6; ADR 0005; design
  documents.
- **Not allowed**: `src/aimediator/assets/fixtures/cases.json` and every
  published evaluation set (invariant 2.1.6); the routing rules of
  `qualify`; the emotion measurement; extraction and verify requests other
  than the quality appendices; v1 validation of stored records.
- If U4.2 escalates and the owner approves the fallback of plan 4.2, the
  boundary gains `src/aimediator/assets/fixtures/quality-cases-v2\.json` and
  `data/evaluation/evidence-quality-synthetic-v2/`, recorded in the change
  record.
- **Decisions in force**: UP-D10 (U4.4 to U4.6).
- **Owner actions**: run or authorize U4-L; review the batch.

## 4. Sessions

### U4-1 (implementation): steps U4.1 to U4.3

### U4-2 (implementation): steps U4.4 and U4.5

### U4-3 (implementation): steps U4.6 and U4.7, after U4-L

All three use this prompt, with their own session ID and step range:

```text
You are session U4-<k> (implementation) of the AIMediator pipeline upgrade,
steps <first> to <last>.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/pipeline-upgrade-handoffs/u4-quality-segmentation.md); the plan
docs/plans/pipeline-upgrade.md, sections 1 to 5, the U4 part of section 7,
and sections 8 and 10; docs/design/evidence-quality.md sections 3 and 4;
the change record.
Task: execute your steps in order, inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates, including the
  behavior lock, after every commit.
- One kind of operation per commit, with "Step: U4.x" and, for U4.4 to
  U4.6, "Decision: UP-D10" in the body. A B step lists the changed lock
  paths and adds its "Behavior changes" rows.
- Never add any attribution. Never edit assets/fixtures/cases.json.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **U4.1** N: `evidence.clause_segments(units)` as in plan 4.2.
  - Split points: after `,` `;` `:` and their full-width forms, and after
    `、`, when the character before and the character after are not both
    digits. Trailing punctuation stays left; whitespace at the edges is
    dropped; a unit without a split point is one segment.
  - Each segment: `segment_id` `E<n>.<k>`, `evidence_id`, `text`, `start`,
    `end`, with `text == original[start:end]`.
  - Property tests over every `text_original` of the tracked evaluation
    sets and fixtures: segments are ordered, disjoint, inside their unit,
    and together cover every non-whitespace character of every unit.
  - Unit tests: mixed scripts, emoji, combining marks, CRLF, `1.5`, `1,000`,
    move notation such as `2MP`, empty and punctuation-only units.
- **U4.2** N `chore`: a test that maps each of the 38 fixture annotations
  onto clause segments. A case maps when every v1 segment is a union of
  whole clause segments; the derived labels are the v1 segment's labels,
  and the points keep their segment sets.
  - All 38 map: keep the test; `FixtureTransport` derives v2 answers in
    U4.4.
  - Any case does not map: commit nothing but the record entry, escalate
    with the cases and the options of plan 4.2, and stop before U4.4.
- **U4.3** N: `evidence_quality.annotation_schema_v2(comment_id, segments,
  literals)`, `validate_annotation_v2` and `to_v1_annotation` as in plan
  4.2. The schema uses `quality_obj`; its property order is part of this
  step's design and is pinned by a test like `tests/test_schema.py`.
  Unit tests for structure errors, foreign segment IDs, a literal outside
  the selected segments, and the round trip v2 to v1 to `qualify` on the
  fixture cases (same routing as the v1 annotations).
- **U4.4** B (UP-D10)
  - Quality view v2 of plan 4.1; `schema_for('quality', ...)` builds the v2
    schema from the context; `normalize` validates v2, converts to v1 and
    keeps both the v2 annotation and the derived v1 annotation in the
    record (`annotation` is the v1 shape, so routing and readers stay;
    `annotation_v2` is new).
  - Policy file in place: `version` `evidence-quality-policy-v2`,
    `schema_version` `evidence-quality-v2`, `segmentation_version`
    `clause-v1`; `load_policy` checks the new keys.
  - Prompt pair `evidence-quality.{en,zh}` rewritten for labeling given
    segments: the same decisions about current position, information level
    and scope, without any offset or quote instruction; two short authored
    examples per language. `quality-extract` and `quality-verify` change
    only where they name segment fields.
  - `FixtureTransport` answers v2 from the mapping of U4.2.
- **U4.5** B (UP-D10): readers dispatch on each record's `schema_version`:
  `review.load_run` (v1 records keep v1 validation; v2 records are
  validated by v2 and their derived v1 annotation must equal the stored
  one), `evaluation.evaluate_quality`, `quality_scoring.evaluate`,
  `legacy_review.apply_review`, `design_briefs.quality_design_errors`
  (accepts both schema versions). Tests: review and report of a v2 demo
  run, and of a synthetic run folder whose quality records are v1 records
  built by `qualify` from the v1 fixture annotations (tests cannot check
  out older code; the verification session does that, checklist item 4).
- **U4.6** B (LAT-07, UP-D10, conditional), after U4-L: only if every
  quality request of U4-L had prompt plus output below 6,000 tokens, set the
  policy's `num_ctx` to 8192, with its lock update; otherwise record
  `skipped` with the measured maximum.
- **U4.7** N, after U4-L: ADR `docs/decisions/0005-program-segmentation-of-quality-annotations.md`;
  evidence-quality.md (sections 3 and 4 marked as v1 where they describe
  offsets, with the v2 contract added), emotion-quantification-and-evidence-isolation.md,
  design/cli.md section 5.

### U4-L (live)

```text
You are session U4-L (live) of the AIMediator pipeline upgrade. You run on
the owner's machine with the local model service.
Read: RULES.md; this work order; the plan, sections 1, 4.2, 5 and 8.6 and
the U4 part of section 7; the change record.
Task: check the environment, run the U4-L runs at the U4.5 commit, measure
and score them, apply the adoption rule, archive the full runs, and record
the results in the change record and in
reports/<YYYYMMDD>-upgrade-u4-evaluation/, committed with "Session: U4-L"
in the body.
Rules: never open, print or copy .env. If the environment differs from the
U0.6 record or doctor fails, stop and report. Do not revert anything
yourself. Never add attribution.
Finish with a session-log entry; your final message repeats it.
```

Runs: `u4-benchmark-shadow`, `u4-benchmark-enforce`,
`u4-quality-synthetic-shadow`, and the archived quality development sources
in `shadow`. Report T4 and T5, first-attempt and final validity, the error
classes of failed attempts, route agreement on the synthetic cases, the
largest prompt plus output token count (for the `num_ctx` follow-up), and
the extraction and audit counts of the `enforce` run.

Inputs (UP-D17): the benchmark and the synthetic cases are the
`latency-benchmark` and `quality-synthetic` samples of plan 5.3. Cut by
UP-D18: `u4-benchmark-enforce` and the archived quality development
sources are not run, and the report leaves out the extraction and audit
counts of the `enforce` run.

### U4-V (verification)

```text
You are session U4-V (verification) of the AIMediator pipeline upgrade. You
did not implement batch U4. Change nothing except the change record.
Read: RULES.md; this work order; the plan, sections 1, 2, 4.2, 5, 8 and 10
and the U4 part of section 7; ADR 0005; the change record.
Task: run every item of the U4-V checklist on HEAD, and append a
verification note committed with "Session: U4-V". If every item passes, tag
that commit upgrade-u4-review and stop for the owner's review. Otherwise
record fix-up steps U4.F1 and so on and stop without tagging. Never add
attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary and commit hygiene from `upgrade-u3` (plan 8.8).
2. `git diff upgrade-u3..HEAD -- src/aimediator/assets/fixtures/cases.json data/evaluation`
   prints nothing (unless the owner approved the plan 4.2 fallback, which
   then adds only new files).
3. The routing rules are unchanged: `qualify` has no diff, and the round
   trip test of U4.3 passes.
4. A v1 demo run made by `upgrade-u3` code still passes `review export`,
   `review import` and `report` at HEAD.
5. The lock changed only in U4.4, U4.5 and U4.6, each with
   `Decision: UP-D10`; the "Behavior changes" table lists the policy and
   the three prompt pairs with recomputable SHA-256 values.
6. U4-L verdicts are recorded; gates, foreign directory and wheel
   acceptance pass; ADR 0005 and its index row exist.

## 5. Exit and handoff out

- Review tag `upgrade-u4-review` (U4-V); after the owner's review a closure
  session records it and tags `upgrade-u4`.
- UP-D18: when the review recorded under the owner's standing instruction
  yields no fix-up step, U4-V records it in its own commit
  (`docs: record the owner review of batch U4`, "Session: U4-V") and sets
  `upgrade-u4` after `upgrade-u4-review`; otherwise the closure session
  runs as above.
- The next work order is [U5](u5-extraction-precision.md).

## 6. Escalation triggers

- A fixture case does not map onto clause segments (U4.2).
- Clause segmentation would need a split rule that changes evidence-unit
  boundaries or E-IDs.
- A v2 annotation that validates converts into a v1 annotation that fails
  v1 validation.
- U4-L shows lower first-attempt validity or route agreement than the
  reference.
