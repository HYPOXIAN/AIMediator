# Documentation index

- Type: Reference (index)
- Status: Active
- Updated: 2026-11-03
- Applies to: every document under `docs/` (RULES.md D4)

Every document under `docs/` is listed once, grouped by the categories of
RULES.md D1. Records, decisions and meeting notes are frozen once final
(D3); living documents follow the implementation. The project rules are in
[RULES.md](../RULES.md); the entry point is the root [README](../README.md).

## Guides

| Document | Type | Status | Description |
| -------- | ---- | ------ | ----------- |
| [cli-usage.md](guides/cli-usage.md) | Guide | Active | Install the `aimediator` CLI and operate it: offline workflow, configuration, live analysis, recovery, review, reports and evaluation. |

## Design

| Document | Type | Status | Description |
| -------- | ---- | ------ | ----------- |
| [cli.md](design/cli.md) | Design | Active | CLI specification: product invariants, command contract, package architecture, configuration, run persistence, coverage and report contracts. |
| [balance-analysis.md](design/balance-analysis.md) | Design | Active | Bilingual evidence-grounded balance pipeline: prompts and routing, admission, extraction, source checks, report files and source review. |
| [evidence-quality.md](design/evidence-quality.md) | Design | Active | Pre-implementation specification of the evidence-quality module: segment annotation, emotion ratio, routing, integration, tests and evaluation targets. |
| [emotion-quantification-and-evidence-isolation.md](design/emotion-quantification-and-evidence-isolation.md) | Design | Active | Short description of the implemented evidence-quality module: flow, segment labels, emotion ratio and evidence routes. |

## Decisions

| Document | Type | Status | Description |
| -------- | ---- | ------ | ----------- |
| [0001-package-as-single-runtime.md](decisions/0001-package-as-single-runtime.md) | Decision | Active | The `aimediator` package is the single runtime implementation; scripts import it. |

## Plans and status

| Document | Type | Status | Description |
| -------- | ---- | ------ | ----------- |
| [cli-implementation-status.md](plans/cli-implementation-status.md) | Plan (implementation status) | Active | CLI V1 milestones P0–P4, their verification and the validation still open. |
| [review-follow-ups.md](plans/review-follow-ups.md) | Plan (follow-up list) | Active | Senior review work log: decisions taken, delivery checklist and open external follow-ups. |
| [code-restructuring.md](plans/code-restructuring.md) | Plan | Active | Code optimization and restructuring: diagnosis, target module layout, behavior lock, batches B0–B7 and owner decisions (all adopted 2026-11-03). |
| [code-restructuring-blueprint.md](plans/code-restructuring-blueprint.md) | Plan (blueprint) | Active | Engineering blueprint of the code restructuring: approved scope, metrics, interface contracts, standards, roles and responsibilities, session protocol, quality system, milestones. |
| [b0-safety-net.md](plans/code-restructuring-handoffs/b0-safety-net.md) | Agent handoff | Active | Work order B0: change record, working-directory fix, behavior lock, baseline measurements. |
| [b1-defects-and-hot-spots.md](plans/code-restructuring-handoffs/b1-defects-and-hot-spots.md) | Agent handoff | Active | Work order B1: glossary cache, defect fixes, console-text test, archives; owner review. |
| [b2-engine-split.md](plans/code-restructuring-handoffs/b2-engine-split.md) | Agent handoff | Active | Work order B2: injection seams, then pure moves out of `engine.py`, layering test. |
| [b3-callers-and-tests.md](plans/code-restructuring-handoffs/b3-callers-and-tests.md) | Agent handoff | Active | Work order B3: callers, tests and experiment scripts import the new modules; facade removed. |
| [b4-layer-removal-and-docs.md](plans/code-restructuring-handoffs/b4-layer-removal-and-docs.md) | Agent handoff | Active | Work order B4: forwarders and symlinks removed, documents updated, `RULES.md` v1.3, ADR 0002; owner review. |
| [b5-internals-and-performance.md](plans/code-restructuring-handoffs/b5-internals-and-performance.md) | Agent handoff | Active | Work order B5: helper unification, stage split, callbacks, incremental run state, legacy code snapshots. |
| [b6-research-code.md](plans/code-restructuring-handoffs/b6-research-code.md) | Agent handoff | Active | Work order B6: workspace root, collection subpackage, shared research helpers. |
| [b7-readability-and-acceptance.md](plans/code-restructuring-handoffs/b7-readability-and-acceptance.md) | Agent handoff | Active | Work order B7: style normalization, documents, `RULES.md` v1.4, final acceptance and archiving. |

## Records

| Document | Type | Status | Description |
| -------- | ---- | ------ | ----------- |
| [20261022-alias-review.md](records/20261022-alias-review.md) | Record | Active | Conclusion of the glossary alias reviews (2026-10-08 and 2026-10-22); the review dumps are archived. |
| [20261022-balance-review-v2.md](records/20261022-balance-review-v2.md) | Record | Active | Balance review and evaluation v2 and the v2.2 targeted extraction follow-up. |
| [20261026-evidence-quality-implementation.md](records/20261026-evidence-quality-implementation.md) | Record | Active | Implementation and verification of the evidence-quality module v1. |
| [20261027-screening-audit.md](records/20261027-screening-audit.md) | Record | Active | Audit of the existing screening mechanism on all 321 retained records (agent silver), translated from the report summary. |
| [20261027-balanced-validation.md](records/20261027-balanced-validation.md) | Record | Active | Fresh balanced 600-comment validation: collection, full run, controls and known limitations. |
| [20261028-directory-cleanup.md](records/20261028-directory-cleanup.md) | Record | Active | The 2026-10-28 cleanup: deleted paths, retained dependencies and validation. |
| [20261103-reorganization.md](records/20261103-reorganization.md) | Record | Active | Change record of the 2026-11 reorganization, batch by batch, with decisions, archives and results. |
| [20261103-dead-file-cleanup.md](records/20261103-dead-file-cleanup.md) | Record | Active | Workspace review for dead files after the reorganization: findings, the archived `runs/` output and what was kept. |
| [20261103-code-restructuring.md](records/20261103-code-restructuring.md) | Record | Active | Change record of the code restructuring: decisions, progress, session log, verification notes and archives. |

## Reference

| Document | Type | Status | Description |
| -------- | ---- | ------ | ----------- |
| [compatibility-layers.md](reference/compatibility-layers.md) | Reference | Active | Register of compatibility symlinks and forwarding scripts with their removal conditions (RULES.md G2). |
| [glossary.md](reference/glossary.md) | Reference | Active | Street Fighter 6 bilingual glossary: provenance, integration rules and all entries with aliases. |
| [glossary-vector-index.md](reference/glossary-vector-index.md) | Reference | Active | Glossary vector index: configuration, build and search commands, storage layout. |

## Meetings

| Document | Type | Status | Description |
| -------- | ---- | ------ | ----------- |
| [20261022-work-summary.md](meetings/20261022-work-summary.md) | Meeting | Active | Work summary of 2026-10-22: done and to-do items. |

## Archive

| Document | Type | Status | Description |
| -------- | ---- | ------ | ----------- |
| [next-development-plan.md](archive/next-development-plan.md) | Plan | Archived | Development plan of 2026-10-23, outdated. |
| [cli-coding-agent-prompt.md](archive/cli-coding-agent-prompt.md) | Agent handoff | Archived | Handoff prompt for the completed CLI implementation task. |
| [evidence-quality-coding-agent-prompt.md](archive/evidence-quality-coding-agent-prompt.md) | Agent handoff | Archived | Handoff prompt for the completed evidence-quality implementation task. |
| [reorganization.md](archive/reorganization.md) | Plan | Archived | The 2026-11 project cleanup and reorganization plan, its batches and decisions; completed. |
| [readme-research-history.md](archive/readme-research-history.md) | Entry (excerpt of the root README) | Archived | Research-history sections removed from the root README in 2026-11. |
