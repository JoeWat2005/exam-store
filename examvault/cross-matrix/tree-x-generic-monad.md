<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Tree × Generic Monad m**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · **tree × generic-monad** · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Tree × Generic Monad m

**Why this combo:** when you write your function with `Monad m =>` instead of a specific monad, ONE definition handles `Maybe` (failure), `State` (counters), `Writer` (logs), `IO` (effects), `Either e` (errors), all at once. This is the most reusable shape — the course Mock Test Q2 was exactly this idiom on lists; the tree version generalises it.

**Recognition triggers:**
- "Define `mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)`"
- "Generic over any monad"
- "Apply an effectful function at every node"
- "Filter / fold a tree with a monadic predicate"
- Any signature with `Monad m =>` on a tree.

**Search keywords:** mapMTree, foldMTree, filterMTree, traverseTree, Monad m tree, generic monad tree, mapM BT, mapM Rose, monadic recursion tree

## Pattern (the canonical `mapMTree`)

```haskell
mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)
mapMTree _ Empty        = return Empty
mapMTree f (Fork x l r) = do
  v' <- f x
  l' <- mapMTree f l
  r' <- mapMTree f r
  return (Fork v' l' r')
```

This is the tree analogue of `mapM :: Monad m => (a -> m b) -> [a] -> m [b]`. Same structure: walk every node, run the action, rebuild with the results, all inside `m`.

## Worked variants

### `mapMTree` for Rose

```haskell
data Rose a = Leaf a | Branch [Rose a]

mapMRose :: Monad m => (a -> m b) -> Rose a -> m (Rose b)
mapMRose f (Leaf x)    = do y <- f x; return (Leaf y)
mapMRose f (Branch xs) = do ys <- mapM (mapMRose f) xs; return (Branch ys)

-- or more idiomatically:
mapMRose' f (Leaf x)    = Leaf   <$> f x
mapMRose' f (Branch xs) = Branch <$> mapM (mapMRose' f) xs
```

The outer `mapM` is for `[Rose a]`; the inner `mapMRose'` recurses.

### `mapMTree` for Expr

```haskell
data Expr a = Var a | Lit Int | Add (Expr a) (Expr a) | Mul (Expr a) (Expr a)

mapMExpr :: Monad m => (a -> m b) -> Expr a -> m (Expr b)
mapMExpr _ (Lit n)     = return (Lit n)
mapMExpr f (Var x)     = do y <- f x; return (Var y)
mapMExpr f (Add e1 e2) = do
  e1' <- mapMExpr f e1
  e2' <- mapMExpr f e2
  return (Add e1' e2')
mapMExpr f (Mul e1 e2) = do
  e1' <- mapMExpr f e1
  e2' <- mapMExpr f e2
  return (Mul e1' e2')
```

### `traverseTree` (the Applicative-flavoured analogue)

```haskell
traverseTree :: Applicative f => (a -> f b) -> BT a -> f (BT b)
traverseTree _ Empty        = pure Empty
traverseTree f (Fork x l r) =
  Fork <$> f x <*> traverseTree f l <*> traverseTree f r
```

This IS `traverse` from `instance Traversable BT`. Strictly more general than `mapMTree` — works for any Applicative, not just any Monad. See [typeclasses/traversable.md](../typeclasses/traversable.md).

### `foldMTree` (monadic fold)

```haskell
foldMTree :: Monad m => (b -> a -> b -> m b) -> b -> BT a -> m b
foldMTree _ z Empty        = return z
foldMTree f z (Fork x l r) = do
  bl <- foldMTree f z l
  br <- foldMTree f z r
  f bl x br
```

Usage example — sum of nodes, may fail if any value is negative:
```haskell
safeSum :: BT Int -> Maybe Int
safeSum = foldMTree combine 0
  where
    combine bl x br
      | x < 0     = Nothing
      | otherwise = Just (bl + x + br)
```

### `filterMTree` (drop nodes whose monadic test returns False; preserves shape locally)

```haskell
-- Keep a node only if predicate returns Just True;
-- replace dropped Fork with Empty.
filterMTree :: Monad m => (a -> m Bool) -> BT a -> m (BT a)
filterMTree _ Empty        = return Empty
filterMTree p (Fork x l r) = do
  keep <- p x
  l'   <- filterMTree p l
  r'   <- filterMTree p r
  if keep then return (Fork x l' r')
          else return Empty                -- drop subtree entirely
```

Variant: drop only the value, keep the structure (replace with `Empty` only):
```haskell
filterMTree' :: Monad m => (a -> m Bool) -> BT a -> m [a]
filterMTree' _ Empty        = return []
filterMTree' p (Fork x l r) = do
  keep <- p x
  ls   <- filterMTree' p l
  rs   <- filterMTree' p r
  return $ (if keep then [x] else []) ++ ls ++ rs
```

### `forMTree` (mapMTree with args flipped — like Prelude.forM)

```haskell
forMTree :: Monad m => BT a -> (a -> m b) -> m (BT b)
forMTree = flip mapMTree
```

### `sequenceTree` (turn tree of actions inside-out)

```haskell
sequenceTree :: Monad m => BT (m a) -> m (BT a)
sequenceTree Empty                = return Empty
sequenceTree (Fork mx l r)        = do
  x  <- mx
  l' <- sequenceTree l
  r' <- sequenceTree r
  return (Fork x l' r')

-- equivalent: sequenceTree = mapMTree id
```

### `replicateMTree` (build a tree of fresh values)

If you can produce a single fresh value `m a`, then to build a *specific tree shape* with every node freshly produced:

```haskell
replicateMTree :: Monad m => m a -> BT () -> m (BT a)
replicateMTree act = mapMTree (\() -> act)
```

E.g. fill an unlabelled tree with fresh integers via State:
```haskell
freshN :: State Int Int
freshN = do n <- get; put (n + 1); return n

fillFresh :: BT () -> BT Int
fillFresh t = evalState (replicateMTree freshN t) 0
```

## Instantiating the same `mapMTree` for different effects

```haskell
-- Maybe: short-circuit on failure
mapMTree (\x -> if x > 0 then Just x else Nothing) tree
  -- Nothing if any node has non-positive value

-- State: label every node
mapMTree (\x -> do n <- get; put (n+1); return (n, x)) tree
  -- labels every node 0,1,2,...

-- Writer: log every node visited
mapMTree (\x -> do tell ["visiting " ++ show x]; return x) tree
  -- log of all values visited, in mapMTree's traversal order

-- IO: print each value
mapMTree (\x -> print x >> return x) tree
  -- runs print at every node

-- Either: validate
mapMTree (\x -> if valid x then Right x else Left "bad") tree
```

ONE function — five behaviours, just by changing the monad at the call site.

## Mutations the examiner may inflict

- **Constrain `Monad` to `Applicative`** → use `<$>` / `<*>` instead of `do`.
- **Change tree shape** → BT → Rose → Expr → custom labelled tree.
- **Add a generic effect at a non-leaf** (Forks emit log, leaves don't).
- **Force you to keep the original `x`** alongside the transformed.
- **Combine with filter** → `mapAndFilterMTree`.
- **Order of effects** → "pre-order" vs "in-order" — change order of `<-` lines.
- **Reverse traversal** → call `mapMTree f r` before `l`.

## Specific-monad vs generic-monad

The exam often offers BOTH options. Pick generic:
- Cleaner — one definition.
- Reusable — different call sites with different monads.
- Tests the law-abiding-ness of your code (must work for ALL monads, so you can't cheat).

But sometimes the specific monad is requested — the generic and specific look identical, you just change the type signature:

```haskell
-- Generic:
mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)

-- Specific (State only):
mapMTreeS :: (a -> State Int b) -> BT a -> State Int (BT b)
```

The implementation is byte-for-byte identical — only the signature differs.

## QuickCheck attacks

```haskell
-- Identity: mapMTree return == return
prop_mapM_identity :: BT Int -> Bool
prop_mapM_identity t = runIdentity (mapMTree Identity t) == t

-- Shape preservation
prop_mapM_shape :: BT Int -> Bool
prop_mapM_shape t =
  let r = runIdentity (mapMTree Identity t)
  in countForks r == countForks t

-- Composition (under suitable monads)
prop_mapM_compose :: ...

-- For State: label count equals size of tree
prop_label_count :: BT Int -> Bool
prop_label_count t =
  let labelled = evalState (mapMTree (\x -> do n <- get; put (n+1); return n) t) 0
      n        = size t
  in toList labelled == [0 .. n-1]
```

## Pitfalls

- **Forgetting `return` at the end.** `do v <- f x; l' <- ... ; Fork v l' r'` — wrong, needs `return (Fork v l' r')`.
- **Wrong recursion target.** Calling `mapM f x` where `x` is a `BT a`, not a `[a]`. The `Prelude.mapM` is for lists; you wrote your own for trees.
- **Empty case must `return Empty`**, not just `Empty`.
- **For Rose's `Branch xs`**: must call `mapM (mapMRose f) xs`, NOT `mapMRose f xs` (`xs` is a *list*).
- **Order of `<-` for Empty**: trivial — no `<-` needed.
- **Confusing `mapMTree id` with `sequenceTree`** — they're identical.
- **`forM`/`forMTree` reverses args** — useful when the function is verbose and the structure is short.
- **`Applicative m` is enough** when no `<-` depends on a previous `<-`'s value. Prefer `traverse`-style `<$>`/`<*>`.

## See also

**Combined archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A03 generic monad](../archetypes/A03-generic-monad.md)
**Theory:** [binary tree](../trees/binary-tree.md) · [generic Monad m](../monads/generic-combinators.md)
**Question families:** [tree-transform](../question-families/tree-transform-family.md) · [monad-combinator](../question-families/monad-combinator-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md) · [monad attacks](../quickcheck/monad-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
