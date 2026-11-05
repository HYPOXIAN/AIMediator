# Pipeline Upgrade Change Record

- Type: Record
- Status: Active
- Updated: 2026-11-05
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
| UP-D17 | adopt (raised by the owner) | 2026-11-04 | plan section 9; smaller live samples from U0.8 on (`upgrade-samples-v1`, steps U0.7 and U0.8); given after U0.6 |
| UP-D18 | adopt (raised by the owner) | 2026-11-05 | plan section 9; time budget of 8 hours from 00:17 (no batch starts that cannot finish by about 08:20); fewer live runs in U4-L, U5-L1 to U5-L3, U6-L and U7.1; at a review point without fix-up steps the verification session also does the closure |
| UP-D19 | adopt (raised by the owner) | 2026-11-05 | plan section 9 and 5.4 ("Hosted API"); given at 02:52, after the owner's computer shut down from overload during the U2-L1 runs: every live run of U2 to U7 calls the hosted API of `.env` (`LLM_MODEL` `deepseek/deepseek-v4-flash`) through the bridge `runs/upgrade/tools/api_bridge.py`, with no package change; the references are rerun through it in U2-L0; the local U2-L1 runs are kept aside and decide nothing |
| UP-D20 | adopt (raised by the owner) | 2026-11-05 | plan section 9; given at 03:05 and 03:06: API spend within 3.00 USD (the bridge refuses from 2.98 USD); the remaining chain finishes within 6 hours, by 09:05 (replaces the 08:20 limit of UP-D18); every chain session runs Opus 5.5 at effort xhigh; skipped: U2.5 with U2-L2, U6.3, U6.6; eight sessions with time boxes |

**Standing instruction (owner, 2026-11-04, after U0.6).** The remaining
sessions of U0 to U7 run unattended, one after another. Where a step, a
stop condition, an escalation or a review point needs an owner decision,
approval, review or choice, the session adopts the recommendation (of the
plan, the work order, this record or its own registered entry) and records
it as adopted under this instruction. An item without a recommendation, or
one that needs an action only the owner can take (such as restarting the
model service with other settings), is marked `bypassed` with the
question, the options and what was skipped; it holds back only the steps
that depend on it directly. The hard limits of `RULES.md` and plan section
1 stay in force: an action that would break one is bypassed, not adopted.
Reviews and answers recorded under this instruction were not given by the
owner in person.

**Owner authorization (2026-11-05 03:11, extends the standing
instruction).** The whole chain runs automatically without stopping, and
the agents may adopt their own suggestions as the owner's decisions. Where
a step, stop condition, escalation or review needs an owner decision, the
session adopts the recommendation (of the plan, a work order, this record
or its own registered entry); for an item without one, it forms its own
recommendation, adopts it and records it as adopted under this
authorization. A session does not end at a stop condition or escalation: it
records it, takes the adopted action and continues with the remaining
steps. The only exceptions are actions that would break `RULES.md` or the
hard limits of plan section 1 (credentials, frozen content, deletion
without archive): those are recorded as `bypassed` and the session
continues without them. Added to this record by session U3-1.

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
| U0.7 | D | done | 250 | green | UP-D17 (owner's amendment of 2026-11-04 after U0.6): `data/evaluation/upgrade-samples-v1/` frozen, four samples with `ids.json` and `manifest.json` each and a top-level manifest; see "Evaluation sets". `materialize` reproduces 30, 114, 19 and 120 rows with every content hash matching |
| U0.8 | L | done | 250 | green | UP-D17. Session U0-L2 on the owner's machine: environment equal to the U0.6 record, checked before and after the runs (`doctor` passed); the four samples materialized (30, 114, 19 and 120 rows, every content hash matching); the four sample reference runs at `0abfe02` measured and scored, see "Live evaluations" and the plan 5.5 baselines on the samples there; compared with the U0.6 rows in full and paired (D-5), differences beyond the intervals recorded as findings; curated report `reports/20261105-upgrade-baseline-samples/`; full runs archived with `SHA256SUMS` (2,693 files). The first U0-L2 agent was stopped after the runs had finished; a second agent finished the step without rerunning them |
| U1.1 | N | done | 254 | green | LAT-05, request index of plan 4.6. `Runner(..., journal=None)` calls `journal(<request directory relative to the run folder>, <no errors>)` after each `validation.json` write, and `operations.analyze` passes `run_store.record_request`, which updates the index of the last run folder (kept sorted by the relative parts of the `validation.json` path, the B5.8 order, with `bisect`). `initialize` starts the index empty; the first `state` call for a folder without one lists and reads `requests/**/validation.json` (resume: `load_resume` drops the folder's index, so a resume in the same process lists too); a write with status `interrupted` or `failed` lists again, because the interruption may fall between a validation write and its journal call. Contract: a scratch harness in the B5.8 form compared `run-state.json` after every write with a full scan of the validation files from the same previous state (`updated_at_utc` aside): 3,295 writes in 32 scenarios (three modes; stop stages `full`, `relevance` and `quality`, each resumed once; interruptions at the 1st, 2nd, 9th, 25th, 40th, 60th and 75th chat request of each mode, resumed with a second interruption and then to the end; invalid answers on every 5th request, resumed twice), all identical, key order included. `tests/test_run_store.py`: the B5.8 test rewritten for the journal, plus 50 `state` calls with one listing, a journal call before the first listing, the runner's journal call, and the reduced harness (13 cases, three modes interrupted twice and resumed, an invalid-answer run resumed; 230 writes) (+4). T9, measured with the new `scripts/experiments/run_synthetic_fixture_scale.py --comments 600 --mode shadow` (committed first, `43ec4cb`; Python 3.14.8, run folder on tmpfs; 1,236 requests): before, 31.1 s plain, 46.5 s under cProfile, `run_store.state` 1,239 calls, 27.6 s (59.4 % of the profiled time; B5.9 reported 54 % as 16.9 s of the plain 31.2 s); after, 14.6 s plain, 19.7 s under cProfile, `state` 1.06 s (5.4 %). Target below 5 %: not met. The rest of `state` is reading `run-state.json` and `resolved-config.json` and writing `run-state.json`, whose completed-identity list grows with the run and is frozen content |
| U1.2 | N | done | 257 | green | ALG-03. `balance_policy.term_matches` compiles each term's pattern once (`_term_pattern`, `functools.lru_cache(maxsize=8192)`; same pattern and flags, plain substring for terms without a Latin letter). `evidence.character_reference(text)` is memoized by `text` (`lru_cache(maxsize=1024)` on the builder) and returns a new copy on every call, by a structural copy instead of `copy.deepcopy` (decision found during execution D-6); `test_character_reference_returns_new_objects` passes. New `tests/test_character_matching.py` (+3): for the 350 `text_original` values of the tracked evaluation sets (the behavior lock's screening sets), the 38 fixture texts, `''` and one joined text, the new `character_reference`, `character_candidates` and `attributed_candidates` equal copies of the implementations at `678307e`, twice (the second pass reads the memo); `term_matches` equals its copy on every character term of the glossary; the memo hands out new objects at every level. A mutant without `re.I` fails both equivalence tests. T10 (plan 8.4 script; Python 3.14.8): at `678307e`, demo 0.88 to 0.92 s plain, 1.6 s under cProfile, `character_reference` 688 calls, 0.65 s (41 %; U0.4: 1.08 s, 35 %); after, 0.62 s plain, 0.93 s under cProfile, 688 calls, 0.076 s (8.2 %). Both targets met (at most 1.0 s; below 10 %). In the script's order the profiled demo follows the plain one in the same process and reads the memo; a profiled demo in a fresh process gives 1.02 s and 0.151 s (14.8 %) |
| U1.3 | N | done | 260 | green | ALG-04. `inference.streamed_chat` keeps one growing output string and a private `_LoopGuard`, created at the first chunk as the old code read the schema there: the identity scan (keys of an object `assessments`, or `comment_id` values of an array) and the claim scan resume at the end of their last match, the seen identities, key positions, pending claim starts and claim signatures persist between chunks, and only claim starts that did not decode yet are decoded again. The scans are exact rather than bounded by a key-length overlap: a complete match of each pattern does not change when the output grows, and an attempt that reaches the end leaves no complete match after it, so resuming at the last match end finds the matches of a full scan. Whitespace guard, check order, `done_reason` values, partial log and result unchanged; `repeated_claim` unchanged. New `tests/test_stream_guards.py` (+3) against copies of `streamed_chat` and `repeated_claim` at `a1c034e`, through a fake response object: 12 synthetic streams (normal English and Chinese outputs, duplicate key, duplicate claim, the same claim under two comments, a key inside a string value, array outputs with and without a duplicate `comment_id`, whitespace loops above and below 256, a quality-shaped output, malformed claims) at chunk sizes 1 to 16 and whole, and every two-chunk boundary for the samples up to 400 characters; two late and early claim loops of 4 comments with 8 claims; `repeated_claim` on prefixes. Same result dictionary and partial log every time. Timing (4 comments, 4-character chunks; best of 3): 2 claims each, 522 chunks, old 0.051 s, new 0.0055 s; 8 claims, 2,013 chunks, 0.654 s and 0.022 s; 30 claims, 7,495 chunks, 8.55 s and 0.097 s (plan 0.1: 549, 2,079 and 7,709 chunks, 0.05, 0.67 and 9.5 s) |
| U1.4 | B | done | 266 | updated by UP-D03 | LNK-04, plan 4.7. `Transport.version()` reads `/api/version` under `connection_timeout`; HTTP 404 gives `None` (recorded as unavailable), other failures raise `Failure(3)` with the messages of `probe`; `inference.service_version(transport)` returns the `version` string or `None` and refuses any other answer with `Failure(3)`. `run_store.identity` and `initialize` take the service version: identity key `service`, `{"ollama_version": ...}`, after `models`. `operations.analyze` reads it after `probe` for a new run; on resume, after the model digest check and before any write, a different value (`null` included) raises `Failure(4, 'Service version differs from saved run; start a new run')`, also for a completed run, as for model digests. `engine.run` reads `/api/version` through `api_transport` (HTTP 404 gives `None`) and records `service_version` after `models`; the L2 `fixture_api` of `tests/behavior_lock.py` answers `/api/version` from `FixtureTransport.version()`, `{'version': 'fixture-not-a-service'}`. New `tests/test_service_identity.py` (+6): endpoint, method and timeout; 404, HTTP 500, connection error, timeout and invalid JSON; the version string; the CLI identity with and without a version; resume of an interrupted fixture run with another version and with `null` exits 4 with no call and no file changed, then resumes with the saved version; the legacy identity with and without the endpoint (checklist item 5 of the work order). Lock regenerated (468 keys) for exactly the eight keys of work order section 3: `L1:<off|shadow|enforce>/manifest.json`, `L2:<off|shadow|enforce>/manifest.json`, `L1:example-report/report.json`, `L3:reviewed-report/report.json`; no other key differed. design/cli.md sections 5 and 7; guide, recovery section and exit-code advice. Escalation trigger of work order section 6 (`/api/version` on the owner's service): not raised; the U0.6 record holds the service's answer, Ollama 0.34.2, read from `/api/version` as plan 4.7 expects. No live call in this session |
| U1.5 | B | done | 270 | green | LNK-04, plan 4.7. `Runner._generate` appends `Context window reached` after the other validation errors when the response carries both `prompt_eval_count` and `eval_count` as integers (not booleans) and their sum is at least `payload['options']['num_ctx']`; the error reaches `validation.json`, the trace and the stage's existing failure handling. New `tests/test_context_guard.py` (+4): sums at and above 8192 fail, sums below it, missing, null, string and boolean counters pass; a fixture run in `off` whose multi-comment extraction responses fill the context splits every such batch into single-comment requests that succeed (no `generation_failed`); a fixture run in `shadow` whose first quality attempt for one comment fills the context sends attempt 2, which succeeds, and no other comment retries. Fixture responses carry no counters: the lock passes unchanged (468 keys). design/cli.md section 5 (runner). The runner journal test of U1.1 now answers the relevance request validly (`1c238ca`, `chore`, Step U1.1) |
| U1.6 | N | done | 270 | green | LNK-05 (open item B2-1 of the restructuring). `scripts/experiments/replay_balance_admission.py` passes the source manifest's `identity['evidence_quality']` as the runner's `quality_identity` when the manifest has one, and `None` (today's behavior) otherwise. Checked by hand at `517194d` plus this change (scratch, not committed): a legacy fixture run, `engine.run` with the fixture transport and `fixture_api` as lock target L2 runs it, on the 38 packaged sources with `--relevance-only` (which requires quality `off`; the identity still holds `evidence_quality`), 6 relevance requests. Before the change the script recomputed the request IDs without the quality identity, found no journaled response and stopped with `RuntimeError: Replay cannot run inference` (exit 1); after it, exit 0 with `verified_requests` 6, `comments` 38, `admitted` 38, `all_admission_decisions_unchanged` true and `fresh_inference_calls` 0. A copy of the run with `evidence_quality` removed from its manifest stops with the same `RuntimeError` before and after, as a manifest without the key did before. The script's other checks (policy and prompt hashes, cached source text, admission equality) are unchanged |
| U2.1 | N | done | 273 | green | LNK-01, plan 4.1. `stages.view(stage, data, ids)` returns the model-visible view: the audit view for `verify` (the former `prepare`, renamed; no caller needs the old name, so no alias), `data` itself for the other stages. `stages.MODEL_VISIBLE`: per stage the sets `top` and `comments` of the keys a view may hold, equal to today's keys. `Runner._generate` sends `{**view, 'response_schema': schema}`, passes the full `data` to `schema_for`, and to `normalize` for every stage except `verify`, which receives the view (its verdict's `scope` reads `selected_source_segments`). `Runner.generate(..., request_context=None)`: a context that is not `None` enters the cache identity as `request_context` and is not written into `request.json`; no caller passes one yet. New `tests/test_request_views.py` (+3): every request of the demo in three modes holds only `MODEL_VISIBLE` keys and the table lists no unused key (the demo sends no retrieval-review request; that row equals the relevance row); `request_context` changes only the request ID; the verify scope reads the view. `tests/test_stages.py` calls `view`. Lock unchanged (468 keys). design/cli.md section 5 (`stages`, `runner`, request construction) |
| U2.2 | B | done | 277 | updated by UP-D04 | LAT-01, PRM-05, plan 4.1. The quality view (`stages.view`) holds `comments` (`comment_id`, `units` with `evidence_id`, `text`, `start`, `end`), `language` and `character_normalization_reference` with only the entries whose canonical name `evidence.character_candidates` finds in the source text; `source`, `quality_contract` and `attempt` stay in the context. New `pipeline.quality_request(runner, row, units, language, contract, attempts)` builds the context of the next attempt and the `request_context` `{'attempt': n}`; after a failed attempt the context holds `previous_attempt` (`errors`, `transport_failure`) and the view adds `previous_attempt_errors`: the attempt's validation errors, at most 20, each cut to 300 characters, or the single entry `transport failure` when the new `Runner.transport_failed(stage, request_id)` finds the journaled response unreadable, malformed or carrying an `error` (transport, service, cache), so no remote text reaches the model. `assess_quality`, `scripts/experiments/diagnose_evidence_quality_live.py` and `run_quality_screening_experiment.py` call it; without the request context those scripts would have replayed attempt 1 as attempt 2. Prompt pair `evidence-quality.{en,zh}`: one closing paragraph on `previous_attempt_errors` (repair; never copy the error text; the meaning of `transport failure`); no other prompt change. `FixtureTransport` reads no removed key: unchanged. `MODEL_VISIBLE['quality']` follows. Tests (+4, `tests/test_request_views.py`): the view and its reference filter; the 20 by 300 cut and the transport entry; `transport_failed` on five journaled responses; a fixture run in `shadow` whose first attempt fails validation for one comment and in transport (`OSError` with remote text) for another: attempt 2 carries the trace errors or `['transport failure']`, the remote text appears in no request, no quality request holds `source`, `quality_contract` or `attempt`. The context guard and evidence-quality tests detect attempt 2 by `previous_attempt_errors`. Lock regenerated: exactly the 25 keys under "Behavior changes" (prompt assets and snapshots, manifests and the two reports through the prompt hashes, quality request digests); no extract, verify or relevance request changed. design/cli.md section 5 (`stages`, `runner`, `pipeline`); evidence-quality.md section 3.2 (the retry holds through `previous_attempt_errors`) |
| U2.3 | B | done | 278 | updated by UP-D05 | LAT-02, plan 4.1. The extraction view (`stages.view`) holds the units with `evidence_id` and `text` (no offsets); `allowed_quality_points` (enforce) with `point_id`, `evidence_ids` (the selected segments' E-IDs, first occurrence order), `quotes` (the selected segments' quotes), `scope`, `detail_level`, `stance`, `direction`, `character_literal` and `mechanic_literal` instead of the whole routing entry (`comment_id`, `route`, `reason`, `point` with `segment_ids`, `segments` with offsets and labels); and `character_normalization_reference` with the entries that `evidence.character_candidates` finds in a comment of the batch, on the comment's joined unit texts as `schema_for` finds the allowed characters, so every allowed character keeps its entry. `schema_for`, `ground_claim` and `bind_claim` read the full context, and the batches are still sized on it: `format`, `response_schema`, batching and gates unchanged. `diagnostics.extract` follows the view through the runner (docstring only). `FixtureTransport` reads `point_id` only: unchanged. Tests (+1): `tests/test_request_views.py` checks the view of a three-comment batch with quality points against the context, the reference filter and the schema's allowed characters; `tests/test_diagnostics.py` expects the view of real allowed points; `tests/test_stages.py` follows. Lock regenerated: exactly the 12 extraction request keys under "Behavior changes"; no artifact, prompt or other request changed. design/cli.md section 5 (`stages`, `diagnostics`) |
| U2.4 | B | done | 280 | updated by UP-D07 | LAT-03, plan 4.4. The relevance and retrieval-review prompt pairs gain a last paragraph, one line that introduces the topic list (P topics balance-related, N topics unrelated, cited by `topic_id` with their cosine), and `resources.prompts` appends `P1: <text>` to `P10: <text>` and `N1: <text>` to `N10: <text>`, one line each ending with a newline, in the order of `retrieval-anchors.json`, to those two stages only; the anchors keep one source (G2). The relevance and retrieval-review views keep `comment_id` and `text`, and each `retrieved_topics` item keeps `topic_id` and `cosine` rounded to 4 decimals (no `text`, no `class`, whose meaning the ID prefix and the prompt line carry). `retrieval.json`, `relevance.json` and the review queue keep the full references. `prompt-snapshot.json` and the identities' prompt hashes change. `scripts/experiments/replay_balance_admission.py` now takes the two prompts from `resources.prompts('off')`, as runs send them, instead of the asset files: it refuses every run made before this step (`Relevance prompt changed`, by design, plan 2.3), and without the change it would also have refused every run made after it. Checked by hand (scratch, not committed): a relevance-only legacy fixture run at this step replays with `verified_requests` 6, 38 admission decisions unchanged and no inference; the script without the change stops with `Relevance prompt changed`. Tests (+2, `tests/test_request_views.py`): the topic list ends exactly the relevance and retrieval-review prompts in all three modes and no other; every topic of every demo relevance request is cited by ID with the rounded cosine and found with its text in the system prompt; `tests/test_stages.py` checks the view. Lock regenerated: exactly the 38 keys under "Behavior changes" (prompt assets, snapshots, manifests and the two reports through the prompt hashes, relevance request digests); no other request or artifact changed. design/cli.md section 5 (`resources`, `stages`) |
| U2-L0 | L | done | 280 | green | UP-D19, UP-D20. The five reference runs (the four U0.8 sample runs and the U0.6 silver run, with their commands) through the API bridge `openrouter-bridge-1` at `0abfe02`, run by the orchestrating session from a copy of that commit's `src/` first on `sys.path`, in parallel with the U2-L1 runs; identity of every run checked (30 module and 21 resource hashes equal to `0abfe02`, digests equal to `doctor`, inputs equal to U0.8 and U0.6, every response from `deepseek/deepseek-v4-flash` on DeepInfra through version 1); API environment recorded, see "API environment (U2-L0, UP-D19)"; measured and scored with the committed tools and the one-off scorers; rows and API baselines in "Live evaluations"; compared with the local U0.8 and U0.6 rows as findings only; curated report `reports/20261105-upgrade-api-reference/`; full runs archived with `SHA256SUMS` (2,446 files). Spend of the ten runs 0.1082 USD |
| U2-L1 | L | done | 280 | green | UP-D19, UP-D20, D-8. The five U2-L1 runs at the code of `b7d1cc5` (the U2.4 commit) through bridge version 1, run by the orchestrating session in parallel with the U2-L0 runs; identity checked (30 module hashes equal to `b7d1cc5` and HEAD, service `openrouter-bridge-1`, digests equal to `doctor` and to U2-L0, inputs equal to the references, every response from `deepseek/deepseek-v4-flash` on DeepInfra); measured and scored; compared with the U2-L0 rows (`compare_u2l1.py` pointed at the `u2l0-*` runs) and the adoption rule applied per step as D-8 reads it: U2.2 holds, U2.3 fails rule 4 (recall 43.9 % against 48.8 %, −4.9 points), U2.4 holds; nothing reverted, U2.3 recorded for the owner's review (E-3). T2 met (48.0 % of the U2-L0 baseline, target 71.8 %); T1 (66.2 %, target 49.9 %) and T3 (75.0 %, target 65 %) not met. Budgets of U2.6 measured. Curated report `reports/20261105-upgrade-u2-evaluation/`; full runs archived with `SHA256SUMS` (3,244 files, with the local runs `u2l1-local-*`, which decide nothing) |
| U2.5 | B | skipped (UP-D20) | — | — | Response template trial (UP-D06) skipped by the owner's decision UP-D20 |
| U2-L2 | L | skipped (UP-D20) | — | — | Skipped with U2.5 (UP-D20); U2-L2 adds no summary file to the U2 report |
| U2.6 | N | done | 285 | green | Payload test of plan 4.1 (`cd3fd48`, `chore`): new `tests/test_request_payload.py` (+5). Every request of the offline demo and of lock target L2, three modes each, holds only the keys of `stages.MODEL_VISIBLE` (`response_schema` last); both targets send relevance, extraction, verify and, in `shadow` and `enforce`, quality requests and no retrieval-review request; no quality request holds `source`, `quality_contract` or `attempt`; the non-comment characters of every user message (its length minus the JSON-encoded `comments[].text`, `comments[].units[].text` and verify `original_evidence`) stay within the U2-L1 maxima plus 20 %, written as constants with that origin: relevance 2,512, retrieval review 2,422, quality 5,688, extraction 12,072, verify 2,376 (the demo and L2 reach 1,990, none, 4,784, 8,218 and 1,187); the count is checked on a hand-made message. ADR `docs/decisions/0003-model-visible-request-views.md` (context, decision, the measured effects of U2-L1, consequences) with its index row; design/cli.md section 5 (the payload contract after the frozen request construction text), balance-analysis.md (the relevance and retrieval-review prompts with the topic list, the relevance request, the extraction view under output), evidence-quality.md (inputs; the retry result of U2-L1). Lock unchanged (468 keys). Foreign working directory: 285 pass. Installed-wheel acceptance: `"passed": true`, 18 commands. The work order places U2.6 after U2-L2, which UP-D20 skips. The extraction budget measures the U2.3 view, which E-3 may revert |
| U3.1 | N | done | 289 | green | LAT-04, plan 4.5. `pipeline.ordered(units, work, commit, limit=1)`: a `ThreadPoolExecutor` with at most `limit` units in flight; `commit(unit, result)` runs on the calling thread in input order, and when the window is full the next unit is submitted only after the oldest is committed, so with limit 1 requests and writes interleave as in the serial loop. On any exception (`KeyboardInterrupt` included) pending units are cancelled, running ones finish or fail, nothing after the failed unit is committed, and the exception propagates. Units (plan 4.5): one retrieval-review batch with the single rechecks of its items (the rechecks follow their batch in the trace, as before); one relevance batch; one relevance recheck (`refinement_performed` is now set for every candidate before the rechecks, with the same values and key order); one quality comment with its attempts; one extraction batch with its single-comment split retries in queue order; one audited claim. Every write of the write schedule happens in the commit callbacks, in the current order. `RunState.max_parallel_requests` (default 1) is the limit; nothing sets it in this step. New `tests/test_concurrency.py` (+4): input-order commits on the calling thread at limits 1, 2, 4 and 8 with out-of-order completion; the window bound; the serial interleaving at limit 1; an interruption in the third unit at limit 3 commits units 1 and 2 only. Lock unchanged (468 keys); the resume and interruption tests pass |
| U3.2 | B | done | 291 | updated by UP-D08 | UP-D08, plan 4.5. Configuration key `max_parallel_requests` (integer 1 to 8, default 1; booleans, floats and `null` refused with exit 2), validated in `config.validate`, after `num_gpu` in the defaults; `aimediator analyze --max-parallel-requests`; a configuration file without the key resolves to 1. `operations.analyze` passes it to `pipeline.process` (`RunState.max_parallel_requests`; the legacy `engine` passes none and keeps 1) and serializes the journal callback, `run-state.json` updates and progress lines with one lock. `Runner` holds a lock per request identity around the response, `validation.json` write and journal call (`_validate`). Tests (+2, `tests/test_concurrency.py`): fixture runs in three modes at limits 1, 2 and 4 with a transport that sleeps and records the requests in flight (at most N, more than 1 above 1, the same call count) give the top-level artifacts of the N = 1 run with digests and elapsed times masked (the trace order included) and complete; the key's validation, the defaults for a file without it, the override, and the CLI refusal of 9 before any run directory exists. Lock regenerated: exactly the 8 keys `L1:<off|shadow|enforce>/manifest.json`, `L1:<off|shadow|enforce>/resolved-config.json`, `L1:example-report/report.json`, `L3:reviewed-report/report.json` (configuration and run identity); no request digest or other artifact changed. Guide (configuration section) and design/cli.md sections 4.2 and 6 |
| U3.3 | B | done | 295 | updated by UP-D09 | LAT-06, UP-D09, plan 4.6. New module `cache` (infrastructure; imports `common`): `chat_key(payload, model_digest, service_version, request_context=None)`, `SharedCache(root)` with `lookup(key, request)` and `store(key, request, response)` under `chat/<key[:2]>/<key>/request.json` and `response.json` (written with `common.write`), and `lookup_embedding`/`store_embedding` under `embedding/` for U3.4. The key is the SHA-256 of the payload with `stream` false, the model digest and the service version, plus the request context when given (D-9); the run identity is not part of it. Only finished responses (`done` true, `done_reason` `stop`, no `error`, a message) are stored, and a lookup returns a response only when the stored request equals the request. `Runner(..., shared_cache, model_digests, service_version)`: lookup order run journal, shared cache, transport; a hit writes `request.json`, `reuse-provenance.json` (`source` `shared_cache`, `key`, `original_elapsed_seconds`) and `response.json` with `elapsed_seconds` 0; a miss stores the response after the run's `response.json`. Configuration key `cache_dir` (default `null`), validated (a nonempty string or `null`); `aimediator analyze --cache-dir`; a relative path in a configuration file resolves against the file's directory, a CLI path against the invocation directory. `operations.analyze` builds the cache and passes the digests and service version of the run identity. `measurement` already counted `reuse-provenance.json` as reuse (U0.2): unchanged. Layering (UP-D01, plan 4.11): row `cache` → `common`; `runner` adds `cache`; `operations` adds `cache` (D-9). New `tests/test_shared_cache.py` (+4): two `enforce` fixture runs with one cache directory, the second makes no chat call and writes every JSON file of the first (manifest and requests included) apart from `run-state.json`, the provenance files, elapsed times and timestamps; one provenance file per response; `request_metrics` counts every request as reused; a third run at limit 3 makes no call; the runner's lookup order, unfinished answers not stored, a run with another run identity hits, another digest, service version or request context misses; the key and `storable`; the configuration key. Lock regenerated: exactly the 11 keys of the configuration and identity (as in U3.2) and the three existence-only keys `L2:<off|shadow|enforce>/code-snapshot/cache.py` (471 keys); no request digest changed. design/cli.md sections 5, 6 and 7; guide |

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

### API environment (U2-L0, UP-D19)

Recorded on 2026-11-05 by session U2-L0 from `runs/upgrade/logs/api-bridge.out`,
the bridge log (counters only), the doctor outputs and the run manifests
(`summary/u2l0-environment.json` and `summary/u2l0-identity.json` of
[`reports/20261105-upgrade-api-reference/`](../../reports/20261105-upgrade-api-reference/manifest.json)).
For every API session it replaces the local items of the record above
(plan 5.4, "Hosted API").

- Bridge version 1: `runs/upgrade/tools/api_bridge.py` on
  `127.0.0.1:11435`, started with `api_bridge_start.sh` in its own process
  session at 02:59; `/api/version` answers `openrouter-bridge-1`; SHA-256
  `32c5fc6ae82811d433f6932f632fe9ed8208deb425ca828ddabc0acf60fc2706`. It
  served all ten runs of U2-L0 and U2-L1 (03:01:38 to 03:20:46). Digests
  of `/api/tags`, reported by both `doctor` runs and recorded in every run
  manifest (embedding digest verified): `llama3.1:latest`
  `8d574ae973c939145534723ccb69d0ef74d725c7613b53b7dc92abc26235823e`,
  `qwen2.5:7b`
  `597b9a66239b131ee6abc2e0ed574bb6cbbafc5cfa8c350515668560889fab54`,
  `qwen3-embedding:8b`
  `0256197832255f898de62f2d76fcf769a29b520685c84113bd60850af1374439`.
  An earlier version-1 build (SHA-256
  `ba86da155967d1c9c3c722d96feec158f0d5928c45e345d8b59cbab34e82495e`)
  answered 8 probe requests before 02:59, one refused by the provider
  (`stream error 400`); no run used it.
- Bridge version 2 (`openrouter-bridge-2`, the UP-D20 spend guard;
  requests and answers unchanged), SHA-256
  `f42e0087ebcde0b193eaaa1d60cd2c735b7630fa7735ccda14acd7403e1137e9`,
  replaced version 1 at 03:20:59, after both run chains ended. Digests:
  `llama3.1:latest`
  `5d41ee66bd5e06ce8ab073183af15eef121e9672fb55dacf331d6d466a1d76e3`,
  `qwen2.5:7b`
  `1a7f84d0ce55a0f32267af827657ae645670fd8245df828a55c2489e8c338c66`,
  `qwen3-embedding:8b`
  `cd11cb615c74ae997aa0bbe3f1ad22e1f00f1fb4a27736bd9ca1cf6f1726539b`.
  Later API sessions check version 2 against these values (plan 5.4 names
  version 1; the replacement belongs to UP-D20). Each digest of the three
  starts recomputes from the version, the SHA-256 and the mapping below as
  the bridge computes it, so the mapping is the same in all three.
- The source of version 1 is not kept: version 2 overwrote
  `api_bridge.py` at 03:08, while version 1 was running from the file it
  had read at its start. The archive and `provenance/` hold version 2;
  version 1 is identified by its SHA-256 and digests above.
- Mapping: `llama3.1:latest` and `qwen2.5:7b` to
  `deepseek/deepseek-v4-flash`, `qwen3-embedding:8b` to
  `qwen/qwen3-embedding-8b`; providers pinned to DeepInfra without
  fallbacks.
- Remote model and provider: every chat response of the ten runs (339 in
  U2-L0, 342 in U2-L1; `response.json` and each transport attempt) carries
  a `remote` object with `deepseek/deepseek-v4-flash`, `DeepInfra` and
  `openrouter-bridge-1`. The bridge log of the run window holds 681 chat
  requests and 108 embedding requests (`qwen/qwen3-embedding-8b`,
  DeepInfra), all `ok`.
- Configuration: `runs/upgrade/live-config-api.json`, SHA-256
  `b44df0f2f8d7d0d6e295d7daa1314a729e2c285ec345596beff56a71fc1c4530`,
  equal to `live-config.json` except `base_url` `http://127.0.0.1:11435`;
  unchanged after the runs; no `--env-file`. Runtime Python 3.14.8,
  NumPy 2.4.6, package 0.1.0.
- Spend: the ten runs cost 0.1082 USD by the bridge log (chat and
  embedding, 03:01:38 to 03:20:59); the `remote` objects of the chat
  responses give 0.0587 USD for U2-L0 and 0.0484 USD for U2-L1. At its
  start version 2 restored 0.1198 USD from the whole log (0.1098 USD) plus
  its 0.01 USD allowance for unlogged probes; 2.86 USD remain below the
  refusal point of 2.98 USD.

## Live evaluations

| Session | Commit | Set | Mode | Wall time | Prompt tokens by stage | Output tokens by stage | Failures | Claims generated / accepted | Precision / recall (dev) | Quality validity | Verdict |
| ------- | ------ | --- | ---- | --------- | ---------------------- | ---------------------- | -------- | --------------------------- | ------------------------ | ---------------- | ------- |
| U0-L (`u0-benchmark-off`) | `50becc2` | `latency-benchmark-v1` (60) | `off` | 431.9 s | relevance 1,456 (1,278 uncached); retrieval_review 1,202 (962); extract 3,982 (3,404); verify 846 (254) | relevance 19; retrieval_review 20; extract 306; verify 7 | 0 requests with errors; 0 failed comments; 2 pending (review queue) | 43 / 17 (5 quarantined; 21 of 38 audited rejected) | 5/14 (35.7 %) / 5/20 (25.0 %), the 22 scored benchmark comments of the development split | — | reference |
| U0-L (`u0-benchmark-shadow`) | `50becc2` | `latency-benchmark-v1` (60) | `shadow` | 3,130.2 s | relevance 1,418 (1,240); retrieval_review 1,263 (1,056); quality 3,353 (2,089); extract 3,976 (3,399); verify 813 (305) | relevance 18; retrieval_review 21; quality 643; extract 252; verify 6 | 26 quality requests with validation errors, 0 transport; 13 quality-failed comments; 3 pending | 32 / 11 (4 quarantined; 17 of 28 rejected) | 3/8 (37.5 %) / 3/20 (15.0 %), same 22 comments | first attempt 41/54 (75.9 %, Wilson 63.1–85.4 %); 67 attempts | reference |
| U0-L (`u0-extraction-development-off`) | `50becc2` | `extraction-precision-v1` development (227) | `off` | 2,434.7 s | relevance 2,439 (2,250); retrieval_review 1,836 (1,621); extract 4,429 (3,782); verify 1,019 (345) | relevance 21; retrieval_review 21; extract 491; verify 7 | 0 requests with errors; 0 failed comments; 5 pending | 327 / 137 (26 quarantined; 164 of 301 rejected, 54.5 %) | accepted 65/117 (55.6 %, Wilson 46.5–64.2 %) / 64/222 (28.8 %, Wilson 23.3–35.1 %); generated 108/291 (37.1 %); recall over admitted 64/220 (29.1 %) | — | reference |
| U0-L (`u0-silver-development-relevance`) | `50becc2` | `balance-silver-v1` development (70) | `off`, `--stop-after relevance` | 186.8 s | relevance 2,033 (1,857); retrieval_review 1,520 (1,301) | relevance 20; retrieval_review 22 | 0 requests with errors; 3 pending | — | relevance agreement 59/69 (85.5 %, Wilson 75.3–91.9 %): 55 TP, 4 TN, 8 FN, 2 FP; 1 uncertain excluded | — | reference |
| U0-L (`u0-quality-synthetic-shadow`) | `50becc2` | `evidence-quality-synthetic-v1` (38) | `shadow`, `--stop-after quality` | 851.2 s | relevance 1,255 (1,089); retrieval_review 772 (664); quality 2,725 (1,681) | relevance 19; retrieval_review 18; quality 383 | 12 quality requests with validation errors, 0 transport; 6 quality-failed comments; 1 pending | — | — | first attempt 28/34 (82.4 %, Wilson 66.5–91.7 %); 40 attempts; route agreement 16/34 (47.1 %, Wilson 31.5–63.3 %), English 10/16, Chinese 6/18; 4 cases do not reach quality (3 rejected, 1 pending) | reference |
| U0-L2 (`u0s-benchmark-off`) | `0abfe02` | `upgrade-samples-v1/latency-benchmark` (30) | `off` | 188.0 s | relevance 1,576 (1,423 uncached); retrieval_review 1,329 (1,185); extract 3,955 (3,476); verify 763 (337) | relevance 19; retrieval_review 21; extract 228; verify 7 | 0 requests with errors; 0 failed comments; 2 pending (review queue) | 13 / 8 (0 quarantined; 5 of 13 audited rejected) | 2/6 (33.3 %) / 2/10 (20.0 %), the 11 scored sample comments of the development split | — | sample reference |
| U0-L2 (`u0s-benchmark-shadow`) | `0abfe02` | `upgrade-samples-v1/latency-benchmark` (30) | `shadow` | 1,565.4 s | relevance 1,619 (1,466); retrieval_review 1,329 (1,185); quality 3,338 (2,093); extract 3,880 (3,382); verify 856 (213) | relevance 20; retrieval_review 21; quality 633; extract 354; verify 7 | 13 quality requests with validation errors, 0 transport; 6 quality-failed comments; 1 pending | 30 / 19 (0 quarantined; 11 of 30 rejected) | 2/17 (11.8 %) / 2/10 (20.0 %), same 11 comments | first attempt 21/28 (75.0 %, Wilson 56.6–87.3 %); 35 attempts | sample reference |
| U0-L2 (`u0s-extraction-development-off`) | `0abfe02` | `upgrade-samples-v1/extraction-development` (114) | `off` | 1,372.4 s | relevance 2,861 (2,682); retrieval_review 1,773 (1,584); extract 3,955 (3,261), 44 of 48 requests with counters; verify 1,129 (394) | relevance 23; retrieval_review 19; extract 398; verify 7 | 4 extract requests with validation errors (`duplicate_claim_loop`), 0 transport; 1 generation-failed comment; 3 pending | 178 / 70 (23 quarantined; 85 of 155 rejected, 54.8 %) | accepted 45/66 (68.2 %, Wilson 56.2–78.2 %) / 40/123 (32.5 %, Wilson 24.9–41.2 %); generated 81/169 (47.9 %); recall over admitted 40/121 (33.1 %) | — | sample reference |
| U0-L2 (`u0s-quality-synthetic-shadow`) | `0abfe02` | `upgrade-samples-v1/quality-synthetic` (19) | `shadow`, `--stop-after quality` | 475.8 s | relevance 1,677 (1,576); retrieval_review 654 (582); quality 2,777 (1,636) | relevance 22; retrieval_review 16; quality 521 | 10 quality requests with validation errors, 0 transport; 5 quality-failed comments; 1 pending | — | — | first attempt 13/18 (72.2 %, Wilson 49.1–87.5 %); 23 attempts; route agreement 8/18 (44.4 %, Wilson 24.6–66.3 %), English 5/8, Chinese 3/10; 1 case does not reach quality (pending) | sample reference |
| U2-L0 (`u2l0-benchmark-off`) | `0abfe02` | `upgrade-samples-v1/latency-benchmark` (30) | `off` | 104.1 s | relevance 1,571 (1,539); retrieval_review 1,314 (1,314); extract 4,064 (3,771); verify 755 (499) | relevance 16; retrieval_review 15; extract 231; verify 7 | 0 requests with errors; 0 transport; 0 generation-failed comments; 1 pending | 14 / 8 (0 quarantined; 6 of 14 audited rejected, 42.9 %) | 4/6 (66.7 %) / 4/10 (40.0 %), the 11 scored sample comments of the development split | — | API reference |
| U2-L0 (`u2l0-benchmark-shadow`) | `0abfe02` | `upgrade-samples-v1/latency-benchmark` (30) | `shadow` | 538.1 s | relevance 1,571 (1,379); retrieval_review 1,314 (418); quality 3,469 (2,692); extract 4,064 (2,016); verify 760 (405) | relevance 16; retrieval_review 14; quality 782; extract 215; verify 7 | 6 quality requests with validation errors; 0 transport; 3 quality-failed comments; 0 generation-failed comments; 1 pending | 13 / 8 (0 quarantined; 5 of 13 audited rejected, 38.5 %) | 4/6 (66.7 %) / 4/10 (40.0 %), the 11 scored sample comments of the development split | first attempt 23/26 (88.5 %, Wilson 71.0–96.0 %); 29 attempts | API reference |
| U2-L0 (`u2l0-extraction-development-off`) | `0abfe02` | `upgrade-samples-v1/extraction-development` (114) | `off` | 340.7 s | relevance 2,979 (2,979); retrieval_review 3,496 (3,035); extract 4,437 (3,955); verify 968 (396) | relevance 19; retrieval_review 22; extract 373; verify 7 | 0 requests with errors; 0 transport; 0 generation-failed comments; 2 pending | 137 / 82 (3 quarantined; 52 of 134 audited rejected, 38.8 %) | accepted 61/80 (76.2 %, Wilson 65.9–84.2 %) / 60/123 (48.8 %, Wilson 40.1–57.5 %); generated 85/131 (64.9 %); recall over admitted 60/123 (48.8 %) | — | API reference |
| U2-L0 (`u2l0-silver-development-relevance`) | `0abfe02` | `balance-silver-v1` development (70) | `off`, `--stop-after relevance` | 41.1 s | relevance 2,063 (2,063); retrieval_review 1,882 (1,882) | relevance 16; retrieval_review 18 | 0 requests with errors; 0 transport; 0 generation-failed comments; 1 pending | — | relevance agreement 63/69 (91.3 %, Wilson 82.3–96.0 %): 60 TP, 3 TN, 3 FN, 3 FP; 1 uncertain excluded | — | API reference |
| U2-L0 (`u2l0-quality-synthetic-shadow`) | `0abfe02` | `upgrade-samples-v1/quality-synthetic` (19) | `shadow`, `--stop-after quality` | 120.1 s | relevance 1,476 (1,476); retrieval_review 610 (610); quality 2,845 (1,875) | relevance 16; retrieval_review 11; quality 429 | 6 quality requests with validation errors; 0 transport; 3 quality-failed comments; 0 generation-failed comments; 2 pending | — | — | first attempt 13/16 (81.2 %, Wilson 57.0–93.4 %); 19 attempts; route agreement 11/16 (68.8 %, Wilson 44.4–85.8 %), English 5/7, Chinese 6/9; 16 of 19 cases reach quality | API reference |
| U2-L1 (`u2l1-benchmark-off`) | `b7d1cc5` | `upgrade-samples-v1/latency-benchmark` (30) | `off` | 103.0 s | relevance 1,439 (1,154); retrieval_review 1,353 (1,251); extract 2,788 (2,495); verify 741 (464) | relevance 15; retrieval_review 14; extract 198; verify 7 | 0 requests with errors; 0 transport; 0 generation-failed comments; 2 pending | 12 / 8 (0 quarantined; 4 of 12 audited rejected, 33.3 %) | 4/6 (66.7 %) / 4/10 (40.0 %), the 11 scored sample comments of the development split | — | rules 2 and 3: T1 and T3 move down; see the verdicts |
| U2-L1 (`u2l1-benchmark-shadow`) | `b7d1cc5` | `upgrade-samples-v1/latency-benchmark` (30) | `shadow` | 510.2 s | relevance 1,539 (698); retrieval_review 1,353 (790); quality 1,957 (1,293); extract 2,874 (2,435); verify 757 (501) | relevance 16; retrieval_review 14; quality 775; extract 219; verify 7 | 5 quality requests with validation errors; 0 transport; 2 quality-failed comments; 0 generation-failed comments; 3 pending | 13 / 8 (0 quarantined; 5 of 13 audited rejected, 38.5 %) | 4/6 (66.7 %) / 4/10 (40.0 %), the 11 scored sample comments of the development split | first attempt 21/24 (87.5 %, Wilson 69.0–95.7 %); 27 attempts | rules 2 and 3: T2 moves down; see the verdicts |
| U2-L1 (`u2l1-extraction-development-off`) | `b7d1cc5` | `upgrade-samples-v1/extraction-development` (114) | `off` | 347.5 s | relevance 2,256 (1,826); retrieval_review 2,795 (2,027); extract 3,353 (2,841); verify 975 (604) | relevance 17; retrieval_review 20; extract 362; verify 7 | 0 requests with errors; 0 transport; 0 generation-failed comments; 2 pending | 130 / 76 (1 quarantined; 53 of 129 audited rejected, 41.1 %) | accepted 55/74 (74.3 %, Wilson 63.3–82.9 %) / 54/123 (43.9 %, Wilson 35.4–52.7 %); generated 74/120 (61.7 %); recall over admitted 54/121 (44.6 %) | — | U2.3 rule 4 fails: recall 4.9 points below the reference |
| U2-L1 (`u2l1-silver-development-relevance`) | `b7d1cc5` | `balance-silver-v1` development (70) | `off`, `--stop-after relevance` | 35.7 s | relevance 2,082 (1,634); retrieval_review 1,645 (1,154) | relevance 16; retrieval_review 15 | 0 requests with errors; 0 transport; 0 generation-failed comments; 6 pending | — | relevance agreement 64/69 (92.8 %, Wilson 84.1–96.9 %): 58 TP, 6 TN, 5 FN, 0 FP; 1 uncertain excluded | — | U2.4 rule 4 holds: one agreeing comment more |
| U2-L1 (`u2l1-quality-synthetic-shadow`) | `b7d1cc5` | `upgrade-samples-v1/quality-synthetic` (19) | `shadow`, `--stop-after quality` | 112.2 s | relevance 1,313 (1,185); retrieval_review 958 (617); quality 1,799 (1,233) | relevance 16; retrieval_review 11; quality 418 | 6 quality requests with validation errors; 0 transport; 3 quality-failed comments; 0 generation-failed comments; 2 pending | — | — | first attempt 13/16 (81.2 %, Wilson 57.0–93.4 %); 19 attempts; route agreement 11/16 (68.8 %, Wilson 44.4–85.8 %), English 5/7, Chinese 6/9; 16 of 19 cases reach quality | U2.2 rule 4 holds: validity and route agreement equal |

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

Rows of U0.8 (runs from 2026-11-04 23:19 to 2026-11-05 00:19, session
U0-L2): the four sample reference runs of plan 7 U0.8 on
`upgrade-samples-v1` (UP-D17), at `0abfe02` (the U0.7 commit; `src/` is
unchanged since `50becc2`, and every module hash in the run manifests
equals the package file at `0abfe02`), with the U0.6 commands and live
configuration, one after another, each in its own process session. They
are the sample reference of U2 and later live sessions (plan 5.4); the
U0.6 rows stay the full-set baseline. The environment was checked against
the section above before the runs and again after them: service 0.34.2,
the same service process since 2026-11-04 17:10:10 (no restart before or
during the runs), the server settings, GPU, the three model digests
(each run manifest records them, embedding digest verified) and the
runtime equal to the U0.6 record; `doctor` passed every check;
`live-config.json` unchanged (SHA-256
`03659ca91320224b2d8c772758654e30e9fa8c36ce4b81b34637a973ca781f7b`); no
`--env-file`. Each run's identity differs from its U0.6 run only by the
input and source hashes. Inputs, materialized with the command in each
sample's manifest, every content hash checked:
`runs/upgrade/inputs/upgrade-sample-benchmark.jsonl` (30 rows,
`ce7ee3df8efc73d36840b96dff00407e42cea9f29de2369ccb64aa4abac28f4a`),
`upgrade-sample-extraction-development.jsonl` (114,
`46e5bb22d38c7b76f8521b376eaac5635ac8988007b9d3c37510315273c6b311`),
`upgrade-sample-quality-synthetic.jsonl` (19,
`0d7a8e8adf6650ee673145d93530abfd0a2c79785712b5bfc2fa58af1590a8e4`) and
`upgrade-sample-full-balanced.jsonl` (120,
`434bf553b4b2447d336ba736c6269fa15dcbee1214601fbd67430779bfd1f3c7`, for
U7.1, not run here). Route agreement uses the D-4 scorer with `cases.json`
of `evidence-quality-synthetic-v1` filtered to the 19 sample IDs
(`runs/upgrade/inputs/upgrade-sample-quality-synthetic-cases.json`).
Token figures are means over fresh requests with counters (every request
is fresh; the 4 looped extraction requests of the extraction sample carry
no counters). "Failures" follows D-2. Wall time is the measurement
tool's; every run ended `partial` (exit 5) because of pending review-queue
units, as in U0.6. Measurements, scores, the paired U0.6 values and the
comparison are in
[`reports/20261105-upgrade-baseline-samples/`](../../reports/20261105-upgrade-baseline-samples/manifest.json);
full runs in the archive (see "Archive and deletions").

Baselines of plan 5.5 on the samples (from U0.8 on, a baseline named U0.6
is the U0.8 run of the same sample and mode, plan 5.5). "U0.6 paired" is
the U0.6 run over the sample's comments only; the batched stages
(relevance, extraction) have no paired value, because their requests mix
comments.

| ID | U0.8 sample baseline | Run | U0.6 full set | U0.6 paired | Target (plan 5.5) |
| -- | -------------------- | --- | ------------- | ----------- | ----------------- |
| T1 | extraction 3,476 uncached prompt tokens per request (shadow 3,382) | `u0s-benchmark-off` | 3,404 (shadow 3,399) | — | at most 1,700 |
| T2 | quality 2,093 uncached prompt tokens per request (3,338 in total) | `u0s-benchmark-shadow` | 2,089 (3,353) | 2,176 (3,333) | at most 1,500 |
| T3 | relevance 1,423 uncached prompt tokens per request (shadow 1,466) | `u0s-benchmark-off` | 1,278 (shadow 1,240) | — | at most 925 (65 %) |
| T4 | quality 46.9 s per comment (1,312.7 s for 28 comments) | `u0s-benchmark-shadow` | 50.0 s (54 comments) | 44.1 s (1,147.5 s for 26) | at most 23.4 s |
| T5 | quality first-attempt validity 75.0 % (21/28, Wilson 56.6–87.3 %) | `u0s-benchmark-shadow` | 75.9 % (41/54) | 80.8 % (21/26) | at least 95 % |
| T6 | 54.8 % of audited claims rejected (85/155, Wilson 47.0–62.5 %) | `u0s-extraction-development-off` | 54.5 % (164/301) | 57.2 % (91/159) | at most 35 % |
| T7 | precision of accepted claims 68.2 % (45/66, Wilson 56.2–78.2 %), recall 32.5 % (40/123, Wilson 24.9–41.2 %) | `u0s-extraction-development-off` | 55.6 %, 28.8 % | 64.5 % (40/62), 31.7 % (39/123) | precision at least 78.2 %, recall at least 29.5 % |

Comparison with the U0.6 rows (`summary/u0s-comparison.json`, rule D-5).
Within the intervals: the quality prompt, uncached and output tokens and
elapsed time per request; first-attempt validity on the benchmark (75.0 %
against 75.9 %, paired 80.8 %) and on the synthetic sample (72.2 % against
82.4 %, paired 81.3 %); route agreement (8/18, 44.4 %, against 16/34,
47.1 %, paired 8/16, 50.0 %); extraction recall (32.5 % against 28.8 %,
paired 31.7 %); audit rejection on the extraction sample (54.8 % against
54.5 %, paired 57.2 %); the relevance and retrieval-review means of every
run; the extraction prompt tokens and elapsed time on the benchmark.
Differences beyond the intervals are the findings below; none is a stop.

Findings of U0.8:

- **The extraction sample scores higher than the full split.** Precision
  of accepted claims, 68.2 %, lies above the U0.6 interval (55.6 %, 46.5
  to 64.2 %), and precision of generated claims, 47.9 %, above its own
  (37.1 %, 31.8 to 42.8 %). Paired, the U0.6 run scores 64.5 % and 41.9 %
  on the same 114 comments, so the sample run differs by +3.7 and +6.1
  points, within the intervals. The sample's comments are easier than the
  rest of the development split: T7 on the sample starts from 68.2 % and
  its target is 78.2 %, not 65.6 %.
- **Benchmark precision follows one comment.** In `u0s-benchmark-shadow`
  precision of accepted claims is 2/17 (11.8 %), below the full U0.6
  interval (3/8, 37.5 %, 13.7 to 69.4 %; paired 2/7, 28.6 %, within), and
  precision of generated claims is 4/27 (14.8 %), below both intervals
  (paired 5/14, 35.7 %, 16.3 to 61.2 %). Twelve of the 17 accepted claims
  are the same `Terry` `nerf` claim on one English comment
  (`steam:217837645`) whose label holds no position; that comment receives
  1 such claim in `u0s-benchmark-off`, 7 in `u0-benchmark-off` and 3 in
  `u0-benchmark-shadow`. Precision counts every claim (recall counts a
  position once), so on 11 scored comments one comment decides the value;
  without it, 2/5. Benchmark precision is not a stable comparison;
  adoption rule 4 reads the extraction sample.
- **One generation failure on the extraction sample.** Four extraction
  requests of `llama3.1:latest` ended with `duplicate_claim_loop` (no
  counters, 92.8 s together): three 4-comment batches, whose comments were
  then retried one per request, and the retry of `steam:231760293`, which
  ended `generation_failed` (coverage `extraction_failed`). The U0.6 run of
  the full split had no such request; the archived run had 7. Under the
  D-2 reading the extraction sample reference holds 1 technical-failure
  unit. The benchmark references hold 0 failed comments in `off` and 6
  quality-failed comments of 28 in `shadow` (U0.6: 13 of 54; paired 5 of
  26), with 2 and 1 pending units.
- **Extraction requests on the extraction sample are smaller.** 3,955
  prompt tokens (3,261 uncached), 398 output tokens and 18.3 s per request
  against 4,429 (3,782), 491 and 23.5 s, all beyond the intervals. The
  sample fills fewer batches: 2.56 comments per request against 3.32 (18
  single-comment requests against 10, 12 of them the retries above).
  Per-request means of batched stages depend on how an input fills the
  batches; T1 is measured on the benchmark sample, where the extraction
  means agree with U0.6 (3,476 uncached against 3,404).
- **Verification and audit rejection follow the claim set.** The verify
  means lie outside the U0.6 intervals in all three full-pipeline runs
  (uncached prompt tokens 337, 213 and 394 against 254, 305 and 345;
  elapsed time within 0.2 s per request); a verify request carries one
  claim, so these means move with the claims. Audit rejection on the
  benchmark is 5/13 (38.5 %) in `off` and 11/30 (36.7 %) in `shadow`
  against 21/38 (55.3 %) and 17/28 (60.7 %) for the full set, beyond the
  intervals; paired (11/25, 44.0 %; 5/15, 33.3 %) within. Benchmark
  extraction output in `shadow` (354 tokens against 252) lies above the
  U0.6 interval; its own interval is wide (84 to 623, 8 requests).
- **Admission differs on a few sample comments.** Paired over the sample
  comments: benchmark `off` admits `steam:235458828` and not
  `steam:237735508`; `shadow` admits `steam:229390012` and
  `steam:235458828` in addition; the extraction sample admits 3 comments
  the U0.6 run did not and misses 2 it admitted; the synthetic sample
  admits `price_and_opinion:en` and `venting:zh`, which U0.6 rejected at
  relevance. Relevance and retrieval-review requests batch several
  comments, so on a sample a comment meets other neighbours than in the
  full set, and the embedding drift of U0.6 adds to that. From U2 on the
  comparisons use the U0.8 runs, so these differences do not enter them.
- **Route agreement is unchanged on the common cases.** The 16 cases that
  reached quality in both runs agree in the same 8. The two cases admitted
  only in U0.8 disagree (`venting:zh` failed validation and carries its
  fallback `review`; `price_and_opinion:en` gives `system_evidence` where
  `exclude` and `opinion_only` are expected); `high_emotion:zh` failed
  validation in U0.8 (completed in U0.6, disagreeing in both); `me_too:en`
  stays pending.
- **Failure classes of quality attempts (ALG-01)** are those of U0.6.
  Benchmark (13 failed attempts): `character_literal` 8, uncovered
  non-whitespace original content 7, quote/offset mismatch 4,
  point/segment detail conflict 2, `mechanic_literal` 2. Synthetic (10):
  quote/offset mismatch 8, `character_literal` 4, uncovered content 4,
  detail conflict 2. No attempt failed in transport.
- **Wall time.** 188.0 s, 1,565.4 s, 1,372.4 s and 475.8 s, together
  3,601.6 s (60.0 minutes), against 6,848.0 s for the four U0.6 runs
  (53 %). Quality takes 1,312.7 s of the benchmark `shadow` run (84 %).

Rows of U2-L0 (UP-D19; runs from 2026-11-05 03:01 to 03:21, started by
the orchestrating session as one chain beside the chain of the U2-L1
runs; session U2-L0): the four U0.8 sample runs and the U0.6 silver run
of plan 7 U2-L0, with their commands, through bridge version 1 at
`0abfe02`, run from `runs/upgrade/code-0abfe02/src` (`git archive` of
that commit) first on `sys.path`. Identity of each run
(`check_api_identity.py`): the 30 module and 21 resource hashes of its
manifest equal the files at `0abfe02`; model and embedding digests equal
the doctor output; input and source hashes equal those of the U0.8 run
(U0.6 for the silver split); the code of `0abfe02` records no service
version (U1.4 came later), so the version comes from the `remote`
objects. Token figures, Failures and wall time as in the U0.8 rows;
tokens are counted by the provider's tokenizer, and "uncached" is the
provider's prompt cache (findings below). Every run ended `partial`
(exit 5) because of pending units. These rows are the reference of U2-L1
and later API sessions; the local rows stay history and are not compared
with API runs (plan 5.4). Measurements, scores, the identity check, the
environment record and the comparison with the local rows are in
[`reports/20261105-upgrade-api-reference/`](../../reports/20261105-upgrade-api-reference/manifest.json);
full runs in the archive (see "Archive and deletions").

Baselines of plan 5.5 through the API (from U2-L0 on, a baseline named
U0.6 or U0.8 is its U2-L0 run; T1 and T2 keep the ratio of their targets
to the U0.6 baselines, plan 5.4; T8 comes from the U3 L run):

| ID | U2-L0 API baseline | Run | Target |
| -- | ------------------ | --- | ------ |
| T1 | extraction 3,771 uncached prompt tokens per request (4,064 in total; shadow 2,016 uncached) | `u2l0-benchmark-off` | at most 1,882 (49.9 %) |
| T2 | quality 2,692 uncached prompt tokens per request (3,469 in total) | `u2l0-benchmark-shadow` | at most 1,933 (71.8 %) |
| T3 | relevance 1,539 uncached prompt tokens per request (1,571 in total; shadow 1,379) | `u2l0-benchmark-off` | at most 1,000 (65 %) |
| T4 | quality 18.3 s per comment (476.6 s for 26 comments) | `u2l0-benchmark-shadow` | at most 9.2 s (indicative, plan 5.4) |
| T5 | quality first-attempt validity 88.5 % (23/26, Wilson 71.0–96.0 %) | `u2l0-benchmark-shadow` | at least 95 % |
| T6 | 38.8 % of audited claims rejected (52/134, Wilson 31.0–47.3 %) | `u2l0-extraction-development-off` | at most 35 % |
| T7 | precision of accepted claims 76.2 % (61/80, Wilson 65.9–84.2 %), recall 48.8 % (60/123, Wilson 40.1–57.5 %) | `u2l0-extraction-development-off` | precision at least 86.2 %, recall at least 45.8 % |

Findings of U2-L0, from the comparison with the local U0.8 and U0.6 rows
(`summary/u2l0-local-comparison.json`; findings only, they decide
nothing):

- **The hosted model is faster and scores higher.** Wall time 104.1,
  538.1, 340.7, 41.1 and 120.1 s (19.1 minutes) against 188.0, 1,565.4,
  1,372.4, 186.8 and 475.8 s (63.1 minutes); quality 18.3 s per comment
  against 46.9 s. Extraction sample: precision of accepted claims 76.2 %
  against 68.2 % (+8.1 points, Newcombe −6.3 to +22.5), recall 48.8 %
  against 32.5 % (+16.3, +4.0 to +27.9), audit rejection 38.8 % against
  54.8 %. Relevance agreement 63/69 against 59/69. Quality first-attempt
  validity 23/26 against 21/28 on the benchmark and 13/16 against 13/18
  on the synthetic sample; route agreement 11/16 (68.8 %) against 8/18
  (44.4 %). No generation-failed comment (local: 1 on the extraction
  sample), 3 quality-failed comments in each quality run (local: 6 and
  5), no transport failure, 1 or 2 pending units per run.
- **One model for both languages.** Both chat names reach
  `deepseek/deepseek-v4-flash`; the local rows had `llama3.1:latest` for
  English and `qwen2.5:7b` for Chinese, so per-language findings of the
  local rows do not carry over.
- **Prompt tokens agree; uncached tokens follow the provider's cache.**
  On the benchmark the provider's prompt token means are within 5 % of the
  local ones (extraction 4,064 against 3,955, quality 3,469 against 3,338,
  relevance 1,571 against 1,576). The cached share is the provider's
  prompt cache, which requests share across runs and across the two
  chains that ran the same prompt prefixes side by side: in
  `u2l0-benchmark-shadow` retrieval review has 418 uncached tokens of
  1,314 and extraction 2,016 of 4,064, against 1,314 and 3,771 in
  `u2l0-benchmark-off`, which ran first. Uncached means depend on run
  order and concurrency; T1 to T3 keep the plan's metric (D-8), and the
  rows give the total prompt tokens beside it.
- **Admission differs on a few comments.** Benchmark `off` admits 3
  comments the U0.8 run did not and misses 3 (26 each); the silver split
  admits 64 against 58; the synthetic sample 16 against 18
  (`injection:en` and `venting:zh` rejected at relevance).
- **Elapsed times measure the provider and the network** (plan 5.4):
  1 to 16 s per request on average by stage; T4 is indicative.

Rows of U2-L1 (UP-D19; runs from 2026-11-05 03:01 to 03:20, started by
the orchestrating session as one chain beside the chain of the U2-L0
runs; session U2-L1): the five runs of the work order at HEAD, the code
of `b7d1cc5` (the U2.4 commit; no later commit changes `src/`), through
bridge version 1, with the API configuration. Identity of each run: the
30 module hashes of its manifest equal the files at `b7d1cc5` and at
HEAD; service `{"ollama_version": "openrouter-bridge-1"}`; model and
embedding digests equal the doctor output and the U2-L0 runs; input and
source hashes equal the reference runs'; every chat response from
`deepseek/deepseek-v4-flash` on DeepInfra (see "API environment (U2-L0,
UP-D19)"). Values as in the U2-L0 rows. The gates at HEAD (`79cfbb5`,
code of `b7d1cc5`) before the measurement: 280 tests, rule check 0, lock
green (468 keys). The reference of each run is its U2-L0 run, and every
reading of D-8 holds with the U2-L0 runs in place of the U0.8 and U0.6
runs (UP-D19). The local runs `runs/upgrade/u2l1-local-*` made before the
shutdown are archived with these runs and decide nothing. Measurements,
scores, the identity check and the comparison (`summary/u2l1-comparison.json`,
with Wilson intervals, Newcombe intervals of the differences and the
paired quality attempts) are in
[`reports/20261105-upgrade-u2-evaluation/`](../../reports/20261105-upgrade-u2-evaluation/manifest.json);
full runs in the archive.

Verdicts of U2-L1 (adoption rule of plan 5.4, read as D-8):

| Step | Rule 1 gates | Rule 2 failure units and coverage | Rule 3 target metric | Rule 4 no inferiority | Verdict |
| ---- | ------------ | --------------------------------- | -------------------- | --------------------- | ------- |
| U2.2 (UP-D04) | pass | quality-failed comments 0 and 2 against 0 and 3 (benchmark `off`, `shadow`); 0 transport; coverage complete | T2: quality 1,293 uncached prompt tokens per request against 2,692 (−52.0 %, difference interval −1,668 to −1,129); 1,957 against 3,469 in total; paired attempt 1 of 24 comments −1,402 (−51.5 %) | synthetic first-attempt validity 13/16 against 13/16; route agreement 11/16 against 11/16, no case changed | kept |
| U2.3 (UP-D05) | pass | generation-failed comments 0 and 0 against 0 and 0; 0 transport; coverage complete | T1: extraction 2,495 uncached prompt tokens per request against 3,771 (−33.8 %, −2,161 to −391); 2,788 against 4,064 in total | precision of accepted claims 55/74 (74.3 %) against 61/80 (76.2 %), −1.9 points (Newcombe −15.5 to +11.5), within 3; recall 54/123 (43.9 %) against 60/123 (48.8 %), −4.9 points (−17.0 to +7.5), beyond 3 | **fails rule 4** (recall); recorded for the owner's review (E-3), not reverted |
| U2.4 (UP-D07) | pass | 0 transport; coverage complete; pending units 2 and 3 against 1 and 1 (compared apart, D-8) | T3: relevance 1,154 uncached prompt tokens per request against 1,539 (−25.0 %, −1,297 to +528); 1,439 against 1,571 in total | relevance agreement 64/69 (92.8 %) against 63/69 (91.3 %), +1 comment, the same 69 evaluated | kept |

Targets of plan 5.5 through the API (plan 5.4 ratios): T1 2,495, 66.2 %
of the U2-L0 baseline, not met (at most 49.9 %, 1,882); T2 1,293, 48.0 %,
met (at most 71.8 %, 1,933; also below the plan's 1,500); T3 1,154,
75.0 %, not met (at most 65 %, 1,000).

Findings of U2-L1:

- **The extraction recall loss is Chinese and partly admission.** Recall
  English 29/46 against 30/46, Chinese 25/77 against 30/77; precision
  English 29/31 against 30/32, Chinese 26/43 against 31/48. The
  extraction sample admits 109 comments against 111 (3 no longer
  admitted, 1 newly admitted), a change of the relevance stage (U2.4)
  that recall over all labeled positions counts; recall over admitted
  comments is 54/121 (44.6 %) against 60/123 (48.8 %), −4.2 points, still
  beyond 3. The three steps were measured together, so the share of U2.3
  and of U2.4 in the loss cannot be separated, and both intervals of the
  difference include 0.
- **Uncached tokens follow the provider's cache.** The shadow benchmark
  gives relevance 698 uncached tokens (50.6 % of 1,379) and extraction
  2,435 (120.8 % of 2,016), against 75.0 % and 66.2 % in `off`; the
  totals fall in both modes (extraction 2,874 against 4,064 in `shadow`).
  Per comment sent, extraction falls from 1,015 to 759 uncached tokens
  and relevance from 385 to 325 in `off`. D-8 reads the uncached means;
  the totals agree in direction for every step.
- **Relevance holds more units pending.** Pending units: benchmark 2 and
  3 against 1 and 1, silver split 6 against 1, extraction sample 2
  against 2. The silver split admits 59 against 64, with 2 newly wrong
  and 3 newly right comments; the benchmark admits 23 and 24 against 26.
- **Quality.** First-attempt validity on the benchmark 21/24 (87.5 %)
  against 23/26 (88.5 %); of the 24 common comments 20 valid in both, 1
  valid only in U2-L1 and 1 only in U2-L0. Quality output and elapsed
  time per comment are unchanged (775 against 782 tokens, 18.5 s against
  18.3 s). Attempt 2 now carries `previous_attempt_errors`; 1 of 3
  benchmark retries succeeded (U2-L0: 0 of 3; synthetic: 0 of 3 in both).
- **Budgets for U2.6** (`budgets_u2_6` of the comparison): the largest
  non-comment characters of a user message over the 342 requests of the
  five runs, by stage: relevance 2,093, retrieval review 2,018, quality
  4,740, extraction 10,060, verify 1,980. Comment texts are
  `comments[].text`, `comments[].units[].text` and verify
  `original_evidence`; the tool counted `original_comment` only before this
  session, a key no view has, so the session added `original_evidence`
  before the budgets were computed. The other readings of D-8 are
  unchanged.

## Behavior changes (P7)

| Step | Decision | Asset or request part | Old SHA-256 | New SHA-256 | Lock paths |
| ---- | -------- | --------------------- | ----------- | ----------- | ---------- |
| U1.4 | UP-D03 | Run manifest identity: new key `service` (`ollama_version`) in CLI runs, `service_version` in legacy runs; no asset or prompt changes; request bytes change only in the run ID that CLI quality requests carry (LAT-01), as with every code change (plan 2.3), and request IDs through it; the lock normalizes both | — (no asset) | — (no asset) | `L1:enforce/manifest.json`, `L1:off/manifest.json`, `L1:shadow/manifest.json`, `L2:enforce/manifest.json`, `L2:off/manifest.json`, `L2:shadow/manifest.json`, `L1:example-report/report.json`, `L3:reviewed-report/report.json` |
| U1.5 | UP-D03 | Request validation: the error `Context window reached` when `prompt_eval_count + eval_count >= num_ctx`; no asset, prompt or request byte changes | — (no asset) | — (no asset) | none (fixture responses carry no counters; lock unchanged) |
| U2.2 | UP-D04 | Quality request view: no `source`, `quality_contract` or `attempt`; character reference limited to the comment's candidates; `previous_attempt_errors` on attempt 2; the attempt in the cache identity (`request_context`). Prompt `src/aimediator/assets/prompts/evidence-quality.en.txt` | `ac6bcd87b33cfad586402f5b8b9b516a09dcaa6f959989a9adedaf80f0543db0` | `0da81e6d66b596c68d911723be5b3e97f3b368c85032da4dacd92b666b4bf2c7` | `L1:enforce/manifest.json`, `L1:enforce/prompt-snapshot.json`, `L1:enforce/requests/**/request.json`, `L1:enforce/requests/quality/<request-id>/request.json`, `L1:enforce/resource-snapshot/prompts/evidence-quality.en.txt`, `L1:enforce/resource-snapshot/prompts/evidence-quality.zh.txt`, `L1:example-report/report.json`, `L1:off/manifest.json`, `L1:off/resource-snapshot/prompts/evidence-quality.en.txt`, `L1:off/resource-snapshot/prompts/evidence-quality.zh.txt`, `L1:shadow/manifest.json`, `L1:shadow/prompt-snapshot.json`, `L1:shadow/requests/**/request.json`, `L1:shadow/requests/quality/<request-id>/request.json`, `L1:shadow/resource-snapshot/prompts/evidence-quality.en.txt`, `L1:shadow/resource-snapshot/prompts/evidence-quality.zh.txt`, `L2:enforce/manifest.json`, `L2:enforce/prompt-snapshot.json`, `L2:enforce/requests/**/request.json`, `L2:enforce/requests/quality/<request-id>/request.json`, `L2:shadow/manifest.json`, `L2:shadow/prompt-snapshot.json`, `L2:shadow/requests/**/request.json`, `L2:shadow/requests/quality/<request-id>/request.json`, `L3:reviewed-report/report.json` |
| U2.2 | UP-D04 | Prompt `src/aimediator/assets/prompts/evidence-quality.zh.txt` (same paragraph) | `1e7099fb80a2ce26d6a919d4aff993c64d467ff4b3e89a1eb72b63c5bac9ecc4` | `1db0f055acbd7c40e945e97c9fb955061107c1477632dfd3543404bb76675f6e` | as above |
| U2.3 | UP-D05 | Extraction request view: units without offsets, trimmed `allowed_quality_points`, character reference limited to the batch's candidates; no asset or prompt changes | — (no asset) | — (no asset) | `L1:enforce/requests/**/request.json`, `L1:enforce/requests/extract/<request-id>/request.json`, `L1:off/requests/**/request.json`, `L1:off/requests/extract/<request-id>/request.json`, `L1:shadow/requests/**/request.json`, `L1:shadow/requests/extract/<request-id>/request.json`, `L2:enforce/requests/**/request.json`, `L2:enforce/requests/extract/<request-id>/request.json`, `L2:off/requests/**/request.json`, `L2:off/requests/extract/<request-id>/request.json`, `L2:shadow/requests/**/request.json`, `L2:shadow/requests/extract/<request-id>/request.json` |
| U2.4 | UP-D07 | Prompt `src/aimediator/assets/prompts/relevance.en.txt` (new last paragraph introducing the topic list) | `ea21f6e8ffc3becac8e7a6a06511019d767df1eabddc49715bb7b4826cf9abe2` | `78207e6c61b78db2ed8334e84ec07715fce6c76aaeea9ecf001f0181883342ea` | `L1:enforce/manifest.json`, `L1:enforce/prompt-snapshot.json`, `L1:enforce/requests/**/request.json`, `L1:enforce/requests/relevance/<request-id>/request.json`, `L1:enforce/resource-snapshot/prompts/relevance.en.txt`, `L1:enforce/resource-snapshot/prompts/relevance.zh.txt`, `L1:enforce/resource-snapshot/prompts/retrieval-review.en.txt`, `L1:enforce/resource-snapshot/prompts/retrieval-review.zh.txt`, `L1:example-report/report.json`, `L1:off/manifest.json`, `L1:off/prompt-snapshot.json`, `L1:off/requests/**/request.json`, `L1:off/requests/relevance/<request-id>/request.json`, `L1:off/resource-snapshot/prompts/relevance.en.txt`, `L1:off/resource-snapshot/prompts/relevance.zh.txt`, `L1:off/resource-snapshot/prompts/retrieval-review.en.txt`, `L1:off/resource-snapshot/prompts/retrieval-review.zh.txt`, `L1:shadow/manifest.json`, `L1:shadow/prompt-snapshot.json`, `L1:shadow/requests/**/request.json`, `L1:shadow/requests/relevance/<request-id>/request.json`, `L1:shadow/resource-snapshot/prompts/relevance.en.txt`, `L1:shadow/resource-snapshot/prompts/relevance.zh.txt`, `L1:shadow/resource-snapshot/prompts/retrieval-review.en.txt`, `L1:shadow/resource-snapshot/prompts/retrieval-review.zh.txt`, `L2:enforce/manifest.json`, `L2:enforce/prompt-snapshot.json`, `L2:enforce/requests/**/request.json`, `L2:enforce/requests/relevance/<request-id>/request.json`, `L2:off/manifest.json`, `L2:off/prompt-snapshot.json`, `L2:off/requests/**/request.json`, `L2:off/requests/relevance/<request-id>/request.json`, `L2:shadow/manifest.json`, `L2:shadow/prompt-snapshot.json`, `L2:shadow/requests/**/request.json`, `L2:shadow/requests/relevance/<request-id>/request.json`, `L3:reviewed-report/report.json` |
| U2.4 | UP-D07 | Prompt `src/aimediator/assets/prompts/relevance.zh.txt` (same) | `056abaefb8cca96c3091ed0e6d16b20527229f7476cddd4a7d442f4388519ef6` | `b361bbd6466bbe1101b6bbbb9bdd219700edabb89666be35c391919627cec2af` | as above |
| U2.4 | UP-D07 | Prompt `src/aimediator/assets/prompts/retrieval-review.en.txt` (same) | `f513b9095a3db43588599a6287530a4a97a776976de000bbeaaeb12deda76caf` | `3fa9b45bee55e4d75d89f9ceb9ea2fbc09d54827e79097be5ce2c03b576d4570` | as above |
| U2.4 | UP-D07 | Prompt `src/aimediator/assets/prompts/retrieval-review.zh.txt` (same) | `39f85b6e2a933a1e26930d27e99c7ccb26cf8dc727779a6865449230543de747` | `d380ce74d326effd506437c9f483a98bcfccee5432ae454b2e80d6c845857f19` | as above |
| U2.4 | UP-D07 | System prompts as sent (`resources.prompts`, asset plus the 20 topic lines): relevance en, relevance zh, retrieval_review en, retrieval_review zh; relevance and retrieval-review request views (topics by `topic_id` and rounded `cosine`) | the asset values above | `0159d9b864e92e531ad3722d737b69a4db07f6e00d189a8b5b19df53d9caac13`, `756139556593fdafeee5c0f3ce27b90aa40c743a28b04d0a8f5b54126bb53be0`, `9a74eec994f693b70471658b71c01ab8a1aeb6337313592459fe35876abf7e3b`, `77290b24d196825b2ca80dc6dcdd122c5fe7db234e9e17e08c741c2f97d86cfc` | as above |
| U3.2 | UP-D08 | Configuration key `max_parallel_requests` (default 1) in `resolved-config.json` and the run identity; no asset, prompt or request byte changes | — (no asset) | — (no asset) | `L1:enforce/manifest.json`, `L1:enforce/resolved-config.json`, `L1:off/manifest.json`, `L1:off/resolved-config.json`, `L1:shadow/manifest.json`, `L1:shadow/resolved-config.json`, `L1:example-report/report.json`, `L3:reviewed-report/report.json` |
| U3.3 | UP-D09 | Configuration key `cache_dir` (default `null`) in `resolved-config.json` and the run identity; new module `cache` in the code identity and the legacy `code-snapshot/`; `reuse-provenance.json` on shared-cache hits; no asset, prompt or request byte changes | — (no asset) | — (no asset) | the 8 keys of U3.2 and `L2:enforce/code-snapshot/cache.py`, `L2:off/code-snapshot/cache.py`, `L2:shadow/code-snapshot/cache.py` |

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
- **`upgrade-samples-v1`** (U0.7, UP-D17; frozen 2026-11-04). Purpose:
  smaller inputs for the live runs from U0.8 on (plan 5.3); no labels
  (`reviewer_type` `none`), IDs and content hashes only. Four
  subdirectories, each a set that `materialize` reads (`ids.json` with
  `record_id`, `language`, `content_sha256`, and `length_tercile` where
  stratified; its own `manifest.json` with the rule, the source dataset
  and its SHA-256, and the `materialize` command):
  `latency-benchmark` (30: the first 5 per language and tercile of
  `latency-benchmark-v1` in its own hash order; `ids_sha256`
  `f5c5cff429f2a07781ef088f355bfe85baeff0d03527f0f01d75b05593f51cae`);
  `extraction-development` (114: per language the first half of the
  development split by SHA-256 of `upgrade-samples-v1:<comment_id>`, 45
  English and 69 Chinese; 9 uncertain, 123 scored positions;
  `3f02f0ddc72f1531b9137323b4ffe93f206dfdab8d4a4c6340538851c02913da`);
  `quality-synthetic` (19: one case per category of
  `evidence-quality-synthetic-v1`, Chinese and English alternating in
  category order, 10 Chinese and 9 English;
  `e4e936dbe7d93f62ea5e149ee79422b1130bbf9f0895ee41eea31fe3274aa58e`);
  `full-balanced` (120 of the 600-comment dataset for U7.1: 20 per
  language and tercile with the cut points of `latency-benchmark-v1`, by
  SHA-256 of `upgrade-samples-v1:<record_id>`;
  `98ae4aee683e2ea88b2a9f9d37b087757583860c958a8737b4e059abf298685d`).
  Twelve of the 114 extraction comments are benchmark IDs. Built by the
  orchestrating agent on the owner's instruction; the manifests state
  every rule, so U0-V can rerun them.

## Archive and deletions

| Path | Archive location | SHA256SUMS entry | Reason | Step |
| ---- | ---------------- | ---------------- | ------ | ---- |
| `runs/upgrade/` (the five U0.6 runs, `u0-benchmark-shadow-interrupted`, measurements, materialized inputs, logs, live configuration, one-off scripts; ignored, not tracked) | `~/Archives/AIMediator/reports/20261104-upgrade-baseline/` | `SHA256SUMS` at the archive root, 5,323 files, 156,944,888 bytes | full runs of the U0.6 reference (P2); the curated report keeps the manifest and summary | U0.6 |
| `runs/upgrade/` (the four U0.8 sample runs, their measurements and the comparison, the materialized samples and derived inputs, logs, live configuration, doctor output and environment check, one-off scripts; ignored, not tracked) | `~/Archives/AIMediator/reports/20261105-upgrade-baseline-samples/` | `SHA256SUMS` at the archive root, 2,693 files, 74,493,575 bytes | full runs of the U0.8 sample reference (P2); the curated report keeps the manifest and summary | U0.8 |
| `runs/upgrade/` (the five U2-L0 runs, their measurements, identity check, environment record and comparison with the local rows, the materialized inputs, run logs and the bridge log, the API configuration and doctor output, the bridge and one-off scripts; ignored, not tracked) | `~/Archives/AIMediator/reports/20261105-upgrade-api-reference/` | `SHA256SUMS` at the archive root, 2,446 files, 118,026,987 bytes | full runs of the U2-L0 API reference (P2); the curated report keeps the manifest, summary and provenance | U2-L0 |
| `runs/upgrade/` (the five U2-L1 runs, their measurements, identity check and comparison, the materialized inputs, run logs and the bridge log, the API configuration and doctor output, the bridge and one-off scripts; the local runs `u2l1-local-benchmark-off`, `u2l1-local-benchmark-shadow` and `u2l1-local-extraction-development-off-interrupted` with their measurements and logs under `local/`; ignored, not tracked) | `~/Archives/AIMediator/reports/20261105-upgrade-u2-evaluation/` | `SHA256SUMS` at the archive root, 3,244 files, 156,077,243 bytes | full runs of the U2-L1 evaluation (P2); the curated report keeps the manifest, summary and provenance | U2-L1 |

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
- **D-5 (U0.8) How the sample runs are compared with the U0.6 rows.** The
  step note asks for a comparison of each sample row with its U0.6 row,
  where "a difference beyond the intervals is a finding". The sample and
  the full set hold different comments, and the note does not define the
  interval. Options: (a) compare twice, with the whole U0.6 run and paired
  with the U0.6 run restricted to the sample's comments (quality requests
  are per comment and pair; the batched stages compare over the whole run
  only), and call a difference beyond the interval when the U0.8 value
  lies outside the 95 % interval of the U0.6 value (Wilson for
  proportions, mean ± 1.96 standard errors for per-request means); (b) an
  interval of the difference (Newcombe for proportions, Welch for means),
  full set only; (c) paired values only. Recommendation and action: (a),
  as implemented by the one-off `compare_u0s.py` of the first U0-L2 agent
  (archived under `provenance/`): it reports every comparison both ways and
  flags more differences than (b), which suits a step whose flags are
  findings and not stops. N-class (run output and record only).
- **D-6 (U1.2) How the memoized character reference is copied.** The step
  note asks `evidence.character_reference` to return `copy.deepcopy` of
  the cached value. With `copy.deepcopy` the demo spends about 0.21 s of
  1.1 s under cProfile (19 %) in `character_reference`, almost all in
  the copy, against the T10 target below 10 %. The reference is
  JSON-shaped (dicts, lists and immutable leaves from `glossary.json` and
  `balance-review-policy.json`, no object shared inside it). Options:
  (a) `copy.deepcopy`, as the note says; (b) a structural copy that
  creates a new dict or list at every level and shares only the
  immutable leaves (`evidence._json_copy`), which gives callers the same
  values and new objects, as `copy.deepcopy` does for this data, at
  8.2 %. Recommendation and action: (b). N-class, undone by a revert, no
  `RULES.md` change, nothing deleted; the equivalence and new-object
  tests hold for both.
- **D-7 (U2.4) Prompts of `replay_balance_admission.py`.** The step note
  says the script "will refuse the new prompts by design (it checks prompt
  hashes)". The script read the relevance and retrieval-review prompts
  from the asset files, while runs send `resources.prompts`, which from
  U2.4 on appends the topic list to the asset text. Left as it was, it
  would refuse every run, those made after U2.4 included, and its replay
  requests would lack the topic list. Options: (a) leave the script as
  it is; (b) take the two prompts from `resources.prompts('off')`, which
  for runs made before U2.4 hashes exactly as the asset files did.
  Recommendation and action: (b), in the U2.4 commit
  (`scripts/experiments/` is in the U2 boundary): runs made before U2.4
  are still refused (plan 2.3), runs made after it replay. Checked by
  hand (U2.4 row). Undone by a revert of the script lines, no `RULES.md`
  change, nothing deleted; no package request byte changes.
- **D-8 (U2-L1) How the adoption rule reads for three B steps measured
  together.** The U2-L1 runs measure U2.2, U2.3 and U2.4 at once, and the
  work order names the metrics of each verdict. Plan 5.4 does not say how
  rule 2 (technical-failure units) is attributed to a step, which
  precision rule 4 means, or how "do not fall" reads for proportions whose
  denominators move with admission. Options: (a) per step, the metrics the
  work order names, read on the stage the step changes: rule 1 the gates
  at HEAD; rule 2 on both benchmark runs, the step's failure units within
  one of the reference (U2.2 quality-failed comments, U2.3
  generation-failed comments, every step transport failures; D-2 reading,
  pending units compared apart) and every input comment with a coverage
  status, the whole-run total reported beside it; rule 3 the step's target
  mean (T2 quality on the benchmark `shadow`, T1 extraction and T3
  relevance on the benchmark `off`) below the reference; rule 4 for U2.2
  first-attempt validity and route agreement on the synthetic sample not
  below the reference value, for U2.3 precision of accepted claims and
  recall over all labeled positions on the extraction sample not more than
  3 points below, for U2.4 agreeing comments on the silver split not more
  than one below with the same evaluated count. The reference is the
  whole U0.8 run of the same sample and mode (the same input; U0.6 for the
  silver split), the deciding values are the run values of the "Live
  evaluations" row, and paired per-comment values, Wilson intervals and
  Newcombe intervals of the differences are reported beside them without
  deciding; (b) every rule-4 metric for every step, so that any failure
  fails all three; (c) decide on the comments common to both runs only.
  Recommendation and action: (a), fixed before the runs were measured
  (`runs/upgrade/tools/compare_u2l1.py`, archived under `provenance/`): a
  step can only move the metrics of the stages it changes (in `off` runs
  no quality request is sent), and (c) would drop the comments whose
  admission the steps change. N-class (record and run output only).

- **D-9 (U3.3) Shared-cache key and the `operations` layering row.**
  Registered by session U3-1 on 2026-11-05. (1) Plan 4.6 names the key as
  the payload with `stream` false, the model digest and the service
  version. Quality attempts 2 and 3 can send the same bytes when their
  previous errors are equal, and the run journal separates them by
  `request_context` (U2.2); without it in the shared key, attempt 3 would
  receive attempt 2's answer from the cache. Options: (a) add the request
  context, when given, to the key; (b) the plan's key only. (2) Plan 4.11
  adds `cache` to the `runner` row only, but `operations.analyze` builds the
  cache from the configuration and U3.4 hands it to `retrieval` too.
  Options: (a) `operations` adds `cache` (a service importing
  infrastructure, as it imports `runner`); (b) `runner` builds the cache
  from a path, and `retrieval` imports `cache`, which changes a third row.
  Recommendation and action for both: (a), adopted under the owner
  authorization of 2026-11-05 03:11; a revert undoes both, no request byte
  and no `RULES.md` rule changes.

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
- **E-2 (U2-L1) This record reaches the D7 size limit.** Raised on
  2026-11-05 by the orchestrating session while committing D-8, which
  the U2-L1 session had written before the shutdown: with D-8 the record
  holds 102,837 bytes against the D7 limit of 102,400, and the pre-commit
  hook refused the commit. Every later session adds to this record.
  Options: (a) list this record in `D7_JUSTIFIED` of `check_rules.py`
  with its reason, as the owner decided for the restructuring's record
  (E-4 of [that record](20261103-code-restructuring.md)); (b) continue in
  a second record, which changes the plan and every work order; (c)
  condense this record, which buys room for one session only.
  Recommendation and action: (a), adopted under the owner's standing
  instruction, in its own `chore` commit; `RULES.md` does not change and
  the D7 test already covers a listed file. Blocked: nothing after the
  commit.

- **E-3 (U2-L1) U2.3 fails adoption rule 4.** Raised on 2026-11-05 by
  session U2-L1. Recall of (character, direction) positions on the
  extraction sample is 43.9 % against 48.8 % for the U2-L0 reference,
  −4.9 points (Newcombe −17.0 to +7.5), beyond the 3-point margin; the
  other rules hold (see the U2-L1 verdicts under "Live evaluations").
  Options: (a) revert U2.3 as a fix-up step of the U2 review (plan 1.7,
  5.4), then remeasure, and rederive the extraction budget of the U2.6
  payload test, which the U2.3 view sets; (b) keep U2.3 against the rule,
  with the reason recorded (the loss is within the sampling error, mostly
  Chinese, and partly the admission change of U2.4); (c) measure U2.3
  alone (U2.4 reverted in a scratch run) before deciding. Recommendation:
  (a), the plan's rule; U5 builds on U2.3 (plan 6), so a revert reaches U5
  too. Not adopted by this session: the work order assigns the decision to
  the owner's review and forbids a revert in the live session; it is
  recorded for U2-V and the review recorded under the owner's standing
  instruction. Blocked: nothing in this session; U2.6 proceeds on HEAD.

## Verification notes

### 2026-11-05 U0-V

- Range: `upgrade-plan..c587115`; 14 commits. Steps U0.1 to U0.8: U0-1
  `43a0c23`, `be3875d`, `bca6490`, `cdf6e33`; U0-A `50becc2`; U0-L
  `0976760`, `2fb1532`, `09ca80c`; U0.7 `0abfe02`, committed by the
  orchestrating session on the owner's amendment; U0-L2 `8255249`,
  `5967ab6`. Three commits are not batch steps: `6a68245` (the standing
  instruction), `84d03a9` (UP-D17) and `c587115` (UP-D18). All checks
  ran on `c587115` with Python 3.14.8 and NumPy 2.4.6. Temporary output
  went outside the checkout; `runs/` and the archive were not written.
- Checks:
  1. Boundary and commit hygiene (plan 8.8): pass. The boundary check
     prints 8 paths, all under `docs/plans/` (the plan and seven work
     orders). Only `84d03a9` (UP-D17) and `c587115` (UP-D18) change them,
     the owner amendments that work order section 3 exempts. Those two
     commits and `6a68245` change nothing else except the decision rows
     and the standing instruction in this record: no code, test, data,
     report or lock. No step commit leaves the pattern. `src/` changes
     only by `measurement.py`, `data/` only by the three new sets and
     `reports/` only by the two new directories. No existing file under
     `data/` or `reports/` is modified or removed. The hygiene check
     prints nothing: every commit has a `Step:` or `Session:` line. The
     steps name their decisions (U0.2 UP-D01; U0.3 and U0.5 UP-D02; U0.7
     and U0.8 UP-D17), subjects use P5 types, each set has its own `data`
     commit, and each step's last commit carries its progress row. No
     commit message or changed file holds attribution.
  2. Lock fixture: pass. Only `be3875d` (U0.2) changes
     `tests/fixtures/behavior-lock.json`. It adds three lines,
     `L2:<enforce|off|shadow>/code-snapshot/measurement.py`, each
     `<exempt: existence only>`. No other key changed.
  3. Gates, foreign directory and wheel: pass. 250 tests pass (floor 241),
     and again from a foreign working directory; rule check `Total: 0`;
     lock green. Installed-wheel acceptance: `"passed": true`,
     `"commands": 18` (as in U0.4); the wheel holds
     `aimediator/measurement.py`.
  4. Evaluation sets: pass. Every SHA-256 in the manifest of the raw
     dataset `20261027-balanced` matches its file (19 files). The
     recomputed `ids_sha256` of `latency-benchmark-v1` (`8f0931b0…`) and
     `labels_sha256` of `extraction-precision-v1` (`de7d7e32…`) equal
     their manifests and this record. Rerunning the U0.3 rule from the
     manifest gives the cut points (English 208 and 764, Chinese 31 and
     99), the tercile sizes and the 60 rows of `ids.json` exactly: IDs,
     order, languages, content hashes and terciles. The split rule holds
     for all 301 labels: 227 development and 74 test, with 27 benchmark
     IDs, 8 of them forced into development. The labels are in hash
     order, and every content hash and language matches the dataset.
     Beyond the item, the U0.5 selection was rerun from
     `extraction-coverage.json`, using IDs and counts only (its SHA-256
     equals the manifest's). It gives the same 301 IDs: 251 with claims
     and 50 of 272 eligible. The four `ids_sha256` of `upgrade-samples-v1`
     (`f5c5cff4…`, `3f02f0dd…`, `e4e936db…`, `98ae4aee…`) equal the sample
     manifests, the top-level manifest and this record. Each rule, rerun
     from its manifest, gives its `ids.json` exactly: 30; 114 (45 English,
     69 Chinese); 19 (10 Chinese, 9 English); 120. Each source dataset
     hash matches. `materialize` reproduces every set and split, and the
     materialized inputs hash to the values recorded for U0.6 and U0.8.
  5. Plan 8.7 rerun: pass. Both outputs are byte-identical to the U0.4
     outputs in `runs/upgrade/`, and every figure of the U0.4 entry
     agrees. For example: extract, both models, 157 (122) requests,
     19.7 s, 4,080 prompt, 659 cached and 3,421 uncached tokens; 404
     claims generated, 187 accepted, audit rejection 51.7 %; quality 5
     requests, 18.2 s, 3,594 prompt tokens. The archive listing (paths,
     sizes, modification times) is the same before and after the run.
  6. Reports and table: pass. Both report manifests name their archive
     path (`~/Archives/AIMediator/reports/20261104-upgrade-baseline/` and
     `…/20261105-upgrade-baseline-samples/`) and `SHA256SUMS`, as well as
     the record, datasets, code version and retention reason. Both
     `SHA256SUMS` files exist. They list 5,323 and 2,693 files, the
     archives' file counts, and `sha256sum -c` passes on both. Every
     module hash in the nine archived run manifests equals the package
     file at HEAD (`src/` is unchanged since `50becc2`). "Live
     evaluations" holds the five U0-L reference rows and the four U0-L2
     sample rows. Their wall times, claim counts, scores and quality
     validity agree with the report summaries, which hold no source text.
- Measurements: tests 250 in 9.1 s (wall 9.4 s); demo 1.06 s plain, 1.9 s
  under cProfile (`evidence.character_reference` 688 calls, 0.66 s); lock
  green.
- Result: accepted, tag `upgrade-u0`. Nothing was adopted or bypassed
  under the owner's standing instruction; no escalation.

### 2026-11-05 U1-V

- Range: `upgrade-u0..2303f99`; 9 commits, all by session U1-1: U1.1
  `43ec4cb`, `678307e`, `1c238ca`; U1.2 `a1c034e`; U1.3 `974b956`; U1.4
  `63145f4`; U1.5 `517194d`; U1.6 `a34ad48`; session log `2303f99`. All
  checks ran on `2303f99` with Python 3.14.8 and NumPy 2.4.6. Temporary
  output went to a scratch directory outside the checkout; the wheel build
  refreshed the ignored `build/`. `runs/`, `reports/`, `data/` and the
  archive were not written, and nothing used the network.
- Checks:
  1. Boundary and commit hygiene (plan 8.8): pass. The boundary check with
     the pattern of work order section 3 prints nothing. The 20 changed
     files are 8 package modules, the two scripts, tests, design/cli.md,
     the guide and this record. Nothing under `src/aimediator/assets/`,
     `data/` or `reports/` changed. The hygiene check prints nothing.
     Subjects use P5 types; U1.4 and U1.5 name UP-D03 and list their lock
     paths; the test-only `1c238ca` is `chore`. No commit message or
     changed file holds attribution or a `/home/` path. Deviation,
     accepted: `1c238ca` (Step U1.1, test only: the runner journal test
     answers the relevance request validly) came after U1.4, so the last
     U1.1 commit does not carry the U1.1 row; the U1.5 row records it.
  2. Lock fixture: pass. Only `63145f4` (U1.4) changes
     `tests/fixtures/behavior-lock.json`. Its diff changes exactly the
     eight keys of work order section 3: `L1:<off|shadow|enforce>/manifest.json`,
     `L2:<off|shadow|enforce>/manifest.json`, `L1:example-report/report.json`
     and `L3:reviewed-report/report.json`. It still has 468 keys, none
     added or removed. Checked independently: at `974b956` (U1.3 done) the
     suite (260) and the lock pass with the U0 fixture, so U1.1 to U1.3 are
     neutral without regeneration. Normalized as the lock does, the demo
     output of `974b956` and HEAD differs only in the four L1 keys. The
     cause is the new identity key `service` (`run_identity.service` in the
     report).
  3. Gates, foreign directory and wheel: pass. 270 tests pass (floor 241;
     20 more than U0: run store 4, character matching 3, stream guards 3,
     service identity 6, context guard 4), and again from a foreign working
     directory. Rule check `Total: 0`; lock green. Installed-wheel
     acceptance: `"passed": true`, `"commands": 18` (as in U0). Every
     module in the wheel equals `src/`, and the wheel holds no `.env` and
     no `data/raw`.
  4. T9, T10 and equivalence tests: pass. Both targets are recorded with
     before and after values (U1.1 and U1.2 rows, U1-1 session log), and
     the U1.2 row states the measurement order of T10. Reproduced here:
     - T9, `run_synthetic_fixture_scale.py --comments 600 --mode shadow`
       (one run per process, 1,236 requests). At `43ec4cb`: 30.9 s plain;
       `run_store.state` 27.97 s of 47.2 s profiled (59.2 %). At HEAD:
       13.8 s plain; 1.01 s of 16.4 s (6.1 %). Target below 5 %: not met.
     - T10, plan 8.4 order. At `678307e`: 0.89 to 0.92 s plain;
       `character_reference` 40.7 to 41.1 %. At HEAD: 0.63 to 0.65 s
       plain; 8.1 to 8.2 %. A profiled demo in a fresh process takes
       1.04 s, with a 14.5 % share (record: 14.8 %). So the share target
       is met in the plan 8.4 order only.
     - The equivalence tests are in the suite and pass:
       `RunStateHarnessTests` (the reduced U1.1 harness) and the listing
       tests in `tests/test_run_store.py`, `tests/test_character_matching.py`
       (U1.2) and `tests/test_stream_guards.py` (U1.3). Their old copies
       equal the functions at `678307e` and `a1c034e` by AST comparison;
       `character_candidates` differs only by calling the unchanged
       `evidence.character_terms` through the module.
     - Beyond the item: the 600-comment runs of `43ec4cb` and HEAD,
       normalized as the lock does, differ only in `manifest.json` (the
       `service` key). The other 89 keys are equal, including every
       request digest and `run-state.json`.
     - Also beyond the item: the U1.6 check was rerun by hand on a
       relevance-only legacy fixture run. The script at HEAD exits 0
       (`verified_requests` 6, 38 admission decisions unchanged, no
       inference). The script at `upgrade-u0` stops with `RuntimeError:
       Replay cannot run inference`.
  5. Resume with another service version: pass.
     `test_resume_refuses_a_changed_service_version` in
     `tests/test_service_identity.py` resumes with `0.35.0` and with
     `null`. Each time it asserts `Failure(4, 'Service version differs
     from saved run; start a new run')`, no transport call and no changed
     file; a resume with the saved version then completes. Manual check
     through `cli.main` after `aimediator demo`: `analyze --resume
     <demo>/shadow --json`, with `FixtureTransport.version` patched to
     `0.35.0` and to `None`, exits 4 (`identity_or_output_conflict`) and
     leaves every file unchanged. Unpatched, it exits 0.
- Points U1-1 raised, judged against the step notes and plan 4.6 and 4.7.
  All four are accepted with no fix-up step:
  - U1.1 differs from its step note in three places. (1) A new run
    starts with an empty index: its folder is new, so a listing would find
    nothing. (2) `load_resume` drops the folder's index, so a resume reads
    the disk even within one process. (3) A `state` write with status
    `interrupted` or `failed` lists again, because an interruption can
    fall between a `validation.json` write and its journal call. Each one
    serves the contract on `run-state.json` content, which the note puts
    first. They change only when listings happen, never the content
    written, so plan 4.6 holds. `Runner._generate` is the only writer of
    `validation.json`, and the only `Runner` that `operations.analyze`
    builds passes the journal. The deviations are documented in
    design/cli.md section 5.
  - U1.3 resumes each scan at the end of its last match, not at the tail
    plus an overlap of the longest allowed key. The docstring's argument
    holds for all three patterns: a match attempt that reaches the end of
    the output leaves no later complete match, and a lookbehind still sees
    text before the scan position. An overlap of the longest key would not
    bound `\s*` or a `comment_id` value. The equivalence tests pass.
  - D-6 (a structural copy instead of `copy.deepcopy`). The cached value
    is built from `json.loads` data by comprehensions. Its leaves are
    immutable and no container is shared, so both copies give equal
    values and new containers at every level. It is N-class and within
    plan rule 1.8.
  - T9 and T10. The plan 5.5 targets are not gates. Both are recorded
    with before and after values, and the measurement order of T10 is
    stated. T9 stays above target (6.1 %). The rest of its share is the
    read and write of `run-state.json`, which the N-class contract keeps
    unchanged.
- Other findings, none blocking. `tests/test_service_identity.py` leaves
  two `HTTPError` objects unclosed, which adds two `ResourceWarning` lines
  (HTTP 404 and 500) to the test output. `/api/version` was not called on
  the owner's service, since U1 has no live session; the U0.6 record holds
  Ollama 0.34.2, read from that endpoint.
- Measurements: tests 270 in 12.3 s (wall 12.6 s); demo 0.65 s plain,
  1.0 s under cProfile (`evidence.character_reference` 688 calls,
  0.079 s); lock green.
- Result: accepted, tag `upgrade-u1`. Nothing was adopted or bypassed
  under the owner's standing instruction; no escalation.

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

### 2026-11-05 U0-L2 (live)

- Steps: U0.8 done; none started and stashed.
- State: HEAD is this entry's commit (parent `8255249`); tests 250; lock
  green; rule check 0. The four sample runs ran at `0abfe02`; the commits
  since add only the curated report and change the change record.
- Findings: the first U0-L2 agent checked the environment, materialized
  the samples and ran the four runs (2026-11-04 23:19 to 2026-11-05 00:19,
  each `partial`, exit 5, like U0.6), and was stopped after the runs and
  before it recorded anything; a second agent verified its environment
  check, inputs and code identity, did not rerun the runs, regenerated
  every measurement and the comparison, and finished the step. Decision
  found during execution D-5 (comparison rule); no escalation; nothing
  adopted or bypassed under the owner's standing instruction. The
  extraction sample scores higher than the full split (precision 68.2 %
  against 55.6 %, paired 64.5 %), so the T7 target on the sample is
  78.2 %; benchmark precision depends on one comment with 1 to 12
  identical accepted claims; one `generation_failed` comment after
  `duplicate_claim_loop` on the extraction sample (U0.6: none); smaller
  extraction batches on the extraction sample; verify, audit and
  admission differences that follow the claim set and the batch
  composition. The sample runs took 60 minutes against 114 for the U0.6
  equivalents.
- Next: U0-V (verification, fresh session); then U1 (work order U1);
  blockers: none.

### 2026-11-05 U0-V (verification)

- Steps: none (verification); none started and stashed.
- State: HEAD is this entry's commit (parent `c587115`), tagged
  `upgrade-u0`; tests 250; lock green; rule check 0.
- Findings: every checklist item passes (see "Verification notes"); no
  decision found during execution; nothing adopted or bypassed under the
  owner's standing instruction; no escalation.
- Next: U1-1 (implementation, work order U1, steps U1.1 to U1.6);
  blockers: none.

### 2026-11-05 U1-1 (implementation)

- Steps: U1.1, U1.2, U1.3, U1.4, U1.5, U1.6 done; none started and stashed.
- State: HEAD is this entry's commit (parent `a34ad48`); tests 270; lock
  updated by UP-D03 (U1.4, exactly the eight keys of work order section
  3; 468 keys), green since; rule check 0. Foreign working directory: 270
  pass. Installed-wheel acceptance: `"passed": true`, `"commands": 18`.
- Findings: decision found during execution D-6 (a structural copy
  instead of `copy.deepcopy` for the memoized character reference); no
  escalation, because no trigger of work order section 6 occurred:
  `run-state.json` equalled a full scan at all 3,295 harness writes, the
  equivalence tests of U1.2 and U1.3 found no difference, U1.4 changed
  only the eight lock keys, and `/api/version` answered as plan 4.7
  expects in the U0.6 record (no live call in this session); nothing
  adopted or bypassed under the owner's standing instruction. T9 not met:
  `run_store.state` takes 5.4 % of the profiled 600-comment fixture run
  at U1.1 and 6.1 % at `a34ad48` (from 59.4 %; target below 5 %), because
  the rest of the run got faster too; what remains is the read and
  write of `run-state.json`, whose completed-identity list grows with
  the run and is frozen content. The run takes 13.4 s plain at
  `a34ad48` (31.1 s before U1.1). T10 met: demo 0.63 s plain,
  `character_reference` 8.1 % of the profiled demo at `a34ad48`. Stream
  guards at 7,495 chunks: 8.55 s before, 0.097 s after. The scratch
  harness and the measurement and check scripts are not committed.
- Next: U1-V (verification, fresh session, work order U1 section 4);
  blockers: none.

### 2026-11-05 U1-V (verification)

- Steps: none (verification); none started and stashed.
- State: HEAD is this entry's commit (parent `2303f99`), tagged
  `upgrade-u1`; tests 270; lock green; rule check 0.
- Findings: every checklist item passes (see "Verification notes"). The
  four points U1-1 raised are accepted: the U1.1 index deviations, the
  U1.3 scan resumption, D-6, and T9 missed (6.1 %) while T10 is met in
  the plan 8.4 order. No decision found during execution; nothing adopted
  or bypassed under the owner's standing instruction; no escalation.
- Next: U2-1 (implementation, work order U2, steps U2.1 to U2.4);
  blockers: none.

### 2026-11-05 U2-1 (implementation)

- Steps: U2.1, U2.2, U2.3, U2.4 done; none started and stashed.
- State: HEAD is this entry's commit (parent `b7d1cc5`); tests 280; lock
  updated by UP-D04 (U2.2, 25 keys), UP-D05 (U2.3, 12 keys) and UP-D07
  (U2.4, 38 keys), 468 keys, green after each step; U2.1 left it
  unchanged; rule check 0. Foreign working directory: 280 pass.
  Installed-wheel acceptance: `"passed": true`, `"commands": 18`.
  Boundary and hygiene checks of plan 8.8 from `upgrade-u1` print
  nothing.
- Findings: decision found during execution D-7 (the replay script takes
  the prompts as runs send them, so it replays runs made after U2.4 and
  still refuses older ones). The deferred D-4 item (relevance and route
  agreement in `measurement`) is bypassed under the owner's standing
  instruction, because its recommended action needs an owner amendment of
  the U2 boundary; U2-L1 and U2-L2 keep the one-off scorer
  `runs/upgrade/tools/score_u0_extra.py` (see "Deferred"). Nothing
  adopted under the standing instruction. No escalation: no trigger of
  work order section 6 occurred; no view needed a change to a gate, a
  schema or the verify request (`format` and `response_schema` are
  unchanged in every step), and `FixtureTransport` answers every view
  unchanged. Quality attempt 2 now differs from attempt 1 by
  `previous_attempt_errors` and by its `request_context`; the two quality
  experiment scripts build their attempts with `pipeline.quality_request`,
  because without the request context they would have replayed attempt 1
  as attempt 2. No live run in this session.
- Next: U2-L1 (live, work order U2 section 4), whose runs measure the
  code of `b7d1cc5` (the U2.4 commit; the commits after it change only
  this record), against the U0.8 sample rows and the U0.6 silver row;
  then U2-2 (implementation, U2.5 and U2.6); blockers: none.

### 2026-11-05 U2-L0 (live)

- Steps: U2-L0 done; none started and stashed.
- State: HEAD is this entry's commit (parent `79cfbb5`); tests 280; lock
  green; rule check 0. The five runs ran at `0abfe02` through bridge
  version 1; this session started no run.
- Findings: the runs were launched by the orchestrating session
  (`u2l0_api_runs.sh`) and had finished before this session measured
  them; identity checks passed for all five, nothing rerun. Bridge
  version 2 replaced version 1 after the runs (UP-D20); both are recorded
  under "API environment (U2-L0, UP-D19)". The source of version 1 is not
  kept (overwritten by version 2 while version 1 ran). Uncached token
  counts follow the provider's shared prompt cache, so they depend on run
  order and on the parallel chains. The hosted model is faster and scores
  higher than the local models on every measured metric. No escalation;
  nothing adopted or bypassed under the owner's standing instruction.
  Spend 0.1082 USD for the ten runs of U2-L0 and U2-L1.
- Next: U2-L1 (live), in this agent; blockers: none.

### 2026-11-05 U2-L1 (live)

- Steps: U2-L1 done; U2.5 and U2-L2 skipped (UP-D20); none started and
  stashed.
- State: HEAD is this entry's commit (parent `e6c7917`); tests 280; lock
  green; rule check 0. The five runs ran at the code of `b7d1cc5` through
  bridge version 1; this session started no run.
- Findings: identity checks passed for all five runs, nothing rerun.
  Verdicts under the adoption rule (D-8, U2-L0 reference): U2.2 kept,
  U2.3 fails rule 4 on recall (−4.9 points), U2.4 kept; escalation E-3
  records U2.3 for the owner's review, nothing reverted. T2 met; T1 and
  T3 not met. `compare_u2l1.py` now takes the reference runs as an option
  (U2-L0 by default) and counts verify `original_evidence` as comment
  text in the budgets. The local runs `u2l1-local-*` are archived and
  decide nothing. No API spend in this session beyond the ten runs
  recorded under U2-L0.
- Next: U2.6 (step of session U2-2), in this agent; then U2-V
  (verification); blockers: none.

### 2026-11-05 U2-2 (implementation)

- Steps: U2.6 done; U2.5 skipped (UP-D20); none started and stashed.
- State: HEAD is this entry's commit (parent `cd3fd48`); tests 285; lock
  green, unchanged (468 keys); rule check 0. Foreign working directory:
  285 pass. Installed-wheel acceptance: `"passed": true`, 18 commands.
- Findings: the budgets are those of the U2-L1 runs plus 20 %; the demo's
  largest quality request (4,784 non-comment characters) exceeds the live
  maximum (4,740) and stays within its budget. Boundary check of plan 8.8
  from `upgrade-u1`: outside the pattern of work order section 3 are
  `reports/20261105-upgrade-api-reference/` (the U2-L0 report, which the
  UP-D19 note of the work order names), `docs/plans/` and the U2 handoff
  (UP-D19 and UP-D20, committed by the orchestrating session) and
  `scripts/maintenance/` (E-2); the commit hygiene check prints nothing.
  `.gitignore` tracks only `manifest.json` and `summary/` under
  `reports/`, so the `provenance/` lists of the U2-L0 and U2-L1 manifests
  name files kept in each archive's `provenance/` (every SHA-256 checked
  against the manifest) and in the ignored local report directory, as the
  earlier reports keep theirs. No escalation in this session beyond E-3
  of U2-L1; nothing adopted or bypassed under the owner's standing
  instruction.
- Next: U2-V (verification, fresh session; work order U2 section 4),
  which carries E-3 to the review of batch U2; then U3 (work order U3);
  blockers: none.

## Deferred

- **Relevance and route agreement in `measurement`** (D-4, from U0.6). Add
  the relevance agreement of `balance-silver-v1` and the route agreement of
  `evidence-quality-synthetic-v1`, with tests, to `aimediator.measurement`
  before U2-L1, so the L sessions of U2 compute them with committed code
  and the rule of D-4. The U2 boundary does not list `measurement.py`; the
  owner decides whether the U2 work order adds it or U2-L reuses the
  archived one-off scorer.

  **Bypassed** by session U2-1 on 2026-11-05 under the owner's standing
  instruction of 2026-11-04 (item 2). Question: does the U2 work order add
  `src/aimediator/measurement.py` to its boundary so that a U2
  implementation session moves both functions into the package before
  U2-L1, or do U2-L1 and U2-L2 reuse the one-off scorer? Options: (a)
  amend the U2 boundary and move them, with tests (the recommendation of
  D-4); (b) U2-L1 and U2-L2 run the one-off scorer
  `runs/upgrade/tools/score_u0_extra.py` (the D-4 rule; archived as
  `provenance/score_u0_extra.py` of the U0.6 and U0.8 reports). Why it
  could not be decided: the recommended action needs an amendment of the
  work order's boundary, which only the owner makes; a session does not
  widen its own boundary. Kept: the current state, (b). The U2 live
  sessions compute relevance agreement and route agreement with the same
  code and rule that produced the U0.6 and U0.8 references, so the paired
  comparisons stay like for like; their reports keep a copy under
  `provenance/`. Skipped: the move into `aimediator.measurement` before
  U2-L1; the item stays open here. The U3 boundary lists `measurement.py`,
  so the owner can assign the move to U3. No step of U2-1 depends on it.
