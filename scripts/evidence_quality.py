"""Compatibility entry point for :mod:`aimediator.evidence_quality`."""
from pathlib import Path
import sys

# Checkout commands always use the adjacent package, even when a wheel is installed.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from aimediator import evidence_quality as implementation

sys.modules[__name__] = implementation
