<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: list-rewrite**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · **list-rewrite** · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: list-rewrite

**Archetype:** A01 (recursion on `[a]` — `[]` vs `x:xs`)   |   **Stars:** ⭐   |   **Course week(s):** 2
**Search keywords:** myLength, mySum, myMap, myFilter, myReverse, myTake, myDrop, myZip, myElem, Prelude reimpl

## Generator template
```haskell
-- The seed: recursion on a list. Empty case yields a *unit* value;
-- cons case combines f(x) with the recursive call.
seed :: [a] -> b
seed []     = unit
seed (x:xs) = combine x (seed xs)
```

Every mutation in this family is "pick a `unit` and a `combine`":
| function   | unit | combine             |
|------------|------|---------------------|
| sum        | 0    | (+) x acc           |
| product    | 1    | (*) x acc           |
| length     | 0    | const (1+) acc      |
| reverse    | []   | acc ++ [x]          |
| map f      | []   | f x : acc           |
| filter p   | []   | if p x then x:acc else acc |
| concat     | []   | x ++ acc            |

This is exactly `foldr combine unit` — see `list-fold-family.md` for the foldr presentation. The exam usually wants the explicit recursion *here*, and the `foldr` rewrite in the *fold* family.

## Mutations (the examiner picks one)

### Mutation 1 — myLength (= problem 11)
**Sig:** `myLength :: [a] -> Int`
**Solution:**
```haskell
myLength :: [a] -> Int
myLength []     = 0
myLength (_:xs) = 1 + myLength xs
```
**QC trap:** Use `_` not `x` — emphasises the polymorphism. `myLength undefined` should error on the spine, not the elements.

### Mutation 2 — mySum (= problem 12)
**Sig:** `mySum :: Num a => [a] -> a`
**Solution:**
```haskell
mySum :: Num a => [a] -> a
mySum []     = 0
mySum (x:xs) = x + mySum xs
```
**QC trap:** Lazy `+` causes a thunk pile-up on long lists. Examiner sometimes asks for a strict-accumulator alternative.

### Mutation 3 — myProduct (= problem 13)
**Sig:** `myProduct :: Num a => [a] -> a`
**Solution:**
```haskell
myProduct :: Num a => [a] -> a
myProduct []     = 1
myProduct (x:xs) = x * myProduct xs
```
**QC trap:** Unit changes to 1. A `0` anywhere short-circuits the value but *not* the recursion (Haskell's `*` is strict in both args).

### Mutation 4 — myReverse (= problem 14)
**Sig:** `myReverse :: [a] -> [a]`
**Solution:**
```haskell
myReverse :: [a] -> [a]
myReverse []     = []
myReverse (x:xs) = myReverse xs ++ [x]
```
**QC trap:** O(n²) because of the `++` at every level. See `fastReverse` (mutation 8 of this family) for the accumulator fix.

### Mutation 5 — myMap (= problem 43 / mapWithFoldr)
**Sig:** `myMap :: (a -> b) -> [a] -> [b]`
**Solution:**
```haskell
myMap :: (a -> b) -> [a] -> [b]
myMap _ []     = []
myMap f (x:xs) = f x : myMap f xs
```
**QC trap:** `myMap id == id`. Always preserves length.

### Mutation 6 — myFilter
**Sig:** `myFilter :: (a -> Bool) -> [a] -> [a]`
**Solution:**
```haskell
myFilter :: (a -> Bool) -> [a] -> [a]
myFilter _ []     = []
myFilter p (x:xs)
  | p x           = x : myFilter p xs
  | otherwise     = myFilter p xs
```
**QC trap:** Result length is `<=` input length. `myFilter (const True) == id`. `myFilter (const False) == const []`.

### Mutation 7 — myTake (= problem 18)
**Sig:** `myTake :: Int -> [a] -> [a]`
**Solution:**
```haskell
myTake :: Int -> [a] -> [a]
myTake n _ | n <= 0  = []
myTake _ []          = []
myTake n (x:xs)      = x : myTake (n-1) xs
```
**QC trap:** Three cases — negative `n`, empty list, normal. Negative must come FIRST or you'll crash on `n` decrement. `length (myTake n xs) == min n (length xs)` is the QC invariant.

### Mutation 8 — myDrop (= problem 19)
**Sig:** `myDrop :: Int -> [a] -> [a]`
**Solution:**
```haskell
myDrop :: Int -> [a] -> [a]
myDrop n xs | n <= 0  = xs
myDrop _ []           = []
myDrop n (_:xs)       = myDrop (n-1) xs
```
**QC trap:** `myTake n xs ++ myDrop n xs == xs` for all `n,xs`.

### Mutation 9 — myZip (= problem 20)
**Sig:** `myZip :: [a] -> [b] -> [(a,b)]`
**Solution:**
```haskell
myZip :: [a] -> [b] -> [(a,b)]
myZip [] _              = []
myZip _ []              = []
myZip (x:xs) (y:ys)     = (x,y) : myZip xs ys
```
**QC trap:** Result length is `min (length xs) (length ys)`. Two `[]` cases — both required, or the catch-all leaks.

### Mutation 10 — myElem (= problem 16)
**Sig:** `myElem :: Eq a => a -> [a] -> Bool`
**Solution:**
```haskell
myElem :: Eq a => a -> [a] -> Bool
myElem _ []     = False
myElem x (y:ys) = x == y || myElem x ys
```
**QC trap:** Short-circuit via lazy `||` — terminates on infinite lists if the element occurs early.

### Mutation 11 — fastReverse (accumulator) (= problem 15)
**Sig:** `fastReverse :: [a] -> [a]`
**Solution:**
```haskell
fastReverse :: [a] -> [a]
fastReverse = go []
  where
    go acc []     = acc
    go acc (x:xs) = go (x:acc) xs
```
**QC trap:** O(n). `fastReverse . fastReverse == id`. Empty list short-circuits to `[]`.

### Mutation 12 — myConcat (= problem 17)
**Sig:** `myConcat :: [[a]] -> [a]`
**Solution:**
```haskell
myConcat :: [[a]] -> [a]
myConcat []       = []
myConcat (xs:xss) = xs ++ myConcat xss
```
**QC trap:** Quadratic in worst case (`[[a],[b],...,[z]]` is O(n)). Watch out — examiner sometimes adds "stack-safety on giant input".

## Hidden-predicate mutations
- "Sum of elements satisfying p" → fuse mySum + myFilter:
```haskell
sumIf :: (Num a) => (a -> Bool) -> [a] -> a
sumIf _ []     = 0
sumIf p (x:xs) = (if p x then x else 0) + sumIf p xs
```
- "Length of elements satisfying p" → `countIf p xs = length (filter p xs)` but exam-style:
```haskell
countIf :: (a -> Bool) -> [a] -> Int
countIf _ []     = 0
countIf p (x:xs) = (if p x then 1 else 0) + countIf p xs
```

## Accumulator-style alternative
Sum, length, reverse all have strict-accumulator variants. Sum is the canonical example:
```haskell
mySumAcc :: Num a => [a] -> a
mySumAcc = go 0
  where go !acc []     = acc
        go !acc (x:xs) = go (acc + x) xs
```
The bang patterns require `{-# LANGUAGE BangPatterns #-}` if your file doesn't have it.

## Fold-style alternative
See `list-fold-family.md` for the full table. Quick reference:
```haskell
mySum     = foldr (+) 0
myProduct = foldr (*) 1
myLength  = foldr (\_ n -> n + 1) 0
myMap f   = foldr (\x acc -> f x : acc) []
myFilter p= foldr (\x acc -> if p x then x:acc else acc) []
myReverse = foldl (flip (:)) []
```

## Cross-family combinations
- this family + `list-fold-family.md` is the natural pair — same functions, two presentations.
- this family + `list-comp-family.md`: filter via comprehension.
- this family + Maybe: `mapMaybe' = myFilter isJust . myMap f` — see `error-handling-family.md`.

## QuickCheck universal attacks
- **Empty list:** every recursion hits the base case; result must equal the unit.
- **Singleton:** result equals `combine x unit`.
- **Two-element list:** distinguishes left-fold vs right-fold associativity (subtle for `(+)` since it's associative, but watch for non-associative ops).
- **Negative number for take/drop:** classic edge case.
- **`myTake n xs ++ myDrop n xs == xs`** — universal invariant.
- **Comparison with library:** `myLength xs == length xs` etc. for QC.

## Pitfalls (per mutation)
- M1: writing `length xs = length xs + 1` (no recursion on `xs`).
- M2: not using `Num a =>` constraint.
- M3: unit of 0 instead of 1.
- M4: forgetting it's O(n²); examiner may ask "why slow?"
- M5: writing `f xs` instead of `f x` (type error catches this).
- M6: confusing `:` with `++`.
- M7: ordering negative-n case after recursive case.
- M8: returning `xs` for negative n (matches Prelude — some students reset to `[]`).
- M9: missing one of the `[]` cases.
- M10: forgetting `Eq` constraint.
- M11: pushing in the wrong order (gives `xs` not `reverse xs`).
- M12: empty result vs empty input list of lists.

## See also

**Primary archetype:** [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md)
**Sibling families:** [list-fold](./list-fold-family.md) · [list-comp](./list-comp-family.md)
**Basics:** [sorting](../haskell-basics/sorting.md) — the five hand-rolled sorts (insertion / selection / bubble / quick / merge)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md)
**Pitfalls:** [P-018 head/tail/!! without guard](../pitfalls/HIGH-severity.md#p-018)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
