import functools
import json,re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.resources import glossary, workspace_root
from aimediator.collection.screening import classify, classify_rules, load_sources, main, write_rows


if __name__=='__main__':
    main()
