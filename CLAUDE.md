# CLAUDE.md

- Type: Reference
- Status: Active
- Updated: 2026-11-04
- Applies to: `RULES.md` v1.4

## Rules

All project conventions are in [RULES.md](RULES.md). It takes precedence over
this file (G1); this file only points to it and lists commands.

The completed 2026-11 reorganization is described in
[docs/archive/reorganization.md](docs/archive/reorganization.md) and recorded in
[docs/records/20261103-reorganization.md](docs/records/20261103-reorganization.md).

The current engineering project is the pipeline upgrade:
[docs/plans/pipeline-upgrade.md](docs/plans/pipeline-upgrade.md), with one
work order per batch in `docs/plans/pipeline-upgrade-handoffs/`.

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
