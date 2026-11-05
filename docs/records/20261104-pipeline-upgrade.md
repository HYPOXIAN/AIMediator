# Pipeline Upgrade Change Record

- Type: Record
- Status: Active
- Updated: 2026-11-04
- Applies to: the [pipeline upgrade plan](../plans/pipeline-upgrade.md); commit `31d00f8` (tag `upgrade-plan`) and later

The single change record of the pipeline upgrade. Every step adds its row to
the progress table in its own commit. Frozen when the plan is finished (D3).

## Owner decisions

| ID | Answer | Date | Notes |
| -- | ------ | ---- | ----- |
| UP-D01 | adopt | 2026-11-04 | plan section 9 |
| UP-D02 | adopt | 2026-11-04 | plan section 9 |
| UP-D03 | adopt | 2026-11-04 | plan section 9 |
| UP-D04 | adopt | 2026-11-04 | plan section 9 |
| UP-D05 | adopt | 2026-11-04 | plan section 9 |
| UP-D06 | trial under the adoption rule | 2026-11-04 | plan section 9; U2-L2 decides |
| UP-D07 | adopt | 2026-11-04 | plan section 9 |
| UP-D08 | adopt | 2026-11-04 | plan section 9 |
| UP-D09 | adopt | 2026-11-04 | plan section 9 |
| UP-D10 | pending | — | plan section 9: answered after U0.6 measures the failure classes (ALG-01) |
| UP-D11 | adopt, each step under the adoption rule | 2026-11-04 | plan section 9 |
| UP-D12 | adopt | 2026-11-04 | plan section 9 |
| UP-D13 | adopt after the offline comparison | 2026-11-04 | plan section 9 |
| UP-D14 | adopt | 2026-11-04 | plan section 9 |
| UP-D15 | trial, default off | 2026-11-04 | plan section 9 |
| UP-D16 | adopt | 2026-11-04 | plan section 9 |

## Progress

The commit of a step is found with `git log --grep 'Step: <ID>'`.

| Step | Class | Status | Tests | Lock | Notes |
| ---- | ----- | ------ | ----- | ---- | ----- |
| U0.1 | N | done | 241 | green | Change record opened from plan section 11; owner decisions copied (UP-D10 pending by its own terms); index row added |
| U0.2 | N | done | 250 | updated by UP-D01 | New module `aimediator.measurement` (`request_metrics`, `claim_outcomes`, `materialize`, `score_positions`; standard library, `common` and `quality_scoring.proportion` only) and the scripts `measure_run_requests.py` (writes both metrics and outcomes), `materialize_evaluation_input.py` and `score_extraction.py`. New `tests/test_measurement.py` (+9): synthetic runs with and without counters and both reuse formats, wall time, the three demo runs end to end (counters `None`), the three label formats, missing rows, hash mismatches, hand-computed precision and recall, the scripts. Layering row `measurement` → `common`, `quality_scoring`; design/cli.md section 5 layout and contract. Lock regenerated for exactly `L2:enforce/code-snapshot/measurement.py`, `L2:off/…` and `L2:shadow/…` (existence only); no other key differed. Beyond plan 5.2: fresh and reused statistics kept apart (reused archived responses keep their original counters with near-zero elapsed time); counts and sums beside the means; audit rejection share; extraction dispositions; quality attempt errors (IDs and key names only, no source text); `materialize` also checks `ids_sha256` or `labels_sha256` and `source_dataset_sha256` when the set's manifest records them. Nested text parts are counted without JSON quotes, which matches plan 0.2 (unit text 15.3 %, raw; 15.75 % with quotes). Decision found during execution D-1 |

## Baseline measurements (U0.4)

## Live environment and configuration (U0.6)

## Live evaluations

| Session | Commit | Set | Mode | Wall time | Prompt tokens by stage | Output tokens by stage | Failures | Claims generated / accepted | Precision / recall (dev) | Quality validity | Verdict |
| ------- | ------ | --- | ---- | --------- | ---------------------- | ---------------------- | -------- | --------------------------- | ------------------------ | ---------------- | ------- |

## Behavior changes (P7)

| Step | Decision | Asset or request part | Old SHA-256 | New SHA-256 | Lock paths |
| ---- | -------- | --------------------- | ----------- | ----------- | ---------- |

## Evaluation sets

## Archive and deletions

| Path | Archive location | SHA256SUMS entry | Reason | Step |
| ---- | ---------------- | ---------------- | ------ | ---- |

## Decisions found during execution

- **D-1 (U0.2) Output of `materialize_evaluation_input.py`.** The step note
  asks the scripts to write their output with `common.write`, which writes
  indented JSON. The materialized input must be JSONL holding the dataset
  rows unchanged, because `aimediator analyze --input` reads JSONL. Options:
  (a) the script writes the bytes from `materialize` through a synced
  temporary file and replaces the target, as `common.write` does; (b) add a
  JSONL writer to `common` (outside the U0 boundary); (c) write a JSON array
  (`analyze` cannot read it). Recommendation and action: (a). N-class, undone
  by a revert, no `RULES.md` change, nothing deleted. The two other scripts
  use `common.write`.

## Escalations

## Verification notes

## Session log

## Deferred
