<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Rose × Writer**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · **rose × writer** · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Rose × Writer

**Why this combo:** log every visit / count nodes / collect a flattened DFS sequence — all without explicit accumulator threading. Same as `tree-x-writer.md` but with Rose's `[Rose a]` children handled by `mapM_`.

**Recognition triggers:**
- "DFS log of every leaf"
- "Enter/leave trace for every branch"
- "Count branches and leaves separately"
- "Collect all values in traversal order via Writer"

**Search keywords:** Writer Rose, log Rose, dfs Rose Writer, Sum count Rose, execWriter Rose, trace rose

## Pattern (DFS log)

```haskell
import Control.Monad.Writer

data Rose a = Leaf a | Branch [Rose a]

dfsLog :: Show a => Rose a -> Writer [String] ()
dfsLog (Leaf x)    = tell ["leaf " ++ show x]
dfsLog (Branch xs) = do
  tell ["branch ("]
  mapM_ dfsLog xs
  tell [")"]
```

Run with `execWriter (dfsLog t)`.

## Worked variants

### Enter/leave matched pairs

```haskell
enterLeave :: Show a => Rose a -> Writer [String] ()
enterLeave (Leaf x)    = tell ["L " ++ show x]
enterLeave (Branch xs) = do
  tell ["enter"]
  mapM_ enterLeave xs
  tell ["leave"]
```

### Count leaves vs branches separately

> **WARNING — not an allowed import:** `Sum`/`Product`/`Any`/`All` are in `Data.Monoid` (and `Max`/`Min` in `Data.Semigroup`), which are NOT on the exam whitelist and are NOT re-exported by `Control.Monad.Writer` (`import Control.Monad.Writer` alone gives 'Not in scope: Sum'). To count/total with only allowed imports, use a `Writer [()]`/`Writer [String]` log + `length`, carry an `Int` via `Control.Monad.State`, or define a local `newtype` with a hand-written `Monoid`. Use the `Sum` form only if the question's own `Types` module provides it.

**Whitelist-safe (primary)** — count by `length` of a `[()]` log per component (the tuple of two `[()]` monoids is itself a monoid):

```haskell
analyse :: Rose a -> Writer ([()], [()]) ()       -- (leaves, branches)
analyse (Leaf _)    = tell ([()], [])
analyse (Branch xs) = do
  tell ([], [()])
  mapM_ analyse xs

-- Run:
let (ls, bs) = execWriter (analyse t) in (length ls, length bs)
```

**Only if `Types` provides `Sum`** — the classic two-counter version needs `import Data.Monoid (Sum(..))`, which is **NOT whitelisted (scores 0)**:

```haskell
import Data.Monoid (Sum(..))   -- NOT an allowed import on its own
analyseSum :: Rose a -> Writer (Sum Int, Sum Int) ()
analyseSum (Leaf _)    = tell (Sum 1, Sum 0)         -- (leaves, branches)
analyseSum (Branch xs) = do
  tell (Sum 0, Sum 1)
  mapM_ analyseSum xs

-- Run:
let (_, (Sum l, Sum b)) = runWriter (analyseSum t) in (l, b)
```

### Collect all values in pre-order

```haskell
collect :: Rose a -> Writer [a] ()
collect (Leaf x)    = tell [x]
collect (Branch xs) = mapM_ collect xs

-- This recovers `toList`:
preOrderList :: Rose a -> [a]
preOrderList t = execWriter (collect t)
```

### Map and log

```haskell
mapAndLog :: Show a => (a -> b) -> Rose a -> Writer [String] (Rose b)
mapAndLog f (Leaf x) = do
  tell ["map " ++ show x]
  return (Leaf (f x))
mapAndLog f (Branch xs) = do
  tell ["entering branch"]
  ys <- mapM (mapAndLog f) xs
  return (Branch ys)
```

### Depth-aware log (combine with Reader)

```haskell
import Control.Monad.Reader

dfsLogDepth :: Show a => Rose a -> ReaderT Int (Writer [String]) ()
dfsLogDepth (Leaf x) = do
  d <- ask
  tell [replicate (2*d) ' ' ++ "L " ++ show x]
dfsLogDepth (Branch xs) = do
  d <- ask
  tell [replicate (2*d) ' ' ++ "B"]
  local (+1) (mapM_ dfsLogDepth xs)
```

(Uses ReaderT; if the marker doesn't want transformers, pass depth as explicit param.)

### Track frontier (lines list) and totals

**Whitelist-safe (primary)** — pair the `[String]` log with a `[Int]` of the values, then `sum` it at the end (no `Sum` needed):

```haskell
report :: Rose Int -> Writer ([String], [Int]) ()
report (Leaf x)    = tell (["leaf " ++ show x], [x])
report (Branch xs) = do
  tell (["branch"], [])
  mapM_ report xs

-- total: let (_, xs) = execWriter (report t) in sum xs
```

**Only if `Types` provides `Sum`** (needs `import Data.Monoid (Sum(..))`, NOT whitelisted → scores 0):

```haskell
import Data.Monoid (Sum(..))   -- NOT an allowed import on its own
reportSum :: Rose Int -> Writer ([String], Sum Int) ()
reportSum (Leaf x)    = tell (["leaf " ++ show x], Sum x)
reportSum (Branch xs) = do
  tell (["branch"], Sum 0)
  mapM_ reportSum xs
```

## Mutations

- **Monoid choice**: `[String]`, `String`, `[()]`/`[Int]` + `length`/`sum` (whitelist-safe), a local `newtype` Monoid, custom. (`Sum`, `(Sum, Sum)` only if `Types` provides them — `Data.Monoid` is NOT whitelisted.)
- **Traversal order**: pre / post / mixed (mid-Branch log).
- **Conditional logs**: only log Leaves, only log Branches, only matching.
- **Combine with State**: counter + log.

## QuickCheck attacks

```haskell
-- Pre-order list length == size
prop_preOrder_size :: Rose Int -> Bool
prop_preOrder_size t = length (preOrderList t) == numLeaves t

-- Log contains every leaf value (for Show inst)
prop_log_contains_leaves :: Rose Int -> Bool
prop_log_contains_leaves t =
  let log = execWriter (dfsLog t)
      vals = preOrderList t
  in all (\v -> any (("leaf " ++ show v) `isInfixOf`) log) vals

-- Enter count == branch count, leave count == branch count
prop_enter_leave_balanced :: Rose Int -> Bool
prop_enter_leave_balanced t =
  let log = execWriter (enterLeave t)
  in length (filter (== "enter") log) == length (filter (== "leave") log)
```

## Pitfalls

- **`mapM_ f xs`** not `mapM f xs` (we don't need the list of `()`).
- **`tell` accumulates in execution order** — the log reflects whatever order your DFS visits.
- **Branch `[]`** — empty branch. The pattern still matches; `mapM_ f []` returns `return ()`. No log emitted from the inside but enter/leave bracket may still appear.
- **Don't reach for `forM_`** unless you specifically want it for clarity — `mapM_` is the same.
- **`Writer [String]` accumulates by `++`** — for long traces, this is O(n²). For exam scope, fine. For production, use `DList`.
- **Tuple monoid for separate counts** — `(Sum Int, Sum Int)` works only because both components are monoids.

## See also

**Combined archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A15 writer trace](../archetypes/A15-writer-trace.md)
**Theory:** [rose tree](../trees/rose-tree.md) · [Writer](../monads/writer.md)
**Question families:** [rose-ops](../question-families/rose-ops-family.md) · [writer-trace](../question-families/writer-trace-family.md)
**QuickCheck:** [rose attacks](../quickcheck/rose-attacks.md) · [writer attacks](../quickcheck/writer-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
