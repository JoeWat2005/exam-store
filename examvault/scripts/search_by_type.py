#!/usr/bin/env python3
"""Search the vault by type signature shape.

Usage:
  python search_by_type.py "<sig fragment>"

Examples:
  python search_by_type.py "Tree a -> Int"
  python search_by_type.py "Monad m => m a"
  python search_by_type.py "[[Int]] -> Bool"
"""
import sys
import pathlib
import re

# Force UTF-8 stdout so cp1252 Windows consoles don't choke on unicode arrows/stars.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VAULT = pathlib.Path(__file__).resolve().parent.parent

# CONFIG: 35+ sig-fragment → family/archetype/canonical-file rules.
SIG_RULES = [
    # Generic monad combinators
    (r"Monad m =>.*-> Int -> m \[a\]",      ("monad-combinator-family", ["A03"], "archetypes/A03-generic-monad.md", "applyNTimes (Mock Q2)")),
    (r"Monad m =>.*\[m a\] -> m \[a\]",      ("monad-combinator-family", ["A03"], "monads/generic-combinators.md", "sequenceM")),
    (r"Monad m =>.*\(a -> m b\) -> \[a\]",   ("monad-combinator-family", ["A03"], "monads/generic-combinators.md", "mapM")),
    (r"Monad m =>.*m \(m a\) -> m a",        ("monad-combinator-family", ["A03"], "monads/generic-combinators.md", "join")),
    (r"Monad m =>.*BT a -> m \(BT b\)",      ("monad-combinator-family", ["A03"], "cross-matrix/tree-x-generic-monad.md", "mapMTree")),
    (r"Monad m =>.*m a ->.*-> m a",          ("monad-combinator-family", ["A03"], "monads/generic-combinators.md", "iterate-shape (m a → m a, any middle args)")),
    (r"Monad m =>.*m a -> Int",              ("monad-combinator-family", ["A03"], "archetypes/A03-generic-monad.md", "applyNTimes-shape (Mock Q2)")),
    (r"Applicative.*f \(a -> b\) -> f a",    ("applicative-monad-instance-family", ["A24"], "typeclasses/applicative.md", "<*> signature")),
    (r"Applicative.*\(a -> b -> c\)",        ("applicative-monad-instance-family", ["A24"], "typeclasses/applicative.md", "liftA2")),
    # Tree shapes
    (r"BT a -> Int",                          ("tree-counting-family", ["A01"], "archetypes/A01-tree-recursion.md", "sizeBT / heightBT / countBT")),
    # Alias: the vault's tree type is BT, but students often write the generic name 'Tree'.
    (r"Tree a -> Int",                        ("tree-counting-family", ["A01"], "archetypes/A01-tree-recursion.md", "sizeBT / heightBT / countBT (NB: the vault's tree type is BT, not Tree)")),
    (r"BT a -> \[a\]",                        ("tree-extract-family", ["A01"], "question-families/tree-extract-family.md", "flatten / leaves")),
    (r"BT a -> BT a",                         ("tree-transform-family", ["A01"], "question-families/tree-transform-family.md", "mirror")),
    (r"\(a -> b\) -> BT a -> BT b",           ("functor-instance-family", ["A06", "A01"], "trees/tree-functor.md", "mapBT / Functor BT")),
    (r"Rose a -> Int",                        ("tree-counting-family", ["A01"], "trees/rose-tree.md", "sizeRose / heightRose")),
    (r"Rose a -> Rose a",                     ("tree-transform-family", ["A01"], "question-families/rose-ops-family.md", "prune-shape")),
    (r"Int -> Rose a -> Bool",                ("rose-ops-family", ["A01"], "indexes/MOCK-Q-INDEX.md", "isNBranching (Mock Q1)")),
    (r"Int -> Rose a -> Rose a",              ("rose-ops-family", ["A01"], "indexes/MOCK-Q-INDEX.md", "prune (Mock Q1)")),
    (r"Ord a => BT a -> Bool",                ("bst-ops-family", ["A11"], "archetypes/A11-bst-ops.md", "isBST")),
    (r"Ord a => a -> BT a -> BT a",           ("bst-ops-family", ["A11"], "archetypes/A11-bst-ops.md", "insert/delete")),
    (r"Ord a => a -> BT a -> Bool",           ("bst-ops-family", ["A11"], "archetypes/A11-bst-ops.md", "memberBST")),
    (r"Ord a => \[a\] -> BT a",               ("bst-ops-family", ["A11"], "archetypes/A11-bst-ops.md", "fromList")),
    # Expr / interpreter
    (r"Expr -> Int",                          ("env-eval-family", ["A08"], "interpreters/simple-arith.md", "evalExpr")),
    (r"Expr -> Maybe Int",                    ("env-eval-family", ["A08"], "interpreters/expr-maybe.md", "partial eval")),
    (r"Env -> Expr -> Maybe",                 ("env-eval-family", ["A08"], "archetypes/A08-env-eval.md", "evalWithEnv (problem 148)")),
    (r"Expr -> Circuit",                      ("adt-translation-family", ["A05"], "archetypes/A05-adt-translation.md", "circuit (Mock Q5)")),
    (r"Expr -> Expr",                         ("adt-translation-family", ["A05"], "question-families/adt-translation-family.md", "normalize / simplify")),
    (r"MonadError.*Expr -> m Int",            ("env-eval-family", ["A14"], "interpreters/expr-state-either.md", "calc-with-errors")),
    # Matrix
    (r"\[\[Int\]\] -> Bool",                  ("matrix-predicate-family", ["A04"], "archetypes/A04-matrix-predicate.md", "isMagicSquare (Mock Q4)")),
    (r"\[\[a\]\] -> \[\[a\]\]",               ("matrix-predicate-family", ["A04"], "archetypes/A04-matrix-predicate.md", "transpose-shape")),
    # State / Writer / Reader
    (r"State Int Int",                        ("state-counter-family", ["A02"], "archetypes/A02-state-game.md", "fresh-shape")),
    (r"State s a",                            ("state-game-family", ["A02"], "monads/state.md", "general State")),
    (r"BT a -> BT \(Int, a\)",                ("state-counter-family", ["A02"], "cross-matrix/tree-x-state.md", "labelTree")),
    (r"BT a -> BT \(a, ?Int\)",               ("state-counter-family", ["A02", "A01"], "cross-matrix/tree-x-state.md", "labelTree (reversed tuple)")),
    (r"BT a -> State.*BT",                    ("state-counter-family", ["A02", "A01"], "cross-matrix/tree-x-state.md", "labelTree (Tree × State)")),
    (r"Rose a -> State",                      ("state-counter-family", ["A02", "A01"], "cross-matrix/rose-x-state.md", "labelRose (Rose × State)")),
    (r"NimGame",                              ("state-game-family", ["A02"], "archetypes/A02-state-game.md", "Mock Q3 Nim")),
    (r"Writer.*Sum Int",                      ("writer-trace-family", ["A15"], "monads/writer.md", "countSteps")),
    (r"Writer \[String\]",                    ("writer-trace-family", ["A15"], "monads/writer.md", "logFactorial")),
    (r"Writer w",                             ("writer-trace-family", ["A15"], "monads/writer.md", "general Writer")),
    (r"Reader r",                             ("env-eval-family", ["A08"], "monads/reader.md", "general Reader")),
    # Maybe / Either / error-handling
    (r"\[a\] -> Maybe a",                     ("error-handling-family", ["A09"], "monads/maybe.md", "safeHead-shape")),
    (r"Int -> Int -> Maybe Int",              ("error-handling-family", ["A09"], "monads/maybe.md", "safeDiv-shape")),
    (r"\[Maybe a\] -> Maybe a",               ("error-handling-family", ["A09"], "monads/maybe.md", "firstJust")),
    (r"\[Maybe a\] -> \[a\]",                 ("error-handling-family", ["A09"], "monads/maybe.md", "catMaybes")),
    (r"\(a -> Maybe b\) -> \[a\] -> \[b\]",   ("error-handling-family", ["A09"], "monads/maybe.md", "mapMaybe")),
    (r"Eq a => a -> \[\(a, ?b\)\] -> Maybe b",("error-handling-family", ["A09"], "monads/maybe.md", "lookup-shape")),
    (r"Either",                               ("error-handling-family", ["A09", "A14"], "monads/either.md", "error-with-message")),
    # List
    (r"\[a\] -> Int",                          ("list-rewrite-family", ["A09", "A10"], "archetypes/A09-prelude-reimpl.md", "length-shape")),
    (r"Num a => \[a\] -> a",                   ("list-rewrite-family", ["A09", "A10"], "archetypes/A09-prelude-reimpl.md", "sum/product-shape")),
    (r"\[a\] -> \[a\]",                        ("list-rewrite-family", ["A09", "A10"], "archetypes/A09-prelude-reimpl.md", "transformation")),
    (r"\(a -> b\) -> \[a\] -> \[b\]",          ("list-rewrite-family", ["A09", "A10"], "question-families/list-rewrite-family.md", "map-shape")),
    (r"\(a -> Bool\) -> \[a\] -> \[a\]",       ("list-rewrite-family", ["A09", "A10"], "question-families/list-rewrite-family.md", "filter-shape")),
    (r"\(a -> b -> b\) -> b -> \[a\] -> b",    ("list-fold-family", ["A10"], "archetypes/A10-fold-reformulation.md", "foldr signature")),
    (r"\[\[a\]\] -> \[a\]",                   ("list-rewrite-family", ["A09"], "archetypes/A09-prelude-reimpl.md", "concat")),
    (r"Eq a => a -> \[a\] -> Bool",           ("list-rewrite-family", ["A09"], "archetypes/A09-prelude-reimpl.md", "elem")),
    (r"Int -> a -> \[a\]",                    ("list-rewrite-family", ["A09"], "archetypes/A09-prelude-reimpl.md", "replicate")),
    (r"\[a\] -> \[b\] -> \[\(a, ?b\)\]",      ("list-rewrite-family", ["A09"], "archetypes/A09-prelude-reimpl.md", "zip-shape")),
    # List comp
    (r"Int -> \[\(Int, ?Int, ?Int\)\]",       ("list-comp-family", ["A21"], "question-families/list-comp-family.md", "pyths-shape")),
    (r"Int -> \[Int\]",                        ("list-comp-family", ["A21"], "question-families/list-comp-family.md", "factors/perfects-shape")),
    (r"Int -> Bool",                           ("list-comp-family", ["A21"], "question-families/list-comp-family.md", "isPrime-shape")),
    # String / Char
    (r"String -> String",                     ("codec-family", ["A09", "A07"], "question-families/codec-family.md", "string-transform")),
    (r"String -> Int",                        ("list-comp-family", ["A21"], "question-families/list-comp-family.md", "string-count")),
    (r"String -> Bool",                       ("list-rewrite-family", ["A09"], "question-families/list-rewrite-family.md", "palindrome-shape")),
    (r"Char -> Bool",                         ("codec-family", ["A09"], "question-families/codec-family.md", "char predicate")),
    (r"Int -> String -> String",              ("codec-family", ["A07"], "archetypes/A07-codec-pair.md", "Caesar encode/decode")),
    (r"Eq a => \[a\] -> \[\(a, ?Int\)\]",     ("codec-family", ["A07"], "archetypes/A07-codec-pair.md", "RLE encode")),
    # Lazy / infinite / parser
    (r"\[Integer\]",                          ("lazy-infinite-family", ["A18"], "archetypes/A18-lazy-memo.md", "infinite Integer list (fibs)")),
    (r"\(a -> a\) -> a",                      ("lazy-infinite-family", ["A18"], "archetypes/A18-lazy-memo.md", "fix")),
    (r"\(a -> a\) -> a -> \[a\]",             ("lazy-infinite-family", ["A18"], "archetypes/A18-lazy-memo.md", "iterate")),
    (r"Parser Char",                          ("parser-family", ["A16"], "archetypes/A16-parser-combinators.md", "item / digitP")),
    (r"Parser Int",                           ("parser-family", ["A16"], "archetypes/A16-parser-combinators.md", "parseNat / parseExpr")),
    # IO
    (r"IO \(\)",                              ("error-handling-family", ["A03"], "monads/io.md", "IO action")),
    (r"IO \[Int\]",                           ("error-handling-family", ["A03"], "monads/io.md", "threeNumbers-shape")),
    # Typeclass instance shapes
    (r"Functor f =>",                         ("functor-instance-family", ["A06"], "typeclasses/functor.md", "Functor-using function")),
    (r"Functor.*fmap",                        ("functor-instance-family", ["A06"], "typeclasses/functor.md", "Functor body")),
    (r"Monoid",                               ("applicative-monad-instance-family", ["A22"], "typeclasses/monoid.md", "Monoid usage")),
    # General catch-alls
    # Generic Monad fallback: placed AFTER the specific Monad-sig rules above so those win first.
    (r"Monad m =>",                           ("monad-combinator-family", ["A03"], "archetypes/A03-generic-monad.md", "generic Monad signature (see the A03 combinator family)")),
    (r"Ord a =>",                             ("list-rewrite-family", ["A09", "A11"], "trees/bst.md", "Ord-dependent (sort or BST)")),
    (r"Eq a =>",                              ("list-rewrite-family", ["A09"], "archetypes/A09-prelude-reimpl.md", "Eq-dependent operation")),
    (r"Num a =>",                             ("list-rewrite-family", ["A09"], "typeclasses/num.md", "Num-dependent")),
]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    query = " ".join(sys.argv[1:]).strip()
    # Normalise whitespace
    query_n = re.sub(r"\s+", " ", query)

    matches = []
    for pattern, payload in SIG_RULES:
        if re.search(pattern, query_n):
            matches.append((pattern, payload))

    if not matches:
        print(f"No rule matched signature: {query!r}")
        print()
        print("Try a more general shape, e.g.:")
        print('  python search_by_type.py "Tree a -> Int"')
        print('  python search_by_type.py "Monad m =>"')
        print('  python search_by_type.py "[[Int]] -> Bool"')
        print()
        print("Or browse indexes/TYPE-SIGNATURE-DATABASE.md directly.")
        return 1

    print(f"Query: {query}")
    print(f"Matches: {len(matches)}")
    print("=" * 70)
    for pattern, (family, archs, canonical, note) in matches:
        print(f"\n  Matched pattern: {pattern}")
        print(f"  Family:          {family}")
        print(f"  Archetype(s):    {', '.join(archs)}")
        print(f"  Canonical file:  {canonical}")
        print(f"  Note:            {note}")

    print("\n" + "=" * 70)
    print(f"See also: {VAULT.relative_to(VAULT.parent)}/indexes/TYPE-SIGNATURE-DATABASE.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
