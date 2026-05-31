#!/usr/bin/env python3
"""Look up Mock Test Q1..Q5 context + marker quirks.

Usage:
  python mock_q_lookup.py <query>

Examples:
  python mock_q_lookup.py Q1
  python mock_q_lookup.py applyNTimes
  python mock_q_lookup.py "magic square"
  python mock_q_lookup.py Nim
"""
import sys
import pathlib
import re

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VAULT = pathlib.Path(__file__).resolve().parent.parent
MOCK_INDEX = VAULT / "indexes" / "MOCK-Q-INDEX.md"

# Mock Q catalog (kept embedded for fast lookup; mirrors MOCK-Q-INDEX.md).
MOCK_QS = {
    "Q1": {
        "topic":     "isNBranching + prune (Rose tree)",
        "sigs":      ["isNBranching :: Int -> Rose a -> Bool", "prune :: Int -> Rose a -> Rose a"],
        "archetype": "A01",
        "quirk":     "None significant. Make sure `Leaf` is True in isNBranching, and prune does take n . map prune (NOT map prune . take n).",
        "files":     ["archetypes/A01-tree-recursion.md", "trees/rose-tree.md", "question-families/rose-ops-family.md"],
        "aliases":   ["isnbranching", "prune", "rose tree", "branch"],
    },
    "Q2": {
        "topic":     "applyNTimes (generic Monad combinator)",
        "sigs":      ["applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]"],
        "archetype": "A03",
        "quirk":     "Generator deliberately starts at n=2. Off-by-one (n vs n+1 items) is silently lenient: 8 of 10 marks still available. The hard test is 'each monadic action runs exactly once'.",
        "files":     ["archetypes/A03-generic-monad.md", "monads/generic-combinators.md", "quickcheck/monad-attacks.md"],
        "aliases":   ["applyntimes", "apply n times", "generic monad", "monad m"],
    },
    "Q3": {
        "topic":     "Nim with State (gameOver + takeTokens)",
        "sigs":      ["gameOver :: NimGame Bool", "takeTokens :: Int -> Heap -> NimGame ()"],
        "archetype": "A02",
        "quirk":     "`gameOver` has a hardcoded (0,0) test worth 4 free marks: literally `gameOver = pure True` gets 4/10. `takeTokens` MUST clamp at 0 (max 0 (a-n)) — marker tests overshooting.",
        "files":     ["archetypes/A02-state-game.md", "monads/state.md", "cross-matrix/game-state.md"],
        "aliases":   ["nim", "gameover", "taketokens", "heap", "state game", "nimgame"],
    },
    "Q4": {
        "topic":     "isMagicSquare (matrix predicate)",
        "sigs":      ["isMagicSquare :: [[Int]] -> Bool"],
        "archetype": "A04",
        "quirk":     "1x1 matrices are True (vacuously). Don't forget the anti-diagonal — many candidates do.",
        "files":     ["archetypes/A04-matrix-predicate.md", "question-families/matrix-predicate-family.md", "quickcheck/matrix-attacks.md"],
        "aliases":   ["ismagicsquare", "magic square", "transpose", "matrix"],
    },
    "Q5": {
        "topic":     "circuit (Expr -> Circuit ADT translation)",
        "sigs":      ["circuit :: Expr -> Circuit  -- Expr has Var/Not/And/Or/Implies; Circuit has Input/Nand"],
        "archetype": "A05",
        "quirk":     "Checked SEMANTICALLY (boolean equivalence over all assignments), NOT structurally. Verbose-but-correct Nand expansions are fully accepted. DO NOT evaluate Expr to Bool — must be Expr -> Circuit.",
        "files":     ["archetypes/A05-adt-translation.md", "question-families/adt-translation-family.md", "interpreters/desugar-pipeline.md"],
        "aliases":   ["circuit", "nand", "expr to circuit", "translate expr"],
    },
}


def lookup(query: str) -> list:
    q = query.lower().strip()
    hits = []
    for qid, info in MOCK_QS.items():
        if q == qid.lower() or q == qid.lower().replace("q", ""):
            hits.append((qid, info))
            continue
        for alias in info["aliases"]:
            if alias in q or q in alias:
                hits.append((qid, info))
                break
        else:
            # Search topic / sigs for substring
            if q in info["topic"].lower():
                hits.append((qid, info))
                continue
            for s in info["sigs"]:
                if q in s.lower():
                    hits.append((qid, info))
                    break
    # Dedupe by qid
    seen = set()
    unique = []
    for qid, info in hits:
        if qid not in seen:
            seen.add(qid)
            unique.append((qid, info))
    return unique


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    query = " ".join(sys.argv[1:])
    hits = lookup(query)

    if not hits:
        print(f"No Mock Q matched: {query!r}")
        print("Try: Q1 / Q2 / Q3 / Q4 / Q5 / applyNTimes / Nim / circuit / magic / isNBranching")
        return 1

    print(f"Query: {query!r}")
    print(f"Matched {len(hits)} Mock Q entries.")
    print("=" * 70)

    for qid, info in hits:
        print(f"\n  {qid} - {info['topic']}")
        print(f"  Archetype: {info['archetype']}")
        print(f"  Signature(s):")
        for s in info["sigs"]:
            print(f"    {s}")
        print(f"  Marker quirk:")
        # word-wrap quirk text
        words = info["quirk"].split()
        line = "    "
        for w in words:
            if len(line) + len(w) + 1 > 70:
                print(line)
                line = "    " + w + " "
            else:
                line += w + " "
        if line.strip():
            print(line)
        print(f"  Files:")
        for f in info["files"]:
            print(f"    - {f}")

    print()
    print("=" * 70)
    print(f"Full source: indexes/MOCK-Q-INDEX.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
