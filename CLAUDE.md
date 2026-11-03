# CLAUDE.md

- Type: Reference
- Status: Active
- Updated: 2026-11-03
- Applies to: `RULES.md` v1.0

## Rules

All project conventions are in [RULES.md](RULES.md). It takes precedence over
this file (G1); this file only points to it and lists commands.

The reorganization in progress follows [docs/plans/reorganization.md](docs/plans/reorganization.md).

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

# Enable the report-only pre-commit hook
git config core.hooksPath scripts/maintenance/hooks
```

## Attribution

Agents do not sign their work (RULES.md P6).
