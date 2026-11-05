# Handoff U2: Request views

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-04
- Applies to: [pipeline upgrade plan](../pipeline-upgrade.md) batch U2; entry tag `upgrade-u1`

Work order for batch U2. The steps are defined in plan section 7 (U2) and
the target in plan 4.1, 4.3 and 4.4. This is the first batch that changes
what the models see. Every B step is measured by a live session against the
U0.6 reference and kept only under the adoption rule (plan 5.4). U2 ends at
an owner review.

## 1. Mission

- Separate the model-visible view of every request from the program
  context (LNK-01), first without changing bytes.
- Send quality requests without the source row, the contract and the
  attempt number, and make attempt 2 a repair attempt (LAT-01, PRM-05).
- Trim extraction requests (LAT-02) and relevance requests (LAT-03).
- Trial a response template in extraction requests (UP-D06).
- Pin the payload contract with a test, an ADR and the design documents.

## 2. Entry conditions

- Tag `upgrade-u1` exists. Clean tree, no `WIP Step` stash, the gates pass.
- UP-D04, UP-D05 and UP-D07 are answered; UP-D06 is needed for U2.5 only.
- The U0.6 reference rows exist in the change record.

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/(runner|stages|pipeline|resources|evidence|evidence_quality|fixture_transport|diagnostics|operations|engine)\.py$|src/aimediator/assets/prompts/(evidence-quality|relevance|retrieval-review|summarize-balance)\.(en|zh)\.txt$|tests/|scripts/experiments/|reports/[0-9]{8}-upgrade-u2-evaluation/|docs/records/[0-9]{8}-pipeline-upgrade\.md$|docs/decisions/0003-[a-z0-9-]+\.md$|docs/design/[a-z0-9-]+\.md$|docs/README\.md$)
```

- **Allowed**: the listed modules; the four prompt pairs, only in the step
  that names them; the lock fixture in the B steps; experiment scripts that
  build requests themselves (`diagnostics` callers) so that they follow the
  new views; ADR 0003 and its index row; design documents.
- **Not allowed**: the verify request; `quality-extract` and
  `quality-verify` appendices; policies, glossary, anchors and fixtures;
  quality or extraction schemas (beyond the response template of U2.5);
  artifact names and write order; the domain gates.
- **Decisions in force**: UP-D04 (U2.2), UP-D05 (U2.3), UP-D07 (U2.4),
  UP-D06 (U2.5).
- **Owner actions**: run or authorize U2-L1 and U2-L2; review the batch.

## 4. Sessions

### U2-1 (implementation): steps U2.1 to U2.4

### U2-2 (implementation): steps U2.5 and U2.6, after U2-L1

Both use this prompt, with their own session ID and step range:

```text
You are session U2-<k> (implementation) of the AIMediator pipeline upgrade,
steps <first> to <last>.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/pipeline-upgrade-handoffs/u2-request-views.md); the plan
docs/plans/pipeline-upgrade.md, sections 1 to 5, the U2 part of section 7,
and sections 8 and 10; design/cli.md section 5; the change record.
Task: execute your steps in order, inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates, including the
  behavior lock, after every commit.
- One kind of operation per commit, with "Step: U2.x" and the step's
  "Decision: UP-Dnn" in the body. A B step lists the changed lock paths and
  adds its "Behavior changes" rows (old and new SHA-256 of each asset).
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **U2.1** N (LNK-01)
  - `stages.view(stage, data, ids)` returns the model-visible data. For
    `verify` it is today's `prepare`; for the other stages it returns
    `data` itself in this step. Keep `prepare` as an alias if a caller
    needs it.
  - `Runner._generate` builds the payload from the view and passes the
    full `data` to `stages.schema_for`. `stages.normalize` receives the
    full `data` for relevance, retrieval review, quality and extract, and
    the view for `verify`, whose verdict `scope` reads
    `selected_source_segments` from the view (`stages.py` line 128).
    Passing the full `data` there changes 13 lock keys in `enforce`.
  - `stages.MODEL_VISIBLE`: per stage, the set of top-level and
    `comments[]` keys the view may hold, equal to today's keys.
  - `Runner` accepts an optional `request_context` (default `None`) that
    enters the cache identity only when it is not `None`, so this step
    changes no identity.
  - Lock unchanged.
- **U2.2** B (LAT-01, PRM-05, UP-D04)
  - Quality view of plan 4.1. `source`, `quality_contract` and `attempt`
    stay in the context. The character reference holds only entries with a
    candidate in the comment (`evidence.character_candidates`).
  - `request_context` = `{'attempt': n}`.
  - Attempt 2 adds `previous_attempt_errors`: the validation errors of
    attempt 1, at most 20 entries, each cut to 300 characters. A transport
    failure of attempt 1 gives the single entry `transport failure` and no
    remote text.
  - Prompt pair `evidence-quality.{en,zh}`: one paragraph that explains
    `previous_attempt_errors` (repair the annotation; never copy the error
    text into it). No other prompt change.
  - Update `FixtureTransport` only if it reads a removed key.
  - The specification's retry rule (evidence-quality.md section 3.2) now
    holds through `previous_attempt_errors`; write that into the design
    document.
- **U2.3** B (LAT-02, UP-D05)
  - Extraction view of plan 4.1: units carry `evidence_id` and `text`;
    the reference keeps the entries with a candidate in the batch;
    `allowed_quality_points` keeps the fields of plan 4.1, with `quotes`
    taken from the selected segments.
  - `ground_claim`, `bind_claim` and `schema_for` still read the full
    context, so the gates are unchanged.
  - `diagnostics.extract` follows the same view.
- **U2.4** B (LAT-03, UP-D07)
  - The relevance and retrieval-review prompt pairs gain a last line that
    introduces the topic list. `resources.prompts` appends one line per
    anchor, `P1: <text>` to `N10: <text>`, in the order of
    `retrieval-anchors.json`, to those two stages only.
  - `retrieved_topics` items keep `topic_id` and `cosine`, rounded to 4
    decimals.
  - `prompt-snapshot.json` changes accordingly; `replay_balance_admission.py`
    will refuse the new prompts by design (it checks prompt hashes).
- **U2.5** B (LAT-02, UP-D06, trial), after U2-L1
  - Response template of plan 4.3 for `extract` only. `format` keeps the
    full schema.
  - Requirement: the template text is at most 30 % of the characters of
    the per-request schema copy it replaces, measured on the demo
    requests.
  - The extraction prompt pair says where the allowed values are.
- **U2.6** N, after U2-L2
  - Payload test: every request of the demo (three modes) and of lock target
    L2 holds only `stages.MODEL_VISIBLE` keys, and the non-comment
    characters of each user message stay within the budgets measured in
    U2-L1 plus 20 %, written as constants in the test with that origin.
  - ADR `docs/decisions/0003-model-visible-request-views.md`: context,
    decision, the measured effects, consequences; index row.
  - design/cli.md section 5 (`runner`, `stages` contracts and the frozen
    request construction text), balance-analysis.md (prompts, admission,
    output), evidence-quality.md (inputs, retry).

### U2-L1 and U2-L2 (live)

```text
You are session U2-L<k> (live) of the AIMediator pipeline upgrade. You run
on the owner's machine with the local model service.
Read: RULES.md; this work order; the plan, sections 1, 5 and 8.6 and the U2
part of section 7; the change record, especially the U0.6 rows.
Task: check the environment against the U0.6 record, run the runs listed
for your session at HEAD, measure and score them, apply the adoption rule
to each step under evaluation, archive the full runs, and record the
results in the change record and in
reports/<YYYYMMDD>-upgrade-u2-evaluation/, committed with
"Session: U2-L<k>" in the body.
Rules: never open, print or copy .env. If the environment differs from the
U0.6 record or doctor fails, stop and report. Do not revert anything
yourself: record a failed step for the owner's review. Never add
attribution.
Finish with a session-log entry; your final message repeats it.
```

Runs:

- **U2-L1** at the U2.4 commit: `u2l1-benchmark-off`, `u2l1-benchmark-shadow`,
  `u2l1-extraction-development-off`, `u2l1-silver-development-relevance`,
  `u2l1-quality-synthetic-shadow`. Verdicts: U2.2 on quality validity,
  route agreement and quality tokens (T2); U2.3 on extraction precision and
  recall and extraction tokens (T1); U2.4 on relevance agreement and
  relevance tokens (T3). A curated report summarizes both sessions; U2-L1
  creates it, U2-L2 adds its summary file in its own commit.
- **U2-L2** at the U2.5 commit: `u2l2-benchmark-off`,
  `u2l2-extraction-development-off`; reference U2-L1. Verdict on U2.5.

### U2-V (verification)

```text
You are session U2-V (verification) of the AIMediator pipeline upgrade. You
did not implement batch U2. Change nothing except the change record.
Read: RULES.md; this work order; the plan, sections 1, 2, 4, 5, 8 and 10
and the U2 part of section 7; ADR 0003; the change record.
Task: run every item of the U2-V checklist on HEAD, and append a
verification note committed with "Session: U2-V". If every item passes, tag
that commit upgrade-u2-review and stop for the owner's review. Otherwise
record fix-up steps U2.F1 and so on and stop without tagging. Never add
attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary and commit hygiene from `upgrade-u1` (plan 8.8).
2. Every lock-fixture change belongs to U2.2, U2.3, U2.4 or U2.5 and names
   its decision; U2.1 and U2.6 left the fixture unchanged.
3. The "Behavior changes" table lists every changed prompt asset with old
   and new SHA-256; recompute the new values.
4. The payload test passes, and a quality request of the demo contains no
   key `source`, `quality_contract` or `attempt`.
5. Every B step has a recorded verdict under the adoption rule; a failed
   step is marked for the owner's review.
6. Gates, foreign directory and wheel acceptance pass; ADR 0003 and the
   index row exist.

## 5. Exit and handoff out

- Review tag `upgrade-u2-review` (U2-V); after the owner's review a closure
  session records it, reverts rejected steps as fix-up steps and tags
  `upgrade-u2`.
- The next work order is [U3](u3-concurrency-and-caching.md).

## 6. Escalation triggers

- A view change would need a change to a gate, a schema or the verify
  request.
- A live result fails the adoption rule (record and continue; the owner
  decides at the review).
- U2.5 cannot meet the 30 % requirement without dropping a rule the model
  needs.
- `FixtureTransport` cannot answer a new view without changing the fixture
  cases (invariant 2.1.6).
