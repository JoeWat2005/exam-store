"""Phase 1f (deferred): linkify backtick vault paths in body content of theory files.

For each `path/to/file.md` mention OUTSIDE a fenced code block, convert to
[file](relative/path/to/file.md). Skips text already inside markdown link URLs.
Preserves file structure and never touches fenced code blocks.
"""
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'scripts', 'graphs', '.git'}
SKIP_FILES = {'GAP-AUDIT.md', 'script-baseline.txt', 'script-postupgrade.txt', 'script-diff.txt',
              'SCRIPT-COMPATIBILITY-REPORT.md', 'WIKI-UPGRADE-REPORT.md'}

# Match: `<dir>/<file>.md` where dir is a known vault top-level dir
KNOWN_DIRS = {'archetypes', 'question-families', 'cross-matrix', 'trees', 'monads',
              'typeclasses', 'interpreters', 'quickcheck', 'pitfalls', 'exam-day',
              'indexes', 'meta', 'haskell-basics'}
DIR_RE = '|'.join(KNOWN_DIRS)
BACKTICK_PATH = re.compile(rf'`((?:{DIR_RE})/[A-Za-z][A-Za-z0-9_-]*\.md)(#[a-z0-9-]+)?`')
# Fenced code blocks
FENCE = re.compile(r'^```')

def compute_rel(from_file, target_path):
    """Compute the relative path from from_file's directory to target_path (which is vault-relative)."""
    from_dir = from_file.parent
    target = VAULT / target_path
    try:
        rel = target.resolve().relative_to(from_dir.resolve())
        return str(rel).replace('\\', '/')
    except ValueError:
        # Need to go up
        from_parts = from_dir.resolve().parts
        target_parts = target.resolve().parts
        # Find common prefix
        i = 0
        while i < len(from_parts) and i < len(target_parts) and from_parts[i] == target_parts[i]:
            i += 1
        up = ['..'] * (len(from_parts) - i)
        down = list(target_parts[i:])
        return '/'.join(up + down)

def transform_file(file_path):
    text = file_path.read_text(encoding='utf-8', newline='')
    lines = text.splitlines(keepends=True)
    out = []
    in_code = False
    n = 0
    for line in lines:
        if FENCE.match(line):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        def replace(m):
            nonlocal n
            target = m.group(1)
            anchor = m.group(2) or ''
            rel = compute_rel(file_path, target)
            label = target.split('/')[-1].replace('.md', '')
            n += 1
            return f'[{label}]({rel}{anchor})'
        new_line = BACKTICK_PATH.sub(replace, line)
        out.append(new_line)
    new = ''.join(out)
    if new != text:
        file_path.write_text(new, encoding='utf-8', newline='')
    return n

def main():
    total = 0
    files = 0
    for md in sorted(VAULT.rglob('*.md')):
        parts = md.relative_to(VAULT).parts
        if parts[0] in SKIP_DIRS:
            continue
        if md.name in SKIP_FILES:
            continue
        n = transform_file(md)
        if n > 0:
            total += n
            files += 1
            print(f'OK {md.relative_to(VAULT)}: {n} links')
    print(f'\nTotal: {total} backtick-paths linkified across {files} files')

if __name__ == '__main__':
    main()
