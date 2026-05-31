"""Walk all .md files and count broken internal links.

Two passes:
  1. PATH pass   — does the target file exist on disk?
  2. ANCHOR pass — for `file.md#anchor` links, does the anchor exist in the
                   target file? An anchor exists if the target file declares
                   `id="anchor"` OR has a heading whose GitHub slug equals it.
                   A bare `#` (top of page) is always valid and skipped.

No third-party deps — stdlib only (re, sys, io, pathlib).
"""
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
VAULT = Path(__file__).resolve().parent.parent

LINK = re.compile(r'\[([^\]]+)\]\(([^)#]+)(#[^)]*)?\)')
# Full-link matcher used for the anchor pass (keeps the fragment attached).
LINK_FULL = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
ID_RE = re.compile(r'id="([^"]+)"')
HEAD_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
SKIP_DIRS = {'scripts', 'graphs', '.git'}


def gh_slug(text: str) -> str:
    """Approximate GitHub's heading -> anchor slug algorithm."""
    # [label](url) -> label ; drop inline-code backticks
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = text.replace('`', '')
    s = text.strip().lower()
    # keep only alnum, space, hyphen (drops parens, dots, slashes, etc.)
    s = re.sub(r'[^a-z0-9 \-]', '', s)
    s = s.replace(' ', '-')
    return s


def anchors_for(text: str) -> set:
    """All valid anchors in a file: explicit id="..." + GitHub heading slugs.

    Duplicate heading slugs get the GitHub `-1`, `-2`, ... suffixes.
    """
    anchors = set(ID_RE.findall(text))
    seen = {}
    for line in text.splitlines():
        m = HEAD_RE.match(line)
        if not m:
            continue
        base = gh_slug(m.group(2))
        if not base:
            continue
        if base in seen:
            seen[base] += 1
            anchors.add(f'{base}-{seen[base]}')
        else:
            seen[base] = 0
            anchors.add(base)
    return anchors


def main():
    # Collect the in-scope .md files once (skip tooling / graph / git dirs).
    md_files = []
    for md in VAULT.rglob('*.md'):
        if md.relative_to(VAULT).parts[0] in SKIP_DIRS:
            continue
        md_files.append(md)

    # ---- Pass 1: path existence ----
    n_total = 0
    n_broken = 0
    broken = []
    for md in md_files:
        rel = md.relative_to(VAULT)
        text = md.read_text(encoding='utf-8')
        for m in LINK.finditer(text):
            url = m.group(2)
            if url.startswith(('http', 'mailto', '#')):
                continue
            target = (md.parent / url).resolve()
            n_total += 1
            if not target.exists():
                n_broken += 1
                broken.append((str(rel), url, m.group(1)[:50]))
    print(f'Total internal links: {n_total}')
    print(f'Broken (path): {n_broken}  ({100*n_broken//max(n_total,1)}%)')
    if broken:
        print('\nBroken paths:')
        for f, u, lbl in broken:          # no cap — print every offender
            print(f'  {f}: -> {u}  [{lbl}]')

    # ---- Pass 2: anchor validation ----
    # Build the anchor set for every in-scope file up front.
    file_anchors = {}
    for md in md_files:
        file_anchors[md.resolve()] = anchors_for(md.read_text(encoding='utf-8'))

    n_anchor = 0
    anchor_broken = []
    for md in md_files:
        rel = md.relative_to(VAULT)
        text = md.read_text(encoding='utf-8')
        for m in LINK_FULL.finditer(text):
            url = m.group(2)
            if url.startswith(('http', 'mailto')):
                continue
            if '#' not in url:
                continue
            path, frag = url.split('#', 1)
            if frag == '':
                continue  # bare '#' == top of page; always valid
            tgt = md.resolve() if path == '' else (md.parent / path).resolve()
            anchors = file_anchors.get(tgt)
            if anchors is None:
                # Target file is outside scope or missing on disk — that is a
                # PATH problem already counted in pass 1; don't double-report.
                continue
            n_anchor += 1
            if frag not in anchors:
                anchor_broken.append((str(rel), url, frag))

    print(f'\nAnchor links checked: {n_anchor}')
    print(f'Broken (anchor): {len(anchor_broken)}')
    if anchor_broken:
        print('\nBroken anchors:')
        for f, u, frag in anchor_broken:  # no cap
            print(f'  {f}: -> {u}  (no anchor "{frag}" in target)')


if __name__ == '__main__':
    main()
