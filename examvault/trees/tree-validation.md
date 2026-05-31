<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [trees](./README.md) · **Tree validation — the predicate family**

<!-- siblings:start -->
> **Peers:** [binary-tree](./binary-tree.md) · [bst-delete-trace](./bst-delete-trace.md) · [bst](./bst.md) · [expression-tree](./expression-tree.md) · [rose-tree](./rose-tree.md) · [tree-counting](./tree-counting.md) · [tree-fold](./tree-fold.md) · [tree-functor](./tree-functor.md) · [tree-traversals](./tree-traversals.md) · **tree-validation** · [tree-zipper](./tree-zipper.md)
<!-- siblings:end -->






# Tree validation — the predicate family

Twin sibling of [tree-counting.md](tree-counting.md). Every "is this tree X?" question is the same pattern: walk every Fork, decide what the local invariant is, AND the recursive call.

## The template

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

validate :: BT a -> Bool
validate Empty        = True                              -- base: vacuously valid
validate (Fork x l r) = localOK x l r
                     && validate l
                     && validate r
```
Empty always returns True (an empty tree satisfies any "for every node…" predicate vacuously). The Fork case checks the LOCAL invariant and recurses.

## The family — one-line mutations

### `isBST` — bound-threaded (linear time)

```haskell
isBST :: Ord a => BT a -> Bool
isBST = go Nothing Nothing
  where
    go _   _  Empty        = True
    go lo  hi (Fork x l r) =
        maybe True (< x) lo
     && maybe True (x <) hi
     && go lo (Just x) l
     && go (Just x) hi r
```
Local invariant: `lo < x < hi`. Bounds tighten as we descend. See [bst.md](bst.md) for the naive O(n²) and flatten-and-check versions.

### `isComplete` — every level full except possibly the last (and last is filled left-to-right)

```haskell
isComplete :: BT a -> Bool
isComplete t = case go t of Just _ -> True; Nothing -> False
  where
    -- Returns Just depth if t is a complete subtree of that depth.
    -- Tricky: must enforce shape rules at each level.
    go Empty        = Just 0
    go (Fork _ l r) = do
        dl <- go l
        dr <- go r
        if   dl == dr     then Just (dl + 1)     -- perfect on both sides
        else if dl == dr + 1                     -- left one deeper; OK only if right is perfect
             && isPerfect r then Just (dl + 1)
        else Nothing
    isPerfect Empty        = True
    isPerfect (Fork _ l r) = isPerfect l && isPerfect r && height l == height r
```
Simpler-but-O(n²) version (good for exam):
```haskell
isCompleteSimple :: BT a -> Bool
isCompleteSimple t = let xs = bfsWithEmpty t
                     in all isFork (takeWhile isFork xs) && all isEmpty (dropWhile isFork xs)
  where
    bfsWithEmpty Empty        = [Empty]
    bfsWithEmpty t@(Fork _ l r) = t : bfsWithEmpty l ++ bfsWithEmpty r
    isFork (Fork _ _ _) = True; isFork _ = False
    isEmpty Empty       = True; isEmpty _ = False
```

### `isFull` — every Fork has either 0 or 2 non-empty children

```haskell
isFull :: BT a -> Bool
isFull Empty                = True
isFull (Fork _ Empty Empty) = True                        -- leaf
isFull (Fork _ Empty _)     = False                       -- only one child
isFull (Fork _ _ Empty)     = False                       -- only one child
isFull (Fork _ l r)         = isFull l && isFull r        -- both: recurse
```

### `isPerfect` — every leaf at the same depth, every internal has two children

```haskell
isPerfect :: BT a -> Bool
isPerfect Empty        = True
isPerfect (Fork _ l r) = height l == height r && isPerfect l && isPerfect r
-- needs `height`; alternatively pass depth as accumulator and check at leaves
```

### `isBalanced` — height-balanced (|h(l) - h(r)| ≤ 1 everywhere)

```haskell
isBalanced :: BT a -> Bool
isBalanced Empty        = True
isBalanced (Fork _ l r) = abs (height l - height r) <= 1
                       && isBalanced l && isBalanced r
-- O(n²) — recomputes height. Linear-time version:

isBalancedLinear :: BT a -> Bool
isBalancedLinear = (/= -1) . check
  where
    check Empty        = 0
    check (Fork _ l r) = case (check l, check r) of
        (-1, _) -> -1
        (_, -1) -> -1
        (hl, hr) | abs (hl - hr) > 1 -> -1
                 | otherwise         -> 1 + max hl hr
-- returns height, or -1 if unbalanced; short-circuits
```

### `isHeap` — value-monotone (max-heap variant)

```haskell
isMaxHeap :: Ord a => BT a -> Bool
isMaxHeap Empty        = True
isMaxHeap (Fork x l r) = atMost x l && atMost x r && isMaxHeap l && isMaxHeap r
  where atMost _ Empty            = True
        atMost m (Fork y _ _)     = y <= m
-- O(n²); linear-time bound-thread version available
```

### `isNBranching` — for Rose B (Mock Q1)

```haskell
data Rose a = Leaf a | Branch [Rose a]

isNBranching :: Int -> Rose a -> Bool
isNBranching _ (Leaf _)        = True
isNBranching n (Branch forest) = length forest == n
                              && all (isNBranching n) forest
-- the Mock Q1 answer; the `all (isNBranching n)` recursion is essential
```

### `isMirrorOf` — two trees are mirror images

```haskell
isMirrorOf :: Eq a => BT a -> BT a -> Bool
isMirrorOf Empty Empty                            = True
isMirrorOf (Fork x l1 r1) (Fork y l2 r2)          = x == y
                                                 && isMirrorOf l1 r2
                                                 && isMirrorOf r1 l2
isMirrorOf _ _                                    = False
-- in pair-recursion: left-of-first ↔ right-of-second
```

### `isSubtreeOf` — t1 occurs anywhere inside t2

```haskell
isSubtreeOf :: Eq a => BT a -> BT a -> Bool
isSubtreeOf t1 t2 = t1 `equalsAt` t2 || case t2 of
    Empty        -> False
    Fork _ l r   -> isSubtreeOf t1 l || isSubtreeOf t1 r
  where
    equalsAt Empty Empty                     = True
    equalsAt (Fork x la ra) (Fork y lb rb)   = x == y && equalsAt la lb && equalsAt ra rb
    equalsAt _ _                              = False
-- O(n*m) naive; KMP-style speedup is beyond exam scope
```

### `isSorted` — for the BST case (alias)

```haskell
isSorted :: Ord a => BT a -> Bool
isSorted = isBST
```

### `hasProperty p` — every node satisfies p

```haskell
hasProperty :: (a -> Bool) -> BT a -> Bool
hasProperty _ Empty        = True
hasProperty p (Fork x l r) = p x && hasProperty p l && hasProperty p r
-- this is `all p` via Foldable; included for explicit recursion
```

## Combinators

```haskell
-- "&& over a tree" — a clean way to write the family
forAllNodes :: (a -> Bool) -> BT a -> Bool
forAllNodes _ Empty        = True
forAllNodes p (Fork x l r) = p x && forAllNodes p l && forAllNodes p r

-- "|| over a tree"
existsNode :: (a -> Bool) -> BT a -> Bool
existsNode _ Empty        = False
existsNode p (Fork x l r) = p x || existsNode p l || existsNode p r
```

## Family for Rose trees

```haskell
-- Variant A: data Rose a = Branch a [Rose a]
forAllRoseA :: (a -> Bool) -> Rose a -> Bool
forAllRoseA p (Branch x ts) = p x && all (forAllRoseA p) ts

-- Variant B: data Rose a = Leaf a | Branch [Rose a]
forAllRoseB :: (a -> Bool) -> Rose a -> Bool
forAllRoseB p (Leaf x)    = p x
forAllRoseB _ (Branch ts) = all (forAllRoseB (const True)) ts    -- vacuous on Branch
-- or, the more useful form (predicate sees the structure):
allLeavesB :: (a -> Bool) -> Rose a -> Bool
allLeavesB p (Leaf x)    = p x
allLeavesB p (Branch ts) = all (allLeavesB p) ts
```

## Mutations cheat-sheet

| Question phrasing | Specialise |
|-------------------|------------|
| "every value is positive" | `forAllNodes (> 0)` |
| "some node equals 42" | `existsNode (== 42)` |
| "every leaf is even" | thread to leaves only |
| "every internal node has at least 2 children" | for Rose, `length ts >= 2` |
| "every Fork has exactly k descendants" | walk and count, compare |
| "tree is symmetric" | `isMirrorOf t t` |
| "tree obeys heap property AND is complete" | conjunction: `isMaxHeap t && isComplete t` (this is a binary heap) |
| "no two adjacent equal values" | check at every Fork: x ≠ root(l), x ≠ root(r), recurse |

## QuickCheck

```haskell
prop_balancedAfterBalance t       = isBalanced (balance t)
prop_BSTInsertPreserves x t       = isBST t ==> isBST (insert x t)
prop_BSTDeletePreserves x t       = isBST t ==> isBST (delete x t)
prop_perfectIsBalanced t          = isPerfect t ==> isBalanced t
prop_perfectIsComplete t          = isPerfect t ==> isComplete t
prop_completeIsBalanced t         = isComplete t ==> isBalanced t      -- NOT vice versa
prop_mirrorIsMirror t             = isMirrorOf t (mirror t)
prop_subtreeIsSubtree t           = isSubtreeOf t t
prop_subtreeOfEmpty t             = isSubtreeOf Empty t
prop_forAllConst t                = forAllNodes (const True) t
prop_isNBPrune n t                = (n >= 0) ==> isNBranching n (regenAt n t)  -- with helper
```

## Pitfalls

- **Vacuous truth**: `validate Empty = True` for all "for-all-style" predicates. Easy to get wrong — beginners write `False` thinking "empty = invalid".
- **Existential is dual**: `exists Empty = False` (no nodes ⇒ no witness).
- **`isBST Empty = True`** specifically — Empty has no values, hence no violations.
- **`isBalanced` is NOT `isPerfect`**: balanced allows height diff up to 1; perfect requires equal everywhere.
- **`isMirrorOf` is NOT `t == mirror t'`**: structural-eq with values matters; `(Fork 1 (Fork 2 E E) E)` is not a mirror of itself unless you only care about shape.
- **`isComplete` is the trickiest**: easiest correct approach is BFS-with-Empties and check that all Forks come before all Empties in the sequence.
- **`forAllNodes p Empty` is True** — same vacuous-truth point.
- Mock Q1 `isNBranching`: the `Leaf` case is True regardless of n. Branch must check BOTH `length == n` AND recurse.
- Naive `isBST` is quadratic; lecture says so explicitly. Bound-threading is the lecture-approved linear version.
- `isBalanced` recomputing `height` is O(n²); the integer-encoded `-1` short-circuit version is O(n).

## Cross-references

- The counting family (sibling): [tree-counting.md](tree-counting.md)
- BST validation in detail: [bst.md](bst.md)
- Generic fold (alternative expression): [tree-fold.md](tree-fold.md)
- Foldable's `any`/`all`: [tree-functor.md](tree-functor.md), [../typeclasses/foldable.md](../typeclasses/foldable.md)
- Mock Q1 deep dive: [rose-tree.md §Variant B](rose-tree.md)
- Problems: 28 (isSorted), 81 (isBST), 143 (isNBranching)
- Lecture: `fp-learning-2025/files/LectureNotes/Sections/Data2.md` §Binary search trees (isBST proofs)

## See also

**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A11 BST ops](../archetypes/A11-bst-ops.md)
**Question families:** [tree-validation](../question-families/tree-validation-family.md) · [bst-ops](../question-families/bst-ops-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md) · [bst attacks](../quickcheck/bst-attacks.md)
**Related (trees):** [binary tree](./binary-tree.md) · [bst](./bst.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
