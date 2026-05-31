<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: List × Writer**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · **list × writer** · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: List × Writer

**Why this combo:** emit a log entry per list element. The list provides the iteration; Writer collects the side-channel without any explicit accumulator. Sum/Product/Any/All wrappers turn this into "aggregate over the list".

**Recognition triggers:**
- "Log each element as you visit"
- "Sum up scores while traversing"
- "Count nodes matching a predicate"
- "Build a flattened representation"

**Search keywords:** Writer list, log list, tell list, Sum list Writer, execWriter list, mapM Writer

## Pattern (log each element)

```haskell
import Control.Monad.Writer

logList :: Show a => [a] -> Writer [String] ()
logList = mapM_ (\x -> tell ["Visit " ++ show x])

-- snd (runWriter (logList [1,2,3])) == ["Visit 1","Visit 2","Visit 3"]
-- execWriter (logList [1,2,3])      == ["Visit 1","Visit 2","Visit 3"]
```

## Worked variants

### Sum via Writer

> **WARNING — not an allowed import:** `Sum`/`Product`/`Any`/`All` are in `Data.Monoid` (and `Max`/`Min` in `Data.Semigroup`), which are NOT on the exam whitelist and are NOT re-exported by `Control.Monad.Writer` (`import Control.Monad.Writer` alone gives 'Not in scope: Sum'). To count/total with only allowed imports, use a `Writer [()]`/`Writer [String]` log + `length`, carry an `Int` via `Control.Monad.State`, or define a local `newtype` with a hand-written `Monoid`. Use the `Sum` form only if the question's own `Types` module provides it.

**Primary (whitelist-safe)** — collect the values into a `[a]` log, then `sum`:

```haskell
sumW :: Num a => [a] -> Writer [a] ()
sumW = mapM_ (\x -> tell [x])

-- sum (execWriter (sumW [1,2,3,4])) == 10
```

**Only if `Types` provides `Sum`** (needs `import Data.Monoid (Sum(..))`, NOT whitelisted → scores 0):

```haskell
import Data.Monoid (Sum(..))   -- NOT an allowed import on its own
sumWSum :: Num a => [a] -> Writer (Sum a) ()
sumWSum = mapM_ (tell . Sum)
-- getSum (execWriter (sumWSum [1,2,3,4])) == 10
```

### Count matching predicate

**Primary (whitelist-safe)** — log one `()` per match, then take `length`:

```haskell
countMatching :: (a -> Bool) -> [a] -> Writer [()] ()
countMatching p = mapM_ (\x -> when (p x) (tell [()]))

-- length (execWriter (countMatching even [1..10])) == 5
```

**Only if `Types` provides `Sum`** (needs `import Data.Monoid (Sum(..))`, NOT whitelisted → scores 0):

```haskell
import Data.Monoid (Sum(..))   -- NOT an allowed import on its own
countMatchingSum :: (a -> Bool) -> [a] -> Writer (Sum Int) ()
countMatchingSum p = mapM_ (\x -> when (p x) (tell (Sum 1)))
-- getSum (execWriter (countMatchingSum even [1..10])) == 5
```

### Both result and log (map + log)

```haskell
mapAndLog :: Show a => (a -> b) -> [a] -> Writer [String] [b]
mapAndLog f = mapM (\x -> do tell ["map " ++ show x]; return (f x))

-- runWriter (mapAndLog (*2) [1,2,3])
--   == ([2,4,6], ["map 1","map 2","map 3"])
```

### Statistics (sum + count + max + min)

`Max`/`Min` live in `Data.Semigroup` and `Sum` in `Data.Monoid` — **neither is whitelisted**, so the four-way tuple monoid below scores 0 unless `Types` provides them.

**Primary (whitelist-safe)** — log every value into a `[Int]`, then derive all four stats from the list with allowed Prelude functions:

```haskell
analyse :: [Int] -> Writer [Int] ()
analyse = mapM_ (\x -> tell [x])

-- Run (guard against the empty list before maximum/minimum):
let ys = execWriter (analyse xs)
in (sum ys, length ys, maximum ys, minimum ys)   -- (total, count, max, min)
```

**Only if `Types` provides `Sum`/`Max`/`Min`** (needs `import Data.Monoid (Sum(..))` + `import Data.Semigroup (Max(..), Min(..))`, NOT whitelisted → scores 0):

```haskell
import Data.Monoid (Sum(..))
import Data.Semigroup (Max(..), Min(..))   -- NOT allowed imports on their own
type Stats = (Sum Int, Sum Int, Max Int, Min Int)   -- (total, count, max, min)

analyseStats :: [Int] -> Writer Stats ()
analyseStats = mapM_ $ \x ->
  tell (Sum x, Sum 1, Max x, Min x)

-- Run:
let (_, (Sum tot, Sum cnt, Max mx, Min mn)) = runWriter (analyseStats xs)
in (tot, cnt, mx, mn)
```

### Filter and log dropped

```haskell
filterLog :: Show a => (a -> Bool) -> [a] -> Writer [String] [a]
filterLog p = foldr step (return [])
  where
    step x rest = do
      if p x then do
        xs <- rest
        return (x : xs)
      else do
        tell ["dropped " ++ show x]
        rest

-- runWriter (filterLog even [1,2,3,4])
--   == ([2,4], ["dropped 1","dropped 3"])
```

### foldM-style accumulation with log

```haskell
foldWithLog :: [Int] -> Writer [String] Int
foldWithLog = foldM step 0
  where
    step acc x = do
      let acc' = acc + x
      tell ["added " ++ show x ++ " => " ++ show acc']
      return acc'

-- runWriter (foldWithLog [1,2,3])
--   == (6, ["added 1 => 1","added 2 => 3","added 3 => 6"])
```

### Log at certain points only

```haskell
import Control.Monad (when, unless)

logBig :: (Show a, Ord a) => a -> [a] -> Writer [String] ()
logBig threshold = mapM_ $ \x ->
  when (x > threshold) $ tell ["big: " ++ show x]
```

## Mutations

- **Monoid w**: `[String]`, `[()]`/`[a]` + `length`/`sum`/`product`/`or`/`and` (whitelist-safe), a local `newtype` Monoid, tuple, custom. (`Sum`, `Product`, `Any`, `All` come from `Data.Monoid` — NOT whitelisted, use only if `Types` provides them.)
- **Log granularity**: every element / only matching / only first / only last.
- **Combine with State** (counter + log of recent ops) — see [expr-x-multi.md](expr-x-multi.md).
- **Reverse direction**: `foldr` vs `foldl` vs `mapM_`.

## QuickCheck attacks

```haskell
-- Sum via Writer matches Prelude.sum (whitelist-safe sumW :: Writer [a])
prop_sumW_matches :: [Int] -> Bool
prop_sumW_matches xs =
  sum (execWriter (sumW xs)) == sum xs

-- countMatching gives same as `length . filter p` (whitelist-safe countMatching :: Writer [()])
prop_countMatching_matches :: [Int] -> Bool
prop_countMatching_matches xs =
  length (execWriter (countMatching even xs)) == length (filter even xs)

-- mapAndLog values match plain map
prop_mapAndLog_values :: [Int] -> Bool
prop_mapAndLog_values xs =
  fst (runWriter (mapAndLog (*2) xs)) == map (*2) xs

-- log length == input length (one entry per element)
prop_logList_len :: [Int] -> Bool
prop_logList_len xs =
  length (execWriter (logList xs)) == length xs
```

## Pitfalls

- **`Int` is NOT a monoid.** Whitelist-safe: log into `[Int]`/`[()]` and `sum`/`length` at the end, or a local `newtype` Monoid. (`Sum Int`/`Product Int` work but need the non-whitelisted `Data.Monoid` — see the warning above.)
- **`Writer w` requires `Monoid w`** — instance constraint.
- **`tell` is the only emit primitive.** `return` puts value, not log.
- **Log accumulates left-to-right** in `mapM_`/`mapM`/`foldM` order — match the spec.
- **`execWriter` extracts only the log**; `runWriter` gives `(value, log)`.
- **Tuple monoid** for combined stats — both components must be Monoid.
- **`mapM_ tell xs`** if `xs :: [w]` already.

## Comparison: list-x-writer vs list-x-state

| | Writer | State |
|---|---|---|
| Direction | side-channel, additive | hidden, mutable |
| Read back | end only | anytime via `get` |
| Use when | log / aggregate | counter / dependent decision |
| Monoid required? | yes | no |
| Reversible? | only via Dual | yes |

## See also

**Combined archetypes:** [A15 writer trace](../archetypes/A15-writer-trace.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)
**Theory:** [Writer](../monads/writer.md)
**Question families:** [writer-trace](../question-families/writer-trace-family.md) · [list-fold](../question-families/list-fold-family.md)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md) · [writer attacks](../quickcheck/writer-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
