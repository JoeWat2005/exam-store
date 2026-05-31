<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: BST × Writer**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · **bst × writer** · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: BST × Writer

**Why this combo:** when you want to *audit* a sequence of BST operations — which path the insert took, which subtree was rebalanced, which keys were deleted — Writer is the cleanest tool. The log records every comparison; the BST result is unchanged.

**Recognition triggers:**
- "Trace insert/delete steps"
- "Log path taken by lookup"
- "Record every comparison made"
- "Build BST AND produce step-by-step log"

**Search keywords:** Writer BST, log insert, trace BST, BST audit, tell BST, insertion log

## Pattern (insert-with-trace)

```haskell
import Control.Monad.Writer

data BST a = Empty | Node a (BST a) (BST a) deriving Show

insertLog :: (Ord a, Show a) => a -> BST a -> Writer [String] (BST a)
insertLog x Empty = do
  tell ["insert " ++ show x ++ " at empty"]
  return (Node x Empty Empty)
insertLog x t@(Node y l r) = case compare x y of
  LT -> do
    tell [show x ++ " < " ++ show y ++ " : descending left"]
    l' <- insertLog x l
    return (Node y l' r)
  GT -> do
    tell [show x ++ " > " ++ show y ++ " : descending right"]
    r' <- insertLog x r
    return (Node y l r')
  EQ -> do
    tell [show x ++ " already present"]
    return t
```

Run with `runWriter` to get `(BST, [String])`.

## Worked variants

### Trace a delete operation

```haskell
deleteLog :: (Ord a, Show a) => a -> BST a -> Writer [String] (BST a)
deleteLog x Empty = do
  tell ["delete " ++ show x ++ ": not found"]
  return Empty
deleteLog x t@(Node y l r) = case compare x y of
  LT -> do
    tell [show x ++ " < " ++ show y ++ " : descending left"]
    l' <- deleteLog x l
    return (Node y l' r)
  GT -> do
    tell [show x ++ " > " ++ show y ++ " : descending right"]
    r' <- deleteLog x r
    return (Node y l r')
  EQ -> do
    tell ["found " ++ show x ++ " : deleting"]
    deleteRoot t

deleteRoot :: Show a => BST a -> Writer [String] (BST a)
deleteRoot Empty = return Empty
deleteRoot (Node _ Empty r) = do tell ["replace with right"];  return r
deleteRoot (Node _ l Empty) = do tell ["replace with left"];   return l
deleteRoot (Node _ l r) = do
  tell ["pick min from right"]
  let (m, r') = extractMin r
  tell ["min is " ++ show m]
  return (Node m l r')

extractMin :: BST a -> (a, BST a)
extractMin (Node x Empty r) = (x, r)
extractMin (Node x l r)     = let (m, l') = extractMin l in (m, Node x l' r)
```

### Trace a lookup (returns Maybe)

```haskell
lookupLog :: (Ord a, Show a) => a -> BST a -> Writer [String] (Maybe a)
lookupLog x Empty = do
  tell ["lookup " ++ show x ++ " : not found"]
  return Nothing
lookupLog x (Node y l r) = case compare x y of
  EQ -> do tell ["found " ++ show x]; return (Just y)
  LT -> do tell ["LT " ++ show y]; lookupLog x l
  GT -> do tell ["GT " ++ show y]; lookupLog x r
```

### Count comparisons (whitelist-safe)

> **WARNING — not an allowed import:** `Sum`/`Product`/`Any`/`All` are in `Data.Monoid` (and `Max`/`Min` in `Data.Semigroup`), which are NOT on the exam whitelist and are NOT re-exported by `Control.Monad.Writer` (`import Control.Monad.Writer` alone gives 'Not in scope: Sum'). To count/total with only allowed imports, use a `Writer [()]`/`Writer [String]` log + `length`, carry an `Int` via `Control.Monad.State`, or define a local `newtype` with a hand-written `Monoid`. Use the `Sum` form only if the question's own `Types` module provides it.

**Primary** — log one `()` per comparison, then take `length`. Only `Control.Monad.Writer` needed:

```haskell
countCompare :: Ord a => a -> BST a -> Writer [()] (Maybe a)
countCompare _ Empty = return Nothing
countCompare x (Node y l r) = do
  tell [()]                     -- one compare
  case compare x y of
    EQ -> return (Just y)
    LT -> countCompare x l
    GT -> countCompare x r

-- Total compares for a sequence:
totalCompares :: Ord a => [a] -> BST a -> Int
totalCompares xs t = length $ execWriter $ mapM_ (\k -> countCompare k t) xs
```

Carrying an `Int` through `Control.Monad.State` is equally safe (`modify (+1)` per comparison, then `execState ... 0`).

**Only if `Types` provides `Sum`** (needs `import Data.Monoid (Sum(..))`, NOT whitelisted → scores 0):

```haskell
import Data.Monoid (Sum(..))   -- NOT an allowed import on its own
countCompareSum :: Ord a => a -> BST a -> Writer (Sum Int) (Maybe a)
countCompareSum _ Empty = return Nothing
countCompareSum x (Node y l r) = do
  tell (Sum 1)
  case compare x y of
    EQ -> return (Just y)
    LT -> countCompareSum x l
    GT -> countCompareSum x r

-- totalComparesSum xs t = getSum $ execWriter $ mapM_ (\k -> countCompareSum k t) xs
```

### Building BST from a list, log each step

```haskell
buildLog :: (Ord a, Show a) => [a] -> Writer [String] (BST a)
buildLog = foldM (flip insertLog) Empty
```

### Combined State + Writer (id-tracking with trace)

```haskell
import Control.Monad.State

type BSTM a = StateT Int (Writer [String]) (BST a)

-- (or model directly with a tuple `State (Int, [String])`, see expr-x-multi.md)
```

(Multi-effect; usually outside basic exam scope, but possible.)

## Mutations

- **Log granularity**: per-comparison / per-step / per-major-event.
- **Different `w` choice**: `[String]` / `String` / `[()]` + `length` (whitelist-safe) / a local `newtype` Monoid / nested log. (`Sum` needs the non-whitelisted `Data.Monoid` — use only if `Types` provides it.)
- **Add indentation by depth**: pass depth as Reader and `tell [replicate (2*d) ' ' ++ msg]`.
- **Multiple operations** (insert + delete + lookup) — each adds to the same log.
- **Compute a metric in addition to log** — use a `([()], [String])` tuple monoid and `length` the first component (whitelist-safe). (`(Sum Int, [String])` works too but needs the non-whitelisted `Data.Monoid`.)

## QuickCheck attacks

```haskell
-- Result tree matches non-logging insert
prop_log_insert_matches :: Int -> BST Int -> Bool
prop_log_insert_matches x t =
  fst (runWriter (insertLog x t)) == insertPure x t

-- Log length proportional to descent depth
prop_log_length :: Int -> BST Int -> Bool
prop_log_length x t =
  length (snd (runWriter (insertLog x t))) <= depth t + 1

-- Total compares for a list bounded by length * depth
prop_total_compares_bounded :: [Int] -> BST Int -> Property
prop_total_compares_bounded ks t = not (null ks) ==>
  totalCompares ks t <= length ks * depth t

-- Log contains "found" iff value was in tree
prop_log_contains_found :: Int -> BST Int -> Bool
prop_log_contains_found x t =
  let (r, log) = runWriter (lookupLog x t)
  in isJust r == any ("found" `isInfixOf`) log
```

## Pitfalls

- **`tell` per comparison** is verbose — sometimes you want `tell` only at meaningful steps (descent direction, found/not-found).
- **`[String]` order matters** — accumulates in `tell` order. Reverse-iterate the tree → reverse log.
- **`execWriter` for log only**, `runWriter` for both.
- **`foldM` for sequenced inserts** — `mapM_` discards the result; we want the final tree.
- **`flip insertLog`** when using `foldM` (function expects (acc, elem) but we built (elem, acc)).
- **Don't log inside `Empty` insert** unless the spec asks — many specs only log internal nodes.
- **Combining Writer + Maybe** for "trace lookup, allow failure" — pure Writer-of-Maybe works fine.

## See also

**Combined archetypes:** [A11 BST ops](../archetypes/A11-bst-ops.md) · [A15 writer trace](../archetypes/A15-writer-trace.md)
**Theory:** [BST](../trees/bst.md) · [Writer](../monads/writer.md)
**Question families:** [bst-ops](../question-families/bst-ops-family.md) · [writer-trace](../question-families/writer-trace-family.md)
**QuickCheck:** [bst attacks](../quickcheck/bst-attacks.md) · [writer attacks](../quickcheck/writer-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
