<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: List × Monad m (`mapM`, `filterM`, `replicateM`, `forM`)**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · **list × monad** · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: List × Monad m (`mapM`, `filterM`, `replicateM`, `forM`)

**Why this combo:** lists are the simplest "container" and the most common driver for monadic effects. `mapM` runs an effect at each element and collects the results; `filterM` runs an effectful predicate; `replicateM` runs the same effect n times. These are the core list-x-monad idioms — one definition, fits every monad.

**Recognition triggers:**
- "Apply a monadic action to each element of a list"
- "Filter a list with a monadic predicate"
- "Generate a list of `n` random / fresh / stateful values"
- "Sequence a list of actions"
- Signature `Monad m => (a -> m b) -> [a] -> m [b]` or similar.

**Search keywords:** mapM, mapM_, filterM, replicateM, forM, sequence, mapM list, monadic recursion list, traverse list

## Pattern (mapM — the workhorse)

```haskell
mapM :: Monad m => (a -> m b) -> [a] -> m [b]
mapM _ []     = return []
mapM f (x:xs) = do
  y  <- f x
  ys <- mapM f xs
  return (y : ys)

-- Equivalent (Applicative-flavoured):
mapM f = traverse f       -- = traverse for [] is mapM constrained to Monad

-- _ -version: discard the results
mapM_ :: Monad m => (a -> m b) -> [a] -> m ()
mapM_ _ []     = return ()
mapM_ f (x:xs) = do f x; mapM_ f xs
```

## Worked variants

### filterM (monadic filter)

```haskell
filterM :: Monad m => (a -> m Bool) -> [a] -> m [a]
filterM _ []     = return []
filterM p (x:xs) = do
  keep <- p x
  ys   <- filterM p xs
  return $ if keep then x : ys else ys
```

In the list monad, `filterM` returns ALL subsets:

```haskell
ghci> filterM (\_ -> [True, False]) [1,2,3]
[[1,2,3], [1,2], [1,3], [1], [2,3], [2], [3], []]
```

### replicateM (run an action n times, collect results)

```haskell
replicateM :: Monad m => Int -> m a -> m [a]
replicateM 0 _ = return []
replicateM n m = do
  x  <- m
  xs <- replicateM (n - 1) m
  return (x : xs)
```

E.g. `replicateM 3 getLine` gets 3 lines from stdin.

### sequence (turn a list of actions into an action of list)

```haskell
sequence :: Monad m => [m a] -> m [a]
sequence []     = return []
sequence (m:ms) = do
  x  <- m
  xs <- sequence ms
  return (x : xs)

-- Equivalent: mapM id
```

### forM (mapM with args swapped — useful when fn is long)

```haskell
forM :: Monad m => [a] -> (a -> m b) -> m [b]
forM = flip mapM
```

```haskell
forM [1,2,3] $ \n -> do
  let r = n * n
  modify (+r)
  return r
```

### foldM (monadic fold)

```haskell
foldM :: Monad m => (b -> a -> m b) -> b -> [a] -> m b
foldM _ z []     = return z
foldM f z (x:xs) = do
  z' <- f z x
  foldM f z' xs
```

E.g. compute sum and count via State:

```haskell
sumAndCount :: [Int] -> State Int Int
sumAndCount = foldM (\acc x -> do modify (+1); return (acc + x)) 0
```

### zipWithM (zip + map + sequence)

```haskell
zipWithM :: Monad m => (a -> b -> m c) -> [a] -> [b] -> m [c]
zipWithM f xs ys = sequence (zipWith f xs ys)
```

### when / unless

```haskell
when :: Monad m => Bool -> m () -> m ()
when True  m = m
when False _ = return ()

unless :: Monad m => Bool -> m () -> m ()
unless = when . not
```

Used inside mapM loops to gate effects.

## The MockTest Q2 pattern (applyNTimes)

```haskell
-- Iterate an effectful function n times, accumulating results.
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx mf n = reverse <$> go n
  where
    go 0 = (\x -> [x]) <$> mx
    go m = do
      xs <- go (m - 1)
      x  <- mf (head xs)
      return (x : xs)
```

Or the cleaner forward-direction:

```haskell
applyN :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyN mx _  0 = do x <- mx; return [x]
applyN mx mf n = do
  xs <- applyN mx mf (n - 1)
  x  <- mf (head xs)        -- mind: "exactly once" wording
  return (x : xs)
```

The "exactly once" wording is the hint: don't recall `mf` twice; thread the result.

## Instantiations

### With Maybe — fail if any element bad

```haskell
mapM Just [1,2,3]                                    == Just [1,2,3]
mapM (\x -> if x > 0 then Just x else Nothing) [1,-1,3]  == Nothing
```

### With State — counter / fresh / labelling

```haskell
mapM (\x -> do n <- get; put (n+1); return (n, x)) "abc"
  -- evalState ... 0 == [(0,'a'),(1,'b'),(2,'c')]
```

### With Writer — log each element

```haskell
mapM (\x -> do tell [show x]; return x) [1,2,3]
  -- execWriter ... == ["1","2","3"]
```

### With IO — print each

```haskell
mapM_ print [1,2,3]
  -- prints 1, 2, 3 on separate lines
```

### With Reader — env-aware lookup of each

```haskell
mapM (\k -> asks (lookup k)) keys :: Reader Env [Maybe Int]
```

### With List (non-determinism) — see [list-x-list-monad.md](list-x-list-monad.md)

```haskell
mapM (\_ -> [True, False]) [1,2,3] = [[T,T,T], [T,T,F], ..., [F,F,F]]
```

## Mutations

- **Strict vs lazy**: `mapM_` discards results — use it when only the effect matters.
- **`for` vs `mapM`**: same thing, args swapped.
- **`forM_`** / `mapM_` / `sequence_` — all `_`-variants discard.
- **`traverse` vs `mapM`**: `traverse` is more general (Applicative). For exam: pick whichever is allowed.
- **Replace `[a]` with another Traversable** — same idea on trees.

## QuickCheck attacks

```haskell
-- Identity in Identity monad
prop_mapM_identity :: [Int] -> Bool
prop_mapM_identity xs = runIdentity (mapM Identity xs) == xs

-- Length preservation
prop_mapM_length :: [Int] -> Bool
prop_mapM_length xs = length (runIdentity (mapM Identity xs)) == length xs

-- Sequence matches mapM id
prop_sequence_mapM_id :: [Identity Int] -> Bool
prop_sequence_mapM_id ms = runIdentity (sequence ms) == runIdentity (mapM id ms)

-- replicateM 0 == return []
prop_replicateM_zero :: Bool
prop_replicateM_zero = runIdentity (replicateM 0 (Identity 5)) == ([] :: [Int])

-- filterM with const (return True) == identity
prop_filterM_keepAll :: [Int] -> Bool
prop_filterM_keepAll xs =
  runIdentity (filterM (const (Identity True)) xs) == xs
```

## Pitfalls

- **`mapM_` discards results.** If you need them, use `mapM`. If you only want the side effect, `mapM_`.
- **List-monad surprise.** `mapM f xs` in the list monad gives the cartesian product — not what you want for "first element".
- **`replicateM_ n m`** discards results but still RUNS `m` n times.
- **`foldM`** order: `foldM f z [x1,x2] = f z x1 >>= \z' -> f z' x2`. State threads left-to-right.
- **`flip` confusion with `forM`**: `forM = flip mapM`, so `forM xs f` not `forM f xs`.
- **`return` placement**: `mapM` rebuilds via `return (y : ys)` — forgetting `return` is a type error.
- **`sequence []` == `return []`** — base case.
- **Strict accumulation in `foldM`**: results are computed left-to-right, but laziness can defer.

## See also

**Combined archetypes:** [A03 generic monad](../archetypes/A03-generic-monad.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)
**Theory:** [generic Monad m](../monads/generic-combinators.md)
**Question families:** [monad-combinator](../question-families/monad-combinator-family.md) · [list-fold](../question-families/list-fold-family.md)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md) · [monad attacks](../quickcheck/monad-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
