# Coding agent handoff prompt

- Type: Agent handoff
- Status: Archived
- Updated: 2026-11-03
- Applies to: evidence-quality implementation task of 2026-10-26, completed (RULES.md P6)
- Translated 2026-11 from the Chinese original (commit `3ceb123`); only the language changed.

Implement the RAG comment evidence-quality and emotional-interference control module in `<project root>`. First read the applicable AGENTS.md, then read `docs/design/evidence-quality.md` completely and take that file as the engineering specification for this task; start implementing after reading the existing source files it lists, and do not only give a plan.

The goal is to route unrelated content, general strength opinions, concrete character mechanism evidence, system balance feedback and content pending review separately, while quantifying the length of pure emotion. Keep emotional criticism that carries information; emotional intensity must not be treated as credibility or evidence weight, and general complaints must not be promoted to concrete adjustment recommendations.

Add a separate quality stage after the existing relevance review and before extraction; implement off/shadow/enforce and quality-only, with off as the default. Add bilingual prompts, structured segment and information-point annotation, exact source-offset validation, program-computed ratios and routes, request caching and failure review. Pay attention to the stage parsing and output budget of Runner.generate, the stability of the source evidence_id, multi-route splitting of mixed comments, and the programmatic evidence-eligibility checks of enforce.

Output general opinions, character mechanism evidence that passed the later review, system feedback, and exclusion and review records separately. Keep the existing identity, numerical intent, source review and versioned-data gates; update the aggregation and the engineering-design entry, and forbid low-information opinions from gaining engineering eligibility by borrowing other evidence from the same comment. Add full-pipeline coverage and a versioned manifest, and keep an explicit compatibility policy for the old format.

Following the implementation order of the handoff document, complete the pure-logic tests, mock integration tests and all existing unit tests. Build bilingual boundary cases of a new version and an evaluation tool; do not modify historical frozen labels, admission, reports or original comments; all new experiments use new directories. Do not read or output unrelated credentials, add no external API, change no model or retrieval strategy, and build no UI.

When local models are available, run a small real shadow/enforce comparison; when they are unavailable or there are no human annotations, continue to complete the offline engineering and list explicitly what was not run or verified. Synthetic cases, silver-label diagnostics and human accuracy must be reported separately; claiming that emotional bias has been eliminated, or that unverified effectiveness metrics have been reached, is forbidden.

Final delivery: a list of implementation files, behavior changes, test results, copyable run and rollback commands, the locations of example outputs, compatibility notes and the effectiveness validation not yet completed. Except for real blockers, complete the implementation and fixes within the specification autonomously, and do not stop at the planning stage.
