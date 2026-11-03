# Root README research history

- Type: Entry (excerpt of the root README)
- Status: Archived
- Updated: 2026-11-03
- Applies to: root `README.md` at commit `4e2cccb`, before the 2026-11 slim-down

The root README used to retell the project's research history. RULES.md D4
keeps that out of the entry point, so the sections below were moved here
verbatim when the README was slimmed down (change record, P4-D02). Sections
whose topic has a record went to that record instead: the glossary and
Unique Move alias sections to
[20261022-alias-review.md](../records/20261022-alias-review.md), the
balance review v2 and v2.2 paragraphs to
[20261022-balance-review-v2.md](../records/20261022-balance-review-v2.md),
the evidence-quality section to
[20261026-evidence-quality-implementation.md](../records/20261026-evidence-quality-implementation.md),
and the October 27 validation to
[20261027-balanced-validation.md](../records/20261027-balanced-validation.md).

The text describes the project as it was when each section was written.
Paths and commands are kept as they were, except where later changes in
this reorganization updated references.

## Research runners (from "Layout")

The command-line retrieval, bilingual extraction and evidence-audit pipeline is
available in `scripts/run_balance_analysis.py` (Python and numpy). The original
standard-library debugging runner remains in `scripts/run_smoke_test.py`.

## Local smoke test

Run `python3 scripts/run_smoke_test.py` with Ollama running locally. Each run creates a new timestamped directory under `reports/` without overwriting earlier results.

To repeat the same ten comments with vocabulary assistance, run `python3 scripts/run_smoke_test.py --glossary`. The run saves a glossary snapshot and hash, and the exact retrieved reference in each request. It keeps the baseline generation settings and original cases. Add `--cpu` to explicitly request CPU inference (`num_gpu=0`) after a GPU backend failure; runtime is then not comparable to the GPU baseline. Short and overloaded matches are candidates only; the model must apply their context restrictions.

To recover an interrupted run, use `python3 scripts/run_smoke_test.py --resume reports/<run-directory>`. The runner loads the saved prompt and cases, verifies the original model digests, retains completed responses, archives failed attempts, and reruns missing or interrupted cases. JSON result files are written via an atomic replacement after flushing to disk.

The runner uses ten synthetic Ryu comments, five English and five Chinese, plus a verified subset of official patch context. It preserves the prompt, cases, model identities, inference options, complete requests and responses, timing, automatic structural checks, and blank human review fields. It does not enforce JSON output or retry failed requests.

Open the run's `review.md` to inspect the inputs and raw outputs. Fill in `review.csv` and the blank notes in `review.md` to assess semantics before choosing a model. Generated runs remain on disk but are excluded from version control by default.

Official patch source: https://www.streetfighter.com/6/buckler/battle_change/20260803

## Original milestone: verify model extraction

1. Choose one balance patch and record its exact date or version. Do not combine comments about different patches.
2. Run `ollama list` locally and record the exact installed Qwen and Llama tags.
3. Prepare ten manually reviewed debugging comments: five English and five Chinese. Include a clear buff request, a clear nerf request, slang or a nickname, an emotional but specific complaint, and an ambiguous or sarcastic statement. Label synthetic examples as synthetic; keep them separate from community evidence.
4. Run both models on the same comments using `prompts/extract-feedback.txt` (archived: `~/Archives/AIMediator/prompts/extract-feedback.txt`). Replace the input placeholders and use the exact installed model tag, for example `ollama run <model-tag>`.
5. Check whether each output is valid JSON, identifies the correct character or mechanic, preserves the requested direction, and quotes evidence actually present in the input. Unknown patch details must not be invented.
6. Record model tag, prompt version, comment ID, raw output, elapsed time, and observed errors in `reports/model-smoke-test.md` (not retained).
7. Select the initial model based on observed extraction quality and acceptable runtime. Then implement the import and local inference pipeline.

Initial debugging gate: both models have been exercised on all ten comments and failures have been recorded. A suggested readiness target for the initial model is at least nine valid JSON outputs out of ten, with every retained evidence quote checked against its source. This is a debugging target, not a benchmark claim.

Keep a separate held-out evaluation set for later assessment. Do not reuse these debugging comments as independent evaluation evidence.

## Deferred work

The proposed next development sequence and acceptance criteria are in
[the next development plan](next-development-plan.md), dated October 23, 2026.

Large-scale or recurring scraping, a web interface, fine-tuning, complex retrieval, multiple games, and automatic numerical balance changes are outside the initial prototype scope. A bounded official-API feedback collector was added at the user's request; see Public feedback collection below.

## Public feedback collection

Run `python3 scripts/collect/collect_feedback.py` with Python 3.9 or later. Settings are in `configs/feedback-collection.json`; instructions, source access dependencies, rate controls, and data-retention limits are in `docs/feedback-collector.md` (not retained). The local dataset is in `data/raw/feedback/20261015-initial/`: 850 Steam reviews and 702 YouTube comments, with original text and blank review fields. Combined provisional language counts are 1,173 English and 352 Chinese, plus 27 undetermined. No content or patch filtering was performed. Bluesky anonymous search returned 403 and was stopped. YouTube collection succeeded using the user-specified `YOUTUBE_API_KEY` in the project `.env`; `--env-file .env` supports that file without global environment initialization. Bluesky collection is still incomplete. New records have unreviewed patch applicability and are not a historical August 2026 dataset. `python3 -m unittest discover -s tests -v` runs the collector checks.

## Coarse feedback screening

`python3 scripts/collect/screen_feedback.py --input data/raw/feedback/20261015-initial` produces retained counterparts of every JSONL view in `data/raw/feedback/20261015-initial/screened/` while preserving the original files. The current coarse pass retains 166 of 1,552 unique records, excludes 1,358, and separates 28 uncertain records for review. Use `screened/records.jsonl` as the canonical retained set; do not sum overlapping views. See `docs/feedback-screening.md` (not retained) for criteria, reversible exclusion reasons, boundary corrections, and limitations. This is relevance screening only; patch applicability and factual correctness remain unverified.

## Expanded balance-feedback dataset

The current expanded result is `data/raw/feedback/20261015-expanded/screened/`: 207 retained English records and 113 Chinese records after coarse screening and explicit language-label fixes, plus one separately marked Portuguese record. The previous batch is preserved. The expansion fetched 2,200 additional Steam reviews using 22 spaced official-API requests; existing YouTube material was inherited and Bluesky was not retried. See `docs/feedback-expansion.md` (not retained) for reproduction, decisions, rate controls, corrected-language provenance, and the distinction between intermediate collection goals and final retained counts.

## Grounded real-feedback pilot

`python3 scripts/experiments/run_grounded_feedback_live.py` tests local Qwen/Llama on ten real retained reviews plus two separately labeled empty controls per model. JSON Schema constrains identity and reference values; exact quotes are reconstructed from source spans. Invalid responses are quarantined and accepted outputs remain pending human semantic review. The initial run is in `reports/grounded-20261015-pilot/` (not retained); see `docs/grounded-feedback-test.md` (not retained) for the schema, source-binding checks, reproducibility, and limitations. The existing free-form synthetic smoke runner remains unchanged.

## Glossary vector retrieval

`scripts/glossary_vectors.py` builds a local cosine-search index from **all**
entries and aliases in `data/glossary.json`, using the embedding model, API URL
and API key in `.env`. Pending aliases retain their review and context metadata;
indexing does not approve them. The separate low-alias review proposals are not
imported. Build with `python scripts/glossary_vectors.py build`; query with
`python scripts/glossary_vectors.py search '隆的波掌击' --scope Ryu`.
See [index documentation](../reference/glossary-vector-index.md) for storage, resumability,
configuration and downstream RAG restrictions. The existing smoke-test runner is
unchanged and does not automatically use this vector index.

## Bilingual evidence-grounded balance summaries

Run `python3 scripts/run_balance_analysis.py --out reports/balance-v2-full`
to test the complete expanded dataset (207 English, 113 Chinese, one separately
recorded unsupported Portuguese comment). English instructions and comments go
to Llama; equivalent Chinese instructions and comments go to Qwen. Vector topic
retrieval must agree with a relevance review before a comment enters extraction.
Every admitted comment receives a coverage record. Source-bound quotations,
number checks and a separate-context semantic audit check generated details,
but semantic errors remain possible. Exact frame/damage targets are retained only
when the source actually requests them; otherwise quantities remain unspecified.
See [the pipeline documentation](../design/balance-analysis.md) for schemas,
reproduction, resume behavior, report files and evaluation limits.

The 2026-10-22 experiment admitted 197 comments, with two generation failures.
All 122 complete proposals received a separate agent source review, retaining
47 qualitative claims with explicitly labeled corrections. Local numeric
entailment controls passed 3/4; automatic output still requires source review.
The generated `reports/balance-engineering-20261022-final-review/evaluation.md`
records results and limitations; `source-reviewed-report.json` preserves the
reviewed engineering opinions alongside the unchanged raw model results.
