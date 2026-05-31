<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: list-comp**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · **list-comp** · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: list-comp

**Archetype:** A07 (generator-with-predicate list comprehension)   |   **Stars:** ⭐⭐   |   **Course week(s):** 4
**Search keywords:** list comprehension, pyths, factors, perfects, positions, pairs, wordCount, cartesian, generator+guard

## Generator template
```haskell
-- The seed: a list comprehension with a generator, optional dependent generator,
-- and a Boolean guard.
seed :: ... -> [b]
seed xs = [ expr x y | x <- xs, y <- gen x, guard x y ]
```

Every mutation in this family adjusts:
- the number of generators,
- the dependency between later generators and earlier-bound variables,
- the guard,
- the output expression.

## Mutations (the examiner picks one)

### Mutation 1 — pyths (= problem 31)
**Spec:** All Pythagorean triples with components ≤ n.
**Sig:** `pyths :: Int -> [(Int,Int,Int)]`
**Solution:**
```haskell
pyths :: Int -> [(Int,Int,Int)]
pyths n = [ (a,b,c) | a <- [1..n], b <- [1..n], c <- [1..n], a*a + b*b == c*c ]
```
**QC trap:** Result includes both `(3,4,5)` and `(4,3,5)`. If the spec wants only `a <= b`, change `b <- [1..n]` to `b <- [a..n]`.

### Mutation 2 — factors (= problem 32)
**Spec:** All positive divisors of `n`.
**Sig:** `factors :: Int -> [Int]`
**Solution:**
```haskell
factors :: Int -> [Int]
factors n = [ d | d <- [1..n], n `mod` d == 0 ]
```
**QC trap:** Includes 1 and n. `factors 0` would loop forever — exclude or document.

### Mutation 3 — perfects (= problem 35)
**Spec:** Numbers up to `n` equal to the sum of their proper divisors.
**Sig:** `perfects :: Int -> [Int]`
**Solution:**
```haskell
perfects :: Int -> [Int]
perfects n = [ x | x <- [1..n], sum (init (factors x)) == x ]
```
**QC trap:** "Proper divisor" excludes the number itself — hence `init`. (`init [1,2,4,7,14,28] == [1,2,4,7,14]`, and `1+2+4+7+14 == 28`.)

### Mutation 4 — positions (= problem 37)
**Spec:** All zero-based indices of `x` in the list.
**Sig:** `positions :: Eq a => a -> [a] -> [Int]`
**Solution:**
```haskell
positions :: Eq a => a -> [a] -> [Int]
positions x xs = [ i | (y, i) <- zip xs [0..], y == x ]
```
**QC trap:** Returns `[]` when `x` not in list. `head (positions x xs)` is the same as `Data.List.elemIndex x xs` (when present) — useful sanity check.

### Mutation 5 — pairs (= problem 38)
**Spec:** Consecutive overlapping pairs from the list.
**Sig:** `pairs :: [a] -> [(a,a)]`
**Solution:**
```haskell
pairs :: [a] -> [(a,a)]
pairs xs = zip xs (tail xs)
```
**QC trap:** Singleton list returns `[]` (because `tail [x] = []`). Empty list also returns `[]`. The "pairs" list always has length `max 0 (length xs - 1)`.

### Mutation 6 — wordCount (= problem 39)
**Spec:** Number of words (space-separated tokens) in the string.
**Sig:** `wordCount :: String -> Int`
**Solution:**
```haskell
wordCount :: String -> Int
wordCount = length . words
```
Or, more list-comp flavoured:
```haskell
wordCount s = length [ w | w <- words s ]
```
**QC trap:** Consecutive spaces; leading/trailing spaces are *all* handled correctly by `words`. Writing `length . filter (' '/=) . groupBy ...` is overkill.

### Mutation 7 — cartesian (= problem 40)
**Spec:** Cartesian product of two lists.
**Sig:** `cartesian :: [a] -> [b] -> [(a,b)]`
**Solution:**
```haskell
cartesian :: [a] -> [b] -> [(a,b)]
cartesian xs ys = [ (x,y) | x <- xs, y <- ys ]
```
**QC trap:** Order matters: with `xs = [1,2]` and `ys = [3,4]`, result is `[(1,3),(1,4),(2,3),(2,4)]`. Inner loop is `y`, outer is `x`.

### Mutation 8 — scalar / dot product (= problem 36)
**Spec:** Dot product of two same-length lists.
**Sig:** `scalar :: Num a => [a] -> [a] -> a`
**Solution:**
```haskell
scalar :: Num a => [a] -> [a] -> a
scalar xs ys = sum [ x * y | (x, y) <- zip xs ys ]
```
**QC trap:** Assumes equal length. `scalar [1,2] [3,4,5]` gives `1*3 + 2*4 = 11` (truncates) — exam may say "you may assume same length".

### Mutation 9 — primesUpTo (= problem 34)
**Spec:** All primes ≤ n.
**Sig:** `primesUpTo :: Int -> [Int]`
**Solution:**
```haskell
isPrime :: Int -> Bool
isPrime n = n > 1 && factors n == [1, n]

primesUpTo :: Int -> [Int]
primesUpTo n = [ p | p <- [2..n], isPrime p ]
```
**QC trap:** `primesUpTo 1 == []`. `isPrime 1 == False` (1 is not prime by convention).

### Mutation 10 — allPairs (= problem 106, ordered distinct pairs)
**Spec:** All ordered pairs of distinct positions.
**Sig:** `allPairs :: [a] -> [(a,a)]`
**Solution:**
```haskell
allPairs :: [a] -> [(a,a)]
allPairs xs = [ (x,y) | (x:rest) <- tails xs, y <- rest ]
  where tails [] = [[]]
        tails (a:as) = (a:as) : tails as
```
**QC trap:** Result length is `n*(n-1)/2` for `length xs == n`. Order is `(x1,x2),(x1,x3),...,(x1,xn),(x2,x3),...`.

## Hidden-predicate mutations
- "All triples (i,j,k) with i<j<k and ..." → add `j <- [i+1..n], k <- [j+1..n]` style monotone generators.
- "Where the predicate p holds" → add a guard `, p x` at the end.

## Accumulator-style alternative
Most list comprehensions desugar to monadic `do`-notation on the list monad:
```haskell
pythsDo :: Int -> [(Int,Int,Int)]
pythsDo n = do
  a <- [1..n]
  b <- [1..n]
  c <- [1..n]
  guard (a*a + b*b == c*c)
  pure (a,b,c)
```
(requires `import Control.Monad (guard)`)

## Fold-style alternative
For "filter then collect", a `foldr` rewrite of mutation 4:
```haskell
positionsFold :: Eq a => a -> [a] -> [Int]
positionsFold x = foldr (\(y,i) acc -> if y == x then i : acc else acc) []
                . flip zip [0..]
```
Comprehension reads better; only switch if asked.

## Cross-family combinations
- this family + `list-fold-family.md`: comprehensions desugar to foldr.
- this family + `monad-combinator-family.md`: list monad = list comprehension with `guard`.
- this family + `tree-extract-family.md`: `flattenInOrder` can be written as `[v | v <- inOrderTraversal t]` once you have a traversal.

## QuickCheck universal attacks
- **Empty input:** every comprehension over `[]` yields `[]`.
- **Single-element input:** very useful for `pairs` (returns `[]`) and `positions` (returns `[0]` if match).
- **Predicate that's always False:** result is `[]`.
- **Predicate that's always True:** result enumerates the generator(s) Cartesian-product-style.
- **Cross-check with Hoogle-Prelude:** `pairs = zip xs (tail xs)`; `positions x = map fst . filter ((==x) . snd) . zip [0..] xs`.

## Pitfalls (per mutation)
- M1: forgetting `a*a + b*b == c*c` and writing `a^2 + b^2 == c^2` — works but slow integer power.
- M2: starting from 0 (divide-by-zero) — must be `[1..n]`.
- M3: forgetting `init` (or using `tail` — wrong end).
- M4: zipping with `[1..]` instead of `[0..]`.
- M5: forgetting that `tail []` crashes — handle empty input.
- M6: writing space-splitting from scratch when `words` is allowed.
- M7: swapping order of `x <- xs, y <- ys`.
- M8: relying on equal length without saying so.
- M9: forgetting that 1 is not prime.
- M10: writing `[ (x,y) | x <- xs, y <- xs, x /= y]` (wrong — order matters; this gives both `(1,2)` and `(2,1)`).
- M11: using `x > p` in the second partition (drops duplicates of the pivot) — must be `x >= p`.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — qsort (quicksort via list comprehension)

**Spec:** Sort a list ascending using the canonical comprehension-based quicksort: pick the head as pivot, recurse on the elements smaller than it and the elements at-least-as-big as it.

**Type sig:** `qsort :: Ord a => [a] -> [a]`

```haskell
qsort :: Ord a => [a] -> [a]
qsort []     = []
qsort (p:xs) = qsort [x | x <- xs, x < p] ++ [p] ++ qsort [x | x <- xs, x >= p]
```

**What changes vs seed:** Two *separate* single-generator comprehensions used as a **partition**, feeding a recursive call — not the flat generator+guard of the seed. The list comp here is the partition primitive; the recursion structure is the algorithm. (`Ord a`, not `Num a` — works on any orderable type, e.g. `qsort "haskell" == "aehklls"`.)

**QC trap:** The second partition **must** be `x >= p`, not `x > p` — using `x > p` silently drops every element equal to the pivot, so `qsort [3,1,2,1] == [1,2,3]` instead of `[1,1,2,3]`. The two comprehensions both scan `xs` (the tail), never the whole `p:xs`, or it loops forever. QC checks: `qsort xs == Data.List.sort xs`, and idempotence `qsort (qsort xs) == qsort xs`.

## See also

**Primary archetype:** [A21 list comp synthesis](../archetypes/A21-list-comp-synthesis.md)
**Sibling families:** [list-rewrite](./list-rewrite-family.md) · [list-fold](./list-fold-family.md)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
