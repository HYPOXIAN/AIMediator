"""Entry point for the feedback expansion (aimediator.collection.expansion)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.collection.expansion import main

if __name__ == '__main__':
    raise SystemExit(main())
