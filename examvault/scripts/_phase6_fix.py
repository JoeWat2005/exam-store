"""Repair the nested-link damage from the first Phase 6 run.

The original script applied path-to-link transformation, then ran the bare 'A09' code
linkifier across the same line — which re-substituted inside the URL of the just-created
link, producing broken nested markdown like:

  [A09-prelude-reimpl](../archetypes/[A09](../archetypes/A09-prelude-reimpl.md)-prelude-reimpl.md)

This script detects that pattern and restores it to:

  [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md)
"""
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
INDEXES = VAULT / 'indexes'

# Damaged pattern. Captures:
#   group 1: the outer label (e.g., 'A09-prelude-reimpl')
#   group 2: the actual filename (e.g., 'A09-prelude-reimpl.md')
DAMAGED = re.compile(
    r'\[([^\]]+)\]\(\.\./archetypes/\[A\d+\]\(\.\./archetypes/(A\d+-[a-zA-Z0-9-]+\.md)\)-[a-zA-Z0-9-]+\.md\)'
)

# Pitfalls / monads / trees / etc dirs may also have damage when the bare code coincided
# with a file label — match any nested form.
DAMAGED_GENERIC = re.compile(
    r'\[([^\]]+)\]\(\.\./([a-z][a-z-]+)/\[A\d+\]\(\.\./archetypes/(A\d+-[a-zA-Z0-9-]+\.md)\)[^)]*\)'
)

def fix_file(path):
    text = path.read_text(encoding='utf-8', newline='')
    n = 0
    while True:
        new = DAMAGED.sub(r'[\1](../archetypes/\2)', text)
        if new == text:
            break
        text = new
        n += 1
    while True:
        new = DAMAGED_GENERIC.sub(r'[\1](../archetypes/\3)', text)
        if new == text:
            break
        text = new
        n += 1
    if n > 0:
        path.write_text(text, encoding='utf-8', newline='')
    # Count actual remaining links by inspecting result
    return n

def main():
    targets = sorted(INDEXES.glob('*.md'))
    total = 0
    for path in targets:
        n = fix_file(path)
        total += n
        marker = 'OK' if n > 0 else '  '
        print(f'{marker} {path.name}: {n} repair passes')
    print(f'\nTotal: {total} repair passes across {len(targets)} files')

if __name__ == '__main__':
    main()
