"""Repair the nested-link damage from _phase1f_body_linkify.py.

The body linkifier ran on lines that already contained existing markdown links of the form
  [`path/file.md`](path/file.md)
It replaced the backtick label part with a link, producing nested markup:
  [[file](path/file.md)](path/file.md)

This script detects that pattern and restores [file](path/file.md).
"""
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'scripts', 'graphs', '.git'}

# [[name](url1)](url2)  -- if url1 == url2 (or one is a prefix of the other with anchor), collapse.
# Allow optional #anchor on either URL.
DAMAGED = re.compile(r'\[\[([^\]]+)\]\(([^)]+)\)\]\(([^)]+)\)')

def fix_text(text):
    n = 0
    while True:
        m = DAMAGED.search(text)
        if not m:
            break
        label, url1, url2 = m.group(1), m.group(2), m.group(3)
        # Strip anchors for comparison
        u1_base = url1.split('#')[0]
        u2_base = url2.split('#')[0]
        if u1_base == u2_base:
            # Collapse to [label](url1) -- the more specific URL (with anchor) wins
            url = url1 if '#' in url1 else url2
            replacement = f'[{label}]({url})'
            text = text[:m.start()] + replacement + text[m.end():]
            n += 1
        else:
            # Genuine nested link — skip
            break
    return text, n

def main():
    total = 0
    files = 0
    for md in sorted(VAULT.rglob('*.md')):
        parts = md.relative_to(VAULT).parts
        if parts[0] in SKIP_DIRS:
            continue
        text = md.read_text(encoding='utf-8', newline='')
        new, n = fix_text(text)
        if n > 0:
            md.write_text(new, encoding='utf-8', newline='')
            total += n
            files += 1
            print(f'OK {md.relative_to(VAULT)}: {n} fixes')
    print(f'\nTotal: {total} fixes across {files} files')

if __name__ == '__main__':
    main()
