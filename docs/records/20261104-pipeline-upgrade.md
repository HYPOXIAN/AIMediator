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
| UP-D10 | adopt | 2026-11-04 | plan section 9; adopted without waiting for the U0.6 measurement of the failure classes (ALG-01), which U0.6 still takes. Corrected in U0.6 from `pending`: the owner's answer predates the U0.1 commit (session log, U0-L) |
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
| U0.5 | D | done | 250 | green | UP-D02: `data/evaluation/extraction-precision-v1/` frozen (`labels.jsonl`, `manifest.json`); 301 comments labeled by session U0-A from the source text only, 227 development and 74 test; see "Evaluation sets". `materialize` reproduces 301, 227 and 74 rows with every hash matching; `score_positions` reads the labels |
| U0.6 | L | done | 250 | green | Session U0-L on the owner's machine: environment and live configuration recorded (Ollama 0.34.2, local embeddings, `connection_timeout` 120 after E-1); the five reference runs at `50becc2` measured and scored, see "Live evaluations" and the plan 5.5 baselines there; curated report `reports/20261104-upgrade-baseline/`; full runs archived with `SHA256SUMS` (5,323 files). Decisions found during execution D-2 (Failures column), D-3 (interrupted run rerun clean), D-4 (relevance and route agreement outside the package); escalation E-1 resolved by the owner. UP-D10 row corrected to the owner's answer |

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

Recorded on 2026-11-04 by session U0-L at `50becc2` (U0.5 done). Every L
session checks these values at its start (plan 5.4); a difference
invalidates comparisons with the U0.6 rows and is escalated.

| Item | U0.6 value | Source |
| ---- | ---------- | ------ |
| Service | Ollama 0.34.2 at `http://127.0.0.1:11434` | `/api/version` |
| `OLLAMA_NUM_PARALLEL` | 1 | stated by the owner on 2026-11-04; equal to the service's startup log |
| `OLLAMA_FLASH_ATTENTION` | false | as above |
| `OLLAMA_KV_CACHE_TYPE` | unset (f16) | as above |
| Other server settings | `OLLAMA_CONTEXT_LENGTH` 0, `OLLAMA_MAX_LOADED_MODELS` 0, `OLLAMA_SCHED_SPREAD` false, `OLLAMA_GPU_OVERHEAD` 0 | startup log |
| GPU | AMD Radeon RX 6700S (Navi 23), 8 GiB (8,176 MiB), Vulkan backend (RADV); about 6,640 MiB free when a model loads. The integrated Radeon 680M is not used | startup log, `lspci` |
| Host memory | 22 GiB | `free` |
| Chat models | `llama3.1:latest` `46e0c10c039e019119339687c3c1757cc81b9da49709a3b3924863ba87ca666e`; `qwen2.5:7b` `845dbda0ea48ed749caafd9e6037047aa19acfcfd82e704d7ca97d631a0b697e` | `aimediator doctor` |
| Embedding | provider `ollama`, `qwen3-embedding:8b` `64b933495768fbd3b87c20583d379728a07471e0c66733a9df87cd1901b3c44b`, digest verified (`remote_digest_verified` true); chosen by the owner on 2026-11-04 | `aimediator doctor`, live configuration |
| Runtime | Python 3.14.8, NumPy 2.4.6, `aimediator` 0.1.0 installed editable into `.venv` (system site packages, no network: `pip install --no-deps --no-index --no-build-isolation -e .`) | `aimediator doctor` |

- The embedding provider differs from the archived 600-comment run and the
  2026-10-28 CLI diagnostic, which used the configured provider
  (`qwen/qwen3-embedding-8b` on a remote endpoint, no weight digest).
  Retrieval scores of the U0.6 runs are therefore not comparable with the
  archived run; later L sessions compare with U0.6.
- `qwen3-embedding:8b` does not fit the GPU whole: 27 to 29 of 37 layers
  are offloaded, depending on free memory at load time. It and the chat
  models replace one another in GPU memory during a run.
- `doctor` passed only after escalation E-1 (`connection_timeout` 120).

Live configuration `runs/upgrade/live-config.json`: the output of
`aimediator init` on 2026-11-04 with one change, `connection_timeout` 120
instead of 10 (owner, E-1). The embedding endpoint is `null`, no
credential is read, and no L session passes `--env-file`.

```json
{
  "schema_version": "aimediator-config-v1",
  "base_url": "http://127.0.0.1:11434",
  "routing": {
    "models": {
      "llama3.1:latest": {
        "language": "en",
        "prompt": "prompts/summarize-balance.en.txt"
      },
      "qwen2.5:7b": {
        "language": "zh",
        "prompt": "prompts/summarize-balance.zh.txt"
      }
    },
    "policy": "Route English comments and English instructions only to Llama, Chinese comments and Chinese instructions only to Qwen. Unsupported languages are recorded and not sent. Admit comments to extraction only when vector retrieval and relevance review agree; audit every generated claim against original evidence before aggregation."
  },
  "inference_options": {
    "temperature": 0,
    "seed": 42,
    "num_ctx": 8192
  },
  "connection_timeout": 120,
  "request_timeout": 1800,
  "embedding": {
    "provider": "ollama",
    "model": "qwen3-embedding:8b",
    "endpoint": null,
    "credential_env": "EMBEDDING_API_KEY"
  },
  "evidence_quality": "off",
  "stop_after": "full",
  "num_gpu": null,
  "report_scope": "collection_sample"
}
```

Inputs (plan 8.6), materialized with the committed tool, every content hash
checked: `runs/upgrade/inputs/latency-benchmark-v1.jsonl` (60 rows, SHA-256
`24a452ceabe140fe531d72dc4b7a385182c7291cf2df21f63d525ffee9403519`),
`extraction-precision-v1-development.jsonl` (227 rows,
`0d6c9d3f3df0e444a6204611d8de0856ff881de06d0efc0ebdc76c0cb2424d2d`) and
`balance-silver-v1-development.jsonl` (70 rows, from
`data/raw/feedback/20261015-expanded/screened/records.jsonl`,
`c05a30342ae57e222b58105d1ae0d37698ff41aa77db6ddd6db96733131abce8`). The
synthetic quality run reads
`data/evaluation/evidence-quality-synthetic-v1/records.jsonl` as is (38
rows, `8a41f808074bce16f5badcc3a645c0f34eec7f78ece77196fd22c5725dc8a216`).

## Live evaluations

| Session | Commit | Set | Mode | Wall time | Prompt tokens by stage | Output tokens by stage | Failures | Claims generated / accepted | Precision / recall (dev) | Quality validity | Verdict |
| ------- | ------ | --- | ---- | --------- | ---------------------- | ---------------------- | -------- | --------------------------- | ------------------------ | ---------------- | ------- |
| U0-L (`u0-benchmark-off`) | `50becc2` | `latency-benchmark-v1` (60) | `off` | 431.9 s | relevance 1,456 (1,278 uncached); retrieval_review 1,202 (962); extract 3,982 (3,404); verify 846 (254) | relevance 19; retrieval_review 20; extract 306; verify 7 | 0 requests with errors; 0 failed comments; 2 pending (review queue) | 43 / 17 (5 quarantined; 21 of 38 audited rejected) | 5/14 (35.7 %) / 5/20 (25.0 %), the 22 scored benchmark comments of the development split | — | reference |
| U0-L (`u0-benchmark-shadow`) | `50becc2` | `latency-benchmark-v1` (60) | `shadow` | 3,130.2 s | relevance 1,418 (1,240); retrieval_review 1,263 (1,056); quality 3,353 (2,089); extract 3,976 (3,399); verify 813 (305) | relevance 18; retrieval_review 21; quality 643; extract 252; verify 6 | 26 quality requests with validation errors, 0 transport; 13 quality-failed comments; 3 pending | 32 / 11 (4 quarantined; 17 of 28 rejected) | 3/8 (37.5 %) / 3/20 (15.0 %), same 22 comments | first attempt 41/54 (75.9 %, Wilson 63.1–85.4 %); 67 attempts | reference |
| U0-L (`u0-extraction-development-off`) | `50becc2` | `extraction-precision-v1` development (227) | `off` | 2,434.7 s | relevance 2,439 (2,250); retrieval_review 1,836 (1,621); extract 4,429 (3,782); verify 1,019 (345) | relevance 21; retrieval_review 21; extract 491; verify 7 | 0 requests with errors; 0 failed comments; 5 pending | 327 / 137 (26 quarantined; 164 of 301 rejected, 54.5 %) | accepted 65/117 (55.6 %, Wilson 46.5–64.2 %) / 64/222 (28.8 %, Wilson 23.3–35.1 %); generated 108/291 (37.1 %); recall over admitted 64/220 (29.1 %) | — | reference |
| U0-L (`u0-silver-development-relevance`) | `50becc2` | `balance-silver-v1` development (70) | `off`, `--stop-after relevance` | 186.8 s | relevance 2,033 (1,857); retrieval_review 1,520 (1,301) | relevance 20; retrieval_review 22 | 0 requests with errors; 3 pending | — | relevance agreement 59/69 (85.5 %, Wilson 75.3–91.9 %): 55 TP, 4 TN, 8 FN, 2 FP; 1 uncertain excluded | — | reference |
| U0-L (`u0-quality-synthetic-shadow`) | `50becc2` | `evidence-quality-synthetic-v1` (38) | `shadow`, `--stop-after quality` | 851.2 s | relevance 1,255 (1,089); retrieval_review 772 (664); quality 2,725 (1,681) | relevance 19; retrieval_review 18; quality 383 | 12 quality requests with validation errors, 0 transport; 6 quality-failed comments; 1 pending | — | — | first attempt 28/34 (82.4 %, Wilson 66.5–91.7 %); 40 attempts; route agreement 16/34 (47.1 %, Wilson 31.5–63.3 %), English 10/16, Chinese 6/18; 4 cases do not reach quality (3 rejected, 1 pending) | reference |

Rows of U0.6 (2026-11-04, session U0-L): the five reference runs of plan
7 U0.6, environment and configuration as in the section above. Token
figures are means over fresh requests (every U0.6 request is fresh and
carries counters), uncached in parentheses. "Failures" follows D-2.
Wall time is the measurement tool's (manifest creation to last state
update); every run ended `partial` (exit 5) because of its pending
review-queue units. Measurements, scores and agreements are in
[`reports/20261104-upgrade-baseline/`](../../reports/20261104-upgrade-baseline/manifest.json);
full runs in the archive (see "Archive and deletions").

Baselines of plan 5.5 from U0.6:

| ID | U0.6 baseline | Run | Target (plan 5.5) |
| -- | ------------- | --- | ----------------- |
| T1 | extraction 3,404 uncached prompt tokens per request (shadow 3,399; archive 3,421) | `u0-benchmark-off` | at most 1,700 |
| T2 | quality 2,089 uncached prompt tokens per request (3,353 in total) | `u0-benchmark-shadow` | at most 1,500 |
| T3 | relevance 1,278 uncached prompt tokens per request (shadow 1,240) | `u0-benchmark-off` | at most 831 (65 %) |
| T4 | quality 50.0 s per comment (2,701.7 s for 54 comments) | `u0-benchmark-shadow` | at most 25.0 s |
| T5 | quality first-attempt validity 75.9 % (41/54) | `u0-benchmark-shadow` | at least 95 % |
| T6 | 54.5 % of audited claims rejected (164/301) | `u0-extraction-development-off` | at most 35 % |
| T7 | precision of accepted claims 55.6 %, recall 28.8 % | `u0-extraction-development-off` | precision at least 65.6 %, recall at least 25.8 % |

Findings of U0.6:

- **Run-to-run variation at the same commit.** The two benchmark runs
  send byte-identical embedding requests (the same 10 request IDs), but
  the returned vectors differ: topic scores by up to 0.0075 and margins by
  up to 0.004. One English comment sits on the triage boundary (margin
  0.000 in `off`, −0.001 in `shadow`) and changed from candidate to review
  queue; the changed candidate set changed the relevance batches, and four
  other English decisions changed with it. Admitted comments 55 and 54,
  pending units 2 and 3. A probable cause is the partial GPU offload of
  the embedding model, whose layer split varies with free memory (not
  confirmed). Differences of this size between U0.6 and later L runs are
  noise, comparable to the one-unit tolerance of adoption rule 2.
- **Quality is slower than the archive suggested.** Benchmark quality
  requests take 40.3 s on average (2,701.7 s in total, 86 % of the shadow
  run's wall time) against 18.2 s in the archived legacy run. The cost is
  in decoding: `llama3.1:latest` writes 904 output tokens per quality
  request (75.5 s on average; the longest 283 s with 3,177 tokens),
  `qwen2.5:7b` 457 (15.0 s). Prompt sizes match the archive (3,353
  tokens).
- **Failure classes of quality attempts (ALG-01, for UP-D10).** Error
  counts over the attempts that failed validation (an attempt can carry
  several errors). Benchmark (26 attempts): `Literal absent from selected
  spans: character_literal` 22, `mechanic_literal` 4, uncovered
  non-whitespace original content 4, point/segment detail conflict 8,
  quote/offset mismatch 2. Synthetic (12 attempts): `character_literal` 6,
  uncovered content 4, quote/offset mismatch 8, detail conflict 2. No
  attempt failed in transport.
- **Route agreement under the D-4 rule.** Of the 18 disagreements, 6 are
  Chinese comments that failed validation; three of them
  (`missing_character`, `quoted_voice`, `me_too`) expect `review` and
  carry it as their fallback route, so comparing routes only would give
  19/34. Of the 12 completed disagreements: `mechanism_evidence` expected
  and `opinion_only` produced 5; an expected `exclude` part missing 4 (the
  two `high_emotion` cases also produce `review`); `review` expected and
  `opinion_only` produced 2 (`quoted_voice` and `sarcasm`, English);
  `exclude` expected and `review` produced 1 (`injection`, English).
- **Extraction by language.** English: precision 39/65 (60.0 %), recall
  38/73 (52.1 %). Chinese: precision 26/52 (50.0 %), recall 26/149
  (17.4 %). Labels keep the literal `阿俊` apart from `Arjun` (see
  "Evaluation sets"), which lowers both by string comparison.
- **Extraction tokens** agree with the archive: 3,404 and 3,782 uncached
  tokens per request against 3,421; extraction requests take 16.9 s on
  the benchmark and 23.5 s on the development split against 19.7 s.

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
- **`extraction-precision-v1`** (U0.5, UP-D02; frozen 2026-11-04). Purpose:
  comment-level (character, direction) precision and recall of extracted
  claims. Agent silver labels (`reviewer_type` `agent`,
  `independent_human_gold` false), written by session U0-A from
  `text_original` only, without any claim, quarantined claim, audit or
  relevance result of the archived run. Same source dataset and SHA-256 as
  `latency-benchmark-v1`. Selection from
  `full-pipeline-final/extraction-coverage.json` of the archived run
  `latest-balanced-20261027` (SHA-256 `85646b27…c5e38ead`, matching the
  archive's `SHA256SUMS`; IDs only): the 251 comments with
  `claims_generated` above 0 and the first 50 of the 272 eligible
  zero-claim comments (not `generation_failed`) in the order of SHA-256 of
  `extraction-precision-v1:<record_id>`. Split by that hash (first 8 hex
  digits modulo 10 below 7) plus the benchmark IDs: 27 benchmark IDs are in
  the set, 8 of them forced into development. 301 comments: development
  227 (89 English, 138 Chinese), test 74 (30, 44). Uncertain 24 (22
  development, 2 test). Scored positions: development 222 in 205 comments
  (166 nerf, 45 buff, 10 unclear, 1 keep; 62 comments without a position),
  test 71 in 72 comments. `labels_sha256`
  `de7d7e32ae46dc1feba31d9c01b818d33116157630a6e2492bdc8161eded9e63`. The
  manifest states the selection, split and label policy. Characters
  outside the glossary keep their source literal: `阿俊` (46 positions)
  and `Arjun` (8) probably name the same future character and are kept
  apart, so a scorer comparing strings counts a claim of one against a
  label of the other as wrong; seven other nicknames occur once to three
  times. Nationality-only references and sarcasm the text does not settle
  make a comment uncertain; a request with no textual cue of sarcasm is
  labeled literally.

## Archive and deletions

| Path | Archive location | SHA256SUMS entry | Reason | Step |
| ---- | ---------------- | ---------------- | ------ | ---- |
| `runs/upgrade/` (the five U0.6 runs, `u0-benchmark-shadow-interrupted`, measurements, materialized inputs, logs, live configuration, one-off scripts; ignored, not tracked) | `~/Archives/AIMediator/reports/20261104-upgrade-baseline/` | `SHA256SUMS` at the archive root, 5,323 files, 156,944,888 bytes | full runs of the U0.6 reference (P2); the curated report keeps the manifest and summary | U0.6 |

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
- **D-2 (U0.6) What the "Failures" column counts.** Plan 5.4 rule 2
  compares "technical-failure units on the benchmark" without defining the
  unit. `u0-benchmark-off` ended `partial` (exit 5, "requested processing
  has unresolved technical failures") with 0 failed requests and 0
  generation-failed comments. The two units behind the exit code are
  comments with a borderline retrieval margin (review queue) that the
  retrieval review rejected: they never become relevance candidates, keep
  `model_related` `null`, and `pipeline.coverage` reports them as
  `relevance_pending_or_failed` (coverage `relevance_state`
  `technical_failure_or_pending`). The run summary's `failed_requests`
  counts every request whose trace has errors, so in `shadow` runs it
  also counts quality outputs that fail validation. Options: (a) record
  the counts apart: requests with errors (validation and transport named
  apart), failed comments (`generation_failed`, `quality_failed`) and
  pending units (`relevance_pending_or_failed`); (b) count all of them as
  technical failures; (c) count failed requests only. Recommendation and
  action: (a), so any reading of rule 2 can be applied to the U0.6 rows;
  the recommended reading for U2 counts failed comments and transport
  failures as technical-failure units, with pending units compared apart.
  N-class (record only). Finding: the CLI's `partial` message calls
  review-queue units technical failures.
- **D-3 (U0.6) Interrupted live run discarded instead of resumed.** The
  agent session ended at about 21:04 while `u0-benchmark-shadow` was in its
  quality stage, and the run process ended with it (state `running`, last
  update 2026-11-05T05:03:58Z). Plan 10.4 resumes an interrupted live run
  with `--resume`. For a reference run that would (1) add the downtime to
  the wall time, which the tool measures from manifest creation to the last
  state update, and (2) return the in-flight quality request, whose only
  transport attempt is reserved as `started`, as
  `attempt_budget_exhausted`: a failure caused by the interruption. Both
  would enter the U2 reference. Options: (a) resume as plan 10.4 says and
  correct the numbers by hand; (b) keep the interrupted run as
  `runs/upgrade/u0-benchmark-shadow-interrupted` (archived, not measured)
  and run `u0-benchmark-shadow` again in a new directory. Recommendation and
  action: (b). N-class (`runs/` and the archive only), nothing deleted. The
  remaining runs ran in their own process session (`setsid`), so the end of
  an agent session no longer stops them.
- **D-4 (U0.6) Relevance and route agreement computed outside the
  package.** Rule 4 of plan 5.4 and step U0.6 need relevance agreement with
  the `balance-silver-v1` development labels and route agreement on
  `evidence-quality-synthetic-v1`. `aimediator.measurement` computes
  neither; `aimediator evaluate quality` scores point-level labels with
  adjudicated matches, which the synthetic set does not hold; and
  `evaluate_balance_review.py` requires the holdout sources in the run. The
  U0 boundary gives U0-L no package or script change. Options: (a) a
  one-off scorer under `runs/upgrade/tools/` that applies `relevance_metrics`
  of `scripts/experiments/evaluate_balance_review.py` (label `related`
  expects `relevance.json` `agreement` true; `uncertain` excluded) and the
  route check of `tests/test_evidence_quality.py` (over the cases that
  reach the quality stage: status `completed`, no errors, and sorted
  `routes_present` equal to sorted `expected_routes`), with its code
  archived under `provenance/` and its output in the curated summary; (b)
  add both functions to `measurement` (outside the U0-L boundary).
  Recommendation and action: (a); both functions move into `measurement`
  with tests before U2-L1 (see "Deferred").

## Escalations

- **E-1 (U0.6) `aimediator doctor` fails with the local embedding
  provider.** Raised and resolved on 2026-11-04. The first
  `doctor --config runs/upgrade/live-config.json` (the `init` defaults,
  `connection_timeout` 10) exited 3, `service_unavailable`, "Service/model
  probe unavailable (TimeoutError)". The probe's `/api/embed` call runs
  under `connection_timeout` (`inference.probe` through `Transport.api`
  without a run folder) and includes loading `qwen3-embedding:8b`; the
  service log shows the load aborted when the client closed the connection
  after 10.08 s (HTTP 499). One cold load from the page cache took 7.0 s
  (measured with `keep_alive` 0); the load from disk took longer than 10 s.
  `analyze` runs the same probe at the start of every run, and the chat
  models evict the embedding model, so run starts would pass or fail with
  the page cache. Options: (a) `connection_timeout` 120 in the live
  configuration; (b) keep 10 s and retry failed starts; (c) the configured
  remote provider; (d) end U0-L without runs. Owner decision on
  2026-11-04: (a). No request byte changes; the key also bounds
  `/api/tags`. `doctor` then passed every check. Blocked: nothing after
  the decision. Finding for U1 (service identity, plan 4.7): the probe
  applies the connection timeout to a call that loads a model.

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

### 2026-11-04 U0-A (annotation)

- Steps: U0.5 done; none started and stashed.
- State: HEAD is this entry's commit (parent `cdf6e33`); tests 250; lock
  green; rule check 0.
- Findings: no escalation; no label needed model outputs. Interpretations
  of the step notes, stated in the manifest's label policy: plain
  transliteration variants of a canonical name (`吉米`, `雅思敏`,
  `阿利克斯`) and a Ryu-only move name map to the glossary character;
  nicknames outside the glossary keep their literal, so `阿俊` and `Arjun`
  stay apart (see "Evaluation sets"); a comment with an unresolvable stance
  is uncertain even when it also holds clear positions.
- Next: U0.6 in session U0-L on the owner's machine; then U0-V; blockers:
  U0.6 needs the live environment and the embedding keys of the live
  configuration.

### 2026-11-04 U0-L (live)

- Steps: U0.6 done; none started and stashed.
- State: HEAD is this entry's commit (parent `2fb1532`); tests 250; lock
  green; rule check 0. The five reference runs ran at
  `50becc2`; the commits since change only the change record and the
  curated report.
- Findings: escalation E-1 (`doctor` failed on the embedding probe's 10 s
  connection timeout; the owner set `connection_timeout` 120); decisions
  found during execution D-2 (Failures column), D-3 (the agent session
  ended during `u0-benchmark-shadow`; the run was kept aside and rerun
  clean instead of resumed) and D-4 (relevance and route agreement from a
  one-off scorer, the package functions deferred); the UP-D10 row now
  carries the owner's answer (adopt), which the owner gave before U0.1 in
  `runs/20261104-up-owner-decisions.md`; the owner chose local
  embeddings, which differ from the archived run; two benchmark runs at
  the same commit differ by one admitted comment through embedding drift;
  quality takes 40 s per request, twice the archive, because of long
  `llama3.1:latest` outputs.
- Next: U0-V (verification, fresh session); then U1 (work order U1);
  blockers: none.

## Deferred

- **Relevance and route agreement in `measurement`** (D-4, from U0.6). Add
  the relevance agreement of `balance-silver-v1` and the route agreement of
  `evidence-quality-synthetic-v1`, with tests, to `aimediator.measurement`
  before U2-L1, so the L sessions of U2 compute them with committed code
  and the rule of D-4. The U2 boundary does not list `measurement.py`; the
  owner decides whether the U2 work order adds it or U2-L reuses the
  archived one-off scorer.
