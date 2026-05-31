<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: Binary Search Trees**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · **bst** · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: Binary Search Trees

> **⚠ Constructor-name banner.** The examples below use a generic `Tree`/`Node` for readability, but **the course type is**
> ```haskell
> data BT a = Empty | Fork a (BT a) (BT a)
> ```
> — a BST is just a `BT` whose in-order traversal is strictly sorted; there is **no separate `BST` type**. So `Node` here ≡ `Fork`, and the empty case ≡ `Empty`. **Always substitute the exact constructor names from the question's own `Types` module** (it may use `BT`/`Fork`, `Tree`/`Node`, `Bin`/`Lf`/`Nd`, …) and never redefine the type. The most-copied snippets (`isBST`, `insert`, `member`, `delete`) appear in `BT`/`Empty`/`Fork` below so they paste straight onto the course type.

**Search keywords:** BST, BT, isBST, insertBST, memberBST, deleteBST, insert, delete, member, Ord, ordering invariant, vacuous truth, Empty = True, two children deletion, in-order successor

## What the marker generates

BSTs are usually tested by:
1. Inserting a random `[Int]` into `Empty` and checking the BST invariant holds.
2. Comparing `member` against `elem` on the corresponding `flatten`.
3. Comparing `delete` against a reference implementation.

The marker will generate **sequential insertions** (think `[1,2,3,4,5]` → skewed right) AND **random shuffles** (`[3,1,4,1,5,9,2,6]` → balanced-ish). Both must work.

For `isBST` checks, the marker often constructs trees DIRECTLY (not via `insert`) so an "I always call insert" assumption fails — your `isBST` must verify the invariant from scratch.

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | `isBST Empty` | `Empty` | If you write `isBST Empty = False`, you get the universal vacuous-truth bug | `isBST Empty = True` — a tree with no nodes vacuously satisfies the ordering invariant |
| 2 | `isBST (Fork x Empty Empty)` | single-node | Off-by-one in min/max comparison | Single node IS a valid BST. `isBST (Fork _ Empty Empty) = True` (falls through to general case) |
| 3 | `isBST` **only checks root vs children, not whole subtree** | `Fork 5 (Fork 3 Empty (Fork 7 Empty Empty)) Empty` — root 5, left has 3 (good) but contains 7 (BAD!) | Returns `True` incorrectly because root invariant alone passes | Check `all (< x) (flatten l) && all (> x) (flatten r) && isBST l && isBST r` — or use min/max-bounded recursion |
| 4 | `insert x Empty` | `Empty` | Pattern non-exhaustive | `insert x Empty = Fork x Empty Empty` |
| 5 | `insert x` when `x` already present | `insert 5 (Fork 5 Empty Empty)` | Depends on spec: should it ignore? Duplicate? Crash? | **Default course behaviour: IGNORE duplicates.** `insert x t \| x `elem` flatten t = t \| otherwise = ...`. Verify with the spec. |
| 6 | `member x Empty` | `Empty` | Pattern non-exhaustive | `member x Empty = False` |
| 7 | `member x t` for absent `x` | `member 100 small-tree` | Off-by-one, falls into wrong subtree | `member x (Fork y l r) \| x == y = True \| x < y = member x l \| otherwise = member x r` |
| 8 | `member x t` for present `x` at root | `member 5 (Fork 5 _ _)` | `==` not checked first | First case in `member`: `x == y` returns `True` |
| 9 | `delete x Empty` | `Empty` | Non-exhaustive or wrong return | `delete x Empty = Empty` (no-op on empty) |
| 10 | `delete x` for missing `x` | `delete 100 t` where `100 \notin t` | Spec: should be a no-op (returns `t` unchanged). If you "find" a node to delete that isn't there, you might delete the wrong one. | `delete x (Fork y l r) \| x < y = Fork y (delete x l) r \| x > y = ... \| otherwise = ...` |
| 11 | `delete` a leaf | `delete 5 (Fork 5 Empty Empty)` | Off-by-one in restructuring | Leaf deletion: return `Empty` |
| 12 | `delete` a node with ONE child | `delete 5 (Fork 5 (Fork 3 Empty Empty) Empty)` | Promotes the wrong child or duplicates | Promote the non-empty child: return `l` (or `r`, whichever is non-Empty) |
| 13 | `delete` a node with TWO children | `delete 5 (Fork 5 (Fork 3 _ _) (Fork 7 _ _))` | **The classic bug.** Most students forget this. Either replace with min-of-right-subtree OR max-of-left-subtree, then delete that. | `delete x (Fork x l r) = let m = minimum (flatten r) in Fork m l (delete m r)` |
| 14 | `delete root` of a deep tree | causes restructuring through many levels | The "promote min of right" must itself work recursively | Test on `[1,2,3,4,5,6,7]` then `delete 4` |
| 15 | `insert` then `member` round-trip | `member x (insert x t)` should be `True` | Off-by-one in `==` | Round-trip property |
| 16 | `insert x . insert x` should be same as `insert x` (if duplicates ignored) | idempotence | Bug: inserts duplicate node | Idempotence property |
| 17 | Skewed BST from sorted insert | `insert 1, insert 2, ..., insert 10` | `member`/`delete` recursion goes 10 levels deep | Fine for short lists; QC won't go beyond ~100 |

## The four most-copied BST functions (in course `BT`/`Empty`/`Fork`)

Paste straight onto `data BT a = Empty | Fork a (BT a) (BT a)`. Note `isBST Empty = True` (vacuous), `insert` ignores duplicates (set semantics), and two-children `delete` promotes the min of the right subtree.

```haskell
isBST :: Ord a => BT a -> Bool
isBST Empty = True
isBST (Fork x l r) =
     all (< x) (flatten l)
  && all (> x) (flatten r)
  && isBST l
  && isBST r

insert :: Ord a => a -> BT a -> BT a
insert x Empty = Fork x Empty Empty
insert x (Fork y l r)
  | x < y     = Fork y (insert x l) r
  | x > y     = Fork y l (insert x r)
  | otherwise = Fork y l r              -- already present → no-op (set semantics)

member :: Ord a => a -> BT a -> Bool
member _ Empty = False
member x (Fork y l r)
  | x == y    = True
  | x < y     = member x l
  | otherwise = member x r

delete :: Ord a => a -> BT a -> BT a
delete _ Empty = Empty
delete x (Fork y l r)
  | x < y     = Fork y (delete x l) r
  | x > y     = Fork y l (delete x r)
  | otherwise = case (l, r) of
      (Empty, _) -> r
      (_, Empty) -> l
      _          -> let m = findMin r in Fork m l (delete m r)
  where
    findMin (Fork v Empty _)   = v
    findMin (Fork _ leftSub _) = findMin leftSub
    findMin Empty              = error "findMin Empty"   -- unreachable: r non-empty here
```

(`flatten` is the in-order traversal: `flatten Empty = []; flatten (Fork x l r) = flatten l ++ [x] ++ flatten r`.)

## Property templates

```haskell
import Test.QuickCheck
import Data.List (sort, nub)

-- Build a BST from a list
fromList :: Ord a => [a] -> BT a
fromList = foldr insert Empty

-- isBST should accept empty
prop_isBST_empty :: Bool
prop_isBST_empty = isBST (Empty :: BT Int) == True

-- isBST should accept singleton
prop_isBST_singleton :: Int -> Bool
prop_isBST_singleton x = isBST (Fork x Empty Empty)

-- isBST should accept any tree built by insert
prop_isBST_afterInserts :: [Int] -> Bool
prop_isBST_afterInserts xs = isBST (fromList xs)

-- isBST should reject a deliberately-bad tree
prop_isBST_rejectsBad :: Bool
prop_isBST_rejectsBad = not (isBST badTree)
  where badTree = Fork 5 (Fork 3 Empty (Fork 7 Empty Empty)) Empty
                  -- left subtree contains 7 > 5 → not a BST

-- member after insert is True
prop_memberAfterInsert :: Int -> [Int] -> Bool
prop_memberAfterInsert x xs = member x (insert x (fromList xs))

-- member matches elem on flatten
prop_memberMatchesElem :: Int -> [Int] -> Bool
prop_memberMatchesElem x xs = member x (fromList xs) == (x `elem` xs)

-- flatten of BST is sorted (in-order traversal)
prop_flattenSorted :: [Int] -> Bool
prop_flattenSorted xs = sorted (flatten (fromList xs))
  where sorted ys = ys == sort ys

-- insert is idempotent (if duplicates ignored)
prop_insertIdempotent :: Int -> [Int] -> Bool
prop_insertIdempotent x xs =
  flatten (insert x (insert x t)) == flatten (insert x t)
  where t = fromList xs

-- delete missing key is no-op
prop_deleteMissing :: Int -> [Int] -> Property
prop_deleteMissing x xs = not (x `elem` xs) ==>
  flatten (delete x (fromList xs)) == sort (nub xs)

-- delete then member is False
prop_deleteRemoves :: Int -> [Int] -> Bool
prop_deleteRemoves x xs = not (member x (delete x (fromList (x:xs))))

-- delete preserves BST invariant
prop_deletePreservesBST :: Int -> [Int] -> Bool
prop_deletePreservesBST x xs = isBST (delete x (fromList xs))
```

## Self-test before submission checklist

- [ ] `isBST Empty == True`  (NOT False!)
- [ ] `isBST` checks invariant on whole subtrees, not just root vs immediate children
- [ ] `insert x Empty == Fork x Empty Empty`
- [ ] `insert x` ignores duplicates (or whatever the spec says)
- [ ] `member x Empty == False`
- [ ] `member` recurses left/right correctly based on `compare`
- [ ] `delete x Empty == Empty` (no-op)
- [ ] `delete x` is a no-op when `x` is not in the tree
- [ ] `delete` a leaf works
- [ ] `delete` a one-child node promotes the child
- [ ] `delete` a two-children node uses min-of-right (or max-of-left) replacement
- [ ] After any sequence of `insert`/`delete`, the result still satisfies `isBST`
- [ ] `flatten (fromList xs) == sort (nub xs)` (if duplicates ignored)

## Pitfalls that specifically lose QC marks

### Pitfall: `isBST Empty = False`
This is the single most common BST bug in student code (visible in the user's own `githubinitial.hs`).

```haskell
-- WRONG:
isBST Empty = False
-- QC builds an empty tree, asks isBST, expects True (vacuous truth)
-- Fix:
isBST Empty = True
```

### Pitfall: shallow `isBST` check
```haskell
-- WRONG: only checks root
isBST Empty = True
isBST (Fork x Empty Empty) = True
isBST (Fork x l r) = maxL < x && minR > x
  where maxL = maximum (flatten l); minR = minimum (flatten r)
-- This forgets to recurse into l and r!
-- Counterexample: Fork 5 (Fork 4 Empty (Fork 10 Empty Empty)) Empty
--   root: max of left subtree is 10 — but flatten = [4, 10] so max = 10
--   Hmm actually the bug here is different. The fix is recursion:

-- RIGHT:
isBST Empty = True
isBST (Fork x l r) =
     all (< x) (flatten l)
  && all (> x) (flatten r)
  && isBST l
  && isBST r
```

### Pitfall: two-children delete
```haskell
-- WRONG: discards right subtree's elements!
delete x (Fork y l r)
  | x < y = Fork y (delete x l) r
  | x > y = Fork y l (delete x r)
  | otherwise = case (l, r) of
      (Empty, _) -> r
      (_, Empty) -> l
      _          -> l   -- BUG: drops r's contents entirely

-- RIGHT: replace with min of right, delete that from right
delete x Empty = Empty
delete x (Fork y l r)
  | x < y = Fork y (delete x l) r
  | x > y = Fork y l (delete x r)
  | otherwise = case (l, r) of
      (Empty, _) -> r
      (_, Empty) -> l
      _          -> let m = findMin r in Fork m l (delete m r)
  where
    findMin (Fork v Empty _) = v
    findMin (Fork _ leftSub _) = findMin leftSub
```

### Pitfall: `delete` of missing key produces wrong tree
```haskell
-- WRONG: silently restructures even if x missing
delete x (Fork y l r) = ...  -- always restructures
-- Should be a no-op if x not in tree.
-- The recursive structure naturally handles this:
delete x Empty = Empty               -- key def: missing → return Empty
delete x (Fork y l r)
  | x < y = Fork y (delete x l) r    -- recurse left, if x not there, l is unchanged
  | x > y = Fork y l (delete x r)    -- recurse right, ditto
  | otherwise = ...                  -- this case only fires when x == y, meaning x WAS found
```

### Pitfall: insert allows duplicates when spec says "set semantics"
```haskell
-- WRONG: always inserts even if present
insert x (Fork y l r)
  | x < y = Fork y (insert x l) r
  | x > y = Fork y l (insert x r)
  | otherwise = Fork y (insert x l) r   -- duplicates!

-- RIGHT (set semantics):
insert x Empty = Fork x Empty Empty
insert x (Fork y l r)
  | x < y = Fork y (insert x l) r
  | x > y = Fork y l (insert x r)
  | otherwise = Fork y l r              -- already present, no-op
```

### Pitfall: `member` uses `==` only on equality, not on the recursive case
```haskell
-- WRONG (linear search!):
member x (Fork y l r) = x == y || member x l || member x r
-- Works but is O(n) — defeats the point of BST.
-- The marker may not care about complexity, but a randomly-structured
-- worst case is slow.

-- RIGHT (O(log n) average):
member x Empty = False
member x (Fork y l r)
  | x == y = True
  | x < y  = member x l
  | otherwise = member x r
```

### Pitfall: forgetting `Ord` constraint
```haskell
-- WRONG signature:
insert :: a -> BT a -> BT a            -- can't compare!
-- RIGHT:
insert :: Ord a => a -> BT a -> BT a
```

**If the template provides the signature, copy it verbatim.** If you ADD the constraint, you cannot insert into a non-Ord type the marker tries (rare). If you REMOVE a template constraint, your code may not even compile.

### Pitfall: assuming the tree type is defined a particular way
The **course / vault canonical** type is `data BT a = Empty | Fork a (BT a) (BT a)` (used in every snippet above). But different practice files and `Types.hs` variants use:
- `data BT a = Empty | Fork a (BT a) (BT a)` ← course default
- `data Tree a = Empty | Node a (Tree a) (Tree a)`
- `data BinTree a = EmptyTree | Node a (BinTree a) (BinTree a)`
- `data Bin a = Lf | Nd a (Bin a) (Bin a)`

**Use whatever constructor names the question's `Types.hs` uses.** Don't redefine.

## See also

**Archetypes:** [A11 BST ops](../archetypes/A11-bst-ops.md)
**Cross-topic:** [bst × state](../cross-matrix/bst-x-state.md)
**Question families:** [bst-ops](../question-families/bst-ops-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
