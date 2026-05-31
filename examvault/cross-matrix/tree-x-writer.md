<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Tree × Writer**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · **tree × writer** · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Tree × Writer

**Why this combo:** Writer accumulates a *side-channel* (a log of strings, a count, a sum) alongside the main result. Combined with a tree, you can walk every node, return the (possibly transformed) tree, AND produce an audit trail or aggregate metric — both in ONE pass, without mutating state.

**Recognition triggers:**
- "Log every node visited"
- "Count nodes / leaves / forks (via Sum)"
- "Trace the traversal order"
- "Compute X, AND produce a log/metric describing the computation"

**Search keywords:** Writer BT, log tree, tell tree, Sum count tree, execWriter tree, runWriter tree, trace tree

## Pattern (log every value visited, in-order)

```haskell
import Control.Monad.Writer

data BT a = Empty | Fork a (BT a) (BT a)

logTree :: Show a => BT a -> Writer [String] ()
logTree Empty        = return ()
logTree (Fork x l r) = do
  logTree l
  tell ["Visit " ++ show x]
  logTree r

-- Run:
-- snd (runWriter (logTree someTree)) == ["Visit a","Visit b",...]
-- execWriter (logTree someTree)      == ["Visit a","Visit b",...]
```

## Worked variants

### Count nodes (whitelist-safe)

> **WARNING — not an allowed import:** `Sum`/`Product`/`Any`/`All` are in `Data.Monoid` (and `Max`/`Min` in `Data.Semigroup`), which are NOT on the exam whitelist and are NOT re-exported by `Control.Monad.Writer` (`import Control.Monad.Writer` alone gives 'Not in scope: Sum'). To count/total with only allowed imports, use a `Writer [()]`/`Writer [String]` log + `length`, carry an `Int` via `Control.Monad.State`, or define a local `newtype` with a hand-written `Monoid`. Use the `Sum` form only if the question's own `Types` module provides it.

**Primary** — log one `()` per node, then take `length`. Only `Control.Monad.Writer` needed:

```haskell
countNodes :: BT a -> Writer [()] ()
countNodes Empty        = return ()
countNodes (Fork _ l r) = do
  tell [()]
  countNodes l
  countNodes r

-- Run:
length (execWriter (countNodes t))
```

The same idea with `Writer [String]` (`tell ["."]`) or by carrying an `Int` through `Control.Monad.State` works identically:

```haskell
import Control.Monad.State

countNodesS :: BT a -> State Int ()
countNodesS Empty        = return ()
countNodesS (Fork _ l r) = do { modify (+1); countNodesS l; countNodesS r }

-- Run:  execState (countNodesS t) 0
```

**Only if `Types` provides `Sum`** (needs `import Data.Monoid (Sum(..))`, NOT whitelisted → scores 0):

```haskell
import Data.Monoid (Sum(..))   -- NOT an allowed import on its own
countNodesSum :: BT a -> Writer (Sum Int) ()
countNodesSum Empty        = return ()
countNodesSum (Fork _ l r) = do
  tell (Sum 1)
  countNodesSum l
  countNodesSum r

-- Run:  getSum (execWriter (countNodesSum t))
```

### Sum values — value AS a side channel

**Primary (whitelist-safe)** — collect the values into a `[Int]` log, then `sum`:

```haskell
sumValues :: BT Int -> Writer [Int] ()
sumValues Empty        = return ()
sumValues (Fork x l r) = do
  tell [x]
  sumValues l
  sumValues r

-- Run:  sum (execWriter (sumValues t))
```

**Only if `Types` provides `Sum`** (needs `import Data.Monoid (Sum(..))`, NOT whitelisted → scores 0):

```haskell
import Data.Monoid (Sum(..))   -- NOT an allowed import on its own
sumValuesSum :: BT Int -> Writer (Sum Int) ()
sumValuesSum Empty        = return ()
sumValuesSum (Fork x l r) = do
  tell (Sum x)
  sumValuesSum l
  sumValuesSum r

-- Run:  getSum (execWriter (sumValuesSum t))
```

### Trace pre/in/post-order (multi-line log)

```haskell
tracePre :: Show a => BT a -> Writer [String] ()
tracePre Empty        = tell ["()"]
tracePre (Fork x l r) = do
  tell ["pre: "  ++ show x]
  tracePre l
  tracePre r

traceIn :: Show a => BT a -> Writer [String] ()
traceIn Empty        = tell ["()"]
traceIn (Fork x l r) = do
  traceIn l
  tell ["in: "  ++ show x]
  traceIn r

tracePost :: Show a => BT a -> Writer [String] ()
tracePost Empty        = tell ["()"]
tracePost (Fork x l r) = do
  tracePost l
  tracePost r
  tell ["post: " ++ show x]
```

### Map + log (combine result with side-channel)

```haskell
mapAndLog :: Show a => (a -> b) -> BT a -> Writer [String] (BT b)
mapAndLog _ Empty        = return Empty
mapAndLog f (Fork x l r) = do
  tell ["mapping " ++ show x]
  l' <- mapAndLog f l
  r' <- mapAndLog f r
  return (Fork (f x) l' r')
```

### Both a count AND a value (tuple of monoids)

**Primary (whitelist-safe)** — pair a `[()]` counting log with the `[String]` log; the count is the `length` of the first component:

```haskell
analyseTree :: Show a => BT a -> Writer ([()], [String]) ()
analyseTree Empty        = return ()
analyseTree (Fork x l r) = do
  tell ([()], ["Visit " ++ show x])
  analyseTree l
  analyseTree r

-- Run:
let (cs, log) = execWriter (analyseTree t)
in (length cs, log)
```

**Only if `Types` provides `Sum`** (needs `import Data.Monoid (Sum(..))`, NOT whitelisted → scores 0):

```haskell
import Data.Monoid (Sum(..))   -- NOT an allowed import on its own
analyseTreeSum :: Show a => BT a -> Writer (Sum Int, [String]) ()
analyseTreeSum Empty        = return ()
analyseTreeSum (Fork x l r) = do
  tell (Sum 1, ["Visit " ++ show x])
  analyseTreeSum l
  analyseTreeSum r

-- Run:
let (_, (Sum n, log)) = runWriter (analyseTreeSum t)
in (n, log)
```

The tuple monoid `(a, b)` is a monoid iff both components are — `([()], [String])` qualifies with only allowed imports.

### Enter/leave logs (matched pairs)

```haskell
enterLeave :: Show a => BT a -> Writer [String] ()
enterLeave Empty        = return ()
enterLeave (Fork x l r) = do
  tell ["Enter " ++ show x]
  enterLeave l
  enterLeave r
  tell ["Leave " ++ show x]
```

### foldMap via Writer (rederive the Foldable instance)

```haskell
foldMapTree :: Monoid w => (a -> w) -> BT a -> w
foldMapTree f t = execWriter (go t)
  where
    go Empty = return ()
    go (Fork x l r) = do
      go l
      tell (f x)
      go r
```

This shows Writer IS the cheap way to give a Foldable-style aggregation without an explicit Foldable instance.

## Mutations

- **Different monoid w**: `[String]` / `String` / `[()]` or `[Int]` + `length`/`sum` (whitelist-safe) / a local `newtype` Monoid. (`Sum Int` / `Product` / `Max` / `Min` / `Any` / `All` come from `Data.Monoid`/`Data.Semigroup`, which are NOT whitelisted — use only if `Types` provides them.)
- **Different traversal order**: move `tell` before/after subtree-recursion.
- **Combine with State** (counter that's both threaded AND logged) — see [tree-x-multi via Writer+State](expr-x-multi.md).
- **Custom indentation** for nested logs — use `(Endo (++ "  "))` or pass depth as Reader.
- **Conditional logging** — `when condition (tell ["..."])`.

## QuickCheck attacks

```haskell
-- Count via Writer matches manual size (whitelist-safe countNodes :: Writer [()])
prop_countWriter_matches_size :: BT Int -> Bool
prop_countWriter_matches_size t =
  length (execWriter (countNodes t)) == size t

-- Sum via Writer matches manual sum (whitelist-safe sumValues :: Writer [Int])
prop_sumWriter_matches_sum :: BT Int -> Bool
prop_sumWriter_matches_sum t =
  sum (execWriter (sumValues t)) == sum (toList t)

-- Log length equals tree size
prop_log_length :: BT Int -> Bool
prop_log_length t =
  length (execWriter (tracePre t)) == size t + numEmptyForks t

-- Idempotent: extracting value gives ()
prop_value_unit :: BT Int -> Bool
prop_value_unit t = fst (runWriter (countNodes t)) == ()
```

## Pitfalls

- **Plain `Int` is NOT a monoid** — wrap it. Whitelist-safe: log into `[()]`/`[Int]` and `length`/`sum` at the end, or a local `newtype` Monoid. (`Sum Int`/`Product Int` work too but need the non-whitelisted `Data.Monoid` — see the warning above.)
- **`tell w` is required**, NOT `return w` — `return` puts `w` in the result, not the log.
- **Log accumulates left-to-right** in the order `tell` is called. Reordering subtree calls reorders the log.
- **`execWriter` extracts only the log**; `runWriter` gives `(a, w)`; `fst (runWriter ...)` gets value. Pick the right runner.
- **Mempty for tuples**: `mempty :: ([()], [String]) == ([], [])` — Haskell figures it out from context (same for `(Sum 0, [])` if you use the non-whitelisted `Sum`).
- **`Writer w` requires `Monoid w` constraint** on the instance — `instance Monoid w => Monad (Writer w)`.
- **Don't use `tell` outside a Writer monad** — type error.

## Why Writer beats accumulator-passing

You could simulate this with manual `(BT b, [String])` returns:

```haskell
logTreeManual :: Show a => BT a -> [String]
logTreeManual Empty = []
logTreeManual (Fork x l r) = logTreeManual l ++ ["Visit " ++ show x] ++ logTreeManual r
```

Works, but:
- Verbose: every call combines logs manually.
- Doesn't compose with other monad-aware code.
- Doesn't gain `tell`/`pass`/`listen`/`censor` mechanism.

Writer abstracts the accumulation.

## See also

**Combined archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A15 writer trace](../archetypes/A15-writer-trace.md)
**Theory:** [binary tree](../trees/binary-tree.md) · [Writer](../monads/writer.md)
**Question families:** [tree-counting](../question-families/tree-counting-family.md) · [writer-trace](../question-families/writer-trace-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md) · [writer attacks](../quickcheck/writer-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
