# AI Mediator

A local LLM research prototype for analyzing Street Fighter 6 community feedback and producing evidence-linked community consensus reports.

The installable Linux `aimediator` CLI provides explicit input analysis, bounded
resume, offline status, immutable source review, deterministic report exports,
quality evaluation and a packaged bilingual offline demo. It runs the research
analysis pipeline in-process. Default evidence quality remains `off`; examples
recommend `shadow` while independent semantic validation is outstanding.

Consensus describes the collected sample, not the entire player community or an objectively correct balance adjustment. Emotional language must not automatically invalidate a concrete gameplay concern.

## Install

Linux, Python 3.9 or later; NumPy is the only runtime dependency. From a
checkout:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install .
```

For development, install in editable mode (`pip install -e .`). Building a
wheel and source distribution, and installing the wheel outside the
checkout, are described in [the CLI guide](docs/guides/cli-usage.md).

## Quick start

These commands make no model or network calls and need no credentials:

```sh
.venv/bin/aimediator init --out ./aimediator.json
.venv/bin/aimediator doctor --config ./aimediator.json --offline
.venv/bin/aimediator demo --out ./demo-001
.venv/bin/aimediator report --run ./demo-001/enforce --out ./example-report-001
```

The demo runs 38 authored bilingual synthetic sources through the pipeline in
the `off`, `shadow` and `enforce` modes with fixture responses. Live analysis
(`aimediator analyze`) needs a local Ollama service; configuration, review,
reports and evaluation are in [the CLI guide](docs/guides/cli-usage.md).

## Scope

- Game: Street Fighter 6.
- Runtime: locally deployed Ollama.
- Models: `qwen2.5:7b` and `llama3.1:latest`; model identities are recorded per test run.
- Patch: `08.03.2026 Update`, dated August 3, 2026.
- Languages: English and Mandarin Chinese feedback.
- Current validation dataset: 600 retained comments, 300 English and 300 simplified Chinese; publication dates span multiple versions and target-patch applicability remains unverified. The earlier expanded dataset remains available.
- Deliverable: a runnable command-line tool, sample reports, and a small evaluation record.
- Development budget: six weeks at five hours per week.
- Outside the prototype scope: large-scale or recurring scraping, a web interface, fine-tuning, complex retrieval, multiple games, and automatic numerical balance changes.

Documentation is in English (RULES.md D8). Chinese appears only as corpus
content: source feedback, quoted evidence, glossary terms and aliases, and
model inputs and outputs. Original evidence must retain its meaning.

## Research commands

The research pipeline that the CLI packages is also available as package
modules and scripts, run from the project root. The modules need the checkout
package on the import path: install it with `pip install -e .`, or put
`PYTHONPATH=src` before the command.

- `python3 -m aimediator.engine`: the full-corpus balance runner.
- `python3 -m aimediator.legacy_review`, `python3 -m aimediator.quality_scoring`
  and `python3 -m aimediator.glossary_vectors`: source review of a runner
  output, quality annotation and scoring, and the glossary vector index.
- `scripts/collect/`: bounded public-feedback collection and screening.
- `scripts/experiments/`: evaluation, regression, diagnostic and live-model
  experiments.
- `scripts/maintenance/`: the rule check, its pre-commit hook and the
  clean-install verification.

New run output goes to `runs/` by default. The pipeline is described in
[balance analysis](docs/design/balance-analysis.md) and
[evidence quality](docs/design/evidence-quality.md).

## Layout

```text
AIMediator/
├── README.md            # This entry point
├── RULES.md             # Project rules
├── CLAUDE.md            # Agent entry file
├── pyproject.toml       # Package metadata
├── MANIFEST.in          # Extra sdist files
├── .env.example         # Configuration key names, no values
├── .gitignore           # Ignored locations (RULES.md G4)
├── src/aimediator/      # The package: CLI, analysis, research modules, assets
├── tests/               # Offline automated tests
├── scripts/             # Entry-point scripts, no files at this level
│   ├── collect/         # Feedback collection and screening
│   ├── experiments/     # Evaluations, diagnostics, live experiments
│   └── maintenance/     # Rule check, hook, install verification
├── configs/             # Collection settings
├── data/
│   ├── raw/             # Collected datasets (ignored; manifests tracked)
│   ├── processed/       # Glossary vector index (ignored; manifest tracked)
│   └── evaluation/      # Versioned annotation and regression sets
├── docs/                # Documentation, indexed in docs/README.md
├── reports/             # Curated results: manifests and summaries
├── runs/                # Run output (ignored, safe to empty)
└── dist/                # Current wheel and sdist (ignored)
```

- `src/aimediator/` is the only implementation. Its modules, their layers
  and contracts are in [CLI design](docs/design/cli.md), section 5. The
  collection and experiment scripts call it; the rule check runs without it.
- `src/aimediator/assets/` holds the only copy of the prompts, policies,
  routing, the glossary and fixtures. One link to it remains:
  `data/evaluation/evidence-quality-synthetic-v1/cases.json`, a member of a
  frozen evaluation set, listed in the
  [compatibility register](docs/reference/compatibility-layers.md).
- `data/raw/` is read-only source data; each dataset has a `manifest.json`.
- `reports/<name>/` keeps a `manifest.json` and a curated `summary/`; full run
  contents are in the external archive named by the manifest.
- `.env` (local only) holds credentials and is never committed; `.claude/`
  is ignored local state of the coding-agent harness.

## Documentation

The [documentation index](docs/README.md) lists every document. Core
documents:

- [CLI installation and operations](docs/guides/cli-usage.md)
- [CLI design and contracts](docs/design/cli.md) and
  [implementation status](docs/plans/cli-implementation-status.md)
- [Balance analysis pipeline](docs/design/balance-analysis.md)
- [Evidence-quality specification](docs/design/evidence-quality.md)
- [Project rules](RULES.md)

Current engineering work: the [pipeline upgrade](docs/plans/pipeline-upgrade.md),
which lowers live-analysis run time, replaces fragile algorithms and data
structures, improves the prompts and model-visible requests, and links
modules that work in isolation. It runs in batches U0 to U7, each with a
work order in `docs/plans/pipeline-upgrade-handoffs/`, and starts from tag
`upgrade-plan`, set after `restructure-done` closed the code restructuring.

## Development

```sh
python3 -m unittest discover -s tests -q
python3 scripts/maintenance/check_rules.py
git config core.hooksPath scripts/maintenance/hooks
```

The first command runs the offline test suite; live-model checks are separate
scripts. The second runs the rule check; the third enables its pre-commit
hook.

Official patch source: <https://www.streetfighter.com/6/buckler/battle_change/20260803>
