<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Rose × State**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · **rose × state** · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Rose × State

**Why this combo:** Rose trees have *unbounded* children (a list of subtrees), so the labelling/counting pattern uses `mapM` over the list of children instead of `<-` twice. This is the MockTest tree shape — `data Rose a = Leaf a | Branch [Rose a]`.

**Recognition triggers:**
- "Number every node of a rose tree"
- "Assign fresh IDs to leaves only / branches only"
- "Pre-order / post-order labelling of a Rose"
- "Replace each label with (index, label)"

**Search keywords:** Rose State, labelRose, numberRose, fresh Rose, mapM Rose, traverse Rose, Branch [Rose]

## Pattern (label every node in pre-order)

```haskell
import Control.Monad.State

data Rose a = Leaf a | Branch [Rose a] deriving Show

labelRose :: Rose a -> Rose (Int, a)
labelRose t = evalState (go t) 0
  where
    go (Leaf x)    = do n <- get; put (n + 1); return (Leaf (n, x))
    go (Branch xs) = do ys <- mapM go xs; return (Branch ys)
```

The `mapM go xs` is the giveaway — Rose has `[Rose a]`, so the list-of-children is handled by `mapM`.

## Worked variants

### Pre-order with explicit go-fresh

```haskell
fresh :: State Int Int
fresh = do n <- get; put (n+1); return n

labelRosePre :: Rose a -> Rose (Int, a)
labelRosePre t = evalState (go t) 0
  where
    go (Leaf x)    = Leaf . (, x) <$> fresh
    go (Branch xs) = Branch <$> mapM go xs
```

### Post-order

```haskell
labelRosePost :: Rose a -> Rose (Int, a)
labelRosePost t = evalState (go t) 0
  where
    go (Leaf x)    = do n <- fresh; return (Leaf (n, x))    -- leaf is itself last
    go (Branch xs) = do
      ys <- mapM go xs
      return (Branch ys)
```

For a Rose, leaves are themselves the "post" point; branches process children before being labelled.

### Label only leaves

```haskell
labelLeaves :: Rose a -> Rose (Either Int a)
labelLeaves t = evalState (go t) 0
  where
    go (Leaf x)    = do n <- fresh; return (Leaf (Left n))
    go (Branch xs) = Branch <$> mapM go xs

-- Branches are unlabelled (or could be labelled with `Right ()`)
```

### Label only branches (count internal nodes)

```haskell
labelBranches :: Rose a -> Rose a
-- Doesn't actually relabel; but we can count via execState:
countBranches :: Rose a -> Int
countBranches t = execState (go t) 0
  where
    go :: Rose a -> State Int ()
    go (Leaf _)    = return ()
    go (Branch xs) = do
      modify (+1)
      mapM_ go xs
```

### Counter with `Traversable` instance

If you've declared `instance Traversable Rose`:

```haskell
instance Functor Rose where
  fmap f (Leaf x)    = Leaf (f x)
  fmap f (Branch xs) = Branch (map (fmap f) xs)

instance Foldable Rose where
  foldMap f (Leaf x)    = f x
  foldMap f (Branch xs) = foldMap (foldMap f) xs

instance Traversable Rose where
  traverse f (Leaf x)    = Leaf <$> f x
  traverse f (Branch xs) = Branch <$> traverse (traverse f) xs

-- Now labelling is just:
labelRoseT :: Rose a -> Rose (Int, a)
labelRoseT t = evalState (traverse step t) 0
  where step x = do n <- fresh; return (n, x)
```

### Track depth via State (combine counter + depth)

```haskell
labelDepth :: Rose a -> Rose (Int, Int, a)   -- (id, depth, value)
labelDepth t = evalState (go 0 t) 0
  where
    go d (Leaf x)    = do n <- fresh; return (Leaf (n, d, x))
    go d (Branch xs) = Branch <$> mapM (go (d+1)) xs
```

### Replicate fresh values to build a labelled tree

```haskell
relabelAll :: Rose a -> Rose Int
relabelAll = fmap fst . labelRose   -- discard the original payload
```

## Mutations

- **Traversal order**: pre / post / level-order (BFS, requires queue).
- **State type**: `Int` / `(Int, [String])` / a record.
- **Per-level reset of counter** — use `local`-like manual handling.
- **Filter as you go** — combine with Maybe to drop subtrees.
- **Different effect**: State → Writer (log every visit) → Either (validate).

## QuickCheck attacks

```haskell
-- Distinct labels
prop_labelRose_distinct :: Rose Int -> Bool
prop_labelRose_distinct t =
  let labels = collectLabels (labelRose t)
  in nub labels == labels

-- Label count == tree size
prop_labelRose_size :: Rose Int -> Bool
prop_labelRose_size t =
  length (collectLabels (labelRose t)) == roseSize t

-- Shape preserved
prop_labelRose_shape :: Rose Int -> Bool
prop_labelRose_shape t =
  roseSize (labelRose t) == roseSize t

-- Values preserved
prop_labelRose_values :: Rose Int -> Bool
prop_labelRose_values t =
  collectValues (labelRose t) == collectValues t

collectLabels :: Rose (Int, a) -> [Int]
collectLabels (Leaf (n, _)) = [n]
collectLabels (Branch xs)   = concatMap collectLabels xs

roseSize :: Rose a -> Int
roseSize (Leaf _)    = 1
roseSize (Branch xs) = 1 + sum (map roseSize xs)
```

## Pitfalls

- **`mapM go xs` for the list of children**, NOT `go xs` (xs is a list).
- **`Leaf` is the base case**, not `Empty` (Rose has no Empty in MockTest's definition).
- **`Branch []`** is a Branch with no children — legitimate, often used as a marker. Make sure `mapM go []` returns `return []` correctly (it does).
- **`fresh` thrown around naively** can cause off-by-one — count an unused fresh.
- **Don't confuse Rose with BT** — Rose has `[Rose a]`, BT has `BT a` and `BT a`.
- **`<$>` vs `do`**: `Branch <$> mapM go xs` is cleaner than `do ys <- mapM go xs; return (Branch ys)`.
- **Branches without leaves** — `Branch []` has zero values. Make sure your labeller handles it without consuming a fresh ID.

## Why Rose, not BT?

The MockTest used Rose for Q1 (`isNBranching`, `prune`). The labelling/State combo on Rose is just as exam-likely as on BT — sometimes more, because Rose's variable arity makes for richer mutations.

## See also

**Combined archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A02 state game](../archetypes/A02-state-game.md)
**Theory:** [rose tree](../trees/rose-tree.md) · [State](../monads/state.md)
**Question families:** [rose-ops](../question-families/rose-ops-family.md) · [state-counter](../question-families/state-counter-family.md)
**QuickCheck:** [rose attacks](../quickcheck/rose-attacks.md) · [state attacks](../quickcheck/state-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
