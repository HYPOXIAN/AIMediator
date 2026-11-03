# Fresh balanced feedback validation

Completed: 2026-10-27T20:18:07.183245-07:00 (America/Los_Angeles).

## Collection and coarse screening

Fresh official-API collection: 6,376 source records. Coarse decisions: {'exclude': 5552, 'review': 202, 'keep': 622}. Final canonical set: 600 comments, English 300 and simplified Chinese 300; all 600 selected records are Steam reviews.
Actual request counts across collection/resumption: {'steam': 63, 'bluesky': 1, 'youtube': 5}. Bluesky returned HTTP 403 and stopped; YouTube material did not enter the final corrected sample.
Source publication range, UTC: English 2025-12-26T23:04:27+00:00 to 2026-10-24T20:37:21+00:00; Chinese 2026-08-03T09:11:37+00:00 to 2026-10-27T17:15:03+00:00.
This is a fresh retrieval from latest-sorted streams, not 600 newly published replies. 277 selected IDs also appeared in the previous expanded raw dataset; no old files were used to seed this collection. Configured source types are Steam reviews and YouTube top-level comments; nested forum replies were not collected.
Exact normalized-text duplicates were removed. Language-label errors and the traditional-Chinese film discussion were handled with fingerprinted agent source reviews; original raw text/labels remain unchanged. Language heuristics and targeted inspection do not establish a fully human-verified language corpus.
Frozen canonical dataset SHA-256: `3eb87a7561b41ff31cef3e7035f0a25353adbe1999e023ff5e46b1bcf4852e3f`.

## Full 600-comment program test

Mode: full pipeline, evidence-quality=off (the existing default). All 600 inputs were embedded and routed: English to local Llama and Chinese to local Qwen. Embeddings use the previously configured Qwen3 service; no locally verifiable weight digest is available for that remote embedding model.
Retrieval/relevance agreement: 525; assessed comments: 525; generated claims: 404; accepted after source/semantic checks: 187; quarantined: 217.
Failed requests: 7; final extraction-failed comments: 2. Coverage statuses: {'extraction_completed': 523, 'relevance_rejected': 52, 'relevance_pending_or_failed': 23, 'extraction_failed': 2}.
Separate bounded recovery of the INITIAL run's one failed source: 0/1 produced valid generation; 1 remain failed within that retry scope. Recovery accepted 0 claims after the unchanged source and semantic gates. The current-code run has 2 failures, reported above; this older retry count is not its failure total. Supplemental runs do not overwrite full-run counts or establish independent semantic accuracy.
Audit of the newly failed final-run source: its initial four generated claims were all quarantined, and neither full run accepted a claim from it. See generation-failure-audit.json. One separate bounded retry of this source: {"original_failed_comments": 1, "generation_recovered": 1, "still_failed": 0}. It does not replace the full-run outcome.
IMPORTANT supplemental semantic failure: the retry produced valid JSON, but its 10 automatically accepted claims wrongly attribute World Tour progression/difficulty, generic Drive Impact complaints or optimization praise to Ryu adjustments. Agent source review rejects the entire supplement; none are merged into the primary 187 claims. The same-model verifier missed these errors. This demonstrates a material semantic limitation rather than a successful source recovery; see generation-recovery-final-new-source/agent-source-review.json.
Additional isolated recovery trials used temperature 0.4 and, once, a bounded 2,048-token strict-JSON trial that delayed the early repeated-claim abort. Neither recovered the long source; no partial output or repaired JSON was admitted. Every request and failed attempt remains available.
By language: {'en': {'input': 300, 'retrieval_related': 164, 'agreement_related': 244, 'accepted_claims': 87}, 'zh': {'input': 300, 'retrieval_related': 238, 'agreement_related': 281, 'accepted_claims': 100}}.
Summed request-processing elapsed time, including failed attempts and excluding collection/embedding: 40.9 minutes. Replayed responses have negligible transport time, so this is not a fresh-inference throughput benchmark. Stage detail: {'retrieval_review': {'requests': 87, 'elapsed_seconds': 0.055830961020546965}, 'relevance': {'requests': 160, 'elapsed_seconds': 0.101003300085722}, 'extract': {'requests': 157, 'elapsed_seconds': 2397.418214393023}, 'verify': {'requests': 387, 'elapsed_seconds': 54.965041585957806}}.
Integrity: 20/20 assertions passed. Covers exact source snapshots, language counts, deduplication, every admitted comment's accounting, exact accepted source spans, claim accounting, numerical source checks and isolation of unverified character identities.
After the first full-corpus run, a decoder-schema consistency fix removed impossible null-only numeric parameters when no requested value/delta is available. All 184/184 initially accepted claims were replay-validated and all eight live semantic controls rerun. The selected full-corpus result is full-pipeline-final; it executes the current code on all 600 inputs. Exactly identical model-visible requests may reuse recorded results, while changed schemas/messages/options require fresh inference. It is not 600 wholly independent fresh generations. Transport counts: {'counts': {'reused_identical_model_request': 603, 'fresh_inference': 188}, 'by_stage': {'retrieval_review': {'reused_identical_model_request': 87}, 'relevance': {'reused_identical_model_request': 160}, 'extract': {'fresh_inference': 122, 'reused_identical_model_request': 35}, 'verify': {'reused_identical_model_request': 321, 'fresh_inference': 66}}, 'note': 'Reused results are not fresh inference; all changed model requests were executed, and every response was validated by current code.'}.
Passing source checks does not establish that player claims are true. Same-model semantic audits have correlated error risk. Accepted claims still require source review and versioned game data before engineering use.

## Prompt changes and paired diagnostic

The active bilingual prompts are prompts/summarize-balance.{en,zh}.txt and prompts/verify-balance.{en,zh}.txt. The final report is aggregated deterministically; there is no separate free-form final-summary LLM prompt.
The revised extraction prompts require a complete subject/action sentence, distinguish conditional threats from opposition to nerfs, preserve attacker/victim and clause-local subjects, separate system from character opinions, preserve restrictions and reject numbers occurring only in insults, jokes, prices, playtime or unrelated comparisons. The verifier checks the whole recommendation instead of accepting a correct direction label with meaningless text.
Six known-case regressions, with the same frozen runner/model configuration and frozen expectations: baseline 4/6, final 4/6. Their overall pass count did not improve. The revised prompts repair the publisher-only recommendation and the conditional nerf threat; an insulting numeric expression is still misread and blocked, and one attacker complaint does not pass semantic review. These known debugging cases are not an independent accuracy benchmark; unchanged legacy expectations can also be disputed.
Numeric entailment controls: pipeline 4/4, model-only 4/4. End-to-end numeric extraction: 2/2. Synthetic controls never enter community counts.

Bilingual semantic controls: 8/8, covering negated nerfs, conditional nerf threats, attacker/victim attribution and system versus roster clauses. These are synthetic diagnostics, not a real-source accuracy estimate.

Per-case baseline/final recommendations and outcomes:

- steam:229094178 (explicit_buff): baseline pass=True, final pass=True.
  Baseline: [{"character": "Manon", "direction": "buff", "recommendation": "capcom", "source_errors": [], "audit": "supported"}]
  Final: [{"character": "Manon", "direction": "buff", "recommendation": "buff Manon", "source_errors": [], "audit": "supported"}]
- steam:229292137 (system_not_roster_praise): baseline pass=True, final pass=True.
  Baseline: []
  Final: []
- steam:235001445 (hostile_wording_does_not_reverse_direction): baseline pass=True, final pass=False.
  Baseline: [{"character": "Jamie", "direction": "buff", "recommendation": "下次加强杰米", "source_errors": [], "audit": "supported"}]
  Final: [{"character": "Jamie", "direction": "buff", "recommendation": "加强杰米。", "source_errors": ["Numerical adjustment intent absent or ambiguous; review required"], "audit": null}]
- steam:237619085 (attacker_not_victim): baseline pass=False, final pass=False.
  Baseline: [{"character": "Arjun", "direction": "unclear", "recommendation": "做好角色", "source_errors": [], "audit": "uncertain"}]
  Final: [{"character": "Arjun", "direction": "nerf", "recommendation": "削弱阿俊。", "source_errors": [], "audit": "unsupported"}]
- steam:237685225 (nationality_not_identity): baseline pass=True, final pass=True.
  Baseline: []
  Final: []
- steam:237728767 (source_literal_unknown_official_identity): baseline pass=False, final pass=True.
  Baseline: [{"character": "Arjun", "direction": "unclear", "recommendation": "不削", "source_errors": [], "audit": "supported"}]
  Final: [{"character": "Arjun", "direction": "nerf", "recommendation": "削弱阿俊。", "source_errors": [], "audit": "supported"}]

## Quality-module scope

Selected quality diagnostic: quality-live-enforce-v4. Quality prompt refinement is evaluated on the same four known development sources, never reported as held-out accuracy.
Development route-plus-current-position checks: [('quality-live-enforce', 0, 4), ('quality-live-enforce-v3', 2, 4), ('quality-live-enforce-v4', 3, 4)]. The intermediate variant matched all four routes but still got two directions wrong; the selected variant retains three valid primary classifications and sends the fourth to review. Failed compact-quote recovery attempts remain in separate folders; none were silently converted into successful annotations.
A separate live enforce diagnostic used 4 real sources drawn from the frozen 600-comment set. Relevance admitted 4; quality completed 3, failed 1. Route comment counts (overlapping): {'exclude': 0, 'opinion_only': 2, 'mechanism_evidence': 0, 'system_evidence': 1, 'review': 1}.
This small diagnostic plus the complete offline regression suite tests quality integration. The 600-comment run does not claim 600 fresh quality span annotations, full shadow/enforce coverage, measured emotion-bias reduction or semantic precision/recall.

## New-source meaning checks

Eight deliberately selected new-corpus sources (four per language) received source-only agent expectations before the corresponding corpus outcomes were inspected. The frozen default/off pipeline matches 5/8 of these debugging expectations; see new-source-diagnostics.json for all cases and failures. Three sources were later reused for quality-prompt development, as recorded in new-source-diagnostic-use-note.json. This is not human ground truth, random sampling, a held-out study or an independent accuracy estimate.

## Code regression

----------------------------------------------------------------------
Ran 147 tests in 10.540s

OK

## Limitations and retained history

No independent human labels, patch applicability check, official identity update or game-mechanic truth verification was performed. These are bounded program and prompt diagnostics, not proof of globally optimal prompts, overall player consensus or ready-to-ship balance values.
Baseline prompts, intermediate candidate prompts/regressions, the provisional-language run and interrupted CPU experiment are retained. Their results were not substituted for the final complete corpus run.

Primary files: full-pipeline-final/balance-report.json, full-pipeline-final/full-pipeline-coverage.json, full-pipeline-final/validated-claims.json, full-pipeline-final/quarantined-claims.json, final-integrity-checks.json, validation-results.json and the per-run requests/ directories.
