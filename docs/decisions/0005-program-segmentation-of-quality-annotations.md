# 0005 Program segmentation of quality annotations

- Type: Decision
- Status: Superseded by [0006-revert-of-quality-annotation-v2.md](0006-revert-of-quality-annotation-v2.md)
- Updated: 2026-11-05
- Applies to: `aimediator` 0.1.0 from pipeline upgrade batch U4 (steps U4.1 to U4.5, measured by U4-L); `evidence-quality-policy-v2`, schema `evidence-quality-v2`, segmentation `clause-v1`; `RULES.md` v1.4
- Owner decision UP-D10 of the
  [pipeline upgrade plan](../archive/pipeline-upgrade.md) (section 4.2,
  ALG-01 and ALG-02); the execution and the live measurements are recorded
  in the [change record](../records/20261104-pipeline-upgrade.md) and in
  [`reports/20261105-upgrade-u4-evaluation/`](../../reports/20261105-upgrade-u4-evaluation/manifest.json).

## Context

Before batch U4 the evidence-quality annotation (schema
`evidence-quality-v1`) asked the model to cut every evidence unit into
segments itself and to write each segment's `start`, `end` and `quote`
next to its labels. The program then checked that the offsets were
integers inside the unit, that each quote equalled the original text at
its offsets, and that the segments covered every non-whitespace character
in order without overlap. Most failed attempts failed these checks rather
than a judgment about the comment: in the U2-L1 benchmark run (hosted
model) 21 of the 27 attempt errors were quote and offset mismatches or
overlapping spans. In the local U0.6 runs the most frequent class was a
point literal outside its selected spans, which program segmentation does
not remove by itself (UP-D10). The offsets and quotes also made up
most of the output the model had to decode, and decoding dominated the
quality stage's time.

The constraints were the routing rules of `evidence_quality.qualify`
(invariant 2.1.1), which must not change; the frozen fixture annotations
(`assets/fixtures/cases.json`) and evaluation sets, which are v1; and the
readers of stored runs (`review`, `report`, `evaluate`), which must keep
reading runs written by earlier code (invariant 2.1.9).

## Decision

1. **Program clause segments** (U4.1). `evidence.clause_segments(units)`,
   version `clause-v1`, splits each evidence unit after a run of clause
   punctuation (`,` `;` `:`, their full-width forms and `、`) with the
   combining marks that follow it, never between two digits. Segments are
   `E<n>.<k>` with absolute code-point offsets, stripped of edge
   whitespace, and partition every unit's non-whitespace text.
2. **The model labels; the program places** (U4.3, U4.4). The request
   holds each unit's segments by `segment_id` and `text`, the language and
   the character names present in the comment (`character_literals`); no
   offsets, quotes or reference entries. The response schema
   `evidence-quality-v2` has one required label object per segment
   (`scope`, `content_kind`, `emotional_tone`, `reason_code`) and the
   information points of v1, with `segment_ids` limited to the segment IDs
   and `character_literal` to `null` and the names present.
3. **One set of routing rules** (U4.3). `to_v1_annotation` converts a v2
   answer into the v1 shape with the program's offsets and quotes;
   `validate_annotation_v2` is the v2 schema followed by the unchanged v1
   rules on that conversion, and `qualify` routes it unchanged. A valid v2
   answer therefore always gives a valid v1 annotation.
4. **Both versions stay readable** (U4.5). A v2 record keeps the derived
   v1 `annotation`, which reports, review and extraction read, and the
   model's `annotation_v2`. Readers dispatch on each record's
   `schema_version`: v1 records keep the v1 rules; v2 records are
   validated by v2, and their derived v1 annotation must equal the stored
   one.
5. **Fixtures by mapping** (U4.2). Every frozen v1 fixture segment is a
   union of whole clauses, so `FixtureTransport` derives its v2 answers
   from the v1 annotations; no fixture or evaluation set changed.

## Measurements (U4-L)

U4-L ran the `latency-benchmark` sample (30 comments) and the
`quality-synthetic` sample (19 cases) in `shadow` through the hosted-API
bridge (UP-D19) at the U4.5 commit, against the U2-L1 runs of the same
samples (the change record, "U4-L" under "Live evaluations").

| Measure | U4-L | U2-L1 reference |
| ------- | ---- | --------------- |
| Quality elapsed per comment, benchmark (T4, indicative) | 11.2 s (23 comments) | 18.5 s (24) |
| First-attempt validity, benchmark (T5) | 18/23 (78.3 %) | 21/24 (87.5 %) |
| Quality-failed comments, benchmark | 4 | 2 |
| First-attempt validity, synthetic | 16/16 | 13/16 |
| Route agreement, synthetic | 14/16 | 11/16 |
| Quality output tokens per request, benchmark | 501 | 775 |
| Quality prompt tokens per request, benchmark | 3,673 | 1,957 |
| Largest prompt plus output | 14,346 | 6,557 |

No offset, quote, overlap or coverage error occurred. The remaining
errors were 7 point/segment detail conflicts (a concrete point selecting a
clause labeled `general_opinion`) and 2 literals outside the selected
clauses. The step failed adoption rules 2 and 3 on the benchmark while
rule 4 held on the synthetic sample; escalation E-4 of the change record
holds the options and the adopted recommendation (a prompt fix-up step,
with the revert of U4.4 and U4.5 as its fallback). U4.6 (`num_ctx` 8192)
was skipped because the largest request exceeds 6,000 tokens.

## Consequences

- Offset, quote, overlap and coverage errors can no longer occur; the
  failure classes that remain are the semantic ones (point and segment
  scope or detail conflicts, a literal outside the selected segments).
- A point cannot be finer than a clause. The prompts tell the model to
  label a clause that only supplies the subject, negation or condition of
  the next clause's concrete statement with that statement's labels, and
  show two authored examples per language.
- The schema grows with the clause count: the label object (about 760
  characters) repeats per segment in `format` and in the user message's
  `response_schema` (D-11 of the change record). Long comments send larger
  prompts than in v1, which the U4-L measurements quantify; the
  `num_ctx` reduction of U4.6 depends on them.
- The policy file changed in place (`evidence-quality-policy-v2`), so the
  run identity of every quality run changes; earlier runs cannot be
  resumed with this code (plan 2.3), and stay readable.
- The fixture runs keep their routes, claims and summaries; their routing
  entries hold clause segments, and the larger context splits one legacy
  extraction batch differently (U4.4).
- The legacy runner `engine.py` still records the hash of the v1 schema in
  its quality identity (Deferred in the change record).
