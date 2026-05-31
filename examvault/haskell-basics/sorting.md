<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Sorting algorithms**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · **sorting**
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->





# Sorting algorithms

**Search keywords:** sort · insertion sort · selection sort · bubble sort · quicksort · merge sort · isSorted · ordered · `Ord a => [a] -> [a]`

## What this is
The five hand-rolled comparison sorts. The exam never wants `import Data.List (sort)` — it wants you to **write the recursion yourself** for a `sort :: Ord a => [a] -> [a]` stem. Every one below compiles under `{-# LANGUAGE Safe #-}` with **no imports** (everything used is in `Prelude`).

## Recognition triggers
- "Write a function that sorts a list **without** using `Data.List.sort`."
- The signature is `Ord a => [a] -> [a]` and the spec mentions "ascending" / "ordered" / "in order".
- "Implement *quicksort* / *insertion sort* / *merge sort* in Haskell."
- A QuickCheck spec that says `isSorted (mySort xs)` and "`mySort xs` is a permutation of `xs`".

## Mental model
Each sort is a **different recursion shape** over the same type:

| Sort | One-line idea | Recursion shape | Time |
|---|---|---|---|
| Insertion | insert one element into an already-sorted tail | linear recursion + helper `ins` | O(n²) |
| Selection | pull out the minimum, repeat on the rest | linear recursion + `minimum`/`delete1` | O(n²) |
| Bubble | sweep swapping neighbours, repeat until no swaps | fixpoint of a one-pass function | O(n²) |
| Quick | partition around a pivot, recurse on both sides | tree recursion (divide) | O(n log n) avg |
| Merge | split in half, sort each, merge | tree recursion (divide) + `merge` | O(n log n) |

If you only memorise **two**, memorise **quicksort** (shortest to write) and **merge sort** (the one examiners ask for the `merge` helper of).

## Insertion sort
Insert each element into the sorted result of the rest.
```haskell
insertionSort :: Ord a => [a] -> [a]
insertionSort []     = []
insertionSort (x:xs) = ins x (insertionSort xs)
  where
    ins y []     = [y]
    ins y (z:zs)
      | y <= z    = y : z : zs        -- found the slot
      | otherwise = z : ins y zs      -- keep walking right
```
`ins` is the whole trick: it walks down a **sorted** list and drops `y` in front of the first thing it is `<=`. Stable.

## Selection sort
Repeatedly take the minimum.
```haskell
selectionSort :: Ord a => [a] -> [a]
selectionSort [] = []
selectionSort xs = m : selectionSort (delete1 m xs)
  where
    m = minimum xs
    delete1 _ []     = []
    delete1 y (z:zs)
      | y == z    = zs                -- remove ONE occurrence only
      | otherwise = z : delete1 y zs
```
`delete1` removes a **single** copy of the minimum — removing all copies would lose duplicates.

## Bubble sort
One pass swaps out-of-order neighbours; repeat until a pass changes nothing.
```haskell
bubbleSort :: Ord a => [a] -> [a]
bubbleSort xs
  | xs == xs' = xs                    -- fixpoint: no swaps this pass
  | otherwise = bubbleSort xs'
  where
    xs' = onePass xs
    onePass (a:b:rest)
      | a > b     = b : onePass (a:rest)
      | otherwise = a : onePass (b:rest)
    onePass ys = ys
```
The `xs == xs'` guard needs `Eq a`, which `Ord a` already implies.

## Quicksort
Partition the tail around the head as pivot. The shortest sort to write — two list comprehensions.
```haskell
quickSort :: Ord a => [a] -> [a]
quickSort []     = []
quickSort (p:xs) = quickSort smaller ++ [p] ++ quickSort larger
  where
    smaller = [x | x <- xs, x <  p]
    larger  = [x | x <- xs, x >= p]   -- >= keeps duplicates of the pivot
```
**Watch the partition:** use `< p` and `>= p` (or `<= p` and `> p`). If you write `< p` and `> p`, every element equal to the pivot is **silently dropped** — see [pitfalls](#common-mistakes).

## Merge sort
Split in half, sort the halves, merge them.
```haskell
mergeSort :: Ord a => [a] -> [a]
mergeSort []  = []
mergeSort [x] = [x]                    -- this base case is essential (stops the split)
mergeSort xs  = merge (mergeSort left) (mergeSort right)
  where
    (left, right) = splitAt (length xs `div` 2) xs
    merge [] ys = ys
    merge as [] = as
    merge (a:as) (b:bs)
      | a <= b    = a : merge as (b:bs)
      | otherwise = b : merge (a:as) bs
```
`merge` is the part examiners most often ask for on its own (`merge :: Ord a => [a] -> [a] -> [a]`, "merge two sorted lists"). The `[x]` base case is **not optional** — without it, `mergeSort [x]` splits into `([], [x])` forever.

## Smallest example
```haskell
>>> quickSort [5,3,8,3,1,9,2,7,3]
[1,2,3,3,3,5,7,8,9]
>>> insertionSort "haskell"
"aehklls"
>>> mergeSort ([] :: [Int])
[]
```
All five sorts return the same result; duplicates are preserved.

## QuickCheck properties (how a sort gets auto-marked)
A sort is marked by **properties**, not a fixed output. The marker (and you, before submitting) checks:
```haskell
isSorted :: Ord a => [a] -> Bool
isSorted []       = True
isSorted [_]      = True
isSorted (x:y:zs) = x <= y && isSorted (y:zs)

prop_sorted  xs = isSorted (mySort xs)                 -- output is ordered
prop_perm    xs = mySort xs == sort xs                 -- same elements (sort from Data.List as oracle)
prop_length  xs = length (mySort xs) == length xs      -- nothing dropped/duplicated  <- catches the quicksort >/>= bug
prop_idem    xs = mySort (mySort xs) == mySort xs       -- sorting twice == once
```
`prop_perm` and `prop_length` are the ones that catch a sort that *looks* ordered but loses or invents elements. (`Data.List.sort` is an allowed import to use as the oracle **in a test**, just not as your answer.)

## Common mistakes
- **Quicksort drops pivot-duplicates.** `[x | x <- xs, x > p]` for the right side throws away every element equal to `p`. Use `>= p` on exactly one side. `prop_length` fails loudly if you get this wrong.
- **Merge sort with no `[x]` base case** → non-termination (`splitAt 0` never shrinks a singleton).
- **Selection sort deletes *all* copies of the minimum** (using `filter (/= m)`), losing duplicates. Remove one with `delete1`.
- **Insertion `ins` stops too early** — it must keep recursing (`z : ins y zs`) past every element smaller than `y`, not return after the first.
- **`Ord` vs `Eq`.** All five only need `Ord a` in the signature; do not over-constrain to `(Ord a, Eq a)` — `Ord` already implies `Eq`.
- **Reaching for `Data.Ord (comparing)` / `sortBy`** for a "sort by key" variant — `Data.Ord` is **not** an allowed import. Sort by tagging: `map snd (mySort [(key x, x) | x <- xs])`.

## See also
**Basics:** [recursion](./recursion.md) · [list-comprehensions](./list-comprehensions.md) · [foldr](./foldr.md) · [helper-functions](./helper-functions.md) · [allowed-builtins](./allowed-builtins.md)
**Archetypes:** [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)
**Families:** [list-rewrite-family](../question-families/list-rewrite-family.md) · [list-comp-family](../question-families/list-comp-family.md) · [list-fold-family](../question-families/list-fold-family.md)
**QuickCheck:** [lists-attacks](../quickcheck/lists-attacks.md) · [PROPERTY-PATTERNS](../quickcheck/PROPERTY-PATTERNS.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
