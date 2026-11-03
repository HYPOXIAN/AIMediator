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
3. **List first, then execute**: every phase that moves, deletes or renames anything first produces a migration list (object → action → reason → referenced by → destination). In batches 1 and 2, execution starts only after the owner has reviewed it. From batch 3 on, the list is a working document and the owner reviews after implementation (section 2; section 7, decision 13).
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
- **Review points must come one after another**: P2, P3 and P4 each have a migration list, and each list depends on the result of the previous phase.
- **Work with different kinds of risk is kept apart**: P2 contains irreversible deletions, P3 changes code, P4 touches only documents.
- **Every batch ends in a stable state**: tests pass and a tag is set, so pausing midway leaves nothing half-done.

| Batch | Phases | Review point | Start | Exit tag |
|------|----------|----------------------------|------|----------|
| 1 | P1 | None (only adds files; no moves, no deletions) | `0d390c4` | `reorg-p1` |
| 2 | P2 | Before execution: move-out and deletion list | `reorg-p1` | `reorg-p2` |
| 3 | P3 | After implementation: decisions and rename and archive results (decision 13) | `reorg-p2` | `reorg-p3-review`, then `reorg-p3` |
| 4 | P4 + P5 | After implementation: decisions and document destination results (decision 13) | `reorg-p3` | a review tag, then `reorg-done` |

- **Post-implementation review (batches 3 and 4, decision 13)**: the batch does not stop for approval of its migration list. Before changing code or data, it enters every choice that needs the owner in the change record under "Decisions pending owner review" and commits that on its own. A decision is implemented as recommended only if reverting its commit (and, where needed, restoring from the archive) fully undoes it; otherwise the batch bypasses it and keeps the current state. Each implemented decision is a commit of its own whose message body names it (`Decision: P3-Dnn`). The batch ends with a `-review` tag; after the owner's review, rejected decisions are reverted or redone, bypassed ones are implemented or deferred, and the final tag is set.
- P5 only verifies and does not change structure, so it is merged into batch 4.
- If batch 4 turns out too large, "add headers, translate, slim down the README, final acceptance" can be split off as batch 5, with the completion of batch 4's moves as the dividing line.
- **The pre-commit hook is enabled in two steps**: batch 1 installs it in report-only mode, without blocking commits (violations are certain to exist during the reorganization, and blocking would stop every commit); batch 4 switches it to blocking mode once violations reach zero.
- **Rule amendment at the start of batch 2** (section 7, decisions 8 and 12): the first commit of batch 2 amends `RULES.md` to v1.1 (G3 and D2), records the date and reason in its revision log, and updates the G3 allowlist in `scripts/maintenance/check_rules.py` to match. The migration list follows that commit.

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
- The check tool depends only on the standard library, does not read the contents of `reports/`, and never prints any credential value. Changed by section 7, decision 20: from batch 4 it reads `reports/*/manifest.json` and `reports/*/summary/` for the G7 and G9 scans.
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
    - Renames (section 7, decision 11; pattern `[YYYYMMDD-]slug[-vN]`): `balance-engineering-20261022-final-review` → `20261022-balance-engineering-review`; `cli-implementation-20261028` → `20261028-cli-implementation`; `latest-balanced-20261027` → `20261027-balanced-validation`; `screening-audit-20261027` → `20261027-screening-audit`; `evidence-quality-v1-delivery` → `evidence-quality-delivery-v1`; `evidence-quality-v1-live-verified` → `evidence-quality-live-verified-v1`; `evidence-quality-v1-verification` → `evidence-quality-verification-v1`. `balance-review-v2`, `balance-review-v22`, `quality-screening-existing-100-v1` and `quality-screening-existing-100-recovered-v2` keep their names.
  - **The 4 directories with no references at all** (`cli-demo-backups`, `cli-demo-monitoring`, `cli-real-unfiltered-20261028`, `cli-walkthrough-16-20261029`): archived only, nothing kept in the project. They keep their original names in the archive.
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
  - Dataset directory renames: `20261027-latest-balanced` becomes `20261027-balanced`, and the code and configuration files that reference it are updated in step. Correction (section 7, decision 11): `20261028-cli-unfiltered`, listed here originally, contains no forbidden word and keeps its name.
  - The `pending` in `evidence-quality-real-v1-pending` is a status; it moves into the manifest and the set becomes `evidence-quality-real-v1`.
  - Every dataset gets a `manifest.json`.
  - Raw glossary sources (decision 11): the seven `data/raw/glossary/*-20261008.json` files move into `data/raw/glossary/20261008-glossary-sources/` without the date suffix in their names (for example `community-aliases.json`), with a `manifest.json` listing original names and SHA256 values. Contents do not change; hashes are compared before and after and entered in the change record. The two `evidence_file` paths inside `src/aimediator/assets/data/glossary.json` are updated in the same commit (D5); this changes `glossary_sha256` in run identities, as already accepted above.
  - Duplicate synthetic cases (decision 9): `src/aimediator/assets/fixtures/cases.json` stays the single file; `data/evaluation/evidence-quality-synthetic-v1/cases.json` becomes a symlink to it, registered in the compatibility register, and a new offline test checks that the file matches `cases_sha256` in that set's manifest (P1 freeze).
- **Prompts and configuration** (P7):
  - The two legacy prompts in the root `prompts/`: archived after confirming they are unreferenced. Found in batch 1: they are referenced (`extract-feedback.txt` by `scripts/run_smoke_test.py` and the README; `extract-grounded-feedback.txt` by `scripts/test_grounded_feedback.py`), so the migration list decides whether they are archived together with those scripts or kept. Decided in the batch 3 review (section 7, decision 17): `extract-grounded-feedback.txt` moves to `src/aimediator/assets/prompts/`; `extract-feedback.txt` is archived in batch 4.
  - The two files in `configs/` containing `latest` are renamed per G8, and their references are updated in step: `feedback-collection-latest-balanced.json` → `feedback-collection-balanced.json`; `feedback-latest-20261027-source-reviews-v2.json` → `20261027-feedback-source-reviews-v2.json`.
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
- `MANIFEST.in` (decision 10), changed in the same commit as the document moves: it includes only `docs/guides/cli-usage.md` and `docs/design/cli.md`. The implementation status and the archived coding-agent prompt are no longer shipped.
- `prompts/extract-feedback.txt` (decision 17): archived (copy, verify, delete) once the README rewrite no longer names it; `prompts/` then holds only registered links.
- Check tool (decision 20): reads `reports/*/manifest.json` and `reports/*/summary/` for the G7 and G9 scans, before the hook becomes blocking in P5.
- `src/aimediator/assets/data/glossary.json`: its `review_file` field points to `docs/unique-move-alias-review.md`, which moves to the external archive; it is updated to the new conclusion record `records/20261022-alias-review.md` in the same commit (D5). This is the second change to `glossary.json` in the reorganization, after batch 3.

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

Decisions taken after batch 1 (2026-11-03), on items recorded under "Deferred" in the change record:

8. **G3 amendment**: `prompts/` is added to the top-level allowlist, limited to compatibility links listed in the G2 register; the directory is removed once it is empty. Executed as the first commit of batch 2 (section 2).
9. **Duplicate `cases.json`**: the packaged fixture is the single file; the evaluation set path becomes a registered symlink, guarded by a hash test (P3, batch 3).
10. **`MANIFEST.in`**: fixed in batch 4 together with the document moves; ships `docs/guides/cli-usage.md` and `docs/design/cli.md` only (P4).
11. **Naming beyond the original list**: the renames listed in P2 and P3 (reports in batch 2; raw glossary sources, configuration files, evaluation set and raw feedback dataset in batch 3). `20261028-cli-unfiltered` keeps its name. `glossary.json` is changed twice: provenance paths in batch 3, `review_file` in batch 4.
12. **D2 scope**: D2 applies to every document under `docs/`. Exempt: the root `README.md` (it is the package long description), `RULES.md` (it carries its own version line and revision log), agent entry files, and README files inside `data/` (dataset descriptions belong to manifests). Executed with decision 8 in the v1.1 amendment; the check tool already uses this scope.

Decision taken before batch 3 (2026-11-03):

13. **Post-implementation review for batches 3 and 4**: the owner no longer approves the migration list before execution. Each batch first registers every decision that needs the owner (number, question and options, recommendation and reason, handling `implemented` or `bypassed`, effect on the rest of the batch, rollback, status, commits) in the change record and commits it; it then implements the decisions that a revert fully undoes and bypasses those that would amend `RULES.md`, change program behavior or output meaning (changing only a default path does not count), alter a registered compatibility layer, delete content without an archive copy, or rest on thin evidence or on two defensible options with very different consequences. Bypassed items do not block other work, which proceeds from the current state. Routine work that the rules and this plan already specify is not a decision. The batch sets a review tag (`reorg-p3-review` for batch 3) and stops; after the owner's review, decisions are marked `approved`, `reverted` or `deferred`, resolved ones are appended here as numbered decisions, and the final tag is set. Section 0, item 3 and section 2 are updated to match.

Decisions taken in the batch 3 review (2026-11-03), on the decisions registered in the change record (P3 section). The owner adopted every recommendation; P3-D08 (top-level `.claude/`) is deferred.

14. **Seventh forwarding script** (P3-D01): `scripts/run_local_direction_comparison.py` stays a registered wrapper (R3); it writes to `runs/<run name>` and its `--run-name` default is the undated `local-direction-comparison`.
15. **One-off scripts** (P3-D02): the nine `*latest*` scripts and `build_screening_audit.py` are archived in `~/Archives/AIMediator/scripts/` with their runs.
16. **Smoke-test scripts** (P3-D03): `run_smoke_test.py` and `render_test_results.py` are archived; their inputs no longer exist.
17. **Legacy prompts** (P3-D04): `extract-grounded-feedback.txt` moves to `src/aimediator/assets/prompts/` (single source, shipped though unused by the package); `extract-feedback.txt` is archived in batch 4 once the README rewrite drops the manual procedure step that names it.
18. **Dataset manifests** (P3-D05): `manifest.json` files under the ignored `data/raw/` and `data/processed/` are tracked through `.gitignore` exceptions.
19. **Loose alias candidate file** (P3-D06): it becomes the versioned set `data/evaluation/character-alias-candidates-v1/`, with `pending` as a status in its manifest.
20. **Check tool and `reports/`** (P3-D07): the tool reads `reports/*/manifest.json` and `reports/*/summary/` for the G7 and G9 scans; implemented in batch 4 before the hook becomes blocking.
21. **Project-root constant** (P3-D09): the package's `cwd`-based root and the scripts' `__file__`-based roots both stay for now; the choice between one package constant and a shared helper is made with the CLI work.
22. **Collection defaults** (P3-D10): `--output` of `expand_feedback.py` and `--input` of `screen_feedback.py` are required, so a bare run cannot write into a frozen raw dataset.

Decisions taken in the batch 4 review (2026-11-03), on the decisions registered in the change record (P4 section). The owner adopted every recommendation, including those for the bypassed P4-D09, P4-D11 and P4-D12 and for the deferred P3-D08.

23. **Module report** (P4-D01): `emotion-quantification-and-evidence-isolation.md` sits in `docs/design/` next to `evidence-quality.md`; the two are not merged.
24. **README research history** (P4-D02): sections whose topic has a record are appended verbatim to that record; the rest are kept verbatim in `docs/archive/readme-research-history.md`.
25. **Corpus content** (P4-D03): Chinese aliases and authored model-input cases stay in code spans as corpus (D8); authored cases carry an English rendering.
26. **ADR boundary** (P4-D04): one ADR, `0001-package-as-single-runtime.md`, written only from the refactoring note; no ADRs are written after the fact for other trade-offs.
27. **Historical commands in records** (P4-D05): kept verbatim, with a dated note on what moved.
28. **Commands in living documents** (P4-D06): new output under `runs/`; a command reading an archived run uses a `runs/<run>` placeholder and links the report manifest.
29. **Links to moved-out reports** (P4-D07): to the kept `summary/` copy when there is one, otherwise to `reports/<name>/manifest.json`.
30. **References to content that exists nowhere** (P4-D08): kept as code spans marked "(not retained)".
31. **Collector output** (P4-D09): the generated review sheet points at the dataset `manifest.json`.
32. **Hand-entered low-alias decisions** (P4-D10): listed verbatim in `records/20261022-alias-review.md`, not interpreted or applied.
33. **`.claude/` and the blocking hook** (P4-D11 with P3-D08): RULES.md v1.2 allows `.claude/` at the root as ignored local agent state.
34. **Reports without a result record** (P4-D12): the screening audit gets `records/20261027-screening-audit.md`, translated from its summary; the two quality-screening reports keep the cleanup record.
