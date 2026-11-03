# Review and evaluation v2

- Type: Record
- Status: Active
- Updated: 2026-11-03
- Applies to: reports `balance-review-v2` and `balance-review-v22`; `data/evaluation/balance-silver-v1`, `data/evaluation/balance-regressions-v1`

This iteration implements a frozen evaluation set, explicit identity policy,
retrieval review queue, conservative numerical-intent checks, known-error
regressions and a separate engineering-design preparation contract. It preserves
the 2026-10-22 v1 experiment as a historical record.

## Review provenance and decisions

`docs/plans/review-follow-ups.md` records decisions and unavailable inputs. The 100-comment
set in `data/evaluation/balance-silver-v1/` is **agent silver**, not independent
human gold. It has 50 English/50 Chinese comments, 70 development/30 holdout,
written reasons, original-text hashes and selected character/direction/numeric
expectations. Only selected clear character pairs are annotated; unlisted
characters cannot be counted as false positives. Sampling deliberately includes
old errors and is not a prevalence estimate. Two uncertain relevance labels are
excluded from binary metrics. Threshold selection reads development labels only.
Corrections to frozen labels require a new version.

## Identity preservation

`configs/balance-review-policy.json` is separate from the original patch-specific
glossary. Nationality and selected derogatory aliases cannot establish Dhalsim.
Explicit canonical names and other candidate aliases still require context and
semantic review. The policy registry maps Arjun/阿俊 only as a source-local name
correspondence, based on both spellings in `steam:237730282`. It does not assert
an official roster fact. Each grounded claim records the source literal,
normalization status and glossary patch. Source-only identities have canonical
name null, remain inspectable in `unresolved_identity_claims` and are excluded
from verified character adjustment groups. New unfamiliar names require a
provenance-bearing candidate registry entry; there is no unrestricted name guess.

## Retrieval queue and admission

The original vector-positive condition remains visible. A vector-negative
comment is nominated for review when its margin is within the calibrated band,
or it contains an explicit numerical change cue. Nomination never admits a
comment. A dedicated retrieval-topic review must affirm it, then a separate
same-language relevance review must agree without uncertainty. Batch rejections
and uncertainty are individually rechecked, retaining the initial result.
Clearly unresolved cases remain in `review-queue.json`.

The development set selected an absolute margin of 0.08 from the fixed tested
candidates, targeting at least 95% related-source *nomination* recall while
minimizing queue size. Nomination recall and final admission recall are reported
separately. On this pre-screened corpus, the extra review workload is substantial;
performance/precision estimates from the small silver sample do not generalize.

## Numerical evidence and design

The source gate now requires a local requested-change cue for each proposed
numeric target/delta. Merely seeing Ryu's 600 and Ken's 500 does not support
changing Ryu 600→500. Past-change and negated-action cues require review. This is
a conservative bilingual lexical boundary, not a complete semantic parser:
unusual valid wording may be withheld, and a model audit is still necessary.
Explicit strengthening/weakening actions that contradict their direction tag
are also blocked, without assuming how reducing a frame value changes strength.
Concrete numeric demonstration values were removed from extraction examples to
reduce example leakage. Equivalent English/Chinese prompts preserve source
requests and isolate engineering assumptions.

`prepare_balance_design.py` accepts reviewed claims and optional verified move
records: character, exact target, patch version, metric, current value, unit,
reference URL and verified status. Duplicate keys, incomplete records and
unverified records fail. A supplied verified flag is an input attestation; URL
format validation alone does not verify the underlying game facts. Matching data and an explicit target patch can make a
brief ready for engineering design; they never approve a game change.
Each brief preserves the source request unchanged and separately reserves
engineering hypotheses, rationale, versioned references and playtest results.
Absent information blocks design; no frame or damage database is fabricated.
The 47 prior reviewed claims all remain blocked because required patch/move
inputs are missing.

## Run the checks

```sh
python3 -m unittest discover -s tests -v
python3 scripts/experiments/evaluate_balance_review.py --out reports/balance-review-v2/evaluation
python3 scripts/experiments/replay_balance_admission.py --from-run reports/balance-review-v2/relevance --out reports/balance-review-v22/admission-replay
python3 scripts/experiments/evaluate_balance_review.py --candidate reports/balance-review-v2/relevance --out reports/balance-review-v2/evaluation
python3 scripts/experiments/check_balance_regressions.py --out reports/balance-review-v2/regression-replay.json
python3 scripts/experiments/run_balance_regression_live.py --admission-run reports/balance-review-v2/relevance --out reports/balance-review-v22/live-regressions
python3 scripts/experiments/run_balance_controls_live.py --out reports/balance-review-v22/numeric-controls
python3 scripts/experiments/prepare_balance_design.py --claims reports/balance-engineering-20261022-final-review/source-reviewed-claims.json --out reports/balance-review-v2/design-briefs.json
```

For a new full-generation experiment, omit `--relevance-only` and choose a new
output folder, for example `reports/balance-v2-full`. The v1 manifest intentionally
rejects resume with changed v2 code/prompts. Do not overwrite the historical v1
report. Complete compatible requests and embeddings are content-addressed and
reusable in a new experiment; model/prompt/policy hashes guard run identity.

Actual-error fixtures preserve twelve original source/proposal pairs, including
copied numbers, historical patches, direction reversal, comparisons, system
misattribution and attacker/victim reversal. Replay of old outputs is labeled
as replay. Six separate live development-set cases test updated extraction against real sources
that first passed the new relevance gate. Four numeric controls are synthetic,
kept outside community counts, and report **model-only** and **combined-gate**
results separately. Passing a guard does not mean the underlying model improved.

## Remaining external work

Independent human double annotation, official roster/patch identity verification,
versioned move inputs and actual matchup/playtest validation remain explicit
follow-ups. A source-bound quotation and an agent review do not establish game
truth or readiness for unattended tuning. Every automatic report retains
`requires_source_review_and_versioned_game_data` release status.

## Targeted extraction follow-up

The first v2 live generation check passed only 1/6 and numeric extraction 0/2.
Those failed results remain unchanged. The v2.1 attempt was interrupted after
showing repeated roster/system misattribution. The v2.2 iteration shortens the
bilingual prompts, constrains current/proposed/delta/unit to literal source
candidates, and excludes explicit cosmetic-only mentions and clear recipients
from the proposed attack-subject enum. It does not resolve arbitrary sarcasm or
comparisons. Attribute exclusions are exported with full source text.

```sh
python3 scripts/experiments/run_balance_numeric_extraction_live.py --out reports/balance-review-v22/numeric-extraction
python3 scripts/experiments/review_balance_live.py --live-run reports/balance-review-v22/live-regressions --admission-run reports/balance-review-v2/relevance --decisions reports/balance-review-v22/source-review-decisions.json --out reports/balance-review-v22/source-review
```

The 275-source admission result stays frozen; all 161 saved admission requests
were replayed with the current validator, without inference or retuning, and
all decisions stayed identical. Fresh extraction/audit requests use the new
prompts and their own manifests. The six-case score checks selected diagnostic
expectations and is not a proof that every recommendation body is actionable.
Separate fingerprinted review repairs or excludes actual proposals, preserving
raw texts and directions. Known silver-label disputes remain in errata and also
block engineering readiness. For a new *fresh* relevance experiment, use a new
output directory with `--relevance-only`; old manifests deliberately reject
changed code or prompts.

## Moved from the root README

These paragraphs were moved verbatim from the root `README.md` (section
"Bilingual evidence-grounded balance summaries") on 2026-11-03 (change
record, P4-D02).

The next review iteration adds a frozen 100-comment agent silver set, versioned
identity policy, retrieval review queue, actual-error regressions and separate
engineering-design prerequisites. See [review v2](20261022-balance-review-v2.md) and
[decisions and follow-ups](../plans/review-follow-ups.md). The v2 evaluation uses full-corpus
retrieval/relevance and selected live extraction regressions; it does not claim
a full rerun of v1 generation or independent human accuracy.

The latest targeted generation follow-up is recorded in
`reports/balance-review-v22/review-summary.md`: 94 code checks pass, numeric
extraction controls pass 2/2, and numeric entailment controls pass 4/4. Six real
regressions meet the frozen diagnostic expectation in 4/6 cases and still need
source review; malformed recommendation text is separately repaired or blocked.
The frozen 275-comment admission decisions were replay-validated without fresh
inference or holdout retuning. Failed v2 results remain available; the superseded
interrupted v2.1 run was removed during directory cleanup.
