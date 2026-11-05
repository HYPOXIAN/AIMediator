# Handoff U5: Extraction precision

- Type: Agent handoff
- Status: Archived
- Updated: 2026-11-05
- Applies to: [pipeline upgrade plan](../pipeline-upgrade.md) batch U5; entry tag `upgrade-u4`
- Archived 2026-11-05 when the pipeline upgrade was completed (tag `upgrade-done`).

Work order for batch U5. The steps are defined in plan section 7 (U5) and
the target in plan 4.3. Three independent changes to the extraction request
and prompts, each followed by its own live session and kept only under the
adoption rule. The verify prompts do not change in this batch, so the audit
stays a fixed yardstick. The batch ends with an owner review; the test
split of `extraction-precision-v1` runs only in U7.2.

## 1. Mission

- Generate evidence before the subject: evidence-first property order
  (PRM-02).
- Make the model declare the subjects of a comment before its claims, with
  a program gate (PRM-03).
- Add authored examples to the extraction prompts (PRM-04, PRM-01).
- Measure precision and recall on the `extraction-precision-v1`
  development split (T6, T7).

## 2. Entry conditions

- Tag `upgrade-u4` exists (or `upgrade-u3` if the owner swapped U4 and U5).
  Clean tree, no `WIP Step` stash, the gates pass.
- UP-D11 is answered.
- U2.3 is in effect (extraction view).
- The latest accepted live reference for `extraction-precision-v1`
  development and the benchmark in `off` is in the change record.

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/(evidence|stages|pipeline|inference|diagnostics|fixture_transport|review|legacy_review|measurement)\.py$|src/aimediator/assets/prompts/(summarize-balance|quality-extract)\.(en|zh)\.txt$|tests/|scripts/experiments/|reports/[0-9]{8}-upgrade-u5-evaluation/|docs/records/[0-9]{8}-pipeline-upgrade\.md$|docs/design/(cli|balance-analysis)\.md$)
```

- **Allowed**: `evidence.CLAIM` and the extraction schema in `stages`; the
  extraction prompt pairs; the program gate for `subjects`; the lock
  fixture in U5.1 to U5.3; the two design documents.
- **Not allowed**: the verify prompts and the verify request; the
  relevance, quality and retrieval-review stages; the source-binding,
  identity and numeric checks (the `subjects` gate is added, nothing is
  removed or relaxed); evaluation sets; any test-split run.
- **Decisions in force**: UP-D11 (U5.1 to U5.3).
- **Owner actions**: run or authorize U5-L1 to U5-L3; review the batch.

## 4. Sessions

Implementation and live sessions alternate: U5-1 (U5.1), U5-L1, U5-2
(U5.2), U5-L2, U5-3 (U5.3), U5-L3, U5-4 (U5.4).
A step that fails its live session is reverted by the next implementation
session as a fix-up step before it starts its own step, unless the owner
says otherwise; the change record states which.

Implementation prompt, with the session ID and step:

```text
You are session U5-<k> (implementation) of the AIMediator pipeline upgrade,
step <U5.x>.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/pipeline-upgrade-handoffs/u5-extraction-precision.md); the plan
docs/plans/pipeline-upgrade.md, sections 1 to 5, the U5 part of section 7,
and sections 8 and 10; docs/design/balance-analysis.md; the change record,
especially the verdict of the previous live session.
Task: if the previous step failed its live session, first revert it as a
fix-up step; then execute your step inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates, including the
  behavior lock, after every commit.
- One kind of operation per commit, with "Step: U5.x" and
  "Decision: UP-D11" in the body. List the changed lock paths and add the
  "Behavior changes" rows.
- Never inspect test-split comments or labels (the scoring tool reads only
  the split it is given), and never use any comment of
  extraction-precision-v1 as a prompt example.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **U5.1** B (PRM-02): reorder `evidence.CLAIM` to `evidence_ids`,
  `character`, `target`, `direction`, `recommendation`, `specificity`,
  `parameters`, `uncertain`. `stages.schema_for('extract', ...)` keeps the
  order when it narrows properties and appends `quality_point_ids` last.
  `proposal_hash` sorts keys, so review fingerprints keep their meaning;
  check that review export and import of a demo run still pass.
  - The duplicate-claim loop guard of `inference.streamed_chat` finds claim
    objects by their first property (today the literal `"character"`).
    Derive that property inside `inference` from the request's own schema:
    the first key of the claim item properties under
    `payload['format']['properties']['assessments']['properties'][<comment
    ID>]['properties']['claims']['items']['properties']` (after U5.2, of
    the `claims` property inside `{subjects, claims}`). `inference` may not
    import `evidence` (layering table), and `runner` is outside this work
    order's boundary. Without this the guard silently stops detecting
    repeated claims.
  - Extend the U1.3 equivalence streams with the new order. For those
    streams the expected result differs from the old copy: the new guard
    detects the duplicate-claim loop, the copy of the old function does not.
- **U5.2** B (PRM-03)
  - Each comment's schema becomes `{subjects, claims}`, `subjects` before
    `claims`: an array of the comment's allowed characters with
    `uniqueItems`, empty when no character is allowed.
  - `stages.normalize` keeps `subjects` in the assessment; the pipeline adds
    the source-binding error `Claim character not declared as subject` for
    a claim whose character is not in `subjects`.
  - The loop guards of `inference.streamed_chat` still find the comment
    keys and the claims inside `{subjects, claims}`; add a test.
  - The extraction prompt pair defines `subjects` in two sentences: the
    fighters whose balance the author takes a position on; a mention,
    comparison, victim or cosmetic remark does not make a subject.
  - `FixtureTransport` fills `subjects` from the characters of its claims.
- **U5.3** B (PRM-04, PRM-01)
  - Three authored examples per language at the end of each extraction
    prompt, marked as synthetic, with input units and the expected JSON:
    a long pros-and-cons review that only mentions fighters (`subjects`
    and `claims` empty); a conditional threat (`nerf`); a system complaint
    next to a fighter's name (no claim for that fighter). The Chinese prompt
    adds an example whose direction is `unclear` with `uncertain` true, and
    one where a general complaint gives a qualitative claim.
  - Keep each example under 400 characters; record the prompt sizes.
- **U5.4** N: balance-analysis.md (output and claim contract, prompts) and
  design/cli.md section 5 (`evidence.CLAIM`, `stages`).

Live prompt, with the session ID:

```text
You are session U5-L<k> (live) of the AIMediator pipeline upgrade. You run
on the owner's machine with the local model service.
Read: RULES.md; this work order; the plan, sections 1, 5 and 8.6 and the U5
part of section 7; the change record.
Task: check the environment, run extraction-precision-v1 development and
the benchmark in off at HEAD, measure and score them against the latest
accepted reference, apply the adoption rule to the step under evaluation,
archive the full runs, and record the results in the change record and in
reports/<YYYYMMDD>-upgrade-u5-evaluation/, committed with
"Session: U5-L<k>" in the body.
Rules: never open, print or copy .env. If the environment differs from the
U0.6 record or doctor fails, stop and report. Never run the test split.
Do not revert anything yourself. Never add attribution.
Finish with a session-log entry; your final message repeats it.
```

**UP-D19 (owner, 2026-11-05).** The live session runs through the API
bridge of plan 5.4 ("Hosted API") with `runs/upgrade/live-config-api.json`,
after `bash runs/upgrade/tools/api_bridge_start.sh`. In the prompt above,
"the local model service" reads as the bridge, and "the U0.6 record" of
the environment check reads as the bridge record of U2-L0. References
and baselines named U0.8 or U0.6 are their U2-L0 API runs; local rows are
never compared with API runs.

Each live session reports, against the reference: precision of accepted and
of generated claims, recall over all and over admitted positions, by
language; the share of audited claims rejected (T6); claims per comment for
comments over 400 characters; extraction prompt and output tokens; failures.

Inputs (UP-D17): `extraction-precision-v1` development means its
`extraction-development` sample of plan 5.3 (114 comments) and the
benchmark its `latency-benchmark` sample (30); scoring keeps the labels of
`extraction-precision-v1` and the development split. Cut by UP-D18: the
benchmark run is dropped; each U5-L session runs only the
`extraction-development` sample, and rule 2 of plan 5.4 counts the
technical failures of that run against its reference.

### U5-V (verification)

```text
You are session U5-V (verification) of the AIMediator pipeline upgrade. You
did not implement batch U5. Change nothing except the change record.
Read: RULES.md; this work order; the plan, sections 1, 2, 4.3, 5, 8 and 10
and the U5 part of section 7; the change record.
Task: run every item of the U5-V checklist on HEAD, and append a
verification note committed with "Session: U5-V". If every item passes, tag
that commit upgrade-u5-review and stop for the owner's review. Otherwise
record fix-up steps U5.F1 and so on and stop without tagging. Never add
attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary and commit hygiene from the entry tag (plan 8.8).
2. `git diff <entry tag>..HEAD -- src/aimediator/assets/prompts/verify-balance.en.txt src/aimediator/assets/prompts/verify-balance.zh.txt src/aimediator/assets/prompts/quality-verify.en.txt src/aimediator/assets/prompts/quality-verify.zh.txt`
   prints nothing.
3. Every B step has a live verdict; every failed step is reverted or kept
   by a recorded owner decision.
4. No run directory or change-record entry of U5 uses the
   `extraction-precision-v1` test split.
5. No prompt example matches a comment of `extraction-precision-v1` (search
   the prompt text for each labeled comment's first 30 characters).
6. Gates, foreign directory and wheel acceptance pass.

## 5. Exit and handoff out

- Review tag `upgrade-u5-review` (U5-V); after the owner's review a closure
  session records it and tags `upgrade-u5`.
- UP-D18: when the review recorded under the owner's standing instruction
  yields no fix-up step, U5-V records it in its own commit
  (`docs: record the owner review of batch U5`, "Session: U5-V") and sets
  `upgrade-u5` after `upgrade-u5-review`; otherwise the closure session
  runs as above.
- The next work order is [U6](u6-module-linkage.md).

## 6. Escalation triggers

- A step improves precision but lowers recall by more than the adoption
  rule allows (record; the owner decides).
- The `subjects` gate would reject claims that the labels count as correct
  in more than a handful of cases: the definition in the prompt is likely
  wrong.
- An example would need real corpus text.
- The test split would be needed before U7.2.
