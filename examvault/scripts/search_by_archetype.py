#!/usr/bin/env python3
"""Search the vault by archetype number or label.

Usage:
  python search_by_archetype.py <A##|label>

Examples:
  python search_by_archetype.py A02
  python search_by_archetype.py "State Monad"
  python search_by_archetype.py A14
"""
import sys
import json
import pathlib

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VAULT = pathlib.Path(__file__).resolve().parent.parent
ARCH_GRAPH = VAULT / "graphs" / "ARCHETYPE-GRAPH.json"
TOPIC_GRAPH = VAULT / "graphs" / "TOPIC-GRAPH.json"


def normalise(s: str) -> str:
    return s.lower().replace("-", " ").replace("_", " ").strip()


def find_archetype(query: str, nodes: list) -> list:
    q = normalise(query)
    hits = []
    for n in nodes:
        nid = n.get("id", "")
        if not nid.startswith("A"):
            continue
        # Direct A## hit
        if nid.lower() == q or nid.lower() == q.replace(" ", ""):
            hits.append(n)
            continue
        # Label substring
        label = normalise(n.get("label", ""))
        if q in label or label in q:
            hits.append(n)
            continue
        # Tag match
        tags = [normalise(t) for t in n.get("tags", [])]
        if any(q in t for t in tags):
            hits.append(n)
    return hits


def list_combines(arch_id: str, edges: list) -> list:
    out = []
    for e in edges:
        if e.get("type") != "combines-with":
            continue
        if e.get("from") == arch_id and e.get("weight", 0) >= 3:
            out.append((e["to"], e.get("weight", 0), e.get("note", "")))
        elif e.get("to") == arch_id and e.get("weight", 0) >= 3:
            out.append((e["from"], e.get("weight", 0), e.get("note", "")))
    out.sort(key=lambda x: (-x[1], x[0]))
    return out


def grep_files(arch_id: str) -> list:
    """Find every .md file under the vault that mentions arch_id."""
    found = []
    for path in VAULT.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        if arch_id in text:
            # Count occurrences as a relevance proxy
            count = text.count(arch_id)
            rel = path.relative_to(VAULT).as_posix()
            found.append((rel, count))
    found.sort(key=lambda x: (-x[1], x[0]))
    return found


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    query = " ".join(sys.argv[1:])

    arch_data = json.loads(ARCH_GRAPH.read_text(encoding="utf-8"))
    hits = find_archetype(query, arch_data["nodes"])

    if not hits:
        print(f"No archetype matched: {query!r}")
        print("Available archetypes: A01 .. A24. See archetypes/README.md.")
        return 1

    print(f"Query: {query!r}")
    print("=" * 70)
    for node in hits[:5]:
        nid = node["id"]
        print()
        print(f"  {nid} - {node['label']}")
        print(f"  Tier:     {node.get('tier', '?')}   Stars: {'*' * node.get('stars', 0)}")
        print(f"  F/D/C/E:  {node.get('frequency','?')}/{node.get('difficulty','?')}/{node.get('conceptual-weight','?')}/{node.get('exam-likelihood','?')}")
        print(f"  Primary files:")
        for f in node.get("files", []):
            print(f"    - {f}")

        combines = list_combines(nid, arch_data["edges"])
        if combines:
            print(f"  Combines with (weight >= 3):")
            for other, w, note in combines[:10]:
                print(f"    - {other}  (w={w})  {note}")

        # Files in the vault that mention this archetype
        grep = grep_files(nid)
        if grep:
            print(f"  Mentioned in {len(grep)} vault files (top 10 by frequency):")
            for rel, count in grep[:10]:
                print(f"    - {rel}  ({count}×)")

    print()
    print("=" * 70)
    print("See also: archetypes/README.md for the full priority table.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
