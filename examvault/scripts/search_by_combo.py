#!/usr/bin/env python3
"""Search for cross-matrix files and archetype combos for X + Y.

Usage:
  python search_by_combo.py "<X> + <Y>"
  python search_by_combo.py "<X>" "<Y>"

Examples:
  python search_by_combo.py "Tree + State"
  python search_by_combo.py Tree State
  python search_by_combo.py "Rose + Writer"
"""
import sys
import json
import pathlib
import re

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VAULT = pathlib.Path(__file__).resolve().parent.parent
ARCH_GRAPH = VAULT / "graphs" / "ARCHETYPE-GRAPH.json"
TREE_GRAPH = VAULT / "graphs" / "TREE-GRAPH.json"

# Common shorthand mappings to canonical labels in graphs
LABEL_TO_ARCHETYPE = {
    "tree":          "A01",
    "bt":            "A01",
    "rose":          "A01",
    "expr":          "A05",
    "state":         "A02",
    "writer":        "A15",
    "reader":        "A06",
    "list":          "A21",
    "maybe":         "A09",
    "either":        "A09",
    "bst":           "A11",
    "functor":       "A06",
    "applicative":   "A24",
    "monad":         "A03",
    "parser":        "A16",
    "matrix":        "A04",
    "lazy":          "A18",
    "game":          "A23",
    "interpreter":   "A08",
    "env":           "A08",
    "free":          "A14",
    "scheduler":     "A14",
}


def parse_pair(args: list) -> tuple:
    if len(args) == 1 and "+" in args[0]:
        a, b = args[0].split("+", 1)
        return a.strip().lower(), b.strip().lower()
    if len(args) >= 2:
        return args[0].strip().lower(), args[1].strip().lower()
    return None, None


def find_archetype_for(label: str) -> str | None:
    key = label.lower().strip()
    for k, v in LABEL_TO_ARCHETYPE.items():
        if k in key or key in k:
            return v
    return None


def cross_matrix_files(a: str, b: str) -> list:
    out = []
    cm_dir = VAULT / "cross-matrix"
    if not cm_dir.exists():
        return out
    for path in cm_dir.glob("*.md"):
        name = path.stem.lower()
        if a in name and b in name:
            out.append(path.relative_to(VAULT).as_posix())
    return sorted(out)


def archetype_combo(a_id: str, b_id: str, edges: list) -> tuple:
    """Find combines-with weight between two archetypes."""
    for e in edges:
        if e.get("type") != "combines-with":
            continue
        f, t = e.get("from"), e.get("to")
        if (f == a_id and t == b_id) or (f == b_id and t == a_id):
            return e.get("weight", 0), e.get("note", "")
    return 0, ""


def grep_combo(a: str, b: str) -> list:
    """Find vault files where both a and b co-occur within 500 chars."""
    out = []
    pat_a = re.compile(re.escape(a), re.IGNORECASE)
    pat_b = re.compile(re.escape(b), re.IGNORECASE)
    for path in VAULT.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        if pat_a.search(text) and pat_b.search(text):
            # Co-occurrence window check: at least one instance of `a` within
            # 500 chars of an instance of `b`.
            best = None
            for ma in pat_a.finditer(text):
                for mb in pat_b.finditer(text):
                    dist = abs(ma.start() - mb.start())
                    if dist < 500:
                        best = dist
                        break
                if best is not None:
                    break
            if best is not None:
                rel = path.relative_to(VAULT).as_posix()
                out.append((rel, best))
    out.sort(key=lambda x: x[1])
    return out


def main() -> int:
    args = sys.argv[1:]
    a, b = parse_pair(args)
    if not a or not b:
        print(__doc__)
        return 1

    print(f"Combination: {a!r} + {b!r}")
    print("=" * 70)

    # Step 1 — cross-matrix files
    cm = cross_matrix_files(a, b)
    print(f"\nCross-matrix files:")
    if cm:
        for f in cm:
            print(f"  - {f}")
    else:
        print(f"  (no cross-matrix file for {a}-x-{b} or {b}-x-{a})")

    # Step 2 — archetype combo
    a_id = find_archetype_for(a)
    b_id = find_archetype_for(b)
    print(f"\nArchetype mapping:")
    print(f"  {a!r:20} -> {a_id}")
    print(f"  {b!r:20} -> {b_id}")

    if a_id and b_id:
        data = json.loads(ARCH_GRAPH.read_text(encoding="utf-8"))
        w, note = archetype_combo(a_id, b_id, data["edges"])
        print(f"\nArchetype combines-with weight: {w}  (5 = canonical, 0 = never)")
        if note:
            print(f"  Note: {note}")
        if w >= 3:
            print(f"  -> This is a strong combination. Open both archetype files:")
            print(f"    - archetypes/{a_id}-*.md")
            print(f"    - archetypes/{b_id}-*.md")

    # Step 3 — vault file grep for co-occurrence
    print(f"\nFiles where both terms co-occur (within 500 chars; top 15 by proximity):")
    co = grep_combo(a, b)[:15]
    if co:
        for rel, dist in co:
            print(f"  {dist:>4}c  {rel}")
    else:
        print("  (none)")

    print()
    print("=" * 70)
    print("See cross-matrix/README.md for the data × effect matrix.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
