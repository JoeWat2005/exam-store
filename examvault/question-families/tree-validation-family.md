<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: tree-validation**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · **tree-validation** · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: tree-validation

**Archetype:** A04 (recursive predicate / "all-children-satisfy")   |   **Stars:** ⭐⭐⭐   |   **Course week(s):** 6–7
**Search keywords:** isBST, isBalanced, isComplete, isMirror, isHeap, isNBranching, predicate, structural test

## Generator template
```haskell
-- The seed: a Bool-returning structural predicate on a BT a.
-- Pattern: Empty is the unit (True); a Fork is True iff some local condition
-- holds AND both subtrees recursively satisfy the predicate.
data BT a = Empty | Fork a (BT a) (BT a)

seed :: BT a -> Bool
seed Empty        = True
seed (Fork _ l r) = localOK l r && seed l && seed r
  where localOK _ _ = True   -- the slot the examiner mutates
```

## Mutations (the examiner picks one)

### Mutation 1 — isBST (binary search tree)
**Spec:** In-order traversal is strictly increasing.
**Sig:** `isBST :: Ord a => BT a -> Bool`
**What changes vs seed:** `localOK` becomes "every left-subtree value < v < every right-subtree value". Easiest implementation: flatten in-order, then check strictly-sorted.
**Solution:**
```haskell
isBST :: Ord a => BT a -> Bool
isBST = strictSorted . flatten
  where
    flatten Empty        = []
    flatten (Fork v l r) = flatten l ++ [v] ++ flatten r
    strictSorted xs      = and (zipWith (<) xs (tail xs))
```
**QC trap:** `[]` and `[x]` are vacuously strictly sorted. Duplicates *must* return `False` (strict `<`, not `<=`).

### Mutation 2 — isBalanced (height-balanced AVL-style)
**Spec:** At every node, |height(left) - height(right)| <= 1.
**Sig:** `isBalanced :: BT a -> Bool`
**What changes vs seed:** `localOK` requires both subtrees' heights to differ by at most 1.
**Solution:**
```haskell
isBalanced :: BT a -> Bool
isBalanced Empty        = True
isBalanced (Fork _ l r) = abs (h l - h r) <= 1 && isBalanced l && isBalanced r
  where
    h Empty        = 0
    h (Fork _ a b) = 1 + max (h a) (h b)
```
**QC trap:** O(n^2). For the fast version, fuse height+balance and use `Nothing` as "unbalanced":
```haskell
isBalancedFast :: BT a -> Bool
isBalancedFast = ok . go
  where go Empty = Just 0
        go (Fork _ l r) = do
          a <- go l; b <- go r
          if abs (a-b) <= 1 then Just (1 + max a b) else Nothing
        ok = maybe False (const True)
```

### Mutation 3 — isComplete (every level full except possibly the last, left-filled)
**Spec:** Level-order traversal: once you see an `Empty`, every subsequent slot must also be `Empty`.
**Sig:** `isComplete :: BT a -> Bool`
**What changes vs seed:** Need a queue traversal (BFS), not a recursive structural one.
**Solution:**
```haskell
isComplete :: BT a -> Bool
isComplete t = scan [t] False
  where
    scan []     _      = True
    scan (Empty:ts) _  = scan ts True
    scan (Fork _ l r : ts) seenEmpty
      | seenEmpty      = False
      | otherwise      = scan (ts ++ [l,r]) False
```
**QC trap:** The seed pattern doesn't fit this one — you can't decide completeness from a recursive child predicate alone. Watch for this in interviews: the examiner is testing whether you'll force-fit recursion.

### Mutation 4 — isNBranching (rose-tree variant — from mock test Q1)
**Spec:** Every `Branch` of the rose tree has exactly `n` children.
**Sig:** `isNBranching :: Int -> Rose a -> Bool`
**What changes vs seed:** Switches to a rose tree; `localOK` is `length children == n`; recursion uses `all`.
**Solution:**
```haskell
data Rose a = Leaf a | Branch [Rose a]

isNBranching :: Int -> Rose a -> Bool
isNBranching _ (Leaf _)        = True
isNBranching n (Branch forest) = length forest == n
                              && all (isNBranching n) forest
```
**QC trap:** Leaves are *always* OK regardless of `n`. A `Branch []` only satisfies `isNBranching 0`. (This is canonical — appears verbatim on the 2024 mock.)

### Mutation 5 — isHeap (max-heap shape predicate)
**Spec:** Every parent's value is `>=` every child's value.
**Sig:** `isMaxHeap :: Ord a => BT a -> Bool`
**What changes vs seed:** `localOK l r` checks `v >= rootVal l` and `v >= rootVal r` where rootVal is the value at a non-empty child.
**Solution:**
```haskell
isMaxHeap :: Ord a => BT a -> Bool
isMaxHeap Empty        = True
isMaxHeap (Fork v l r) = bigger v l && bigger v r
                      && isMaxHeap l && isMaxHeap r
  where
    bigger _ Empty        = True
    bigger x (Fork w _ _) = x >= w
```
**QC trap:** Equal values are allowed (`>=`). Empty children always pass. Don't forget to recurse — a single check at the root is not enough.

### Mutation 6 — isMirror (two trees structurally mirror each other)
**Spec:** `isMirror t1 t2` iff `t2` is `t1` with every Fork's children swapped.
**Sig:** `isMirror :: Eq a => BT a -> BT a -> Bool`
**What changes vs seed:** Binary predicate (two trees) instead of unary; cross-recursion swaps L↔R.
**Solution:**
```haskell
isMirror :: Eq a => BT a -> BT a -> Bool
isMirror Empty Empty               = True
isMirror (Fork a l1 r1) (Fork b l2 r2)
                                   = a == b
                                  && isMirror l1 r2
                                  && isMirror r1 l2
isMirror _ _                       = False
```
**QC trap:** The catch-all `_ _ = False` is essential — without it pattern-match is incomplete (`Empty` vs `Fork` etc.).

### Mutation 7 — isSymmetric (single tree, internally mirrored)
**Spec:** A tree is symmetric iff its left subtree mirrors its right subtree.
**Sig:** `isSymmetric :: Eq a => BT a -> Bool`
**What changes vs seed:** Reduces to mutation 6 applied to root's two children.
**Solution:**
```haskell
isSymmetric :: Eq a => BT a -> Bool
isSymmetric Empty        = True
isSymmetric (Fork _ l r) = isMirror l r
```
**QC trap:** A skewed tree is NOT symmetric. Don't confuse "every left=right value" with mirror structure (e.g. mirror requires l1↔r2 cross, not l1↔l2).

### Mutation 8 — isFull (every node has 0 or 2 children — no unary nodes)
**Spec:** A `Fork _ Empty Empty` (leaf) is OK; `Fork _ l r` with both non-empty is OK; mixed is not.
**Sig:** `isFull :: BT a -> Bool`
**What changes vs seed:** `localOK l r` is "both empty or both non-empty".
**Solution:**
```haskell
isFull :: BT a -> Bool
isFull Empty                          = True
isFull (Fork _ Empty Empty)           = True
isFull (Fork _ Empty _)               = False
isFull (Fork _ _ Empty)               = False
isFull (Fork _ l r)                   = isFull l && isFull r
```
**QC trap:** Mutation order matters. The mixed cases (rows 3 and 4) MUST be matched before the catch-all `Fork _ l r`. Otherwise the `&&` fires recursively when it shouldn't.

### Mutation 9 — isAllPositive (value-only predicate)
**Spec:** Every stored value is positive.
**Sig:** `isAllPositive :: (Ord a, Num a) => BT a -> Bool`
**What changes vs seed:** `localOK` only inspects `v`, ignores subtree shapes.
**Solution:**
```haskell
isAllPositive :: (Ord a, Num a) => BT a -> Bool
isAllPositive Empty        = True
isAllPositive (Fork v l r) = v > 0 && isAllPositive l && isAllPositive r
```
**QC trap:** Empty tree is vacuously True. Watch the strictness: `v > 0` (not `>=`).

### Mutation 10 — allBT (hidden predicate version of mutation 9)
**Spec:** Every stored value satisfies the supplied predicate.
**Sig:** `allBT :: (a -> Bool) -> BT a -> Bool`
**What changes vs seed:** Predicate becomes a parameter — strictly generalises mutation 9.
**Solution:**
```haskell
allBT :: (a -> Bool) -> BT a -> Bool
allBT _ Empty        = True
allBT p (Fork v l r) = p v && allBT p l && allBT p r
```
**QC trap:** `allBT (const True) == const True`; `allBT (const False) == isEmpty`.

## Hidden-predicate mutations
Mutation 10 is the canonical "examiner adds a predicate parameter" twist. Watch for spec wording:
- "Every value is in this list" → `allBT (`elem` xs)`
- "No value exceeds k" → `allBT (<= k)`
- "Every node passes a validation function" → `allBT validate`

Another twist: change `&&` to `||` to get an "any" predicate (`anyBT`). The shape is identical.

## Accumulator-style alternative
For value-only predicates, fuse with a fold-Bool:
```haskell
foldOk :: (a -> Bool) -> Bool -> BT a -> Bool
foldOk _ acc Empty        = acc
foldOk p acc (Fork v l r) = foldOk p (foldOk p (acc && p v) l) r
```
But this *loses short-circuiting* — `allBT` short-circuits at the first `False` thanks to Haskell's lazy `&&`. The fold version evaluates more.

## Fold-style alternative
Express via `foldBT` (see tree-counting-family.md):
```haskell
isMaxHeap'    = foldBT True (\v ls rs -> ls && rs && ...)   -- but lose access to child root values
```
Be careful: predicates needing to inspect *child node values* (heap, mirror, BST-via-range) don't reduce cleanly to `foldBT` because the fold loses the children's structure.

## Cross-family combinations
- this family + `bst-ops-family.md` (isBST → insertBST → memberBST chain)
- this family + `tree-counting-family.md` (`countBT = length . filter . flatten`)
- this family + state monad (validate while labelling — see `state-counter-family.md`)

## QuickCheck universal attacks
- **Empty:** every "structural" predicate returns True on Empty.
- **Singleton:** Fork v Empty Empty is True for every reasonable predicate.
- **Skewed left (depth=100):** `isBalanced` fails; `isBST` may pass if values descend.
- **Mirror of self:** `isSymmetric` should be True. Use `mirror t == t` as a checking property.
- **Duplicate at root and child:** `isBST` should be False (strict inequality).
- **All values equal:** `isMaxHeap` True; `isBST` False; `isFull` depends on shape.

## Pitfalls (per mutation)
- M1: using `<=` instead of `<` (duplicates incorrectly pass).
- M2: doing height in `O(n)` inside the predicate, blowing up to `O(n²)` total.
- M3: trying to do completeness recursively (you can't without rank info).
- M4: forgetting that leaves are always OK.
- M5: comparing only with children's `v` but not recursing.
- M6: missing the `_ _ = False` fallthrough.
- M7: confusing structural mirror with value mirror.
- M8: putting the catch-all pattern too early.
- M9: using `>=` 0 instead of `>` 0 (or vice versa).
- M10: forgetting the empty case returns True.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — isPathSumK (root-to-leaf path sum equals k — DFS with path accumulator)

**Spec:** True iff some root-to-leaf path's sum equals `k`. Tests every path; returns True if any matches.

**Type sig:** `isPathSumK :: (Num a, Eq a) => a -> BT a -> Bool`

```haskell
isPathSumK :: (Num a, Eq a) => a -> BT a -> Bool
isPathSumK _ Empty                       = False
isPathSumK k (Fork x Empty Empty)        = x == k
isPathSumK k (Fork x l r)                = isPathSumK (k-x) l || isPathSumK (k-x) r
```

**What changes vs seed:** Recursion threads a numeric accumulator (the *remaining* target) DOWN the tree. Most validations sum/check UP; this one decrements down. Different recursion direction.

**QC trap:** Distinguish leaves (`Fork x Empty Empty`) from internal nodes whose subtrees are both empty after pruning. The clause order matters — must put the leaf clause before the general one.

### Mutation 12 — isBalanced (height check — single-pass returning Maybe Int)

**Spec:** True iff every node's left and right subtree heights differ by at most 1. Returns `Maybe Int` (Just height if balanced, Nothing if not) to avoid recomputing heights.

**Type sig:** `isBalanced :: BT a -> Maybe Int`

```haskell
isBalanced :: BT a -> Maybe Int
isBalanced Empty        = Just 0
isBalanced (Fork _ l r) = do
  hl <- isBalanced l
  hr <- isBalanced r
  if abs (hl - hr) <= 1 then Just (1 + max hl hr) else Nothing
```

**What changes vs seed:** Uses the Maybe monad in `do`-notation to short-circuit AND carry the computed height — avoids the naive O(n²) "compute height at every node" approach.

**QC trap:** Returning `Just 0` for `Empty` (not `Nothing`) is correct — an empty tree IS balanced. Students often write `Nothing` for empty and then everything bubbles up as imbalanced.

## Additional Phase-12 mutations (cap relaxed to 25)

### Mutation 13 — isSubtreeOf (structural subtree check)
**Sig:** `isSubtreeOf :: Eq a => BT a -> BT a -> Bool`
**Spec:** True iff the first tree is structurally identical to some subtree of the second.
```haskell
isSubtreeOf :: Eq a => BT a -> BT a -> Bool
isSubtreeOf t s = sameShape t s || case s of
  Empty        -> False
  Fork _ l r   -> isSubtreeOf t l || isSubtreeOf t r
  where
    sameShape Empty Empty                   = True
    sameShape (Fork x l1 r1) (Fork y l2 r2) = x == y && sameShape l1 l2 && sameShape r1 r2
    sameShape _ _                           = False
```
**Why distinct:** Cross-tree comparison. Two recursions inside one — `sameShape` and the outer scan. New shape.

### Mutation 14 — hasUniqueValues (set predicate)
**Sig:** `hasUniqueValues :: Eq a => BT a -> Bool`
**Spec:** No value appears more than once in the tree.
```haskell
hasUniqueValues :: Eq a => BT a -> Bool
hasUniqueValues t = let xs = flatten t in length xs == length (nub xs)
  where flatten Empty        = []
        flatten (Fork x l r) = x : flatten l ++ flatten r
```
**Why distinct:** Set-cardinality predicate; collects then compares lengths.

### Mutation 15 — isFullAndComplete (perfect-tree check)
**Sig:** `isPerfect :: BT a -> Bool`
**Spec:** Every internal node has 2 children and every leaf is at the same depth.
```haskell
isPerfect :: BT a -> Bool
isPerfect t = case depths t of
  []     -> True
  (d:ds) -> all (== d) ds
  where
    depths Empty                       = []
    depths (Fork _ Empty Empty)        = [0]
    depths (Fork _ Empty _)            = [-1]   -- imbalance signal
    depths (Fork _ _ Empty)            = [-1]
    depths (Fork _ l r)                = map (+1) (depths l ++ depths r)
```
**Why distinct:** Multi-pass through structural depth; rejects asymmetric branches.

### Mutation 16 — allBT (universally-quantified predicate)
**Sig:** `allBT :: (a -> Bool) -> BT a -> Bool`
**Spec:** Predicate holds at every node.
```haskell
allBT :: (a -> Bool) -> BT a -> Bool
allBT _ Empty        = True
allBT p (Fork x l r) = p x && allBT p l && allBT p r
```
**Why distinct:** Generic over predicate — companion to `anyBT`. Often used to define other validations.

### Mutation 17 — isBSTBoundThreaded (explicit bound version)
**Sig:** `isBSTBounded :: Ord a => Maybe a -> Maybe a -> BT a -> Bool`
**Spec:** isBST with explicit lower / upper bound passed down. Demonstrates the canonical bound-threading technique.
```haskell
isBSTBounded :: Ord a => Maybe a -> Maybe a -> BT a -> Bool
isBSTBounded _ _ Empty             = True
isBSTBounded lo hi (Fork v l r)    =
  inRange lo hi v
    && isBSTBounded lo (Just v) l
    && isBSTBounded (Just v) hi r
  where
    inRange lo' hi' x = maybe True (< x) lo' && maybe True (x <) hi'
```
**Why distinct:** Bound-threading. Avoids the O(n²) `allLT` / `allGT` pitfall.

## See also

**Primary archetype:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Sibling families:** [bst-ops](./bst-ops-family.md) · [tree-counting](./tree-counting-family.md) · [rose-ops](./rose-ops-family.md)
**Cross-topic:** [tree × maybe](../cross-matrix/tree-x-maybe.md)
**Theory:** [binary tree](../trees/binary-tree.md) · [bst](../trees/bst.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md) · [bst attacks](../quickcheck/bst-attacks.md)
**Pitfalls:** [P-009 isBST Empty = False](../pitfalls/HIGH-severity.md#p-009) · [P-014 shallow recursion](../pitfalls/HIGH-severity.md#p-014)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
