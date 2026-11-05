# Pipeline Upgrade Plan

- Type: Plan
- Status: Active
- Updated: 2026-11-04
- Applies to: commit `d0aed08` and later; `RULES.md` v1.4; `aimediator` 0.1.0

The owner commissioned this project on 2026-11-04. It follows the code
restructuring and upgrades the analysis pipeline in four directions: run
time of live analysis, algorithms and data structures, prompts and
model-visible requests, and the links between modules that today work in
isolation. Unlike the restructuring, this project changes model requests and
outputs on purpose. Every such change is authorized by a decision in
section 9, documented under RULES.md P7 and evaluated with the local models
before it is kept.

One work order per batch in `docs/plans/pipeline-upgrade-handoffs/` assigns
the work to sessions, starting with
[U0](pipeline-upgrade-handoffs/u0-baseline-and-measurement.md). Step U0.1
creates the change record `docs/records/<YYYYMMDD>-pipeline-upgrade.md`.

> **Basis**: [RULES.md](../../RULES.md) v1.4. Rule IDs (G, D, P) are cited directly.
> **Starting point**: commit `d0aed08` on `main`, tag `restructure-b7-review`.
> 241 offline tests pass and the rule check reports 0 violations.
> **Entry condition**: the code restructuring is closed: the owner's final
> review is recorded and tag `restructure-done` exists
> ([restructuring plan](../archive/code-restructuring.md), section 12). U0 does not start before.
> **Scope**: `src/aimediator/`, `scripts/experiments/`, `tests/`, prompts and
> policies under `src/aimediator/assets/` (only under the decisions that name
> them), new evaluation sets under `data/evaluation/`, new curated
> directories under `reports/`, and the documents that describe the code.
> **Out of scope**: replacing or fine-tuning models, new data collection, a
> web interface, changes to frozen evaluation sets and records, numerical
> balance design.

---

## How to use this plan (read first)

### Audience

Any coding agent with no memory of earlier sessions, and the project owner,
who answers section 9 and runs or authorizes the live sessions. You need
this file, the handoff for your batch, `RULES.md` and the change record.
Line numbers in section 3 refer to commit `d0aed08`. Locate code by the
quoted function name when a line number no longer matches.

### Read order

1. `RULES.md`, in full. It overrides this plan (G1).
2. The handoff for your batch in `docs/plans/pipeline-upgrade-handoffs/`. It
   names your session, its steps, its boundary and what else to read.
3. This plan, sections 0 to 6, once. Then the section 7 part for your batch,
   and sections 8 and 10.
4. The change record. Its progress table names the next step.

### Resume procedure (start of every session)

1. `git status --short` must print nothing. If it prints anything, do not
   commit, stash or discard it: stop and report to the owner. Then run
   `git stash list`: an entry named `WIP Step U...` is an interrupted step
   (section 10.4).
2. Find the last finished step in the change record's progress table. Its
   commit is found with `git log --grep 'Step: U<n>.<m>'`. The last tag
   (`git describe --tags --abbrev=0`) names the last finished batch.
3. Run the gates (section 8.1). If they fail on an unmodified checkout, stop
   and report. Do not fix forward a failure you did not cause.
4. Check section 9 and the change record for the decisions the next step
   needs. If one is unanswered, skip the dependent steps (they name their
   decision) and continue with independent ones.
5. Execute the step, run the gates, commit (section 1), and continue.

### Stop conditions

Stop, write the reason in the change record, and report to the owner when:

- the behavior lock fails and the step names no decision that authorizes an
  output change;
- a gate fails and the cause is not the current step;
- a step would modify frozen content: final records, decisions and meeting
  notes (D3), `data/raw/`, a published evaluation set, an existing
  `reports/` directory;
- a step would change an asset under `src/aimediator/assets/` or the bytes
  of a model request without the decision the step names;
- a live evaluation fails the adoption rule (section 5.4);
- a step needs a new runtime dependency, Python syntax newer than 3.9, or
  network access other than the local model service in a live session;
- a session would read, print or copy `.env` or any credential (G9);
- every remaining step is blocked by an unanswered decision.

---

## 0. Baseline (measured 2026-11-04)

### 0.1 Offline, at `d0aed08`

| Item | Value |
| ---- | ----- |
| Package | 29 top-level modules and the `collection/` subpackage (8 files) |
| Offline tests | 241 pass in about 9 to 11 s; the P4 floor is 241 |
| Rule check | 0 violations; the pre-commit hook blocks commits with violations |
| Offline demo | 1.07 s plain, 1.9 s under cProfile; `evidence.character_reference` 688 calls and 0.67 s cumulative (35 %) |
| Stream loop guards (`inference.streamed_chat`) | synthetic extraction outputs in 4-character chunks: 549 chunks 0.05 s; 2,079 chunks 0.67 s; 7,709 chunks 9.5 s, growing with the square of the output length |
| `run_store.state` | 54 % of a synthetic 600-comment fixture run (restructuring record, B5.9) |

### 0.2 Live, from the archived 600-comment run

Source: `~/Archives/AIMediator/reports/latest-balanced-20261027/full-pipeline-final/`
([manifest](../../reports/20261027-balanced-validation/manifest.json),
[record](../records/20261027-balanced-validation.md)). Evidence quality
`off`, run on 2026-10-27 by the runner that preceded the package. Its prompt
snapshot equals the current assets for every stage. The quality numbers come
from `quality-live-enforce-v4` in the same archive (4 comments, 5 requests),
run by the legacy runner.

| Stage, model | Requests (fresh) | Mean elapsed | Prompt tokens | Cached tokens | Output tokens | Prefill | Decode |
| ------------ | ---------------- | ------------ | ------------- | ------------- | ------------- | ------- | ------ |
| extract, `llama3.1:latest` | 81 (62) | 20.2 s | 4,369 | — | 228 | 9.7 s | 9.6 s |
| extract, `qwen2.5:7b` | 76 (60) | 19.1 s | 3,796 | — | 336 | 6.2 s | 12.6 s |
| extract, both, fresh with cache counters | 117 | — | 4,080 | 659 | — | 7.9 s | — |
| verify, both | 387 (66) | 0.8 s | 872 | 556 | 6 to 7 | 0.6 s | 0.2 s |

- Token, prefill and decode means are over the requests that carry
  counters (58 of the 62 fresh llama requests, 59 of the 60 fresh qwen
  requests); the 5 fresh requests that a loop guard stopped carry none.
- Uncached prefill runs at about 450 tokens/s (extract) and 510 tokens/s
  (verify). The only cached prefix is the system prompt. Every 1,000
  model-visible tokens therefore cost about 2.2 s per request.
- Extraction took 2,397 s of the 2,452 s summed request time. Relevance and
  retrieval review were reused from an earlier run.
- Composition of the user message, mean characters:

  | Stage | Largest parts |
  | ----- | ------------- |
  | extract (10,702) | `response_schema` 45 %; `character_normalization_reference` 25 % (32 entries); `comments` 29 %, of which unit text 15 % |
  | relevance (4,918) | retrieved topic texts 47 %; comment text 42 % |
  | retrieval_review (4,434) | retrieved topic texts 38 %; comment text 52 % |
  | verify (1,772) | original comment 52 %; `naming_reference` 25 % |

- Quality (legacy runner): 14.0 to 23.1 s per request; 3,336 to 3,820
  prompt tokens for comments of 7 to 44 characters. The user message holds
  `source` (1.2 k characters: the whole source row, 27 fields),
  `quality_contract` (1.2 k: policy and code hashes), the character
  reference (2.5 k to 3.0 k), the schema (2.1 k) and the comment units (110
  to 250). One comment failed both attempts with the same prompt (3,820) and
  output (453) token counts and the same error,
  `Literal absent from selected spans: character_literal`.
- Claim outcomes: 404 generated; 17 quarantined by source binding; 387
  audited; 200 rejected by the semantic audit (163 unsupported, 37
  uncertain); 187 accepted. Rejection share among audited claims: comments
  with three or more claims (34 comments, 158 claims) 64 %; Chinese
  `unclear` direction (62 claims) 85 %; English `nerf` (119 claims) 55 %.
  A sample of rejected claims shows mostly real extraction errors: passing
  mentions in long pros-and-cons reviews turned into nerf requests.

Section 8.7 gives the commands that reproduce these numbers. Step U0.4
repeats them with the committed measurement tool.

---

## 1. Execution rules (apply to every step)

1. **Entry condition**: clean working tree; tests and the rule check pass.
2. **Commits**: one kind of operation per commit (G5). The subject uses
   `type: summary` with a P5 type (`feat`, `fix`, `docs`, `refactor`,
   `chore`, `data`; commits that only change tests use `chore`). The body
   names the step, and the decision when the step has one. The step's last
   commit adds or updates its row in the change record's progress table.
   **No attribution** (P6): no `Co-Authored-By` trailer, no "Generated
   with" line and no agent byline, even if the tooling suggests one.
3. **Step classes**. Every step in section 7 carries one:
   - **N** (behavior-neutral): request bytes and run artifacts stay
     identical; the behavior lock passes without regeneration. One
     exception: a step that adds a top-level module (4.11, UP-D01)
     regenerates the lock for exactly the three existence-only keys
     `L2:<off|shadow|enforce>/code-snapshot/<module>.py` that the legacy
     runner's code snapshot adds (restructuring escalation E-5); the commit
     body lists them, and no other key may change.
   - **B** (behavior change): changes request bytes, prompts, schemas,
     configuration keys or artifacts. Allowed only under the named decision.
     In the same commit it regenerates the lock
     (`python3 tests/behavior_lock.py --write`) when the lock changes, lists
     the changed lock paths and the decision in the body, adds an entry under
     "Behavior changes" in the change record with the old and new SHA-256 of
     every changed asset (P7), and updates the design documents it affects
     (D9).
   - **L** (live): a live evaluation (section 5.4). It writes only under
     `runs/`, into the batch's new curated directory under `reports/`, and
     into the change record. A live step of section 7 (U0.6, U7.1, U7.2)
     commits with `Step:`; a live session attached to a batch
     (`U2-L1`, `U3-L` and so on) commits with `Session:`.
   - **D** (data): creates a new evaluation set under `data/evaluation/`,
     frozen once committed (P1). Corrections go into a separate errata file.
4. **Gates after every step** (section 8.1): offline tests, rule check,
   behavior lock. The pre-commit hook runs only the rule check, so run the
   tests yourself before committing.
5. **Live gate**: a batch with B steps that change model-visible content
   exits only after its L session compared the batch with the reference
   measurement and applied the adoption rule (section 5.4).
6. **Batch exit**: a verification session that did not implement the batch
   reruns the gates and the installed-wheel acceptance (section 8.2), runs
   the handoff checklist, writes a verification note and sets the tag
   `upgrade-u<n>`. At a review point (U2, U4, U5, U7) it sets
   `upgrade-u<n>-review`; the batch tag (for U7, `upgrade-done`) follows the
   owner's review (section 10.5).
7. **Rollback**: revert a step with `git revert <commit>`, keeping the
   subject type of P5 (`fix: revert <summary>`) and the lines
   `Step: U<n>.<m>` and `Reverts: <hash>` in the body. A B step rejected by
   its live evaluation is reverted this way and recorded under "Live
   evaluations".
8. **Decisions found during execution**: register the question, options and
   recommendation in the change record before acting. Implement only if a
   revert fully undoes the change, it is N-class, it does not amend
   `RULES.md` and it deletes nothing without an archive copy. Otherwise mark
   it `bypassed`, keep the current state and continue.
9. **Deleting tracked files** (G6): git history is the backup. Also copy the
   files to `~/Archives/AIMediator/scripts/<YYYYMMDD>-<topic>/` with a
   `SHA256SUMS` file, check that nothing outside frozen records and the
   archive refers to them, and enter path, archive location and reason in
   the change record.
10. **Documents**: every new or moved document gets the D2 header and an
    index entry in `docs/README.md` in the same commit (D4).
11. **Test and holdout splits**: no session tunes against a test or holdout
    split. The only runs on them are in U7.2, each once.

Commit message example (item 2):

```text
feat: send only the model-visible view of quality requests

Step: U2.2
Decision: UP-D04
Lock: L1, L2 request digests and request.json of the quality stage
```

---

## 2. Invariants

### 2.1 Must not change

1. **Domain gates**: every claim is bound to immutable source spans; the
   identity rules (glossary candidates, blocked identity-only aliases,
   isolated source literals); the numeric-intent checks; the fail-closed
   semantic audit; the routing rules of `evidence_quality.qualify`; review
   cannot bypass any check; no translated or rewritten text is sent or kept
   as evidence.
2. **Coverage**: every input row has exactly one coverage record and every
   admitted comment is accounted for.
3. **CLI**: commands, exit codes and error codes. Options and configuration
   keys change only under UP-D08, UP-D09 and UP-D15.
4. **Artifact names and schema versions**, except the changes in 2.2.
5. **Determinism**: two report exports of the same run are byte-identical.
   With `max_parallel_requests` 1 and the same responses, a run's artifacts
   are byte-identical to those of the serial code.
6. **Frozen content**: final records, decisions and meeting notes (D3);
   `data/raw/`; every published evaluation set, including
   `evidence-quality-synthetic-v1` and the target of its `cases.json` link,
   `src/aimediator/assets/fixtures/cases.json` (CR-D08); existing `reports/`
   directories.
7. **Runtime**: Python 3.9 syntax; NumPy is the only runtime dependency; the
   package starts no subprocesses and works from an installed wheel outside
   the checkout.
8. **Models and routing**: `qwen2.5:7b` for Chinese, `llama3.1:latest` for
   English, `qwen3-embedding:8b` for embeddings; temperature 0 and seed 42.
9. **Earlier runs stay readable**: `review`, `report`, `status` and
   `evaluate` keep reading `aimediator-run-v1` runs written by earlier code.

### 2.2 Deliberate changes (only under their decisions)

| Change | Decision | Batch |
| ------ | -------- | ----- |
| Run manifest identity records the service version; context-window errors | UP-D03 | U1 |
| Model-visible content of quality, extract, relevance and retrieval-review requests | UP-D04 to UP-D07 | U2 |
| Configuration keys `max_parallel_requests` and `cache_dir`, matching `analyze` options | UP-D08, UP-D09 | U3 |
| Embedding cache layout and batch size; shared request cache | UP-D09 | U3 |
| `evidence-quality-v2` schema, policy v2, quality prompts | UP-D10 | U4 |
| Extraction schema order, `subjects`, extraction prompts | UP-D11 | U5 |
| Claim `target_reference`; report schema `aimediator-report-v2` | UP-D12 | U6 |
| Screening `coarse-v2` | UP-D13 | U6 |
| `near-duplicates.json`; `balance-review-policy-v3` | UP-D14 | U6 |
| Optional second audit; routing asset key | UP-D15 | U6 |
| `RULES.md` v1.5 (P4 floor) | UP-D16 | U7 |

### 2.3 Accepted consequences

- Every commit that changes a package module changes the run identity, so
  earlier CLI runs cannot be resumed (already true; ADR 0001).
- Live comparisons are between commits on fixed evaluation sets. With these
  sample sizes they are decision aids, not accuracy guarantees.
- With `max_parallel_requests` above 1, fresh inference is not bitwise
  identical to serial inference. Replay from the run journal or the shared
  cache stays exact.
- Once U2.4 changes the relevance request, the frozen 275-comment admission
  result ([record](../records/20261022-balance-review-v2.md)) stays
  historical. It is neither recomputed nor retuned.

---

## 3. Diagnosis

Every finding has an ID that later steps cite.

### 3.1 Latency

- **LAT-01** Quality requests carry program context.
  `pipeline.assess_quality` (lines 233 to 236) puts `source` (the whole
  source row), `quality_contract` (the quality identity: mode, policy and
  `run_identity` in the CLI, `operations.analyze` line 100; policy and code
  hashes in the legacy runner) and `attempt` into the request data, and
  `Runner._generate` (line 62) serializes all of it into the user message.
  Effects: the comment is 1 to 2 % of the model-visible content; metadata
  outside the input list of the
  [evidence-quality specification](../design/evidence-quality.md) (section
  3.1), such as votes, playtime and the coarse screening decision, can bias
  annotations; the run identity in the prompt makes the request for the
  same comment differ between runs, which prevents reuse and can change
  outputs.
- **LAT-02** Extraction payload: a copy of the response schema (45 %) and
  the full character reference (25 %), plus unit offsets the model does not
  use; the comment text itself is 15 % of the user message.
- **LAT-03** Relevance and retrieval review: each comment carries the full
  text of 4 retrieved anchors (47 % and 38 %). The 20 anchors are constants
  that could sit in the cached system prompt.
- **LAT-04** All model requests are serial, although quality annotations
  (per comment), audits (per claim) and single relevance rechecks are
  independent.
- **LAT-05** `run_store.state` lists every request directory before each
  request (open item B5-3 of the restructuring). Small in live runs, it
  dominates resume and replay, where every request is a cache hit.
- **LAT-06** Request and embedding caches live inside one run. A changed
  code identity forces a new run directory and full re-inference; the
  600-comment validation reused 603 requests by hand. The embedding cache is
  keyed by the composition of an 8-text batch (`retrieval.retrieve`, lines
  26 to 28), so a batch-size change invalidates it.
- **LAT-07** (low priority) The quality stage uses `num_ctx` 16384 and the
  others 8192, so the service reloads the model between stages; U4.6 acts
  on it only if U4-L shows that 8192 suffices. Progress files are rewritten
  after every record; the restructuring measured the coverage rebuild below
  its threshold (B5.9), so this plan leaves the write schedule alone.

### 3.2 Algorithms and data structures

- **ALG-01** The quality annotation asks a 7B model for absolute Unicode
  code-point offsets and verbatim quotes of every segment, which the program
  then checks (`evidence_quality.validate_annotation`), and it makes the
  output long. The failures observed so far are not offset or quote errors:
  in the diagnostic failure of 0.2 every offset and quote is correct, and a
  point names a character literal that its selected segments do not contain
  (`Literal absent from selected spans`); the two compact-quote recovery runs
  in the same archive failed with the same error and with a point/segment
  detail conflict. The v2 contract of 4.2 keeps both checks, so it removes
  the offset and quote contract but not these failure classes. The samples
  are small; U0.6 measures the failure classes on the benchmark, and UP-D10
  is answered with that measurement.
- **ALG-02** Enumerable fields of the quality schema are free strings
  (`evidence_quality.annotation_schema`, line 43 and 55): `evidence_id` and
  `character_literal`.
- **ALG-03** `evidence.character_reference(text)` matches 285 aliases on
  every call, and one claim calls it 3 to 5 times with the same text;
  `balance_policy.term_matches` builds a pattern per call.
- **ALG-04** `inference.streamed_chat` joins and rescans the whole output
  on every chunk (lines 61 to 67).
- **ALG-05** Duplicates are found by exact normalized text only (collection,
  `quality_scoring.prepare_dataset`), although retrieval already computes a
  vector for every comment.

### 3.3 Prompts and model-visible schemas

- **PRM-01** Extraction precision is the main quality bottleneck: 52 % of
  audited claims are rejected (section 0.2).
- **PRM-02** `evidence.CLAIM` (line 16) puts `character` first and
  `evidence_ids` near the end. Constrained decoding generates properties in
  schema order, so the model commits to a subject before it selects
  evidence.
- **PRM-03** Long multi-topic comments get no subject selection: every
  mentioned candidate can become the subject of a claim.
- **PRM-04** The prompts are rules without examples. The system prompt is
  the only cached prefix, so examples placed there cost almost nothing after
  the first request of a stage.
- **PRM-05** The quality retry differs from attempt 1 only by the attempt
  number in the content. With temperature 0 and seed 42 it repeated the
  failure (section 0.2).
- **PRM-06** The semantic audit uses the extraction model, so their errors
  correlate: an archived recovery run had 10 wrongly attributed Ryu claims
  accepted ([record](../records/20261027-balanced-validation.md)).

### 3.4 Module linkage

- **LNK-01** `Runner` sends the request data and the validation context as
  one object: `stages.normalize` reads `data['source']` from the same
  dictionary the model receives. No contract states what the model may see.
  This is the root cause of LAT-01.
- **LNK-02** The glossary has 849 entries. Its 818 move, system and mechanic
  entries, with 4,047 aliases, are unused by the pipeline; `glossary_vectors`
  is only a research command. Report export groups topics by normalized
  literal (`reporting.groups_for`, line 38), and the report itself states
  that this fragments equivalent topics across wording and language.
- **LNK-03** The coarse screening patterns `CHAR_ZH` and `MECH`
  (`collection/screening.py`, lines 18 and 22) are hand-written copies of
  glossary content (G2); only the English character pattern reads the
  glossary.
- **LNK-04** The run identity records model digests but not the service
  version. Batches are sized in characters, and nothing detects a prompt
  plus output reaching `num_ctx`: the largest extraction prompt was 6,478
  tokens, and `num_predict` 4,096 allows the sum to pass 8,192.
- **LNK-05** `pipeline.process` takes an argparse-style namespace that
  `operations.analyze` and `engine.run` build differently.
  `replay_balance_admission.py` builds its `Runner` without
  `quality_identity`, so it cannot replay runs made with one (open item
  B2-1 of the restructuring).

---

## 4. Target design

### 4.1 Request views (U2)

`stages.view(stage, data, ids)` returns the model-visible data. `Runner`
sends `{**view, 'response_schema': schema}` (or the response template of
4.3) and keeps `data` as context for `stages.schema_for` and, except for
`verify`, for `stages.normalize(stage, parsed, ids, data)`; the verify
verdict's `scope` reads `selected_source_segments`, which only the view
holds (`stages.py` line 128). The cache identity stays the SHA-256 of the
payload with `stream`
false plus `pipeline_quality_identity`, and adds a `request_context` for
program context that must separate requests, such as the quality attempt.
`stages.MODEL_VISIBLE` lists the allowed keys per stage. A test checks every
request of the demo and of the legacy fixture runs against that table and a
character budget.

| Stage | Model-visible keys after U2 |
| ----- | --------------------------- |
| relevance, retrieval_review | `comments[comment_id, text, retrieved_topics[topic_id, cosine]]`; the anchors are in the system prompt (4.4) |
| quality (v1) | `comments[comment_id, units[evidence_id, text, start, end]]`, `language`, `character_normalization_reference` (entries with a candidate in the comment), `previous_attempt_errors` (attempt 2 only) |
| quality (v2, U4) | `comments[comment_id, units[evidence_id, segments[segment_id, text]]]`, `language`, `character_literals` (literal names present in the comment), `previous_attempt_errors` |
| extract | `comments[comment_id, units[evidence_id, text]]`, in enforce also `allowed_quality_points[point_id, evidence_ids, quotes, scope, detail_level, stance, direction, character_literal, mechanic_literal]`; `character_normalization_reference` (entries with a candidate in the batch) |
| verify | unchanged |

### 4.2 Quality annotation v2 (U4)

- `evidence.clause_segments(units)` splits each evidence unit at clause
  punctuation (`,` `;` `:` and their full-width forms, and `、`), never
  between two digits. Trailing punctuation stays with the clause on its
  left; whitespace at the edges is dropped. IDs are `E<n>.<k>`, offsets are
  absolute code points, and the segments cover every non-whitespace
  character of every unit exactly once. Version `clause-v1`.
- Schema `evidence-quality-v2`: `comment_id`; `segment_labels`, an object
  whose required keys are the segment IDs, each with `scope`,
  `content_kind`, `emotional_tone` and `reason_code`; `information_points`
  with `segment_ids` limited to the segment IDs, `character_literal` limited
  to `null` and the literal names present, and `mechanic_literal` as a
  nullable string.
- `evidence_quality.to_v1_annotation(annotation, segments, text)` converts
  a v2 annotation into the v1 shape, with program offsets and quotes taken
  from the original. The existing `validate_annotation` and `qualify` then
  apply unchanged, so the routing rules stay (invariant 2.1.1). One check is
  new: `mechanic_literal` must occur in the selected segments.
- The policy file is updated in place: `evidence-quality-policy-v2`, schema
  `evidence-quality-v2`, `segmentation_version` `clause-v1`; the measurement
  version is unchanged. Records keep their `schema_version`. Every reader
  (`review.load_run`, `evaluation`, `legacy_review.apply_review`,
  `design_briefs.quality_design_errors`, `quality_scoring`) accepts v1 and
  v2 and validates each with its own rules.
- Fixtures: `assets/fixtures/cases.json` cannot change (invariant 2.1.6).
  `FixtureTransport` derives v2 answers from the v1 annotations when every
  v1 segment is a union of whole clause segments (checked in U4.2).
  Otherwise U4.2 escalates: a new fixture `assets/fixtures/quality-cases-v2.json`
  and a new set `evidence-quality-synthetic-v2` would be authored.

### 4.3 Extraction request v2 (U2, U5)

- View as in 4.1.
- Response template (UP-D06, trial): the user message carries
  `response_template`, one claim template that names each field and its
  rule once, and every comment entry carries its allowed values
  (`allowed_characters`, `allowed_numeric_values`, `allowed_deltas`,
  `allowed_units`). The `format` field keeps the full per-comment schema, so
  constrained decoding is unchanged.
- Property order (U5.1): `evidence_ids`, `character`, `target`, `direction`,
  `recommendation`, `specificity`, `parameters`, `uncertain`. The
  duplicate-claim loop guard of `inference.streamed_chat` recognizes claim
  objects by the first property of the claim schema in the request's
  `format`, so it follows the order without importing `evidence`, which
  the layering table forbids.
- Subjects (U5.2): each comment's object becomes `{subjects, claims}`.
  `subjects` is a unique array of the comment's allowed characters: the
  fighters whose balance the author takes a position on. A program gate adds
  the source-binding error `Claim character not declared as subject`.
- Examples (U5.3): three authored, synthetic examples per language at the
  end of the extraction prompts, labeled as synthetic and never drawn from
  an evaluation set.
- The verify prompts stay unchanged during U5, so the audit is a fixed
  yardstick while extraction changes.

### 4.4 Relevance request v2 (U2)

The relevance and retrieval-review prompt assets end with a header line for
the topic list. `resources.prompts` appends the lines `P1: <text>` to
`N10: <text>` from `retrieval-anchors.json`, so the anchors keep one source
(G2). Each `retrieved_topics` item keeps `topic_id` and `cosine`.

### 4.5 Bounded concurrency (U3)

- Configuration key `max_parallel_requests`, an integer from 1 to 8 with
  default 1, and the option `aimediator analyze --max-parallel-requests`.
- `pipeline` runs independent units through an ordered executor: at most N
  units in flight on a thread pool, results committed in input order on the
  calling thread, so trace entries, progress files and artifacts keep serial
  order. Units: one quality comment with its attempts; one audited claim;
  one relevance or retrieval-review batch; one single recheck; one
  extraction batch including its split retries, which run inside the unit
  in serial order.
- `Runner` serializes requests with the same identity; `progress` and
  `run_store` updates are serialized.
- The service needs `OLLAMA_NUM_PARALLEL` of at least N, set by the owner
  and recorded by the live session.
- With N = 1 every artifact and request is byte-identical to the serial
  code.

### 4.6 Request index and shared cache (U1, U3)

- Request index (U1.1): `Runner` takes a `journal(request_dir, completed)`
  callback, called after each `validation.json` write. `run_store` keeps a
  per-folder index and lists the request directories only the first time
  it sees a folder in a process. `run-state.json` keeps its content.
- Shared cache (U3.3): configuration key `cache_dir` (default `null`;
  recommended `runs/cache`) and a new module `cache`. The key is the
  SHA-256 of the canonical payload (with `stream` false), the model digest
  and the service version; the run identity is not part of it. Only
  responses with `done` true and `done_reason` `stop` are stored. A hit
  writes the run's `response.json` with `elapsed_seconds` 0 and a
  `reuse-provenance.json` (source, key, original elapsed time).
  `measurement` counts reused and fresh requests separately.
- Embeddings (U3.4): one record per text,
  `embeddings/<SHA-256 of model, endpoint and text>.json`; requests embed
  only missing texts, in batches of 32; the shared cache keys them by model
  digest.

### 4.7 Service identity and context guard (U1)

- `Transport.version()` calls `/api/version`. The run manifest identity
  gains `service: {"ollama_version": ...}`; resume refuses a changed version
  (exit 4). `FixtureTransport.version()` returns a fixed fixture marker.
- `Runner` adds the error `Context window reached` when the response
  reports `prompt_eval_count + eval_count >= num_ctx`. The existing failure
  handling applies: extraction batches split, quality retries, other stages
  fail closed.

### 4.8 Glossary linkage (U6)

- New module `topics` (domain layer). It indexes the glossary entries of
  every category except `character`, with their aliases and alias flags:
  `candidate_only` and `requires_context` aliases yield candidates, never
  resolved references. `target_reference(target, character)` returns the
  glossary IDs, a status (`resolved`, `candidate` or `unmatched`) and the
  matched alias. Character-scoped entries match only for their character.
- The pipeline adds `target_reference` to each grounded claim; `review`
  recomputes and compares it. Report export (`aimediator-report-v2`) groups
  by resolved glossary ID, then by literal, and keeps every literal.
  Candidates never merge groups.
- Hint list (U6.3, kept only if U6-L shows a benefit): the glossary terms
  present in a comment, added as `mechanic_terms` to the quality and
  extraction views.
- Screening `coarse-v2` (U6.4): the Chinese character pattern and the
  mechanic pattern are generated from glossary labels and aliases, plus a
  reviewed supplemental list in `configs/feedback-screening-terms.json`
  (collection configuration, P7). Datasets screened with `coarse-v1` keep
  their recorded decisions; nothing is screened again.

### 4.9 Near-duplicates (U6)

`retrieval` writes `near-duplicates.json`: clusters of comments whose vectors
have a cosine at or above `near_duplicate_cosine` (a new key in
`balance-review-policy.json`, version `balance-review-policy-v3`). The report
adds `near_duplicate_clusters` with a note; no count changes.
`quality_scoring.prepare_dataset` accepts the clusters when it assigns
splits for new annotation sets.

### 4.10 Second audit (U6, trial)

Configuration key `second_audit` (default `false`). The routing asset gains
`second_audit_models` (`en` to `qwen2.5:7b`, `zh` to `llama3.1:latest`),
which use the verify prompt of the claim's language. With the key set, a
claim is accepted only when both audits return `supported`; artifacts keep
both verdicts.

### 4.11 Module table changes (UP-D01)

New rows in the table of `tests/test_module_layers.py` and in
[design/cli.md](../design/cli.md), section 5:

| Module | Layer | May import | Step |
| ------ | ----- | ---------- | ---- |
| `measurement` | research | `common`, `quality_scoring` | U0.2 |
| `cache` | infrastructure | `common` | U3.3 |
| `topics` | domain | `resources`, `balance_policy` | U6.1 |

Changed rows: `runner` adds `cache` (U3.3); `pipeline` and `review` add
`topics` (U6.1). Each new module is also hashed into run identities
(`run_store.code_manifest`) and copied by the legacy runner into
`code-snapshot/`, which adds three existence-only lock keys (rule 1.3).

---

## 5. Evaluation and measurement

### 5.1 Offline checks

The gates (8.1), the behavior lock (8.3), the unit tests of each step and,
from U2.6, the payload test of 4.1. Tests never need a live model (P4).

### 5.2 Measurement tool (U0.2)

Module `aimediator.measurement` with thin scripts in `scripts/experiments/`:

- `request_metrics(folder)`: per stage and model, request count, fresh and
  reused requests, `done_reason` counts, requests with validation errors,
  and mean, median and maximum of prompt, cached, uncached and output
  tokens, prefill, decode and load seconds and elapsed seconds; mean
  characters of the system prompt, of `format` and of every top-level key
  of the user message; wall time from the manifest and run state. Values are
  `null` when a response has no counters (fixture runs).
- `claim_outcomes(folder)`: generated, binding-quarantined (by error),
  audit-rejected (by status) and accepted claims, by language and
  direction; coverage status counts; quality first-attempt validity,
  attempts and route counts.
- `materialize(set_dir, dataset, split=None)`: the input JSONL of an
  evaluation set, read from the raw dataset and checked against the stored
  content hashes.
- `score_positions(folder, labels, split)`: precision of accepted and of
  generated claims against comment-level (character, direction) positions,
  recall over all labeled positions and over admitted comments only, by
  language, each with Wilson 95 % intervals (`quality_scoring.proportion`).

It reads CLI runs, legacy runs and the archived run, and writes JSON only.

### 5.3 Evaluation sets

| Set | Created | Used for | Rule |
| --- | ------- | -------- | ---- |
| `latency-benchmark-v1` | U0.3 | time, tokens, failures and outcome counts in every L session | 60 IDs from `data/raw/feedback/20261027-balanced/screened/records.jsonl`: 30 English and 30 Chinese, 10 per length tercile and language, ordered by SHA-256 of `latency-benchmark-v1:<record_id>`. IDs and content hashes only |
| `extraction-precision-v1` | U0.5 | extraction precision and recall | Agent silver labels per comment: every (character, direction) position the author takes, exhaustively, plus `uncertain` and a reason. 251 comments with claims in the archived run and 50 admitted zero-claim comments chosen by hash order. Split 70/30 by SHA-256 of `extraction-precision-v1:<record_id>`; benchmark IDs forced into development. Labels are written from the source text, without the model claims |
| `balance-silver-v1` development (existing) | — | relevance agreement, character expectations | holdout only in U7.2 |
| `balance-regressions-v1` (existing) | — | known-error regressions | development |
| `evidence-quality-synthetic-v1` (existing) | — | quality route agreement on authored cases | development |
| quality development sources (existing, archived) | — | quality spot checks | `quality-live-sources.jsonl` in the archived run, development |

The test split of `extraction-precision-v1` and the holdout of
`balance-silver-v1` run once each, in U7.2.

**Samples (UP-D17).** From U0.8 on, live runs use smaller samples, frozen
in step U0.7 as `data/evaluation/upgrade-samples-v1/`. Each subdirectory
is a set that `materialize` reads; its manifest states the rule in full.

| Sample | Comments | Replaces | Rule |
| ------ | -------- | -------- | ---- |
| `latency-benchmark` | 30 | `latency-benchmark-v1` (60) | the first 5 per language and tercile in the set's own order (SHA-256 of `latency-benchmark-v1:<record_id>`); every ID is in the set |
| `extraction-development` | 114 | `extraction-precision-v1` development (227) | per language, the first half by SHA-256 of `upgrade-samples-v1:<comment_id>` (45 English, 69 Chinese); scored with the labels of `extraction-precision-v1`, which skip labeled comments absent from the run |
| `quality-synthetic` | 19 | `evidence-quality-synthetic-v1` (38) | one case per category, Chinese and English alternating in category order |
| `full-balanced` | 120 | the 600-comment dataset of U7.1 | 20 per language and tercile (the cut points of `latency-benchmark-v1`) by SHA-256 of `upgrade-samples-v1:<record_id>` |

Kept in full: the `balance-silver-v1` development split (about 3 minutes
per run), the U7.2 holdout and test runs, the archived quality development
sources (U4-L) and the PRM-06 spot check (U6-L). Wherever this plan or a
work order names a replaced input for a live run from U0.8 on, the run
uses the sample and keeps its run directory name. The U0.6 rows stay the
full-set baseline; the U0.8 rows are the sample reference.

### 5.4 Live evaluation protocol

- **Environment**, recorded in U0.6 and checked at the start of every L
  session: service version, the server settings `OLLAMA_NUM_PARALLEL`,
  `OLLAMA_FLASH_ATTENTION` and `OLLAMA_KV_CACHE_TYPE`, GPU and memory, model
  digests (from `aimediator doctor`), embedding provider. A difference from
  the U0.6 record invalidates comparisons: escalate.
- **Configuration**: `runs/upgrade/live-config.json`, created in U0.6 with
  `aimediator init` and the owner's embedding settings, and copied into the
  change record with the embedding endpoint redacted (it holds no
  credentials, only the name of the credential variable). Every L session
  uses it and changes only keys that a decision introduced.
- **Runs**: `runs/upgrade/<step>-<set>-<mode>/`, with the measurement output
  beside each run. A curated summary goes to
  `reports/<YYYYMMDD>-upgrade-<batch>-evaluation/` with a `manifest.json`
  (P2) and `summary/`; full runs are archived to
  `~/Archives/AIMediator/reports/<same name>/` with `SHA256SUMS`.
- **Reference**: the most recent accepted L measurement of the same set and
  mode; for U2 the U0.8 sample runs (UP-D17), and the U0.6 run for the
  `balance-silver-v1` development split, which is kept in full. On the
  samples the comparison is paired (the same comments on both sides), and
  the live session reports the Wilson intervals beside each difference,
  because the margins of rule 4 are close to the sampling error.
- **Adoption rule** for a B step that changes model-visible content. Keep
  the step when all hold:
  1. the gates pass;
  2. technical-failure units on the benchmark do not exceed the reference
     by more than 1, and coverage is complete;
  3. the metric the step targets moves in the intended direction;
  4. no inferiority: (character, direction) precision and recall on
     `extraction-precision-v1` development do not fall by more than 3
     percentage points; relevance agreement with the `balance-silver-v1`
     development labels does not fall by more than one comment; quality
     first-attempt validity and route agreement on
     `evidence-quality-synthetic-v1` do not fall.

  Otherwise revert the step (rule 1.7) and record the result. At a review
  point the owner may decide against the rule; the reason is recorded.

### 5.5 Objectives

Candidate targets, not guarantees. Each is measured by the L session of its
batch on `latency-benchmark-v1` unless stated otherwise. From U0.8 on, the
sets are the samples of 5.3 (UP-D17), and a baseline named U0.6 is the
U0.8 run of the same sample and mode.

| ID | Metric | Baseline | Target | Batch |
| -- | ------ | -------- | ------ | ----- |
| T1 | Extraction: mean uncached prompt tokens per request | U0.6 (archive: 3,421) | at most 1,700 | U2 |
| T2 | Quality: mean uncached prompt tokens per request | U0.6 (archive, legacy runner: 633 to 3,646 uncached; 3,336 to 3,820 in total) | at most 1,500 | U2 |
| T3 | Relevance: mean uncached prompt tokens per request | U0.6 | at most 65 % of baseline | U2 |
| T4 | Quality: mean elapsed per comment | U0.6 | at most 50 % of baseline | U4 |
| T5 | Quality: first-attempt validity | U0.6 | at least 95 % | U4 |
| T6 | Extraction: share of audited claims rejected, development | U0.6 (archive, 600 comments: 52 %) | at most 35 % | U5 |
| T7 | Extraction: (character, direction) precision of accepted claims, development | U0.6 | baseline + 10 points, recall within 3 points | U5 |
| T8 | Throughput with `max_parallel_requests` 2, quality stage | U3 L run with 1 | at least 1.4 times | U3 |
| T9 | Replay of the synthetic 600-comment fixture run: share of `run_store.state` | 54 % | below 5 % | U1 |
| T10 | Offline demo; share of `character_reference` | 1.07 s; 35 % | at most 1.0 s; below 10 % | U1 |

---

## 6. Batch overview

| Batch | Goal | Step classes | Decisions | Live session | Review point | Exit tag |
| ----- | ---- | ------------ | --------- | ------------ | ------------ | -------- |
| U0 | Baseline, measurement tool, evaluation sets | N, D, L | UP-D01, UP-D02, UP-D17 | U0-L (baseline), U0-L2 (sample reference) | none | `upgrade-u0` |
| U1 | Behavior-neutral performance, service identity | N, B | UP-D03 | none | none | `upgrade-u1` |
| U2 | Request views | N, B, L | UP-D04 to UP-D07 | U2-L1, U2-L2 | owner | `upgrade-u2` |
| U3 | Concurrency and caching | N, B, L | UP-D08, UP-D09 | U3-L | none | `upgrade-u3` |
| U4 | Quality annotation v2 | N, B, L | UP-D10 | U4-L | owner | `upgrade-u4` |
| U5 | Extraction precision | B, L | UP-D11 | U5-L1 to U5-L3 | owner | `upgrade-u5` |
| U6 | Module linkage | N, B, L | UP-D12 to UP-D15 | U6-L | none | `upgrade-u6` |
| U7 | Acceptance and documents | L, N | UP-D16 | U7-L | final | `upgrade-done` |

Batches run in order. U3 needs U2.2 (no run identity in prompts); U4 needs
U2.1 and U2.2; U5 needs U2.3. U4 and U5 are independent and may be swapped.
The test count never falls below the P4 floor (241); record it after every
step.

---

## 7. Batches

Every step ends with the gates and a commit (section 1). "Lock unchanged"
means the lock passes without regeneration.

### U0 Baseline, measurement tool and evaluation sets

Entry: tag `upgrade-plan` (the corrected plan, after `restructure-done`);
UP-D01 and UP-D02 answered.

- **U0.1** N `docs`: create the change record from the section 11 skeleton,
  dated with the start date; copy the owner's answers; add it to
  `docs/README.md`.
- **U0.2** N `feat`: module `measurement` (5.2) with `request_metrics`,
  `claim_outcomes`, `materialize` and `score_positions`; scripts
  `scripts/experiments/measure_run_requests.py`,
  `materialize_evaluation_input.py` and `score_extraction.py`; the
  `measurement` row in the layering test and in design/cli.md section 5
  (UP-D01). Tests run on a demo run and on synthetic folders.
- **U0.3** D `data`: `data/evaluation/latency-benchmark-v1/` with
  `manifest.json` and `ids.json` (record ID, language, content SHA-256,
  length tercile), selected by the rule of 5.3 (UP-D02).
- **U0.4** N `docs`: measure section 0 again at HEAD (8.4, 8.5, 8.2) and
  apply the measurement tool to the archived run (8.7); record both.
- **U0.5** D `data`: `data/evaluation/extraction-precision-v1/` with
  `manifest.json` and `labels.jsonl` by the rule of 5.3 (UP-D02), written
  by an annotation session (U0-A).
- **U0.6** L: record the environment and the live configuration (5.4).
  Reference runs: the benchmark in `off` and `shadow`; the
  `extraction-precision-v1` development split in `off`; the
  `balance-silver-v1` development split with `--stop-after relevance`; the
  38 cases of `evidence-quality-synthetic-v1` in `shadow` with
  `--stop-after quality` (route agreement over the cases that reach the
  quality stage, with denominators). Measure and score; curated summary
  `reports/<YYYYMMDD>-upgrade-baseline/`.
- **U0.7** D `data` (UP-D17): `data/evaluation/upgrade-samples-v1/` with
  the four samples of 5.3 and their manifests; added by the owner's
  amendment of 2026-11-04 after U0.6.
- **U0.8** L (UP-D17): the sample reference runs at the U0.7 commit, in
  session U0-L2: `u0s-benchmark-off` and `u0s-benchmark-shadow` (sample
  `latency-benchmark`), `u0s-extraction-development-off` (sample
  `extraction-development`) and `u0s-quality-synthetic-shadow` (sample
  `quality-synthetic`, `--stop-after quality`). Measure and score as in
  U0.6, with the 5.5 baselines on the samples; curated summary
  `reports/<YYYYMMDD>-upgrade-baseline-samples/`.

### U1 Behavior-neutral performance and service identity

- **U1.1** N `refactor` (LAT-05): request index of 4.6, and
  `scripts/experiments/run_synthetic_fixture_scale.py`, which builds the
  synthetic 600-comment fixture run of the restructuring's B5.9 (copied
  fixture cases, a matching fixture transport, `operations.analyze` in
  `shadow`). Measure T9 before and after.
- **U1.2** N `refactor` (ALG-03): cached compiled term patterns in
  `balance_policy`, and `evidence.character_reference` memoized by text,
  returning new objects on every call. Measure T10.
- **U1.3** N `refactor` (ALG-04): incremental loop guards in
  `streamed_chat`: the same stop decisions and content as before, checked
  against a copy of the old function on synthetic streams.
- **U1.4** B `feat` (LNK-04, UP-D03): service identity of 4.7.
- **U1.5** B `feat` (LNK-04, UP-D03): context guard of 4.7. Fixture
  responses carry no counters, so the lock is unchanged.
- **U1.6** N `fix` (LNK-05): `replay_balance_admission.py` passes the
  source run's `identity['evidence_quality']` as `quality_identity` when the
  manifest has one; checked on a legacy fixture run.

### U2 Request views

- **U2.1** N `refactor` (LNK-01): `stages.view`, `stages.MODEL_VISIBLE` and
  the context split of 4.1, with each view equal to the current data; lock
  unchanged.
- **U2.2** B `feat` (LAT-01, PRM-05, UP-D04): quality view of 4.1;
  `source`, `quality_contract` and `attempt` move to the context; the
  attempt enters `request_context`; attempt 2 sends
  `previous_attempt_errors` (the validation errors of attempt 1); the
  quality prompts explain that field.
- **U2.3** B `feat` (LAT-02, UP-D05): extraction view of 4.1: units without
  offsets, the character reference limited to the batch's candidates,
  trimmed `allowed_quality_points`.
- **U2.4** B `feat` (LAT-03, UP-D07): relevance and retrieval-review views
  and prompts of 4.4.
- **U2-L1** L: benchmark in `off` and `shadow`, extraction development
  split, relevance agreement on the `balance-silver-v1` development split;
  adoption rule per step (U2.2 quality metrics, U2.3 extraction metrics,
  U2.4 relevance metrics); T1 to T3.
- **U2.5** B `feat` (LAT-02, UP-D06, trial): response template of 4.3.
- **U2-L2** L: extraction development split and benchmark `off` against
  U2-L1; adoption rule; revert U2.5 if it fails.
- **U2.6** N `chore` and `docs`: the payload test of 4.1 with the budgets
  measured in U2-L1 plus 20 %; ADR 0003 (request views and the payload
  contract); design/cli.md, balance-analysis.md and evidence-quality.md
  updated.

### U3 Concurrency and caching

- **U3.1** N `refactor` (LAT-04): the ordered executor of 4.5 with N fixed
  at 1; lock unchanged.
- **U3.2** B `feat` (UP-D08): configuration key and option
  `max_parallel_requests`; thread-safe `Runner` and run-state updates;
  guide and design/cli.md section 6 updated.
- **U3.3** B `feat` (LAT-06, UP-D09): module `cache`, configuration key and
  option `cache_dir`, reuse provenance; the `cache` row and the changed
  `runner` row (UP-D01).
- **U3.4** B `feat` (LAT-06, UP-D09): per-text embedding cache, batch size
  32.
- **U3-L** L: benchmark `shadow` with a cold cache at N = 1 and N = 2 (and
  4 when memory allows); a warm-cache rerun that must make no fresh chat
  request and reproduce the cold run's artifacts; retrieval scores with
  batch size 8 against 32 (largest score difference, decision flips). T8.
- **U3.5** N `docs`: ADR 0004 (concurrency and shared cache), design/cli.md
  sections 6 and 7, guide.

### U4 Quality annotation v2

- **U4.1** N `feat` (ALG-01): `evidence.clause_segments` with tests (mixed
  scripts, emoji, combining marks, CRLF, decimals, move notation, empty and
  punctuation-only units).
- **U4.2** N `chore`: fixture mapping check of 4.2 on all 38 fixture cases;
  escalate if any case does not map.
- **U4.3** N `feat` (ALG-01, ALG-02): v2 schema builder, `to_v1_annotation`
  and the v2 validation, not yet used by the pipeline.
- **U4.4** B `feat` (UP-D10): the pipeline sends v2 quality requests; policy
  v2; bilingual prompts v2; `FixtureTransport` answers v2.
- **U4.5** B `feat` (UP-D10): every reader of 4.2 accepts both schema
  versions.
- **U4-L** L: benchmark `shadow` and `enforce`, the 38 synthetic cases and
  the archived quality development sources; T4 and T5; adoption rule.
- **U4.6** B `feat` (LAT-07, UP-D10, conditional): the quality `num_ctx`
  becomes 8192 in the policy, only if U4-L shows that prompt plus output
  stayed below 6,000 tokens in every quality request; otherwise skipped.
  The options are not model-visible content, so no further live session is
  needed.
- **U4.7** N `docs`: ADR 0005 (program segmentation of quality
  annotations), evidence-quality.md, emotion-quantification-and-evidence-isolation.md,
  design/cli.md.

### U5 Extraction precision

Each B step is followed by its L session, which compares it with the
previous accepted state on the `extraction-precision-v1` development split
and the benchmark in `off`.

- **U5.1** B `feat` (PRM-02, UP-D11): evidence-first property order of 4.3.
  Then U5-L1.
- **U5.2** B `feat` (PRM-03, UP-D11): `subjects` and its gate. Then U5-L2.
- **U5.3** B `feat` (PRM-04, PRM-01, UP-D11): examples in the extraction
  prompts, including a long review that only mentions fighters, a
  conditional threat, a system complaint next to a fighter's name and a
  Chinese comment whose direction is unclear. Then U5-L3.
- **U5.4** N `docs`: balance-analysis.md and design/cli.md.

### U6 Module linkage

- **U6.1** B `feat` (LNK-02, UP-D12): module `topics`; `target_reference`
  on grounded claims; recomputed in review; rows of 4.11.
- **U6.2** B `feat` (LNK-02, UP-D12): report export `aimediator-report-v2`
  grouped by glossary ID.
- **U6.3** B `feat` (LNK-02, UP-D12, conditional): `mechanic_terms` in the
  quality and extraction views; kept only if U6-L passes the adoption rule
  with a gain in T5 or T7.
- **U6.4** B `feat` (LNK-03, UP-D13): screening `coarse-v2`; an offline
  comparison of `coarse-v1` and `coarse-v2` decisions on the raw records of
  `20261027-balanced` and `20261015-expanded`, with an agent review of a
  sample of the changed decisions, recorded before the commit.
- **U6.5** B `feat` (ALG-05, UP-D14): near-duplicate clusters of 4.9; the
  threshold is chosen on development data only and recorded with a sample
  of cluster pairs.
- **U6.6** B `feat` (PRM-06, UP-D15, trial): the second audit of 4.10,
  default off.
- **U6.7** N `refactor` (LNK-05): a `RunOptions` dataclass replaces the
  namespace argument of `pipeline.process`; lock unchanged.
- **U6-L** L: benchmark `off` and `enforce`; extraction development split
  with `second_audit` false and true; the archived recovery case of PRM-06
  as a spot check.

### U7 Acceptance and documents

- **U7.1** L: the `full-balanced` sample (120 of the 600 comments, UP-D17)
  in `off`, `shadow` and `enforce`, with the adopted configuration;
  compared per comment and per request with the archived `off` run and
  with the U0.6 and U0.8 baselines.
- **U7.2** L: the `balance-silver-v1` holdout and the
  `extraction-precision-v1` test split, once each.
- **U7.3** N `docs`: design documents, the CLI guide, the README, and a
  record `docs/records/<YYYYMMDD>-pipeline-upgrade-validation.md` for the
  results of U7.1 and U7.2 (D9).
- **U7.4** N `docs` (UP-D16): `RULES.md` v1.5, P4 floor raised to the final
  test count; the owner approves the wording.
- **U7.5** N `docs`: final acceptance against section 13 and the targets of
  5.5, in the change record.
- **U7.6** N `docs` (closure, after the owner's final review): freeze the
  change record; move this plan and its handoffs to `docs/archive/` (P6);
  update the index and the README; tag `upgrade-done`.

---

## 8. Verification reference

Run every command from the checkout root unless stated otherwise.

### 8.1 Gates

```sh
git status --short                           # empty before a step starts
python3 -m unittest discover -s tests -q     # all pass; record the count
python3 scripts/maintenance/check_rules.py   # "Total: 0"
```

### 8.2 Installed-wheel acceptance (offline)

```sh
R=$(pwd); W=$(mktemp -d)
python3 -c "import setuptools.build_meta as b, sys; b.build_wheel(sys.argv[1])" "$W/dist"
python3 -m venv --system-site-packages "$W/venv"
"$W/venv/bin/python" -m pip install --no-deps --no-index -q "$W"/dist/aimediator-*.whl
(cd "$W" && "$W/venv/bin/python" -I "$R/scripts/maintenance/verify_cli_install.py" --out "$W/acceptance")
```

Expected: one JSON line with `"passed": true`. Record the command count; a
change of the count needs the step that caused it.

### 8.3 Behavior lock

```sh
python3 -m unittest discover -s tests -p 'test_behavior_lock.py'
python3 tests/behavior_lock.py --write        # only in a B step, section 1 item 3
```

### 8.4 Timing and profile

```sh
time python3 -m unittest discover -s tests -q
python3 - <<'EOF'
import cProfile, pathlib, pstats, sys, tempfile, time
sys.path.insert(0, 'src')
from aimediator.demo import demo
start = time.perf_counter(); demo(pathlib.Path(tempfile.mkdtemp()) / 'demo', quiet=True)
print('demo plain %.2fs' % (time.perf_counter() - start))
profile = cProfile.Profile(); profile.enable()
demo(pathlib.Path(tempfile.mkdtemp()) / 'demo', quiet=True); profile.disable()
stats = pstats.Stats(profile)
print('demo profiled %.1fs' % stats.total_tt)
stats.sort_stats('cumulative').print_stats('aimediator', 15)
EOF
```

### 8.5 Foreign working directory

```sh
R=$(pwd); (cd "$(mktemp -d)" && python3 -m unittest discover -s "$R/tests" -t "$R/tests" -q)
```

### 8.6 Live commands

The package is installed with `pip install -e .`. `<cfg>` is
`runs/upgrade/live-config.json`. A live session passes `--env-file .env`
only when the owner's configuration uses the configured embedding provider,
and never opens that file.

```sh
# Once, in U0.6 (the owner sets the embedding keys of the configuration)
python3 -m aimediator init --out runs/upgrade/live-config.json
python3 scripts/experiments/materialize_evaluation_input.py --set data/evaluation/latency-benchmark-v1 \
  --dataset data/raw/feedback/20261027-balanced/screened/records.jsonl --out runs/upgrade/inputs/latency-benchmark-v1.jsonl
python3 scripts/experiments/materialize_evaluation_input.py --set data/evaluation/extraction-precision-v1 --split development \
  --dataset data/raw/feedback/20261027-balanced/screened/records.jsonl --out runs/upgrade/inputs/extraction-precision-v1-development.jsonl
# Every L session
python3 -m aimediator doctor --config <cfg>
python3 -m aimediator analyze --config <cfg> --input runs/upgrade/inputs/<set>.jsonl \
  --out runs/upgrade/<step>-<set>-<mode> --evidence-quality <mode> --json
python3 scripts/experiments/measure_run_requests.py --run runs/upgrade/<step>-<set>-<mode> \
  --out runs/upgrade/<step>-<set>-<mode>-metrics.json
python3 scripts/experiments/score_extraction.py --run runs/upgrade/<step>-<set>-<mode> \
  --labels data/evaluation/extraction-precision-v1 --split development --out runs/upgrade/<step>-<set>-<mode>-scores.json
```

The `balance-silver-v1` comments come from
`data/raw/feedback/20261015-expanded/screened/records.jsonl`; materialize
them the same way with the set's own labels file (U0.2 supports both
formats).

From U0.8 on (UP-D17), live runs read the materialized samples of 5.3,
`runs/upgrade/inputs/upgrade-sample-<name>.jsonl`, written in U0.8 with the
`materialize` command in each sample's manifest. `score_extraction.py`
keeps `--labels data/evaluation/extraction-precision-v1 --split
development`. A route scorer counts only the cases of the run's input.

### 8.7 Archived baseline (read-only)

```sh
python3 scripts/experiments/measure_run_requests.py \
  --run ~/Archives/AIMediator/reports/latest-balanced-20261027/full-pipeline-final --out runs/upgrade/archived-600-metrics.json
python3 scripts/experiments/measure_run_requests.py \
  --run ~/Archives/AIMediator/reports/latest-balanced-20261027/quality-live-enforce-v4 --out runs/upgrade/archived-quality-metrics.json
```

The archived run marks reused requests in `transport-provenance.json`
(`kind`); the tool reads that file. The archive is never written.

### 8.8 Boundary and commit hygiene

```sh
git diff --name-only <entry-tag>..HEAD | grep -vE '<allowed-path pattern>'     # prints nothing
git log --format='%h %B%x00' <entry-tag>..HEAD | python3 -c "import sys; [print(c.split()[0]) for c in sys.stdin.read().split('\0') if c.strip() and (('Step: ' not in c and 'Session: ' not in c) or 'Co-Authored-By' in c or 'Generated with' in c)]"
```

The allowed-path pattern is in each handoff, section 3.

---

## 9. Decisions for the owner

Unanswered on 2026-11-04. Step U0.1 copies the answers into the change
record. A step whose decision is unanswered or rejected is skipped and
recorded as `skipped (UP-Dnn not adopted)`.

| ID | Question | Recommendation | Steps |
| -- | -------- | -------------- | ----- |
| UP-D01 | New modules and layering rows of 4.11 | adopt | U0.2, U3.3, U6.1 |
| UP-D02 | Evaluation sets `latency-benchmark-v1` and `extraction-precision-v1` (agent silver) | adopt | U0.3, U0.5 |
| UP-D03 | Service version in the run identity; context-window error | adopt | U1.4, U1.5 |
| UP-D04 | Quality view without source row, contract and attempt; attempt 2 sends the errors of attempt 1 | adopt | U2.2 |
| UP-D05 | Extraction view: no offsets, candidates only, trimmed quality points | adopt | U2.3 |
| UP-D06 | Response template instead of the schema copy in extraction prompts | trial under the adoption rule | U2.5 |
| UP-D07 | Anchors in the relevance system prompts; topics by ID | adopt | U2.4 |
| UP-D08 | Bounded concurrency, configuration key `max_parallel_requests` (default 1) | adopt | U3.1, U3.2 |
| UP-D09 | Shared cache (`cache_dir`, default off), per-text embedding cache, batch 32 | adopt | U3.3, U3.4 |
| UP-D10 | Quality annotation v2 with program segmentation | adopt, answered after U0.6 measures the failure classes (ALG-01) | U4.4 to U4.6 |
| UP-D11 | Extraction v2: evidence-first order, `subjects`, examples | adopt, each step under the adoption rule | U5.1 to U5.3 |
| UP-D12 | Glossary target references; report `aimediator-report-v2` | adopt | U6.1 to U6.3 |
| UP-D13 | Screening `coarse-v2` from the glossary | adopt after the offline comparison | U6.4 |
| UP-D14 | Near-duplicate clusters; `balance-review-policy-v3` | adopt | U6.5 |
| UP-D15 | Optional second audit by the other routed model | trial, default off | U6.6 |
| UP-D16 | `RULES.md` v1.5: P4 floor raised to the final count | adopt | U7.4 |
| UP-D17 | Smaller live samples from U0.8 on (raised by the owner after U0.6) | adopt | U0.7, U0.8, every live run of U2 to U7 |

**UP-D01 New modules.** `measurement` keeps evaluation logic out of scripts
(P3: tests use it); `cache` and `topics` give the shared cache and the
glossary matching one home each. Rejecting it blocks U0.2, U3.3 and U6.1.

**UP-D02 Evaluation sets.** Prompt and payload changes need fixed sets with
labels that do not come from the models. Both sets are agent silver, not
human gold (as `balance-silver-v1`). `extraction-precision-v1` labels about
300 comments, which is one or two annotation sessions. Without it, U2 and U5
can only compare audit acceptance, which correlates with the model under
test (PRM-06).

**UP-D03 Service identity and context guard.** The service version and
server settings change outputs as model digests do. Resume then refuses a
run whose service changed, which is the same rule as for model digests.

**UP-D04 Quality view.** Fixes LAT-01 and PRM-05 together: without the
attempt number in the content, attempt 2 would repeat attempt 1, so it must
carry the errors of attempt 1. The specification (section 3.2) asks for a
new, recorded retry; this is one.

**UP-D05 Extraction view.** The schema already limits characters to each
comment's candidates; the reference only needs those entries. Offsets are
program data.

**UP-D06 Response template.** The service documentation recommends a copy
of the schema in the prompt, so removing it may lower quality. It is a trial:
U2-L2 decides, and a revert is the fallback.

**UP-D07 Relevance prompts.** The anchors become part of the cached system
prompt. Admissions can change; the frozen admission result stays historical
(2.3).

**UP-D08 Concurrency.** Default 1 keeps today's behavior. A value above 1
gives throughput at the cost of bitwise reproducibility of fresh inference
(2.3) and memory per slot. The owner chooses the value for live runs after
U3-L.

**UP-D09 Caching.** The shared cache is off unless `cache_dir` is set. Each
reused response is marked, so reports can separate fresh from reused
inference, as the 600-comment validation did by hand.

**UP-D10 Quality v2.** Removes offsets and quotes from model output and
shortens it. It does not by itself remove the failure class observed so far
(a point literal outside its selected segments, ALG-01), which the repair
attempt of U2.2 addresses. It cannot split finer than the program's
clauses. Readers keep v1.

**UP-D11 Extraction v2.** Three independent changes, each kept only when its
L session passes the adoption rule.

**UP-D12 Glossary references.** Groups equivalent targets across wording and
language without semantic guessing: only exact aliases resolve. The report
schema version changes.

**UP-D13 Screening.** Removes a second copy of glossary content. Screening
decisions change for new collections only.

**UP-D14 Near-duplicates.** Annotation only; no count changes. Changes the
retrieval policy file, so its version changes.

**UP-D15 Second audit.** Decorrelates audit errors, at the cost of one
model switch and one more request per accepted claim. The routing asset
changes; the default stays off until the owner adopts it after U6-L.

**UP-D16 Test floor.** Same procedure as CR-D10 of the restructuring.

**UP-D17 Live samples.** Raised by the owner on 2026-11-04 after U0.6, to
shorten the live sessions: at the U0.6 speeds the live runs of U2 to U7
take about 30 hours on the full sets and about 11 with the samples, U0.8
included. Costs: one more live session (U0.8, about an hour), so that
every comparison stays paired on the same comments; wider intervals, so a
verdict near a margin of rule 4 is less certain; U7.1 accepts on 120
comments instead of 600.

Owner actions: close the restructuring (entry condition); answer this
section; provide the live environment or run the L sessions (5.4); review at
U2, U4, U5 and U7.

---

## 10. Roles and session protocol

### 10.1 Roles

- **Owner**: decides, approves `RULES.md` wording, runs or authorizes live
  sessions, reviews at U2, U4, U5 and U7, answers escalations, owns
  `~/Archives/AIMediator/`, and is the only one who may keep a step against
  the adoption rule.
- **Implementation session** (`U<n>-<k>`): executes its steps inside the
  batch boundary; writes code, tests and documents; keeps the progress table
  and session log; never sets tags and never regenerates the lock outside a
  B step.
- **Annotation session** (`U0-A`): writes evaluation labels from source
  text only, in a fresh context, and never sees model claims for the
  comments it labels.
- **Live session** (`U<n>-L<k>`): runs on the owner's machine with the
  local model service; executes section 8.6; writes only the files of rule
  1.3 L; applies the adoption rule and recommends. It never reverts code: a
  failed step is recorded, and the revert is a fix-up step of the next
  implementation session, or of the closure session when the batch ends at
  a review point and the owner decides.
- **Verification session** (`U<n>-V`): a fresh context that did not
  implement the batch; reruns the gates and the checklist; writes the
  verification note (its only file change) and sets the tag.
- **Closure session**: records the owner's review, turns rejected items into
  fix-up steps `U<n>.F<k>`, and sets the batch tag.

### 10.2 Session lifecycle

1. **Start**: read what the session prompt lists; run the resume procedure;
   confirm the handoff's entry conditions, or stop and report.
2. **Work**: execute the assigned steps in order, gates after each step, a
   commit per section 1.
3. **End**: at a step boundary with a clean tree; add a session-log entry
   (10.3) in a `docs` commit or in the last step's commit; the final message
   to the owner repeats that entry. Never start a step that cannot be
   finished in the same session.

### 10.3 Session log and verification note

```text
### <YYYY-MM-DD> <session ID> (<implementation | annotation | live | verification | closure>)
- Steps: <IDs done>; <ID started and stashed, or "none">
- State: HEAD <short hash>; tests <count>; lock <green | updated by UP-Dnn>; rule check 0
- Findings: <decisions, escalations, deviations, or "none">
- Next: <next step ID and session ID>; blockers: <or "none">
```

```text
### <YYYY-MM-DD> U<n>-V
- Range: <entry tag>..<short hash>; <count> commits
- Checks: <one line per checklist item: pass, or fail with the detail>
- Measurements: tests <count> in <seconds> s; demo <seconds> s; lock green
- Result: accepted, tag <tag> | rejected, fix-up steps <U<n>.F1, ...>
```

### 10.4 Interrupted step

Run `git stash push -u -m "WIP Step U<n>.<m>: <reason>"`, then commit a
session-log entry that names the stash. The next session reads it with
`git stash show -p`, pops it and finishes the step or drops it and restarts
the step, and records which. A live run interrupted midway is resumed with
`aimediator analyze --resume <run>`; a run whose identity no longer matches
is discarded and started again in a new directory.

### 10.5 Reviews and escalation

- Review points: the verification session sets `upgrade-u<n>-review` and
  stops; the owner reviews; a closure session records the outcome in a
  `docs` commit (`docs: record the owner review of batch U<n>`), turns
  rejected items into fix-up steps, and sets `upgrade-u<n>` (for U7,
  `upgrade-done` after U7.6).
- Escalation: add an entry `E-<n>` under "Escalations" in the change record
  (step, question, options, recommendation, what is blocked), commit it,
  name it in the final message, and continue with unblocked steps or end the
  session.

---

## 11. Change record skeleton (copy in U0.1)

```markdown
# Pipeline Upgrade Change Record

- Type: Record
- Status: Active
- Updated: <YYYY-MM-DD>
- Applies to: the [pipeline upgrade plan](../plans/pipeline-upgrade.md); commit `<entry hash>` and later

The single change record of the pipeline upgrade. Every step adds its row to
the progress table in its own commit. Frozen when the plan is finished (D3).

## Owner decisions

| ID | Answer | Date | Notes |
| -- | ------ | ---- | ----- |

## Progress

The commit of a step is found with `git log --grep 'Step: <ID>'`.

| Step | Class | Status | Tests | Lock | Notes |
| ---- | ----- | ------ | ----- | ---- | ----- |

## Baseline measurements (U0.4)

## Live environment and configuration (U0.6)

## Live evaluations

| Session | Commit | Set | Mode | Wall time | Prompt tokens by stage | Output tokens by stage | Failures | Claims generated / accepted | Precision / recall (dev) | Quality validity | Verdict |
| ------- | ------ | --- | ---- | --------- | ---------------------- | ---------------------- | -------- | --------------------------- | ------------------------ | ---------------- | ------- |

## Behavior changes (P7)

| Step | Decision | Asset or request part | Old SHA-256 | New SHA-256 | Lock paths |
| ---- | -------- | --------------------- | ----------- | ----------- | ---------- |

## Evaluation sets

## Archive and deletions

| Path | Archive location | SHA256SUMS entry | Reason | Step |
| ---- | ---------------- | ---------------- | ------ | ---- |

## Decisions found during execution

## Escalations

## Verification notes

## Session log

## Deferred
```

`Status` is one of `done`, `reverted (see Live evaluations)`,
`skipped (UP-Dnn not adopted)` or `bypassed (see Decisions found during execution)`.

---

## 12. Risks and mitigations

| Risk | Mitigation |
| ---- | ---------- |
| A payload change lowers quality unnoticed | Adoption rule (5.4) on labels that do not come from the models; one change per step; revert path |
| Prompt tuning overfits the evaluation sets | Development splits only; test and holdout runs limited to U7.2 (rule 1.11); examples are synthetic |
| The same-model audit hides extraction errors | `extraction-precision-v1` labels; audit prompts fixed during U5; optional second audit (U6.6) |
| A frozen fixture or evaluation set changes through the v2 work | Invariant 2.1.6; U4.2 mapping check before U4.4; escalation instead of edits |
| Readers of earlier runs break on new schema versions | Invariant 2.1.9; U4.5 and U6.2 keep v1 readers; review and report tests on demo runs of both versions |
| Parallel requests reorder artifacts or race on a journal folder | Ordered commit and per-identity locks (4.5); N = 1 keeps the lock unchanged |
| Shared-cache hits are mistaken for fresh inference | Reuse provenance per request; measurement counts both |
| The live environment drifts between L sessions | Environment record and check at every L session start (5.4) |
| Samples make verdicts noisier (UP-D17) | Paired comparisons against the U0.8 sample references; intervals reported beside differences; the full-set U0.6 rows kept |
| Live sessions are unavailable | L steps are owner actions; implementation continues with independent steps; batch exits wait |
| Credentials leak through live commands | `.env` is passed by path only and never opened (G9); configurations hold variable names only |
| Tooling adds attribution trailers | Rule 1.2 (P6); commit-hygiene check (8.8) |

---

## 13. Completion criteria

The upgrade is complete when all of the following hold:

1. Every step is `done`, `reverted`, `skipped` or `bypassed`, with its
   reason recorded.
2. The gates pass, also from a foreign directory (8.5), and the wheel
   acceptance passes (8.2).
3. The behavior lock passes, and every regeneration belongs to a B step with
   its decision.
4. Every live evaluation is in the change record, with a curated report for
   each batch that had one.
5. The targets of 5.5 are reported with their measured values, met or not.
6. The U7.1 runs (the `full-balanced` sample, UP-D17) account for every
   input row.
7. The design documents, the guide and the README describe the code (U7.3).
8. `RULES.md` matches the tree (U7.4).
9. The change record is final and frozen; this plan and its handoffs are
   archived (U7.6).
