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
