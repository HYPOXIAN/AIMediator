# Handoff U1: Behavior-neutral performance and service identity

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-04
- Applies to: [pipeline upgrade plan](../pipeline-upgrade.md) batch U1; entry tag `upgrade-u0`

Work order for batch U1. The steps are defined in plan section 7 (U1). Four
steps keep every request and artifact byte-identical; two (U1.4, U1.5) add
the service identity and the context guard under UP-D03. No step needs a
live model.

## 1. Mission

- Replace the per-request directory listing of `run_store.state` with a
  request index (LAT-05), and commit a reusable synthetic scale run.
- Memoize character references and compile term patterns once (ALG-03).
- Make the stream loop guards incremental (ALG-04).
- Record the service version in run identities and detect a full context
  window (LNK-04).
- Let `replay_balance_admission.py` replay runs made with a quality
  identity (LNK-05).

## 2. Entry conditions

- Tag `upgrade-u0` exists. Clean tree, no `WIP Step` stash, the gates pass.
- UP-D03 is answered (U1.4, U1.5 only).

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/(runner|run_store|operations|evidence|balance_policy|inference|fixture_transport|engine)\.py$|tests/|scripts/experiments/(run_synthetic_fixture_scale|replay_balance_admission)\.py$|docs/records/[0-9]{8}-pipeline-upgrade\.md$|docs/design/cli\.md$|docs/guides/cli-usage\.md$)
```

- **Allowed**: the listed modules within plan 4.6 and 4.7; new tests; the
  new scale script; the replay script; design/cli.md sections 5 and 7 and
  the guide for U1.4.
- **Not allowed**: request bytes (all steps); artifact content except the
  manifest identity of U1.4; assets; exception types on existing paths; the
  write schedule of `pipeline`.
- **Lock**: unchanged in U1.1, U1.2, U1.3, U1.5 and U1.6. U1.4 regenerates
  it for the manifest identity only (`manifest.json` of L1 and L2, and the
  values derived from the run ID if the lock does not already normalize
  them).
- **Decisions in force**: UP-D03 (U1.4, U1.5).
- **Owner actions**: none.

## 4. Sessions

### U1-1 (implementation): steps U1.1 to U1.6

```text
You are session U1-1 (implementation) of the AIMediator pipeline upgrade,
steps U1.1 to U1.6.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/pipeline-upgrade-handoffs/u1-neutral-performance.md); the plan
docs/plans/pipeline-upgrade.md, sections 1 to 4, the U1 part of section 7,
and sections 8 and 10; design/cli.md sections 5 and 7; the change record.
Task: execute your steps in order, inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates, including the
  behavior lock, after every commit.
- One kind of operation per commit, with "Step: U1.x" in the body and
  "Decision: UP-D03" for U1.4 and U1.5.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **U1.1** (LAT-05)
  - `Runner(..., journal=None)`: after writing `validation.json`, call
    `journal(<request directory relative to the run folder>, <no errors>)`.
    `progress` keeps its signature.
  - `run_store.record_request(folder, relative, completed)` updates the
    per-folder index. `state` lists `requests/**/validation.json` only on
    its first call for a folder in a process (resume), then uses the index.
    Keep the sort order of the restructuring's B5.8 entry (relative path
    parts).
  - `operations.analyze` passes the journal callback.
  - Contract: `run-state.json` content at every write equals what the
    current code writes (`updated_at_utc` aside). Check it with a harness
    like B5.8's on CLI runs in the three modes, with interruptions and
    resumes; keep the harness in the test suite in reduced form.
  - Test: the number of directory listings over 50 `state()` calls in one
    process is 1.
  - `run_synthetic_fixture_scale.py --comments 600 --mode shadow --out <run>`
    reproduces the B5.9 setup (copied fixture cases under new IDs, a
    fixture transport answering from their annotations,
    `operations.analyze` with `stop_after` `full`) and prints wall time and
    the profiled share of `run_store.state`. Commit the script first in
    its own `chore` commit, measure T9 on the unchanged code, then commit
    the refactor and measure again.
- **U1.2** (ALG-03)
  - `balance_policy.term_matches`: compile each term's pattern once
    (`functools.lru_cache` on a pattern builder); same matching rules.
  - `evidence.character_reference(text)`: memoize by `text` and return
    `copy.deepcopy` of the cached value, so callers still get new objects
    (`test_character_reference_returns_new_objects`).
  - Equivalence test: for every `text_original` in the tracked evaluation
    sets and fixtures, the new `character_reference`,
    `character_candidates` and `attributed_candidates` equal a copy of the
    current implementations kept in the test.
  - Record T10 (plan 8.4).
- **U1.3** (ALG-04)
  - Keep one growing buffer; scan only the new tail plus an overlap of the
    longest allowed key; keep the seen identities and claim signatures
    between chunks.
  - Equivalence test against a copy of the current `streamed_chat` and
    `repeated_claim` on synthetic streams: normal outputs, a duplicate key
    loop, a duplicate claim loop, a whitespace loop, and every chunk
    boundary position for short samples. Same `done_reason`, same content.
  - Timing: the plan 0.1 sizes (4 comments with 2, 8 and 30 claims each,
    4-character chunks, a fake response object instead of the network),
    run against the old copy and the new function; record both.
- **U1.4** (LNK-04, UP-D03)
  - `Transport.version()` reads `/api/version` with the connection
    timeout; an HTTP 404 gives `null` (recorded as unavailable), other
    failures follow `probe`.
  - `run_store.identity` and `initialize` take the service version;
    identity key `service` with `ollama_version`.
  - `operations.analyze` on resume compares the version and raises
    `Failure(4, 'Service version differs from saved run; start a new run')`.
  - `engine.run` reads it through its `api_transport` (`/api/version`) and
    records it in its identity as `service_version`; the fixture API of
    lock target L2 in `tests/behavior_lock.py` answers that endpoint.
  - `FixtureTransport.version()` returns
    `{'version': 'fixture-not-a-service'}`.
  - Update design/cli.md section 7 (run identity) and the guide (resume
    refusal).
- **U1.5** (LNK-04, UP-D03): in `Runner._generate`, when the response has
  both counters and their sum is at least `payload['options']['num_ctx']`,
  append `Context window reached`. Tests with a fake transport for the
  extract stage (batch split follows) and the quality stage (a failed
  attempt follows).
- **U1.6** (LNK-05): when the source manifest has
  `identity['evidence_quality']`, the script passes it as
  `quality_identity`. Check by hand on a legacy fixture run (`engine.run`
  with the fixture transport, as lock target L2 does) and record the
  result; runs without it keep today's behavior.

### U1-V (verification)

```text
You are session U1-V (verification) of the AIMediator pipeline upgrade. You
did not implement batch U1. Change nothing except the change record.
Read: RULES.md; this work order; the plan, sections 1, 2, 4.6, 4.7, 8 and
10 and the U1 part of section 7; the change record.
Task: run every item of the U1-V checklist on HEAD, and append a
verification note committed with "Session: U1-V". If every item passes, tag
that commit upgrade-u1. Otherwise record fix-up steps U1.F1 and so on and
stop without tagging. Never add attribution. Your final message repeats the
verification note.
```

Checklist:

1. Boundary and commit hygiene from `upgrade-u0` (plan 8.8).
2. `git log upgrade-u0..HEAD -- tests/fixtures/behavior-lock.json` lists
   only the U1.4 commit, and its fixture diff touches only manifest keys.
3. Gates, foreign directory and wheel acceptance pass.
4. T9 and T10 are recorded with before and after values; the equivalence
   tests of U1.1 to U1.3 are in the suite and pass.
5. Resume of a fixture run with a different service version fails with
   exit code 4 (a test or a recorded manual check).

## 5. Exit and handoff out

- Exit tag: `upgrade-u1`, set by U1-V.
- The next work order is [U2](u2-request-views.md).

## 6. Escalation triggers

- `run-state.json` content differs from the current code at any write.
- An equivalence test of U1.2 or U1.3 finds a difference.
- U1.4 changes a lock key that is not part of the manifest identity.
- `/api/version` behaves differently from plan 4.7 on the owner's service.
