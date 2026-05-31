<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A21 — List Comprehension Synthesis (NEW)**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · **A21** · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A21 — List Comprehension Synthesis (NEW)

**Tier:** 2   |   **Stars:** ⭐⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** A2 (uses `concat [brackets t | t <- ts]` in spec)
**Combines with:** A09 · A10 · A04 · A11
**Search keywords:** list comprehension · `[x | x <- xs, p x]` · generator · guard · cartesian · enumerate · Pythagorean · factors · perfects

## Justification for inclusion as its own archetype
List comprehensions are syntactically distinct from explicit recursion (A09) and from folds (A10) — students often DON'T see the equivalence, and exam graders frequently mark off when a list comp is the obvious answer but the student writes a fold or vice-versa. The course (Problem Sheets 4, Week 3 lecture) drills list comps specifically as "the way to enumerate". When the question stem is "all `(a, b, c)` such that …", that's a UNIQUE recognition pattern that doesn't map to A09 or A10 cleanly. Worth carving off as a separate archetype with its own recognition triggers and 10 mutations.

## What it tests
Whether you can express set-comprehension-style enumeration with multiple generators (cartesian product), filter guards, and dependent generators (`y <- [x..]`), without falling back to nested explicit loops.

## Recognition triggers
- "all `(a, b, c)` such that …"
- "all divisors of n", "all primes", "all perfect numbers"
- "Pythagorean triples", "Pascal's triangle"
- "all pairs `(x, y)` from this list with x < y"
- The expected output is a LIST of items satisfying multiple predicates
- Type signature returns `[(a, b)]` or `[(a, b, c)]` with no input list (just `Int`)
- "Use list comprehensions" appears in the spec

## Canonical template
```haskell
result :: Int -> [(Int, Int, Int)]
result n = [(a, b, c) | a <- [1..n], b <- [a..n], c <- [b..n], pred a b c]
```

## Mutations (the examiner picks one)

### M1 — `pyths` (problem 31, Pythagorean triples)
```haskell
pyths :: Int -> [(Int, Int, Int)]
pyths n = [(a, b, c) | a <- [1..n], b <- [a..n], c <- [b..n], a*a + b*b == c*c]
```
What changes: ordered triples (a ≤ b ≤ c) via dependent generators; guard checks Pythagoras.

### M2 — `factors` (problem 32)
```haskell
factors :: Int -> [Int]
factors n = [d | d <- [1..n], n `mod` d == 0]
```
What changes: single generator with divisibility guard.

### M3 — `isPrime` via factors (problem 33)
```haskell
isPrime :: Int -> Bool
isPrime n = factors n == [1, n]
```
What changes: not a list comp itself, but builds on M2.

### M4 — `primesUpTo` (problem 34)
```haskell
primesUpTo :: Int -> [Int]
primesUpTo n = [p | p <- [2..n], isPrime p]
```
What changes: filter guard using a predicate; classic comprehension.

### M5 — `perfects` (problem 35)
```haskell
perfects :: Int -> [Int]
perfects n = [k | k <- [1..n], sum (init (factors k)) == k]
```
What changes: more complex guard; uses M2 inside.

### M6 — `scalar` (problem 36, dot product)
```haskell
scalar :: Num a => [a] -> [a] -> a
scalar xs ys = sum [x * y | (x, y) <- zip xs ys]
```
What changes: pattern destructuring in generator; combine with `sum`.

### M7 — `positions` (problem 37)
```haskell
positions :: Eq a => a -> [a] -> [Int]
positions x xs = [i | (y, i) <- zip xs [0..], y == x]
```
What changes: generator emits pairs, guard filters on first, output is second; classic enumerate pattern.

### M8 — `pairs` (problem 38, consecutive)
```haskell
pairs :: [a] -> [(a, a)]
pairs xs = [(a, b) | (a, b) <- zip xs (tail xs)]
```
What changes: derive a paired list using `zip xs (tail xs)`.

### M9 — `cartesian` (problem 40)
```haskell
cartesian :: [a] -> [b] -> [(a, b)]
cartesian xs ys = [(x, y) | x <- xs, y <- ys]
```
What changes: pure double generator; no guard; output is full cartesian product.

### M10 — `allPairs` distinct positions (problem 106)
```haskell
allPairs :: [a] -> [(a, a)]
allPairs xs = [(x, y) | (i, x) <- zip [0..] xs, (j, y) <- zip [0..] xs, i < j]
```
What changes: dependent index guard; ordered, distinct pairs.

### M11 — `knightMoves` (problem 105, list-monad style)
```haskell
knightMoves :: (Int, Int) -> [(Int, Int)]
knightMoves (x, y) =
  [(x + dx, y + dy) | (dx, dy) <- [(1,2),(2,1),(-1,2),(2,-1),(1,-2),(-2,1),(-1,-2),(-2,-1)],
                       x + dx >= 1, x + dx <= 8,
                       y + dy >= 1, y + dy <= 8]
```
What changes: filter by board boundaries; tuple destructure in generator.

### M12 — `qsort` (problem 27)
```haskell
qsort :: Ord a => [a] -> [a]
qsort []     = []
qsort (p:xs) = qsort [x | x <- xs, x < p]
            ++ [p]
            ++ qsort [x | x <- xs, x >= p]
```
What changes: list comp inside recursion; partition by pivot.

## Worked examples from this course
- Problem sheet Set 4 (#31-40): the whole set is list-comp territory.
- Problem sheet Set 11 (#105-106): `knightMoves`, `allPairs`.
- Practice file `problems.hs` and others: scattered usage.
- Assignment 2 spec: `brackets (Round ts) = "(" ++ concat [brackets t | t <- ts] ++ ")"`.

## QuickCheck attack surface
- **`pyths 10`** must include `(3,4,5)`, `(6,8,10)` and nothing else (in ordered form).
- **`factors 12 == [1,2,3,4,6,12]`** — must include 1 and n.
- **`primesUpTo 10 == [2,3,5,7]`** — exclude 1.
- **`perfects 500 == [6,28,496]`**.
- **`scalar [1,2,3] [4,5,6] == 32`** (= 4+10+18).
- **`positions 3 [1,3,2,3,3] == [1,3,4]`** — 0-indexed positions.
- **`allPairs [1,2,3] == [(1,2),(1,3),(2,3)]`** — distinct, ordered.
- **Empty input**: `qsort []`, `factors 1 == [1]`, etc.

## Pitfalls (marks-killers)
- **Generator order matters for performance**: `[ (a,b) | a <- xs, b <- ys, p a b ]` enumerates `b` faster. For dependent (`b <- [a..]`), order is fixed by dependence.
- **Wrong order of `[]` and `(:)` in qsort**: must concat `[≤p] ++ [p] ++ [>p]`; reversing gives reverse sort.
- **Off-by-one in `b <- [a..n]`** vs `b <- [a+1..n]`: depends on whether `a==b` is allowed.
- **Using `tail xs` on `[]`**: `pairs []` should be `[]`, not crash; `zip` saves you because `zip [] _ = []`.
- **`mod`/`rem` confusion**: stick to `mod` for positive numbers; the spec is usually `n mod d == 0`.
- **`elem` confusion**: `[x | x <- xs, x `elem` ys]` is right, not `x `elem xs`.
- **Lazy infinite generator**: `[x | x <- [1..], p x]` works for `take`, but `length` infinite-loops.

## Combines-with deep dive

### A21 × A09 — list comp vs explicit recursion
Same problem, different syntax. Mark equivalence explicitly:
```haskell
factors_rec :: Int -> [Int]
factors_rec n = go 1
  where go d | d > n             = []
             | n `mod` d == 0    = d : go (d + 1)
             | otherwise         = go (d + 1)
```

### A21 × A04 — generating matrix candidates
```haskell
candidateSquares :: Int -> [[[Int]]]
candidateSquares n = [chunks n p | p <- permutations [1..n*n]]
  where chunks _ [] = []
        chunks k xs = take k xs : chunks k (drop k xs)
```

### A21 × A11 — qsort uses list comp
See M12. Classic illustration.

## See also

**Combines with:** [A09 prelude reimpl](./A09-prelude-reimpl.md) · [A10 fold reformulation](./A10-fold-reformulation.md) · [A04 matrix predicate](./A04-matrix-predicate.md)
**Question families:** [list-comp](../question-families/list-comp-family.md)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
