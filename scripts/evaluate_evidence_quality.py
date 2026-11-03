"""Compatibility entry point for :mod:`aimediator.quality_scoring`."""
from pathlib import Path
import sys

# Checkout commands always use the adjacent package, even when a wheel is installed.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from aimediator import quality_scoring as implementation

if __name__ == "__main__":
    implementation.main()
else:
    sys.modules[__name__] = implementation
