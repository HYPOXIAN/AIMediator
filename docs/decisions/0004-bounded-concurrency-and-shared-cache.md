# 0004 Bounded concurrency and a shared request cache

- Type: Decision
- Status: Active
- Updated: 2026-11-05
- Applies to: `aimediator` 0.1.0 from pipeline upgrade batch U3 (steps U3.1 to U3.4, measured by U3-L); `RULES.md` v1.4
- Owner decisions UP-D08 and UP-D09 of the
  [pipeline upgrade plan](../plans/pipeline-upgrade.md) (sections 4.5 and
  4.6); the execution and the live measurements are recorded in the
  [change record](../records/20261104-pipeline-upgrade.md) and in
  [`reports/20261105-upgrade-u3-evaluation/`](../../reports/20261105-upgrade-u3-evaluation/manifest.json).

## Context

Before batch U3 a run sent one model request at a time, and every run
asked the model again for every request, even when an earlier run had sent
the same bytes to the same model. The model service can serve several
requests at once, so a serial run left it idle between requests, and
repeated runs on fixed evaluation sets paid for answers they already had.
The 600-comment validation separated fresh from reused answers by hand.
Embeddings were cached per run in files of 8 texts, so a changed batch
boundary invalidated every file after it, and no record was shared across
runs.

The constraints were the frozen artifacts: the trace, the progress files
and the artifacts are written in a fixed order that resume, interruption
and the behavior lock rely on (design/cli.md section 5), and with the
default settings every request and artifact had to stay byte-identical.

## Decision

1. **Ordered executor** (U3.1). `pipeline.ordered(units, work, commit,
   limit)` runs independent units on a thread pool with at most `limit`
   units in flight and commits their results in input order on the calling
   thread. Every write of the write schedule happens in the commit callback,
   in the serial order. Units: one quality comment with its attempts; one
   audited claim; one relevance batch; one relevance recheck; one
   retrieval-review batch with the single rechecks of its items; one
   extraction batch with its split retries in serial order. With a full
   window the next unit is submitted only after the oldest is committed, so
   with limit 1 requests and writes interleave as in the serial loop. On an
   exception, `KeyboardInterrupt` included, pending units are cancelled,
   running ones finish, and nothing after the failed unit is committed.
2. **`max_parallel_requests`** (U3.2, UP-D08), an integer from 1 to 8,
   default 1, with `analyze --max-parallel-requests`. `Runner` runs requests
   with the same identity one at a time; `operations.analyze` serializes
   the journal callback, `run-state.json` and progress lines with one lock.
3. **Shared cache** (U3.3, UP-D09), off unless `cache_dir` (or
   `analyze --cache-dir`) is set. Module `cache` (infrastructure, imports
   `common`): the key is the SHA-256 of the payload with `stream` false, the
   model digest, the service version and the request context when given
   (the quality attempt, decision D-9); the run identity is not part of it.
   Lookup order: the run journal, the shared cache, the transport. Only
   finished answers are stored. A hit writes the run's `response.json` with
   `elapsed_seconds` 0 and a `reuse-provenance.json` (source, key, original
   elapsed time), which `measurement` counts as reuse.
4. **Embeddings per text** (U3.4, UP-D09). One record per text,
   `embeddings/<SHA-256 of model, endpoint and text>.json`; only texts
   without a record are embedded, each distinct text once, in batches of 32
   in input order; the shared cache keeps the records under the model
   digest. `retrieval.json` keeps its schema.

## Measurements (U3-L)

Session U3-L ran four runs at the U3.4 commit on the 30-comment
`latency-benchmark` sample in `shadow`, through the hosted-API bridge of
plan 5.4 (UP-D19), so the times describe the provider and the network and
are indicative:

| Run | `max_parallel_requests` | Shared cache | Wall time | Fresh chat requests | Quality stage throughput |
| --- | ----------------------- | ------------ | --------- | ------------------- | ------------------------ |
| p1 | 1 | cold | 322.7 s | 59 | 0.107 requests/s, 84 output tokens/s |
| warm | 1 | the cache of p1 | 5.2 s | 0 | (replay) |
| p2 | 2 | cold | 245.7 s | 58 | 1.25 times p1 |
| p4 | 4 | cold | 263.8 s | 61 | 1.17 times p1 |

- Target T8 (at least 1.4 times on the quality stage at 2) was not met:
  1.25 times. The provider shares throughput between parallel requests;
  the mean elapsed time of a quality request rose from 9.3 s to 12.5 s at 2
  and 16.1 s at 4. The bridge log shows the requests in flight (peaks of 2
  and 4). A local service with free slots may gain more; that is not
  measured.
- The warm run made no chat request and no retrieval embedding request and
  reproduced every request and artifact file of p1 byte for byte, apart
  from elapsed times and timestamps.
- Embedding at batch 32 against batch 8 (p1 against the U2-L0 reference
  run of the same comments): largest score difference 0.0035, no retrieval
  decision changed. Two fresh runs at batch 32 differed by up to 0.0020 and
  in one decision (a margin of about 0.0001), so on the API the batch-size
  effect is within the hosted model's own variation.
- Technical failures and coverage did not change with the setting (3, 3,
  3 and 2 pending relevance units; coverage complete).

The value for the later live runs of the pipeline upgrade stays 1, without
a shared cache (decision D-10 of the change record): the gain is small on
the API, and parallel requests would bias the elapsed-time comparisons
against serial references.

## Consequences

- With the defaults (`max_parallel_requests` 1, no `cache_dir`) requests
  and artifacts are those of the serial code; the behavior lock changed
  only in the configuration and identity files, the existence-only
  `code-snapshot/cache.py` keys and the `embeddings/` layout.
- With `max_parallel_requests` above 1, fresh inference is not bitwise
  identical to serial inference (plan 2.3): the service batches parallel
  requests. The artifacts keep the serial order, and replay from the run
  journal or the shared cache stays exact. The model service must hold the
  slots (for Ollama, `OLLAMA_NUM_PARALLEL` of at least the value and the
  memory for each slot).
- A reused answer carries the provenance of its first run. Reports and
  measurements separate fresh from reused inference by
  `reuse-provenance.json`; a run whose answers all come from the cache
  measures the cache, not the model.
- The cache grows without bound and holds model answers with source text;
  it holds no credentials. Deleting it only makes the next run cold.
- `cache_dir` enters the resolved configuration and the run identity as an
  absolute path, so runs with different cache directories have different
  identities.
- Two processes that store the same key at the same moment can collide on
  the temporary file of `common.write`; one run then fails with an
  `OSError`. Sharing one cache directory between concurrent runs is not
  supported.
