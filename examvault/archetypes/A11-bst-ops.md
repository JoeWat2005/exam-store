<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A11 — Binary Search Tree Operations**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · **A11** · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A11 — Binary Search Tree Operations

**Tier:** 2   |   **Stars:** ⭐⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** none direct
**Combines with:** A01 · A05 · A20 · A22
**Search keywords:** BST · binary search tree · insertBST · deleteBST · memberBST · isBST · fromList · ordered

## What it tests
Whether you can write the canonical "3-way Ord guard" insert/member/delete on a BST, AND prove `isBST` correctly using either bound-threading or in-order monotonicity.

## Recognition triggers
- "BST", "binary search tree", "ordered tree"
- "preserving the BST property"
- `Ord a =>` constraint
- The data type is `data BT a = Empty | Fork a (BT a) (BT a)` and the property is sortedness
- Question mentions "left subtree < x < right subtree"
- "delete preserving …"; "merge two BSTs"

## Canonical template
```haskell
data BT a = Empty | Fork a (BT a) (BT a)

isBST :: Ord a => BT a -> Bool
isBST = go Nothing Nothing
  where
    go _   _   Empty        = True
    go lo  hi  (Fork x l r) =
      maybe True (< x) lo
        && maybe True (> x) hi
        && go lo      (Just x) l
        && go (Just x) hi      r

insertBST :: Ord a => a -> BT a -> BT a
insertBST x Empty            = Fork x Empty Empty
insertBST x t@(Fork v l r)
  | x < v     = Fork v (insertBST x l) r
  | x > v     = Fork v l (insertBST x r)
  | otherwise = t        -- duplicate: keep original

memberBST :: Ord a => a -> BT a -> Bool
memberBST _ Empty        = False
memberBST x (Fork v l r)
  | x < v  = memberBST x l
  | x > v  = memberBST x r
  | otherwise = True
```

## Mutations (the examiner picks one)

### M1 — `isBST` via in-order (problem 81)
```haskell
isBST :: Ord a => BT a -> Bool
isBST = isSorted . inOrder
  where
    inOrder Empty        = []
    inOrder (Fork x l r) = inOrder l ++ [x] ++ inOrder r
    isSorted xs = and (zipWith (<) xs (tail xs))   -- strict, no duplicates
```
What changes: uses linearisation; slower (O(n²) due to `++`) but clear.

### M2 — `isBST` via bound-threading (efficient)
See canonical template. What changes: O(n), no allocation, cleaner spec.

### M3 — `insertBST` (problem 82)
See canonical template. What changes: idiomatic.

### M4 — `deleteBST` rightmost-of-left (problem 84)
```haskell
deleteBST :: Ord a => a -> BT a -> BT a
deleteBST _ Empty = Empty
deleteBST x (Fork v l r)
  | x < v = Fork v (deleteBST x l) r
  | x > v = Fork v l (deleteBST x r)
  | otherwise = case (l, r) of
      (Empty, _)         -> r
      (_,     Empty)     -> l
      (l,     r)         -> let (m, l') = popMax l
                            in Fork m l' r
  where
    popMax (Fork x sub Empty) = (x, sub)
    popMax (Fork x l r)       = let (m, r') = popMax r in (m, Fork x l r')
    popMax Empty              = error "popMax on empty"
```
What changes: 4-case on `(l, r)`; popMax returns largest from left subtree.

### M5 — `memberBST` (problem 83)
See canonical template. What changes: O(log n) average, O(n) worst (degenerate to a list).

### M6 — `fromList` (problem 85)
```haskell
fromList :: Ord a => [a] -> BT a
fromList = foldr insertBST Empty
```
What changes: insert from RIGHT (with `foldr`) — or `foldl (flip insertBST)` for left.

### M7 — `bstSort`
```haskell
bstSort :: Ord a => [a] -> [a]
bstSort = flatten . fromList
  where flatten Empty        = []
        flatten (Fork x l r) = flatten l ++ [x] ++ flatten r
```
What changes: combines `fromList` + `inOrder` traversal; duplicates removed silently.

### M8 — `bstUnion` (merge two BSTs)
```haskell
bstUnion :: Ord a => BT a -> BT a -> BT a
bstUnion Empty t = t
bstUnion (Fork x l r) t = bstUnion l (bstUnion r (insertBST x t))
```
What changes: insert every element of one tree into the other.

### M9 — `range` predicate (collect values in `[lo, hi]`)
```haskell
range :: Ord a => a -> a -> BT a -> [a]
range _  _  Empty = []
range lo hi (Fork x l r)
  | x < lo  = range lo hi r
  | x > hi  = range lo hi l
  | otherwise = range lo hi l ++ [x] ++ range lo hi r
```
What changes: pruned in-order — skips subtrees whose values can't be in range.

### M10 — `bstHeight` (problem-extension)
```haskell
bstHeight :: BT a -> Int
bstHeight Empty        = 0
bstHeight (Fork _ l r) = 1 + max (bstHeight l) (bstHeight r)
```
What changes: just a measure; not BST-specific but combines well.

## Worked examples from this course
- Problem sheet Set 9 (#81-85): `isBST`, `insertBST`, `memberBST`, `deleteBST`, `fromList`.
- Practice file `hoogle.hs`: full BST drill.
- Week 6 lecture: introduces BSTs alongside the polymorphic BT type.

## QuickCheck attack surface
- **`isBST Empty == True`** — common bug returns False.
- **`isBST (Fork 5 Empty Empty) == True`**: a singleton is always a BST.
- **Insert preserves BST**: marker generates a random valid BST, inserts a random `x`, checks the result is still a valid BST.
- **Insert is idempotent**: `insertBST x (insertBST x t) == insertBST x t`.
- **Member after insert**: `memberBST x (insertBST x t) == True`.
- **Order of insertion**: `fromList [3,1,2]` and `fromList [1,2,3]` give different trees but `flatten (fromList xs) == sort (nub xs)`.
- **Delete from BST**: `deleteBST x t` is a valid BST AND `not (memberBST x (deleteBST x t))`.
- **Delete root with two children**: handled by rightmost-of-left swap (or leftmost-of-right).

## Pitfalls (marks-killers)
- **`isBST Empty = False`**: marker explicitly tests `isBST Empty == True`. Common bug.
- **Local-only `isBST` check**: `isBST (Fork x l r) = … && rootVal l < x && x < rootVal r`. This is WRONG — e.g. `Fork 5 (Fork 3 Empty (Fork 6 Empty Empty)) Empty` passes the root check but contains a `6` to the left of `5`. Use bound-threading.
- **Strict `<` vs `<=`**: the course convention is strict (no duplicates in valid BST). Some problems allow duplicates — read the spec.
- **`deleteBST` not handling all four `(l, r)` cases**: `(Empty, Empty)`, `(l, Empty)`, `(Empty, r)`, `(l, r)`. Missing any → crash.
- **Mixing rightmost-of-left with leftmost-of-right**: pick one and be consistent.
- **`Ord a =>` constraint forgotten**: GHC's error is loud but the marker silently rejects.

## Combines-with deep dive

### A11 × A01 — BST is a tree
The shape IS tree recursion (A01) with the extra invariant. Most measure/transform functions are reusable.

### A11 × A20 — proving BST properties
"Prove that `insertBST x t` preserves the BST invariant" — structural induction. The bound-threaded `isBST` makes the proof natural.

### A11 × A22 — `Ord` and `Show` for the BST
A custom BST type can derive `Eq`, `Show`, but if asked to write `Eq` by hand, it's structural-equality (A22).

```haskell
instance Eq a => Eq (BT a) where
  Empty         == Empty           = True
  Fork x l1 r1  == Fork y l2 r2    = x == y && l1 == l2 && r1 == r2
  _             == _               = False
```

### A11 × A05 — BST as a representation of a Set
`fromList :: Ord a => [a] -> BT a` is a translation between list and BST representations.

## See also

**Combines with:** [A01 tree recursion](./A01-tree-recursion.md)
**Question families:** [bst-ops](../question-families/bst-ops-family.md)
**Cross-topic:** [bst × state](../cross-matrix/bst-x-state.md) · [bst × writer](../cross-matrix/bst-x-writer.md)
**Theory:** [BST](../trees/bst.md) · [BST delete trace](../trees/bst-delete-trace.md)
**Pitfalls:** [P-009 isBST Empty = False](../pitfalls/HIGH-severity.md#p-009) · [P-015 BST delete two-children](../pitfalls/HIGH-severity.md#p-015) · [P-020 three different isBST impls](../pitfalls/HIGH-severity.md#p-020)
**QuickCheck:** [bst attacks](../quickcheck/bst-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
