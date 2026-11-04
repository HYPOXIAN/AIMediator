# Code Restructuring Change Record

- Type: Record
- Status: Active
- Updated: 2026-11-03
- Applies to: commit `7282f49` and later; `RULES.md` v1.2 and later amendments

The single change record of the code restructuring
([plan](../plans/code-restructuring.md)). Every step adds its row to the
progress table in its own commit. Deletions are entered under "Archive and
deletions" (G6). Frozen when the plan is finished (D3).

## Owner decisions

| ID | Answer | Date | Notes |
| -- | ------ | ---- | ----- |
| CR-D01 | adopt | 2026-11-03 | plan section 9 |
| CR-D02 | adopt | 2026-11-03 | plan section 9 |
| CR-D03 | adopt | 2026-11-03 | plan section 9 |
| CR-D04 | adopt | 2026-11-03 | plan section 9 |
| CR-D05 | adopt | 2026-11-03 | plan section 9 |
| CR-D06 | adopt | 2026-11-03 | plan section 9; includes confirmation that no experiment output must be resumed under its old identity |
| CR-D07 | adopt | 2026-11-03 | plan section 9 |
| CR-D08 | adopt | 2026-11-03 | plan section 9 |
| CR-D09 | adopt | 2026-11-03 | plan section 9 |
| CR-D10 | adopt | 2026-11-03 | plan section 9 |
| CR-D11 | adopt | 2026-11-03 | plan section 9 |
| CR-D12 | adopt | 2026-11-03 | plan section 9 |

## Progress

The commit of a step is found with `git log --grep 'Step: <ID>'`.

| Step | Status | Tests | Lock | Notes |
| ---- | ------ | ----- | ---- | ----- |
| B0.1 | done | 222 | — | Change record opened; index row added. The lock does not exist before B0.3 |
| B0.2 | done | 222 | — | F-04 fixed: the test reads the prompt through `asset_path`. Plan 8.5 from a foreign directory: 222 pass, no error |
| B0.3 | done | 223 | green (fixture created) | Behavior lock L1 to L4 and its self-test; see "Behavior lock (B0.3)". Suite 123 s, of which the lock takes about 51 s |
| B0.4 | done | 223 | green | Baseline measured again, with the wheel acceptance and the foreign-directory run; see "Baseline measurements (B0.4)". Escalation E-1 (not blocking) |

## Baseline measurements (B0.4)

Measured on 2026-11-03 at `3979a72` (B0.3 done), with Python 3.14.8 and
NumPy 2.4.6, by the commands of plan section 8. B0 changed nothing under
`src/` or `scripts/`, so the code figures equal those at `7282f49`.

### Plan section 0 items

| Item | Section 0 (at `7282f49`) | B0.4 (at `3979a72`) | Command |
| ---- | ------------------------ | ------------------- | ------- |
| Tracked files | 195 | 209: the plan, blueprint and 8 handoffs (10, `ab86db6`) and B0's change record, lock module, lock test and fixture (4) | count 1 |
| Package `src/aimediator/` | 20 modules, 3,444 lines; `engine.py` 931 | 20 modules, 3,444 lines; `engine.py` 931 | count 2 |
| `scripts/` | `collect/` 4 files (824 lines), `experiments/` 18 (1,764), root forwarders 7 (92), `maintenance/` 3 (1,093) | unchanged: 4 (824), 18 (1,764), 7 (92), 3 (1,093) | count 3 |
| Offline tests | 222 pass in about 70 s | 223 pass in 118.8 s (wall 119.2 s); the lock adds 1 test and about 51 s | plan 8.1, 8.4 |
| Rule check | 0 violations; the hook blocks | `Total: 0`; the hook ran on every B0 commit | plan 8.1 |
| Compatibility layers | 19 symlinks, 7 forwarding scripts | 19 tracked symlinks (14 `prompts/`, 3 `configs/`, 1 `data/`, 1 evaluation set), 7 forwarding scripts in the register | count 4 |
| Offline demo | 26.2 s; `engine.character_reference` 688 calls, 19.4 s cumulative (74 %) | 26.2 s; `engine.character_reference` 688 calls, 19.2 s cumulative (73 %) | plan 8.4 |
| Slowest tests | presentation demo test 26.2 s; `test_cli_product` 31.1 s in total | behavior lock 51.2 s; presentation demo test 24.9 s; `test_cli_product` 35 tests in 28.8 s run alone | count 5 |
| Working-directory dependence | 1 test errors from outside the checkout | none: 223 pass from a foreign directory (F-04 fixed in B0.2) | plan 8.5 |
| Installed-wheel acceptance | passes offline (18 commands) | passes: `"passed": true`, `"commands": 18`, Python 3.14.8, NumPy 2.4.6 | plan 8.2 |
| Interpreters | Python 3.14.8 with NumPy 2.4.6; no `.venv/`; system Python 3.10 to 3.12 without NumPy | unchanged | count 6 |

The counts in the Command column:

```sh
git ls-files | wc -l                                              # count 1
ls src/aimediator/*.py | wc -l; cat src/aimediator/*.py | wc -l   # count 2
cat scripts/collect/*.py | wc -l                                  # count 3, per directory;
git ls-files scripts/maintenance | xargs wc -l                    #   maintenance includes hooks/pre-commit
git ls-files -s | grep -c '^120000'                               # count 4
python3 -m unittest discover -s tests -q --durations 12           # count 5
python3 -m unittest discover -s tests -p 'test_cli_product.py'    # count 5
python3.12 -c 'import numpy'                                      # count 6, also 3.10 and 3.11
```

### Function-length metric (blueprint 7.3)

8 functions over 60 lines, the same 8 as at `7282f49`:

| Lines | Function |
| ----- | -------- |
| 259 | `engine.process` |
| 136 | `review.load_run` |
| 112 | `engine._generate` |
| 111 | `operations.analyze` |
| 105 | `reporting.export_report` |
| 78 | `engine.run` |
| 71 | `quality_scoring.score_group` |
| 61 | `evidence_quality.qualify` |

### Plan 8.7 greps

Each must print nothing at the point stated in the plan; none is due yet.

| Grep | Due | Lines printed now | Notes |
| ---- | --- | ----------------- | ----- |
| 1 Forwarder imports | after B3 | 42 lines in 25 files: 9 under `tests/`, 16 under `scripts/` | 9 test files also at `7282f49`; the blueprint baseline says 14 (escalation E-1) |
| 2 `engine` imports inside the package | after B3.1 | 37 lines in 7 modules | blueprint baseline 7 |
| 3 Users of the symlink paths | before B4.3 | 55 lines in 25 files: `src` 11 (6), `scripts` 7 (6), `tests` 2 (2), `README.md` 1, `docs/design` 5 (2), `docs/plans` 9 (5), `docs/reference` 20 (3) | the plan's own mentions are expected |
| 4 `Path.cwd()` roots | after B6.1 | 2 | blueprint baseline 2 |
| 5 Text I/O without encoding | after B1.3 | 129 | 130 at `7282f49`; B0.2 added the encoding to one test call |

## Behavior lock (B0.3): volatile keys, exclusions, self-test results

Built at `ebdca39` (plan section 5). Files:

- `tests/behavior_lock.py`: one producer per target, the normalizer and
  `--write`, which rewrites the fixture with sorted keys;
- `tests/test_behavior_lock.py`: one test that compares the produced digests
  with the fixture and lists the differing keys;
- `tests/fixtures/behavior-lock.json`: 378 keys with 2,204 values, of which
  2,189 are SHA-256 digests and 15 are the existence placeholder. It holds no
  corpus text.

The lock takes about 51 s: the demo about 25 s, the legacy runs about 24 s.

### Targets

- **L1**: `aimediator.demo.demo(<tmp>/demo, quiet=True)` with stdout and
  stderr captured. Keys `L1:<path below demo/>`. L1 is digested before L3
  edits the review template.
- **L3**: `reviewer_type` `agent` and `reviewer_id` `behavior-lock` set in
  `demo/review-template/decisions.json`; `import_review` into
  `<tmp>/overlay`; `export_report` of `demo/enforce` with that overlay into
  `<tmp>/reviewed-report`. Keys `L3:overlay/...` and
  `L3:reviewed-report/...`.
- **L2**: `engine.run` in `off`, `shadow` and `enforce` on the fixture
  sources, written as the demo writes `synthetic-input.jsonl`. Arguments as
  the B0 handoff gives them. `engine.api` is patched with a dispatcher
  (`/api/tags` to `FixtureTransport.tags`, any other endpoint to
  `FixtureTransport.api`), `engine.streamed_chat` with
  `FixtureTransport.chat`, and stdout is captured. B2.2 replaces the patches
  with injection. Keys `L2:...`.
- **L4**: `classify_rules` from `scripts/collect/screen_feedback.py`, loaded
  with `importlib`, on 350 `text_original` values in file order: 12 from
  `balance-regressions-v1/cases.json`, 300 from
  `evidence-quality-real-v1/annotation-template.json` and 38 from
  `evidence-quality-synthetic-v1/records.jsonl`. The producer fails if a
  count changes. One digest of the JSON list of results (key
  `L4:classify_rules`). Plan 5.2 names `classify()`; without overrides it
  returns the `classify_rules` result plus the constant `'rules'`, so the
  rules result covers it.

Each produced file gives the SHA-256 of its normalized bytes under its
normalized path. Several files can share a normalized path (request
directories). Their key then holds the sorted list of digests. For each run,
the key `<run>/requests/**/request.json` holds the sorted digests of all its
normalized `request.json` files (model-input equivalence, plan 5.2).

JSON files are parsed and re-serialized in the writer's own format (indent 2,
compact or canonical), so formatting stays locked. A file whose bytes no
format reproduces is normalized as plain text.

### Discovery (plan 5.3)

Outputs were produced at `ebdca39` and compared as parsed JSON key paths,
with request directories paired through `request-trace.json`:

- **A and B**: the same code, two temporary directories. Their differences
  are V1.
- **C1**: a copy of `src/` with `# lock probe` appended to `common.py`, as
  plan 5.3 step 2 says. Its differences from A, outside V1, are V2.
- **C2**: a copy of `src/` with the probe appended to every package module.
  This variant was added because the legacy runner hashes `engine.py`,
  `balance_policy.py` and `evidence_quality.py` one by one, which a
  `common.py` probe cannot reveal. B2 changes `engine.py`.

After normalization, A, B, C1 and C2 give identical digest maps, and the
fixture written by `--write` equals A. Removing any one key from the
normalizer makes a variant differ, except for four keys that hold the same
value as another key (see the table). Markdown and CSV files did not differ
in any variant. The discovery scripts were temporary and are not kept; the
producers in `tests/behavior_lock.py` repeat the procedure.

### Volatile keys

A key's value is replaced wherever the key occurs in a JSON file.

| Key | Set | Where found | Placeholder |
| --- | --- | ----------- | ----------- |
| `created_at_utc` | V1 | L1 and L2 `manifest.json` | `<time>` |
| `updated_at_utc` | V1 | L1 `run-state.json` | `<time>` |
| `elapsed_seconds` | V1 | `response.json`, `request-trace.json`, `evidence-quality.json` attempts | `<duration>` |
| `dataset` | V1 (absolute path) | L2 `manifest.json` | `<path>` |
| `run_sha256` | V1, V2 | review template and overlay `decisions.json`, `review-manifest.json`, `report.json` (`run_fingerprints`, `reviewer_provenance`) | `<fingerprint>` |
| `decisions_sha256` | V1, V2 | `review-manifest.json`, `report.json` `reviewer_provenance` | `<fingerprint>` |
| `artifact_hashes` | V1, V2 | L1 `run-state.json` | each value `<artifact-sha256>`; the artifact names stay locked |
| `code` | V2 | L1 `manifest.json` `identity`, `report.json` `run_identity` | `<code>`; covers `modules` and the Python and NumPy versions |
| `shared_code_sha256` | V2 | L2 `manifest.json` `identity` | `<code>` |
| `runner_sha256` | V2 (C2) | L2 `manifest.json` `identity.evidence_quality` | `<code-sha256>`; same value as `script_sha256` |
| `script_sha256` | V2 (C2) | L2 `manifest.json` `identity` | `<code-sha256>`; same value as `runner_sha256` |
| `module_sha256` | V2 (C2) | L2 `manifest.json` `identity.evidence_quality` | `<code-sha256>`; also a `shared_code_sha256` value |
| `policy_module_sha256` | V2 (C2) | L2 `manifest.json` `identity` and `identity.evidence_quality` | `<code-sha256>`; also a `shared_code_sha256` value |
| `run_id` | V2 | L1 `manifest.json` | `<run-id>` |
| `request_id` | V2 | `request-trace.json`, `evidence-quality.json` attempts | `<request-id>` |

The string leaves of these values with 16 or more characters are also
replaced, with the same placeholder, wherever they occur as text. That
covers:

- the request directory names under `requests/<stage>/`;
- `quality_request_ids` and `completed_request_identities`, element by
  element, so that list lengths and stage names stay locked;
- `run_identity` inside the L1 quality request contents
  (`quality_contract`);
- `runner_sha256`, `module_sha256` and `policy_module_sha256` inside the L2
  quality request contents.

`run_identity` is not a volatile key. In `report.json` it holds the whole
run identity (input, configuration, resource and model hashes), and only its
`code` member varies. L3 shares L1's literals because the overlay and the
report derive from the L1 `enforce` run. L2 is normalized only with its own
literals.

### Exemptions

Existence is locked; content is replaced by `<exempt: existence only>`. No
other file is excluded.

| Files | Where | Reason |
| ----- | ----- | ------ |
| `*-snapshot.py` | L2 runs: `runner-`, `quality-module-` and `policy-module-snapshot.py` | Code only; the 9 files differ in C2 |
| `code-manifest.json` | L1 runs | Code hashes plus the Python and NumPy versions. Equal in all variants today; exempt because B2 adds modules and the interpreter can differ |
| `.writer.lock` | L1 runs | The empty advisory writer lock (plan 5.3, item 4) |

### Self-test (plan 5.4)

The lock was green twice in a row before the self-test. Each edit was made
in the checkout, the lock was run, and the file was restored with
`git checkout -- <file>`. The tree was clean after every case.

| Temporary edit | Required | Result | Differing keys |
| -------------- | -------- | ------ | -------------- |
| A space appended to `src/aimediator/assets/prompts/summarize-balance.en.txt` | fail | fail | 31 (L1 16, L2 14, L3 1) |
| `'recommendation'` and `'specificity'` swapped in `CLAIM` (`engine.py` lines 110 to 113) | fail | fail | 18 (L1 9, L2 9) |
| `count=4` changed to `count=3` (`engine.py` line 773) | fail | fail | 39 (L1 21, L2 18) |
| `'# SF6 collected-sample feedback'` changed to `'# SF6 collected-sample comments'` (`reporting.py` line 125) | fail | fail | 2 (L1 1, L3 1) |
| `'general_not_mechanism'` changed to `'general_not_a_mechanism'` (`evidence_quality.py` line 182) | fail | fail | 18 (L1 9, L2 7, L3 2) |
| `# lock probe` appended to `src/aimediator/common.py` | pass | pass | 0 |
| Plain rerun | pass | pass | 0 |
| Extra case: `'explicit_balance_or_strength_claim'` changed to `'explicit_balance_claim'` in `scripts/collect/screen_feedback.py`, to show that L4 is live | fail | fail | 1 (L4) |

## Archive and deletions

| Path | Archive location | SHA256SUMS entry | Reason | Step |
| ---- | ---------------- | ---------------- | ------ | ---- |

## Decisions found during execution

## Escalations

### E-1 Baseline of "Test files importing forwarders" (B0.4)

- **Question**: blueprint section 2 gives the metric "Test files importing
  forwarders" a baseline of 14 and names plan 8.7, first grep, as its
  measurement. That grep finds 9 test files, both at `7282f49` and at
  `3979a72`. 14 is the plan's T-01 figure (section 3.6), which is defined
  differently: test files that put `scripts/` directories on `sys.path`. A
  plain search finds 11 such files now. Which baseline does the metric use?
- **Options**: (a) correct the blueprint baseline to 9, the count of the
  named command; (b) keep 14 and give the T-01 definition its own command.
- **Recommendation**: (a). The target (0 after B3.3) and the command stay
  the same; only the baseline figure changes. The B0 boundary does not
  include the blueprint, so B0 does not correct it.
- **Blocked**: nothing.
- **Answer**: the owner, 2026-11-03, given to session B0-V: option (a),
  correct the blueprint figure to 9. B0-V made the correction at the
  owner's instruction in its own `docs` commit, which also records this
  answer. The commit lies outside the B0 boundary (blueprint section 9:
  corrections to the blueprint are `docs` commits that cite the reason).
  Plan T-01 keeps its own figure and definition.

## Verification notes

## Session log

### 2026-11-03 B0-1 (implementation)

- Steps: B0.1, B0.2, B0.3, B0.4; none started and stashed.
- State: HEAD is the B0.4 commit (parent `3979a72`); tests 223; lock green;
  rule check 0.
- Findings: escalation E-1 (blueprint metric baseline 14 versus 9 measured;
  not blocking). Deviations, all recorded under "Behavior lock (B0.3)": the
  discovery added an all-modules probe (C2) to the plan's `common.py` probe;
  the self-test has one extra case, for L4; L4 uses `classify_rules`, as the
  handoff says, where plan 5.2 names `classify()`. No decisions found during
  execution.
- Next: B0-V (verification of B0, sets `restructure-b0`); blockers: none.

## Batch results

## Deferred
