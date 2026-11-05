# Handoff U6: Module linkage

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-04
- Applies to: [pipeline upgrade plan](../pipeline-upgrade.md) batch U6; entry tag `upgrade-u5`

Work order for batch U6. The steps are defined in plan section 7 (U6) and
the targets in plan 4.8 to 4.10. The batch connects the unused glossary
entries to claims and reports, generates the screening patterns from the
glossary, annotates near-duplicates from the retrieval vectors, offers an
optional second audit, and replaces the namespace argument of the pipeline.

## 1. Mission

- Glossary references for claim targets and report grouping by glossary ID
  (LNK-02, UP-D12).
- An optional hint list of glossary terms in model views (UP-D12,
  conditional).
- Screening `coarse-v2` from the glossary (LNK-03, UP-D13).
- Near-duplicate clusters (ALG-05, UP-D14).
- An opt-in second audit by the other routed model (PRM-06, UP-D15).
- `RunOptions` for `pipeline.process` (LNK-05).

## 2. Entry conditions

- Tag `upgrade-u5` exists. Clean tree, no `WIP Step` stash, the gates pass.
- UP-D12 to UP-D15 are answered; a step whose decision is rejected is
  skipped.

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/(topics|pipeline|review|reporting|retrieval|quality_scoring|stages|runner|evidence|config|cli|operations|engine|fixture_transport|measurement)\.py$|src/aimediator/collection/screening\.py$|src/aimediator/assets/configs/(balance-review-policy|local-language-routing)\.json$|src/aimediator/assets/prompts/(evidence-quality|summarize-balance)\.(en|zh)\.txt$|configs/feedback-screening-terms\.json$|tests/|scripts/experiments/|reports/[0-9]{8}-upgrade-u6-evaluation/|docs/records/[0-9]{8}-pipeline-upgrade\.md$|docs/design/[a-z0-9-]+\.md$|docs/guides/cli-usage\.md$|docs/reference/glossary-vector-index\.md$)
```

- **Allowed**: the module `topics` and its layering rows (UP-D01); the
  report schema `aimediator-report-v2`; the two policy and routing assets in
  U6.5 and U6.6; prompt pairs only in U6.3; the supplemental screening
  terms; the lock fixture in B steps; design documents and the guide.
- **Not allowed**: the glossary itself (`assets/data/glossary.json`);
  existing datasets and their recorded screening decisions; any change to
  claim acceptance except through U6.6 with `second_audit` true; counts in
  reports (near-duplicates annotate only).
- **Decisions in force**: UP-D12 (U6.1 to U6.3), UP-D13 (U6.4), UP-D14
  (U6.5), UP-D15 (U6.6).
- **Owner actions**: review the screening comparison of U6.4 before its
  commit; run or authorize U6-L; decide on `second_audit` after U6-L.

## 4. Sessions

### U6-1 (implementation): steps U6.1, U6.2 and U6.7

### U6-2 (implementation): steps U6.4 and U6.5

### U6-3 (implementation): steps U6.3 and U6.6, then U6-L

All three use this prompt, with their own session ID and steps:

```text
You are session U6-<k> (implementation) of the AIMediator pipeline upgrade,
steps <list>.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/pipeline-upgrade-handoffs/u6-module-linkage.md); the plan
docs/plans/pipeline-upgrade.md, sections 1 to 5, the U6 part of section 7,
and sections 8 and 10; design/cli.md sections 5 and 8;
docs/reference/glossary.md (entry categories and alias flags); the change
record.
Task: execute your steps in order, inside the boundary of this work order.
Rules:
- Start with the plan's resume procedure. Run the gates, including the
  behavior lock, after every commit.
- One kind of operation per commit, with "Step: U6.x" and the step's
  "Decision: UP-Dnn" in the body. A B step lists the changed lock paths and
  adds its "Behavior changes" rows.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Step notes:

- **U6.1** B (LNK-02, UP-D12)
  - `topics.target_reference(target, character)` as in plan 4.8. The index
    is built once per process from `resources.glossary()` and never
    mutated. Matching uses `balance_policy.term_matches` on the target
    literal; an entry with a character scope matches only for that
    character.
  - A `candidate_only` or `requires_context` alias gives status
    `candidate`; only other aliases, canonical names and Chinese labels
    resolve.
  - The pipeline adds `target_reference` after `ground_claim`; `review`
    recomputes it and fails the proposal on a difference, like the saved
    evidence check.
  - Tests: English and Chinese literals for at least Drive Impact, Drive
    Rush, Perfect Parry and three character moves; an ambiguous alias
    stays a candidate; a move of another character stays unmatched.
- **U6.2** B (LNK-02, UP-D12)
  - `reporting.groups_for` groups resolved targets by
    (character, glossary ID) and keeps the literal grouping for the rest;
    each group lists its literals; candidates never merge.
  - `report.json` gets `schema_version` `aimediator-report-v2`, and the
    Markdown section names the glossary entry. The limitation text about
    literal grouping is updated, not removed.
  - Reports of runs without `target_reference` (earlier runs) recompute it
    at export.
- **U6.3** B (UP-D12, conditional): `mechanic_terms` (terms present in the
  comment, canonical name and matched literal) in the quality and
  extraction views; one sentence in each prompt pair. Kept only if U6-L
  shows a gain in T5 or T7 under the adoption rule; otherwise reverted.
- **U6.4** B (LNK-03, UP-D13)
  - The Chinese character pattern: glossary Chinese labels and Chinese
    aliases of `character` entries, plus the supplemental terms. The
    mechanic pattern: aliases of `system` and `mechanic` entries, plus the
    supplemental terms. Patterns are built on first use, as `_char_en`
    is.
  - `configs/feedback-screening-terms.json` holds the terms of today's
    `CHAR_ZH` and `MECH` that the glossary lacks, each with a reason.
  - Before the commit, compare `coarse-v1` and `coarse-v2` decisions on all
    raw records of `20261027-balanced` and `20261015-expanded` (offline),
    record the changed-decision counts and an agent review of up to 40
    changed records, and wait for the owner's review.
  - The screening version string becomes `coarse-v2`; lock target L4
    changes.
- **U6.5** B (ALG-05, UP-D14)
  - `retrieval` computes the cosine between comment vectors (the vectors it
    already has) and writes `near-duplicates.json`: clusters by single
    linkage at or above `near_duplicate_cosine`, with member IDs and the
    pairwise maxima.
  - Choose the threshold on the development comments of
    `extraction-precision-v1` only; record 20 sampled pairs above and 20
    just below it.
  - `balance-review-policy.json` gains the key and becomes
    `balance-review-policy-v3`; its `calibration` block is unchanged.
  - The report adds `near_duplicate_clusters` and a note that counts are
    unchanged; `quality_scoring.prepare_dataset` accepts an optional
    clusters file for split assignment.
- **U6.6** B (PRM-06, UP-D15, trial)
  - Configuration key `second_audit` (default `false`); routing asset key
    `second_audit_models` as in plan 4.10; `config.validate` accepts the
    new routing.
  - With the key set, every claim the first audit supports gets a second
    `verify` request by the other model, with the verify prompt of the
    claim's language; acceptance needs both. Artifacts keep `audit` and
    `second_audit`.
  - Default runs and the lock request digests stay unchanged except for the
    configuration and routing bytes.
- **U6.7** N (LNK-05): a `RunOptions` dataclass (out folder, base URL,
  embedding model, quality mode, relevance-only, quality-only) built by
  `operations.analyze` and `engine.run`; `pipeline.process` and the stage
  functions read it; lock unchanged.

### U6-L (live)

```text
You are session U6-L (live) of the AIMediator pipeline upgrade. You run on
the owner's machine with the local model service.
Read: RULES.md; this work order; the plan, sections 1, 4.8 to 4.10, 5 and
8.6 and the U6 part of section 7; the change record.
Task: check the environment, run the U6-L runs at HEAD, measure and score
them, apply the adoption rule to U6.3, report U6.6, archive the full runs,
and record the results in the change record and in
reports/<YYYYMMDD>-upgrade-u6-evaluation/, committed with "Session: U6-L"
in the body.
Rules: never open, print or copy .env. If the environment differs from the
U0.6 record or doctor fails, stop and report. Do not revert anything
yourself. Never add attribution.
Finish with a session-log entry; your final message repeats it.
```

Runs: `u6-benchmark-off`, `u6-benchmark-enforce`;
`u6-extraction-development-off` with `second_audit` false and true; the
archived recovery source of PRM-06 (the source of
`generation-recovery-final-new-source` in the archived run) with
`second_audit` true, as a spot check. Report the share of claims with a
resolved target reference, the number of report groups before and after
glossary grouping, the near-duplicate clusters found, and for the second
audit the precision and recall change and the added time.

Inputs (UP-D17): the benchmark and the extraction development split are
the `latency-benchmark` and `extraction-development` samples of plan 5.3;
the PRM-06 spot check is unchanged.

### U6-V (verification)

```text
You are session U6-V (verification) of the AIMediator pipeline upgrade. You
did not implement batch U6. Change nothing except the change record.
Read: RULES.md; this work order; the plan, sections 1, 2, 4.8 to 4.11, 8
and 10 and the U6 part of section 7; the change record.
Task: run every item of the U6-V checklist on HEAD, and append a
verification note committed with "Session: U6-V". If every item passes, tag
that commit upgrade-u6. Otherwise record fix-up steps U6.F1 and so on and
stop without tagging. Never add attribution. Your final message repeats the
verification note.
```

Checklist:

1. Boundary and commit hygiene from `upgrade-u5` (plan 8.8).
2. `git diff upgrade-u5..HEAD -- src/aimediator/assets/data/glossary.json data/`
   prints nothing.
3. A report export of a demo run made at `upgrade-u5` works at HEAD and
   recomputes target references; two exports of one run are
   byte-identical.
4. The U6.4 comparison and the owner's review of it are recorded before
   the U6.4 commit; L4 changed only in that commit.
5. With `second_audit` false the lock request digests are unchanged by
   U6.6.
6. Gates, foreign directory and wheel acceptance pass; the layering test
   holds the `topics` row.

## 5. Exit and handoff out

- Exit tag: `upgrade-u6`, set by U6-V.
- The next work order is [U7](u7-acceptance-and-documents.md).

## 6. Escalation triggers

- Target matching would need a semantic or fuzzy rule (out of scope: only
  exact aliases resolve).
- `coarse-v2` changes more than 5 % of decisions on either raw dataset.
- A near-duplicate threshold cannot be chosen without looking at test
  comments.
- The second audit rejects more than a third of the claims that the labels
  count as correct.
