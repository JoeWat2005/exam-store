<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: lists**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · **lists** · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: lists

**Search keywords:** list, [], singleton, duplicates, head, tail, last, init, length, reverse, map, filter, foldr, foldl, take, drop, zip, !!, sort, nub, !!, empty list, off-by-one

## What the marker generates

For unconstrained `[Int]` / `[a]`, the default `Arbitrary` instance produces:
- Frequently `[]` (~5% of generated inputs) — yes, really.
- Short lists 0-10 elements most of the time.
- Occasional longer lists (size knob can scale to 100+).
- Elements drawn from a small `Int` range (usually `-99..99`).
- May contain duplicates.
- Order is uniform random — NOT sorted.

In the assignments and mock, custom generators are used for specific list shapes:
```haskell
arbitraryWord = listOf1 arbitraryChar      -- guarantees non-empty
listOf gen                                  -- can be []
vectorOf n gen                              -- exactly n
chooseInt (0, 35)                           -- bounded numeric ranges
```

`listOf1` is **non-empty by construction**, so the marker is NOT testing the empty case in those scenarios — but you should still write your function to handle `[]`.

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | Empty list | `[]` | `head []`, `last []`, `(_:_) -> ...` non-exhaustive → exception, marker logs counterexample `[]` | Add `f [] = ...` as the first clause |
| 2 | Singleton | `[x]` | Off-by-one when your "recursive" case fires on length 1 and assumes there's a tail (`x:y:rest`) | First clause `f [x] = ...`, or recurse correctly through `f (x:xs) = ... f xs` |
| 3 | Two-element list | `[x, y]` | "compare adjacent" predicates like `isSorted` need at least 2; the recursive case needs to fire here | Same — pattern `(x:y:rest)` for adjacent-element predicates |
| 4 | Duplicates | `[1, 1, 1]` | `nub`-style assumptions; "unique" properties wrongly assume distinct elements | If spec says "ignore duplicates", do `nub` once at start, not in recursion |
| 5 | Sorted ascending | `[1, 2, 3, 4, 5]` | Bug where you accidentally call `sort` twice (idempotent so hidden) | Test on an unsorted shuffle |
| 6 | Reverse-sorted | `[5, 4, 3, 2, 1]` | Bug where you depend on Ord direction; `head xs` may not be the minimum | Use `minimum` / `maximum` explicitly |
| 7 | All same | `[7, 7, 7, 7]` | Bug in `head` vs `maximum` comparison; off-by-one in "unique" count | Test mentally |
| 8 | Negative ints | `[-3, -1, -7]` | Code paths assuming `> 0`; `length` is `Int`, not `Word`; `(< 0) ==> ...` | `abs` when needed; never assume positivity |
| 9 | Mix of pos/neg/zero | `[-3, 0, 5]` | `signum` confusion; division by zero from sum | Handle 0 separately if your code divides |
| 10 | Long list | `[1..1000]` | Stack overflow from `foldr` on non-strict accumulator | Use `foldl'` from `Data.List` if accumulating numerically. For `Bool` `&&`/`\|\|`, `foldr` is fine because of short-circuit. |
| 11 | List of lists | `[[1,2], [], [3]]` | Inner `[]` not handled; `concat`/`length . concat` distinguishes |  Always handle inner `[]` with an `f [] = ...` clause OR use library `concat`/`map` |
| 12 | List of strings with `""` | `["abc", "", "def"]` | `head ""` crashes; "first character" assumptions | Filter `not . null` or pattern-match the empty string |
| 13 | `[Char]` aka `String` | `"hello"` | Same as 1-12 but you forgot strings are lists | All list attacks apply |

## Property templates

```haskell
import Test.QuickCheck

-- Test that your reverse function is involutive
prop_revInvolutive :: [Int] -> Bool
prop_revInvolutive xs = myReverse (myReverse xs) == xs

-- Test that length is non-negative and 0 for []
prop_lengthBase :: Bool
prop_lengthBase = myLength ([] :: [Int]) == 0

-- Test length equivalence to Prelude
prop_lengthAgree :: [Int] -> Bool
prop_lengthAgree xs = myLength xs == length xs

-- Test sort idempotence
prop_sortIdempotent :: [Int] -> Bool
prop_sortIdempotent xs = mySort (mySort xs) == mySort xs

-- Test sort preserves elements
prop_sortPerm :: [Int] -> Property
prop_sortPerm xs = mySort xs === sort xs   -- Data.List.sort

-- Test take/drop split
prop_takeDrop :: Int -> [Int] -> Bool
prop_takeDrop n xs = myTake n xs ++ myDrop n xs == xs

-- Test filter idempotence
prop_filterIdempotent :: (Int -> Bool) -> [Int] -> Property
prop_filterIdempotent p xs = myFilter p (myFilter p xs) === myFilter p xs

-- Test that map preserves length
prop_mapLength :: (Int -> Int) -> [Int] -> Bool
prop_mapLength f xs = length (myMap f xs) == length xs

-- Test that zip respects min length
prop_zipMinLen :: [Int] -> [Char] -> Bool
prop_zipMinLen xs ys = length (myZip xs ys) == min (length xs) (length ys)

-- Edge case batteries
prop_baseEmpty_id :: Bool                      -- replace `myFoo` with your fn
prop_baseEmpty_id = myFoo ([] :: [Int]) == []

prop_baseSingleton :: Int -> Bool
prop_baseSingleton x = myFoo [x] == [x]        -- or [f x] depending on spec
```

## Self-test before submission checklist

- [ ] handles `[]` (returns the correct value, not exception)
- [ ] handles single-element `[x]` (no off-by-one)
- [ ] handles `[x, y]` (two-element — the boundary of "any adjacent pair" predicates)
- [ ] handles a list with duplicates `[1, 1, 2]`
- [ ] handles a sorted list `[1, 2, 3]`
- [ ] handles a reverse-sorted list `[3, 2, 1]`
- [ ] handles negative ints if the type is `Int`
- [ ] handles `0` element
- [ ] handles a 100+ element list (no stack overflow)
- [ ] does NOT use `head`/`tail`/`!!` without first ruling out `[]`
- [ ] uses `Data.List` library functions only if imported; otherwise hand-rolled

## Pitfalls that specifically lose QC marks

### Pitfall: `head` on possibly-empty list
```haskell
-- WRONG: crashes on []
maxOfList xs = head (sort xs)
-- Counterexample QC reports: []
-- Fix:
maxOfList []     = error "empty"   -- or Nothing if returning Maybe
maxOfList (x:xs) = foldr max x xs
```

### Pitfall: `myTake` doesn't handle `n <= 0`
```haskell
-- WRONG:
myTake n (x:xs) = x : myTake (n-1) xs
myTake _ []     = []
-- QC tries n = -5 and finds infinite recursion → timeout
-- Fix:
myTake n _ | n <= 0 = []
myTake _ []         = []
myTake n (x:xs)     = x : myTake (n-1) xs
```

### Pitfall: assuming sorted but the spec didn't say so
```haskell
-- WRONG: only works for sorted input
myInsertUnique x [] = [x]
myInsertUnique x (y:ys) | x == y = y:ys
                       | x < y  = x : y : ys
                       | otherwise = y : myInsertUnique x ys
-- For input [3, 1, 2], inserting 0 misses placement
-- Fix: read spec — is input sorted? if not, just sort first or do linear scan
```

### Pitfall: `foldl` vs `foldr` direction
```haskell
-- WRONG direction (reverses):
myReverse = foldl (flip (:)) []   -- actually this IS reverse, but
mySum = foldl (-) 0 [1, 2, 3]     -- = -6, not 6 — subtraction is left-assoc
-- For commutative ops (sum, product, max, min), direction does not matter.
-- For non-commutative ops, direction MATTERS.
```

### Pitfall: forgot `nub` is `O(n^2)` but the marker doesn't care
QC doesn't time you out at 10ms — performance is rarely the issue. Correctness is.

### Pitfall: `zip` truncates silently
```haskell
-- If you need to detect mismatched lengths, `zip` won't help:
zip [1,2,3] [10, 20] == [(1,10), (2,20)]   -- silently drops 3
-- Detect with: `length xs == length ys`
```

### Pitfall: `!!` is partial AND O(n)
```haskell
-- WRONG: crashes on n out of range; also slow for big indices
xs !! n
-- Use pattern match or `drop n xs` then `head`
```

### Pitfall: `null` for short lists is fine, but `length xs == 0` is bad on infinite lists
```haskell
-- Use: null xs
-- Not: length xs == 0
```

## See also

**Archetypes:** [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md) · [A21 list comp synthesis](../archetypes/A21-list-comp-synthesis.md)
**Question families:** [list-rewrite](../question-families/list-rewrite-family.md) · [list-fold](../question-families/list-fold-family.md) · [list-comp](../question-families/list-comp-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
