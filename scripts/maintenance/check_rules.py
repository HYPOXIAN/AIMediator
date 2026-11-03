#!/usr/bin/env python3
"""Read-only rule checker for RULES.md.

Prints one line per violation, prefixed with its rule ID, followed by a
summary of counts per rule. Exits 0 when no violation is found, 1 when at
least one is found and 2 on a usage error.

    python3 scripts/maintenance/check_rules.py
    python3 scripts/maintenance/check_rules.py --rule G3 --rule D5,D8
    python3 scripts/maintenance/check_rules.py --list-rules

Scope and limits:

- Standard library only; never writes, moves or deletes anything.
- "Source files" are tracked files plus untracked files that git does not
  ignore. Outside a git checkout the tree is walked instead, skipping the
  usual generated and data directories.
- Below ``reports/`` only the curated files are read: each
  ``reports/<name>/manifest.json`` and everything under
  ``reports/<name>/summary/``, for the G7 and G9 scans (reorganization plan,
  section 7, decision 20). Other report files are never read; for P2 and G8
  only their names are listed. Documentation checks skip ``reports/``.
- ``.env`` files are never opened. Credential findings report the file, line
  and pattern name only, never the matched text.
- Package listings (G9) read archive member names only.
"""
import argparse
import ast
import collections
import hashlib
import os
import re
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]

Violation = collections.namedtuple('Violation', 'rule path line message')

G3_ALLOWED = frozenset({
    'README.md', 'RULES.md', 'pyproject.toml', 'MANIFEST.in', '.gitignore',
    '.env.example', '.env', 'CLAUDE.md', 'AGENTS.md', 'src', 'tests',
    'scripts', 'configs', 'data', 'docs', 'examples', 'reports', 'runs',
    'build', 'dist', '.venv',
    # RULES.md v1.1: registered compatibility links only (checked by G2).
    'prompts',
    # The repository itself; required by G5.
    '.git',
})
D1_DIRS = frozenset({'guides', 'design', 'decisions', 'plans', 'records',
                     'reference', 'meetings', 'archive'})
P3_SCRIPT_DIRS = frozenset({'collect', 'experiments', 'maintenance'})
REGISTER = 'docs/reference/compatibility-layers.md'
INDEX = 'docs/README.md'
FORBIDDEN_WORDS = frozenset({'final', 'latest', 'new', 'fixed'})
CONVENTIONAL_NAMES = frozenset({'README.md', 'RULES.md', 'CLAUDE.md',
                                'AGENTS.md', 'MANIFEST.in', 'LICENSE',
                                'SHA256SUMS', 'CHANGELOG.md'})
WALK_SKIP = frozenset({'.git', 'build', 'dist', '.venv', 'venv', 'runs',
                       'reports', '__pycache__', '.pytest_cache',
                       '.ruff_cache'})
CODE_SUFFIXES = frozenset({'.py', '.ts', '.tsx', '.js', '.jsx', '.sh',
                           '.ipynb'})
ARCHIVE_SUFFIXES = frozenset({'.zip', '.tar', '.gz', '.tgz', '.7z', '.whl'})
MAX_TEXT_BYTES = 5 * 1024 * 1024
D7_MAX_MD_BYTES = 100 * 1024

KEBAB = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
KEBAB_FILE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*(?:\.[a-z0-9]+)*$')
SNAKE = re.compile(r'^[a-z_][a-z0-9_]*$')
DATE_TOKEN = re.compile(r'^20\d{6}$')
VERSION_TOKEN = re.compile(r'^v\d+$')
DATED_DIR = re.compile(r'^\d{8}-[a-z0-9]+(?:-[a-z0-9]+)*$')
DATE_IN_TEXT = re.compile(r'(?<!\d)20\d{6}(?!\d)')
# A home directory followed by a user name; "/home/..." in prose is not one.
HOME_PATH = re.compile(r'/home/[A-Za-z0-9_][A-Za-z0-9_.-]*')
CJK = re.compile(r'[㐀-䶿一-鿿豈-﫿]')
FENCE = re.compile(r'^\s*(```|~~~)')
INLINE_CODE = re.compile(r'(`+)(?:(?!\1).)+?\1')
MD_LINK = re.compile(r'!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)')
MD_REF_DEF = re.compile(r'^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s+.*)?$')
URL_SCHEME = re.compile(r'^[A-Za-z][A-Za-z0-9+.-]*:')
HEADER_FIELD = re.compile(
    r'^\s*(?:[-*]\s+)?\**\s*(type|status|updated|applies to)\s*\**\s*:'
    r'\s*\**\s*(.*?)\s*$', re.IGNORECASE)
STATUS_VALUE = re.compile(r'^(Draft|Active|Archived|Superseded by .+)$')
ISO_DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
FORWARDER_DOC = re.compile(
    r'^\s*(?:#![^\n]*\n\s*)?(?:#[^\n]*\n\s*)*[rRuU]?("""|\'\'\')\s*'
    r'Compatibility entry point')
STATE_NAME = re.compile(r'(\.lock|\.pid|[-_]state\.json)$')
SECRET_PATTERNS = (
    ('Google API key', re.compile(r'AIza[0-9A-Za-z_\-]{35}')),
    ('sk- style API key', re.compile(r'\bsk-[A-Za-z0-9_\-]{20,}')),
    ('GitHub token', re.compile(r'\bgh[pousr]_[A-Za-z0-9]{36,}')),
    ('AWS access key ID', re.compile(r'\bAKIA[0-9A-Z]{16}\b')),
    ('Slack token', re.compile(r'\bxox[abprs]-[A-Za-z0-9-]{10,}')),
    ('private key block', re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')),
    ('assigned secret', re.compile(
        r'(?i)\b(?:api[_-]?key|secret|token|password|passwd)\b["\']?\s*[:=]'
        r'\s*["\'][A-Za-z0-9_\-+/=]{16,}["\']')),
)


def is_curated_report(rel):
    """True for reports/<name>/manifest.json and files under
    reports/<name>/summary/, the report files the checks may read."""
    parts = PurePosixPath(rel).parts
    if len(parts) < 3 or parts[0] != 'reports':
        return False
    return (parts[2] == 'manifest.json' and len(parts) == 3
            or parts[2] == 'summary' and len(parts) > 3)


def curated_report_files(root):
    """Curated report files found by walking, for trees without git."""
    found = []
    base = Path(root) / 'reports'
    if not base.is_dir() or base.is_symlink():
        return found
    for report in sorted(base.iterdir()):
        if not report.is_dir() or report.is_symlink():
            continue
        if (report / 'manifest.json').is_file():
            found.append('reports/%s/manifest.json' % report.name)
        summary = report / 'summary'
        if summary.is_dir() and not summary.is_symlink():
            for current, dirs, files in os.walk(str(summary)):
                rel = Path(current).relative_to(root).as_posix()
                found.extend(rel + '/' + f for f in files)
    return found


class Project:
    """File access for one project root, with per-run caches."""

    def __init__(self, root):
        self.root = Path(root).resolve()
        self._files = None
        self._text = {}

    def files(self):
        """Sorted repo-relative POSIX paths of the source files."""
        if self._files is None:
            names = self._git_files()
            if names is None:
                names = self._walk_files()
            self._files = sorted(n for n in set(names)
                                 if os.path.lexists(self.root / n))
        return self._files

    def _git_files(self):
        if not (self.root / '.git').exists():
            return None
        try:
            out = subprocess.run(
                ['git', 'ls-files', '-z', '--cached', '--others',
                 '--exclude-standard'],
                cwd=str(self.root), check=True, stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL).stdout
        except (OSError, subprocess.CalledProcessError):
            return None
        return [n for n in out.decode('utf-8', 'surrogateescape').split('\0')
                if n]

    def _walk_files(self):
        found = []
        for current, dirs, files in os.walk(str(self.root)):
            rel = Path(current).relative_to(self.root).as_posix()
            rel = '' if rel == '.' else rel + '/'
            keep = []
            for d in dirs:
                path = rel + d
                if (d in WALK_SKIP or d.endswith('.egg-info')
                        or path in ('data/raw', 'data/processed')):
                    if path == 'reports':
                        found.extend(curated_report_files(self.root))
                    continue
                if os.path.islink(os.path.join(current, d)):
                    found.append(path)
                    continue
                keep.append(d)
            dirs[:] = keep
            found.extend(rel + f for f in files)
        return found

    def under(self, prefix):
        prefix = prefix.rstrip('/') + '/'
        return [f for f in self.files() if f.startswith(prefix)]

    def is_link(self, rel):
        return os.path.islink(str(self.root / rel))

    def text(self, rel):
        """File text, or None for binaries, symlinks, large files, .env
        files and report files other than the curated ones, which are
        never read."""
        if rel in self._text:
            return self._text[rel]
        result = None
        name = PurePosixPath(rel).name
        protected = ((rel.startswith('reports/')
                      and not is_curated_report(rel)) or name == '.env'
                     or (name.startswith('.env.') and name != '.env.example'))
        path = self.root / rel
        if not protected and not path.is_symlink() and path.is_file():
            try:
                if path.stat().st_size <= MAX_TEXT_BYTES:
                    data = path.read_bytes()
                    if b'\0' not in data[:8192]:
                        result = data.decode('utf-8', 'replace')
            except OSError:
                result = None
        self._text[rel] = result
        return result

    def listdir(self, rel):
        path = self.root / rel
        try:
            return sorted(os.listdir(str(path))) if path.is_dir() else []
        except OSError:
            return []


# ---------------------------------------------------------------- helpers

def markdown_lines(text):
    """Yield (line number, line, in_code_block) for a Markdown text."""
    fenced = None
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if fenced is None:
                fenced = marker
                yield number, line, True
                continue
            if marker == fenced:
                fenced = None
                yield number, line, True
                continue
        yield number, line, fenced is not None


def markdown_links(text):
    """Yield (line number, target) for inline links and reference
    definitions outside code."""
    for number, line, in_code in markdown_lines(text):
        if in_code:
            continue
        stripped = INLINE_CODE.sub('', line)
        for match in MD_LINK.finditer(stripped):
            yield number, match.group(1)
        ref = MD_REF_DEF.match(stripped)
        if ref:
            yield number, ref.group(1)


def resolve_link(source, target):
    """Repo-relative path a relative link points to, or None to skip it."""
    if not target or target.startswith('#') or URL_SCHEME.match(target):
        return None
    target = unquote(target.split('#', 1)[0].split('?', 1)[0])
    if not target:
        return None
    base = PurePosixPath(source).parent
    return os.path.normpath(str(base / target)).replace(os.sep, '/')


def registered_layers(project):
    """Paths in the first column of the register's tables, or None if the
    register does not exist."""
    text = project.text(REGISTER)
    if text is None:
        return None
    paths = set()
    for _, line, in_code in markdown_lines(text):
        if in_code or not line.lstrip().startswith('|'):
            continue
        cells = line.strip().strip('|').split('|')
        match = re.match(r'^\s*`([^`]+)`\s*$', cells[0]) if cells else None
        if match:
            paths.add(match.group(1))
    return paths


def compatibility_layers(project):
    """Map of path -> 'symlink' or 'forwarding script'."""
    layers = {}
    for rel in project.files():
        if project.is_link(rel):
            layers[rel] = 'symlink'
        elif rel.endswith('.py'):
            text = project.text(rel)
            if text and FORWARDER_DOC.match(text[:2000]):
                layers[rel] = 'forwarding script'
    return layers


def markdown_files(project):
    return [f for f in project.files() if f.endswith('.md')
            and not f.startswith('reports/') and not project.is_link(f)]


def name_issues(name, is_dir, is_package=False):
    """Naming problems (G8) for one path component."""
    issues = []
    if name.startswith('.') or name == '__pycache__':
        return issues
    if not is_dir and name in CONVENTIONAL_NAMES:
        return issues
    if is_dir:
        stem = name
        pattern, style = ((SNAKE, 'snake_case') if is_package
                          else (KEBAB, 'kebab-case'))
        if not pattern.match(name):
            issues.append('directory name is not ' + style)
    elif name.endswith('.py'):
        stem = name[:-3]
        if not SNAKE.match(stem):
            issues.append('Python module name is not snake_case')
    else:
        stem = name.split('.', 1)[0]
        if not KEBAB_FILE.match(name):
            issues.append('file name is not lowercase kebab-case')
    tokens = [t for t in re.split(r'[-_.]', stem.lower()) if t]
    words = sorted(FORBIDDEN_WORDS.intersection(tokens))
    if words:
        issues.append('forbidden relative word ' + ', '.join(
            repr(w) for w in words))
    if any(DATE_TOKEN.match(t) for t in tokens[1:]):
        issues.append('date is not a YYYYMMDD- prefix')
    if any(VERSION_TOKEN.match(t) for t in tokens[:-1]):
        issues.append('version is not a -vN suffix')
    return issues


def default_strings(node):
    return [n.value for n in ast.walk(node)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def names_dated_run(strings):
    joined = '/'.join(strings)
    if re.search(r'(^|/)reports(/|$)', joined):
        return True
    return bool(DATE_IN_TEXT.search(joined)
                and not re.search(r'(^|/)data(/|$)', joined))


# ---------------------------------------------------------------- checks

def check_g2(project):
    """Symlinks and forwarding scripts are registered; no duplicate files."""
    found = []
    layers = compatibility_layers(project)
    registered = registered_layers(project)
    if registered is None:
        found.append(Violation('G2', REGISTER, None,
                               'compatibility register is missing'))
        registered = set()
    for rel, kind in sorted(layers.items()):
        if rel not in registered:
            found.append(Violation('G2', rel, None,
                                   kind + ' not in the compatibility register'))
    for rel in sorted(registered - set(layers)):
        message = ('registered layer no longer exists'
                   if not os.path.lexists(str(project.root / rel))
                   else 'registered path is not a symlink or forwarding script')
        found.append(Violation('G2', REGISTER, None, message + ': ' + rel))
    by_size = collections.defaultdict(list)
    for rel in project.files():
        path = project.root / rel
        if rel.startswith('reports/') or project.is_link(rel):
            continue
        name = path.name
        if name == '.env' or (name.startswith('.env.')
                              and name != '.env.example'):
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size:
            by_size[size].append(rel)
    groups = collections.defaultdict(list)
    for paths in by_size.values():
        if len(paths) < 2:
            continue
        for rel in paths:
            try:
                digest = hashlib.sha256(
                    (project.root / rel).read_bytes()).hexdigest()
            except OSError:
                continue
            groups[digest].append(rel)
    for paths in groups.values():
        if len(paths) > 1:
            paths.sort()
            found.append(Violation('G2', paths[0], None,
                                   'identical content in ' + ', '.join(paths[1:])))
    return found


def check_g3(project):
    """The root holds only allowlisted entries."""
    return [Violation('G3', name, None, 'top-level entry not in the allowlist')
            for name in project.listdir('.') if name not in G3_ALLOWED]


def check_g7(project):
    """No absolute user paths; no default argument names a dated run."""
    found = []
    for rel in project.files():
        text = project.text(rel)
        if text is None:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if HOME_PATH.search(line):
                found.append(Violation('G7', rel, number,
                                       'absolute user path'))
        if not rel.endswith('.py'):
            continue
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError):
            continue
        for node in ast.walk(tree):
            defaults = []
            if isinstance(node, ast.Call):
                defaults = [k.value for k in node.keywords
                            if k.arg == 'default']
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                   ast.Lambda)):
                defaults = node.args.defaults + [
                    d for d in node.args.kw_defaults if d is not None]
            for value in defaults:
                if names_dated_run(default_strings(value)):
                    found.append(Violation(
                        'G7', rel, getattr(value, 'lineno', None),
                        'default argument names reports/ or a dated run'))
    return found


def check_g8(project):
    """Directory and file names follow the naming rule."""
    entries = {}
    for rel in project.files():
        parts = PurePosixPath(rel).parts
        for depth in range(1, len(parts)):
            entries.setdefault('/'.join(parts[:depth]), True)
        entries[rel] = project.is_link(rel) and (project.root / rel).is_dir()
    # Ignored locations whose names the rules still govern; names only.
    for name in project.listdir('reports'):
        entries.setdefault('reports/' + name,
                           (project.root / 'reports' / name).is_dir())
    for name in project.listdir('data/raw'):
        rel = 'data/raw/' + name
        is_dir = (project.root / rel).is_dir()
        entries.setdefault(rel, is_dir)
        if is_dir:
            for child in project.listdir(rel):
                entries.setdefault(rel + '/' + child,
                                   (project.root / rel / child).is_dir())
    for name in project.listdir('data/processed'):
        entries.setdefault('data/processed/' + name,
                           (project.root / 'data/processed' / name).is_dir())
    found = []
    for rel in sorted(entries):
        is_dir = entries[rel]
        is_package = is_dir and (project.root / rel / '__init__.py').exists()
        issues = name_issues(PurePosixPath(rel).name, is_dir, is_package)
        if issues:
            found.append(Violation('G8', rel + ('/' if is_dir else ''), None,
                                   '; '.join(issues)))
    return found


def check_g9(project):
    """No credentials in the tree, examples or package listings."""
    found = []
    for rel in project.files():
        name = PurePosixPath(rel).name
        if name == '.env' or (name.startswith('.env.')
                              and name != '.env.example'):
            found.append(Violation('G9', rel, None,
                                   'credential file in the source tree'))
            continue
        text = project.text(rel)
        if text is None:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    found.append(Violation('G9', rel, number,
                                           'possible ' + label))
    example = project.root / '.env.example'
    if not example.is_file():
        found.append(Violation('G9', '.env.example', None,
                               '.env.example is missing'))
    else:
        for number, line in enumerate(
                example.read_text(encoding='utf-8', errors='replace')
                .splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#') or '=' not in stripped:
                continue
            key, value = stripped.split('=', 1)
            if value.strip():
                found.append(Violation('G9', '.env.example', number,
                                       'value present for key '
                                       + key.replace('export ', '').strip()))
    manifest = project.text('MANIFEST.in') or ''
    for number, line in enumerate(manifest.splitlines(), 1):
        if 'data/raw' in line or re.search(r'(^|[\s/])\.env\b', line):
            found.append(Violation('G9', 'MANIFEST.in', number,
                                   'MANIFEST.in includes data/raw or .env'))
    for rel, members in package_listings(project):
        kinds = collections.Counter(filter(None, map(package_member_kind,
                                                     members)))
        if kinds:
            found.append(Violation('G9', rel, None, 'package lists %d .env '
                                   'and %d data/raw entries'
                                   % (kinds['.env'], kinds['data/raw'])))
    return found


def package_member_kind(member):
    """'.env', 'data/raw' or None for one archive member name."""
    member = '/' + member.lstrip('./')
    name = member.rsplit('/', 1)[-1]
    if name == '.env' or (name.startswith('.env.') and name != '.env.example'):
        return '.env'
    if '/data/raw/' in member or member.endswith('/data/raw'):
        return 'data/raw'
    return None


def package_listings(project):
    """Yield (repo-relative path, member names) for archives under dist/."""
    dist = project.root / 'dist'
    if not dist.is_dir():
        return
    for current, _, files in os.walk(str(dist)):
        for name in sorted(files):
            path = Path(current) / name
            rel = path.relative_to(project.root).as_posix()
            try:
                if name.endswith(('.whl', '.zip')):
                    with zipfile.ZipFile(str(path)) as archive:
                        yield rel, archive.namelist()
                elif name.endswith(('.tar.gz', '.tgz', '.tar')):
                    with tarfile.open(str(path)) as archive:
                        yield rel, archive.getnames()
            except (OSError, zipfile.BadZipFile, tarfile.TarError):
                yield rel, []


def check_d1(project):
    """docs/ uses only the D1 directories and holds only the index at its root."""
    found = []
    seen = set()
    for rel in project.under('docs'):
        parts = PurePosixPath(rel).parts
        if len(parts) == 2:
            if rel != INDEX:
                found.append(Violation('D1', rel, None,
                                       'loose file at the docs/ root'))
        elif parts[1] not in D1_DIRS and parts[1] not in seen:
            seen.add(parts[1])
            found.append(Violation('D1', 'docs/%s/' % parts[1], None,
                                   'directory not defined by D1'))
    return found


def check_d2(project):
    """Every document under docs/ starts with the D2 header."""
    found = []
    for rel in markdown_files(project):
        if not rel.startswith('docs/'):
            continue
        text = project.text(rel) or ''
        fields = {}
        for line in text.splitlines()[:15]:
            match = HEADER_FIELD.match(line)
            if match:
                fields.setdefault(match.group(1).lower(), match.group(2))
        missing = [k for k in ('type', 'status', 'updated', 'applies to')
                   if not fields.get(k)]
        if missing:
            found.append(Violation('D2', rel, None,
                                   'header lacks ' + ', '.join(missing)))
            continue
        problems = []
        if not STATUS_VALUE.match(fields['status'].strip('`*')):
            problems.append('invalid status %r' % fields['status'])
        if not ISO_DATE.match(fields['updated'].strip('`*')):
            problems.append('Updated is not YYYY-MM-DD')
        if problems:
            found.append(Violation('D2', rel, None, '; '.join(problems)))
    return found


def check_d4(project):
    """docs/README.md lists every document under docs/."""
    documents = [f for f in markdown_files(project)
                 if f.startswith('docs/') and f != INDEX]
    text = project.text(INDEX)
    if text is None:
        found = [Violation('D4', INDEX, None, 'documentation index is missing')]
        listed = set()
    else:
        found = []
        listed = {resolve_link(INDEX, target)
                  for _, target in markdown_links(text)}
    found.extend(Violation('D4', rel, None, 'not listed in ' + INDEX)
                 for rel in documents if rel not in listed)
    return found


def check_d5(project):
    """Relative links and MANIFEST.in entries resolve."""
    found = []
    for rel in markdown_files(project):
        for number, target in markdown_links(project.text(rel) or ''):
            if target.startswith('/'):
                found.append(Violation('D5', rel, number,
                                       'absolute link: ' + target))
                continue
            resolved = resolve_link(rel, target)
            if resolved is None:
                continue
            if resolved == '..' or resolved.startswith('../'):
                found.append(Violation('D5', rel, number,
                                       'link leaves the project: ' + target))
            elif not os.path.lexists(str(project.root / resolved)):
                found.append(Violation('D5', rel, number,
                                       'broken link: ' + target))
    manifest = project.text('MANIFEST.in') or ''
    for number, line in enumerate(manifest.splitlines(), 1):
        words = line.split()
        if len(words) < 2 or words[0].startswith('#'):
            continue
        command, args = words[0], words[1:]
        if command in ('include', 'exclude'):
            paths = args
        elif command in ('recursive-include', 'recursive-exclude', 'graft',
                         'prune'):
            paths = args[:1]
        else:
            continue
        for path in paths:
            if not list(project.root.glob(path)):
                found.append(Violation('D5', 'MANIFEST.in', number,
                                       'path does not exist: ' + path))
    return found


def check_d6(project):
    """Document names: dated records and meetings, numbered decisions,
    undated living documents."""
    found = []
    for rel in markdown_files(project):
        parts = PurePosixPath(rel).parts
        if len(parts) != 3 or parts[0] != 'docs':
            continue
        folder, name = parts[1], parts[2]
        stem = name[:-3]
        if folder in ('records', 'meetings'):
            if not DATED_DIR.match(stem):
                found.append(Violation('D6', rel, None,
                                       'name lacks a YYYYMMDD- prefix'))
        elif folder == 'decisions':
            if not re.match(r'^\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*$', stem):
                found.append(Violation('D6', rel, None,
                                       'decision is not named NNNN-title.md'))
        elif folder in ('guides', 'design', 'plans', 'reference'):
            tokens = stem.split('-')
            if any(DATE_IN_TEXT.search(t) or VERSION_TOKEN.match(t)
                   for t in tokens):
                found.append(Violation('D6', rel, None,
                                       'living document name carries a date '
                                       'or version'))
    return found


def check_d7(project):
    """No JSON under docs/; Markdown files stay under 100 KB."""
    found = []
    for rel in project.under('docs'):
        if rel.endswith(('.json', '.jsonl')):
            found.append(Violation('D7', rel, None, 'data file under docs/'))
        elif rel.endswith('.md') and not project.is_link(rel):
            size = (project.root / rel).stat().st_size
            if size > D7_MAX_MD_BYTES:
                found.append(Violation(
                    'D7', rel, None,
                    'Markdown file of %d KB exceeds 100 KB' % (size // 1024)))
    return found


def check_d8(project):
    """Chinese appears in documents only as corpus content.

    Allowed: glossary-type documents (file name contains "glossary"),
    blockquotes, fenced code blocks and inline code spans.
    """
    found = []
    for rel in markdown_files(project):
        if 'glossary' in PurePosixPath(rel).name:
            continue
        lines = []
        for number, line, in_code in markdown_lines(project.text(rel) or ''):
            if in_code or line.lstrip().startswith('>'):
                continue
            if CJK.search(INLINE_CODE.sub('', line)):
                lines.append(number)
        if lines:
            found.append(Violation(
                'D8', rel, lines[0],
                'Chinese outside corpus content on %d line(s)' % len(lines)))
    return found


def check_p1(project):
    """Datasets are dated and have manifests; no runtime state in data/."""
    found = []
    for collection in project.listdir('data/raw'):
        rel = 'data/raw/' + collection
        if collection.startswith('.') or STATE_NAME.search(collection):
            continue
        if not (project.root / rel).is_dir():
            found.append(Violation('P1', rel, None,
                                   'file outside a dataset directory'))
            continue
        loose = 0
        for name in project.listdir(rel):
            path = rel + '/' + name
            if not (project.root / path).is_dir():
                loose += 1
                continue
            if not DATED_DIR.match(name):
                found.append(Violation('P1', path + '/', None,
                                       'dataset directory is not named '
                                       'YYYYMMDD-slug'))
            if not (project.root / path / 'manifest.json').is_file():
                found.append(Violation('P1', path + '/', None,
                                       'dataset has no manifest.json'))
        if loose:
            found.append(Violation('P1', rel + '/', None,
                                   '%d file(s) outside a dataset directory'
                                   % loose))
    for name in project.listdir('data/evaluation'):
        rel = 'data/evaluation/' + name
        if name.startswith('.'):
            continue
        if not (project.root / rel).is_dir():
            found.append(Violation('P1', rel, None,
                                   'annotation file outside a versioned set'))
            continue
        if not re.search(r'-v\d+$', name):
            found.append(Violation('P1', rel + '/', None,
                                   'annotation set name does not end in -vN'))
        if not (project.root / rel / 'manifest.json').is_file():
            found.append(Violation('P1', rel + '/', None,
                                   'annotation set has no manifest.json'))
    data = project.root / 'data'
    if data.is_dir():
        for current, dirs, files in os.walk(str(data)):
            dirs.sort()
            for name in sorted(files):
                if STATE_NAME.search(name):
                    rel = (Path(current) / name).relative_to(
                        project.root).as_posix()
                    found.append(Violation('P1', rel, None,
                                           'runtime state file under data/'))
    return found


def check_p2(project):
    """reports/ holds manifests and curated results; dist/ only the current
    wheel and sdist. Only names are listed; no file is opened."""
    found = []
    for name in project.listdir('reports'):
        rel = 'reports/' + name
        if name.startswith('.'):
            continue
        if not (project.root / rel).is_dir():
            found.append(Violation('P2', rel, None, 'loose file in reports/'))
            continue
        if not (project.root / rel / 'manifest.json').is_file():
            found.append(Violation('P2', rel + '/', None,
                                   'report has no manifest.json'))
        code = backups = 0
        for current, dirs, files in os.walk(str(project.root / rel)):
            parts = Path(current).relative_to(project.root / rel).parts
            if 'provenance' in parts:
                dirs[:] = []
                continue
            backups += sum(1 for d in dirs if re.search(
                r'backup|checkpoint', d, re.IGNORECASE))
            for file_name in files:
                suffix = os.path.splitext(file_name)[1].lower()
                if suffix in CODE_SUFFIXES or suffix in ARCHIVE_SUFFIXES:
                    code += 1
                elif (suffix == '.bak'
                      or re.search(r'backup|checkpoint', file_name,
                                   re.IGNORECASE)):
                    backups += 1
        if code:
            found.append(Violation('P2', rel + '/', None,
                                   '%d code or archive file(s) outside '
                                   'provenance/' % code))
        if backups:
            found.append(Violation('P2', rel + '/', None,
                                   '%d backup or checkpoint entr(ies)'
                                   % backups))
    allowed = set()
    pyproject = project.text('pyproject.toml') or ''
    name = re.search(r'(?m)^name\s*=\s*"([^"]+)"', pyproject)
    version = re.search(r'(?m)^version\s*=\s*"([^"]+)"', pyproject)
    if name and version:
        dist_name = re.sub(r'[-_.]+', '_', name.group(1))
        allowed = {'%s-%s-py3-none-any.whl' % (dist_name, version.group(1)),
                   '%s-%s.tar.gz' % (dist_name, version.group(1))}
    for entry in project.listdir('dist'):
        if entry not in allowed:
            found.append(Violation('P2', 'dist/' + entry, None,
                                   'not the current wheel or sdist'))
    return found


def check_p3(project):
    """Scripts are grouped by purpose and carry no test_ prefix."""
    found = []
    registered = registered_layers(project) or set()
    reported_dirs = set()
    for rel in project.under('scripts'):
        parts = PurePosixPath(rel).parts
        if parts[-1].startswith('test_'):
            found.append(Violation('P3', rel, None,
                                   'test_ prefix in scripts/'))
        if len(parts) == 2:
            if rel not in registered:
                found.append(Violation(
                    'P3', rel, None,
                    'not in collect/, experiments/ or maintenance/ and not '
                    'a registered compatibility layer'))
        elif parts[1] not in P3_SCRIPT_DIRS and parts[1] not in reported_dirs:
            reported_dirs.add(parts[1])
            found.append(Violation('P3', 'scripts/%s/' % parts[1], None,
                                   'scripts/ subdirectory not defined by P3'))
    return found


def count_tests(project):
    """Static count of test methods in tests/test*.py."""
    total = 0
    for rel in project.under('tests'):
        name = PurePosixPath(rel).name
        if not (name.startswith('test') and name.endswith('.py')):
            continue
        try:
            tree = ast.parse(project.text(rel) or '')
        except (SyntaxError, ValueError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                total += sum(
                    1 for item in node.body
                    if isinstance(item, (ast.FunctionDef,
                                         ast.AsyncFunctionDef))
                    and item.name.startswith('test'))
    return total


def recorded_baseline(project):
    text = ' '.join((project.text('RULES.md') or '').split())
    match = re.search(r'baseline count \((\d+) on', text)
    return int(match.group(1)) if match else None


def check_p4(project):
    """Test count is not below the baseline; tests do not use reports/."""
    found = []
    baseline = recorded_baseline(project)
    if baseline is None:
        found.append(Violation('P4', 'RULES.md', None,
                               'recorded test baseline not found'))
    else:
        count = count_tests(project)
        if count < baseline:
            found.append(Violation('P4', 'tests/', None,
                                   '%d tests, below the baseline of %d'
                                   % (count, baseline)))
    # A test depends on reports/ when it reaches the project's reports/
    # through the root, or names an existing report directory. Paths below
    # temporary directories are not flagged.
    existing = [re.escape(n) for n in project.listdir('reports')
                if not n.startswith('.')]
    patterns = [re.compile(r'''(\bROOT\b|parents\[\d+\]).*\breports\b''')]
    if existing:
        patterns.append(re.compile(r'\breports\W+(%s)\b' % '|'.join(existing)))
    for rel in project.under('tests'):
        if not rel.endswith('.py'):
            continue
        for number, line in enumerate(
                (project.text(rel) or '').splitlines(), 1):
            if any(p.search(line) for p in patterns):
                found.append(Violation('P4', rel, number,
                                       'test refers to the project reports/'))
    return found


CHECKS = collections.OrderedDict([
    ('G2', check_g2), ('G3', check_g3), ('G7', check_g7), ('G8', check_g8),
    ('G9', check_g9), ('D1', check_d1), ('D2', check_d2), ('D4', check_d4),
    ('D5', check_d5), ('D6', check_d6), ('D7', check_d7), ('D8', check_d8),
    ('P1', check_p1), ('P2', check_p2), ('P3', check_p3), ('P4', check_p4),
])


def run(project, rules):
    """Run the selected checks; return {rule: [Violation, ...]}."""
    results = collections.OrderedDict()
    for rule in rules:
        try:
            results[rule] = CHECKS[rule](project)
        except Exception as error:  # report and keep checking other rules
            results[rule] = [Violation(rule, '-', None,
                                       'check failed: %s' % type(error).__name__)]
    return results


def format_violation(v):
    location = v.path if v.line is None else '%s:%d' % (v.path, v.line)
    return '%-3s %s: %s' % (v.rule, location, v.message)


def parse_rules(values):
    rules = []
    for value in values or []:
        for item in value.split(','):
            item = item.strip().upper()
            if item and item not in rules:
                rules.append(item)
    return rules


def main(argv=None, out=None):
    out = out or sys.stdout
    parser = argparse.ArgumentParser(
        description='Check the project against RULES.md (read-only).')
    parser.add_argument('--rule', action='append', metavar='ID',
                        help='rule ID(s) to check, repeatable or '
                             'comma-separated (default: all)')
    parser.add_argument('--root', type=Path, default=ROOT,
                        help='project root (default: this checkout)')
    parser.add_argument('--list-rules', action='store_true',
                        help='list the checks and exit')
    args = parser.parse_args(argv)
    if args.list_rules:
        for rule, check in CHECKS.items():
            out.write('%-3s %s\n' % (rule, check.__doc__.splitlines()[0]))
        return 0
    rules = parse_rules(args.rule) or list(CHECKS)
    unknown = [r for r in rules if r not in CHECKS]
    if unknown:
        parser.error('unknown rule ID(s): %s (known: %s)'
                     % (', '.join(unknown), ', '.join(CHECKS)))
    results = run(Project(args.root), rules)
    total = 0
    for violations in results.values():
        for v in violations:
            out.write(format_violation(v) + '\n')
        total += len(violations)
    out.write('\nViolations by rule:\n')
    for rule, violations in results.items():
        out.write('  %-3s %d\n' % (rule, len(violations)))
    out.write('Total: %d\n' % total)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
