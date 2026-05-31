<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Tree × Maybe**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · **tree × maybe** · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Tree × Maybe

**Why this combo:** Maybe gives you *short-circuiting failure* at any node of the tree. The first `Nothing` aborts the whole traversal — no further node is visited. This is the obvious encoding of "search may fail" or "may not find a path" or "validation may reject".

**Recognition triggers:**
- "Look up a value in the tree; return Nothing if absent"
- "Compute a path to a target; Nothing if not present"
- "Partially evaluate; Nothing if any subtree is invalid"
- "Find the leftmost / rightmost / nearest matching element"

**Search keywords:** Maybe BT, safe lookup tree, findPath tree, BT Maybe, partial tree, isJust tree, find tree, lookup BST

## Pattern (safe BST lookup)

```haskell
data BT a = Empty | Fork a (BT a) (BT a) deriving Show

lookupBST :: Ord a => a -> BT a -> Maybe a
lookupBST _ Empty = Nothing
lookupBST k (Fork x l r) = case compare k x of
  EQ -> Just x
  LT -> lookupBST k l
  GT -> lookupBST k r
```

## Worked variants

### Find path (Just [LeftRight directions] to target, Nothing if missing)

```haskell
data Dir = L | R deriving Show

findPath :: Eq a => a -> BT a -> Maybe [Dir]
findPath _ Empty = Nothing
findPath k (Fork x l r)
  | k == x = Just []
  | otherwise = case findPath k l of
      Just ds -> Just (L : ds)
      Nothing -> case findPath k r of
        Just ds -> Just (R : ds)
        Nothing -> Nothing
```

Idiomatic with Alternative:
```haskell
findPath' :: Eq a => a -> BT a -> Maybe [Dir]
findPath' _ Empty = Nothing
findPath' k (Fork x l r)
  | k == x    = Just []
  | otherwise = ((L:) <$> findPath' k l) <|> ((R:) <$> findPath' k r)
```

### Safe partial evaluator

```haskell
data Expr = Lit Int | Div Expr Expr

safeEval :: Expr -> Maybe Int
safeEval (Lit n) = Just n
safeEval (Div e1 e2) = do
  x <- safeEval e1
  y <- safeEval e2
  if y == 0 then Nothing else Just (x `div` y)
```

The `do`-block in Maybe propagates `Nothing` from any subcomputation automatically.

### Find first element matching predicate (in-order)

```haskell
findBT :: (a -> Bool) -> BT a -> Maybe a
findBT _ Empty = Nothing
findBT p (Fork x l r) =
  findBT p l <|> (if p x then Just x else Nothing) <|> findBT p r
```

The `<|>` chains alternatives; first `Just` wins.

### Drop a subtree on failure (mapMTree specialisation)

```haskell
mapMTreeMaybe :: (a -> Maybe b) -> BT a -> Maybe (BT b)
mapMTreeMaybe _ Empty = Just Empty
mapMTreeMaybe f (Fork x l r) = do
  v' <- f x
  l' <- mapMTreeMaybe f l
  r' <- mapMTreeMaybe f r
  return (Fork v' l' r')

-- Use: if ANY node returns Nothing, the WHOLE tree is Nothing.
```

### Safe-map-with-pruning (keep valid subtrees only)

```haskell
pruneInvalid :: (a -> Maybe b) -> BT a -> BT b
pruneInvalid _ Empty = Empty
pruneInvalid f (Fork x l r) = case f x of
  Just y  -> Fork y (pruneInvalid f l) (pruneInvalid f r)
  Nothing -> Empty  -- prune at first invalid node
```

(Notice this is NOT `mapMTreeMaybe` — that aborts globally; this prunes locally.)

## Mutations

- **Find ALL paths to value** → switch to list monad ([list-x-list-monad.md](list-x-list-monad.md)).
- **First-fail vs collect-failures** → switch to Either or `[String]`.
- **Different traversal order** (DFS vs BFS) — change function call order.
- **`<|>` chain order** → left-bias (`l <|> r`) vs right-bias (`r <|> l`).
- **Combine with Reader for env-dependent failure** → see [tree-x-multi](expr-x-multi.md).

## QuickCheck attacks

```haskell
-- If the value is in the tree, lookup succeeds
prop_lookup_present :: Int -> BT Int -> Bool
prop_lookup_present k t =
  k `elem` toList t ==> isJust (findBT (==k) t)

-- If lookup returns Just y, then y satisfies predicate
prop_lookup_sound :: (Int -> Bool) -> BT Int -> Property
prop_lookup_sound p t = case findBT p t of
  Just y  -> property (p y)
  Nothing -> property True

-- mapMTreeMaybe with always-Just is Just (Total)
prop_mapM_total :: BT Int -> Bool
prop_mapM_total t = mapMTreeMaybe Just t == Just t

-- mapMTreeMaybe with always-Nothing is Nothing for non-Empty
prop_mapM_dead :: BT Int -> Property
prop_mapM_dead t = isEmpty t || mapMTreeMaybe (const Nothing) t == (Nothing :: Maybe (BT Int))
```

## Pitfalls

- **Short-circuit vs prune**: `mapMTreeMaybe` aborts globally; `pruneInvalid` recovers per-subtree. Pick the right semantics.
- **Alternative on Maybe** is left-biased: `Just 1 <|> Just 2 = Just 1`. Order matters for "find first".
- **`isJust`/`fromJust`** in code is a smell — prefer pattern-match or `<|>` chain.
- **`findBT _ Empty`** must be `Nothing`, not `Just _` — empty has nothing.
- **`case compare ... of`** is the BST lookup idiom — don't repeat `<`, `==`, `>` separately.
- **Don't propagate manually**: `do` over Maybe IS automatic propagation. Reaching for `case` everywhere = missed idiom.

## Pattern comparison: tree×Maybe vs tree×Either

| Feature | Maybe | Either e |
|---|---|---|
| Fail-with-message | no | yes |
| Cost of failure | 0 | message stored |
| `<\|>` recovery | yes (Alternative) | depends on `Monoid e` |
| Use when | binary fail/succeed | named error / context |

## See also

**Combined archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A08 env eval](../archetypes/A08-env-eval.md)
**Theory:** [binary tree](../trees/binary-tree.md) · [Maybe](../monads/maybe.md)
**Question families:** [tree-extract](../question-families/tree-extract-family.md) · [env-eval](../question-families/env-eval-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md) · [maybe-either attacks](../quickcheck/maybe-either-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
