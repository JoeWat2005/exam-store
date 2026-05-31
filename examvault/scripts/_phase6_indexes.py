"""Phase 6 index linkifier.

Walks IF-YOU-SEE-X.md, KEYWORD-INDEX.md, MASTER-INDEX.md, MOCK-Q-INDEX.md, TYPE-SIGNATURE-DATABASE.md
and converts backtick-quoted vault paths into clickable markdown links. Preserves row count
and column count so scripts that parse these files (search_by_type, etc.) keep working.

PRELUDE-INDEX.md is skipped — its 5-col positional format is parsed by prelude_lookup.py.

Skips text inside fenced code blocks so we don't mangle Haskell examples that contain
backtick names.
"""
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
INDEXES = VAULT / 'indexes'

# Build archetype filename map: 'A01' -> 'A01-tree-recursion.md'
ARCH_FILES = {a.stem.split('-',1)[0]: a.name for a in (VAULT/'archetypes').glob('A*.md')}
ARCH_NAMES = {
    'A01': 'tree recursion', 'A02': 'state game', 'A03': 'generic monad',
    'A04': 'matrix predicate', 'A05': 'ADT translation', 'A06': 'functor instance',
    'A07': 'codec pair', 'A08': 'env eval', 'A09': 'prelude reimpl',
    'A10': 'fold reformulation', 'A11': 'BST ops', 'A12': 'rep conversion',
    'A13': 'pretty printer', 'A14': 'multi-effect interp', 'A15': 'writer trace',
    'A16': 'parser combinators', 'A17': 'zipper', 'A18': 'lazy memo',
    'A19': 'extend interpreter', 'A20': 'laws / iso', 'A21': 'list comp synthesis',
    'A22': 'typeclass instance', 'A23': 'mini-game', 'A24': 'applicative instance',
}

# Match backtick-quoted vault paths like `archetypes/A09-prelude-reimpl.md` or `monads/state.md` or `pitfalls/HIGH-severity.md`
BACKTICK_PATH = re.compile(r'`([a-z][a-z0-9_-]*(?:/[A-Za-z][A-Za-z0-9_-]*)+\.md)`')
# Match bare archetype codes in table cells: 'A09' or 'A09 (acc)' or 'A09 / A21'
ARCH_CODE = re.compile(r'\bA(\d{2})\b')

# Detect fenced code blocks so we leave their content alone
FENCE = re.compile(r'^```')

def link_path(path):
    """Given a vault-relative path like 'archetypes/A09-prelude-reimpl.md', produce a link from indexes/'s POV."""
    # From indexes/, the relative path is '../<path>'
    name = path.split('/')[-1]
    # Drop the .md and dir prefix for the link label
    label = name.replace('.md', '')
    return f'[{label}](../{path})'

def link_arch(code):
    """A09 -> [A09](../archetypes/A09-prelude-reimpl.md)"""
    if code not in ARCH_FILES:
        return code
    return f'[A{code[1:]}](../archetypes/{ARCH_FILES[code]})'

def transform_line(line):
    # Skip if line is mostly text without a table pipe
    # Convert each backtick path to a link
    new = BACKTICK_PATH.sub(lambda m: link_path(m.group(1)), line)
    # Convert bare archetype codes (only outside backticks)
    # Apply only within table cells (delimited by '|')
    if '|' in new:
        parts = new.split('|')
        for i, part in enumerate(parts):
            # Only linkify A## that isn't already inside a markdown link
            def safe_arch(m):
                code = 'A' + m.group(1)
                start = m.start()
                # check if we're inside [...](...) — look for '[' before without matching ']'
                before = part[:start]
                if before.count('[') > before.count(']'):
                    return m.group(0)
                return link_arch(code)
            parts[i] = ARCH_CODE.sub(safe_arch, part)
        new = '|'.join(parts)
    return new

def transform_file(path):
    text = path.read_text(encoding='utf-8', newline='')
    out_lines = []
    in_code = False
    n_changes = 0
    for line in text.splitlines(keepends=True):
        if FENCE.match(line):
            in_code = not in_code
            out_lines.append(line)
            continue
        if in_code:
            out_lines.append(line)
            continue
        new_line = transform_line(line)
        if new_line != line:
            n_changes += 1
        out_lines.append(new_line)
    new = ''.join(out_lines)
    if new != text:
        path.write_text(new, encoding='utf-8', newline='')
    return n_changes

def main():
    targets = [
        'IF-YOU-SEE-X.md',
        'KEYWORD-INDEX.md',
        'MASTER-INDEX.md',
        'MOCK-Q-INDEX.md',
        'TYPE-SIGNATURE-DATABASE.md',
        'LECTURE-INDEX.md',
        'PROBLEM-NUMBER-INDEX.md',
        'ASSIGNMENT-INDEX.md',
    ]
    total = 0
    for name in targets:
        path = INDEXES / name
        if not path.exists():
            print(f'MISS {name}')
            continue
        n = transform_file(path)
        total += n
        print(f'OK   {name}: {n} lines changed')
    print(f'\nTotal: {total} lines changed across {len(targets)} files')

if __name__ == '__main__':
    main()
