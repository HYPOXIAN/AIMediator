# Handoff B2: Split `engine.py` by pure moves

- Type: Agent handoff
- Status: Active
- Updated: 2026-11-03
- Applies to: [code restructuring plan](../code-restructuring.md) batch B2; entry tag `restructure-b1`

Work order for batch B2. The steps are defined in plan section 7 (B2). The
target interfaces are in [blueprint](../code-restructuring-blueprint.md)
section 3.3, and the dependency table is in plan section 4.2.

## 1. Mission

First replace the module-global patch seams with explicit injection. Then
move the content of `engine.py` into `schema`, `evidence`, `inference`,
`stages`, `runner`, `retrieval` and `pipeline`, and move `FixtureTransport`
into `fixture_transport`.

- Every move is a pure move. `engine.py` re-exports the moved names (the
  facade) until B3.6.
- No behavior changes: the lock stays green at every step, and its fixture
  does not change.

## 2. Entry conditions

- Tag `restructure-b1` exists (after the owner review of B1).
- Clean tree, no `WIP Step` stash. The gates pass.

## 3. Responsibility boundary

Allowed paths:

```text
^(src/aimediator/|tests/|scripts/experiments/replay_balance_admission\.py$|docs/records/[0-9]{8}-code-restructuring\.md$)
```

- **Allowed**:
  - new modules in `src/aimediator/`;
  - `engine.py`, `inference.py`, `demo.py` and `operations.py` (imports
    only, B2.9);
  - test changes for injection (B2.2) and the layering test (B2.10);
  - `replay_balance_admission.py` (B2.2 only).
- **Not allowed**:
  - changing the logic of moved code, renaming, or changing a default;
  - other scripts;
  - documents other than the change record;
  - the lock fixture.
- **Decisions in force**: none specific to B2. The contracts are in
  blueprint sections 3.3 to 3.5.
- **Owner actions**: none.

## 4. Sessions

### B2-1 (implementation): steps B2.1 to B2.4

### B2-2 (implementation): steps B2.5 to B2.10

Both sessions use this prompt, with their own session ID and step range:

```text
You are session B2-<k> (implementation) of the AIMediator code restructuring,
steps <first> to <last>.
Work in the AIMediator checkout on branch main.
Before changing anything, read: RULES.md; this work order
(docs/plans/code-restructuring-handoffs/b2-engine-split.md); the blueprint
docs/plans/code-restructuring-blueprint.md, sections 3, 4, 5 and 6; the plan
docs/plans/code-restructuring.md, sections 1, 2, 4.1, 4.2, 5, 8.6 and the B2
part of section 7; the change record.
Task: execute your steps in order, inside the boundary of this work order.
The order is mandatory: B2.1 and B2.2 come before any move.
Rules:
- Start with the plan's resume procedure. Run the gates, plus the move check
  of plan 8.6, after every move.
- One kind of operation per commit, with "Step: B2.x" in the body.
- Never add any attribution.
- Stop and escalate on the plan's stop conditions and on section 6 of this
  work order.
Finish at a step boundary with a clean tree and a session-log entry. Your
final message repeats that entry.
```

Pure-move procedure (B2.3 to B2.9):

1. Create the new module with the moved definitions copied unchanged, and
   with the imports they need.
2. Use the same import aliases as `engine.py`: `digest`, `write_json`,
   `strict_json`, and `quality` for `evidence_quality`. Function bodies then
   stay byte-identical, and the move check compares ASTs.
3. Delete the definitions from `engine.py` and import them back into it (the
   facade).
4. Run the move check (plan 8.6) with the commit before the step as the
   base. Every moved name must be `same`, or listed in the step's commit
   body as intentionally changed.
5. Run the gates. The lock must be green.

Step notes:

- **B2.1** Inside `run`:
  - Resolve each transport at call time: `(api_transport or api)` for the
    `/api/tags` call.
  - Runner factory: `Runner` when `chat_transport` is `None`, otherwise a
    function that creates `Runner(*values, chat_transport=chat_transport)`.
  - Retrieval service: `retrieval_service`; or `retrieve` when no transport
    is given; or a function that calls `retrieve(*values,
    api_transport=api_transport, embed_transport=embed_transport)`.
  - Because the defaults are looked up in `engine`'s namespace at call time,
    today's module-global patches keep working until B2.2.
- **B2.2** Replace the patches:
  - `test_balance_analysis.py` lines 96 and 112: build the `Runner` with
    `chat_transport`.
  - `test_balanced_collection.py` line 80: pass `api_transport` and
    `embed_transport` instead of patching `api` and `glossary_vectors.embed`.
    Line 93: pass `chat_transport`.
  - `test_evidence_quality.py` lines 291 and 292: pass `api_transport`,
    `chat_transport` and `retrieval_service`.
  - `replay_balance_admission.py` line 33: build its `Runner` with a
    `chat_transport` that raises `RuntimeError('Replay cannot run
    inference')`.
  - `tests/behavior_lock.py`: pass the fixture transports as parameters.
  - Afterwards, the grep in plan step B2.2 must print nothing.
- **B2.3** `schema.py` gets `obj`, `arr`, `STRING`, `NULL_STRING` and `BOOL`,
  copied unchanged from `engine.py`. `evidence.py` gets `PARAMETER`, `CLAIM`,
  `evidence_units`, `character_reference`, `character_candidates`,
  `numeric_tokens` and `ground_claim`.
  - The move check covers only functions. For the constants, write
    `json.dumps(engine.CLAIM)` and `json.dumps(engine.PARAMETER)` to a
    temporary file before the step, and compare them with the moved values
    after it.
- **B2.4** Move `api`, `repeated_claim` and `streamed_chat` into
  `inference.py`. In the same commit, replace in `inference.py`:
  - `engine.strict_json` with `strict_json` from `common`;
  - `engine.glossary_vectors.normalize` with `glossary_vectors.normalize`;
  - `engine.streamed_chat` with the local `streamed_chat`;

  and remove `from . import engine`. List the changed `Transport` methods as
  intentional.
- **B2.5** `stages.py` gets `schema_for` and `exact_coverage`. They need
  `copy`, `re`, `quality`, `CLAIM`, `arr`, `obj`, `numeric_tokens`,
  `character_candidates` and `attributed_candidates`.
- **B2.6** `runner.py` gets `Runner`.
  - It calls `schema_errors(parsed, schema)`. Import `schema_errors` from
    `evidence_quality`: it is the function that `engine.schema_errors`
    delegates to, with the same arguments. The `engine` wrapper stays until
    B3.6.
  - Its default chat transport is `inference.streamed_chat`.
- **B2.7** `retrieval.py` gets `retrieve`, and keeps `POS, NEG = anchors()`
  at module level, so the function body stays identical; B5.10 makes it
  lazy. `engine.py` imports `POS` and `NEG` from `retrieval`.
- **B2.8** `pipeline.py` gets `VERSION`, `relevance_agrees`, `batches`,
  `aggregate`, `quality_source_counts`, `build_full_coverage`,
  `validate_modes` and `process`.
  - The defaults of `process` (`runner_factory=Runner`,
    `retrieval_service=retrieve`) import from `runner` and `retrieval`.
  - `engine.py` keeps `ROOT`, `run`, `main`, the `schema_errors` wrapper and
    the facade imports. Its docstring says that the facade goes in B3.6.
- **B2.9** `fixture_transport.py` gets `FixtureTransport`. Replace:
  - `engine.NEG` with `anchors()[1]` from `resources`, because the table
    does not let `fixture_transport` import `retrieval`;
  - `engine.character_candidates` and `engine.character_reference` with
    imports from `evidence`;

  and list them as intentional. `demo.py` imports `FixtureTransport` from
  the new module, and drops its now unused `inference` import, which the
  table forbids. `operations.py` line 70 imports from `fixture_transport`.
  The tests that import `aimediator.demo.FixtureTransport` keep working.
- **B2.10** `tests/test_module_layers.py`:
  - Copy the table of plan section 4.2 into the test, with the transitional
    allowance.
  - Collect imports with `ast`: `ImportFrom` with level 1 or more (the first
    component of the module, or the imported names when the module is
    `None`), and `import aimediator.<x>`.
  - Assert that every edge is allowed, that the graph has no cycle, and that
    every module file appears in the table, so new modules are added on
    purpose.

At the end of B2, `engine.py` holds `ROOT`, `run`, `main`, the
`schema_errors` wrapper and import lines.

### B2-V (verification)

```text
You are session B2-V (verification) of the AIMediator code restructuring.
You did not implement batch B2. Change nothing except the change record.
Read: RULES.md; this work order; the blueprint, sections 3, 4, 5, 6.6 and 7;
the plan, sections 2, 4.2, 5, 8 and the B2 part of section 7; the change
record.
Task: run every item of the B2-V checklist in this work order on HEAD, and
append a verification note committed with "Session: B2-V". If every item
passes, tag that commit restructure-b2. Otherwise record the findings as
fix-up steps B2.F1 and so on, and stop without tagging.
Never add attribution. Your final message repeats the verification note.
```

Checklist:

1. Boundary check from `restructure-b1`, and commit hygiene.
2. Move check for the whole batch: `python3 <move-check> restructure-b1
   src/aimediator/engine.py src/aimediator/*.py`, and the same for
   `src/aimediator/demo.py`. Everything is `same`, except names that a step
   commit lists as intentional.
3. `git diff restructure-b0..HEAD -- tests/fixtures/` prints nothing, and the
   lock is green.
4. The B2.2 grep prints nothing. `tests/test_module_layers.py` passes, and
   finds no cycle.
5. Gates, the foreign directory check (plan 8.5) and the wheel acceptance
   (plan 8.2).
6. `engine.py` holds only what the end of section 4 lists.

## 5. Exit and handoff out

- Exit tag: `restructure-b2`, set by B2-V.
- The next work order is [B3](b3-callers-and-tests.md).

## 6. Escalation triggers

- The lock turns red during a move.
- An import cycle cannot be broken without changing logic.
- A test passes only with a module-global patch.
- A moved definition cannot keep an identical AST.
