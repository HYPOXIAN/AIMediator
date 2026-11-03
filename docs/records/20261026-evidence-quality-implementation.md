# Comment evidence-quality module: implementation and verification

- Type: Record
- Status: Active
- Updated: 2026-11-03
- Applies to: evidence-quality module v1; `data/evaluation/evidence-quality-synthetic-v1`, `data/evaluation/evidence-quality-real-v1`; reports `evidence-quality-*-v1`
- Translated 2026-11 from the Chinese original (commit `3ceb123`); only the language changed.

Date: 2026-10-26 (America/Los_Angeles). The engineering specification is `docs/design/evidence-quality.md`.
This delivery provides the CLI engineering capability; independent human validation of effectiveness has not been obtained, and running shadow first is recommended.

## Implementation files

- `scripts/evidence_quality.py`: strict schema, coverage and source validation, Unicode LNMS length ratio, per-information-point routing, claim eligibility binding, separate opinion statistics.
- `configs/evidence-quality-policy.json`: v1 policy, ratio algorithm `unicode-LNMS-codepoint-v1`; 0.70 is only an uncalibrated warning and cannot serve as a deletion threshold. One annotation request per comment, 8192 output budget, 16384 context, at most two separate requests on failure.
- `prompts/evidence-quality.{en,zh}.txt`: bilingual annotation; outputs no final route, credibility or engineering recommendation.
- `prompts/quality-extract.{en,zh}.txt`, `prompts/quality-verify.{en,zh}.txt`: appended to the current main-flow prompts only under enforce; the off/shadow prompts stay as they were.
- `scripts/run_balance_analysis.py`: after relevance admission, comments enter the quality stage; separate parsing and schema; the three modes, quality-only, cache, snapshots, coverage and report outlets.
- `scripts/review_balance_sources.py`: source review keeps and revalidates eligibility; the proposal fingerprint includes eligibility. A modified claim cannot keep the automatic semantic audit from before the modification.
- `scripts/experiments/prepare_balance_design.py`: new-version input also requires mechanism eligibility, references to the selected segments, semantic audit and official identity; source accept, an explicit target, numerical intent and matching versioned data are still required.
- `scripts/experiments/demo_evidence_quality.py`: replay of synthetic annotations and mock end-to-end examples of the three modes; connects to no model and produces no real accuracy.
- `scripts/experiments/diagnose_evidence_quality_live.py`: explicitly selects comments from the frozen admission and runs real quality plus shadow/enforce extraction and audit comparisons in a new directory; does not rerun retrieval.
- `scripts/evaluate_evidence_quality.py`: creates sets to be annotated and scores effectiveness, by source, language, development/test and fixed-admission condition; does not take model output as labels automatically.
- `tests/test_evidence_quality.py`, `tests/test_evidence_quality_evaluation.py`: bilingual pure-logic, mock full-pipeline, failure/recovery and evaluation-boundary tests.

## Behavior and compatibility

The default `--evidence-quality off` adds no quality model calls; the old extraction, counts and the main semantics of the report are kept, but new code must use a new directory. The default output changed to `runs/balance-quality-v1`, to avoid continuing in a historical experiment directory.

Shadow annotations and routing outputs are observations only; the original extraction/aggregation runs as before, and the formal report does not mix in these observations. Under enforce only explicit character mechanism information points enter extraction. The complete original units still serve as context, the original E-IDs and `[start,end)` do not change, and model rewrites do not replace evidence.

Every claim must reference **one** eligible `quality_point_ids` of its own comment, and the corresponding evidence IDs must exactly match the selected point; character, direction, target and numbers must pass local binding checks. When a point involves several segments, the sources of all segments are kept. The separate semantic audit sees the complete original text as interpretive context, but only the selected segments may support the claim, and the distinction between request and observation is kept; eligibility labels, emotion share or emotional intensity are not taken as evidence. The local numerical check does not replace the existing numerical intent, identity, source and version rules.

The program cannot prove that the semantic segmentation, subject, deduplication or concreteness proposed by the model is correct. The current v1 applies a conservative literal constraint to concrete targets that appear in the original text; cross-language rewording may increase the review workload. Do not count review as successful extraction. Missing context, sarcasm, quoted abuse, structural errors or request failures can all go to review; other certain points can still be kept independently.

The enforce outlets of `balance-report-v3` include:

- `opinion_summary`: general opinions, keeping the direction and separate source counts for explicit_request / strength_assessment / observation; no concrete design is generated.
- `character_adjustments`: only mechanism evidence supported by the later review, counted by character, literal topic and direction, keeping buff/nerf/keep/unclear.
- `system_feedback`: system feedback with its general/concrete level, stored separately; v1 has no system recommendation generator.
- `quality_review_queue` / `quality_exclusions`: segment, source, reason, run status and traceable requests.

The weight is unique comment IDs per character/topic/direction, unaffected by emotional intensity and repeated venting. The stance sub-counts of opinions can overlap and cannot be added up. `quality-summary.json` additionally provides the union and intersection of the source sets of general opinions and of **review-passed mechanism evidence**. Categories, topics and directions can all overlap; comment counts cannot be called numbers of independent players or overall consensus. Unverified names within a source stay isolated and do not enter verified character groups.

The old claim lists of the design entry still take the `legacy/quality_not_assessed` branch. New-version `balance-report-v3` reports enforce eligibility automatically; when passing a new-version claim list on its own, add `--quality-mode enforce` explicitly, so that missing eligibility fields are not treated as legacy. Missing fields cannot default to passing the new version. A human accept cannot promote opinion_only to mechanism evidence either.

## Running, recovery and rollback

Run the following commands from the repository root, with a separate new directory for each mode. They depend on the existing numpy and local Ollama, and still use the language routing configuration and `qwen3-embedding:8b`; they do not read `.env` and add no external API or model.

```sh
cd <project root>
python3 -m unittest discover -s tests -p 'test_*.py'

# Recommended: observe first, without changing the old downstream flow
python3 scripts/run_balance_analysis.py --evidence-quality shadow --out reports/quality-shadow-new

# Stop after retrieval, relevance and quality
python3 scripts/run_balance_analysis.py --evidence-quality shadow --quality-only --out reports/quality-only-new

# Full flow with the eligibility gate
python3 scripts/run_balance_analysis.py --evidence-quality enforce --out reports/quality-enforce-new

# After source review, the new-version list must still use the enforce design gate explicitly
python3 scripts/experiments/prepare_balance_design.py --claims reports/quality-enforce-new/source-reviewed-claims.json --quality-mode enforce --out reports/quality-enforce-new/design-briefs.json

# Roll back run behavior: off plus a new directory, without rewriting historical output
python3 scripts/run_balance_analysis.py --evidence-quality off --out reports/quality-rollback-new

# Without a model service, replay the synthetic mixed routing and the mock three-mode end-to-end examples
python3 scripts/experiments/demo_evidence_quality.py --mock-pipeline --out reports/quality-demo-new
```

`--relevance-only` is allowed only with off; `--quality-only` requires shadow/enforce and cannot be used together with relevance-only. Argument errors are reported before any model call.

To recover, repeat **the same command with the same directory**. The manifest compares mode, data, model digests, code, schema, policy, prompts, output budget and measurement version; any identity change requires a new directory. Each request stores request/response/validation and the raw streamed output; quality attempts 1/2 use separate identities, so a retry is not a repeated reading of the same failed response. Two failures are persisted as review, not counted as exclude or generation_failed. Cache recovery adds no information-point weight and no double counting; interrupted raw streamed output is kept as a separate file.

Outputs include `evidence-quality.json`, `quality-routing.json`, `quality-summary.json`, `quality-review-queue.json`, `quality-exclusions.json`, `opinion-summary.json`, `system-feedback.json`, `full-pipeline-coverage.json`. The meaning of the existing coverage fields is kept; the new coverage records exactly one row per input, recording separately language unsupported/unselected, relevance rejected/pending, quality pending/complete/failed, extraction complete/failed, and review and source-review pending states. Normal routing after the quality decision does not count as extraction failure.

## Examples and the new annotation set

`data/evaluation/evidence-quality-synthetic-v1/` has 38 agent-authored Chinese and English synthetic cases, all development, covering the 12 boundary kinds required by the handoff plus additional historical/comparison/sarcasm/unknown-identity/emotion-equivalent variants. They are not community evidence or human ground truth.

`reports/evidence-quality-v1-delivery/examples/mixed-comment-examples.json` (archived; [manifest](../../reports/evidence-quality-delivery-v1/manifest.json)) shows multi-route output for price plus a general request, system plus cosmetics, and heavy venting plus a concrete mechanism; `mock-pipeline/{off,shadow,enforce}/` runs the complete pipeline with mock models and retrieval, all inputs are passed by the mock, and `execution-provenance.json` states the simulated source explicitly.

`data/evaluation/evidence-quality-real-v1/` draws 300 records deterministically by duplicate cluster from the existing **pre-screening** corpus: 198 en, 101 zh, 1 und; all labels are null/unlabeled, and there is no human accuracy. Sources that appeared in the historical admission are forced into development; normalized duplicate content does not cross splits. Equivalent clusters still need to be merged by humans, the language/source stratification checked and the split frozen before double annotation and adjudication; the current provisional test cannot be claimed directly as an independent blind test.

Commands to create a new annotation template (they do not overwrite an existing directory):

```sh
python3 scripts/evaluate_evidence_quality.py prepare --dataset data/raw/feedback/20261015-expanded/records.jsonl --source-stage raw_pre_screen --inspected-labels data/evaluation/balance-silver-v1/labels.jsonl --limit 300 --out data/evaluation/quality-labels-new
python3 scripts/evaluate_evidence_quality.py score --labels data/evaluation/quality-labels-new/annotation-template.json --run reports/quality-shadow-new --out reports/quality-score-new.json
```

So that identical segment IDs do not pass as semantic agreement, scoring requires human/silver labels to provide `points` (with point_id, route, segment_ids) and `point_matches` (a one-to-one adjudication of gold_point_id and predicted_point_id). Mechanism outputs without a match record count in the precision denominator; missing/review count as recall loss. `segments` keeps the exact-source segment format; emotion span precision/recall and the ratio error are computed **only** for records with reviewer_type=human and span labels. human / silver / agent_authored_synthetic and development/test results are kept separate and not merged into one overall accuracy. All ratios keep numerator and denominator with Wilson intervals, and a zero denominator is null; relevance false acceptance is defined as the unrelated share among admitted records that have a binary relevance label. The intervals are not corrected for within-comment/between-character correlation and cannot serve as small-sample guarantees.

The report gives at the same time mechanism precision/recall, the false-exclusion rate of concrete mechanisms, the promotion rate of general opinions, the rate of system feedback wrongly bound to a character, review/failure rates, the recall loss from review, and equivalent eligibility/unit-weight agreement. Results on the fixed admission subset are conditional performance; only scoring that covers pre-screening samples and upstream admission status can discuss end-to-end recall. This module cannot recover comments that never entered it.

## Verification status

See [`reports/evidence-quality-verification-v1/summary/verification.json`](../../reports/evidence-quality-verification-v1/summary/verification.json) and `tests.log` (archived; [manifest](../../reports/evidence-quality-verification-v1/manifest.json)).
The existing frozen silver-v1, admission, original comments and historical reports were not overwritten. New code requires a new directory and does not continue old results directly.

The real diagnostic uses the original-language models and two sources from the fixed historical admission, saving all raw responses and the shadow/enforce audit records. The English Drive Rush input was labeled exclude by the model; the coarse annotation and extraction of the Chinese sample still need human checking, and the enforce semantic audit once returned uncertain. All of these are observations awaiting review, not conclusions about correctness. The final diagnostic status is given by [`reports/evidence-quality-live-verified-v1/summary/diagnostic-summary.json`](../../reports/evidence-quality-live-verified-v1/summary/diagnostic-summary.json).

The current local model list lacks `qwen3-embedding:8b`, so the complete online run of fresh retrieval + relevance + quality + extraction was not completed; the fixed-admission diagnostic did not bypass or forge that model's digest. The complete run commands above can be executed only after the original embedding model is restored. This delivery does not download or replace models automatically.

Not yet verified: independent bilingual double annotation and adjudication of 200–400 records, the quality of semantic segmentation/deduplication, span label accuracy, real-inference consistency of emotion-equivalent variants, the effectiveness metrics on an independent test set, full-pipeline recall after upstream misses, and versioned facts and actual balance effects. The 95%/5%/2%/95% in the specification remain candidate targets and are not claimed as achieved. The default is off, shadow is currently recommended, and the complete enforce capability is in place.

## Moved from the root README

This section was moved from the root `README.md` on 2026-11-03 (change
record, P4-D02), and translated with this record.

### Comment evidence quality and emotional-interference control

New: `--evidence-quality off|shadow|enforce` (default off) and `--quality-only`.
After relevance admission, comments are routed by original segment and information point into unrelated/pure venting, general opinion, character mechanism,
system feedback and pending review; the pure-emotion length share is diagnostic only and does not change the eligibility or weight of comments that carry information.
General opinions cannot support concrete move/numerical design. enforce still applies the existing identity, source, numerical,
source-review and versioned-data gates; off/shadow keep the old downstream semantics.

Both running and rollback use a new directory, for example:
`python3 scripts/run_balance_analysis.py --evidence-quality shadow --out reports/quality-shadow-new`;
for rollback use `--evidence-quality off --out reports/quality-rollback-new` instead.
Without a model, run `python3 scripts/experiments/demo_evidence_quality.py --mock-pipeline --out reports/quality-demo-new`.
See [implementation, commands, outputs and unverified items](20261026-evidence-quality-implementation.md).
Independent human validation of effectiveness is not complete, and shadow is currently recommended; synthetic tests and small real diagnostics do not represent accuracy.
