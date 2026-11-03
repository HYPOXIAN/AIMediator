"""Make a separate, explicitly unreviewed demo overlay; never accept a claim."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()
data = json.loads(args.source.read_text(encoding="utf-8"))
data["reviewer_type"] = "agent"
data["reviewer_id"] = "cli-demo-template-helper"
for decision in data["decisions"].values():
    decision["decision"] = "uncertain"
    decision["reason"] = "CLI workflow demonstration only; source not independently reviewed."
with args.output.open("x", encoding="utf-8") as stream:
    json.dump(data, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
