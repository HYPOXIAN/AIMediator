# 0002 Module boundaries and research entry points

- Type: Decision
- Status: Active
- Updated: 2026-11-04
- Applies to: `aimediator` 0.1.0 from code restructuring batch B4; `RULES.md` v1.3
- Owner decisions CR-D05, CR-D06, CR-D07 and CR-D08 of the code
  restructuring; the execution is recorded in the
  [change record](../records/20261103-code-restructuring.md).

## Context

[ADR 0001](0001-package-as-single-runtime.md) made the package the single
runtime implementation. Three things still held the code in its pre-package
shape:

- **The `engine` hub.** `engine.py` had 931 lines. It held the Ollama
  client, JSON-schema construction, evidence segmentation, the
  content-addressed request journal (`Runner`), embedding retrieval, the
  orchestration of a run, report assembly and the legacy command line.
  Seven package modules imported it; `inference` did so only to reach three
  helpers, and `demo` and `operations` imported each other.
- **Patch seams.** The CLI design planned separate `pipeline`, `retrieval`
  and `evidence` modules, but the primitives stayed in `engine.py` because
  tests replaced its module globals (`api`, `streamed_chat`, `retrieve`).
  Moving a function would have left those patches on a name that nothing
  calls any more.
- **Compatibility layers.** Six pure forwarding scripts directly under
  `scripts/` and 18 symlinks in `prompts/`, `configs/` and `data/` kept the
  pre-package paths working. Tests and experiment scripts imported the
  forwarders through `sys.path`. Experiment identities hashed the
  forwarders' few lines instead of the implementation, so they could not
  detect a code change. The active prompts, policies, routing and glossary
  each had a second path.

## Decision

1. **Modules by responsibility.** `engine.py` is split by pure moves;
   `engine` keeps only the legacy research runner (`ROOT`, `run`, `main`).
   The modules form layers. A module imports only from its own layer or the
   layers below it, never in a cycle.
2. **An enforced dependency table.** The intra-package imports each module
   may make, first set out in the code restructuring plan (sections 4.1 and
   4.2), are held in `TABLE` in
   [tests/test_module_layers.py](../../tests/test_module_layers.py). The
   test parses every module, imports inside functions included, and fails on
   an import the table does not allow and on any cycle. `__init__.py`
   imports nothing from the package. A change to the table is a decision
   recorded with the change, and the test changes in the same commit.
3. **Injection instead of patching.** Callers and tests pass transports and
   services in, for example `engine.run(args, api_transport=...,
   chat_transport=..., embed_transport=..., retrieval_service=...)` and
   `Runner(..., chat_transport=...)`, and never patch module globals of
   moved functions.
4. **Research commands are package modules** (CR-D05):
   `python3 -m aimediator.engine`, `python3 -m aimediator.legacy_review`,
   `python3 -m aimediator.quality_scoring` and
   `python3 -m aimediator.glossary_vectors`, with the forwarders' flags and
   defaults. Scripts in `scripts/collect/` and `scripts/experiments/` put
   the checkout's `src` on `sys.path` and import `aimediator` modules.
5. **The compatibility layers are removed** (CR-D05, CR-D07). The six
   forwarders and the 18 symlinks are deleted. Code reads every resource
   through `resources.asset_path()`, and `src/aimediator/assets/` holds the
   only copy. One registered link stays:
   `data/evaluation/evidence-quality-synthetic-v1/cases.json`, a member of a
   frozen evaluation set (CR-D08). `RULES.md` v1.3 removes `prompts/` from
   the G3 allowlist.

The layers:

| Layer | Modules |
| ----- | ------- |
| Interfaces | `cli`, `presentation`, `__main__` |
| Services | `operations`, `review`, `legacy_review`, `reporting`, `evaluation`, `quality_scoring`, `demo`, `engine` (legacy research runner) |
| Orchestration | `pipeline` |
| Infrastructure | `inference`, `runner`, `retrieval`, `run_store`, `fixture_transport` |
| Domain | `evidence`, `evidence_quality`, `stages` |
| Foundation | `common`, `schema`, `resources`, `config`, `balance_policy`, `glossary_vectors` |
| Research (planned for batch B6) | `design_briefs`, `diagnostics`, `collection.*`; outside the CLI path and outside CLI run identities |

## Consequences

- **Run identities.** Experiment identities hash the package modules
  (`package_code_sha256`) and the assets they read (`asset_sha256`) instead
  of forwarders and links (CR-D06). Experiment output made before that
  change cannot be resumed under its old identity; the owner confirmed that
  none must be. CLI run identities hash the top-level package modules as
  before (`run_store.code_manifest`), so a run made before the split cannot
  resume under the new code, as after any code change.
- **Editable install.** The `python3 -m` commands need the checkout package
  on the import path: `pip install -e .`, or `PYTHONPATH=src` before the
  command. Their defaults resolve against the working directory, so they
  run from the project root.
- **Historical paths in frozen documents.** Frozen records, decisions,
  meeting notes, the archive and curated reports keep the removed script
  and link paths as history (CR-D07; `RULES.md` D3, P1, P2). Those paths no
  longer exist in a checkout. Git history and the archive copies named in
  the change record hold the removed files. Living documents name the
  package commands and the asset paths.
- **Changing the structure.** A new module or import edge needs a recorded
  decision and a change to the layering test, which fails otherwise. The
  [compatibility register](../reference/compatibility-layers.md) lists the
  one remaining link; a new compatibility layer needs a row there (G2).
- Product behavior, prompts, assets and the CLI commands did not change:
  the behavior lock stayed green through the split and the removals.
