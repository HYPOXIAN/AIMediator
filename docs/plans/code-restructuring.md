# Code Optimization and Restructuring Plan

- Type: Plan
- Status: Active
- Updated: 2026-11-03
- Applies to: commit `7282f49` and later; `RULES.md` v1.2; `aimediator` 0.1.0

The owner adopted every recommendation in section 9 on 2026-11-03. The
[blueprint](code-restructuring-blueprint.md) governs how the work is
organized: roles, sessions, contracts and standards. One handoff per batch in
`docs/plans/code-restructuring-handoffs/` assigns the work to sessions,
starting with [B0](code-restructuring-handoffs/b0-safety-net.md).

> **Basis**: [RULES.md](../../RULES.md) v1.2. Rule IDs (G, D, P) are cited directly.
> **Starting point**: commit `7282f49` on `main`. Tag `reorg-done` is at `745d7eb`.
> 222 offline tests pass and the rule check reports 0 violations.
> **Scope**: the code in `src/aimediator/`, `scripts/` and `tests/`, plus the
> documents that describe that code. Out of scope: prompt or model changes,
> new features, collected data, curated reports.
> **Predecessor**: the 2026-11 structural reorganization
> ([plan](../archive/reorganization.md), [record](../records/20261103-reorganization.md)).
> It moved files and documents. This plan restructures the code itself.

---

## How to use this plan (read first)

### Audience

Any coding agent with no memory of earlier sessions, and the project owner,
who answers section 9. You need this file, the blueprint, the handoff for
your batch, `RULES.md` and the change record. Line numbers refer to commit `7282f49`. They shift as work proceeds,
so locate code by the quoted function name when a line number no longer
matches.

### Read order

1. `RULES.md`, in full. It overrides this plan (G1).
2. The handoff for your batch in `docs/plans/code-restructuring-handoffs/`.
   It names your session, its steps and its boundary, and what else to read.
3. The [blueprint](code-restructuring-blueprint.md), at least the sections
   your handoff lists.
4. This plan, sections 0 to 6, once. Then the section 7 part for your batch,
   and section 8 for commands.
5. The change record `docs/records/<YYYYMMDD>-code-restructuring.md`, created
   in step B0.1. Its progress table names the next step.

### Resume procedure (start of every session)

1. `git status --short` must print nothing. If it prints anything, do not
   commit, stash or discard it: stop and report to the owner. Then run
   `git stash list`: an entry named `WIP Step ...` is an interrupted step,
   handled as the blueprint (section 6.3) describes.
2. Find the last finished step in the change record's progress table. The

   step's commit is found with `git log --grep 'Step: B<n>.<m>'`. The last
    tag (`git describe --tags --abbrev=0`) names the last finished batch.
3. Run the gates (section 8.1). If they fail on an unmodified checkout, stop

   and report. Do not fix forward a failure you did not cause.
4. Check section 9 for the decisions the next step depends on. If one is

   unanswered, skip the dependent steps (they are marked) and continue with
    independent ones.
5. Execute the step, run the gates, commit (section 1), and continue.

### Stop conditions

Stop, write the reason in the change record, and report to the owner when:

- the behavior lock (section 5) fails and no decision in section 9 authorizes
the change;
- a gate fails and the cause is not the current step;
- a step would modify a frozen record (D3), `data/raw/`, `data/evaluation/`,
`reports/`, or any file under `src/aimediator/assets/`;
- a step would need a new dependency, Python syntax newer than 3.9, network
access or a live model (every gate in this plan is offline);
- every remaining step is blocked by an unanswered decision.

---

## 0. Baseline (measured 2026-11-03 at `7282f49`)

| Item | Value |
| ---- | ----- |
| Tracked files | 195 |
| Package `src/aimediator/` | 20 modules, 3,444 lines; `engine.py` alone 931 |
| `scripts/` | `collect/` 4 files (824 lines), `experiments/` 18 (1,764), root forwarders 7 (92), `maintenance/` 3 (1,093) |
| Offline tests | 222 pass in about 70 s; the RULES.md P4 floor is 192 |
| Rule check | 0 violations; the pre-commit hook blocks commits with violations |
| Compatibility layers | 19 symlinks and 7 forwarding scripts ([register](../reference/compatibility-layers.md)) |
| Offline demo (`aimediator demo`) | 26.2 s; `engine.character_reference` has 688 calls and 19.4 s cumulative time (74 %) |
| Slowest tests | the presentation demo test takes 26.2 s; `test_cli_product` takes 31.1 s in total |
| Working-directory dependence | 1 test errors when the suite runs from outside the checkout |
| Installed-wheel acceptance | passes offline (18 commands) in a `--system-site-packages` virtual environment |
| Interpreters | Python 3.14.8 with NumPy 2.4.6. There is no `.venv/` in the checkout; the system Python 3.10 to 3.12 have no NumPy |

Section 8 gives the command behind every number. B0.4 measures them again.

---

## 1. Execution rules (apply to every step)

1. **Entry condition**: clean working tree; tests and the rule check pass.
2. **One kind of operation per commit** (G5). Most steps are one commit; a
   step whose text says so is a series of commits. The subject line uses
   `type: summary` with a type from P5 (`feat`, `fix`, `docs`, `refactor`,
   `chore`, `data`; commits that only change tests use `chore`). The body
   names the step, and the decision when there is one (example after this
   list). The step's last commit adds or updates its row in the progress
   table of the change record. **No attribution** (P6): no `Co-Authored-By`
   trailer, no "Generated with" line and no agent byline, even if the
   tooling suggests one.
3. **Moves and rewrites are separate.** A "pure move" step relocates code

   unchanged. Only import lines and module-qualified names may differ, and
    this is verified with section 8.6. Rewrites happen in later steps.
4. **Gates after every step** (section 8.1): offline tests, rule check and

   behavior lock. The pre-commit hook runs only the rule check, so run the
    tests yourself before committing.
5. **Behavior lock**: never regenerate it to make a step pass. It changes only

   in a step whose decision authorizes an output change, in the same commit,
    with the changed paths listed in the commit body (section 5.5).
6. **Batch exit**: a verification session that did not implement the batch
   reruns the gates and the installed-wheel acceptance (section 8.2), checks
   the batch against its handoff, records the result and sets the batch tag
   (`restructure-b0` to `restructure-b6`). At an owner review point (section
   6) it sets `restructure-bN-review` instead, and the batch tag (for B7,
   `restructure-done`) follows the owner's review. The blueprint (sections 5
   and 7) defines these roles.
7. **Rollback**: revert a step with `git revert <commit>`. Undo a batch by

   reverting its commits back to the previous tag. Restore archived files from
    `~/Archives/AIMediator/` (section 1, item 9).
8. **Decisions found during execution** follow the protocol of reorganization

   decision 13 ([archived plan](../archive/reorganization.md), section 7).
    Register the question, options and recommendation in the change record
    before acting. Implement only if a revert fully undoes the change and it
    neither changes behavior (the lock stays green), nor amends `RULES.md`, nor
    deletes content without an archive copy. Otherwise mark it `bypassed`,
    keep the current state and continue.
9. **Deleting tracked files** (G6): git history is the backup. In addition,

   copy the files to `~/Archives/AIMediator/scripts/<YYYYMMDD>-<topic>/` with
    a `SHA256SUMS` file, check that nothing outside frozen records and the
    archive refers to them, and enter path, archive location and reason in the
    change record.
10. **Documents**: every new or moved document gets the D2 header and an

    index entry in `docs/README.md` in the same commit, or the blocking hook
      refuses the commit (D4).

Commit message example (item 2):

```text
refactor: move evidence primitives out of engine.py

Step: B2.3
Decision: CR-D05
```

---

## 2. Invariants

### 2.1 Must not change

1. **CLI contract** ([design/cli.md](../design/cli.md), sections 3, 4, 6, 7

   and 8): commands, options, defaults, structured result keys, exit codes and
    error codes.
2. **Artifact names and schema versions**: `aimediator-run-v1`,

   `aimediator-state-v1`, `aimediator-coverage-v1`,
    `aimediator-source-review-v1`, `aimediator-review-overlay-v1`,
    `aimediator-report-v1`, `balance-evidence-v2`, `balance-report-v3`,
    `quality-evaluation-v1`, `aimediator-config-v1`, and every file name a run
    writes.
3. **Model requests**: the bytes of every `request.json`. That means the

   system prompt, the user JSON with its key order, the response schema with
    its property order (Ollama compiles property order into the decoding
    grammar, so order affects generation), the options and `keep_alive`. Also
    the stage order, the batch limits (12/18000, 8/10000, 4/9000 or 4/4000 for
    Chinese, and 1), retry counts and refinement rules.
4. **Asset bytes** under `src/aimediator/assets/`: prompts, policies,

   routing, glossary, anchors and fixtures.
5. **Determinism**: two report exports of the same run are byte-identical.
6. **Frozen content**: final records, decisions and meeting notes (D3);

   `data/raw/`, `data/evaluation/` (P1); `reports/` (P2).
7. **Runtime**: Python 3.9 syntax; NumPy stays the only runtime dependency

   and no other dependency is added; the package never imports `scripts/`,
    never starts subprocesses, and works from an installed wheel outside the
    checkout.
8. **Domain gates**: source binding, identity rules, numeric-intent checks,

   quality routing, the fail-closed semantic audit, and the rule that review
    cannot bypass checks (design/cli.md, section 3).

### 2.2 Accepted consequences

- Every package module is hashed into each CLI run identity
(`run_store.code_manifest`). Request cache identities include the run ID
through `quality_identity`. Every code commit therefore makes earlier CLI
runs non-resumable. That is intended (design/cli.md invariant 8;
[ADR 0001](../decisions/0001-package-as-single-runtime.md)). The behavior
lock normalizes these values (section 5.3).
- Legacy research runs (`engine.run`) hash all package modules
(`shared_code_sha256`), with the same consequence.

---

## 3. Diagnosis

Every finding has an ID that later steps cite.

### 3.1 Architecture

- `engine.py` is the hub. Its 931 lines mix the Ollama HTTP client and
streaming loop guards, JSON-schema construction, evidence segmentation,
identity glue, the content-addressed request journal (`Runner`), embedding
retrieval, orchestration (`process()`, lines 648 to 906, 259 lines),
report assembly and the legacy research command line.
- Current intra-package imports (function-level imports included):
  | Module | Imports |
  | ------ | ------- |
  | `engine` | balance_policy, common, evidence_quality, glossary_vectors, resources |
  | `inference` | common, **engine** |
  | `review` | common, **engine**, legacy_review |
  | `reporting` | common, **engine**, review |
  | `operations` | common, config, demo, **engine**, inference, resources, run_store |
  | `evaluation` | common, **engine**, quality_scoring, review |
  | `demo` | common, config, **engine**, inference, operations, reporting, resources, review |
  | `legacy_review` | **engine**, evidence_quality |
  | `cli` | common, config, demo, evaluation, operations, reporting, review |
  | others | only common, config, resources, balance_policy, evidence_quality |
- `inference.py` imports `engine` only to reach `common.strict_json` (line
19), `glossary_vectors.normalize` (lines 64 and 99) and `streamed_chat`
(line 77). The transport layer therefore depends on the orchestration
module.
- `demo` and `operations` import each other: `operations.py` line 70 and
`demo.py` line 78, both inside functions.
- [design/cli.md](../design/cli.md) section 5 planned separate `pipeline`,
`retrieval`, `evidence` and `preflight` modules. The
[implementation status](cli-implementation-status.md) ("Layout decisions")
records that the primitives stayed in `engine.py` to keep test patch seams.
Tests still replace `engine` module globals: `streamed_chat`
(`test_balance_analysis.py` lines 96 and 112, `test_balanced_collection.py`
line 93, `test_evidence_quality.py` line 291), `api`
(`test_balanced_collection.py` line 80, `test_evidence_quality.py` line 291)
and `retrieve` (`test_evidence_quality.py` line 291). Steps B2.1 and B2.2
replace these seams with explicit injection before anything moves.

### 3.2 Confirmed defects

- **F-01** `scripts/run_local_direction_comparison.py` crashes. It builds an
`argparse.Namespace` without `evidence_quality`, but `engine.process` reads
`args.evidence_quality` (line 652): `AttributeError`. Reproduced offline
with `engine.api` patched. The crash happens after a live `/api/tags` call,
so the script has not worked since the evidence-quality stage was added.
- **F-02** `scripts/experiments/demo_evidence_quality.py --mock-pipeline`
crashes. Its retrieval stub takes 4 positional parameters (line 18), but
`engine.process` passes 5 (line 655): `TypeError`. Reproduced offline.
- **F-03** Experiment run identities hash the 9- to 12-line forwarding scripts
instead of the implementation: `replay_balance_admission.py` line 45,
`run_balance_numeric_extraction_live.py` lines 16 and 17,
`run_balance_regression_live.py` lines 34 and 35,
`run_balance_semantic_controls_live.py` line 33,
`diagnose_evidence_quality_live.py` lines 35 to 41 (it also copies them as
"code snapshots", line 51), `run_quality_screening_experiment.py` lines 130
to 135, and `demo_evidence_quality.py` line 75. The forwarders never change,
so these identities cannot detect implementation changes, and a resumed
experiment can silently mix code versions.
- **F-04** `tests/test_balance_analysis.py` line 194 reads
`m.ROOT / 'prompts/verify-balance.en.txt'`, where `ROOT = Path.cwd()`
(`engine.py` line 27). The suite reports 1 error when it is not run from the
checkout root.
- **F-05** `engine.ground_claim` (lines 478 and 479) uses `assert` to enforce
that evidence spans equal the source text. `python -O` removes the check.
- **F-06** Text I/O without an explicit encoding: 88 `read_text`/`write_text`
calls in `scripts/`, 41 in `tests/` and 1 in `src/`, plus a few `open()`
calls. The result depends on the locale and breaks on the Chinese corpus
under a non-UTF-8 locale.
- **F-07** `scripts/collect/collect_balanced_feedback.py` lines 65 and 66: a
held collector lock raises a raw `BlockingIOError` traceback, whereas
`collect_feedback.py` and `expand_feedback.py` report it through
`parser.error`. The collectors never close their lock files, which causes a
`ResourceWarning` in the test run.
- **F-08** The library prints progress to stdout (`engine.py` lines 297, 384
and 905). `operations.analyze` hides this with
`contextlib.redirect_stdout` (`operations.py` line 135), and the test output
is noisy.

### 3.3 Performance

- **P-01** Re-parsing the glossary. `character_reference` (`engine.py` lines
402 to 409) reads and parses the 2.7 MB `assets/data/glossary.json` on every
call. `ground_claim` calls it three times and reads the glossary a fourth
time for `target_patch` (lines 432, 435, 468 and 477). That is about 110 ms
per claim. In the 38-case demo it accounts for 688 calls and 19.4 s of
26.2 s. Review import and report export pay the same cost, because
`review.load_run` grounds every proposal again.
- **P-02** `run_store.state` (lines 71 to 80) rescans every
`requests/**/validation.json` on each call. `operations.analyze` calls it
before every model request through the progress callback (`operations.py`
lines 116 to 118). The cost grows with the square of the request count: a
600-comment run with a few thousand requests reads millions of small files.
In the demo: 201 calls and 1.4 s.
- **P-03** `engine.process` rebuilds and rewrites `full-pipeline-coverage.json`
after every quality record (line 764), and `build_full_coverage` counts
claims per row with linear scans (lines 553 to 555). Both are quadratic in
the number of comments but small at current sizes. Measure before changing.
- **P-04** Import-time I/O: `engine.py` line 21 loads the anchors at import;
`scripts/collect/screen_feedback.py` line 4 parses the 2.7 MB glossary at
import.

### 3.4 Duplication

- **U-01** Prompts are loaded in two places: `engine.run` (lines 589 to 598)
and `operations.prompts_for` (lines 41 to 52), with the same names and
appendix rule.
- **U-02** JSON-schema builders exist twice, with a subtle difference:
`engine.py` lines 95 to 106, where `NULL_STRING` has no `minLength`, and
`evidence_quality.py` lines 32 to 42, where `NULL_STRING` has
`minLength: 1`. There is one validator, `evidence_quality.schema_errors`,
which `engine.schema_errors` wraps.
- **U-03** The character term list `[canonical_name, chinese_label] + alias texts` is built inline in 6 places: `engine.py` lines 414 and 471 to 472,
`balance_policy.py` lines 79 to 81, `evidence_quality.py` lines 247 to 248
and 283 to 284, and `scripts/experiments/export_balance_review_followups.py`
line 31. The sites filter empty entries differently.
- **U-04** The numeric-token regular expression exists twice:
`engine.numeric_tokens` (lines 417 and 418) and the lambda in
`evidence_quality.bind_claim` (line 256).
- **U-05** The fixture chat responder exists three times:
`demo.FixtureTransport.chat` (`demo.py` lines 35 to 74),
`demo_evidence_quality.mock_pipeline` (lines 23 to 49) and
`tests/test_evidence_quality.py` (lines 248 to 286).
- **U-06** Atomic JSON writers: `common.write`, `collect_feedback.write_json`
(lines 49 to 56), `run_grounded_feedback_live.save_json` (lines 35 to 40)
and `screen_feedback.write_rows` (lines 87 to 92, without fsync).
- **U-07** Environment-file parsing: `config.env_values` and
`collect_feedback.load_youtube_key`. The second is stricter on purpose.
- **U-08** The live extract, ground and audit loop is repeated in
`run_balance_controls_live.py`, `run_balance_numeric_extraction_live.py`,
`run_balance_regression_live.py`, `run_balance_semantic_controls_live.py`
and `diagnose_evidence_quality_live.py`.
- **U-09** Identity and snapshot logic: the legacy `engine.run` (lines 599 to
  643) next to `run_store.identity` and `run_store.initialize`.

### 3.5 Rule gaps the checker does not detect

- **R-01** P3 says `scripts/` holds thin entry points. Yet the collection
implementation lives in `scripts/collect/`: HTTP client, rate limiting,
storage, source adapters and screening rules, 824 lines. The experiments
also hold logic reused elsewhere: `prepare_balance_design.prepare_briefs` is
used by 3 scripts and 2 test files.
- **R-02** P7: `scripts/experiments/run_quality_screening_recovery.py` lines
36 to 48 hold two prompts outside `src/aimediator/assets/`.
- **R-03** G7 asks for one project-root constant. Two notions remain:
`engine.py` line 27 and `glossary_vectors.py` line 16 use `Path.cwd()`,
while scripts use `Path(__file__).parents[n]`. Reorganization decision 21
deferred this "to the CLI work".
- **R-04** G2: 19 symlinks and 7 forwarding scripts remain. This work can
meet their removal conditions R1 to R3.
- **R-05** P3: one-off scripts bound to the finished 100-comment
quality-screening experiment remain. `present_quality_screening_results.py`
emits a Cursor canvas TSX file. `protect_quality_screening_checkpoint.py`.
`resume_quality_screening_local.py` monkeypatches `engine` at import.
`run_quality_screening_recovery.py` (see also R-02).

### 3.6 Tests

- **T-01** 14 of 19 test files put `scripts/`, `scripts/collect/` and
`scripts/experiments/` on `sys.path` and import forwarders. 4 more load
scripts by file path with `importlib`.
- **T-02** Test modules import each other as fixture libraries:
`test_evidence_quality` is imported by three other test files.
- **T-03** Module-global patch seams (section 3.1).
- **T-04** No test locks the complete output of a run. A structural refactor
needs one (section 5).

### 3.7 Readability

- **S-01** Dense style: semicolon-joined statements and one-line blocks in
`cli.py`, `quality_scoring.py`, most experiment scripts and several tests.
- **S-02** Long functions: `engine.process` (259 lines),
`engine.Runner._generate` (112), `review.load_run` (136),
`reporting.export_report` (105) and `collect_feedback.Client.get` (74).
- **S-03** No type hints outside `common.py`, and few docstrings on public
functions.

---

## 4. Target architecture

### 4.1 Package modules

All modules are flat under `src/aimediator/`, except the `collection/`
subpackage (CR-D01). New modules are marked with their creation step.

| Module | Responsibility | Content comes from (`7282f49`) |
| ------ | -------------- | ------------------------------ |
| `common` | Strict JSON, canonical bytes, hashing, atomic write, `Failure`, input rows, new output paths | unchanged |
| `schema` (B2.3) | JSON-schema builders and the validator | `engine.py` lines 95 to 106; from B5.2 also `evidence_quality.py` lines 32 to 42 and 67 to 98 |
| `resources` | `asset_path`, `module_path`, cached loaders `glossary()` (B1.1), `anchors()`, `prompts(mode)` (B5.1); `workspace_root()` (B6.1) | `resources.py`; `engine.py` lines 589 to 598; `operations.py` lines 41 to 52 |
| `config` | unchanged | |
| `balance_policy` | unchanged rules | |
| `glossary_vectors` | unchanged; `ROOT` replaced in B6.1 | |
| `evidence` (B2.3) | `evidence_units`, `numeric_tokens`, `PARAMETER`, `CLAIM`, `character_reference`, `character_candidates`, `character_terms` (B5.3), `ground_claim` | `engine.py` lines 107 to 113, 178 to 190 and 402 to 480 |
| `evidence_quality` | unchanged logic; builders from `schema` (B5.2) | |
| `stages` (B2.5) | per-stage response schema (`schema_for`), request-data shaping, response normalization (B5.5), `exact_coverage` | `engine.py` lines 116 to 167 and 174 to 175; from B5.5 also lines 242 to 265 and 322 to 345 |
| `inference` | Ollama `api`, `streamed_chat`, `repeated_claim`, `Transport`, `probe` | `engine.py` lines 31 to 92, `inference.py` |
| `runner` (B2.6) | `Runner`: content-addressed request journal | `engine.py` lines 210 to 352 |
| `retrieval` (B2.7) | `retrieve` and anchor scoring | `engine.py` lines 355 to 399 |
| `pipeline` (B2.8) | `VERSION`, `batches`, `aggregate`, `quality_source_counts`, `build_full_coverage`, `validate_modes`, `process` (split into stage functions in B5.6) | `engine.py` lines 28, 197 to 207 and 483 to 906 |
| `engine` | legacy research runner only: `ROOT`, `run(args)`, `main()` | `engine.py` lines 27, 568 to 645 and 909 to 931 |
| `fixture_transport` (B2.9) | `FixtureTransport` | `demo.py` lines 12 to 74 |
| `run_store`, `operations`, `review`, `legacy_review`, `reporting`, `evaluation`, `quality_scoring`, `demo`, `cli`, `presentation` | unchanged responsibilities; imports updated | |
| `design_briefs` (B6.3, CR-D02) | engineering-brief readiness logic | `scripts/experiments/prepare_balance_design.py` lines 14 to 89 |
| `diagnostics` (B6.4, CR-D02) | shared live extract, ground and audit loop | U-08 |
| `collection/` (B6.2, CR-D01) | `client`, `store`, `sources`, `export`, `screening`, `balanced`, `expansion` | `scripts/collect/*.py` |

`run_store.code_manifest` hashes only top-level modules (`root.glob('*.py')`),
so the `collection/` subpackage stays outside CLI run identities. That is
correct, because analysis does not use it.

### 4.2 Dependency rules

Step B2.10 adds `tests/test_module_layers.py`. It parses every module under
`src/aimediator/`, including imports inside functions. It fails on any
intra-package import that is missing from the table below, and on any import
cycle. Every module may import `aimediator.__version__`. To change the table,
register a decision in the change record and update the test in the same
commit.

| Module | May import (intra-package) |
| ------ | -------------------------- |
| `common`, `schema`, `design_briefs` | none |
| `resources` | common |
| `config` | common, resources |
| `balance_policy` | resources |
| `glossary_vectors` | common, config, resources |
| `evidence` | common, resources, schema, balance_policy |
| `evidence_quality` | resources, schema, balance_policy, evidence |
| `stages` | schema, evidence, evidence_quality, balance_policy |
| `inference` | common, glossary_vectors |
| `runner` | common, stages, inference, evidence, evidence_quality |
| `retrieval` | common, resources, inference, glossary_vectors |
| `pipeline` | common, resources, balance_policy, evidence, evidence_quality, runner, retrieval |
| `run_store` | common, resources |
| `fixture_transport` | common, resources, inference, evidence |
| `operations` | common, config, resources, inference, run_store, pipeline, runner, retrieval, evidence_quality, balance_policy, fixture_transport |
| `legacy_review` | common, schema, evidence, evidence_quality, pipeline |
| `review` | common, schema, evidence, evidence_quality, balance_policy, legacy_review |
| `reporting` | common, evidence, evidence_quality, review |
| `quality_scoring` | common, evidence_quality |
| `evaluation` | common, schema, evidence, evidence_quality, quality_scoring, review |
| `demo` | common, config, resources, fixture_transport, operations, review, reporting |
| `cli` | common, config, operations, review, reporting, evaluation, demo |
| `presentation` | common, cli |
| `__main__` | cli |
| `engine` | common, resources, balance_policy, evidence, evidence_quality, glossary_vectors, inference, runner, retrieval, pipeline |
| `diagnostics` | evidence, evidence_quality, runner |
| `collection.*` | common, resources, other `collection` modules |

**Transitional allowance (B2.10 to B3.6 only)**: `engine` may re-export any
module. `review`, `reporting`, `operations`, `evaluation`, `demo` and
`legacy_review` may still import `engine`. The cycle check applies
throughout. B3.6 removes the allowance.

### 4.3 Entry points and the script layout afterwards

Research commands become package modules (CR-D05). They need the checkout
package on the import path, either through `pip install -e .` (see
`CLAUDE.md`) or `PYTHONPATH=src`.

| Command until B4 | Command from B4 |
| ---------------- | --------------- |
| `python3 scripts/run_balance_analysis.py ...` | `python3 -m aimediator.engine ...` |
| `python3 scripts/review_balance_sources.py ...` | `python3 -m aimediator.legacy_review ...` |
| `python3 scripts/evaluate_evidence_quality.py ...` | `python3 -m aimediator.quality_scoring ...` |
| `python3 scripts/glossary_vectors.py ...` | `python3 -m aimediator.glossary_vectors ...` |

Scripts that stay under `scripts/collect/` and `scripts/experiments/` begin
with the same two-line bootstrap the forwarders use today. Checkout scripts
therefore always run the checkout package:

```python
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator import evidence, runner  # import what the script uses
```

After the plan, `scripts/` has no files at its top level. It holds
`collect/` (4 thin wrappers), `experiments/` (13 scripts) and
`maintenance/` (unchanged).

### 4.4 Disposition of every script

| Script | Disposition | Steps | Decision |
| ------ | ----------- | ----- | -------- |
| `scripts/run_balance_analysis.py` | delete; use `python3 -m aimediator.engine` | B4.2 | CR-D05 |
| `scripts/review_balance_sources.py` | delete; use `python3 -m aimediator.legacy_review` | B4.2 | CR-D05 |
| `scripts/evaluate_evidence_quality.py` | delete; use `python3 -m aimediator.quality_scoring` | B4.2 | CR-D05 |
| `scripts/glossary_vectors.py` | delete; use `python3 -m aimediator.glossary_vectors` | B4.2 | CR-D05 |
| `scripts/evidence_quality.py`, `scripts/balance_policy.py` | delete (import-only forwarders) | B4.2 | CR-D05 |
| `scripts/run_local_direction_comparison.py` | archive (broken, F-01) | B1.7 | CR-D04 |
| `collect/collect_feedback.py`, `collect_balanced_feedback.py`, `expand_feedback.py` | thin wrappers over `aimediator.collection` | B1.3, B1.4, B6.2 | CR-D01 |
| `collect/screen_feedback.py` | glossary from the asset (B3.5), then a thin wrapper | B3.5, B6.2 | CR-D01 |
| `experiments/demo_evidence_quality.py` | archive (broken, F-02; `aimediator demo` supersedes it) | B1.7 | CR-D04 |
| `experiments/present_quality_screening_results.py`, `protect_quality_screening_checkpoint.py`, `resume_quality_screening_local.py`, `run_quality_screening_recovery.py` | archive (one-off, R-05, R-02) | B1.6 | CR-D03 |
| `experiments/prepare_balance_design.py` | thin wrapper over `aimediator.design_briefs` | B3.4, B6.3 | CR-D02 |
| `experiments/run_balance_controls_live.py`, `run_balance_numeric_extraction_live.py`, `run_balance_regression_live.py`, `run_balance_semantic_controls_live.py`, `diagnose_evidence_quality_live.py` | keep; package imports, assets, identities (F-03), shared `diagnostics` loop. `--prompt-dir` of the regression script defaults to `asset_path('prompts')` | B3.4, B6.4 | CR-D02, CR-D06 |
| `experiments/check_balance_regressions.py`, `evaluate_balance_review.py`, `export_balance_review_followups.py`, `review_balance_live.py`, `replay_balance_admission.py`, `run_quality_screening_experiment.py` | keep; package imports, assets, identities | B2.2, B3.4 | CR-D06 |
| `experiments/run_grounded_feedback_live.py` | keep frozen (historical pilot): bootstrap, encoding and root fixes only | B1.3, B3.4, B6.1 | CR-D02 |
| `maintenance/check_rules.py` | standalone and standard-library only; only the G3 allowlist changes | B4.4 | CR-D10 |
| `maintenance/verify_cli_install.py`, `maintenance/hooks/pre-commit` | unchanged | | |

### 4.5 Deliberately unchanged

- `check_rules.py` must keep running without the package.
- `presentation.py`: its Chinese output keys are product output, not
documentation (D8 covers documents).
- `run_grounded_feedback_live.py` keeps its own segmentation and HTTP code,
because they define a historical pilot's behavior.
- Prompts, policies, the glossary and every asset.
- No new CLI command and no new dependency.

---

## 5. Behavior lock (step B0.3)

### 5.1 Purpose

The lock proves that a step changed no observable behavior. It is the main
safety net for B2 to B7.

### 5.2 Scope

All four targets run offline, with fixture transports:

- **L1 CLI demo**: `aimediator.demo.demo(out, quiet=True)`, which produces
the `off`, `shadow` and `enforce` runs, `example-report/` and
`review-template/`.
- **L2 Legacy runner**: `engine.run(args)` in the three quality modes on the
packaged fixture cases. The transports return the responses
`FixtureTransport` returns: in B0 through the current module-global patches,
from B2.2 through injection.
- **L3 Reviewed report**: a review overlay imported from the demo template
with reviewer metadata set, as `verify_cli_install.py` does, and the report
exported with that overlay.
- **L4 Coarse screening**: the screening `classify()` result for every
`text_original` found in tracked files under `data/evaluation/` (rules only,
no network).

What is compared:

- for each produced file, the SHA-256 of its normalized bytes, keyed by its
normalized relative path;
- for each run, the sorted list of SHA-256 values of its normalized
`request.json` files (model-input equivalence, invariant 2.1.3).

### 5.3 Normalization

Replace only values that are known to vary. Discover them empirically rather
than guessing:

1. Produce outputs A and B from the same code into two different temporary

   directories. Every difference is time- or path-volatile (set V1).
2. Copy `src/` to a temporary directory, append the line `# lock probe` to

   the copy's `common.py`, and produce output C with `PYTHONPATH` pointing at
    the copy. The differences between A and C that are not in V1 are
    code-volatile (set V2): module hashes, run ID, request IDs and the
    fingerprints that hash them.
3. The normalizer parses JSON files and replaces V1 and V2 values by key path

   with placeholders. It replaces the same literals textually where they occur
    inside strings: JSON text inside message content, directory names under
    `requests/`, Markdown, CSV and JSONL files.
4. Everything else must be byte-stable. Do not exclude whole files, except the

   empty `.writer.lock`. List every exclusion and every volatile key in the
    change record.

### 5.4 Self-test (record the results in the change record)

Make each edit below temporarily, run the lock, and undo the edit without
committing it. The lock must **fail** for:

- one changed byte in a prompt asset;
- two properties swapped in `CLAIM`;
- the extraction batch count changed from 4 to 3;
- one word changed in the report Markdown text;
- a changed quality route reason.

The lock must **pass** for a comment appended to a module and for a rerun.

### 5.5 Files and updates

- `tests/behavior_lock.py`: producer and normalizer. Running
`python3 tests/behavior_lock.py --write` rewrites the fixture.
- `tests/test_behavior_lock.py`: compares the digests and, on failure, prints
the normalized paths that differ.
- `tests/fixtures/behavior-lock.json`: digests only, no corpus text.
- Update the fixture only in the commit that makes a change authorized by a
section 9 decision. The commit body lists the changed paths and the
decision.
- The lock runs the demo, which takes about 26 s until B1.1 and about 7 s
after it.

---

## 6. Batch overview

| Batch | Goal | Kind of risk | Needs decisions | Review point | Exit tag | Test delta (expected) |
| ----- | ---- | ------------ | --------------- | ------------ | -------- | --------------------- |
| B0 | Safety net and baseline | tests only | none | none | `restructure-b0` | + lock tests |
| B1 | Confirmed defects, hot spot, archives | small fixes; deletions with archive | CR-D03, CR-D04 (B1.6, B1.7) | after B1 (archives) | `restructure-b1` | +1, −9 if CR-D03 is adopted |
| B2 | Split `engine.py` by pure moves behind a facade | code moves | none | none | `restructure-b2` | +1 (layers) |
| B3 | Callers leave the facade and the forwarders | import changes | CR-D06 (B3.4) | none | `restructure-b3` | 0 |
| B4 | Remove compatibility layers; documentation; ADR | deletions, rule amendment | CR-D05, CR-D07, CR-D08, CR-D10 | after B4 | `restructure-b4` | −1 |
| B5 | Internal decomposition and performance | rewrites | CR-D12 (B5.11) | none | `restructure-b5` | + stage and state tests |
| B6 | Research code: workspace root, collection, shared helpers | moves and rewrites in research code | CR-D01, CR-D02, CR-D09 | none | `restructure-b6` | + helper tests |
| B7 | Readability and final acceptance | formatting (AST-checked), documents | CR-D10, CR-D11 | final | `restructure-done` | 0 |

The test count may never fall below the P4 floor (192). Record the count
after every step; every decrease needs a reason tied to a step. Batches run
in order. B5 and B6 are independent of each other and may be swapped.

---

## 7. Batches

Every step ends with the gates (section 8.1) and a commit (section 1). "Lock
unchanged" means the behavior lock passes without regeneration.

### B0 Safety net and baseline

Entry: the owner has answered section 9 and set this plan to Active.

- **B0.1** `docs`: create the change record
`docs/records/<YYYYMMDD>-code-restructuring.md` from the section 10
skeleton, with the start date as prefix. Copy the owner's answers into it,
and add it to `docs/README.md`.
- **B0.2** `chore`: fix F-04. The test reads the prompt with
`asset_path('prompts/verify-balance.en.txt')`. Verify with section 8.5,
which must report no failure.
- **B0.3** `chore`: add the behavior lock (section 5) with targets L1 to L4.
Run the self-test (section 5.4) and record its results.
- **B0.4** `docs`: measure every section 0 item again with section 8 and
record the results in the change record.

Exit: tag `restructure-b0`.

### B1 Confirmed defects, the main hot spot, archives

- **B1.1** `refactor` (P-01): add `resources.glossary()`, a
`functools.lru_cache(maxsize=1)` loader that returns the parsed glossary.
`character_reference` and `ground_claim` use it and never mutate it. Add a
test showing that mutating a returned reference does not change the next
call's result. Lock unchanged. Measure with section 8.4: the cumulative
time of `character_reference` must fall below 1 s and the demo below 10 s.
- **B1.2** `fix` (F-05): replace the `assert` in `ground_claim` with
`if ...: raise AssertionError(...)`. This keeps the exception type, and
with it the CLI exit code 1, and survives `python -O`.
- **B1.3** `fix` (F-06): pass `encoding='utf-8'` to every text read and write
in `src/`, `scripts/` and `tests/`, including text-mode `open()`. The
section 8.7 grep must return nothing. Lock unchanged. Under a UTF-8 locale,
output bytes are unchanged.
- **B1.4** `fix` (F-07): `collect_balanced_feedback.py` reports a held lock
through `parser.error`. The collectors close their lock handles on exit.
- **B1.5** `chore`: capture current stdout progress lines in a test, so that
B5.7 can prove the legacy console text is preserved.
- **B1.6** `chore` (CR-D03; skip if not adopted): archive the four
quality-screening one-off scripts and their tests
(`test_quality_screening_compact.py`, 4 tests;
`test_quality_screening_recovery.py`, 5 tests) following section 1, item 9.
Update "Used by" in the register.
- **B1.7** `chore` (CR-D04): archive `scripts/run_local_direction_comparison.py`
and `scripts/experiments/demo_evidence_quality.py`. Remove the R3 row from
the register and add a change-log entry there. Update the "Used by" cell of
the `cases.json` symlink row. Update the mentions in
`docs/design/balance-analysis.md` (line 45) and `docs/design/cli.md` (line
90). If CR-D04 is rejected, fix both scripts
instead: add `evidence_quality='off'`, `quality_only=False` and
`relevance_only=False` to the namespace, and give the retrieval stub the
signature `(rows, base, out, model, embedding_config=None)`.

Exit: lock unchanged, timings recorded. Tag `restructure-b1-review`, wait for
the owner, then tag `restructure-b1`.

### B2 Split `engine.py` by pure moves

- **B2.1** `refactor`: `engine.run(args, *, api_transport=None, chat_transport=None, embed_transport=None, retrieval_service=None)`. A
`None` resolves at call time to today's module-level function, so the
module-global patches still work. Pass the values through to `retrieve` and
`Runner`. Lock unchanged.
- **B2.2** `chore`: tests, scripts and the lock harness stop patching
`engine` globals and use the B2.1 parameters or
`Runner(..., chat_transport=...)`. Sites: `test_balance_analysis.py`
(lines 96 and 112), `test_balanced_collection.py` (lines 80 and 93),
`test_evidence_quality.py` (lines 291 and 292),
`replay_balance_admission.py` (line 33), `tests/behavior_lock.py`, and
`demo_evidence_quality.py` (line 54) if CR-D04 kept it.
`test_balanced_collection.py` line 80 also patches
`glossary_vectors.embed`: pass `embed_transport` instead. Patches of `urllib.request.urlopen` reach
the shared `urllib` module and may stay. Verify:
`git grep -nE "patch(\.object)?\((m|engine) *, *'(api|streamed_chat|retrieve|Runner)'" -- tests scripts`
prints nothing.
- **B2.3** `refactor`: create `schema.py` with the `engine.py` builders
(`obj`, `arr`, `STRING`, `NULL_STRING`, `BOOL`) and `evidence.py` (see
section 4.1). `engine.py` imports the moved names back, so the facade keeps
every name importable. Verify the move (section 8.6).
- **B2.4** `refactor`: move `api`, `repeated_claim` and `streamed_chat` into
`inference.py`. In the same commit, `inference` stops importing `engine`:
it uses `common.strict_json`, `glossary_vectors.normalize` and its own
`streamed_chat`. Doing both together avoids an import cycle.
- **B2.5** `refactor`: move `schema_for` and `exact_coverage` into
`stages.py`.
- **B2.6** `refactor`: move `Runner` unchanged into `runner.py`. Its default
chat transport is `inference.streamed_chat`.
- **B2.7** `refactor`: move `retrieve` into `retrieval.py`. It gets `POS` and
`NEG` from `resources.anchors()`.
- **B2.8** `refactor`: move `VERSION`, `batches`, `aggregate`,
`quality_source_counts`, `build_full_coverage`, `validate_modes` and
`process` into `pipeline.py`. `engine.py` keeps `ROOT`, `run`, `main` and
the facade re-exports, and its docstring states that the facade is removed
in B3.6.
- **B2.9** `refactor`: move `FixtureTransport` into `fixture_transport.py`.
`operations` imports it from there, which breaks the `demo` and
`operations` cycle.
- **B2.10** `chore`: add `tests/test_module_layers.py` (section 4.2, with the
transitional allowance).

Exit: lock unchanged at every step. Tag `restructure-b2`.

### B3 Callers leave the facade and the forwarders

- **B3.1** `refactor`: package modules import from the new modules instead of
`engine`:
  - `review.relevance_agrees` becomes `balance_policy.retrieval_review_agrees`;
  `CLAIM`, `ground_claim`, `character_reference` and `evidence_units` come
  from `evidence`; `schema_errors` from `evidence_quality` (it moves to
  `schema` in B5.2); quality functions from
  `evidence_quality`. The same applies to `reporting`, `operations`,
  `evaluation`, `fixture_transport` and `legacy_review`.
  - `legacy_review` also drops its unused `ROOT` import.

  Verify with section 8.7: no `engine` import remains in the package outside
  `engine.py`.
- **B3.2** `chore`: create `tests/support.py` for the shared fixtures (case
builders, qualified records, the fixture chat responder, and the cases read
through `asset_path('fixtures/cases.json')`). This removes the imports
between test modules (T-02).
- **B3.3** `chore`: tests import package modules instead of forwarders. Keep
`scripts/...` on `sys.path` only where a test exercises a script itself.
Commit one test area at a time.
- **B3.4** `refactor` (CR-D06 for the identity part): experiment scripts use
the section 4.3 bootstrap and `aimediator` imports. They read assets with
`asset_path`. They hash the package modules they use (`module_path(...)`)
instead of forwarders and symlinks (F-03). `run_balance_regression_live.py`
defaults `--prompt-dir` to `asset_path('prompts')`. Commit one script group
at a time. If CR-D06 is rejected, leave the identity code unchanged and skip
B4.2.
- **B3.5** `refactor`: `screen_feedback.py` reads the glossary through
`asset_path` instead of `data/glossary.json`. Lock target L4 unchanged.
- **B3.6** `refactor`: remove the facade re-exports. `engine.py` keeps only
what `run` and `main` use. Remove the transitional allowance from
`test_module_layers.py`.

Exit: tag `restructure-b3`.

### B4 Remove the compatibility layers; documentation

- **B4.1** `docs`: living documents switch to the section 4.3 commands and to
asset paths (D9):
  - `README.md` ("Research and compatibility commands", "Layout");
  - `docs/guides/cli-usage.md` (line 182);
  - `docs/design/balance-analysis.md` (lines 6, 8, 29 and 168, plus the
  prompt and policy paths);
  - `docs/design/cli.md` (section 2, lines 75 to 87);
  - `docs/design/evidence-quality.md` (lines 33, 42 and 47);
  - `docs/reference/glossary-vector-index.md` (lines 28 and 29).

  Frozen records and the archive keep their historical text (CR-D07).
- **B4.2** `refactor` (CR-D05, R2): delete the six pure forwarders and their
register rows. Delete
`test_refactored_boundaries.test_compatibility_imports_share_package_state`
(−1 test; record the reason). G2 and P3 must report 0.
- **B4.3** `refactor` (CR-D07, CR-D08, R1): delete the 14 prompt symlinks and
`prompts/`, the 3 policy and routing symlinks in `configs/`, and
`data/glossary.json`. Keep `data/evaluation/evidence-quality-synthetic-v1/cases.json`
and set its removal condition to "kept: member of a frozen evaluation set".
Update the register and the README "Layout". The section 8.7 grep must find
no user of the deleted paths in code, tests or living documents.
- **B4.4** `docs` and `chore` (CR-D10, two commits): `RULES.md` v1.3, in which
G3 no longer lists `prompts/` and P3 gains the CR-D02 clarification, with a
revision-log entry. Then drop `'prompts'` from `G3_ALLOWED` in
`check_rules.py` and from its test.
- **B4.5** `docs`: ADR `docs/decisions/0002-module-boundaries-and-entry-points.md`
covering the module table, the layering test, the `python -m` entry points
and the removal of the layers (D9). Index it.

Exit: tag `restructure-b4-review`, wait for the owner, then tag
`restructure-b4`.

### B5 Internal decomposition and performance

- **B5.1** `refactor` (U-01): `resources.prompts(mode)` becomes the only
prompt loader. `operations.prompts_for` stays as a one-line alias, because
`tests/test_cli_product.py` line 335 uses it. Lock unchanged
(`prompt-snapshot.json`).
- **B5.2** `refactor` (U-02): `schema.py` holds the only builders and
validator. Keep both nullable-string variants with their exact current
dictionaries, under the names `NULLABLE_STRING` (from `engine.py`) and
`NULLABLE_NONEMPTY_STRING` (from `evidence_quality.py`). Keep both object
builders as well. The one from `engine.py` orders its keys `type`,
`additionalProperties`, `properties`, `required`; the one from
`evidence_quality.py` orders them `type`, `properties`, `required`,
`additionalProperties`. That order is part of the request bytes (blueprint,
section 3.3). Request lock unchanged.
- **B5.3** `refactor` (U-03): `evidence.character_terms(entry)` returns the
raw ordered list, `None` included. Each of the six sites keeps its own
filtering, so results stay identical.
- **B5.4** `refactor` (U-04): `evidence_quality.bind_claim` uses
`evidence.numeric_tokens`.
- **B5.5** `refactor`: split `Runner._generate`. The `stages` module gets
`prepare(stage, data, ids)` (verify-stage shaping), `options(stage, policy)` and `normalize(stage, parsed, ids, data)`. `Runner` keeps the
journal, the cache lookup, transport errors and the validation record.
Request lock unchanged.
- **B5.6** `refactor` (S-02): split `pipeline.process` into stage functions
that share one state object (a `dataclass`): triage, retrieval review,
relevance with refinement, quality, extraction, audit and assembly. Keep
every intermediate write (file, content and order) where it is, because
partial runs and resume read them. Aim for functions of about 60 lines or
fewer. Lock unchanged; the resume and interruption tests pass.
- **B5.7** `refactor` (F-08): a progress callback replaces `print` in
`pipeline`, `runner` and `retrieval`. `engine.main` passes a stdout printer,
so the research console text stays identical (B1.5 test).
`operations.analyze` drops `redirect_stdout`.
- **B5.8** `refactor` (P-02): `run_store.state` tracks completed request
identities incrementally, for example from the progress callback or by
scanning only new request directories. The content of `run-state.json` at
each write stays identical. Add a test counting file reads, and measure a
synthetic run with about 2,000 request directories before and after.
- **B5.9** `refactor` (P-03, conditional): measure a synthetic 600-comment
shadow run with fixture transports. Change the coverage rebuild only if it
takes more than 10 % of the run time; otherwise record "measured, not
needed".
- **B5.10** `refactor` (P-04): the package no longer reads files at import
time. Anchors load lazily through the cached `resources.anchors()`.
- **B5.11** `refactor` (CR-D12; skip if not adopted): legacy `engine.run`
additionally snapshots every package module into `code-snapshot/`. The
existing three snapshot files stay. This step updates lock target L2
(section 5.5).

Exit: tag `restructure-b5`.

### B6 Research code: workspace root, collection, shared helpers

- **B6.1** `refactor` (CR-D09, R-03): add `resources.workspace_root()`. It
returns the checkout root when the package is imported from a checkout
(`Path(aimediator.__file__).parents[2]` contains `RULES.md`), and the
working directory otherwise. `engine.ROOT`, `glossary_vectors.ROOT` and
`DEFAULT_INDEX`, and every script root use it. Verify with section 8.5 and
`python3 -m aimediator.engine --help` run from a foreign directory: the
defaults point into the checkout.
- **B6.2** `refactor` (CR-D01, R-01): create `src/aimediator/collection/`
with `client.py` (`Halt`, `RestrictedRedirect`, `Client`, `retry_delay`,
`HOSTS`, `load_youtube_key`), `store.py`, `sources.py` (`steam`, `bluesky`,
`youtube`, `guess_language`, `timestamp`), `export.py`, `screening.py`,
`balanced.py` and `expansion.py`.
  - Each script in `scripts/collect/` keeps its arguments and defaults and
  calls the package. The state location stays under
  `workspace_root() / 'runs/state'`.
  - JSON writes use `common.write` (U-06). The stricter
  `load_youtube_key` stays separate from `config.env_values` (U-07).
  - The screening summary's `script_sha256` now hashes `screening.py`.
  Record this change of meaning in the change record.
  - Tests import the package. Lock target L4 unchanged.
  - Move one module per commit, starting with `screening`.
- **B6.3** `refactor` (CR-D02): create `aimediator.design_briefs` from
`prepare_balance_design.py`. Update the script, `check_balance_regressions.py`,
`review_balance_live.py` and the tests to use it.
- **B6.4** `refactor` (CR-D02, U-08): create `aimediator.diagnostics` with the
shared extract, ground and audit loop. The five live scripts use it. Add
offline tests with a fake chat transport. Live reruns are out of scope;
record that they were not performed.

Exit: tag `restructure-b6`.

### B7 Readability and final acceptance

- **B7.1** `refactor` (CR-D11): one statement per line and no semicolon joins
in the agreed scope. Commit one file group at a time. Every commit must be
AST-equivalent (section 8.6).
- **B7.2** `refactor` (S-03): docstrings and type hints for the public
functions of `common`, `resources`, `schema`, `evidence`, `stages`,
`runner`, `retrieval`, `pipeline` and `run_store`. Use
`from __future__ import annotations` for Python 3.9 compatibility.
- **B7.3** `docs`: update `docs/design/cli.md` section 5 to the actual layout,
stating how it differs from the original target. Also update
`docs/plans/cli-implementation-status.md` ("Layout decisions"), the README
"Layout", the register and the index.
- **B7.4** `docs` (CR-D10): `RULES.md` v1.4 raises the P4 floor to the final
test count and adds a revision-log entry.
- **B7.5** `docs`: final acceptance.
  1. Run every gate (8.1), the wheel acceptance (8.2), the foreign working
     directory check (8.5), the timings (8.4) and the greps (8.7), and record
     the results. The verification session then sets `restructure-b7-review`,
     and the owner gives the final review.
  2. After the review: move this plan, the blueprint and the handoff
     directory to `docs/archive/` with Status Archived, and update every
     inbound link (D5).
  3. Finalize the change record and freeze it (D3), then tag
     `restructure-done`.

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

Expected: one JSON line with `"passed": true` and `"commands": 18`. The
build also writes the ignored `build/` and `src/aimediator.egg-info/` into
the checkout. Leave them: they are reproducible (G4), and an existing
editable install may use the metadata.

### 8.3 Behavior lock

```sh
python3 -m unittest discover -s tests -p 'test_behavior_lock.py'
python3 tests/behavior_lock.py --write        # only under section 5.5
```

### 8.4 Timing and profile

```sh
time python3 -m unittest discover -s tests -q
python3 - <<'EOF'
import cProfile, pathlib, pstats, sys, tempfile
sys.path.insert(0, 'src')
from aimediator.demo import demo
out = pathlib.Path(tempfile.mkdtemp()) / 'demo'
profile = cProfile.Profile(); profile.enable(); demo(out, quiet=True); profile.disable()
stats = pstats.Stats(profile)
print('demo total %.1fs' % stats.total_tt)
stats.sort_stats('cumulative').print_stats('aimediator', 15)
EOF
```

### 8.5 Foreign working directory

```sh
R=$(pwd); (cd "$(mktemp -d)" && python3 -m unittest discover -s "$R/tests" -t "$R/tests" -q)
```

### 8.6 Move and format equivalence

Pure moves: every top-level function or class of the old file must exist with
an identical AST in one of the new files. Save the script below to a
temporary file and run it as
`python3 <file> <base-commit> src/aimediator/engine.py src/aimediator/*.py`.

```python
import ast, subprocess, sys
base, old_file, new_files = sys.argv[1], sys.argv[2], sys.argv[3:]
def defs(text):
    return {n.name: ast.dump(n) for n in ast.parse(text).body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
old = defs(subprocess.run(['git', 'show', base + ':' + old_file], check=True,
                          capture_output=True, text=True).stdout)
new = {}  # one name can be defined in several modules (main, obj, load_policy)
for name in new_files:
    with open(name, encoding='utf-8') as handle:
        for key, dump in defs(handle.read()).items():
            new.setdefault(key, set()).add(dump)
for name, dump in sorted(old.items()):
    print('same' if dump in new.get(name, ()) else 'MISSING' if name not in new else 'CHANGED', name)
```

On the unmodified tree at `7282f49`, the command prints `same` for all 24
definitions of `engine.py`.

`same` is required, except for names the step lists as intentionally changed;
a change in a module-qualified call such as `quality.` to `evidence_quality.`
counts as intentional and must be listed. For formatting commits (B7.1), each
file's `ast.dump(ast.parse(old))` must equal `ast.dump(ast.parse(new))`.

### 8.7 Greps

```sh
# No forwarder imports (after B3)
git grep -nE "^(import|from) (run_balance_analysis|evidence_quality|balance_policy|review_balance_sources|evaluate_evidence_quality|glossary_vectors)\b" -- tests scripts
# No engine imports inside the package except engine.py (after B3.1)
git grep -nE "from \. import engine|from \.engine import|\bengine\." -- src/aimediator ':!src/aimediator/engine.py'
# No users of the symlink paths (before B4.3)
git grep -nE "(^|[^a-z/])(prompts/[a-z-]+\.(en|zh)\.txt|configs/(balance-review-policy|evidence-quality-policy|local-language-routing)\.json|data/glossary\.json)" -- src scripts tests README.md docs/guides docs/design docs/plans docs/reference
# No working-directory roots outside workspace_root's fallback (after B6.1)
git grep -n "Path.cwd()" -- src scripts ':!src/aimediator/resources.py'
# Explicit encodings (after B1.3)
git grep -nE "\.(read_text|write_text)\(" -- src scripts tests | grep -v "encoding="
```

Each command must print nothing at the stated point. In the third grep, this
plan's own mention of the paths is expected until it is archived.

---

## 9. Decisions for the owner

The owner adopted all twelve recommendations on 2026-11-03, in the planning
session. Adopting CR-D06 includes the owner's confirmation that no experiment
output must be resumed or replayed under its old identity. B0.1 copies the
answers into the change record. The blueprint (section 1.1) states what each
answer binds.

| ID     | Question                                                        | Recommendation                                     | Steps                  | Owner answer |
| ------ | --------------------------------------------------------------- | -------------------------------------------------- | ---------------------- | ------------ |
| CR-D01 | Move the collection implementation into `aimediator.collection` | yes                                                | B6.2                   | adopt        |
| CR-D02 | P3 reading for experiment scripts                               | experiment-specific code stays; shared logic moves | B3.4, B4.4, B6.3, B6.4 | adopt        |
| CR-D03 | Archive the four quality-screening one-off scripts (−9 tests)   | archive                                            | B1.6                   | adopt        |
| CR-D04 | The two broken scripts (F-01, F-02)                             | archive                                            | B1.7                   | adopt        |
| CR-D05 | Replace the forwarders with `python -m aimediator.<module>`     | yes                                                | B4.1, B4.2             | adopt        |
| CR-D06 | Experiment identities hash package modules                      | yes                                                | B3.4                   | adopt        |
| CR-D07 | R1 exempts frozen records and the archive; delete 18 symlinks   | yes                                                | B4.3                   | adopt        |
| CR-D08 | Keep the evaluation-set `cases.json` symlink permanently        | keep                                               | B4.3                   | adopt        |
| CR-D09 | One `workspace_root()` helper (reorganization decision 21)      | yes                                                | B6.1                   | adopt        |
| CR-D10 | `RULES.md` v1.3 (G3, P3) and v1.4 (P4 floor)                    | yes                                                | B4.4, B7.4             | adopt        |
| CR-D11 | Scope of the style normalization                                | `src/` and `scripts/`                              | B7.1                   | adopt        |
| CR-D12 | Legacy runs snapshot every package module                       | yes                                                | B5.11                  | adopt        |

**CR-D01 Collection code in the package.** P3 says `src/aimediator/` is the
only implementation and scripts are thin. The collectors (824 lines) sit in
`scripts/collect/`. Options:

- (a) move them into the `aimediator.collection` subpackage with no CLI
command, so the wheel ships the code but no data;
- (b) keep them and amend P3.

Recommendation: (a). It satisfies P3 without a rule change, gives the
collectors the shared helpers and tests against the package, and keeps them
out of CLI run identities (section 4.1). If rejected, skip B6.2 and add the
amendment to CR-D10.

**CR-D02 What "thin" means for experiments.** Moving every experiment into
the package would ship one-off research code in the product.

Recommendation: experiment scripts may keep experiment-specific
orchestration, case lists and report formatting. Logic used by two or more
scripts, or by tests, moves into the package: `design_briefs` and
`diagnostics`. `run_grounded_feedback_live.py` stays as a frozen historical
pilot. Add one clarifying sentence to P3 in v1.3 (CR-D10). If rejected,
B6.3 and B6.4 still run, but P3 is not amended.

**CR-D03 Quality-screening one-off scripts.** The scripts are
`present_quality_screening_results.py`, `protect_quality_screening_checkpoint.py`,
`resume_quality_screening_local.py` and `run_quality_screening_recovery.py`.
They are bound to the finished 100-comment experiment (reports
`quality-screening-existing-100-v1` and `-recovered-v2`), and the recovery
script holds prompts outside the assets (R-02).

Recommendation: archive them to `~/Archives/AIMediator/scripts/`, as in
reorganization decision 15, with their 9 tests. `run_quality_screening_experiment.py`
is parameterized and stays. If rejected, B3.4 must migrate all four, and
R-02 needs its prompts moved into the assets, which P7 treats as a behavior
change with a record.

**CR-D04 Broken scripts.** F-01 and F-02 have crashed since the
evidence-quality stage was added, so nobody uses them. `aimediator demo`
supersedes `demo_evidence_quality.py`. Options:

- (a) archive both;
- (b) fix both (the fix is given in B1.7).

Recommendation: (a). It also meets R3 for the wrapper.

**CR-D05 Research entry points.** Recommendation: the four documented
commands become `python3 -m aimediator.<module>` (section 4.3), and the six
pure forwarders are deleted. This meets R2 once B3 and B4.1 are done.
Alternative: keep them as registered layers indefinitely.

**CR-D06 Experiment identities.** Hashing the package modules instead of the
forwarders fixes F-03. It changes what the identity means, so an experiment
directory created before the change cannot be resumed. This is the R2
condition.

Recommendation: adopt, after the owner confirms that no experiment output
under `runs/` must still be resumed or replayed with its old identity. If
rejected, skip the identity part of B3.4, and then also B4.2.

**CR-D07 Removal condition R1.** R1 requires that "no tracked file names the
link path any more", but frozen records and the archive name the old paths
as history, and D3 forbids editing them. All such mentions are code spans,
not links, so the link check is unaffected.

Recommendation: read R1 as code, tests, configuration and living documents
only. Delete the 14 prompt, 3 configuration and 1 glossary symlinks, and
record the reading in the register.

**CR-D08 The evaluation-set** `cases.json` **link.** The frozen set
`data/evaluation/evidence-quality-synthetic-v1/` lists `cases.json` in its
manifest. The packaged fixture is the single source (reorganization decision
9). Options:

- (a) keep the symlink permanently, with removal condition "kept";
- (b) remove it and change the frozen manifest.

Recommendation: (a). P1 freezes the set.

**CR-D09 Project root (G7, reorganization decision 21).** Options:

- (a) keep both notions;
- (b) use `Path.cwd()` everywhere;
- (c) one helper, `workspace_root()`: the checkout containing the imported
package, else the working directory.

Recommendation: (c). Scripts and `python -m` commands then resolve the same
root from any directory. With an installed wheel outside a checkout, the
helper falls back to the working directory, which is today's package
behavior.

**CR-D10 Rule amendments.**

- v1.3 (B4.4): G3 no longer lists `prompts/`. G3 already says the directory
"is removed once it is empty". P3 gains the CR-D02 sentence.
- v1.4 (B7.4): the P4 floor rises from 192 to the final count, so later work
cannot drop tests silently.

Recommendation: adopt both. The amendments state date and reason (G1).

**CR-D11 Style normalization.** One statement per line, verified
AST-equivalent. Options:

- (a) `src/` and `scripts/`;
- (b) also `tests/`;
- (c) none.

Recommendation: (a). Tests change in B3 anyway, and a full reformat of them
adds churn without a safety benefit.

**CR-D12 Legacy run code snapshots.** After the split, the legacy
`runner-snapshot.py` would contain only the small `engine.py`, which weakens
provenance. Options:

- (a) add `code-snapshot/<module>.py` for every package module and keep the
three existing files;
- (b) keep today's snapshots.

Recommendation: (a). The change touches only lock target L2, updated in the
same commit.

---

## 10. Change record skeleton (copy in B0.1)

```markdown
# Code Restructuring Change Record

- Type: Record
- Status: Active
- Updated: <YYYY-MM-DD>
- Applies to: commit `7282f49` and later; `RULES.md` v1.2 and later amendments

The single change record of the code restructuring
([plan](../plans/code-restructuring.md)). Every step adds its row to the
progress table in its own commit. Deletions are entered under "Archive and
deletions" (G6). Frozen when the plan is finished (D3).

## Owner decisions

| ID | Answer | Date | Notes |
| -- | ------ | ---- | ----- |

## Progress

The commit of a step is found with `git log --grep 'Step: <ID>'`.

| Step | Status | Tests | Lock | Notes |
| ---- | ------ | ----- | ---- | ----- |

## Baseline measurements (B0.4)

## Behavior lock (B0.3): volatile keys, exclusions, self-test results

## Archive and deletions

| Path | Archive location | SHA256SUMS entry | Reason | Step |
| ---- | ---------------- | ---------------- | ------ | ---- |

## Decisions found during execution

## Escalations

## Verification notes

## Session log

## Batch results

## Deferred
```

The blueprint (section 6) defines the formats of the session log, the
escalations and the verification notes.

`Status` is one of `done`, `skipped (CR-Dnn not adopted)` or
`bypassed (see Decisions found during execution)`.

---

## 11. Risks and mitigations

| Risk | Mitigation |
| ---- | ---------- |
| Request payloads drift (schema property order, user JSON key order) and silently change model behavior | Request digests in lock targets L1 and L2; pure-move verification (8.6); B5.2 keeps both schema variants verbatim |
| Moved code escapes module-global patches, so a test reaches the network | B2.1 and B2.2 come before any move; B2.2's grep; a test that hangs on network access is a stop condition |
| The cached glossary is mutated by a caller | B1.1 copy test; callers build new objects, as they do today |
| Intermediate writes move during the B5.6 decomposition and break resume or partial reports | Section 7 rule "keep every intermediate write"; lock; existing resume and interruption tests |
| Hidden users of deleted paths | Section 8.7 greps; the G2, D5 and P3 checks |
| The behavior lock is "fixed" by regenerating it | Section 1, item 5; regeneration only under section 5.5 with a decision |
| The blocking hook refuses a commit with a new document | Section 1, item 10 |
| Tooling adds attribution trailers | Section 1, item 2 (P6) |
| An owner edit of Markdown reflows code spans containing `*` | Run the rule check after owner edits and inspect the affected code spans |
| Identity changes break an experiment someone still needs | CR-D06 asks the owner first |

---

## 12. Completion criteria

The restructuring is complete when all of the following hold:

1. Every step is `done` or `skipped` or `bypassed` with a recorded reason.
2. The section 8.1 gates pass. The suite also passes from a foreign directory

   (8.5).
3. The wheel acceptance passes (8.2).
4. The behavior lock passes, and every regeneration is tied to a decision.
5. `tests/test_module_layers.py` passes without the transitional allowance.
6. The section 8.7 greps print nothing.
7. The demo and suite timings are recorded against section 0.
8. The documents describe the actual code (B4.1, B7.3).
9. `RULES.md` and the register match the tree.
10. The change record is final and frozen, and this plan is archived.
