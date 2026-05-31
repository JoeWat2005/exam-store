<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: List × State**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · **list × state** · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: List × State

**Why this combo:** thread a counter / accumulator / running total / partition table through a list. `mapM` over State is the labelling pattern; `foldM` over State is the running-total pattern.

**Recognition triggers:**
- "Number each element of the list with its index"
- "Compute a running total while building the list"
- "Partition a list into buckets via a counter"
- "Allocate a fresh ID per element"

**Search keywords:** State list, labelList, indexed list, running total State, partition State, fresh list

## Pattern (label with index)

```haskell
import Control.Monad.State

labelList :: [a] -> [(Int, a)]
labelList xs = evalState (mapM step xs) 0
  where
    step x = do n <- get; put (n + 1); return (n, x)

-- labelList "abc" == [(0,'a'),(1,'b'),(2,'c')]
```

## Worked variants

### Running total

```haskell
runningTotal :: Num a => [a] -> [a]
runningTotal xs = evalState (mapM step xs) 0
  where
    step x = do n <- get; let n' = n + x; put n'; return n'

-- runningTotal [1,2,3,4] == [1,3,6,10]
```

### Partition by index parity

```haskell
partitionByIndex :: [a] -> ([a], [a])  -- (evens, odds)
partitionByIndex xs = execState (mapM_ step xs) ([], [])
  where
    step x = do
      (es, os) <- get
      put $ if length es <= length os
            then (x : es, os)        -- even index → es
            else (es, x : os)
-- (Returns reversed; caller can reverse if order matters.)
```

### Allocate fresh IDs (generate n unique IDs)

```haskell
fresh :: State Int Int
fresh = do n <- get; put (n+1); return n

idList :: Int -> State Int [Int]
idList 0 = return []
idList n = do
  x  <- fresh
  xs <- idList (n - 1)
  return (x : xs)

-- evalState (idList 5) 0 == [0,1,2,3,4]
```

### Build a unique-list (dedupe via State Set)

```haskell
import qualified Data.Set as Set

dedupe :: Ord a => [a] -> [a]
dedupe xs = evalState (go xs) Set.empty
  where
    go []     = return []
    go (y:ys) = do
      seen <- get
      if y `Set.member` seen
        then go ys
        else do put (Set.insert y seen); rest <- go ys; return (y : rest)
```

### Stateful zip (zip with running counter)

```haskell
zipWithCount :: [a] -> [b] -> [(Int, a, b)]
zipWithCount xs ys = evalState (zipWithM step xs ys) 0
  where
    step a b = do n <- get; put (n+1); return (n, a, b)
```

### Iterate effect n times — replicateM

```haskell
replicateM :: Monad m => Int -> m a -> m [a]
-- defined in Control.Monad

genFresh :: Int -> [Int]
genFresh n = evalState (replicateM n fresh) 0
```

### Reverse-build (efficient prepend)

```haskell
reverseAcc :: [a] -> [a]
reverseAcc xs = execState (mapM_ (\x -> modify (x:)) xs) []

-- reverseAcc [1,2,3] == [3,2,1]
```

(This is the State implementation of the classic accumulator-reverse.)

## Mutations

- **State type**: `Int` / `(Int, Int)` / `[a]` / `Map k v`.
- **Initial value**: 0 / 1 / mempty / custom.
- **`mapM` vs `foldM` vs `mapM_`**: pick by whether you need results / final acc.
- **Backwards** (reverse traversal): `foldr (\x acc -> do ... ) ...` or reverse the list first.
- **Combine with Writer**: counter + log of choices.

## QuickCheck attacks

```haskell
-- labelList preserves values
prop_labelList_values :: [Int] -> Bool
prop_labelList_values xs = map snd (labelList xs) == xs

-- labelList indices are [0..n-1]
prop_labelList_idx :: [Int] -> Bool
prop_labelList_idx xs = map fst (labelList xs) == [0 .. length xs - 1]

-- runningTotal matches `scanl (+) 0` tail
prop_runningTotal_matches :: [Int] -> Bool
prop_runningTotal_matches xs = runningTotal xs == tail (scanl (+) 0 xs)

-- Fresh IDs all distinct
prop_idList_distinct :: NonNegative Int -> Bool
prop_idList_distinct (NonNegative n) =
  let ids = evalState (idList n) 0 in length (nub ids) == n
```

## Pitfalls

- **`mapM` vs `mapM_`**: pick the one whose result type matches.
- **`evalState` vs `execState`**: value vs final state.
- **`fresh` defined once** — DRY.
- **State threading is implicit** in `mapM`/`foldM` — don't pass it manually.
- **Reverse-build order**: `mapM_ (modify . (:))` prepends, so result is reversed.
- **`replicateM 0 m` == `return []`** — base case.
- **Initial state**: usually 0; mark spec carefully.

## Comparison: list-x-state vs list-x-writer

| | State | Writer |
|---|---|---|
| Direction | hidden, mutable | side-channel, append-only |
| Read-back | `get`, `gets` | read at end via `runWriter` |
| Use when | per-element counter | per-element log/metric |
| Monoid required? | no | yes (on `w`) |
| Bidirectional? | yes (`put` changes) | no (append-only) |

## See also

**Combined archetypes:** [A02 state game](../archetypes/A02-state-game.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)
**Theory:** [State](../monads/state.md)
**Question families:** [state-counter](../question-families/state-counter-family.md) · [list-fold](../question-families/list-fold-family.md)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md) · [state attacks](../quickcheck/state-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
