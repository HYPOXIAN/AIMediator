# CLI implementation status

- Type: Plan (implementation status)
- Status: Active
- Updated: 2026-11-03
- Applies to: `aimediator` 0.1.0; engineering acceptance of 2026-10-28

Specification: [design/cli.md](../design/cli.md).
Engineering acceptance completed 2026-10-28. Semantic/human/patch validation
remains separate and is not declared complete.

The 2026-10-28 [directory cleanup](../records/20261028-directory-cleanup.md) removed intermediate
demo output, superseded install checks and development/build logs mentioned in
this historical acceptance record. Final verification JSON, `all-tests-final.log`,
`release-demo/`, the live diagnostic and release archives remain available.

## P0 — passed: baseline and contracts

Read the complete implementation handoff, read-first documentation and listed
production modules. No applicable AGENTS.md was present. Git metadata was empty;
it was not initialized or reconstructed.

`python3 -m unittest discover -s tests -v`: original 147 tests passed (11.396 s).
The saved repeat baseline is `reports/cli-implementation-20261028/baseline-tests.log` (archived; [manifest](../../reports/20261028-cli-implementation/manifest.json)).
Source hashes/runtime are in `source-baseline.json` in that directory. Existing
prompt/config bytes were rechecked after migration: 26 files unchanged, recorded
in `resource-preservation.json`. Historical data, frozen labels, decisions,
experimental prompts and old reports were not rewritten.

## P1 — passed: extraction, resources, installation

Added `pyproject.toml`, versioned package/console entry point and
`python -m aimediator`. Active paired prompts, policies, routing, glossary and
exact anchors have one authoritative packaged source. Checkout paths for moved
resources are compatibility symlinks; the old anchor experiment imports the
same resource. Historical frozen synthetic cases remain intact; the package
contains an explicitly hashed redistributable snapshot for its fixture demo.

Production code resolves defaults with importlib.resources. Package services
never invoke research scripts or subprocesses. Compatibility adapters execute
one authoritative implementation in adapter globals to retain existing script
patch seams/defaults. Only checkout adapters bootstrap the source path.

`python3 -m unittest discover -s tests -v`: extraction gate 147 passed (9.740 s),
`p1-tests.log`. A wheel was installed in a clean venv and imported with `python -I`
from `/tmp`; see `p1-outside-import.log`. Final wheel contents and installed module/
resource hashes are verified in `verification.json` and `package-inventory.json`.

## P2 — passed: operations and recovery

Implemented init/doctor/analyze/status, strict configuration/input validation,
explicit creation/resume, original-byte/parsed snapshots, code/resource/model/
runtime identity, sanitized configured embedding, credential-only resume,
finite durable attempt slots, atomic writes, Linux flock, state/coverage and
structured errors/progress. No implicit global config or unrelated .env read.

The final full suite command is `python3 -m unittest discover -s tests -v`:
182 tests passed (147 existing and 35 product tests), 39.921 s;
`reports/cli-implementation-20261028/all-tests-final.log` (archived; [manifest](../../reports/20261028-cli-implementation/manifest.json)).
Product checks cover no-call invalid preflight, unsupported languages, Unicode,
relocation, complete replay, model/code/config/resource/byte mismatch before
mutation, competing writers, crash consumption, exhausted repeated resume,
missing/replaced credentials, endpoint/model freezing and secret redaction.

## P3 — passed: review, reports, evaluation and demo

Implemented immutable source review with exact proposal coverage, unset reviewer
metadata, uncertain templates, original errors and source/quality revalidation.
Corrections invalidate audits in every mode. Quarantined source acceptance never
becomes automatic audit success; pending-audit proposals remain reviewable after
interruption. New products and explicit legacy v2/v3 read-only adapters validate
quality modes and retrieval/model admission independently. Unknown schemas fail.

Deterministic Markdown/JSON exports preserve conflicts, keep/unclear, literal
topics, source wording/Unicode offsets, unique comment sets, overlap, denominators,
partial status, review provenance and safe evidence rendering. The quality
adapter validates label/span/point alignment, provenance and split boundaries;
zero denominators remain null. Quality=off is rejected by evaluation.

The final suite tests these evidence boundaries and no-mutation contracts.
The packaged demo runs 38 authored bilingual cases through the actual pipeline
in all three modes using injected fixture transports, without monkeypatches or
network/model/credential requirements. Durable release examples are under
`reports/cli-implementation-20261028/release-demo/` (archived; [manifest](../../reports/20261028-cli-implementation/manifest.json)); its `example-report/` and
`review-template/` are the delivered sample report and review artifact.

## P4 — passed: clean delivery and diagnostics

Built wheel and sdist with:

```sh
python3 -c "import setuptools.build_meta as b; b.build_wheel('dist'); b.build_sdist('dist')"
```

Artifacts: `dist/aimediator-0.1.0-py3-none-any.whl` and
`dist/aimediator-0.1.0.tar.gz`. Inventory verifies packaged resources and excludes
raw community datasets, historical/private reports and credential files.
Operating instructions are [cli-usage.md](../guides/cli-usage.md); they are also included
in the source distribution. No system models were downloaded or substituted.

Three clean venvs, all without system site packages, installed the wheel outside
the checkout. Each ran 18 command checks using isolated Python, with no PYTHONPATH
and network calls denied, while unrelated credentials and an unrelated .env were
present. Each passed help/version/init/offline doctor, all-mode demo, status,
completed resume, review export/import, deterministic automatic/review reports,
quality evaluation and structured error/no-overwrite checks. Matrix:

- Python 3.14.8 / NumPy 2.5.4: `clean-install-py314-final.json`.
- Python 3.9.25 / NumPy 2.0.2: `clean-install-py39-final.json`.
- Python 3.9.25 / minimum NumPy 1.23.5: `clean-install-py39-min-numpy-final.json`.

Actual isolated command pattern (with the matching interpreter/output per row):

```sh
cd /tmp
/tmp/aimediator-clean-20261028/bin/python -I \
  <project root>/scripts/verify_cli_install.py \
  --out /tmp/aimediator-acceptance314-final182
```

The first restricted package-index attempt failed DNS; authorized network-enabled
installation of temporary test dependencies/runtimes succeeded. All outputs and
installed packages stayed in caller-owned project or temporary directories.

Default online doctor confirmed missing local `qwen3-embedding:8b`. A separate,
explicitly selected configured embedding probe succeeded. A bounded bilingual
live diagnostic then completed two authored numeric-request sources with real
local Llama/Qwen, shadow, configured remote embeddings and num_gpu=99, taking
approximately 84.1 seconds after preflight, with zero technical failure units. Raw inputs,
resolved settings, model digests, requests/responses and agent source review are
in `reports/cli-implementation-20261028/live-diagnostic/` (archived; [manifest](../../reports/20261028-cli-implementation/manifest.json)).

Both generated proposals preserve the explicit synthetic 600-to-500 request.
The Chinese quality annotation routes that concrete numerical request to
opinion_only, while English routes to mechanism_evidence. This is a semantic
classification concern, not a reason to change prompts or claim accuracy.
The real diagnostic's exact wheel is preserved as `diagnostic-build.whl` with
its hash. Later release hardening changes invalid snapshot/proposal/legacy/
quality-label validation only; model-visible prompts, routing, resources and
inference policy are unchanged. The final delivered build passes all offline
and installed-wheel gates. Its live generation was not rerun after those
validation-only changes. Configured remote weights have no verifiable digest.

## Layout decisions and remaining verification

Section 5 permits layout changes: evidence/retrieval primitives remain in the
shared engine module, with separate configuration, persistence, inference,
operations, review, reporting, evaluation and fixture services. This preserves
behavior/patch seams without introducing another engine implementation.
Linux is the supported OS. Exact runtime identity intentionally rejects resume
under changed Python/NumPy. Legacy analysis resume, review re-audit, semantic
cross-language clustering and collector/index-management commands are outside V1.

Engineering V1 commands and delivery gates are complete. Independent bilingual
human double annotation/adjudication, held-out semantic/recall/bias measurement,
source-level error analysis beyond the bounded diagnostic, patch applicability,
versioned game facts and engineering balance tests remain unfinished. Synthetic
fixtures and same-agent silver/source review are not independent accuracy.
