<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Generic Monad Combinators**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · **generic-combinators** · [io](./io.md) · [list-monad](./list-monad.md) · [maybe](./maybe.md) · [monad-laws](./monad-laws.md) · [monaderror](./monaderror.md) · [multi-effect](./multi-effect.md) · [reader](./reader.md) · [state](./state.md) · [transformer-stack-order](./transformer-stack-order.md) · [transformers](./transformers.md) · [writer](./writer.md)
<!-- siblings:end -->






# Generic Monad Combinators

Combinators from `Control.Monad` and `Prelude` that work for ANY `Monad m`. Use when the question says `Monad m =>` or `Applicative f =>` in the signature.

## Complete reference table

| Op | Signature | Semantics (one-line) | Use when |
|---|---|---|---|
| `pure` / `return` | `Monad m => a -> m a`                                        | inject pure value | always available |
| `(>>=)`           | `Monad m => m a -> (a -> m b) -> m b`                        | bind / sequence with dependency | core |
| `(=<<)`           | `Monad m => (a -> m b) -> m a -> m b`                        | flipped `>>=` | when fn is the focus |
| `(>>)`            | `Monad m => m a -> m b -> m b`                               | sequence, **discard** first result | `putStr ">> " >> getLine` |
| `(>=>)`           | `Monad m => (a -> m b) -> (b -> m c) -> a -> m c`           | Kleisli composition (left-to-right) | chain validators |
| `(<=<)`           | `Monad m => (b -> m c) -> (a -> m b) -> a -> m c`           | Kleisli composition (right-to-left, like `(.)`) | mirror of `(.)` |
| `join`            | `Monad m => m (m a) -> m a`                                  | flatten one layer | `join . pure ≡ id` |
| `mapM`            | `Monad m => (a -> m b) -> [a] -> m [b]`                      | map then collect monadic results | "for each, do, collect" |
| `mapM_`           | `Monad m => (a -> m b) -> [a] -> m ()`                       | map but discard results | "for each, do, throw away" |
| `forM`            | `Monad m => [a] -> (a -> m b) -> m [b]`                      | `flip mapM` — body-last syntax | long lambda body |
| `forM_`           | `Monad m => [a] -> (a -> m b) -> m ()`                       | `flip mapM_` | long body, discard |
| `sequence`        | `Monad m => [m a] -> m [a]`                                  | run all, collect | `[Maybe a] -> Maybe [a]` |
| `sequence_`       | `Monad m => [m a] -> m ()`                                   | run all, discard | `[IO ()] -> IO ()` |
| `replicateM`      | `Monad m => Int -> m a -> m [a]`                             | run `n` times, collect | `replicateM 3 readLn` |
| `replicateM_`     | `Monad m => Int -> m a -> m ()`                              | run `n` times, discard | `replicateM_ 10 (putStrLn "*")` |
| `when`            | `Applicative f => Bool -> f () -> f ()`                      | run if True, else skip | guard within do |
| `unless`          | `Applicative f => Bool -> f () -> f ()`                      | negated `when` | `unless quiet $ putStrLn ...` |
| `void`            | `Functor f => f a -> f ()`                                   | discard result, keep effect | `void $ readLn` |
| `forever`         | `Applicative f => f a -> f b`                                | repeat forever | game loop |
| `foldM`           | `Monad m => (b -> a -> m b) -> b -> [a] -> m b`             | monadic left fold | imperative accumulator |
| `foldM_`          | `Monad m => (b -> a -> m b) -> b -> [a] -> m ()`            | monadic fold, discard | discard accumulator |
| `filterM`         | `Applicative m => (a -> m Bool) -> [a] -> m [a]`            | predicate may be monadic | "for each, ask if include" |
| `zipWithM`        | `Applicative m => (a -> b -> m c) -> [a] -> [b] -> m [c]`   | monadic zipWith | parallel monadic walk |
| `zipWithM_`       | `Applicative m => (a -> b -> m c) -> [a] -> [b] -> m ()`    | monadic zipWith, discard | |
| `liftM`           | `Monad m => (a -> b) -> m a -> m b`                          | legacy alias for `fmap` | almost never needed |
| `ap`              | `Monad m => m (a -> b) -> m a -> m b`                        | legacy `<*>` | for completeness |
| `guard`           | `Alternative f => Bool -> f ()`                              | `True → pure ()`, `False → empty` | list/maybe monad filter |
| `msum`            | `Foldable t, MonadPlus m => t (m a) -> m a`                  | combine with `<|>` / `mplus` | choose first non-empty |
| `mfilter`         | `MonadPlus m => (a -> Bool) -> m a -> m a`                   | filter inside any MonadPlus | |

## Mock Q2 — `applyNTimes` (preferred version is in A03)

**Use the simpler forward recursion from [A03](../archetypes/A03-generic-monad.md#canonical-template) — copy that one.** It is the cleanest applyNTimes in the vault:

```haskell
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx _  0 = do x <- mx; return [x]
applyNTimes mx mf n = do x  <- mx
                         xs <- applyNTimes (mf x) mf (n - 1)
                         return (x : xs)
```

### Alternative — backwards-building variant (harder; NOT preferred)

```haskell
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx mf n = reverse <$> go n
 where
  go 0 = (\x -> [x]) <$> mx
  go m = do
   xs <- go (m - 1)
   x  <- mf (head xs)
   pure (x : xs)
```

The shape: produce a value from `mx`, then `n` times apply `mf` to the latest value, returning the chain. The trick is `reverse <$>` at the end and building the list backwards so `head xs` is the latest. Works for *any* monad — but the `head xs` and final `reverse` make it fiddlier than the forward version above, so prefer A03's.

Examples of monomorphisations the marker tests:
- `m = []`, `mx = [1]`, `mf = \x -> [x+1, x*2]` → branching list of trajectories.
- `m = Maybe`, `mx = Just 0`, `mf = \x -> if x < 10 then Just (x+1) else Nothing` → may fail.
- `m = State Int`, `mx = pure 0`, `mf = \x -> modify (+1) >> pure (x+1)` → counts iterations.

## One-line "use when" for each

### Sequencing / chaining

#### `(>>=)` — bind with dependency
```haskell
getLine >>= putStrLn          -- echo
Just 5 >>= \x -> Just (x+1)   -- Just 6
```

#### `(>>)` — sequence, discard
```haskell
putStr "name: " >> getLine    -- prompt then read
```

#### `(=<<)` — flipped bind (good for `f =<< action`)
```haskell
print =<< getLine             -- print the input line
```

#### `(>=>)` — Kleisli compose
```haskell
safeDiv 100 >=> safeDiv 50    -- :: Int -> Maybe Int  (first: 100/x, then 50/result)
```

#### `(<=<)` — mirror of `(.)` for monadic fns
```haskell
parseInt <=< fmap toLower     -- if parseInt :: String -> Maybe Int
```

#### `join` — flatten
```haskell
join (Just (Just 5))          -- Just 5
join [[1,2],[3,4]]            -- [1,2,3,4]    (list-monad join = concat)
```

### Iterating over a list

#### `mapM` — collect results
```haskell
safeDiv :: Int -> Int -> Maybe Int       -- helper used below
safeDiv _ 0 = Nothing
safeDiv a b = Just (a `div` b)

mapM (safeDiv 10) [2,5,10]   -- Just [5,2,1]   (note the section: safeDiv is applied to 10 first)
mapM print [1,2,3]           -- prints, returns IO [(), (), ()]
sequence . map f = mapM f
```

#### `mapM_` — discard
```haskell
mapM_ print [1,2,3]           -- prints, returns IO ()
```

#### `forM` / `forM_` — flipped versions
```haskell
forM [1..5] $ \i -> do        -- when body is long, body-last reads nicer
  putStrLn ("i = " ++ show i)
  pure (i * i)
```

#### `sequence` — convert `[m a]` to `m [a]`
```haskell
sequence [Just 1, Just 2, Just 3]    -- Just [1,2,3]
sequence [Just 1, Nothing, Just 3]   -- Nothing
sequence [getLine, getLine]          -- IO [String, String]
```

#### `replicateM` — repeat an action
```haskell
replicateM 3 readLn                  -- IO [Int]   (read 3 ints) — problem 110
replicateM 5 (pure 0 :: Maybe Int)   -- Just [0,0,0,0,0]
```

### Conditionals

#### `when` / `unless`
```haskell
when (n > 0) $ putStrLn "positive"
unless quiet $ putStrLn "verbose log"
```

#### `void` — keep effect, drop value
```haskell
void getLine        -- read a line, throw away the string
void (forever m)    -- type-juggle when forever returns the wrong shape
```

#### `forever` — never returns
```haskell
forever (putStrLn "ping" >> threadDelay 1000000)
```

### Folds and filters

#### `foldM` — monadic foldl
```haskell
import Data.List (foldl')
-- Pure: foldl' (+) 0 [1..10]
-- Monadic, with logging:
foldM (\acc x -> tell [show x] >> pure (acc + x)) 0 [1..10] :: Writer [String] Int
```

#### `filterM` — monadic filter
```haskell
filterM (\x -> pure (x > 3)) [1..6]       -- Just [4,5,6] in Maybe
filterM (\_ -> [True, False]) [1,2,3]     -- powerset!
```

#### `zipWithM` / `zipWithM_`
```haskell
zipWithM (\a b -> pure (a + b)) [1,2,3] [10,20,30]   -- Just [11,22,33]
zipWithM_ (\i x -> putStrLn (show i ++ ": " ++ x)) [1..] ["a","b","c"]
```

### List-monad specific

#### `guard` — filter inside `do`
```haskell
import Control.Monad (guard)

triples n = do
  a <- [1..n]; b <- [a..n]; c <- [b..n]
  guard (a*a + b*b == c*c)
  pure (a, b, c)
```

## Reimplementations (problems 128–130)

These appear as "implement these by hand" questions.

### `sequence` from `>>=`
```haskell
sequenceM :: Monad m => [m a] -> m [a]
sequenceM []     = pure []
sequenceM (m:ms) = do
  x  <- m
  xs <- sequenceM ms
  pure (x : xs)
```

### `mapM` via `sequence`
```haskell
mapM' :: Monad m => (a -> m b) -> [a] -> m [b]
mapM' f = sequence . map f

-- OR direct:
mapM' _ []     = pure []
mapM' f (x:xs) = do
  y  <- f x
  ys <- mapM' f xs
  pure (y : ys)
```

### `join` from `>>=`
```haskell
join' :: Monad m => m (m a) -> m a
join' mma = mma >>= id
```

### `liftA2` from `<*>`
```haskell
liftA2' :: Applicative f => (a -> b -> c) -> f a -> f b -> f c
liftA2' g fa fb = pure g <*> fa <*> fb
-- equivalent: g <$> fa <*> fb
```

## Common combinator-result tables

### `sequence` on each monad
```
sequence [Just 1, Just 2]    == Just [1, 2]
sequence [Just 1, Nothing]   == Nothing
sequence [[1,2], [3,4]]      == [[1,3],[1,4],[2,3],[2,4]]     -- Cartesian!
sequence [Right 1, Right 2]  == Right [1, 2]
sequence [Right 1, Left "x"] == Left "x"
```

### `replicateM n m` for each monad
```
replicateM 3 [0,1]           == [[0,0,0],[0,0,1],[0,1,0],...,[1,1,1]]   -- 2^3 lists
replicateM 3 (Just 7)        == Just [7,7,7]
replicateM 3 readLn          :: IO [Int]                                -- reads 3 lines
replicateM_ 5 (putStr "*")   :: IO ()                                    -- "*****"
```

## Pitfalls

- `mapM` vs `mapM_` — using `mapM` and ignoring the result type-checks but allocates a list for nothing. Use `mapM_` if you don't need results.
- `sequence` on lists `[[a]] -> [[a]]` does **Cartesian product**, NOT concatenation. (For concat, use `concat` or `join`.)
- `replicateM 0 m == pure []` (the empty effect). Not an error.
- `forever m` has type `m b` for any `b` — the type annotation may need help.
- `when` takes a `Bool` then an `f ()` — easy to invert.
- `guard True == pure ()`, `guard False == empty` — only works in `Alternative` (lists, Maybe, parsers).
- `void` drops the value, NOT the effect: `void getLine` STILL reads.
- For `foldM`, the accumulator order matches `foldl`, not `foldr`. There's no `foldrM` in the basic Prelude.

## Quick `<*>` vs `>>=` decision

- If the second action **does not depend on** the first's result → use `<*>` / `liftA2`.
- If it depends → use `>>=` / `do`-notation.
- `<*>` works for *Applicative*, which is strictly weaker than Monad. Some structures (e.g. some parsers, validation) are Applicative but not Monad.

## Worked examples

- **Mock Q2** (`applyNTimes`) — see top of file.
- Problem 109 (`mapMTree`) — monadic map over a tree.
- Problem 110 (`replicateM 3 readLn`).
- Problem 128 (`join`), 129 (`sequenceM`), 130 (`mapM'`).

## See also

**Archetypes:** [A03 generic monad](../archetypes/A03-generic-monad.md)
**Cross-topic:** [tree × generic-monad](../cross-matrix/tree-x-generic-monad.md) · [list × monad](../cross-matrix/list-x-monad.md)
**Question families:** [monad-combinator](../question-families/monad-combinator-family.md)
**QuickCheck:** [monad attacks](../quickcheck/monad-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
