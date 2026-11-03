# AI Mediator

A local LLM research prototype for analyzing Street Fighter 6 community feedback and producing evidence-linked community consensus reports.

The installable Linux `aimediator` CLI provides explicit input analysis, bounded
resume, offline status, immutable source review, deterministic report exports,
quality evaluation and a packaged bilingual offline demo. It uses the existing
Python engine in-process. Default evidence quality remains `off`; examples
recommend `shadow` while independent semantic validation is outstanding.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install dist/aimediator-0.1.0-py3-none-any.whl
.venv/bin/aimediator init --out ./aimediator.json
.venv/bin/aimediator doctor --config ./aimediator.json --offline
.venv/bin/aimediator demo --out ./demo-001
.venv/bin/aimediator report --run ./demo-001/enforce --out ./example-report-001
```

See [CLI installation and operations](docs/cli-usage.md),
[implementation status and verification](docs/cli-implementation-status.md), and
[the implementation specification](docs/cli-design-handoff.md). The sections
below retain the research history and compatibility commands.

Directory cleanup on 2026-10-28 removed superseded experiments, intermediate
datasets, build caches and obsolete logs. Current validation results, release
archives, active tests and datasets required by compatibility commands remain.
See [the cleanup record](docs/directory-cleanup.md) for deleted paths and retained
dependencies; historical references below do not imply every old run is on disk.

## Scope

- Game: Street Fighter 6.
- Runtime: locally deployed Ollama.
- Models: `qwen2.5:7b` and `llama3.1:latest`; model identities are recorded per test run.
- Patch: `08.03.2026 Update`, dated August 3, 2026.
- Languages: English and Mandarin Chinese feedback.
- Latest validation dataset: 600 retained comments, 300 English and 300 simplified Chinese; publication dates span multiple versions and target-patch applicability remains unverified. The earlier expanded dataset remains available.
- Deliverable: a runnable command-line tool, sample reports, and a small evaluation record.
- Development budget: six weeks at five hours per week.

The repository uses English for code, comments, documentation, and field names. Chinese text is allowed in Chinese model debugging inputs and source feedback; original evidence must retain its meaning.

Consensus describes the collected sample, not the entire player community or an objectively correct balance adjustment. Emotional language must not automatically invalidate a concrete gameplay concern.

## Layout

```text
AIMediator/
├── README.md
├── pyproject.toml
├── src/aimediator/       # CLI, engine and packaged resources
├── configs/             # Collection settings and policy compatibility links
├── data/
│   ├── raw/             # Source evidence and active collection datasets
│   ├── processed/       # Published glossary vector index
│   └── evaluation/      # Frozen labels, regression cases and pending annotation
├── docs/
├── notes/
├── prompts/             # Legacy prompts and packaged-resource links
├── scripts/             # Research and compatibility commands
├── tests/               # Active automated regression checks
├── dist/                # Current wheel and source release
└── reports/             # Retained baselines, final validation and release examples
```

- `src/aimediator/`: installable engine, CLI services and authoritative packaged resources.
- `data/raw/`: original feedback with comment IDs, sources, language, and patch context.
- `data/processed/`: cleaned data and model extraction results.
- `prompts/`: compatibility paths; active paired prompts point to the packaged resources.
- `reports/`: evaluation records and generated community reports.

The command-line retrieval, bilingual extraction and evidence-audit pipeline is
available in `scripts/run_balance_analysis.py` (Python and numpy). The original
standard-library debugging runner remains in `scripts/run_smoke_test.py`.

## Bilingual glossary

`data/glossary.json` contains universal Street Fighter 6 vocabulary plus character-specific names for all 31 playable characters available at the target patch, including Yasmine. System, Mechanic, Tactic, Input, and Normal Move categories apply to all characters. Normal-move labels never imply Ryu by default. `docs/glossary.md` provides a readable collection, source notes, integration guidance, and review status. English canonical names and notes are used; Chinese terms are language data. Future Arjun, Tifa, and Bosch are excluded from this experiment version. The original ten-case debugging suite remains Ryu-only and cannot establish extraction quality for the expanded roster.

The collection has 849 concepts, 3822 alias mappings, and 82 ambiguous alias records. All human review fields remain blank. `docs/alias-review.md` groups the 1582 retained new mappings (775 distinct text/language pairs) with sources and context restrictions: 225 observed community candidates, 174 historical candidates, and 1183 generated spelling/notation variants. `data/raw/glossary/community-aliases-20261008.json` preserves the original collection snapshot. User exclusions are recorded in `data/glossary.json`; removed aliases are absent from the active glossary and review sheet. The smoke-test runner supplies these as candidates with `--glossary`; pending nicknames do not establish hard character scope. It preserves ambiguity and does not replace the original comment.

Chinese feedback scope is simplified Chinese only. Traditional Chinese aliases and community sources have been removed. For Chinese community comments, bare CA normalizes to the SA3 move family; an enhanced Critical Art variant is inferred only from explicit variant context. Original comment wording remains unchanged.

The original ZH02 synthetic case conflated a collarbone move name with Solar Plexus Strike. The repeat run intentionally retains this conflict to inspect uncertainty handling. Its provisional expected label must not be treated as an unquestioned semantic answer; use a corrected dataset version for future accuracy evaluation.

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
4. Run both models on the same comments using `prompts/extract-feedback.txt`. Replace the input placeholders and use the exact installed model tag, for example `ollama run <model-tag>`.
5. Check whether each output is valid JSON, identifies the correct character or mechanic, preserves the requested direction, and quotes evidence actually present in the input. Unknown patch details must not be invented.
6. Record model tag, prompt version, comment ID, raw output, elapsed time, and observed errors in `reports/model-smoke-test.md`.
7. Select the initial model based on observed extraction quality and acceptable runtime. Then implement the import and local inference pipeline.

Initial debugging gate: both models have been exercised on all ten comments and failures have been recorded. A suggested readiness target for the initial model is at least nine valid JSON outputs out of ten, with every retained evidence quote checked against its source. This is a debugging target, not a benchmark claim.

Keep a separate held-out evaluation set for later assessment. Do not reuse these debugging comments as independent evaluation evidence.

## Deferred work

The proposed next development sequence and acceptance criteria are in
[the next development plan](docs/next-development-plan.md), dated October 23, 2026.

Large-scale or recurring scraping, a web interface, fine-tuning, complex retrieval, multiple games, and automatic numerical balance changes are outside the initial prototype scope. A bounded official-API feedback collector was added at the user's request; see Public feedback collection below.

## Unique move alias review

All 244 Unique Move entries across the 31 target-patch characters have overhead or direction/button aliases. Review `docs/unique-move-alias-review.md` for inputs, conditions, and blank decisions. Capcom live properties were checked on October 8, 2026; historical August 3, 2026 behavior remains pending verification. Evidence and the change audit are saved in `data/raw/glossary/unique-move-reference-20261008.json` and `data/raw/glossary/unique-move-aliases-20261008.json`.

## Public feedback collection

Run `python3 scripts/collect/collect_feedback.py` with Python 3.9 or later. Settings are in `configs/feedback-collection.json`; instructions, source access dependencies, rate controls, and data-retention limits are in `docs/feedback-collector.md`. The local dataset is in `data/raw/feedback/20261015-initial/`: 850 Steam reviews and 702 YouTube comments, with original text and blank review fields. Combined provisional language counts are 1,173 English and 352 Chinese, plus 27 undetermined. No content or patch filtering was performed. Bluesky anonymous search returned 403 and was stopped. YouTube collection succeeded using the user-specified `YOUTUBE_API_KEY` in the project `.env`; `--env-file .env` supports that file without global environment initialization. Bluesky collection is still incomplete. New records have unreviewed patch applicability and are not a historical August 2026 dataset. `python3 -m unittest discover -s tests -v` runs the collector checks.

## Coarse feedback screening

`python3 scripts/collect/screen_feedback.py` produces retained counterparts of every JSONL view in `data/raw/feedback/20261015-initial/screened/` while preserving the original files. The current coarse pass retains 166 of 1,552 unique records, excludes 1,358, and separates 28 uncertain records for review. Use `screened/records.jsonl` as the canonical retained set; do not sum overlapping views. See `docs/feedback-screening.md` for criteria, reversible exclusion reasons, boundary corrections, and limitations. This is relevance screening only; patch applicability and factual correctness remain unverified.

## Expanded balance-feedback dataset

The current expanded result is `data/raw/feedback/20261015-expanded/screened/`: 207 retained English records and 113 Chinese records after coarse screening and explicit language-label fixes, plus one separately marked Portuguese record. The previous batch is preserved. The expansion fetched 2,200 additional Steam reviews using 22 spaced official-API requests; existing YouTube material was inherited and Bluesky was not retried. See `docs/feedback-expansion.md` for reproduction, decisions, rate controls, corrected-language provenance, and the distinction between intermediate collection goals and final retained counts.

## Grounded real-feedback pilot

`python3 scripts/experiments/test_grounded_feedback.py` tests local Qwen/Llama on ten real retained reviews plus two separately labeled empty controls per model. JSON Schema constrains identity and reference values; exact quotes are reconstructed from source spans. Invalid responses are quarantined and accepted outputs remain pending human semantic review. The initial run is in `reports/grounded-20261015-pilot/`; see `docs/grounded-feedback-test.md` for the schema, source-binding checks, reproducibility, and limitations. The existing free-form synthetic smoke runner remains unchanged.

## Glossary vector retrieval

`scripts/glossary_vectors.py` builds a local cosine-search index from **all**
entries and aliases in `data/glossary.json`, using the embedding model, API URL
and API key in `.env`. Pending aliases retain their review and context metadata;
indexing does not approve them. The separate low-alias review proposals are not
imported. Build with `python scripts/glossary_vectors.py build`; query with
`python scripts/glossary_vectors.py search '隆的波掌击' --scope Ryu`.
See [index documentation](docs/glossary-vector-index.md) for storage, resumability,
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
See [the pipeline documentation](docs/balance-analysis.md) for schemas,
reproduction, resume behavior, report files and evaluation limits.

The 2026-10-22 experiment admitted 197 comments, with two generation failures.
All 122 complete proposals received a separate agent source review, retaining
47 qualitative claims with explicitly labeled corrections. Local numeric
entailment controls passed 3/4; automatic output still requires source review.
The generated `reports/balance-engineering-20261022-final-review/evaluation.md`
records results and limitations; `source-reviewed-report.json` preserves the
reviewed engineering opinions alongside the unchanged raw model results.

The next review iteration adds a frozen 100-comment agent silver set, versioned
identity policy, retrieval review queue, actual-error regressions and separate
engineering-design prerequisites. See [review v2](docs/balance-review-v2.md) and
[decisions and follow-ups](docs/review-todo.md). The v2 evaluation uses full-corpus
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

## 评论证据质量与情绪干扰控制

新增 `--evidence-quality off|shadow|enforce`（默认 off）和 `--quality-only`。
相关性放行后按原文片段与信息点分流为无关/纯发泄、一般意见、角色机制、
系统反馈和待复核；纯情绪篇幅只作诊断，不改变有信息评论的资格或权重。
一般意见不能支撑具体招式/数值设计。enforce 仍执行既有身份、原文、数值、
来源复核及版本数据门槛，off/shadow 保留旧下游语义。

运行与回滚均使用新目录，例如：
`python3 scripts/run_balance_analysis.py --evidence-quality shadow --out reports/quality-shadow-new`；
回滚改为 `--evidence-quality off --out reports/quality-rollback-new`。
无模型可运行 `python3 scripts/experiments/demo_evidence_quality.py --mock-pipeline --out reports/quality-demo-new`。
详见 [实现、命令、产物及未验证事项](docs/evidence-quality-implementation.md)。
独立人工效果验证尚未完成，当前推荐 shadow；合成测试与小规模真实诊断不代表准确率。

## Fresh balanced validation (October 27, 2026)

The new canonical dataset is
`data/raw/feedback/20261027-latest-balanced/screened/records.jsonl`: 600 retained
Steam reviews, with 300 English and 300 simplified-Chinese records after
fingerprinted language corrections. Collection restarted from latest-sorted
streams without seeding old files, but meeting the retained quota reaches back
to December 2025 for English and August 2026 for Chinese. It is not a set of 600
posts published today. Existing raw evidence and provisional selections remain
available.

See [collection, full-run commands and diagnostic scope](docs/latest-balanced-validation.md).
The active bilingual extraction and source-verification prompts now require a
complete subject/action recommendation, preserve conditional and negated intent,
keep clause-local subjects, and reject unrelated numbers as tuning targets.
`--embedding-provider configured` supports the already configured embedding
service; `--num-gpu` records explicit placement. The full default run and its
separate controls live under `reports/latest-balanced-20261027/`. Completion,
quarantine and failure counts are read from the resulting reports, never assumed
from an in-progress run. The 600-comment default run uses evidence-quality=off;
quality integration has separate live diagnostics and offline tests.
