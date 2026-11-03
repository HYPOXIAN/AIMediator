# Workspace refactoring

The refactor preserves evidence schemas, bilingual routing, source binding,
review gates, and bounded request journals. The package is the single runtime
implementation; research entry points import it directly.

Structural changes:

- Six compatibility scripts now import package modules instead of compiling and
  executing their source. Imports share one module identity, so patches and
  caches no longer depend on which entry point loaded the implementation.
- JSON persistence and hashing live in `common.py`; embedding endpoint and
  environment-file parsing live in `config.py`. Scoring no longer imports the
  pipeline merely to access persistence helpers. Shared persistence primitives
  have explicit type annotations.
- Runner progress is an explicit callback instead of a replacement method.
  Coverage uses precomputed counts, and status computes failures once.

Transport retries handle expected I/O and response-shape errors. Unexpected
programming errors propagate instead of consuming the retry budget. The CLI
still translates errors into its public exit-code contract; run lifecycle
handling still records failure before returning. Source validation and atomic
checkpoint writes are intentional domain requirements.

Research datasets and historical outputs have not been rewritten. Existing run
identities include source hashes: an old run cannot resume under changed code;
create a new run with this version. Research command defaults resolve relative
to the current working directory; run them from the workspace root.

Run all offline checks:

```sh
python3 -m unittest discover -s tests -q
```

Run the packaged demo without inference services:

```sh
python3 -m pip install .
aimediator demo --out ./refactored-demo
```

Live model inference is not part of the offline checks.
