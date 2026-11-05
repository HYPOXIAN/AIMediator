# Pipeline Upgrade Validation

- Type: Record
- Status: Active
- Updated: 2026-11-05
- Applies to: commit `b73f0e9` (tag `upgrade-u6`, the code of the adopted configuration) through the API bridge `openrouter-bridge-2`; `upgrade-samples-v1/latency-benchmark`, the `balance-silver-v1` holdout and the `extraction-precision-v1` test split; `RULES.md` v1.4

The acceptance measurements of the [pipeline upgrade](../plans/pipeline-upgrade.md)
(steps U7.1 and U7.2), with their denominators and intervals, the targets
of plan section 5.5 with their measured values, and the limits of these
readings. The execution, the decisions and the escalations are in the
[change record](20261104-pipeline-upgrade.md) (section "U7-L"); the
curated measurements are in
[`reports/20261105-upgrade-acceptance/`](../../reports/20261105-upgrade-acceptance/manifest.json);
the full runs are archived in
`~/Archives/AIMediator/reports/20261105-upgrade-acceptance/`.

## 1. What was measured

The adopted configuration is the code at `b73f0e9`: the request views of
U2.1 to U2.4 with the payload test of U2.6, bounded concurrency and the
shared cache of U3, the clause segmentation code of U4.1 to U4.3 (unused
by the pipeline after the E-4 reverts, ADR
[0006](../decisions/0006-revert-of-quality-annotation-v2.md)), the
evidence-first claim order of U5.1 (U5.2 and U5.3 reverted after the U5
review), and the module linkage of U6.1, U6.2, U6.4, U6.5 and U6.7.
Skipped by the owner's decision UP-D20: the response-template trial (U2.5
with U2-L2), the mechanic terms in the views (U6.3) and the second audit
(U6.6). The conditional quality budget step U4.6 was skipped by its own
condition.

Run settings (decision D-16 of the change record, adopted under the
owner's authorization): `runs/upgrade/live-config-api.json`
unchanged, `max_parallel_requests` 2, a new empty `cache_dir` per run (no
request was reused), quality `off` or `enforce`. Every chat request went
through the bridge of plan 5.4 to `deepseek/deepseek-v4-flash` on
DeepInfra, for both routed model names (UP-D19); embeddings to
`qwen/qwen3-embedding-8b`. The identity check passed for every run.

| Run | Step | Set | Mode | Inputs | Wall time | Cost |
| --- | ---- | --- | ---- | ------ | --------- | ---- |
| `u7-benchmark-off` | U7.1 | `upgrade-samples-v1/latency-benchmark` | `off` | 30 | 43.9 s | 0.0039 USD |
| `u7-benchmark-enforce` | U7.1 | `upgrade-samples-v1/latency-benchmark` | `enforce` | 30 | 155.9 s | 0.0075 USD |
| `u7-silver-holdout-off` | U7.2 | `balance-silver-v1` holdout | `off` | 30 | 37.3 s | 0.0044 USD |
| `u7-extraction-test-off` | U7.2 | `extraction-precision-v1` test | `off` | 74 | 124.8 s | 0.0138 USD |

Each holdout and test split ran once, here and nowhere else (plan rule
1.11). Coverage is complete in every run: each input row has exactly one
coverage record. Every run ends `partial` because 1 to 3 comments stay
relevance-pending, as in every reference run (escalation E-7).

## 2. U7.1: the benchmark sample

References are API runs of the same model (UP-D19): `u2l0-benchmark-off`
and `u2l0-benchmark-shadow` (the U0.8 code through the API) and
`u6-benchmark-off` (the latest accepted run). Token figures are means per
request, uncached in parentheses; intervals are Wilson 95 % for
proportions and Newcombe 95 % for differences of proportions.

| Measure | `u7-benchmark-off` | `u2l0-benchmark-off` |
| ------- | ------------------ | -------------------- |
| Technical failure units; pending units | 0; 3 | 0; 1 |
| Admitted comments | 23 of 30 | 26 of 30 |
| Claims generated / accepted | 11 / 8 | 14 / 8 |
| Audit rejected | 3/11 (27.3 %, 9.7–56.6 %) | 6/14 (42.9 %, 21.4–67.4 %) |
| Precision of accepted claims (11 labeled comments) | 4/6 (66.7 %) | 4/6 (66.7 %), difference 0.0 points (−43.6 to +43.6) |
| Recall (10 labeled positions) | 4/10 (40.0 %) | 4/10 (40.0 %) |
| Extraction prompt tokens | 2,788 (2,642) | 4,064 (3,771) |
| Relevance prompt tokens | 1,474 (1,154) | 1,571 (1,539) |
| Retrieval-review prompt tokens | 1,353 (1,046) | 1,314 (1,314) |

Per comment, the accepted (character, direction) positions of the two
runs are equal on all 30 comments; 3 comments admitted by the reference
are not admitted here. Against `u6-benchmark-off`, admission, coverage
status and accepted positions are equal on all 30.

| Measure | `u7-benchmark-enforce` | `u2l0-benchmark-shadow` |
| ------- | ---------------------- | ----------------------- |
| Quality-failed comments; pending units | 2; 3 | 3; 1 |
| Quality first-attempt validity | 21/24 (87.5 %, 69.0–95.7 %) | 23/26 (88.5 %, 71.0–96.0 %) |
| Quality prompt tokens; output tokens | 1,926 (1,263); 667 | 3,469 (2,692); 782 |
| Quality elapsed per comment | 9.7 s | 18.3 s |
| Comments reaching extraction; accepted claims | 1; 0 | 26; 8 |

In `enforce` only comments with a `mechanism_evidence` route reach
extraction. On this sample that is 1 comment, which yields no supported
claim; the labeled positions sit in comments routed `opinion_only`, which
the `enforce` report shows as general opinions. The formal claims view of
`enforce` is therefore empty on this sample (recall 0/10 against 4/10 in
`shadow`). This is the designed contract, not a failure.

## 3. U7.2: the holdout and the test split

**`balance-silver-v1` holdout** (30 comments, agent silver labels).
Relevance agreement 27/29 (93.1 %, 78.0–98.1 %): 25 true positives, 2
true negatives, 2 related comments not admitted, 0 unrelated comments
admitted, 1 uncertain label excluded; English 15/15, Chinese 12/14. The
development split gives 64/69 (92.8 %) with the same relevance request
(U2-L1) and 63/69 (91.3 %) with the U0.8 code (U2-L0). The selected
character expectations of 7 comments (not exhaustive, so recall only) are
found by accepted claims in 5 of 7 (71.4 %, 35.9–91.8 %); the 2 misses
are the source literal `source:Arjun`, which is not a roster identity and
cannot be claimed by design.

**`extraction-precision-v1` test split** (74 comments, 72 scored, 2
labeled uncertain):

| Measure | Test split | Development, U5-L1 (114) | Difference (Newcombe 95 %) |
| ------- | ---------- | ------------------------ | -------------------------- |
| Precision of accepted claims | 19/32 (59.4 %, 42.3–74.5 %) | 58/77 (75.3 %) | −15.9 points (−35.0 to +2.5) |
| Precision of generated claims | 41/68 (60.3 %) | 74/113 (65.5 %) | −5.2 points (−19.6 to +8.9) |
| Recall | 19/71 (26.8 %, 17.9–38.1 %) | 58/123 (47.2 %) | −20.4 points (−32.9 to −6.2) |
| Audit rejected | 35/69 (50.7 %, 39.2–62.2 %) | 40/119 (33.6 %) | — |
| English precision; recall | 10/12; 10/17 | 30/33; 30/46 | — |
| Chinese precision; recall | 9/20; 9/54 | 28/44; 28/77 | — |

U5-L1 is the last accepted development run with the extraction request
of the adopted configuration. Against the API reference before the
upgrade (`u2l0-extraction-development-off`, 76.2 % and 48.8 %) the test
split is −16.9 and −22.0 points. The loss is mostly Chinese; the test
split holds 76 % of its labeled positions in Chinese (development 67 %).
The work order's second escalation trigger fired (E-8): the result is
recorded and nothing was tuned. One run of one configuration cannot tell
a harder split from overfitting; the only prompt changes made against the
development sample (U4.F1, U5.2, U5.3) were reverted, and the pre-upgrade
reference scores as far above the test split as the adopted code does.

## 4. Targets of plan 5.5

Targets through the API keep the ratio of the plan's targets to their
U0.6 baselines (plan 5.4); baselines are the U2-L0 runs. Elapsed-time
targets (T4, T8) are indicative under UP-D19.

| ID | Metric | Baseline | Target | Measured (adopted configuration) | Met |
| -- | ------ | -------- | ------ | -------------------------------- | --- |
| T1 | Extraction: mean uncached prompt tokens per request | 3,771 (`u2l0-benchmark-off`) | at most 1,882 (49.9 %) | 2,642 (70.1 %), `u7-benchmark-off`; 2,788 in total against 4,064 | no |
| T2 | Quality: mean uncached prompt tokens per request | 2,692 (`u2l0-benchmark-shadow`) | at most 1,933 (71.8 %) | 1,263 (46.9 %), `u7-benchmark-enforce`; also below the plan's 1,500 | yes |
| T3 | Relevance: mean uncached prompt tokens per request | 1,539 (`u2l0-benchmark-off`) | at most 1,000 (65 %) | 1,154 (75.0 %), `u7-benchmark-off` | no |
| T4 | Quality: mean elapsed per comment | 18.3 s (`u2l0-benchmark-shadow`) | at most 9.2 s (50 %) | 9.7 s (53.1 %), `u7-benchmark-enforce`, with 2 parallel requests | no (indicative) |
| T5 | Quality: first-attempt validity | 88.5 % (23/26) | at least 95 % | 87.5 % (21/24, 69.0–95.7 %), `u7-benchmark-enforce` | no |
| T6 | Extraction: share of audited claims rejected, development | 38.8 % (52/134, `u2l0-extraction-development-off`) | at most 35 % | 33.6 % (40/119), U5-L1 on the development sample; test split 50.7 % (35/69) | yes on development; not on the test split |
| T7 | Extraction: precision of accepted claims, development; recall within 3 points | 76.2 % and 48.8 % (`u2l0-extraction-development-off`) | precision at least 86.2 %, recall at least 45.8 % | 75.3 % and 47.2 %, U5-L1; test split 59.4 % and 26.8 % | no (precision); recall held on development |
| T8 | Quality-stage throughput with 2 parallel requests | U3-L run with 1 | at least 1.4 times | 1.25 times (U3-L) | no (indicative) |
| T9 | Synthetic 600-comment fixture run: share of `run_store.state` | 54 % (59.4 % measured in U1) | below 5 % | 7.7 % (1.40 s of 18.2 s profiled; 14.4 s plain), at `b73f0e9` | no |
| T10 | Offline demo time; share of `character_reference` | 1.07 s; 35 % | at most 1.0 s; below 10 % | 0.98 to 0.99 s; 7.5 to 7.6 % (plan 8.4 order), at `b73f0e9` | yes |

T9 and T10 were measured in this session on the owner's machine (Python
3.14.8, run folder on tmpfs). U1 measured T9 at 5.4 % and T10 at 0.63
to 0.65 s; later batches added work to every run (target references,
near-duplicates), which the demo and the fixture run now include.

## 5. Limitations

- **Hosted model, not the routed local models.** Every live reading
  describes `deepseek/deepseek-v4-flash` answering both routed names
  (UP-D19). The package still routes to `llama3.1:latest` and
  `qwen2.5:7b`; the readings carry over only as far as those models
  behave alike. The local U0.6 and U0.8 rows are history and decide
  nothing.
- **Agent silver labels.** `extraction-precision-v1` and
  `balance-silver-v1` were labeled by agents from the source text; they
  are not independent human gold. The silver character expectations are
  selected, not exhaustive.
- **Same-model audit.** The claim audit uses the same hosted model that
  generated the claims; the second audit (UP-D15) was skipped (UP-D20),
  so audit errors are not decorrelated.
- **Sample sizes.** U7.1 accepts on 30 comments (UP-D18) with 11 labeled
  benchmark comments; the holdout has 30 comments and 7 with
  expectations; the test split 72 scored comments. Most differences have
  intervals wider than the effects they would show.
- **Elapsed times** measure the provider and the network; with 2
  parallel requests a request's elapsed time includes the provider's
  sharing. T4 and T8 are indicative.
- **Uncached token figures** depend on the provider's prompt cache,
  shared across runs; the totals are given beside them.
- **Pending and failed units** (E-7): 1 to 3 relevance-pending comments
  per run and 2 quality-failed comments in `enforce`.
- **Test split** (E-8): precision and recall well below development,
  mostly in Chinese; not tuned.
