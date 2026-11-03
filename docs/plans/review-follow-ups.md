# Senior review work log

- Type: Plan (follow-up list)
- Status: Active
- Updated: 2026-11-03
- Applies to: balance review v2 and v2.2; `data/evaluation/balance-silver-v1`

## Decisions recorded before implementation

- [x] Independent human annotations are unavailable. Build a 100-comment **agent-reviewed silver** set with source hashes, written reasons, uncertainty and a frozen development/holdout split. Do not call it gold or report human accuracy. Independent double annotation remains an external follow-up.
- [x] The glossary targets an older patch. Preserve that glossary; add a separate source-literal candidate registry with provenance for Arjun/`阿俊`. Its official roster identity stays unverified. Nationality-only aliases cannot establish identity.
- [x] Preserve the previous experiment unchanged. Evaluate frozen previous outputs and new gates separately; new prompt/model tests use new report directories.
- [x] Retain retrieval/model agreement before extraction. Borderline or explicitly quantitative vector-negative comments go to a review queue, not directly to extraction.
- [x] Numeric intent rules are conservative safety checks, not a proof of entailment. Ambiguous requests require review rather than invented values.
- [x] Official move/frame data is unavailable in the repository. Implement an engineering-design readiness stage that blocks numerical design until versioned data and source review are present. Do not fabricate a frame database.

## Delivery checklist

- [x] Versioned identity policy and unknown-name preservation integrated into extraction/audit.
- [x] Source request versus engineering-design contract and readiness report.
- [x] 100 reviewed comments, frozen split and reproducible metrics.
- [x] Regression fixtures from actual failures and bilingual numeric controls.
- [x] Retrieval triage calibrated on development labels; held-out labels excluded from calibration.
- [x] Whole-corpus retrieval/relevance replay plus live queued relevance review.
- [x] Live bilingual extraction/source-audit regression and numerical controls.
- [x] Documentation, final checks and explicit unresolved external work.

## External follow-up (not substituted with fabricated evidence)

- [ ] Independent human double annotation/adjudication of silver labels.
- [ ] Verify official roster identity and patch applicability for source-only names.
- [ ] Supply licensed/versioned move data, then design and playtest concrete tuning changes.

- [x] Local single-source review was slow. Reuse completed single checks; batch remaining candidates, individually recheck batch rejections/uncertainty, and preserve both verdicts. No nomination bypasses the final relevance gate.

- [x] The spelling `阿利克斯` in `steam:237633927` is not matched by the older Alex aliases. Decision: do not silently assert that canonical mapping from transliteration alone. Preserve this explicit source name in a pending candidate record; require identity/alias confirmation before a future registry version. This does not change the frozen relevance experiment or its thresholds.

- [x] A vector-positive/model-negative disagreement is not necessarily a genuinely unrelated source. Decision: export a separate follow-up queue for all such disagreements, plus unverified source-only identities. The export preserves the original text and never changes admission by itself.

## End-to-end failures and targeted follow-up

- [x] The first live v2 regression passed only 1/6; numerical extraction passed 0/2 although the guard rejected fabricated deltas/units. Preserve these failed reports. Decision: constrain generated numeric values/units to source candidates, force absent delta/unit to null, shorten the bilingual extraction/audit instructions, and test a separate v2.1 generation iteration. The frozen 275-comment relevance result and silver holdout metrics must not be retuned.
- [x] Complete the v2.2 targeted generation/audit regression; preserve the failed v2 and interrupted v2.1 artifacts and explicitly report remaining model errors.

- [x] The sole held-out apparent false positive contains a high-level randomness assertion and the silver unrelated label may be too strict. Decision: record an adjudication erratum, preserve the frozen score, and do not retune against the holdout.

- [x] A second review found the hostile “next Jamie buff” case can be read literally or sarcastically. Decision: preserve its frozen diagnostic expectation, add an adjudication erratum, and do not use it as proof of model direction accuracy or a release-ready buff.

- [x] A shortened prompt correctly recovered the plain Manon request, but the model still attached system concerns to roster-only Elena and repeated claims. Decision: add conservative source-attribution constraints for explicitly cosmetic/roster-only mentions and explicit attacker/victim constructions. These are source grammar checks, not inferred gameplay facts; preserve full originals and exclusions. Retain the interrupted v2.1 trace as a failed diagnostic and run a new targeted iteration.

- [x] The latest model produced an addressee-only recommendation and two unclear Arjun directions. Decision: require an actual engineering action before design, apply fingerprinted agent source review, correct only an explicit nerf request, and keep ambiguous opinions outside accepted adjustments. Known annotation disputes also block design readiness.
