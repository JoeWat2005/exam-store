<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A10 — Fold Reformulation**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · **A10** · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A10 — Fold Reformulation

**Tier:** 3   |   **Stars:** ⭐⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** none direct
**Combines with:** A09 · A21 · A22
**Search keywords:** foldr · foldl · without recursion · without explicit recursion · using only · `foldr step base`

## What it tests
Whether you can re-express a list-recursion as `foldr step base` or `foldl step base` — identifying the per-cons step function and the empty-list base value, then plugging into the fold skeleton.

## Recognition triggers
- "Using only `foldr` / `foldl`" appears in the spec
- "without explicit recursion"
- "Define `f` as a fold" or "Reimplement `g` using `foldr`"
- The Prelude name has a `WithFoldr` / `WithFoldl` suffix in the problem stem
- The task description: "given a list, …" with no mention of an explicit recursion pattern

## Canonical template
```haskell
-- Schema:    f []     = base
--            f (x:xs) = step x (f xs)
-- Becomes:   f = foldr step base
```

## Mutations (the examiner picks one)

### M1 — `sumWithFoldr` (problem 41)
```haskell
sumWithFoldr :: Num a => [a] -> a
sumWithFoldr = foldr (+) 0
```
What changes: `step = (+)`, `base = 0`.

### M2 — `lengthWithFoldr` (problem 42)
```haskell
lengthWithFoldr :: [a] -> Int
lengthWithFoldr = foldr (\_ n -> n + 1) 0
```
What changes: ignore the head element with `_`; just increment the recursive result.

### M3 — `mapWithFoldr` (problem 43)
```haskell
mapWithFoldr :: (a -> b) -> [a] -> [b]
mapWithFoldr f = foldr (\x acc -> f x : acc) []
```
What changes: cons `f x` onto the accumulating list.

### M4 — `filterWithFoldr` (problem 44)
```haskell
filterWithFoldr :: (a -> Bool) -> [a] -> [a]
filterWithFoldr p = foldr (\x acc -> if p x then x : acc else acc) []
```
What changes: guard on predicate; otherwise pass through.

### M5 — `reverseWithFoldl` (problem 45)
```haskell
reverseWithFoldl :: [a] -> [a]
reverseWithFoldl = foldl (flip (:)) []
```
What changes: `foldl` (O(n)) flips the cons. Using `foldr` gives O(n²).

### M6 — `allWithFoldr` (problem 46)
```haskell
allWithFoldr :: (a -> Bool) -> [a] -> Bool
allWithFoldr p = foldr (\x acc -> p x && acc) True
```
What changes: combine with `&&`; base `True` is the identity of `&&`.

### M7 — `concatWithFoldr`
```haskell
concatWithFoldr :: [[a]] -> [a]
concatWithFoldr = foldr (++) []
```
What changes: `++` is the binary op; `[]` is the identity.

### M8 — `compose'` (problem 47)
```haskell
compose' :: [a -> a] -> (a -> a)
compose' = foldr (.) id
```
What changes: function-composition fold; `id` is the identity of `.`.

### M9 — `maxWithFoldr`
```haskell
maxWithFoldr :: Ord a => [a] -> Maybe a
maxWithFoldr = foldr step Nothing
  where step x Nothing  = Just x
        step x (Just y) = Just (max x y)
```
What changes: needs `Maybe` to handle empty list — base case is `Nothing`.

### M10 — `partitionWithFoldr` (problem 50 style)
```haskell
partitionWithFoldr :: (a -> Bool) -> [a] -> ([a], [a])
partitionWithFoldr p = foldr step ([], [])
  where step x (yes, no) | p x       = (x:yes, no)
                         | otherwise = (yes, x:no)
```
What changes: accumulator is a tuple; pattern-match in lambda's body.

### M11 — `dropLastWithFoldr` (`init`)
```haskell
initWithFoldr :: [a] -> [a]
initWithFoldr = foldr step []
  where step x [] = []
        step x ys = x : ys
```
What changes: base shrinks (the singleton becomes `[]`), recursive case keeps cons. Note: requires non-empty input.

## Worked examples from this course
- Problem sheet Set 5 (#41-47): the whole gym — `sumWithFoldr`, `lengthWithFoldr`, `mapWithFoldr`, `filterWithFoldr`, `reverseWithFoldl`, `allWithFoldr`, `compose'`.
- Lecture notes Week 4: fold introduction; defining `foldr` from scratch.
- Practice file: `final10.hs` exercises rewriting via folds.

## QuickCheck attack surface
- **Empty list**: `mapWithFoldr f [] == []`, `sumWithFoldr [] == 0`. The base value of `foldr` is returned literally.
- **Singleton**: `mapWithFoldr (+1) [5] == [6]`. Catches step-function bugs.
- **Equivalence to Prelude**: marker generates a random list and checks `mapWithFoldr f xs == map f xs`.
- **Polymorphic typing**: `sumWithFoldr [1.0, 2.0] == 3.0`. The signature must use `Num a`.
- **Infinite-list short-circuit (foldr only)**: `take 5 (mapWithFoldr (+1) [1..]) == [2,3,4,5,6]`. Bug: using `foldl` here loops forever.
- **Stack overflow with foldr / foldl**: huge lists (1M elements) — foldl' is the safer big-list fold, but the course mostly accepts plain `foldl`.

## Pitfalls (marks-killers)
- **`acc` confusion**: in `foldr step base`, `acc` is the RESULT of folding the rest (`f xs`), NOT the rest of the input list. Easy to confuse.
- **Wrong `base`**: identity of the step function. For `(+)` it's `0`; for `(*)` it's `1`; for `(&&)` it's `True`; for `(.)` it's `id`; for `(++)` it's `[]`.
- **`foldr` for reverse**: gives O(n²) since `(++ [x])` is per-element. Use `foldl` with `flip (:)` for O(n).
- **`foldl` on infinite lists**: never terminates. Use `foldr` if the step is lazy enough to short-circuit (`&&`, `||`).
- **Argument order in step**: `foldr` step is `(a -> b -> b)` (element-first, accumulator-second). `foldl` step is `(b -> a -> b)` (accumulator-first, element-second). Mixing these is a common typo.
- **Pointless-style trips**: `length = foldr (const (1+)) 0` and `length = foldr (\_ -> (+1)) 0` are equivalent and both correct.

## Combines-with deep dive

### A10 × A09 — Prelude reimpl, fold edition
Every problem in A09 has a fold version in A10. Pick `foldr` for shape-preserving / list-output; pick `foldl` when an accumulator is needed.

### A10 × A22 — fold on a custom type
For a custom recursive ADT, define `foldT :: (a -> b -> b) -> b -> T a -> b`, then re-express functions over `T` using `foldT`.

```haskell
foldBT :: (a -> b -> b -> b) -> b -> BT a -> b
foldBT _ z Empty        = z
foldBT f z (Fork x l r) = f x (foldBT f z l) (foldBT f z r)

sizeBT' = foldBT (\_ l r -> 1 + l + r) 0
heightBT' = foldBT (\_ l r -> 1 + max l r) 0
```

### A10 × A21 — fold vs list comp
```haskell
sumSquares xs = foldr (\x acc -> x*x + acc) 0 xs
sumSquaresLC xs = sum [x*x | x <- xs]
```

## See also

**Combines with:** [A09 prelude reimpl](./A09-prelude-reimpl.md) · [A21 list comp synthesis](./A21-list-comp-synthesis.md)
**Question families:** [list-fold](../question-families/list-fold-family.md)
**Cross-topic:** [list × list-monad](../cross-matrix/list-x-list-monad.md)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
