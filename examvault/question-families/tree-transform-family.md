<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: tree-transform**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · **tree-transform** · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: tree-transform

**Archetype:** A05 (structural map / structural prune)   |   **Stars:** ⭐⭐   |   **Course week(s):** 6–7
**Search keywords:** mirror, prune, mapBT, fmap, take-depth, mergeBT, transform, Functor BT

## Generator template
```haskell
data BT a = Empty | Fork a (BT a) (BT a)

-- The seed: a structure-preserving transformation BT a -> BT b.
-- Walks Empty -> Empty, Fork v l r -> Fork (g v) (rec l) (rec r), where
-- g and the optional permutation of (l,r) are what the examiner mutates.
seed :: (a -> b) -> BT a -> BT b
seed _ Empty        = Empty
seed g (Fork v l r) = Fork (g v) (seed g l) (seed g r)
```

## Mutations (the examiner picks one)

### Mutation 1 — mapBT (= problem 77)
**Spec:** Apply `f` to every stored value, preserving shape.
**Sig:** `mapBT :: (a -> b) -> BT a -> BT b`
**What changes vs seed:** This *is* the seed.
**Solution:**
```haskell
mapBT :: (a -> b) -> BT a -> BT b
mapBT _ Empty        = Empty
mapBT f (Fork v l r) = Fork (f v) (mapBT f l) (mapBT f r)
```
**QC trap:** `mapBT id == id`. `mapBT (f . g) == mapBT f . mapBT g`. These are the Functor laws — see `functor-instance-family.md`.

### Mutation 2 — mirror (= problem 74)
**Spec:** Swap left and right at every Fork.
**Sig:** `mirror :: BT a -> BT a`
**What changes vs seed:** No transformation on `v`, but children are *swapped* and recursed.
**Solution:**
```haskell
mirror :: BT a -> BT a
mirror Empty        = Empty
mirror (Fork v l r) = Fork v (mirror r) (mirror l)
```
**QC trap:** `mirror . mirror == id`. Easy QC property. On a symmetric tree, `mirror t == t` — use as a sanity check.

### Mutation 3 — pruneDepth (cut at depth k)
**Spec:** Replace every subtree at depth >= k with `Empty`.
**Sig:** `pruneDepth :: Int -> BT a -> BT a`
**What changes vs seed:** Need an explicit depth counter parameter; base case becomes "depth reached → Empty".
**Solution:**
```haskell
pruneDepth :: Int -> BT a -> BT a
pruneDepth d t = go 0 t
  where
    go _ Empty               = Empty
    go k (Fork v l r)
      | k >= d               = Empty
      | otherwise            = Fork v (go (k+1) l) (go (k+1) r)
```
**QC trap:** `pruneDepth 0 t == Empty` for any non-empty `t`. `pruneDepth (height t + 1) t == t`. Negative `d` → `Empty`.

### Mutation 4 — pruneRose (= mock Q1 part 2)
**Spec:** Keep at most `n` children at every Branch of a rose tree.
**Sig:** `prune :: Int -> Rose a -> Rose a`
**What changes vs seed:** Cuts in the *width* (number of children) rather than depth. Combines `map` with `take`.
**Solution:**
```haskell
data Rose a = Leaf a | Branch [Rose a]

prune :: Int -> Rose a -> Rose a
prune _ (Leaf x)        = Leaf x
prune n (Branch forest) = Branch (take n (map (prune n) forest))
```
**QC trap:** `take` happens *after* `map`, but lazy evaluation means deeper subtrees beyond the first `n` are never forced. If you write `map (prune n) (take n forest)` you get the same result eagerly — both pass QC, but the former is the canonical solution.

### Mutation 5 — filterBT (keep only nodes satisfying predicate, collapse failures)
**Spec:** Drop entire subtrees whose root value fails the predicate (root failure → Empty).
**Sig:** `filterBT :: (a -> Bool) -> BT a -> BT a`
**What changes vs seed:** Adds a guard at the Fork case that may collapse to Empty.
**Solution:**
```haskell
filterBT :: (a -> Bool) -> BT a -> BT a
filterBT _ Empty        = Empty
filterBT p (Fork v l r)
  | p v                 = Fork v (filterBT p l) (filterBT p r)
  | otherwise           = Empty
```
**QC trap:** This collapses the *entire* subtree if root fails. The alternative "promote a surviving child" is a different (harder) function — read the spec carefully.

### Mutation 6 — mergeBT (zip two BTs of same shape)
**Spec:** Combine corresponding nodes pairwise; stop when either tree ends.
**Sig:** `mergeBT :: (a -> b -> c) -> BT a -> BT b -> BT c`
**What changes vs seed:** Two trees, two patterns each → four cases.
**Solution:**
```haskell
mergeBT :: (a -> b -> c) -> BT a -> BT b -> BT c
mergeBT _ Empty _                   = Empty
mergeBT _ _ Empty                   = Empty
mergeBT f (Fork a la ra) (Fork b lb rb)
                                    = Fork (f a b) (mergeBT f la lb) (mergeBT f ra rb)
```
**QC trap:** Where trees differ in shape, the result has the *intersection* shape. `mergeBT const t Empty == Empty`.

### Mutation 7 — addPathSum (annotate each node with sum of ancestors)
**Spec:** Replace each value `v` with `v + sum-of-ancestors`. Root keeps its own value.
**Sig:** `addPathSum :: Num a => BT a -> BT a`
**What changes vs seed:** An accumulator (running sum) threads through.
**Solution:**
```haskell
addPathSum :: Num a => BT a -> BT a
addPathSum = go 0
  where
    go _ Empty        = Empty
    go acc (Fork v l r) = let v' = v + acc
                          in  Fork v' (go v' l) (go v' r)
```
**QC trap:** The root's new value is `v + 0 = v`. Every descendant's increment uses the *parent's new* value, not the parent's original.

### Mutation 8 — fmapInTree (Functor-instance presentation)
**Spec:** Same as mapBT but via `instance Functor BT`.
**Sig:** `fmap :: (a -> b) -> BT a -> BT b`
**What changes vs seed:** Wrap in `instance Functor BT where fmap = ...`.
**Solution:**
```haskell
instance Functor BT where
  fmap _ Empty        = Empty
  fmap f (Fork v l r) = Fork (f v) (fmap f l) (fmap f r)
```
**QC trap:** Once you write the instance, `fmap` shadows the implementation everywhere — make sure no other constraint of the question expects the explicit name.

### Mutation 9 — reverseAtEvenDepth (depth-conditional mirror)
**Spec:** Mirror only at even-depth nodes.
**Sig:** `reverseAtEvenDepth :: BT a -> BT a`
**What changes vs seed:** Depth parameter + mutation 2's swap-pattern, applied conditionally.
**Solution:**
```haskell
reverseAtEvenDepth :: BT a -> BT a
reverseAtEvenDepth = go 0
  where
    go _ Empty        = Empty
    go k (Fork v l r)
      | even k        = Fork v (go (k+1) r) (go (k+1) l)
      | otherwise     = Fork v (go (k+1) l) (go (k+1) r)
```
**QC trap:** "Even depth" includes depth 0 — the root *is* mirrored.

### Mutation 10 — substituteAt (replace a marked subtree by another)
**Spec:** Replace the subtree rooted at a node whose value equals `target` with `replacement`. Replace only the first such match in pre-order.
**Sig:** `substituteFirst :: Eq a => a -> BT a -> BT a -> BT a`
**What changes vs seed:** Need to thread "have I replaced yet" — easiest is a Maybe-returning helper.
**Solution:**
```haskell
substituteFirst :: Eq a => a -> BT a -> BT a -> BT a
substituteFirst target replacement t = case go t of
                                         Just t' -> t'
                                         Nothing -> t
  where
    go Empty                          = Nothing
    go (Fork v l r)
      | v == target                   = Just replacement
      | otherwise                     = case go l of
          Just l' -> Just (Fork v l' r)
          Nothing -> case go r of
            Just r' -> Just (Fork v l r')
            Nothing -> Nothing
```
**QC trap:** "First in pre-order" must short-circuit — don't replace in both subtrees.

## Hidden-predicate mutations
The two most common predicate twists on this family:
- "transform values for which `p v` holds, leave others untouched" → `mapBy p f`
- "prune subtrees where `p v`" → `pruneBy p`

```haskell
mapBy :: (a -> Bool) -> (a -> a) -> BT a -> BT a
mapBy _ _ Empty        = Empty
mapBy p f (Fork v l r) = let v' = if p v then f v else v
                         in  Fork v' (mapBy p f l) (mapBy p f r)
```

## Accumulator-style alternative
Most transformations don't benefit — they're already O(n). The exception is mutation 7 (addPathSum) which is *intrinsically* an accumulator pattern. Trying to do it without acc requires precomputing the path on each call — O(n^2).

## Fold-style alternative
Using `foldBT`:
```haskell
mapBT' g = foldBT Empty (\v l r -> Fork (g v) l r)
mirror'  = foldBT Empty (\v l r -> Fork v r l)
```
Clean for non-conditional transforms; loses access to subtree structure for conditional ones.

## Cross-family combinations
- this family + `tree-validation-family.md`: `mirror . mirror == id`, `isSymmetric t == (t == mirror t)`
- this family + `state-counter-family.md`: `labelTree` is a transform that threads State (problem 112)
- this family + `functor-instance-family.md`: mutation 8 is the bridge
- this family + `writer-trace-family.md`: log every node visited during the transform

## QuickCheck universal attacks
- **Empty:** every transform should leave Empty as Empty.
- **Singleton:** Fork x Empty Empty → Fork (f x) Empty Empty (and Empty for filter when p x is False).
- **Symmetric (Fork x t t):** mirror is identity.
- **Asymmetric depth-1:** mirror swaps L and R but only at root.
- **Inverses:** mirror² = id; map id = id; prune (height+1) = id.
- **Idempotent:** `pruneDepth k . pruneDepth k == pruneDepth k`.

## Pitfalls (per mutation)
- M1: pattern-match laziness — `mapBT f undefined` should diverge; some students accidentally return Empty.
- M2: swapping in only one direction (writing `Fork v (mirror r) l`) — both must recurse.
- M3: not bumping depth or using `>` vs `>=` (read spec).
- M4: writing `take n (map ...)` versus `map ... (take n ...)` — both work because of laziness but the canonical is the former.
- M5: confusing "collapse" semantics with "promote children" — different functions.
- M6: forgetting one of the Empty cases (need both).
- M7: using parent's original value instead of new value.
- M8: instance writes outside `instance Functor` block.
- M9: even/odd flip mid-recursion.
- M10: replacing in both subtrees instead of first.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — mirrorOnlyIf (predicate-guarded structural transform)

**Spec:** Mirror a `BT a` left-right only at nodes whose value satisfies a predicate.

**Type sig:** `mirrorOnlyIf :: (a -> Bool) -> BT a -> BT a`

```haskell
mirrorOnlyIf :: (a -> Bool) -> BT a -> BT a
mirrorOnlyIf _ Empty        = Empty
mirrorOnlyIf p (Fork x l r)
  | p x       = Fork x (mirrorOnlyIf p r) (mirrorOnlyIf p l)
  | otherwise = Fork x (mirrorOnlyIf p l) (mirrorOnlyIf p r)
```

**What changes vs seed:** Predicate-guarded mirror: same recursion shape but the swap-or-not decision is local to each node. Different from `mirror` which unconditionally swaps.

**QC trap:** Note: the mirror happens at the NODE level — children are swapped BEFORE the recursive call, but the predicate is on `x`. Swapping AFTER recursion (`flipChildren (Fork x (rec l) (rec r))`) is identical here (different operation order, same result), but won't be if your recursion depends on the parent's swap state.

## Additional Phase-12 mutations (cap relaxed to 25)

### Mutation 12 — treeStatistics (multi-result single pass)
**Sig:** `treeStatistics :: BT a -> (Int, Int, Int)`
**Spec:** Return `(size, height, leafCount)` in a single traversal.
```haskell
treeStatistics :: BT a -> (Int, Int, Int)
treeStatistics Empty                       = (0, 0, 0)
treeStatistics (Fork _ Empty Empty)        = (1, 1, 1)
treeStatistics (Fork _ l r)                = (1 + sl + sr, 1 + max hl hr, lcl + lcr)
  where (sl, hl, lcl) = treeStatistics l
        (sr, hr, lcr) = treeStatistics r
```
**Why distinct:** Triple-result single-pass. Combines what would normally be 3 folds.

### Mutation 13 — pruneByPredicate (collapse failing subtrees)
**Sig:** `pruneBy :: (a -> Bool) -> BT a -> BT a`
**Spec:** Replace any subtree whose root fails the predicate with `Empty`.
```haskell
pruneBy :: (a -> Bool) -> BT a -> BT a
pruneBy _ Empty        = Empty
pruneBy p (Fork x l r)
  | p x       = Fork x (pruneBy p l) (pruneBy p r)
  | otherwise = Empty
```
**Why distinct:** Wholesale subtree elimination. Differs from `filterBT` (M5) which keeps grandchildren.

### Mutation 14 — rotateLeft / rotateRight (BST rebalance primitives)
**Sig:** `rotateLeft, rotateRight :: BT a -> BT a`
**Spec:** Local tree rotations used by self-balancing BSTs.
```haskell
rotateLeft :: BT a -> BT a
rotateLeft (Fork x a (Fork y b c)) = Fork y (Fork x a b) c
rotateLeft t                       = t

rotateRight :: BT a -> BT a
rotateRight (Fork y (Fork x a b) c) = Fork x a (Fork y b c)
rotateRight t                       = t
```
**Why distinct:** Local-only transform — not a full traversal. Used in BST self-balancing variants.

### Mutation 15 — replaceAt (depth-targeted replacement)
**Sig:** `replaceAt :: Int -> a -> BT a -> BT a`
**Spec:** Replace value at root if depth = 0; otherwise descend to both subtrees with depth - 1.
```haskell
replaceAt :: Int -> a -> BT a -> BT a
replaceAt _ _ Empty                    = Empty
replaceAt 0 v (Fork _ l r)             = Fork v l r
replaceAt d v (Fork x l r) | d > 0     = Fork x (replaceAt (d-1) v l) (replaceAt (d-1) v r)
                            | otherwise = Fork x l r
```
**Why distinct:** Recursion bounded by `Int` parameter; updates at the *depth boundary*, not at a value match.

### Mutation 16 — zipTrees (parallel zip of same-shape trees)
**Sig:** `zipTrees :: BT a -> BT b -> Maybe (BT (a, b))`
**Spec:** Pair up corresponding nodes; return `Nothing` if shapes differ.
```haskell
zipTrees :: BT a -> BT b -> Maybe (BT (a, b))
zipTrees Empty Empty                   = Just Empty
zipTrees (Fork x lx rx) (Fork y ly ry) = do
  l <- zipTrees lx ly
  r <- zipTrees rx ry
  Just (Fork (x, y) l r)
zipTrees _ _                           = Nothing
```
**Why distinct:** Two-tree walk with `Maybe`-shape-mismatch detection. Different from `mergeBT` (M6) which assumes same shape.

## See also

**Primary archetype:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Sibling families:** [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [rose-ops](./rose-ops-family.md)
**Cross-topic:** [tree × state](../cross-matrix/tree-x-state.md) · [tree × generic-monad](../cross-matrix/tree-x-generic-monad.md)
**Theory:** [binary tree](../trees/binary-tree.md) · [tree functor](../trees/tree-functor.md) · [tree zipper](../trees/tree-zipper.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md)
**Pitfalls:** [P-016 functor doesn't preserve shape](../pitfalls/HIGH-severity.md#p-016)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
