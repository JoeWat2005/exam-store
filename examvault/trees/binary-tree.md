<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [trees](./README.md) · **Binary Tree — `data BT a = Empty | Fork a (BT a) (BT a)`**

<!-- siblings:start -->
> **Peers:** **binary-tree** · [bst-delete-trace](./bst-delete-trace.md) · [bst](./bst.md) · [expression-tree](./expression-tree.md) · [rose-tree](./rose-tree.md) · [tree-counting](./tree-counting.md) · [tree-fold](./tree-fold.md) · [tree-functor](./tree-functor.md) · [tree-traversals](./tree-traversals.md) · [tree-validation](./tree-validation.md) · [tree-zipper](./tree-zipper.md)
<!-- siblings:end -->






# Binary Tree — `data BT a = Empty | Fork a (BT a) (BT a)`

The course's canonical binary tree (Data1.md). Every problem 71–80 uses this exact type.

## Type declaration (verbatim, copy this)

```haskell
data BT a = Empty
          | Fork a (BT a) (BT a)
          deriving (Show, Read, Eq, Ord)

-- Constructors:
-- Empty :: BT a
-- Fork  :: a -> BT a -> BT a -> BT a
```

## Canonical recursion shape

```haskell
f :: BT a -> r
f Empty        = base
f (Fork x l r) = combine x (f l) (f r)
```

Every operation on this page is one of:
- a pure left-to-right recursion (size, height, sum)
- a structural rebuild (mirror, mapBT)
- a flattening (in/pre/post-order)

## Core size/structure operations

```haskell
size :: BT a -> Int
size Empty        = 0
size (Fork _ l r) = 1 + size l + size r
-- counts Fork nodes; size Empty = 0
```

```haskell
height :: BT a -> Int
height Empty        = 0
height (Fork _ l r) = 1 + max (height l) (height r)
-- length of longest root-to-Empty path in nodes
-- COURSE CONVENTION: height Empty = 0, height (singleton) = 1
```

```haskell
depth :: BT a -> Int
depth = height
-- "depth" and "height" are used interchangeably in the course
```

```haskell
leaves :: BT a -> Int
leaves Empty                = 0
leaves (Fork _ Empty Empty) = 1
leaves (Fork _ l r)         = leaves l + leaves r
-- counts Fork nodes whose BOTH children are Empty
-- NOT the Data1 convention `leaves Empty = 1` (that counts dangling Empties)
```

```haskell
internal :: BT a -> Int
internal Empty                = 0
internal (Fork _ Empty Empty) = 0
internal (Fork _ l r)         = 1 + internal l + internal r
-- nodes with at least one non-Empty child
-- invariant: size = leaves + internal
```

```haskell
sumBT :: Num a => BT a -> a
sumBT Empty        = 0
sumBT (Fork x l r) = x + sumBT l + sumBT r
```

```haskell
maxBT :: Ord a => BT a -> Maybe a
maxBT Empty        = Nothing
maxBT (Fork x l r) = Just $ case (maxBT l, maxBT r) of
    (Nothing, Nothing) -> x
    (Just lm, Nothing) -> max x lm
    (Nothing, Just rm) -> max x rm
    (Just lm, Just rm) -> max x (max lm rm)
-- Maybe because Empty has no maximum
```

## Structural rebuilds

```haskell
mirror :: BT a -> BT a
mirror Empty        = Empty
mirror (Fork x l r) = Fork x (mirror r) (mirror l)
-- swap subtrees recursively; mirror . mirror = id
```

```haskell
mapBT :: (a -> b) -> BT a -> BT b
mapBT _ Empty        = Empty
mapBT f (Fork x l r) = Fork (f x) (mapBT f l) (mapBT f r)
-- this IS the Functor instance — see tree-functor.md
```

```haskell
-- Same thing via the Functor class (tree-functor.md):
instance Functor BT where
  fmap _ Empty        = Empty
  fmap f (Fork x l r) = Fork (f x) (fmap f l) (fmap f r)
```

## Flattening (three traversals)

```haskell
flattenInOrder, flattenPreOrder, flattenPostOrder :: BT a -> [a]

flattenInOrder Empty        = []
flattenInOrder (Fork x l r) = flattenInOrder l ++ [x] ++ flattenInOrder r

flattenPreOrder Empty        = []
flattenPreOrder (Fork x l r) = [x] ++ flattenPreOrder l ++ flattenPreOrder r

flattenPostOrder Empty        = []
flattenPostOrder (Fork x l r) = flattenPostOrder l ++ flattenPostOrder r ++ [x]
```
Note: in-order on a BST gives the sorted list — basis of `bstSort`. See [tree-traversals.md](tree-traversals.md) for level-order (BFS).

## Paths and addresses

```haskell
data Direction = L | R deriving (Show, Eq)
type Address   = [Direction]

paths :: BT a -> [[a]]
paths Empty                = []
paths (Fork x Empty Empty) = [[x]]
paths (Fork x l r)         = [ x:p | p <- paths l ++ paths r ]
-- all root-to-LEAF paths as value lists
-- e.g. paths (Fork 1 (singleton 2) (singleton 3)) == [[1,2],[1,3]]
--      paths (singleton 9)                        == [[9]]
-- NB the naive `paths Empty = [[]]` version DOUBLES every path: a leaf has
-- two Empty children, so `[x:p | p <- paths l] ++ [x:p | p <- paths r]`
-- emits its path once per Empty child. The explicit leaf case above fixes it.
```

```haskell
addresses :: BT a -> [Address]
addresses Empty        = [[]]
addresses (Fork _ l r) =  [[]]
                       ++ [L:a | a <- addresses l]
                       ++ [R:a | a <- addresses r]
-- all valid subtree-addresses including the empty address [] = "the whole tree"
```

```haskell
subtree :: Address -> BT a -> Maybe (BT a)
subtree []     t            = Just t
subtree (_:_)  Empty        = Nothing
subtree (L:ds) (Fork _ l _) = subtree ds l
subtree (R:ds) (Fork _ _ r) = subtree ds r
-- follow directions or return Nothing if invalid address
```

```haskell
isValid :: Address -> BT a -> Bool
isValid []     _            = True
isValid (_:_)  Empty        = False
isValid (L:ds) (Fork _ l _) = isValid ds l
isValid (R:ds) (Fork _ _ r) = isValid ds r
-- spec: isValid ds t  ==  ds `elem` addresses t
```

## Membership / counting / search

```haskell
member :: Eq a => a -> BT a -> Bool
member _ Empty        = False
member y (Fork x l r) = y == x || member y l || member y r
-- linear-time generic membership (NOT BST-aware — for BST see bst.md)
```

```haskell
countBT :: Eq a => a -> BT a -> Int
countBT _ Empty                          = 0
countBT y (Fork x l r) | y == x    = 1 + countBT y l + countBT y r
                       | otherwise =     countBT y l + countBT y r
```
For the count *family* (count leaves, count internal, count by predicate, count by depth) see [tree-counting.md](tree-counting.md).

## Building trees

```haskell
treeFromList :: [a] -> BT a
treeFromList = foldr insertLeft Empty
  where insertLeft x t = Fork x t Empty
-- crude: produces a right-leaning skewed tree

balancedTreeFromList :: [a] -> BT a
balancedTreeFromList [] = Empty
balancedTreeFromList xs =
    let (ys, x:zs) = splitAt (length xs `div` 2) xs
    in Fork x (balancedTreeFromList ys) (balancedTreeFromList zs)
-- O(n log n); produces balanced; if xs is sorted you get a BST
```

```haskell
singleton :: a -> BT a
singleton x = Fork x Empty Empty
```

## Generic fold (the most useful one operation)

```haskell
foldBT :: (a -> b -> b -> b)   -- combine at Fork
       -> b                    -- value at Empty
       -> BT a
       -> b
foldBT _ e Empty        = e
foldBT f e (Fork x l r) = f x (foldBT f e l) (foldBT f e r)

-- All the above as one-liners:
size'    = foldBT (\_ l r -> 1 + l + r) 0
height'  = foldBT (\_ l r -> 1 + max l r) 0
sumBT'   = foldBT (\x l r -> x + l + r) 0
mirror'  = foldBT (\x l r -> Fork x r l) Empty
mapBT' f = foldBT (\x l r -> Fork (f x) l r) Empty
flatten' = foldBT (\x l r -> l ++ [x] ++ r) []
toList'  = foldBT (\x l r -> x : l ++ r) []           -- pre-order
```
See [tree-fold.md](tree-fold.md) for the fold archetype in depth.

## Mutations (how examiners deform these)

| Original | Mutation | Change |
|----------|----------|--------|
| `size` | `sizeBy p` | only count Forks where `p x` |
| `height` | `weight` | sum the values along the longest path |
| `mirror` | `rotateLeft` | restructure subtrees instead of swapping |
| `flatten` | `flattenWithDepth` | tag each value with its depth |
| `mapBT` | `mapWithPath`, `mapBT f g h` | different `f` at each depth, or per-constructor |
| `member` | `findPath x t` | return `Maybe Address` instead of `Bool` |

## QuickCheck attack surface

```haskell
-- generators
prop_sizeNonNeg t       = size t >= 0
prop_mirrorIdempotent t = mirror (mirror t) == t
prop_sizeMirror t       = size (mirror t) == size t
prop_flattenSize t      = length (flattenInOrder t) == size t
prop_heightLeBound t    = height t <= size t

-- pathological inputs
emptyT       = Empty
single       = singleton 'a'
leftSpine n  = foldr (\x t -> Fork x t Empty) Empty [1..n]
rightSpine n = foldr (\x t -> Fork x Empty t) Empty [1..n]
perfect 0    = Empty
perfect n    = Fork 0 (perfect (n-1)) (perfect (n-1))
```

For the *generic* harness, generate with:
```haskell
instance Arbitrary a => Arbitrary (BT a) where
  arbitrary = sized go
    where
      go 0 = pure Empty
      go n = oneof [pure Empty, Fork <$> arbitrary <*> go (n `div` 2) <*> go (n `div` 2)]
```

## Pitfalls

- `height Empty = 0` is the course convention. If a question says "a Leaf has height 1" you must use `Fork _ Empty Empty -> 1` and adjust accordingly.
- `leaves Empty = 1` is wrong here (it's the Data1 lecture *internal* convention for counting dangling leaves, which gives `leaves = size + 1` — useful for proofs but not what problem 73 asks for).
- `flattenInOrder l ++ [x] ++ flattenInOrder r` is O(n²) due to left-biased `++`. For exam purposes that's fine; for production use difference lists or accumulator.
- Don't pattern-match `Fork x (Fork ...) ...` to handle "non-empty left subtree" cases unless you have to — most operations only need `Empty` vs `Fork x l r`.
- Constructor names vary: Assignment 2 uses `Empty | Branch (Maybe Char) Tree Tree` (data-bearing branches), problem 146. Always read the question's data declaration.
- Don't import `Data.Tree` — the course doesn't use it.

## See also

**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Cross-topic:** [tree × state](../cross-matrix/tree-x-state.md) · [tree × writer](../cross-matrix/tree-x-writer.md) · [tree × maybe](../cross-matrix/tree-x-maybe.md) · [tree × either](../cross-matrix/tree-x-either.md) · [tree × reader](../cross-matrix/tree-x-reader.md) · [tree × generic-monad](../cross-matrix/tree-x-generic-monad.md)
**Question families:** [tree-counting](../question-families/tree-counting-family.md) · [tree-validation](../question-families/tree-validation-family.md) · [tree-transform](../question-families/tree-transform-family.md) · [tree-extract](../question-families/tree-extract-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md)
**Related (trees):** [bst](./bst.md) · [rose tree](./rose-tree.md) · [tree fold](./tree-fold.md) · [tree functor](./tree-functor.md) · [tree traversals](./tree-traversals.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
