# Code Restructuring Blueprint

- Type: Plan (blueprint)
- Status: Archived
- Updated: 2026-11-04
- Applies to: the [code restructuring plan](code-restructuring.md), batches B0 to B7; commit `7282f49` and later; `RULES.md` v1.2
- Archived 2026-11-04 when the code restructuring was completed (tag `restructure-done`).

This blueprint governs the code restructuring as an engineering project. It
fixes the approved scope, the target interfaces, the engineering standards,
who is responsible for what, how sessions start, end and hand over, and how
quality is checked. It does not repeat the plan. Each step is defined once,
in the plan, and is cited here and in the handoffs by its ID (G2).

---

## 0. Document map

| Document | Authoritative for |
| -------- | ----------------- |
| [RULES.md](../../RULES.md) | All project rules. It overrides everything below (G1) |
| [Plan](code-restructuring.md) | Findings (F, P, U, R, T, S IDs), invariants (section 2), module table and dependency rules (4.1, 4.2), behavior lock (5), step definitions (7), verification commands (8), decisions (9) |
| This blueprint | Approved scope and its consequences (1), objectives and metrics (2), interface contracts (3), engineering standards (4), roles and responsibilities (5), session protocol (6), quality system (7), milestones (8) |
| Handoffs in `code-restructuring-handoffs/` | One work order per batch: sessions, boundaries, step notes, exit checklists, prompts to start each session |
| Change record `docs/records/<YYYYMMDD>-code-restructuring.md` (created in B0.1) | The state of execution and its evidence: progress, session log, verification notes, escalations, archives |
| [Compatibility register](../reference/compatibility-layers.md) | Remaining compatibility layers |

When two documents disagree, the higher one in this order wins: RULES.md,
the plan (for steps and invariants), this blueprint, the handoff. A session
that finds a disagreement follows the higher document, writes the conflict in
the change record and escalates if it affects behavior (section 6.5).

Handoffs: [B0](code-restructuring-handoffs/b0-safety-net.md),
[B1](code-restructuring-handoffs/b1-defects-and-hot-spots.md),
[B2](code-restructuring-handoffs/b2-engine-split.md),
[B3](code-restructuring-handoffs/b3-callers-and-tests.md),
[B4](code-restructuring-handoffs/b4-layer-removal-and-docs.md),
[B5](code-restructuring-handoffs/b5-internals-and-performance.md),
[B6](code-restructuring-handoffs/b6-research-code.md),
[B7](code-restructuring-handoffs/b7-readability-and-acceptance.md).

---

## 1. Approved scope

### 1.1 Decisions in force

The owner adopted all twelve recommendations of plan section 9 on
2026-11-03. Each answer removes the alternative branches that the plan still
describes. Ignore every "if rejected" or "skip if not adopted" clause in the
plan.

| ID | Binding consequence | Executed in |
| -- | ------------------- | ----------- |
| CR-D01 | The collectors move into the subpackage `aimediator.collection`. They get no CLI command, and P3 is not amended for them | B6.2 |
| CR-D02 | Experiment scripts keep experiment-specific orchestration, case lists and output formatting. Logic used by two or more scripts or by tests moves into `aimediator.design_briefs` and `aimediator.diagnostics`. `run_grounded_feedback_live.py` stays as a frozen pilot. P3 gains one clarifying sentence in v1.3 | B4.4, B6.3, B6.4 |
| CR-D03 | Four quality-screening scripts and their two test files (9 tests) are archived. `run_quality_screening_experiment.py` stays | B1.6 |
| CR-D04 | `run_local_direction_comparison.py` and `demo_evidence_quality.py` are archived, not fixed. The register loses its R3 row | B1.7 |
| CR-D05 | Research commands become `python3 -m aimediator.<module>`, and the six pure forwarders are deleted | B4.1, B4.2 |
| CR-D06 | Experiment identities hash package modules and assets instead of forwarders and symlinks (rule in section 3.6). The owner confirmed that no experiment output must be resumed or replayed under its old identity | B3.4 |
| CR-D07 | Removal condition R1 counts code, tests, configuration and living documents only. Frozen records and the archive keep their historical paths. 18 symlinks are deleted | B4.3 |
| CR-D08 | `data/evaluation/evidence-quality-synthetic-v1/cases.json` stays as a permanent registered symlink | B4.3 |
| CR-D09 | One helper, `resources.workspace_root()`, is the project root for package defaults and scripts (section 3.3) | B6.1 |
| CR-D10 | `RULES.md` v1.3: G3 drops `prompts/`, P3 gets the CR-D02 sentence. v1.4: the P4 floor rises to the final test count. The owner confirms the wording at the B4 and B7 reviews | B4.4, B7.4 |
| CR-D11 | Style normalization applies to `src/` and `scripts/` only, never to `tests/` | B7.1 |
| CR-D12 | Legacy `engine.run` also writes `code-snapshot/<module>.py` for every top-level package module | B5.11 |

### 1.2 Scope boundaries

In scope: the code in `src/aimediator/`, `scripts/` and `tests/`; the
documents that describe it; `RULES.md` amendments CR-D10; the compatibility
register.

Out of scope:

- prompt, policy, glossary, anchor or fixture changes;
- model or inference-option changes;
- new CLI commands or features;
- new dependencies;
- collected data, evaluation sets, curated reports;
- live-model reruns.

Known gaps that this restructuring leaves on purpose (candidates for later
work, recorded here so no session "fixes" them on the side):

| Function | Lines at `7282f49` | Why it stays |
| -------- | ------------------ | ------------ |
| `review.load_run` | 136 | Dense validation code covered by many product tests; splitting it is not needed for layering |
| `operations.analyze` | 111 | Run lifecycle and error translation; changed only where B5.7 removes `redirect_stdout` |
| `reporting.export_report` | 105 | Determinism contract; no finding requires a rewrite |
| `quality_scoring.score_group` | 71 | Metric code with frozen semantics |
| `engine.run` | 78 | Legacy identity construction; shrinks a little in B5.1 but keeps its identity fields |
| `evidence_quality.qualify` | 61 | Routing rules with frozen semantics, one line over the threshold |
| collector `main()` functions and `Client.get` | 63 to 95 | Moved without changes in B6.2 |

### 1.3 Expected test count

| After | Expected change | Reason |
| ----- | --------------- | ------ |
| Start | 222 | Baseline |
| B0 | + lock tests | Behavior lock (B0.3) |
| B1 | +1, +1, −9 | Glossary copy test (B1.1), console text test (B1.5), archived tests (B1.6) |
| B2 | +1 or more | Module layering test (B2.10) |
| B3 | 0 | Imports only |
| B4 | −1 | Forwarder identity test removed with the forwarders (B4.2) |
| B5 | + some | Stage and state tests (B5.2, B5.5, B5.8) |
| B6 | + some | `workspace_root`, `diagnostics`, collection tests |
| B7 | 0 | Formatting and documents |

The count may never fall below 192 (P4). Every decrease is tied to a step in
the progress table.

---

## 2. Objectives and metrics

| Objective | Metric | Baseline | Target | Batch | How measured |
| --------- | ------ | -------- | ------ | ----- | ------------ |
| Remove the hub module | `engine.py` content | 931 lines, 24 definitions | `ROOT`, `run`, `main` only | B3.6 | read the file |
| Clear layering | Modules importing `engine` | 7 | 0 | B3 | plan 8.7, second grep |
| Clear layering | Intra-package import cycles | 1 (`demo` and `operations`) | 0 | B2.9 | `tests/test_module_layers.py` |
| Short functions | Functions over 60 lines in `pipeline`, `runner`, `stages`, `evidence`, `retrieval` | `process` 259, `_generate` 112 | none | B5.5, B5.6 | section 7.3 command |
| Correctness | Crashing entry points (F-01, F-02) | 2 | 0 | B1.7 | archive |
| Correctness | Fixes for F-03 to F-08 | open | done | B1, B3.4, B5.7 | plan steps |
| Performance | Offline demo wall time | 26.2 s | at most 10 s | B1.1 | plan 8.4 |
| Performance | Offline suite wall time | about 70 s | at most 45 s, lock included (target, not a gate) | B1 to B5 | plan 8.4 |
| Performance | `run_store.state` reads per call | all validation files | only new ones | B5.8 | test counting reads |
| Conformance | Compatibility layers | 19 symlinks, 7 forwarders | 1 symlink, 0 forwarders | B4 | register, G2 |
| Conformance | Text I/O without encoding | 130 calls | 0 | B1.3 | plan 8.7, fifth grep |
| Conformance | Working-directory roots in code | 2 | 0 | B6.1 | plan 8.7, fourth grep |
| Conformance | Prompts outside assets (P7) | 1 file | 0 | B1.6 | archive |
| Tests | Working-directory dependent tests | 1 | 0 | B0.2 | plan 8.5 |
| Tests | Test files importing forwarders | 9 | 0 | B3.3 | plan 8.7, first grep |
| Safety | Behavior lock | none | green after every step | B0 onward | plan 8.3 |

---

## 3. Target system

### 3.1 Layers

The plan's dependency table (section 4.2) is authoritative and is enforced
by `tests/test_module_layers.py`. The layer picture below explains it. A
module imports only from its own layer or the ones below it, and never in a
cycle.

```text
interfaces      cli, presentation, __main__
services        operations, review, legacy_review, reporting, evaluation,
                quality_scoring, demo, engine (legacy research runner)
orchestration   pipeline
infrastructure  inference, runner, retrieval, run_store, fixture_transport
domain          evidence, evidence_quality, stages
foundation      common, schema, resources, config, balance_policy,
                glossary_vectors
research        design_briefs, diagnostics, collection.* (outside the CLI
                path and outside run identities)
```

### 3.2 Data flow of a run

CLI analysis (`aimediator analyze`):

1. `cli` calls `operations.analyze`.
2. `operations.analyze` runs the preflight, creates the run through
   `run_store.initialize`, takes the run lock, and calls `pipeline.process`
   with a runner factory that injects `Transport.chat`, and a retrieval
   service that injects `Transport.api` and `Transport.embed`.
3. `pipeline.process`:
   1. `retrieval.retrieve` (embeddings and anchors);
   2. per routed model: retrieval triage, retrieval review, relevance with
      refinement, then (shadow or enforce) quality annotation, extraction,
      source binding (`evidence.ground_claim`, plus
      `evidence_quality.bind_claim` in enforce), and the semantic audit;
   3. assembly of the summary and the report.
4. Every model call goes through `runner.Runner.generate`, which journals
   it under `requests/`.
5. `operations.analyze` writes the coverage ledger and `run-state.json`
   through `run_store`.

Legacy research run (`python3 -m aimediator.engine`): `engine.run` builds
the legacy identity and snapshots, then calls the same `pipeline.process`
with `runner.Runner` and `retrieval.retrieve`, and transports injected or
defaulted to `inference`.

### 3.3 Interface contracts

"Unchanged" means the signature and behavior at `7282f49`. The names listed
are each module's surface for other modules, scripts and tests. Moved code
keeps its names. Rename only where this section says so.

**`resources`**

- `asset_path(name='') -> Path` and `module_path(name) -> Path`: unchanged.
- `glossary() -> dict` (B1.1): the parsed `assets/data/glossary.json`
  (`json.loads`, as today), loaded once per process. Callers never mutate it;
  functions that derive data from it return new objects.
- `anchors() -> tuple[list[str], list[str]]` (cached from B5.10): positive
  and negative anchor texts, read-only. `retrieval.retrieve` relies on
  exactly 10 positive and 10 negative anchors (it slices at 20 and at 10);
  that assumption is frozen with the asset.
- `prompts(mode) -> dict[str, dict[str, str]]` (B5.1): stage, then
  language, then prompt text. The stages, in this key order, are
  `relevance`, `retrieval_review`, `extract` and `verify`, plus `quality`
  when the mode is `shadow` or `enforce`. In `enforce`, `extract` and
  `verify` get `'\n'` plus the `quality-extract` or `quality-verify`
  appendix. The result equals today's `operations.prompts_for(mode)` and
  `engine.run`'s dictionary, key order included.
- `workspace_root() -> Path` (B6.1): if `Path(__file__).resolve().parents[2]`
  (the checkout when the package is imported from `src/`) contains both
  `RULES.md` and `pyproject.toml`, return it; otherwise return
  `Path.cwd()`. Evaluated at call time.

**`schema`** (B2.3; complete from B5.2)

- Builders: `obj(properties)` with keys in the order `type`,
  `additionalProperties`, `properties`, `required` (from `engine.py`);
  `quality_obj(properties)` with keys in the order `type`, `properties`,
  `required`, `additionalProperties` (from `evidence_quality.obj`);
  `arr(items)`; `enum(values)`.
- Constants: `STRING`, `NULLABLE_STRING` (`{'type': ['string', 'null']}`),
  `NULLABLE_NONEMPTY_STRING` (the same with `'minLength': 1`), `BOOL`.
- Validator: `schema_errors(value, schema, path='$') -> list[str]`,
  unchanged from `evidence_quality.schema_errors`.
- The two object builders differ only in key order. That order reaches the
  model through the request, so both are frozen. A unit test pins the
  serialized form of each.

**`evidence`** (B2.3, B5.3, B5.4)

- `evidence_units(text)`, `numeric_tokens(text)`,
  `character_candidates(text, reference)`: unchanged.
- `PARAMETER`, `CLAIM`: unchanged dictionaries, built with `schema.obj`.
- `character_reference(text='') -> list[dict]`: unchanged result. It is
  built from `resources.glossary()` from B1.1 and returns new objects on
  every call.
- `character_terms(entry) -> list` (B5.3): returns
  `[entry['canonical_name'], entry.get('chinese_label')]` plus the alias
  texts, in that order and unfiltered. Callers keep their own filtering.
- `ground_claim(claim, row, characters) -> (errors, enriched or None)`:
  unchanged. The span invariant raises `AssertionError` explicitly (B1.2).

**`stages`** (B2.5, B5.5)

- `schema_for(stage, ids, data=None)` and
  `exact_coverage(rows, key, expected)`: unchanged.
- `prepare(stage, data, ids) -> dict` (B5.5): for `verify`, it builds the
  audit view exactly as `Runner._generate` does at `engine.py` lines 242 to
  265 (keys `original_evidence`, `proposed_claim`, `naming_reference`,
  `claim_id`, then the optional `selected_source_segments` and
  `selected_source_points`). For every other stage it returns `data`
  itself.
- `options(stage, quality_policy) -> dict` (B5.5): returns
  `{'temperature': 0, 'seed': 42, 'num_ctx': 8192, 'num_predict': 4096}` for
  `extract`, with `256` instead of `4096` for the other stages. For
  `quality`, `num_predict` and `num_ctx` are then replaced from the policy
  (`evidence_quality.load_policy()` when the policy is `None`). The key order
  is kept. `Runner` applies `runtime_options` afterwards.
- `normalize(stage, parsed, ids, data) -> (parsed or None, errors)` (B5.5):
  the post-validation transformations of `engine.py` lines 327 to 343.
  `Runner` calls it only when the schema check passed, inside the same
  `try` block that catches `ValueError`, `KeyError` and `TypeError`.

**`inference`** (B2.4)

- `api(base, endpoint, payload=None)`,
  `streamed_chat(base, payload, partial_path, timeout=1800)`,
  `repeated_claim(output, allowed_ids)`, `Transport` and `probe`:
  unchanged. `inference` never imports `engine`.

**`runner`** (B2.6, B5.5, B5.7)

- `Runner(base, folder, prompts, quality_identity=None, quality_policy=None,
  chat_transport=None, progress=None)`, with attribute `runtime_options`
  (default `{}`). It gains `log=None` in B5.7.
- `cached_single_ids(model, language, stage)` and
  `generate(model, language, stage, data, ids) -> (parsed or None, meta)`:
  unchanged. `meta` has the keys `request_id`, `errors` and
  `elapsed_seconds`. `progress(stage, ids, None)` is called before each
  request, `progress(stage, ids, bool(parsed))` after it.
- Journal: `requests/<stage>/<request_id>/` holds `request.json`,
  `response.json`, `validation.json` and `partial-output.txt`; the quality
  stage adds `interrupted-partial-<n>.txt`, and the CLI transport adds
  `transport-attempts/`.
- Error semantics are unchanged. Stages other than `quality` propagate
  transport errors and unreadable cache files; `quality` turns them into
  failed attempts with `done_reason` `transport_error`, `invalid_cache` or
  `invalid_response`.
- B5.7: `log(text)` receives exactly the text the current `print` writes
  (`'<stage>: <model>, <n> items'`). The default `None` writes nothing.

**`retrieval`** (B2.7, B5.7, B5.10)

- `retrieve(rows, base, folder, model, embedding_config=None,
  api_transport=None, embed_transport=None) -> list[dict]`: unchanged. It
  writes `retrieval.json` and `embeddings/<sha256>.json`. It gains `log=None`
  in B5.7 for the `'Embedding <n>/<total>'` lines.

**`pipeline`** (B2.8, B5.6, B5.7)

- `VERSION` (`'balance-evidence-v2'`), `batches`, `aggregate`,
  `quality_source_counts`, `build_full_coverage`, `validate_modes` and
  `relevance_agrees`: unchanged.
- `process(args, rows, routing, models, prompts, quality_identity,
  quality_policy, identity, embedding_config=None, runner_factory=Runner,
  retrieval_service=retrieve) -> dict`: unchanged. It gains `log=None` in
  B5.7, which receives the summary JSON text that is printed today.
- B5.6: stage functions share one `RunState` dataclass (no `slots`, no
  `kw_only`, for Python 3.9). Suggested names: `triage`, `review_retrieval`,
  `admit_relevance`, `assess_quality`, `extract_claims`, `audit_claims`,
  `assemble`. Section 3.4 is the contract they keep.

**`engine`** (B2.8, B3.6, B5.11, B6.1)

- `ROOT` (`workspace_root()` from B6.1), `main()`, and
  `run(args, *, api_transport=None, chat_transport=None,
  embed_transport=None, retrieval_service=None)` (B2.1). From B5.7, `run`
  also takes `log=None`, and `main` passes a printer that writes each text
  with `print(text, flush=True)`, so the console output is unchanged.
- B5.11: when the run manifest is first created, it writes
  `code-snapshot/<module>.py` for every top-level package module, sorted,
  next to the three existing snapshot files.

**`fixture_transport`** (B2.9): `FixtureTransport(cfg, key=None, folder=None)`,
unchanged, with provenance `agent_authored_synthetic_fixture_transports`.
`demo.FixtureTransport` stays importable, because `demo` imports it.

**`run_store`** (B5.8): `state(folder, status, stage, reason=None)` has an
unchanged signature, and `run-state.json` keeps the same content at every
write. Only how completed request identities are found changes.

**`operations`** (B5.1): `prompts_for(mode)` stays as an alias of
`resources.prompts`.

**`design_briefs`** (B6.3): `validate_move_data`, `quality_design_errors`
and `prepare_briefs(claims, move_data=None, target_patch=None,
pending_adjudication_ids=(), quality_mode=None)`, unchanged. The module
imports nothing from the package.

**`diagnostics`** (B6.4)

- `extract(runner, model, language, row, *, allowed_points=None) -> (parsed,
  meta)`: sends the extraction request with the data
  `{'comments': [{'comment_id': ..., 'units': ...}],
  'character_normalization_reference': character_reference(text)}`, adding
  `allowed_quality_points` after `units` when given. This is the key order
  the scripts use today.
- `audit(runner, model, language, row, claims, characters, *,
  quality_record=None) -> list[dict]`: for each claim, runs `ground_claim`,
  then `bind_claim` when a quality record is given, and the `verify` request
  only when no error remains. It returns neutral records with the keys
  `index`, `claim`, `enriched`, `errors`, `audit` and `audit_meta`.
- Each script maps these records to its own existing output keys, so result
  files keep their format.
- A script's request bytes must not change. B6.4 verifies this per script
  (handoff B6).

**`collection`** (B6.2)

- Modules `client`, `store`, `sources`, `export`, `screening`, `balanced`
  and `expansion` hold today's names unchanged (`Halt`,
  `RestrictedRedirect`, `Client`, `retry_delay`, `HOSTS`,
  `load_youtube_key`, `Store`, `steam`, `bluesky`, `youtube`,
  `guess_language`, `timestamp`, `export`, `classify_rules`, `classify`,
  `load_sources`, `write_rows`, `reviewed_rows`, `retained`,
  `select_balanced`, `kept_counts`).
- Each tool module exposes `main(argv=None)` with today's argparse and
  orchestration, and returns today's exit code: `sources` for
  `collect_feedback`, plus `balanced`, `expansion` and `screening`.
- The state directory is `workspace_root() / 'runs/state'`.

### 3.4 Artifact write schedule of `pipeline.process` (frozen)

Partial runs, resume, `status` and partial reports read these files, so
their write points, content and order must survive B5.6. Line numbers refer
to `engine.py` at `7282f49`.

1. Before the model loop, `retrieve` writes `embeddings/` and
   `retrieval.json`.
2. For each routed model, after its relevance pass: `relevance.json`,
   `review-queue.json` (lines 725 to 727). With `relevance_only`, the model
   loop continues with the next model here.
3. Before quality: `full-pipeline-coverage.json` (line 734).
4. After each quality record: `evidence-quality.json`,
   `full-pipeline-coverage.json`, `request-trace.json` (lines 763 to 765).
   With `quality_only`, the loop continues here.
5. After each extraction batch: `extraction-coverage.json`,
   `claims-before-audit.json`, `quarantined-claims.json` (lines 808 to 810).
6. After each audit batch: `audit-progress.json`, `quarantined-claims.json`
   (lines 825 and 826).
7. After the loop: `full-pipeline-coverage.json` (line 868).
8. In shadow and enforce, in this order: `evidence-quality.json`,
   `quality-routing.json`, `quality-review-queue.json`,
   `quality-summary.json`, `opinion-summary.json`, `system-feedback.json`,
   `quality-exclusions.json` (lines 890 to 893).
9. In this order: `relevance.json`, `validated-claims.json`,
   `quarantined-claims.json`, `request-trace.json`, `summary.json`,
   `balance-report.json` (lines 899 to 904). Then the summary text is
   printed, which becomes a `log` call in B5.7.

`KeyboardInterrupt` passes through `process` unhandled; `operations.analyze`
handles it. Add no `try` block that changes this.

### 3.5 Request construction (frozen)

Every model request is built as follows. B2 moves this code and B5.5 splits
it, and the request digests of the behavior lock must not change.

- `schema = schema_for(stage, ids, data)`, after the `verify` shaping.
- The payload keys, in this order: `model`; `messages` (the system prompt,
  then the user content); `format` (the schema); `stream` (`True`);
  `keep_alive` (`'10m'`); `options`.
- The user content is
  `json.dumps({**data, 'response_schema': schema}, ensure_ascii=False)`,
  without `sort_keys`, so the key order of `data` is part of the bytes.
- Options follow section 3.3 (`stages.options`), then `runtime_options`, so
  `num_gpu`, when set, comes last.
- The cache identity is the SHA-256 of
  `json.dumps({**payload, 'stream': False} plus 'pipeline_quality_identity'
  when set, sort_keys=True, ensure_ascii=False)`.
- `request.json` is the payload as written by `common.write` (indented, not
  sorted). `streamed_chat` posts `json.dumps(payload, ensure_ascii=False)`.
- Batching: retrieval review and relevance use `batches(count=8,
  chars=10000)`, and the retrieval review reuses cached single checks;
  failed or uncertain items are rechecked one at a time. Quality is one
  comment per request, with `max_attempts` from the policy. Extraction uses
  `batches(count=4, chars=9000)` for English and `chars=4000` for Chinese,
  and splits a failed batch into single requests. The audit uses
  `batches(count=1)`.

### 3.6 Research scripts

Applies to every script that remains in `scripts/collect/` and
`scripts/experiments/`.

- **Bootstrap**: the two lines of plan section 4.3, then imports from
  `aimediator`. Sibling scripts may still import each other, for example
  `from prepare_balance_design import ...`, until B6.3.
- **Docstring**: the first docstring line must not begin with "Compatibility
  entry point". The rule check treats such a file as a forwarding script that
  must be registered (G2). Use "Entry point for ..." for thin wrappers.
- **Flags and defaults**: unchanged. A default that named a removed path now
  names the same file through `asset_path` (for example `--prompt-dir` of
  `run_balance_regression_live.py`).
- **Identity** (CR-D06, B3.4):
  - Replace every hash of a forwarder or symlink path with
    `package_code_sha256: run_store.code_manifest()['modules']`, and with
    `asset_sha256: {name: SHA-256 of asset_path(name)}` for every asset the
    script reads.
  - Keep `script_sha256` (the script's own file).
  - Code snapshots copy `module_path(name)` files into `code-snapshot/`.
  - B3.4 lists each script's identity keys in the change record.
- **Console output**: from B5.7, scripts that build a `Runner` or call
  `retrieve` or `process` pass a printer as `log`, so their console text
  stays as it was.
- **Outputs**: file names and keys stay unchanged, except the identity and
  snapshot fields above and in CR-D12.

### 3.7 Stability classes

| Class | Members | Rule |
| ----- | ------- | ---- |
| Frozen | The CLI contract; run artifacts and their schema versions; request bytes; assets; research script flags and output files | Must not change (plan section 2), except as sections 3.6 and 1.1 state |
| Internal | Python names in `src/aimediator/` | May change only as section 3.3 says; every caller in the package, scripts and tests is updated in the same batch |
| Test-only | `tests/support.py`, `tests/behavior_lock.py` | Owned by the tests; may change in any batch that has `tests/` in its boundary |

---

## 4. Engineering standards

### 4.1 Code

1. **Python 3.9 syntax.** Do not use `match`, parenthesized multi-item
   `with`, `zip(strict=...)`, or dataclass `slots` or `kw_only`. Do not use
   `X | Y` or built-in generics in annotations that are evaluated at runtime;
   use `from __future__ import annotations`.
2. **Dependencies**: the standard library and NumPy only.
3. **Imports**: relative imports inside the package (`from .evidence import
   ground_claim`) and no star imports. When moving code, keep the importing
   module's aliases (`digest`, `write_json`, `quality`), so that function
   bodies stay identical and the move check (plan 8.6) passes.
4. **I/O**: always pass `encoding='utf-8'` for text. No file reads at import
   time after B5.10.
5. **Output**: no `print` in the analysis modules (`common`, `schema`,
   `resources`, `config`, `balance_policy`, `evidence`, `evidence_quality`,
   `stages`, `inference`, `runner`, `retrieval`, `pipeline`, `run_store`,
   `review`, `reporting`, `evaluation`) after B5.7. `operations` keeps its
   progress lines on stderr. `main()` functions and the research-tool modules
   (`collection.*`, `glossary_vectors`, `quality_scoring`, `legacy_review`,
   `engine.main`) may print.
6. **Serialization order is behavior.** Never reorder a dict literal, a
   schema's properties, or a list that ends up in a request or an artifact.
   Never add `sort_keys` where it is absent or remove it where it is
   present.
7. **Exceptions are contract.** The CLI maps exception types to exit codes,
   so keep the type raised on every existing path.
8. **Comments that state domain rules** move with their code (for example
   "Do not send a second copy of the full text").
9. **New public functions** get a one-line docstring. Type hints follow in
   B7.2.

### 4.2 Tests

1. Tests live in `tests/test_<area>.py` as `unittest.TestCase` methods. The
   rule check counts only methods of test classes.
2. A test puts `src/` on `sys.path` and imports `aimediator` modules. Shared
   fixtures live in `tests/support.py` (from B3.2). A test never imports
   another test module.
3. Inject transports, and patch only objects passed in or the shared
   `urllib.request` module. After B2.2, never patch module globals of moved
   functions.
4. Tests run offline, and do not depend on `reports/` (P4) or on the working
   directory (use `asset_path` or `Path(__file__)`).
5. A test that only asserts a re-export is removed with the re-export.
6. Changes to the behavior-lock fixture follow plan section 5.5.

### 4.3 Commits and tags

Commit rules are in plan section 1, item 2: one kind of operation per
commit, `type: summary`, `Step:` and `Decision:` lines, and no attribution
(P6). A commit that belongs to no step carries `Session: <session ID>` in its
body instead of `Step:`. That covers session-log entries, verification notes,
escalations and review closures. Tags:

| Tag | Set by | When |
| --- | ------ | ---- |
| `restructure-plan` | The owner, or a session the owner asks | On the commit that adds the plan, this blueprint and the handoffs; B0 starts from it |
| `restructure-b0`, `-b2`, `-b3`, `-b5`, `-b6` | Verification session | After its checks pass |
| `restructure-b1-review`, `-b4-review`, `-b7-review` | Verification session | After its checks pass, at owner review points |
| `restructure-b1`, `-b4`, `restructure-done` | The closure session the owner instructs (section 6.4) | After the owner's review |

### 4.4 Documents

1. English (D8). Every document has the D2 header and an index entry (D4),
   in the same commit that adds it.
2. Never put a fenced code block inside a list item. The owner's Markdown
   formatter drops it: this already happened once in the plan. Put command
   examples after the list.
3. Living documents follow the code (D9). Records and decisions are frozen
   when final (D3).
4. After the owner edits a Markdown file, run the rule check and look at the
   code spans containing `*` and at the fenced blocks.

---

## 5. Roles and responsibilities

### 5.1 Roles

- **Owner** (the human project owner):
  - decides, approves `RULES.md` wording and reviews at B1, B4 and B7;
  - answers escalations, and owns `~/Archives/AIMediator/`;
  - is the only one who may authorize a behavior change, which means an
    output change in the lock, or a deviation from the plan;
  - does not have to run commands.
- **Implementation session** (an agent, ID `B<n>-<k>`):
  - executes the steps its handoff assigns, inside the batch boundary;
  - writes code, tests and documents, commits, and keeps the progress table
    and session log;
  - registers decisions found during execution, and escalates;
  - never sets batch tags, never edits `RULES.md` outside B4.4 and B7.4,
    and never regenerates the lock outside plan section 5.5.
- **Verification session** (an agent, ID `B<n>-V`, with a fresh context, and
  never the session that implemented the batch):
  - reruns every batch check (section 7), checks the boundary, and reviews
    the diffs against sections 3 and 4;
  - writes a verification note in the change record, its only file change,
    and sets the batch or review tag;
  - when a check fails, it records the findings and stops. An
    implementation session fixes them as fix-up steps `B<n>.F<k>`, and a
    verification session checks again.
- **Closure session** (an implementation session the owner instructs after
  a review): records the owner's review outcome, turns rejected items into
  fix-up steps, and sets the final tag (section 6.4).
- **Pre-commit hook**: refuses any commit with a rule violation (G10).

### 5.2 Responsibility matrix

R: does the work. A: accountable or approves. C: consulted. I: informed.

| Activity | Owner | Implementation | Verification |
| -------- | ----- | -------------- | ------------ |
| Plan decisions (done 2026-11-03) | A, R | I | I |
| Execute assigned steps | I | A, R | — |
| Stay inside the batch boundary | I | R | checks |
| Progress table and session log | I | R | reads |
| Register a decision found during execution | A for bypassed ones | R | checks |
| Regenerate the behavior lock (only with a decision) | A | R | checks the commit body |
| Archive copies and deletions (G6) | A (CR-D03, CR-D04) | R | verifies `SHA256SUMS` |
| `RULES.md` amendment wording | A | R (draft) | checks rule-check consistency |
| Batch verification and verification note | I | C | A, R |
| Batch and review tags | I | — | R |
| Reviews at B1, B4 and B7 | A, R | C | C |
| Record a review outcome and set the final tag | A | R (closure) | — |
| Fix-up steps after a failed verification | I | R | re-verifies |
| Escalations | A (answers) | R (raises) | R (raises) |

### 5.3 Boundary rules

1. Each handoff lists the paths its batch may change, as a regular
   expression. At session end the boundary check (section 7.2) must print
   nothing.
2. A defect left by an earlier batch is fixed in the current batch only if
   the fix lies inside the current boundary, as a registered fix-up step
   `B<n>.F<k>` with its own commit. Otherwise escalate.
3. A verification session changes only the change record, and sets tags.
4. No session changes frozen content, assets, `data/` or `reports/`.
5. Only the owner approves `RULES.md` wording, decides the outcome of a
   bypassed decision, closes a review or waives a check.

---

## 6. Session protocol

### 6.1 Session lifecycle

1. **Start**:
   1. Read what the handoff's session prompt lists.
   2. Run the plan's resume procedure (`git status`, `git stash list`,
      progress table, gates).
   3. Confirm the handoff's entry conditions. If one fails, stop and report.
2. **Work**: execute the assigned steps in order, with the gates after each
   step and a commit per plan section 1.
3. **End**: only at a step boundary with a clean tree. Add a session-log
   entry (section 6.2) in a `docs` commit, or in the last step's commit.
   Make the final message to the owner a copy of that entry.

A session that runs out of room stops after its last finished step. It
never starts a step it cannot finish in the same session, unless the step is
a series of commits, in which case it stops between commits.

### 6.2 Session log

Append under "Session log" in the change record:

```text
### <YYYY-MM-DD> <session ID> (<implementation | verification | closure>)
- Steps: <IDs done>; <ID started and stashed, or "none">
- State: HEAD <short hash>; tests <count>; lock <green | updated by CR-Dnn>; rule check 0
- Findings: <new decisions, escalations, deviations, or "none">
- Next: <next step ID and session ID>; blockers: <or "none">
```

### 6.3 Interrupted step

If a step must stop midway (a tool failure, a lost context):

1. Run `git stash push -u -m "WIP Step B<n>.<m>: <reason>"`. The tree is
   now clean.
2. Commit a session-log entry that names the stash.

The next session sees the stash during the resume procedure. It reads the
stash with `git stash show -p`, then either pops it and finishes the step,
or drops it and restarts the step, and records which in its log entry.

### 6.4 Between batches and review closure

- **Handoff out**: the verification note plus the batch tag. The next
  batch's first session reads both.
- **Review points** (B1, B4, B7):
  1. The verification session sets `restructure-bN-review` and stops.
  2. The owner reviews and tells a session the outcome.
  3. That closure session records the outcome under "Verification notes" in
     a `docs` commit (`docs: record the owner review of batch BN`).
  4. Every rejected item becomes a fix-up step, which a verification session
     checks again.
  5. The closure session then sets `restructure-bN` (for B7,
     `restructure-done`, after plan B7.5).

### 6.5 Escalation

Escalate when a plan stop condition or a handoff trigger occurs:

1. Add an entry under "Escalations" in the change record: ID `E-<n>`, step,
   question, options, recommendation, and what is blocked.
2. Commit it.
3. Name it in the final message to the owner.
4. Continue with unblocked steps, or end the session. Never wait idle.

### 6.6 Verification note

A verification session appends one note under "Verification notes" in the
change record. It commits the note with `Session: B<n>-V` in the body, then
tags that commit if the batch is accepted.

```text
### <YYYY-MM-DD> B<n>-V
- Range: <entry-tag>..<short hash>; <count> commits
- Checks: <one line per handoff checklist item: pass, or fail with the detail>
- Measurements: tests <count> in <seconds> s; demo <seconds> s; lock green
- Result: accepted, tag <tag> | rejected, fix-up steps <B<n>.F1, ...>
```

---

## 7. Quality system

### 7.1 Gate levels

| Level | When | Who | Checks |
| ----- | ---- | --- | ------ |
| Step | Before each commit | Implementation | Plan 8.1 gates (tests, rule check, lock); the step's own check from the handoff; plan 8.6 for pure moves |
| Session | At session end | Implementation | Clean tree; boundary check (7.2); session-log entry |
| Batch | After the last step | Verification | Step gates at HEAD; wheel acceptance (plan 8.2); foreign directory (8.5); timings (8.4); the greps due by this batch (8.7); module layers; every commit names its step and carries no attribution; progress table complete; changed modules match sections 3 and 4 |
| Review | B1, B4, B7 | Owner | Verification note, archives, `RULES.md` wording, documents |
| Final | After B7 | Verification, then owner | Plan section 12 |

### 7.2 Boundary check

Run from the checkout root. `<entry-tag>` is the batch's entry tag, and the
pattern is the handoff's allowed-path expression. The command must print
nothing.

```sh
git diff --name-only <entry-tag>..HEAD | grep -vE '<allowed-path pattern>'
```

Commit hygiene for the batch: every commit body has a `Step:` or `Session:`
line (section 4.3), and none has an attribution line. This command lists the
commits that violate either rule, and must print nothing:

```sh
git log --format='%h %B%x00' <entry-tag>..HEAD | python3 -c "import sys; [print(c.split()[0]) for c in sys.stdin.read().split('\0') if c.strip() and (('Step: ' not in c and 'Session: ' not in c) or 'Co-Authored-By' in c or 'Generated with' in c)]"
```

### 7.3 Function-length metric

```sh
python3 - <<'EOF'
import ast, pathlib
for path in sorted(pathlib.Path('src/aimediator').rglob('*.py')):
    for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            length = node.end_lineno - node.lineno + 1
            if length > 60:
                print(length, path, node.name)
EOF
```

At `7282f49` this lists 8 functions in the package. After B5, none may
remain in `pipeline`, `runner`, `stages`, `evidence` or `retrieval`. The
functions listed in section 1.2 may remain.

---

## 8. Milestones and sessions

| Milestone | Batch | Exit tag | Owner involvement | Implementation sessions | Verification |
| --------- | ----- | -------- | ----------------- | ----------------------- | ------------ |
| M0 Plan approved | — | `restructure-plan` | Decisions (done) | — | — |
| M1 Safety net | B0 | `restructure-b0` | none | B0-1 | B0-V |
| M2 Defects fixed, archives | B1 | `restructure-b1-review`, then `restructure-b1` | Review | B1-1, closure | B1-V |
| M3 Engine split | B2 | `restructure-b2` | none | B2-1, B2-2 | B2-V |
| M4 Callers migrated | B3 | `restructure-b3` | none | B3-1, B3-2 | B3-V |
| M5 Layers removed, v1.3 | B4 | `restructure-b4-review`, then `restructure-b4` | Review, `RULES.md` v1.3 wording | B4-1, closure | B4-V |
| M6 Internals and performance | B5 | `restructure-b5` | none | B5-1, B5-2, B5-3 | B5-V |
| M7 Research code | B6 | `restructure-b6` | none | B6-1, B6-2 | B6-V |
| M8 Done | B7 | `restructure-b7-review`, then `restructure-done` | Final review, `RULES.md` v1.4 wording | B7-1, B7-2, closure (B7-3) | B7-V |

That makes 17 implementation sessions (closures included) and 8 verification
sessions. Batches run in order, each starting from the previous batch's
final tag. B5 and B6 may be swapped if the owner says so. They never run in
parallel, because both use `main` and the change record.

---

## 9. Lifecycle of these documents

- The plan, this blueprint and the handoffs are living documents until
  `restructure-done`. Corrections to them are `docs` commits that cite the
  reason.
- In B7.3, the interface contracts of section 3 that still describe the code
  are merged into `docs/design/cli.md`, section 5 (P6: useful handoff
  content merges into design). ADR 0002 (B4.5) keeps the module-boundary
  decision.
- In B7.5, after the owner's final review, the plan, this blueprint and the
  handoff directory move to `docs/archive/` with Status Archived. The change
  record is finalized and frozen (D3).
