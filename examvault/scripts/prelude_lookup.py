#!/usr/bin/env python3
"""Look up a Prelude / Data.List / Data.Char / Data.Maybe / Control.Monad function.

Usage:
  python prelude_lookup.py <name>

Examples:
  python prelude_lookup.py mapM
  python prelude_lookup.py foldr
  python prelude_lookup.py transpose
  python prelude_lookup.py fromMaybe
"""
import sys
import pathlib
import re

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VAULT = pathlib.Path(__file__).resolve().parent.parent
PRELUDE_INDEX = VAULT / "indexes" / "PRELUDE-INDEX.md"


def parse_index() -> list:
    """Parse markdown tables in PRELUDE-INDEX.md into a list of rows.

    Each entry is a dict: {name, sig, what, used_in, pitfall, section}.
    """
    text = PRELUDE_INDEX.read_text(encoding="utf-8")
    rows = []
    section = "(unknown)"

    for line in text.splitlines():
        s = line.strip()

        # Track section heading
        if s.startswith("## "):
            section = s.lstrip("# ").strip()
            continue

        # Markdown table row: starts with `|`, has at least 5 cells, second char `\``
        if not s.startswith("|"):
            continue
        # Skip header / separator rows
        if "Name" in s and "Signature" in s:
            continue
        if re.match(r"^\|\s*[-:|]+\s*\|", s):
            continue

        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 5:
            continue

        name_cell = cells[0]
        # Extract the first backtick token as the name
        m = re.search(r"`([^`]+)`", name_cell)
        if not m:
            continue
        name = m.group(1).strip()
        sig = strip_md(cells[1])
        what = strip_md(cells[2])
        used = strip_md(cells[3])
        pitfall = strip_md(cells[4])
        rows.append({
            "name": name,
            "sig": sig,
            "what": what,
            "used_in": used,
            "pitfall": pitfall,
            "section": section,
        })
    return rows


def strip_md(s: str) -> str:
    return s.replace("`", "")


def find(query: str, rows: list) -> list:
    q = query.lower().strip()
    exact = []
    sub = []
    for row in rows:
        n = row["name"].lower()
        if n == q:
            exact.append(row)
        elif q in n or n in q:
            sub.append(row)
    return exact + sub


def grep_uses(name: str) -> list:
    """Find vault files (under archetypes/, monads/, trees/) that mention this name."""
    out = []
    pattern = re.compile(rf"\b{re.escape(name)}\b")
    targets = [VAULT / d for d in ["archetypes", "monads", "trees", "interpreters", "typeclasses", "question-families", "cross-matrix"]]
    for base in targets:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            matches = len(pattern.findall(text))
            if matches:
                rel = path.relative_to(VAULT).as_posix()
                out.append((rel, matches))
    out.sort(key=lambda x: (-x[1], x[0]))
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    query = sys.argv[1]
    try:
        rows = parse_index()
    except Exception as e:
        print(f"ERROR: could not parse PRELUDE-INDEX.md: {e}")
        return 1

    hits = find(query, rows)
    if not hits:
        print(f"Function not found in PRELUDE-INDEX.md: {query!r}")
        print(f"Index has {len(rows)} entries. Try a substring (e.g. 'safe', 'fold').")
        return 1

    print(f"Query: {query!r}")
    print(f"Matched {len(hits)} entries.")
    print("=" * 70)

    for row in hits[:8]:
        print()
        print(f"  {row['name']}")
        print(f"    Section:  {row['section']}")
        print(f"    Sig:      {row['sig']}")
        print(f"    What:     {row['what']}")
        print(f"    Used in:  {row['used_in']}")
        if row["pitfall"]:
            print(f"    Pitfall:  {row['pitfall']}")

    # Where this name appears in vault
    if hits:
        primary = hits[0]["name"]
        uses = grep_uses(primary)
        print()
        print(f"  Files using '{primary}' (top 12):")
        if uses:
            for rel, n in uses[:12]:
                print(f"    {n:>3}×  {rel}")
        else:
            print("    (none found)")

    print()
    print("=" * 70)
    print(f"Full reference: indexes/PRELUDE-INDEX.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
