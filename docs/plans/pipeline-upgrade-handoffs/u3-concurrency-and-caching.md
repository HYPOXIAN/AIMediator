# Handoff U3: Concurrency and caching

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-04
- Applies to: [pipeline upgrade plan](../pipeline-upgrade.md) batch U3; entry tag `upgrade-u2`

Work order for batch U3. The steps are defined in plan section 7 (U3) and
the target in plan 4.5 and 4.6. Defaults keep today's behavior: one request
at a time and no shared cache. The live session measures what the new
settings gain and checks that replay stays exact.

## 1. Mission

- Run independent requests through an ordered executor that keeps serial
  artifact order (LAT-04).
- Expose the request limit as `max_parallel_requests` (UP-D08).
- Share model responses across runs through a content-addressed cache with
  per-request reuse provenance (LAT-06, UP-D09).
- Cache embeddings per text and embed in batches of 32 (LAT-06, UP-D09).

## 2. Entry conditions

- Tag `upgrade-u2` exists. Clean tree, no `WIP Step` stash, the gates pass.
- UP-D08 and UP-D09 are answered.
- Quality requests carry no run identity (U2.2 done and kept). If U2.2 was
  reverted, U3.3 is blocked: escalate.

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/(cache|runner|pipeline|run_store|operations|config|cli|retrieval|inference|fixture_transport|engine|measurement)\.py$|tests/|scripts/experiments/|reports/[0-9]{8}-upgrade-u3-evaluation/|docs/records/[0-9]{8}-pipeline-upgrade\.md$|docs/decisions/0004-[a-z0-9-]+\.md$|docs/design/cli\.md$|docs/guides/cli-usage\.md$|docs/README\.md$)
```

- **Allowed**: the listed modules within plan 4.5 and 4.6; the `cache` row
  and the changed `runner` row of the layering table (UP-D01); the lock
  fixture in U3.2 to U3.4 and for the three existence-only keys of
  `cache.py`; ADR 0004; the guide and design/cli.md.
- **Not allowed**: request bytes of chat requests; assets; the domain gates;
  artifact names and order, except the `embeddings/` layout of U3.4 and the
  new `reuse-provenance.json`.
- **Decisions in force**: UP-D01 (rows), UP-D08 (U3.1, U3.2), UP-D09 (U3.3,
  U3.4).
- **Owner actions**: start the model service with `OLLAMA_NUM_PARALLEL` of
  at least the tested limit for U3-L; choose the default value for later
  live runs after U3-L.

## 4. Sessions

### U3-1 (implementation): steps U3.1 to U3.5

```text
You are session U3-1 (implementation) of the AIMediator pipeline upgrade,
steps U3.1 to U3.5 (U3.5 after U3-L).
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/pipeline-upgrade-handoffs/u3-concurrency-and-caching.md); the
plan docs/plans/pipeline-upgrade.md, sections 1 to 4, the U3 part of
section 7, and sections 8 and 10; design/cli.md sections 5 to 7; the change
record.
Task: execute your steps in order, inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates, including the
  behavior lock, after every commit.
- One kind of operation per commit, with "Step: U3.x" and the step's
  "Decision: UP-Dnn" in the body.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **U3.1** N (LAT-04)
  - An ordered executor in `pipeline`: `concurrent.futures.ThreadPoolExecutor`,
    a window of at most N submitted units, results committed in input order
    on the calling thread. N is a parameter fixed at 1 in this step.
  - Units as in plan 4.5. An extraction batch and its split retries form
    one unit and run in serial order inside it, so the queue order of
    `extract_claims` is preserved.
  - Every write of the write schedule (design/cli.md section 5) happens in
    the commit callback, in the current order.
  - `KeyboardInterrupt`: cancel pending units, let running ones finish or
    fail, commit nothing out of order, and propagate as today.
  - Lock unchanged; the resume and interruption tests pass.
- **U3.2** B (UP-D08)
  - Configuration key `max_parallel_requests` (integer 1 to 8, default 1),
    validated in `config.validate`; `aimediator analyze
    --max-parallel-requests`. Configuration files without the key stay
    valid, because resolution starts from the defaults.
  - `Runner`: a lock per request identity around `_response`; the journal
    callback and `progress` serialized in `operations.analyze` with one
    lock.
  - `aimediator init` output and the default configuration change, so the
    lock changes (`resolved-config.json`, the run identity). List the
    paths.
  - A test with a fixture transport that sleeps and records concurrency:
    at most N requests in flight, artifacts equal to an N = 1 run.
  - Guide and design/cli.md section 6.
- **U3.3** B (LAT-06, UP-D09)
  - Module `cache` (infrastructure; imports `common`): `SharedCache(root)`
    with `lookup(key)` and `store(key, request, response)`; files
    `chat/<key[:2]>/<key>/request.json` and `response.json`, written with
    `common.write`.
  - Key as in plan 4.6. `Runner` receives the model digests and the service
    version from the run identity.
  - Lookup order: run journal, then shared cache, then transport. A hit
    writes `response.json` with `elapsed_seconds` 0 and
    `reuse-provenance.json`; a miss stores successful responses after the
    transport returns.
  - Configuration key `cache_dir` (default `null`) and
    `aimediator analyze --cache-dir`; a relative path resolves against the
    configuration file, as other user paths do.
  - `measurement` counts `reuse-provenance.json` as reuse (plan 5.2).
  - Tests: two fixture runs with the same cache directory; the second makes
    no chat transport call and writes artifacts equal to the first, except
    the provenance files and elapsed times.
- **U3.4** B (LAT-06, UP-D09)
  - `retrieval.retrieve`: one record per text,
    `embeddings/<SHA-256 of model, endpoint and text>.json` holding the
    model, the text and its vector; embed only missing texts, in batches of
    32, in input order; then the same scoring.
  - The shared cache stores embedding records under `embedding/` with the
    model digest in the key.
  - `retrieval.json` keeps its schema.
- **U3.5** N, after U3-L: ADR `docs/decisions/0004-bounded-concurrency-and-shared-cache.md`
  with the U3-L measurements; design/cli.md sections 6 and 7; guide
  (options, the cache directory, reuse provenance, the reproducibility
  consequence of plan 2.3).

### U3-L (live)

```text
You are session U3-L (live) of the AIMediator pipeline upgrade. You run on
the owner's machine with the local model service, started with
OLLAMA_NUM_PARALLEL set by the owner.
Read: RULES.md; this work order; the plan, sections 1, 4.5, 4.6, 5 and 8.6
and the U3 part of section 7; the change record.
Task: check the environment, run the U3-L runs at the U3.4 commit, measure
them, archive the full runs, and record the results in the change record
and in reports/<YYYYMMDD>-upgrade-u3-evaluation/, committed with
"Session: U3-L" in the body.
Rules: never open, print or copy .env. If the environment differs from the
U0.6 record in anything but OLLAMA_NUM_PARALLEL, or doctor fails, stop and
report. Never add attribution.
Finish with a session-log entry; your final message repeats it.
```

Runs, all on the benchmark in `shadow`, each with a new empty
`runs/upgrade/cache-<n>/` unless stated:

1. `u3-benchmark-shadow-p1`: `max_parallel_requests` 1, cold cache.
2. `u3-benchmark-shadow-p2`: 2, cold cache. T8 against run 1.
3. `u3-benchmark-shadow-p4`: 4, cold cache, only if the owner confirms the
   memory for 4 slots.
4. `u3-benchmark-shadow-warm`: 1, the cache of run 1. Must make no fresh
   chat or embedding request and give artifacts equal to run 1 apart from
   provenance and elapsed times.
5. Retrieval check: the largest absolute difference of positive and
   negative scores and the number of changed `retrieval_related` decisions
   between run 1 and `u0-benchmark-shadow` (batch 8 against 32).

Record per-stage throughput (requests and output tokens per second) and the
memory the service reports in `/api/ps` during runs 2 and 3.

### U3-V (verification)

```text
You are session U3-V (verification) of the AIMediator pipeline upgrade. You
did not implement batch U3. Change nothing except the change record.
Read: RULES.md; this work order; the plan, sections 1, 2, 4.5, 4.6, 8 and
10 and the U3 part of section 7; ADR 0004; the change record.
Task: run every item of the U3-V checklist on HEAD, and append a
verification note committed with "Session: U3-V". If every item passes, tag
that commit upgrade-u3. Otherwise record fix-up steps U3.F1 and so on and
stop without tagging. Never add attribution. Your final message repeats the
verification note.
```

Checklist:

1. Boundary and commit hygiene from `upgrade-u2` (plan 8.8).
2. The lock fixture is unchanged by U3.1 and U3.5; U3.2 to U3.4 name their
   decisions and list their paths.
3. The chat request digests of the lock fixture are identical at
   `upgrade-u2` and HEAD (`git diff upgrade-u2..HEAD -- tests/fixtures/behavior-lock.json`
   touches no request-digest entry), and every other fixture change is one
   that U3.2 to U3.4 list in their commit bodies (configuration, identity,
   `embeddings/` layout, existence-only `cache.py` keys).
4. The concurrency and cache tests pass; the warm-cache run of U3-L made
   no fresh request.
5. Gates, foreign directory and wheel acceptance pass; ADR 0004 and its
   index row exist.

## 5. Exit and handoff out

- Exit tag: `upgrade-u3`, set by U3-V.
- The next work order is [U4](u4-quality-segmentation.md).

## 6. Escalation triggers

- Ordered commit would need to move, merge or reorder an artifact write.
- A warm-cache run makes a fresh request or produces different artifacts.
- Retrieval decisions change between batch sizes 8 and 32.
- The service cannot hold the tested number of slots in memory.
