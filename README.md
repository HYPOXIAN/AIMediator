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

See [CLI installation and operations](docs/guides/cli-usage.md),
[implementation status and verification](docs/plans/cli-implementation-status.md), and
[the implementation specification](docs/design/cli.md). The sections
below retain the research history and compatibility commands.


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
