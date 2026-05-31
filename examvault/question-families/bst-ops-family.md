<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: bst-ops**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · **bst-ops** · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: bst-ops

**Archetype:** A04 + A05 (BT predicate + transform — BST specialization)   |   **Stars:** ⭐⭐⭐   |   **Course week(s):** 6–7
**Search keywords:** isBST, insertBST, memberBST, deleteBST, fromList, min, max, predecessor, successor, bstSort

## Generator template
```haskell
data BT a = Empty | Fork a (BT a) (BT a)

-- The seed: recursive descent down the BT following Ord on the value.
-- For each operation: hit the right subtree if x > v, left if x < v, success at v == x.
seed :: Ord a => a -> BT a -> Result
seed _ Empty                              = baseResult
seed x (Fork v l r)
  | x < v                                 = seed x l (combined-with-this-node)
  | x > v                                 = seed x r (combined-with-this-node)
  | otherwise   {- x == v -}              = matchResult
```

## Mutations (the examiner picks one)

### Mutation 1 — memberBST (= problem 83)
**Sig:** `memberBST :: Ord a => a -> BT a -> Bool`
**Solution:**
```haskell
memberBST :: Ord a => a -> BT a -> Bool
memberBST _ Empty        = False
memberBST x (Fork v l r)
  | x == v               = True
  | x < v                = memberBST x l
  | otherwise            = memberBST x r
```
**QC trap:** O(log n) when balanced, O(n) when skewed. Note: ordering on `==` first is fine — but `<` and `>` would also work and might be slightly idiomatic.

### Mutation 2 — insertBST (= problem 82)
**Sig:** `insertBST :: Ord a => a -> BT a -> BT a`
**Solution:**
```haskell
insertBST :: Ord a => a -> BT a -> BT a
insertBST x Empty            = Fork x Empty Empty
insertBST x t@(Fork v l r)
  | x == v                   = t       -- ignore duplicates
  | x < v                    = Fork v (insertBST x l) r
  | otherwise                = Fork v l (insertBST x r)
```
**QC trap:** "Ignore duplicates" is spec-dependent. Some variants put duplicates in the right subtree (multiset BST). Read carefully.

### Mutation 3 — fromList (= problem 85)
**Spec:** Build a BST from a list using repeated insert.
**Sig:** `fromList :: Ord a => [a] -> BT a`
**Solution:**
```haskell
fromList :: Ord a => [a] -> BT a
fromList = foldr insertBST Empty
```
**QC trap:** `foldr` vs `foldl` gives differently-shaped trees but both satisfy `isBST`. Examiner sometimes asks "why is this not balanced?" — because input ordering decides.

### Mutation 4 — bstSort (sort by build-and-flatten)
**Sig:** `bstSort :: Ord a => [a] -> [a]`
**Solution:**
```haskell
bstSort :: Ord a => [a] -> [a]
bstSort = flattenInOrder . fromList
  where
    flattenInOrder Empty        = []
    flattenInOrder (Fork v l r) = flattenInOrder l ++ [v] ++ flattenInOrder r
```
**QC trap:** Removes duplicates (because mutation 2 ignored them). Output is sorted. O(n²) on already-sorted input due to skewed tree.

### Mutation 5 — minBST / maxBST
**Spec:** Smallest / largest value in BST. Crash or Maybe on Empty.
**Sig:** `minBST :: BT a -> Maybe a`
**Solution:**
```haskell
minBST :: BT a -> Maybe a
minBST Empty            = Nothing
minBST (Fork v Empty _) = Just v
minBST (Fork _ l     _) = minBST l

maxBST :: BT a -> Maybe a
maxBST Empty            = Nothing
maxBST (Fork v _ Empty) = Just v
maxBST (Fork _ _ r    ) = maxBST r
```
**QC trap:** "Smallest" is the leftmost leaf, "largest" is the rightmost. Don't traverse both children — only go in one direction.

### Mutation 6 — deleteBST (= problem 84)
**Spec:** Remove `x` from BST. For two-child case, replace with max from left subtree.
**Sig:** `deleteBST :: Ord a => a -> BT a -> BT a`
**Solution:**
```haskell
deleteBST :: Ord a => a -> BT a -> BT a
deleteBST _ Empty            = Empty
deleteBST x (Fork v l r)
  | x < v                    = Fork v (deleteBST x l) r
  | x > v                    = Fork v l (deleteBST x r)
  | otherwise                = removeRoot l r
  where
    removeRoot Empty rt      = rt
    removeRoot lt Empty      = lt
    removeRoot lt rt         = let Just m = maxBST lt
                               in  Fork m (deleteBST m lt) rt
```
**QC trap:** Three sub-cases (no children, one child, two children) — easy to miss one. After delete, the result is still a BST: `isBST t ==> isBST (deleteBST x t)`.

### Mutation 7 — predecessorBST (largest value < x)
**Spec:** Find the largest value strictly less than `x`.
**Sig:** `predBST :: Ord a => a -> BT a -> Maybe a`
**Solution:**
```haskell
predBST :: Ord a => a -> BT a -> Maybe a
predBST _ Empty        = Nothing
predBST x (Fork v l r)
  | v >= x             = predBST x l
  | otherwise          = case predBST x r of
                           Just w  -> Just w
                           Nothing -> Just v
```
**QC trap:** Tricky logic. When `v < x`, the answer is at least `v`, but might be larger if there's a value in the right subtree still less than `x`. So recurse right and prefer that if available.

### Mutation 8 — successorBST (smallest value > x)
**Sig:** `succBST :: Ord a => a -> BT a -> Maybe a`
**Solution:**
```haskell
succBST :: Ord a => a -> BT a -> Maybe a
succBST _ Empty        = Nothing
succBST x (Fork v l r)
  | v <= x             = succBST x r
  | otherwise          = case succBST x l of
                           Just w  -> Just w
                           Nothing -> Just v
```
**QC trap:** Mirror of mutation 7. Equally tricky.

### Mutation 9 — toSortedList
**Spec:** Extract every element in sorted order.
**Sig:** `toSortedList :: BT a -> [a]`
**Solution:**
```haskell
toSortedList :: BT a -> [a]
toSortedList Empty        = []
toSortedList (Fork v l r) = toSortedList l ++ [v] ++ toSortedList r
```
**QC trap:** This is just `flattenInOrder` from `tree-extract-family.md`. Property: `isBST t ==> isSorted (toSortedList t)`.

### Mutation 10 — heightBST (= problem 72 specialized)
**Spec:** Height of the BST.
**Sig:** `heightBST :: BT a -> Int`
**Solution:**
```haskell
heightBST :: BT a -> Int
heightBST Empty        = 0
heightBST (Fork _ l r) = 1 + max (heightBST l) (heightBST r)
```
**QC trap:** Identical to `heightBT` — BST-ness doesn't affect height; it's purely structural.

## Hidden-predicate mutations
- "Insert only if predicate p v holds" → conditional insertBST.
- "Find smallest element satisfying p" → filtered minBST:
```haskell
findMinSat :: Ord a => (a -> Bool) -> BT a -> Maybe a
findMinSat p Empty        = Nothing
findMinSat p (Fork v l r) = case findMinSat p l of
  Just w  -> Just w
  Nothing -> if p v then Just v else findMinSat p r
```

## Accumulator-style alternative
For deleteBST, you can avoid the `let Just m = maxBST lt; deleteBST m lt` two-pass by writing a "remove max and return it" combined operation:
```haskell
removeMax :: BT a -> Maybe (a, BT a)
removeMax Empty            = Nothing
removeMax (Fork v l Empty) = Just (v, l)
removeMax (Fork v l r)     = case removeMax r of
                               Just (m, r') -> Just (m, Fork v l r')
                               Nothing      -> Just (v, l)
```
Then `deleteBST` uses `removeMax lt` once.

## Fold-style alternative
Most BST ops resist clean fold expression because they need to *split* on Ord comparison, not visit every node. `fromList = foldr insertBST Empty` is the one exception.

## Cross-family combinations
- this family + `tree-validation-family.md`: isBST as a precondition.
- this family + `tree-extract-family.md`: flattenInOrder gives a sorted list.
- this family + State: `labelTree t` only makes sense if t is a BST.
- this family + Reader: BST lookup with reader-supplied comparator (unusual but possible).

## QuickCheck universal attacks
- **Empty:** member returns False, insert returns singleton, min/max return Nothing, height 0.
- **`isBST (fromList xs)` is True** — invariant.
- **`memberBST x (insertBST x t)` is True** — round trip.
- **`memberBST x (deleteBST x t)` is False** — delete then check.
- **`bstSort xs == sort (nub xs)`** — sanity.
- **`length (toSortedList t) == sizeBT t`** — bridge to tree-counting-family.
- **`minBST t <= maxBST t`** — sanity.

## Pitfalls (per mutation)
- M1: comparing `>=` vs `>` in wrong direction.
- M2: failing to ignore duplicates (or replacing existing value — spec-dependent).
- M3: getting tree shape unexpectedly.
- M4: forgetting `flattenInOrder` removes dups.
- M5: traversing both subtrees — only one is needed.
- M6: missing the two-children case.
- M7: not preferring the right-subtree answer.
- M8: mirror of M7.
- M9: same as flattenInOrder.
- M10: same as heightBT.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — rangeCount (count BST entries within an inclusive range)

**Spec:** Count how many values in the BST fall in `[lo, hi]` inclusive. Use BST ordering to prune subtrees.

**Type sig:** `rangeCount :: Ord a => a -> a -> BT a -> Int`

```haskell
rangeCount :: Ord a => a -> a -> BT a -> Int
rangeCount _  _  Empty        = 0
rangeCount lo hi (Fork x l r)
  | x < lo    = rangeCount lo hi r
  | x > hi    = rangeCount lo hi l
  | otherwise = 1 + rangeCount lo hi l + rangeCount lo hi r
```

**What changes vs seed:** Uses BST invariant to skip whole subtrees (different recursion shape than naïve "visit every node"). Time O(k + log n) for k matches.

**QC trap:** When `x` is in `[lo, hi]`, you must recurse on BOTH subtrees (because both can contain in-range values). Skipping one is the bug.

### Mutation 12 — kthSmallest (in-order traversal with early exit)

**Spec:** Return the kth-smallest value in a BST (1-indexed), or `Nothing` if `k` exceeds size.

**Type sig:** `kthSmallest :: Int -> BT a -> Maybe a`

```haskell
kthSmallest :: Int -> BT a -> Maybe a
kthSmallest k t
  | k < 1 || k > sz = Nothing
  | otherwise       = Just (inorder t !! (k - 1))
  where sz = sizeBT t
        inorder Empty        = []
        inorder (Fork x l r) = inorder l ++ [x] ++ inorder r
        sizeBT Empty        = 0
        sizeBT (Fork _ l r) = 1 + sizeBT l + sizeBT r
```

**What changes vs seed:** Combines a structural in-order traversal with list indexing — a *data layout* shift from BST to `[a]`. Adds defensive guards using `sizeBT`.

**QC trap:** `k = 0` and `k > size` both return `Nothing`. `inorder t !! (k-1)` would crash with `Prelude.!!: index too large` if you removed the guard.

## See also

**Primary archetype:** [A11 BST ops](../archetypes/A11-bst-ops.md)
**Sibling families:** [tree-validation](./tree-validation-family.md) · [tree-counting](./tree-counting-family.md)
**Cross-topic:** [bst × state](../cross-matrix/bst-x-state.md) · [bst × writer](../cross-matrix/bst-x-writer.md)
**Theory:** [bst](../trees/bst.md)
**QuickCheck:** [bst attacks](../quickcheck/bst-attacks.md)
**Pitfalls:** [P-009 isBST Empty = False](../pitfalls/HIGH-severity.md#p-009) · [P-015 BST delete two-children](../pitfalls/HIGH-severity.md#p-015) · [P-020 three impls](../pitfalls/HIGH-severity.md#p-020)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
