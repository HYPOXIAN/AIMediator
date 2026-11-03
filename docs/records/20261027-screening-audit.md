# Audit of the existing screening mechanism · 2026-10-27

- Type: Record
- Status: Active
- Updated: 2026-11-03
- Applies to: report `20261027-screening-audit` (archived as `screening-audit-20261027`); dataset `data/raw/feedback/20261015-expanded/screened/records.jsonl` with the `balance-review-v2` relevance run and `quality-screening-existing-100-recovered-v2`
- Translated 2026-11 from the report summary [`summary/report.zh.md`](../../reports/20261027-screening-audit/summary/report.zh.md); only the language changed (change record, P4-D12).

> **Note (2026-11-03, reorganization).** This record is the result record of
> the report, which had none (P2). The files it names (`ALL-REVIEWS.md`,
> `comment-audits.jsonl`, `MODEL-POINT-REVIEWS.md`, `model-point-audits.json`,
> `relevance-overrides.tsv`, `historical-silver-disagreements.json`) and
> "this directory" are in the archived report; see the
> [manifest](../../reports/20261027-screening-audit/manifest.json). The kept
> `summary/summary.json` and `summary/verification.json` hold the counts and
> checks.

Conclusion: the existing results are not enough to conclude that the screening mechanism removes emotional interference and unrelated content precisely. Observed: concrete information blocked, unrelated content wrongly admitted, purely negative attitude entering system evidence, general opinions promoted to character mechanisms, and character requests wrongly assigned to the system. Passing format validation does not prove that these semantics are correct.

## Coverage and results of this audit

- All 321 records audited one by one: 207 English, 113 Chinese, 1 Portuguese.
- Mutually exclusive primary categories: 133 with character/system candidates, 147 general opinion only, 27 pending review, 13 wholly unrelated, 1 Portuguese isolated.
- A single record can contain general opinion, mechanism, system feedback and pending parts at the same time; overlapping route counts cannot be added up as a total number of comments. Candidates still need checks of identity, version, facts and source, and cannot be used directly for tuning.
- Latest frozen relevance: 320 Chinese and English records, 275 admitted, 45 not admitted; 161 requests replayed with the current code were all identical, with no new inference calls. The 45 include retrieval rejections, review rejections and uncertain states; not every non-admission is called a model rejection.
- Of the 299 records this silver audit considers related, 264 were admitted and 35 were not. Of the 13 unrelated, 5 were wrongly admitted and 8 not admitted.
- Conditional relevance precision = 264/269 = 98.1%; conditional recall within the current coarse-screened retained set = 264/299 = 88.3%. Computed only on the 312 comments with an explicit binary topic label; the 8 whose topic remains uncertain and the 1 Portuguese record are not in the denominator. Of the 27 pending review for their use, 19 are in fact clearly on topic, only identity/direction/facts are unresolved, and they must not be mixed up with off-topic; the per-record basis is in relevance-overrides.tsv. General opinions also count as related; this is not an "accuracy of concrete mechanism evidence".
- The 320 Chinese and English records kept by coarse screening still contain 13 unrelated ones (13/320 = 4.1%); this only describes what remains in the retained set and is not the complete precision/recall of coarse screening. The originally rejected corpus was not audited.

## The quality stage must not be read as 38 records audited successfully

The existing 100-record diagnostic experiment classified only 38 records, 16 of which reused the upstream non-admission result; actual quality attempts were 22, all English. 15 passed structural validation and 7 failed and went to review. The other 253 records admitted by relevance have no quality result from this experiment, and Chinese quality performance in particular was not verified by it. 15/22 only means the share that passed structural validation, not a correctness rate; review is neither successful removal nor successful extraction.

All 16 published information points were audited; 7 of them entered a retained route: 2 character mechanism points and 5 system points. Both character mechanism points wrongly promoted a general complaint/update observation; the 5 system points variously mixed in unrelated content, leaked purely negative attitude, assigned a character to the system, or misclassified request/observation. They come from a diagnostic subset that deliberately contains historical problems, and the full error rate cannot be extrapolated from them.

## Failure examples that can be checked directly

- #14 steam:236856267: a DI complaint and an exaggerated Ryu "war crimes" complaint were combined into Ryu mechanism evidence. It should be lowered to a general opinion; DI properties cannot be bound to Ryu.
- #23 steam:236222206: concrete feedback on Drive-rush corner-carry / 50-50 was excluded, while a sigh went to review. This is a segment wrongly deleted; the information is not protected just because the whole record went to review.
- #63 steam:233481207: the sarcastic "another year of Ryu buffs" was taken as a concrete Ryu mechanism, and "buffs" even as a mechanism name; an update observation cannot pass as the author supporting a buff.
- #94 steam:232518681: praise of action and visual readability was admitted by relevance; the whole text has no claim about character strength or a battle adjustment.
- #163 youtube:UgzJYtb-vEd9Z3T9GQh4AaABAg: a long text ending with an explicit request to fix the 100% throw-tech input bug was not admitted at the relevance stage.
- #185 steam:231963988: the conditional requests (Drive Rush 3 bars, remove throw loops, parry −1 frame) were not released as system information; everything stayed in review.
- #220 steam:229094178: "buff manon" was wrongly taken as system feedback; the literal name Manon was lost, and the explicit request was misread as a strength assessment.
- #233 steam:228172110: "and this review will be negative" was kept as system evidence; a JP nerf request was again wrongly assigned to the system.

## How emotional bias was audited

This audit checked whether emotion replaced information, whether valid information carrying emotion was wrongly deleted, whether pure venting or unrelated segments were mixed into evidence, and whether segmentation or character attribution distorted opinions. Angry wording does not prove a cognitive bias, nor that the information is wrong; without real human double annotation, real-inference comparisons of emotion-equivalent and neutral pairs, or player background, this audit cannot measure psychological bias or prove that a tone caused an error.

"balance sux", `加强JP` ("buff JP") and the like are general opinions the policy allows; they can only be counted and cannot yield concrete mechanism or numerical proposals. Naming a mechanism while only expressing dislike does not automatically qualify as mechanism evidence either. Pure exclamations, abuse, looks, price, network, cheating, story and roster preferences should be removed from battle-balance evidence; mixed comments keep their valid parts and cannot be cut out wholesale.

The emotion ratio 0.70 in the code is diagnostic only and cannot delete records or change weights; the default quality mode is off, shadow only observes, and only enforce constrains downstream. This replay and the existing unit checks show that the deterministic controls are reproducible; they do not prove that the local model's real segmentation and semantics meet the bar.

## Suggested order of fixes

1. First fix the scope, character attribution, concreteness and request/observation distinction of information points, and block general opinions from being promoted and emotional segments from entering evidence first.
2. Use the actual failures above to check mixed long texts, valid sentences at the end, sarcasm, positive feedback, general overall opinions and segment context; adding or removing keywords alone is not enough.
3. Keep review as an independent state and provide an actual release process; non-extraction should be recorded as a loss and not packaged as successful removal.
4. Confirm these AI silver labels with independent human double annotation and adjudication, then measure the complete flow on pre-screening samples that took no part in the fixes. At this stage enforce is not good enough to be treated as a reliable replacement for automatic review.

## Where the full conclusions are

All 321 records are in ALL-REVIEWS.md / comment-audits.jsonl; the 16 model information points and per-point comments are in MODEL-POINT-REVIEWS.md / model-point-audits.json. Each entry has the complete original text, source, quotation position, audit reason, confidence, the original coarse-screening decision, the latest relevance status and the available quality output.

This audit was done by a single AI, not blind, and is agent silver, not independent human ground truth; the auditor had seen some historical failure cases before. After the first pass, boundaries such as pure learning, matchmaking preferences and update frequency were checked against the existing prompts and historical silver labels; the historical silver labels were not rewritten. Disagreements are stored one by one in historical-silver-disagreements.json, all awaiting independent adjudication. In particular, #82 (high-level randomness), #163 (the throw-tech bug) and #319 (a positive system observation) have disagreements about the counting basis and should be checked against the original text; neither the new nor the old AI label may be taken as a human answer.

No original text, historical model result or screening rule was changed, the local model was not called again, and actual versions, official identities, frame counts, damage and balance effects were not verified. All source checksums, snapshots and verification records are in this directory.
