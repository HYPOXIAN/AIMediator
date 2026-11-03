# CLI demonstration

The input contains 50 original comments: 25 English and 25 Chinese. Matching

Use the current checkout through `./cli`. Python 3 and the project dependencies
(including NumPy) must be available to `python3`. Ollama must already be running
at `http://127.0.0.1:11434` with `llama3.1:latest` (English), `qwen2.5:7b`
(Chinese), and `qwen3-embedding:8b` (retrieval) installed.

```bash
cd <project root>/cli-demo
DEMO_RUN="$(python3 -c 'import json; print(json.load(open("run-location.json"))["operational_run"])')"
DEMO_SESSION="$PWD/sessions/$(date +%Y%m%d-%H%M%S)-$$"
mkdir -p "$DEMO_SESSION" &&
./cli doctor --config live-config.json --input input.jsonl --offline --json &&
./cli doctor --config live-config.json --input input.jsonl --json &&
./cli analyze --config live-config.json --input input.jsonl \
  --out "$DEMO_RUN" --json &&
./cli report --run "$DEMO_RUN" \
  --out "$DEMO_SESSION/automatic-report" --json > /dev/null &&
./cli evaluate quality --run "$DEMO_RUN" --labels labels/annotation-template.json \
  --out "$DEMO_SESSION/evaluation" --json
```

Analysis performs real local inference and can take time. Routine progress is
hidden. On success, it prints only `提取结果`, `相关性测试`, `质量测试`, and
`最终结论`. `分析完成` is true only for a completed full analysis. Relevance
covers 50 input comments; quality/extraction counts depend on admission decisions
and need not equal 50. Claim counts and recommendations depend on the run.

The report command saves `report.md` and `report.json` under
`$DEMO_SESSION/automatic-report`. Its terminal output is redirected to avoid
repeating the final conclusions. Evaluation prints a `质量测试` result and saves
`evaluation.json` under `$DEMO_SESSION/evaluation`. With the supplied templates,
expect `labeled_comments=0`, `unlabeled_comments=50`, `groups={}`, and
`independent_effectiveness_established=false`. Independent relevance/quality
accuracy has not been established; accuracy fields remain null.

The operational run, including evidence and request records, is saved outside
this directory at `$DEMO_RUN` (initially `reports/cli-demo-50` under the project
root). No step requires `precomputed-run`, `RESULTS.md`, archived runs, or old
partial reports. `run-location.json` supplies the initial path; its state fields
are setup metadata and are not updated by analysis. Actual state is saved in
`$DEMO_RUN/run-state.json`.

## Resume or repeat

Ctrl+C retains completed requests and partial results. Fix any failure before
resuming. In the same shell, resume using the saved run and output controls only:

```bash
./cli analyze --resume "$DEMO_RUN" --json
```

Do not add `--input`, `--out`, or `--config` to resume. The saved model,
configuration, resource, and code identities are checked. Resume does not reset
exhausted request attempt budgets. Interrupted/partial output is not a completed
conclusion. Exit 130 means interrupted; exit 5 means technical failures remain.

After successful resume, create a new `DEMO_SESSION` using the assignment and
`mkdir` above, then rerun report and evaluation. Output destinations are never
overwritten. For a separate fresh analysis, assign unused paths below, then rerun
the checks, analysis, report, and evaluation commands without reloading `DEMO_RUN`
from `run-location.json`:

```bash
DEMO_RUN="$PWD/../reports/cli-demo-50-$(date +%Y%m%d-%H%M%S)-$$"
DEMO_SESSION="$PWD/sessions/$(date +%Y%m%d-%H%M%S)-$$"
```

## Optional source-review workflow

After successful analysis, the existing review export/import workflow remains
available in the same shell and makes no model calls. The helper marks every
proposal uncertain with an agent identity; it does not inspect sources or accept
claims. Proposal counts depend on the run and are not fixed at zero.

```bash
./cli review export --run "$DEMO_RUN" \
  --out "$DEMO_SESSION/review-template" --json &&
python3 prepare-review.py "$DEMO_SESSION/review-template/decisions.json" \
  "$DEMO_SESSION/uncertain-decisions.json" &&
./cli review import --run "$DEMO_RUN" \
  --decisions "$DEMO_SESSION/uncertain-decisions.json" \
  --out "$DEMO_SESSION/review-applied" --json &&
./cli report --run "$DEMO_RUN" --review "$DEMO_SESSION/review-applied" \
  --out "$DEMO_SESSION/reviewed-report" --json
```

Only the report prints a `最终结论` result. This all-uncertain overlay has zero
formally accepted claims; it demonstrates the interface and is not a completed
human review. Importing the original template without reviewer identity fails
with exit 2. Reusing an output path fails with exit 4. Deliberate error
examples are omitted from the normal sequence.

## Optional offline fixture demonstration

This separate built-in check uses 38 authored synthetic records across `off`,
`shadow`, and `enforce`. It needs no Ollama service, does not analyze the
50-comment input, and does not establish semantic accuracy. Run it separately
using an unused output path:

```bash
./cli demo --out "$DEMO_SESSION/offline-demo" --quiet --json
```

It prints the four business categories grouped by quality mode. Successful
`init`, `doctor`, `status`, review export/import, and preparation helpers are
silent through this demonstration entry point; version/help output is hidden.
`--json` selects business JSON here, rather than the standard CLI operational
envelope. Necessary errors still appear on stderr with their original exit codes.
The normal sequence excludes file listings, raw report previews, shell statistics,
and exit-code echoes to keep terminal output limited to the business results.
