"""Flush newly published experiment JSON and directories without changing file bytes."""
import argparse
import json
import os
from pathlib import Path
import time


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',type=Path,required=True)
    parser.add_argument('--once',action='store_true')
    args=parser.parse_args();folder=args.run.resolve();seen={}
    while True:
        changed=0
        for path in sorted(folder.rglob('*.json')):
            try:
                stat=path.stat();key=(stat.st_ino,stat.st_size,stat.st_mtime_ns)
                if seen.get(path)==key:continue
                with path.open('rb') as stream:
                    json.loads(stream.read());os.fsync(stream.fileno())
                fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
                try:os.fsync(fd)
                finally:os.close(fd)
                seen[path]=key;changed+=1
            except (OSError,ValueError):
                # A concurrent atomic replacement will be revisited next cycle.
                continue
        if changed:print(json.dumps({'published_json_flushed':changed,'total_seen':len(seen)}),flush=True)
        progress=folder/'progress.json';summary=folder/'summary.json'
        complete=False
        if progress.exists() and summary.exists():
            try:complete=json.loads(progress.read_text(encoding='utf-8'))['completed']==json.loads(progress.read_text(encoding='utf-8'))['input']
            except (ValueError,KeyError,OSError):pass
        if args.once or complete:break
        time.sleep(20)


if __name__=='__main__':main()
