# Pipeline Upgrade Change Record

- Type: Record
- Status: Active
- Updated: 2026-11-04
- Applies to: the [pipeline upgrade plan](../plans/pipeline-upgrade.md); commit `31d00f8` (tag `upgrade-plan`) and later

The single change record of the pipeline upgrade. Every step adds its row to
the progress table in its own commit. Frozen when the plan is finished (D3).

## Owner decisions

| ID | Answer | Date | Notes |
| -- | ------ | ---- | ----- |
| UP-D01 | adopt | 2026-11-04 | plan section 9 |
| UP-D02 | adopt | 2026-11-04 | plan section 9 |
| UP-D03 | adopt | 2026-11-04 | plan section 9 |
| UP-D04 | adopt | 2026-11-04 | plan section 9 |
| UP-D05 | adopt | 2026-11-04 | plan section 9 |
| UP-D06 | trial under the adoption rule | 2026-11-04 | plan section 9; U2-L2 decides |
| UP-D07 | adopt | 2026-11-04 | plan section 9 |
| UP-D08 | adopt | 2026-11-04 | plan section 9 |
| UP-D09 | adopt | 2026-11-04 | plan section 9 |
| UP-D10 | pending | — | plan section 9: answered after U0.6 measures the failure classes (ALG-01) |
| UP-D11 | adopt, each step under the adoption rule | 2026-11-04 | plan section 9 |
| UP-D12 | adopt | 2026-11-04 | plan section 9 |
| UP-D13 | adopt after the offline comparison | 2026-11-04 | plan section 9 |
| UP-D14 | adopt | 2026-11-04 | plan section 9 |
| UP-D15 | trial, default off | 2026-11-04 | plan section 9 |
| UP-D16 | adopt | 2026-11-04 | plan section 9 |

## Progress

The commit of a step is found with `git log --grep 'Step: <ID>'`.

| Step | Class | Status | Tests | Lock | Notes |
| ---- | ----- | ------ | ----- | ---- | ----- |
| U0.1 | N | done | 241 | green | Change record opened from plan section 11; owner decisions copied (UP-D10 pending by its own terms); index row added |
| U0.2 | N | done | 250 | updated by UP-D01 | New module `aimediator.measurement` (`request_metrics`, `claim_outcomes`, `materialize`, `score_positions`; standard library, `common` and `quality_scoring.proportion` only) and the scripts `measure_run_requests.py` (writes both metrics and outcomes), `materialize_evaluation_input.py` and `score_extraction.py`. New `tests/test_measurement.py` (+9): synthetic runs with and without counters and both reuse formats, wall time, the three demo runs end to end (counters `None`), the three label formats, missing rows, hash mismatches, hand-computed precision and recall, the scripts. Layering row `measurement` → `common`, `quality_scoring`; design/cli.md section 5 layout and contract. Lock regenerated for exactly `L2:enforce/code-snapshot/measurement.py`, `L2:off/…` and `L2:shadow/…` (existence only); no other key differed. Beyond plan 5.2: fresh and reused statistics kept apart (reused archived responses keep their original counters with near-zero elapsed time); counts and sums beside the means; audit rejection share; extraction dispositions; quality attempt errors (IDs and key names only, no source text); `materialize` also checks `ids_sha256` or `labels_sha256` and `source_dataset_sha256` when the set's manifest records them. Nested text parts are counted without JSON quotes, which matches plan 0.2 (unit text 15.3 %, raw; 15.75 % with quotes). Decision found during execution D-1 |
| U0.3 | D | done | 250 | green | UP-D02: `data/evaluation/latency-benchmark-v1/` frozen (`ids.json`, `manifest.json`); 60 IDs, 10 per language and length tercile; see "Evaluation sets". `materialize` reproduces the 60 rows in set order with every content hash matching |
| U0.4 | N | done | 250 | green | Plan 8.1, 8.2, 8.4 and 8.5 at `bca6490`, and plan 8.7 with the committed tool; see "Baseline measurements (U0.4)". Every archived figure of plan 0.2 agrees within rounding; no baseline of plan 5.5 changes |

## Baseline measurements (U0.4)

Measured on 2026-11-04 at `bca6490` (U0.3 done), with Python 3.14.8 and
NumPy 2.4.6. Batch U0 changed no pipeline code; the package differs from
`d0aed08` only by the new research module `measurement`.

### Offline (plan section 0.1)

| Item | Plan 0.1 (at `d0aed08`) | U0.4 (at `bca6490`) | Command |
| ---- | ----------------------- | ------------------- | ------- |
| Package | 29 top-level modules and `collection/` (8 files) | 30 top-level modules (`measurement` added) and `collection/` (8 files) | `ls src/aimediator/*.py` |
| Offline tests | 241 pass in about 9 to 11 s; floor 241 | 250 pass in 9.2 s (wall 9.6 s); `test_measurement` adds 9 | plan 8.1, 8.4 |
| Rule check | 0 violations; the hook blocks | `Total: 0`; the hook ran on every U0 commit | plan 8.1 |
| Behavior lock | green | green; regenerated once, in U0.2, for the three existence-only `measurement.py` keys | plan 8.3 |
| Offline demo | 1.07 s plain, 1.9 s under cProfile; `evidence.character_reference` 688 calls, 0.67 s cumulative (35 %) | 1.08 s plain, 1.9 s under cProfile; `evidence.character_reference` 688 calls, 0.67 s cumulative (35 %); `balance_policy.term_matches` 222,493 calls, 0.62 s; `run_store.state` 201 calls, 0.38 s | plan 8.4 |
| Foreign working directory | — | 250 pass | plan 8.5 |
| Installed-wheel acceptance | — | `"passed": true`, `"commands": 18` (the count of the restructuring's closure), Python 3.14.8, NumPy 2.4.6; the wheel contains `aimediator/measurement.py` | plan 8.2 |

The stream loop-guard timings and the `run_store.state` share of the
synthetic 600-comment fixture run in plan 0.1 are not produced by plan 8.1
to 8.5 and were not measured again; U1 measures them for T9 and its
stream-guard step.

### Archived 600-comment run (plan section 0.2, plan 8.7)

`measure_run_requests.py` on
`~/Archives/AIMediator/reports/latest-balanced-20261027/full-pipeline-final`
(read only; no archive file changed), output
`runs/upgrade/archived-600-metrics.json`. The archived run is a legacy run
without `run-state.json`, so its wall time is `null`. Fresh requests only;
token, prefill and decode means over the fresh requests that carry
counters.

| Stage, model | Requests (fresh) | Mean elapsed | Prompt tokens | Cached tokens | Uncached tokens | Output tokens | Prefill | Decode | Requests with counters |
| ------------ | ---------------- | ------------ | ------------- | ------------- | --------------- | ------------- | ------- | ------ | ---------------------- |
| relevance, both | 160 (0) | — | — | — | — | — | — | — | 0 |
| retrieval_review, both | 87 (0) | — | — | — | — | — | — | — | 0 |
| extract, `llama3.1:latest` | 81 (62) | 20.2 s | 4,369 | 635 | 3,733 | 228 | 9.7 s | 9.6 s | 58 |
| extract, `qwen2.5:7b` | 76 (60) | 19.1 s | 3,796 | 682 | 3,114 | 336 | 6.2 s | 12.6 s | 59 |
| extract, both | 157 (122) | 19.7 s | 4,080 | 659 | 3,421 | 283 | 7.9 s | 11.1 s | 117 |
| verify, `llama3.1:latest` | 161 (12) | 0.8 s | 817 | 554 | 263 | 7.0 | 0.5 s | 0.2 s | 12 |
| verify, `qwen2.5:7b` | 226 (54) | 0.8 s | 885 | 557 | 328 | 6.3 | 0.6 s | 0.2 s | 54 |
| verify, both | 387 (66) | 0.8 s | 872 | 556 | 316 | 6.4 | 0.6 s | 0.2 s | 66 |

Summed fresh request time: extract 2,397.3 s, verify 54.6 s, together
2,451.9 s. `done_reason` of the extract requests: 150 `stop` and 7
`duplicate_claim_loop` (6 llama, 1 qwen), of which 5 are fresh (the 5
fresh requests without counters) and 2 reused; these 7 are the extract
requests with validation errors. Every other request ended with `stop`.

Composition of the requests, mean characters over all requests of the
stage (fresh and reused); shares are of the user message:

| Stage | System prompt | `format` | User message | Top-level user keys | Nested parts |
| ----- | ------------- | -------- | ------------ | ------------------- | ------------ |
| relevance | 665 | 212 | 4,918 | `comments` 4,671 (95.0 %), `response_schema` 212 (4.3 %) | `comments[].retrieved_topics` 2,321 (47.2 %), `comments[].text` 2,063 (41.9 %) |
| retrieval_review | 951 | 212 | 4,434 | `comments` 4,187 (94.4 %), `response_schema` 212 (4.8 %) | `comments[].text` 2,307 (52.0 %), `comments[].retrieved_topics` 1,683 (38.0 %) |
| extract | 2,268 | 4,862 | 10,702 | `response_schema` 4,862 (45.4 %), `comments` 3,120 (29.2 %), `character_normalization_reference` 2,646 (24.7 %) | `comments[].units[].text` 1,642 (15.3 %) |
| verify | 1,529 | 172 | 1,772 | `original_evidence` 921 (52.0 %), `naming_reference` 440 (24.8 %), `response_schema` 172 (9.7 %), `proposed_claim` 120 (6.8 %), `claim_id` 19 (1.1 %) | — |

Claim outcomes (`claim_outcomes`, same output): 404 generated; 17
quarantined by source binding (most frequent errors: numerical adjustment
intent absent or ambiguous 15, parameter proposed absent from its span 6,
parameter proposed token mismatch 6, explicit action contradicts direction
6); 387 audited; 200 rejected by the semantic audit (163 unsupported, 37
uncertain); 187 accepted. Audit rejection share 51.7 % (Wilson 95 % 46.7
to 56.6 %); Chinese `unclear` 53 of 62 audited (85.5 %); English `nerf` 66
of 119 audited (55.5 %).

### Archived quality run (plan section 0.2, plan 8.7)

`measure_run_requests.py` on `quality-live-enforce-v4` of the same archive,
output `runs/upgrade/archived-quality-metrics.json`; all 8 requests fresh.

| Stage, model | Requests | Mean elapsed (range) | Prompt tokens (range) | Uncached tokens (range) | Output tokens (range) | Prefill | Decode |
| ------------ | -------- | -------------------- | --------------------- | ----------------------- | --------------------- | ------- | ------ |
| quality, both | 5 | 18.2 s (14.0 to 23.1) | 3,594 (3,336 to 3,820) | 2,588 (633 to 3,646) | 296 (190 to 453) | 5.4 s | 11.4 s |
| relevance, both | 3 | 4.4 s | 749 | 685 | 15 | 1.2 s | 0.5 s |

The ranges come from `measurement.request_records`. Quality user message
(mean 7,591 characters; per-request ranges): `character_normalization_reference`
2,689 (2,505 to 2,950), `response_schema` 2,128, `quality_contract` 1,247,
`source` 1,209 (1,187 to 1,226), `comments` 178 (110 to 250), unit text
28. System prompt 2,911, `format` 2,128. Quality outcomes: 4 comments, 3
valid at the first attempt (75 %, Wilson 95 % 30 to 95 %), 5 attempts; the
failed comment's two attempts both have 3,820 prompt and 453 output tokens
and the error `Literal absent from selected spans: character_literal`.

### Comparison with plan section 0.2

Every figure the tool measures agrees with plan 0.2 within rounding, and no
baseline of plan 5.5 changes (T1 archive 3,421 uncached; T2 633 to 3,646
uncached, 3,336 to 3,820 in total; T6 52 %). Findings for the record, none
blocking:

- Unit text is 15.3 % when counted without JSON quotes, as the tool does,
  and 15.75 % with them; plan 0.2 says 15 %.
- Plan 0.2 leaves the per-model cached tokens of extraction blank; the tool
  measures 635 (llama) and 682 (qwen).
- Not measured by the tool, so not checked again: the 32 entries of the
  character reference, and the rejection share of comments with three or
  more claims (34 comments, 158 claims, 64 %).

## Live environment and configuration (U0.6)

## Live evaluations

| Session | Commit | Set | Mode | Wall time | Prompt tokens by stage | Output tokens by stage | Failures | Claims generated / accepted | Precision / recall (dev) | Quality validity | Verdict |
| ------- | ------ | --- | ---- | --------- | ---------------------- | ---------------------- | -------- | --------------------------- | ------------------------ | ---------------- | ------- |

## Behavior changes (P7)

| Step | Decision | Asset or request part | Old SHA-256 | New SHA-256 | Lock paths |
| ---- | -------- | --------------------- | ----------- | ----------- | ---------- |

## Evaluation sets

- **`latency-benchmark-v1`** (U0.3, UP-D02; frozen 2026-11-04). Purpose:
  latency and outcome counts; not an accuracy set; no labels
  (`reviewer_type` `none`). Source
  `data/raw/feedback/20261027-balanced/screened/records.jsonl` (SHA-256
  `3eb87a7561b41ff31cef3e7035f0a25353adbe1999e023ff5e46b1bcf4852e3f`, 300
  English and 300 Chinese rows). Terciles of `len(text_original)` per
  language; cut points (largest length of terciles 1 and 2): English 208
  and 764, Chinese 31 and 99; ties put 101, 101 and 98 English and 100, 102
  and 98 Chinese source rows into the terciles. The first 10 rows per
  language and tercile in the order of SHA-256 of
  `latency-benchmark-v1:<record_id>`: 60 IDs, 30 per language. Selected
  lengths: English 15–154, 239–734 and 905–2,719; Chinese 4–31, 34–91 and
  117–611 characters. `ids.json` holds `record_id`, `language`,
  `content_sha256` and `length_tercile` only; `ids_sha256`
  `8f0931b032fd215b1666559de9e91385b81d844b0c0b7b09ddcf961cc1a8514a`. The
  manifest states the selection rule in full, so U0-V can rerun it.

## Archive and deletions

| Path | Archive location | SHA256SUMS entry | Reason | Step |
| ---- | ---------------- | ---------------- | ------ | ---- |

## Decisions found during execution

- **D-1 (U0.2) Output of `materialize_evaluation_input.py`.** The step note
  asks the scripts to write their output with `common.write`, which writes
  indented JSON. The materialized input must be JSONL holding the dataset
  rows unchanged, because `aimediator analyze --input` reads JSONL. Options:
  (a) the script writes the bytes from `materialize` through a synced
  temporary file and replaces the target, as `common.write` does; (b) add a
  JSONL writer to `common` (outside the U0 boundary); (c) write a JSON array
  (`analyze` cannot read it). Recommendation and action: (a). N-class, undone
  by a revert, no `RULES.md` change, nothing deleted. The two other scripts
  use `common.write`.

## Escalations

## Verification notes

## Session log

### 2026-11-04 U0-1 (implementation)

- Steps: U0.1, U0.2, U0.3, U0.4 done; none started and stashed.
- State: HEAD is this entry's commit (parent `bca6490`); tests 250; lock
  updated by UP-D01 (U0.2, three existence-only keys), green since; rule
  check 0.
- Findings: the owner answered the decisions at the session start (UP-D10
  pending by its own terms); decision found during execution D-1 (JSONL
  output of `materialize_evaluation_input.py`); every archived figure of
  plan 0.2 agrees within rounding (U0.4).
- Next: U0.5 in session U0-A (annotation, fresh context); then U0.6 in
  session U0-L on the owner's machine; blockers: U0.6 needs the live
  environment, the embedding keys of the live configuration, and U0.5.

## Deferred
