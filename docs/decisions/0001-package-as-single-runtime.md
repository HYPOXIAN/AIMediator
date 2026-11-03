# 0001 The package is the single runtime implementation

- Type: Decision
- Status: Active
- Updated: 2026-11-03
- Applies to: `aimediator` 0.1.0 package layout
- Rewritten 2026-11 as an ADR from the workspace refactoring note
  (`docs/reviews/refactoring.md`, commit `3ceb123`), using only its content;
  its two command blocks are left out (change record, P4-D04). The date of
  the refactoring was not recorded; it predates the 2026-11-03 baseline.

## Context

Before the refactoring, the compatibility scripts in `scripts/` compiled and
executed the package source instead of importing it, so the module identity
depended on which entry point loaded the implementation, and so did patches
and caches. Scoring imported the pipeline merely to access persistence
helpers. Runner progress was reported through a replacement method.

The refactoring had to keep evidence schemas, bilingual routing, source
binding, review gates and bounded request journals unchanged.

## Decision

The package `src/aimediator/` is the single runtime implementation; research
entry points import it directly.

- Six compatibility scripts import package modules instead of compiling and
  executing their source. Imports share one module identity.
- JSON persistence and hashing live in `common.py`; embedding endpoint and
  environment-file parsing live in `config.py`. Scoring no longer imports the
  pipeline to access persistence helpers. Shared persistence primitives have
  explicit type annotations.
- Runner progress is an explicit callback instead of a replacement method.
  Coverage uses precomputed counts, and status computes failures once.
- Transport retries handle expected I/O and response-shape errors.
  Unexpected programming errors propagate instead of consuming the retry
  budget.

## Consequences

- Patches and caches no longer depend on which entry point loaded the
  implementation.
- The CLI still translates errors into its public exit-code contract; run
  lifecycle handling still records failure before returning. Source
  validation and atomic checkpoint writes are intentional domain
  requirements, not leftovers.
- Research datasets and historical outputs were not rewritten. Existing run
  identities include source hashes: an old run cannot resume under changed
  code; create a new run with this version.
- Research command defaults resolve relative to the current working
  directory; run them from the workspace root.
- Live model inference is not part of the offline checks.

The compatibility scripts are registered in
[the compatibility register](../reference/compatibility-layers.md) with their
removal conditions. The offline test and demo commands are in the root
[README](../../README.md).
