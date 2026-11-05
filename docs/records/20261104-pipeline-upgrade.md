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
| U3.4 | B | done | 296 | updated by UP-D09 | LAT-06, UP-D09, plan 4.6. `retrieval.retrieve` writes one record per text, `embeddings/<SHA-256 of model, endpoint and text>.json` (`text_identity`; the endpoint is the configured embedding URL or the service base) with `model`, `text` and `vector`; it embeds only texts without a record, each distinct text once, in batches of 32 (`BATCH`, was 8 texts per file) in input order, then scores as before; `retrieval.json` keeps its schema and, in the fixture runs, its bytes. The shared cache (`retrieve(..., shared_cache, model_digest)`, passed by `operations.analyze` with the run identity's embedding digest) supplies records under `embedding/<key[:2]>/<key>.json`, `embedding_key` = SHA-256 of model, endpoint, text and model digest, before the service is asked, and keeps new ones. The availability probe of `analyze` (one text) is unchanged. Tests: `tests/test_shared_cache.py` (+1): 50 comments with 40 distinct texts and the 20 anchors give two calls of 32 and 28 texts in input order and 60 records; a rerun in the same folder and a run in a new folder with the shared cache make no call and return the same decisions; another digest misses; the warm fixture run of U3.3 makes no retrieval embedding call. `test_console_output` expects `Embedding 32/58` and `58/58`; `test_balanced_collection` one configured-embedding call for 21 texts. Lock regenerated: only `embeddings/` keys of `L1` and `L2` in three modes, 8 batch files out and 58 text records in per run (771 keys); no request, retrieval or other artifact changed. design/cli.md sections 5 and 7 |
| U3-L | L | done | 296 | green | UP-D08, UP-D09, UP-D19, UP-D20. The four runs of the work order at the U3.4 commit `1a5d520` on the `latency-benchmark` sample in `shadow` through bridge `openrouter-bridge-2` (SHA-256, digests and `live-config-api.json` equal to the record; `doctor` passed; every request `ok` from `deepseek/deepseek-v4-flash` and `qwen/qwen3-embedding-8b` on DeepInfra), started by this session in its own process session, one after another: `u3-benchmark-shadow-p1` (N 1, cold `cache-1`), `-warm` (N 1, `cache-1`), `-p2` (N 2, cold `cache-2`), `-p4` (N 4, cold `cache-3`; it runs under UP-D19). The warm run made no chat and no retrieval embedding request and reproduced run 1 exactly; retrieval at batch 32 against `u2l0-benchmark-shadow` (batch 8): no decision changed. T8 (indicative): 1.25 times, not met. See "U3-L" under "Live evaluations"; the owner action on the value for later live runs is D-10. Curated report `reports/20261105-upgrade-u3-evaluation/`; full runs with their caches archived with `SHA256SUMS` (2,257 files). Spend of the doctor call and the four runs 0.0288 USD (0.1198 to 0.1486 USD) |
| U3.5 | N | done | 296 | green | ADR `docs/decisions/0004-bounded-concurrency-and-shared-cache.md` (context, the four decisions of U3.1 to U3.4, the U3-L measurements, consequences: serial bytes at the defaults, reproducibility of plan 2.3, reuse provenance, cache growth and content, `cache_dir` in the run identity, no concurrent runs on one cache directory) with its index row in `docs/README.md`; design/cli.md section 6 (the measured gain, the concurrent-run limit) and section 7 (exact replay as measured, per-text embedding records); guide (the measured gain, cache content, embedding reuse beyond the probe, reproducibility, concurrent runs). Lock unchanged (771 keys). Foreign working directory: 296 pass. Installed-wheel acceptance at `1a5d520`: `"passed": true`, 18 commands (the documents changed since) |
| U4.1 | N | done | 301 | green | ALG-01, plan 4.2. `evidence.clause_segments(units)` (version constant `SEGMENTATION_VERSION` `clause-v1`): each unit splits after a run of `,` `;` `:` `，` `；` `：` `、` together with the combining marks that follow it (so a mark never leaves its base), unless the characters before and after the run are both decimal digits (`isdecimal`, as `\d`); punctuation stays left, segment edges are stripped of whitespace, a unit without a split point is one segment. Segments `{segment_id E<n>.<k>, evidence_id, text, start, end}` with absolute code-point offsets and `text == original[start:end]`. New `tests/test_clause_segments.py` (+5): the partition properties (ordered, disjoint, inside the unit, stripped, consecutive IDs, every non-whitespace character covered) over the 350 `text_original` values of the tracked evaluation sets and the 38 fixture texts; split points in English and Chinese, punctuation runs and a leading comma; `1,000`, `1.5x`, `1:30`, full-width `５，０００`, `2MP,2HP`; mixed scripts, an emoji with a skin-tone modifier, a combining acute accent before and after a comma, CRLF line ends with absolute offsets; empty, whitespace-only and punctuation-only units. Not used by the pipeline yet; lock unchanged |
| U4.2 | N | done | 303 | green | Plan 4.2 fixture check. New `tests/test_fixture_clause_mapping.py` (+2): all 38 fixture annotations map: each of the 124 v1 segments is a union of whole clause segments (138 clauses in all), no clause crosses a v1 segment edge, every clause belongs to exactly one v1 segment and takes its four labels, and each point's clause set is the union of its v1 segments' clauses; a crossing clause and leftover text do not map. No escalation (work order section 6, first trigger): `FixtureTransport` derives v2 answers from this mapping in U4.4. Lock unchanged |
| U4.3 | N | done | 310 | green | ALG-01, ALG-02, plan 4.2; not used by the pipeline yet. In `evidence_quality`: `character_literals(text)` (the canonical names, Chinese labels and permitted aliases of `character_reference(text)` as the text writes them, Latin terms by the whole-word, case-free pattern of `term_matches` (`balance_policy._term_pattern`), by first occurrence, longer first); `annotation_schema_v2(comment_id, segments, literals)` with `quality_obj` objects in the order `comment_id`, `segment_labels` (one required key per segment ID, each `scope`, `content_kind`, `emotional_tone`, `reason_code`), `information_points` (the v1 point order; `segment_ids` limited to the segment IDs, `minItems` 1, `uniqueItems`; `character_literal` an enum of `null` and the literals; `mechanic_literal` nullable nonempty string); `to_v1_annotation(annotation, segments, text)` (one v1 segment per clause with program offsets and quotes, clause IDs as v1 segment IDs, points unchanged); `validate_annotation_v2(annotation, row, segments, units, literals=None)`: the v2 schema, then the unchanged `validate_annotation` on the conversion, so a valid v2 annotation always converts into a valid v1 annotation (work order section 6, third trigger, by construction) and the mechanic literal is checked inside the selected segments. `fixture_transport.v2_annotation(annotation, text)` derives the v2 answer of a v1 fixture annotation from the U4.2 mapping (used by the transport in U4.4). New `tests/test_quality_v2.py` (+7): the serialized schema pinned as in `tests/test_schema.py`; literals; a valid annotation, its v1 offsets, quotes and key order, routed by `qualify`; missing, extra and out-of-enum labels, offsets in the answer, a foreign comment ID, duplicate points; foreign and repeated segment IDs; character and mechanic literals outside the selected segments and an unknown literal; the round trip v2 → v1 → `qualify` on the 38 fixture cases (same status, routes present, expected routes, point routes and reasons, fragment routes, emotion measurement and point counts as the v1 annotations). Lock unchanged |
| U4.4 | B | done | 310 | updated by UP-D10 | ALG-01, plan 4.1 and 4.2. `pipeline.quality_request` adds the context keys `segments` (`evidence.clause_segments(units)`) and `character_literals` (`evidence_quality.character_literals`) and no longer holds the character reference; `stages.view` sends the quality view v2 (`MODEL_VISIBLE['quality']` follows); `schema_for('quality', ids, data)` builds `annotation_schema_v2` from the context; `normalize` validates v2 (`validate_annotation_v2`, which runs the v1 rules on the conversion); `assess_quality` routes with the new `evidence_quality.qualify_v2` (the unchanged `qualify` on `to_v1_annotation`), and the record keeps `annotation` (the derived v1 annotation, so routing and readers stay) and `annotation_v2` right after it (`null` in failed v2 records, `failed_record`). Policy in place: `evidence-quality-policy-v2`, `evidence-quality-v2`, `segmentation_version` `clause-v1`; `load_policy` checks the three. Prompt pair `evidence-quality.{en,zh}` rewritten for labeling given segments (two authored synthetic examples per language, each valid under `validate_annotation_v2` and routed as intended); `quality-extract` and `quality-verify` unchanged (see "Behavior changes"). `FixtureTransport` answers v2 with `v2_annotation` (the U4.2 mapping). `design_briefs.quality_design_errors` accepts both schema versions (D-11, part 2). Scripts `diagnose_evidence_quality_live.py` and `run_quality_screening_experiment.py` route with `qualify_v2`. Tests: the mock transports of `test_cli_product`, `test_context_guard`, `test_evidence_quality` and `test_request_views` answer v2; `test_stages` normalizes v2; `test_request_views` checks the v2 view (no offsets, quotes or reference entries); `test_request_payload` counts segment texts as comment texts and adds the per-segment schema part to the quality budget (D-11, part 1); `test_console_output` pins the legacy `enforce` extraction batches of `qwen2.5:7b` as 3, 4, 1, 1 (was 4, 4, 1): batches are sized on the context, whose routing entries now hold clause segments; routes, claims and summaries of the fixture runs are unchanged (the two `injection` cases add one `exclude` fragment each). Lock regenerated (771 keys): exactly the 100 keys under "Behavior changes". Design documents follow in U4.7 (work order) |
| U4.5 | B | done | 316 | green | Plan 4.2, UP-D10. New `evidence_quality.stored_annotation_errors(record, row, units)` dispatches on the record's `schema_version`: `evidence-quality-v1` (and records without a version) keep `validate_annotation` on `annotation`; `evidence-quality-v2` records are validated by `validate_annotation_v2` on `annotation_v2` against `clause_segments(units)`, and `to_v1_annotation` of it must equal the stored `annotation`; any other version is refused (`SCHEMA_VERSIONS`). `review.load_run` uses it before the unchanged routing recomputation, so `evaluation.evaluate_quality` (which reads through `load_run`) follows. `quality_scoring.evaluate` refuses unknown versions and reads the v1-shaped annotation and routing that both versions hold. `legacy_review.apply_review` refuses a qualification of unknown version (`Review cannot bypass evidence quality: unknown schema version`) and binds v1 and v2 qualifications alike. `design_briefs.quality_design_errors` accepts both since U4.4 (D-11). New `tests/test_quality_readers.py` (+6): the v2 demo `enforce` run (every record `evidence-quality-v2`, `annotation_v2` after `annotation`) passes `load_run`, review export, review import and report; tampered v2 records (a label, the derived annotation, a missing `annotation_v2`, an unknown version) fail `load_run` with exit 2; a run folder whose quality records are v1 records built by `qualify` from the v1 fixture annotations under the v1 policy (the demo `shadow` run, whose claims are not bound to quality points) passes `load_run`, review and report, and fails with a tampered quote; `quality_scoring.evaluate` gives equal scores for v1 and v2 versions of the records and refuses an unknown one; design briefs and `apply_review` accept both versions and refuse an unknown one; the dispatch itself. The behavior lock passes unchanged (771 keys): no artifact of the fixture runs changes. Checking out older code is left to checklist item 4 of U4-V |
| U4-L | L | done | 316 | green | UP-D10, UP-D18, UP-D19, UP-D20. The two runs that UP-D18 keeps (`u4-benchmark-shadow`, `u4-quality-synthetic-shadow`) at the U4.5 commit `2614453` through bridge `openrouter-bridge-2` (SHA-256, digests and `live-config-api.json` equal to the record; `doctor` passed; every response from `deepseek/deepseek-v4-flash` on DeepInfra), started by this session in its own process session; reference the U2-L1 rows (U2.2 kept). Measured and scored with the committed tools and the D-4 route scorer; compared in `u4l_analyze.py`. Verdict: U4.4 and U4.5 fail rules 2 (benchmark quality-failed comments 4 against 2) and 3 (T5 18/23 against 21/24); rule 4 holds (synthetic validity 16/16 against 13/16, route agreement 14/16 against 11/16); T4 11.2 s per comment, 60.4 % of the reference (indicative; target not met); escalation E-4, not reverted. Largest prompt plus output 14,346 tokens (U4.6). See "U4-L" under "Live evaluations". Curated report `reports/20261105-upgrade-u4-evaluation/`; full runs archived with `SHA256SUMS` (721 files). Spend of `doctor` and the two runs 0.0179 USD (0.1486 to 0.1665 USD) |
| U4.6 | B | skipped | 316 | green | LAT-07, UP-D10, conditional on every U4-L quality request having prompt plus output below 6,000 tokens. Measured from the API counters (`prompt_eval_count` plus `eval_count` of every quality `response.json`): maximum 13,520 on the benchmark (11,453 prompt, 2,067 output) and 14,346 on the synthetic sample (12,260 and 2,086); 4 and 1 requests reach 6,000 or more. The policy's `num_ctx` stays 16384; no lock change. The prompt growth is the per-clause label schema (D-11) |
| U4.7 | N | done | 316 | green | ADR `docs/decisions/0005-program-segmentation-of-quality-annotations.md` (context with the U2-L1 and U0.6 failure classes, the five decisions of U4.1 to U4.5, the U4-L measurements against U2-L1 and the E-4 outcome, consequences: no offset errors, clause granularity, schema growth (D-11), policy v2 in the run identity, fixture batches, the legacy identity hash) with its index row in `docs/README.md`; evidence-quality.md (header; sections 3.1 and 3.2 marked as v1, new section 3.3 with the v2 contract: segmentation, request, schema, validation and routing, records and readers, granularity, fixtures; section 4 holds for both versions on the derived annotation); emotion-quantification-and-evidence-isolation.md (header; section 3 on v2 labeling and the program's offsets); design/cli.md section 5 (`evidence.clause_segments`, the v2 quality view, `quality_request` context, v2 `schema_for` and `normalize`, `qualify_v2`, the readers of both versions). Lock unchanged |
| U4.F1 | B | done | 316 | updated by UP-D10 | Fix-up step of E-4, option (c), adopted under the owner authorization of 2026-11-05 03:11. Prompt pair `evidence-quality.{en,zh}`: one addition to the labeling paragraph aimed at the remaining U4-L failure class (a concrete point selecting a clause labeled `general_opinion`, 7 of 9 benchmark attempt errors) and at a literal outside the selected clauses (2 of 9); see "Behavior changes". The authored examples are unchanged and still valid under `validate_annotation_v2`. No code, schema, policy or routing change. Lock regenerated: exactly the 25 keys under "Behavior changes" (the keys of the U2.2 prompt change). Measured by U4-L2 |
| U4-L2 | L | done | 316 | green | E-4 option (c), UP-D19, UP-D20, D-12. The two U4-L runs repeated at the U4.F1 commit `385f744` (`u4f1-benchmark-shadow`, `u4f1-quality-synthetic-shadow`) through bridge version 2, environment and identity equal to the record. Verdict: rule 2 still fails (benchmark quality-failed comments 5 against 2), T5 78.3 % unchanged, T4 11.0 s per comment (59.5 %), rule 4 holds (synthetic 15/16, routes 14/16 against 13/16 and 11/16); the fallback (a) of E-4 applies and passes to U4-V (revert U4.F1, U4.5, U4.4). See "U4-L2" under "Live evaluations". No `reports/` directory (D-12); full runs, measurements and comparison archived with `SHA256SUMS` (726 files). Spend 0.0186 USD (0.1665 to 0.1851 USD) |
| U2-R | L | done | 316 | green | E-3 option (c), UP-D19, UP-D20, D-8; run by session U5 (UP-D20, chain session 4) before U5.1. `u2r-extraction-development-off`: the extraction-development sample in `off` at the code of `39a1efd` (the U2.3 commit; U2.2 sends no request in `off`, U2.4 not applied), extracted with `git archive` into `runs/upgrade/code-39a1efd/src` and first on `sys.path`, through bridge `openrouter-bridge-2` (SHA-256, digests and `live-config-api.json` equal to the record; `doctor` passed; 30 module hashes equal to `39a1efd`; input equal to the reference; all 176 chat attempts from `deepseek/deepseek-v4-flash` on DeepInfra). Against `u2l0-extraction-development-off` as D-8 reads rule 4 for U2.3: precision of accepted claims 60/79 (75.9 %) against 61/80 (76.2 %), −0.3 points (Newcombe −13.5 to +12.9); recall 59/123 (48.0 %) against 60/123 (48.8 %), −0.8 points (−13.1 to +11.5); rule 2 0 against 0 technical failures, coverage complete. U2.3 alone holds rule 4; E-3 decided as (b) on the evidence of (c): U2.3 kept, adopted under the owner authorization of 2026-11-05 03:11. See "U2-R" under "Live evaluations". Spend 0.0255 USD (0.1851 to 0.2105 USD) |
| U5.1 | B | done | 318 | updated by UP-D11 | PRM-02, plan 4.3. `evidence.CLAIM` in the evidence-first order `evidence_ids`, `character`, `target`, `direction`, `recommendation`, `specificity`, `parameters`, `uncertain`; `stages.schema_for('extract', ...)` keeps it when it narrows properties (reassigned keys keep their place) and appends `quality_point_ids` last. `inference.claim_key(assessment_schema)` returns the first property of the claim items under `properties[<comment ID>].properties.claims.items.properties` of the request's `format` (None without claim items), and the loop guard of `streamed_chat` and `repeated_claim(output, allowed_ids, first_key)` find claim objects by that key instead of the literal `"character"`; `inference` does not import `evidence`. `proposal_hash` sorts keys: review export and import of the demo runs pass (`test_quality_readers`, `test_cli_product`). Tests (+2, `tests/test_stream_guards.py`): the U1.3 equivalence streams carry a schema whose claims start with `character` and still equal the copies of `a1c034e`; `claim_key` on the U5.1 schema, the old order, comments without claim items and array schemas; evidence-first streams (normal, a duplicate claim, late and early loops of 8 claims, the same claim under two comments) at chunk sizes 1, 4, 9 and whole: the new guard stops every claim loop (`duplicate_claim_loop`, on a prefix of the same output) where the old copy, keyed on `character`, does not. Lock regenerated (771 keys): exactly the 18 extraction request keys under "Behavior changes"; no artifact changed (fixture claims keep their own key order). Design documents follow in U5.4 (work order) |
| U5-L1 | L | done | 318 | green | UP-D11, UP-D18, UP-D19, UP-D20, D-13. `u5l1-extraction-development-off`: the extraction-development sample in `off` at the U5.1 commit `e64701d` (a `git archive` copy first on `sys.path`) through bridge `openrouter-bridge-2` (identity check passed: 30 module hashes, digests, bridge and configuration hashes equal to the record, `doctor` passed, all 182 chat attempts from `deepseek/deepseek-v4-flash` on DeepInfra). Reference `u2l1-extraction-development-off` (E-3 kept U2.3). Verdict (D-13): U5.1 passes and is kept: 0 technical failures against 0, coverage complete; precision of accepted claims 58/77 (75.3 %) against 55/74 (74.3 %), +1.0 points (Newcombe −12.7 to +14.7); recall 58/123 (47.2 %) against 54/123 (43.9 %), +3.3 points; T6 40/119 (33.6 %) against 53/129 (41.1 %). The entry rerun `u5r-extraction-development-off` (code of `e34e08d`, decides nothing) gives 55/73 and 54/123: against it U5.1 adds 0.0 points of precision and +3.3 of recall. See "U5-L1" under "Live evaluations". Spend of both runs 0.0482 USD (0.2105 to 0.2587 USD); the report follows with U5-L3 (D-13) |
| U5.2 | B | done | 324 | updated by UP-D11 | PRM-03, plan 4.3. Each comment's extraction schema is `{subjects, claims}`, `subjects` first: an array of the comment's allowed characters (the enum of the claim `character`) with `uniqueItems` and `maxItems` the number of allowed characters (beyond the work order: a bound that holds where a provider drops `uniqueItems`, as the bridge does), `maxItems` 0 when no character is allowed; without request data an array of strings with `uniqueItems`. `stages.normalize` keeps `subjects` in each assessment; `pipeline.extract_claims` adds the source-binding error `Claim character not declared as subject` to a claim whose character is not in its comment's `subjects` (after the grounding errors; nothing removed or relaxed). `FixtureTransport` fills `subjects` with the characters of its claims in first-occurrence order. Prompt pair `summarize-balance.{en,zh}`: every comment carries subjects and claims, and two sentences define `subjects` (the supplied fighters whose balance the author takes a position on, each claim's character among them; a mention, comparison, victim or cosmetic remark does not make a subject); see "Behavior changes". `quality-extract` unchanged. New `tests/test_subjects.py` (+6): schema order, enum, bounds and the bare schema; repeated, unknown, missing and forbidden subjects refused; `normalize` keeps them; the loop guards inside `{subjects, claims}` (duplicate claim, duplicate comment key, the same claim under two comments); fixture runs in `off` and `enforce` whose subjects equal their claims' characters and trip no gate; a fixture answer with one subject removed quarantines exactly that comment's claims of that character at source binding. Mock transports of five test files answer with `subjects`. Lock regenerated (771 keys): exactly the 50 keys under "Behavior changes". Design documents follow in U5.4 |
| U5-L2 | L | done | 324 | green | UP-D11, UP-D18, UP-D19, UP-D20, D-13. `u5l2-extraction-development-off` at the U5.2 commit `30d41be` (a `git archive` copy first on `sys.path`) through bridge version 2 (identity check passed; all 191 chat attempts from `deepseek/deepseek-v4-flash` on DeepInfra). Reference `u5l1-extraction-development-off` (U5.1 passed). Verdict (D-13): U5.2 **fails rule 3**: precision of accepted claims 61/81 (75.3 %) against 58/77 (75.3 %), −0.02 points (Newcombe −13.3 to +13.4), not above the reference; rules 2 (0 against 0 technical failures, coverage complete) and 4 (precision −0.0, recall 60/123 against 58/123, +1.6 points) hold. The subjects gate quarantined no claim. Escalation E-5; not reverted (the session's instruction: a failed step stays for the review). See "U5-L2" under "Live evaluations". Spend 0.0253 USD (0.2587 to 0.2841 USD) |
| U5.3 | B | done | 326 | updated by UP-D11 | PRM-04, PRM-01, plan 4.3. Authored synthetic examples at the end of the prompt pair `summarize-balance.{en,zh}`, headed as authored for the prompt and not real comments, each one line of input units (`E1 "..." E2 "..."`) and one line with the expected entry of `assessments` in the U5.1 and U5.2 shape: English 3 (a long pros-and-cons review that only mentions Ken and Marisa: empty `subjects` and `claims`; a conditional threat on Guile's Sonic Boom: `nerf`; a system complaint next to Luke's name: empty), Chinese 5 (the same three, an ironic remark on Manon: `unclear` with `uncertain` true, and a general complaint on Luke: a qualitative `nerf`). Example sizes in characters: English 214, 310, 142; Chinese 107, 238, 66, 247, 224 (all under 400). Prompt sizes in characters: English 3,480 to 4,271, Chinese 1,330 to 2,268 (UTF-8 bytes 3,480 to 4,271 and 3,178 to 4,498); in `enforce` `quality-extract` still follows them. No example text comes from an evaluation set: every text was written for the prompt; the first 30 characters of none of the 227 development comments of `extraction-precision-v1` occur in the new example lines (the one development comment found in the prompt, the 4-character `加强曼侬`, matches the recommendation line `加强曼侬。` that predates U5; the test split was not read; checklist item 5 of U5-V). New `tests/test_prompt_examples.py` (+2): the examples are last, marked and under 400 characters (3 and 5); each example's units equal `evidence_units` of its own text, its expected entry is valid under `schema_for('extract', ...)` built for that text, every claim's character is a declared subject, and the directions and `uncertain` values are those listed above. Lock regenerated (771 keys): exactly the 32 keys under "Behavior changes" (prompt assets and snapshots, manifests and the two reports through the prompt hashes, extraction request digests); no response or other artifact changed. Design documents follow in U5.4 |
| U5.4 | N | done | 326 | green | Design documents of U5.1 to U5.3 (D9). balance-analysis.md: the prompt pair with the `subjects` definition and the authored synthetic examples (kinds, size limit, no evaluation-set text, the example test); the claim order (evidence first, the loop guard following the request's schema, readers keyed by name, fingerprints sorting keys); the model boundary `{subjects, claims}` with the subjects gate and its open review (E-5). design/cli.md section 5: `evidence.CLAIM` order; `stages.schema_for` and `normalize` for `extract` (claim order kept, `quality_point_ids` last, `{subjects, claims}`, `subjects` bounds) and the gate in `pipeline.extract_claims`; `inference.claim_key`, `claim_pattern` and `repeated_claim(output, allowed_ids, first_key)`. No guide change (no CLI option or behavior visible to the user changed). Lock unchanged (771 keys) |
| U5-L3 | L | done | 326 | green | UP-D11, UP-D18, UP-D19, UP-D20, D-13. `u5l3-extraction-development-off` at the U5.3 commit `476d502` (a `git archive` copy first on `sys.path`; U5.2 included) through bridge version 2 (identity check passed; all 190 chat attempts from `deepseek/deepseek-v4-flash` on DeepInfra). Reference `u5l1-extraction-development-off` (U5.1, the latest step that passed; D-13). Verdict: U5.3 **fails rules 3 and 4**: precision of accepted claims 52/71 (73.2 %) against 58/77 (75.3 %), −2.1 points (Newcombe −16.1 to +11.8); recall 52/123 (42.3 %) against 58/123 (47.2 %), −4.9 points (−17.0 to +7.5), beyond 3; T6 54/126 (42.9 %) against 40/119 (33.6 %); rule 2 holds (0 against 0, coverage complete). Against the U5.2 run: −2.1 and −6.5 points. Escalation E-6; not reverted. Run U5-L3 ran while U5.4 (documents) was committed. Curated report `reports/20261105-upgrade-u5-evaluation/` (D-13) with the five U5 runs; full runs archived with `SHA256SUMS`. See "U5-L3" under "Live evaluations". Spend 0.0256 USD (0.2841 to 0.3097 USD) |
| U4.F2 | B | done | 326 | updated by UP-D10 | Fix-up step of E-4, fallback (a), adopted under the owner authorization of 2026-11-05 03:11 and moved from the verification session to session U6 by its prompt (later commits would make the reverts harder; the verification session checks them). `git revert` of U4.F1 (`385f744`): the prompt pair `evidence-quality.{en,zh}` returns to its U4.4 text; see "Behavior changes". The record and the lock kept their HEAD versions in the conflict resolution (the record keeps the U4.F1 rows as history); the lock was regenerated: exactly the 25 keys of U4.F1 (the prompt assets and snapshots, manifests, the quality request digests and the two reports), 771 keys |
| U4.F3 | B | done | 320 | green | Fix-up step of E-4, fallback (a), adopted under the owner authorization of 2026-11-05 03:11 (moved to session U6 as U4.F2). `git revert` of U4.5 (`2614453`): `evidence_quality.stored_annotation_errors` and `SCHEMA_VERSIONS` removed; `review.load_run` again validates the stored `annotation` with `validate_annotation`; `quality_scoring.evaluate` and `legacy_review.apply_review` no longer refuse unknown schema versions. The record kept its HEAD version in the conflict resolution. `tests/test_quality_readers.py` (+6 in U4.5) removed with the step, so the count falls from 326 to 320 (above the P4 floor of 241); the file is archived (see "Archive and deletions"). Until U4.F4, the pipeline still writes v2 records, whose derived `annotation` the v1 rules accept, as at the U4.4 commit. Lock unchanged (771 keys) |
| U4.F4 | B | done | 320 | updated by UP-D10 | Fix-up step of E-4, fallback (a), adopted under the owner authorization of 2026-11-05 03:11 (moved to session U6 as U4.F2). `git revert` of U4.4 (`09a79e3`): the pipeline sends quality v1 requests again (the U2.2 view with offsets and the character reference; `annotation_schema`, `validate_annotation`, `qualify`), the policy returns to `evidence-quality-policy-v1` (schema `evidence-quality-v1`, no `segmentation_version`), the prompt pair `evidence-quality.{en,zh}` to its U2.2 text, `FixtureTransport` to v1 answers, `design_briefs.quality_design_errors` to v1 (D-11, part 2) and the two quality scripts to `qualify`; the tests of U4.4 return to their U2.2 to U3 form. The code merged without conflict with the U5 commits; the record and the lock kept their HEAD versions. U4.1 to U4.3 (`clause_segments`, the v2 schema builder, `to_v1_annotation`, `validate_annotation_v2`, `qualify_v2`, `fixture_transport.v2_annotation`) and U4.7 stay, unused by the pipeline. Lock regenerated (771 keys): exactly the 100 keys of U4.4; 77 return to their values before U4.4, and 23 (extraction and verify requests of `enforce`, manifests, prompt snapshots, reports) keep the U5 changes. See "Behavior changes" |
| U4.F5 | N | done | 320 | green | Documentation fix-up of E-4 after U4.F2 to U4.F4 (the session's prompt: one sentence where a document describes a v2 request no longer sent). evidence-quality.md section 3.3, emotion-quantification-and-evidence-isolation.md section 3 and design/cli.md section 5 (`stages`) each say that the v2 contract is not in effect and the pipeline sends and reads v1 again. ADR `0005` is not edited: a decision is frozen once final (D3), so the sentence there is **bypassed** (adding it would break `RULES.md`); its index row and status stay, and E-4 holds the outcome. Lock unchanged |
| U6.7 | N | done | 323 | green | LNK-05. `pipeline.RunOptions`, a frozen dataclass (`out`, `base_url`, `embedding_model`, `quality_mode`, `relevance_only`, `quality_only`, `max_parallel_requests` with the defaults `off`, false, false, 1), replaces the namespace argument of `pipeline.process`: `operations.analyze` builds it from the resolved configuration (its `SimpleNamespace` removed) and `engine.run` from its argparse namespace (the values it read before: the resolved `out`, `validate_modes` for the mode, the flags and `max_parallel_requests` with their old defaults); `RunState.options` replaces `RunState.args`, and `build_full_coverage` and the stages read the flags from it. `validate_modes` keeps reading any object (the legacy parser). New `tests/test_run_options.py` (+3): fields, defaults and immutability; the demo passes `RunOptions` in three modes; `engine.run` (lock target L2 in `shadow`) passes options with the namespace's values and an absolute `out`. Lock unchanged (771 keys). design/cli.md section 5 (`pipeline`), which also drops the U4.4 context keys of `quality_request` (U4.F4) |
| U6.1 | B | done | 331 | updated by UP-D12 | LNK-02, plan 4.8 and 4.11. New module `topics` (domain; imports `resources`, `balance_policy`): `target_reference(target, character)` returns `glossary_ids` (sorted), `status` and `matched_alias`. Index (built once per process, `lru_cache`, never mutated): the 818 entries outside the `character` category with canonical name, Chinese label and aliases. A term matches when `balance_policy.term_matches` finds it in the target literal; an entry scoped to a character matches only that character; terms inside a longer matched term (flagged or not) are dropped, so `斗气` (Drive Gauge) does not decide inside the flagged `斗气冲击`; `resolved` needs the remaining unflagged terms to name exactly one entry; several entries (`CA`; `Drive Rush into Drive Impact`; `Sonic Boom recovery`) or only `candidate_only`/`requires_context` aliases give `candidate`; otherwise `unmatched`. Only exact terms resolve (no escalation, work order section 6, first trigger). `pipeline.extract_claims` adds `target_reference` after `ground_claim` (before `evidence_quality` in `enforce`); the verify view carries only its four claim fields, so no request changes. `review.load_run` recomputes it for every saved claim that holds one and adds `Saved target reference differs from the glossary` (an automatic claim then fails closed, as the saved evidence check); runs without the key load. Layering rows: `topics` → `resources`, `balance_policy`; `pipeline` and `review` add `topics`. New `tests/test_topics.py` (+8): Drive Impact, Drive Rush and Perfect Parry in English and Chinese; Ryu's Hadoken, Guile's Sonic Boom, Ken's Shoryuken and OD Sonic Cross; flagged, nested and ambiguous aliases stay candidates; moves of another character and free text stay unmatched; whole-word Latin matching; the index; the demo claims in three modes carry the recomputed reference; review fails a changed reference and loads a run without one. Demo: 18 of 26 claims resolved in `off` and `shadow`, 18 of 20 in `enforce`. Lock regenerated (774 keys): exactly the 32 keys under "Behavior changes", the three existence-only `code-snapshot/topics.py` keys among them; no request digest changed. design/cli.md section 5 (layout, `topics`) |
| U6.2 | B | done | 333 | updated by UP-D12 | LNK-02, plan 4.8. `reporting.groups_for` groups a formal claim whose target reference is `resolved` by (character, glossary ID) and every other claim, candidates included, by (character, normalized literal), so candidates never merge; each group adds `grouping`, `glossary_id`, `glossary_entry` (canonical name, Chinese label, category), every literal in `topic_original_literals` and `target_reference_statuses`; `topic_literal_normalized` stays (the normalized canonical name for a glossary group; `presentation` reads it and is outside the boundary). The reference is the saved one (checked by `load_run`) or computed for claims without one (`review.target_reference`; earlier runs and reviewed claims); `review.glossary_entry` reads `topics.entry`, so `reporting` keeps its layering row. `report.json`: `schema_version` `aimediator-report-v2` and `topic_grouping` (status counts of formal claims, groups, glossary and literal groups, `groups_by_literal_only`); the Markdown heading of a glossary group names the entry and lists its literals; the limitation on literal grouping is rewritten, not removed. Demo `enforce` report: 18 formal claims, all resolved; 3 groups against 6 by literal alone. Tests (+2, `tests/test_topics.py`): grouping across English and Chinese literals, a candidate (`CA`, and `shoryuken startup`, which also names the mechanic Startup) kept apart, a move of another character in its own group; the report v2 keys, two byte-identical exports, and an export of a run stripped of `target_reference` giving the same groups. Lock regenerated (774 keys): exactly `L1:example-report/report.json`, `L1:example-report/report.md`, `L3:reviewed-report/report.json`, `L3:reviewed-report/report.md`. design/cli.md section 8 (report contract), guide (reports) |
| U6.5 | B | done | 337 | updated by UP-D14 | ALG-05, plan 4.9. `retrieval.near_duplicate_clusters(ids, vectors, threshold)` (single linkage over the comment unit vectors that `retrieve` already has, blockwise; clusters `D<n>` with sorted `comment_ids`, `max_cosine`, each member's highest cosine, the linking pairs) and `retrieve` writes `near-duplicates.json` after `retrieval.json` (threshold and version read from the policy asset; `retrieval` keeps its layering row). `balance-review-policy.json`: `near_duplicate_cosine` 0.9, version `balance-review-policy-v3`, `calibration` unchanged. Threshold chosen on development comments only: the 114 comments of the extraction-development sample (all in the development split; vectors from the embedding records of `u5l3-extraction-development-off`, no new request); 6,441 pairs, 5 at or above 0.90, all the same request, position or complaint (`buff jp` and `加强JP` at 0.936 among them); of the 20 pairs just below (0.833 to 0.889), 8 the same and 7 opposite, the highest opposite pair at 0.872; recorded in `reports/20261105-upgrade-u6-evaluation/summary/near-duplicate-threshold.json` (5 pairs above instead of 20: no more exist; no escalation, work order section 6, third trigger). Report export adds `near_duplicate_clusters` with the note that counts are unchanged (null without the file); `quality_scoring.prepare_dataset(..., near_duplicates=None)` and `prepare --near-duplicates` merge exact-duplicate clusters that share a near-duplicate cluster into one split. New `tests/test_near_duplicates.py` (+4). Lock regenerated (780 keys): exactly the 23 keys under "Behavior changes" (6 `near-duplicates.json` keys added); no request digest changed. design/cli.md section 5 (`retrieval`) |
| U6.4 | B | done | 341 | updated by UP-D13 | LNK-03, plan 4.8. `collection/screening.py` version `coarse-v2` (`VERSION`): `CHAR_ZH` and `MECH` replaced by `_char_zh()` and `_mech()`, built on first use as `_char_en`: Chinese labels and every Chinese alias of `character` entries plus the 18 coarse-v1 names the glossary lacks (traditional spellings, community names); canonical names, Chinese labels and unflagged aliases of `system` and `mechanic` entries plus the 92 coarse-v1 patterns no unflagged alias covers, without the reviewed exclusions (D-15). New collection configuration `configs/feedback-screening-terms.json` (P7; every entry with a reason). Decisions and summary carry `coarse-v2`; the summary adds `terms_sha256`. Comparison before the commit (offline, rules, all raw records): first pass, the plain generator: 264 of 6,376 decisions changed on `20261027-balanced` (4.14 %), 150 of 3,752 on `20261015-expanded` (4.00 %); agent review of 40: 11 better, 3 neutral, 26 worse (control-type entries and `PC`); committed, with the exclusions: 24 (0.38 %; exclude to review 20, to keep 4) and 7 (0.19 %; 6 and 1); agent review of all 24 changed IDs: 4 better (Drive Rush and Drive Impact complaints, a fighter's pressure), 5 neutral, 15 worse (two-letter aliases in other languages, technical `startup`, a controller), net +5 kept and +26 for review. Below the 5 % trigger (work order section 6). The owner's review of the comparison (UP-D13) is recorded as adopted under the owner authorization of 2026-11-05 03:11, after the agent's review of the changed decisions: the change removes the copy of glossary content (G2) at a cost of a few more review-queue records. Recorded datasets keep their decisions; nothing is screened again. Tests (+4, `tests/test_screen_feedback.py`): version and terms file, the glossary Chinese labels, glossary mechanics with spelling variants and the exclusions, a glossary mechanic with a claim kept. Lock regenerated (780 keys): exactly `L4:classify_rules`. design/cli.md section 5 (`collection`). Decisions found during execution D-14 (bypassed) and D-15. Files: `reports/20261105-upgrade-u6-evaluation/summary/screening-comparison.json` |
| U6.3 | B | skipped (UP-D20) | — | — | Mechanic terms in the quality and extraction views (UP-D12, conditional) skipped by the owner's decision UP-D20 |
| U6.6 | B | skipped (UP-D20) | — | — | Second audit trial (UP-D15) skipped by the owner's decision UP-D20; `second_audit` does not exist, so the owner action "decide on `second_audit` after U6-L" falls away |
| U6-L | L | done | 341 | green | UP-D12 to UP-D14, UP-D18, UP-D19, UP-D20. `u6-benchmark-off` and `u6-extraction-development-off` (default configuration, no second audit) at the U6.5 commit `a05b0ee` (module and asset hashes equal to HEAD) through bridge `openrouter-bridge-2` (identity check passed; `doctor` passed; every response from `deepseek/deepseek-v4-flash` on DeepInfra). No U6 step changes model-visible content (U6.3, U6.6 skipped), so the adoption rule applies to none; regression check against `u2l1-benchmark-off` (equal precision 4/6 and recall 4/10, 0 against 0 failures) and `u5l3-extraction-development-off` (same request code: precision of accepted claims 57/76 against 52/71, +1.8 points; recall 56/123 against 52/123, +3.3; 0 against 0 failures, coverage complete). Readings: 5 of 117 grounded claims resolve to a glossary entry (100 have no target), 5 candidates; report groups 8 with glossary grouping and 8 by literal; 3 near-duplicate clusters of 7 comments. See "U6-L" under "Live evaluations". Curated report `reports/20261105-upgrade-u6-evaluation/`; full runs archived with `SHA256SUMS` (1,606 files). Spend 0.0283 USD (0.3097 to 0.3380 USD) |

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
| U4-L (`u4-benchmark-shadow`) | `2614453` | `upgrade-samples-v1/latency-benchmark` (30) | `shadow` | 321.1 s | relevance 1,474 (1,090); retrieval_review 1,353 (1,046); quality 3,673 (2,630); extract 2,788 (2,495); verify 742 (571) | relevance 15; retrieval_review 14; quality 501; extract 200; verify 7 | 9 quality requests with validation errors; 0 transport; 4 quality-failed comments; 0 generation-failed comments; 3 pending | 12 / 8 (0 quarantined; 4 of 12 audited rejected, 33.3 %) | 4/6 (66.7 %) / 4/10 (40.0 %), the 11 scored sample comments of the development split | first attempt 18/23 (78.3 %, Wilson 58.1–90.3 %); 28 attempts; final 19/23 | U4.4 and U4.5: rules 2 and 3 (T5) fail; see the verdicts |
| U4-L (`u4-quality-synthetic-shadow`) | `2614453` | `upgrade-samples-v1/quality-synthetic` (19) | `shadow`, `--stop-after quality` | 127.7 s | relevance 1,312 (928); retrieval_review 958 (446); quality 2,865 (1,745) | relevance 16; retrieval_review 11; quality 311 | 0 quality requests with validation errors; 0 transport; 0 quality-failed comments; 2 pending | — | — | first attempt 16/16 (100 %, Wilson 80.6–100 %); 16 attempts; route agreement 14/16 (87.5 %, Wilson 64.0–96.5 %), English 5/7, Chinese 9/9; 16 of 19 cases reach quality | rule 4 holds: validity and route agreement up |
| U4-L2 (`u4f1-benchmark-shadow`) | `385f744` | `upgrade-samples-v1/latency-benchmark` (30) | `shadow` | 313.3 s | relevance 1,474 (1,090); retrieval_review 1,353 (1,148); quality 3,951 (2,589); extract 2,788 (2,422); verify 742 (508) | relevance 15; retrieval_review 14; quality 530; extract 201; verify 7 | 10 quality requests with validation errors (5 comments, both attempts); 0 transport; 5 quality-failed comments; 0 generation-failed comments; 3 pending | 12 / 10 (0 quarantined; 2 of 12 audited rejected, 16.7 %) | 4/8 (50.0 %) / 4/10 (40.0 %), the 11 scored sample comments of the development split | first attempt 18/23 (78.3 %, Wilson 58.1–90.3 %); 28 attempts; final 18/23 | U4.F1: rule 2 still fails; see the verdicts |
| U4-L2 (`u4f1-quality-synthetic-shadow`) | `385f744` | `upgrade-samples-v1/quality-synthetic` (19) | `shadow`, `--stop-after quality` | 108.7 s | quality 2,971 (1,978) | quality 307 | 2 quality requests with validation errors; 0 transport; 1 quality-failed comment; 2 pending | — | — | first attempt 15/16 (93.8 %, Wilson 71.7–98.9 %); 17 attempts; route agreement 14/16 (87.5 %), English 7/7, Chinese 7/9 | rule 4 holds against U2-L1 |

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

### U3-L (UP-D08, UP-D09; API, UP-D19)

Session U3-L on 2026-11-05, at the U3.4 commit `1a5d520`, on
`upgrade-samples-v1/latency-benchmark` (30 comments, input SHA-256 equal to
the U2-L0 and U2-L1 runs) in `shadow`, through bridge
`openrouter-bridge-2`, with `runs/upgrade/live-config-api.json` and only
the options `--max-parallel-requests` and `--cache-dir`. Measured with the
committed tools and the one-off `runs/upgrade/tools/u3l_analyze.py` (kept
under `provenance/` of the report). Stage windows are summed per routed
model (first `request.json` to last `response.json`), because the stages of
the two models run one after the other. Overlap comes from the bridge log
(each request's logged end minus its elapsed time), which replaces the
`/api/ps` record (UP-D19).

| Run | N | Cache | Wall | Chat / embed requests (bridge) | Peak in flight | Technical failure units | Claims accepted / quarantined | Precision / recall (dev, 11 comments) | Quality first attempt | Cost |
| --- | - | ----- | ---- | ------------------------------ | -------------- | ----------------------- | ----------------------------- | ------------------------------------- | --------------------- | ---- |
| `u3-benchmark-shadow-p1` | 1 | `cache-1`, cold | 322.7 s | 59 / 3 (51 texts: the probe, then 32 and 18) | 1 | 3 | 9 / 3 | 5/7 / 5/10 | 19/23 | 0.0109 USD |
| `u3-benchmark-shadow-warm` | 1 | `cache-1` | 5.2 s | 0 / 1 (the availability probe) | 1 | 3 | 9 / 3 | 5/7 / 5/10 | 19/23 | 0.0000 USD |
| `u3-benchmark-shadow-p2` | 2 | `cache-2`, cold | 245.7 s | 58 / 3 | 2 (50 of 61 requests overlap another) | 3 | 9 / 3 | 4/7 / 4/10 | 20/23 | 0.0079 USD |
| `u3-benchmark-shadow-p4` | 4 | `cache-3`, cold | 263.8 s | 61 / 3 | 4 (53 of 64 overlap) | 2 | 8 / 5 | 3/6 / 3/10 | 20/24 | 0.0100 USD |

Throughput by stage (requests per second, output tokens per second; ratio
to p1 in brackets):

| Stage | p1 | p2 | p4 |
| ----- | -- | -- | -- |
| retrieval review (5 requests) | 1.03, 14.9 | 1.40, 19.7 (1.36, 1.32) | 0.95, 14.0 (0.92, 0.94) |
| relevance (8) | 0.83, 12.8 | 0.41, 6.3 (0.49, 0.49) | 1.71, 26.8 (2.06, 2.09) |
| quality (26 to 28) | 0.107, 84.2 | 0.133, 105.4 (1.25, 1.25) | 0.125, 99.2 (1.17, 1.18) |
| extract (7) | 0.38, 74.6 | 0.44, 86.3 (1.16, 1.16) | 0.48, 102.5 (1.27, 1.38) |
| verify (12 or 13) | 1.41, 9.3 | 1.90, 12.7 (1.35, 1.37) | 1.24, 8.3 (0.88, 0.90) |

- **T8** (quality stage with N 2 against N 1, target at least 1.4 times;
  indicative under UP-D19): 1.25 times in requests and in output tokens per
  second; **not met**. The whole run is 1.31 times faster at N 2 and 1.22
  times at N 4. The provider shares throughput between parallel requests:
  the mean elapsed time of a quality request rises from 9.3 s (median 5.3,
  maximum 45.5) at N 1 to 12.5 s (7.8, 50.7) at N 2 and 16.1 s (10.1, 65.5)
  at N 4, while the output per request stays at about 790 tokens. With 11
  to 13 quality comments per model, the slowest comment also bounds each
  model's window. The stages with 5 to 13 requests swing both ways (relevance
  0.49 and 2.06 times) and say little.
- **Warm cache** (run 4): 0 chat requests and no retrieval embedding request
  reached the bridge; the one embedding request is the availability probe
  of `analyze` (one text), which runs before the run folder exists. Every
  one of the 59 chat responses has a `reuse-provenance.json` (source
  `shared_cache`) and `elapsed_seconds` 0, the run has no
  `requests/embedding/` and its 50 embedding records came from the shared
  cache. All 259 JSON files of run 1 (manifest, configuration, artifacts,
  `request.json`, `response.json` and `validation.json` of every request;
  without `run-state.json`, the provenance files, the transport attempts and
  `requests/embedding/`) are byte-identical to run 4 apart from elapsed
  times and timestamps; the run identity is the same. Escalation trigger of
  work order section 6: not raised.
- **Retrieval, batch 8 against 32** (run 5 of the work order, run 1 against
  `u2l0-benchmark-shadow`, the same 30 comments and the same remote
  embedding model through bridge versions 1 and 2): largest absolute
  difference 0.00348 of the positive scores and 0.0 of the negative
  scores; **0** `retrieval_related` decisions changed (the reference's
  smallest margin is 0.00071). Escalation trigger: not raised. The same
  comparison of fresh embeddings at the same batch size shows the hosted
  model's own variation: p2 against p1 differs by at most 9e-8, but p4
  against p1 by 0.00202 in a positive score and changes **1** decision (a
  comment whose p1 margin is about 0.0001), which admits one more comment to
  quality in p4. On the API the batch-size effect is of the size of this
  variation; the comparison cannot separate them.
- **Failures and coverage**: coverage complete in every run (30 of 30);
  technical failure units 3, 3, 3 and 2 (U2-L1 `shadow` 3, U2-L0 1): the
  three comments of U2-L1 `shadow` whose relevance stays
  `technical_failure_or_pending` (`steam:230206787`, `steam:234299803`,
  `steam:235458828`; p4 has the first and the last). Rule 2 of 5.4 would
  hold (at most one unit above the reference); U3 changes no
  model-visible content, so no adoption rule applies.
- **Spend**: 0.0288 USD for the doctor call and the four runs (bridge total
  0.1198 to 0.1486 USD; 2.83 USD remain below the refusal point).


### U4-L (UP-D10; API, UP-D19)

Rows of U4-L (2026-11-05, runs from 04:33:22 to 04:40:54, session U4-1 to
U4-3 and U4-L in one agent, UP-D20): the two runs of the work order that
UP-D18 keeps, `u4-benchmark-shadow` and `u4-quality-synthetic-shadow`, at
the U4.5 commit `2614453` (HEAD; `pip install -e .`), started by this
session in its own process session (`runs/upgrade/tools/u4l_api_runs.sh`),
one after another, with `max_parallel_requests` 1 and no `cache_dir`
(D-10). Environment check (plan 5.4, "Hosted API"): `/api/version`
answers `openrouter-bridge-2`; `api_bridge.py` SHA-256
`f42e0087ebcde0b193eaaa1d60cd2c735b7630fa7735ccda14acd7403e1137e9` and
the three digests of `doctor` (passed) equal the record (version 2);
`live-config-api.json` unchanged (SHA-256 `b44df0f2…c4530`). Identity of
each run (`check_api_identity.py --prefix u4 --commit 2614453`): the 31
module and 21 resource hashes of the manifest equal `2614453`, digests
equal `doctor`, inputs and sources equal the reference runs, service
`{"ollama_version": "openrouter-bridge-2"}`, every chat response (60 and
23, and every transport attempt) from `deepseek/deepseek-v4-flash` on
DeepInfra through version 2. The tool reports `passed: false` only because
it pins version 1 (it was written for U2-L0 and U2-L1); every item holds
for version 2. Spend: 0.0179 USD for `doctor` and the two runs (bridge
total 0.1486 to 0.1665 USD; the `remote` objects give 0.0136 and
0.0043 USD).

Reference (session prompt): the most recent API row of the same sample and
mode whose steps passed the adoption rule. U2.2 passed in U2-L1, so the
references are `u2l1-benchmark-shadow` and `u2l1-quality-synthetic-shadow`
(U2-L1 rows above). The U3-L run `u3-benchmark-shadow-p1` is later but
measured U3 steps that do not change model-visible content, and the
prompt names U2-L1; it is not used. Measurements, scores, the identity
check and the comparison (`summary/u4l-analysis.json`: Wilson intervals,
Newcombe intervals of the differences, paired first attempts, error
classes, the largest prompt plus output) are in
[`reports/20261105-upgrade-u4-evaluation/`](../../reports/20261105-upgrade-u4-evaluation/manifest.json);
full runs in the archive (see "Archive and deletions").

Verdicts of U4-L (adoption rule of plan 5.4; U4.4 and U4.5 measured
together, U4.5 changes no request):

| Step | Rule 1 gates | Rule 2 failure units and coverage | Rule 3 target metrics | Rule 4 no inferiority | Verdict |
| ---- | ------------ | --------------------------------- | --------------------- | --------------------- | ------- |
| U4.4 and U4.5 (UP-D10) | pass (316 tests, rule check 0, lock green at `2614453`) | benchmark quality-failed comments 4 against 2 (+2, beyond the margin of 1); 0 transport; 0 generation-failed; coverage complete (30 records); pending 3 against 3 | T4: quality 11.2 s per comment (257.6 s for 23) against 18.5 s (445.0 s for 24), 60.4 % (U2-L0 baseline 18.3 s: 61.2 %, target at most 50 %, indicative); T5: benchmark first-attempt validity 18/23 (78.3 %) against 21/24 (87.5 %), −9.2 points (Newcombe −31.0 to +12.9), the wrong direction | synthetic first-attempt validity 16/16 against 13/16 (+18.8 points, −4.1 to +43.0); route agreement 14/16 against 11/16 (+18.8, −10.3 to +44.7), 5 cases newly agreeing and 2 no longer; extraction precision and recall on `extraction-precision-v1` development not run (UP-D18); benchmark scores equal (4/6, 4/10) | **fails rules 2 and 3 (T5)**; escalation E-4 (work order section 6, fourth trigger); not reverted in this session |

Targets of plan 5.5 through the API: T4 11.2 s per comment, 61.2 % of
the U2-L0 baseline, not met (at most 50 %, 9.2 s; indicative); T5 78.3 %
on the benchmark, not met (at least 95 %; the synthetic sample reaches
16/16).

Findings of U4-L:

- **The offset failure classes are gone; one semantic class remains.**
  Attempt errors on the benchmark: `Point/segment detail conflict: P1` 7,
  `Literal absent from selected spans: character_literal` 2 (U2-L1: 21 of
  27 were quote, offset or overlap errors). The 4 failed comments are 3
  Chinese comments whose concrete point selects clauses the answer labels
  `general_opinion` (both attempts), and 1 Chinese comment whose literal
  lies outside its selected clauses (both attempts); the repair attempt
  fixed 1 of 5 first-attempt failures. In v1 the model could cover a
  naming clause and a concrete clause with one concrete segment; with
  program clauses each clause takes its own label, and the concrete point
  rejects a general one. Of the 23 common comments, 15 are valid on the
  first attempt in both runs, 3 only in U4-L and 5 only in U2-L1.
- **Output falls, prompts grow.** Quality output 501 tokens per request
  against 775 (synthetic 311 against 418); prompt 3,673 against 1,957
  (synthetic 2,865 against 1,799) because the label schema repeats per
  clause (D-11). Elapsed 9.2 s per request against 16.5 s.
- **Largest prompt plus output (U4.6).** 13,520 tokens on the benchmark
  (11,453 prompt and 2,067 output, attempt 1) and 14,346 on the synthetic
  sample (12,260 and 2,086); 4 benchmark requests and 1 synthetic request
  reach 6,000 or more. U2-L1: 6,557 and 6,275.
- **Admission.** The benchmark admits 23 comments to quality against 24
  (4 rejected at relevance against 3); the synthetic sample 16 against 16.
  These relevance differences are run-to-run variation of the unchanged
  relevance stage.


### U4-L2 (E-4; API, UP-D19)

Rows of U4-L2 (2026-11-05, runs from 04:47:26 to 04:54:40, same agent):
the two U4-L runs repeated at the U4.F1 commit `385f744` as
`u4f1-benchmark-shadow` and `u4f1-quality-synthetic-shadow`
(`runs/upgrade/tools/u4l2_api_runs.sh`, own process session, N 1, no
`cache_dir`), the measurement of option (c) of E-4. Environment and
identity as in U4-L: bridge version 2 with the recorded SHA-256 and
digests, `doctor` passed, configuration unchanged; 31 module and 21
resource hashes equal `385f744`; every chat response (60 and 24) from
`deepseek/deepseek-v4-flash` on DeepInfra through version 2. Spend 0.0186
USD (bridge total 0.1665 to 0.1851 USD). References: the U2-L1 rows, as
for U4-L. Curated summary (D-12): this record; the runs, measurements,
comparison (`measurements/u4l2-analysis.json`, also against the U4-L
runs) and identity check are in
`~/Archives/AIMediator/reports/20261105-upgrade-u4-fixup-evaluation/`
(726 files with `SHA256SUMS` and `manifest.json`).

| Step | Rule 1 gates | Rule 2 failure units and coverage | Rule 3 target metrics | Rule 4 no inferiority | Verdict |
| ---- | ------------ | --------------------------------- | --------------------- | --------------------- | ------- |
| U4.4, U4.5 and U4.F1 (UP-D10, E-4) | pass (316 tests, rule check 0, lock green at `385f744`) | benchmark quality-failed comments 5 against 2 (+3, beyond the margin of 1; U4-L: 4); 0 transport; coverage complete | T4: 11.0 s per comment against 18.5 s (59.5 %; indicative); T5: 18/23 (78.3 %) against 21/24, −9.2 points (−31.0 to +12.9), unchanged from U4-L | synthetic first-attempt validity 15/16 against 13/16 (+12.5 points, −12.7 to +37.3); route agreement 14/16 against 11/16 (−10.3 to +44.7) | **fails rules 2 and 3 (T5)**; the fallback (a) of E-4 applies; not reverted in this session |

Findings of U4-L2:

- **The prompt fix moved the failures, not their number.** Benchmark
  attempt errors: `Point/segment detail conflict: P1` 4 (U4-L: 7),
  `Literal absent from selected spans: mechanic_literal` 4 (U4-L: 0),
  `character_literal` 2 (2). Of the 23 common comments 18 are valid on the
  first attempt in both U4-L runs; 2 became valid and 2 invalid.
- **Synthetic sample.** One case (`Point/segment detail conflict`, both
  attempts) fails, against none in U4-L; route agreement 14/16 in both
  (English 7/7 against 5/7, Chinese 7/9 against 9/9).
- **Benchmark claims.** 12 generated and 10 accepted (U4-L: 12 and 8);
  accepted claims score 4 of 8 scored positions (U4-L and U2-L1: 4 of 6);
  recall 4/10 in all three runs. The extraction
  sample was not run (UP-D18), so rule 4's extraction margin is not
  measured for U4.
- **Largest prompt plus output** 13,339 on the benchmark and 14,482 on
  the synthetic sample; U4.6 stays skipped.

### U2-R (E-3; API, UP-D19)

Run by the U5 session on 2026-11-05 from 04:59 to 05:06, before U5.1, to
settle E-3 with option (c): U2.3 measured without U2.4. The code of
`39a1efd` (the U2.3 commit) was extracted with `git archive` into
`runs/upgrade/code-39a1efd/src` and put first on `sys.path`, as
`u2l0_api_runs.sh` did for `0abfe02`; the U2-L1 commands for the
extraction-development sample in `off` (`runs/upgrade/tools/u5_api_run.sh`).
In `off` no quality request is sent, so the run differs from the U2-L0 run
only by U2.3. Identity (`runs/upgrade/tools/u5_identity.py`): 30 module
hashes equal to `39a1efd`; service `openrouter-bridge-2`, bridge SHA-256,
digests and `live-config-api.json` equal to the record; `doctor` passed;
input and source hashes equal to the reference; all 176 chat attempts from
`deepseek/deepseek-v4-flash` on DeepInfra. Compared with
`runs/upgrade/tools/u5_compare.py` (D-8 reading; the tool reproduces the
U2-L1 values of E-3 exactly when pointed at the U2-L1 run).

| Run | Precision accepted | Precision generated | Recall | Recall admitted | T6 rejected | Extraction prompt (uncached) | Output | Failures |
| --- | ------------------ | ------------------- | ------ | --------------- | ----------- | ---------------------------- | ------ | -------- |
| `u2l0-extraction-development-off` (reference, `0abfe02`) | 61/80 (76.2 %) | 85/131 (64.9 %) | 60/123 (48.8 %) | 60/123 | 52/134 (38.8 %) | 4,437 (3,955) | 373 | 0 |
| `u2r-extraction-development-off` (U2.3 alone, `39a1efd`) | 60/79 (75.9 %) | 76/112 (67.9 %) | 59/123 (48.0 %) | 59/123 | 37/117 (31.6 %) | 3,369 (2,959) | 332 | 0 |
| `u2l1-extraction-development-off` (U2.2 to U2.4, `b7d1cc5`) | 55/74 (74.3 %) | 74/120 (61.7 %) | 54/123 (43.9 %) | 54/121 | 53/129 (41.1 %) | 3,353 (2,841) | 362 | 0 |

Verdict for U2.3 alone (D-8): rule 2 holds (0 against 0 technical
failures, coverage complete); rule 3 holds (T1 extraction uncached prompt
tokens 2,959 against 3,955, −25.2 %); rule 4 holds: precision of accepted
claims −0.3 points (Newcombe −13.5 to +12.9), recall −0.8 points (−13.1 to
+11.5), English recall 30/46 in both, Chinese 29/77 against 30/77. Against
the U2.3-only run, the U2-L1 run (which adds U2.4) loses 4.1 points of
recall (−16.2 to +8.3) and 3.3 over admitted comments; its admission
differs on 4 comments. The loss of E-3 therefore arises with U2.4 and
run-to-run variation of the hosted model, not with U2.3; every interval
includes 0. Finding for U2-V and the U2 review: U2.4 was judged on
relevance agreement (D-8) and kept; its effect on extraction recall
(through admission) is not a D-8 metric of U2.4 and is recorded here only.

### U5-L1 (UP-D11; API, UP-D19)

Runs of 2026-11-05 from 05:09 to 05:26, started by the U5 session in
their own process sessions, side by side, with
`runs/upgrade/tools/u5_api_run.sh` from `git archive` copies of their
commits first on `sys.path` (so later edits of the checkout could not
reach a running process): `u5l1-extraction-development-off` at the U5.1
commit `e64701d`, and `u5r-extraction-development-off` at `e34e08d`, the
U5 entry state (code of the U4 session), as an estimate of run-to-run
variation that decides nothing. Both identity checks
(`runs/upgrade/tools/u5_identity.py`) passed: module hashes equal to their
commits, service `openrouter-bridge-2` with the recorded SHA-256 and
digests, `live-config-api.json` unchanged, `doctor` passed, input equal to
the reference, every chat attempt from `deepseek/deepseek-v4-flash` on
DeepInfra. Reference: `u2l1-extraction-development-off` (E-3). Compared
with `runs/upgrade/tools/u5_compare.py` as D-13 reads the rule.

| Run | Precision accepted | Precision generated | Recall | Recall admitted | T6 rejected | Claims per long comment (generated, accepted) | Extraction prompt (uncached) | Output | Failures |
| --- | ------------------ | ------------------- | ------ | --------------- | ----------- | --------------------------------------------- | ---------------------------- | ------ | -------- |
| `u2l1-extraction-development-off` (reference) | 55/74 (74.3 %) | 74/120 (61.7 %) | 54/123 (43.9 %) | 54/121 | 53/129 (41.1 %) | 1.24, 0.39 (33 comments) | 3,353 (2,841) | 362 | 0 |
| `u5r-extraction-development-off` (entry rerun) | 55/73 (75.3 %) | 72/112 (64.3 %) | 54/123 (43.9 %) | 54/121 | 44/118 (37.3 %) | 0.94, 0.39 (31) | 3,432 (2,952) | 369 | 0 |
| `u5l1-extraction-development-off` (U5.1) | 58/77 (75.3 %) | 74/113 (65.5 %) | 58/123 (47.2 %) | 58/121 | 40/119 (33.6 %) | 0.97, 0.52 (31) | 3,389 (2,939) | 369 | 0 |

By language (U5.1 against the reference): English precision of accepted
claims 30/33 against 29/31, recall 30/46 against 29/46; Chinese 28/44
against 26/43 and 28/77 against 25/77. Long comments are admitted
comments over 400 characters (35 in the sample) whose extraction
completed. Failures: transport failures plus generation-failed comments;
every run has 2 relevance units pending (exit 5, as every extraction run
since U0.6).

Verdict of U5-L1 (D-13):

| Step | Rule 1 gates | Rule 2 failures and coverage | Rule 3 T7 precision of accepted claims | Rule 4 no inferiority | Verdict |
| ---- | ------------ | ---------------------------- | -------------------------------------- | --------------------- | ------- |
| U5.1 (UP-D11) | pass (318 tests, rule check 0, lock 771 keys) | 0 against 0; coverage complete | 75.3 % against 74.3 %, +1.0 points (Newcombe −12.7 to +14.7) | precision +1.0, recall +3.3 points (−9.1 to +15.4) | kept |

Findings of U5-L1: the entry rerun moves by +1.0 points of precision and
0.0 of recall against the reference with the same code, so differences of
a few points are within run-to-run variation; against the rerun U5.1
gains 0.0 points of precision and 3.3 of recall. T6 falls in both new
runs (37.3 % and 33.6 % against 41.1 %), and U5.1 generates fewer claims
on long comments (0.97 against 1.24 per comment) with more of them
accepted (0.52 against 0.39). T6 target (at most 35 %) met by the U5.1
run; T7 target (+10 points) not met.

### U5-L2 (UP-D11; API, UP-D19)

Run of 2026-11-05 from 05:28 to 05:35, started by the U5 session in its
own process session: `u5l2-extraction-development-off` at the U5.2 commit
`30d41be` from a `git archive` copy first on `sys.path`. Identity check
passed as in U5-L1 (module hashes equal to `30d41be`, bridge version 2
with the recorded SHA-256 and digests, configuration unchanged, `doctor`
passed, input equal to the reference, all 191 chat attempts from
`deepseek/deepseek-v4-flash` on DeepInfra). Reference:
`u5l1-extraction-development-off` (D-13).

| Run | Precision accepted | Precision generated | Recall | Recall admitted | T6 rejected | Claims per long comment (generated, accepted) | Extraction prompt (uncached) | Output | Failures |
| --- | ------------------ | ------------------- | ------ | --------------- | ----------- | --------------------------------------------- | ---------------------------- | ------ | -------- |
| `u5l1-extraction-development-off` (reference, U5.1) | 58/77 (75.3 %) | 74/113 (65.5 %) | 58/123 (47.2 %) | 58/121 | 40/119 (33.6 %) | 0.97, 0.52 (31 comments) | 3,389 (2,939) | 369 | 0 |
| `u5l2-extraction-development-off` (U5.2) | 61/81 (75.3 %) | 72/118 (61.0 %) | 60/123 (48.8 %) | 60/121 | 44/126 (34.9 %) | 1.06, 0.58 (31) | 3,567 (3,117) | 408 | 0 |

By language: English precision of accepted claims 31/32 against 30/33,
recall 31/46 against 30/46; Chinese 30/49 against 28/44 and 29/77 against
28/77. The subjects gate (`Claim character not declared as subject`)
quarantined no claim, so it removed no claim that a label counts as
correct (work order section 6, second trigger: not raised).

Verdict of U5-L2 (D-13):

| Step | Rule 1 gates | Rule 2 failures and coverage | Rule 3 T7 precision of accepted claims | Rule 4 no inferiority | Verdict |
| ---- | ------------ | ---------------------------- | -------------------------------------- | --------------------- | ------- |
| U5.2 (UP-D11) | pass (324 tests, rule check 0, lock 771 keys) | 0 against 0; coverage complete | 75.3 % against 75.3 %, −0.02 points (−13.3 to +13.4): not above | precision −0.0, recall +1.6 points (−10.7 to +13.9) | **fails rule 3**; recorded for the review (E-5), not reverted |

Findings of U5-L2: the model declared subjects consistent with its claims
on all 114 comments, so the gate has not yet acted on this sample; the
step's measured effect is a cost of 178 prompt and 39 output tokens per
extraction request (+5.3 % and +10.6 %) and more Chinese claims generated
(precision of generated claims 61.0 % against 65.5 %) with accepted
precision unchanged. T6 34.9 %, still within the T6 target of 35 %.

### U5-L3 (UP-D11; API, UP-D19)

Run of 2026-11-05 from 05:36 to 05:44, started by the U5 session in its
own process session: `u5l3-extraction-development-off` at the U5.3 commit
`476d502` (which includes U5.2) from a `git archive` copy first on
`sys.path`. Identity check passed as in U5-L1 (module hashes equal to
`476d502`, bridge version 2 with the recorded SHA-256 and digests,
configuration unchanged, `doctor` passed, input equal to the reference,
all 190 chat attempts from `deepseek/deepseek-v4-flash` on DeepInfra).
Reference: `u5l1-extraction-development-off`, the latest step that passed
(D-13); the U5.2 run is reported beside it.

| Run | Precision accepted | Precision generated | Recall | Recall admitted | T6 rejected | Claims per long comment (generated, accepted) | Extraction prompt (uncached) | Output | Failures |
| --- | ------------------ | ------------------- | ------ | --------------- | ----------- | --------------------------------------------- | ---------------------------- | ------ | -------- |
| `u5l1-extraction-development-off` (reference, U5.1) | 58/77 (75.3 %) | 74/113 (65.5 %) | 58/123 (47.2 %) | 58/121 | 40/119 (33.6 %) | 0.97, 0.52 (31 comments) | 3,389 (2,939) | 369 | 0 |
| `u5l2-extraction-development-off` (U5.2) | 61/81 (75.3 %) | 72/118 (61.0 %) | 60/123 (48.8 %) | 60/121 | 44/126 (34.9 %) | 1.06, 0.58 (31) | 3,567 (3,117) | 408 | 0 |
| `u5l3-extraction-development-off` (U5.3 with U5.2) | 52/71 (73.2 %) | 78/121 (64.5 %) | 52/123 (42.3 %) | 52/122 | 54/126 (42.9 %) | 1.03, 0.53 (32) | 3,859 (3,046) | 416 | 0 |

By language against the reference: English precision of accepted claims
23/25 against 30/33, recall 23/46 against 30/46 (−15.2 points, −33.6 to
+4.8); Chinese 29/46 against 28/44 and 29/77 against 28/77. Source
binding quarantined 4 claims in each of the two runs; in U5-L3 they carry
25 errors, mostly numeric (11 `Numerical adjustment intent absent or
ambiguous; review required`, 9 `Parameter lacks requested target or
delta`), against 5 errors in U5-L1. The subjects gate quarantined no claim.

Verdict of U5-L3 (D-13):

| Step | Rule 1 gates | Rule 2 failures and coverage | Rule 3 T7 precision of accepted claims | Rule 4 no inferiority | Verdict |
| ---- | ------------ | ---------------------------- | -------------------------------------- | --------------------- | ------- |
| U5.3 (UP-D11) | pass (326 tests, rule check 0, lock 771 keys) | 0 against 0; coverage complete | 73.2 % against 75.3 %, −2.1 points (−16.1 to +11.8): not above | precision −2.1 points, within 3; recall −4.9 points (−17.0 to +7.5), beyond 3 | **fails rules 3 and 4**; recorded for the review (E-6), not reverted |

Findings of U5-L3: the loss is English: fewer English claims are accepted
(25 against 33) while the audit rejects more (T6 42.9 %); the examples add
292 prompt tokens per extraction request against the U5.2 run (+8.2 %),
470 with U5.2 against U5.1 (+13.9 %; 107 uncached, the rest cached by the
provider). Targets of plan 5.5 after U5 (indicative, API; the T7 baseline
is the U2-L0 run, 61/80, 76.2 %, plan 5.4): T6 (at most 35 %) is met by
the U5.1 run (33.6 %) and the U5.2 run (34.9 %), not by U5.3; T7 (+10
points with recall within 3) is met by none (U5.1 and U5.2 −0.9, U5.3
−3.0 points).

Curated report (D-13): [`reports/20261105-upgrade-u5-evaluation/`](../../reports/20261105-upgrade-u5-evaluation/manifest.json)
holds the metrics, scores, comparisons, identity checks and `doctor`
outputs of `u2r`, `u5r`, `u5l1`, `u5l2` and `u5l3`, and the tools under
`provenance/`; the full runs, logs, configuration, input and tools are in
the archive with `SHA256SUMS`.

### U6-L (UP-D12 to UP-D14; API, UP-D19)

Runs of 2026-11-05 from 06:12 to 06:18, started by the U6 session in its
own process session with `runs/upgrade/tools/u6_api_runs.sh`, one after
another, default configuration (no second audit: U6.6 is skipped by
UP-D20): `u6-benchmark-off` and `u6-extraction-development-off` at the
U6.5 commit `a05b0ee` from a `git archive` copy first on `sys.path`. The
later commits of the session (U6.4) change only `collection/`, root
`configs/`, tests and documents, so the runs' 32 module hashes and asset
hashes also equal HEAD's. Identity check passed for both (module hashes,
bridge `openrouter-bridge-2` with the recorded SHA-256 and digests,
`live-config-api.json` unchanged, `doctor` passed, inputs equal to the
references, all 34 and 179 chat attempts from `deepseek/deepseek-v4-flash`
on DeepInfra). U6 sends no new model-visible content (U6.3 and U6.6
skipped; U6.1, U6.2, U6.5 and U6.7 change no request byte), so no step of
U6 is under the adoption rule; the runs check that nothing regressed and
give the U6 readings. References: `u2l1-benchmark-off`, the latest
accepted benchmark `off` run; `u5l3-extraction-development-off`, the same
extraction request code (U5.2 and U5.3 are still in HEAD; E-5, E-6), and
`u5l1-extraction-development-off`, the latest run that passed.

| Run | Precision accepted | Precision generated | Recall | Recall admitted | T6 rejected | Claims per long comment (generated, accepted) | Failures |
| --- | ------------------ | ------------------- | ------ | --------------- | ----------- | --------------------------------------------- | -------- |
| `u2l1-benchmark-off` (reference) | 4/6 | 5/10 | 4/10 | 4/10 | 4/12 | 0, 0 (4 comments) | 0 |
| `u6-benchmark-off` | 4/6 | 6/12 | 4/10 | 4/10 | 6/14 | 0, 0 (4) | 0 |
| `u5l1-extraction-development-off` (U5.1) | 58/77 (75.3 %) | 74/113 (65.5 %) | 58/123 (47.2 %) | 58/121 | 40/119 (33.6 %) | 0.97, 0.52 (31) | 0 |
| `u5l3-extraction-development-off` (U5.3) | 52/71 (73.2 %) | 78/121 (64.5 %) | 52/123 (42.3 %) | 52/122 | 54/126 (42.9 %) | 1.03, 0.53 (32) | 0 |
| `u6-extraction-development-off` (HEAD) | 57/76 (75.0 %) | 73/108 (67.6 %) | 56/123 (45.5 %) | 56/123 | 39/116 (33.6 %) | 0.81, 0.47 (32) | 0 |

Against `u5l3` (same request code): precision of accepted claims +1.8
points (Newcombe −12.2 to +15.8), recall +3.3 points (−9.0 to +15.4);
against `u5l1`: −0.3 and −1.6 points; rules 2 and 4 as D-8 reads them
hold against both, and the benchmark equals the U2-L1 reference in
precision and recall (0 against 0 technical failures, coverage complete
in both runs; `run_state` `partial` as in every reference, from
relevance-pending comments). The U5.3 run and this run share their
extraction code, so their differences (English recall 27/46 against
23/46; 1 binding quarantine against 4) are run-to-run variation, which
bears on E-6.

U6 readings (`summary/u6l-linkage.json`):

- Target references (U6.1): of 117 grounded claims of the extraction
  run, 17 carry a target literal and 100 have `target` null; 5 resolve
  (4.3 % of all, 29 % of those with a target: `下重脚`, `2MP` and `2MK`
  to the crouching normals, `一气必杀` and `1气` to `system.sa1`), 5 are
  candidates (`Raging Demon`, a flagged alias of Akuma's super;
  `OD龙炎舞`, the move and Overdrive; `白血`, `白血机制` and `打白血设计`,
  which match only the flagged alias `白` of Burnout, since the glossary
  has no entry for chip damage) and 107 are unmatched; of the 77 accepted claims, 12 carry a
  target: 1 resolved, 5 candidates, 6 unmatched (`投`, `大屁股`,
  `高人肘击`, `整个玩法逻辑`, `拳脚`, `技能`). The benchmark run's 14
  claims have no target.
- Report groups (U6.2): the report of the extraction run has 8 topic
  groups with glossary grouping and 8 by literal alone (1 glossary group,
  7 literal groups; 69 formal claims stay unresolved for identity or
  target, mostly null targets); no group merged on this sample. Two
  exports of each run are byte-identical.
- Near-duplicates (U6.5): 3 clusters of 7 comments in the extraction run
  (the JP buff pair across languages, the general balance complaints, the
  three Jamie buff requests; the pairs of the threshold record), none in
  the benchmark run; the report copies them with its note; no count
  changed.
- U6.3 (mechanic terms) and U6.6 (second audit): skipped by UP-D20; no
  adoption rule applied and no second-audit precision, recall or time to
  report.

Findings: the extraction model leaves `target` null for most claims about
a fighter's overall strength, so glossary grouping acts on few claims;
its effect on report fragmentation shows only where targets are named
(the demo: 6 literal groups into 3). Spend of the two runs with their
`doctor` calls 0.0283 USD (0.3097 to 0.3380 USD, 224 requests).

Curated report: [`reports/20261105-upgrade-u6-evaluation/`](../../reports/20261105-upgrade-u6-evaluation/manifest.json)
holds the metrics, scores, comparisons, identity checks, `doctor` outputs,
linkage readings and spend of both runs, the U6.4 and U6.5 evidence, and
the tools under `provenance/`; the full runs, logs, configuration, inputs
and tools are in the archive with `SHA256SUMS`.

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
| U3.4 | UP-D09 | Embedding record layout `embeddings/` (one record per text, batches of 32 instead of 8); no asset, prompt or chat request byte changes | — (no asset) | — (no asset) | `L1:<off|shadow|enforce>/embeddings/<sha256>.json` and `L2:<off|shadow|enforce>/embeddings/<sha256>.json` (8 removed and 58 added per run) |
| U4.4 | UP-D10 | Quality request v2 (plan 4.1, 4.2): the view sends `comments[comment_id, units[evidence_id, segments[segment_id, text]]]`, `language`, `character_literals` and `previous_attempt_errors` (no offsets, texts of whole units or reference entries); `format` and `response_schema` are `annotation_schema_v2` (one label object per clause segment, `character_literal` limited to the literals); records hold the derived v1 `annotation` and the new `annotation_v2`; extraction `allowed_quality_points` and verify `selected_source_segments` follow the clause segments of the converted annotation. Policy `src/aimediator/assets/configs/evidence-quality-policy.json` (`version` `evidence-quality-policy-v2`, `schema_version` `evidence-quality-v2`, new `segmentation_version` `clause-v1`) | `496090a7296a3d8a739d8f3d87ea15b9e3a9a026fa2df8830661bf29aab3146e` | `fb273e2ce8132a8ad90397c13b4108b64d95667f27dba7d8fa80db4f4ddcc06f` | 100 keys, none added or removed: `L1:<shadow|enforce>/` and `L2:<shadow|enforce>/` `evidence-quality.json`, `manifest.json`, `opinion-summary.json`, `prompt-snapshot.json`, `quality-exclusions.json`, `quality-policy-snapshot.json`, `quality-review-queue.json`, `quality-routing.json`, `quality-summary.json`, `system-feedback.json`, `requests/**/request.json` and the four files of `requests/quality/<request-id>/`; in `enforce` also `audit-progress.json`, `balance-report.json`, `claims-before-audit.json`, `request-trace.json`, `validated-claims.json`, the four files of `requests/extract/<request-id>/` and `requests/verify/<request-id>/request.json`; `L1:<off|shadow|enforce>/resource-snapshot/configs/evidence-quality-policy.json` and `…/prompts/evidence-quality.{en,zh}.txt`; `L1:off/manifest.json`, `L1:enforce/run-state.json`; `L1:example-report/report.json`, `L1:example-report/report.md`, `L1:review-template/decisions.json`, `L1:review-template/proposals.json`; `L3:overlay/decisions.json`, `L3:overlay/review-manifest.json`, `L3:overlay/source-review-exclusions.json`, `L3:reviewed-report/report.json`, `L3:reviewed-report/report.md`. No relevance request and no `off` request changed |
| U4.4 | UP-D10 | Prompt `src/aimediator/assets/prompts/evidence-quality.en.txt`: labeling of given segments (the offset and quote paragraph replaced by one on labeling each fixed segment once; `character_literal` chosen from `character_literals` inside a selected segment), the decisions on current position, information level and scope unchanged, two authored synthetic examples | `0da81e6d66b596c68d911723be5b3e97f3b368c85032da4dacd92b666b4bf2c7` | `e24371de447ec5b5598ed415bc3a78d80e832ca544bf0a942faebecf66fb62ea` | as above |
| U4.4 | UP-D10 | Prompt `src/aimediator/assets/prompts/evidence-quality.zh.txt` (same changes) | `1db0f055acbd7c40e945e97c9fb955061107c1477632dfd3543404bb76675f6e` | `ebc63543f4036b632ee4ac5102e4a5ebc63a9e60f42ad7711ca0ba7a276fea21` | as above |
| U4.4 | UP-D10 | Prompt pairs `quality-extract.{en,zh}` and `quality-verify.{en,zh}`: unchanged; they name `allowed_quality_points`, `quality_point_ids`, `evidence_ids`, `selected_source_segments` and `selected_source_points`, whose fields v2 keeps | `345e69b9…dc5`, `d2fe70eb…985b978`, `62ff2904…b4e4f894`, `51c15dca…0ad` | unchanged | none |
| U4.F1 | UP-D10 (E-4) | Prompt `src/aimediator/assets/prompts/evidence-quality.en.txt`: the labeling paragraph adds that points are decided before labels, that every segment of a concrete point is `concrete_feedback` (or `uncertain`) and of a general point `general_opinion` (or `uncertain`), that a segment naming the fighter or judging its strength next to a concrete statement about the same fighter joins that concrete point, and that a point needing the name selects the naming segment or sets `character_literal` to null | `e24371de447ec5b5598ed415bc3a78d80e832ca544bf0a942faebecf66fb62ea` | `825c11cdfe6a9a43495aeedabff678b0ede56ad7b70b1532ea3483e7b0564b7f` | `L1:<shadow|enforce>/manifest.json`, `L1:<shadow|enforce>/prompt-snapshot.json`, `L1:<shadow|enforce>/requests/**/request.json`, `L1:<shadow|enforce>/requests/quality/<request-id>/request.json`, `L1:<off|shadow|enforce>/resource-snapshot/prompts/evidence-quality.{en,zh}.txt`, `L1:off/manifest.json`, `L1:example-report/report.json`, `L2:<shadow|enforce>/manifest.json`, `L2:<shadow|enforce>/prompt-snapshot.json`, `L2:<shadow|enforce>/requests/**/request.json`, `L2:<shadow|enforce>/requests/quality/<request-id>/request.json`, `L3:reviewed-report/report.json` (25 keys, none added or removed) |
| U4.F1 | UP-D10 (E-4) | Prompt `src/aimediator/assets/prompts/evidence-quality.zh.txt` (same paragraph) | `ebc63543f4036b632ee4ac5102e4a5ebc63a9e60f42ad7711ca0ba7a276fea21` | `a383d423eeec97c91a88a1fba05f3a20f3c2e491879b329db38ac19f49eae7ae` | as above |
| U5.1 | UP-D11 | Extraction response schema (`format` and `response_schema` of extraction requests): claim properties in the evidence-first order of plan 4.3 (`evidence.CLAIM`); the duplicate-claim loop guard of `inference.streamed_chat` finds claims by the first claim property of the request's schema; no asset or prompt changes | — (no asset) | — (no asset) | `L1:enforce/requests/**/request.json`, `L1:enforce/requests/extract/<request-id>/request.json`, `L1:enforce/requests/extract/<request-id>/validation.json`, `L1:off/requests/**/request.json`, `L1:off/requests/extract/<request-id>/request.json`, `L1:off/requests/extract/<request-id>/validation.json`, `L1:shadow/requests/**/request.json`, `L1:shadow/requests/extract/<request-id>/request.json`, `L1:shadow/requests/extract/<request-id>/validation.json`, `L2:enforce/requests/**/request.json`, `L2:enforce/requests/extract/<request-id>/request.json`, `L2:enforce/requests/extract/<request-id>/validation.json`, `L2:off/requests/**/request.json`, `L2:off/requests/extract/<request-id>/request.json`, `L2:off/requests/extract/<request-id>/validation.json`, `L2:shadow/requests/**/request.json`, `L2:shadow/requests/extract/<request-id>/request.json`, `L2:shadow/requests/extract/<request-id>/validation.json` |
| U5.2 | UP-D11 | Extraction response schema: each comment `{subjects, claims}` (`subjects` an array of the allowed characters, `uniqueItems`, `maxItems`); fixture answers carry `subjects`; the source-binding error `Claim character not declared as subject`. Prompt `src/aimediator/assets/prompts/summarize-balance.en.txt` (subjects and claims per comment; a two-sentence definition of `subjects` before the subject and direction rules) | `8787336b7d2399cd26866fcd960fdc33d91d6c8af2df195a39ff68208e4ea705` | `6d9835917fed3fffd06de88fe18d1a75d3dd9a396087afaae5b7bd765e92c3e9` | `L<1|2>:<off|shadow|enforce>/requests/**/request.json`, `…/requests/extract/<request-id>/request.json`, `…/response.json`, `…/partial-output.txt`, `…/validation.json`, `L<1|2>:<mode>/manifest.json`, `L<1|2>:<mode>/prompt-snapshot.json`, `L1:<mode>/resource-snapshot/prompts/summarize-balance.en.txt`, `L1:<mode>/resource-snapshot/prompts/summarize-balance.zh.txt`, `L1:example-report/report.json`, `L3:reviewed-report/report.json` (50 keys) |
| U5.2 | UP-D11 | Prompt `src/aimediator/assets/prompts/summarize-balance.zh.txt` (same) | `ae02facccaa8ee313b53f5f2e683357e6b18cfeaa9cb83cf49b9b2202bdf8926` | `b40bbfa5e14323b3d9a418c8126c39834e286eab7e1a559183bbbb840e324381` | as above |
| U5.3 | UP-D11 | Prompt `src/aimediator/assets/prompts/summarize-balance.en.txt`: three authored synthetic examples at the end (input units and the expected entry of `assessments`) | `6d9835917fed3fffd06de88fe18d1a75d3dd9a396087afaae5b7bd765e92c3e9` | `5797deca162eb264c0985c646d1c0d79885ebf6940f4083d740385ff36eed330` | `L<1|2>:<off|shadow|enforce>/manifest.json`, `…/prompt-snapshot.json`, `…/requests/**/request.json`, `…/requests/extract/<request-id>/request.json`, `L1:<mode>/resource-snapshot/prompts/summarize-balance.en.txt`, `L1:<mode>/resource-snapshot/prompts/summarize-balance.zh.txt`, `L1:example-report/report.json`, `L3:reviewed-report/report.json` (32 keys) |
| U5.3 | UP-D11 | Prompt `src/aimediator/assets/prompts/summarize-balance.zh.txt`: five authored synthetic examples at the end (the three of English, an `unclear` and `uncertain` position, a qualitative claim from a general complaint) | `b40bbfa5e14323b3d9a418c8126c39834e286eab7e1a559183bbbb840e324381` | `e901d527721bb9663e9e1d7cce2ed6a47ee0e24b22254e99da951099be5fce86` | as above |
| U4.F2 | UP-D10 (E-4) | Revert of U4.F1: prompt `src/aimediator/assets/prompts/evidence-quality.en.txt` returns to its U4.4 text | `825c11cdfe6a9a43495aeedabff678b0ede56ad7b70b1532ea3483e7b0564b7f` | `e24371de447ec5b5598ed415bc3a78d80e832ca544bf0a942faebecf66fb62ea` | the 25 keys of U4.F1 |
| U4.F2 | UP-D10 (E-4) | Revert of U4.F1: prompt `src/aimediator/assets/prompts/evidence-quality.zh.txt` (same) | `a383d423eeec97c91a88a1fba05f3a20f3c2e491879b329db38ac19f49eae7ae` | `ebc63543f4036b632ee4ac5102e4a5ebc63a9e60f42ad7711ca0ba7a276fea21` | as above |
| U4.F4 | UP-D10 (E-4) | Revert of U4.4: quality requests return to v1 (the U2.2 view `comments[comment_id, units[evidence_id, text, start, end]]`, `language`, `character_normalization_reference`, `previous_attempt_errors`; the v1 schema); records `evidence-quality-v1` without `annotation_v2`. Policy `src/aimediator/assets/configs/evidence-quality-policy.json` returns to `evidence-quality-policy-v1` | `fb273e2ce8132a8ad90397c13b4108b64d95667f27dba7d8fa80db4f4ddcc06f` | `496090a7296a3d8a739d8f3d87ea15b9e3a9a026fa2df8830661bf29aab3146e` | the 100 keys of U4.4 |
| U4.F4 | UP-D10 (E-4) | Revert of U4.4: prompt `src/aimediator/assets/prompts/evidence-quality.en.txt` returns to its U2.2 text | `e24371de447ec5b5598ed415bc3a78d80e832ca544bf0a942faebecf66fb62ea` | `0da81e6d66b596c68d911723be5b3e97f3b368c85032da4dacd92b666b4bf2c7` | as above |
| U4.F4 | UP-D10 (E-4) | Revert of U4.4: prompt `src/aimediator/assets/prompts/evidence-quality.zh.txt` (same) | `ebc63543f4036b632ee4ac5102e4a5ebc63a9e60f42ad7711ca0ba7a276fea21` | `1db0f055acbd7c40e945e97c9fb955061107c1477632dfd3543404bb76675f6e` | as above |
| U6.1 | UP-D12 | Claim field `target_reference` (`glossary_ids`, `status`, `matched_alias`) on every grounded claim, after the `ground_claim` fields and before `evidence_quality`; new module `topics` in the code manifest; no asset, prompt or request byte changes | — (no asset) | — (no asset) | L1:<enforce|off|shadow>/audit-progress.json, L1:<enforce|off|shadow>/balance-report.json, L1:<enforce|off|shadow>/claims-before-audit.json, L1:review-template/proposals.json, L1:example-report/report.json, L1:<enforce|off|shadow>/validated-claims.json, L2:<enforce|off|shadow>/audit-progress.json, L2:<enforce|off|shadow>/balance-report.json, L2:<enforce|off|shadow>/claims-before-audit.json, L2:<enforce|off|shadow>/code-snapshot/topics.py, L2:<enforce|off|shadow>/validated-claims.json, L3:reviewed-report/report.json, L3:overlay/review-manifest.json, L3:overlay/source-review-exclusions.json |
| U6.2 | UP-D12 | Report export schema `aimediator-report-v2`: groups by glossary ID, then literal; `topic_grouping`; Markdown headings of glossary groups; the literal-grouping limitation rewritten; no asset, prompt or request byte changes | — (no asset) | — (no asset) | `L1:example-report/report.json`, `L1:example-report/report.md`, `L3:reviewed-report/report.json`, `L3:reviewed-report/report.md` |
| U6.5 | UP-D14 | Policy `src/aimediator/assets/configs/balance-review-policy.json`: `near_duplicate_cosine` 0.9, version `balance-review-policy-v3`; new artifact `near-duplicates.json`; report key `near_duplicate_clusters`; no prompt or request byte changes | `b31a46b0ec590fc2c906a6874007bc6805575873f5e9975f2d01564525c242c5` | `0d9e12e6ac539d4b6f9ee20a2731664fd1c41d91d71ca0966f050988017b6972` | L1:<enforce|off|shadow>/manifest.json, L1:<enforce|off|shadow>/near-duplicates.json, L1:example-report/report.json, L1:<enforce|off|shadow>/resource-snapshot/configs/balance-review-policy.json, L1:<enforce|off|shadow>/review-policy-snapshot.json, L2:<enforce|off|shadow>/manifest.json, L2:<enforce|off|shadow>/near-duplicates.json, L2:<enforce|off|shadow>/review-policy-snapshot.json, L3:reviewed-report/report.json |
| U6.4 | UP-D13 | Screening `coarse-v2` (`src/aimediator/collection/screening.py`): Chinese character and mechanic patterns generated from the glossary plus the new collection configuration `configs/feedback-screening-terms.json`; no package asset, prompt or request byte changes | — (new file) | `416c0163eff147ba3cc9cc08e048c12aef87419be8287005ef1c35c76fba1182` (`configs/feedback-screening-terms.json`) | `L4:classify_rules` |

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
| `runs/upgrade/` (the four U3-L runs, their caches, measurements and analysis, inputs, logs, configuration and the bridge and one-off scripts; ignored, not tracked) | `~/Archives/AIMediator/reports/20261105-upgrade-u3-evaluation/` | `SHA256SUMS` at the archive root, 2,257 files, 81,254,355 bytes (row added by U2-V to U6-V, which found the archive without a row) | full runs of the U3-L evaluation (P2); the curated report keeps the manifest and summary | U3-L |
| `runs/upgrade/` (the two U4-L runs, their measurements, route scores, identity check and comparison, the materialized benchmark and synthetic samples with the synthetic cases, run logs and the bridge log, the API configuration and doctor output, the spend before and after, the bridge and one-off scripts; ignored, not tracked) | `~/Archives/AIMediator/reports/20261105-upgrade-u4-evaluation/` | `SHA256SUMS` at the archive root, 721 files, 32,688,012 bytes | full runs of the U4-L evaluation (P2); the curated report keeps the manifest, summary and provenance | U4-L |
| `runs/upgrade/` (the two U4-L2 runs, their measurements, route scores, identity check and comparison with U2-L1 and U4-L, run logs and the bridge log, the API configuration and doctor output, the spend before and after, the bridge and one-off scripts, a manifest; ignored, not tracked) | `~/Archives/AIMediator/reports/20261105-upgrade-u4-fixup-evaluation/` | `SHA256SUMS` at the archive root, 726 files, 32,827,363 bytes | full runs of the U4-L2 rerun (P2); no curated `reports/` directory (D-12) | U4-L2 |
| `tests/test_quality_readers.py` (tracked; added by U4.5, removed by its revert) | `~/Archives/AIMediator/scripts/20261105-upgrade-u4-reverts/tests/test_quality_readers.py` | `SHA256SUMS` in that directory: `c6c232925c767c1c4f0e9014211328b7a79fed2bf75374267c7301be86f34b79` | U4.F3 reverts U4.5 (E-4, fallback (a)); git history keeps the file at `2614453`; outside this record nothing refers to it | U4.F3 |
| `runs/upgrade/` (the two U6-L runs, their measurements, identity checks, comparisons, linkage readings and report exports, run logs and the bridge log, the API configuration and doctor outputs, the spend before and after, the materialized inputs, the run script, tools and the U6.4 and U6.5 helper scripts with the coarse-v1 module copy; ignored, not tracked) | `~/Archives/AIMediator/reports/20261105-upgrade-u6-evaluation/` | `SHA256SUMS` at the archive root, 1,606 files, 61,177,205 bytes | U6-L full runs (P2); the curated summary is `reports/20261105-upgrade-u6-evaluation/` | U6-L |

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

- **D-10 (U3-L) Values of `max_parallel_requests` and `cache_dir` for later
  live runs.** Registered by session U3-L on 2026-11-05; the work order
  (section 3) assigns this choice to the owner after U3-L. Options: (a)
  keep `max_parallel_requests` 1 and no `cache_dir` in the later live runs;
  (b) N 2 (1.31 times faster runs on the benchmark); (c) N 4 (1.22 times);
  (d) a shared cache across the later live runs. Recommendation and action:
  (a), adopted under the owner authorization of 2026-11-05 03:11. The gain
  on the API is small (a benchmark run takes 4 to 5 minutes), parallel
  requests raise each request's elapsed time by a third to three quarters,
  which would bias T4 (quality elapsed per comment, U4) against its serial
  baseline, and every later comparison is paired with a serial reference
  run; a shared cache would answer repeated requests of a later batch from
  an earlier batch, so the measured run would partly measure the cache.
  Nothing changes in `live-config-api.json` or the package defaults; a
  later session may still pass the options for a run that is not compared.

- **D-11 (U4.4) Size of the v2 quality schema, and two consequences
  outside the step text.** Registered by session U4-2 on 2026-11-05.
  (1) The plan 4.2 schema makes `segment_labels` an object with one
  required key per clause segment, so the label schema (about 760
  characters serialized) repeats once per segment in `format` and in the
  user message's `response_schema`: the 41-clause fixture case sends
  31,281 schema characters (v1: one segment item schema for every
  comment). Options: (a) keep the plan's object form, which lets the
  decoding grammar require every segment exactly once, and measure the
  prompt and context effect in U4-L; (b) an array of labels with a
  `segment_id` enum (one item schema, but the grammar can no longer
  require each segment once, which moves coverage errors back to
  validation, against T5); (c) `$defs`/`$ref` for the label object (the
  package validator and the bridge's provider path are untested with
  references). Recommendation and action: (a), adopted under the owner
  authorization of 2026-11-05 03:11; it is the plan's design, a revert
  undoes it, and U4-L reports the largest prompt plus output for U4.6.
  The payload budget of U2.6 (`tests/test_request_payload.py`) keeps its
  quality constant for the rest of the message and adds the per-segment
  part counted from `annotation_schema_v2` itself; segment texts count as
  comment texts. (2) `design_briefs.quality_design_errors` accepted only
  `evidence-quality-v1`, so every `enforce` claim of a v2 run would lose
  its design brief at U4.4: the acceptance of both versions, listed for
  U4.5, is in the U4.4 commit so that the gates pass after it. (3) The
  legacy runner `engine.py` (outside the U4 boundary) still records
  `schema_sha256` of the v1 `annotation_schema` in its quality identity;
  the policy (version `evidence-quality-policy-v2`) and the module hash in
  the same identity mark the change, so nothing is bypassed; the stale
  hash is left for a session whose boundary lists `engine.py` (Deferred).

- **D-12 (U4-L2) Where the curated summary of the fix-up rerun goes.**
  Registered by session U4-L2 on 2026-11-05. The rerun of the two U4-L
  runs after U4.F1 (E-4, option c) needs a curated summary, but the batch's
  report directory `reports/20261105-upgrade-u4-evaluation/` was committed
  by U4-L and is frozen (invariant 2.1.6), and the U4 boundary admits no
  second report directory. Options: (a) the change record carries the
  rows, verdicts and findings, and the full runs with their measurements,
  comparison and identity check go to the archive
  `~/Archives/AIMediator/reports/20261105-upgrade-u4-fixup-evaluation/`
  with `SHA256SUMS` and a manifest, without a `reports/` directory; (b) add
  the files to the U4 report directory (modifies frozen content); (c) a new
  `reports/` directory outside the boundary. Recommendation and action:
  (a), adopted under the owner authorization of 2026-11-05 03:11; it
  changes no frozen content and no boundary, and a revert removes only
  record text. A later session whose boundary allows it may curate the
  archived measurements into a report directory.

- **D-13 (U5-L1) How the adoption rule reads for the U5 steps, and where
  the U5 report goes.** The U5 steps are measured one at a time on the
  extraction-development sample only (UP-D18), and the work order names
  T6 and T7 without saying which one rule 3 reads; D-8 covers only U2.
  The work order also asks every L session to add its summary to one
  curated report, while an existing `reports/` directory is frozen (plan
  2.1.6). Options: (a) rule 1 the gates at the step's commit; rule 2
  transport failures plus generation-failed comments of the extraction
  run at most one above the reference, and every input comment with a
  coverage status; rule 3 T7, the precision of accepted claims, above the
  reference, for each of U5.1 to U5.3 (all three aim at precision, plan
  4.3); rule 4 precision of accepted claims and recall over all labeled
  positions not more than 3 points below the reference; the reference is
  the latest run whose step passed (U5-L1: `u2l1-extraction-development-off`
  after E-3), whole-run values decide, intervals, languages, T6 and the
  other values are reported beside them; a rerun of the entry state
  (`u5r`) is reported and decides nothing; the report
  `reports/20261105-upgrade-u5-evaluation/` is written once, by the last
  L session of this agent, with the summaries of every U5 run and one
  archive, and the earlier L commits record their values here; (b) rule
  3 on T6; (c) a report directory per L session. Recommendation and
  action: (a), adopted under the owner authorization of 2026-11-05 03:11,
  fixed before the U5-L1 verdict was recorded (`u5_compare.py --target
  precision`); T6 falls with precision in every U5 run so far, so (b)
  would not change the U5-L1 verdict; (c) multiplies reports for one
  batch. N-class (record and run output only).

- **D-14 (U6.4) `balanced` and `expansion` write the literal `coarse-v1`.**
  `collection/balanced.py` (`select_balanced`) and
  `collection/expansion.py` (the expansion report) classify with
  `screening` but write `'coarse-v1'` as the screening version, so after
  U6.4 new collections made through them would label `coarse-v2`
  decisions `coarse-v1`. Options: (a) both read `screening.VERSION`; (b)
  keep them and record the mismatch. Recommendation: (a). Not
  implementable here: both files lie outside the U6 boundary, and the
  change alters collection outputs (not N-class, plan rule 1.8), so it is
  **bypassed**; kept: the current state, (b). `screening.VERSION` exists,
  so (a) is a one-line change in each module for a session whose boundary
  lists them (U7 or the owner). No step of U6 depends on it.
- **D-15 (U6.4) Reviewed exclusions in the screening terms file.**
  Generated as the work order states it, the mechanic pattern takes the
  glossary's control-type entries (`Modern`, `现代`, `Classic`, `经典`) and
  the alias `PC` of Punish Counter; on the two raw datasets 4.14 % and
  4.00 % of the decisions change (below the 5 % trigger), and the agent
  review of 40 of them finds 26 worse (accessibility praise, adjectives,
  the platform), 11 better and 3 neutral; the existing test that
  accessibility praise is excluded fails. Options: (a) keep the plain
  generator and change that test; (b) add `excluded_glossary_entries`
  (`system.modern`, `system.classic`: control types, which `CONTROL`
  already handles) and `excluded_glossary_terms` (`PC`, `启动`, `发生`)
  with reasons to `configs/feedback-screening-terms.json`, the reviewed
  collection configuration of plan 4.8; (c) skip U6.4. Recommendation and
  action: (b), adopted under the owner authorization of 2026-11-05 03:11:
  the glossary stays untouched, every exclusion is listed with its reason,
  the test holds, and the changes fall to 0.38 % and 0.19 %. Fully undone
  by a revert of U6.4. Both passes are in
  `reports/20261105-upgrade-u6-evaluation/summary/screening-comparison.json`.

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

  Outcome (session U5, 2026-11-05, before U5.1): settled under the owner
  authorization of 2026-11-05 03:11, because U5 builds on U2.3 (plan 6)
  and the verification of U2 runs only after U6 (UP-D20). Option (c) was
  measured first (`u2r-extraction-development-off`, the code of `39a1efd`
  through bridge version 2; see "U2-R" under "Live evaluations"): against
  the U2-L0 reference, precision of accepted claims −0.3 points and recall
  −0.8 points, within the 3-point margin; rules 2 and 3 hold. Adopted:
  (b) on the evidence of (c), U2.3 kept; no revert and no fix-up step
  U2.F1; the extraction budget of the U2.6 payload test stays. The U5
  reference is `u2l1-extraction-development-off`, the state of HEAD's
  extraction and relevance code (U2.2 to U2.4; later steps before U5 are
  behavior-neutral in `off` or change only quality requests). U2-V
  carries the finding of "U2-R" on U2.4. Blocked: nothing.

- **E-4 (U4-L) U4.4 and U4.5 fail adoption rules 2 and 3.** Raised on
  2026-11-05 by session U4-L. On the benchmark 4 comments fail quality
  against 2 for the U2-L1 reference (margin 1), and first-attempt validity
  is 18/23 against 21/24 (work order section 6, fourth trigger); on the
  synthetic sample validity and route agreement rise (16/16 and 14/16
  against 13/16 and 11/16) and T4 falls to 60.4 % (see the U4-L verdicts).
  Options: (a) revert U4.4 and U4.5 as fix-up steps of the U4 review (plan
  1.7, 5.4; U4.1 to U4.3 are N and stay); (b) keep both against the rule,
  with the reason recorded (synthetic gains, the T4 gain, the benchmark
  loss inside its interval, one remaining failure class); (c) a fix-up
  prompt step U4.F1 aimed at that class (a concrete point that selects a
  clause labeled `general_opinion`), measured by a rerun of the two U4-L
  runs, with (a) if rule 2 or the fourth trigger still fails.
  Recommendation: (c) with (a) as its fallback. Adopted under the owner
  authorization of 2026-11-05 03:11 as far as this session's role allows:
  the live session does not revert (plan 10.1); this session records U4-L,
  executes U4.6 and U4.7, and then executes U4.F1 with its rerun only if
  the step, the runs and their record can be committed by 06:00; whatever
  it does not finish passes to U4-V, which applies the rest of the adopted
  recommendation. Blocked: nothing in this session.

  Outcome (U4-L2, same day): U4.F1 was committed (`385f744`) and measured
  by U4-L2; rule 2 still fails (5 quality-failed benchmark comments
  against 2), so the fallback (a) applies. Adopted action, under the same
  authorization: U4-V, which applies the fix-up reverts of failed steps
  (UP-D20, session 6 of the chain), reverts U4.F1, U4.5 and U4.4 in that
  order (plan 1.7, `fix: revert ...` with `Step:` and `Reverts:` lines, the
  lock regenerated by each revert), records the documents of U4.7 that
  then describe a contract no longer in effect (ADR 0005 status,
  evidence-quality.md section 3.3, the emotion design note, design/cli.md
  section 5) as a fix-up documentation step, and keeps U4.1 to U4.3 (N,
  unused by the pipeline). This session does not revert: a live session
  never reverts (plan 10.1), and the reverts are fix-up steps of the
  review. The owner's own review may decide against the rule (plan 5.4);
  the reasons for keeping are the synthetic gains (validity 15/16 and
  16/16 against 13/16, routes 14/16 against 11/16), T4 at 60 % and no
  offset errors, against 4 to 5 failed benchmark comments instead of 2.

  Fix-ups (session U6, 2026-11-05, before U6.7): the session's prompt
  moved the adopted reverts from the verification session to U6, because
  later commits would make them harder; the verification session checks
  them. U4.F2 reverts U4.F1 (`385f744`); U4.F3 reverts U4.5 (`2614453`);
  U4.F4 reverts U4.4 (`09a79e3`). Each revert regenerated the lock (U4.F2
  and U4.F4 the keys of the reverted step; U4.F3 none) and passed the
  gates. U4.1 to U4.3 (N, unused by the pipeline) and U4.7 stay; U4.F5
  adds one sentence to the three design documents that describe the v2
  contract (the sentence in ADR 0005 is bypassed: D3).

- **E-5 (U5-L2) U5.2 fails adoption rule 3.** Raised on 2026-11-05 by
  the U5 session at U5-L2. Precision of accepted claims, the metric the
  step targets (D-13), is 61/81 (75.3 %) against 58/77 (75.3 %) for the
  U5.1 run, −0.02 points; rules 2 and 4 hold (recall +1.6 points); the
  subjects gate quarantined no claim (see the U5-L2 verdicts). Options:
  (a) revert U5.2 as a fix-up step of the U5 review (plan 1.7, 5.4),
  which also removes `subjects` from the expected entries of the U5.3
  examples and from `tests/test_prompt_examples.py` when U5.3 is kept;
  (b) keep U5.2 against the rule, with the reason recorded (a fail-closed
  gate that costs no recall, precision equal within 0.02 points, the
  examples of U5.3 built on it); (c) rerun U5-L2 to separate the step
  from run-to-run variation (the entry rerun of U5-L1 moved precision by
  1.0 points with unchanged code). Recommendation: (a), the plan's rule:
  the step adds 5 % prompt and 11 % output tokens per extraction request
  and has no measured effect on precision or on the gate. Adopted under
  the owner authorization of 2026-11-05 03:11 as far as this session may:
  the session's instruction keeps a failed step for the review and
  forbids a revert here, so U5.2 stays, U5.3 and U5-L3 proceed on top of
  it (U5-L3 keeps the U5.1 run as its reference, D-13), and the review of
  batch U5 (the verification session, UP-D20) applies (a), after any
  revert that U5-L3 calls for (E-6 numbers them: U5.F1 reverts U5.3,
  U5.F2 reverts U5.2). Blocked: nothing in this session.

- **E-6 (U5-L3) U5.3 fails adoption rules 3 and 4.** Raised on
  2026-11-05 by the U5 session at U5-L3. Against the U5.1 run, precision
  of accepted claims is 73.2 % against 75.3 % (−2.1 points) and recall
  42.3 % against 47.2 % (−4.9 points, beyond the 3-point margin); T6
  rises to 42.9 % (see the U5-L3 verdicts). The loss is English (recall
  23/46 against 30/46). Options: (a) revert U5.3 as fix-up step U5.F1 of
  the U5 review (plan 1.7, 5.4), before the revert of U5.2 that E-5
  recommends (U5.F2), then a documentation fix-up of U5.4 for the
  reverted parts; (b) keep U5.3 against the rule; (c) a prompt fix-up
  with other examples, measured by a rerun. Recommendation: (a), the
  plan's rule: both intervals include 0, but no metric moved in the
  intended direction and the examples cost 8 % more prompt tokens per
  extraction request.
  Adopted under the owner authorization of 2026-11-05 03:11 as far as
  this session may: the step stays for the review (the session's
  instruction forbids its own revert); the verification session of
  UP-D20 reverts U5.3 (U5.F1) and U5.2 (U5.F2, E-5) in that order, with
  `Step:` and `Reverts:` lines and the lock regenerated by each revert,
  and updates the U5.4 text of balance-analysis.md and design/cli.md for
  the reverted parts (U5.F3); U5.1 stays. Blocked: nothing in this
  session.

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

### 2026-11-05 U2-V

- Range: `upgrade-u1..c6452d8`; 14 commits: U2.1 `93536cd`; U2.2
  `faee371`; U2.3 `39a1efd`; U2.4 `b7d1cc5`; U2-1 session log `6926262`;
  U2-L1 `5f6d2f6` (E-2), `5566ac1` (D-8) and `b55d48c`; the owner
  amendments `9f113cc` (UP-D19) and `79cfbb5` (UP-D20); U2-L0 `e6c7917`;
  U2.6 `cd3fd48`, `fb49f79` and `c6452d8`. U2.5 and U2-L2 are skipped
  (UP-D20). The U2 review also covers `e34e08d` (U2-R, E-3), committed by
  the U5 session. Verification session U2-V to U6-V (UP-D20, chain
  session 6), which implemented none of U2 to U6. The checklist follows
  UP-D20's shorter form: the gates, the foreign directory and the
  installed-wheel acceptance ran once, at `6a77e5b` (HEAD at session
  start; results in the U6-V note); each batch was checked for boundary
  and commit hygiene, lock-fixture changes, behavior-change hashes and
  recorded live verdicts. Python 3.14.8, NumPy 2.4.6. Scratch output went
  to the ignored `runs/upgrade/verify/` and to temporary directories. No
  live run, no network use, nothing written to `reports/`, `data/` or the
  archive.
- Checks:
  1. Boundary and commit hygiene (plan 8.8): pass, with the exceptions
     recorded in the U2-2 session log. Outside the work-order pattern:
     `docs/plans/pipeline-upgrade.md` and the six handoffs (the owner
     amendments UP-D19 and UP-D20), `reports/20261105-upgrade-api-reference/`
     (the U2-L0 report named by the work order's UP-D19 note) and
     `scripts/maintenance/check_rules.py` (E-2). The hygiene command
     prints nothing. Every subject uses a P5 type. The one test-only
     commit, `cd3fd48`, is `chore`. No commit message or added line holds
     attribution or a `/home/` path.
  2. Lock fixture: pass. Only `faee371` (U2.2, UP-D04), `39a1efd` (U2.3,
     UP-D05) and `b7d1cc5` (U2.4, UP-D07) change
     `tests/fixtures/behavior-lock.json`, and each lists its decision and
     its `Lock:` paths. U2.1 (`Lock: unchanged`) and U2.6 leave the
     fixture unchanged.
  3. Behavior changes: pass. The table lists the six prompt assets that U2
     changes: `evidence-quality.{en,zh}` (U2.2) and `relevance.{en,zh}`
     and `retrieval-review.{en,zh}` (U2.4). Every old and new SHA-256,
     recomputed from `git show <commit>^:<path>` and
     `git show <commit>:<path>`, equals the table. No other asset changes
     in the range.
  4. Payload test and demo request: pass. `tests/test_request_payload.py`
     (5 tests) passes. The 76 quality requests of a HEAD demo hold only
     the user keys `comments`, `language`,
     `character_normalization_reference` and `response_schema`, and none
     of `source`, `quality_contract` or `attempt`. Since U4.F4, HEAD sends
     the U2.2 quality view again.
  5. Live verdicts: pass. U2-L1 records a verdict for each B step (read
     as D-8): U2.2 and U2.4 kept; U2.3 fails rule 4 (recall −4.9 points)
     and is escalated as E-3. The U5 session settled E-3 before U5.1:
     measured alone (U2-R), U2.3 is −0.3 points of precision and −0.8 of
     recall, so it is kept. U2.5 is skipped (UP-D20) and needs no
     verdict.
  6. Gates, foreign directory and wheel at HEAD: pass (U6-V note). ADR
     0003 (`docs/decisions/0003-model-visible-request-views.md`, Active)
     and its index row exist.
- Targets (U2-L1, not gates): T1 66.2 % of the U2-L0 baseline, not met;
  T2 48.0 %, met; T3 75.0 %, not met.
- Findings: the U2-R finding on U2.4 is carried to the review below.
- Measurements: tests 341 in 33.7 s at HEAD; demo 0.97 s; lock green.
- Result: accepted, tag `upgrade-u2-review`; the review follows.

### 2026-11-05 U2 review (recorded by U2-V)

Recorded under the owner's standing instruction and the owner
authorization of 2026-11-05 03:11. The owner did not give this review in
person. Basis: the U2-V note above, the U2-L1 verdicts, E-3 and its
outcome, and "U2-R" under "Live evaluations". Rule: the adoption rule
of plan 5.4. Steps that passed are kept and steps that failed are
reverted as fix-up steps.

| Step | Class | Verdict | Review outcome |
| ---- | ----- | ------- | -------------- |
| U2.1 | N | lock unchanged | kept |
| U2.2 (UP-D04) | B | kept by U2-L1 | kept |
| U2.3 (UP-D05) | B | failed rule 4 in U2-L1 (E-3); passed when measured alone (U2-R) | kept. The U5 session decided this before U5.1 under the owner authorization (E-3 outcome: option (b) on the evidence of (c)). This review records that decision and does not decide it again. No fix-up step U2.F1 |
| U2.4 (UP-D07) | B | kept by U2-L1 (relevance agreement 64/69 against 63/69) | kept. U2-R found that most of the extraction-recall loss of E-3 comes with U2.4 (through admission) and run-to-run variation. That effect is not a D-8 metric of U2.4, and every interval includes 0, so it stays a finding for U7.1 and U7.2. U7 accepts on the adopted configuration, which includes U2.4 |
| U2.5 with U2-L2 (UP-D06) | B, L | skipped (UP-D20) | not reviewed; the UP-D06 trial did not run |
| U2.6 | N | lock unchanged | kept; the payload budgets (U2-L1 plus 20 %) stay |

Fix-up steps: none. Under plan 10.5 and UP-D18, U2-V sets `upgrade-u2`
on this commit, after `upgrade-u2-review`. The owner may still decide
against the rule (plan 5.4) and revert a kept step in a later session.

### 2026-11-05 U3-V

- Range: `c6452d8..d9b2de9`; 7 commits: U3.1 `335a5e2`; U3.2 `335b4bc`;
  U3.3 `aaf93ae`; U3.4 `1a5d520`; U3-L `ce09d19`; U3.5 `f7185bc`; session
  log `d9b2de9`. Under UP-D20, U3 started without the U2 tag, so the
  last U2 commit, `c6452d8`, stands in for `upgrade-u2`. The checklist
  was shortened as in the U2-V note.
- Checks:
  1. Boundary and commit hygiene (plan 8.8): pass. The boundary check
     prints nothing and so does the hygiene check. Every subject uses a
     P5 type.
  2. Lock fixture: pass. U3.1 (`Lock: unchanged`) and U3.5 do not touch
     it. U3.2 (UP-D08), U3.3 and U3.4 (UP-D09) name their decisions and
     list their paths.
  3. Request digests: pass. The lock diff from `c6452d8` to `d9b2de9`
     (468 to 771 keys, 407 changed) touches no `requests/` entry. The
     changes are the ones the three commit bodies list:
     `L1:<off|shadow|enforce>/manifest.json` and `resolved-config.json`,
     `L1:example-report/report.json` and `L3:reviewed-report/report.json`
     (configuration and run identity, U3.2 and U3.3); the three
     existence-only keys `L2:<mode>/code-snapshot/cache.py` (U3.3); and
     396 `embeddings/` keys (the layout of U3.4).
  4. Concurrency and cache: pass. The suite holds the U3 tests and
     passes. In the U3-L warm-cache run no chat request and no retrieval
     embedding request reached the bridge; the one request was the
     availability probe. Its 259 JSON files are byte-identical to the cold
     run apart from times.
  5. Gates, foreign directory and wheel at HEAD: pass (U6-V note). ADR
     0004 (`docs/decisions/0004-bounded-concurrency-and-shared-cache.md`,
     Active) and its index row exist.
- Behavior changes: U3 changes no asset. The table rows U3.2 to U3.4 name
  only configuration, identity and layout, which agrees with item 3.
- Live readings: T8 reached 1.25 times against the target of 1.4, so it
  is not met; it is indicative under UP-D19. U3 changes no
  model-visible content, so no adoption rule applies. The values of D-10
  stand.
- Finding, fixed in this commit: "Archive and deletions" had no row for
  the U3-L archive. The archive exists with `SHA256SUMS` (2,257 files),
  and a row now records it.
- Result: accepted, tag `upgrade-u3`.

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

### 2026-11-05 U3-1 and U3-L (implementation and live)

- Steps: U3.1, U3.2, U3.3, U3.4, U3-L and U3.5 done; none started and
  stashed.
- State: HEAD is this entry's commit (parent `f7185bc`); tests 296; lock
  updated by UP-D08 (U3.2, 8 keys) and UP-D09 (U3.3, 11 keys; U3.4,
  `embeddings/` keys only, 771 keys), green after each step; U3.1 and U3.5
  left it unchanged; rule check 0. Foreign working directory: 296 pass.
  Installed-wheel acceptance at `1a5d520`: `"passed": true`, 18 commands.
- Findings: entry without the tag `upgrade-u2` (UP-D20): the U2-L1 verdicts
  and U2.6 are recorded; the U2 step that failed the adoption rule is U2.3
  (E-3, rule 4, recall −4.9 points), kept until the review. Resume
  procedure: clean tree, no `WIP Step` stash, gates passed. The owner
  authorization of 2026-11-05 03:11 is added after the standing
  instruction. D-9 (the request context in the shared key; `operations`
  imports `cache`) and D-10 (later live runs keep `max_parallel_requests` 1
  and no `cache_dir`) adopted under that authorization. U3-L: bridge
  `openrouter-bridge-2`, digests and configuration equal to the record,
  `doctor` passed; T8 1.25 times, not met (indicative; per-request latency
  rises with N on the API); the warm run made no fresh chat or retrieval
  embedding request and reproduced run 1 exactly; batch 8 against 32 changed
  no retrieval decision (largest score difference 0.0035), while two fresh
  runs at batch 32 differed in one decision; no escalation trigger of work
  order section 6 raised. Spend of this session 0.0288 USD (bridge total
  0.1486 USD). Boundary check of plan 8.8 from `c6452d8` and the commit
  hygiene check print nothing; no request digest of the lock changed. With
  the ordered executor, an interruption lets the running request finish
  before the run stops (work order U3.1), also at N 1, where the serial
  code stopped inside the request. Nothing bypassed.
- Next: U4 (work order U4, sessions U4-1 and U4-L in one agent, UP-D20);
  U3-V runs in the verification session after U6; blockers: none.

### 2026-11-05 U4-1, U4-2, U4-L, U4-3 and U4-L2 (implementation and live)

- Steps: U4.1, U4.2, U4.3, U4.4, U4.5, U4-L, U4.7, U4.F1 and U4-L2 done;
  U4.6 skipped (measured context size: largest prompt plus output 14,346
  tokens, at least 6,000 in 5 requests); none started and stashed.
- State: HEAD is this entry's commit (parent `81ccfd8`); tests 316; lock
  updated by UP-D10 (U4.4, 100 keys; U4.F1, 25 keys; 771 keys), green
  after every step; U4.1 to U4.3, U4.5 and U4.7 left it unchanged; rule
  check 0. Foreign working directory: 316 pass. Installed-wheel
  acceptance at `81ccfd8`: `"passed": true`, 18 commands.
- Findings: entry without the tags `upgrade-u2` and `upgrade-u3`
  (UP-D20); resume procedure: clean tree, no `WIP Step` stash, gates
  passed; the owner authorization of 03:11 was already in the record. U4.2
  found that all 38 fixture cases map (124 v1 segments onto 138 clauses),
  so no escalation and no fallback fixture. D-11 (the per-clause label
  schema kept as the plan specifies; design briefs accept both versions
  in U4.4 so that its gates pass; the legacy identity hash deferred) and
  D-12 (the U4-L2 summary in the record and the archive, since the U4
  report directory is frozen) adopted under the owner authorization.
  U4-L: reference the U2-L1 rows (U2.2 kept; named in the U4-L section);
  bridge `openrouter-bridge-2`, digests and configuration equal to the
  record, `doctor` passed; T4 11.2 s per comment (60.4 % of the reference,
  indicative, target not met); T5 78.3 % on the benchmark, not met; no
  offset, quote or coverage error; synthetic validity 16/16 and route
  agreement 14/16 against 13/16 and 11/16; U4.4 and U4.5 fail adoption
  rules 2 (4 quality-failed benchmark comments against 2) and 3 (T5):
  escalation E-4, whose recommendation (c), a prompt fix-up U4.F1 with the
  revert as fallback, was adopted under the authorization. U4-L2 measured
  U4.F1: rule 2 still fails (5 against 2), so the fallback applies and
  passes to U4-V (revert U4.F1, U4.5 and U4.4, then a documentation fix-up
  for U4.7); this session did not revert (plan 10.1). Spend of this
  session 0.0365 USD (U4-L 0.0179, U4-L2 0.0186; bridge total 0.1851 USD,
  2.79 USD below the refusal point). Boundary check of plan 8.8 from the
  U4 entry commit `d9b2de9` (no `upgrade-u3` tag) and the commit hygiene
  check print nothing; `cases.json` and `data/evaluation` have no diff;
  `qualify` has no diff. The identity tool `check_api_identity.py` pins
  bridge version 1, so it reports `passed: false` for version-2 runs while
  every item holds. Nothing bypassed.
- Next: U5 (work order U5, sessions U5-1 to U5-L3 in one agent, UP-D20);
  U4-V runs in the verification session after U6 and carries E-4 (the
  reverts of U4.F1, U4.5 and U4.4) to the review of batch U4; blockers:
  none.

### 2026-11-05 U5-1 to U5-4 and U5-L1 to U5-L3 (implementation and live)

- Steps: U2-R (E-3), U5.1, U5-L1, U5.2, U5-L2, U5.3, U5-L3 and U5.4
  done; none started and stashed.
- State: HEAD is this entry's commit (parent `4458779`); tests 326; lock
  updated by UP-D11 (U5.1, 18 keys; U5.2, 50 keys; U5.3, 32 keys; 771
  keys), green after every step; U5.4 left it unchanged; rule check 0.
  Foreign working directory: 326 pass. Installed-wheel acceptance at
  `90a7dd1`: `"passed": true`, 18 commands.
- Findings: entry without the tags `upgrade-u2` to `upgrade-u4`
  (UP-D20); resume procedure: clean tree, no `WIP Step` stash, gates at
  the entry commit `d025bf3` passed (316 tests, rule check 0, lock green;
  checked in a temporary worktree); the owner authorization of 03:11 was
  already in the record. E-3 settled before U5.1 under that
  authorization: U2.3 measured alone (`u2r`, code of `39a1efd`) holds
  rule 4 against U2-L0 (precision −0.3, recall −0.8 points), so U2.3 is
  kept and the U5 reference is `u2l1-extraction-development-off`; the
  U2-L1 recall loss arises with U2.4 and run-to-run variation (finding
  for U2-V). D-13 (rule reading for U5: rule 3 on T7; one report written
  by the last L session) adopted under the authorization. Verdicts: U5.1
  kept (precision +1.0, recall +3.3 points, T6 33.6 %); U5.2 fails rule
  3 (precision −0.02 points; the subjects gate quarantined no claim):
  E-5; U5.3 fails rules 3 and 4 (precision −2.1, recall −4.9 points, the
  loss English, T6 42.9 %): E-6. Adopted action for both: the
  verification session reverts U5.3 (U5.F1) and U5.2 (U5.F2) and fixes
  the U5.4 text (U5.F3); this session did not revert (its instruction).
  An entry rerun (`u5r`, decides nothing) moved precision by 1.0 point
  with unchanged code: differences of a few points are within run-to-run
  variation. Deviations: `subjects` also carries `maxItems` (the bridge
  drops `uniqueItems`); U5.4 was committed while U5-L3 ran, so its text
  names E-5 but not E-6; every run used a `git archive` copy of its
  commit. One development comment (`加强曼侬`, 4 characters) occurs in
  the extraction prompt through a rule line that predates U5, not through
  an example (U5-V checklist item 5). T6 met by U5.1 and U5.2, T7 met by
  none. Spend of this session 0.1246 USD for five runs with their
  `doctor` calls (0.1851 to 0.3097 USD; 2.67 USD below the refusal
  point). Boundary check of plan 8.8 from `d025bf3` and the commit
  hygiene check print nothing; the verify prompts have no diff. Nothing
  bypassed.
- Next: U6 (work order U6, chain session 5); U5-V runs in the
  verification session after U6 and carries E-5 and E-6 (U5.F1 to U5.F3)
  to the review of batch U5; blockers: none.

### 2026-11-05 U6-1 to U6-3 and U6-L (implementation and live)

- Steps: E-4 fix-ups U4.F2 (revert of U4.F1), U4.F3 (revert of U4.5),
  U4.F4 (revert of U4.4) and U4.F5 (documents); U6.7, U6.1, U6.2, U6.5,
  U6.4 and U6-L done; U6.3 and U6.6 skipped (UP-D20); none started and
  stashed.
- State: HEAD is this entry's commit (parent `c008cef`); tests 341
  (326 at entry, 320 after U4.F3, which removed the 6 tests of U4.5); lock
  updated by UP-D10 (U4.F2, 25 keys; U4.F4, the 100 keys of U4.4), UP-D12
  (U6.1, 32 keys with the 3 existence-only `code-snapshot/topics.py`
  keys; U6.2, 4 report keys), UP-D14 (U6.5, 23 keys) and UP-D13 (U6.4,
  `L4:classify_rules`); 780 keys; green after every step; U4.F3, U4.F5
  and U6.7 left it unchanged; rule check 0. Foreign working directory:
  341 pass. Installed-wheel acceptance at `4555fa4`: `"passed": true`, 18
  commands.
- Findings: entry without the tags `upgrade-u2` to `upgrade-u5`
  (UP-D20); resume procedure: clean tree, no `WIP Step` stash, gates at
  the entry commit `dc05a37` passed (326 tests, rule check 0, lock green);
  the owner authorization of 03:11 was already in the record. E-4
  executed as adopted, moved here from the verification session by this
  session's prompt: each revert resolved only record and lock conflicts
  (the record kept its rows as history, the lock was regenerated), the
  code merged with the U5 commits without conflict; `tests/test_quality_readers.py`
  archived with `SHA256SUMS`; the deferred legacy quality identity item
  (D-11, part 3) no longer applies; the sentence in ADR 0005 is
  **bypassed** (D3), the three design documents carry it. U6.1: only exact
  terms resolve; a term inside a longer matched term is dropped and a
  target naming several entries is a candidate (`shoryuken startup` names
  the move and the mechanic Startup). U6.2: `topic_literal_normalized`
  stays for `presentation` (outside the boundary). U6.5: threshold 0.90
  from the 114 development comments; only 5 pairs reach it, so 5 instead
  of 20 are recorded above. U6.4: D-15 (reviewed exclusions in the terms
  file; changes 0.38 % and 0.19 % instead of 4.14 % and 4.00 %), D-14
  **bypassed** (`balanced` and `expansion` write `coarse-v1`, outside the
  boundary, not N-class); the comparison and the owner's review, adopted
  under the authorization after the agent review, were committed before
  the code (`f7b8745`, then `4555fa4`). U6-L: runs at the U6.5 commit
  `a05b0ee` while U6.4 was written, identity-equal to HEAD (U6.4 changes
  only `collection/` and root `configs/`); no U6 step is under the
  adoption rule; no regression against U2-L1 and U5-L3; 5 of 117 grounded
  claims resolve (100 have no target), report groups 8 and 8, 3
  near-duplicate clusters; the U5.3 and U6 runs share their extraction
  code yet differ by 4 points of recall, which bears on E-6. Boundary
  check of plan 8.8 from `dc05a37`: only the U4 fix-up files
  (`evidence_quality.py`, `legacy_review.py`, `design_briefs.py`,
  `evidence-quality-policy.json`, all in the U4 boundary) fall outside the
  U6 pattern; the commit hygiene check prints nothing; the glossary,
  `data/`, `cases.json` and `docs/decisions/` have no diff. Spend of this
  session 0.0283 USD (0.3097 to 0.3380 USD; 2.64 USD below the refusal
  point).
- Next: the verification session (chain session 6: U2-V to U6-V with
  the reviews, the fix-up reverts of E-5 and E-6 (U5.F1 to U5.F3) and the
  batch tags); it checks U4.F2 to U4.F5 for U4-V and runs U6-V from
  `upgrade-u5`; blockers: none.

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

- **Legacy quality identity hash** (D-11, part 3, from U4.4). `engine.py`
  records `schema_sha256` of the v1 `annotation_schema(['COMMENT_ID'])` in
  the legacy runner's quality identity; since U4.4 the legacy runner sends
  v2 requests. A session whose boundary lists `engine.py` replaces it with
  the hash of the v2 schema builder's output for a fixed example, with its
  lock update; the policy version and module hash in the same identity
  already mark the change. No longer needed since U4.F4 (2026-11-05): the
  revert of U4.4 returns the legacy runner to v1 requests, which the
  recorded v1 schema hash describes.
