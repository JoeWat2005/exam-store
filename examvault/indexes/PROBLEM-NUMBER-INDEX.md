<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **PROBLEM-NUMBER-INDEX**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · [MASTER-INDEX](./MASTER-INDEX.md) · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · **PROBLEM-NUMBER-INDEX** · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# PROBLEM-NUMBER-INDEX

Problems 1–150 from [Haskell-Practice-Problems](../../fp-learning-2025/Haskell-Practice-Problems.md) mapped to vault.

> Student says "do problem 87" → look up here → know exactly where the template lives.

**Format:** `# · name · signature · topic · archetype · canonical file`

---

## Set 1 — Functions, patterns, guards, polymorphism (Day 1)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 1 | `double` | `Int -> Int` | arithmetic | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 2 | `between` | `Int -> Int -> Int -> Bool` | guards | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 3 | `sign` | `Int -> Int` | guards | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 4 | `maxOfThree` | `Int -> Int -> Int -> Int` | guards | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 5 | `dayName` | `Int -> String` | pattern-match | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 6 | `leapYear` | `Int -> Bool` | guards | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 7 | `swap` | `(a, b) -> (b, a)` | polymorphism | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 8 | `fst3` `snd3` `thd3` | `(a, b, c) -> a` etc. | polymorphism | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 9 | `applyTwice` | `(a -> a) -> a -> a` | higher-order | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 10 | `flip'` | `(a -> b -> c) -> b -> a -> c` | higher-order | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |

## Set 2 — List recursion basics (Day 2)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 11 | `myLength` | `[a] -> Int` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 12 | `mySum` | `Num a => [a] -> a` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 13 | `myProduct` | `Num a => [a] -> a` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 14 | `myReverse` | `[a] -> [a]` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 15 | `fastReverse` | `[a] -> [a]` | accumulator | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 16 | `myElem` | `Eq a => a -> [a] -> Bool` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 17 | `myConcat` | `[[a]] -> [a]` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 18 | `myTake` | `Int -> [a] -> [a]` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 19 | `myDrop` | `Int -> [a] -> [a]` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 20 | `myZip` | `[a] -> [b] -> [(a,b)]` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |

## Set 3 — More list recursion + sorting (Day 3)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 21 | `myReplicate` | `Int -> a -> [a]` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 22 | `myLast` | `[a] -> a` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 23 | `myInit` | `[a] -> [a]` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 24 | `myLookup` | `Eq a => a -> [(a,b)] -> Maybe b` | Maybe | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) |
| 25 | `merge` | `Ord a => [a] -> [a] -> [a]` | sort-merge | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 26 | `msort` | `Ord a => [a] -> [a]` | merge sort | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 27 | `qsort` | `Ord a => [a] -> [a]` | quicksort | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 28 | `isSorted` | `Ord a => [a] -> Bool` | predicate | [A10](../archetypes/A10-fold-reformulation.md) | [list-fold-family](../question-families/list-fold-family.md) |
| 29 | `removeDuplicates` | `Eq a => [a] -> [a]` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 30 | `interleave` | `[a] -> [a] -> [a]` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |

## Set 4 — List comprehensions (Day 4)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 31 | `pyths` | `Int -> [(Int,Int,Int)]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 32 | `factors` | `Int -> [Int]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 33 | `isPrime` | `Int -> Bool` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 34 | `primesUpTo` | `Int -> [Int]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 35 | `perfects` | `Int -> [Int]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 36 | `scalar` | `Num a => [a] -> [a] -> a` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 37 | `positions` | `Eq a => a -> [a] -> [Int]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 38 | `pairs` | `[a] -> [(a,a)]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 39 | `wordCount` | `String -> Int` | string | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 40 | `cartesian` | `[a] -> [b] -> [(a,b)]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |

## Set 5 — Higher-order functions (Day 5)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 41 | `sumWithFoldr` | `Num a => [a] -> a` | fold | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) |
| 42 | `lengthWithFoldr` | `[a] -> Int` | fold | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) |
| 43 | `mapWithFoldr` | `(a -> b) -> [a] -> [b]` | fold | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) |
| 44 | `filterWithFoldr` | `(a -> Bool) -> [a] -> [a]` | fold | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) |
| 45 | `reverseWithFoldl` | `[a] -> [a]` | foldl | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) |
| 46 | `allWithFoldr` | `(a -> Bool) -> [a] -> Bool` | fold | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) |
| 47 | `compose'` | `[a -> a] -> (a -> a)` | fold | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) |
| 48 | `iterate'` | `(a -> a) -> a -> [a]` | lazy / infinite | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) |
| 49 | `takeWhile'` | `(a -> Bool) -> [a] -> [a]` | list-recursion | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| 50 | `partition'` | `(a -> Bool) -> [a] -> ([a],[a])` | list-rewrite | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |

## Set 6 — Strings, chars, Caesar cipher (Day 6)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 51 | `toUpper'` | `String -> String` | string | [A09](../archetypes/A09-prelude-reimpl.md) | [codec-family](../question-families/codec-family.md) |
| 52 | `isVowel` | `Char -> Bool` | char predicate | [A09](../archetypes/A09-prelude-reimpl.md) | [codec-family](../question-families/codec-family.md) |
| 53 | `countVowels` | `String -> Int` | string | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 54 | `reverseWords` | `String -> String` | string | [A09](../archetypes/A09-prelude-reimpl.md) | [codec-family](../question-families/codec-family.md) |
| 55 | `isPalindrome` | `String -> Bool` | string predicate | [A09](../archetypes/A09-prelude-reimpl.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) |
| 56 | `letterFreqs` | `String -> [(Char,Int)]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 57 | `shift` | `Int -> Char -> Char` | char codec | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) |
| 58 | `encode` | `Int -> String -> String` | Caesar | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) |
| 59 | `caesarDecode` | `Int -> String -> String` | Caesar | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) |
| 60 | `crack` | `String -> String` | Caesar break | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) |

## Set 7 — Custom data types & typeclass instances (Day 7)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 61 | `area` (Shape) | `Shape -> Double` | ADT | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) |
| 62 | `isWeekend` / `daysUntilWeekend` (WeekDay) | `WeekDay -> Bool/Int` | enum | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) |
| 63 | `opposite` / `turnRight` (Direction) | `Direction -> Direction` | enum | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) |
| 64 | Custom `Show` for Color | `Color -> String` | Show / pretty | [A13](../archetypes/A13-pretty-printer.md) | [A13-pretty-printer](../archetypes/A13-pretty-printer.md) |
| 65 | Vec3 ops | `Vec3 -> Vec3 -> Vec3` etc. | data | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) |
| 66 | Stack (push/pop/peek) | `Stack a` ops | data | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) |
| 67 | Queue (enqueue/dequeue) | `Queue a` ops | data | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) |
| 68 | Set (insert/member/union) | `Ord a => Set a` ops | data | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) |
| 69 | `MyEq` class | `class MyEq a where (===)` | typeclass | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) |
| 70 | Functor MyMaybe | `(a -> b) -> MyMaybe a -> MyMaybe b` | Functor | [A06](../archetypes/A06-functor-instance.md) | [functor](../typeclasses/functor.md) |

## Set 8 — Binary trees (Day 8)

`data BT a = Empty | Fork a (BT a) (BT a)`

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 71 | `sizeBT` | `BT a -> Int` | tree-counting | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) |
| 72 | `heightBT` | `BT a -> Int` | tree-counting | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) |
| 73 | `leavesBT` | `BT a -> [a]` | tree-extract | [A01](../archetypes/A01-tree-recursion.md) | [tree-extract-family](../question-families/tree-extract-family.md) |
| 74 | `mirror` | `BT a -> BT a` | tree-transform | [A01](../archetypes/A01-tree-recursion.md) | [tree-transform-family](../question-families/tree-transform-family.md) |
| 75 | `flattenInOrder` | `BT a -> [a]` | traversal | [A01](../archetypes/A01-tree-recursion.md) | [tree-traversals](../trees/tree-traversals.md) |
| 76 | `flattenPreOrder` / `flattenPostOrder` | `BT a -> [a]` | traversal | [A01](../archetypes/A01-tree-recursion.md) | [tree-traversals](../trees/tree-traversals.md) |
| 77 | `mapBT` | `(a -> b) -> BT a -> BT b` | functor / transform | [A06](../archetypes/A06-functor-instance.md) / [A01](../archetypes/A01-tree-recursion.md) | [tree-functor](../trees/tree-functor.md) |
| 78 | `sumBT` | `Num a => BT a -> a` | tree-fold | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) |
| 79 | `maxBT` | `Ord a => BT a -> Maybe a` | tree-extract | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) |
| 80 | `countBT` | `Eq a => a -> BT a -> Int` | tree-counting | [A01](../archetypes/A01-tree-recursion.md) | [tree-counting-family](../question-families/tree-counting-family.md) |

## Set 9 — BSTs, Rose trees, expressions (Day 9)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 81 | `isBST` | `Ord a => BT a -> Bool` | bst | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) |
| 82 | `insertBST` | `Ord a => a -> BT a -> BT a` | bst | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) |
| 83 | `memberBST` | `Ord a => a -> BT a -> Bool` | bst | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) |
| 84 | `deleteBST` | `Ord a => a -> BT a -> BT a` | bst | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) |
| 85 | `fromList` (BST) | `Ord a => [a] -> BT a` | bst | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) |
| 86 | `sizeRose` | `Rose a -> Int` | rose | [A01](../archetypes/A01-tree-recursion.md) | [rose-tree](../trees/rose-tree.md) |
| 87 | `heightRose` | `Rose a -> Int` | rose | [A01](../archetypes/A01-tree-recursion.md) | [rose-tree](../trees/rose-tree.md) |
| 88 | `flattenRose` | `Rose a -> [a]` | rose-extract | [A01](../archetypes/A01-tree-recursion.md) | [rose-tree](../trees/rose-tree.md) |
| 89 | `evalExpr` | `Expr -> Int` | interp-arith | [A08](../archetypes/A08-env-eval.md) | [simple-arith](../interpreters/simple-arith.md) |
| 90 | `depthExpr` | `Expr -> Int` | tree-counting | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) |

## Set 10 — Maybe and Either, error-handling (Day 10)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 91 | `safeHead` | `[a] -> Maybe a` | Maybe | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) |
| 92 | `safeDiv` | `Int -> Int -> Maybe Int` | Maybe | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) |
| 93 | `safeSqrt` | `Double -> Maybe Double` | Maybe | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) |
| 94 | `safeIndex` | `[a] -> Int -> Maybe a` | Maybe | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) |
| 95 | `chainDivisions` | `Int -> [Int] -> Maybe Int` | Maybe (do) | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) |
| 96 | `firstJust` | `[Maybe a] -> Maybe a` | Maybe | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) |
| 97 | `catMaybes'` | `[Maybe a] -> [a]` | Maybe | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) |
| 98 | `mapMaybe'` | `(a -> Maybe b) -> [a] -> [b]` | Maybe | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) |
| 99 | `zipEither` | `[a] -> [b] -> Either String [(a,b)]` | Either | [A09](../archetypes/A09-prelude-reimpl.md) | [either](../monads/either.md) |
| 100 | `parseDigit` / `parseNumber` | `Char -> Maybe Int` / `String -> Maybe Int` | parse | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) |

## Set 11 — Monads: IO, List, Writer (Day 11)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 101 | `greet` | `IO ()` | IO | [A03](../archetypes/A03-generic-monad.md) | [io](../monads/io.md) |
| 102 | `sumInput` | `IO ()` | IO | [A03](../archetypes/A03-generic-monad.md) | [io](../monads/io.md) |
| 103 | `echoUntilQuit` | `IO ()` | IO | [A03](../archetypes/A03-generic-monad.md) | [io](../monads/io.md) |
| 104 | `printList` | `Show a => [a] -> IO ()` | IO | [A03](../archetypes/A03-generic-monad.md) | [io](../monads/io.md) |
| 105 | `knightMoves` | `(Int,Int) -> [(Int,Int)]` | list monad | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-monad](../monads/list-monad.md) |
| 106 | `allPairs` | `[a] -> [(a,a)]` | list-comp | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) |
| 107 | `logFactorial` | `Int -> Writer [String] Int` | Writer | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) |
| 108 | `countSteps` | `Int -> Writer (Sum Int) Int` | Writer | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) |
| 109 | `mapMTree` | `Monad m => (a -> m b) -> BT a -> m (BT b)` | monad × tree | [A03](../archetypes/A03-generic-monad.md) | [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md) |
| 110 | `threeNumbers` | `IO [Int]` | IO | [A03](../archetypes/A03-generic-monad.md) | [io](../monads/io.md) |

## Set 12 — State monad (Day 12)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 111 | `fresh` | `State Int Int` | State | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) |
| 112 | `labelTree` | `BT a -> BT (Int, a)` | State × tree | [A02](../archetypes/A02-state-game.md) | [tree-x-state](../cross-matrix/tree-x-state.md) |
| 113 | `countLeaves` | `BT a -> State Int ()` | State × tree | [A02](../archetypes/A02-state-game.md) | [tree-x-state](../cross-matrix/tree-x-state.md) |
| 114 | `pushAll` | `[a] -> State [a] ()` | State | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) |
| 115 | `average` | `[Double] -> Double` (via State) | State | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) |
| 116 | `rollUntil` | `Int -> State Int Int` | State | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) |
| 117 | `fibState` | `Int -> State (Int,Int) ()` | State | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) |
| 118 | `evalCalc` | `[CalcCmd] -> State [Int] ()` | State stack-calc | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) |
| 119 | `uniqueIds` | `[String] -> State Int [(String,Int)]` | State counter | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) |
| 120 | `countOccurrences` | `Ord a => [a] -> [(a,Int)]` | State or fold | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) |

## Set 13 — Functor, Applicative, custom Monad (Day 13)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 121 | Functor/App/Monad MyMaybe | instance bodies | typeclass | [A06](../archetypes/A06-functor-instance.md) | [monad](../typeclasses/monad.md) |
| 122 | Functor/App/Monad MyList | instance bodies | typeclass | [A06](../archetypes/A06-functor-instance.md) | [monad](../typeclasses/monad.md) |
| 123 | Functor/App/Monad Identity | instance bodies | typeclass | [A06](../archetypes/A06-functor-instance.md) | [monad](../typeclasses/monad.md) |
| 124 | Functor/App/Monad Reader | instance bodies | typeclass | [A06](../archetypes/A06-functor-instance.md) | [reader](../monads/reader.md) |
| 125 | Functor BT | `(a -> b) -> BT a -> BT b` | typeclass | [A06](../archetypes/A06-functor-instance.md) | [tree-functor](../trees/tree-functor.md) |
| 126 | Functor Rose | `(a -> b) -> Rose a -> Rose b` | typeclass | [A06](../archetypes/A06-functor-instance.md) | [tree-functor](../trees/tree-functor.md) |
| 127 | `liftA2'` | `Applicative f => (a -> b -> c) -> f a -> f b -> f c` | combinator | [A24](../archetypes/A24-applicative-instance.md) | [applicative](../typeclasses/applicative.md) |
| 128 | `join'` | `Monad m => m (m a) -> m a` | combinator | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) |
| 129 | `sequenceM` | `Monad m => [m a] -> m [a]` | combinator | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) |
| 130 | `mapM'` | `Monad m => (a -> m b) -> [a] -> m [b]` | combinator | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) |

## Set 14 — Laziness, infinite data, parsing (Day 14)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 131 | `ones` | `[Int]` | lazy | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) |
| 132 | `fibs` | `[Integer]` | lazy | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) |
| 133 | `primes` | `[Int]` | lazy sieve | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) |
| 134 | Lazy Nat (`addNat`, `infty`) | `Nat -> Nat -> Nat` | lazy-nat | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) |
| 135 | `lengthNat` / `toNat` | `[a] -> Nat`, `Int -> Nat` | lazy-nat | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) |
| 136 | `memoFib` | `Int -> Integer` | memo | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) |
| 137 | `fix'` | `(a -> a) -> a` | lazy | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) |
| 138 | Parser type, item, sat, digitP | Parser primitives | parser | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) |
| 139 | `parseNat` | `Parser Int` | parser | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) |
| 140 | `parseExpr` | `Parser Int` | parser | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) |

## Set 15 — Mixed exam-style problems (Day 15)

| # | Name | Signature | Topic | Archetype | File |
|---|---|---|---|---|---|
| 141 | `isMagicSquare` (Mock Q4) | `[[Int]] -> Bool` | matrix | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) |
| 142 | `applyNTimes` (Mock Q2) | `Monad m => m a -> (a -> m a) -> Int -> m [a]` | generic monad | [A03](../archetypes/A03-generic-monad.md) | [A03-generic-monad](../archetypes/A03-generic-monad.md) |
| 143 | `isNBranching` / `prune` (Mock Q1) | `Int -> Rose a -> Bool` / `Int -> Rose a -> Rose a` | rose | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) |
| 144 | Nim (`gameOver`, `takeTokens`) (Mock Q3) | `NimGame Bool` / `Int -> Heap -> NimGame ()` | State game | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) |
| 145 | `circuit` (Mock Q5) | `Expr -> Circuit` | ADT translation | [A05](../archetypes/A05-adt-translation.md) | [A05-adt-translation](../archetypes/A05-adt-translation.md) |
| 146 | `ramify` / `tabulate` (A2) | `Table -> Tree` / `Tree -> Table` | rep conversion | [A12](../archetypes/A12-rep-conversion.md) | [A12-rep-conversion](../archetypes/A12-rep-conversion.md) |
| 147 | `rle` / `rld` | `Eq a => [a] -> [(a,Int)]` / inv. | codec | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) |
| 148 | `evalWithEnv` | `Env -> Expr -> Maybe Int` | env eval | [A08](../archetypes/A08-env-eval.md) | [A08-env-eval](../archetypes/A08-env-eval.md) |
| 149 | `roundRobin` | `[Action s] -> State s ()` | scheduler | [A14](../archetypes/A14-multi-effect-interp.md) | [multi-effect](../monads/multi-effect.md) |
| 150 | `winner` (TTT) | `Grid -> Maybe Player` | matrix / game | [A23](../archetypes/A23-mini-game.md) | [A23-mini-game](../archetypes/A23-mini-game.md) |

---

## Bonus: Mock-Test cross-reference

| Mock Q | Problem # | Name | Archetype | Marker quirks |
|---|---|---|---|---|
| Q1 | 143 | isNBranching / prune | [A01](../archetypes/A01-tree-recursion.md) | None significant |
| Q2 | 142 | applyNTimes | [A03](../archetypes/A03-generic-monad.md) | Generator starts at n=2 — off-by-one is silently lenient (8/10 still available) |
| Q3 | 144 | Nim | [A02](../archetypes/A02-state-game.md) | `gameOver` has hardcoded `(0,0)` test worth 4 free marks |
| Q4 | 141 | isMagicSquare | [A04](../archetypes/A04-matrix-predicate.md) | Spec says 1×1 case is True |
| Q5 | 145 | circuit | [A05](../archetypes/A05-adt-translation.md) | Checked **semantically** (boolean equivalence over all assignments), NOT structurally — verbose-but-correct gets full marks |

## See also
- [MOCK-Q-INDEX](../indexes/MOCK-Q-INDEX.md) — Mock Q1–Q5 in depth.
- [TYPE-SIGNATURE-DATABASE](../indexes/TYPE-SIGNATURE-DATABASE.md) — sigs clustered by shape.
- [Haskell-Practice-Problems](../../fp-learning-2025/Haskell-Practice-Problems.md) — the canonical problem source.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
