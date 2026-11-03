# AIMediator Project Rules

Version 1.2 · Effective 2026-11-03 · Approved by the project owner.

This file is the highest-level convention for the project's structure. Every
rule has a **Check**: the way compliance is verified. Rule IDs are stable; cite
them in commits, reviews and records.

---

## 1. Global rules (G)

**G1 Precedence.** This file overrides any conflicting code comment, document or
agent instruction. Amendments state the date and reason in the Revision log.
*Check:* agent entry files (`CLAUDE.md`, `AGENTS.md`) only reference this file
and add no rules of their own.

**G2 Single source of truth.** Each resource (code, prompt, configuration,
dataset, document) has exactly one authoritative location; other places
reference it and never copy it. A compatibility symlink or forwarding script is
allowed only when listed in the compatibility register
(`docs/reference/compatibility-layers.md`) with its removal condition.
*Check:* no duplicate-content files; every symlink and forwarding script is in
the register.

**G3 Top-level allowlist.** The project root may contain only: `README.md`,
`RULES.md`, `pyproject.toml`, `MANIFEST.in`, `.gitignore`, `.env.example`,
`.env` (local only), agent entry files (`CLAUDE.md`, `AGENTS.md`), `src/`,
`tests/`, `scripts/`, `configs/`, `data/`, `docs/`, `examples/`, `reports/`,
`runs/`, plus the ignored `build/`, `dist/` and `.venv/`. `prompts/` is also
allowed, but only for compatibility links listed in the G2 register; it is
removed once it is empty. `.claude/` is also allowed as ignored local state of
the coding-agent harness; it holds no project content. Adding a top-level
entry requires amending this rule first.
*Check:* `ls -A` matches the allowlist.

**G4 Sources and generated output are separate.** Anything reproducible from
code and data (`build/`, `dist/`, `*.egg-info`, `__pycache__`, run outputs,
caches, checkpoints, logs) lives in ignored locations and can be deleted at any
time without breaking a feature or a document.
*Check:* after deleting every ignored directory, tests pass and no document
link breaks.

**G5 Version control first.** The project is a working git repository. Every
bulk move, deletion or rename starts from a clean commit and is committed on its
own. Large data stays out of git and is backed up separately (P5).
*Check:* `git status` works; every reorganization operation has its own commit.

**G6 Irreversible operations.** Before deleting non-reproducible content (raw
data, human annotations, results cited by documents), all three must hold:
(a) a backup or git history exists; (b) no code or document references it;
(c) the path and reason are entered in the change record
(`docs/records/YYYYMMDD-<topic>.md`).
*Check:* every deletion has an entry in a change record.

**G7 Paths.** Tracked files contain no absolute user paths (`/home/...`). Code
resolves resources through one project-root constant and relative paths.
Default output paths never point at a specific historical run.
*Check:* `grep -r /home/` over tracked files is empty; no default argument names
a dated run directory.

**G8 Naming.** Directories and non-Python files use lowercase kebab-case; Python
modules use snake_case. Dates are a `YYYYMMDD-` **prefix**; versions are a `-vN`
suffix. Relative words such as `final`, `latest`, `new`, `fixed` are forbidden
because they stop being true over time.
*Check:* the naming check reports no violations.

**G9 Sensitive information.** `.env` and credentials never enter version
control, `dist/`, archives or reports, and are never printed or copied.
`.env.example` lists key names without values. Raw data contains public
authors' URLs and is not distributed in release packages or examples.
*Check:* secret scan is clean; release package listings contain no `data/raw`
and no `.env`.

**G10 Definition of done.** A structural change is complete only when: the
offline tests pass (count not below the recorded baseline), the link check
passes, `MANIFEST.in` and package contents are valid, and the README "Layout"
section matches the actual tree.
*Check:* the rule-check command set (`scripts/maintenance/check_rules.py`)
passes.

---

## 2. Documentation rules (D)

**D1 Categories and locations.** Each document has one purpose and one home:

| Type | Location | Content |
|------|----------|---------|
| Entry | `README.md` | What it is, install, quick start, layout, link to the index |
| Guides | `docs/guides/` | How to install, run, operate |
| Design | `docs/design/` | Module design, interface contracts, specifications |
| Decisions | `docs/decisions/` | ADRs named `NNNN-title.md` |
| Plans and status | `docs/plans/` | Roadmaps, to-do lists, implementation status (living) |
| Records | `docs/records/` | Dated conclusions of an experiment, validation or cleanup; frozen once final |
| Reference | `docs/reference/` | Glossaries, index descriptions, registers |
| Meetings | `docs/meetings/` | `YYYYMMDD-topic.md` |
| Archive | `docs/archive/` | Superseded or retired documents, original names kept |
| Agent handoffs | see P6 | Prompts written for coding agents |

*Check:* `docs/` has no directory outside this table and no loose files at its
root other than the index.

**D2 Header.** Every document under `docs/` starts with `Type / Status /
Updated / Applies to (version or dataset)`. Status is one of `Draft`,
`Active`, `Superseded by <document>`, `Archived`. Exempt: the root
`README.md` (it is the package long description), `RULES.md` (it carries its
own version line and revision log), agent entry files, and README files
inside `data/` (dataset descriptions belong to manifests).
*Check:* script verifies every document under `docs/` has the header.

**D3 Lifecycle.** Living documents (guides, design, plans) are updated with the
implementation. Records, decisions and meeting notes are frozen once final: only
the status header may change; corrections go in an erratum or a new record.
Superseded documents move to `docs/archive/` with their file names kept.
*Check:* final files in `docs/records/` have no changes except the header (git).

**D4 Index.** `docs/README.md` lists every document with its type, status and a
one-line description. No orphan documents. The root README links to the index
and a few core documents and does not retell the research history.
*Check:* script compares the index with the file list.

**D5 Link integrity.** Links are relative. Moving or renaming a document updates
every inbound reference in the same change: README, other documents,
`MANIFEST.in`, and strings in code.
*Check:* link check reports zero broken links.

**D6 Naming.** English kebab-case. Living documents carry no version or date in
the name (git holds versions). Records use a `YYYYMMDD-` prefix.
*Check:* covered by the G8 naming check.

**D7 Documents are not data stores.** Machine-generated tables, review dumps and
JSON belong in `data/` or `reports/` and are linked from documents. A Markdown
file over 100 KB must be justified.
*Check:* no `.json` under `docs/`; no unjustified file over the threshold.

**D8 Language.** All documents are written in English. Chinese is allowed only
as corpus content inside documents (source feedback, quoted evidence, glossary
terms and aliases, model inputs and outputs).
*Check:* Chinese text appears only in corpus content.

**D9 Update triggers.** A CLI behavior or option change updates `guides`; an
interface change updates `design`; a trade-off adds an ADR; a finished
experiment or validation adds a `records` entry; a layout change updates the
README "Layout" section.
*Check:* reviewed manually as part of G10.

---

## 3. Data rules (P1)

- `data/raw/` holds collected source data, read-only and never overwritten. One
  directory per dataset, named `YYYYMMDD-slug`, with a `manifest.json` (source,
  record count, hashes, producing script, consumers).
- `data/processed/` holds only reproducible data, with its generating command
  recorded. Annotation sets in `data/evaluation/` carry `-vN`, are frozen once
  published, and are corrected only by separate errata files.
- Runtime state (lock files, HTTP/rate-limit state) is not stored under `data/`.

## 4. Run output and retention rules (P2)

- All run output goes to `runs/` by default (ignored, safe to empty).
- `reports/` holds only curated results cited by documents. Each subdirectory
  has a `manifest.json` naming its record document, dataset, code version and
  reason for retention. Full run contents are kept in the external archive
  (`~/Archives/AIMediator/`); the project keeps the manifest and a curated
  summary.
- Backups, interrupted runs and checkpoints are never stored in the project.
- Code snapshots are allowed only in a `provenance/` subdirectory and are listed
  in the manifest.
- `dist/` holds only the current wheel and sdist; packaging the whole workspace
  is forbidden.

## 5. Code and script rules (P3)

- `src/aimediator/` is the only implementation. `scripts/` contains thin entry
  points that call the package.
- Scripts are grouped by purpose in `scripts/collect/`, `scripts/experiments/`
  and `scripts/maintenance/`.
- No `test_` prefix in `scripts/`.
- One-off scripts bound to a single run are archived or deleted after that run.
- Compatibility forwarding scripts are listed in the G2 register with a removal
  condition.

## 6. Test and verification rules (P4)

- `tests/` holds offline automated tests only. Tests needing live services
  (Ollama and similar) are stored separately, marked, and excluded from the
  default suite.
- Every reorganization step keeps the suite passing with at least the recorded
  baseline count (192 on 2026-11-03; a baseline change is recorded with its
  reason in a change record).
- Tests do not depend on historical run results under `reports/`.

## 7. Version control and backup rules (P5)

- Baseline commit: `0d390c4` (2026-11-03), taken before reorganization.
- `.gitignore` follows G4. Large data and retained results are not committed;
  they are backed up to `~/Archives/AIMediator/` with a checksum list
  (`SHA256SUMS`).
- Commit messages: `type: summary`, where type is one of `feat`, `fix`, `docs`,
  `refactor`, `chore`, `data`.

## 8. AI agent rules (P6)

- The root has a `CLAUDE.md` (and optionally `AGENTS.md`) that references this
  file and lists common commands, adding no rules of its own.
- Agent output is written to `runs/` or to a location these rules assign.
- Handoff prompts for agents are not kept as living documents once the task is
  done: useful content merges into `design`, the rest moves to `docs/archive/`.
- Empty tool directories (`.agents/`, `.codex/`, `.aws/`) are removed unless a
  reason for keeping them is recorded.
- **Agents do not sign their work**: no `Co-Authored-By` trailers, "Generated
  with" lines or agent bylines in commits, pull requests, documents or code.

## 9. Prompt and configuration rules (P7)

- `src/aimediator/assets/` is the only source for prompts and policy
  configuration.
- Root `prompts/` and `configs/` keep only collection configuration and the
  compatibility links listed in the G2 register.
- Legacy prompts (such as `extract-feedback.txt`) are archived once confirmed
  unreferenced.
- A prompt change is a behavior change and is documented in a record or ADR.

---

## Revision log

- 2026-11-03 v1.0 — First approved version. Decisions taken in review: English
  documentation with corpus exception (D8); single root `RULES.md` (location);
  full reports archived outside the project (P2); compatibility layers are
  registered only and not removed in the reorganization; `cli-demo/` is
  removed and will be rebuilt later; git baseline committed before
  reorganization (P5); agents do not sign their work (P6). Clarifications
  added with this version: `RULES.md` added to the G3 allowlist; register
  location (G2) and change record location (G6) fixed; P5 restated as a
  standing rule now that the baseline exists.
- 2026-11-03 v1.1 — Owner decisions on the batch 1 deferred items
  (reorganization plan, section 7, decisions 8 and 12). G3: `prompts/` is
  allowed for registered compatibility links only, because P7 keeps those
  links there and v1.0 did not list the directory. D2: scope limited to
  documents under `docs/`, with the listed exemptions, because those files
  already carry their own identification or belong to manifests.
- 2026-11-03 v1.2 — Owner decision in the batch 4 review (reorganization
  plan, section 7, decision 33; change record P4-D11 with P3-D08). G3:
  `.claude/` is allowed as ignored local agent state, because the
  coding-agent harness recreates it in every session and a blocking
  pre-commit hook would otherwise refuse every commit made from a session.
  It is listed in `.gitignore`.
- 2026-11-03 — Reorganization complete. All four batches of the
  reorganization plan are done (plan archived as
  `docs/archive/reorganization.md`; change record
  `docs/records/20261103-reorganization.md`, frozen). The rule check reports
  0 violations and the pre-commit hook now blocks commits with violations
  (G10). No rule changed; the version stays 1.2.
