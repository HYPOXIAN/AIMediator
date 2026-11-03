# Compatibility Layer Register

- Type: Reference
- Status: Active
- Updated: 2026-11-03
- Applies to: commit `0d390c4` and later; `RULES.md` v1.0 (G2, P3, P7)

This register lists every symlink and forwarding script that RULES.md G2
allows as a compatibility layer. A symlink or a script whose docstring begins
with "Compatibility entry point" that is not listed here is a G2 violation;
`scripts/maintenance/check_rules.py --rule G2` checks this. The first column
of each table holds the registered path; the check reads it.

Per the reorganization plan (decision Q4), the layers are registered only and
are not removed during the reorganization.

Inventory taken 2026-11-03 with `find . -type l` (excluding `.git/`) and a
search for the docstring "Compatibility entry point": 18 symlinks and 7
forwarding scripts. The plan expected 6 forwarding scripts; the seventh,
`scripts/run_local_direction_comparison.py`, is a wrapper with its own
arguments rather than a pure forwarder (see its row).

"Used by" lists tracked code and documents that name the path, found with
`git grep` at commit `0d390c4` and updated in batch 3 for the scripts that
were archived, moved into `scripts/collect/` or `scripts/experiments/`, or
renamed (change record, P3), and in batch 4 for the documents that moved into
the D1 directories (change record, P4). Scripts are listed by file name.
Documents are listed by path under `docs/`; `README.md` is the root README.

## Removal conditions

- **R1 (asset links)**: every code user reads the resource through
  `aimediator.resources.asset_path()` or has been archived, every document cites
  the `src/aimediator/assets/` path, and no tracked file names the link path
  any more.
- **R2 (pure forwarding scripts)**: every importer imports
  `aimediator.<module>` directly or has been archived, every documented
  command for the script has been replaced by a package entry point, and no
  code hashes the script's bytes into a run identity that must still be
  resumed or replayed.
- **R3 (wrapper script)**: the historical command it replaces is no longer
  documented, or the behavior has moved into the `aimediator` CLI.

## Symlinks to packaged configuration and data

| Path | Points to | Used by | Removal |
| ---- | --------- | ------- | ------- |
| `configs/balance-review-policy.json` | `../src/aimediator/assets/configs/balance-review-policy.json` | scripts: `replay_balance_admission.py`, `run_balance_regression_live.py`, `run_quality_screening_experiment.py`; docs: `records/20261022-balance-review-v2.md`, `design/evidence-quality.md` | R1 |
| `configs/evidence-quality-policy.json` | `../src/aimediator/assets/configs/evidence-quality-policy.json` | scripts: `run_quality_screening_experiment.py`; docs: `design/evidence-quality.md`, `records/20261026-evidence-quality-implementation.md` | R1 |
| `configs/local-language-routing.json` | `../src/aimediator/assets/configs/local-language-routing.json` | scripts: `diagnose_evidence_quality_live.py`, `run_quality_screening_experiment.py`, `run_quality_screening_recovery.py`; docs: `design/balance-analysis.md` | R1 |
| `data/glossary.json` | `../src/aimediator/assets/data/glossary.json` | scripts: `run_quality_screening_experiment.py`, `screen_feedback.py`; docs: `README.md`, `records/20261022-alias-review.md`, `reference/glossary.md`, `reference/glossary-vector-index.md` | R1 |
| `data/evaluation/evidence-quality-synthetic-v1/cases.json` | `../../../src/aimediator/assets/fixtures/cases.json` | scripts: `experiments/demo_evidence_quality.py`; tests: `test_evidence_quality.py`; `tests/test_evaluation_sets.py` checks it against `cases_sha256` in the set's `manifest.json`; docs: `records/20261026-evidence-quality-implementation.md` | R1 |

## Symlinks to packaged prompts

| Path | Points to | Used by | Removal |
| ---- | --------- | ------- | ------- |
| `prompts/evidence-quality.en.txt` | `../src/aimediator/assets/prompts/evidence-quality.en.txt` | scripts: `diagnose_evidence_quality_live.py`, `run_quality_screening_experiment.py`; docs: `design/evidence-quality.md`, `records/20261026-evidence-quality-implementation.md` | R1 |
| `prompts/evidence-quality.zh.txt` | `../src/aimediator/assets/prompts/evidence-quality.zh.txt` | same as `evidence-quality.en.txt` | R1 |
| `prompts/quality-extract.en.txt` | `../src/aimediator/assets/prompts/quality-extract.en.txt` | scripts: `diagnose_evidence_quality_live.py`; docs: `records/20261026-evidence-quality-implementation.md` | R1 |
| `prompts/quality-extract.zh.txt` | `../src/aimediator/assets/prompts/quality-extract.zh.txt` | same as `quality-extract.en.txt` | R1 |
| `prompts/quality-verify.en.txt` | `../src/aimediator/assets/prompts/quality-verify.en.txt` | scripts: `diagnose_evidence_quality_live.py`; docs: `records/20261026-evidence-quality-implementation.md` | R1 |
| `prompts/quality-verify.zh.txt` | `../src/aimediator/assets/prompts/quality-verify.zh.txt` | same as `quality-verify.en.txt` | R1 |
| `prompts/relevance.en.txt` | `../src/aimediator/assets/prompts/relevance.en.txt` | scripts: `replay_balance_admission.py`; docs: `design/balance-analysis.md`, `design/evidence-quality.md` | R1 |
| `prompts/relevance.zh.txt` | `../src/aimediator/assets/prompts/relevance.zh.txt` | same as `relevance.en.txt` | R1 |
| `prompts/retrieval-review.en.txt` | `../src/aimediator/assets/prompts/retrieval-review.en.txt` | scripts: `replay_balance_admission.py`; docs: `design/evidence-quality.md` | R1 |
| `prompts/retrieval-review.zh.txt` | `../src/aimediator/assets/prompts/retrieval-review.zh.txt` | same as `retrieval-review.en.txt` | R1 |
| `prompts/summarize-balance.en.txt` | `../src/aimediator/assets/prompts/summarize-balance.en.txt` | scripts: `diagnose_evidence_quality_live.py`, `run_balance_regression_live.py` (default `--prompt-dir`), `run_balance_numeric_extraction_live.py`, `run_balance_semantic_controls_live.py`; docs: `design/balance-analysis.md`, `design/evidence-quality.md`, `records/20261027-balanced-validation.md` | R1 |
| `prompts/summarize-balance.zh.txt` | `../src/aimediator/assets/prompts/summarize-balance.zh.txt` | same as `summarize-balance.en.txt` | R1 |
| `prompts/verify-balance.en.txt` | `../src/aimediator/assets/prompts/verify-balance.en.txt` | tests: `test_balance_analysis.py`; scripts: `diagnose_evidence_quality_live.py`, `run_balance_regression_live.py` (default `--prompt-dir`), `run_balance_controls_live.py`, `run_balance_numeric_extraction_live.py`, `run_balance_semantic_controls_live.py`; docs: `design/balance-analysis.md`, `records/20261027-balanced-validation.md` | R1 |
| `prompts/verify-balance.zh.txt` | `../src/aimediator/assets/prompts/verify-balance.zh.txt` | scripts: same as `verify-balance.en.txt` (tests excepted) | R1 |

## Forwarding scripts

Scripts that tests and other scripts import from `scripts/` by putting that
directory on `sys.path`. The pure forwarders replace their own module entry
in `sys.modules` with the package module, so importers get the package
implementation.

| Path | Points to | Used by | Removal |
| ---- | --------- | ------- | ------- |
| `scripts/balance_policy.py` | `aimediator.balance_policy` | tests: `test_balance_review_pipeline.py`; scripts: `evaluate_balance_review.py`, `export_balance_review_followups.py`, `replay_balance_admission.py`; file hashed into run identities by `diagnose_evidence_quality_live.py`, `run_balance_regression_live.py`, `run_quality_screening_experiment.py`, `run_balance_numeric_extraction_live.py`; docs: `design/cli.md`, `design/evidence-quality.md` | R2 |
| `scripts/evaluate_evidence_quality.py` | `aimediator.quality_scoring` (runs `main()` when executed) | tests: `test_evidence_quality_evaluation.py`; docs: `design/cli.md`, `guides/cli-usage.md`, `records/20261026-evidence-quality-implementation.md` | R2 |
| `scripts/evidence_quality.py` | `aimediator.evidence_quality` | tests: `test_evidence_quality.py`, `test_evidence_quality_evaluation.py`, `test_quality_screening_compact.py`, `test_quality_screening_experiment.py`; scripts: `demo_evidence_quality.py`, `diagnose_evidence_quality_live.py`, `present_quality_screening_results.py`, `run_quality_screening_experiment.py`, `run_quality_screening_recovery.py` (several also hash the file); docs: `design/cli.md`, `design/evidence-quality.md`, `records/20261026-evidence-quality-implementation.md` | R2 |
| `scripts/glossary_vectors.py` | `aimediator.glossary_vectors` (runs `main()` when executed) | docs: `README.md`, `design/cli.md`, `reference/glossary-vector-index.md` (documented commands) | R2 |
| `scripts/review_balance_sources.py` | `aimediator.legacy_review` (runs `main()` when executed) | tests: `test_balance_source_review.py`, `test_evidence_quality.py`; scripts: `check_balance_regressions.py`, `review_balance_live.py`; docs: `design/balance-analysis.md`, `design/cli.md`, `records/20261026-evidence-quality-implementation.md` | R2 |
| `scripts/run_balance_analysis.py` | `aimediator.engine` (runs `main()` when executed) | tests: `test_balance_analysis.py`, `test_balance_review_pipeline.py`, `test_balanced_collection.py`, `test_evidence_quality.py`, `test_evidence_quality_evaluation.py`, `test_quality_screening_compact.py`, `test_quality_screening_experiment.py`, `test_quality_screening_recovery.py`; scripts (17): `check_balance_regressions.py`, `demo_evidence_quality.py`, `diagnose_evidence_quality_live.py`, `evaluate_balance_review.py`, `export_balance_review_followups.py`, `prepare_balance_design.py`, `present_quality_screening_results.py`, `replay_balance_admission.py`, `resume_quality_screening_local.py`, `review_balance_live.py`, `run_balance_regression_live.py`, `run_local_direction_comparison.py`, `run_quality_screening_experiment.py`, `run_quality_screening_recovery.py`, `run_balance_controls_live.py`, `run_balance_numeric_extraction_live.py`, `run_balance_semantic_controls_live.py`; docs: `README.md`, `design/balance-analysis.md`, `design/cli.md`, `design/evidence-quality.md`, `records/20261026-evidence-quality-implementation.md`, `records/20261027-balanced-validation.md` | R2 |
| `scripts/run_local_direction_comparison.py` | `run_balance_analysis.run` (that is, `aimediator.engine.run`), with its own arguments; replaces the historical 32-comment experiment command | docs: `design/balance-analysis.md` | R3 |

## Change log

- 2026-11-03: register created with 18 symlinks and 7 forwarding scripts.
- 2026-11-03 (batch 3): "Used by" updated: archived one-off and smoke-test
  scripts dropped, the four `test_*` scripts renamed to `run_*_live`, and
  the `cli-demo/` entry (removed in batch 2) dropped. No layer changed.
- 2026-11-03 (batch 3): added the symlink
  `data/evaluation/evidence-quality-synthetic-v1/cases.json`, which replaced a
  byte-identical copy of the packaged fixture (plan section 7, decision 9).
  The register now lists 19 symlinks and 7 forwarding scripts.
- 2026-11-03 (batch 3 review, P3-D01): `scripts/run_local_direction_comparison.py`
  writes to `runs/<run name>` instead of `reports/<run name>`, and its
  `--run-name` default is `local-direction-comparison` instead of the dated
  `balance-evidence-20261022` (G7). The layer stays registered under R3.
