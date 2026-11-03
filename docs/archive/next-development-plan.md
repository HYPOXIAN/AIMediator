# Next development plan

Planning date: 2026-10-23. This is a proposed development sequence, not a record of completed implementation.

## Recommended outcome

Deliver a reproducible bilingual CLI that turns a bounded feedback dataset into an evidence-linked, reviewable sample-consensus report. The next milestone is a complete and measurable analysis workflow. Concrete numerical game-design proposals remain a later milestone requiring verified patch/move data and playtesting.

## Observed starting point

- Collection, coarse screening, glossary retrieval, language routing, source binding, semantic audit, review exports and design-readiness checks already exist.
- The current dataset has 320 English/Chinese records and one unsupported-language record. Patch applicability is not established by the collection date or target-patch context field.
- The frozen v2 admission experiment admits 275 comments. v2.2 tested selected extraction cases; it did not regenerate all 275 comments.
- The recorded live diagnostic matches selected character/direction expectations in 4/6 cases. One matching case has recommendation text `capcom`; the score does not establish usable recommendation quality. Some expectations have recorded annotation disputes.
- The 100-comment reference set is agent-reviewed silver, with a frozen development/holdout split and separate errata. Independent human annotation remains outstanding.
- There are 55 exported follow-up records: 30 relevance disagreements and 25 unverified source identities. Their decisions must not be silently overwritten.
- `aggregate()` currently groups by character and buff/nerf direction. Topic-level synthesis and explicit handling of opposing opinions need a reporting contract.
- Application logic lives primarily in `scripts/`; `src/aimediator/` is a placeholder and there is no packaging manifest.
- All 94 unit tests passed again on the planning date. This validates existing code checks, not model accuracy. No fresh model inference was run for this plan.

Sources: `README.md`, `docs/meetings/20261022-work-summary.md`, `docs/plans/review-follow-ups.md`, `docs/records/20261022-balance-review-v2.md`, `reports/balance-review-v22/review-summary.md`, and the current runner/tests.

## Priority 0: define the dataset and evaluation contract

Why first: neither prompt tuning nor a polished CLI can resolve ambiguous labels or an unverified historical patch scope.

Work:

1. Choose the next report scope explicitly: a collection-period feedback analysis, or a patch-specific study. A patch-specific report must include only verified applicable evidence; keep unknown applicability visible and outside patch-specific conclusions. Preserve the existing glossary's patch identity.
2. Define labels for topic, source-literal/canonical identity, requested direction, historical versus requested changes, numeric intent and uncertainty. Separate emotional wording from the substantive gameplay concern. Sarcasm or an unclear action can legitimately require review.
3. Export a review worksheet with source IDs, original text, hashes, reasons and adjudication fields. Use the existing 55-item queue as a starting inventory. Record unresolved items rather than forcing a decision.
4. Prepare a new version for corrected annotations. Preserve silver-v1, its split, its scores and errata. Put inspected cases in development; reserve fresh unseen sources for a later evaluation and keep them out of tuning.
5. Request independent double annotation/adjudication when reviewers are available. Until then, label results as silver diagnostics and report the provenance explicitly.

Acceptance:

- A written annotation/report-scope contract and versioned dataset manifest exist.
- Every review item has a disposition or an explicit pending reason.
- Existing frozen labels and admission results remain unchanged.
- Model-only outputs, automatic gate outcomes and reviewer corrections are scored separately.

## Priority 1: measure and improve extraction quality

Why next: `capcom` passing the current diagnostic exposes a gap between pair matching and useful extraction.

Work:

1. Extend the diagnostic to assess meaningful recommendation text, correct attribution, direction/action consistency, source support and appropriate abstention. Report separate dimensions rather than one character/direction pass rate.
2. Keep explicit requests, inferred opinions and unresolved statements distinct. Preserve complaints containing gameplay information even when hostile. Do not infer a numerical change, an official identity or a buff/nerf direction from emotional intensity.
3. Cover system-wide feedback as its own topic so avoiding a false character assignment does not silently erase a substantive Drive-system concern.
4. Use the existing historical failures and fresh bilingual development examples for prompt/constraint changes. Preserve disputed expectations as historical diagnostics; assess corrected interpretations in a new evaluation version.
5. Compare the current baseline with one candidate change at a time. Keep routing/models fixed initially so effects are attributable. Consider a model or retrieval change only if the observed errors justify a separate experiment.

Acceptance:

- Addressee-only text cannot count as a valid recommendation.
- Explicit unambiguous requests are retained; genuinely ambiguous statements can abstain without being rewritten into definite actions.
- The reviewed development outputs contain no accepted unsupported numerical target or unverified canonical identity; all detected violations remain quarantined or pending.
- Report omissions and unnecessary abstentions alongside false acceptance, so rejecting everything cannot appear to be an improvement.
- Preserve raw outputs and provenance; reviewer repairs never increase the reported raw-model score.

## Priority 2: complete one end-to-end reporting experiment

Work:

1. After the preceding checks, run the current corpus with the selected extraction/audit configuration in a new experiment directory. Treat 275 admissions as the frozen baseline, not an invariant for a fresh relevance run. If reusing frozen admissions, add an explicit import-and-hash contract; offline admission replay alone is not extraction.
2. Account for every input and admitted comment: unsupported language, rejected/pending relevance, extraction complete with/without claims, or generation failure. Account for every generated claim through source binding, audit and review outcomes.
3. Add a readable Markdown report alongside JSON. Group evidence by character/system and concrete topic; show supporting and opposing directions, uncertainty and provenance.
4. Count distinct comments per topic/direction and display denominators by language/source. A comment may contain multiple claims; do not present claim counts as independent voters. Do not label sampled support as community-wide prevalence.
5. Review all proposed numeric changes, identity ambiguities and known failure categories, plus a documented sample of ordinary outputs. Save source-bound decisions separately.
6. Record runtime, failure counts and review workload. Reuse compatible caches and test interruption/resume without overwriting prior experiments.

Acceptance:

- Every input and every admitted comment has one explicit final coverage status; every generated claim has a traceable outcome.
- Every retained report claim links to exact original evidence and its review status.
- System concerns and conflicting opinions remain visible; unresolved names stay outside verified character groups.
- A complete run, its manifest and its reviewed sample report can be reproduced or resumed.
- Report model-only quality, gated quality and reviewed quality separately, with evaluation-set provenance.

## Priority 3: package the established workflow as a CLI

Work:

1. Move stable shared logic incrementally into `src/aimediator/`; keep existing scripts as compatibility entry points while preserving behavior.
2. Add packaging, pinned experiment metadata and installation instructions. Expose a small command surface for analysis, evaluation, review export/import and report export.
3. Add a preflight check for local models, dependencies, input paths and configuration; provide clear progress, failure messages and exit codes.
4. Include a small distributable fixture, a reproducible demonstration and a documented review workflow. Existing ignored datasets/reports must not be the only evidence needed to understand the demo; confirm redistribution rights before including real source text.

Acceptance:

- A clean environment can install the project and run the fixture through the documented commands.
- Invalid configuration fails before expensive inference; partial runs resume under the existing identity checks.
- Existing tests pass and a CLI integration check covers the supported workflow. Live semantic diagnostics remain separate from offline code tests.

## Suggested effort and sequencing

Using the README's five-hours-per-week capacity as an assumption, time-box an initial four-week iteration to approximately 20 developer hours:

1. Week 1, 5 hours: scope/annotation contract, review worksheet and evaluation criteria.
2. Week 2, 5 hours: diagnose recommendation/attribution/abstention errors and evaluate one focused candidate.
3. Week 3, 5 hours: complete the full run and a minimal topic/conflict report with source review records.
4. Week 4, 5 hours: package the minimum CLI and a reproducible demo; close documentation gaps.

This is a proposed capacity allocation, not a promise of completion. Independent human review and local inference wall time are additional dependencies. If quality work exceeds its time box, reduce packaging scope or extend the schedule; retain the evaluation and coverage gates. Human-review delays do not prevent worksheet, CLI or report-format work, but they do prevent claims of independently established semantic accuracy.

## Defer until the evidence supports it

- Larger or recurring collection: first measure errors and review cost on the existing corpus.
- Additional RAG complexity: first attribute misses to retrieval versus relevance, extraction, identity or patch scope. Preserve development-only calibration.
- Web UI, multi-game support and fine-tuning: revisit after the CLI/report workflow has a reproducible evaluation.
- Numerical tuning recommendations: require verified versioned game data, resolved identities, source review and actual design/playtest validation. Existing readiness checks remain in force.

## First implementation task

Extend `scripts/experiments/run_balance_regression_live.py` and its offline tests with a versioned multi-dimensional extraction assessment. Start with the existing Manon addressee-only output, the explicit Arjun nerf request, disputed sarcasm and the Drive-system source. Preserve the historical 4/6 diagnostic unchanged and emit new quality dimensions separately. This gives the next prompt experiment a meaningful success criterion before spending time on another full run.
