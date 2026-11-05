# 0003 Model-visible request views and the payload contract

- Type: Decision
- Status: Active
- Updated: 2026-11-05
- Applies to: `aimediator` 0.1.0 from pipeline upgrade batch U2 (steps U2.1 to U2.4, U2.6); `RULES.md` v1.4
- Owner decisions UP-D04, UP-D05 and UP-D07 of the
  [pipeline upgrade plan](../plans/pipeline-upgrade.md) (section 4.1); the
  execution and the live measurements are recorded in the
  [change record](../records/20261104-pipeline-upgrade.md).

## Context

Before batch U2 every model request carried the whole program context of its
stage. `Runner` serialized the data a stage function built, so the model saw
what the program needed for schema construction, source binding and
routing:

- **Quality** requests carried the source row, the quality contract (run
  identity, policy and schema versions) and the attempt number, and the full
  character reference. The attempt number made attempt 2 a new request, but
  its content otherwise repeated attempt 1.
- **Extraction** requests carried evidence units with offsets, the full
  routing entry of every allowed quality point (segments with offsets and
  labels, route, reason) and the full character reference.
- **Relevance and retrieval-review** requests repeated the text and class of
  every retrieved topic in every comment.

Prompt tokens were the main cost of every stage (plan section 3.1). Program
context in the request is also a coupling: a key added for the program
reached the model and changed the request bytes and the cache identity.

## Decision

1. **A view per stage.** `stages.view(stage, data, ids)` returns the
   model-visible data; `Runner` sends `{**view, 'response_schema': schema}`
   and keeps `data` as the context of `stages.schema_for`, `ground_claim`,
   `bind_claim` and `stages.normalize` (which receives the view for `verify`
   only). Program context that must separate requests, such as the quality
   attempt, enters the cache identity as `request_context` and is not sent.
2. **The views** (plan 4.1): quality sends the units, the language, the
   reference entries with a candidate in the comment and, on attempt 2,
   `previous_attempt_errors` (UP-D04); extraction sends units without
   offsets, the reference entries with a candidate in the batch and trimmed
   `allowed_quality_points` (UP-D05); relevance and retrieval review send the
   comment with the IDs and rounded cosines of its retrieved topics, whose
   texts move once into the system prompt (UP-D07). The verify request is
   unchanged.
3. **The payload contract.** `stages.MODEL_VISIBLE` lists, per stage, the
   keys a view may hold at its top level and in its `comments[]` entries.
   `tests/test_request_payload.py` checks every request of the offline demo
   (three modes) and of behavior-lock target L2 (the legacy runner, three
   modes) against that table and against a per-stage budget of non-comment
   characters in the user message: the user message minus the JSON-encoded
   comment texts it carries (`comments[].text`, `comments[].units[].text`,
   verify `original_evidence`). The budgets are the largest values measured
   over every request of the five U2-L1 live runs plus 20 %:

   | Stage | U2-L1 maximum | Budget |
   | ----- | ------------- | ------ |
   | relevance | 2,093 | 2,512 |
   | retrieval_review | 2,018 | 2,422 |
   | quality | 4,740 | 5,688 |
   | extract | 10,060 | 12,072 |
   | verify | 1,980 | 2,376 |

   A change that adds a key to a view, or makes the program part of a
   request grow beyond its budget, fails the test and needs its own decision.

## Measured effects

Session U2-L1 (2026-11-05) ran the code of the U2.4 commit through the
hosted-API bridge of UP-D19 against the U2-L0 reference at the U0.8 code,
on the samples of UP-D17. The readings describe the hosted model
(`deepseek/deepseek-v4-flash`), not the local models (plan 5.4):

- **Quality (U2.2)**: 1,293 uncached prompt tokens per request on the
  benchmark in `shadow` against 2,692 (−52 %; 1,957 against 3,469 in
  total), 48 % of the reference, which meets T2 (at most 71.8 %).
  First-attempt validity and route agreement on the synthetic sample are
  unchanged (13/16 and 11/16). Kept under the adoption rule.
- **Extraction (U2.3)**: 2,495 uncached prompt tokens per request on the
  benchmark in `off` against 3,771 (−34 %; 2,788 against 4,064 in total),
  66 % of the reference; T1 (at most 49.9 %) is not met. Precision of
  accepted claims on the extraction sample 74.3 % against 76.2 %, recall
  43.9 % against 48.8 %: recall falls by more than the 3-point margin, so
  U2.3 fails adoption rule 4 and is recorded for the owner's review
  (escalation E-3 of the change record). The loss is mostly Chinese, lies
  within the sampling error, and includes admission changes of U2.4.
- **Relevance (U2.4)**: 1,154 uncached prompt tokens per request against
  1,539 (−25 %; 1,439 against 1,571 in total); T3 (at most 65 %) is not
  met, because the topic list now sits in the system prompt of every
  request. Relevance agreement on the silver split 64/69 against 63/69.
  Kept under the adoption rule; more units stay pending at relevance.
- **Caveat**: the provider's prompt cache is shared across requests and
  runs, so uncached counts depend on run order; total prompt tokens fall
  in every stage and mode.

## Consequences

- Program context can grow without changing what the model sees; a view
  change is a behavior change (P7) that the payload test makes visible.
- The views read the context the stage functions build, so the gates
  (source binding, identity rules, audit) still see the full data
  (invariant 2.1.1).
- Every run made before U2.2 to U2.4 has other request bytes; such runs
  cannot be resumed with this code (plan 2.3), and
  `replay_balance_admission.py` refuses relevance prompts older than U2.4.
- The budgets come from live runs on the samples; inputs with longer
  reference lists or larger batches than the samples may need a new
  measurement before the budget is raised.
