# Bilingual prompt and full-corpus test — 2026-10-22

The Chinese instructions route to `qwen2.5:7b`; the equivalent English instructions
route to `llama3.1:latest`. The test uses the existing canonical screened dataset,
not newly collected comments. Embeddings use `qwen3-embedding:8b`.

## What ran

- Input: 321 unique comments: 207 English, 113 Chinese, one Portuguese.
- All 320 routed comments underwent vector retrieval. 198 passed retrieval;
  197 also passed the same-language relevance review (112 English, 85 Chinese).
- Only those 197 agreement-positive comments entered extraction. 195 completed;
  two English comments failed generation. Coverage explicitly records both failures.
- Eighteen relevance decisions were rechecked individually; 17 were rescued.
  The saved initial and final decisions make this refinement visible.
- Extraction produced 122 complete proposals. Four failed deterministic source
  binding, including three copied 8→6-frame example claims absent from the real
  sources and one duplicated evidence reference. All four were excluded.
- The full-original-comment model audit examined the remaining 118 proposals,
  automatically retaining 28 and quarantining 90. All automatically retained
  claims were qualitative; no per-character numerical target was accepted.
- Seven request attempts failed validation, including recovered batch failures;
  these are distinct from the two final failed comments.

## Source review

`source-reviewed-report.json` is the recommended inspection artifact. This is a
separate primary-agent source review, **not independent human ground truth**.
It covers every one of the 122 complete proposals, including automatic rejections.
The raw model report is preserved unchanged in `balance-report.json`.

The review retained 47 claims from 38 comments across 15 glossary characters,
rejected 52 and marked 23 uncertain. Three retained claims required explicit,
labeled direction corrections: Alex's grabs, a direct Jamie buff request and a
Zangief weakness complaint. Twelve retained claims needed additional or changed
source context. Original proposals and review decisions are retained alongside
every revision; these repairs are not counted as correct automatic outputs.

Of the 28 automatically retained proposals, this review rejected eight and marked
two uncertain. The 18 retained after review still include one explicit direction
repair and other context/wording revisions. Quotation provenance alone was not
sufficient to establish that the source supported the proposed action.

Examples of excluded errors include cosmetic praise interpreted as balance,
a quoted historical patch interpreted as a new buff request, a general Drive
Impact complaint assigned to Elena, comparison characters assigned the criticism
intended for another fighter, and victim/attacker reversals.

The older patch-specific glossary omits Arjun/阿俊. Nationality-only and derogatory
aliases caused false Dhalsim assignments. These were excluded or left uncertain.
`source-review-supplement.json` separately preserves source-only agent feedback
from all 21 admitted comments explicitly naming Arjun/阿俊. It does not establish
an official roster identity and does not count as Qwen/Llama extraction success.
It also records four original numerical **system** requests: heavy attacks to
break Drive Impact 3→2, removal of a stated 20% Modern damage penalty, a requested
Drive Rush cost of 3 bars when a fireball is on screen, and a relative -1 parry
block-advantage change under an incorrect blocking direction. They are not
assigned arbitrarily to a fighter; unknown current/target values remain null.

The retained per-character proposals are qualitative. Neither broad "too strong"
comments nor descriptions of current damage/frame statistics support inventing
new tuning values. Exact changes still require engineering design and gameplay
validation. Opposing buff/nerf opinions remain separate, counted by unique
comment IDs rather than asserted community consensus.

## Verification and reproducibility

- Unit checks: **70 passed**, covering strict JSON, duplicate keys, missing
  comments, admission agreement, quote offsets, numerical binding, review
  fingerprints and explicit correction provenance (`unit-tests.log`).
- Local numerical entailment controls: **3/4 passed**. Llama passed both;
  Qwen accepted the positive request but also incorrectly accepted the negative
  source "隆的波动拳伤害为600，肯的波动拳伤害为500。" as support for changing Ryu
  600→500. This demonstrates a remaining semantic failure, not merely a format
  problem. The four synthetic cases are excluded from all community counts.
- Dataset, current prompts, glossary and runner hashes match the tested manifest.
  All retained evidence text matches the immutable original Unicode offsets.
  Coverage contains exactly the 197 admitted IDs, each once.
- Maximum reported input length across active requests: **6016 tokens**, below
  the configured 8192-token context. Full source text was supplied as ordered
  evidence units; no fixed source-text clipping was used.
- Exact model digests, source/prompt snapshots, schemas, requests, raw responses,
  validation errors and active request IDs are saved. Unused copied request-cache
  entries are preserved separately in `../balance-engineering-debug-cache/`.

Reproduce/resume with:

```sh
python3 scripts/run_balance_analysis.py --out reports/balance-engineering-20261022-final-review
python3 scripts/review_balance_sources.py --run reports/balance-engineering-20261022-final-review --decisions reports/balance-engineering-20261022-final-review/source-review-decisions.json
python3 scripts/test_balance_controls.py --out reports/balance-engineering-20261022-final-review/synthetic-controls
python3 -m unittest discover -s tests -v
```

The separate agent supplement is a saved source review, not automatically
regenerated or silently injected into the two local models' reports.

## Practical limits

The run is complete as an experiment, but its automatic output is **not ready
for unattended balance changes**. There are no independent gold labels for this
corpus, so these counts are not precision/recall or accuracy estimates. Retrieved
prototypes and the original threshold have observed misses: `steam:236222206`
passed vector retrieval but failed the model relevance gate, while
`steam:236795479` (which explicitly asks for five additional Modern startup
frames) failed vector retrieval. Neither was admitted or quietly inserted into
accepted outputs. Portuguese is explicitly unrouted. Two generation failures,
unresolved identities and individual extraction omissions remain recorded.
Game assertions, official roster identities outside the glossary and patch
applicability were not externally verified. Agent review may itself be mistaken.
