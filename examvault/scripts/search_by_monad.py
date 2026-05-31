#!/usr/bin/env python3
"""Search for vault files involving a specific monad.

Usage:
  python search_by_monad.py <monad>

Examples:
  python search_by_monad.py State
  python search_by_monad.py Writer
  python search_by_monad.py Maybe
  python search_by_monad.py "MonadError"
"""
import sys
import json
import pathlib

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VAULT = pathlib.Path(__file__).resolve().parent.parent
MONAD_GRAPH = VAULT / "graphs" / "MONAD-GRAPH.json"

# Known monad ids
MONAD_ALIASES = {
    "maybe":          "Maybe",
    "either":         "Either",
    "state":          "State",
    "writer":         "Writer",
    "reader":         "Reader",
    "io":             "IO",
    "list":           "List",
    "identity":       "Identity",
    "monaderror":     "MonadError",
    "monadstate":     "MonadState",
    "monadwriter":    "MonadWriter",
    "monadreader":    "MonadReader",
    "statet":         "StateT",
    "exceptt":        "ExceptT",
    "writert":        "WriterT",
    "readert":        "ReaderT",
    "free":           "Free",
    "fsum":           "FSum",
    "parser":         "Parser",
}


def resolve_monad(query: str) -> str | None:
    q = query.strip().lower().replace("[]", "list").replace("(", "").replace(")", "").replace(" ", "")
    return MONAD_ALIASES.get(q)


def find_node(monad_id: str, nodes: list) -> dict | None:
    for n in nodes:
        if n.get("id") == monad_id:
            return n
    return None


def find_related(monad_id: str, edges: list) -> list:
    out = []
    for e in edges:
        if e.get("from") == monad_id:
            out.append((e.get("to"), e.get("type"), e.get("weight", 0), e.get("note", "")))
        elif e.get("to") == monad_id:
            out.append((e.get("from"), e.get("type") + " (incoming)", e.get("weight", 0), e.get("note", "")))
    return sorted(out, key=lambda x: (-x[2], x[0]))


def grep_vault(monad_id: str) -> list:
    """Files that mention the monad name."""
    target = monad_id
    found = []
    for path in VAULT.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        # Use word-boundary-aware count
        import re
        matches = len(re.findall(rf"\b{re.escape(target)}\b", text))
        if matches:
            rel = path.relative_to(VAULT).as_posix()
            found.append((rel, matches))
    found.sort(key=lambda x: (-x[1], x[0]))
    return found


def cross_matrix_files(monad_id: str) -> list:
    """Cross-matrix files that involve this monad."""
    needle = monad_id.lower()
    out = []
    cm_dir = VAULT / "cross-matrix"
    if not cm_dir.exists():
        return out
    for path in cm_dir.glob("*.md"):
        name = path.stem.lower()
        if needle in name:
            out.append(path.relative_to(VAULT).as_posix())
    return sorted(out)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    query = " ".join(sys.argv[1:])
    monad_id = resolve_monad(query)
    if not monad_id:
        print(f"Unknown monad: {query!r}")
        print(f"Known aliases: {sorted(set(MONAD_ALIASES.values()))}")
        return 1

    data = json.loads(MONAD_GRAPH.read_text(encoding="utf-8"))
    node = find_node(monad_id, data["nodes"])

    if not node:
        print(f"Monad {monad_id} not in MONAD-GRAPH.json.")
        return 1

    print(f"Monad: {monad_id} ({node['label']})")
    print(f"Description: {node['description']}")
    print(f"Kind: {node['kind']}")
    print(f"Files: {', '.join(node.get('files', []))}")
    print(f"Implements: {', '.join(node.get('instances', []))}")
    print(f"Tags: {', '.join(node.get('tags', []))}")
    print("=" * 70)

    print("\nRelated monads / classes (edges):")
    for other, etype, weight, note in find_related(monad_id, data["edges"])[:15]:
        print(f"  [{etype:30}] {other:25} (w={weight}) {note}")

    print("\nCross-matrix files involving this monad:")
    cm = cross_matrix_files(monad_id)
    if cm:
        for f in cm:
            print(f"  - {f}")
    else:
        print("  (none — try a parent class)")

    print("\nAll vault files mentioning this monad (top 20 by frequency):")
    for rel, count in grep_vault(monad_id)[:20]:
        print(f"  {count:>3}×  {rel}")

    print()
    print("=" * 70)
    print(f"See monads/{monad_id.lower()}.md for the canonical reference.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
