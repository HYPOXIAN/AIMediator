# Fresh balanced feedback validation (2026-10-27)

- Type: Record
- Status: Active
- Updated: 2026-11-03
- Applies to: dataset `data/raw/feedback/20261027-balanced`; report `20261027-balanced-validation`

This bounded run uses the existing collection sources and coarse-v1 screening,
then freezes 600 comments (300 English, 300 simplified Chinese). No previous
raw file seeds the collection. Existing source IDs can reappear when fetched
again; this is fresh retrieval, not a claim that all posts are newly published.
The final selected set contains Steam reviews. The configured APIs do not
collect nested forum replies. Actual source publication ranges are in the
screened summary and must be retained when describing recency.

## Reproduce collection

```sh
python3 scripts/collect/collect_balanced_feedback.py \
  --out data/raw/feedback/20261027-balanced \
  --review-decisions configs/20261027-feedback-source-reviews-v2.json
```

`configs/feedback-collection-balanced.json` copies the existing app,
languages, sources, intervals, YouTube quota and queries. It requests latest
YouTube video discovery, resets collection cursors in a new directory, and
extends Steam collection in bounded 100-record pages until each language has
300 coarse-retained unique texts. Steam's adaptive ceiling is 100 requests
with the existing five-second spacing; raw safety caps are 6,000 per language.
HTTP denial and cooldown remain binding. Uncertain records never pad quotas.
The final set selects newest publication timestamps within language quotas.

All raw evidence stays unchanged. The fingerprinted source-review file corrects
platform language errors and excludes a traditional-Chinese film discussion.
The original provisional and first reviewed selections remain in separate
folders. Use `--screen-only` to reselect saved raw evidence without network
requests. Counts refer to the canonical `screened/records.jsonl`, not sums of
overlapping language or platform views.

## Reproduce the full default pipeline

```sh
python3 scripts/run_balance_analysis.py \
  --dataset data/raw/feedback/20261027-balanced/screened/records.jsonl \
  --embedding-provider configured --num-gpu 99 --evidence-quality off \
  --out reports/latest-balanced-20261027/full-pipeline
python3 scripts/validate_latest_run.py \
  --data data/raw/feedback/20261027-balanced \
  --run reports/latest-balanced-20261027/full-pipeline \
  --out reports/latest-balanced-20261027/integrity-checks.json
```

Use a new output folder after changing any frozen prompt, source, policy,
model identity or runner. Repeating an unchanged command resumes exact cached
requests. `--embedding-provider configured` uses the existing embedding URL,
model and credential from `.env`; credentials are never saved in run identity
or caches. The remote embedding service has no locally verified model weight
digest. The existing Ollama embedding path remains the default for other runs.

`--num-gpu` records explicit placement in the run identity and actual requests.
For this experiment a one-token probe verified the GPU placement. CPU and
unforced auto-placement attempts were interrupted and preserved; they are not
counted as the complete experiment. In particular, an already-loaded CPU
instance remained in use under unforced auto placement.

## Paired prompts and diagnostic scope

The active extraction and verification instructions are
`prompts/summarize-balance.{en,zh}.txt` and
`prompts/verify-balance.{en,zh}.txt`. Summarization after verified extraction is
deterministic aggregation, not another free-form model prompt. Preserve original
source wording in evidence even when recommendation wording is normalized.

`python3 scripts/finish_latest_validation.py` waits for the full report, verifies
input/claim accounting, then runs numeric entailment and numeric extraction
controls, a same-runtime baseline/final comparison on six frozen real cases,
and a separate four-source live enforce diagnostic from the new dataset.
Synthetic controls are always separate from community counts. The frozen
six-case expectations are debugging references, not independent gold labels.

The quality annotation prompts additionally prefer copying complete, coherently
classified evidence units, enforce point/segment-kind agreement and preserve
conditional intent. This does not relax source offsets or coverage checks.

The complete 600-comment run uses the existing default `evidence-quality=off`.
It tests retrieval, relevance agreement/refinement, extraction, exact source
binding, numeric intent checks, semantic audit and aggregation. The separate
live four-source enforce diagnostic and offline tests cover the quality module;
they must not be described as 600 fresh shadow/enforce annotations or a measured
reduction in emotion bias.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/experiments/run_balance_semantic_controls_live.py \
  --out reports/latest-balanced-20261027/semantic-controls
python3 scripts/recover_latest_failures.py \
  --run reports/latest-balanced-20261027/full-pipeline \
  --out reports/latest-balanced-20261027/generation-recovery
python3 scripts/render_latest_validation_report.py
```

The final report is [`reports/20261027-balanced-validation/summary/evaluation.md`](../../reports/20261027-balanced-validation/summary/evaluation.md). Review
`full-pipeline/quarantined-claims.json` and final-generation failures as well as
accepted outputs. Automatic completion does not establish semantic accuracy,
patch applicability, mechanic truth, population consensus or optimal tuning.
No independent human labels or versioned game-mechanic verification were added.

## Final decoder fix and known limitations

The full 600-comment experiment is preserved with its original runner snapshot.
After inspecting the synthetic controls, the extractor schema was tightened:
when every allowed proposed/delta value is null, a numerical parameter is
impossible, so decoding must use qualitative_only and an empty parameter array.
This only removes outputs already rejected by the existing source gate.
All 184 initially accepted claims were replay-validated under the current
contract; all eight live semantic controls pass after the fix. The final selected
run executes all 600 inputs on current code. Model-visible requests identical
in every field can replay recorded results; changed schemas, messages or options
receive fresh inference. This is not 600 wholly independent new generations.
Each replay records its original request/response paths and hashes. To run the
current code again, use a new output directory, as required by the manifest.

The final quality prompt is recorded in `quality-live-enforce-v4/`. Its four
known development cases include three valid primary route/current-position
results and one source-context failure routed to review. Earlier variants,
including an intermediate variant with correct routes but incorrect directions,
remain intact. These are development checks, not independent accuracy.
The two compact exact-quote recovery variants did not resolve the failed
annotation; no relaxed quote or coverage validation was used.

The long-comment generation failure also remains explicit after bounded
recovery trials. Standard recovery preserves temperature 0; separate variants
record temperature 0.4 and a bounded JSON-completion experiment. No partial JSON
was accepted and no source wording, values or directions were repaired.
The final current-code full run contains two generation failures. The second
source had four quarantined claims in the initial run and no accepted claims;
its separate targeted retry is recorded in `generation-recovery-final-new-source`.
The initial one-source recovery count must not be read as the final-run total.
That retry returned valid JSON, but source review rejected all ten automatically
accepted supplemental claims for unsupported Ryu attribution/direction. The
whole supplement is excluded from the primary result. This correlated verifier
failure is retained in `agent-source-review.json`, not counted as successful
semantic recovery or silently merged into the 187 primary automatic claims.
The current prototype still requires source review; neither all-concern recall,
optimal prompts nor emotion-bias reduction was established.

## Current-code full rerun with exact request provenance

```sh
python3 scripts/rerun_latest_exact_requests.py \
  --from-run reports/latest-balanced-20261027/full-pipeline \
  --out reports/latest-balanced-20261027/full-pipeline-final \
  --dataset data/raw/feedback/20261027-balanced/screened/records.jsonl
```

The parent dataset hash and local model weight digests must match. Reuse compares
the entire model-visible request, including its message strings, format and
inference options. It never substitutes an old response merely because it would
pass a newer schema. All responses, replayed or fresh, pass the current pipeline
validators. `transport-reuse-summary.json` separates fresh calls from replays;
replayed response processing time is not a fresh-inference throughput measure.
The initial run remains intact for before/after comparison.

## Moved from the root README

This section was moved verbatim from the root `README.md` (section "Fresh
balanced validation (October 27, 2026)") on 2026-11-03 (change record,
P4-D02).

The new canonical dataset is
`data/raw/feedback/20261027-balanced/screened/records.jsonl`: 600 retained
Steam reviews, with 300 English and 300 simplified-Chinese records after
fingerprinted language corrections. Collection restarted from latest-sorted
streams without seeding old files, but meeting the retained quota reaches back
to December 2025 for English and August 2026 for Chinese. It is not a set of 600
posts published today. Existing raw evidence and provisional selections remain
available.

See [collection, full-run commands and diagnostic scope](20261027-balanced-validation.md).
The active bilingual extraction and source-verification prompts now require a
complete subject/action recommendation, preserve conditional and negated intent,
keep clause-local subjects, and reject unrelated numbers as tuning targets.
`--embedding-provider configured` supports the already configured embedding
service; `--num-gpu` records explicit placement. The full default run and its
separate controls live under `reports/latest-balanced-20261027/` (archived; [manifest](../../reports/20261027-balanced-validation/manifest.json)). Completion,
quarantine and failure counts are read from the resulting reports, never assumed
from an in-progress run. The 600-comment default run uses evidence-quality=off;
quality integration has separate live diagnostics and offline tests.
