#!/usr/bin/env python3
"""Pure-Python grep across the vault for a keyword.

Usage:
  python search_by_keyword.py <keyword> [more terms ...]

Examples:
  python search_by_keyword.py applyNTimes
  python search_by_keyword.py Nim
  python search_by_keyword.py "magic square"
"""
import sys
import re
import pathlib

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VAULT = pathlib.Path(__file__).resolve().parent.parent

# CONFIG
MAX_RESULTS = 80         # cap total lines printed
CONTEXT_WIDTH = 110      # truncate long lines to this many chars
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__"}


def grep(query: str) -> list:
    """Return list of (rel-path, line-num, line)."""
    # Build a case-insensitive regex from the query terms.
    terms = [re.escape(t) for t in query.split() if t]
    if not terms:
        return []
    pat = re.compile("|".join(terms), re.IGNORECASE)

    results = []
    for path in VAULT.rglob("*.md"):
        if any(skip in path.parts for skip in SKIP_DIRS):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        rel = path.relative_to(VAULT).as_posix()
        for i, line in enumerate(text.splitlines(), start=1):
            if pat.search(line):
                results.append((rel, i, line.strip()))
    return results


def rank_files(results: list) -> list:
    """File-level summary: count, ordered by hit count."""
    counts = {}
    for rel, _, _ in results:
        counts[rel] = counts.get(rel, 0) + 1
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    query = " ".join(sys.argv[1:])
    results = grep(query)

    if not results:
        print(f"No matches for: {query!r}")
        print(f"Searched: {VAULT}/**/*.md")
        return 1

    print(f"Query: {query!r}")
    print(f"Total matches: {len(results)} across {len({r[0] for r in results})} files")
    print("=" * 70)

    print("\nFile-level summary (top 15 by hit count):")
    for rel, n in rank_files(results)[:15]:
        print(f"  {n:>3}×  {rel}")

    print("\n" + "=" * 70)
    print(f"\nLine matches (first {MAX_RESULTS}):")
    for rel, lineno, line in results[:MAX_RESULTS]:
        line_short = line if len(line) <= CONTEXT_WIDTH else line[:CONTEXT_WIDTH - 3] + "..."
        print(f"  {rel}:{lineno}: {line_short}")

    if len(results) > MAX_RESULTS:
        print(f"\n  ... and {len(results) - MAX_RESULTS} more matches.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
