# Coding-agent handoff: implement the AI Mediator CLI

Work in `<project root>`. The final deliverable is an
installable CLI named `aimediator`, not a web interface or another collection
of research commands. Read applicable `AGENTS.md` instructions and then read
`docs/design/cli.md` completely; it is the implementation specification.
Follow its read-first source list and verify the current baseline before editing.

This is an implementation task. The preceding design session changed only
documentation and added an offline verification record; no product CLI exists
yet. Its baseline was 147 passing tests on Python 3.14.8 / NumPy 2.4.6, recorded
in `reports/cli-design-baseline-20261028-t2qr8gbm/`. Rerun
`python3 -m unittest discover -s tests -v` and inspect the current files before
using that result. It does not establish the proposed minimum Python version
or clean-wheel support. If Git metadata is unavailable, record source hashes;
do not initialize or reconstruct Git merely to proceed.

Implement the specified installable package, resource access, configuration,
doctor, analysis, explicit resume, status, immutable source-review export/import,
deterministic report export, quality evaluation adapter, and offline demo.
Use the existing Python analysis/quality/policy logic. Preserve the current
models, language routing, prompts, retrieval rules, evidence grounding, numerical
intent checks, quality eligibility, and engineering prerequisites during the
refactor. The product must run from an installed wheel outside the checkout;
do not wrap research scripts with subprocess or require repository path hacks.

Preserve old script invocations through compatibility adapters. The current
runner's repository-root paths, resource/code snapshots, import of POS/NEG from
an experiment script, and script-level monkeypatch tests need deliberate
migration. Do not create two authoritative copies of active resources. Require
explicit new-run input/output paths and explicit resume; reject incompatible
identity before changing a run. Never overwrite historical data, frozen labels,
decisions, prompts in prior runs, or historical reports.

Implement the design's credential-only resume exception, persistent retry
budgets, structured error envelopes, and explicit legacy report/review schema
allowlist. A new credential cannot change the saved model or endpoint, an
exhausted resume cannot reset retry limits, and a legacy adapter cannot invent
missing provenance. Keep old script behavior at the compatibility boundary;
new product commands follow the new contracts.

Keep off as the compatibility default and recommend shadow in examples. Quality
enforcement must continue through source review and report export. Emotional
language cannot reduce the weight of substantive evidence. Count comment IDs,
preserve conflicting opinions and uncertainty, and separate source-review
acceptance from automatic audit success. Edited claims cannot reuse an audit
of the original proposal. Review import and report generation make no model calls.

Build the synthetic demo using injected fixture transports through the actual
pipeline, with no network, model, or credential requirement. Bundle only
redistributable resources and authored fixtures. Keep configured remote
embedding explicit, redact secrets, and do not read an unrelated `.env`.
Do not implicitly collect feedback, download/replace models, rerun 600 comments,
optimize prompts, or implement a UI as part of this task.

Follow P0-P4 and the acceptance gates in the design. Run all existing offline
tests, add meaningful persistence/evidence/portability/workflow checks, build
wheel and sdist, and verify the installed wheel in a clean environment outside
the repository. If the intended services are available, run a bounded bilingual
live diagnostic in a new directory; otherwise complete offline engineering and
report the unavailable live checks. Never present mock tests or agent silver
labels as independently measured semantic accuracy.

Create and maintain `docs/plans/cli-implementation-status.md` with each milestone's
status, actual validation command/result, artifact path, and remaining work.
Start with the package/resource extraction and its outside-checkout import
gate; proceed through operations, review/report/demo, and clean-install
acceptance. Update the status file after each gate so work can be handed off
without rediscovering the implementation state. Keep an implementation deviation
explicit and justified; do not silently narrow V1 or lower evidence gates.

Continue implementation and routine fixes autonomously within this scope.
Record genuine blockers and unfinished requirements; do not mark V1 complete
unless its command and delivery contracts are met. Finish with artifact paths,
installation and usage commands, tests actually run, compatibility notes, and
remaining semantic/human/patch-fact verification. Do not stop at another plan.
