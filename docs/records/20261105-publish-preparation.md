# Publish Preparation Change Record

- Type: Record
- Status: Draft
- Updated: 2026-11-05
- Applies to: commit `75f4286` and later; `RULES.md` v1.5 and v1.6; evaluation sets `balance-regressions-v1`, `balance-regressions-v2`, `evidence-quality-real-v1` and `evidence-quality-real-v2`

## Purpose

The change record of the preparation for the first push of the repository
to GitHub. The work order is kept outside the repository at the owner's
request (`~/Archives/AIMediator/planning/20261105-publish-preparation-handoff.md`);
its step IDs (S0 to S11) and decision IDs (PP-D01 to PP-D08) are used
here.

The preparation removes links to commenters' accounts from the tracked
evaluation sets, adds a license, completes the package metadata, rewrites
the root README for public readers, and rewrites the git history so that
no commit holds the removed links or the owner's home directory path. It
then pushes the repository to a private GitHub repository for the owner's
review. Making it public and the release follow that review.

Commit hashes written in this record before the "History rewrite" section
are hashes from before the rewrite; they resolve through the commit map
named there.

## Owner decisions

All answers were given by the owner in person on 2026-11-05.

| ID | Question | Answer | Notes |
| -- | -------- | ------ | ----- |
| PP-D01 | How to handle the two real-comment evaluation sets | A: `-v2` successors without the link fields; comment text and labels unchanged | Option B (withholding the text too) would break the regression test and the behavior lock |
| PP-D02 | The code license and the copyright holder's name | MIT; "Wanlin Young (Camille Yang)" | The name is used in `LICENSE` and in the `pyproject.toml` authors, without an email |
| PP-D03 | Approval of the `RULES.md` v1.6 wording | Approved as shown | The exact diff was shown before the commit |
| PP-D04 | Repository name, path to public visibility, About text, topics | `HYPOXIAN/AIMediator`, created private; About text as proposed | The owner asked to push to "my current private repo"; no such repository existed and the checkout had no remote, so the owner confirmed creating it. The owner asked to keep it private until their review: the visibility change and the topics wait for that review |
| PP-D05 | A corrected report PDF | Not now: the committed PDF is kept | `~/Downloads/AI-Mediator-Project-Report.pdf` was still byte-identical to the committed file. Both defects stay open (see "Open items") |
| PP-D06 | How to clean the history | `git filter-repo` in place, after the S1 backup | Keeps every commit and tag; the commit map resolves old hashes |
| PP-D07 | The commit email | Rewrite to the GitHub no-reply address `180716825+HYPOXIAN@users.noreply.github.com` | Built from the account ID of `HYPOXIAN`; the repository's `user.email` is set to it as well |
| PP-D08 | Whether to release | Not decided | The release follows the visibility change (S10), which the owner deferred to their review |

## Withheld and removed content

Entered under RULES.md G6. Every item has a backup: the full bundle
`~/Archives/AIMediator/20261105-pre-publish/aimediator-all.bundle` (all
refs, taken at `75f4286` before any change), and for the two evaluation
files also a plain copy under
`~/Archives/AIMediator/20261105-pre-publish/data-evaluation/`. The folder
has a `SHA256SUMS`.

| Path | Reason | Backup | References left in frozen documents |
| ---- | ------ | ------ | ----------------------------------- |
| `data/evaluation/balance-regressions-v1/cases.json` | Each of the 12 cases holds `source.source_url`, a link to the commenter's Steam profile (G9). Successor: `balance-regressions-v2` | `data-evaluation/balance-regressions-v1/cases.json`, sha256 `69b5c34c1c5f1c77866fd6a485f4beebf92377e921392ab4bdcb5f66604878ff` | `docs/records/20261022-balance-review-v2.md`, `docs/records/20261103-code-restructuring.md`, `docs/archive/pipeline-upgrade.md`, `docs/archive/code-restructuring-handoffs/b0-safety-net.md` |
| `data/evaluation/evidence-quality-real-v1/annotation-template.json` | Each of the 300 items holds `source_url`, a link to the commenter's Steam profile (237 items) or to the YouTube comment itself (63 items) (G9). Successor: `evidence-quality-real-v2` | `data-evaluation/evidence-quality-real-v1/annotation-template.json`, sha256 `37813fa9124e8f13af464e1ddfd24939d02cbe1b4807853788a002d580260490` | `docs/records/20261026-evidence-quality-implementation.md`, `docs/records/20261103-reorganization.md`, `docs/records/20261103-code-restructuring.md`, `docs/archive/reorganization.md`, `docs/archive/code-restructuring-handoffs/b0-safety-net.md`, `reports/evidence-quality-verification-v1/summary/verification.json` |
| `cli-demo/input.jsonl` (history only) | 50 real reviews with links to the commenters' Steam profiles; deleted from the tree in `bec7512`, removed from the history in S8 | The bundle | None in living documents |
| `cli-demo/labels/annotation-template.json` (history only) | Links to the commenters' Steam profiles; deleted from the tree in `bec7512`, removed from the history in S8 | The bundle | None in living documents |
| The owner's home directory path in old versions of 12 files (history only) | G7; removed from the tree in `9c6587e`. S8 replaces it in every old version | The bundle | None |

Both v1 directories keep their frozen `manifest.json` and gain an
`errata.json` that names the successor and the archive. This follows the
pattern of `data/raw/`, where the manifest is tracked and the content is
not. The frozen documents listed above keep their references unchanged
(D3); the v1 directory and its errata still resolve them.

## Steps and verification

| Step | Status | Tests | Rule check | Notes |
| ---- | ------ | ----- | ---------- | ----- |
| S0 | done | 333 | 0 | HEAD `75f4286`, tree clean, hook path `scripts/maintenance/hooks`, 31 tags, no remote, 309 commits |
| S1 | done | — | — | Bundle verified ("complete history"); `git bundle list-heads` shows `main` and 31 tags. `SHA256SUMS` covers the bundle and the two v1 directories |
| S2 | done | 333 | 0 | See "S2 successor sets" |
| S3 | done | 333 | 0 | `LICENSE` (MIT, unmodified text, "Copyright (c) 2026 Wanlin Young (Camille Yang)"); `RULES.md` v1.6 in the approved wording (G3, D2, P5, revision log); `LICENSE` added to `G3_ALLOWED` and to the G3 allowlist test; `license = "MIT"` and `license-files` in `pyproject.toml`; README Layout and License section; `CLAUDE.md` "Applies to" line |

### S2 successor sets

Both v2 files were written from v1 with the v1 layout (indent 2,
`ensure_ascii` off, key order kept, trailing newline); serializing v1 the
same way reproduces it byte for byte. `diff` against v1 shows only the
removed `source_url` lines: 12 for the regression set, 300 for the real
set, and no added lines.

| Set | File | sha256 |
| --- | ---- | ------ |
| `balance-regressions-v2` | `cases.json` | `63732ace3981081bddbd0519a324cd3c6eedbeb503ff95b15d0a03e23e9d6d3d` |
| `evidence-quality-real-v2` | `annotation-template.json` | `7f71cac4d9f625d01bef68c790250e642080fdecec57c9ecc9dc77541dc3b65e` |

- The v2 manifests are copies of v1 with these changes only: `version`
  set to v2, the hash that covers the changed file, and the new fields
  `derived_from` (v1 name, file and sha256) and `change`. For the
  regression set the covering hash is `cases_sha256`. The real set's
  manifest has no hash of the template (`input_sha256` covers the
  collection input), so no hash changed there. Its `version` was
  `evidence-quality-evaluation-v1` and is now
  `evidence-quality-evaluation-v2`.
- The `change` text of the regression set names only Steam profiles,
  because the set holds no YouTube comments.
- The regression set's `source_hashes` are identical to v1, and each one
  was recomputed from the v2 text.
- Neither v2 set matches a Steam profile URL with a 17-digit ID or a
  YouTube comment link (`lc=` followed by a comment ID), and neither holds
  any other `http` link.
- The references in `tests/behavior_lock.py`, `tests/test_balance_review_pipeline.py`
  and `scripts/experiments/check_balance_regressions.py` point at v2.
  `tests/fixtures/behavior-lock.json` is unchanged and the behavior lock
  passes.

## History rewrite

Filled in at S8.

## Open items

- The two defects of the project report (PP-D05): on page 5 the
  "4.1 Local Setup" heading has no content and the setup paragraph sits
  under 4.2, followed by a stray line "4.2 How the local model failed";
  on page 8, reference [19] "README.md" is auto-linked to an external
  website. The owner can fix the Google Docs source and replace the PDF
  in a later commit.
- Withholding the comment text as well (PP-D01 option B), if wanted later.
- The visibility change to public, the topics, the release `v0.1.0`
  (PP-D08) and the final status of this record, after the owner's review
  of the private repository.
- No PyPI publication is planned.
