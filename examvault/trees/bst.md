<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [trees](./README.md) · **Binary Search Tree — same type, sorted invariant**

<!-- siblings:start -->
> **Peers:** [binary-tree](./binary-tree.md) · [bst-delete-trace](./bst-delete-trace.md) · **bst** · [expression-tree](./expression-tree.md) · [rose-tree](./rose-tree.md) · [tree-counting](./tree-counting.md) · [tree-fold](./tree-fold.md) · [tree-functor](./tree-functor.md) · [tree-traversals](./tree-traversals.md) · [tree-validation](./tree-validation.md) · [tree-zipper](./tree-zipper.md)
<!-- siblings:end -->






# Binary Search Tree — same type, sorted invariant

A BST is a `BT a` (Ord a) where for every `Fork x l r`: every value in `l` is `< x`, every value in `r` is `> x`. Course convention has *no duplicates*.

## Type (verbatim from Data2.md)

```haskell
data BT a = Empty | Fork a (BT a) (BT a) deriving (Show, Eq, Ord)
-- BST is a discipline on this type, not a different type
```

## insert (the easy one)

> **WARNING — name clash with `Data.List`:** `Data.List` also exports `insert`. If your answer file also imports `Data.List`, write `import Data.List hiding (insert, delete)` — otherwise the recursive call to `insert` is an **Ambiguous occurrence** and will not compile. The safe move in the exam is to use the aliased name `insertBST` (problem 82) below, which never clashes.

```haskell
insert :: Ord a => a -> BT a -> BT a
insert x Empty                    = Fork x Empty Empty
insert x t@(Fork y l r)
    | x < y     = Fork y (insert x l) r
    | x > y     = Fork y l (insert x r)
    | otherwise = t                              -- duplicate: idempotent
-- precondition: input is a BST; postcondition: output is a BST containing x
```

```haskell
-- RECOMMENDED EXAM NAME (problem 82) — same body, dodges the Data.List clash:
insertBST :: Ord a => a -> BT a -> BT a
insertBST x Empty                    = Fork x Empty Empty
insertBST x t@(Fork y l r)
    | x < y     = Fork y (insertBST x l) r
    | x > y     = Fork y l (insertBST x r)
    | otherwise = t                              -- duplicate: idempotent
```

```haskell
inserts :: Ord a => [a] -> BT a -> BT a
inserts = flip (foldr insert)
-- Note `foldr` inserts xs in reverse; `foldl` inserts in order. Either works.
```

```haskell
-- Variant with Maybe to signal "already there"
insert' :: Ord a => a -> BT a -> Maybe (BT a)
insert' x Empty       = Just (Fork x Empty Empty)
insert' x (Fork y l r)
    | x < y     = (\l' -> Fork y l' r) <$> insert' x l
    | x > y     = (\r' -> Fork y l r') <$> insert' x r
    | otherwise = Nothing
```

## member (BST-aware, O(log n) on balanced)

```haskell
member :: Ord a => a -> BT a -> Bool
member _ Empty        = False
member x (Fork y l r) = x == y
                     || (x < y && member x l)
                     || (x > y && member x r)
-- short-circuits via lazy && and ||
```

## min / max

```haskell
minBST :: BT a -> Maybe a
minBST Empty             = Nothing
minBST (Fork x Empty _)  = Just x
minBST (Fork _ l _)      = minBST l
-- leftmost node

maxBST :: BT a -> Maybe a
maxBST Empty             = Nothing
maxBST (Fork x _ Empty)  = Just x
maxBST (Fork _ _ r)      = maxBST r
-- rightmost node
```

## predecessor / successor

```haskell
-- predecessor of x: largest value in the tree that is < x
predecessor :: Ord a => a -> BT a -> Maybe a
predecessor _ Empty = Nothing
predecessor x (Fork y l r)
    | x <= y    = predecessor x l
    | otherwise = case predecessor x r of
                    Nothing -> Just y
                    Just p  -> Just p

-- successor of x: smallest value in the tree that is > x
successor :: Ord a => a -> BT a -> Maybe a
successor _ Empty = Nothing
successor x (Fork y l r)
    | x >= y    = successor x r
    | otherwise = case successor x l of
                    Nothing -> Just y
                    Just s  -> Just s
```

## delete — the four-case classic (predecessor-replacement)

> **WARNING — name clash with `Data.List`:** `Data.List` also exports `delete`. If your answer file also imports `Data.List`, write `import Data.List hiding (insert, delete)` — otherwise the recursive call to `delete` is an **Ambiguous occurrence** and will not compile. The safe move in the exam is to use the aliased name `deleteBST` (problem 84) below, which never clashes.

```haskell
delete :: Ord a => a -> BT a -> BT a
delete _ Empty = Empty
delete x (Fork y l r)
    | x < y                 = Fork y (delete x l) r              -- (a) recurse left
    | x > y                 = Fork y l (delete x r)              -- (b) recurse right
    -- x == y from here:
    | l == Empty            = r                                  -- (c1) no left child → use right
    | r == Empty            = l                                  -- (c2) no right child → use left
    | otherwise             = Fork (largestOf l) (withoutLargest l) r  -- (d) two children

largestOf :: BT a -> a
largestOf Empty            = undefined                           -- never called: precondition
largestOf (Fork x _ Empty) = x
largestOf (Fork _ _ r)     = largestOf r

withoutLargest :: BT a -> BT a
withoutLargest Empty            = undefined
withoutLargest (Fork _ l Empty) = l
withoutLargest (Fork x l r)     = Fork x l (withoutLargest r)
```

```haskell
-- RECOMMENDED EXAM NAME (problem 84) — same body, dodges the Data.List clash
-- (largestOf / withoutLargest above are reused unchanged; they do not clash):
deleteBST :: Ord a => a -> BT a -> BT a
deleteBST _ Empty = Empty
deleteBST x (Fork y l r)
    | x < y                 = Fork y (deleteBST x l) r
    | x > y                 = Fork y l (deleteBST x r)
    | l == Empty            = r
    | r == Empty            = l
    | otherwise             = Fork (largestOf l) (withoutLargest l) r
```
Why predecessor-replacement: the largest of the left subtree is the in-order predecessor of x. Replacing x with it keeps the BST invariant.

## delete — successor-replacement variant

```haskell
deleteS :: Ord a => a -> BT a -> BT a
deleteS _ Empty = Empty
deleteS x (Fork y l r)
    | x < y                 = Fork y (deleteS x l) r
    | x > y                 = Fork y l (deleteS x r)
    | l == Empty            = r
    | r == Empty            = l
    | otherwise             = Fork (smallestOf r) l (withoutSmallest r)
  where
    smallestOf (Fork z Empty _) = z
    smallestOf (Fork _ l' _)    = smallestOf l'
    smallestOf Empty            = undefined

    withoutSmallest (Fork _ Empty r') = r'
    withoutSmallest (Fork z l' r')    = Fork z (withoutSmallest l') r'
    withoutSmallest Empty             = undefined
```

## Fused split-min helper (more efficient)

```haskell
splitMin :: BT a -> Maybe (a, BT a)
splitMin Empty             = Nothing
splitMin (Fork x Empty r)  = Just (x, r)
splitMin (Fork x l r)      = case splitMin l of
    Just (m, l') -> Just (m, Fork x l' r)
    Nothing      -> Just (x, r)                  -- unreachable if l ≠ Empty

deleteFused :: Ord a => a -> BT a -> BT a
deleteFused _ Empty = Empty
deleteFused x (Fork y l r)
    | x < y     = Fork y (deleteFused x l) r
    | x > y     = Fork y l (deleteFused x r)
    | otherwise = case splitMin r of
                    Just (m, r') -> Fork m l r'
                    Nothing      -> l            -- r was Empty
```

## fromList / toSortedList / bstSort

```haskell
fromList :: Ord a => [a] -> BT a
fromList = foldr insert Empty

toSortedList :: BT a -> [a]
toSortedList = flattenInOrder
  where
    flattenInOrder Empty        = []
    flattenInOrder (Fork x l r) = flattenInOrder l ++ [x] ++ flattenInOrder r

bstSort :: Ord a => [a] -> [a]
bstSort = toSortedList . fromList
-- nb: removes duplicates because insert is idempotent on duplicates
```

## validate — the bound-threading approach (linear time)

```haskell
isBST :: Ord a => BT a -> Bool
isBST = check Nothing Nothing
  where
    -- check (lo, hi) t  ==  every node x of t satisfies lo < x < hi
    check :: Ord a => Maybe a -> Maybe a -> BT a -> Bool
    check _   _   Empty = True
    check lo  hi  (Fork x l r) =
         maybe True (< x) lo
      && maybe True (x <) hi
      && check lo      (Just x) l
      && check (Just x) hi      r
-- O(n); each node visited once; bounds tighten as we descend
```

The naive version (Data2.md):
```haskell
isBSTNaive :: Ord a => BT a -> Bool
isBSTNaive Empty        = True
isBSTNaive (Fork x l r) = allSmaller x l
                       && allBigger x r
                       && isBSTNaive l
                       && isBSTNaive r
  where
    allSmaller _ Empty        = True
    allSmaller k (Fork y l r) = y < k && allSmaller k l && allSmaller k r
    allBigger  _ Empty        = True
    allBigger  k (Fork y l r) = y > k && allBigger k l && allBigger k r
-- O(n²) — quadratic because each node walked once per ancestor
```

The flatten-and-check shortcut:
```haskell
isBSTByFlatten :: Ord a => BT a -> Bool
isBSTByFlatten = isStrictlyIncreasing . toSortedList
  where
    isStrictlyIncreasing []       = True
    isStrictlyIncreasing [_]      = True
    isStrictlyIncreasing (x:y:zs) = x < y && isStrictlyIncreasing (y:zs)
-- O(n) time, but allocates the whole list; bound-threading is asymptotically equal but space-better
```

## balance (rebuild balanced from in-order)

```haskell
balance :: BT a -> BT a
balance = balancedFromSorted . toSortedList
  where
    balancedFromSorted []  = Empty
    balancedFromSorted xs  = let n        = length xs
                                 (ys, x:zs) = splitAt (n `div` 2) xs
                             in Fork x (balancedFromSorted ys) (balancedFromSorted zs)
-- treeInOrder . balance == treeInOrder; the BST property is preserved
```

## QuickCheck properties (paste-ready)

```haskell
import Test.QuickCheck

-- Generation: build a BST from a random list
newtype BSTOf a = BSTOf { unBSTOf :: BT a } deriving Show
instance (Ord a, Arbitrary a) => Arbitrary (BSTOf a) where
  arbitrary = BSTOf . fromList <$> arbitrary

-- Properties
prop_insertPreservesBST :: Int -> BSTOf Int -> Bool
prop_insertPreservesBST x (BSTOf t) = isBST (insert x t)

prop_deletePreservesBST :: Int -> BSTOf Int -> Bool
prop_deletePreservesBST x (BSTOf t) = isBST (delete x t)

prop_insertMember :: Int -> BSTOf Int -> Bool
prop_insertMember x (BSTOf t) = member x (insert x t)

prop_deleteRemoves :: Int -> BSTOf Int -> Bool
prop_deleteRemoves x (BSTOf t) = not (member x (delete x t))

prop_fromListValid :: [Int] -> Bool
prop_fromListValid xs = isBST (fromList xs)              -- THE BIG ONE

prop_bstSortSorted :: [Int] -> Bool
prop_bstSortSorted xs = let ys = bstSort xs
                       in and (zipWith (<) ys (drop 1 ys))

prop_toListSorted :: BSTOf Int -> Bool
prop_toListSorted (BSTOf t) = let xs = toSortedList t
                              in and (zipWith (<=) xs (drop 1 xs))

prop_balancePreservesContents :: BSTOf Int -> Bool
prop_balancePreservesContents (BSTOf t) =
    toSortedList (balance t) == toSortedList t

prop_balanceStillBST :: BSTOf Int -> Bool
prop_balanceStillBST (BSTOf t) = isBST (balance t)
```

## Pitfalls

- `isBST Empty` is **True** (vacuously). Easy to get wrong.
- `insert` returns the *same* tree when x is already present (idempotency). Don't return a new identical tree — `Fork y l r` directly, not `Fork y (insert x l) r` in the equality case.
- `delete x t` where x is not in t should return t unchanged (this fall-through is automatic via the `< / >` recursion + `Empty` base).
- `largestOf Empty = undefined`: this is safe **only because** the four-case delete never calls it on an empty subtree (precondition: caller guarantees `l ≠ Empty`). If you refactor, keep that precondition explicit.
- `withoutLargest` traverses the right spine of l, dropping the rightmost node. Don't forget to reattach `x` and `l`'s left subtree.
- Two delete strategies (predecessor / successor) are both correct. Mixing them or rotating asymmetrically without justification will look weird to a marker.
- **Naive isBST is O(n²)** — it's the easy-to-write version but bound-threading is the one to know.
- Duplicates: the course definition disallows them. If a question says "multiset BST" the invariants and `delete` semantics shift.

## Cross-references

- Base type & generic ops: [binary-tree.md](binary-tree.md)
- Validation in general (isBST is just one): [tree-validation.md](tree-validation.md)
- BST as archetype: [../archetypes/11-bst.md](../archetypes/A11-bst-ops.md)
- BSTs in lecture: `fp-learning-2025/files/LectureNotes/Sections/Data2.md` §Binary search trees
- Problems 81–85 (isBST, insertBST, memberBST, deleteBST, fromList)
- See also `bstsort` vs `qsort` vs `msort` benchmark in Data2.md

## See also

**Archetypes:** [A11 BST ops](../archetypes/A11-bst-ops.md) · [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Cross-topic:** [bst × state](../cross-matrix/bst-x-state.md) · [bst × writer](../cross-matrix/bst-x-writer.md)
**Question families:** [bst-ops](../question-families/bst-ops-family.md) · [tree-validation](../question-families/tree-validation-family.md)
**QuickCheck:** [bst attacks](../quickcheck/bst-attacks.md)
**Related (trees):** [binary tree](./binary-tree.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
