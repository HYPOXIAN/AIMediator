# AI Mediator

AI Mediator is a command-line research tool. It reads English and Chinese
player comments about a Street Fighter 6 balance patch and writes a
community consensus report. For each character and move, the report counts
the distinct comments that ask for a buff, a nerf or no change, and links
every entry to the exact sentence a player wrote. It is meant for
researchers and game designers who want to see what a sample of players
asked for, and on what evidence. The language models run locally through
Ollama.

The tool keeps only on-topic comments, separates venting from concrete
gameplay points, checks every extracted claim against the source text, and
reports a numerical change only when a comment asks for one. The counts
describe the collected sample, not the whole player community or a correct
balance adjustment. Emotional language does not by itself invalidate a
concrete gameplay concern.

The [project report](docs/records/20261105-project-report.pdf) (PDF, 8
pages) describes the goals, the design, the experiments and the results.

## Status and limits

- AI Mediator 0.1.0 is a research prototype, not a production tool.
- On the held-out test split, 59.4% of the accepted claims were correct and
  the tool found 26.8% of the labeled positions. Chinese results trail
  English ones.
- The evaluation labels were written by an AI agent, not by people, so
  these figures are bounds, not proof.
- The final evaluation used a hosted model (`deepseek-v4-flash` through an
  API), because local 7–8B models were too slow and unreliable on an 8 GiB
  GPU. The package still defaults to local Ollama models.

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

The modes control the evidence-quality filter. `off`, the default, runs no
filter. `shadow` records the quality annotations without changing the
result. `enforce` turns only concrete gameplay points into formal claims
and lists general opinions and system feedback separately.

## Example output

An excerpt of `example-report-001/report.md`, the report of the `enforce`
run in the quick start. The content is synthetic: the demo's comments were
written for testing, and fixture responses stand in for the models. The
file is Markdown source; `[...]` marks omitted lines.

```text
# SF6 collected-sample feedback

Processing completed.

View: automatic; quality: enforced.
Execution: agent_authored_synthetic_fixture_transports. Semantic accuracy: not established.
Scope: collection_sample. Patch applicability: unknown.
Input comments: 38. Formal unique comments: 18.
[...]
### Ryu — Hadoken / 波动拳 (glossary ryu\.hadoken)
[...]
**nerf**: 4 distinct comments

- Please reduce Ryu&\#x27;s Hadoken damage from 600 to 500\. ([synthetic:numeric\_request:en](https://example.test/synthetic))
  - [synthetic:numeric\_request:en/E1](https://example.test/synthetic) source Unicode [0,51): Please reduce Ryu&\#x27;s Hadoken damage from 600 to 500\.
- 请将隆的波动拳伤害从600降低到500。 ([synthetic:numeric\_request:zh](https://example.test/synthetic))
  - [synthetic:numeric\_request:zh/E1](https://example.test/synthetic) source Unicode [0,20): 请将隆的波动拳伤害从600降低到500。
```

## Live analysis

`aimediator analyze` needs a running [Ollama](https://ollama.com) service
with three models: `llama3.1:latest` for English comments, `qwen2.5:7b` for
Chinese comments, and the embedding model `qwen3-embedding:8b`. Pull each
one with `ollama pull` and the model name. The configuration written by
`aimediator init` names these models, and the tool does not substitute
another model. Configuration, recovery, review, reports and evaluation are
in [the CLI guide](docs/guides/cli-usage.md).

## Scope

- Game: Street Fighter 6, the
  [08.03.2026 Update](https://www.streetfighter.com/6/buckler/battle_change/20260803)
  of August 3, 2026.
- Languages: English and Mandarin Chinese feedback.
- Validation data: 600 retained comments, 300 English and 300 simplified
  Chinese. Their publication dates span several game versions, and whether
  each comment applies to the target patch is not verified.
- Outside the scope: large-scale or recurring scraping, a web interface,
  fine-tuning, complex retrieval, multiple games, and automatic numerical
  balance changes.

## Data

The repository contains the manifests of the collected datasets (source,
record count, hashes), the versioned evaluation sets in `data/evaluation/`,
and curated result summaries in `reports/`. It does not contain the raw
collected comments: `data/raw/` holds only their manifests. The evaluation
sets keep the text of real public comments, without links to their
authors' accounts. To analyze new feedback, collect your own with
`scripts/collect/` and your own API keys (see "Collection keys" below).

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
  See "Collection keys" below.
- `scripts/experiments/`: evaluation, regression, diagnostic and live-model
  experiments.
- `scripts/maintenance/`: the rule check, its pre-commit hook and the
  clean-install verification.

New run output goes to `runs/` by default. The pipeline is described in
[balance analysis](docs/design/balance-analysis.md) and
[evidence quality](docs/design/evidence-quality.md).

### Collection keys

The collectors in `scripts/collect/` call the official Steam, Bluesky and
YouTube endpoints. Steam needs no key. The other keys are read from the
environment; `.env.example` lists their names.

- `YOUTUBE_API_KEY`: a YouTube Data API v3 key, needed to collect YouTube
  comments. `collect_feedback.py --env-file <file>` and
  `collect_balanced_feedback.py` (default file `.env`) load it from a local
  file.
- `GOOGLE_API_KEY`: a fallback for `YOUTUBE_API_KEY`, read from the
  environment by `collect_feedback.py` only.
- `BLUESKY_ACCESS_TOKEN`: optional. With it, Bluesky search goes to
  `bsky.social` with the token; without it, to the public endpoint
  `public.api.bsky.app`.

The embedding keys (`EMBEDDING_MODEL`, `EMBEDDING_API_KEY`,
`EMBEDDING_API_URL`) are described in the
[glossary vector index reference](docs/reference/glossary-vector-index.md).

## Layout

```text
AIMediator/
├── README.md            # This entry point
├── RULES.md             # Project rules
├── LICENSE              # MIT License
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

- [Project report](docs/records/20261105-project-report.pdf) (PDF): goals,
  design, experiments and conclusions of the project
- [CLI installation and operations](docs/guides/cli-usage.md)
- [CLI design and contracts](docs/design/cli.md) and
  [implementation status](docs/plans/cli-implementation-status.md)
- [Balance analysis pipeline](docs/design/balance-analysis.md)
- [Evidence-quality specification](docs/design/evidence-quality.md)
- [Project rules](RULES.md)

## Development

```sh
python3 -m unittest discover -s tests -q
python3 scripts/maintenance/check_rules.py
git config core.hooksPath scripts/maintenance/hooks
```

The first command runs the offline test suite; live-model checks are separate
scripts. The second runs the rule check; the third enables its pre-commit
hook.

## License

The code is released under the [MIT License](LICENSE).

The comment text in `data/evaluation/` belongs to its authors. It is
included only for research evaluation and is not covered by the license.
The glossary content comes from the sources listed in its `sources` field:
Capcom's official pages and community references.

Not affiliated with or endorsed by Capcom. Street Fighter is a trademark of
Capcom.
