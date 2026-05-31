<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Tree × State**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · **tree × state** · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Tree × State

**Why this combo:** State threads a hidden accumulator (a counter, an environment, a buffer) through tree traversal, preserving the tree's shape but enriching every node with state-derived info. The canonical case: **fresh-integer labelling** of every node, in any chosen traversal order.

**Recognition triggers:**
- "Label every node with a unique integer"
- "Number nodes in pre-order / in-order / BFS"
- "Replace each value with (index, value)"
- "Convert a tree to a tree of (id, value) pairs"
- "Allocate a fresh id at every node"

**Search keywords:** labelTree, numberTree, fresh, State Int, BT State, mapM tree, traverse tree State, in-order labelling, pre-order labelling, post-order labelling, BFS labelling

## Pattern (in-order labelling — the canonical Birmingham idiom)

```haskell
import Control.Monad.State

data BT a = Empty | Fork a (BT a) (BT a) deriving Show

labelTree :: BT a -> BT (Int, a)
labelTree t = evalState (go t) 0
  where
    go :: BT a -> State Int (BT (Int, a))
    go Empty        = pure Empty
    go (Fork x l r) = do
      l' <- go l                 -- left first
      n  <- get; put (n + 1)     -- read counter, increment
      r' <- go r                 -- right after
      pure (Fork (n, x) l' r')
```

The order of `<-` lines decides the labelling order. Above: the counter advances between left and right children — IN-ORDER labelling.

## Worked variants

### Pre-order labelling

```haskell
labelPre :: BT a -> BT (Int, a)
labelPre t = evalState (go t) 0
  where
    go Empty        = pure Empty
    go (Fork x l r) = do
      n  <- get; put (n + 1)     -- label THIS node FIRST
      l' <- go l
      r' <- go r
      pure (Fork (n, x) l' r')
```

### Post-order labelling

```haskell
labelPost :: BT a -> BT (Int, a)
labelPost t = evalState (go t) 0
  where
    go Empty        = pure Empty
    go (Fork x l r) = do
      l' <- go l
      r' <- go r
      n  <- get; put (n + 1)     -- label THIS node LAST
      pure (Fork (n, x) l' r')
```

### BFS labelling

You can't do BFS straightforwardly inside a pure recursive monad — you need a queue. Either thread a queue through State, or use `Data.Sequence`:

> **NOT an allowed import — illustration only.** `Data.Sequence` is NOT in the exam whitelist (scores 0). For exam answers use the import-free layered `levels` BFS below, which needs nothing beyond `Prelude`.

```haskell
import qualified Data.Sequence as Q
import Data.Sequence (Seq, (|>), ViewL(..))

labelBFS :: BT a -> BT (Int, a)
labelBFS t = go 0 (Q.singleton t)
  -- conceptually a level-by-level relabeller
```

**Import-free layered BFS** (use this one): collect the tree into levels with `Prelude` only, then number across levels.

```haskell
-- one BFS level at a time: values of the current frontier, then descend to children.
-- Keep only the non-Empty nodes in the frontier so we stop with no trailing [] level.
levels :: BT a -> [[a]]
levels t = go [n | n@(Fork _ _ _) <- [t]]
  where
    go [] = []
    go ts = [x | Fork x _ _ <- ts]
          : go [c | Fork _ l r <- ts, c <- [l, r], notEmpty c]
    notEmpty Empty = False
    notEmpty _     = True
```

(In practice the exam stays with DFS variants; BFS is for completeness.)

### Generic monad version (Traversable / mapM)

If you've declared `Traversable BT`, then the labeller IS `traverse`:

```haskell
labelTrav :: BT a -> BT (Int, a)
labelTrav t = evalState (traverse step t) 0
  where
    step :: a -> State Int (Int, a)
    step x = do n <- get; put (n + 1); pure (n, x)
```

This is gorgeous — the `traverse` handles the shape; `step` is purely state-effecting per element. (Note: the labelling order matches the order `traverse` visits elements, which for the canonical `Traversable BT` instance is in-order.)

### Specific State version (no Traversable)

If the marker requires hand-rolled (no `traverse`):

```haskell
labelTreeS :: BT a -> State Int (BT (Int, a))
labelTreeS Empty        = return Empty
labelTreeS (Fork x l r) = do
  l' <- labelTreeS l
  n  <- get
  put (n + 1)
  r' <- labelTreeS r
  return (Fork (n, x) l' r')
```

Run it: `evalState (labelTreeS t) 0`.

### Variant: label only the leaves (count leaves)

```haskell
labelLeavesOnly :: BT a -> BT (Either Int a)
labelLeavesOnly t = evalState (go t) 0
  where
    go Empty                  = pure Empty
    go (Fork x Empty Empty)   = do  -- a leaf
      n <- get; put (n + 1)
      pure (Fork (Left n) Empty Empty)
    go (Fork x l r)           = do
      l' <- go l
      r' <- go r
      pure (Fork (Right x) l' r')
```

### Variant: rose-tree label (see also rose-x-state.md)

```haskell
data Rose a = Leaf a | Branch [Rose a]

labelRose :: Rose a -> Rose (Int, a)
labelRose t = evalState (go t) 0
  where
    go (Leaf x)    = do n <- get; put (n + 1); pure (Leaf (n, x))
    go (Branch xs) = Branch <$> mapM go xs
```

## Mutations the examiner may inflict

- **Order of `<-` lines** → forces you to pick in/pre/post-order.
- **Initial state** → "start counter at 1, not 0" — only changes `evalState (go t) 1`.
- **State type** → `(Int, [a])`: counter + accumulator buffer of seen values.
- **Mixed payload** → tree of `Either a b` with different counters per branch.
- **Different traversal** → "label only forks, not leaves".
- **Read-only "next id" using `modify`** → `modify (+1)` instead of `get; put`.

## Cleaner state primitive

```haskell
fresh :: State Int Int
fresh = do n <- get; put (n + 1); pure n

-- or:
fresh = state (\n -> (n, n + 1))

-- in-order labelling using fresh:
labelTree' :: BT a -> BT (Int, a)
labelTree' t = evalState (go t) 0
  where
    go Empty        = pure Empty
    go (Fork x l r) = do
      l' <- go l
      n  <- fresh
      r' <- go r
      pure (Fork (n, x) l' r')
```

## QuickCheck attacks

```haskell
-- Shape preserved
prop_labelTree_shape :: BT Int -> Bool
prop_labelTree_shape t = shape (labelTree t) == shape t
  where shape Empty = "_"
        shape (Fork _ l r) = "(" ++ shape l ++ "x" ++ shape r ++ ")"

-- All labels distinct
prop_labelTree_distinct :: BT Int -> Bool
prop_labelTree_distinct t =
  let labels = map fst (toList (labelTree t))
  in nub labels == labels

-- Labels span [0..size-1]
prop_labelTree_span :: BT Int -> Bool
prop_labelTree_span t =
  let labels = sort $ map fst (toList (labelTree t))
      n = size t
  in labels == [0..n-1]

-- Values unchanged
prop_labelTree_values :: BT Int -> Bool
prop_labelTree_values t =
  map snd (toList (labelTree t)) == toList t

-- Idempotent in count: relabel after stripping = labelTree id
prop_labelTree_relabel :: BT Int -> Bool
prop_labelTree_relabel t =
  fmap fst (labelTree t) == fmap fst (labelTree (fmap snd (labelTree t)))
```

## Pitfalls

- **Order of `<-` matters.** Swapping `l' <- go l` and `n <- get` changes pre/in/post-order.
- **`get` followed by `put (n+1)`** is fine, but `modify (+1)` after assigning the OLD value is the bug — you must save `n` first.
- **`pure` for `Empty`**, not `return Empty` to a non-monadic value.
- **`evalState` vs `runState`**: use `evalState` to keep only the value, `execState` for final state (total count), `runState` for both.
- **Counter reset.** Each `labelTree` call starts fresh at 0; if you compose `labelTree . someOp`, you need to be careful about which counter is in scope.
- **Wrong final type.** The output is `BT (Int, a)`, NOT `BT Int` — you must keep the `a` alongside.
- **Don't `tell` here.** `tell` is Writer; this is State.
- **`fresh` defined inline**: `state (\n -> (n, n + 1))` is the slickest one-liner.

## See also

**Combined archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A02 state game](../archetypes/A02-state-game.md)
**Theory:** [binary tree](../trees/binary-tree.md) · [State](../monads/state.md)
**Question families:** [tree-counting](../question-families/tree-counting-family.md) · [state-counter](../question-families/state-counter-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md) · [state attacks](../quickcheck/state-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
