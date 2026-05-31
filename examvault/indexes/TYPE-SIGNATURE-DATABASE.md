<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **TYPE-SIGNATURE-DATABASE**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · [MASTER-INDEX](./MASTER-INDEX.md) · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · **TYPE-SIGNATURE-DATABASE** · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# TYPE-SIGNATURE-DATABASE

Type signature shape → archetype + question family + canonical file.

> If the question gives ONLY a signature, this is the first lookup. Find a shape that matches yours, jump to the archetype, then refine.

**Conventions:**
- `T` = some user-defined tree-shaped ADT (BT, Rose, Expr, …)
- `m` = some monad
- `f` = some functor / applicative
- All paths are relative to `examvault/`.

---

## Group 1 — `[a] -> r` (list-summary patterns)

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `[a] -> Int` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md), [A10](../archetypes/A10-fold-reformulation.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 11 myLength, 39 wordCount, 42 lengthWithFoldr |
| `Num a => [a] -> a` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md), [A10](../archetypes/A10-fold-reformulation.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 12 mySum, 13 myProduct, 41 sumWithFoldr |
| `[a] -> a` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 22 myLast (partial) |
| `[a] -> [a]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md), [A10](../archetypes/A10-fold-reformulation.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 14 myReverse, 15 fastReverse, 23 myInit, 45 reverseWithFoldl |
| `[a] -> Bool` | list-validation | [A10](../archetypes/A10-fold-reformulation.md) | [list-fold-family](../question-families/list-fold-family.md) | (predicate variants) |
| `Eq a => [a] -> [a]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 29 removeDuplicates |
| `Eq a => a -> [a] -> Bool` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 16 myElem |
| `Eq a => a -> [a] -> [Int]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | 37 positions |
| `Eq a => [a] -> [(a, Int)]` | list-rewrite | [A07](../archetypes/A07-codec-pair.md) | [codec-family](../question-families/codec-family.md) | 147 rle |
| `Eq a => a -> [(a,b)] -> Maybe b` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) | 24 myLookup |
| `Ord a => [a] -> [a]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) / [A11](../archetypes/A11-bst-ops.md) | [bst](../trees/bst.md) | 26 msort, 27 qsort |
| `Ord a => [a] -> Bool` | list-validation | [A10](../archetypes/A10-fold-reformulation.md) | [list-fold-family](../question-families/list-fold-family.md) | 28 isSorted |
| `Ord a => [a] -> [a] -> [a]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 25 merge |
| `Int -> [a] -> [a]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 18 myTake, 19 myDrop |
| `Int -> a -> [a]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 21 myReplicate |
| `[a] -> [a] -> [a]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 30 interleave |
| `[a] -> [b] -> [(a,b)]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 20 myZip |
| `[[a]] -> [a]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 17 myConcat |
| `[a] -> [(a,a)]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | 38 pairs, 106 allPairs |
| `[a] -> [b] -> [(a,b)]` (cart.) | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | 40 cartesian |
| `(a -> Bool) -> [a] -> [a]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) / [A10](../archetypes/A10-fold-reformulation.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | 44 filterWithFoldr, 49 takeWhile' |
| `(a -> Bool) -> [a] -> Bool` | list-fold | [A10](../archetypes/A10-fold-reformulation.md) | [list-fold-family](../question-families/list-fold-family.md) | 46 allWithFoldr |
| `(a -> Bool) -> [a] -> ([a],[a])` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) / [A10](../archetypes/A10-fold-reformulation.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | 50 partition' |
| `(a -> b) -> [a] -> [b]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) / [A10](../archetypes/A10-fold-reformulation.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | 43 mapWithFoldr |
| `[a -> a] -> (a -> a)` | list-fold | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) | 47 compose' |

## Group 2 — `Int -> r` and `Int -> [r]` (numeric-input patterns)

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `Int -> Int` | (rewrite) | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 1 double, 3 sign |
| `Int -> Int -> Int` | (rewrite) | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | (arithmetic combinators) |
| `Int -> Int -> Int -> Int` | (rewrite) | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 4 maxOfThree |
| `Int -> Int -> Int -> Bool` | (rewrite) | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 2 between |
| `Int -> String` | (rewrite) | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 5 dayName |
| `Int -> Bool` | list-comp / arith | [A21](../archetypes/A21-list-comp-synthesis.md) / [A09](../archetypes/A09-prelude-reimpl.md) | [list-comp-family](../question-families/list-comp-family.md) | 6 leapYear, 33 isPrime |
| `Int -> [Int]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | 32 factors, 34 primesUpTo, 35 perfects |
| `Int -> [(Int,Int,Int)]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | 31 pyths |
| `Num a => [a] -> [a] -> a` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | 36 scalar |

## Group 3 — `T -> r` (tree-summary patterns)

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `BT a -> Int` | tree-counting | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) | 71 sizeBT, 72 heightBT |
| `Rose a -> Int` | tree-counting | [A01](../archetypes/A01-tree-recursion.md) | [rose-tree](../trees/rose-tree.md) | 86 sizeRose, 87 heightRose |
| `Expr -> Int` | tree-counting / interp | [A01](../archetypes/A01-tree-recursion.md), [A08](../archetypes/A08-env-eval.md) | [simple-arith](../interpreters/simple-arith.md) | 89 evalExpr, 90 depthExpr |
| `BT a -> [a]` | tree-extract | [A01](../archetypes/A01-tree-recursion.md) | [tree-extract-family](../question-families/tree-extract-family.md) | 73 leavesBT, 75 flattenInOrder, 76 flattenPreOrder/PostOrder |
| `Rose a -> [a]` | tree-extract | [A01](../archetypes/A01-tree-recursion.md) | [rose-tree](../trees/rose-tree.md) | 88 flattenRose |
| `BT a -> BT a` | tree-transform | [A01](../archetypes/A01-tree-recursion.md) | [tree-transform-family](../question-families/tree-transform-family.md) | 74 mirror |
| `Rose a -> Rose a` | tree-transform | [A01](../archetypes/A01-tree-recursion.md) | [rose-ops-family](../question-families/rose-ops-family.md) | (prune variants) |
| `(a -> b) -> BT a -> BT b` | tree-transform / functor | [A01](../archetypes/A01-tree-recursion.md) / [A06](../archetypes/A06-functor-instance.md) | [tree-functor](../trees/tree-functor.md) | 77 mapBT, 125 Functor BT |
| `Num a => BT a -> a` | tree-fold | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) | 78 sumBT |
| `Ord a => BT a -> Maybe a` | tree-extract | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) | 79 maxBT |
| `Eq a => a -> BT a -> Int` | tree-counting | [A01](../archetypes/A01-tree-recursion.md) | [tree-counting-family](../question-families/tree-counting-family.md) | 80 countBT |
| `Ord a => BT a -> Bool` | tree-validation | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | 81 isBST |
| `Ord a => a -> BT a -> BT a` | bst-ops | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | 82 insertBST, 84 deleteBST |
| `Ord a => a -> BT a -> Bool` | bst-ops | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | 83 memberBST |
| `Ord a => [a] -> BT a` | bst-ops | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | 85 fromList |
| `Int -> Rose a -> Bool` | tree-validation | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) | 143 isNBranching (Mock Q1) |
| `Int -> Rose a -> Rose a` | tree-transform | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) | 143 prune (Mock Q1) |
| `Expr -> Circuit` | adt-translation | [A05](../archetypes/A05-adt-translation.md) | [A05-adt-translation](../archetypes/A05-adt-translation.md) | 145 circuit (Mock Q5) |

## Group 4 — `T -> Bool` (tree-predicate patterns)

| Sig pattern | Likely family | Archetypes | Canonical file | Note |
|---|---|---|---|---|
| `BT a -> Bool` | tree-validation | [A01](../archetypes/A01-tree-recursion.md) | [tree-validation-family](../question-families/tree-validation-family.md) | `Empty` typically `True` |
| `Ord a => BT a -> Bool` | tree-validation | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | isBST — bound-threaded |
| `Rose a -> Bool` | tree-validation | [A01](../archetypes/A01-tree-recursion.md) | [tree-validation-family](../question-families/tree-validation-family.md) | predicate over Rose |
| `Int -> Rose a -> Bool` | rose-ops | [A01](../archetypes/A01-tree-recursion.md) | [rose-ops-family](../question-families/rose-ops-family.md) | isNBranching |
| `Eq a => BT a -> Bool` | tree-validation | [A01](../archetypes/A01-tree-recursion.md) | [tree-validation-family](../question-families/tree-validation-family.md) | dupes / palindrome-shape |
| `(a -> Bool) -> BT a -> Bool` | tree-validation | [A01](../archetypes/A01-tree-recursion.md) | [tree-validation-family](../question-families/tree-validation-family.md) | hidden-predicate mutation |

## Group 5 — `Monad m =>` (generic monad combinators)

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `Monad m => m a -> (a -> m b) -> m b` | (primitive) | [A06](../archetypes/A06-functor-instance.md) | [monad](../typeclasses/monad.md) | `>>=` itself |
| `Monad m => m (m a) -> m a` | combinator | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) | 128 join' |
| `Monad m => [m a] -> m [a]` | combinator | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) | 129 sequenceM |
| `Monad m => (a -> m b) -> [a] -> m [b]` | combinator | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) | 130 mapM' |
| `Monad m => (a -> m b) -> BT a -> m (BT b)` | combinator | [A03](../archetypes/A03-generic-monad.md) | [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md) | 109 mapMTree |
| `Monad m => m a -> (a -> m a) -> Int -> m [a]` | combinator | [A03](../archetypes/A03-generic-monad.md) | [A03-generic-monad](../archetypes/A03-generic-monad.md) | **142 applyNTimes — Mock Q2** |
| `Monad m => Int -> m a -> m [a]` | combinator | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) | replicateM |
| `Monad m => (a -> Bool) -> [a] -> m [a]` (filterM-like) | combinator | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) | (filterM variant) |
| `Monad m => (b -> a -> m b) -> b -> [a] -> m b` | combinator | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) | foldM-shape |
| `Monad m => Bool -> m () -> m ()` | combinator | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) | when/unless |
| `Applicative f => (a -> b -> c) -> f a -> f b -> f c` | combinator | [A24](../archetypes/A24-applicative-instance.md) | [applicative](../typeclasses/applicative.md) | 127 liftA2' |
| `Applicative f => [f a] -> f [a]` | combinator | [A24](../archetypes/A24-applicative-instance.md) | [applicative](../typeclasses/applicative.md) | sequenceA |
| `Applicative f => (a -> f b) -> [a] -> f [b]` | combinator | [A24](../archetypes/A24-applicative-instance.md) | [applicative](../typeclasses/applicative.md) | traverse-shape |

## Group 6 — `Ord a =>` (ordering / sorting / BST)

| Sig pattern | Likely family | Archetypes | Canonical file | Note |
|---|---|---|---|---|
| `Ord a => [a] -> [a]` | list-rewrite / bst | [A09](../archetypes/A09-prelude-reimpl.md) / [A11](../archetypes/A11-bst-ops.md) | [bst](../trees/bst.md) | msort / qsort / bstSort |
| `Ord a => [a] -> [a] -> [a]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | merge |
| `Ord a => BT a -> Bool` | tree-validation | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | isBST |
| `Ord a => a -> BT a -> BT a` | bst-ops | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | insert / delete |
| `Ord a => a -> BT a -> Bool` | bst-ops | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | member |
| `Ord a => [a] -> BT a` | bst-ops | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | fromList |
| `Ord a => BT a -> Maybe a` | tree-extract | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) | maxBT, minBT |
| `Ord a => [a] -> [(a, Int)]` | list-rewrite | (state) | [state-counter-family](../question-families/state-counter-family.md) | 120 countOccurrences |

## Group 7 — `m -> m -> m` and `m -> m` (Monoid / Semigroup patterns)

| Sig pattern | Likely family | Archetypes | Canonical file | Note |
|---|---|---|---|---|
| `Monoid m => [m] -> m` | typeclass | [A22](../archetypes/A22-typeclass-instance.md) | [monoid](../typeclasses/monoid.md) | mconcat |
| `m -> m -> m` (with `Monoid m`) | typeclass | [A22](../archetypes/A22-typeclass-instance.md) | [monoid](../typeclasses/monoid.md) | `<>` |
| `Monoid w => Writer w a` | writer | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | tell-based |
| `Sum Int` / `Product Int` | writer | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | numeric monoid wrapper |
| `Monoid m => (a -> m) -> [a] -> m` | typeclass | [A22](../archetypes/A22-typeclass-instance.md) | [foldable](../typeclasses/foldable.md) | foldMap |

## Group 8 — `f a -> f b` (Functor patterns)

| Sig pattern | Likely family | Archetypes | Canonical file | Note |
|---|---|---|---|---|
| `Functor f => (a -> b) -> f a -> f b` | functor | [A06](../archetypes/A06-functor-instance.md) | [functor](../typeclasses/functor.md) | fmap signature |
| `(a -> b) -> Maybe a -> Maybe b` | functor | [A06](../archetypes/A06-functor-instance.md) | [functor](../typeclasses/functor.md) | 121 Functor MyMaybe |
| `(a -> b) -> [a] -> [b]` | functor | [A06](../archetypes/A06-functor-instance.md) / [A09](../archetypes/A09-prelude-reimpl.md) | [functor](../typeclasses/functor.md) | 122 Functor MyList |
| `(a -> b) -> BT a -> BT b` | functor / transform | [A06](../archetypes/A06-functor-instance.md) / [A01](../archetypes/A01-tree-recursion.md) | [tree-functor](../trees/tree-functor.md) | 77 mapBT, 125 Functor BT |
| `(a -> b) -> Rose a -> Rose b` | functor | [A06](../archetypes/A06-functor-instance.md) | [tree-functor](../trees/tree-functor.md) | 126 Functor Rose |
| `(a -> b) -> Identity a -> Identity b` | functor | [A06](../archetypes/A06-functor-instance.md) | [functor](../typeclasses/functor.md) | 123 Functor Identity |
| `(a -> b) -> Reader r a -> Reader r b` | functor | [A06](../archetypes/A06-functor-instance.md) | [reader](../monads/reader.md) | 124 Functor (Reader r) |
| `(a -> b) -> Either e a -> Either e b` | functor | [A06](../archetypes/A06-functor-instance.md) | [either](../monads/either.md) | right-biased |

## Group 9 — Applicative `f (a -> b) -> f a -> f b`

| Sig pattern | Likely family | Archetypes | Canonical file | Note |
|---|---|---|---|---|
| `Applicative f => a -> f a` | applicative | [A24](../archetypes/A24-applicative-instance.md) | [applicative](../typeclasses/applicative.md) | `pure` |
| `Applicative f => f (a -> b) -> f a -> f b` | applicative | [A24](../archetypes/A24-applicative-instance.md) | [applicative](../typeclasses/applicative.md) | `<*>` |
| `Maybe (a -> b) -> Maybe a -> Maybe b` | applicative | [A24](../archetypes/A24-applicative-instance.md) | [applicative](../typeclasses/applicative.md) | 121 Applicative MyMaybe |
| `[a -> b] -> [a] -> [b]` | applicative | [A24](../archetypes/A24-applicative-instance.md) | [applicative](../typeclasses/applicative.md) | 122 Applicative MyList |
| `Parser (a -> b) -> Parser a -> Parser b` | applicative | [A24](../archetypes/A24-applicative-instance.md) / [A16](../archetypes/A16-parser-combinators.md) | [A24-applicative-instance](../archetypes/A24-applicative-instance.md) | 138 Parser machinery |
| `Reader r (a -> b) -> Reader r a -> Reader r b` | applicative | [A24](../archetypes/A24-applicative-instance.md) | [reader](../monads/reader.md) | 124 Applicative (Reader r) |

## Group 10 — Monad `m a -> (a -> m b) -> m b`

| Sig pattern | Likely family | Archetypes | Canonical file | Note |
|---|---|---|---|---|
| `Monad m => a -> m a` | monad | [A06](../archetypes/A06-functor-instance.md) | [monad](../typeclasses/monad.md) | `return` / `pure` |
| `Monad m => m a -> (a -> m b) -> m b` | monad | [A06](../archetypes/A06-functor-instance.md) | [monad](../typeclasses/monad.md) | `>>=` |
| `Maybe a -> (a -> Maybe b) -> Maybe b` | monad | [A06](../archetypes/A06-functor-instance.md) | [maybe](../monads/maybe.md) | 121 Monad MyMaybe |
| `[a] -> (a -> [b]) -> [b]` | monad | [A06](../archetypes/A06-functor-instance.md) | [list-monad](../monads/list-monad.md) | 122 Monad MyList |
| `Identity a -> (a -> Identity b) -> Identity b` | monad | [A06](../archetypes/A06-functor-instance.md) | [monad](../typeclasses/monad.md) | 123 Monad Identity |
| `Reader r a -> (a -> Reader r b) -> Reader r b` | monad | [A06](../archetypes/A06-functor-instance.md) | [reader](../monads/reader.md) | 124 Monad (Reader r) |

## Group 11 — `Expr -> r` (interpreter shapes)

| Sig pattern | Likely family | Archetypes | Canonical file | Note |
|---|---|---|---|---|
| `Expr -> Int` | env-eval (pure) | [A08](../archetypes/A08-env-eval.md) | [simple-arith](../interpreters/simple-arith.md) | 89 evalExpr |
| `Expr -> Maybe Int` | env-eval (partial) | [A08](../archetypes/A08-env-eval.md) | [expr-maybe](../interpreters/expr-maybe.md) | div / lookup may fail |
| `Expr -> Either String Int` | env-eval (error) | [A08](../archetypes/A08-env-eval.md) / [A14](../archetypes/A14-multi-effect-interp.md) | [expr-either](../interpreters/expr-either.md) | error with message |
| `MonadError String m => Expr -> m Int` | interp-error | [A14](../archetypes/A14-multi-effect-interp.md) | [expr-state-either](../interpreters/expr-state-either.md) | calculator with errors |
| `Env -> Expr -> Maybe Int` | env-eval | [A08](../archetypes/A08-env-eval.md) | [A08-env-eval](../archetypes/A08-env-eval.md) | 148 evalWithEnv |
| `Env -> Expr -> Int` | env-eval (pure) | [A08](../archetypes/A08-env-eval.md) | [expr-reader](../interpreters/expr-reader.md) | Reader-style |
| `Reader Env Int` | env-eval | [A08](../archetypes/A08-env-eval.md) | [expr-reader](../interpreters/expr-reader.md) | Reader monad form |
| `Expr -> Expr` | adt-rewrite | [A05](../archetypes/A05-adt-translation.md) | [adt-translation-family](../question-families/adt-translation-family.md) | normalize/simplify |
| `Expr -> Circuit` | adt-translation | [A05](../archetypes/A05-adt-translation.md) | [A05-adt-translation](../archetypes/A05-adt-translation.md) | 145 circuit (Mock Q5) |
| `Expr -> Logic` (variant) | adt-translation | [A05](../archetypes/A05-adt-translation.md) | [A05-adt-translation](../archetypes/A05-adt-translation.md) | simplify chain |
| `Storage -> Expr -> Integer` | imperative-eval | [A19](../archetypes/A19-extend-interpreter.md) | [imperative-eval](../interpreters/imperative-eval.md) | course interpreter |
| `Program -> Storage -> Storage` | imperative-eval | [A19](../archetypes/A19-extend-interpreter.md) | [imperative-eval](../interpreters/imperative-eval.md) | course interpreter run |

## Group 12 — `[[a]] -> ...` (matrix patterns)

| Sig pattern | Likely family | Archetypes | Canonical file | Note |
|---|---|---|---|---|
| `[[Int]] -> Bool` | matrix-predicate | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | 141 isMagicSquare |
| `[[a]] -> [[a]]` | matrix | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | transpose / rotate |
| `[[a]] -> [a]` | matrix | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | flatten matrix |
| `[[Maybe Player]] -> Maybe Player` | matrix / game | [A04](../archetypes/A04-matrix-predicate.md) / [A23](../archetypes/A23-mini-game.md) | [A23-mini-game](../archetypes/A23-mini-game.md) | 150 TTT winner |
| `Int -> [[Player]]` | grid-gen | [A21](../archetypes/A21-list-comp-synthesis.md) / [A23](../archetypes/A23-mini-game.md) | [A23-mini-game](../archetypes/A23-mini-game.md) | empty grid generation |

## Group 13 — `State s a` shapes

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `State s a` (general) | state | [A02](../archetypes/A02-state-game.md) | [state](../monads/state.md) | many |
| `State Int Int` | state-counter | [A02](../archetypes/A02-state-game.md) | [state-counter-family](../question-families/state-counter-family.md) | 111 fresh |
| `BT a -> BT (Int, a)` | state-counter | [A02](../archetypes/A02-state-game.md) | [tree-x-state](../cross-matrix/tree-x-state.md) | 112 labelTree |
| `BT a -> State Int ()` | state-counter | [A02](../archetypes/A02-state-game.md) | [tree-x-state](../cross-matrix/tree-x-state.md) | 113 countLeaves |
| `[a] -> State [a] ()` | state-game | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | 114 pushAll |
| `[Double] -> Double` (via State) | state-counter | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | 115 average |
| `Int -> State Int Int` | state-game | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | 116 rollUntil |
| `Int -> State (Int,Int) ()` | state-game | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | 117 fibState |
| `[CalcCmd] -> State [Int] ()` | state-game | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | 118 evalCalc |
| `[String] -> State Int [(String,Int)]` | state-counter | [A02](../archetypes/A02-state-game.md) | [state-counter-family](../question-families/state-counter-family.md) | 119 uniqueIds |
| `Ord a => [a] -> [(a,Int)]` (via State) | state-counter | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | 120 countOccurrences |
| `NimGame Bool` (Mock) | state-game | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | 144 gameOver |
| `Int -> Heap -> NimGame ()` (Mock) | state-game | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | 144 takeTokens |
| `[Action s] -> State s ()` | scheduler | [A14](../archetypes/A14-multi-effect-interp.md) | [multi-effect](../monads/multi-effect.md) | 149 roundRobin |

## Group 14 — `Writer w a` shapes

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `Writer [String] a` | writer-trace | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | 107 logFactorial |
| `Writer (Sum Int) a` | writer-trace | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | 108 countSteps |
| `Int -> Writer [String] Int` | writer-trace | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | 107 logFactorial |
| `Int -> Writer (Sum Int) Int` | writer-trace | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | 108 countSteps |
| `BT a -> Writer [String] ()` | tree×writer | [A15](../archetypes/A15-writer-trace.md) | [tree-x-writer](../cross-matrix/tree-x-writer.md) | log every node |

## Group 15 — `Either e a` shapes

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `Either String a` | error-handling | [A09](../archetypes/A09-prelude-reimpl.md) / [A14](../archetypes/A14-multi-effect-interp.md) | [either](../monads/either.md) | basic error |
| `[a] -> [b] -> Either String [(a,b)]` | error-handling | [A09](../archetypes/A09-prelude-reimpl.md) | [either](../monads/either.md) | 99 zipEither |
| `MonadError e m => Expr -> m Int` | interp-error | [A14](../archetypes/A14-multi-effect-interp.md) | [expr-state-either](../interpreters/expr-state-either.md) | generic eval |

## Group 16 — `Maybe a` shapes

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `[a] -> Maybe a` | error-handling | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) | 91 safeHead |
| `Int -> Int -> Maybe Int` | error-handling | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) | 92 safeDiv |
| `Double -> Maybe Double` | error-handling | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) | 93 safeSqrt |
| `[a] -> Int -> Maybe a` | error-handling | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) | 94 safeIndex |
| `Int -> [Int] -> Maybe Int` | error-handling | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) | 95 chainDivisions |
| `[Maybe a] -> Maybe a` | error-handling | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) | 96 firstJust |
| `[Maybe a] -> [a]` | error-handling | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) | 97 catMaybes' |
| `(a -> Maybe b) -> [a] -> [b]` | error-handling | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) | 98 mapMaybe' |
| `Char -> Maybe Int` | parse | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) | 100 parseDigit |
| `String -> Maybe Int` | parse | [A09](../archetypes/A09-prelude-reimpl.md) / [A16](../archetypes/A16-parser-combinators.md) | [maybe](../monads/maybe.md) | 100 parseNumber |

## Group 17 — `Char` / `String` patterns

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `String -> String` | codec | [A09](../archetypes/A09-prelude-reimpl.md) / [A07](../archetypes/A07-codec-pair.md) | [codec-family](../question-families/codec-family.md) | 51 toUpper', 54 reverseWords |
| `String -> Int` | list-summary | [A09](../archetypes/A09-prelude-reimpl.md) / [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | 53 countVowels |
| `String -> Bool` | predicate | [A09](../archetypes/A09-prelude-reimpl.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | 55 isPalindrome |
| `String -> [(Char, Int)]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | 56 letterFreqs |
| `Char -> Bool` | char-predicate | (rewrite) | [codec-family](../question-families/codec-family.md) | 52 isVowel |
| `Char -> Char` | char-transform | [A09](../archetypes/A09-prelude-reimpl.md) | [codec-family](../question-families/codec-family.md) | 57 shift |
| `Int -> Char -> Char` | codec | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) | 57 shift |
| `Int -> String -> String` | codec | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) | 58 encode, 59 caesarDecode |
| `String -> String` (crack) | codec | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) | 60 crack |

## Group 18 — IO patterns

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `IO ()` | io | [A03](../archetypes/A03-generic-monad.md) | [io](../monads/io.md) | 101 greet, 102 sumInput, 103 echoUntilQuit |
| `IO [Int]` | io | [A03](../archetypes/A03-generic-monad.md) | [io](../monads/io.md) | 110 threeNumbers |
| `Show a => [a] -> IO ()` | io | [A03](../archetypes/A03-generic-monad.md) | [io](../monads/io.md) | 104 printList |

## Group 19 — Lazy / Infinite patterns

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `[Int]` (infinite) | lazy | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | 131 ones |
| `[Integer]` (infinite) | lazy | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | 132 fibs |
| `[Int]` (primes) | lazy | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | 133 primes |
| `Nat -> Nat -> Nat` | lazy-nat | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | 134 addNat |
| `[a] -> Nat` | lazy-nat | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | 135 lengthNat |
| `Int -> Nat` | lazy-nat | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | 135 toNat |
| `Int -> Integer` (memo) | lazy-memo | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | 136 memoFib |
| `(a -> a) -> a` (fix) | lazy | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | 137 fix' |
| `(a -> a) -> a -> [a]` (iterate) | lazy | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | 48 iterate' |

## Group 20 — Parser patterns

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `newtype Parser a` | parser | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | 138 Parser type |
| `Parser a -> String -> [(a, String)]` | parser | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | 138 parse |
| `Parser Char` | parser | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | 138 item, digitP |
| `(Char -> Bool) -> Parser Char` | parser | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | 138 sat |
| `Parser Int` | parser | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | 139 parseNat, 140 parseExpr |

## Group 21 — Typeclass instance shapes (Group skeletons)

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `instance Functor T where fmap = …` | typeclass | [A06](../archetypes/A06-functor-instance.md) | [functor](../typeclasses/functor.md) | 70, 121, 122, 123, 124, 125, 126 |
| `instance Applicative T where pure = …; (<*>) = …` | typeclass | [A24](../archetypes/A24-applicative-instance.md) | [applicative](../typeclasses/applicative.md) | 121, 122, 123, 124 |
| `instance Monad T where (>>=) = …` | typeclass | [A06](../archetypes/A06-functor-instance.md) | [monad](../typeclasses/monad.md) | 121, 122, 123, 124 |
| `instance Eq T where (==) = …` | typeclass | [A22](../archetypes/A22-typeclass-instance.md) | [eq-ord](../typeclasses/eq-ord.md) | (custom) |
| `instance Ord T where compare = …` | typeclass | [A22](../archetypes/A22-typeclass-instance.md) | [eq-ord](../typeclasses/eq-ord.md) | (custom) |
| `instance Show T where show = …` | typeclass | [A13](../archetypes/A13-pretty-printer.md) | [A13-pretty-printer](../archetypes/A13-pretty-printer.md) | 64 Show Color |
| `instance Num T where (+) (*) … fromInteger = …` | typeclass | [A22](../archetypes/A22-typeclass-instance.md) | [num](../typeclasses/num.md) | (rare) |
| `instance Monoid T where mempty = … mappend = …` | typeclass | [A22](../archetypes/A22-typeclass-instance.md) | [monoid](../typeclasses/monoid.md) | (rare) |
| `class MyEq a where (===) :: a -> a -> Bool` | typeclass | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | 69 MyEq class + instances |
| `Shape -> Double` | (data-rewrite) | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | 61 area |
| `WeekDay -> Bool` / `WeekDay -> Int` | (enum) | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | 62 isWeekend / daysUntilWeekend |
| `Direction -> Direction` | (enum) | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | 63 opposite / turnRight |
| `Vec3 -> Vec3 -> Vec3` | (data) | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | 65 addV, scaleV |
| `Stack a -> Maybe (a, Stack a)` | data | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | 66 pop / peek |
| `Queue a -> Maybe (a, Queue a)` | data | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | 67 dequeue |
| `Ord a => a -> Set a -> Set a` | data | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | 68 insertS |

## Group 22 — Polymorphic basic shapes

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `a -> a` (id) | polymorphism | [A09](../archetypes/A09-prelude-reimpl.md) | [COURSE-MAP](../meta/COURSE-MAP.md) | (intro) |
| `a -> b -> a` (const) | polymorphism | [A09](../archetypes/A09-prelude-reimpl.md) | [COURSE-MAP](../meta/COURSE-MAP.md) | (intro) |
| `(a, b) -> (b, a)` | polymorphism | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 7 swap |
| `(a, b, c) -> a` | polymorphism | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 8 fst3 |
| `(a -> a) -> a -> a` | higher-order | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 9 applyTwice |
| `(a -> b -> c) -> b -> a -> c` | higher-order | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 10 flip' |
| `(b -> c) -> (a -> b) -> a -> c` (.) | higher-order | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) | composition |

## Group 23 — Codec / Pair patterns

| Sig pattern | Likely family | Archetypes | Canonical file | Example problems |
|---|---|---|---|---|
| `(a -> b, b -> a)` pair | codec | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) | encode/decode pair |
| `Eq a => [a] -> [(a, Int)]` | codec | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) | 147 rle |
| `[(a, Int)] -> [a]` | codec | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) | 147 rld |
| `Table -> Tree` | adt-translation | [A12](../archetypes/A12-rep-conversion.md) | [A12-rep-conversion](../archetypes/A12-rep-conversion.md) | 146 ramify |
| `Tree -> Table` | adt-translation | [A12](../archetypes/A12-rep-conversion.md) | [A12-rep-conversion](../archetypes/A12-rep-conversion.md) | 146 tabulate |

## Group 24 — Mock-specific signatures (Q1–Q5)

| Q | Sig | Archetype | File |
|---|---|---|---|
| **Q1** | `Int -> Rose a -> Bool` (isNBranching) | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) |
| **Q1** | `Int -> Rose a -> Rose a` (prune) | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) |
| **Q2** | `Monad m => m a -> (a -> m a) -> Int -> m [a]` (applyNTimes) | [A03](../archetypes/A03-generic-monad.md) | [A03-generic-monad](../archetypes/A03-generic-monad.md) |
| **Q3** | `NimGame Bool` (gameOver) | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) |
| **Q3** | `Int -> Heap -> NimGame ()` (takeTokens) | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) |
| **Q4** | `[[Int]] -> Bool` (isMagicSquare) | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) |
| **Q5** | `Expr -> Circuit` (circuit) | [A05](../archetypes/A05-adt-translation.md) | [A05-adt-translation](../archetypes/A05-adt-translation.md) |

## Group 25 — Assignment-specific signatures

| Asn | Sig | Archetype | File |
|---|---|---|---|
| **A1** | `GridWithAPointer` ops (move L/R/U/D) | [A17](../archetypes/A17-zipper.md) | [A17-zipper](../archetypes/A17-zipper.md) |
| **A1** | `Color -> String` (hex Show) | [A13](../archetypes/A13-pretty-printer.md) | [A13-pretty-printer](../archetypes/A13-pretty-printer.md) |
| **A2** | `Table -> Tree` (ramify) | [A12](../archetypes/A12-rep-conversion.md) / [A20](../archetypes/A20-laws-iso.md) | [A12-rep-conversion](../archetypes/A12-rep-conversion.md) |
| **A2** | `Tree -> Table` (tabulate) | [A12](../archetypes/A12-rep-conversion.md) / [A20](../archetypes/A20-laws-iso.md) | [A12-rep-conversion](../archetypes/A12-rep-conversion.md) |
| **A3** | `Free [] a -> Rose a` (toRose) | [A20](../archetypes/A20-laws-iso.md) | [A20-laws-iso](../archetypes/A20-laws-iso.md) |
| **A3** | `Rose a -> Free [] a` (fromRose) | [A20](../archetypes/A20-laws-iso.md) | [A20-laws-iso](../archetypes/A20-laws-iso.md) |
| **A3** | `[Free (FSum (State s) Yield) ()] -> State s ()` (roundRobin) | [A14](../archetypes/A14-multi-effect-interp.md) | [multi-effect](../monads/multi-effect.md) |
| **A3** | `[SleepState s ()] -> State s ()` (schedule) | [A14](../archetypes/A14-multi-effect-interp.md) | [multi-effect](../monads/multi-effect.md) |

---

## Recognition heuristics

When the sig contains:

1. **`m` with `Monad m =>` constraint** — A03 generic combinator. The body should use only `pure`/`return` and `>>=`.
2. **`Ord a =>`** — almost certainly sorting / BST / member.
3. **A custom data type `T`** in the result position — could be A05 (translation), A06 (Functor), or A01 (recursion).
4. **A custom data type `T`** as the only argument, returning `Int`/`Bool`/`[a]` — A01 structural recursion.
5. **`[[Int]]` or `[[a]]`** in argument — A04 matrix predicate (transpose).
6. **`State`, `Writer`, `Reader`** named — direct monad use, A02/A15/A06.
7. **`Either e` or `MonadError e m`** — A14 multi-effect or A09 error handling.
8. **`Free f`** — A14 multi-effect / Assignment 3.
9. **`(a -> Bool)` or `(a -> a)` parameter** — higher-order, often A09 with the *hidden-predicate* mutation.
10. **`Char` / `String`** — A07 codec or A21 list-comprehension over chars.

---

## See also
- [IF-YOU-SEE-X](../indexes/IF-YOU-SEE-X.md) — by English phrase.
- [PROBLEM-NUMBER-INDEX](../indexes/PROBLEM-NUMBER-INDEX.md) — by problem number.
- [PRELUDE-INDEX](../indexes/PRELUDE-INDEX.md) — Prelude function reference.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
