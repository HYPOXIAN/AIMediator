"""Entry point for the coarse feedback screening (aimediator.collection.screening)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.collection.screening import main

if __name__ == '__main__':
    raise SystemExit(main())
