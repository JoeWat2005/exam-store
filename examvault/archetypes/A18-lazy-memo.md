<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A18 — Lazy Memoisation via Infinite Data**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · **A18** · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A18 — Lazy Memoisation via Infinite Data

**Tier:** 4   |   **Stars:** ⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** none
**Combines with:** A01 · A06
**Search keywords:** lazy · memoise · memoize · infinite tree · fix · fibBT · memoBT · tstore · tfetch

## What it tests
Whether you can convert an exponential-recursion function (`fib n = fib (n-1) + fib (n-2)`) into a linear-or-better implementation by ROUTING all recursive calls through a single LAZY infinite data structure (list or tree).

## Recognition triggers
- "Memoise Fibonacci" or similar exponential recursion
- `fix`, `fix'`, `let x = f x in x` in the spec
- "Should run instantly for `memoFib 1000`"
- `data BT a = Fork a (BT a) (BT a)` (or any infinite-friendly tree — an infinite memo tree needs no `Empty`)
- Type signature `(Integer -> a) -> (Integer -> a)` (a memoising functor)
- Imports include nothing — pure laziness

## Canonical template
```haskell
-- An infinite memo tree never bottoms out, so it needs NO Empty constructor:
data BT a = Fork a (BT a) (BT a)

fix' :: (a -> a) -> a
fix' f = let x = f x in x

-- Step a recursive function so it takes its own recursive call as an argument:
fibStep :: (Integer -> Integer) -> Integer -> Integer
fibStep _   0 = 0
fibStep _   1 = 1
fibStep rec n = rec (n - 1) + rec (n - 2)

-- A memoiser turns Int -> a into a faster Int -> a:
memo :: (Integer -> a) -> (Integer -> a)
memo f = tfetch (tstore f)

tstore :: (Integer -> a) -> BT a
tstore f = Fork (f 0)
  (tstore (\n -> f (1 + 2*n)))    -- odd numbers
  (tstore (\n -> f (2 + 2*n)))    -- even numbers >0

tfetch :: BT a -> Integer -> a
tfetch (Fork a _ _) 0 = a
tfetch (Fork _ l r) n
  | odd n     = tfetch l ((n - 1) `div` 2)
  | otherwise = tfetch r ((n - 2) `div` 2)

fibFast :: Integer -> Integer
fibFast = fix' (memo . fibStep)
```

## Mutations (the examiner picks one)

### M1 — `fix'` definition
```haskell
fix' :: (a -> a) -> a
fix' f = let x = f x in x
```
What changes: one-liner; the magic is sharing `x`.

### M2 — Factorial via fix
```haskell
factFix :: Int -> Int
factFix = fix' factStep
  where factStep _   0 = 1
        factStep rec n = n * rec (n - 1)
```
What changes: factorial doesn't benefit from memoisation, but illustrates `fix`.

### M3 — `memoList` (list-based memo)
```haskell
memoList :: (Integer -> a) -> (Integer -> a)
memoList f = (map f [0..] !!) . fromIntegral
```
What changes: simpler than BT memo; O(n) lookup not O(log n).

### M4 — `fibList`
```haskell
fibList :: Integer -> Integer
fibList = fix' (memoList . fibStep)
```
What changes: just plug `memoList` in.

### M5 — `tstore` / `tfetch` (above)
See canonical template. Key idea: store at odd indices in left subtree, even indices in right.

### M6 — Infinite-list `fibs` (idiomatic, no memo function)
```haskell
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)
```
What changes: tied-knot style; the list refers to itself.

### M7 — `primes` via lazy sieve
```haskell
primes :: [Int]
primes = sieve [2..]
  where sieve (p:xs) = p : sieve [x | x <- xs, x `mod` p /= 0]
```
What changes: infinite filter; only what you `take` is computed.

### M8 — Infinite `ones`, `cycle'`
```haskell
ones :: [Int]
ones = 1 : ones

cycle' :: [a] -> [a]
cycle' xs = let cs = xs ++ cs in cs
```
What changes: minimal infinite lists; instructive base cases.

### M9 — `Lazy Nat` (problem 134)
```haskell
data Nat = Zero | Succ Nat

addNat :: Nat -> Nat -> Nat
addNat Zero     n = n
addNat (Succ m) n = Succ (addNat m n)

infty :: Nat
infty = Succ infty
```
What changes: data type that uses laziness; `infty` is well-defined but only evaluable lazily.

### M10 — Lazy `lengthNat`
```haskell
lengthNat :: [a] -> Nat
lengthNat []     = Zero
lengthNat (_:xs) = Succ (lengthNat xs)
```
What changes: laziness in the input flows through; `lengthNat [1..] == infty`.

## Worked examples from this course
- Problem sheet Set 14 (#131-137): `ones`, `fibsInfinite`, `primesSieve`, `Lazy Nat`, `lengthNat`, `memoFib`, `fix'`.
- Week 8 lecture: introduces laziness, infinite data, memo trees.
- Practice file: none extensive. `final10.hs` may touch `fix`.

## QuickCheck attack surface
- **`memoFib 1000` returns instantly**: marker times out at ~1s. Naive `fib 1000` takes longer than the lifetime of the universe; memoised should be sub-second.
- **`memoFib 0 == 0`, `memoFib 1 == 1`** — base cases.
- **`take 10 fibs == [0,1,1,2,3,5,8,13,21,34]`**.
- **`take 5 primes == [2,3,5,7,11]`**.
- **`lengthNat [1..] == infty`** — checked structurally up to a depth.
- **No strict eval**: marker may use `seq`/`!` to test; you should NOT.

## Pitfalls (marks-killers)
- **Strict patterns**: `f !x` forces `x`; breaks laziness in the closure.
- **`BangPatterns` pragma**: don't enable it.
- **Calling the unmemoised version recursively**: `fibFast n = ... fibStep fibFast n ...` directly — no sharing happens; each level rebuilds the tree.
- **Calling `memo` on the wrong level**: it MUST go between `fix` and `step`: `fix (memo . step)`.
- **Building a list every call**: `fibList n = (map fib [0..]) !! fromIntegral n` — no sharing across calls because `map` is rebuilt.
- **Using `Int` where `Integer` is needed**: `fib 100` overflows `Int`.

## Combines-with deep dive

### A18 × A01 — memo tree IS a BT
The `tstore`/`tfetch` pair is structural recursion on an infinite BT.

### A18 × A06 — `Functor` for memo
```haskell
mapBT :: (a -> b) -> BT a -> BT b
mapBT f (Fork x l r) = Fork (f x) (mapBT f l) (mapBT f r)

-- memo via fmap:
memoF :: Functor f => f (Integer -> a) -> Integer -> f a
-- (sketch)
```

## See also

**Combines with:** [A09 prelude reimpl](./A09-prelude-reimpl.md)
**Question families:** [lazy-infinite](../question-families/lazy-infinite-family.md)
**Pitfalls:** [P-023 deepseq exposes lazy undefined](../pitfalls/HIGH-severity.md#p-023)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
