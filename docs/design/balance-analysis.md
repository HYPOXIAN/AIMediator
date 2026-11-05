# Evidence-grounded bilingual balance analysis

- Type: Design
- Status: Active
- Updated: 2026-11-05
- Applies to: balance pipeline `aimediator.engine` (`python3 -m aimediator.engine`); dataset `data/raw/feedback/20261015-expanded`

The current full-corpus test runner is `python3 -m aimediator.engine`, run from
the project root. Like `python3 -m aimediator.legacy_review` below, it needs the
checkout package on the import path: `pip install -e .`, or `PYTHONPATH=src`
before the command. It uses all records in the expanded canonical screened
dataset, not the historical 50-comment retrieval sample or the 32-comment
direction experiment.

## Prompts and routing

- `src/aimediator/assets/prompts/summarize-balance.zh.txt`: Chinese instructions for `qwen2.5:7b`.
- `src/aimediator/assets/prompts/summarize-balance.en.txt`: equivalent English instructions for `llama3.1:latest`.
  The `subjects` definition (pipeline upgrade step U5.2) and the authored
  synthetic examples (step U5.3) were reverted after the review of batch
  U5 (fix-up steps U5.F2 and U5.F1 of the
  [change record](../records/20261104-pipeline-upgrade.md)); the pair
  holds neither.
- `src/aimediator/assets/prompts/relevance.{zh,en}.txt` and `retrieval-review.{zh,en}.txt`: topic-agreement review before extraction. Each ends with a line that introduces the topic list; `resources.prompts` appends the twenty anchors of `retrieval-anchors.json` after it, `P1: <text>` to `N10: <text>`, so the anchors keep one source (pipeline upgrade step U2.4, UP-D07).
- `src/aimediator/assets/prompts/verify-balance.{zh,en}.txt`: claim entailment audit after extraction.
- `src/aimediator/assets/configs/local-language-routing.json`: model, language, and prompt assignments.

Descriptions follow the original language; JSON keys, direction enums and
normalized character names are shared. Original comments are never translated
or rewritten. Unsupported languages are recorded and excluded from generation.
The earlier single-comment smoke/pilot prompts remain available for reproducing
those experiments; they are not used by the new batch pipeline.

## Run and resume

```sh
python3 -m aimediator.engine --out runs/balance-v2-full
python3 -m unittest discover -s tests -v
python3 scripts/experiments/run_balance_controls_live.py --out runs/balance-v2-full/synthetic-controls
```

Run the same command again to resume. Completed requests are content-addressed
and reused. The manifest checks the dataset, prompt texts, routing, glossary,
code, anchors and installed model digests. Changed inputs require a new output
directory. Python 3.9+, numpy and the three installed Ollama models are required.
New requests save streamed partial output for diagnosis. A run of excessive
whitespace or repeated comment IDs is rejected; failed extraction batches are retried individually.
Request failures and final unprocessed comments are counted separately.
No cloud service, new data collection or additional package installation is used.
The separate control command tests two requested numerical changes and two
numerical coincidences in English/Chinese. Its synthetic sources are explicitly
labeled and never included in community counts or the engineering report.
The compatibility command `run_local_direction_comparison.py` invoked this
full pipeline, with `--run-name` selecting a new run directory under `runs/`
(default `local-direction-comparison`). Note (2026-11-03): archived on
2026-11-03, code restructuring step B1.7; it had stopped working when the
evidence-quality stage was added.

## Admission before judgment

1. Embed all routed comments and the existing ten positive and ten negative
   combat-balance topic prototypes with local `qwen3-embedding:8b`. Save the exact
   inputs and vectors. No comment is truncated.
2. Retrieve the nearest topic descriptions by cosine similarity. As in the
   previous experiment, compare mean top-three positive similarities with mean
   top-three negative similarities. Positive must be strictly greater; ties fail.
3. Ask the language-routed generation model to review each retrieval-positive
   comment against the retrieved topics. This stage makes no balance suggestions.
   The request carries the comment ID and text and, per retrieved topic, its
   `topic_id` and cosine rounded to 4 decimals; the topic texts are in the
   system prompt. `retrieval.json`, `relevance.json` and the review queue keep
   the full topic references (step U2.4).
4. Recheck batch rejections and uncertainty individually, retaining both results.
   This prevents an initial batch-level mistake from silently becoming final.
5. Only vector-positive **and** model-related **and** model-not-uncertain comments
   enter extraction. Rejected or unresolved comments remain in `relevance.json`.

To limit local decoding time, relevance returns one status per input in order;
the semantic audit returns one explicit supported/unsupported/uncertain label
for one claim in a dedicated request. It reads the full original comment, with
the proposed gameplay fields separated from confidence and provenance metadata. The schemas
require exactly the input count, and the program binds positions back to the
immutable IDs. These stages provide verdicts without generated explanations;
the saved requests retain the complete sources and their input order.

These are topic prototypes, not established factual game rules. The threshold
was not tuned against the new corpus. This run does not establish retrieval
precision/recall without independently reviewed reference labels.

## Output and engineering specificity

Extraction requests show the model a view of the batch (pipeline upgrade
step U2.3, UP-D05; [ADR 0003](../decisions/0003-model-visible-request-views.md)):
evidence units with `evidence_id` and `text` but no offsets, the character
reference entries with a candidate in a comment of the batch, and in
`enforce` the allowed quality points with their evidence IDs, quotes and
labels instead of the whole routing entry. Source binding, the identity
rules and the response schema read the full program context, so every claim
still binds to the original offsets and the output files keep their shape.
The payload test bounds the non-comment part of every request
([CLI design](cli.md), section 5).

The model receives full comments and immutable evidence units in bounded
batches. Extraction sends all original text through the ordered evidence units
without duplicating the full comment a second time. An 8,192-token context and
smaller batches keep the installed models within the local GPU memory budget.
It must account for every admitted comment exactly once. There is no
three-claim limit. The runner checks strict JSON, rejects duplicate keys and
nonfinite values, validates required keys/types/enums, requires complete item-ID
coverage, and quarantines incomplete generation.

Each extracted claim contains, in this order, `evidence_ids`, `character`,
`target`, `direction`, `recommendation`, `specificity`, `parameters` and
`uncertain`: the model selects the supporting units before it names the
subject (evidence-first order, pipeline upgrade step U5.1, UP-D11). The
order reaches the model through the response schema; the duplicate-claim
loop guard recognizes claims by the first claim property of the request's
schema. Readers key claims by name, so stored claims of either order stay
readable, and review fingerprints sort keys.
Each numerical parameter contains `metric`, `current`, `proposed`, `delta`,
`unit`, and its own `evidence_id`. Unknown quantities are JSON null. All non-null
value strings retain exact source spelling, including number words.
At the model boundary, `assessments` is an object whose unique required keys are
the exact input comment IDs; each value contains only a claims array. The
`subjects` array and its source-binding gate of step U5.2 were reverted
after the review of batch U5 (fix-up step U5.F2; escalation E-5 of the
[change record](../records/20261104-pipeline-upgrade.md)). The runner
derives coverage status and normalizes the output into coverage records.
This schema prevents repeated comment IDs from replacing other input records.

`source_numeric` means the source actually asks for a numerical adjustment.
An existing statistic or a description of an old patch is not a target value.
Without a numerical request, `parameters` is empty and `specificity` is
`qualitative_only`. For example, "Ryu is too strong" can support a broad nerf
request; it cannot justify inventing a damage reduction or a frame change.
A request for exact values cannot be satisfied from qualitative source data
without an additional, explicitly labeled engineering-design step.

No character adjustment is fabricated from general-system feedback. Such
comments and unresolved identities stay in coverage as
`no_supported_character_claim`. The program derives this status from an empty
claims array; it does not claim an independent semantic judgment. Keep opinions
and unclear directions remain separately available rather than being forced
into a fighter's buff/nerf group. Pending aliases
cannot establish identity alone. Character names outside the supplied glossary
remain unresolved rather than being normalized to an unrelated known fighter.

## Source checks and their limits

The program reconstructs every quotation from a selected evidence ID, binds it
to the same immutable comment, and saves original Unicode offsets and source URL.
It rejects unsupported number tokens (including signs), nonexistent references,
unknown characters and inconsistent numerical fields. Each comment schema
restricts characters to name/alias candidates actually present in that source;
without any candidate, the model must return an empty claims array. Candidate
presence is not proof of identity or sentiment, especially for pending aliases.
Model-written quote text
is never accepted in place of the original span.

A second call, in a separate context, audits whether the complete original text entails the
whole recommendation: subject, mechanic, direction, conditions and the role of
all quantities. Unsupported or uncertain claims are quarantined before
aggregation. This call uses the same language-routed model as extraction, so it
is an automated semantic check with correlated error risk, not an independent
human annotation or proof of gameplay truth. Exact quotation alone does not
prove entailment. The test suite includes a deliberately wrong numerical claim
whose numbers happen to occur in the source, documenting why this audit matters.

The final `balance-report.json` is built deterministically from accepted claims.
It groups by character and buff/nerf direction, retains each source-specific
recommendation and opposing views, and counts distinct comment IDs per group.
It does not manufacture a merged numerical consensus. Repeated comments or
multiple accounts cannot be inferred to be independent people. Patch
applicability and the factual truth of reviewer assertions remain unverified.

Measured limits of the adopted pipeline (pipeline upgrade, steps U7.1 and
U7.2, through a hosted model that answered both routed model names; the
[validation record](../records/20261105-pipeline-upgrade-validation.md)
has the denominators and intervals). On the `extraction-precision-v1`
test split, run once, 59.4 % of the accepted (character, direction)
claims match a labeled position and 26.8 % of the labeled positions are
found, against 75.3 % and 47.2 % on the development split; the loss is
mostly in Chinese comments, and half of the audited claims are rejected
(50.7 %). The labels are agent silver labels, and the audit uses the same
model as extraction, so these figures bound the pipeline only as far as
those labels and that model go.

## Report files

- `balance-report.json`: strict JSON engineering report, grouped adjustments and coverage.
- `validated-claims.json`: claims that passed both source binding and model semantic audit.
- `quarantined-claims.json`: failed claims and explicit reasons.
- `relevance.json`: retrieval scores, retrieved references and agreement decisions.
- `summary.json`: corpus counts, stage counts, failures and limitations.
- `requests/`: exact prompts, response schemas, requests, raw responses and checks.
- `manifest.json`, `source-snapshot.json`, `prompt-snapshot.json`: reproducibility records.

Automatic completeness means every admitted comment was assessed. It does not
prove that every individual gameplay concern was recognized correctly. Inspect
raw sources, no-adjustment decisions and quarantined claims before using results
as a release plan.

## Separate full-source review

The automated verifier sees the full original comment, with the proposed action
separated from confidence and provenance metadata. It can still make shallow
entailment judgments, admit unsupported opinions or reject genuine requests.
Keep the raw model reports as the experimental record.
For a separate agent or human review, inspect each complete proposal against the
full original comment and save fingerprinted decisions in
`source-review-decisions.json` with `reviewer_type` explicitly `agent` or `human`.

```sh
python3 -m aimediator.legacy_review \
  --run runs/<run> \
  --decisions runs/<run>/source-review-decisions.json
```

The 2026-10-22 engineering review ran this command on
`reports/balance-engineering-20261022-final-review`, now archived as
`20261022-balance-engineering-review`
([manifest](../../reports/20261022-balance-engineering-review/manifest.json)).

The review must cover every complete proposal. It can add exact original context
or clarify action wording. Character identity cannot change. A direction repair
requires an explicit `corrected_direction` field, a written reason and a labeled
correction retaining the original model direction; it is not counted as an
automatically correct model result.
Changed proposals invalidate existing decisions. All retained wording, numbers
and quotations are checked against the original spans again. Outputs are
`source-reviewed-report.json`, `source-reviewed-claims.json` and
`source-review-exclusions.json`; model reports remain unchanged. Context and
wording revisions are labeled, and unassigned admitted comments retain their
complete original text. An agent review is not human ground truth.

The completed experiment also saves `source-review-supplement.json`. It separately
records source-only agent reviews of explicitly named Arjun/`阿俊` feedback omitted
by the older glossary, and numerical system requests that must not be assigned
to one fighter. These are labeled as agent additions, never counted as successful
Qwen/Llama outputs. The official identity and patch applicability of names outside
the glossary remain unverified; nationality-only nicknames are not normalized.

The current runner includes the [v2 review policy](../records/20261022-balance-review-v2.md). Its
retrieval review queue can rescue vector-negative candidates only after an
affirmative retrieval-topic review and separate relevance agreement. The
original v1 experiment remains historical and cannot resume under changed code.
