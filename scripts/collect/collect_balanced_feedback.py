"""Collect fresh feedback using existing sources, then freeze a balanced coarse set."""
import argparse
from collections import Counter
from copy import deepcopy
import fcntl
import hashlib
import json
from pathlib import Path

import collect_feedback as c
import screen_feedback as s
from aimediator.collection.balanced import main, retained, reviewed_rows, select_balanced


if __name__ == '__main__':
    raise SystemExit(main())
