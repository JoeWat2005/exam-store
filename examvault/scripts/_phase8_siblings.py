"""Phase 8: inject a siblings navigation strip below the breadcrumb of every content page.

For each directory containing multiple peer .md files, generate a strip listing all peers,
with the current page bolded (not linked) and others linked. Inserted directly after the
breadcrumb line at the top of every content file.

Idempotent: re-running overwrites the existing strip block.

Marker:  <!-- siblings:start --> ... <!-- siblings:end -->
"""
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent

START = '<!-- siblings:start -->'
END = '<!-- siblings:end -->'
SIBLING_BLOCK = re.compile(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', re.DOTALL)

# Short-label rules per directory
def short_label(dirname, filename):
    """Produce a compact label for a sibling pill."""
    stem = filename.replace('.md', '')
    if dirname == 'archetypes':
        return stem.split('-', 1)[0]   # 'A01-tree-recursion' -> 'A01'
    if dirname == 'question-families':
        return stem.replace('-family', '')
    if dirname == 'cross-matrix':
        return stem.replace('-x-', ' × ')
    if dirname == 'pitfalls':
        return stem  # e.g. HIGH-severity, signature-pitfalls
    if dirname == 'quickcheck':
        return stem.replace('-attacks', '')
    if dirname == 'exam-day':
        return stem
    if dirname == 'indexes':
        return stem
    if dirname == 'meta':
        return stem
    if dirname == 'haskell-basics':
        return stem
    # theory dirs
    return stem

# For haskell-basics: group into categories for readability
BASICS_GROUPS = [
    ('Syntax',          ['pattern-matching','guards','if-expressions','let-in','where-clauses','case-expressions','tuples','local-definitions']),
    ('Data',            ['lists','strings','recursion','accumulator-recursion','helper-functions','sorting']),
    ('HOFs',            ['list-comprehensions','higher-order-functions','lambdas','function-composition','currying','partial-application']),
    ('Operators',       ['dollar-operator','dot-operator','sections']),
    ('Types',           ['type-signatures','polymorphism','algebraic-data-types','recursive-data-types','deriving']),
    ('Effects',         ['maybe-basics','either-basics','do-notation-basics']),
    ('Std HOFs',        ['map','filter','foldr','foldl','zip','zipWith','all-any']),
    ('Testing & tools', ['testing-functions','testing-recursive-functions','testing-monadic-functions','testing-tree-functions','ghci-commands','allowed-builtins','safe-haskell','common-templates','ghc-error-decoder']),
]

# Directories we'll process. (dirname, sort_fn)
DIRS = ['archetypes', 'question-families', 'cross-matrix', 'trees', 'monads',
        'typeclasses', 'interpreters', 'quickcheck', 'pitfalls', 'exam-day',
        'indexes', 'meta', 'haskell-basics']

def build_basics_strip(current):
    """Multi-line grouped strip for haskell-basics."""
    lines = []
    for group_name, files in BASICS_GROUPS:
        pills = []
        for f in files:
            if f == current.replace('.md',''):
                pills.append(f'**{f}**')
            else:
                pills.append(f'[{f}](./{f}.md)')
        lines.append(f'> **{group_name}:** ' + ' · '.join(pills))
    return '\n'.join(lines)

def build_single_strip(dirname, peers, current):
    """One-line strip for non-basics dirs."""
    pills = []
    for f in sorted(peers):
        label = short_label(dirname, f)
        if f == current:
            pills.append(f'**{label}**')
        else:
            pills.append(f'[{label}](./{f})')
    return '> **Peers:** ' + ' · '.join(pills)

def list_peers(dir_path):
    """All .md files in dir except README.md."""
    return [p.name for p in dir_path.glob('*.md') if p.name != 'README.md']

def inject_into_file(path, strip):
    text = path.read_text(encoding='utf-8', newline='')
    # Remove any existing sibling block
    text = SIBLING_BLOCK.sub('', text)
    # Find breadcrumb line (starts with '> [examvault](')
    lines = text.splitlines(keepends=True)
    out = []
    inserted = False
    for i, line in enumerate(lines):
        out.append(line)
        if not inserted and line.startswith('> [examvault]'):
            # Insert blank line + strip block after breadcrumb
            block = f'\n{START}\n{strip}\n{END}\n'
            out.append(block)
            inserted = True
    if not inserted:
        # No breadcrumb — prepend strip block
        block = f'{START}\n{strip}\n{END}\n\n'
        out.insert(0, block)
    path.write_text(''.join(out), encoding='utf-8', newline='')

def main():
    total = 0
    for dirname in DIRS:
        d = VAULT / dirname
        if not d.exists():
            continue
        peers = list_peers(d)
        if len(peers) < 2:
            continue
        for fname in peers:
            path = d / fname
            if dirname == 'haskell-basics':
                strip = build_basics_strip(fname)
            else:
                strip = build_single_strip(dirname, peers, fname)
            inject_into_file(path, strip)
            total += 1
        print(f'OK   {dirname}/: {len(peers)} pages got sibling strips')
    print(f'\nTotal: {total} pages updated')

if __name__ == '__main__':
    main()
