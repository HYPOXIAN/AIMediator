# Reorganization Change Record

- Type: Record
- Status: Draft
- Updated: 2026-11-03
- Applies to: baseline commit `0d390c4` and later; `RULES.md` v1.0

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
