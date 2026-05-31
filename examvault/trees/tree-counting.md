<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [trees](./README.md) · **Tree counting — the family generator**

<!-- siblings:start -->
> **Peers:** [binary-tree](./binary-tree.md) · [bst-delete-trace](./bst-delete-trace.md) · [bst](./bst.md) · [expression-tree](./expression-tree.md) · [rose-tree](./rose-tree.md) · **tree-counting** · [tree-fold](./tree-fold.md) · [tree-functor](./tree-functor.md) · [tree-traversals](./tree-traversals.md) · [tree-validation](./tree-validation.md) · [tree-zipper](./tree-zipper.md)
<!-- siblings:end -->






# Tree counting — the family generator

Eight problems are the *same problem*: count things in a tree. Memorise the template, then write the body in three lines per problem.

## The template

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

-- The pattern: walk every Fork; decide what counts; sum.
count :: (a -> Bool) -> BT a -> Int
count _ Empty                  = 0
count p (Fork x l r)
    | p x       = 1 + count p l + count p r
    | otherwise =     count p l + count p r
```
Every count-variant on BT is a one-line mutation of this.

## The family — each is a one-line change

### 1. Count all nodes (`size`)
```haskell
sizeT :: BT a -> Int
sizeT = count (const True)
-- predicate that's always True; equivalently:
-- sizeT Empty        = 0
-- sizeT (Fork _ l r) = 1 + sizeT l + sizeT r
```

### 2. Count leaves (`Fork _ Empty Empty`)
```haskell
leavesT :: BT a -> Int
leavesT Empty                = 0
leavesT (Fork _ Empty Empty) = 1
leavesT (Fork _ l r)         = leavesT l + leavesT r
-- specialised: predicate isn't on `x` alone, it's on the SHAPE
```

### 3. Count internal nodes (≥1 non-Empty child)
```haskell
internalT :: BT a -> Int
internalT Empty                = 0
internalT (Fork _ Empty Empty) = 0
internalT (Fork _ l r)         = 1 + internalT l + internalT r
-- invariant: sizeT t = leavesT t + internalT t
```

### 4. Count nodes matching a predicate
```haskell
countWhere :: (a -> Bool) -> BT a -> Int
countWhere = count
-- the template itself, named usefully
```

### 5. Count occurrences of a specific value
```haskell
countValue :: Eq a => a -> BT a -> Int
countValue x = count (== x)
-- problem 80 (countBT)
```

### 6. Count by tag (over a sum-type-valued tree)
```haskell
data Tag = T1 | T2 | T3 deriving Eq

countTag :: Tag -> BT Tag -> Int
countTag t = count (== t)
-- same template, predicate `(== t)`
```

### 7. Count distinct values
```haskell
import Data.List (nub)
import qualified Data.Set as Set      -- only if Set is allowed; in exam, use nub

countDistinct :: Eq a => BT a -> Int
countDistinct = length . nub . toList
  where toList Empty        = []
        toList (Fork x l r) = x : toList l ++ toList r
-- NOT a direct fold; needs to see the whole list of values then dedup
```

### 8. Count at exactly depth k
```haskell
countAtDepth :: Int -> BT a -> Int
countAtDepth k = go 0
  where
    go _ Empty                  = 0
    go d (Fork _ l r) | d == k    = 1                    -- found a node at depth k; don't recurse
                      | otherwise = go (d+1) l + go (d+1) r
-- thread depth `d` as an accumulator
```

### 9. Count at depth ≤ k (top-k levels)
```haskell
countAtMostDepth :: Int -> BT a -> Int
countAtMostDepth k = go 0
  where
    go d _              | d > k     = 0
    go _ Empty                       = 0
    go d (Fork _ l r)                = 1 + go (d+1) l + go (d+1) r
```

### 10. Count nodes whose subtree has size ≥ k (anywhere)
```haskell
countLargeSubtrees :: Int -> BT a -> Int
countLargeSubtrees k Empty            = 0
countLargeSubtrees k t@(Fork _ l r)
    | sizeT t >= k = 1 + countLargeSubtrees k l + countLargeSubtrees k r
    | otherwise    =     countLargeSubtrees k l + countLargeSubtrees k r
-- predicate is on the SUBTREE, not the value
```

### 11. Count distinct paths of a given length
```haskell
countPathsLen :: Int -> BT a -> Int
countPathsLen n = length . filter (== n) . map length . paths
  where
    paths Empty        = [[]]
    paths (Fork x l r) = map (x:) (paths l) ++ map (x:) (paths r)
```

## Rose-tree counting family (variant B, Mock Q1 shape)

```haskell
data Rose a = Leaf a | Branch [Rose a]

countR :: (a -> Bool) -> Rose a -> Int
countR p (Leaf x)    = if p x then 1 else 0
countR p (Branch ts) = sum (map (countR p) ts)
-- countR considers Leaf values only

-- Counting Leafs:
countLeafs :: Rose a -> Int
countLeafs (Leaf _)    = 1
countLeafs (Branch ts) = sum (map countLeafs ts)

-- Counting Branches:
countBranches :: Rose a -> Int
countBranches (Leaf _)    = 0
countBranches (Branch ts) = 1 + sum (map countBranches ts)

-- size = leafs + branches
sizeR :: Rose a -> Int
sizeR (Leaf _)    = 1
sizeR (Branch ts) = 1 + sum (map sizeR ts)
```

## The general count, via foldBT

```haskell
import Prelude hiding (toList)

-- Once you have foldBT, everything's a one-liner:
countF :: (a -> Bool) -> BT a -> Int
countF p = foldBT (\x l r -> (if p x then 1 else 0) + l + r) 0
```
See [tree-fold.md](tree-fold.md).

## State-monad version (problem 113, countLeaves)

```haskell
import Control.Monad.State

countLeavesS :: BT a -> State Int ()
countLeavesS Empty                = return ()
countLeavesS (Fork _ Empty Empty) = modify (+1)
countLeavesS (Fork _ l r)         = countLeavesS l >> countLeavesS r

-- run with: execState (countLeavesS t) 0
```
Same family, different effect type. Useful when you want to *also* log something or thread other state.

## Counting BY a predicate that depends on PATH

Easy if you thread the path in an accumulator:

```haskell
countByPath :: ([a] -> Bool) -> BT a -> Int
countByPath p = go []
  where
    go _   Empty        = 0
    go acc (Fork x l r) = let path = reverse (x:acc)
                          in (if p path then 1 else 0)
                           + go (x:acc) l + go (x:acc) r
```

## Mutations cheat-sheet

| Question phrasing | Predicate / structure |
|-------------------|-----------------------|
| "count odd values" | `count odd` |
| "count nodes >10" | `count (>10)` |
| "count nodes whose value equals their depth" | thread depth, compare |
| "count nodes whose left child is Empty" | match `Fork x Empty _` |
| "count Forks whose subtree-sum is divisible by 3" | predicate on subtree |
| "count complete subtrees" | predicate is `isComplete` (see tree-validation.md) |
| "count duplicates" | `length xs - countDistinct` |
| "count chains of length n" | thread depth + reset on Empty / branching |

## QuickCheck

```haskell
prop_sizeNonneg t                = sizeT t >= 0
prop_leafsInternalSum t          = leavesT t + internalT t == sizeT t
prop_countValueLE x t            = countValue x t <= sizeT t
prop_countDistinctLE t           = countDistinct t <= sizeT t
prop_countWhereTrue t            = countWhere (const True) t == sizeT t
prop_countWhereFalse t           = countWhere (const False) t == 0
prop_countAtDepth k t            = countAtDepth k t <= sizeT t
prop_countSplit p t              = countWhere p t + countWhere (not . p) t == sizeT t
```

## Pitfalls

- For `leavesT`, the predicate is about *shape* (both children Empty), not value. You cannot write it with the value-only `count` template directly.
- `count (const True) t` is `sizeT t` — but if a question says "count all nodes including Empty", `Empty` doesn't count (it's not a node). Lecture convention: only `Fork`s are nodes.
- Depth-aware counting needs an accumulator; you cannot do `countAtDepth k = foldBT ...` cleanly because each subtree call needs to know its depth.
- For `countDistinct`, don't try to use a fold with `Set` if `Data.Set` isn't allowed — `nub . toList` is O(n²) but safe.
- Rose-tree variant B: `countR p` only counts Leaf values; the Branch nodes have no value to test.
- Don't forget that `Empty` returns `0` (not `1`). The template's first equation is non-negotiable.

## Cross-references

- Validate family (a related family-generator): [tree-validation.md](tree-validation.md)
- Generic fold (cleanest expression): [tree-fold.md](tree-fold.md)
- State-monad counting: [../monads/state.md](../monads/state.md), [../cross-matrix/tree-x-state.md](../cross-matrix/tree-x-state.md)
- Problem references: 71 (sizeBT), 73 (leavesBT — slightly different — values at leaves), 78 (sumBT), 80 (countBT), 113 (countLeaves State), 117 (count occurrences with State)

## See also

**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Cross-topic:** [tree × state](../cross-matrix/tree-x-state.md)
**Question families:** [tree-counting](../question-families/tree-counting-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md)
**Related (trees):** [binary tree](./binary-tree.md) · [tree fold](./tree-fold.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
