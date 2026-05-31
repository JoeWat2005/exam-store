<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: lazy-infinite**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · **lazy-infinite** · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: lazy-infinite

**Archetype:** A18 (infinite/lazy data structures)   |   **Stars:** ⭐⭐⭐⭐   |   **Course week(s):** 11
**Search keywords:** ones, fibs, sieve, repeat, iterate, cycle, knot-tying, infty, lengthNat, memoFib, fix

## Generator template
```haskell
-- The seed: a recursive definition that *refers to itself* on the right-hand side,
-- relying on Haskell's laziness to make sense of the cyclic reference.
seed :: [a]
seed = expr seed
```

Examples:
- `ones = 1 : ones`
- `fibs = 0 : 1 : zipWith (+) fibs (tail fibs)`
- `cycle xs = xs ++ cycle xs`

## Mutations (the examiner picks one)

### Mutation 1 — ones (= problem 131)
**Sig:** `ones :: [Int]`
**Solution:**
```haskell
ones :: [Int]
ones = 1 : ones
```
**QC trap:** `take 5 ones == [1,1,1,1,1]`. `length ones` diverges. `head ones == 1`. The simplest non-trivial infinite list.

### Mutation 2 — fibs (Fibonacci via zipWith) (= problem 132)
**Sig:** `fibs :: [Integer]`
**Solution:**
```haskell
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)
```
**QC trap:** `fibs !! 0 == 0`, `fibs !! 1 == 1`, `fibs !! 100 == 354224848179261915075`. Uses Integer (not Int) — Int would overflow.

### Mutation 3 — primes via sieve (= problem 133)
**Sig:** `primes :: [Int]`
**Solution:**
```haskell
primes :: [Int]
primes = sieve [2..]
  where
    sieve (p:xs) = p : sieve [x | x <- xs, x `mod` p /= 0]
```
**QC trap:** Trial-division sieve, not the Eratosthenes-grid sieve. `take 5 primes == [2,3,5,7,11]`. Famously *slow* — the textbook one-liner is O(n²/log n) at best.

### Mutation 4 — lazy Nat (= problem 134)
**Spec:** `data Nat = Zero | Succ Nat`; `infty = Succ infty`.
**Sig:** `infty :: Nat`
**Solution:**
```haskell
data Nat = Zero | Succ Nat deriving (Show, Eq, Ord)

addNat :: Nat -> Nat -> Nat
addNat Zero n     = n
addNat (Succ m) n = Succ (addNat m n)

infty :: Nat
infty = Succ infty
```
**QC trap:** `addNat infty 5 == infty` (laziness). `infty == infty` *diverges* under structural equality — don't try.

### Mutation 5 — lengthNat (= problem 135)
**Sig:** `lengthNat :: [a] -> Nat`
**Solution:**
```haskell
lengthNat :: [a] -> Nat
lengthNat []     = Zero
lengthNat (_:xs) = Succ (lengthNat xs)

toNat :: Int -> Nat
toNat 0 = Zero
toNat n = Succ (toNat (n - 1))
```
**QC trap:** `lengthNat [1..] == infty` works because Nat is lazy. Comparing `lengthNat [1..5] < toNat 6` terminates because Ord on Nat stops on the first difference.

### Mutation 6 — memoFib via infinite tree (= problem 136)
**Spec:** Memoise Fibonacci using an infinite indexed tree.
**Sig:** `memoFib :: Int -> Integer`
**Solution:**
```haskell
data IntTree = LFork IntTree Integer IntTree

memoFib :: Int -> Integer
memoFib n = lookupTree treeFib n
  where
    treeFib  = buildTree fib
    fib 0    = 0
    fib 1    = 1
    fib n    = lookupTree treeFib (n - 1) + lookupTree treeFib (n - 2)
    buildTree f = go 0 1
      where
        go offset step = LFork (go (offset + step) (step * 2))
                               (f offset)
                               (go (offset + step * 2) (step * 2))
        -- adapt this to a sensible index scheme
    lookupTree (LFork _ v _) 0  = v
    lookupTree (LFork l _ r) n
      | even n   = lookupTree l (n `div` 2)
      | otherwise = lookupTree r ((n - 1) `div` 2)
```
**QC trap:** "Knot tying" — `treeFib` refers to itself via `fib`. Subtle to get the index scheme right.

### Mutation 7 — fix' (= problem 137)
**Sig:** `fix' :: (a -> a) -> a`
**Solution:**
```haskell
fix' :: (a -> a) -> a
fix' f = let x = f x in x

factorial :: Int -> Int
factorial = fix' $ \rec n -> if n <= 0 then 1 else n * rec (n - 1)
```
**QC trap:** `fix' (1:)` is `[1, 1, ..]` = `repeat 1`. `fix' id` diverges. The recursive call is named via the lambda parameter `rec`.

### Mutation 8 — iterate' (= problem 48)
**Sig:** `iterate' :: (a -> a) -> a -> [a]`
**Solution:**
```haskell
iterate' :: (a -> a) -> a -> [a]
iterate' f x = x : iterate' f (f x)
```
**QC trap:** `take 5 (iterate' (*2) 1) == [1,2,4,8,16]`. Infinite list. Powers the pure side of `applyNTimes`.

### Mutation 9 — repeat / cycle
**Sig:** `repeat :: a -> [a]`, `cycle :: [a] -> [a]`
**Solution:**
```haskell
repeat :: a -> [a]
repeat x = x : repeat x

cycle :: [a] -> [a]
cycle []  = error "empty cycle"
cycle xs  = xs ++ cycle xs
```
**QC trap:** `take 6 (cycle [1,2,3]) == [1,2,3,1,2,3]`. `cycle []` is undefined (error). `repeat x = cycle [x]`.

### Mutation 10 — naturals / odds
**Sig:** `naturals :: [Int]`, `odds :: [Int]`
**Solution:**
```haskell
naturals :: [Int]
naturals = [0..]

odds :: [Int]
odds = filter odd [1..]
-- or recursively:
oddsRec = go 1
  where go n = n : go (n + 2)
```
**QC trap:** `[0..]` works because `enumFrom 0` is lazy. `take 5 odds == [1,3,5,7,9]`.

## Hidden-predicate mutations
- "Filter an infinite list by predicate p" → `filter p` works iff p accepts arbitrarily many.
- "Take elements while p holds" → `takeWhile p` terminates on infinite lists when p eventually fails.

## Accumulator-style alternative
Lazy infinite structures are *inherently* defined recursively without accumulator. The closest analog is an *explicit* generator function via `unfoldr`:
```haskell
import Data.List (unfoldr)

fibsUnfold :: [Integer]
fibsUnfold = unfoldr (\(a, b) -> Just (a, (b, a + b))) (0, 1)
```

## Fold-style alternative
`foldr` on infinite input works *iff the combine is lazy in its second arg*:
```haskell
take' :: Int -> [a] -> [a]
take' n xs = foldr (\x rest k -> if k <= 0 then [] else x : rest (k - 1)) (const []) xs n
```
Notice: the result of `foldr` is *a function*, not a list. CPS-style.

## Cross-family combinations
- this family + `list-fold-family.md`: foldr on infinite lists.
- this family + `monad-combinator-family.md`: `iterate` for the pure side of applyNTimes.
- this family + `matrix-predicate-family.md`: infinite Conway's Life evolution.
- this family + State: an infinite stream of "die rolls" (problem 116).

## QuickCheck universal attacks
- **Take is total:** `length (take n inf) == n` for any `inf :: [a]` and finite `n`.
- **Element existence:** `5 `elem` [1..]` terminates (returns True). `(-1) `elem` [1..]` *diverges*.
- **Take then drop:** `take n xs ++ drop n xs` is `xs` only for finite `xs`.
- **`fibs !! n == fib n`** for the naïve fib.
- **`take n (iterate' f x) == take n (zipWith ($) (repeat f) (iterate' f x))`** modulo definitions.
- **`take n primes` is the first n primes:** sanity.

## Pitfalls (per mutation)
- M1: defining `ones = repeat 1` — correct but circumvents the spec.
- M2: using `Int` instead of `Integer` — overflow.
- M3: writing `[2..]` then filtering by `not . any divides` — much slower than the sieve.
- M4: trying to evaluate `infty == infty` — diverges.
- M5: not relying on Ord short-circuit.
- M6: getting the tree indexing wrong — tricky.
- M7: writing `fix' f = f (fix' f)` — also valid, but the `let x = f x` form is more efficient.
- M8: confusing iterate with iterateUntil.
- M9: cycling an empty list.
- M10: writing `naturals = 0 : map (+1) naturals` — also valid, equivalent to `[0..]`.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — takeWhileFinite (lazy infinite generator + take prefix)

**Spec:** Lazily generate the Fibonacci sequence and return the prefix up to (but not including) the first term exceeding `n`.

**Type sig:** `fibsBelow :: Int -> [Int]`

```haskell
fibs :: [Int]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

fibsBelow :: Int -> [Int]
fibsBelow n = takeWhile (< n) fibs
```

**What changes vs seed:** Different evaluation strategy: relies on lazy generation of an infinite list. `fibs` is defined via `zipWith` on itself — classic Haskell idiom.

**QC trap:** If `n = 0`, result is `[]` (correctly). If `n = 1`, result is `[0]`. The strict-evaluation trap: avoid `takeWhile (< n) (take 100 fibs)` — the inner `take` forces 100 values even if you only need 5.

### Mutation 12 — biggerThan (lazy length comparison — the LazyNaturals fast-compare)

**Spec:** Compare a list's length against an `Int` *without* forcing the whole list. The trick is to compare lazily-built `Nat`s: structural recursion stops at the first `Succ`/`Zero` difference, so it terminates even when the list is infinite. This is the LazyNaturals lecture's central example. Reuses the family's `Nat` / `lengthNat` / `toNat` (Mutations 4–5).

**Type sig:** `checkLengthBiggerThan :: [a] -> Int -> Bool`

```haskell
-- biggerThan: lazy structural comparison, terminates on infinite lists
biggerThan :: Nat -> Nat -> Bool
Zero     `biggerThan` _        = False
(Succ _) `biggerThan` Zero     = True
(Succ x) `biggerThan` (Succ y) = x `biggerThan` y

checkLengthBiggerThan :: [a] -> Int -> Bool
checkLengthBiggerThan xs n = lengthNat xs `biggerThan` toNat n
```

**Why distinct:** Unlike Mutation 5's `lengthNat`/`toNat` (which only *build* lazy Nats), this consumes two Nats and short-circuits on the first constructor mismatch — so `length xs > n` becomes decidable on infinite `xs`. `length xs > n` in `Int` would diverge; this does not.

**QC trap:** Terminates on `[1..]` because `biggerThan` only forces as many `Succ`s as it needs: `checkLengthBiggerThan [1..] 5 == True` (it reaches `Succ` six times and stops). Also `checkLengthBiggerThan [1,2,3] 5 == False`. Because `Nat` has `deriving Ord` (Mutation 4) and structural `compare` short-circuits the same way, you can skip `biggerThan` entirely and write `lengthNat xs > toNat n` — e.g. `lengthNat [1..] > toNat 5 == True` — for the identical lazy result.

## See also

**Primary archetype:** [A18 lazy memo](../archetypes/A18-lazy-memo.md)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md)
**Pitfalls:** [P-023 deepseq exposes lazy undefined](../pitfalls/HIGH-severity.md#p-023)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
