<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [trees](./README.md) · **Tree traversals — preorder, inorder, postorder, BFS, paths**

<!-- siblings:start -->
> **Peers:** [binary-tree](./binary-tree.md) · [bst-delete-trace](./bst-delete-trace.md) · [bst](./bst.md) · [expression-tree](./expression-tree.md) · [rose-tree](./rose-tree.md) · [tree-counting](./tree-counting.md) · [tree-fold](./tree-fold.md) · [tree-functor](./tree-functor.md) · **tree-traversals** · [tree-validation](./tree-validation.md) · [tree-zipper](./tree-zipper.md)
<!-- siblings:end -->






# Tree traversals — preorder, inorder, postorder, BFS, paths

All five common traversals on the standard `BT a = Empty | Fork a (BT a) (BT a)`.

## The three depth-first traversals

```haskell
preorder, inorder, postorder :: BT a -> [a]

preorder Empty        = []
preorder (Fork x l r) = x : preorder l ++ preorder r
-- root, left, right; e.g. [8,4,2,16,20] on btexample

inorder Empty        = []
inorder (Fork x l r) = inorder l ++ [x] ++ inorder r
-- left, root, right; e.g. [2,4,8,16,20]; sorted on a BST

postorder Empty        = []
postorder (Fork x l r) = postorder l ++ postorder r ++ [x]
-- left, right, root; e.g. [2,4,20,16,8]
```

## Level-order (BFS)

Two implementations: the *layered* one (Data1.md style) and the *queue-based* one.

### Layered (lecture-correct)

```haskell
levels :: BT a -> [[a]]
levels Empty        = []
levels (Fork x l r) = [x] : zipappend (levels l) (levels r)
  where
    zipappend []       yss      = yss
    zipappend xss      []       = xss
    zipappend (xs:xss) (ys:yss) = (xs ++ ys) : zipappend xss yss

bfs :: BT a -> [a]
bfs = concat . levels
-- [8,4,16,2,20] on btexample
```
`zipappend` is `zipWith (++)` extended to handle uneven list lengths (so subtrees of different heights are merged correctly).

### Queue-based (iterative)

```haskell
bfsQueue :: BT a -> [a]
bfsQueue t = go [t]
  where
    go []                  = []
    go (Empty       : ts)  = go ts
    go (Fork x l r  : ts)  = x : go (ts ++ [l, r])
-- O(n²) due to ++ on the queue; use a proper queue (Data.Sequence) for O(n)
```

### Reverse-BFS (deepest-first)

```haskell
reverseBfs :: BT a -> [a]
reverseBfs = concat . reverse . levels
```

## Paths

```haskell
paths :: BT a -> [[a]]
paths Empty        = [[]]
paths (Fork x l r) = [x:p | p <- paths l] ++ [x:p | p <- paths r]
-- every root-to-Empty path; |paths t| = leaves t + 1 (counting Empty-leaves)
```

```haskell
leafPaths :: BT a -> [[a]]
leafPaths Empty                = []
leafPaths (Fork x Empty Empty) = [[x]]
leafPaths (Fork x l r)         = [x:p | p <- leafPaths l ++ leafPaths r]
-- only root-to-leaf (where a leaf is a Fork with both children Empty)
```

```haskell
pathsWithAddresses :: BT a -> [([Direction], a)]
pathsWithAddresses = go []
  where
    go _   Empty        = []
    go acc (Fork x l r) = (reverse acc, x) : go (L:acc) l ++ go (R:acc) r
-- every node tagged with its directional address from the root
```

```haskell
longestPath :: BT a -> [a]
longestPath = head . foldr (\p acc -> if length p > length (head acc) then [p] else acc) [[]]
            . paths
-- one of the longest paths; ties broken by leftmost
```

## Inverting traversals (generating trees from a list)

```haskell
-- Build a balanced tree whose inorder traversal is xs
balancedTree :: [a] -> BT a
balancedTree []  = Empty
balancedTree xs  = let (ys, x:zs) = splitAt (length xs `div` 2) xs
                   in Fork x (balancedTree ys) (balancedTree zs)
-- property: inorder (balancedTree xs) == xs

-- All BTs with the given inorder traversal
inOrderTree :: [a] -> [BT a]
inOrderTree [] = [Empty]
inOrderTree xs = [Fork x l r | i <- [0 .. length xs - 1]
                             , let (ys, x:zs) = splitAt i xs
                             , l <- inOrderTree ys
                             , r <- inOrderTree zs]
-- generates the Catalan number C_n of trees
```

For pre-order:
```haskell
preOrderTree :: [a] -> [BT a]
preOrderTree []     = [Empty]
preOrderTree (x:xs) = [Fork x l r | i <- [0..length xs]
                                  , let (ys, zs) = splitAt i xs
                                  , l <- preOrderTree ys
                                  , r <- preOrderTree zs]
```

For BFS the inversion is much harder — see Data1.md hint.

## Building from sorted in-order (BST construction)

```haskell
fromSortedList :: [a] -> BT a
fromSortedList = balancedTree
-- if the input list is sorted, the result is a balanced BST
```

## Relation: inorder = sort for a BST

```haskell
inorderIsSorted :: Ord a => BT a -> Bool
inorderIsSorted t = let xs = inorder t in xs == sort xs
-- this IS one definition of isBST (see bst.md, the flatten-and-check variant)
```

## Reconstruction from two traversals (classic interview)

Given preorder + inorder, you can reconstruct the BT uniquely (assuming distinct values).

```haskell
import Data.List (elemIndex)

buildFromPreIn :: Eq a => [a] -> [a] -> Maybe (BT a)
buildFromPreIn []     []  = Just Empty
buildFromPreIn (x:ps) ins = do
    i <- elemIndex x ins                              -- find root in inorder
    let (lin, _:rin) = splitAt i ins                  -- split inorder around root
        (lpre, rpre) = splitAt i ps                   -- preorder: first i = left subtree
    Fork x <$> buildFromPreIn lpre lin
           <*> buildFromPreIn rpre rin
buildFromPreIn _ _ = Nothing                          -- mismatched inputs
```

## Mutations

| Question wants | Change |
|----------------|--------|
| zigzag traversal | alternate L/R-first per level: track depth, swap at odd depths |
| boundary traversal | leftmost path + bottom leaves + reversed rightmost path |
| pre/in/post with index | `zip [0..] . preorder` |
| traversal of Rose | `preorder (Branch x ts) = x : concatMap preorder ts` |
| level-order on Rose | extend `levels` to handle `[Rose a]` children |
| spiral traversal | `levels` then reverse every other |
| boundaries-only | left spine + right spine + leaves |
| n-th element of in-order | thread a counter; stop when reached n |

## QuickCheck

```haskell
prop_traversalLength t = length (preorder t)  == size t
                       && length (inorder t)   == size t
                       && length (postorder t) == size t
                       && length (bfs t)       == size t

prop_inorderIdent xs = inorder (balancedTree xs) == xs

prop_traversalPerms t = sort (preorder t) == sort (inorder t)
                     && sort (inorder t)  == sort (postorder t)
                     && sort (bfs t)      == sort (inorder t)
-- all four are permutations of the same multiset of values

prop_inorderBSTSorted (BSTOf t) = inorder t == sort (inorder t)
-- where BSTOf is from bst.md

prop_pathsLeafCount t = length (leafPaths t) == leaves t
```

## Pitfalls

- `inorder ++ [x] ++` is O(n²) due to left-biased `(++)`. Use difference lists or accumulator for production:
  ```haskell
  inorderDL :: BT a -> [a] -> [a]
  inorderDL Empty        = id
  inorderDL (Fork x l r) = inorderDL l . (x:) . inorderDL r
  -- inorder t = inorderDL t []
  ```
- BFS via `++ [l,r]` on a list queue is O(n²). For real BFS, use `Data.Sequence` (`|> l |> r` is O(1)) — but the course doesn't require this.
- `paths Empty = [[]]` includes the empty path. If you want *non-empty* paths only, base case is `[]`.
- `levels Empty = []` (no level) vs `[[]]` (one empty level) — the lecture uses `[]`. Check the question convention.
- Reconstructing from preorder+postorder alone is **not unique** in general (consider `[a]` and `[a]`). You need at least one traversal that records the root position, like inorder.
- `zipappend` (≠ `zipWith (++)`) is the version that handles uneven lists. If you replace it with `zipWith (++)` you lose the leftover levels.

## Cross-references

- Generic ops: [binary-tree.md](binary-tree.md)
- BST in-order = sorted: [bst.md](bst.md)
- Foldable's `toList`: [tree-functor.md](tree-functor.md), [../typeclasses/foldable.md](../typeclasses/foldable.md)
- Lecture: `fp-learning-2025/files/LectureNotes/Sections/Data1.md` §Traversals in binary trees
- Problem 75 (flattenInOrder), 76 (pre/post), 113 (`balanceTreeFromList`)

## See also

**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Cross-topic:** [tree × generic-monad](../cross-matrix/tree-x-generic-monad.md)
**Question families:** [tree-extract](../question-families/tree-extract-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md)
**Related (trees):** [binary tree](./binary-tree.md) · [tree fold](./tree-fold.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
