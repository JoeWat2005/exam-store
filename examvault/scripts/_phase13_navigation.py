"""Phase 13: inject a consistent quick-nav strip at the top and a back-to-index
footer at the bottom of every content page. Makes HOME, NAVIGATION, and the
MASTER-INDEX reachable from any page in one click, no matter how deep the user
has scrolled.

Top block (between breadcrumb and content):
  <!-- topnav:start -->
  > **Quick nav:** [HOME](<rel>HOME.md) · [NAVIGATION](<rel>NAVIGATION.md) · [MASTER-INDEX](<rel>indexes/MASTER-INDEX.md)
  <!-- topnav:end -->

Bottom block (end of file):
  <!-- footernav:start -->
  ---
  > **Back to:** [HOME](<rel>HOME.md) · [NAVIGATION](<rel>NAVIGATION.md) · [MASTER-INDEX](<rel>indexes/MASTER-INDEX.md) · [^ top](#)
  <!-- footernav:end -->

Idempotent: re-running overwrites the existing blocks.

Skips HOME.md, NAVIGATION.md, and indexes/MASTER-INDEX.md so they don't
self-link.
"""
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent

SKIP_RELS = {
    'HOME.md',
    'NAVIGATION.md',
    'indexes/MASTER-INDEX.md',
}

TOPNAV_START = '<!-- topnav:start -->'
TOPNAV_END = '<!-- topnav:end -->'
FOOTERNAV_START = '<!-- footernav:start -->'
FOOTERNAV_END = '<!-- footernav:end -->'

TOPNAV_BLOCK = re.compile(
    re.escape(TOPNAV_START) + r'.*?' + re.escape(TOPNAV_END) + r'\n?',
    re.DOTALL,
)
FOOTERNAV_BLOCK = re.compile(
    re.escape(FOOTERNAV_START) + r'.*?' + re.escape(FOOTERNAV_END) + r'\n?',
    re.DOTALL,
)


def make_paths(depth):
    """Return relative paths to HOME / NAV / INDEX from a file at the given depth."""
    prefix = '../' * depth
    return {
        'HOME':  prefix + 'HOME.md',
        'NAV':   prefix + 'NAVIGATION.md',
        'INDEX': prefix + 'indexes/MASTER-INDEX.md',
    }


def build_topnav(paths):
    return (
        f"{TOPNAV_START}\n"
        f"> **Quick nav:** [HOME]({paths['HOME']}) · [NAVIGATION]({paths['NAV']}) · [MASTER-INDEX]({paths['INDEX']})\n"
        f"{TOPNAV_END}\n"
    )


def build_footernav(paths):
    return (
        f"{FOOTERNAV_START}\n"
        f"\n---\n"
        f"> **Back to:** [HOME]({paths['HOME']}) · [NAVIGATION]({paths['NAV']}) · [MASTER-INDEX]({paths['INDEX']}) · [^ top](#)\n"
        f"{FOOTERNAV_END}\n"
    )


def process(path, vault_root):
    text = path.read_text(encoding='utf-8', newline='')

    # Remove existing top/footer nav blocks (idempotency)
    text = TOPNAV_BLOCK.sub('', text)
    text = FOOTERNAV_BLOCK.sub('', text)

    # Compute depth
    rel = path.relative_to(vault_root)
    depth = len(rel.parts) - 1
    paths = make_paths(depth)

    topnav = build_topnav(paths)
    footernav = build_footernav(paths)

    # Inject topnav: prepend at very start of file, with a blank line after
    new_text = topnav + '\n' + text.lstrip()

    # Inject footernav: append at end, ensuring a separating blank line
    if not new_text.endswith('\n'):
        new_text += '\n'
    new_text = new_text.rstrip() + '\n\n' + footernav

    path.write_text(new_text, encoding='utf-8', newline='')


def main():
    total = 0
    skipped = 0
    for md in VAULT.rglob('*.md'):
        rel_posix = md.relative_to(VAULT).as_posix()
        if rel_posix in SKIP_RELS:
            skipped += 1
            continue
        process(md, VAULT)
        total += 1
    print(f'Total: {total} pages got nav blocks (skipped {skipped} self-targets)')


if __name__ == '__main__':
    main()
