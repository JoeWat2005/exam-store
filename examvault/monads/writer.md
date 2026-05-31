<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Monad: Writer**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · [generic-combinators](./generic-combinators.md) · [io](./io.md) · [list-monad](./list-monad.md) · [maybe](./maybe.md) · [monad-laws](./monad-laws.md) · [monaderror](./monaderror.md) · [multi-effect](./multi-effect.md) · [reader](./reader.md) · [state](./state.md) · [transformer-stack-order](./transformer-stack-order.md) · [transformers](./transformers.md) · **writer**
<!-- siblings:end -->






# Monad: Writer

**Import:** `import Control.Monad.Writer`
**Type:** `newtype Writer w a` — conceptually `(a, w)` with a `Monoid` constraint on `w`.
**Combines with:** State (multi-effect log + state), Maybe.
**Search keywords:** log, trace, accumulate, append, record, tell, history, monoid, Sum, [String], collect.

## Primitive operations

| Operation | Signature | Semantics | Pitfall |
|---|---|---|---|
| `tell`   | `Monoid w => w -> Writer w ()`  | append `w` to running log | put a *list*, not a single element |
| `pure x` | `a -> Writer w a`               | yields `x` with `mempty` log | — |
| `listen` | `Writer w a -> Writer w (a, w)` | exposes the accumulated log so far | rarely needed in exam |
| `censor` | `(w -> w) -> Writer w a -> Writer w a` | transform the log after the fact | rarely needed in exam |

## Run functions

| Runner | Signature | Returns | Use when |
|---|---|---|---|
| `runWriter`  | `Writer w a -> (a, w)` | both result and log | most common |
| `execWriter` | `Writer w a -> w`      | just the log         | "trace only" / "count only" |

Mnemonic: **e**xec keeps just the log; `runWriter` gives you the **r**esult **a**nd log.

## Common choice of `w`

| Effect | `w` type | Note |
|---|---|---|
| line-by-line log     | `[String]`     | `tell ["start"]` (cons-style) |
| flat string log      | `String`       | `tell "step\n"` — uses `++` |
| count "via length"   | `[String]` / `[()]` | `tell ["."]` / `tell [()]`; then `length` |
| numeric total        | `Sum Int` ⚠️    | `tell (Sum 1)`; `getSum` — see import warning below |
| numeric product      | `Product Int` ⚠️ | `tell (Product k)` — see import warning below |
| disjunction of bools | `Any` ⚠️        | `tell (Any True)` — see import warning below |
| conjunction of bools | `All` ⚠️        | `tell (All True)` — see import warning below |
| histogram            | `Map k Int`    | needs `Data.Map` (NOT whitelisted) |

`String` IS a `Monoid` (via `++`), but **`[String]` is usually cleaner** because each log line stays separate.

> **WARNING — `Sum`/`Product`/`Any`/`All` are NOT whitelisted.** They live in `Data.Monoid`, and current `mtl` does **not** re-export `Data.Monoid` from `Control.Monad.Writer`. With only `import Control.Monad.Writer`, `Sum` is *not in scope* (`ghc` says "Not in scope: type constructor `Sum`"). The only way to get them is `import Data.Monoid (Sum(..))`, which is **NOT on the exam allow-list → scores 0.** For counting/totals, prefer a `[String]`/`[()]` log + `length`, carry an `Int` via `Control.Monad.State`, or a local `newtype` with a hand-written `Monoid` instance (legal under `-XSafe`, no import). Only reach for `Sum`/`Product` if **the question's own Types module already provides it**.

## When to reach for Writer

- "Log every step of the computation."
- "Record the sequence of recursive arguments."
- "Count the number of multiplications/comparisons" — log one entry per event into a `[String]`/`[()]` and take `length` (whitelist-safe). *(`Sum Int` also works but needs the non-whitelisted `Data.Monoid` — avoid unless Types provides it.)*
- "Trace the path through a tree."
- "Collect all the leaves you pass through."

If you'd also *read* the accumulator at every step, use State instead.

## Canonical templates

### Trace recursion (the `fib4` lecture example)
```haskell
fib4 :: Integer -> Writer [Integer] Integer
fib4 n
 | n <  0 = error "negative"
 | n == 0 = pure 0
 | n == 1 = pure 1
 | otherwise = do
     tell [n]
     x <- fib4 (n - 2)
     y <- fib4 (n - 1)
     pure (x + y)

-- runWriter (fib4 11) == (89, [11,9,7,5,3,2,4,2,3,2,6,...])
```

### Log factorial — problem 107
```haskell
logFactorial :: Int -> Writer [String] Int
logFactorial 0 = pure 1
logFactorial n = do
  tell ["multiplying by " ++ show n]
  k <- logFactorial (n - 1)
  pure (n * k)
```

### Count steps (Collatz) — problem 108 — WHITELIST-SAFE (primary)
```haskell
-- Log one entry per step, then take length. Only Control.Monad.Writer needed.
countSteps :: Int -> Writer [String] Int
countSteps 1 = pure 1
countSteps n = do
  tell ["step"]
  if even n then countSteps (n `div` 2) else countSteps (3*n + 1)

-- number of steps:  length (execWriter (countSteps 27)) == 111
```

The same idea with `Writer [()]` (`tell [()]`) or by carrying an `Int` through
`Control.Monad.State` (`modify (+1)`, then `execState ... 0`) is equally safe.
If you genuinely want a monoidal `Int`, write a local `newtype` — legal under
`-XSafe`, no import:

```haskell
newtype Count = Count Int
getCount :: Count -> Int
getCount (Count n) = n
instance Semigroup Count where Count a <> Count b = Count (a + b)
instance Monoid    Count where mempty = Count 0

countSteps' :: Int -> Writer Count Int
countSteps' 1 = pure 1
countSteps' n = do
  tell (Count 1)
  if even n then countSteps' (n `div` 2) else countSteps' (3*n + 1)
-- getCount (execWriter (countSteps' 27)) == 111
```

> **Aside — only if the Types module provides `Sum`:** the classic
> `Writer (Sum Int)` version below requires `import Data.Monoid (Sum(..))`,
> which is **NOT whitelisted (scores 0)**. Do not copy it unless the question's
> own Types module already exports `Sum`.
> ```haskell
> import Data.Monoid (Sum(..))   -- NOT an allowed import on its own
> countStepsSum :: Int -> Writer (Sum Int) Int
> countStepsSum 1 = pure 1
> countStepsSum n = do
>   tell (Sum 1)
>   if even n then countStepsSum (n `div` 2) else countStepsSum (3*n + 1)
> -- snd (runWriter (countStepsSum 27)) == Sum {getSum = 111}
> ```

### Trace a tree traversal (enter/leave style)
```haskell
logTraverse :: BT a -> Writer [String] ()
logTraverse Empty        = tell ["Empty"]
logTraverse (Fork x l r) = do
  tell ["enter"]
  logTraverse l
  logTraverse r
  tell ["leave"]
```

### Accumulate visited leaves
```haskell
collectLeaves :: BT a -> Writer [a] ()
collectLeaves Empty                = pure ()
collectLeaves (Fork x Empty Empty) = tell [x]
collectLeaves (Fork _ l r)         = do
  collectLeaves l
  collectLeaves r
```

## Question families this monad belongs to

- [`../question-families/writer-trace-family.md`](../question-families/writer-trace-family.md) — the main Writer family (logFactorial, countSteps, traceEval, …)
- [`../question-families/state-counter-family.md`](../question-families/state-counter-family.md) — when counting via State beats Writer
- [`../question-families/list-fold-family.md`](../question-families/list-fold-family.md) — fold-with-log over a list

## QuickCheck traps

- `runWriter (pure x)` MUST give `(x, mempty)` — not `(x, [])` accidentally typed where `Sum Int` is expected.
- For `Sum Int`, your test compares `getSum (snd (runWriter ...)) == expected`.
- The order of log entries matters — entering left subtree before right etc.; auto-marker checks the list.
- Using `tell x` where `x` should be `tell [x]` (i.e. forgetting the list constructor) — compile error or wrong type, easy to debug.

## Pitfalls

- **`tell x` vs `tell [x]`** — for `Writer [a] _`, you write `tell [x]` to add one element. Writing `tell x` (a single `a`) is a TYPE ERROR.
- `tell ""` for `String` log adds nothing — fine but pointless.
- Need `Monoid w` — raw `Int` is NOT a monoid. `Sum`/`Product` come from `Data.Monoid`, which is **NOT whitelisted and is NOT re-exported by `Control.Monad.Writer`** (verified: with only that import, `Sum` is "Not in scope"). Whitelist-safe options: a `[String]`/`[()]` log + `length`, an `Int` via `Control.Monad.State`, or a local `newtype` with a hand-written `Monoid`.
- `Writer` is lazy in its accumulator → space leaks on huge logs. Not usually a problem in 2-hour exams.
- `Writer w a` — `w` is FIRST type param (just like `State s a`).
- The signature shown in 107 is `Writer [String] Int`, NOT `Writer [String] ()`. You still return the factorial.

## Worked examples

- Problem 107 (`logFactorial`) and 108 (`countSteps`).
- `fib4` from `monads.md`.

## See also

**Archetypes:** [A15 writer trace](../archetypes/A15-writer-trace.md)
**Cross-topic:** [tree × writer](../cross-matrix/tree-x-writer.md) · [bst × writer](../cross-matrix/bst-x-writer.md) · [rose × writer](../cross-matrix/rose-x-writer.md) · [list × writer](../cross-matrix/list-x-writer.md)
**Question families:** [writer-trace](../question-families/writer-trace-family.md)
**QuickCheck:** [writer attacks](../quickcheck/writer-attacks.md)
**Related (monads):** [transformers](./transformers.md) · [multi effect](./multi-effect.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
