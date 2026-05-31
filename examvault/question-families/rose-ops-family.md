<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: rose-ops**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · **rose-ops** · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: rose-ops

**Archetype:** A03+A04+A05+A06 specialised to rose trees   |   **Stars:** ⭐⭐⭐   |   **Course week(s):** 6–7
**Search keywords:** Rose, sizeRose, heightRose, flattenRose, isNBranching, prune, mapRose, foldRose

## Generator template
```haskell
-- There are two common Rose tree shapes — the question will specify which.
-- Variant A (values at every node):
data Rose a = Branch a [Rose a]

-- Variant B (values only at leaves) — the mock test variant:
data Rose a = Leaf a | Branch [Rose a]

-- Seed for variant A:
seed :: Rose a -> Result
seed (Branch v children) = combine (g v) (map seed children)

-- Seed for variant B:
seed (Leaf x)            = leafResult x
seed (Branch children)   = combine (map seed children)
```

## Mutations (the examiner picks one)

### Mutation 1 — sizeRose (= problem 86)
**Spec:** Count all nodes (including root).
**Variant A Sig:** `sizeRose :: Rose a -> Int`
**Solution (Variant A):**
```haskell
sizeRose :: Rose a -> Int
sizeRose (Branch _ children) = 1 + sum (map sizeRose children)
```
**Solution (Variant B):**
```haskell
sizeRose :: Rose a -> Int
sizeRose (Leaf _)         = 1
sizeRose (Branch children) = sum (map sizeRose children)
```
**QC trap:** Variant B's `Branch []` has size 0 (no leaves below). Variant A's `Branch x []` has size 1 (the root).

### Mutation 2 — heightRose (= problem 87)
**Spec:** A leaf has height 1; a branch is 1 + max child height.
**Sig:** `heightRose :: Rose a -> Int`
**Solution (Variant A):**
```haskell
heightRose :: Rose a -> Int
heightRose (Branch _ []) = 1
heightRose (Branch _ cs) = 1 + maximum (map heightRose cs)
```
**Solution (Variant B):**
```haskell
heightRose :: Rose a -> Int
heightRose (Leaf _)      = 1
heightRose (Branch [])   = 0
heightRose (Branch cs)   = 1 + maximum (map heightRose cs)
```
**QC trap:** Empty children list. Use `maximum`, not `max` on the list. Variant B's `Branch []` is a "branch with no children" — convention says height 0.

### Mutation 3 — flattenRose (= problem 88)
**Spec:** Pre-order traversal.
**Variant A Sig:** `flattenRose :: Rose a -> [a]`
**Solution (Variant A):**
```haskell
flattenRose :: Rose a -> [a]
flattenRose (Branch v cs) = v : concatMap flattenRose cs
```
**Solution (Variant B):**
```haskell
flattenRose :: Rose a -> [a]
flattenRose (Leaf x)      = [x]
flattenRose (Branch cs)   = concatMap flattenRose cs
```
**QC trap:** Watch for the constructor difference. The mock test uses Variant B.

### Mutation 4 — isNBranching (= mock Q1 / problem 143)
**Spec:** Every Branch has exactly `n` children.
**Sig:** `isNBranching :: Int -> Rose a -> Bool`
**Solution (Variant B):**
```haskell
data Rose a = Leaf a | Branch [Rose a]

isNBranching :: Int -> Rose a -> Bool
isNBranching _ (Leaf _)         = True
isNBranching n (Branch forest)  = length forest == n
                               && all (isNBranching n) forest
```
**QC trap:** Leaves trivially satisfy. `Branch []` only satisfies `isNBranching 0`.

### Mutation 5 — prune (= mock Q1 / problem 143)
**Spec:** Keep at most `n` children at every Branch.
**Sig:** `prune :: Int -> Rose a -> Rose a`
**Solution (Variant B):**
```haskell
prune :: Int -> Rose a -> Rose a
prune _ (Leaf x)        = Leaf x
prune n (Branch forest) = Branch (take n (map (prune n) forest))
```
**QC trap:** `take n . map (prune n)` vs `map (prune n) . take n` — both equivalent thanks to laziness, but the former is the official solution.

### Mutation 6 — mapRose (Functor)
**Sig:** `mapRose :: (a -> b) -> Rose a -> Rose b`
**Solution (Variant A):**
```haskell
mapRose :: (a -> b) -> Rose a -> Rose b
mapRose f (Branch v cs) = Branch (f v) (map (mapRose f) cs)
```
**Solution (Variant B):**
```haskell
mapRose :: (a -> b) -> Rose a -> Rose b
mapRose f (Leaf x)      = Leaf (f x)
mapRose f (Branch cs)   = Branch (map (mapRose f) cs)
```
**Common bug — do NOT copy this:** forgetting to thread `f` through the recursive call:
```haskell
-- WRONG: passes id instead of f to the recursion, so the Branch subtree
-- is never mapped. This does not even typecheck against the signature
-- (a -> b) -> Rose a -> Rose b: `mapRose id cs` yields Rose a, but the
-- Leaf clause forces the result to Rose b, so GHC reports
-- "Couldn't match type `a' with `b'". A classic exam-killer.
mapRose _ (Branch cs)   = Branch (map (mapRose id) cs)   -- BUG
```
Always pass the *same* `f` to the recursive call.

### Mutation 7 — foldRose (generic structural fold)
**Sig:** `foldRose :: (a -> [b] -> b) -> Rose a -> b` (Variant A)
**Solution:**
```haskell
foldRose :: (a -> [b] -> b) -> Rose a -> b
foldRose f (Branch v cs) = f v (map (foldRose f) cs)

-- Then:
sizeRose'   = foldRose (\_ xs -> 1 + sum xs)
heightRose' = foldRose (\_ xs -> if null xs then 1 else 1 + maximum xs)
flatten'    = foldRose (\v xs -> v : concat xs)
```
**QC trap:** Once you've defined `foldRose`, every other operation is a one-liner — but the exam usually wants the explicit recursion.

### Mutation 8 — countLeavesRose (Variant A — count nodes with no children)
**Spec:** Count `Branch v []` instances.
**Sig:** `countLeavesRose :: Rose a -> Int`
**Solution (Variant A):**
```haskell
countLeavesRose :: Rose a -> Int
countLeavesRose (Branch _ []) = 1
countLeavesRose (Branch _ cs) = sum (map countLeavesRose cs)
```
**QC trap:** In Variant A, a leaf is a Branch with empty children list. In Variant B, a leaf is the `Leaf` constructor itself.

### Mutation 9 — toRose / fromRose (= Assignment 3 Task 1 — isomorphic with Free [])
**Spec:** Convert between `Rose a` and `Free [] a`.
**Sig:** `toRose :: Free [] a -> Rose a` and `fromRose :: Rose a -> Free [] a`
**Solution (Variant B, the assignment's variant):**
```haskell
data Rose a = Lf a | Br [Rose a]
data Free f a = Pure a | Free (f (Free f a))

toRose :: Free [] a -> Rose a
toRose (Pure x)   = Lf x
toRose (Free xs)  = Br (map toRose xs)

fromRose :: Rose a -> Free [] a
fromRose (Lf x)   = Pure x
fromRose (Br xs)  = Free (map fromRose xs)
```
**QC trap:** `Pure ↔ Lf` and `Free ↔ Br`. Round-trip property: `toRose . fromRose == id` and `fromRose . toRose == id`.

### Mutation 10 — maxDepthValue (find value at greatest depth)
**Spec:** Return the leftmost value at the deepest level.
**Sig:** `deepestValue :: Rose a -> Maybe a`
**Solution (Variant A):**
```haskell
deepestValue :: Rose a -> Maybe a
deepestValue r = Just (snd (go 0 r))
  where
    go d (Branch v []) = (d, v)
    go d (Branch v cs) = let opts = map (go (d+1)) cs
                         in  maximumBy compareFst opts
    compareFst (a, _) (b, _) = compare a b
```
**QC trap:** Two trees of equal depth need tie-breaking. "Leftmost" means *first* in the children list.

## Hidden-predicate mutations
- "Count nodes satisfying predicate p" → straightforward.
- "Prune subtrees whose root value fails p" → conditional prune (different from depth-prune):
```haskell
filterRose :: (a -> Bool) -> Rose a -> Maybe (Rose a)
filterRose p (Branch v cs)
  | p v       = Just (Branch v (mapMaybe (filterRose p) cs))
  | otherwise = Nothing
```

## Accumulator-style alternative
For sizes/heights you can thread an accumulator through `foldl`:
```haskell
sizeRoseAcc r = go 0 r
  where
    go !acc (Branch _ cs) = foldl go (acc + 1) cs
```

## Fold-style alternative
See Mutation 7 above — `foldRose` gives all the unary operations as one-liners.

## Cross-family combinations
- this family + `tree-counting-family.md`: similar counting recursions, different constructor.
- this family + `tree-validation-family.md`: isNBranching is the rose-tree mirror of value/shape predicates.
- this family + `tree-transform-family.md`: prune.
- this family + `state-counter-family.md`: labelling rose-trees (see Mutation 7 of state-counter-family).
- this family + `monad-combinator-family.md`: mapM over rose trees.

## QuickCheck universal attacks
- **Leaf:** trivially everything except Branch-counting.
- **`Branch v []` (Variant A leaf):** matches the "leaf" case.
- **`Branch []` (Variant B):** valid but vacuous; only satisfies `isNBranching 0`.
- **All-leaves Branch:** validates the "all children are leaves" case.
- **Deeply nested Branch [Branch [Branch [...]]]:** stack-safety.
- **`prune n (prune n t) == prune n t`** — idempotent.
- **`mapRose id == id`** — Functor identity.

## Pitfalls (per mutation)
- M1: forgetting to add 1 (Variant A's root counts).
- M2: max-of-empty crashes — guard with the `[]` case.
- M3: confusing variant A vs variant B constructor patterns.
- M4: forgetting that Leaf is always OK.
- M5: `take n . map vs map . take n` matters for performance only (both correct semantically).
- M6: not propagating `f` to recursive call.
- M7: wrong fold signature.
- M8: leaf detection wrong for the variant.
- M9: confusing Pure/Free with Lf/Br.
- M10: leftmost vs rightmost tie-breaking.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — isNBranchingOrLeaf (relaxed predicate — branches can be Leaf or n-children)

**Spec:** A relaxed isNBranching: a `Branch` must have either 0 children (degenerate) or exactly n. Helps prune Mock-style spec ambiguity.

**Type sig:** `isNBranchingRelaxed :: Int -> Rose a -> Bool`

```haskell
isNBranchingRelaxed :: Int -> Rose a -> Bool
isNBranchingRelaxed _ (Leaf _)            = True
isNBranchingRelaxed n (Branch xs)
  | k == 0 || k == n = all (isNBranchingRelaxed n) xs
  | otherwise        = False
  where k = length xs
```

**What changes vs seed:** Same recursion shape as `isNBranching` but the predicate at each node permits two arities. Different *predicate kind*.

**QC trap:** `Branch []` — does it count as 'leaf-like' or as 'failed n-branch'? The relaxed version permits it, the strict version doesn't. Read the spec carefully.

## See also

**Primary archetype:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Sibling families:** [tree-counting](./tree-counting-family.md) · [tree-validation](./tree-validation-family.md) · [tree-transform](./tree-transform-family.md) · [tree-extract](./tree-extract-family.md)
**Cross-topic:** [rose × state](../cross-matrix/rose-x-state.md) · [rose × writer](../cross-matrix/rose-x-writer.md)
**Theory:** [rose tree](../trees/rose-tree.md)
**QuickCheck:** [rose attacks](../quickcheck/rose-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
