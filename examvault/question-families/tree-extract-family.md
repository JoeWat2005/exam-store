<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: tree-extract**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · **tree-extract** · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: tree-extract

**Archetype:** A06 (BT/Rose → [a] structural flatten)   |   **Stars:** ⭐⭐   |   **Course week(s):** 6–7
**Search keywords:** flatten, in-order, pre-order, post-order, paths, leaves-list, nodes-at-depth, breadth-first

## Generator template
```haskell
data BT a = Empty | Fork a (BT a) (BT a)

-- The seed: BT a -> [a]. Walks the tree, combines values via (++).
-- All mutations vary the *order* (where [v] appears) or the *content*
-- (singletons, paths, only-leaves).
seed :: BT a -> [a]
seed Empty        = []
seed (Fork v l r) = seed l ++ [v] ++ seed r   -- in-order
```

## Mutations (the examiner picks one)

### Mutation 1 — flattenInOrder (= problem 75)
**Spec:** Left subtree, root, right subtree.
**Sig:** `flattenInOrder :: BT a -> [a]`
**What changes vs seed:** This *is* the seed.
**Solution:**
```haskell
flattenInOrder :: BT a -> [a]
flattenInOrder Empty        = []
flattenInOrder (Fork v l r) = flattenInOrder l ++ [v] ++ flattenInOrder r
```
**QC trap:** Used in `isBST`. Has O(n²) worst case from `++` — see accumulator alternative.

### Mutation 2 — flattenPreOrder (= problem 76)
**Spec:** Root, left, right.
**Sig:** `flattenPreOrder :: BT a -> [a]`
**What changes vs seed:** `[v]` moves to the front.
**Solution:**
```haskell
flattenPreOrder :: BT a -> [a]
flattenPreOrder Empty        = []
flattenPreOrder (Fork v l r) = [v] ++ flattenPreOrder l ++ flattenPreOrder r
```
**QC trap:** Pre-order of `mirror t` equals pre-order of `t` with each Fork's L/R swapped — useful sanity check.

### Mutation 3 — flattenPostOrder
**Spec:** Left, right, root.
**Sig:** `flattenPostOrder :: BT a -> [a]`
**What changes vs seed:** `[v]` moves to the end.
**Solution:**
```haskell
flattenPostOrder :: BT a -> [a]
flattenPostOrder Empty        = []
flattenPostOrder (Fork v l r) = flattenPostOrder l ++ flattenPostOrder r ++ [v]
```
**QC trap:** `reverse (flattenPostOrder t) == flattenPreOrder (mirror t)`.

### Mutation 4 — leavesList (= problem 73 with list return)
**Spec:** Just the leaf values, in left-to-right order.
**Sig:** `leavesList :: BT a -> [a]`
**What changes vs seed:** Only leaves contribute to the list.
**Solution:**
```haskell
leavesList :: BT a -> [a]
leavesList Empty                = []
leavesList (Fork v Empty Empty) = [v]
leavesList (Fork _ l r)         = leavesList l ++ leavesList r
```
**QC trap:** `length (leavesList t) == leavesCount t` — see `tree-counting-family.md`.

### Mutation 5 — nodesAtDepth (slice at one level)
**Spec:** All values stored exactly at depth `d` (root depth 0), left-to-right.
**Sig:** `nodesAtDepth :: Int -> BT a -> [a]`
**What changes vs seed:** Depth counter; only return at the matched depth.
**Solution:**
```haskell
nodesAtDepth :: Int -> BT a -> [a]
nodesAtDepth d = go 0
  where
    go _ Empty                = []
    go k (Fork v l r)
      | k == d                = [v]
      | otherwise             = go (k+1) l ++ go (k+1) r
```
**QC trap:** Stops descending past the target depth — efficient. `nodesAtDepth (height t - 1) t` gives the deepest level.

### Mutation 6 — pathsToLeaves
**Spec:** Every root-to-leaf path, as a list of value sequences.
**Sig:** `pathsToLeaves :: BT a -> [[a]]`
**What changes vs seed:** Now we return `[[a]]`. Each leaf contributes one path; internal nodes prepend.
**Solution:**
```haskell
pathsToLeaves :: BT a -> [[a]]
pathsToLeaves Empty                = []
pathsToLeaves (Fork v Empty Empty) = [[v]]
pathsToLeaves (Fork v l r)         = map (v:) (pathsToLeaves l ++ pathsToLeaves r)
```
**QC trap:** A `Fork v Empty (Fork w Empty Empty)` produces `[[v,w]]`, NOT `[[v],[v,w]]`. The first case must be exactly "both empty"; mixed cases fall through.

### Mutation 7 — flattenBFS (level-order / breadth-first)
**Spec:** Root, then all depth-1 left-to-right, then depth-2, etc.
**Sig:** `flattenBFS :: BT a -> [a]`
**What changes vs seed:** Queue-based traversal, not recursive on subtrees.
**Solution:**
```haskell
flattenBFS :: BT a -> [a]
flattenBFS t = go [t]
  where
    go []                = []
    go (Empty : rest)    = go rest
    go (Fork v l r : rs) = v : go (rs ++ [l, r])
```
**QC trap:** The queue is a list of *trees*, not values. The trap is `[l, r]` vs `[r, l]` — left first.

### Mutation 8 — flattenRose (= problem 88)
**Spec:** Pre-order over a rose tree.
**Sig:** `flattenRose :: Rose a -> [a]`
**What changes vs seed:** Rose has `n` children; use `concatMap`.
**Solution:**
```haskell
data Rose a = Branch a [Rose a]

flattenRose :: Rose a -> [a]
flattenRose (Branch v children) = v : concatMap flattenRose children
```
**QC trap:** Watch the constructor — some rose-tree variants use `Leaf a | Branch [Rose a]` (mock Q1). Then there's no value at Branch and leaves carry the values.

### Mutation 9 — leafPaths-as-strings (encode each path)
**Spec:** Encode every root-to-leaf path as a string of L/R characters describing direction.
**Sig:** `directions :: BT a -> [String]`
**What changes vs seed:** Returns *direction* strings, not value sequences. Tied to the structural recursion.
**Solution:**
```haskell
directions :: BT a -> [String]
directions Empty                = []
directions (Fork _ Empty Empty) = [""]
directions (Fork _ l r)         = map ('L':) (directions l)
                               ++ map ('R':) (directions r)
```
**QC trap:** Empty tree returns `[]`, not `[""]`. Single leaf returns `[""]`, not `[]`. Get the boundary wrong and the whole spec collapses.

### Mutation 10 — flattenWithDepth (annotate each value with its depth)
**Spec:** In-order list of `(depth, value)` pairs.
**Sig:** `flattenWithDepth :: BT a -> [(Int, a)]`
**What changes vs seed:** Same in-order traversal, depth threaded.
**Solution:**
```haskell
flattenWithDepth :: BT a -> [(Int, a)]
flattenWithDepth = go 0
  where
    go _ Empty        = []
    go k (Fork v l r) = go (k+1) l ++ [(k, v)] ++ go (k+1) r
```
**QC trap:** Confusing depth with index — these are different. Index requires a separate counter.

## Hidden-predicate mutations
- "Extract only values satisfying p" → `extractBy p t = filter p (flattenInOrder t)` — but the inlined recursive version is what the examiner usually wants:
```haskell
extractBy :: (a -> Bool) -> BT a -> [a]
extractBy _ Empty        = []
extractBy p (Fork v l r) = extractBy p l
                       ++ (if p v then [v] else [])
                       ++ extractBy p r
```
- "Extract values at even depth only" → fuse mutations 5 and 10 with `if even k then [v] else []`.

## Accumulator-style alternative
The `(++)` in the seed is O(n) at the root → O(n²) total. The accumulator version uses *difference lists*:
```haskell
flattenInOrder' :: BT a -> [a]
flattenInOrder' t = go t []
  where
    go Empty        acc = acc
    go (Fork v l r) acc = go l (v : go r acc)
```
This is O(n). Worth knowing for the "performance" follow-up that the examiner sometimes tacks on.

## Fold-style alternative
```haskell
flattenInOrder''  = foldBT [] (\v ls rs -> ls ++ [v] ++ rs)
flattenPreOrder'' = foldBT [] (\v ls rs -> v : ls ++ rs)
flattenPostOrder''= foldBT [] (\v ls rs -> ls ++ rs ++ [v])
```
Clean, but still O(n²) without DList-style accumulator.

## Cross-family combinations
- this family + `tree-validation-family.md`: `isBST = strictSorted . flattenInOrder`
- this family + `tree-counting-family.md`: every count equals a `length . extractBy ...`
- this family + `bst-ops-family.md`: `bstSort = flattenInOrder . fromList`
- this family + State monad: paths-as-state for path-finding problems
- this family + Writer monad: log every node visit in extraction order

## QuickCheck universal attacks
- **Empty:** all flattens return `[]`. pathsToLeaves returns `[]`. directions returns `[]`.
- **Singleton:** flattens return `[v]`. pathsToLeaves returns `[[v]]`. directions returns `[""]`.
- **Two-leaf tree** (`Fork r (Fork x Empty Empty) (Fork y Empty Empty)`): used to distinguish in-/pre-/post-order. `[x,r,y]` / `[r,x,y]` / `[x,y,r]`.
- **Skewed (right-spine):** all three orders agree for pre and in (since left is always Empty); post differs.
- **`length . flattenInOrder == sizeBT`** — free QC property.
- **`sort . flattenInOrder == flattenInOrder` ⇔ `isBST`** for distinct values.

## Pitfalls (per mutation)
- M1: confusing `[v]` placement (in/pre/post).
- M2: same.
- M3: same.
- M4: pattern-match order — leaf case must come before the recursive case.
- M5: not stopping when `k == d` (descending past the target).
- M6: forgetting to `map (v:)` to prepend the current node.
- M7: order of `[l, r]` in the queue.
- M8: the leaves-only Rose variant has a different recursion (no value at Branch).
- M9: empty/singleton boundary confusion.
- M10: depth vs in-order index.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — extractMin (return min + tree without min)

**Spec:** Return the smallest value in a `BT a` together with the tree that remains after removing it. Used by `delete`.

**Type sig:** `extractMin :: Ord a => BT a -> Maybe (a, BT a)`

```haskell
extractMin :: Ord a => BT a -> Maybe (a, BT a)
extractMin Empty             = Nothing
extractMin (Fork x Empty r)  = Just (x, r)
extractMin (Fork x l r)      = do
  (m, l') <- extractMin l
  return (m, Fork x l' r)
```

**What changes vs seed:** Returns *two* values — the minimum AND the residual tree — using the Maybe monad to bubble emptiness. Different return shape from canonical `extract :: BT a -> [a]`.

**QC trap:** When you find the leftmost Fork (`l = Empty`), return `r` as the residual (not `Empty`). Forgetting that the right subtree of the leftmost node must survive is the classic bug.

## See also

**Primary archetype:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Sibling families:** [tree-counting](./tree-counting-family.md) · [tree-transform](./tree-transform-family.md) · [rose-ops](./rose-ops-family.md)
**Cross-topic:** [tree × maybe](../cross-matrix/tree-x-maybe.md) · [tree × either](../cross-matrix/tree-x-either.md)
**Theory:** [binary tree](../trees/binary-tree.md) · [tree traversals](../trees/tree-traversals.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
