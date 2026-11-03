# AIMediator Project Cleanup and Reorganization Plan

- Type: Plan
- Status: Active
- Updated: 2026-11-03
- Applies to: baseline commit `0d390c4` and later; `RULES.md` v1.0
- Translated 2026-11 from the approved Chinese plan (finalized 2026-11-03).
  Archive copy of the original: `~/Archives/AIMediator/planning/reorganization-plan.zh.md`.

> **Basis**: `RULES.md` v1.0 (rule IDs are cited directly below)
> **Starting point**: baseline commit `0d390c4` (175 files, all 192 offline tests passing)
> **Backup**: `~/Archives/AIMediator/20261103-baseline/`, 20,989 files, verified with SHA256; `.env` is not in the backup
> **Language**: the original was written in Chinese for review. During batch 1 it is stored in English as `docs/plans/reorganization.md` (D8). The English version is the basis for executing all later batches.

---

## 0. Execution principles (apply to every phase)

1. **Entry condition**: before each phase starts, the working tree must be clean and all offline tests must pass.
2. **One kind of operation per commit** (G5): for example, "move reports out" and "rename datasets" must not share a commit. Commit messages cite the relevant rule IDs and carry no agent attribution of any kind (P5, P6).
3. **List first, then execute**: every phase that moves, deletes or renames anything first produces a migration list (object → action → reason → referenced by → destination). Execution starts only after the owner has reviewed it.
4. **Fixed order for deleting non-reproducible content**: copy to the archive first, then verify SHA256, then delete, and enter it in the change record (G6). The whole reorganization shares one change record: `docs/records/20261103-reorganization.md`.
5. **Phase exit**: at the end of each phase, run the rule-check tool (implemented in phase 1). Violations of the rules that phase is responsible for must reach 0; otherwise the next phase does not start. After the check passes, tag `reorg-pN`.
6. **Rollback**: tracked files with `git revert` or by returning to the previous tag; ignored data is restored from the backup or the archive.
7. **One-off migration exception** (agreed): the translation, header additions and link fixes applied to existing documents in phase 4 are not bound by D3 ("records are frozen once final"). Freezing starts once a document has entered the new index.
8. **Execute in batches**: see section 2. Each batch is completed in its own session and ends with a tag; the next batch starts only from the previous batch's tag.

## 1. Phase overview

| Phase | Goal | Main rules | Depends on |
| ------ | ------ | ---------- | ------ |
| P0 Baseline | Build a safety net | G5, P5 | — (**done**) |
| P1 Rules in place | Rules enter the project; violations become measurable | G1, G2, G10, P6 | P0 |
| P2 Move generated output out | Move bulk and noise out of the project | G4, G6, G9, P2, Q5 | P1 |
| P3 Code and resources in place | Paths, naming, scripts and data all comply with the rules | G2, G7, G8, P1, P3, P7 | P2 |
| P4 Documentation reorganization | The documentation system complies with the rules | D1–D9, G7 | P2, P3 (documents must cite the final paths of code and reports) |
| P5 Final acceptance | Prove every rule is satisfied, and lock it in | G10 and all rules | P1–P4 |

Documentation comes last because the script paths, dataset names and report locations cited in documents only settle after P2 and P3. Doing it the other way round would mean fixing links twice.

## 2. Implementation batches

The work is executed in 4 batches. The split rests on three considerations:
- **Review points must come one after another**: P2, P3 and P4 each have a migration list to review, and each list depends on the result of the previous phase.
- **Work with different kinds of risk is kept apart**: P2 contains irreversible deletions, P3 changes code, P4 touches only documents.
- **Every batch ends in a stable state**: tests pass and a tag is set, so pausing midway leaves nothing half-done.

| Batch | Phases | Review point (stop and wait for approval before executing) | Start | Exit tag |
|------|----------|----------------------------|------|----------|
| 1 | P1 | None (only adds files; no moves, no deletions) | `0d390c4` | `reorg-p1` |
| 2 | P2 | Move-out and deletion list | `reorg-p1` | `reorg-p2` |
| 3 | P3 | Rename and archive list | `reorg-p2` | `reorg-p3` |
| 4 | P4 + P5 | Document destination list | `reorg-p3` | `reorg-done` |

- P5 only verifies and does not change structure, so it is merged into batch 4.
- If batch 4 turns out too large, "add headers, translate, slim down the README, final acceptance" can be split off as batch 5, with the completion of batch 4's moves as the dividing line.
- **The pre-commit hook is enabled in two steps**: batch 1 installs it in report-only mode, without blocking commits (violations are certain to exist during the reorganization, and blocking would stop every commit); batch 4 switches it to blocking mode once violations reach zero.

---

## P0 Baseline (done)

- [x] `git init`, with a full baseline commit `0d390c4` on the `main` branch. Large data stays ignored; `.env` is not tracked.
- [x] Two checks were run before the commit: a credential pattern scan, and a comparison of the values in `.env` against the files to be tracked. Neither produced a hit.
- [x] A full backup was written to `~/Archives/AIMediator/20261103-baseline/`, including `SHA256SUMS`, `SYMLINKS.txt` and `README.txt`, and compared one by one against the original files with a matching result.
- [x] Offline test baseline: 192 tests pass.

**Note**: this backup is a btrfs reflink copy on the **same disk** as the project. It protects against accidental deletion but not against disk failure. It has been decided not to make an off-site copy, because whether the archived content is still worth keeping is itself still to be investigated.

---

## P1 Rules in place and the check tool

**What**
- Put `RULES.md` (final English version) in the root. Create `CLAUDE.md` with only three items: a reference to `RULES.md`, a list of common commands (test, check, install), and the statement "no attribution". Create `.env.example` listing key names only.
- Create the compatibility register `docs/reference/compatibility-layers.md` (G2): register the 18 symlinks and 6 forwarding shells, stating for each what it points to, who uses it and its removal condition. Per the Q4 decision, this time they are **registered only, not removed**.
- Create the change record `docs/records/20261103-reorganization.md`; later phases keep appending to it.
- Implement the rule-check tool `scripts/maintenance/check_rules.py`: read-only, outputs a violation list by rule ID, exits non-zero when there are violations, and supports checking only some rules. It covers at least the following checks:

  | Check | Rule |
  | -------- | ---------- |
  | Root allowlist | G3 |
  | Absolute paths | G7 |
  | Naming (kebab-case, date prefix, forbidden words) | G8, D6 |
  | Credential scan, package content listing | G9 |
  | Links | D5 |
  | Document headers | D2 |
  | Document index consistency | D4 |
  | JSON and oversized files in `docs/` | D7 |
  | Chinese appears only in corpus content | D8, allowlist criteria in P4 |
  | Symlinks and forwarding shells are all registered | G2 |
  | `test_` prefix in `scripts/` | P3 |
  | `reports/` subdirectories have a manifest | P2 |
  | Datasets have a manifest; no runtime state files under `data/` | P1 |
  | Test count not below the baseline | P4 |

- The check tool itself also gets offline tests.
- Add `runs/` to `.gitignore`. This step is brought forward from P2 to here because the violation baseline is written to `runs/`.
- **Install the pre-commit hook in report-only mode, without blocking**:
  - The hook script lives at `scripts/maintenance/hooks/pre-commit` under version control; it is enabled with `git config core.hooksPath scripts/maintenance/hooks`. This adds no top-level directory (G3).
  - The hook runs the check tool and prints violations, but always exits 0.

**How**
- The check tool depends only on the standard library, does not read the contents of `reports/`, and never prints any credential value.
- The result of the first run is saved to `runs/` as the "violation baseline". Every later phase compares its progress against it.

**Done when**
- `RULES.md`, `CLAUDE.md` and `.env.example` are in the root and committed; `CLAUDE.md` contains no rules of its own (G1).
- The register covers all 24 compatibility layers (G2 check reports 0 violations).
- The check tool runs to completion and gives violation counts by rule ID. These counts are the progress table for the later phases.
- Tests pass, with a count of 192 plus the newly added check-tool tests.
- The hook is enabled: commits print violations but are not blocked.
- The English version of the plan is at `docs/plans/reorganization.md`.

---

## P2 Moving generated output out, and cleanup

**What**
- **`reports/`** (Q3, option b): the 15 directories are handled in two groups.
  - **The 11 directories referenced by documents or code** (`balance-engineering-20261022-final-review`, `balance-review-v2`, `balance-review-v22`, `cli-implementation-20261028`, `evidence-quality-v1-delivery`, `evidence-quality-v1-live-verified`, `evidence-quality-v1-verification`, `latest-balanced-20261027`, `quality-screening-existing-100-v1`, `quality-screening-existing-100-recovered-v2`, `screening-audit-20261027`): the full content moves to `~/Archives/AIMediator/reports/`. Only `manifest.json` and a curated summary (the existing `evaluation.md`, `review-summary.md` and similar) stay in the project. Directory names are renamed per G8 at the same time (removing `final`, `latest`). The manifest records the original name, the archive path, the corresponding record document, the dataset and the code version.
  - **The 4 directories with no references at all** (`cli-demo-backups`, `cli-demo-monitoring`, `cli-real-unfiltered-20261028`, `cli-walkthrough-16-20261029`): archived only, nothing kept in the project.
  - The 58 code files, zips and tsx files scattered through the reports go, together with their directories, into a `provenance/` subdirectory of the archive (P2).
- **`.gitignore` adjustment**: the manifests and summaries under `reports/` become tracked (they are small). `runs/` was already ignored in P1.
- **`dist/`**: delete the 112MB workspace zip and the duplicate wheel under `dist/refactored/` (both are in the backup), keeping only the current wheel and sdist.
- **Reproducible products**: delete `build/`, `*.egg-info`, `__pycache__` (G4).
- **`cli-demo/`** (Q5): delete entirely; the related reports are handled in the "archive only" group above. One test in `test_cli_presentation.py` calls `cli-demo/prepare-labels.py`; it is **rewritten** so that it does not depend on cli-demo, and the test baseline stays at 192 (decided).
- **Other**: delete the empty directories `.agents/`, `.codex/`, `.aws/` (P6); delete leftover lock files. The HTTP state file is deleted after archiving; its storage path is changed in P3.

**How**
- Produce the migration list first; execute only after the owner has reviewed it.
- Archiving follows "copy → verify → delete"; one commit per category (reports, dist, demo, miscellaneous).
- Before executing, confirm that no collection or analysis process is running.

**Done when**
- The part of the project excluding `data/` is under 20MB (currently about 780MB); every subdirectory under `reports/` has a manifest and contains no code files, backups or interrupted runs (P2 check reports 0 violations).
- Every moved-out directory in the archive has a `SHA256SUMS`, and it has been verified.
- G4 verification: after deleting every ignored directory, the tests still pass.
- In the G3 check, `cli-demo` and the empty directories no longer appear; the G9 scan passes.

---

## P3 Code, scripts and resources in place

**What**
- **Scripts** (P3):
  - Scripts that are not compatibility layers move by purpose into the three subdirectories `collect/`, `experiments/` and `maintenance/`.
  - The 6 forwarding shells **stay at their original paths**. They are registered compatibility layers and, per the Q4 decision, are not touched this time.
  - The 4 `test_*.py` files are renamed, for example to `run_*_live.py`.
  - One-off scripts bound to a single run (`finish_`, `finalize_`, `complete_`, `recover_latest_*`, `replay_latest_*`, `rerun_latest_*` and so on) are archived or deleted along with their run, as long as that run has been archived.
- **Hard-coded paths** (G7):
  - `engine.py` and the other scripts that write results change their default output to `runs/`.
  - Code that references archived reports (15 files in total) is changed to receive its input through explicit arguments, or is archived together with the one-off scripts.
  - The paths of the lock files and HTTP state files used by the collection scripts move to a location such as `runs/state/` (P1).
- **Data** (P1, G8):
  - Dataset directory renames: directories containing forbidden words, such as `20261027-latest-balanced` and `20261028-cli-unfiltered`, get descriptive names, and the 9 code and configuration files that reference them are updated in step.
  - The `pending` in `evidence-quality-real-v1-pending` is a status; it moves into the manifest.
  - Every dataset gets a `manifest.json`.
- **Prompts and configuration** (P7):
  - The two legacy prompts in the root `prompts/`: archived after confirming they are unreferenced.
  - The two files in `configs/` containing `latest` are renamed per G8, and their references are updated in step.
  - `src/aimediator/assets/` remains the only source; this does not change.

**How**
- Use `git mv`; a rename and the update of all its references go in the same commit.
- Run the tests after every commit, and use grep to confirm the old name no longer appears anywhere.
- Renames may make old runs impossible to resume (the run identity includes source hashes), but the affected old runs are archived in P2, so the impact is acceptable. This is stated in the change record.

**Done when**
- The root of `scripts/` holds only the registered forwarding shells and the three subdirectories; there is no `test_` prefix in `scripts/`.
- Code default arguments contain no `reports/` and no dated run directory; tracked code contains no `/home/` paths.
- The G2, G7, G8, P1, P3 and P7 checks all report 0 violations (registered exceptions excepted); tests pass.

---

## P4 Documentation reorganization

**What**: migrate by D1 category. The preliminary mapping is below; it will be confirmed once more as a migration list before execution.

| Existing file | Destination | Notes |
| ---------- | ------ | ------ |
| `cli-usage` | `guides/cli-usage.md` | Update `MANIFEST.in` in step |
| `cli-design-handoff` | `design/cli.md` | |
| `balance-analysis` | `design/balance-analysis.md` | |
| `evidence-quality-handoff` (Chinese) | `design/evidence-quality.md` | Translate; merge with or place alongside `module-reports/emotion-quantification…` |
| `cli-implementation-status` | `plans/cli-implementation-status.md` | |
| `review-todo` | `plans/review-follow-ups.md` | Still contains open external items |
| `next-development-plan` | `archive/` | Outdated (confirmed); status set to `Archived` |
| `evidence-quality-implementation` (Chinese) | `records/20261026-evidence-quality-implementation.md` | Translate |
| `balance-review-v2` | `records/20261022-balance-review-v2.md` | |
| `latest-balanced-validation` | `records/20261027-balanced-validation.md` | |
| `directory-cleanup` | `records/20261028-directory-cleanup.md` | |
| `refactoring` | `decisions/0001-package-as-single-runtime.md` | Rewritten as an ADR |
| `glossary`, `glossary-vector-index` | `reference/` | The Chinese in the glossary is corpus content and may stay |
| `alias-review`, `low-alias-review` (.md and .json), `unique-move-alias-review` | Moved to the external archive `~/Archives/AIMediator/docs-data/` (D7, decided) | `docs/` keeps only a short conclusion record, `records/20261022-alias-review.md` |
| The two `*-coding-agent-prompt` files | `archive/` | P6 |
| `notes/10-22-meeting.md` | `meetings/20261022-work-summary.md` | Then delete `notes/` |

In addition:
- Add the D2 header to every document; create the master index `docs/README.md` (D4).
- Slim the root `README.md` down to an entry point: keep the introduction, installation, quick start, directory layout and the link to the index. The research-history parts move into the corresponding records or the archive; the Chinese sections in it are translated into English.
- Links pointing to moved-out reports are changed to point to `reports/<name>/manifest.json` inside the project, so the links keep working. Fix the absolute paths in 5 documents (G7).
- D8 allowlist criteria: glossary-type documents and corpus quotation blocks may contain Chinese; Chinese anywhere else in a document is a violation.

**How**
- Move first, rewrite afterwards, in separate commits: first `git mv` and fix links, then add headers and translate. This keeps git's rename tracking working.
- Translation changes only the language, not conclusions or data. Rewritten documents are marked `Translated 2026-11` in their header.

**Done when**
- The D1–D9 checks all report 0 violations; broken links are 0 (currently 13).
- The index matches the file list exactly; there are no JSON files under `docs/`.
- `README.md` is no longer than about 150 lines (currently 227).
- Every path listed in `MANIFEST.in` exists, and the built sdist actually contains those files.

---

## P5 Final acceptance and lock-in

**What**
- Run the full rule check: 0 violations apart from registered exceptions.
- **Clean-clone verification**: `git clone` into a temporary directory, then install, run the offline tests, and run `aimediator doctor --offline` and `aimediator demo`. This exposes hidden dependencies on ignored data (G4).
- Build the wheel and sdist and check the package contents: no `data/raw`, no `.env` (G9).
- Check the README "Directory layout" section item by item against the actual tree (G10).
- Finalize and freeze the change record; append a "reorganization complete" entry to the `RULES.md` revision log; set this plan's status to `Archived` and move it to `docs/archive/`.
- Switch the pre-commit hook from "report only" to "blocking": commits with violations are refused (enabling it was decided).
- Tag `reorg-done`.

**Done when**
- All of the above pass, and the results are written into the change record.
- `ls -A` of the project root matches the G3 allowlist.
- Deliberately creating a violation (for example a new file in the root) and attempting to commit is blocked by the hook; the violation is undone after verification.

---

## 7. Decisions taken (2026-11-03)

1. The test that depends on cli-demo is **rewritten** so it does not depend on cli-demo; the test baseline stays at 192.
2. The one-off migration exception (see section 0, item 7) is **agreed**.
3. **No** off-site backup; whether the archived content is still worth keeping is investigated separately.
4. `next-development-plan` is outdated and is **archived**.
5. The alias review dumps go only into the **external archive**; the project keeps only one conclusion record.
6. The phase order is **agreed**; the pre-commit hook is **enabled**, in the two steps described in section 2.
7. Execution is in **4 batches** as described in section 2.
