# Code Restructuring Change Record

- Type: Record
- Status: Active
- Updated: 2026-11-03
- Applies to: commit `7282f49` and later; `RULES.md` v1.2 and later amendments

The single change record of the code restructuring
([plan](../plans/code-restructuring.md)). Every step adds its row to the
progress table in its own commit. Deletions are entered under "Archive and
deletions" (G6). Frozen when the plan is finished (D3).

## Owner decisions

| ID | Answer | Date | Notes |
| -- | ------ | ---- | ----- |
| CR-D01 | adopt | 2026-11-03 | plan section 9 |
| CR-D02 | adopt | 2026-11-03 | plan section 9 |
| CR-D03 | adopt | 2026-11-03 | plan section 9 |
| CR-D04 | adopt | 2026-11-03 | plan section 9 |
| CR-D05 | adopt | 2026-11-03 | plan section 9 |
| CR-D06 | adopt | 2026-11-03 | plan section 9; includes confirmation that no experiment output must be resumed under its old identity |
| CR-D07 | adopt | 2026-11-03 | plan section 9 |
| CR-D08 | adopt | 2026-11-03 | plan section 9 |
| CR-D09 | adopt | 2026-11-03 | plan section 9 |
| CR-D10 | adopt | 2026-11-03 | plan section 9 |
| CR-D11 | adopt | 2026-11-03 | plan section 9 |
| CR-D12 | adopt | 2026-11-03 | plan section 9 |

## Progress

The commit of a step is found with `git log --grep 'Step: <ID>'`.

| Step | Status | Tests | Lock | Notes |
| ---- | ------ | ----- | ---- | ----- |
| B0.1 | done | 222 | — | Change record opened; index row added. The lock does not exist before B0.3 |
| B0.2 | done | 222 | — | F-04 fixed: the test reads the prompt through `asset_path`. Plan 8.5 from a foreign directory: 222 pass, no error |

## Baseline measurements (B0.4)

## Behavior lock (B0.3): volatile keys, exclusions, self-test results

## Archive and deletions

| Path | Archive location | SHA256SUMS entry | Reason | Step |
| ---- | ---------------- | ---------------- | ------ | ---- |

## Decisions found during execution

## Escalations

## Verification notes

## Session log

## Batch results

## Deferred
