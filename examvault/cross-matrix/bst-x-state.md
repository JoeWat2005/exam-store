<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: BST × State**

<!-- siblings:start -->
> **Peers:** **bst × state** · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: BST × State

**Why this combo:** a BST insertion that allocates fresh IDs (autoincrementing keys, version numbers, timestamps) needs to thread a counter through the insertion. State is the natural carrier — the counter is hidden, the insert function just `get`s a fresh ID and `put`s the next one.

**Recognition triggers:**
- "Insert with auto-generated key"
- "Build a BST where each value gets a unique ID"
- "Track number of insertions"
- "BST whose nodes carry (id, payload)"

**Search keywords:** BST insert State, fresh ID BST, labelled BST, State Int insert, autoinc BST

## Pattern (insert-with-fresh-id)

```haskell
import Control.Monad.State

data BST k v = Empty | Node k v (BST k v) (BST k v) deriving Show

-- A BST keyed by Int IDs, payload v.
-- Each insertion gets a fresh ID.

insertFresh :: Ord k => k -> v -> BST k v -> State Int (BST k v)
insertFresh k v Empty = do
  modify (+1)        -- counter unused here, but for completeness
  return (Node k v Empty Empty)
insertFresh k v (Node k' v' l r) = case compare k k' of
  LT -> do l' <- insertFresh k v l; return (Node k' v' l' r)
  GT -> do r' <- insertFresh k v r; return (Node k' v' l r')
  EQ -> return (Node k v Empty Empty)   -- replace
```

But the more interesting variant: BST keyed by a *fresh* ID, where insertion order determines the key.

## Worked variants

### BST where the key IS the fresh ID

```haskell
data IBST a = IEmpty | INode Int a (IBST a) (IBST a) deriving Show

insertAutoId :: a -> IBST a -> State Int (IBST a)
insertAutoId v t = do
  newId <- get
  put (newId + 1)
  return (insertById newId v t)
  where
    insertById n x IEmpty = INode n x IEmpty IEmpty
    insertById n x (INode k y l r)
      | n < k  = INode k y (insertById n x l) r
      | n > k  = INode k y l (insertById n x r)
      | otherwise = INode n x l r   -- shouldn't happen for fresh

-- Build a BST from a list of values, each getting a fresh id:
buildBST :: [a] -> IBST a
buildBST xs = evalState (foldM (flip insertAutoId) IEmpty xs) 0
```

### BST where node stores (id, value)

```haskell
data BSTL a = LEmpty | LNode a (Int, a) (BSTL a) (BSTL a)
-- Top-key Ord, stored payload (id, val)

insertWithId :: Ord a => a -> BSTL a -> State Int (BSTL a)
insertWithId x LEmpty = do
  n <- get
  put (n + 1)
  return (LNode x (n, x) LEmpty LEmpty)
insertWithId x t@(LNode k p l r) = case compare x k of
  LT -> do l' <- insertWithId x l; return (LNode k p l' r)
  GT -> do r' <- insertWithId x r; return (LNode k p l r')
  EQ -> return t                       -- already present
```

### Build BST from list, threading counter

```haskell
buildBSTL :: Ord a => [a] -> (BSTL a, Int)
buildBSTL xs = runState (build xs) 0
  where
    build []     = return LEmpty
    build (x:xs) = do
      t <- build xs
      insertWithId x t

-- Or fold:
buildBSTL' xs = runState (foldM (flip insertWithId) LEmpty xs) 0
```

### Count insertions (`execState`)

```haskell
countInserts :: Ord a => [a] -> Int
countInserts xs = execState (foldM (flip insertWithId) LEmpty xs) 0
```

### `fresh` primitive

```haskell
fresh :: State Int Int
fresh = do n <- get; put (n+1); return n

insertWithIdClean :: Ord a => a -> BSTL a -> State Int (BSTL a)
insertWithIdClean x LEmpty = do
  n <- fresh
  return (LNode x (n, x) LEmpty LEmpty)
insertWithIdClean x t@(LNode k p l r) = case compare x k of
  LT -> do l' <- insertWithIdClean x l; return (LNode k p l' r)
  GT -> do r' <- insertWithIdClean x r; return (LNode k p l r')
  EQ -> return t
```

## Mutations

- **State carries (counter, log)** — combine with Writer.
- **State carries (counter, list-of-keys-inserted)** — track insertion history.
- **Insert with custom comparator** — pass a `compare`-like Reader.
- **Deletion with counter** — track removals.

## QuickCheck attacks

```haskell
-- Fresh IDs are all distinct
prop_ids_distinct :: [Int] -> Bool
prop_ids_distinct xs =
  let (t, _) = buildBSTL xs
      ids    = map fst (toListIds t)
  in nub ids == ids

-- Number of nodes == number of unique values inserted
prop_node_count :: [Int] -> Bool
prop_node_count xs =
  let (t, _) = buildBSTL xs
  in size t == length (nub xs)

-- Final counter == number of unique values inserted
prop_final_counter :: [Int] -> Bool
prop_final_counter xs =
  let (_, n) = buildBSTL xs
  in n == length (nub xs)

-- BST invariant holds
prop_bst_invariant :: [Int] -> Bool
prop_bst_invariant xs = isBST (fst (buildBSTL xs))
```

## Pitfalls

- **`fresh` defined once and reused.** Don't inline `do n <- get; put (n+1); return n` everywhere — define once.
- **`foldM` vs explicit recursion**: `foldM (flip insertWithId) Empty xs` is the idiom.
- **`flip insertWithId`** because `foldM` expects `(acc -> elem -> m acc)`, but `insertWithId :: elem -> acc -> m acc`.
- **State threaded automatically** — no extra arg in recursive calls.
- **`evalState` for the tree only**, `execState` for the counter only, `runState` for both.
- **Counter starts at 0 unless asked otherwise** — the marker may want `runState (...) 1`.
- **Don't `tell` insertions** — that's Writer; this is State.
- **Insertion may not always increment** — if `EQ` returns existing, you might want to NOT consume a fresh id (depends on the spec).

## See also

**Combined archetypes:** [A11 BST ops](../archetypes/A11-bst-ops.md) · [A02 state game](../archetypes/A02-state-game.md)
**Theory:** [BST](../trees/bst.md) · [State](../monads/state.md)
**Question families:** [bst-ops](../question-families/bst-ops-family.md) · [state-counter](../question-families/state-counter-family.md)
**QuickCheck:** [bst attacks](../quickcheck/bst-attacks.md) · [state attacks](../quickcheck/state-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
