# Code Restructuring Change Record

- Type: Record
- Status: Active
- Updated: 2026-11-04
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
| B1.1 | done | 224 | green | P-01: `resources.glossary()` (`lru_cache(maxsize=1)`); `character_reference` and `ground_claim` use it. New test `test_character_reference_returns_new_objects`. Plan 8.4: demo 3.1 s under cProfile (1.7 s plain), `engine.character_reference` 688 calls, 0.77 s cumulative; suite 224 in 8.5 s (wall 9.3 s), lock 4.3 s alone |
| B1.2 | done | 224 | green | F-05: the span check in `ground_claim` raises `AssertionError('Evidence span differs from the original text')` explicitly, so it survives `python -O`. The CLI still maps it to exit code 1 with the message `Unexpected internal error (AssertionError)` |
| B1.3 | done | 224 | green | F-06: `encoding='utf-8'` added to 145 calls in 32 files: 142 `read_text`/`write_text` and the 3 text-mode collector lock opens (`Path.open('a')`). Found with an AST scan; each file's AST equals HEAD's apart from the added keyword. Plan 8.7 fifth grep: 0 lines (129 at entry); the `review.py` line is a decision found during execution. `open(` hits left without encoding: binary (`'rb'`, two `'wb'`), `tarfile.open`, and three lines inside a string fixture in `test_check_rules.py`. Left alone: `subprocess.run(..., text=True)` in `verify_cli_install.py`, which decodes the child's stdout in the child's locale. Under `LC_ALL=en_US.iso88591`: 224 pass (before B1.3: 36 failures, 7 errors) |
| B1.4 | done | 225 | green | F-07: `collect_balanced_feedback.py` reports a held lock with `parser.error('Another collector is running in this project')`. In all three collectors, everything after the lock open sits in `try`/`finally: lock.close()`; the statements are otherwise unchanged (AST check). New test `test_held_collector_lock_is_reported_through_the_parser` (+1). Checked by hand with a held lock: before, each collector left its lock handle unclosed (1 `ResourceWarning` each); after, none. The suite still shows only the two known HTTPError warnings |
| B1.5 | done | 226 | green | New `tests/test_console_output.py` (+1): runs the L2 producer in `enforce` and compares stdout exactly: 8 `Embedding <n>/58` lines, then per model (`llama3.1:latest`, `qwen2.5:7b`) 35 `<stage>: <model>, <n> items` lines, then the summary JSON (indent 2). Two runs in different directories print identical text with no time, path or hash, so nothing is normalized. The L2 producer is split into `legacy_dataset` and `run_legacy` (one mode, returns stdout); the lock reports `378 keys, 0 differ` |
| B1.6 | done | 217 | green | CR-D03: four quality-screening scripts and their two test files (9 tests) archived to `~/Archives/AIMediator/scripts/20261103-quality-screening/` with `SHA256SUMS` (checked) and removed; see "Archive and deletions". Register: "Used by" cells of `configs/local-language-routing.json`, `scripts/evidence_quality.py` and `scripts/run_balance_analysis.py` updated, change-log line added. The change-log line points to this record instead of naming the files, because the B1.7 grep covers `docs/reference` |
| B1.7 | done | 217 | green | CR-D04 (F-01, F-02): `scripts/run_local_direction_comparison.py` and `scripts/experiments/demo_evidence_quality.py` archived to `~/Archives/AIMediator/scripts/20261103-broken-entry-points/` with `SHA256SUMS` (checked) and removed. Register, in the same commit: R3 row removed; both scripts dropped from the "Used by" cells of `scripts/run_balance_analysis.py`, `scripts/evidence_quality.py` and the `cases.json` symlink; change-log line added (19 symlinks, 6 forwarding scripts); two more mentions reworded (decision found during execution). Dated notes in `design/balance-analysis.md` and `design/cli.md`, whose sentences now use the past tense. The B1.7 grep and the plan 8.7 fifth grep print nothing; G2 and P3 report 0 |
| B2.1 | done | 217 | green | `engine.run(args, *, api_transport=None, chat_transport=None, embed_transport=None, retrieval_service=None)`. The defaults are looked up in `engine`'s namespace when `run` is called, so the module-global patches still work: `(api_transport or api)` for `/api/tags`; runner factory `Runner`, or `functools.partial(Runner, chat_transport=...)`; retrieval service `retrieval_service`, else `retrieve` when no transport is given, else `partial(retrieve, api_transport=..., embed_transport=...)`. `process`, `Runner` and `retrieve` are unchanged. Checked once with a scratch script: L2 through injected transports, with `engine.api` and `engine.streamed_chat` replaced by a function that raises, gives 0 differing keys |
| B2.2 | done | 217 | green | The patches of `engine` globals became injection: `Runner(..., chat_transport=Mock(return_value=...))` in `test_balance_analysis.py` (2 sites) and `test_balanced_collection.py`; `Mock` objects as `api_transport` and `embed_transport` to `m.retrieve`, with the `embed.call_count == 3` and `api.assert_not_called()` assertions kept; `m.run(args, api_transport=Mock(return_value=tags), chat_transport=self.transport, retrieval_service=retrieval)` in `test_evidence_quality.py`; `engine.run(args, api_transport=fixture_api(transport), chat_transport=transport.chat)` in the lock harness, whose `fixture_api` docstring was updated; and in `replay_balance_admission.py` a `Runner` built with `chat_transport=no_inference`, which raises `RuntimeError('Replay cannot run inference')`. The now unused `patch` imports of the lock harness and the replay script were removed. The B2.2 grep prints nothing (9 lines at entry); the lock fixture is unchanged. The replay script, run before and after the edit on a relevance-only fixture run, gives identical output and the same `RuntimeError` |
| B2.3 | done | 217 | green | Pure move. New `schema.py` (`obj`, `arr`, `STRING`, `NULL_STRING`, `BOOL`; no intra-package import) and `evidence.py` (`PARAMETER`, `CLAIM`, `evidence_units`, `character_reference`, `character_candidates`, `numeric_tokens`, `ground_claim`; imports `copy`, `re`, `balance_policy`, `resources.glossary` and `schema`). `engine.py` imports all twelve names back and keeps its other imports; 931 to 822 lines. Move check from `4a28223`: `same` for all 24 definitions, none changed intentionally. `json.dumps([PARAMETER, CLAIM])` is byte-identical before and after; each `engine` name is the same object as in the new module |
| B2.4 | done | 217 | green | Pure move of `api`, `repeated_claim` and `streamed_chat` into `inference.py`, which now imports `json`, `re`, `glossary_vectors` and `common.strict_json`, and no longer `engine`. Intentionally changed: `Transport` (`_json`: `engine.strict_json` to `strict_json`; `embed`: `engine.glossary_vectors.normalize` to `glossary_vectors.normalize`; `chat`: `engine.streamed_chat` to `streamed_chat`) and `probe` (`engine.glossary_vectors.normalize` to `glossary_vectors.normalize`); with those replacements applied to the old file, both ASTs are identical. Module docstring extended by "Ollama HTTP calls". `engine.py` imports the three names back and keeps `import urllib.request`; 822 to 759 lines. Move check from `f4bf0f5`: `engine.py` 17 of 17 `same`; `inference.py` `CHANGED` for `Transport` and `probe` only. `grep -n engine src/aimediator/inference.py` prints nothing, and `aimediator.inference` and `aimediator.engine` each import first in a fresh interpreter. Plan 8.7 grep 2: 32 lines in 6 modules (37 in 7 at entry) |
| B2.5 | done | 217 | green | Pure move of `schema_for` and `exact_coverage` into the new `stages.py`, which imports `collections.Counter`, `copy`, `re`, `evidence_quality` as `quality`, `balance_policy.attributed_candidates`, `CLAIM`, `character_candidates` and `numeric_tokens` from `evidence`, and `arr` and `obj` from `schema` (all inside its plan 4.2 row). `Counter` is needed by `exact_coverage` and is missing from the work order's list. `engine.py` imports both names back and keeps every import line; 759 to 702 lines. Move check from `18a3771`: `same` for all 14 definitions, none changed intentionally. Each `engine` name is the same object as in `stages` |
| B2.6 | done | 217 | green | Pure move of `Runner` into the new `runner.py`, which imports `json`, `time`, `evidence_quality` as `quality`, `digest`, `strict_json` and `write_json` from `common`, `character_candidates` and `character_reference` from `evidence`, `schema_errors` from `evidence_quality` (the function the `engine` wrapper delegates to with the same arguments), `streamed_chat` from `inference` (the default chat transport), and `exact_coverage` and `schema_for` from `stages` (all inside its plan 4.2 row). The progress `print` and the domain comments move unchanged. `engine.py` imports `Runner` back and keeps its `schema_errors` wrapper and every import line; 702 to 558 lines. Move check from `a2a96c4`: `same` for all 12 definitions, none changed intentionally. `engine.Runner` is `runner.Runner` |
| B2.7 | done | 217 | green | Pure move of `retrieve` into the new `retrieval.py`, which imports `json`, `numpy`, `glossary_vectors`, `digest` and `write_json` from `common`, `api` from `inference` and `anchors` from `resources` (all inside its plan 4.2 row), and holds `POS, NEG = anchors()` at module level, so the function body is unchanged; B5.10 makes it lazy. The `POS, NEG = anchors()` line left `engine.py`, which imports `NEG`, `POS` and `retrieve` from `retrieval` and keeps every import line, `from .resources import anchors` included; 558 to 511 lines. `anchors()` now runs once at import, in `retrieval`. Move check from `af5c247`: `same` for all 11 definitions, none changed intentionally. `json.dumps([POS, NEG])` is byte-identical before (from `engine`) and after (from `retrieval`); `engine.retrieve`, `engine.POS` and `engine.NEG` are the `retrieval` objects |
| B2.8 | done | 217 | green | Pure move of `VERSION`, `relevance_agrees`, `batches`, `aggregate`, `quality_source_counts`, `build_full_coverage`, `validate_modes` and `process` into the new `pipeline.py`, which imports `collections.Counter`, `json`, `evidence_quality` as `quality`, `load_policy` (the review policy), `retrieval_review_agrees` and `triage_retrieval` from `balance_policy`, `write_json` from `common`, `character_reference`, `evidence_units` and `ground_claim` from `evidence`, `retrieve` from `retrieval` and `Runner` from `runner` (all inside its plan 4.2 row). The defaults of `process` are `runner.Runner` and `retrieval.retrieve`. `engine.py` imports the eight names back and now holds only the docstring, its import lines (all kept), `ROOT`, the `schema_errors` wrapper, `run`, `main` and the `__main__` guard; 511 to 153 lines. Its docstring gains a paragraph saying that the facade is removed in B3.6; `main` uses the docstring as the argparse description, so only that description in `python3 -m aimediator.engine --help` changes. Move check from `9ffb4fe`: `same` for all 10 definitions, none changed intentionally. `pipeline.VERSION` is `balance-evidence-v2`, and each `engine` name is the `pipeline` object |
| B2.9 | done | 217 | green | Pure move of `FixtureTransport` from `demo.py` into the new `fixture_transport.py`, which imports `json`, `numpy`, `read` from `common`, `character_candidates` and `character_reference` from `evidence`, `Transport` from `inference`, and `anchors` and `asset_path` from `resources` (all inside its plan 4.2 row). Intentionally changed, qualified names only: `FixtureTransport` (`api`: `engine.NEG` to `anchors()[1]`, which the work order prescribes because the table does not allow `fixture_transport` to import `retrieval`; `chat`: `engine.character_candidates` and `engine.character_reference` to the `evidence` names). With those three replacements applied to the old class, both ASTs are identical. `anchors()` now runs once per embedded text in the fixture's `api`; B5.10 caches it. `demo.py` imports `FixtureTransport` from the new module and drops the imports the move left unused: `inference.Transport` (the table forbids `demo -> inference`), `json`, `numpy` and `engine`; the unused `pathlib.Path` was unused before and stays. `operations.py` imports `FixtureTransport` from `fixture_transport` inside `analyze`, which breaks the `demo` and `operations` cycle. `demo.FixtureTransport` is the same class, so the tests and the lock that import it are unchanged. Move check from `5c7a359`: `engine.py` 3 of 3 `same`; `demo.py` `same demo` and `CHANGED FixtureTransport`. Plan 8.7 grep 2: 29 lines in 5 modules (32 in 6 before) |
| B2.10 | done | 222 | green | New `tests/test_module_layers.py` (+5). It holds the plan 4.2 table copied row by row (27 rows; a scratch parse of the plan gives identical rows), allows `__version__` for every module, and has the transitional allowance (`engine` may import any module; `review`, `reporting`, `operations`, `evaluation`, `demo` and `legacy_review` may import `engine`), marked for removal in B3.6. It parses every top-level module under `Path(__file__).resolve().parents[1] / 'src/aimediator'` with `ast.walk`, so imports inside functions count: relative `ImportFrom` (the first module component, or the imported names when the module is `None`), `import aimediator.<x>`, and also the absolute `from aimediator[.<x>] import` form, which no module uses today. Tests: the scanner on a synthetic source with every form; every module file is in the table, and no subpackage exists yet (B6.2 must extend the test on purpose); `__init__.py` imports nothing from the package (decision found during execution, below); every edge is allowed; no cycle. At HEAD: no violation, no cycle. On the tree of `5c7a359` (before B2.9) it reports exactly `demo -> inference (line 9)`, `operations -> demo (line 70)` and the cycle `demo -> operations -> demo`. Scratch copies with `from . import engine` added to `stages.py`, with an unlisted module, or with an import in `__init__.py` fail as expected |
| B3.1 | done | 222 | green | The five package callers of `engine` import the new modules. `review`, `operations`, `evaluation` and `reporting` replace `from . import engine` with module imports and `engine.<name>` with module-qualified names: `engine.quality.` and `engine.schema_errors` become `evidence_quality.`; `engine.CLAIM`, `ground_claim`, `character_reference` and `evidence_units` become `evidence.`; `engine.relevance_agrees` becomes `balance_policy.retrieval_review_agrees` (the function `pipeline.relevance_agrees` wraps with the same arguments); in `operations`, `engine.load_policy`, `Runner`, `retrieve` and `process` become `balance_policy.`, `runner.`, `retrieval.` and `pipeline.`. Module-qualified names rather than bare imports, because `operations.analyze` defines a local `retrieve` that calls `engine.retrieve`. `legacy_review` imports `digest`, `strict_json` and `write_json` from `common` (same aliases), `CLAIM`, `character_reference` and `ground_claim` from `evidence`, `schema_errors` from `evidence_quality` and `aggregate` from `pipeline`, and drops the unused `ROOT`. `fixture_transport` had no `engine` use. All imports lie inside the plan 4.2 rows. Check: with the replacements applied to the HEAD source, every non-import statement of the five files has an identical AST; each new name is the object `engine` exported, except the two prescribed ones (`schema_errors` is the function the `engine` wrapper delegated to, with the same default). Plan 8.7 grep 2 prints nothing (29 lines in 5 modules at entry) |
| B3.2 | done | 222 | green | T-02: new `tests/support.py` with `CASES` (read with `json.loads` from `asset_path('fixtures/cases.json')`, the file the evaluation-set symlink points to), `case` and `qualified` (now `evidence_quality.qualify` and `evidence.evidence_units`, the objects the forwarders `q` and `m` resolved to). It puts `src/` on `sys.path` itself, so it works whichever test imports it first. These three are the only names two or more test modules used: `test_evidence_quality_evaluation.py` and `test_quality_screening_experiment.py` imported `case` and `qualified` from `test_evidence_quality.py`, which now imports all three from `support` and drops its `ROOT`. The claim builders `numeric_claim` and `basic_claim` and the failure-injecting responder are used only inside `test_evidence_quality.py` and stay there. No test module imports another one. Plan 8.5: 222 pass from a foreign directory |
| B3.3 | done | 222 | green | Three commits, one per area: evidence and quality (`test_evidence_quality`, `test_evidence_quality_evaluation`, `test_quality_screening_experiment`), balance (`test_balance_analysis`, `test_balance_review_pipeline`, `test_balance_source_review`, `test_balanced_collection`), and the rest (`test_cli_product`, `test_refactored_boundaries`, `test_expand_feedback`). Forwarder names became package names: the `engine` facade names come from `evidence`, `pipeline`, `stages`, `inference`, `retrieval`, `runner` and `common` (`digest` as the alias of `common.sha`), `schema_errors` from `evidence_quality`, and `engine.run` stays; `review_balance_sources` became `aimediator.legacy_review`, `evaluate_evidence_quality` became `aimediator.quality_scoring` and `balance_policy` became `aimediator.balance_policy`. Each new name is the object the forwarder exposed (checked by identity), except `schema_errors`, the function the `engine` wrapper delegated to. The `streamed_chat` tests patch the shared `urllib.request` module directly (blueprint 4.2 item 3) instead of `engine.urllib.request`; it is the same module object. `test_evidence_quality_evaluation` dropped its unused `q` and `m` imports. A scripts directory stays on `sys.path` only where a test imports a script: `scripts/experiments` in `test_evidence_quality` (`prepare_balance_design`), `test_balance_review_pipeline` (`evaluate_balance_review`, `prepare_balance_design`, `run_balance_regression_live`, `export_balance_review_followups`) and `test_quality_screening_experiment`; `scripts/collect` in `test_balanced_collection` and `test_expand_feedback`; the collector, screening and grounded-pilot tests load their script by file path; `test_refactored_boundaries` keeps `scripts/` for its forwarder-identity test until B4.2. Plan 8.7 grep 1 prints nothing under `tests` (7 files at entry). The test count per module equals `restructure-b2` (222). Plan 8.5: 222 pass from a foreign directory |
| B3.4 | done | 222 | green | CR-D06 (F-03). Three commits: live (`2251a75`), offline research (`5c7ba45`), and `run_quality_screening_experiment` with `run_grounded_feedback_live`. Every experiment script starts with the plan 4.3 bootstrap (`sys.path.insert(0, <checkout>/src)`, replacing the line that put `scripts/` on the path) and imports `aimediator` modules; the forwarder names map as in B3.3, and sibling imports of `prepare_balance_design` stay (blueprint 3.6). Prompts and configs are read with `asset_path`; the pilot reads its prompt with `asset_path` instead of the checkout path of the same file (CR-D02: bootstrap and asset path only). `--prompt-dir` of `run_balance_regression_live.py` defaults to `asset_path('prompts')`. Identities follow blueprint 3.6, key by key in "Experiment identities (B3.4)" below. `ROOT`: four scripts imported it from the `engine` facade, where it is `Path.cwd()`; they now define `ROOT = Path(__file__).resolve().parents[2]` until B6.1 (`check_balance_regressions`, `evaluate_balance_review`, `prepare_balance_design`, `run_quality_screening_experiment`), so their data defaults name the same files when run from the checkout root and no longer depend on the current directory elsewhere. The other scripts used `ROOT` only for forwarder, prompt or config paths and no longer need one. `replay_balance_admission` drops its unused `triage_retrieval` and `load_policy` imports and calls `balance_policy.retrieval_review_agrees`. Checks: all 13 scripts print `--help` with exit 0 from a foreign directory, which stays empty. Every script except the pilot was run offline before and after (a scratch harness stubbing `api` and `Runner` in the script, on fixture runs): apart from the identity and snapshot fields in the table and the wall-clock fields, every output file is identical; the `asset_sha256` values equal the asset digests, and the module snapshots equal `package_code_sha256`. Plan 8.7 grep 1 prints nothing |
| B3.5 | done | 222 | green | `scripts/collect/screen_feedback.py` starts with the plan 4.3 bootstrap and loads `G` from `asset_path('data/glossary.json')` instead of the `data/glossary.json` symlink (the same file). Its local `ROOT` stays for the `--overrides` default. Lock target L4 unchanged: `378 keys, 0 differ`. The four collectors print `--help` with exit 0 from a foreign directory; `collect_balanced_feedback` and `expand_feedback` import `screen_feedback` as before |
| B3.6 | done | 222 | green | The facade is gone: `engine.py` drops the re-exported names, the `schema_errors` wrapper and every import that only the moved code used (`copy`, `Counter`, `defaultdict`, `re`, `time`, `urllib.request`, `numpy`, `strict_json`, `anchors`, `glossary` and seven `balance_policy` names). It keeps the imports `run` and `main` use and holds the docstring, `ROOT`, `run`, `main` and the `__main__` guard; 153 to 130 lines. The B2.8 docstring paragraph about the facade is removed, so the docstring and the `python3 -m aimediator.engine --help` text equal `restructure-b1` again. `run` and `main` have the same AST as before, every global name they load resolves, and no import is unused. `tests/test_module_layers.py` loses the transitional allowance (`FACADE`, `FACADE_USERS`); `allowed` checks the table only, 5 tests pass, and a scratch copy with `from . import engine` in `review.py` fails with `review -> engine (line 5)`. Plan 8.7 greps 1 and 2 print nothing. Plan 8.5: 222 pass from a foreign directory. Plan 8.2: `"passed": true`, `"commands": 18`; the wheel's 27 modules equal the checkout |
| B4.1 | done | 222 | green | CR-D05 (D9): living documents name the package commands and asset paths. `README.md`: section "Research commands" lists `python3 -m aimediator.engine`, `.legacy_review`, `.quality_scoring` and `.glossary_vectors` and says once that they need `pip install -e .` or `PYTHONPATH=src`; its "Layout" line for `scripts/` reads "Collection, experiment and maintenance scripts" (plan B4.1 names "Layout"; the `prompts/` and `configs/` lines are B4.3). `guides/cli-usage.md`: the quality-label command, and the section "Compatibility and validation scope" becomes "Research commands and validation scope" (its symlink sentence stays for B4.3). `design/balance-analysis.md`: lines 6, 8, 29 and 170 (168 at `7282f49`), and the five prompt and routing paths as `src/aimediator/assets/...`. `design/cli.md` section 2 and `design/evidence-quality.md` lines 33, 42 and 47 keep their dated sentences with dated notes (2026-11-04) naming the module and command. The B4.2 grep covers `docs/design`, unlike the B1.7 grep, so those sentences name the old scripts by file name only (`run_balance_analysis.py`), as the B1.7 note in `balance-analysis.md` already did; the first note of each section says they were files directly under `scripts/`. Beyond the listed lines, for R1 under CR-D07: `design/evidence-quality.md` lines 37 and 38 (prompt paths in brace form, which the plan 8.7 grep does not match) cite the asset paths; `reference/glossary-vector-index.md` line 8 and `reference/glossary.md` line 46 cite `src/aimediator/assets/data/glossary.json` (both are "Used by" entries of the `data/glossary.json` register row); and `design/cli.md` section 5 gets one dated note on its instruction to keep compatibility adapters. All five documented commands print `--help` with exit 0 under `PYTHONPATH=src`; their options equal the forwarders' (only the program name differs). D5 0; the B4.2 grep prints only the six register rows that B4.2 removes |
| B4.2 | done | 221 | green | CR-D05 (R2): the six pure forwarders `run_balance_analysis.py`, `review_balance_sources.py`, `evaluate_evidence_quality.py`, `glossary_vectors.py`, `evidence_quality.py` and `balance_policy.py` archived to `~/Archives/AIMediator/scripts/20261104-forwarders/` with `SHA256SUMS` (checked) and removed; see "Archive and deletions". Register: the six rows removed, the section "Forwarding scripts" says none remain, change-log line added (19 symlinks, no forwarding script). `test_refactored_boundaries.test_compatibility_imports_share_package_state` deleted (-1 test): it asserted only that each forwarder re-exported its package module (blueprint 4.2, item 5), and nothing is left to import; the `scripts/` path line and the `importlib` import that only this test used went with it. Before the step, escalation E-2: the glossary index manifest named the glossary forwarder; the owner chose option (a), applied in `376403a`. The B4.2 grep prints nothing; G2 and P3 report 0; `scripts/` has no tracked file at its top level |
| B4.3 | done | 221 | green | CR-D07, CR-D08 (R1): the 14 `prompts/` links, the three policy and routing links in `configs/` and `data/glossary.json` removed; `prompts/` is gone, and `git ls-files -s` lists one symlink, `data/evaluation/evidence-quality-synthetic-v1/cases.json`. Link targets archived as `~/Archives/AIMediator/scripts/20261104-compatibility-links/SYMLINKS.txt` with `SHA256SUMS` (checked); see "Archive and deletions". Register: the 18 rows removed; the `cases.json` removal condition reads "kept (CR-D08): member of the frozen evaluation set `evidence-quality-synthetic-v1`", and its "Used by" cell drops `test_evidence_quality.py`, which reads the packaged fixture through `tests/support.py` since B3.2; R1 gains the CR-D07 reading; the prompts section says none remain; change-log line added (1 symlink, no forwarding script). README "Layout": no `prompts/` line, `configs/` reads "Collection settings", and the assets bullet says the packaged assets are the only copy and names the one remaining link. `guides/cli-usage.md`: the symlink sentence removed. Escalations during the step: E-3 (a test read a link path built by concatenation; fixed in `16412d4`) and E-4 (this record reached the D7 limit; `2127d63`); the work in progress was stashed and restored. Plan 8.7, third grep: outside the planning documents it matches only asset-relative names in `src`, `scripts` and `tests`, and the narrowed command of the B4.1 decision prints nothing |

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

## Experiment identities (B3.4)

CR-D06 rule (blueprint 3.6), as applied: each hash of a forwarder or of a
symlink path is replaced by `package_code_sha256`
(`run_store.code_manifest()['modules']`, the 27 top-level package modules)
and `asset_sha256` (`{name: SHA-256 of asset_path(name)}`), and
`script_sha256` stays. `asset_sha256` lists every asset the script reads,
directly or through the package functions it calls:
`character_reference`, `ground_claim` and the `verify` stage of `Runner`
read `data/glossary.json` and `configs/balance-review-policy.json`;
`evidence_quality.load_policy` reads `configs/evidence-quality-policy.json`.
Content digests that were already in an identity (`prompts`, `policy`,
dataset and run digests) are unchanged. Code snapshots of package modules
go to `code-snapshot/<module>.py`, one per module in
`package_code_sha256`.

| Script | Record | Removed | Added | Assets in `asset_sha256` |
| ------ | ------ | ------- | ----- | ------------------------ |
| `run_balance_numeric_extraction_live` | `manifest.json` | `runner_sha256`, `policy_module_sha256` | `package_code_sha256`, `asset_sha256` | `configs/balance-review-policy.json`, `data/glossary.json`, `prompts/summarize-balance.{en,zh}.txt`, `prompts/verify-balance.{en,zh}.txt` |
| `run_balance_regression_live` | `manifest.json` | `runner_sha256`, `policy_module_sha256`, `policy_sha256` | `package_code_sha256`, `asset_sha256` | `configs/balance-review-policy.json`, `data/glossary.json`; the prompts come from `--prompt-dir` and stay identified by the `prompts` digests |
| `run_balance_semantic_controls_live` | `manifest.json` | `runner_sha256` | `package_code_sha256`, `asset_sha256` | as `run_balance_numeric_extraction_live` |
| `diagnose_evidence_quality_live` | `manifest.json` `identity`; the files written next to it | `code_sha256` (three forwarders and the script); the forwarder copies `evidence_quality.py`, `run_balance_analysis.py`, `balance_policy.py` | `script_sha256` (the value of the script's former `code_sha256` entry), `package_code_sha256`, `asset_sha256`; `code-snapshot/<module>.py` (27 files). The copy `diagnose_evidence_quality_live.py` stays | the three configs, `data/glossary.json`, `prompts/{evidence-quality,quality-extract,quality-verify,summarize-balance,verify-balance}.{en,zh}.txt` (14) |
| `replay_balance_admission` | `replay-results.json` | `current_runner_sha256`, `current_policy_module_sha256` | `package_code_sha256`, `asset_sha256` | `configs/balance-review-policy.json`, `prompts/relevance.{en,zh}.txt`, `prompts/retrieval-review.{en,zh}.txt` |
| `run_quality_screening_experiment` | `manifest.json` `identity`; the snapshot files | `code_and_data_sha256` (three forwarders, the script, and three assets through their symlinks); `snapshot-run_balance_analysis.py`, `snapshot-evidence_quality.py`, `snapshot-balance_policy.py` | `script_sha256`, `package_code_sha256`, `asset_sha256`; `code-snapshot/<module>.py` (27 files). `snapshot-run_quality_screening_experiment.py` and the three asset snapshots stay, read with `asset_path` | the three configs, `data/glossary.json`, `prompts/evidence-quality.{en,zh}.txt` (6) |
| `run_balance_controls_live`, `check_balance_regressions`, `evaluate_balance_review`, `export_balance_review_followups`, `prepare_balance_design`, `review_balance_live`, `run_grounded_feedback_live` | — | none | none | no forwarder or symlink hash; their digests (`fixtures_sha256`, `adjudication_source_sha256`, `raw_model_report_sha256`, the pilot's metadata) hash data files and are unchanged |

Consequences, all within CR-D06:

- `diagnose_evidence_quality_live` and `run_quality_screening_experiment`
  pass their identity to `Runner` as `quality_identity`, so their request
  IDs (cache keys) change. That is the intended effect: earlier output
  directories cannot be resumed under the new identity.
- `run_quality_screening_experiment` also sends its identity to the model
  as the `quality_contract` field of every quality request. The user
  content of those requests therefore changes by exactly the identity
  fields above: about 2.3 KB more per request (27 module and 6 asset
  digests in place of 7 file digests), on top of an identity of about
  9.9 KB that already holds both quality prompts and the policy. The
  quality context is 16,384 tokens. No other script puts its identity
  into a request, so their request bytes are unchanged.

## Archive and deletions

| Path | Archive location | SHA256SUMS entry | Reason | Step |
| ---- | ---------------- | ---------------- | ------ | ---- |
| `scripts/experiments/present_quality_screening_results.py` | `~/Archives/AIMediator/scripts/20261103-quality-screening/` | `96d3ed447e0b58609e084b0d4221968c87886e6ec8fb507d2346a445ba7bb3a6` | One-off presentation of the finished 100-comment quality-screening experiment; emits a Cursor canvas TSX file (R-05, CR-D03) | B1.6 |
| `scripts/experiments/protect_quality_screening_checkpoint.py` | same | `842c35712f8b801282fa7783bc201737964f94e8a13de649cde49245390af86a` | One-off checkpoint guard of that experiment (R-05, CR-D03) | B1.6 |
| `scripts/experiments/resume_quality_screening_local.py` | same | `a44bc854fcd03865c647533d6e76a5281cd4c2495862ee88b0609410110b5766` | One-off resume of that experiment; patches `engine` at import (R-05, CR-D03) | B1.6 |
| `scripts/experiments/run_quality_screening_recovery.py` | same | `62521df7d54939303c10e1bec221742788064e8c7f8ba06e602f541a3a23d795` | One-off recovery of that experiment; holds two prompts outside the assets (R-05, R-02, CR-D03) | B1.6 |
| `tests/test_quality_screening_compact.py` | same | `dffa9ed52be0a7d521bc079b65ac9ca5bb0a41f00f7a09a590c1887b0c699743` | 4 tests of the archived `run_quality_screening_recovery.py` (CR-D03) | B1.6 |
| `tests/test_quality_screening_recovery.py` | same | `b05f3300cd0fb403c3909d2394e735b6941359f16841e135257496ebbf8c3ef1` | 5 tests of the archived `resume_quality_screening_local.py` (CR-D03) | B1.6 |
| `scripts/run_local_direction_comparison.py` | `~/Archives/AIMediator/scripts/20261103-broken-entry-points/` | `23aba938006dc4ac8c1e45c7f6e03d24bd2a71f7d8c177b03810ec01a4355147` | Broken wrapper, registered under R3 (F-01: `AttributeError` on `args.evidence_quality`); CR-D04 | B1.7 |
| `scripts/experiments/demo_evidence_quality.py` | same | `463edad8a19da97601d9e47016628d7a2ec15b2c42d92029f0591185fe4d4f98` | Broken demo (F-02: `TypeError` from its retrieval stub), superseded by `aimediator demo`; CR-D04 | B1.7 |
| `scripts/run_balance_analysis.py` | `~/Archives/AIMediator/scripts/20261104-forwarders/` | `2cacf20f9db5af755fd268595fdba1e2d969fdeb14e1578c7af1340bcddd84f1` | Pure forwarder to `aimediator.engine`; the command is `python3 -m aimediator.engine` (R2, CR-D05) | B4.2 |
| `scripts/review_balance_sources.py` | same | `b72270d7f30544bfd1534181e865da52928d6f3a67a9f670702b874e5e6566c0` | Pure forwarder to `aimediator.legacy_review`; the command is `python3 -m aimediator.legacy_review` (R2, CR-D05) | B4.2 |
| `scripts/evaluate_evidence_quality.py` | same | `3579e769a2548544dbcd86ec025c53b1592c5e837df1392fa1dc34e945b11b8e` | Pure forwarder to `aimediator.quality_scoring`; the command is `python3 -m aimediator.quality_scoring` (R2, CR-D05) | B4.2 |
| `scripts/glossary_vectors.py` | same | `112b26b49ab3285f65a88b4d3ce54f49873fde4a5585c53245b66e0f3a1e568b` | Pure forwarder to `aimediator.glossary_vectors`; the command is `python3 -m aimediator.glossary_vectors` (R2, CR-D05) | B4.2 |
| `scripts/evidence_quality.py` | same | `2c39facd691408933c79a825266ace243b67f53cf49e1b438111eeeed93140ae` | Import-only forwarder to `aimediator.evidence_quality`; no importer since B3.3 and B3.4 (R2, CR-D05) | B4.2 |
| `scripts/balance_policy.py` | same | `60ff8df89a53d4014bcd35fe7e98689c7ef8b4bfd8900b8c16621f39a1676fb2` | Import-only forwarder to `aimediator.balance_policy`; no importer since B3.3 and B3.4 (R2, CR-D05) | B4.2 |
| `prompts/{evidence-quality,quality-extract,quality-verify,relevance,retrieval-review,summarize-balance,verify-balance}.{en,zh}.txt` (14 symlinks) | `~/Archives/AIMediator/scripts/20261104-compatibility-links/SYMLINKS.txt` (one line per link) | `a3f446c52d8ced8ed0200e461f526aec9cdffb2b83326a62e7bc9a0b4e38033c` (`SYMLINKS.txt`) | Compatibility links to `src/aimediator/assets/prompts/`; R1 under the CR-D07 reading | B4.3 |
| `configs/balance-review-policy.json`, `configs/evidence-quality-policy.json`, `configs/local-language-routing.json` (3 symlinks) | same | same | Compatibility links to `src/aimediator/assets/configs/`; R1 under the CR-D07 reading | B4.3 |
| `data/glossary.json` (symlink) | same | same | Compatibility link to `src/aimediator/assets/data/glossary.json`; R1 under the CR-D07 reading | B4.3 |

B1.6: the copies were taken from `99d57a9`, so the scripts include the B1.3
encoding keywords; the earlier bytes are in git history. `sha256sum -c
SHA256SUMS` passed in the archive directory, and each entry equals the
SHA-256 of the blob at `99d57a9`. The existing `scripts/SHA256SUMS` was not
touched. Before the deletion, `git grep` found the six names only in the
two test files (which import two of the scripts and were archived with
them), the planning documents, the frozen reorganization record, the
register (updated in the same commit), and two frozen curated summaries,
`reports/quality-screening-existing-100-v1/summary/recovery.md` and
`reports/quality-screening-existing-100-recovered-v2/summary/recovery.md`.
Those cite the pre-reorganization command paths (`scripts/<name>.py`) as
provenance of the experiment that CR-D03 names, and stay unchanged (P2).

B1.7: the copies were taken from `12cd026`. `sha256sum -c SHA256SUMS`
passed in the archive directory, and each entry equals the SHA-256 of the
blob at `12cd026`. No code, test or configuration used either script.
Before the deletion, `git grep` found the two names, apart from the planning
documents, in: the register and the two design documents (updated in the
same commit); the frozen records `20261026-evidence-quality-implementation.md`
and `20261103-reorganization.md`, and the archived reorganization plan;
`data/raw/feedback/20261015-expanded/manifest.json`, whose consumer list
names the wrapper (`--dataset` default); and
`reports/evidence-quality-verification-v1/summary/verification.json`, which
records the demo script's SHA-256 under its pre-reorganization path.
`data/raw/` and `reports/` are frozen (P1, P2) and keep these historical
mentions.

B4.2: the copies were taken from `376403a`. `sha256sum -c SHA256SUMS`
passed in the archive directory, and each entry equals the SHA-256 of the
blob at `376403a`. Before the deletion, `git grep` found the six paths,
apart from the planning documents and the register (updated in the same
commit), only in: the frozen records `20261026-evidence-quality-implementation.md`,
`20261027-balanced-validation.md`, `20261103-reorganization.md` and this
record; the archived `readme-research-history.md`; and the manifests and
summaries of six curated reports (`20261022-balance-engineering-review`,
`20261027-screening-audit`, `evidence-quality-live-verified-v1`,
`evidence-quality-verification-v1`, `quality-screening-existing-100-v1`
and its `-recovered-v2`), which record the code of their runs. These keep
their historical paths (CR-D07, P2). The manifest of
`data/processed/glossary-vectors/` named the glossary forwarder as its
generating command; it names the module command since the owner's answer
to escalation E-2 (`376403a`).

B4.3: the links are archived as `SYMLINKS.txt`, one line `<path> -> <target>`
per link, written from the link blobs at `16412d4` (decision "Archive form
of the deleted symlinks"); it equals `readlink` of each link, and
`sha256sum -c SHA256SUMS` passed. Before the deletion, the only code or test
user of a link path was `test_cli_product.py` (escalation E-3, fixed in
`16412d4`). Every other match of plan 8.7, third grep, in `src`, `scripts`
and `tests` is a name relative to the assets directory (decision "Reading
of plan 8.7, third grep, after B4.3"). The other files that name the paths
are the planning documents, the register (updated in the same commit), the
frozen records `20261022-alias-review.md`, `20261022-balance-review-v2.md`,
`20261026-evidence-quality-implementation.md`,
`20261027-balanced-validation.md`, `20261103-reorganization.md` and this
record, the archived `readme-research-history.md`, the run manifests and
summaries of five curated reports (`20261027-balanced-validation`,
`20261027-screening-audit`, `evidence-quality-verification-v1`,
`quality-screening-existing-100-v1` and its `-recovered-v2`), and the
`source` value of the glossary index manifest, which says how the current
index was built (E-2). These keep their historical paths (CR-D07, P1, P2).

## Decisions found during execution

### Code-only lock exemptions in plan 5.3 item 4 (found by B0-V)

- **Question**: plan 5.3 item 4 allows only `.writer.lock` as a whole-file
  exclusion. The B0 handoff also exempts the code-only files
  `*-snapshot.py` and `code-manifest.json`, and the lock does so (see the
  B0-V note). Which wording holds?
- **Answer**: the owner, 2026-11-03, given to session B0-V: reword plan 5.3
  item 4 to allow the code-only exemptions. B0-V made the correction at
  the owner's instruction in its own `docs` commit, which also records
  this answer. The lock and its fixture are unchanged.
- **Effect on B1**: the commit follows the `restructure-b0` tag. The B1
  boundary check, run from `restructure-b0`, therefore prints
  `docs/plans/code-restructuring.md` for this commit. That line is
  expected and is not a B1 change.

### Encoding grep line in `review.py` (found in B1.3)

- **Question**: plan 8.7, fifth grep, checks one line at a time. At entry
  it printed `src/aimediator/review.py:171`. That `write_text` call spans
  13 lines and already passes `encoding='utf-8'` on its last line, so the
  grep line is a false positive. The plan counts it as the one `src/` call
  in F-06. B1.3 and B1-V checklist item 6 require the grep to print
  nothing. How is the line resolved?
- **Options**: (a) move the keyword to the call's first line, as
  `write_text(encoding='utf-8', data='''...''')`. The file's bytes and
  behavior are unchanged. (b) Leave the call, and have the owner amend the
  grep or accept one known line. The plan is outside the B1 boundary.
- **Recommendation**: (a). It changes only where the encoding argument
  sits. Restoring the old two lines undoes it, the lock stays green, and
  no rule or content changes.
- **Status**: implemented in B1.3 under plan section 1, item 8. The owner
  may reject it at the B1 review.

### Register mentions outside the B1.7 rows (found in B1.7)

- **Question**: the B1.7 grep of the B1 work order covers `docs/reference`
  and must print nothing after B1.7. Besides the row and the "Used by"
  cells that the work order names, the register named the wrapper in two
  more places: the inventory paragraph and the batch 3 review (P3-D01)
  change-log entry. How are they handled?
- **Options**: (a) reword both to describe the wrapper without its file
  name, pointing to the B1.7 change-log entry; (b) leave them, so that the
  grep prints two lines, which the owner would have to waive.
- **Recommendation**: (a). The register is a living reference document
  inside the B1 boundary. Both passages keep their meaning, a revert
  undoes the change, and nothing outside the register changes.
- **Status**: implemented in B1.7 under plan section 1, item 8. For the
  same reason, the B1.6 and B1.7 change-log lines point to this record for
  the file names instead of naming them.

### `__init__.py` and the module table (found in B2.10)

- **Question**: the B2.10 test asserts that every module file appears in
  the plan 4.2 table. `src/aimediator/__init__.py` has no row: it defines
  only `__version__` and imports nothing. Plan 4.2 says that a table change
  needs a registered decision. How is `__init__.py` handled?
- **Options**: (a) treat `__init__.py` as the package itself, the source of
  the `__version__` that every module may import: leave it out of the
  coverage assertion, and give it its own assertion that it has no
  intra-package import. The copied table stays identical to plan 4.2.
  (b) Add an `__init__` row with no allowed import to the plan table and to
  the test's copy. The plan is outside the B2 boundary. (c) Leave the
  coverage assertion failing until the owner decides.
- **Recommendation**: (a). The test is as strict as under (b), no document
  outside the boundary changes, a revert of the B2.10 commit undoes it, the
  lock stays green, and no rule changes.
- **Status**: implemented in B2.10 under plan section 1, item 8. The owner
  may reject it; (b) would then be a plan correction and a one-row change
  of the test.

### Scope of `asset_sha256` (found in B3.4)

- **Question**: blueprint 3.6 asks for `asset_sha256` "for every asset the
  script reads". Several scripts read assets only through package
  functions: `character_reference`, `ground_claim` and the `verify` stage
  of `Runner` read `data/glossary.json` and
  `configs/balance-review-policy.json`, and `evidence_quality.load_policy`
  reads `configs/evidence-quality-policy.json`. Do those reads count?
- **Options**: (a) count them: list every asset whose content can change
  the script's results, read directly or through the package; (b) list
  only the assets the script opens itself.
- **Recommendation**: (a). It is what F-03 asks of an identity, which must
  detect every change that can alter results, and `engine.run` already
  hashes the glossary and the review policy although `engine` reads
  neither directly. Assets read only at import time and unused by the
  script (the retrieval anchors) are not listed. The prompts that
  `run_balance_regression_live` reads from `--prompt-dir` stay identified
  by their content digests.
- **Status**: implemented in B3.4 under plan section 1, item 8: a revert
  of the three B3.4 commits undoes it, the lock stays green, `RULES.md` is
  unchanged and nothing is deleted. It was registered with the B3-2
  session-log entry, after the B3.4 commits instead of before them. The
  owner may choose (b); that would shorten the `asset_sha256` lists of
  `run_balance_numeric_extraction_live`, `run_balance_regression_live`,
  `run_balance_semantic_controls_live` and `diagnose_evidence_quality_live`
  (table in "Experiment identities (B3.4)").

### Reading of plan 8.7, third grep, after B4.3 (found in B4.1)

- **Question**: work order B4.3 says that afterwards the third grep "may
  match only the planning documents". Its pattern also matches names
  relative to `src/aimediator/assets/`, which never resolve through the
  root links: the `asset_path(...)` arguments in the package
  (`balance_policy`, `config`, `engine`, `evidence_quality`,
  `glossary_vectors`, `resources`), in `screen_feedback.py` and in
  `tests/test_balance_analysis.py`; the `ASSETS` tuples and the snapshot
  loop of six experiment scripts, each name read with `asset_path`; the
  `prompt` values inside the packaged asset
  `src/aimediator/assets/configs/local-language-routing.json`, which no code
  reads; and one synthetic path in the temporary tree of the G8 test in
  `tests/test_check_rules.py`. The B3-2 session-log entry reported this for
  B4. How is the B4.3 condition read?
- **Options**: (a) read it as "no match outside the planning documents names
  a root link path": every remaining match must resolve against the assets
  directory or lie in a test's temporary tree, checked with the narrowed
  command below, which must print nothing; (b) rename the asset-relative
  names, which changes code, an asset (plan stop condition) and experiment
  identities; (c) leave the condition unmet for the owner to waive.
- **Recommendation**: (a). It checks what R1 asks, that nothing uses the
  link paths, changes no file, and leaves the plan's command as it is.
- **Status**: registered before B4.3 and applied in its check; open to the
  owner. Measured in B4.1: the narrowed command prints only
  `README.md` line 110 and the 18 register rows, which B4.3 removes.

```sh
git grep -nE "(^|[^a-z/])(prompts/[a-z-]+\.(en|zh)\.txt|configs/(balance-review-policy|evidence-quality-policy|local-language-routing)\.json|data/glossary\.json)" -- src scripts tests README.md docs/guides docs/design docs/reference ':!src/aimediator/assets' | grep -vE "asset_path\('|^scripts/[a-z_/]+\.py:[0-9]+:( *ASSETS = \(| +'(configs|data|prompts)/| +for name in \('configs/)|^tests/test_check_rules\.py:[0-9]+: +'prompts/relevance\.en\.txt', 'README\.md'"
```

### Archive form of the deleted symlinks (found in B4.1)

- **Question**: plan section 1, item 9 asks for a copy of every deleted
  tracked file in `~/Archives/AIMediator/scripts/<YYYYMMDD>-<topic>/` with a
  `SHA256SUMS` file. B4.3 deletes 18 symlinks. A symlink's only content is
  its target path; a copied link dangles in the archive, and `sha256sum`
  cannot read it. How are the links archived?
- **Options**: (a) as the reorganization baseline backup did
  (`SYMLINKS.txt`, see the reorganization record): one line
  `<path> -> <target>` per link, from the link's git blob, in a file listed
  in `SHA256SUMS`; (b) recreate the links in the archive, which
  `sha256sum -c` cannot check; (c) no archive copy, only git history and
  this record.
- **Recommendation**: (a). The full content of every link is kept outside
  git in a file that `sha256sum -c` checks. It follows an existing
  precedent, changes nothing in the checkout, and leaves behavior and
  `RULES.md` unchanged. The six forwarders of B4.2 are regular files and
  are copied as item 9 says.
- **Status**: registered before B4.3 and applied in it, under plan
  section 1, item 8; open to the owner.

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

### E-2 The glossary index manifest names a forwarder (B4.2)

- **Step**: B4.2.
- **Question**: `data/processed/glossary-vectors/manifest.json`, the P1
  descriptor of the reproducible glossary vector index, records
  `"generating_command": "python3 scripts/glossary_vectors.py build"` and
  the consumer `"scripts/glossary_vectors.py search"`. B4.2 deletes that
  forwarder, so the recorded command would fail. This is the second
  trigger of work order B4, section 6: a deleted path is still used
  outside the planning documents. The file is under `data/`, outside the
  B4 boundary, and no session may change `data/` (blueprint 5.3, item 4).
  Its `source` value also says the index was built "through the
  data/glossary.json link", which B4.3 deletes; that describes how the
  current build was made and stays true. How is the manifest handled?
- **Options**:
  - (a) The owner authorizes one `data` commit that sets
    `generating_command` to `python3 -m aimediator.glossary_vectors build`
    and the consumer to `python3 -m aimediator.glossary_vectors search`.
    Nothing else in the file changes: `files_sha256` covers only the
    ignored index files, and the index identity hashes the source, the
    texts and the model, not the command. B4.2 then runs as written.
  - (b) Keep `scripts/glossary_vectors.py` registered until the manifest
    changes. B4.2 deletes five forwarders, and B4-V checklist item 2
    ("`scripts/` has no file at its top level") needs a waiver.
  - (c) Read the manifest as a historical record, as B1.7 did for the
    consumer list of `data/raw/feedback/20261015-expanded/manifest.json`,
    and delete all six. The recorded command stays wrong until someone
    updates the manifest.
- **Recommendation**: (a). P1 requires the generating command of
  processed data, and the change is two string values in a hand-written
  descriptor (its `manifest_written` names reorganization batch 3), with
  no effect on the index. (c) differs from B1.7: that consumer was a
  broken wrapper with no replacement, while this manifest is the
  instruction for rebuilding the data.
- **Blocked**: B4.2, and B4.5, whose ADR records the removal of the
  layers. B4.3 and B4.4 do not depend on B4.2.
- **Answer**: the owner, 2026-11-04, given to session B4-1: option (a).
  B4-1 changed the two values at the owner's instruction in its own
  `data` commit, which also records this answer; the rest of the
  manifest, the `source` value included, is unchanged. The commit lies
  outside the B4 boundary, so the B4-V boundary check prints
  `data/processed/glossary-vectors/manifest.json` for it. B4.2 then ran
  as written.

### E-3 A test reads a deleted prompt link (B4.3)

- **Step**: B4.3.
- **Question**: with the 18 links deleted in the working tree,
  `test_cli_product.test_existing_script_and_package_use_same_prompt_bytes`
  errors with `FileNotFoundError`. Line 337 reads its expected bytes from
  the checkout path `prompts/summarize-balance.<lang>.txt`, built by string
  concatenation (`'prompts/summarize-balance.'+lang+'.txt'`), so the plan
  8.7 third grep, the B0.4 count and the register's "Used by" cells all
  missed it. A wider scan of `src`, `scripts` and `tests` for the removed
  directory names outside `asset_path` finds no other user. This is the
  second trigger of work order B4, section 6: a deleted path still used
  outside the planning documents. The file is outside the B4 boundary. How
  is the test handled?
- **Options**:
  - (a) The owner authorizes one `chore` commit, before B4.3, that changes
    only the expected side of line 337 to
    `asset_path('prompts/summarize-balance.'+lang+'.txt')`, the file the
    link points to (`asset_path` is already imported). The assertion and
    the test count stay; the test still checks that `prompts_for('off')`
    hands the packaged summarize prompt to extraction byte for byte. B4.3
    then runs as written.
  - (b) Delete the test, whose subject, the checkout path used by the old
    scripts, no longer exists: 220 tests, so B4 becomes -2 against the -1
    of blueprint 1.3.
  - (c) Keep `prompts/summarize-balance.{en,zh}.txt` registered until the
    test changes. `prompts/` stays, so B4.4 (G3) and B4-V checklist item 2
    cannot pass.
- **Recommendation**: (a). The test keeps its value with the single
  source, the change is one expression, a revert undoes it, and the
  behavior lock is not involved.
- **Blocked**: B4.3, and through it B4.4 (G3 needs `prompts/` gone) and
  B4.5. The B4.3 work in progress is stashed as
  `WIP Step B4.3: escalation E-3`.
- **Answer**: the owner, 2026-11-04, given to session B4-1: option (a).
  B4-1 changed the expression at the owner's instruction in its own
  `chore` commit, which also records this answer, after the E-4 commit
  that made the record committable again, then restored the stashed
  B4.3 work and finished B4.3. The commit lies outside the B4 boundary,
  so the B4-V boundary check prints `tests/test_cli_product.py` for it.

### E-4 The change record reaches the D7 size limit (B4.3)

- **Step**: B4.3 (any further entry).
- **Question**: this record is 102,203 bytes at `6409098`, against the D7
  limit of 102,400. The answer to E-3 pushed it over, and the pre-commit
  hook refused that commit. RULES D7 says a Markdown file over 100 KB
  "must be justified", but `check_rules.py` has no way to record a
  justification. B4-1, B4-V and batches B5 to B7 add more entries. How is
  the record kept committable?
- **Options**: (a) a justified-files map for D7 in `check_rules.py`,
  listing only this record with its reason, and the existing D7 test
  extended (no new test); (b) freeze this record at B3 and continue in a
  second record, which changes the plan, the blueprint and the handoffs;
  (c) condense the record, which buys room for this session only.
- **Recommendation**: (a). D7 already allows justified files; only the
  check lacks the means. `RULES.md` does not change.
- **Blocked**: every commit that adds to this record.
- **Answer**: the owner, 2026-11-04, given to session B4-1: option (a).
  B4-1 added `D7_JUSTIFIED` at the owner's instruction in its own `chore`
  commit, which also records this answer. `check_d7` skips a listed file;
  `test_d7_json_and_size` writes an oversize file at this record's path and
  still expects only the two unlisted violations. The test count is
  unchanged. Plan 4.4 allows only the G3 change in `check_rules.py`, so
  this commit is a deviation the owner authorized; its paths lie inside
  the B4 boundary.

## Verification notes

### 2026-11-03 B0-V

- Range: `restructure-plan..72e47fc`; 5 commits. B0-1 made B0.1 to B0.4
  (`1b2f572`, `ebdca39`, `3979a72`, `0b98ccc`). `72e47fc` is the blueprint
  correction that answers E-1, which the owner told B0-V to make. All
  checks ran on `0b98ccc`. The gates and check 1 ran again on `72e47fc`,
  which changes only the blueprint and this record.
- Checks:
  1. Boundary and commit hygiene (blueprint 7.2): pass. Up to `0b98ccc`
     the boundary check prints nothing; all 6 changed paths are inside the
     pattern. Up to `72e47fc` it prints only
     `docs/plans/code-restructuring-blueprint.md`, from the E-1 correction
     the owner instructed. Every commit has a `Step:` or `Session:` line,
     and none has an attribution line.
  2. Plan 8.1 gates: pass. Tree clean, no stash; 223 tests OK (222 plus 1
     lock test); rule check `Total: 0`. Same result at `72e47fc`.
  3. Plan 8.5: pass. 223 tests OK from a foreign temporary directory, with
     no error (F-04 fixed).
  4. Lock independence: pass. Green twice in a row (50.1 s, 50.5 s). One
     byte changed in `prompts/verify-balance.en.txt` (`l` to `L`; a
     different prompt from the B0-1 self-test): red, 31 keys (L1 16, L2 14,
     L3 1), including the digests of the `verify` `request.json` files.
     Restored: green. `# lock probe` appended to `common.py`: green. Both
     files restored with `git checkout --`; tree clean afterwards.
  5. Fixture: pass. 378 keys with 2,204 values: 2,189 64-character hex
     digests and 15 `<exempt: existence only>`. The keys are normalized
     paths only. No corpus text.
  6. Change record: pass. Twelve decision rows, with the CR-D06
     confirmation. The lock section has the targets, discovery, volatile
     keys, exemptions and self-test table. The baseline covers the eleven
     section 0 items, the 7.3 metric and the five 8.7 greps. The progress
     table is complete for B0.1 to B0.4. Spot checks at `0b98ccc` give the
     same figures: 209 tracked files; 20 modules, 3,444 lines; 19
     symlinks; grep line counts 42, 37, 55, 2 and 129; 9 test files in the
     first grep, also at `7282f49`; the same 8 long functions.
  7. Wheel acceptance (plan 8.2): pass. `"passed": true`,
     `"commands": 18`, Python 3.14.8, NumPy 2.4.6.
- Measurements: tests 223 in 118.0 s (wall 118.6 s; 125.6 s at
  `72e47fc`); demo 28.0 s under cProfile (`engine.character_reference` 688
  calls, 20.3 s cumulative); lock green, about 50 s run alone.
- Notes:
  - Standards (blueprint 4.1, 4.2): the B0 test files parse as Python 3.9.
    The lock files pass `encoding='utf-8'` on every text read and write. No
    8.7 grep is due yet, and the module-layer test comes in B2.10.
  - Plan 5.3 item 4 allows only `.writer.lock` as a whole-file exclusion.
    The B0 handoff also exempts the code-only files `*-snapshot.py` and
    `code-manifest.json`, and their existence stays locked. B0-1 followed
    the handoff, and the record lists both exemptions with their reasons.
    The lock needs this: `runner-snapshot.py` is a byte copy of
    `engine.py`, so every B2 move would otherwise turn it red. The
    conflict is in wording only and has no behavior effect, so it is
    recorded here and not escalated (blueprint section 0). Aligning plan
    5.3 item 4 with the handoff is a plan correction for the owner.
  - L4 reads three files. The only other tracked path under
    `data/evaluation/` with `text_original` is the symlink
    `evidence-quality-synthetic-v1/cases.json`. It holds the same 38 texts
    in the same order as `records.jsonl`, so L4 covers plan 5.2 in full.
- Result: accepted, tag `restructure-b0`.

### 2026-11-03 B1-V

- Range: `restructure-b0..9cab5e0`; 9 commits. `0d8e6b1` is the plan
  correction the owner told B0-V to make (`Session: B0-V`); B1-1 made B1.1
  to B1.7 (`131e7d2`, `0bddb94`, `abe48a0`, `58e90b3`, `99d57a9`,
  `12cd026`, `aca3fb5`) and the session-log entry `9cab5e0`. All checks
  ran on `9cab5e0`.
- Checks:
  1. Boundary and commit hygiene (blueprint 7.2): pass. The boundary check
     prints one line, `docs/plans/code-restructuring.md`, from `0d8e6b1`.
     That line is expected (first entry under "Decisions found during
     execution"); no B1 commit changes a path outside the pattern. Every
     commit has a `Step:` or `Session:` line, B1.6 and B1.7 name `CR-D03`
     and `CR-D04`, and none has an attribution line.
  2. Diff review: pass. `git diff restructure-b0..HEAD -- src` changes
     `resources.py` (`glossary()` with `lru_cache(maxsize=1)` and a
     one-line docstring), `engine.py` and `review.py`. In `engine.py`,
     `character_reference` and `glossary_target_patch` use `glossary()`,
     the two `glossary_sha256` reads of file bytes are unchanged, and the
     span check raises `AssertionError('Evidence span differs from the
     original text')` with no `assert` left. The `review.py` change only
     moves `encoding='utf-8'` to the first line of one `write_text` call,
     with the same text and receiver (second entry under "Decisions found
     during execution"). An AST comparison of `abe48a0` with its parent,
     ignoring `encoding='utf-8'` keywords, gives identical trees for the
     other 32 files and 145 added keywords. `git diff -w` of `58e90b3`
     shows only the `BlockingIOError` handler with `parser.error`, the
     `try`/`finally: lock.close()` around the rest of each collector's
     `main`, and the new test. The other script changes are the eight
     deletions. The changes match blueprint 3.3 (`resources`, `evidence`)
     and 4.1: the glossary's `target_patch` is a string, so `ground_claim`
     shares no mutable object with the cache, and every changed or added
     Python file parses as Python 3.9.
  3. Gates (plan 8.1): pass. Tree clean, no stash; 217 tests OK, the
     expected count `223 + 1 + 1 + 1 - 9` with the B1.4 test; rule check
     `Total: 0`. The only warnings are the two known `ResourceWarning`s
     from the simulated HTTP errors 429 and 403 in
     `test_collect_feedback.py`.
  4. Lock: pass. `git diff restructure-b0..HEAD -- tests/fixtures/` prints
     nothing, `python3 tests/behavior_lock.py` prints `378 keys, 0 differ`,
     and plan 8.3 passes. B1.5 split the L2 producer into `legacy_dataset`
     and `run_legacy` in the test-only `tests/behavior_lock.py`; the lock
     inputs are unchanged. `test_console_output.py` imports
     `behavior_lock` as `test_behavior_lock.py` does: it is the lock's
     producer module, not a test module (blueprint 4.2).
  5. Archives: pass. `sha256sum -c SHA256SUMS` reports OK for the 6 files
     in `~/Archives/AIMediator/scripts/20261103-quality-screening/` and the
     2 files in `~/Archives/AIMediator/scripts/20261103-broken-entry-points/`.
     Each entry equals the SHA-256 of the blob at the parent of its
     deleting commit (`99d57a9`, `12cd026`) and the hash under "Archive and
     deletions", which lists all eight paths with location, reason and
     step. The existing `~/Archives/AIMediator/scripts/SHA256SUMS` (12
     entries) still verifies and was last modified before B1 began.
  6. Greps and rules: pass. The B1.7 grep and the plan 8.7 fifth grep
     print nothing. The handoff's whole-call AST check prints exactly the
     four expected calls (`self.opener.open`, `tarfile.open` and the two
     `'wb'` opens), and the only other `open(` lines without an encoding
     are the string fixture at `test_check_rules.py` lines 354 to 356.
     Outside the grep's scope, the archived names appear only in the
     planning documents, the dated notes of the two design documents, the
     frozen records, the archived reorganization plan, and the frozen
     files under `data/raw/` and `reports/` that "Archive and deletions"
     explains. G2 and P3 report 0. The register lists 19 symlinks (19
     tracked) and 6 forwarding scripts, and has no R3 row.
  7. Timing (plan 8.4): pass. Demo 3.0 s under cProfile and 1.68 s plain
     (limit 10 s; 26.2 s at entry); `engine.character_reference` 688
     calls, 0.76 s cumulative (limit 1 s). Suite time under Measurements.
  8. Wheel and foreign directory: pass. Plan 8.2, with the build directory
     outside the checkout, prints `"passed": true` and `"commands": 18`
     (Python 3.14.8, NumPy 2.4.6). Plan 8.5: 217 tests OK from a foreign
     temporary directory, which stays empty.
- Measurements: tests 217 in 9.1 s (wall 9.6 s; 118 s at entry); demo
  3.0 s under cProfile, 1.68 s plain; lock green, 4.3 s run alone.
- Owner review items (work order section 5):
  1. Archived files and their two locations: the four quality-screening
     scripts and their two test files in
     `~/Archives/AIMediator/scripts/20261103-quality-screening/` (B1.6,
     CR-D03), and `scripts/run_local_direction_comparison.py` and
     `scripts/experiments/demo_evidence_quality.py` in
     `~/Archives/AIMediator/scripts/20261103-broken-entry-points/` (B1.7,
     CR-D04). Paths, hashes and reasons are under "Archive and deletions".
  2. Timings: demo 1.68 s plain and 3.0 s under cProfile (26.2 s at
     entry); suite 217 tests in 9.1 s (118 s at entry).
  3. The two decisions found during execution in B1: the encoding grep
     line in `review.py` (B1.3) and the register mentions outside the B1.7
     rows (B1.7). Both are implemented under plan section 1, item 8; a
     revert undoes either, and the owner may reject either. There were no
     escalations in B1.
- Result: accepted, tag `restructure-b1-review`. The owner's review and
  the `restructure-b1` tag follow in a closure session (blueprint 6.4).

### 2026-11-03 B1 owner review

- Recorded by the closure session B1-2 at `aab2fb3`
  (`restructure-b1-review`).
- Outcome: the owner accepted all three review items of the B1-V note:
  1. Archived files and their two locations: accepted.
  2. Timings: accepted.
  3. The two decisions found during execution (the encoding grep line in
     `review.py`, B1.3; the register mentions outside the B1.7 rows, B1.7):
     both accepted as implemented.
- Rejected items: none, so there are no fix-up steps.
- Gates at `aab2fb3`, run again by B1-2: tree clean, no stash; 217 tests
  OK; rule check `Total: 0`; lock `378 keys, 0 differ`.
- Result: batch B1 closed, tag `restructure-b1` on this commit. B2 starts
  from it.

### 2026-11-03 B2-V

- Range: `restructure-b1..e52f3ac`; 12 commits. B2-1 made B2.1 to B2.4
  (`cfae9ae`, `4a28223`, `f4bf0f5`, `eb18a64`) and the session-log entry
  `18a3771`; B2-2 made B2.5 to B2.10 (`a2a96c4`, `af5c247`, `9ffb4fe`,
  `5c7a359`, `7f0213e`, `2fa9304`) and the session-log entry `e52f3ac`.
  All checks ran on `e52f3ac`. Old trees were extracted with `git archive`
  outside the checkout.
- Checks:
  1. Boundary and commit hygiene (blueprint 7.2): pass. The boundary check
     from `restructure-b1` prints nothing. The 18 changed paths are
     `engine.py`, `inference.py`, `demo.py`, `operations.py` (one import
     line inside `analyze`) and the seven new modules; the four test files
     of B2.2 and the new `test_module_layers.py`;
     `replay_balance_admission.py`, changed in B2.2 only; and this record.
     The hygiene check prints nothing: every commit has a `Step:` or
     `Session:` line, and none has an attribution line. No commit has a
     `Decision:` line, because none is in force for B2.
  2. Move check for the whole batch (plan 8.6): pass. From
     `restructure-b1`, `engine.py` gives `same` for 23 definitions and
     `CHANGED run`, and `demo.py` gives `same demo` and
     `CHANGED FixtureTransport`. `run` is the B2.1 signature change, which
     plan B2.1 and blueprint 3.3 prescribe. The B2.1 commit body names
     `engine.run` and describes the change, which meets this item: B2.1 is
     not a move. From `cfae9ae`, all 24 definitions are `same`, so no later
     step changed `run`. The B2.9 commit body lists the three
     `FixtureTransport` replacements as intentional, and B2.4 lists those
     of `Transport` and `probe` in `inference.py`. With the replacements
     applied to the old source, each AST is identical. On the extracted
     tree of each commit, the move check from its parent reports
     `CHANGED` only for the names that commit lists. Further checks:
     23 of the 27 moved definitions are byte-identical in source text, and
     the other four differ only by the listed replacements and B2.1. All
     21 comments of the old `engine.py` and `demo.py` survive. Each global
     name a moved definition uses resolves to the same object as at
     `restructure-b1`, with two prescribed exceptions: `Runner` calls
     `evidence_quality.schema_errors` (work order B2.6; the `engine`
     wrapper delegates to it with the same arguments and default), and
     `main` reads the extended docstring (B2.8). The import-source check
     prints `True True True`: `pipeline.load_policy` is the review policy,
     and `stages.obj` and `evidence.obj` are `schema.obj`. Every name of
     the old `engine` namespace is still in `engine`, and the 29 moved
     names are the same objects as in their new modules.
  3. Lock: pass. `git diff restructure-b0..HEAD -- tests/fixtures/` prints
     nothing, `python3 tests/behavior_lock.py` prints `378 keys, 0 differ`,
     and plan 8.3 passes. The lock also prints `378 keys, 0 differ` on the
     extracted tree of each of the 12 commits.
  4. B2.2 grep and layering test: pass. The grep prints nothing, and no
     remaining `patch` in `tests/` or `scripts/` reaches a module global
     of a moved function. `tests/test_module_layers.py` passes its 5 tests
     with no violation and no cycle. Its table equals plan 4.2 row by row
     (27 rows), and its transitional allowance matches the plan's. The
     test is live: on the tree of `5c7a359` it reports exactly
     `demo -> inference (line 9)`, `operations -> demo (line 70)` and the
     cycle `demo -> operations -> demo`. On scratch copies of HEAD it
     fails for `from . import engine` in `stages.py`, for a
     function-level `from .pipeline import` in `retrieval.py` (a cycle),
     for `import aimediator.engine` in `schema.py` and for an unlisted
     module.
  5. Gates, foreign directory and wheel: pass. Tree clean, no stash; 222
     tests OK (217 plus the 5 layering tests; blueprint 1.3 expects 1 or
     more; P4 floor 192); rule check `Total: 0`. The only warnings are the
     two known `ResourceWarning`s from `test_collect_feedback.py`. Plan
     8.5: 222 tests OK from a foreign temporary directory, which stays
     empty. Plan 8.2, with the build directory outside the checkout:
     `"passed": true`, `"commands": 18` (Python 3.14.8, NumPy 2.4.6). The
     wheel's 27 `aimediator/*.py` files equal the checkout files, with
     none missing and none extra.
  6. `engine.py`: pass. 153 lines (931 at `restructure-b1`). Apart from
     import lines it holds the module docstring, `ROOT = Path.cwd()`, the
     `schema_errors` wrapper, `run`, `main` and the `__main__` guard.
     Plan B2.8 requires the docstring, and the guard was already there: it
     makes `python3 -m aimediator.engine` run. All 16 import statements of
     `restructure-b1` remain, and the facade lines are added. The `--help`
     text differs from `restructure-b1` only by the B2.8 sentence in the
     description; the options are unchanged.
- Measurements: tests 222 in 9.1 s (wall 9.5 s); demo 3.0 s under
  cProfile, 1.67 s plain; lock green, 4.4 s run alone.
- Notes:
  - Batch checks of blueprint 7.1 beyond the checklist. The profile names
    `evidence.py:34(character_reference)`: 688 calls, 0.74 s cumulative.
    Plan 8.7: the fifth grep, the only one due, prints nothing; the second
    grep (due after B3.1) prints 29 lines in 5 modules. The progress table
    has rows B2.1 to B2.10, all `done` with lock `green`. The signatures of
    the nine B2 modules match blueprint 3.3, apart from the parts it
    schedules for B5.2, B5.3, B5.5, B5.7 and B5.10. Blueprint 4.1: all 73
    tracked `.py` files under `src/`, `tests/` and `scripts/` parse as
    Python 3.9; `pyproject.toml` is unchanged; the new modules use
    relative imports with no star import, keep the aliases `digest`,
    `write_json`, `strict_json` and `quality`, and each has a module
    docstring.
  - Decision found during execution: `__init__.py` and the module table
    (B2.10), option (a). The conditions of plan section 1, item 8 hold: a
    revert of `2fa9304` undoes it (one new test file and record text), the
    lock stays green, `RULES.md` is unchanged and nothing is deleted. It
    is implemented, not bypassed. B2 has no owner review point. The owner
    may still reject it; option (b) would then be a plan correction and a
    one-row change of the test.
  - For B5: the 7.3 metric lists 9 functions, the 8 of the B0.4 baseline
    under their new modules (`pipeline.process` 259, `runner._generate`
    112, `engine.run` 82, which was 78 before B2.1) plus
    `evidence.ground_claim` at 61 lines. `ground_claim` grew from 60 to 61
    lines in B1.2 (`0bddb94`), and B2.3 moved it unchanged. Blueprint 7.3
    allows no function over 60 lines in `evidence` after B5, and section
    1.2 does not list `ground_claim`. This is not a B2 finding.
  - Still open for the owner, and not caused by B2:
    `replay_balance_admission.py` builds its `Runner` without
    `quality_identity` (B2-1 session-log entry). Its `no_inference`
    transport takes the same three positional arguments that `Runner`
    passes to `streamed_chat`, so it raises the same `RuntimeError` as
    the patch it replaced.
- Result: accepted, tag `restructure-b2`.

### 2026-11-03 B3-V

- Range: `restructure-b2..b4b84b2`; 12 commits. B3-1 made B3.1 to B3.3
  (`4a3e113`, `267e62b`, and the series `d78a645`, `fc06dc3`, `11f1464`)
  and the session-log entry `3b9fbbc`; B3-2 made B3.4 to B3.6 (the series
  `2251a75`, `5c7ba45`, `d544ddd`, then `c386d4f`, `53edafb`) and the
  session-log entry `b4b84b2`. All checks ran on `b4b84b2`. The tree of
  `restructure-b2` was extracted with `git archive` outside the checkout.
- Checks:
  1. Boundary, commit hygiene and CR-D06: pass. The boundary check from
     `restructure-b2` prints nothing. The 33 changed paths are six package
     modules (`engine`, `evaluation`, `legacy_review`, `operations`,
     `reporting`, `review`), `tests/support.py` and 11 test modules, the
     13 experiment scripts, `scripts/collect/screen_feedback.py` and this
     record; nothing under `src/aimediator/assets/`, `data/` or
     `reports/`. The hygiene check prints nothing: every commit has a
     `Step:` or `Session:` line, and none has an attribution line. Each
     commit changes only the files of its step, plus this record in the
     last commit of a step. The three B3.4 commits (`2251a75`, `5c7ba45`,
     `d544ddd`) each carry `Step: B3.4` and `Decision: CR-D06`; no other
     commit has a `Decision:` line.
  2. Greps and layering test: pass. Plan 8.7, first grep (forwarder
     imports under `tests` and `scripts`) and second grep (`engine`
     imports in the package outside `engine.py`), print nothing.
     `tests/test_module_layers.py` no longer has `FACADE` or
     `FACADE_USERS`, and `allowed` accepts only the table and
     `__version__`. Its 5 tests pass with no violation and no cycle, and
     its table still equals plan 4.2 row by row (27 rows). The test is
     live: a scratch copy of HEAD with `from . import engine` added to
     `review.py` fails with `review -> engine (line 5)`. `engine.py` (130
     lines) holds the docstring, its imports, `ROOT`, `run`, `main` and
     the `__main__` guard. Every global name that `run` and `main` load
     resolves (checked with `symtable`), no import is unused, every import
     lies in its plan 4.2 row, and `run` and `main` have the same AST as at
     `restructure-b2`. `python3 -m aimediator.engine --help` equals
     `restructure-b1`.
  3. Lock and test count: pass. `tests/fixtures/behavior-lock.json` is the
     same blob at `restructure-b0` and at HEAD (`df5a724`), and no B3
     commit touches the fixture, `tests/behavior_lock.py` or
     `tests/test_behavior_lock.py`. `python3 tests/behavior_lock.py`
     prints `378 keys, 0 differ`, and plan 8.3 passes. The suite runs 222
     tests, and the 222 test IDs collected at `restructure-b2` and at HEAD
     are identical, so the count per module is unchanged.
  4. Experiment scripts and identity table: pass. All 13 scripts under
     `scripts/experiments/`, and the 4 collectors, print `--help` with
     exit 0 from a foreign temporary directory, which stays empty. For the
     13 scripts and `screen_feedback.py`, the help text is byte-identical
     to `restructure-b2`. The table "Experiment identities (B3.4)" is in
     this record and matches the code: the removed and added keys of each
     script equal its diff; each of the six `ASSETS` tuples lists the
     assets the table names, and each file exists under `asset_path`; the
     27 entries of `code_manifest()['modules']` resolve through
     `module_path` to files with the same digests, so the `code-snapshot/`
     copies match `package_code_sha256`; the seven scripts listed with no
     identity change hash no forwarder or symlink path. In the
     `restructure-b2` tree, every name a changed script imports from
     `aimediator` is the object its forwarder exposed. The exceptions are
     the new names (`asset_path`, `code_manifest`) and the prescribed
     `retrieval_review_agrees`, the function that
     `pipeline.relevance_agrees` wraps. The new `--prompt-dir` default
     names the asset files that the `prompts/` symlinks point to.
  5. Gates, foreign directory and wheel: pass. Tree clean, no stash; 222
     tests OK; rule check `Total: 0`. The only warnings are the two known
     `ResourceWarning`s from `test_collect_feedback.py`. Plan 8.5: 222
     tests OK from a foreign temporary directory, which stays empty. Plan
     8.2, with the build directory outside the checkout: `"passed": true`,
     `"commands": 18` (Python 3.14.8, NumPy 2.4.6). The wheel's 27
     `aimediator/*.py` files equal the checkout files, with none missing
     and none extra, and the wheel holds no `data/raw` and no `.env`.
- Measurements: tests 222 in 8.7 s (wall 9.2 s); demo 3.0 s under
  cProfile, 1.56 s plain; `evidence.character_reference` 688 calls, 0.74 s
  cumulative; lock green, 4.4 s run alone.
- Notes:
  - Batch checks of blueprint 7.1 beyond the checklist. Plan 8.7, fifth
    grep, prints nothing; the third and fourth are not due. The progress
    table has rows B3.1 to B3.6, all `done` with lock `green`. All 74
    tracked `.py` files under `src/`, `tests/` and `scripts/` parse as
    Python 3.9, none has a star import, and no experiment or collector
    docstring begins with "Compatibility entry point". The package diff
    changes only import lines and module-qualified names. The test diffs
    substitute names and move `CASES`, `case` and `qualified` into
    `tests/support.py`; no assertion changes. No test imports another
    test module. A scripts directory stays on `sys.path` only in the five
    tests that import a script, and in `test_refactored_boundaries` for
    its forwarder-identity test until B4.2. The pilot gets only the
    bootstrap and the asset path (CR-D02), and `screen_feedback.py` only
    the bootstrap and the glossary path.
  - `ROOT`: four scripts now define it from their own path, as work order
    B3.4 prescribes, instead of taking `Path.cwd()` from the facade. From
    the checkout root, their defaults name the same files.
  - Decision found during execution: the scope of `asset_sha256` (B3.4),
    option (a). The conditions of plan section 1, item 8 hold: a revert
    of the three B3.4 commits undoes it, the lock stays green, `RULES.md`
    is unchanged and nothing is deleted. It is implemented, not bypassed,
    and open to the owner. Plan section 1, item 8 asks for registration
    before acting; it was registered after the B3.4 commits, with the
    B3-2 session-log entry. The registration is complete now, so this
    needs no fix-up step.
  - For the owner, within CR-D06: `run_quality_screening_experiment`
    sends its identity to the model as `quality_contract`, so the user
    content of its quality requests changes by exactly the identity
    fields. `diagnose_evidence_quality_live` and
    `run_quality_screening_experiment` pass their identity to `Runner` as
    `quality_identity`, so their request IDs change, which CR-D06
    intends. Nothing beyond the CR-D06 identity fields changes, so the
    escalation trigger of work order section 6 does not apply.
  - Still open for the owner, and not caused by B3:
    `replay_balance_admission.py` builds its `Runner` without
    `quality_identity` (B2-1 session-log entry). For B4: plan 8.7, third
    grep, also matches asset-relative names (B3-2 session-log entry).
- Result: accepted, tag `restructure-b3`.

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

### 2026-11-03 B0-V (verification)

- Steps: none (verification). The owner's E-1 correction is in `72e47fc`,
  made at the owner's instruction.
- State: HEAD is the verification-note commit (parent `72e47fc`), tagged
  `restructure-b0`; tests 223; lock green; rule check 0.
- Findings: E-1 answered and applied. One wording conflict between plan
  5.3 item 4 and the B0 handoff on the lock exemptions; no behavior effect
  (see the B0-V note). No fix-up steps.
- Next: B1.1, session B1-1; blockers: none.

### 2026-11-03 B1-1 (implementation)

- Steps: B1.1 to B1.7 (`131e7d2`, `0bddb94`, `abe48a0`, `58e90b3`,
  `99d57a9`, `12cd026`, `aca3fb5`); none started and stashed.
- State: HEAD is this entry's commit (parent `aca3fb5`); tests 217; lock
  green, fixture unchanged; rule check 0. Measured at `aca3fb5`: suite
  8.4 s (wall 8.8 s; 118 s at entry), lock 4.1 s alone; demo 2.9 s under
  cProfile and 1.6 s plain (26.2 s at entry); `engine.character_reference`
  688 calls, 0.72 s cumulative. Plan 8.5: 217 pass from a foreign
  directory. Plan 8.2: `"passed": true`, `"commands": 18`.
- Findings: two decisions found during execution, both implemented under
  plan section 1, item 8 and open to the owner at the B1 review: the
  `review.py` line of the encoding grep (B1.3) and the register mentions
  outside the B1.7 rows. The B1.4 test was added, so the count is
  `223 + 1 + 1 + 1 - 9 = 217`. Archives: `~/Archives/AIMediator/scripts/20261103-quality-screening/`
  (6 files) and `.../20261103-broken-entry-points/` (2 files), each with a
  checked `SHA256SUMS`. Frozen mentions of the archived files remain in
  `data/raw/` and `reports/` (see "Archive and deletions"). The boundary
  check from `restructure-b0` prints only
  `docs/plans/code-restructuring.md`, from the owner-instructed B0-V
  commit `0d8e6b1`; no B1 path. No escalations.
- Next: B1-V (verification of B1, sets `restructure-b1-review`); blockers:
  none.

### 2026-11-03 B1-V (verification)

- Steps: none (verification).
- State: HEAD is the verification-note commit (parent `9cab5e0`), tagged
  `restructure-b1-review`; tests 217; lock green, fixture unchanged; rule
  check 0.
- Findings: none. All eight checklist items pass; no fix-up steps and no
  escalations. The owner review items are listed in the B1-V note.
- Next: the owner's B1 review, then a closure session that records it and
  sets `restructure-b1` (blueprint 6.4); B2.1, session B2-1, starts from
  that tag. Blockers: the owner's review.

### 2026-11-03 B1-2 (closure)

- Steps: none (closure); none started and stashed.
- State: HEAD is this entry's commit (parent `aab2fb3`), tagged
  `restructure-b1`; tests 217; lock green, fixture unchanged; rule check 0.
- Findings: the owner accepted every B1 review item, including both
  decisions found during execution (see "2026-11-03 B1 owner review"). No
  fix-up steps, no escalations.
- Next: B2.1, session B2-1
  ([B2 work order](../plans/code-restructuring-handoffs/b2-engine-split.md)),
  from `restructure-b1`; blockers: none.

### 2026-11-03 B2-1 (implementation)

- Steps: B2.1 to B2.4 (`cfae9ae`, `4a28223`, `f4bf0f5`, `eb18a64`); none
  started and stashed.
- State: HEAD is this entry's commit (parent `eb18a64`); tests 217; lock
  green, fixture unchanged; rule check 0. Suite 9.1 s. Plan 8.5: 217 pass
  from a foreign directory, which stays empty. The boundary check from
  `restructure-b1` and the commit hygiene check print nothing. All 67
  tracked and new `.py` files under `src/`, `tests/` and `scripts/` parse
  as Python 3.9. `engine.py` has 759 lines (931 at entry).
- Findings: no decisions found during execution and no escalations. The
  cumulative move check from `restructure-b1` prints `same` for 23
  definitions and `CHANGED run`. That is the B2.1 signature change, which
  is not a move and is described in its commit body, so B2-V checklist
  item 2 can read `run` as intentionally changed. Pre-existing and not
  acted on: `replay_balance_admission.py` builds its `Runner` without
  `quality_identity`, but `engine.run` always passes one. The script's
  request identities therefore never match a run made by the current
  runner, and it stops with `RuntimeError('Replay cannot run inference')`.
  It did so in the same way before and after B2.2, on a relevance-only
  fixture run. A fix would change the script's logic, which B2 does not
  allow; where to place it is the owner's call (B3.4 revisits the
  script's identity).
- Next: B2.5, session B2-2; blockers: none.

### 2026-11-03 B2-2 (implementation)

- Steps: B2.5 to B2.10 (`a2a96c4`, `af5c247`, `9ffb4fe`, `5c7a359`,
  `7f0213e`, `2fa9304`); none started and stashed.
- State: HEAD is this entry's commit (parent `2fa9304`); tests 222 (217
  plus the 5 layering tests); lock green, fixture unchanged; rule check 0.
  Suite 9.1 s. `engine.py` has 153 lines (759 at entry) and holds only its
  docstring, import lines, `ROOT`, the `schema_errors` wrapper, `run`,
  `main` and the `__main__` guard. B2-V checklist items 1 to 6, run at
  `2fa9304`: the boundary check from `restructure-b1` and the commit
  hygiene check print nothing; the move check from `restructure-b1` prints
  `same` for 23 definitions of `engine.py` and `CHANGED run` (B2.1), and
  for `demo.py` `same demo` and `CHANGED FixtureTransport` (listed in the
  B2.9 commit); `git diff restructure-b0..HEAD -- tests/fixtures/` prints
  nothing and the lock reports `378 keys, 0 differ`; the B2.2 grep prints
  nothing and the layering test passes with no cycle; plan 8.5: 222 pass
  from a foreign directory, which stays empty; plan 8.2: `"passed": true`,
  `"commands": 18`, and every `.py` file in the wheel equals the checkout,
  the five new modules included. All 73 tracked `.py` files under `src/`,
  `tests/` and `scripts/` parse as Python 3.9. Plan 8.7 grep 2 (due after
  B3.1): 29 lines in 5 modules.
- Findings: one decision found during execution, implemented under plan
  section 1, item 8 and open to the owner: `__init__.py` and the module
  table (B2.10). No escalations. Noted in the step rows: `Counter` was
  missing from the work order's B2.5 list; the B2.8 docstring paragraph
  also appears in the `--help` description of `python3 -m
  aimediator.engine`; after B2.9 the fixture's `api` calls `anchors()` once
  per text until B5.10 caches it; the layering test also reads the
  absolute `from aimediator` form, and fails on any subpackage, so B6.2
  must extend it for `collection.*`. Still open for the owner and not
  touched: the `replay_balance_admission.py` identity item from the B2-1
  entry.
- Next: B2-V (verification of B2, sets `restructure-b2`); blockers: none.

### 2026-11-03 B2-V (verification)

- Steps: none (verification); none started and stashed.
- State: HEAD is the verification-note commit (parent `e52f3ac`), tagged
  `restructure-b2`; tests 222; lock green, fixture unchanged; rule check 0.
- Findings: none. All six checklist items pass; no fix-up steps and no
  escalations. The B2.10 decision (`__init__.py` and the module table) is
  implemented and open to the owner. `evidence.ground_claim` (61 lines) is
  noted for B5.
- Next: B3.1, session B3-1
  ([B3 work order](../plans/code-restructuring-handoffs/b3-callers-and-tests.md)),
  from `restructure-b2`; blockers: none.

### 2026-11-03 B3-1 (implementation)

- Steps: B3.1 to B3.3 (`4a3e113`, `267e62b`, and the series `d78a645`,
  `fc06dc3`, `11f1464`); none started and stashed.
- State: HEAD is this entry's commit (parent `11f1464`); tests 222, the
  same count per module as at `restructure-b2`; lock green, fixture
  unchanged; rule check 0. Suite 9.1 s. Plan 8.5: 222 pass from a foreign
  directory, which stays empty. The boundary check from `restructure-b2`
  and the commit hygiene check print nothing. Plan 8.7 grep 2 prints
  nothing; grep 1 prints nothing under `tests` and still lists the
  experiment scripts, which B3.4 changes.
- Findings: no decisions found during execution and no escalations. B3.1
  uses module-qualified names (`evidence.CLAIM`, `runner.Runner`) instead
  of bare imports, because `operations.analyze` has a local `retrieve`
  that calls `engine.retrieve`. `tests/support.py` holds only `CASES`,
  `case` and `qualified`: the claim builders are used by
  `test_evidence_quality.py` alone. Besides the two files the work order
  names, `test_cli_product.py` also used a facade name
  (`engine.evidence_units`) and was changed in the third B3.3 commit.
- Next: B3.4, session B3-2; blockers: none.

### 2026-11-03 B3-2 (implementation)

- Steps: B3.4 (the series `2251a75`, `5c7ba45`, `d544ddd`), B3.5
  (`c386d4f`), B3.6 (`53edafb`); none started and stashed. B3-1 and B3-2
  ran one after the other in the same agent conversation.
- State: HEAD is this entry's commit (parent `53edafb`); tests 222, the
  same count per module as at `restructure-b2`; lock green, fixture
  unchanged since `restructure-b0`; rule check 0. Suite 8.9 s. Plan 8.7
  greps 1 and 2 print nothing, and the layering test passes without the
  allowance. All 13 experiment scripts and the 4 collectors print
  `--help` with exit 0 from a foreign directory. Plan 8.5: 222 pass from
  a foreign directory, which stays empty. Plan 8.2: `"passed": true`,
  `"commands": 18`. The boundary check from `restructure-b2` and the
  commit hygiene check print nothing, and each B3.4 commit names CR-D06.
  All 74 tracked `.py` files under `src/`, `tests/` and `scripts/` parse
  as Python 3.9. `engine.py` has 130 lines.
- Findings:
  - One decision found during execution, implemented and open to the
    owner: the scope of `asset_sha256` (B3.4). It was registered after
    the B3.4 commits, not before them.
  - Within CR-D06, for the owner's attention:
    `run_quality_screening_experiment` sends its identity to the model as
    `quality_contract`, so each quality request's user content changes
    by exactly the identity fields (about 2.3 KB more; see "Experiment
    identities (B3.4)"). This is not the escalation trigger, because
    nothing beyond the identity fields changes. No other script puts its
    identity into a request.
  - `ROOT`: four scripts took it from the `engine` facade
    (`Path.cwd()`) and now define it from their own path, as the work
    order prescribes. Their data defaults name the same files when run
    from the checkout root (B3.4 row).
  - For B4: plan 8.7, third grep, cannot tell asset-relative names
    (`asset_path('configs/...')`, the B3.4 `ASSETS` tuples) from root
    symlink paths. It already matched the package's own `asset_path`
    calls at `restructure-b2` (`engine.py`, `balance_policy.py`,
    `config.py` and others). The B4 condition "matches only the planning
    documents" after B4.3 needs a narrower pattern or an agreed reading.
    The grep is not due in B3.
  - Still open for the owner and not touched:
    `replay_balance_admission.py` builds its `Runner` without
    `quality_identity` (B2-1 entry). B3.4 replaced only the forwarder
    hashes in its output, because passing an identity to `Runner` would
    change the script's logic.
  - No escalations.
- Next: B3-V (verification of B3, sets `restructure-b3`); blockers: none.

### 2026-11-03 B3-V (verification)

- Steps: none (verification); none started and stashed.
- State: HEAD is the verification-note commit (parent `b4b84b2`), tagged
  `restructure-b3`; tests 222; lock green, fixture unchanged since
  `restructure-b0`; rule check 0.
- Findings: none. All five checklist items pass; no fix-up steps and no
  escalations. The B3.4 decision (scope of `asset_sha256`) is implemented
  and open to the owner; it was registered after its commits. The
  `quality_contract` effect of CR-D06 on the screening experiment's
  requests is noted for the owner.
- Next: B4.1, session B4-1
  ([B4 work order](../plans/code-restructuring-handoffs/b4-layer-removal-and-docs.md)),
  from `restructure-b3`; blockers: none.

## Batch results

## Deferred
