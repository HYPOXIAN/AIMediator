# CLAUDE.md

- Type: Reference
- Status: Active
- Updated: 2026-11-05
- Applies to: `RULES.md` v1.5

## Rules

All project conventions are in [RULES.md](RULES.md). It takes precedence over
this file (G1); this file only points to it and lists commands.

The completed 2026-11 reorganization is described in
[docs/archive/reorganization.md](docs/archive/reorganization.md) and recorded in
[docs/records/20261103-reorganization.md](docs/records/20261103-reorganization.md).
The completed 2026-11 code restructuring is described in
[docs/archive/code-restructuring.md](docs/archive/code-restructuring.md) and
recorded in
[docs/records/20261103-code-restructuring.md](docs/records/20261103-code-restructuring.md).

The completed 2026-11 pipeline upgrade is described in
[docs/archive/pipeline-upgrade.md](docs/archive/pipeline-upgrade.md) and
recorded in
[docs/records/20261104-pipeline-upgrade.md](docs/records/20261104-pipeline-upgrade.md),
with its acceptance measurements in
[docs/records/20261105-pipeline-upgrade-validation.md](docs/records/20261105-pipeline-upgrade-validation.md).
No engineering project is open; new work starts a new plan.

## Common commands

```sh
# Install for development (Python 3.9+)
python3 -m venv .venv
.venv/bin/python -m pip install -e .

# Offline test suite
python3 -m unittest discover -s tests -q

# Rule check (all rules, or selected rule IDs)
python3 scripts/maintenance/check_rules.py
python3 scripts/maintenance/check_rules.py --rule G3 --rule D5

# Enable the blocking pre-commit hook (refuses commits with violations)
git config core.hooksPath scripts/maintenance/hooks
```

## Attribution

Agents do not sign their work (RULES.md P6).
