<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: List × List monad (nondeterminism)**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · **list × list-monad** · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: List × List monad (nondeterminism)

**Why this combo:** the *list itself is the monad*. A `do`-block over `[]` is **enumeration** — every `<-` is "pick a value from this list"; the do-block runs for every combination. This is the canonical way to express nondeterministic search, choose-from-set problems, and Cartesian products.

**Recognition triggers:**
- "Enumerate all combinations / pairs / subsets"
- "Try every possible value of x"
- "Choose-from each list"
- "All paths through a tree" / "all solutions to a problem"
- "Generate all..." anything

**Search keywords:** list monad, do-block list, nondeterminism, guard, MonadPlus, mzero, mplus, sequence list, replicateM list, filterM list

## Pattern (Cartesian product via do-block)

```haskell
pairs :: [Int] -> [Char] -> [(Int, Char)]
pairs xs cs = do
  x <- xs
  c <- cs
  return (x, c)

-- pairs [1,2] "ab" == [(1,'a'),(1,'b'),(2,'a'),(2,'b')]
```

Equivalent forms:

```haskell
-- via list comprehension:
pairs xs cs = [(x, c) | x <- xs, c <- cs]

-- via fmap/<*>:
pairs xs cs = (,) <$> xs <*> cs
```

All three desugar to the same code.

## Worked variants

### Guards (filter from inside do-block)

```haskell
import Control.Monad (guard)

pairsLessThan :: Int -> [Int] -> [Int] -> [(Int, Int)]
pairsLessThan k xs ys = do
  x <- xs
  y <- ys
  guard (x + y < k)
  return (x, y)

-- pairsLessThan 5 [1,2,3] [1,2,3]
--   == [(1,1),(1,2),(1,3),(2,1),(2,2),(3,1)]
```

`guard True = [()]`, `guard False = []`. Inside list monad, `guard False` kills the current branch (drops it from the result).

### Enumeration with bounds

```haskell
import Control.Monad (guard)

triples :: Int -> [(Int, Int, Int)]
triples n = do
  a <- [1..n]
  b <- [a..n]
  c <- [b..n]
  guard (a*a + b*b == c*c)
  return (a, b, c)

-- triples 20 == [(3,4,5),(5,12,13),(6,8,10),(8,15,17),(9,12,15),(12,16,20)]
```

### Subsets via `filterM`

```haskell
subsets :: [a] -> [[a]]
subsets = filterM (const [True, False])

-- subsets [1,2,3] == [[1,2,3],[1,2],[1,3],[1],[2,3],[2],[3],[]]
```

(Order depends on `filterM` impl.)

### Permutations via list monad

```haskell
perms :: [a] -> [[a]]
perms []     = [[]]
perms (x:xs) = do
  rest <- perms xs
  insertAll x rest
  where
    insertAll x [] = [[x]]
    insertAll x ys@(y:ys') = [x : ys] ++ map (y :) (insertAll x ys')
```

(Or use the cleaner `Data.List.permutations`.)

### N-queens-style search

```haskell
queens :: Int -> [[Int]]
queens n = place n
  where
    place 0 = [[]]
    place k = do
      qs <- place (k - 1)
      q  <- [1..n]
      guard (safe q qs)
      return (q : qs)

    safe q qs = and
      [ q /= q' && abs (q - q') /= d
      | (q', d) <- zip qs [1..]
      ]
```

The `do`-block enumerates partial placements, `guard` prunes invalid ones, `return` rebuilds the full solution.

### `replicateM` builds n-tuples-as-list

```haskell
replicateM 3 [0, 1] :: [[Int]]
-- == [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
```

Bit-strings of length 3. Useful for "try all combinations".

### Choose k from n

```haskell
choose :: Int -> [a] -> [[a]]
choose 0 _      = [[]]
choose _ []     = []
choose k (x:xs) = map (x:) (choose (k-1) xs) ++ choose k xs

-- choose 2 [1,2,3,4] == [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
```

### Generate all paths in a tree

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

allPaths :: BT a -> [[a]]
allPaths Empty               = [[]]   -- empty path
allPaths (Fork x Empty Empty) = [[x]]  -- leaf
allPaths (Fork x l r)         = do
  side <- [l, r]                       -- pick left or right
  path <- allPaths side
  return (x : path)
```

(Each `<-` enumerates a choice.)

## Mutations

- **From `>>=` to `concatMap`**: `xs >>= f = concatMap f xs`. Sometimes the question wants you to spell this out.
- **From `<$>` / `<*>` to do-block**: equivalent.
- **Add `guard`**: prune mid-iteration.
- **Replace `[]` with `Maybe`**: turn nondeterminism into "first success" — total semantic change.
- **`pure` vs `[]`**: `pure x = [x]` (one path), `[] = empty` (no paths / failure).

## QuickCheck attacks

```haskell
-- Cartesian product length is product of lengths
prop_cartesian_length :: [Int] -> [Char] -> Bool
prop_cartesian_length xs cs = length (pairs xs cs) == length xs * length cs

-- guard removes all if condition is always False
prop_guard_kills :: [Int] -> Bool
prop_guard_kills xs = null $ do x <- xs; guard False; return x

-- Pythagorean triples are valid
prop_triples_valid :: NonNegative Int -> Bool
prop_triples_valid (NonNegative n) =
  all (\(a,b,c) -> a*a + b*b == c*c) (triples n)

-- subsets has 2^n elements
prop_subsets_size :: NonNegative Int -> Bool
prop_subsets_size (NonNegative n) =
  length (subsets [1..n]) == 2^n

-- replicateM matches replication
prop_replicateM_length :: Bool
prop_replicateM_length =
  length (replicateM 3 [0,1]) == 8
```

## Pitfalls

- **Empty list breaks the do-block.** `do x <- []; return x` is `[]` — no iterations.
- **Order of `<-` matters for result order.** Outer `<-` is "outer loop"; inner is "inner loop". Same as nested loops in C.
- **`pure x = [x]`, NOT `[]`.** `[]` is `empty` (Alternative), not `pure`.
- **`guard` requires `Alternative`** — for `[]`, that's loaded. For Maybe, `guard False = Nothing`.
- **`return` in list monad** wraps a singleton.
- **List comprehension is sugar.** Anything `[expr | bindings]` desugars to do-block over `[]`. Use whichever is clearer.
- **`do` with `<-` from list IS enumeration.** Don't mistake it for "pick one value".

## Comparing list-monad styles

```haskell
-- do-block
do x <- xs; y <- ys; return (x+y)

-- list comprehension
[x + y | x <- xs, y <- ys]

-- applicative
(+) <$> xs <*> ys

-- explicit concatMap
concatMap (\x -> map (\y -> x + y) ys) xs

-- bind
xs >>= \x -> ys >>= \y -> return (x + y)
```

All five give the same result. Marker may ask "rewrite this in `>>=` form" — the desugaring is mechanical.

## guard / MonadPlus

```haskell
guard :: MonadPlus m => Bool -> m ()
guard True  = return ()    -- = pure ()
guard False = mzero        -- = empty
```

For lists: `mzero = []`, `mplus = (++)`. So `guard False` returns `[]`, which when bound in a do-block kills that branch.

## See also

**Combined archetypes:** [A03 generic monad](../archetypes/A03-generic-monad.md) · [A21 list comp synthesis](../archetypes/A21-list-comp-synthesis.md)
**Theory:** [List monad](../monads/list-monad.md)
**Question families:** [monad-combinator](../question-families/monad-combinator-family.md) · [list-comp](../question-families/list-comp-family.md)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md) · [monad attacks](../quickcheck/monad-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
