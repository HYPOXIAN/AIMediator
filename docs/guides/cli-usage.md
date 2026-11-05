# Install and operate AI Mediator

- Type: Guide
- Status: Active
- Updated: 2026-11-05
- Applies to: `aimediator` 0.1.0 (Linux, Python 3.9+)

V1 supports Linux and Python 3.9+. Install the wheel into a virtual environment;
NumPy is the only declared runtime dependency. Python 3.9.25 and 3.14.8 were
used in separate clean-install acceptance checks. The CLI works outside the
source checkout and also supports `python -m aimediator`.

```sh
python3 -m venv ./venv
./venv/bin/python -m pip install /absolute/path/to/AIMediator/dist/aimediator-0.1.0-py3-none-any.whl
./venv/bin/aimediator --help
./venv/bin/aimediator --version
```

The source distribution is `dist/aimediator-0.1.0.tar.gz`. To build from this
checkout, use a build frontend (`python -m build`), or the setuptools backend:

```sh
python3 -c "import setuptools.build_meta as b; b.build_wheel('dist'); b.build_sdist('dist')"
```

## First offline workflow

Set `CLI` to the installed executable. Every output below must be new. These
commands make no model or network calls and do not need credentials.

```sh
CLI=/absolute/path/to/venv/bin/aimediator
$CLI init --out ./aimediator.json
$CLI doctor --config ./aimediator.json --offline
$CLI demo --out ./demo-001 --quiet
$CLI status --run ./demo-001/enforce --json
$CLI review export --run ./demo-001/enforce --out ./review-template-001
```

The demo processes 38 authored bilingual synthetic sources through actual
retrieval, relevance, quality, extraction, grounding, audit, persistence and
report services using injected fixture vectors/responses. It runs `off`,
`shadow` and `enforce`. Outputs include `example-report/report.md`, its JSON,
and `review-template/decisions.json`. Fixture admission/audit decisions are
synthetic execution data, never measured semantic accuracy.

Edit the exported `decisions.json`: set `reviewer_type` to `agent` and
`reviewer_id` to your identifier for the demo. Keep uninspected decisions
`uncertain` with their reason. All complete proposals must remain covered.
Then run:

```sh
$CLI review import --run ./demo-001/enforce \
  --decisions ./review-template-001/decisions.json --out ./review-applied-001
$CLI report --run ./demo-001/enforce --review ./review-applied-001 --out ./reviewed-report-001
$CLI report --run ./demo-001/enforce --out ./automatic-report-001
```

An all-uncertain review has zero accepted claims. Importing a template with
unset reviewer metadata is an error. JSON is authoritative; the spreadsheet-safe
CSV is a reading worksheet. Report and review always write separate derived
directories, outside and not containing the source run.

## Configuration and live analysis

There is no implicit configuration or `.env` discovery. `init` writes a versioned
JSON template and refuses replacement. Unknown fields, credential-bearing URLs,
nonfinite timeouts, unsupported inference tuning and changed model routing are
rejected. Paths supplied on the CLI resolve from the invocation directory.
The V1 configuration has no file-valued resource fields; resources resolve from
the installed package, so it has no hidden relative resource paths.

The template retains English `llama3.1:latest`, Chinese `qwen2.5:7b`, local
`qwen3-embedding:8b`, temperature 0, seed 42, existing stage-specific output/context
budgets and finite timeouts. Doctor probes services, installed names/digests and
one embedding input; it never chats, downloads models or substitutes a model.
Offline doctor explicitly marks those service checks `not_checked`.

```sh
$CLI doctor --config ./aimediator.json --input ./feedback.jsonl --out ./runs/sample-001
$CLI analyze --config ./aimediator.json --input ./feedback.jsonl \
  --out ./runs/sample-001 --evidence-quality shadow
$CLI status --run ./runs/sample-001 --json
$CLI analyze --resume ./runs/sample-001
```

Input is strict UTF-8 JSONL with nonempty string `record_id`, `text_original`,
and `language`. IDs are globally unique. Supported routes are `en` and `zh`;
other nonempty language values remain in coverage without generation. Extra
collector metadata is retained. Duplicate keys, nonfinite numbers, wrong types,
empty input and unroutable-only input fail before calls or run creation. Original
input bytes and Unicode source offsets are preserved.

Quality defaults to `off`. `shadow` records annotations without changing the
existing extraction semantics. `enforce` admits only eligible mechanism points;
general opinions and system feedback remain separate. Emotion does not affect
the weight of substantive evidence. Use `--stop-after quality` with shadow or
enforce, or `--stop-after relevance` with off; `full` is the default.

To use a configured embedding service, explicitly set `embedding.provider` to
`configured`, `embedding.endpoint` to your HTTP(S) embedding endpoint,
`embedding.model` to your existing embedding model, and `embedding.credential_env`
to the credential variable name. Generation remains local and language-routed.
No remote weight digest can be locally verified. Endpoint paths ending in
`/chat/completions` are normalized to `/embeddings`, preserving the existing
configured embedding helper behavior.

```sh
# Credential must already exist in the named environment variable, or supply
# a specifically chosen credential file. The file is never sourced as shell code.
$CLI analyze --config ./configured.json --input ./feedback.jsonl \
  --out ./runs/configured-001 --evidence-quality shadow --env-file ./credentials.env
```

The explicit `--embedding-provider configured` alternative can resolve
`EMBEDDING_API_URL` and `EMBEDDING_MODEL` from environment/an explicitly chosen
file when no JSON provider settings were supplied. `--embedding-model` always
wins over an env-file model. Secrets are never saved in configuration snapshots,
request identity or routine diagnostics. No unrelated `.env` is opened.

## Recovery and identity

New analysis requires both `--input` and `--out`, with an absent output path.
Resume is explicit and freezes original bytes, parsed sources, all active
resources/code/schemas, Python/NumPy runtime, models/digests, endpoint/model,
routing, quality, stop stage and device options. An incompatible run returns 4
before mutation. There is no force override. Relocating the run is supported;
the original input file need not exist.

`--resume` accepts only `--json`, `--quiet` and credential-only `--env-file`.
The saved remote model and endpoint remain authoritative even if a replacement
credential file contains other settings. The original credential file is never
implicitly reopened. Missing required credentials return 3 before mutation.
A completed compatible run returns its existing result without generation.
Live resume still checks local installed model digests and the model service
version (`/api/version`, recorded in the run identity): after a service upgrade
or downgrade, resume returns 4, "Service version differs from saved run; start a
new run", and a new run directory is needed. Synthetic demo resume reconstructs
fixture transports and stays offline.

Each request records its exact input, raw response, validation and separate
transport attempts. Attempts are reserved before I/O; an interruption/crash
consumes that attempt. The existing bounded batch/refinement and two-attempt
quality policies remain. Configured embedding has four durable transport slots.
Failed attempts are not retried indefinitely by resume. Exhausted processing
stays partial with exit 5; another bounded trial needs a new run directory.
Partial streaming text is diagnostic, never accepted JSON. Linux `flock` permits
one writer and releases ownership after a crash. A stale `running` state is not
completion; explicit resume reconstructs outcomes from persisted requests.

## Source review and deterministic reports

Exports contain all structurally complete saved proposals, including quarantine
and pending audits from partial runs. Malformed generations remain diagnostics.
Decisions carry run/source/proposal fingerprints. Allowed corrections are
`evidence_ids`, `target`, `recommendation` and `corrected_direction`; source text,
identity and quality eligibility cannot be edited into existence.

Import rechecks grounding and quality and preserves originals/corrections.
Changed proposals lose the original audit, stay `pending_reaudit`, and appear
only in a labeled appendix. Unchanged quarantined proposals keep their automatic
failures. Source acceptance cannot manufacture automatic audit success. A later
revalidation command is outside V1. Import/report make no model calls.

Reports show automatic versus agent/human-reviewed provenance, sample/language/
platform denominators, unknown patch applicability, processing failures,
uncertainty, review queues, evidence IDs/offsets and safe links. Buff, nerf, keep
and unclear coexist per character and normalized literal target. Unknown targets
stay unresolved; no semantic/cross-language topic merging occurs. Counts use
unique comment IDs, with union/overlap information; they are not people counts
and are not additive across topics. Missing concerns are never invented by
formatting. Off is unassessed; shadow diagnostics are separate; enforce retains
opinion/mechanism/system/exclusion/review routes.

Legacy report/review inputs explicitly allow only `balance-evidence-v2`
(off/shadow) and `balance-report-v3` (enforce), with compatible saved source,
relevance, claims and quality artifacts. The reader rechecks source/quality/
audit boundaries and marks missing legacy model identity as unknown. Unknown
schemas or missing evidence return 2. Legacy runs cannot be resumed by the new
product CLI.

## Quality evaluation

Prepare labels with the research command
`python3 -m aimediator.quality_scoring prepare` (from the checkout root; see
"Research commands and validation scope" below), then explicitly
align/adjudicate points and freeze splits.
The product adapter scores the supplied labels against the specified run:

```sh
$CLI evaluate quality --labels ./annotation-template.json \
  --run ./runs/sample-001 --out ./evaluations/quality-001
```

Off has no quality predictions and is rejected. Label source hashes, provenance,
span binding, one-to-one point matches and cluster split boundaries are checked.
Human, silver, synthetic, development/test, and source/admission stages remain
separate. Zero denominators yield null metrics. Frozen-silver retrieval evaluation
remains a separate research script, not a general accuracy command.

## Output and troubleshooting

Operational leaf commands accept `--json` and `--quiet`. JSON mode emits exactly
one result, including failures; progress goes to stderr and never prints full
source/model output. Results use `command`, `status`, `artifacts`, `counts`,
`warnings`, `error_code` and `error_message`; command-specific details are separate.

Exit codes: 0 completed, 1 internal failure, 2 invalid input/config/schema,
3 unavailable dependency/service/model/required credential, 4 identity/output/
writer conflict, 5 saved partial technical processing, 130 user interruption.
Normal rejection, ambiguity, quarantine and pending source review can finish
with 0; status exposes these independently. A preflight failure creates no run.

Inspect `run-state.json`, `full-pipeline-coverage.json`, `request-trace.json` and
`requests/` for technical failures. Use `status` for offline progress. Start a new
run when inputs/code/resources/runtime/model/service identity changes or budgets are
exhausted. Export partial reports with their visible partial label. Never edit
historical snapshots or reports to make a check pass.

## Research commands and validation scope

The research commands are package modules run with `python3 -m`:
`aimediator.engine` (the full-corpus runner, with its implicit legacy resume),
`aimediator.legacy_review`, `aimediator.quality_scoring` and
`aimediator.glossary_vectors`. They keep their flags and defaults and call the
same package logic in-process. From a checkout they need the package on the
import path: `pip install -e .`, or `PYTHONPATH=src` before the command. The
scripts under `scripts/collect/` and `scripts/experiments/` put the checkout's
`src` on the path themselves. The installed CLI requires neither scripts nor
repository path hacks. Active paired prompts/policies/glossary live once in
`src/aimediator/assets`. Historical experimental resources, data, frozen
labels and reports remain unchanged.

The offline engineering gates do not establish semantic accuracy, absence of
emotion bias, community-wide consensus, patch truth or release-ready balance
values. Independent human double annotation/adjudication, held-out semantic
validation and versioned game-mechanic/engineering checks remain outstanding.
See [implementation status](../plans/cli-implementation-status.md) for actual results.
