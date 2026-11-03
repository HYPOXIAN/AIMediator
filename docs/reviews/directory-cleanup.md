# Directory cleanup — 2026-10-28

Removed superseded generated content after checking current code references and
running the full automated suite. Historical documents describe the experiments
at the time they ran; paths listed below are intentionally no longer available.
Deleted experiment outputs are not recoverable from this checkout's empty Git
metadata. This record contains paths and counts, not a backup of deleted data.

## Result

- Deleted 5,848 files across 105 explicit targets.
- Removed 639,314,748 bytes (609.70 MiB of file contents).
- File contents decreased from 1063.62 MiB to approximately 453.92 MiB; filesystem allocation is about 495 MiB.
- Source code was unchanged except removal of the unused embedding experiment script.
- Updated README layout, historical handoff/status notes and ignore patterns for logs, temporary files and editor backups.

## Retained dependencies

- All active automated tests and frozen evaluation labels/regression fixtures.
- The 600-record latest balanced dataset: 300 English and 300 Chinese records,
  its original source evidence and the final v2 source-review configuration.
- October 15 initial/expanded collections: compatibility collection, screening,
  expansion, evaluation and report commands still use these files. Their age
  alone does not make them unused.
- Original glossary evidence and the published 849 × 4096 vector index.
  Only the reproducible batch-building cache was removed.
- `balance-engineering-20261022-final-review`, `balance-review-v2`,
  `balance-review-v22`, final evidence-quality delivery/verification, the quality
  experiment origin and recovered-v2 results, and screening audit.
- Both `latest-balanced-20261027/full-pipeline` and `full-pipeline-final`:
  the final run records exact request replay provenance against the original.
  Small diagnostic controls, failure records and source-review decisions remain.
- Final CLI verification JSON, `release-demo`, live diagnostic, wheel and source
  archives in `dist/`. The build tree and superseded development demo were removed.
- Final acceptance logs (`all-tests-final.log`, `unit-tests-final.log`,
  `tests.log`) remain as verification evidence. The report renderer reads
  `unit-tests-final.log`; 63 separately targeted obsolete logs were removed.
- Credential file and all compatibility resource links were preserved.

## Validation

- Before cleanup: 182 tests passed (40.076 s).
- After cleanup: 182 tests passed (39.659 s).
- CLI version and offline doctor: passed; dependencies, resources and configuration checked.
- 119 retained files/links and credential metadata matched the pre-cleanup snapshot.
- All 18 compatibility links resolve; published vector file hashes and dataset counts passed.
- No interpreter cache directories remained after verification.

## Deleted targets

Each entry lists the removed path, file count, and reason. Directory counts include
all contained files; nested targets are counted only once.

- `build` — 39 files; Reproducible packaging build tree; release archives remain in dist.
- `configs/feedback-latest-20261027-source-reviews.json` — 1 files; Superseded by source-reviews-v2.json; no active references.
- `reports/balance-engineering-20261022` — 173 files; Superseded by balance-engineering-20261022-final-review.
- `reports/balance-engineering-20261022-bilingual` — 765 files; Superseded by balance-engineering-20261022-final-review.
- `reports/balance-engineering-20261022-run` — 237 files; Superseded by balance-engineering-20261022-final-review.
- `reports/balance-engineering-20261022-tested` — 179 files; Superseded by balance-engineering-20261022-final-review.
- `reports/balance-engineering-20261022-verified` — 193 files; Superseded by balance-engineering-20261022-final-review.
- `reports/balance-engineering-debug-cache` — 373 files; Obsolete engineering debug cache.
- `reports/balance-evidence-20261022-engineering` — 163 files; Superseded by the reviewed engineering baseline and later balanced validation.
- `reports/balance-evidence-20261022-final` — 143 files; Superseded by the reviewed engineering baseline and later balanced validation.
- `reports/balance-evidence-20261022-full` — 157 files; Superseded by the reviewed engineering baseline and later balanced validation.
- `reports/balance-evidence-20261022-v1` — 12 files; Superseded by the reviewed engineering baseline and later balanced validation.
- `reports/balance-evidence-20261022-v2` — 49 files; Superseded by the reviewed engineering baseline and later balanced validation.
- `reports/balance-evidence-20261022-v3` — 52 files; Superseded by the reviewed engineering baseline and later balanced validation.
- `reports/balance-evidence-20261022-v4` — 79 files; Superseded by the reviewed engineering baseline and later balanced validation.
- `reports/balance-evidence-20261022-v5` — 136 files; Superseded by the reviewed engineering baseline and later balanced validation.
- `reports/balance-evidence-20261022-v6` — 137 files; Superseded by the reviewed engineering baseline and later balanced validation.
- `reports/balance-review-v21` — 668 files; Superseded by balance-review-v22.
- `reports/cli-design-baseline-20261028-t2qr8gbm` — 2 files; Temporary design baseline; final CLI verification retained.
- `reports/evidence-quality-v1-examples` — 661 files; Superseded by evidence-quality-v1-delivery/examples.
- `reports/evidence-quality-v1-live-final` — 38 files; Superseded by evidence-quality-v1-live-verified.
- `reports/evidence-quality-v1-live-fixed-admission` — 38 files; Superseded by evidence-quality-v1-live-verified.
- `reports/evidence-quality-v1-synthetic-demo` — 8 files; Superseded by evidence-quality-v1-delivery/mock-pipeline.
- `reports/latest-baseline-tests-20261027.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-collection-20261027-final-screening.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-collection-20261027-reviewed.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-collection-20261027.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/quality-screening-existing-100-recovered-v1` — 29 files; Superseded by recovered-v2.
- `reports/quality-screening-existing-100-recovered-v2-checkpoint-024` — 35 files; Checkpoint superseded by recovered-v2.
- `reports/quality-screening-existing-100-recovery-launch.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/quality-screening-existing-100-recovery-v2.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/quality-screening-existing-100-v1-checkpoint-20261026` — 33 files; Obsolete checkpoint copy; origin and recovered-v2 retained.
- `reports/quality-screening-existing-100-v1-checkpoint-serial-20261026` — 34 files; Obsolete checkpoint copy; origin and recovered-v2 retained.
- `reports/quality-screening-recovery-tests.log` — 1 files; Obsolete launch, progress, development or install log.
- `scripts/__pycache__` — 33 files; Generated interpreter or tool cache.
- `scripts/test_embedding_relevance.py` — 1 files; Unreferenced historical experiment; its required sample/labels directory no longer exists.
- `src/aimediator.egg-info` — 6 files; Generated packaging metadata.
- `tests/__pycache__` — 15 files; Generated interpreter or tool cache.
- `reports/balance-engineering-20261022-final-review/unit-tests.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/balance-review-v2/unit-tests.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/balance-review-v22/unit-tests.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/all-tests-dev.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/baseline-tests.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/build.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/clean-dependency-install.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/clean-install-py314.json` — 1 files; Superseded by the corresponding final clean-install verification.
- `reports/cli-implementation-20261028/clean-install-py39-min-numpy.json` — 1 files; Superseded by the corresponding final clean-install verification.
- `reports/cli-implementation-20261028/clean-install-py39.json` — 1 files; Superseded by the corresponding final clean-install verification.
- `reports/cli-implementation-20261028/demo` — 943 files; Superseded by release-demo.
- `reports/cli-implementation-20261028/final-wheel-install.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/min-numpy-install.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/min-numpy-wheel-install.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/p1-build.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/p1-clean-install.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/p1-outside-import.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/p1-tests.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/p1-wheel-install.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/product-tests-dev.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/python-tooling-install.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/python39-dependency-install.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/python39-install.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/cli-implementation-20261028/python39-wheel-install.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/baseline-matched-regressions.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/baseline-regressions.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/final-regressions.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/final-validation.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/finalize-rerun.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/followup-validation.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/full-pipeline-auto-cpu-interrupted` — 156 files; Abandoned CPU run superseded by completed runs.
- `reports/latest-balanced-20261027/full-pipeline-auto-cpu-interrupted.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/full-pipeline-final.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/full-pipeline-language-provisional` — 93 files; Superseded by corrected full-pipeline and full-pipeline-final.
- `reports/latest-balanced-20261027/full-pipeline-language-provisional.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/full-pipeline.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/generation-recovery-bounded-json.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/generation-recovery-sampled.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/generation-recovery.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/numeric-controls-final.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/numeric-controls.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/numeric-extraction-cpu-interrupted` — 12 files; Superseded by numeric-extraction-final.
- `reports/latest-balanced-20261027/numeric-extraction-cpu-interrupted.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/numeric-extraction-final.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/quality-compact-recovery-sampled.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/quality-compact-recovery.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/quality-live-enforce-v3.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/quality-live-enforce-v4.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/quality-live-enforce.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/revised-regressions.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/revised-v2-regressions.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/semantic-controls-schema-fixed.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/semantic-controls.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/latest-balanced-20261027/unit-tests.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/quality-screening-existing-100-recovered-v2/durability-sync.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/quality-screening-existing-100-v1/resume-20261026.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/quality-screening-existing-100-v1/resume-cpu-cache-recovered-20261026.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/quality-screening-existing-100-v1/resume-cpu-serial-20261026.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/quality-screening-existing-100-v1/resume-final-serial-20261026.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/quality-screening-existing-100-v1/resume-final.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/quality-screening-existing-100-v1/resume-gpu-serial-20261026.log` — 1 files; Obsolete launch, progress, development or install log.
- `reports/quality-screening-existing-100-v1/resume-serial-20261026.log` — 1 files; Obsolete launch, progress, development or install log.
- `src/aimediator/__pycache__` — 19 files; Generated interpreter or tool cache.
- `data/processed/glossary-vectors/batches` — 54 files; Rebuild cache; active published vector index is retained.
- `reports/cli-implementation-20261028/live-diagnostic/progress.log` — 1 files; Obsolete launch, progress, development or install log.
- `data/raw/feedback/20261027-latest-balanced/screened-provisional` — 8 files; Superseded by final screened dataset.
- `data/raw/feedback/20261027-latest-balanced/screened-reviewed-v1` — 8 files; Superseded by final screened dataset and v2 review decisions.
