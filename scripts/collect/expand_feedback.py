import argparse
import collections
import copy
import fcntl
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.resources import workspace_root
import collect_feedback as collector
import screen_feedback as screener
from aimediator.collection.expansion import kept_counts, main


if __name__=='__main__':
    raise SystemExit(main())
