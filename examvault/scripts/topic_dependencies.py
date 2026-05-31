#!/usr/bin/env python3
"""Show prerequisites and downstream topics for a given course topic.

Usage:
  python topic_dependencies.py <topic-id-or-label>

Examples:
  python topic_dependencies.py Functor
  python topic_dependencies.py State
  python topic_dependencies.py monad-transformers
"""
import sys
import json
import pathlib

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VAULT = pathlib.Path(__file__).resolve().parent.parent
DEP_GRAPH = VAULT / "graphs" / "DEPENDENCY-GRAPH.json"


def normalise(s: str) -> str:
    return s.strip().lower().replace("-", " ").replace("_", " ")


def find_node(query: str, nodes: list) -> list:
    q = normalise(query)
    hits = []
    for n in nodes:
        nid = n.get("id", "")
        label = normalise(n.get("label", ""))
        if normalise(nid) == q:
            return [n]
        if q in label or label in q:
            hits.append(n)
    return hits


def prerequisites(node_id: str, edges: list, transitive: bool = False) -> list:
    direct = []
    for e in edges:
        if e.get("to") == node_id and e.get("type") in ("prerequisite-of", "strengthens"):
            direct.append((e.get("from"), e.get("type"), e.get("weight", 0), e.get("note", "")))
    direct.sort(key=lambda x: -x[2])
    if not transitive:
        return direct

    # BFS over the graph
    seen = {node_id}
    queue = [node_id]
    result = []
    while queue:
        nid = queue.pop()
        for e in edges:
            if e.get("to") == nid and e.get("type") in ("prerequisite-of", "strengthens"):
                src = e.get("from")
                if src not in seen:
                    seen.add(src)
                    queue.append(src)
                    result.append((src, e.get("type"), e.get("weight", 0), e.get("note", "")))
    return result


def downstream(node_id: str, edges: list) -> list:
    out = []
    for e in edges:
        if e.get("from") == node_id and e.get("type") in ("prerequisite-of", "strengthens"):
            out.append((e.get("to"), e.get("type"), e.get("weight", 0), e.get("note", "")))
    out.sort(key=lambda x: -x[2])
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    query = " ".join(sys.argv[1:])
    data = json.loads(DEP_GRAPH.read_text(encoding="utf-8"))
    nodes = data["nodes"]
    edges = data["edges"]

    hits = find_node(query, nodes)
    if not hits:
        print(f"No topic matched: {query!r}")
        print(f"Available topics (sample): {', '.join(n['id'] for n in nodes[:15])} ...")
        return 1

    for node in hits[:3]:
        nid = node["id"]
        print(f"Topic: {nid} - {node['label']}")
        print(f"Description: {node['description']}")
        print(f"Introduced: Week {node.get('week-introduced', '?')}")
        print(f"Tags: {', '.join(node.get('tags', []))}")
        print(f"Files: {', '.join(node.get('files', []))}")
        print("=" * 70)

        print("\nDirect prerequisites (you must know these first):")
        prereqs = prerequisites(nid, edges, transitive=False)
        if prereqs:
            for src, etype, w, note in prereqs:
                print(f"  [{etype:18}] {src:30}  (w={w})  {note}")
        else:
            print("  (none — foundational topic)")

        print("\nTransitive prerequisites (full chain, unique):")
        trans = prerequisites(nid, edges, transitive=True)
        seen = set()
        for src, etype, w, note in trans:
            if src not in seen:
                seen.add(src)
                print(f"  - {src}")

        print("\nDirect downstream (these depend on this topic):")
        downs = downstream(nid, edges)
        if downs:
            for tgt, etype, w, note in downs:
                print(f"  [{etype:18}] {tgt:30}  (w={w})  {note}")
        else:
            print("  (leaf — nothing depends on this)")

        print("\n" + "-" * 70)

    print(f"\nSee meta/COURSE-MAP.md for full topic blocks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
