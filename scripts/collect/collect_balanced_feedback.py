"""Entry point for the balanced feedback collection (aimediator.collection.balanced)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.collection.balanced import main

if __name__ == '__main__':
    raise SystemExit(main())
