import argparse
import collections
import datetime as dt
import email.utils
import hashlib
import fcntl
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.common import write as write_json
from aimediator.resources import workspace_root
from aimediator.collection.client import HOSTS, Client, Halt, RestrictedRedirect, load_youtube_key, retry_delay, utc_now
from aimediator.collection.store import Store
from aimediator.collection.export import export
from aimediator.collection.sources import ROOT, STATE, bluesky, guess_language, main, steam, timestamp, youtube


if __name__ == "__main__":
    sys.exit(main())
