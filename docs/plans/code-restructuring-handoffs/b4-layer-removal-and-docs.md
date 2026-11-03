# Handoff B4: Remove the compatibility layers; documentation

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-03
- Applies to: [code restructuring plan](../code-restructuring.md) batch B4; entry tag `restructure-b3`

Work order for batch B4. The steps are defined in plan section 7 (B4).
Roles and the review protocol are in the
[blueprint](../code-restructuring-blueprint.md), sections 5 and 6.4.

## 1. Mission

- Living documents switch to the package commands and to asset paths.
- The six pure forwarders and 18 of the 19 symlinks are deleted, and the
  register is updated to match.
- `RULES.md` becomes v1.3, with the rule check following.
- ADR 0002 records the module boundaries.

The batch ends at an owner review point, where the owner also confirms the
v1.3 wording.

## 2. Entry conditions

- Tag `restructure-b3` exists, and the B3-V note says "accepted".
- Clean tree, no `WIP Step` stash. The gates pass.
- Plan 8.7, first and second greps, print nothing: no forwarder is imported
  any more.

## 3. Responsibility boundary

Allowed paths:

```text
^(scripts/[a-z_]+\.py$|prompts/|configs/(balance-review-policy|evidence-quality-policy|local-language-routing)\.json$|data/glossary\.json$|README\.md$|RULES\.md$|CLAUDE\.md$|docs/(guides|design|reference|decisions)/|docs/README\.md$|scripts/maintenance/check_rules\.py$|tests/test_(check_rules|refactored_boundaries)\.py$|docs/records/[0-9]{8}-code-restructuring\.md$)
```

- **Allowed**:
  - deleting the six forwarders at the top of `scripts/` and the 18
    symlinks;
  - living documents, the register and ADR 0002;
  - `RULES.md` and the version reference in `CLAUDE.md`;
  - the G3 allowlist in `check_rules.py` and its test;
  - deleting one test method in `test_refactored_boundaries.py`.
- **Not allowed**:
  - code under `src/`;
  - frozen records, decisions 0001 and older, meeting notes and the archive
    (CR-D07 keeps their historical paths);
  - the symlink `data/evaluation/evidence-quality-synthetic-v1/cases.json`
    (CR-D08);
  - `configs/` collection settings.
- **Decisions in force**:
  - CR-D05: the forwarders go, and commands use `python3 -m`;
  - CR-D07: the R1 reading, and the deletions;
  - CR-D08: keep `cases.json`;
  - CR-D10 and CR-D02: the v1.3 wording below.
- **Owner actions**: the review after B4-V, including confirmation of the
  v1.3 wording.

## 4. Sessions

### B4-1 (implementation): steps B4.1 to B4.5

```text
You are session B4-1 (implementation) of the AIMediator code restructuring.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/code-restructuring-handoffs/b4-layer-removal-and-docs.md); the
blueprint docs/plans/code-restructuring-blueprint.md, sections 1, 4.4, 5 and
6; the plan docs/plans/code-restructuring.md, sections 1, 4.3, 4.4, 8.7, 9
and the B4 part of section 7; the compatibility register; the change record.
Task: execute steps B4.1 to B4.5 as this work order describes, inside its
boundary.
Rules:
- Start with the plan's resume procedure. Run the gates after every step.
- One kind of operation per commit, with "Step: B4.x" and the decision IDs
  in the body. B4.4 is two commits.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **B4.1** Commands become `python3 -m aimediator.engine`,
  `aimediator.legacy_review`, `aimediator.quality_scoring` and
  `aimediator.glossary_vectors`. State once per document that these need
  `pip install -e .` or `PYTHONPATH=src`. Files:
  - `README.md`: rename the section "Research and compatibility commands"
    to "Research commands".
  - `docs/guides/cli-usage.md`: line 182, and the paragraph "Compatibility
    and validation scope".
  - `docs/design/balance-analysis.md`: lines 6, 8, 29 and 168, plus the
    prompt and policy paths, which become `src/aimediator/assets/...`.
  - `docs/design/cli.md`: section 2, lines 75 to 87. That section describes
    the dated starting point, so keep its sentences and add dated notes.
  - `docs/design/evidence-quality.md`: lines 33, 42 and 47. It is a
    pre-implementation specification, so add dated notes.
  - `docs/reference/glossary-vector-index.md`: lines 28 and 29.

  The link check (D5) must stay at 0.
- **B4.2** In one commit:
  - `git rm` the six forwarders: `run_balance_analysis.py`,
    `review_balance_sources.py`, `evaluate_evidence_quality.py`,
    `glossary_vectors.py`, `evidence_quality.py` and `balance_policy.py`;
  - remove their register rows and add a change-log line;
  - delete `test_compatibility_imports_share_package_state` (−1 test;
    record the reason).

  G2 and P3 must report 0. Afterwards
  `git grep -nE "scripts/(run_balance_analysis|review_balance_sources|evaluate_evidence_quality|glossary_vectors|evidence_quality|balance_policy)\.py" -- src scripts tests README.md docs/guides docs/design docs/reference`
  must print nothing.
- **B4.3** In one commit:
  - `git rm` the 14 files under `prompts/`, the three policy and routing
    links in `configs/`, and `data/glossary.json`;
  - in the register:
    - remove those 18 rows;
    - set the removal condition of the `cases.json` row to "kept (CR-D08):
      member of the frozen evaluation set `evidence-quality-synthetic-v1`";
    - add the CR-D07 reading of R1 to the "Removal conditions" section;
    - add a change-log line;
  - in the README "Layout":
    - remove the `prompts/` line;
    - describe `configs/` as "Collection settings";
    - rewrite the bullet about compatibility links: the packaged assets are
      the only copy, and one evaluation-set link remains;
  - in `docs/guides/cli-usage.md`, remove the sentence saying the original
    checkout paths are symlinks.

  Plan 8.7, third grep, may then match only the planning documents.
- **B4.4, first commit** (`docs`): `RULES.md` v1.3. Draft wording, which the
  owner confirms at review:
  - Version line: `Version 1.3 · Effective <YYYY-MM-DD> · Approved by the project owner.`
  - G3: delete the sentence that begins "`prompts/` is also allowed".
  - P3: add the bullet "Experiment scripts in `scripts/experiments/` may keep
    experiment-specific orchestration, case lists and output formatting;
    logic that two or more scripts or the tests use lives in the package."
  - P7, second bullet: "Root `configs/` keeps only collection
    configuration." This is a consequence of B4.3; name it in the review
    list.
  - Revision log: "<date> v1.3 — Owner decisions CR-D02, CR-D07 and CR-D10
    of the code restructuring plan. G3: `prompts/` removed from the
    allowlist; the directory is empty since step B4.3 removed the last
    compatibility links. P3: states what experiment scripts may keep. P7:
    root `configs/` no longer holds compatibility links."
  - `CLAUDE.md`: "Applies to: `RULES.md` v1.3" and the Updated date.
- **B4.4, second commit** (`chore`):
  - remove `'prompts'` and its two comment lines from `G3_ALLOWED` in
    `check_rules.py`;
  - in `tests/test_check_rules.py`,
    `test_g3_flags_entries_outside_allowlist` now expects
    `['notes', 'prompts', 'stray.txt']`;
  - the G2 test still uses a `prompts` directory inside its temporary root.
    That is fine, because the test checks G2 only.

  Run the rule check (0) and the tests.
- **B4.5** `docs/decisions/0002-module-boundaries-and-entry-points.md` with
  the D2 header (Type Decision, Status Active).
  - Context: the `engine` hub, the patch seams, the compatibility layers.
  - Decision: the module table and dependency rules (plan sections 4.1 and
    4.2) enforced by `tests/test_module_layers.py`; research commands as
    `python3 -m`; the layers removed.
  - Consequences: run identities, the editable-install requirement, and
    historical paths in frozen documents.
  - Add an index row under Decisions.

### B4-V (verification)

```text
You are session B4-V (verification) of the AIMediator code restructuring.
You did not implement batch B4. Change nothing except the change record.
Read: RULES.md; this work order; the blueprint, sections 4.4, 5, 6.4, 6.6 and
7; the plan, sections 4.3, 8 and the B4 part of section 7; the register; the
change record.
Task: run every item of the B4-V checklist in this work order on HEAD, and
append a verification note committed with "Session: B4-V". If every item
passes, tag that commit restructure-b4-review and list the owner review
items from section 5 of this work order. Otherwise record the findings as
fix-up steps B4.F1 and so on, and stop without tagging.
Never add attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary check from `restructure-b3`, and commit hygiene.
2. `ls -A` at the root shows no `prompts/`. `scripts/` has no file at its
   top level. `git ls-files -s | awk '$1=="120000"'` lists exactly one
   symlink.
3. The register matches the tree (G2 0). The README "Layout" matches the
   tree (G10). Links resolve (D5 0).
4. Plan 8.7, third grep, matches only the planning documents.
5. `RULES.md` reads "Version 1.3" with a revision-log entry. `CLAUDE.md`
   names v1.3. `check_rules.py` no longer allows `prompts`.
6. Gates (one test fewer than B3), lock unchanged, wheel acceptance and the
   foreign directory check.

## 5. Exit, owner review and handoff out

- B4-V sets `restructure-b4-review`.
- Owner review items:
  - the v1.3 wording (G3, P3, and the P7 consequence);
  - ADR 0002;
  - the document changes of B4.1 and B4.3;
  - the register.
- After the review, a closure session records the outcome. A wording change
  becomes a fix-up step. The closure session then sets `restructure-b4`.
- The next work order is [B5](b5-internals-and-performance.md).

## 6. Escalation triggers

- A documented command cannot be expressed as `python3 -m aimediator.<module>`.
- A deleted path is still used outside the planning documents.
- The amendment needs wording beyond the draft (for example, another rule
  mentions `prompts/`).
