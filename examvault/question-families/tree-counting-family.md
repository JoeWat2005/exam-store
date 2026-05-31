<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: tree-counting**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · **tree-counting** · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: tree-counting

**Archetype:** A03 (recursive count over an inductive type)   |   **Stars:** ⭐⭐   |   **Course week(s):** 6–7
**Search keywords:** sizeBT, countBT, leaves, internal, depth, count-matching, BT a, Fork

## Generator template
```haskell
-- The seed shape: a structural fold over a BT a returning an Int.
-- ONE function body. Walks both subtrees, combines with (+), adds a local contribution.
data BT a = Empty | Fork a (BT a) (BT a)

seed :: BT a -> Int
seed Empty        = 0
seed (Fork _ l r) = 1 + seed l + seed r
```

This is the "count all nodes" base case. Every mutation is the seed plus one of:
- a predicate on the node value,
- a predicate on the *shape* at the current position (`leaf?`, `unary?`),
- an extra parameter threaded through (depth, target value),
- the answer type promoted to `[a]`/`Maybe a`/`(Int,Int)`.

## Mutations (the examiner picks one)

### Mutation 1 — sizeBT (total node count)
**Spec:** Count every `Fork` constructor in the tree.
**Sig:** `sizeBT :: BT a -> Int`
**What changes vs seed:** Nothing — this *is* the seed.
**Solution:**
```haskell
sizeBT :: BT a -> Int
sizeBT Empty        = 0
sizeBT (Fork _ l r) = 1 + sizeBT l + sizeBT r
```
**QC trap:** `Empty` returns 0 (not 1). A single `Fork _ Empty Empty` returns 1.

### Mutation 2 — leavesCount
**Spec:** Count leaves only (a `Fork` whose two children are both `Empty`).
**Sig:** `leavesCount :: BT a -> Int`
**What changes vs seed:** Local contribution becomes a pattern test, not a constant.
**Solution:**
```haskell
leavesCount :: BT a -> Int
leavesCount Empty                  = 0
leavesCount (Fork _ Empty Empty)   = 1
leavesCount (Fork _ l r)           = leavesCount l + leavesCount r
```
**QC trap:** A `Fork _ Empty (Fork _ Empty Empty)` is NOT a leaf even though one side is `Empty`. The order of patterns matters — the leaf case must come before the recursive case.

### Mutation 3 — internalCount
**Spec:** Count *internal* nodes — a `Fork` that is not a leaf (i.e. has at least one non-`Empty` child).
**Sig:** `internalCount :: BT a -> Int`
**What changes vs seed:** Opposite predicate to mutation 2.
**Solution:**
```haskell
internalCount :: BT a -> Int
internalCount Empty                = 0
internalCount (Fork _ Empty Empty) = 0
internalCount (Fork _ l r)         = 1 + internalCount l + internalCount r
```
**QC trap:** `internalCount t + leavesCount t == sizeBT t` — a free property test.

### Mutation 4 — countBT (count matches of a value)
**Spec:** How many times does `x` appear as a node value?
**Sig:** `countBT :: Eq a => a -> BT a -> Int`
**What changes vs seed:** The local contribution is `if v == x then 1 else 0`. Eq constraint enters.
**Solution:**
```haskell
countBT :: Eq a => a -> BT a -> Int
countBT _ Empty        = 0
countBT x (Fork v l r) = (if v == x then 1 else 0) + countBT x l + countBT x r
```
**QC trap:** Counts in *both* subtrees — even after a match. The examiner sometimes asks for "stop on first match" instead; check the spec carefully.

### Mutation 5 — countBy (hidden predicate)
**Spec:** Count nodes whose value satisfies an arbitrary predicate.
**Sig:** `countBy :: (a -> Bool) -> BT a -> Int`
**What changes vs seed:** Eq replaced by a predicate parameter — strictly more general than countBT.
**Solution:**
```haskell
countBy :: (a -> Bool) -> BT a -> Int
countBy _ Empty        = 0
countBy p (Fork v l r) = (if p v then 1 else 0) + countBy p l + countBy p r
```
**QC trap:** `countBy (==x) == countBT x`. `countBy (const True) == sizeBT`. Sanity-check both.

### Mutation 6 — countAtDepth
**Spec:** Count nodes that occur at exactly depth `d` (root at depth 0).
**Sig:** `countAtDepth :: Int -> BT a -> Int`
**What changes vs seed:** Need a depth-tracking helper because the parameter changes as we descend.
**Solution:**
```haskell
countAtDepth :: Int -> BT a -> Int
countAtDepth d t = go 0 t
  where
    go _ Empty               = 0
    go k (Fork _ l r)
      | k == d               = 1
      | otherwise            = go (k+1) l + go (k+1) r
```
**QC trap:** Negative `d` returns 0 (no node lives there). Depth 0 of a non-empty tree returns 1, not the root value.

### Mutation 7 — countBelowDepth
**Spec:** Count nodes at depth `>= d`.
**Sig:** `countBelowDepth :: Int -> BT a -> Int`
**What changes vs seed:** Predicate on depth instead of equality.
**Solution:**
```haskell
countBelowDepth :: Int -> BT a -> Int
countBelowDepth d t = go 0 t
  where
    go _ Empty               = 0
    go k (Fork _ l r)        = (if k >= d then 1 else 0)
                             + go (k+1) l + go (k+1) r
```
**QC trap:** When `d == 0` this equals `sizeBT`. When `d` exceeds tree height it's 0.

### Mutation 8 — countLeavesByTag (tagged count)
**Spec:** Count leaves whose stored value equals `x`.
**Sig:** `countLeavesByTag :: Eq a => a -> BT a -> Int`
**What changes vs seed:** Combines mutations 2 and 4 — shape *and* value predicate at once.
**Solution:**
```haskell
countLeavesByTag :: Eq a => a -> BT a -> Int
countLeavesByTag _ Empty                            = 0
countLeavesByTag x (Fork v Empty Empty) | v == x    = 1
countLeavesByTag _ (Fork _ Empty Empty)             = 0
countLeavesByTag x (Fork _ l r)                     = countLeavesByTag x l + countLeavesByTag x r
```
**QC trap:** Pattern-match order matters: leaf-with-match → leaf-mismatch → internal. Get them in the wrong order and the internal case shadows leaves.

### Mutation 9 — countNodesSatisfying (path-aware predicate)
**Spec:** Count nodes whose value is greater than every ancestor on the path to it.
**Sig:** `countMaxSoFar :: Ord a => BT a -> Int`
**What changes vs seed:** An accumulator (the running max) is threaded into recursive calls. Promotes a "count" into a "stateful count".
**Solution:**
```haskell
-- Seed the running max from the ROOT value, so no Bounded/minBound is needed
-- (exam tree element types are usually Integer, which has no Bounded instance):
countMaxSoFar :: Ord a => BT a -> Int
countMaxSoFar Empty        = 0
countMaxSoFar (Fork v l r) = 1 + go v l + go v r   -- root always counts
  where
    go _ Empty           = 0
    go m (Fork x l' r')
      | x > m            = 1 + go x l' + go x r'
      | otherwise        = go m l' + go m r'
```
**QC trap:** Empty tree returns 0. The root *always* satisfies the predicate (every ancestor is vacuously beaten), so for a non-empty tree the result is at least 1. Do **not** write `go minBound t` with the advertised `Ord a => BT a -> Int` signature — `minBound` needs `Bounded a`, which `Integer` lacks; seeding from the root avoids the extra constraint.

### Mutation 10 — (Int, Int) split count (leaves vs internal in one pass)
**Spec:** Return `(numLeaves, numInternal)` in a single traversal.
**Sig:** `splitCount :: BT a -> (Int, Int)`
**What changes vs seed:** Return type widens from `Int` to a pair; combination uses `mappend`-style addition.
**Solution:**
```haskell
splitCount :: BT a -> (Int, Int)
splitCount Empty                  = (0, 0)
splitCount (Fork _ Empty Empty)   = (1, 0)
splitCount (Fork _ l r)           = let (a1,b1) = splitCount l
                                        (a2,b2) = splitCount r
                                    in  (a1+a2, 1+b1+b2)
```
**QC trap:** Combines mutations 2 and 3 in one pass — useful when the examiner wants O(n) and forbids two-pass solutions.

## Hidden-predicate mutations
The single most common twist: change the constant `1` in the seed to `if p v then 1 else 0` and add a `(a -> Bool)` parameter. Mutation 5 is this twist applied directly. Watch for English-language phrasing like:
- "Count the nodes whose value is divisible by 3" → `countBy (\v -> v `mod` 3 == 0)`
- "Count the strings starting with capital letters" → `countBy (\s -> not (null s) && isUpper (head s))`
- "Count nodes whose stored Bool is True" → `countBy id`

## Accumulator-style alternative
For mutations 1–5 you can convert to a tail-recursive `foldr` over the explicit traversal:
```haskell
sizeBT' :: BT a -> Int
sizeBT' = go 0
  where
    go !acc Empty        = acc
    go !acc (Fork _ l r) = go (go (acc + 1) l) r
```
Strict accumulator (`!acc`) is essential — lazy accumulators in count problems are the textbook example of a space leak.

## Fold-style alternative
Define a generic tree fold once, then everything is a one-liner:
```haskell
foldBT :: b -> (a -> b -> b -> b) -> BT a -> b
foldBT e _ Empty        = e
foldBT e f (Fork v l r) = f v (foldBT e f l) (foldBT e f r)

sizeBT   = foldBT 0 (\_ l r -> 1 + l + r)
countBT x = foldBT 0 (\v l r -> (if v == x then 1 else 0) + l + r)
```
The exam usually wants explicit recursion, but a foldBT solution scores when "use a single helper" is in the rubric.

## Cross-family combinations
- this family + monad State → `countLeaves :: BT a -> State Int ()` (problem 113) — see `state-counter-family.md`
- this family + rose-trees → `sizeRose` (problem 86) — see `rose-ops-family.md`
- this family + writer monad → "count steps and log each match" — see `writer-trace-family.md`

## QuickCheck universal attacks
- **Empty:** Most counts on `Empty` are 0.
- **Singleton:** `Fork x Empty Empty` is both a leaf and (depending on the predicate) a match.
- **Skewed left** (`Fork _ (Fork _ (Fork _ Empty Empty) Empty) Empty`): tests that you don't accidentally short-circuit on one side.
- **Right-skewed mirror:** same shape but recursion uses the *other* child — catches `countLeaves l + 0` typos.
- **Perfectly balanced n=7:** good for `countAtDepth` — 4 nodes at depth 2, 2 at depth 1, 1 at depth 0.
- **All identical values** (`Fork 5 ... 5`): `countBT 5` should equal `sizeBT`.
- **Stress for laziness:** `countAtDepth 0 (giantTree)` should be O(1) — bail at depth 0 without touching subtrees.

## Pitfalls (per mutation)
- M1: returning `1` for `Empty` (off-by-one).
- M2: writing the leaf pattern *below* the general `Fork _ l r` — the leaf case is unreachable.
- M3: ditto, and forgetting that a `Fork _ Empty (Fork _ Empty Empty)` is internal.
- M4: counting only at one position (not both subtrees) after a match.
- M5: not relating `countBy` back to `countBT` for sanity.
- M6: not bumping depth by 1 — same depth in both children.
- M7: using `>` instead of `>=` (or vice versa) — read the spec letter by letter.
- M8: pattern-match order bug.
- M9: forgetting to propagate the *updated* max — sometimes a student keeps `m` unchanged.
- M10: not strictifying the pair add — easy space leak on big trees.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — countByDepth (returns assoc list)

**Spec:** Count nodes at each depth and return the result as an association list `[(depth, count)]`.

**Type sig:** `countByDepth :: BT a -> [(Int, Int)]`

```haskell
countByDepth :: BT a -> [(Int, Int)]
countByDepth t = aggregate (go t 0)
  where
    go Empty        _ = []
    go (Fork _ l r) d = d : go l (d+1) ++ go r (d+1)
    aggregate ds = [(d, length (filter (==d) ds)) | d <- [0 .. maximum (0:ds)]]
```

**What changes vs seed:** Result shape changes from `Int` to `[(Int, Int)]` — a structural reshape, not just a different scalar combine. Two-pass: collect depths, then aggregate.

**QC trap:** `countByDepth Empty` should be `[]` not `[(0,0)]`. The `maximum (0:ds)` guard is what saves the empty case from a crash.

### Mutation 12 — countSatisfyingWithAccumulator (single-pass strict accumulator)

**Spec:** Count nodes whose value satisfies a predicate, using an accumulator threaded through both subtrees (no foldr).

**Type sig:** `countSatisfyingAcc :: (a -> Bool) -> BT a -> Int`

```haskell
countSatisfyingAcc :: (a -> Bool) -> BT a -> Int
countSatisfyingAcc p = go 0
  where
    go !acc Empty        = acc
    go !acc (Fork x l r) = go (go (if p x then acc+1 else acc) l) r
```

**What changes vs seed:** Different evaluation strategy: strict accumulator (`!acc`) with left-fold order. Compare with the standard structural `1 + sumL + sumR` form. Avoids deep thunks on skewed trees.

**QC trap:** `go (go acc l) r` order matters — swapping to `go (go acc r) l` traverses the tree right-first. Final count is the same but trace order differs (visible if you tee a Writer through it).

## Additional Phase-12 mutations (cap relaxed to 25)

The previous 12 cover the canonical and one-twist variants. The following close gaps with specifically different recursion shapes / accumulators / output types.

### Mutation 13 — sizeAndHeight (tuple-result single pass)
**Sig:** `sizeAndHeight :: BT a -> (Int, Int)`
**Spec:** Return `(size, height)` in one traversal.
```haskell
sizeAndHeight :: BT a -> (Int, Int)
sizeAndHeight Empty        = (0, 0)
sizeAndHeight (Fork _ l r) = (1 + sl + sr, 1 + max hl hr)
  where (sl, hl) = sizeAndHeight l
        (sr, hr) = sizeAndHeight r
```
**Why distinct:** Tuple return type. Combines two folds into one — distinct from M1, M2, M10.
**QC trap:** Both fields must update in lockstep — copy-paste typo can leave `(0, 1+...)` for `Empty`.

### Mutation 14 — countMatchingPath (path predicate)
**Sig:** `countMatchingPath :: ([a] -> Bool) -> BT a -> Int`
**Spec:** Count root-to-leaf paths whose value list satisfies a predicate.
```haskell
countMatchingPath :: ([a] -> Bool) -> BT a -> Int
countMatchingPath p = go []
  where
    go _   Empty                = 0
    go acc (Fork x Empty Empty) = if p (reverse (x:acc)) then 1 else 0
    go acc (Fork x l r)         = go (x:acc) l + go (x:acc) r
```
**Why distinct:** Predicate is on the *path*, not the node. Threads an accumulator down without combining laterally.
**QC trap:** `go _ Empty = 0`, NOT `if p (reverse acc) then 1 else 0`. The naive `Empty` clause counts a phantom path at *every* `Empty` child of an internal node, so a node with one real child and one `Empty` child over-counts. Only a genuine leaf (`Fork x Empty Empty`) is a root-to-leaf path. A one-leaf tree has exactly one path.

### Mutation 15 — mode (most-frequent value)
**Sig:** `mode :: Eq a => BT a -> Maybe a`
**Spec:** The value occurring most often (any one of them on ties). Empty tree → `Nothing`.
```haskell
mode :: Eq a => BT a -> Maybe a
mode Empty = Nothing
mode t     = Just (head (foldr1 longest groups))
  where
    longest a b = if length a >= length b then a else b
    groups      = groupBy (==) (sort (flatten t))
    flatten Empty        = []
    flatten (Fork x l r) = x : flatten l ++ flatten r
```
**Why distinct:** Two-stage (flatten + tally). Maybe return — handles empty.

### Mutation 16 — countDistinct (unique values)
**Sig:** `countDistinct :: Eq a => BT a -> Int`
**Spec:** Number of distinct values.
```haskell
countDistinct :: Eq a => BT a -> Int
countDistinct = length . nub . flatten
  where flatten Empty        = []
        flatten (Fork x l r) = x : flatten l ++ flatten r
```
**Why distinct:** Set-cardinality, not multiset-cardinality. Distinct from M1/M2.

### Mutation 17 — countWithDepthBound (predicate sees depth)
**Sig:** `countWithDepthBound :: Int -> BT a -> Int`
**Spec:** Count nodes whose depth is `<= bound`.
```haskell
countWithDepthBound :: Int -> BT a -> Int
countWithDepthBound bound = go 0
  where
    go _ Empty        = 0
    go d (Fork _ l r)
      | d > bound     = 0           -- bail early
      | otherwise     = 1 + go (d+1) l + go (d+1) r
```
**Why distinct:** Bail-out short-circuit when depth exceeded — only mutation in the family that *avoids* visiting subtrees.

## See also

**Primary archetype:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Sibling families:** [tree-extract](./tree-extract-family.md) · [tree-validation](./tree-validation-family.md) · [rose-ops](./rose-ops-family.md)
**Cross-topic:** [tree × state](../cross-matrix/tree-x-state.md) · [tree × writer](../cross-matrix/tree-x-writer.md) · [tree × maybe](../cross-matrix/tree-x-maybe.md)
**Theory:** [binary tree](../trees/binary-tree.md) · [tree fold](../trees/tree-fold.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md)
**Pitfalls:** [P-005 missing base case](../pitfalls/HIGH-severity.md#p-005)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
