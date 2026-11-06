"""Behavior lock: offline producers, normalizer and fixture writer.

Plan section 5 (docs/archive/code-restructuring.md). Four targets run offline
with fixture transports:

- L1: the CLI demo (``aimediator.demo.demo``);
- L2: the legacy runner (``aimediator.engine.run``) in the three quality modes;
- L3: a review overlay imported from the demo template, and the report
  exported with it;
- L4: the coarse screening rules on every ``text_original`` of the tracked
  evaluation sets.

Each produced file is reduced to the SHA-256 of its normalized bytes, keyed
by its normalized path. Only values that vary between runs of the same code
(times, paths) or with code bytes (module hashes and the identities derived
from them) are replaced; the change record lists them.

``python3 tests/behavior_lock.py --write`` rewrites the fixture. Run it only
in a commit that a plan section 9 decision authorizes (plan section 5.5).
"""
import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tempfile
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
FIXTURE = ROOT / 'tests/fixtures/behavior-lock.json'
MODES = ('off', 'shadow', 'enforce')
SCREENING_SETS = (  # (path, expected number of text_original values)
    ('data/evaluation/balance-regressions-v2/cases.json', 12),
    ('data/evaluation/evidence-quality-real-v2/annotation-template.json', 300),
    ('data/evaluation/evidence-quality-synthetic-v1/records.jsonl', 38),
)

# Volatile values, found empirically (plan 5.3; listed in the change record).
# key: (placeholder for the value, placeholder for its string leaves as text).
# The value is replaced wherever the key occurs in a JSON file. A string leaf
# with a text placeholder is also replaced wherever it occurs as text: JSON
# inside request messages, request directory names, lists of request IDs,
# Markdown, CSV and JSONL files.
VOLATILE_KEYS = {
    # V1: time and path
    'created_at_utc': ('<time>', '<time>'),
    'updated_at_utc': ('<time>', '<time>'),
    'elapsed_seconds': ('<duration>', None),
    'dataset': ('<path>', '<path>'),
    # V2: code hashes and the identities derived from them
    'code': ('<code>', '<code-sha256>'),
    'shared_code_sha256': ('<code>', '<code-sha256>'),
    'runner_sha256': ('<code-sha256>', '<code-sha256>'),
    'script_sha256': ('<code-sha256>', '<code-sha256>'),
    'module_sha256': ('<code-sha256>', '<code-sha256>'),
    'policy_module_sha256': ('<code-sha256>', '<code-sha256>'),
    'run_id': ('<run-id>', '<run-id>'),
    'request_id': ('<request-id>', '<request-id>'),
    # V1 and V2: fingerprints that hash the values above
    'run_sha256': ('<fingerprint>', '<fingerprint>'),
    'decisions_sha256': ('<fingerprint>', '<fingerprint>'),
}
# key: placeholder for every value of the mapping; the names stay locked.
VOLATILE_MAPS = {'artifact_hashes': '<artifact-sha256>'}
HEX_DIGEST = re.compile(r'(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])')
MIN_LITERAL = 16
# Files that hold only code or code hashes: existence is locked, content is not.
CODE_ONLY = re.compile(r'(^|/)([^/]*-snapshot\.py|code-manifest\.json|code-snapshot/[^/]+\.py)$')
# The empty advisory writer lock: existence is locked, content is not (plan 5.3).
EXEMPT = re.compile(r'(^|/)\.writer\.lock$')
EXEMPT_VALUE = '<exempt: existence only>'
JSON_FORMATS = (
    {'ensure_ascii': False, 'indent': 2},
    {'ensure_ascii': False},
    {'ensure_ascii': False, 'sort_keys': True, 'separators': (',', ':')},
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


# Producers ----------------------------------------------------------------

def produce_demo(work):
    """L1: the offline CLI demo into ``work/demo``."""
    from aimediator.demo import demo
    with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
        demo(work / 'demo', quiet=True)
    return work / 'demo'


def produce_reviewed_report(work):
    """L3: import the demo review template as an agent review; export the report with it."""
    from aimediator.reporting import export_report
    from aimediator.review import import_review
    template = work / 'demo/review-template/decisions.json'
    decisions = json.loads(template.read_text(encoding='utf-8'))
    decisions.update(reviewer_type='agent', reviewer_id='behavior-lock')
    template.write_text(json.dumps(decisions, ensure_ascii=False), encoding='utf-8')
    import_review(work / 'demo/enforce', template, work / 'overlay')
    export_report(work / 'demo/enforce', work / 'reviewed-report', work / 'overlay')
    return {'overlay': work / 'overlay', 'reviewed-report': work / 'reviewed-report'}


def fixture_api(transport):
    """``api_transport`` for ``engine.run``: ``/api/tags`` and ``/api/version`` to ``transport.tags`` and
    ``transport.version``, any other endpoint to ``transport.api``."""
    def api(base, endpoint, payload=None):
        if endpoint == '/api/tags':
            return transport.tags()
        if endpoint == '/api/version':
            return transport.version()
        return transport.api(base, endpoint, payload)
    return api


def legacy_dataset(root):
    """Write the packaged fixture sources to ``root`` as the demo writes ``synthetic-input.jsonl``."""
    from aimediator.common import canonical, read
    from aimediator.resources import asset_path
    dataset = root / 'synthetic-input.jsonl'
    cases = read(asset_path('fixtures/cases.json'))
    dataset.write_bytes(b''.join(canonical(c['source']) + b'\n' for c in cases))
    return dataset


def run_legacy(root, dataset, mode):
    """Run ``engine.run`` in one quality mode into ``root/mode`` with the printer of ``engine.main``; return what it printed."""
    from aimediator import engine
    from aimediator.config import defaults
    from aimediator.demo import FixtureTransport
    transport = FixtureTransport(defaults())
    args = SimpleNamespace(dataset=dataset, out=root / mode, model=None,
                           embedding_model='qwen3-embedding:8b', base_url='http://fixture.invalid',
                           evidence_quality=mode, quality_only=False, relevance_only=False)
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        engine.run(args, api_transport=fixture_api(transport), chat_transport=transport.chat,
                   log=lambda text: print(text, flush=True))
    return stdout.getvalue()


def produce_legacy(work):
    """L2: ``engine.run`` in the three quality modes on the packaged fixture sources."""
    root = work / 'legacy'
    root.mkdir()
    dataset = legacy_dataset(root)
    for mode in MODES:
        run_legacy(root, dataset, mode)
    return root


def screening_texts():
    """Every ``text_original`` of the tracked evaluation sets, in file order."""
    def collect(value, found):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == 'text_original':
                    found.append(item)
                else:
                    collect(item, found)
        elif isinstance(value, list):
            for item in value:
                collect(item, found)
    texts = []
    for name, expected in SCREENING_SETS:
        text = (ROOT / name).read_text(encoding='utf-8')
        if name.endswith('.jsonl'):
            values = [json.loads(line) for line in text.splitlines() if line.strip()]
        else:
            values = json.loads(text)
        found = []
        collect(values, found)
        if len(found) != expected:
            raise ValueError('%s: %d text_original values, expected %d' % (name, len(found), expected))
        texts.extend(found)
    return texts


def screening_digest():
    """L4: digest of the JSON list of ``classify_rules`` results (rules only, no network)."""
    from aimediator.collection.screening import classify_rules
    results = [classify_rules({'text_original': text}) for text in screening_texts()]
    return sha256(json.dumps(results, ensure_ascii=False).encode('utf-8'))


# Normalizer ---------------------------------------------------------------

class Normalizer:
    """Replaces volatile values by key, and their literals wherever they occur as text."""

    def __init__(self):
        self.digests = {}  # 64-character hex literal -> placeholder
        self.others = {}   # other literal (times, paths) -> placeholder
        self.ordered = []  # self.others, longest first

    def collect(self, root):
        """Register the string leaves of every volatile value in the JSON files under ``root``."""
        def leaves(value, label):
            if isinstance(value, dict):
                for item in value.values():
                    leaves(item, label)
            elif isinstance(value, list):
                for item in value:
                    leaves(item, label)
            elif isinstance(value, str) and len(value) >= MIN_LITERAL:
                target = self.digests if HEX_DIGEST.fullmatch(value) else self.others
                target.setdefault(value, label)

        def walk(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key in VOLATILE_KEYS:
                        if VOLATILE_KEYS[key][1]:
                            leaves(item, VOLATILE_KEYS[key][1])
                    else:
                        walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)
            elif isinstance(value, str) and value[:1] in '{[':
                try:
                    walk(json.loads(value))
                except ValueError:
                    pass

        for path in sorted(Path(root).rglob('*.json')):
            try:
                walk(json.loads(path.read_text(encoding='utf-8')))
            except ValueError:
                continue
        self.ordered = sorted(self.others, key=lambda item: (-len(item), item))

    def text(self, value):
        for literal in self.ordered:
            value = value.replace(literal, self.others[literal])
        return HEX_DIGEST.sub(lambda match: self.digests.get(match.group(0), match.group(0)), value)

    def value(self, value):
        if isinstance(value, dict):
            result = {}
            for key, item in value.items():
                if key in VOLATILE_KEYS:
                    result[key] = VOLATILE_KEYS[key][0]
                elif key in VOLATILE_MAPS and isinstance(item, dict):
                    result[key] = {self.text(name): VOLATILE_MAPS[key] for name in item}
                else:
                    result[self.text(key)] = self.value(item)
            return result
        if isinstance(value, list):
            return [self.value(item) for item in value]
        if isinstance(value, str):
            return self.text(value)
        return value

    def content(self, path):
        raw = path.read_bytes()
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            return raw
        if path.suffix == '.json':
            try:
                value = json.loads(text)
            except ValueError:
                value = None
            else:
                # Re-serialize in the writer's own format, so that formatting
                # stays locked: a format that does not reproduce the bytes
                # falls back to plain text replacement.
                for options in JSON_FORMATS:
                    serialized = json.dumps(value, **options)
                    for end in ('\n', ''):
                        if serialized + end == text:
                            return (json.dumps(self.value(value), **options) + end).encode('utf-8')
        return self.text(text).encode('utf-8')

    def digest_tree(self, label, root, prefix=''):
        """Return {'<label>:<prefix><normalized path>': digest or sorted digests}."""
        root = Path(root)
        self.collect(root)
        grouped, requests = {}, {}
        for path in sorted(p for p in root.rglob('*') if p.is_file()):
            relative = prefix + path.relative_to(root).as_posix()
            key = label + ':' + self.text(relative)
            if CODE_ONLY.search(relative) or EXEMPT.search(relative):
                digest = EXEMPT_VALUE
            else:
                digest = sha256(self.content(path))
            grouped.setdefault(key, []).append(digest)
            parts = relative.split('/')
            if 'requests' in parts and parts[-1] == 'request.json':
                run = '/'.join(parts[:parts.index('requests')])
                requests.setdefault(label + ':' + run + '/requests/**/request.json', []).append(digest)
        result = {key: values[0] if len(values) == 1 else sorted(values) for key, values in grouped.items()}
        result.update((key, sorted(values)) for key, values in requests.items())
        return result


# Lock ---------------------------------------------------------------------

def compute():
    """Produce every target in a temporary directory and return the digest map."""
    with tempfile.TemporaryDirectory(prefix='behavior-lock-') as tmp:
        work = Path(tmp).resolve()
        # L3 is derived from the L1 enforce run and shares its literals; L2 is
        # normalized only by what it produces itself.
        product = Normalizer()
        digests = product.digest_tree('L1', produce_demo(work))
        for name, root in produce_reviewed_report(work).items():
            digests.update(product.digest_tree('L3', root, name + '/'))
        digests.update(Normalizer().digest_tree('L2', produce_legacy(work)))
        digests['L4:classify_rules'] = screening_digest()
    return dict(sorted(digests.items()))


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding='utf-8'))


def differences(expected, actual):
    """Sorted keys whose digests differ, are missing or are new."""
    return sorted(key for key in set(expected) | set(actual) if expected.get(key) != actual.get(key))


def write_fixture(digests):
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(json.dumps(digests, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--write', action='store_true',
                        help='rewrite the fixture (only under plan section 5.5)')
    args = parser.parse_args()
    sys.path.insert(0, str(SRC))
    digests = compute()
    if args.write:
        write_fixture(digests)
        print('wrote %d keys to %s' % (len(digests), FIXTURE.relative_to(ROOT)))
        return 0
    changed = differences(load_fixture(), digests)
    for key in changed:
        print(key)
    print('%d keys, %d differ' % (len(digests), len(changed)))
    return 1 if changed else 0


if __name__ == '__main__':
    sys.exit(main())
