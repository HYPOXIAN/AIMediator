# Reorganization Change Record

- Type: Record
- Status: Draft
- Updated: 2026-11-03
- Applies to: baseline commit `0d390c4` and later; `RULES.md` v1.0 and v1.1

The single change record for the whole reorganization
([plan](../plans/reorganization.md), section 0, item 4). Every phase appends
to it. Deletions of non-reproducible content are entered here (G6). The
record is frozen when the reorganization is finished (P5).

## P0 Baseline (2026-11-03)

- **Baseline commit**: `0d390c4` on `main`, "chore: baseline snapshot before
  reorganization", 175 tracked files. Large data stays ignored; `.env` is not
  tracked. Before this, `.git/` was an empty directory.
- **Pre-commit checks** run before the baseline commit: a credential pattern
  scan and a comparison of `.env` values against the files to be tracked.
  Neither produced a hit.
- **Backup**: `~/Archives/AIMediator/20261103-baseline/`, containing
  `workspace/` (the full workspace), `SHA256SUMS` (20,989 files), `SYMLINKS.txt`
  (18 symlinks, not in `SHA256SUMS`) and `README.txt`. Excluded: `.env`
  (credentials, G9), `.git`, `build/`, `__pycache__/`, `*.egg-info`
  (reproducible).
- **Backup verification**: compared one by one against the original files at
  creation, with a matching result. Re-verified on 2026-11-03 during batch 1
  with `sha256sum -c --quiet ../SHA256SUMS` run from `workspace/`: all 20,989
  files OK (exit status 0). `SHA256SUMS` has no `.env` entry.
- **Backup limitation**: btrfs reflink copy on the same disk as the project.
  It protects against accidental deletion or overwrite, not against disk
  failure. No off-site copy will be made (plan, section 7, decision 3).
- **Test baseline**: 192 offline tests pass
  (`python3 -m unittest discover -s tests -q`). Recorded in RULES.md P4.
- **Durable planning copies** used by batch 1 before the rules entered the
  project: `~/Archives/AIMediator/planning/` (`RULES.md`,
  `reorganization-plan.zh.md`, `rules-review.zh.md`).

## P1 Rules in place and the check tool (batch 1, 2026-11-03)

Entry check: working tree clean, `HEAD` at `0d390c4`, 192 tests passing.

Batch 1 only adds files; it moves, deletes and renames nothing.

### Changes

- `RULES.md` copied verbatim from the planning copy (byte-identical, checked
  with `cmp`).
- `docs/plans/reorganization.md`: English translation of the approved
  Chinese plan, with a D2 header added. It is the basis for batches 2 to 4.
- `CLAUDE.md`: references `RULES.md`, lists common commands and states that
  agents do not sign their work. No rules of its own (G1).
- `.env.example`: the four key names from `.env`, without values, produced
  from the key column only (G9).
- `.gitignore`: `runs/` added.
- `docs/reference/compatibility-layers.md`: compatibility register (G2).

### Compatibility layer inventory

Measured with `find . -type l` (excluding `.git/`) and a search for the
docstring "Compatibility entry point":

- 18 symlinks, all tracked, matching the plan and the backup's
  `SYMLINKS.txt`: 3 in `configs/`, 1 in `data/`, 14 in `prompts/`, all
  pointing into `src/aimediator/assets/`.
- **7 forwarding scripts, against 6 in the plan.** Six are pure forwarders
  (`balance_policy.py`, `evaluate_evidence_quality.py`, `evidence_quality.py`,
  `glossary_vectors.py`, `review_balance_sources.py`,
  `run_balance_analysis.py`). The seventh,
  `scripts/run_local_direction_comparison.py`, carries the same docstring but
  is a wrapper with its own arguments around `run_balance_analysis.run`. All
  seven are registered, so the register covers 25 layers, not 24.

All layers are registered only; none was removed (decision Q4).

### Rule check tool and hook

- `scripts/maintenance/check_rules.py`: read-only, standard library only,
  output grouped by rule ID, non-zero exit on violations, `--rule` to select
  rules. It never opens files under `reports/` or `.env` files and never
  prints matched credential text. Checks: G2, G3, G7, G8, G9, D1, D2, D4,
  D5, D6, D7, D8, P1, P2, P3, P4.
- `tests/test_check_rules.py`: 29 offline tests. Suite: 221 tests
  (192 + 29), all passing.
- `scripts/maintenance/hooks/pre-commit`: runs the tool, prints violations,
  always exits 0. Enabled with
  `git config core.hooksPath scripts/maintenance/hooks`. Verified on the
  commit that added it: 205 violations printed, commit not blocked.
  `core.hooksPath` is local git configuration, so each clone has to enable
  it (the command is in `CLAUDE.md`).

### Violation baseline

Full run after the batch 1 commits, saved (ignored) to
`runs/reorg-p1-violations.txt`. These counts are the progress table for
later phases.

| Rule | Count | Main sources | Phase |
| ---- | ----: | ------------ | ----- |
| G2 | 1 | duplicate file (see Deferred) | P3 |
| G3 | 6 | `.agents`, `.aws`, `.codex`, `cli-demo`, `notes`, `prompts` | P2, P4, see Deferred |
| G7 | 17 | 8 absolute user paths (5 documents, 2 `cli-demo` files); 9 defaults naming `reports/` or a dated run | P2, P3, P4 |
| G8 | 32 | `latest`/`final` in names, dates not used as prefix, `-vN` not at the end | P2, P3, P4 |
| G9 | 1 | `dist/aimediator-refactored-workspace.zip` lists 66 `data/raw` entries (0 `.env`) | P2 |
| D1 | 2 | `docs/module-reports/`, `docs/reviews/` | P4 |
| D2 | 20 | existing documents without the header | P4 |
| D4 | 24 | no `docs/README.md`; 23 unindexed documents | P4 |
| D5 | 17 | 13 broken document links (as in the plan); 4 missing `MANIFEST.in` paths | P4 |
| D6 | 0 | — | — |
| D7 | 3 | `low-alias-review.json`; two alias reviews over 100 KB | P4 |
| D8 | 10 | Chinese outside corpus content | P4 |
| P1 | 9 | 4 raw datasets without manifest; loose glossary files; `-v1-pending` set name; loose annotation file; 2 runtime state files | P2, P3 |
| P2 | 24 | 10 report directories without manifest; 12 with code or archive files outside `provenance/`; 2 extra `dist/` entries | P2 |
| P3 | 39 | 35 scripts outside the three subdirectories (4 of them `test_*`, which also count for the prefix) | P3 |
| P4 | 0 | static count 221 ≥ baseline 192 | — |
| **Total** | **205** | | |

### Deferred

Issues found in batch 1 that belong to later batches or need an owner
decision. Nothing here was changed.

1. **G3 and P7 conflict.** P7 keeps a root `prompts/` for compatibility
   links, but G3 does not list `prompts/`, so the G3 check reports it. Needs
   an amendment to G3 or relocating the 14 prompt links (batch 3).
2. **Seven forwarding scripts, not six.** The plan's P3 says "the 6
   forwarding shells stay". `scripts/run_local_direction_comparison.py` is
   the seventh; it also has a G7 default (`balance-evidence-20261022` run
   name, output under `reports/`). Batch 3 decides whether it stays as a
   registered layer or is archived as a one-off script.
3. **Duplicate file (G2), not in the plan.**
   `data/evaluation/evidence-quality-synthetic-v1/cases.json` is identical
   to `src/aimediator/assets/fixtures/cases.json`. Batch 3 picks the single
   source.
4. **`MANIFEST.in` points to missing files.** Its four `include docs/cli-*.md`
   lines name paths that do not exist (the files are in `docs/reviews/`), so
   the current sdist cannot contain them. Beyond the 13 broken links the
   plan counted; batch 4.
5. **Naming beyond the plan's list.** G8 also reports dates used as a suffix
   (`cli-implementation-20261028`, `screening-audit-20261027`,
   `cli-walkthrough-16-20261029`, seven `data/raw/glossary/*-20261008.json`
   files) and `-v1-` in the middle of names (`evidence-quality-v1-delivery`
   and two siblings). The batch 2 and batch 3 migration lists should include
   them.
6. **Loose raw glossary files (P1).** `data/raw/glossary/` holds seven files
   directly instead of a `YYYYMMDD-slug` dataset directory with a manifest.
   The plan's P3 covers manifests but not this restructuring.
7. **Chinese aliases in prose (D8).** `balance-analysis.md`,
   `balance-review-v2.md` and `review-todo.md` each have one or two lines
   with a Chinese alias in running text. Per the P4 allowlist they need to
   become code spans or quotations (batch 4).
8. **Scope of the D2 check.** The tool applies D2 to `docs/` only. The root
   `README.md` and `RULES.md` have no D2 header; `RULES.md` was copied
   verbatim as instructed. Owner to decide whether D2 covers root files.
9. **D7 justification.** RULES.md allows a justified Markdown file over
   100 KB but defines no form for the justification; the tool reports every
   such file.
10. **Report code count.** The tool counts 59 code or archive files outside
    `provenance/` in `reports/`; the plan says 58. The batch 2 migration list
    enumerates them exactly.
11. **Checks that are not automated**: G1, G4, G6, D3, D9, P6, P7 and the
    live-service test separation in P4 are verified manually (P5). The P4
    test count is static (test methods counted with `ast`), which matched
    the 192 measured at baseline. `data/processed/` "generating command
    recorded" is not checked.

### Owner decisions on deferred items (2026-11-03)

The owner reviewed proposals for deferred items 1, 3, 4, 5 (with 6) and 8
and adopted the recommended option for each. They are written into the plan
as section 7, decisions 8 to 12, and into the affected phase sections.

| Deferred item | Decision | Plan | Batch |
| ------------- | -------- | ---- | ----- |
| 1. G3 and P7 conflict | Amend G3: allow `prompts/` for registered compatibility links only; remove it once empty | decision 8 | 2 (first commit, RULES.md v1.1) |
| 3. Duplicate `cases.json` | Packaged fixture is the single file; evaluation set path becomes a registered symlink; new hash test against the set manifest | decision 9 | 3 |
| 4. `MANIFEST.in` | Fix with the document moves; ship `docs/guides/cli-usage.md` and `docs/design/cli.md` only | decision 10 | 4 |
| 5 and 6. Naming and loose raw glossary files | Renames listed in plan P2 and P3; raw glossary files go into `20261008-glossary-sources/` without date suffixes; `20261028-cli-unfiltered` keeps its name; `glossary.json` changed in batch 3 and again in batch 4 | decision 11 | 2, 3, 4 |
| 8. Scope of the D2 check | D2 covers documents under `docs/`; root `README.md`, `RULES.md`, agent entry files and README files in `data/` are exempt | decision 12 | 2 (with decision 8) |

Correction to the batch 1 report: the sdist currently in `dist/` was built
before the CLI documents moved into `docs/reviews/` and does contain them; a
fresh build would omit them, because `MANIFEST.in` names the old paths.

Still open: deferred item 2 (the seventh forwarding script) is decided in
the batch 3 migration list; items 7, 9, 10 and 11 stand as recorded.

## P2 Moving generated output out (batch 2, 2026-11-03)

Entry check: tag `reorg-p1` present, working tree clean at `eec9f41`,
221 tests passing, rule check 205 violations (equal to the batch 1
baseline). No collection or analysis process was running. The migration
list was approved by the owner before execution (owner decisions: the
RULES.md v1.1 commit first; `summary.zh.md` archive only; summaries in
`summary/`; defaults accepted).

### RULES.md v1.1

First commit of the batch, as planned (plan section 2; decisions 8 and 12):
G3 allows `prompts/` for registered compatibility links only; D2 covers
documents under `docs/` with the listed exemptions. `check_rules.py`
`G3_ALLOWED` and its test updated.

### Archive procedure

Every deletion below followed the same order (G6): copy with
`cp -a --reflink=auto` into `~/Archives/AIMediator/<area>/`; inside the
archive copy only, move code and archive files to `provenance/<original
relative path>` (reports only); write `SHA256SUMS` in the archive directory;
verify with `sha256sum -c --quiet`, then compare every entry with its source
file (the `provenance/` prefix stripped) and check that entry and source
file counts are equal; only then delete the source. No source contained a
`.env` file (checked by name before copying).

### Reports moved out

Archive: `~/Archives/AIMediator/reports/<original name>/`, each with its
own `SHA256SUMS`. All 15 verified; the source files were additionally
compared with the baseline backup's `SHA256SUMS` (20,749 report entries):
no difference. Reason: P2 (full run contents live in the external archive;
the project keeps a manifest and a curated summary), G8 for the new names.

| Original name | Project name | Files | Bytes | Provenance | Kept in `summary/` |
| ------------- | ------------ | ----: | ----: | ---------: | ------------------ |
| `balance-engineering-20261022-final-review` | `20261022-balance-engineering-review` | 996 | 34,766,612 | 1 | `evaluation.md`, `summary.json` |
| `balance-review-v2` | `balance-review-v2` | 1290 | 61,138,316 | 3 | `review-summary.md` |
| `balance-review-v22` | `balance-review-v22` | 732 | 1,817,270 | 0 | `review-summary.md` |
| `cli-demo-backups` | — (archive only) | 4082 | 167,403,834 | 6 | — |
| `cli-demo-monitoring` | — (archive only) | 2 | 49,325 | 0 | — |
| `cli-implementation-20261028` | `20261028-cli-implementation` | 1084 | 23,542,532 | 1 | `verification.json` |
| `cli-real-unfiltered-20261028` | — (archive only) | 1558 | 47,226,194 | 5 | — |
| `cli-walkthrough-16-20261029` | — (archive only) | 1293 | 27,236,177 | 2 | — |
| `evidence-quality-v1-delivery` | `evidence-quality-delivery-v1` | 661 | 5,666,121 | 9 | `examples-manifest.json` |
| `evidence-quality-v1-live-verified` | `evidence-quality-live-verified-v1` | 38 | 230,260 | 4 | `diagnostic-summary.json` |
| `evidence-quality-v1-verification` | `evidence-quality-verification-v1` | 4 | 7,082 | 0 | `verification.json` |
| `latest-balanced-20261027` | `20261027-balanced-validation` | 8101 | 246,135,113 | 19 | `evaluation.md`, `integrity-checks.json` |
| `quality-screening-existing-100-recovered-v2` | `quality-screening-existing-100-recovered-v2` | 142 | 1,885,355 | 1 | `recovery.md` |
| `quality-screening-existing-100-v1` | `quality-screening-existing-100-v1` | 88 | 4,127,244 | 6 | `recovery.md` |
| `screening-audit-20261027` | `20261027-screening-audit` | 678 | 10,202,389 | 4 | `summary.json`, `verification.json`, `report.zh.md` |
| **Total** | 11 kept | **20749** | **631,433,824** | **61** | |

- Each kept directory has a new `manifest.json`: original name, archive
  path, file and byte counts, provenance list, record document, dataset,
  code version (run identity hashes; no git commit, since every run predates
  the baseline) and reason for retention. Where the report already had a
  run manifest at its root, that original is in the archive and is named by
  `run_manifest`.
- Summaries are byte copies of archive files; upper-case names became
  lower case (`RECOVERY.md` → `recovery.md`, `REPORT.zh.md` →
  `report.zh.md`), `examples/manifest.json` became `examples-manifest.json`.
  Before tracking, all 26 files were scanned: no `/home/` path, no URL, no
  credential pattern.
- `latest-balanced-20261027/summary.zh.md` (cited by
  `docs/reviews/cli-design-handoff.md`) is in the archive only: it contains
  absolute user paths (G7).
- 61 provenance files: the 59 code or archive files the check tool counts
  (the plan said 58) plus two extension-less bash scripts named `cli` in
  `cli-demo-backups/`.
- The four archive-only directories (`cli-demo-backups`,
  `cli-demo-monitoring`, `cli-real-unfiltered-20261028`,
  `cli-walkthrough-16-20261029`) had no references except
  `cli-demo/dataset-provenance.json`, which is removed in this batch.
  Interrupted runs and backups (`balance-review-v2/relevance-interrupted-singles/`,
  `cli-demo-backups/run-interrupted-20261029-163607-579246/`) are in the
  archive only.

### `dist/` and reproducible products

| Path | Files | Bytes | Action | Archive |
| ---- | ----: | ----: | ------ | ------- |
| `dist/aimediator-refactored-workspace.zip` | 1 | 112,139,600 | deleted (P2: no workspace packages; G9: listed 66 `data/raw` entries, 0 `.env`) | `~/Archives/AIMediator/dist/` |
| `dist/refactored/` (`aimediator-0.1.0-py3-none-any.whl`) | 1 | 225,411 | deleted (duplicate wheel, P2) | same |
| `build/` | — | about 3.1 MB | deleted (reproducible, G4) | none |
| `src/aimediator.egg-info/` | — | small | deleted (reproducible, G4) | none |
| `__pycache__/` in `scripts/`, `scripts/maintenance/`, `src/aimediator/`, `tests/` | — | small | deleted (reproducible, G4) | none |

The archived `SHA256SUMS` (2 entries) was verified against the source and
matches the baseline backup. `dist/` keeps only the current wheel and sdist
(`aimediator-0.1.0-py3-none-any.whl`, `aimediator-0.1.0.tar.gz`; version
0.1.0 per `pyproject.toml`). The sdist predates the move of the CLI
documents (see the batch 1 correction above); it is rebuilt in batch 4.

### `cli-demo/` removed

- `cli-demo/`: 11 tracked files, 162,855 bytes, plus the empty ignored
  directory `sessions/20261029-170114-424313/`. Archived to
  `~/Archives/AIMediator/cli-demo/` with `SHA256SUMS`, verified against the
  source and the baseline backup (11 entries, no difference), then removed
  with `git rm -r` (content also in git history). Reason: decision Q5 in
  the RULES.md v1.0 revision log (removed, to be rebuilt later); it also
  carried absolute user paths (G7) and non-snake_case modules (G8).
- `tests/test_cli_presentation.py`: the test that ran
  `cli-demo/prepare-labels.py` now builds the unlabeled label file with the
  package's `aimediator.quality_scoring.prepare_dataset` and still asserts
  that preparation prints nothing. Renamed from
  `test_evaluation_preserves_unlabeled_status_and_helpers_are_silent` to
  `test_evaluation_preserves_unlabeled_status_and_preparation_is_silent`;
  the unused `subprocess` import and `ROOT` constant were removed. Suite:
  221 tests, unchanged (plan, section 7, decision 1).

### Empty tool directories and runtime state files

- `.agents/`, `.codex/`, `.aws/`: empty and untracked (checked with
  `ls -la`); removed with `rmdir` (P6). Nothing to archive.
- `data/raw/feedback-collector.lock` (0 bytes) and
  `data/raw/feedback-http-state.json` (346 bytes): archived to
  `~/Archives/AIMediator/runtime-state/` with `SHA256SUMS`, verified against
  the source (both also match the baseline backup), then deleted (P1: no
  runtime state under `data/`). No process held them. The values in the
  state file were not printed. `scripts/collect_feedback.py`,
  `scripts/collect_balanced_feedback.py` and `scripts/expand_feedback.py`
  still write them under `data/raw/` and recreate them on the next run;
  their paths move in batch 3.

### Results

Tracked state after the batch 2 commits (`c5704c2`..`205e910`).

- **Size** of the project without `data/` (`du` per top-level entry,
  including `.git`): 784.5 MB before, 13.6 MB after (`reports/` 661 MB →
  140 KB, `dist/` 108 MB → 484 KB, `build/` 3.1 MB → 0, `cli-demo/` gone).
  Target < 20 MB: met.
- **Archives**: 18 archive directories, each `SHA256SUMS` re-verified with
  `sha256sum -c` at the end of the batch: `reports/` (15 directories,
  20,749 entries), `dist/` (2), `cli-demo/` (11), `runtime-state/` (2). No
  `.env` file in any of them.
- **`reports/`**: 11 directories, each with `manifest.json` and `summary/`
  only; no code, archive, backup, checkpoint or interrupted-run entries.
- **G4**: a `git clone` of `205e910` (only tracked files, so no ignored
  directory exists) passes all 221 tests.
- **Tests**: 221 after every commit of the batch.

Violation counts (full run saved, ignored, to `runs/reorg-p2-violations.txt`):

| Rule | Batch 1 | Batch 2 | Change | Cause |
| ---- | ------: | ------: | -----: | ----- |
| G2 | 1 | 1 | 0 | batch 3 |
| G3 | 6 | 1 | −5 | `.agents`, `.aws`, `.codex`, `cli-demo` removed; `prompts` allowed by v1.1; `notes` left (batch 4) |
| G7 | 17 | 14 | −3 | `cli-demo/README.md`, `cli-demo/run-location.json` (2 lines) |
| G8 | 32 | 21 | −11 | 9 report names; 2 `cli-demo` modules |
| G9 | 1 | 0 | −1 | workspace zip |
| D1 | 2 | 2 | 0 | batch 4 |
| D2 | 20 | 20 | 0 | batch 4 |
| D4 | 24 | 24 | 0 | batch 4 |
| D5 | 17 | 17 | 0 | batch 4 |
| D6 | 0 | 0 | 0 | — |
| D7 | 3 | 3 | 0 | batch 4 |
| D8 | 10 | 10 | 0 | batch 4 |
| P1 | 9 | 7 | −2 | runtime state files |
| P2 | 24 | 0 | −24 | manifests, archive, `dist/` trimmed |
| P3 | 39 | 39 | 0 | batch 3 |
| P4 | 0 | 0 | 0 | — |
| **Total** | **205** | **159** | **−46** | |

The migration list estimated 160 (161 without the v1.1 commit); it counted
two G7 entries for `cli-demo`, but there were three.

Rules this phase is responsible for (plan section 1: G4, G6, G9, P2, and Q5
for `cli-demo`): G9 and P2 are 0; G3 no longer lists `cli-demo` or the
empty directories. G4 and G6 are verified manually as described above.

### Deferred

Nothing here was changed in batch 2.

1. **Document references to moved-out reports** (batch 4). Documents name
   `reports/<old name>/...` paths that are no longer in the project (all in
   code spans or plain text, so D5 does not count them):
   `README.md` (lines 172, 184, 224), `docs/reviews/balance-analysis.md`,
   `balance-review-v2.md`, `cli-design-handoff.md` (including
   `summary.zh.md`, now archive only), `cli-implementation-status.md`,
   `directory-cleanup.md`, `evidence-quality-implementation.md`,
   `latest-balanced-validation.md`, `next-development-plan.md`. Batch 4
   repoints them to `reports/<new name>/manifest.json`. The manifests'
   `record` fields name today's document paths and change with the moves.
2. **Scripts referencing moved-out reports** (batch 3), which now fail with
   their defaults: `build_screening_audit.py`, `check_balance_regressions.py`,
   `evaluate_balance_review.py`, `finish_latest_validation.py`,
   `run_quality_screening_experiment.py`, `run_quality_screening_recovery.py`,
   `complete_latest_validation.py`, `finalize_latest_rerun.py`,
   `render_latest_validation_report.py`, `replay_latest_accepted_contract.py`.
   Scripts whose default output is under `reports/` (`run_smoke_test.py`,
   `render_test_results.py`, `test_grounded_feedback.py`,
   `run_local_direction_comparison.py`, `engine.py` `--out`) also move to
   `runs/` in batch 3; until then their output is ignored unless it is a
   top-level `manifest.json` or lies in `summary/`.
3. **Reports without a result record** (batch 4): `20261027-screening-audit`
   has `record: null`; the two `quality-screening-existing-100-*` reports
   are named only in the retention list of `directory-cleanup.md`. P2
   expects a record document for each; their manifests say so in
   `record_note`.
4. **Runtime state paths** (batch 3): the three collection scripts listed
   above recreate the lock and HTTP state files under `data/raw/`.
5. **The check tool does not open files under `reports/`** (by design from
   batch 1), so its G7 and G9 scans do not cover the 26 tracked report
   files. They were checked by hand in this batch. Whether the tool should
   read `reports/*/manifest.json` and `summary/` is decided in batch 3 or 4.
6. **`dist/` contents are stale**: the kept wheel and sdist were built on
   2026-10-28, before the CLI documents moved into `docs/reviews/`. They
   are rebuilt and checked in P5 (batch 4).

## P3 Code, scripts and resources in place (batch 3, 2026-11-03)

Entry check: tag `reorg-p2` present, `HEAD` at `f1609fc` (= `reorg-p2`),
working tree clean, 221 tests passing, rule check 160 violations (159 at the
end of batch 2, plus the G3 entry `.claude`, see P3-D08). No collection or
analysis process was running.

Batch 3 runs under post-implementation review (plan section 7, decision 13,
commit `e3ae36a`). The working migration list is in the ignored
`runs/reorg-p3-migration.md`.

### Decisions pending owner review

Registered before any code or data change. "Implemented" means done as
recommended and undone by reverting the listed commit (and, where stated,
restoring from the archive); "bypassed" means the current state is kept and
the rest of the batch proceeds from it.

#### P3-D01 The seventh forwarding script

- **Question**: `scripts/run_local_direction_comparison.py` (batch 1
  deferred item 2) is a registered wrapper (R3) with a G7 problem: default
  run name `balance-evidence-20261022` and output hard-coded to
  `ROOT/'reports'/<run name>`. Options: (a) keep it unchanged as a
  registered layer; (b) keep it registered but change the output to
  `runs/<run name>` and drop the dated default; (c) archive it as a
  one-off script.
- **Recommendation**: (b). The command is still documented in
  `docs/reviews/balance-analysis.md`, so R3 is not met and archiving would
  break a documented command; the output path is the only problem.
- **Handling**: `bypassed`. Both (b) and (c) alter a registered
  compatibility layer, which this batch must not do (Q4).
- **Effect on the batch**: the script stays at its path unchanged; its G7
  violation remains and is listed as an exception at the end of the batch.
- **Rollback**: none needed (nothing changed).
- **Status**: pending
- **Commits**: none

#### P3-D02 One-off scripts archived with their runs

- **Question**: which scripts count as one-off scripts bound to a single run
  (P3; plan P3 names `finish_`, `finalize_`, `complete_`,
  `recover_latest_*`, `replay_latest_*`, `rerun_latest_*` "and so on").
  Proposed set: `complete_latest_validation.py`, `finalize_latest_rerun.py`,
  `finish_latest_validation.py`, `recover_latest_failures.py`,
  `recover_latest_quality.py`, `render_latest_validation_report.py`,
  `replay_latest_accepted_contract.py`, `rerun_latest_exact_requests.py`,
  `validate_latest_run.py` (all bound to `latest-balanced-20261027`) and
  `build_screening_audit.py` (bound to `screening-audit-20261027`).
  Options: (a) archive the set; (b) keep some (for example
  `validate_latest_run.py`, `recover_latest_failures.py`) under new names in
  `experiments/`.
- **Recommendation**: (a). Each one names its run in a default or
  hard-coded path, asserts that run's exact sizes (600 records, 321 rows),
  or is byte-identical to a snapshot in that run's `provenance/`; both runs
  are archived (batch 2). No test imports any of them.
- **Handling**: `implemented`. Copies go to `~/Archives/AIMediator/scripts/`
  with `SHA256SUMS` before `git rm`.
- **Effect on the batch**: removes 10 P3, 9 G8 and 5 G7 violations, and the
  only code users of `data/raw/feedback/20261027-latest-balanced`, so the
  dataset rename touches no code. Documents that name these scripts keep
  the bare names (batch 4).
- **Rollback**: `git revert` of the commit restores the files at their
  original paths; the archive copy is a second source.
- **Status**: pending
- **Commits**: `ecb6c85`

#### P3-D03 Smoke-test scripts with missing inputs

- **Question**: `run_smoke_test.py` writes to `reports/smoke-<stamp>` and,
  for a fresh run, reads `data/raw/debug/smoke-cases.json` and
  `patch-context.json`, which exist neither in the project nor in the
  baseline backup; `render_test_results.py` only reads `reports/smoke-*`,
  which also does not exist. Options: (a) archive both; (b) move both to
  `experiments/` with output under `runs/`.
- **Recommendation**: (a). Neither can run on any existing input, and the
  smoke runs they served are gone; keeping them would carry dead code
  under a new path.
- **Handling**: `implemented` (archive copy first, as in P3-D02).
- **Effect on the batch**: removes 2 P3 violations. `prompts/extract-feedback.txt`
  loses its only code user; the README still names it (P3-D04).
- **Rollback**: `git revert` of the commit.
- **Status**: pending
- **Commits**: `043a622`

#### P3-D04 Legacy prompts in `prompts/`

- **Question**: P7 archives legacy prompts "once confirmed unreferenced",
  and G3 v1.1 allows `prompts/` only for registered links. Both legacy
  prompts are still referenced: `extract-feedback.txt` by `README.md`
  (manual procedure, step 4) and, until P3-D03, `run_smoke_test.py`;
  `extract-grounded-feedback.txt` by the kept
  `test_grounded_feedback.py` (to become `run_grounded_feedback_live.py`),
  which `tests/test_grounded_validation.py` imports. Options for
  `extract-grounded-feedback.txt`: (a) move it to
  `src/aimediator/assets/prompts/` (single source per P7, but ships a
  prompt the package does not use); (b) amend G3 to allow it; (c) archive
  it together with the live script and drop or rewrite the validation
  test.
- **Recommendation**: archive `extract-feedback.txt` in batch 4 once the
  README rewrite drops step 4; for `extract-grounded-feedback.txt`, (a).
- **Handling**: `bypassed`. Neither prompt is unreferenced, and the options
  for the second one amend a rule, change the package contents, or remove
  a tested script, with quite different consequences.
- **Effect on the batch**: both files stay in `prompts/`; the moved
  `run_grounded_feedback_live.py` keeps reading `prompts/extract-grounded-feedback.txt`
  (its `ROOT` is fixed for the new depth).
- **Rollback**: none needed.
- **Status**: pending
- **Commits**: none

#### P3-D05 Track dataset manifests under ignored `data/`

- **Question**: `data/raw/*` and `data/processed/*` are ignored, so the new
  dataset manifests (P1) would exist only on this machine. Options: (a)
  track `manifest.json` files only, through `.gitignore` exceptions;
  (b) leave them ignored, backed up with the data.
- **Recommendation**: (a). Manifests are small, hold no record text or
  URLs (G9), and record provenance that should survive a lost data
  directory; a clean clone then shows which datasets the code expects.
- **Handling**: `implemented`.
- **Effect on the batch**: none on other steps. The manifests (routine P1
  work) were first written into the ignored directories, which needs no
  commit; the decision commit adds the `.gitignore` exceptions and the six
  files.
- **Rollback**: `git revert` of the commit untracks the manifests and
  removes them from the working tree; restore the files with
  `git show <commit>:<path>` (or regenerate them) if they should stay as
  ignored local files.
- **Status**: pending
- **Commits**: `c6ebca1`

#### P3-D06 Loose annotation file `pending-character-candidates.json`

- **Question**: `data/evaluation/pending-character-candidates.json` (one
  agent-reviewed alias candidate, unreferenced, not in the plan) is a P1
  violation: an annotation file outside a versioned set, with a status word
  in its name. Options: (a) move it into a versioned set
  `data/evaluation/character-alias-candidates-v1/candidates.json` with a
  manifest that records `pending` as a status; (b) archive and remove it.
- **Recommendation**: (a). It keeps the content in the project, unchanged,
  and matches how decision 11 treats `evidence-quality-real-v1-pending`.
- **Handling**: `implemented` (`git mv` plus a new manifest).
- **Effect on the batch**: removes 1 P1 violation.
- **Rollback**: `git revert` of the commit.
- **Status**: pending
- **Commits**: `9ee0e72`

#### P3-D07 Check tool coverage of `reports/`

- **Question**: batch 2 deferred item 5: the tool never opens files under
  `reports/`, so its G7 and G9 scans miss the 26 tracked manifest and
  summary files. Options: (a) let the tool read `reports/*/manifest.json`
  and `summary/`; (b) keep the current design and check by hand.
- **Recommendation**: (a), in batch 4, before the hook becomes blocking.
- **Handling**: `bypassed`. It changes what the tool reports (output
  meaning) and is not needed for P3.
- **Effect on the batch**: none; the tracked report files are again checked
  by hand at the end of the batch.
- **Rollback**: none needed.
- **Status**: pending
- **Commits**: none

#### P3-D08 Top-level `.claude/`

- **Question**: since batch 2 a `.claude/` directory has appeared at the
  root (ignored, one `scheduled_tasks.lock` written by the Claude Code
  harness at session start). G3 reports it. Options: (a) remove it after
  agent sessions end; (b) amend G3 to allow ignored agent tool state
  directories; (c) leave it.
- **Recommendation**: (a) for now; (b) only if it keeps returning.
- **Handling**: `bypassed`. It is live state of the running harness, not
  project content, and (b) amends `RULES.md`.
- **Effect on the batch**: G3 stays at 2 (`notes` is batch 4).
- **Rollback**: none needed.
- **Status**: pending
- **Commits**: none

#### P3-D09 One project-root constant (G7)

- **Question**: G7 asks code to resolve resources "through one project-root
  constant". Today there are two notions: the package uses
  `ROOT = Path.cwd()` (`engine.py`, `glossary_vectors.py`), while scripts
  use `Path(__file__)`-based roots. Moving scripts keeps the second notion
  (`parents[1]` becomes `parents[2]`). Options: (a) keep both; (b) make
  scripts use the package constant (changes behavior when run from another
  directory); (c) add a shared root helper.
- **Recommendation**: (a) in this batch; decide (b) or (c) together with
  the CLI work, since `cwd` is part of the CLI contract.
- **Handling**: `bypassed`. Options (b) and (c) change how paths resolve.
- **Effect on the batch**: moved scripts get `parents[2]`; no other change.
- **Rollback**: none needed.
- **Status**: pending
- **Commits**: none

#### P3-D10 Collection defaults that write into existing raw datasets

Found during execution (after the code changes above), registered before
any change to these scripts.

- **Question**: two collection scripts default to writing inside an
  existing dated raw dataset, which G7 ("default output paths never point
  at a specific historical run") and P1 (raw data is never overwritten)
  forbid. The check tool does not report them, because it exempts paths
  under `data/`. `scripts/collect/expand_feedback.py`: `--output` default
  `data/raw/feedback/20261015-expanded` (resumes into that dataset).
  `scripts/collect/screen_feedback.py`: `--input` default
  `data/raw/feedback/20261015-initial`, and the output defaults to
  `<input>/screened`, so a bare run rewrites that dataset's `screened/`.
  Options: (a) make `--output` (expand) and `--input` (screen) required;
  (b) default to a new timestamped directory, as `collect_feedback.py`
  does; (c) keep them.
- **Recommendation**: (a). It matches how this batch treated inputs from
  moved-out reports, and a bare run can no longer write into a frozen
  dataset. (b) would turn a resume into a fresh network collection.
- **Handling**: `bypassed`. (a) changes command-line behavior beyond a
  default path, and (a) and (b) differ in effect (error versus new
  collection).
- **Effect on the batch**: none; both scripts keep their defaults. Listed
  as a manual G7 exception at the end of the batch.
- **Rollback**: none needed.
- **Status**: pending
- **Commits**: none

### Decision summary

| ID | Question | Recommendation | Handling | Commit |
| -- | -------- | -------------- | -------- | ------ |
| P3-D01 | Seventh forwarding script | keep registered, output to `runs/`, no dated default | bypassed | — |
| P3-D02 | One-off scripts | archive 10 scripts with their runs | implemented | `ecb6c85` |
| P3-D03 | Smoke-test scripts without inputs | archive both | implemented | `043a622` |
| P3-D04 | Legacy prompts | batch 4 archives `extract-feedback.txt`; move `extract-grounded-feedback.txt` to package assets | bypassed | — |
| P3-D05 | Track dataset manifests | track `manifest.json` only | implemented | `c6ebca1` |
| P3-D06 | Loose alias candidate file | versioned set `character-alias-candidates-v1` | implemented | `9ee0e72` |
| P3-D07 | Check tool and `reports/` | read manifests and summaries, in batch 4 | bypassed | — |
| P3-D08 | Top-level `.claude/` | remove after agent sessions | bypassed | — |
| P3-D09 | One project-root constant | keep both notions for now | bypassed | — |
| P3-D10 | Collection defaults writing into raw datasets | make `--output` / `--input` required | bypassed | — |

### Changes

Routine work (rules and plan), one kind of operation per commit; tests
(221, then 222) passed after every commit, and `git grep` found no old
name in code, configuration or tests after each rename.

- `e3ae36a` plan decision 13 (post-implementation review).
- `1a52a5c` decisions registered (P3-D01 to P3-D09); `fdaa023` P3-D10,
  found during execution.
- `76a5bda` scripts grouped (P3). 23 scripts moved with `git mv`. Moved
  scripts that define `ROOT` from `__file__` use `parents[2]`;
  experiment scripts that import a forwarding script insert the
  `scripts/` root into `sys.path` (position 1), so they keep importing the
  registered shells; the identity file lists in
  `diagnose_evidence_quality_live.py` and
  `run_quality_screening_experiment.py` name the new paths; tests put
  `scripts/collect` and `scripts/experiments` on `sys.path`. Every moved
  script was started with `--help` from outside the checkout: all import.
- `4b45de5` the four `test_*` scripts renamed (P3, P4).
- `0624193` output defaults to `runs/` (G7, P2).
- `b6a2431` inputs from moved-out reports made explicit (G7).
- `3bcbbc0` collector lock and HTTP state in `runs/state/` (P1).
- `533d152` configuration renames (G8, P7).
- `60ec836`, `c57d49b`, `6726a0b` data renames (G8, P1, decision 11).
- `a774bbb` duplicate `cases.json` replaced by a registered symlink, new
  test `tests/test_evaluation_sets.py` (G2, decision 9). Suite: 222.
- `3e84c67` compatibility register "Used by" column updated (no layer
  changed).
- P1 manifests: written for the four raw feedback datasets,
  `data/raw/glossary/20261008-glossary-sources/` and
  `data/processed/glossary-vectors/` (source, record counts by platform
  and language, per-file SHA256, producing script, consumers; no record
  text, URL or credential). Tracked under P3-D05.

### Renames

| Original | New | Kind | Commit |
| -------- | --- | ---- | ------ |
| `scripts/collect_feedback.py`, `collect_balanced_feedback.py`, `expand_feedback.py`, `screen_feedback.py` | `scripts/collect/<same name>` | move | `76a5bda` |
| `scripts/check_balance_regressions.py`, `demo_evidence_quality.py`, `diagnose_evidence_quality_live.py`, `evaluate_balance_review.py`, `export_balance_review_followups.py`, `prepare_balance_design.py`, `present_quality_screening_results.py`, `protect_quality_screening_checkpoint.py`, `replay_balance_admission.py`, `resume_quality_screening_local.py`, `review_balance_live.py`, `run_balance_regression_live.py`, `run_quality_screening_experiment.py`, `run_quality_screening_recovery.py` | `scripts/experiments/<same name>` | move | `76a5bda` |
| `scripts/test_balance_controls.py` | `scripts/experiments/run_balance_controls_live.py` | move, rename | `76a5bda`, `4b45de5` |
| `scripts/test_balance_numeric_extraction.py` | `scripts/experiments/run_balance_numeric_extraction_live.py` | move, rename | `76a5bda`, `4b45de5` |
| `scripts/test_balance_semantic_controls.py` | `scripts/experiments/run_balance_semantic_controls_live.py` | move, rename | `76a5bda`, `4b45de5` |
| `scripts/test_grounded_feedback.py` | `scripts/experiments/run_grounded_feedback_live.py` | move, rename | `76a5bda`, `4b45de5` |
| `scripts/verify_cli_install.py` | `scripts/maintenance/verify_cli_install.py` | move | `76a5bda` |
| `configs/feedback-collection-latest-balanced.json` | `configs/feedback-collection-balanced.json` | rename | `533d152` |
| `configs/feedback-latest-20261027-source-reviews-v2.json` | `configs/20261027-feedback-source-reviews-v2.json` | rename | `533d152` |
| `data/raw/feedback/20261027-latest-balanced/` (ignored) | `data/raw/feedback/20261027-balanced/` | `mv`, 19 file hashes equal | `60ec836` |
| `data/evaluation/evidence-quality-real-v1-pending/` | `data/evaluation/evidence-quality-real-v1/` (status in manifest) | rename | `c57d49b` |
| `data/raw/glossary/<name>-20261008.json` (7, ignored): `alias-validation`, `community-aliases`, `name-pairing`, `official-moves`, `unique-move-aliases`, `unique-move-alias-validation`, `unique-move-reference` | `data/raw/glossary/20261008-glossary-sources/<name>.json` | `mv`, 7 hashes equal | `6726a0b` |
| `data/evaluation/pending-character-candidates.json` | `data/evaluation/character-alias-candidates-v1/candidates.json` | rename (P3-D06) | `9ee0e72` |
| `data/evaluation/evidence-quality-synthetic-v1/cases.json` (copy) | symlink to `src/aimediator/assets/fixtures/cases.json` | replace (decision 9) | `a774bbb` |
| `data/raw/feedback-collector.lock`, `feedback-http-state.json` (code paths) | `runs/state/` | path change | `3bcbbc0` |

Hard-coded path changes (G7):

| File | Original value | New value | Commit |
| ---- | -------------- | --------- | ------ |
| `src/aimediator/engine.py` | `--out` default `reports/balance-quality-v1` | `runs/balance-quality-v1` | `0624193` |
| `scripts/experiments/run_grounded_feedback_live.py` | fallback output `reports/grounded-<stamp>` | `runs/grounded-<stamp>` | `0624193` |
| `scripts/experiments/check_balance_regressions.py`, `evaluate_balance_review.py` | `--baseline` default `reports/balance-engineering-20261022-final-review` | required | `b6a2431` |
| `scripts/experiments/run_quality_screening_experiment.py` | `--from-run` default `reports/balance-review-v2/relevance` | required | `b6a2431` |
| `scripts/experiments/run_quality_screening_recovery.py` | `--from-run` default `reports/quality-screening-existing-100-v1` | required | `b6a2431` |
| `scripts/collect/collect_feedback.py`, `collect_balanced_feedback.py`, `expand_feedback.py` | `data/raw/feedback-collector.lock`, `data/raw/feedback-http-state.json` | `runs/state/` (one `STATE` constant, created on first use) | `3bcbbc0` |
| `scripts/collect/collect_balanced_feedback.py` | `--config` default `configs/feedback-collection-latest-balanced.json` | `configs/feedback-collection-balanced.json` | `533d152` |
| `src/aimediator/assets/data/glossary.json` | `evidence_file` `data/raw/glossary/community-aliases-20261008.json`, `unique-move-reference-20261008.json` | `data/raw/glossary/20261008-glossary-sources/community-aliases.json`, `unique-move-reference.json` | `6726a0b` |

`glossary.json` SHA256 changed from `5d2eca7b…5d90` to `66f29236…2165`
(decision 11). The glossary vector index in `data/processed/` was built
from the old hash; its texts are unchanged and searching still works, but
a rebuild gets a new identity (recorded in its manifest).

Old names kept on purpose: historical report manifests and summaries in
`reports/` (byte copies or provenance), the deletion log in
`docs/reviews/directory-cleanup.md`, `former_name` and `former_path`
fields in the new manifests, and bare script names in documents (batch 4).

### Archive

| Path | Files | Bytes | Reason | Archive |
| ---- | ----: | ----: | ------ | ------- |
| `scripts/build_screening_audit.py` and the nine `*latest*` scripts | 10 | 80,168 | one-off scripts of archived runs (P3, P3-D02) | `~/Archives/AIMediator/scripts/` |
| `scripts/run_smoke_test.py`, `scripts/render_test_results.py` | 2 | 27,209 | inputs no longer exist (P3-D03) | same |

Order as in batch 2 (G6): copy with `cp -a --reflink=auto`, write
`SHA256SUMS`, verify the archive with `sha256sum -c` and the sources
against the same list, then `git rm` (contents also in git history).
`SHA256SUMS` holds 12 entries and was re-verified at the end of the batch.

### Runs that can no longer be resumed

Accepted in plan P3 ("How"). Run identities hash script bytes and paths,
dataset paths and `glossary.json`; after this batch these runs cannot be
resumed or replayed in place. All are in the external archive (batch 2);
`runs/` holds none of them.

| Run (archive name) | Why |
| ------------------ | --- |
| `latest-balanced-20261027` | dataset renamed; its scripts archived; `glossary.json` changed |
| `quality-screening-existing-100-v1`, `quality-screening-existing-100-recovered-v2` | identity names `scripts/run_quality_screening_experiment.py` (moved; bytes changed); `data/glossary.json` hash changed |
| `screening-audit-20261027` | script archived |
| `evidence-quality-v1-live-verified` | identity names `scripts/diagnose_evidence_quality_live.py` (moved) |
| `balance-review-v2`, `balance-review-v22`, `balance-engineering-20261022-final-review`, `evidence-quality-v1-delivery`, `cli-implementation-20261028` | `glossary_sha256` in engine identities changed |

### Results

State at `fdaa023`. Tests: 222 (221 + `test_evaluation_sets.py`), also in
a fresh `git clone`, where the symlink and the 11 dataset manifests are
present. Full rule check saved (ignored) to `runs/reorg-p3-violations.txt`.

| Rule | Batch 2 | Batch 3 start | Batch 3 | Change | Remaining |
| ---- | ------: | ------------: | ------: | -----: | --------- |
| G2 | 1 | 1 | 0 | −1 | — |
| G3 | 1 | 2 | 2 | 0 | `notes` (batch 4); `.claude` (P3-D08) |
| G7 | 14 | 14 | 6 | −8 | 5 documents (batch 4); `run_local_direction_comparison.py` (P3-D01) |
| G8 | 21 | 21 | 1 | −20 | `docs/reviews/latest-balanced-validation.md` (batch 4) |
| G9 | 0 | 0 | 0 | 0 | — |
| D1 | 2 | 2 | 2 | 0 | batch 4 |
| D2 | 20 | 20 | 20 | 0 | batch 4 |
| D4 | 24 | 24 | 24 | 0 | batch 4 |
| D5 | 17 | 17 | 17 | 0 | batch 4 |
| D6 | 0 | 0 | 0 | 0 | — |
| D7 | 3 | 3 | 3 | 0 | batch 4 |
| D8 | 10 | 10 | 10 | 0 | batch 4 |
| P1 | 7 | 7 | 0 | −7 | — |
| P2 | 0 | 0 | 0 | 0 | — |
| P3 | 39 | 39 | 0 | −39 | — |
| P4 | 0 | 0 | 0 | 0 | static count 222 |
| **Total** | **159** | **160** | **85** | **−75** | |

P3 "Done when", outside bypassed items:

- `scripts/` root holds the seven registered forwarding scripts and
  `collect/`, `experiments/`, `maintenance/` only: met.
- No `test_` prefix under `scripts/`: met.
- No code default argument names `reports/` or a dated run directory:
  met except `run_local_direction_comparison.py` (P3-D01). Checked by hand
  beyond the tool, which exempts `data/` paths: `expand_feedback.py`
  `--output` and `screen_feedback.py` `--input` default to existing dated
  raw datasets (P3-D10, bypassed). Input defaults that read a dataset
  (`engine.py`, `run_grounded_feedback_live.py` `--dataset`) are not output
  paths.
- No `/home/` path in tracked code: met. The only matches are the check
  tool's own pattern and comment and a test fixture string, which the G7
  check does not count.
- G2, G7, G8, P1, P3 at 0 apart from the exceptions listed above; P7
  (checked by hand): `src/aimediator/assets/` is the only prompt and
  policy source; `configs/` holds collection and screening configuration
  plus the three registered links; `prompts/` holds the 14 registered
  links plus the two legacy prompts (P3-D04).
- The 26 tracked files under `reports/` scanned by hand (P3-D07): no
  `/home/` path, no URL.

### Deferred

Nothing here was changed in batch 3.

1. **Bypassed decisions** P3-D01, P3-D04, P3-D07, P3-D08, P3-D09,
   P3-D10: waiting for the owner.
2. **Documents naming archived scripts or old commands** (batch 4):
   `docs/reviews/latest-balanced-validation.md` (archived `*latest*`
   scripts), `README.md` (`run_smoke_test.py` is gone; step 4 uses
   `prompts/extract-feedback.txt`; `reports/grounded-20261015-pilot/`),
   `docs/reviews/balance-review-v2.md` (three commands relied on the old
   `--baseline` default, now required), bare script names elsewhere.
3. **Stale `dist/`** (batch 2 deferred item 6) is unchanged; P5 rebuilds it.
4. **Glossary vector index**: built from the previous `glossary.json`
   hash; rebuild with `python3 scripts/glossary_vectors.py build` when an
   embedding endpoint is available (not needed for search).
5. **Batch 2 deferred items** 1 (document references to moved-out
   reports), 3 (reports without a result record) and 6 stand; items 2 and
   4 were done in this batch; item 5 became P3-D07.
