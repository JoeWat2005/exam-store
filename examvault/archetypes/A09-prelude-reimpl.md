<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A09 — Reimplement Prelude with Explicit Recursion**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · **A09** · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A09 — Reimplement Prelude with Explicit Recursion

**Tier:** 2   |   **Stars:** ⭐⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** none (transpose hand-rolled in A1 solution)
**Combines with:** A10 · A21
**Search keywords:** myLength · myReverse · myMap · myFilter · myTake · myDrop · myZip · myReplicate · myConcat · without using

## What it tests
Whether you can write a recursive equation for a well-known list operation directly: `f [] = base; f (x:xs) = step x (f xs)` — without leaning on Prelude's `length`, `reverse`, etc.

## Recognition triggers
- "Reimplement / Define your own / write `f` without using …"
- Type sig has `[a]` and a familiar Prelude name with `my` prefix or `'` suffix
- "naive" or "O(n²)" hints in the question (signals a non-accumulator solution is acceptable)
- "fast / O(n)" hints signal an accumulator-helper version is expected
- The question explicitly lists what you may NOT import / use

## Canonical template
```haskell
myFoo :: [a] -> [a]
myFoo []     = base
myFoo (x:xs) = step x (myFoo xs)
```

## Mutations (the examiner picks one)

### M1 — `myLength` (problem 11)
```haskell
myLength :: [a] -> Int
myLength []     = 0
myLength (_:xs) = 1 + myLength xs
```
What changes: nothing — the cleanest example.

### M2 — `myReverse` naive (problem 14)
```haskell
myReverse :: [a] -> [a]
myReverse []     = []
myReverse (x:xs) = myReverse xs ++ [x]
```
What changes: structural; O(n²) because `++ [x]` traverses each time. Accept if the spec says naive.

### M3 — `fastReverse` (accumulator, problem 15)
```haskell
fastReverse :: [a] -> [a]
fastReverse = go []
  where go acc []     = acc
        go acc (x:xs) = go (x:acc) xs
```
What changes: extra accumulator, O(n). Push each element to the FRONT of `acc`.

### M4 — `myMap` (problem 43 sans foldr)
```haskell
myMap :: (a -> b) -> [a] -> [b]
myMap _ []     = []
myMap f (x:xs) = f x : myMap f xs
```
What changes: takes a function; apply to head, recurse on tail.

### M5 — `myFilter` (problem 44 sans foldr)
```haskell
myFilter :: (a -> Bool) -> [a] -> [a]
myFilter _ []     = []
myFilter p (x:xs)
  | p x       = x : myFilter p xs
  | otherwise = myFilter p xs
```
What changes: predicate-guarded include/exclude.

### M6 — `myZip` (problem 20)
```haskell
myZip :: [a] -> [b] -> [(a, b)]
myZip []     _      = []
myZip _      []     = []
myZip (x:xs) (y:ys) = (x, y) : myZip xs ys
```
What changes: two lists; stops at the shorter — TWO base cases.

### M7 — `myTake` (problem 18)
```haskell
myTake :: Int -> [a] -> [a]
myTake n _      | n <= 0 = []
myTake _ []              = []
myTake n (x:xs)          = x : myTake (n - 1) xs
```
What changes: int-counter base case + list-empty base case + countdown recursion.

### M8 — `myDrop` (problem 19)
```haskell
myDrop :: Int -> [a] -> [a]
myDrop n xs     | n <= 0 = xs
myDrop _ []              = []
myDrop n (_:xs)          = myDrop (n - 1) xs
```
What changes: like take but throws away the head.

### M9 — `myReplicate` (problem 21)
```haskell
myReplicate :: Int -> a -> [a]
myReplicate n _ | n <= 0 = []
myReplicate n x          = x : myReplicate (n - 1) x
```
What changes: no list input; recursion on the count.

### M10 — `myConcat` (problem 17)
```haskell
myConcat :: [[a]] -> [a]
myConcat []       = []
myConcat (xs:xss) = xs ++ myConcat xss
```
What changes: input is `[[a]]`; combine with `++`. Single recursive call per outer cons.

### M11 — hand-rolled `transpose` (used in A1 solution)
```haskell
transpose' :: [[a]] -> [[a]]
transpose' []        = []
transpose' ([]   :_) = []
transpose' xss       = map head xss : transpose' (map tail xss)
```
What changes: two base cases (empty outer, empty inner); recursion peels off the first column.

## Worked examples from this course
- Problem sheet Set 2 (#11-20): `myLength`, `mySum`, `myProduct`, `myReverse`, `fastReverse`, `myElem`, `myConcat`, `myTake`, `myDrop`, `myZip` — the whole gym.
- Problem sheet Set 3 (#21-22): `myReplicate`, `myLast`, `myInit`, `myLookup`.
- Problem sheet Set 5 (#43-50): fold-based versions of map, filter, length, sum (A10 territory).
- Assignment 1: hand-rolled `transpose` in the solution.
- Practice file `githubinitial.hs`: complete sweep of problems #1-50.

## QuickCheck attack surface
- **Empty list `[]`**: must terminate, must return the appropriate base value.
- **Singleton `[x]`**: catches "drop one too few / take one too many" off-by-one.
- **Negative `n`**: `myTake (-5) [1,2,3] == []` (Prelude `take` returns `[]` for `n <= 0`).
- **`n > length xs`**: `myTake 100 [1,2,3] == [1,2,3]` — both base cases reached.
- **Polymorphic**: marker tests `myReverse [True,False,True]`, `myReverse "abc"`, etc.
- **Quadratic detection**: huge inputs (10000 elements) — `myReverse` naive should pass but `fastReverse` should be measurably faster. Marker may NOT time this; it cares about correctness.
- **`myZip` length**: `length (myZip xs ys) == min (length xs) (length ys)`.

## Pitfalls (marks-killers)
- **Calling the Prelude version inside**: `myLength xs = length xs` — defeats the exercise. Auto-marker may still award marks if it just runs the test cases, but the spirit is broken.
- **Off-by-one on count**: `myTake n (x:xs) = myTake (n-1) xs` (forgot to include `x:`).
- **Missing the `n <= 0` clause**: causes infinite recursion on `myTake (-1) [1..]` or just returns `[]` accidentally only because `xs` is empty.
- **Quadratic reverse**: `myReverse xs ++ [x]` is O(n²). Acceptable for `myReverse`; not for `fastReverse`.
- **Pattern overlap**: writing `myTake 0 xs = xs` instead of `[]` — confuses `take` with `id`.
- **Type annotation for `Num a`**: `mySum :: Num a => [a] -> a` — student writes `[Int]`. Marker may use `[Double]`.

## Combines-with deep dive

### A09 × A10 — fold reformulation
```haskell
myLength'  = foldr (\_ n -> n + 1) 0
myReverse' = foldl (flip (:)) []
myMap' f   = foldr (\x acc -> f x : acc) []
myFilter' p = foldr (\x acc -> if p x then x : acc else acc) []
```

### A09 × A21 — list comprehension reformulation
```haskell
myMap'' f xs    = [f x | x <- xs]
myFilter'' p xs = [x | x <- xs, p x]
myZip'' xs ys   = [(x, y) | (x, y) <- zip xs ys]
```

## See also

**Combines with:** [A10 fold reformulation](./A10-fold-reformulation.md) · [A21 list comp synthesis](./A21-list-comp-synthesis.md)
**Question families:** [list-rewrite](../question-families/list-rewrite-family.md)
**Basics:** [sorting](../haskell-basics/sorting.md) — the five hand-rolled sorts (insertion / selection / bubble / quick / merge)
**Pitfalls:** [P-018 head/tail/!! without guard](../pitfalls/HIGH-severity.md#p-018)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
