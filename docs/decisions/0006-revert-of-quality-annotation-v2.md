# 0006 Revert of quality annotation v2 in the pipeline

- Type: Decision
- Status: Active
- Updated: 2026-11-05
- Applies to: `aimediator` 0.1.0 from pipeline upgrade fix-up steps U4.F2 to U4.F5; schema `evidence-quality-v1`, `evidence-quality-policy.json` v1; supersedes the pipeline decisions of [ADR 0005](0005-program-segmentation-of-quality-annotations.md); `RULES.md` v1.4
- Escalation E-4 of the
  [change record](../records/20261104-pipeline-upgrade.md) of the
  [pipeline upgrade plan](../archive/pipeline-upgrade.md), adopted under the
  owner's standing instruction and the owner authorization of
  2026-11-05 03:11; written by step U7.3 for the deferred item "ADR 0005
  after the E-4 reverts".

## Context

[ADR 0005](0005-program-segmentation-of-quality-annotations.md) recorded
five decisions of batch U4 (owner decision UP-D10): program clause
segments (`clause-v1`, U4.1), a v2 schema builder, conversion and
validation (U4.3), v2 quality requests from the pipeline (U4.4), readers
of both record versions (U4.5), and the measurements of U4-L. Under the
adoption rule of plan 5.4, U4.4 and U4.5 failed rules 2 and 3 on the
`latency-benchmark` sample through the hosted API: 4 quality-failed
comments against 2 in the U2-L1 reference (margin 1), first-attempt
validity 18/23 against 21/24. The synthetic sample improved (validity
16/16, route agreement 14/16 against 11/16) and the quality time per
comment fell to about 60 % of the reference. Escalation E-4 adopted a
fix-up prompt step (U4.F1) with a revert as its fallback; its rerun
(U4-L2) still gave 5 quality-failed benchmark comments against 2, so the
fallback applied.

ADR 0005 is a frozen decision (D3): only its status may change, so it
cannot say itself that its pipeline decisions were reverted.

## Decision

1. The pipeline sends evidence-quality v1 requests again: fix-up step
   U4.F2 reverted U4.F1, U4.F3 reverted U4.5 (the readers of both versions)
   and U4.F4 reverted U4.4 (the v2 request), each with `git revert` and
   its lock update. Quality records are `evidence-quality-v1`; the
   model writes segment offsets and quotes as before U4.
2. The behavior-neutral code of U4.1 to U4.3 stays in the package, unused
   by the pipeline: `evidence.clause_segments` (`clause-v1`) and the v2
   schema builder, conversion and validation of `evidence_quality`. Its
   tests stay. A later decision may use it again; it has to pass the
   adoption rule on its own.
3. The design documents keep their description of the v2 contract with a
   sentence that it is not in effect (U4.F5): evidence-quality.md section
   3.3, the emotion design note, design/cli.md section 5.
4. ADR 0005 is superseded by this record. Its context, measurements and
   the decisions on U4.1 to U4.3 stay readable there.

## Consequences

- The quality request keeps the U2.2 view (UP-D04) and its token savings;
  the T4 and T5 gains measured with v2 do not apply. T5 (first-attempt
  validity at least 95 %) is not met by the adopted configuration; the
  values are in the [validation record](../records/20261105-pipeline-upgrade-validation.md).
- The legacy runner's quality identity again matches the v1 requests it
  sends, so the deferred item on its schema hash (D-11, part 3) no longer
  applies.
- Runs written between U4.4 and U4.F4 hold `evidence-quality-v2` records.
  The v1 readers validate the derived `annotation` of those records with
  the v1 rules, as they did at the U4.4 commit; they no longer check the
  v2 fields (U4.F3). Those runs were live evaluation runs under `runs/`.
