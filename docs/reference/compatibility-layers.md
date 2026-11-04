# Compatibility Layer Register

- Type: Reference
- Status: Active
- Updated: 2026-11-04
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
forwarding scripts. The plan expected 6 forwarding scripts; the seventh, the
wrapper for the historical 32-comment direction comparison, had its own
arguments rather than being a pure forwarder. It was archived in code
restructuring step B1.7 (see the change log).

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
  any more. Reading (owner decision CR-D07 of the code restructuring): R1
  counts code, tests, configuration and living documents only. Frozen
  records and the archive keep their historical paths (D3).
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
| `data/evaluation/evidence-quality-synthetic-v1/cases.json` | `../../../src/aimediator/assets/fixtures/cases.json` | tests: `test_evaluation_sets.py` checks it against `cases_sha256` in the set's `manifest.json`; docs: `README.md` ("Layout"), `decisions/0002-module-boundaries-and-entry-points.md`, `records/20261026-evidence-quality-implementation.md` | kept (CR-D08): member of the frozen evaluation set `evidence-quality-synthetic-v1` |

## Symlinks to packaged prompts

None since code restructuring step B4.3 (see the change log). The prompts
exist only under `src/aimediator/assets/prompts/`.

## Forwarding scripts

None since code restructuring step B4.2 (see the change log). Research
commands are package modules run with `python3 -m aimediator.<module>`.

## Change log

- 2026-11-03: register created with 18 symlinks and 7 forwarding scripts.
- 2026-11-03 (batch 3): "Used by" updated: archived one-off and smoke-test
  scripts dropped, the four `test_*` scripts renamed to `run_*_live`, and
  the `cli-demo/` entry (removed in batch 2) dropped. No layer changed.
- 2026-11-03 (batch 3): added the symlink
  `data/evaluation/evidence-quality-synthetic-v1/cases.json`, which replaced a
  byte-identical copy of the packaged fixture (plan section 7, decision 9).
  The register now lists 19 symlinks and 7 forwarding scripts.
- 2026-11-03 (batch 3 review, P3-D01): the direction-comparison wrapper
  (archived since, see the B1.7 entry) writes to `runs/<run name>` instead
  of `reports/<run name>`, and its
  `--run-name` default is `local-direction-comparison` instead of the dated
  `balance-evidence-20261022` (G7). The layer stays registered under R3.
- 2026-11-03 (batch 4): "Used by" document paths updated for the moves into
  the D1 directories, the archived alias review dumps and the README
  slim-down (change record, P4). No layer changed.
- 2026-11-03 (code restructuring step B1.6, CR-D03): "Used by" updated:
  the four quality-screening one-off scripts of the 100-comment experiment
  and their two test files were archived to
  `~/Archives/AIMediator/scripts/20261103-quality-screening/` and dropped
  (names in the [code restructuring change record](../records/20261103-code-restructuring.md),
  "Archive and deletions"). No layer changed.
- 2026-11-03 (code restructuring step B1.7, CR-D04): the direction-comparison
  wrapper (R3) and the evidence-quality demo script were archived to
  `~/Archives/AIMediator/scripts/20261103-broken-entry-points/`; both had
  stopped working when the evidence-quality stage was added (names in the
  [code restructuring change record](../records/20261103-code-restructuring.md),
  "Archive and deletions"). The wrapper's row is removed, and both scripts
  are dropped from "Used by". The register now lists 19 symlinks and 6
  forwarding scripts; no layer uses R3 any more.
- 2026-11-04 (code restructuring step B4.2, CR-D05): the six pure
  forwarding scripts were archived to
  `~/Archives/AIMediator/scripts/20261104-forwarders/` and removed (names in
  the [code restructuring change record](../records/20261103-code-restructuring.md),
  "Archive and deletions"), and their rows are removed. R2 held for each:
  no test or script imports them since step B3.3 and B3.4, the documented
  commands are `python3 -m aimediator.engine`, `.legacy_review`,
  `.quality_scoring` and `.glossary_vectors` since step B4.1 (in the
  glossary index manifest since the owner's answer to escalation E-2), and
  no run identity hashes them since step B3.4. The register now lists 19
  symlinks and no forwarding script.
- 2026-11-04 (code restructuring step B4.3, CR-D07, CR-D08): the 14 prompt
  links in `prompts/`, the three policy and routing links in `configs/` and
  the glossary link in `data/` were removed, with their rows; `prompts/` no
  longer exists. R1 held for each under the CR-D07 reading (see "Removal
  conditions"): every code user reads the resource through `asset_path()`,
  and the living documents cite the `src/aimediator/assets/` paths since
  step B4.1. The link targets are archived in
  `~/Archives/AIMediator/scripts/20261104-compatibility-links/SYMLINKS.txt`.
  The `cases.json` link of the frozen evaluation set stays (CR-D08); its
  "Used by" cell drops `test_evidence_quality.py`, which reads the packaged
  fixture through `tests/support.py` since step B3.2. The register now lists
  1 symlink and no forwarding script.
- 2026-11-04 (code restructuring step B7.3): state at the end of the code
  restructuring, checked against the tree: 1 symlink, the `cases.json` link
  of the frozen evaluation set (CR-D08), and no forwarding script.
  `git ls-files -s` lists that one symlink, `scripts/` has no files at its
  top level, and no tracked script's docstring begins with "Compatibility
  entry point". The link's "Used by" cell adds `README.md` and ADR 0002,
  which name the path since steps B4.3 and B4.5. The restructuring's plan,
  blueprint and B4 work order also name it; they are not listed, because
  they move to `docs/archive/` when the restructuring closes. No layer
  changed.
