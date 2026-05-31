"""Phase 1 bulk breadcrumb injector. One-shot tool; safe to re-run (idempotent)."""
import re, sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'scripts', 'graphs', '.git'}
TOP_LEVEL_FILES = {'README.md', 'HOW-TO-USE.md', 'ARCHITECTURE.md', 'STATS.md'}

def breadcrumb(file_path):
    rel = file_path.relative_to(VAULT)
    parts = rel.parts
    if len(parts) == 1:
        if file_path.name == 'README.md':
            return None  # root README needs no breadcrumb
        return f'> [examvault](./README.md) · **<TITLE>**'
    elif file_path.name == 'README.md':
        dir_label = parts[0]
        return f'> [examvault](../README.md) · **{dir_label}**'
    else:
        dir_label = parts[0]
        return f'> [examvault](../README.md) · [{dir_label}](./README.md) · **<TITLE>**'

def extract_title(text):
    m = re.search(r'^# (.+)$', text, flags=re.MULTILINE)
    return m.group(1).strip() if m else None

def inject(file_path):
    text = file_path.read_text(encoding='utf-8', newline='')
    if text.startswith('> [examvault]'):
        return 'skip: already-breadcrumbed'
    crumb = breadcrumb(file_path)
    if crumb is None:
        return 'skip: root README'
    if '<TITLE>' in crumb:
        title = extract_title(text)
        if not title:
            return 'skip: no # heading'
        crumb = crumb.replace('<TITLE>', title)
    new_text = f'{crumb}\n\n' + text
    file_path.write_text(new_text, encoding='utf-8', newline='')
    return f'OK: {crumb}'

def main():
    n_ok = n_skip = 0
    for md in sorted(VAULT.rglob('*.md')):
        rel_parts = md.relative_to(VAULT).parts
        if rel_parts[0] in SKIP_DIRS:
            continue
        result = inject(md)
        status = 'OK' if result.startswith('OK') else 'SKIP'
        if status == 'OK':
            n_ok += 1
        else:
            n_skip += 1
        if status == 'OK':
            print(f'{status}  {md.relative_to(VAULT)}')
    print(f'\nTotal: {n_ok} injected, {n_skip} skipped')

if __name__ == '__main__':
    main()
