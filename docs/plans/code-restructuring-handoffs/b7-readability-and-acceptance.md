# Handoff B7: Readability and final acceptance

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-03
- Applies to: [code restructuring plan](../code-restructuring.md) batch B7; entry tag `restructure-b6`

Work order for batch B7. The steps are defined in plan section 7 (B7). The
document lifecycle is in [blueprint](../code-restructuring-blueprint.md)
section 9, and the review closure in section 6.4.

## 1. Mission

- Normalize the code style without changing any AST (CR-D11).
- Add docstrings and type hints to the core modules.
- Make the documents describe the code as it now is.
- Raise the P4 floor (`RULES.md` v1.4).
- Run the final acceptance, and after the owner's final review, archive the
  planning documents and freeze the change record.

## 2. Entry conditions

- Tag `restructure-b6` exists, and the B6-V note says "accepted".
- Clean tree, no `WIP Step` stash. The gates pass.

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/|scripts/|README\.md$|RULES\.md$|CLAUDE\.md$|docs/)
```

- **Allowed**:
  - formatting in `src/` and `scripts/` (B7.1);
  - docstrings and type hints in `src/` (B7.2);
  - living documents, the register, the index, `RULES.md` and `CLAUDE.md`;
  - moving the planning documents to `docs/archive/` (closure).
- **Not allowed**:
  - `tests/` (CR-D11), including the lock fixture;
  - any AST change in B7.1;
  - any behavior change;
  - frozen records other than the change record.
- **Decisions in force**:
  - CR-D10: the v1.4 wording below;
  - CR-D11: the style scope is `src/` and `scripts/`.
- **Owner actions**: the final review after B7-V, including the v1.4
  wording.

## 4. Sessions

### B7-1 (implementation): steps B7.1 and B7.2

### B7-2 (implementation): steps B7.3, B7.4 and B7.5 item 1

Both sessions use this prompt, with their own session ID and step range:

```text
You are session B7-<k> (implementation) of the AIMediator code restructuring,
steps <first> to <last>.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/code-restructuring-handoffs/b7-readability-and-acceptance.md);
the blueprint docs/plans/code-restructuring-blueprint.md, sections 2, 3, 4,
5, 6 and 9; the plan docs/plans/code-restructuring.md, sections 1, 8, 12 and
the B7 part of section 7; the change record.
Task: execute your steps in order, inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates after every commit.
- One kind of operation per commit, with "Step: B7.x" and the decision ID
  in the body. B7.1 is a series of commits.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

AST equivalence check for B7.1. Save this script to a temporary file and run
it as `python3 <file> HEAD <changed .py files>` before each commit. Every
line must read `same`.

```python
import ast, subprocess, sys
base = sys.argv[1]
for name in sys.argv[2:]:
    old = subprocess.run(['git', 'show', base + ':' + name], check=True,
                         capture_output=True, text=True).stdout
    with open(name, encoding='utf-8') as handle:
        new = handle.read()
    print('same' if ast.dump(ast.parse(old)) == ast.dump(ast.parse(new)) else 'CHANGED', name)
```

Step notes:

- **B7.1** One statement per line. No semicolon joins and no one-line `if`,
  `for` or `def` bodies. Strings, docstrings and comments stay as they are.
  - No formatter is installed, so edit by hand or with a small throwaway
    script; never install one.
  - Commit groups:
    1. dense package modules (`cli.py`, `quality_scoring.py`, and any other
       module the check below finds);
    2. `scripts/experiments/`;
    3. `scripts/collect/`;
    4. `scripts/maintenance/verify_cli_install.py`.
  - To find candidates, list lines with `;` outside strings, for example
    `git grep -nE ";[^'\"]*$" -- src scripts`, and inspect each hit.
- **B7.2** Add `from __future__ import annotations` after the module
  docstring, then hints and one-line docstrings for the public functions of
  `common`, `resources`, `schema`, `evidence`, `stages`, `runner`,
  `retrieval`, `pipeline` and `run_store`.
  - Annotations change the AST, so check with the lock and the full suite
    instead of the AST check.
  - No runtime typing imports beyond what Python 3.9 supports.
- **B7.3** In `docs/design/cli.md` section 5:
  - Replace the "Target structure" block with the actual layout.
  - Add a short contract summary per module, taken from blueprint section
    3.3. This is the P6 merge; keep only what still describes the code.
  - Add a dated paragraph on how the layout differs from the original
    target: preflight stayed in `operations`; `stages`, `runner`,
    `fixture_transport`, `collection`, `design_briefs` and `diagnostics`
    were added.
  - Also update:
    - `docs/plans/cli-implementation-status.md` ("Layout decisions");
    - the README "Layout", in which `scripts/` has no top-level files;
    - the register: one symlink, no forwarders, and a change-log line;
    - the index.
- **B7.4** `RULES.md` v1.4. Draft wording, which the owner confirms at the
  final review:
  - Version line: `Version 1.4 · Effective <YYYY-MM-DD> · Approved by the project owner.`
  - P4, second bullet: replace "(192 on 2026-11-03;" with
    "(<N> on <YYYY-MM-DD>;", where N is the test count after B7.2. Keep the
    words "baseline count (" exactly, because `check_rules.py` reads the
    number with the pattern `baseline count \((\d+) on`.
  - Revision log: "<date> v1.4 — Owner decision CR-D10 of the code
    restructuring plan. P4: the test floor rises from 192 to <N>, the count
    at the end of the code restructuring, so later work cannot drop tests
    silently."
  - `CLAUDE.md`: "Applies to: `RULES.md` v1.4".
  - Afterwards, the rule check reports 0, with P4 reading the new number.
- **B7.5, item 1** Run every gate (plan 8.1), the wheel acceptance (8.2), the
  foreign directory check (8.5), the timings (8.4), the greps (8.7) and the
  function-length metric (blueprint 7.3). Under "Batch results", record an
  "Acceptance" table that adds an "Achieved" column to the blueprint
  section 2 metrics.

### B7-V (verification)

```text
You are session B7-V (verification) of the AIMediator code restructuring.
You did not implement batch B7. Change nothing except the change record.
Read: RULES.md; this work order; the blueprint, sections 2, 5, 6.4, 6.6, 7
and 9; the plan, sections 8 and 12; the change record.
Task: run every item of the B7-V checklist in this work order on HEAD, and
append a verification note committed with "Session: B7-V". If every item
passes, tag that commit restructure-b7-review and list the owner review
items from section 5 of this work order. Otherwise record the findings as
fix-up steps B7.F1 and so on, and stop without tagging.
Never add attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary check from `restructure-b6`, and commit hygiene.
2. Every B7.1 commit is AST-equivalent: rerun the check for each commit
   against its parent.
3. Plan section 12, criteria 1 to 9. Criterion 10 follows at closure.
4. The test count equals the number in `RULES.md` v1.4. The lock fixture is
   unchanged since B5.11.
5. The documents match the code: compare `docs/design/cli.md` section 5 with
   `ls src/aimediator` and `tests/test_module_layers.py`.

### B7-3 (closure): plan step B7.5, items 2 and 3, after the owner's final review

```text
You are session B7-3 (closure) of the AIMediator code restructuring. The owner
has given the final review; their outcome is in your instructions.
Read: RULES.md; this work order; the blueprint, sections 6.4 and 9; the plan,
sections 7 (B7.5) and 12; the change record.
Task:
1. Record the review outcome. If the owner rejected items, stop after
   turning them into fix-up steps.
2. Otherwise move the planning documents to the archive and finalize the
   change record, as this work order describes.
3. Pass every gate, then tag restructure-done.
Never add attribution. Your final message repeats your session-log entry.
```

Closure sequence (one kind of operation per commit):

1. `docs: record the owner's final review`, with `Session: B7-3`.
2. Move the planning documents with `git mv`:
   - `docs/plans/code-restructuring.md` and
     `docs/plans/code-restructuring-blueprint.md` go to `docs/archive/`;
   - `docs/plans/code-restructuring-handoffs/` goes to
     `docs/archive/code-restructuring-handoffs/`.
3. In each moved file, set Status Archived and add the header line
   "Archived <date> when the code restructuring was completed (tag
   `restructure-done`)."
4. Fix every link the rule check reports (D5). For example, the plan's link
   `cli-implementation-status.md` becomes `../plans/cli-implementation-status.md`.
5. Fix every inbound reference found with
   `git grep -n "code-restructuring" -- . ':!docs/archive'`. Move the index
   rows to the Archive table (D4).
6. Finalize the change record: add a closing summary and the header line
   "Final <date> (tag `restructure-done`); frozen from then on (D3)."
7. Run the gates and the rule check (0), then tag `restructure-done`.

## 5. Owner review items (set by B7-V)

- The `RULES.md` v1.4 wording, and the final test floor.
- The acceptance table: each metric of blueprint section 2 against its
  target, especially the suite time.
- `docs/design/cli.md` section 5 and the README "Layout".
- Any deferred items and escalations.

## 6. Escalation triggers

- A B7.1 edit cannot stay AST-equivalent.
- A documented contract no longer matches the code, and fixing it would
  change code.
- A plan section 12 criterion fails and cannot be met inside the B7
  boundary.
