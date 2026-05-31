<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: state-counter**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · **state-counter** · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: state-counter

**Archetype:** A12 (State monad — counter-only variant)   |   **Stars:** ⭐⭐⭐   |   **Course week(s):** 10
**Search keywords:** fresh, counter, labelTree, generate-id, numbering pass, uniqueIds, runState, State Int

## Generator template
```haskell
import Control.Monad.State

-- The seed: an action that takes a step using the counter (= State Int).
-- Either reads it (without consuming), or reads-and-increments (= fresh).
seed :: State Int ResultType
seed = do
  n <- get        -- read current
  put (n + 1)     -- increment
  return n        -- return old (= fresh)
```

This family is a *specialisation* of `state-game-family.md` where the world is a single `Int` counter. Why a separate family? Because counter problems are so common (problems 111, 112, 113, 119, plus all "label tree" variants in exam-style problems) that they deserve their own pattern table.

## Mutations (the examiner picks one)

### Mutation 1 — fresh (= problem 111)
**Sig:** `fresh :: State Int Int`
**Solution:**
```haskell
fresh :: State Int Int
fresh = do
  n <- get
  put (n + 1)
  return n
```
**QC trap:** Returns the OLD value. `runState fresh 0 == (0, 1)`.

### Mutation 2 — freshN (return n consecutive fresh ids)
**Sig:** `freshN :: Int -> State Int [Int]`
**Solution:**
```haskell
freshN :: Int -> State Int [Int]
freshN 0 = return []
freshN n = do
  i  <- fresh
  is <- freshN (n - 1)
  return (i : is)
```
Or: `freshN n = replicateM n fresh`.
**QC trap:** `runState (freshN 3) 0 == ([0,1,2], 3)`.

### Mutation 3 — countLeaves (= problem 113)
**Spec:** Walk a binary tree; increment counter for each leaf.
**Sig:** `countLeaves :: BT a -> State Int ()`
**Solution:**
```haskell
countLeaves :: BT a -> State Int ()
countLeaves Empty                = return ()
countLeaves (Fork _ Empty Empty) = modify (+1)
countLeaves (Fork _ l r)         = do
  countLeaves l
  countLeaves r
```
**QC trap:** `execState (countLeaves t) 0 == leavesCount t` — cross-check via tree-counting family.

### Mutation 4 — labelTree in-order (= problem 112)
See `state-game-family.md` Mutation 4 — labelTree.

### Mutation 5 — labelTree pre-order
**Spec:** Same as 112 but the labels follow pre-order traversal.
**Sig:** `labelPre :: BT a -> BT (Int, a)`
**Solution:**
```haskell
labelPre :: BT a -> BT (Int, a)
labelPre t = evalState (go t) 0
  where
    go Empty        = return Empty
    go (Fork v l r) = do
      i  <- fresh
      l' <- go l
      r' <- go r
      return (Fork (i, v) l' r')
```
**QC trap:** Difference vs labelTree (in-order): `i <- fresh` moves to *before* the left recursion. Same code structure, different binding order.

### Mutation 6 — uniqueIds (= problem 119)
**Sig:** `uniqueIds :: [String] -> State Int [(String, Int)]`
**Solution:**
```haskell
uniqueIds :: [String] -> State Int [(String, Int)]
uniqueIds = mapM (\s -> do i <- fresh; return (s, i))
```
**QC trap:** Result has `length input` pairs. Ids start at the initial counter value.

### Mutation 7 — labelEdges (rose tree variant)
**Spec:** Label every edge of a rose tree (each child carries its index from its parent's perspective).
**Sig:** `labelEdges :: Rose a -> Rose (Int, a)`
**Solution:**
```haskell
data Rose a = Branch a [Rose a]

labelEdges :: Rose a -> Rose (Int, a)
labelEdges t = evalState (go t) 0
  where
    go (Branch v children) = do
      i  <- fresh
      cs <- mapM go children
      return (Branch (i, v) cs)
```
**QC trap:** Variant: label by depth-first traversal across the whole tree (above) vs label per-child-index per-parent (no monad needed). Read the spec.

### Mutation 8 — countAtomsInTree (counter as accumulator)
**Spec:** Walk a syntax tree; count occurrences of every variable.
**Sig:** `countVars :: Expr -> State Int ()`
**Solution:**
```haskell
data Expr = Lit Int | Var String | Add Expr Expr | Mul Expr Expr

countVars :: Expr -> State Int ()
countVars (Var _)     = modify (+1)
countVars (Add e1 e2) = countVars e1 >> countVars e2
countVars (Mul e1 e2) = countVars e1 >> countVars e2
countVars _           = return ()
```
**QC trap:** Counts every `Var` occurrence (including duplicates). For *distinct* variables you need `State (Set String)`.

### Mutation 9 — relabel-by-rank (counter that tracks first-occurrence position)
**Spec:** Replace each list element with its first-occurrence rank.
**Sig:** `rankify :: Eq a => [a] -> [Int]`

> **WARNING - not an allowed import:** `Data.Map.Strict` (and `Data.Map`) are NOT on the exam whitelist — importing either scores **0**. The whitelist is only `Prelude, Data.List, Data.Char, Data.Maybe, Control.Monad, Control.Monad.State, Control.Monad.Writer` plus the question's own Types module. Use the assoc-list version below as your PRIMARY answer; only reach for `Data.Map` if the question's own Types module hands it to you.

**Solution (allowed imports — assoc list `[(a,Int)]` as the state):**
```haskell
import Control.Monad.State   -- the only import this needs

rankify :: Eq a => [a] -> [Int]
rankify xs = evalState (mapM rank xs) []
  where
    rank x = do
      m <- get
      case lookup x m of           -- assoc-list lookup (needs Eq a)
        Just i  -> return i
        Nothing -> do
          let i = length m         -- next rank = number of keys so far
          put (m ++ [(x, i)])      -- append the new (key, rank)
          return i
```
**QC trap:** State here is an assoc list, not just an `Int` — but conceptually it's still a "counter that handles repeat lookups". `rankify "banana" == [0,1,2,1,2,1]` because `length m` grows by 1 on each new key. Note the sig only needs `Eq a` (assoc-list `lookup`), not `Ord a`.

**Data.Map version (NOT whitelisted — for reference only):** if the Types module supplies `Data.Map.Strict`, the same logic is `Map.lookup` / `Map.insert` / `Map.size` over `Map.empty`, and the constraint tightens to `Ord a`.

### Mutation 10 — fresh with reset
**Spec:** Issue ids, but every time `reset` is called, restart from 0.
**Sig:** uses `reset :: State Int ()`
**Solution:**
```haskell
reset :: State Int ()
reset = put 0
```
And `fresh` as before. Sequences mix as usual:
```haskell
exampleSeq :: State Int [Int]
exampleSeq = do a <- fresh; b <- fresh; reset; c <- fresh; return [a,b,c]
-- runState exampleSeq 10 == ([10,11,0], 1)
```
**QC trap:** "Reset" doesn't restore the *id-before-reset* — it just `put 0`s.

## Hidden-predicate mutations
- "Label only leaves" → drop the `i <- fresh` in the `Fork _ l r` branch but keep it in `Fork _ Empty Empty`.
- "Issue ids only for nodes matching predicate" → conditional fresh:
```haskell
maybeFresh :: Bool -> State Int (Maybe Int)
maybeFresh False = return Nothing
maybeFresh True  = Just <$> fresh
```

## Accumulator-style alternative
The whole family is "the state-monad version of an accumulator pass". The pure equivalent:
```haskell
labelInOrder :: BT a -> BT (Int, a)
labelInOrder t = snd (go 0 t)
  where
    go n Empty        = (n, Empty)
    go n (Fork v l r) = let (n1, l') = go n l
                            (n2, r') = go (n1+1) r
                        in  (n2, Fork (n1, v) l' r')
```
Some courses prefer this presentation because it's "no monads".

## Fold-style alternative
Not naturally fold-shaped — counter problems require step-wise state, which is what `mapM` / `foldM` already do.

## Cross-family combinations
- this family + `tree-transform-family.md` → labelTree (transform with State)
- this family + `tree-counting-family.md` → countLeaves (count via State)
- this family + Writer → label *and* log each id
- this family + Reader → counter starting from a Reader-supplied base

## QuickCheck universal attacks
- **State law: `fresh >> fresh` ≡ `do a <- fresh; b <- fresh; return ()`** (when discarding results).
- **`evalState fresh 0 == 0; execState fresh 0 == 1`.**
- **`fst (runState (freshN n) k) == [k..k+n-1]`.**
- **`length (fst (runState (freshN n) k)) == n` for all `n >= 0`.**
- **`execState (mapM_ (const fresh) xs) 0 == length xs`.**
- **labelTree preserves shape: `mapBT snd (labelTree t) == t`.**

## Pitfalls (per mutation)
- M1: returning new value, not old.
- M2: missing the 0 base case.
- M3: incrementing for non-leaves.
- M5: same code as in-order but with `i` first — easy to forget.
- M6: forgetting `do` and writing `\s -> (s, fresh)` (type error).
- M7: rose tree's `mapM` does the children — don't forget.
- M8: missing the `Lit` case (default is `return ()`).
- M9: use the count of keys so far (`length m` for the assoc list, or `Map.size` if the Types module supplies a Map) as the new id; appending a duplicate key must NOT change its rank.
- M10: confusing "reset to 0" with "reset to initial state".


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — freshN (return n fresh integers in one shot)

**Spec:** Return a list of n fresh counter values, incrementing state by n.

**Type sig:** `freshN :: Int -> State Int [Int]`

```haskell
freshN :: Int -> State Int [Int]
freshN n = do
  start <- get
  put (start + n)
  return [start .. start + n - 1]
```

**What changes vs seed:** Vectorised over `fresh` — one State operation produces a list, no recursion. Different recursion shape (none) from the structural `replicateM n fresh`.

**QC trap:** `[start .. start + n - 1]` for `n = 0` is `[start .. start-1]` which is `[]`. The state increments by 0 (idempotent). Correct.

## See also

**Primary archetype:** [A02 state game](../archetypes/A02-state-game.md)
**Sibling families:** [state-game](./state-game-family.md)
**Cross-topic:** [rose × state](../cross-matrix/rose-x-state.md) · [tree × state](../cross-matrix/tree-x-state.md) · [bst × state](../cross-matrix/bst-x-state.md)
**Theory:** [state](../monads/state.md)
**QuickCheck:** [state attacks](../quickcheck/state-attacks.md)
**Pitfalls:** [P-008 n<=0 not n==0](../pitfalls/HIGH-severity.md#p-008)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
