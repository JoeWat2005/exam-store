<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: monad-combinator**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · **monad-combinator** · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: monad-combinator

**Archetype:** A11 (apply-once monadic combinator over a list/Int)   |   **Stars:** ⭐⭐⭐⭐   |   **Course week(s):** 9–10
**Search keywords:** applyNTimes, mapM, sequence, replicateM, forM, foldM, filterM, iterate, monadic combinator

## Generator template
```haskell
-- The seed: a generic combinator that walks some shape, runs monadic actions,
-- and threads the results.
seed :: Monad m => (a -> m b) -> [a] -> m [b]
seed _ []     = return []
seed f (x:xs) = do
  y  <- f x
  ys <- seed f xs
  return (y : ys)
-- ^ this is `mapM`.
```

Mutations differ along:
- **Source shape:** `[a]` (mapM), `Int` (replicateM), `BT a` (mapMTree), or "result of last step" (applyNTimes/iterate).
- **What's collected:** `[b]` (mapM), `()` (mapM_), `Bool` (allM), `b` (foldM).
- **Order of effects:** left-to-right (canonical) vs reverse (rare).

## Mutations (the examiner picks one)

### Mutation 1 — applyNTimes (= mock Q2)
**Spec:** Given `mx :: m a`, `mf :: a -> m a`, `n :: Int`, iterate `mf` from `mx` exactly `n` times, returning all `n+1` intermediate values.
**Sig:** `applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]`
**What changes vs seed:** "Source" is the *previous result*, not a list. Output list is the trajectory.
**Solution:**
```haskell
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx _  0 = do x <- mx; pure [x]
applyNTimes mx mf n = do
  xs <- applyNTimes mx mf (n - 1)
  y  <- mf (last xs)
  pure (xs ++ [y])
```
Or, the mock-solution variant (reverse-build):
```haskell
applyNTimes mx mf n = reverse <$> go n
  where
    go 0 = (:[]) <$> mx
    go m = do xs <- go (m - 1)
              x  <- mf (head xs)
              pure (x : xs)
```
**QC trap:** Result has length `n + 1` (NOT `n`). Each monadic action runs exactly once — `mx` runs once and `mf` runs `n` times. If you write `applyNTimes mx mf (n-1) >> applyNTimes mx mf (n-1)` you re-execute `mx`.

### Mutation 2 — mapM' (= problem 130)
**Spec:** Apply a monadic action to each element, sequence the results.
**Sig:** `mapM' :: Monad m => (a -> m b) -> [a] -> m [b]`
**Solution:**
```haskell
mapM' :: Monad m => (a -> m b) -> [a] -> m [b]
mapM' _ []     = return []
mapM' f (x:xs) = do
  y  <- f x
  ys <- mapM' f xs
  return (y : ys)
```
**QC trap:** Order of effects is left-to-right. On Maybe, the first `Nothing` aborts and no later actions run.

### Mutation 3 — sequenceM (= problem 129)
**Spec:** Sequence a list of monadic actions into a monadic list.
**Sig:** `sequenceM :: Monad m => [m a] -> m [a]`
**Solution:**
```haskell
sequenceM :: Monad m => [m a] -> m [a]
sequenceM []       = return []
sequenceM (mx:mxs) = do
  x  <- mx
  xs <- sequenceM mxs
  return (x : xs)
```
Or equivalently: `sequenceM = mapM' id`. Or: `sequenceM = foldr (\mx mxs -> (:) <$> mx <*> mxs) (return [])`.
**QC trap:** `sequenceM [Just 1, Just 2, Nothing, Just 3] == Nothing` — first Nothing kills the whole list.

### Mutation 4 — replicateM' (n copies of one action)
**Spec:** Run the same monadic action `n` times, collecting results.
**Sig:** `replicateM' :: Monad m => Int -> m a -> m [a]`
**Solution:**
```haskell
replicateM' :: Monad m => Int -> m a -> m [a]
replicateM' n ma | n <= 0 = return []
replicateM' n ma          = do
  x  <- ma
  xs <- replicateM' (n - 1) ma
  return (x : xs)
```
**QC trap:** Negative or zero `n` → empty list. With IO, this *runs* the action n times (e.g. `replicateM 3 readLn` reads three lines).

### Mutation 5 — forM' (mapM' with args flipped)
**Spec:** Same as mapM but with the list first.
**Sig:** `forM' :: Monad m => [a] -> (a -> m b) -> m [b]`
**Solution:**
```haskell
forM' :: Monad m => [a] -> (a -> m b) -> m [b]
forM' = flip mapM'
```
**QC trap:** The only difference vs mapM' is argument order — useful when the action is a multi-line `do` block at the call site.

### Mutation 6 — foldM' (monadic fold)
**Spec:** Like foldl, but the combine returns a monadic action.
**Sig:** `foldM' :: Monad m => (b -> a -> m b) -> b -> [a] -> m b`
**Solution:**
```haskell
foldM' :: Monad m => (b -> a -> m b) -> b -> [a] -> m b
foldM' _ z []     = return z
foldM' f z (x:xs) = do
  z' <- f z x
  foldM' f z' xs
```
**QC trap:** Threads `z` through the monad; on Maybe, returns `Nothing` as soon as any step does. Builds left-to-right, like foldl.

### Mutation 7 — filterM' (monadic filter)
**Spec:** Like filter, but the predicate returns `m Bool`.
**Sig:** `filterM' :: Monad m => (a -> m Bool) -> [a] -> m [a]`
**Solution:**
```haskell
filterM' :: Monad m => (a -> m Bool) -> [a] -> m [a]
filterM' _ []     = return []
filterM' p (x:xs) = do
  b  <- p x
  ys <- filterM' p xs
  return (if b then x : ys else ys)
```
**QC trap:** Famous "powerset trick": `filterM (const [True, False]) xs` returns the powerset of `xs`. (List monad.)

### Mutation 8 — mapMTree (= problem 109)
**Spec:** Apply a monadic action to every value in a binary tree.
**Sig:** `mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)`
**Solution:**
```haskell
mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)
mapMTree _ Empty        = return Empty
mapMTree f (Fork v l r) = do
  v' <- f v
  l' <- mapMTree f l
  r' <- mapMTree f r
  return (Fork v' l' r')
```
**QC trap:** Order matters for State/Writer: the root is processed before its children here (pre-order). In-order requires `l' <- ...; v' <- ...; r' <- ...`.

### Mutation 9 — iterate' (lazy infinite version)
**Spec:** Build `[x, f x, f (f x), ...]`.
**Sig:** `iterate' :: (a -> a) -> a -> [a]`
**Solution:**
```haskell
iterate' :: (a -> a) -> a -> [a]
iterate' f x = x : iterate' f (f x)
```
**QC trap:** Infinite list — only use with `take`. Not a monad combinator per se, but the *pure* sibling of applyNTimes.

### Mutation 10 — whenM / unlessM
**Spec:** Conditional execution of monadic actions.
**Sig:** `whenM :: Monad m => m Bool -> m () -> m ()`
**Solution:**
```haskell
whenM :: Monad m => m Bool -> m () -> m ()
whenM cond act = do
  b <- cond
  if b then act else return ()
```
**QC trap:** `cond` runs even if `act` doesn't. `Control.Monad.when` has a simpler signature `Bool -> m () -> m ()`.

## Hidden-predicate mutations
- "applyNTimes but stop early if some predicate holds" → swap the recursion to check `mf` result against a predicate.
- "mapM but skip Nothings" → `mapMaybeM`:
```haskell
mapMaybeM :: Monad m => (a -> m (Maybe b)) -> [a] -> m [b]
mapMaybeM _ []     = return []
mapMaybeM f (x:xs) = do
  mb <- f x
  ys <- mapMaybeM f xs
  return (maybe ys (:ys) mb)
```

## Accumulator-style alternative
The list-building style with `(:)` is the canonical accumulator pattern. For long input, you may want CPS / Difference list to avoid the right-recursion stack growth:
```haskell
mapMAcc f = go id
  where
    go k []     = return (k [])
    go k (x:xs) = do y <- f x
                     go (k . (y:)) xs
```

## Fold-style alternative
Everything in this family can be expressed via foldr in the underlying monad:
```haskell
mapMfold f = foldr (\x mxs -> do y <- f x; ys <- mxs; return (y:ys)) (return [])
sequenceMfold = foldr (\mx mxs -> do x <- mx; xs <- mxs; return (x:xs)) (return [])
```
Idiomatic but less obviously correct on first reading.

## Cross-family combinations
- this family + Writer → `mapM (\x -> tell [show x] >> return x) xs` for logging
- this family + State → `mapM_ updateState xs` for stateful pass
- this family + Maybe → `mapM safeDiv xs` short-circuits on first divide-by-zero
- this family + `tree-counting-family.md` → `countLeaves` (state) is a Folder over a tree

## QuickCheck universal attacks
- **Empty input:** every combinator returns `pure (initial-shape)` — `return []` for mapM/sequence/replicateM 0, `return z` for foldM.
- **Single-element input:** runs the action exactly once; result has length 1.
- **Maybe with one Nothing in middle:** confirms left-to-right short-circuit.
- **`replicateM 0 act` does NOT run `act`:** subtle — guarded by `n <= 0`.
- **`mapM return xs == return xs`:** identity property.
- **`foldM (\acc x -> Just (acc + x)) 0 == Just . sum`:** sanity check.

## Pitfalls (per mutation)
- M1: returning `n` values instead of `n+1`. Forgetting to run `mx` exactly once.
- M2: order swap — `mapM f xs` is left-to-right; running `mapM f (reverse xs)` is different in the Writer monad.
- M3: returning `m [a]` versus `[m a]` — these are sequenced in opposite directions.
- M4: not handling `n <= 0`.
- M5: arg order matters at the call site (`forM xs (\x -> ...)`).
- M6: writing it like foldr (right-fold) instead of foldl (left-fold).
- M7: returning `m (Maybe [a])` because of accidental Maybe-lifting.
- M8: wrong tree traversal order (pre/in/post).
- M9: trying to evaluate the whole infinite list.
- M10: confusing `whenM` with `when` — the former takes `m Bool`.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — applyNTimesUntil (early-exit predicate — short-circuiting)

**Spec:** Like `applyNTimes` but stops as soon as a predicate on the result is true; returns the prefix of results up to and including the first satisfying one.

**Type sig:** `applyNTimesUntil :: Monad m => m a -> (a -> m a) -> (a -> Bool) -> Int -> m [a]`

```haskell
applyNTimesUntil :: Monad m => m a -> (a -> m a) -> (a -> Bool) -> Int -> m [a]
applyNTimesUntil mx _  _ 0 = do x <- mx; return [x]
applyNTimesUntil mx mf p n = do
  x <- mx
  if p x
    then return [x]
    else do xs <- applyNTimesUntil (mf x) mf p (n-1)
            return (x:xs)
```

**What changes vs seed:** Adds a stopping predicate, changing the recursion from "always n steps" to "up to n steps". The base case logic gains a branch.

**QC trap:** When the predicate is `True` at step 0, return `[x]` (singleton) not `[]`. Counting off-by-one between "I did n steps" and "I returned n results".

### Mutation 12 — mapMWithState (Monad m + accumulator state — tuple-bound)

**Spec:** Map a Kleisli arrow over a list while threading an accumulator pure value through. Returns the final accumulator and the mapped list.

**Type sig:** `mapAcc :: Monad m => (s -> a -> m (s, b)) -> s -> [a] -> m (s, [b])`

```haskell
mapAcc :: Monad m => (s -> a -> m (s, b)) -> s -> [a] -> m (s, [b])
mapAcc _ s []     = return (s, [])
mapAcc f s (x:xs) = do
  (s',  y)  <- f s x
  (s'', ys) <- mapAcc f s' xs
  return (s'', y : ys)
```

**What changes vs seed:** Carries pure state through a monadic `mapM`. Recursion shape stays list-cons but the step function takes a tuple in and out — a foldM-like pattern without using `Data.List.foldM`.

**QC trap:** Threading the *new* state `s'` into the recursive call (not the old `s`) is the classic bug. State updates are lost if you `return (s, …)` instead of `return (s'', …)`.

## See also

**Primary archetype:** [A03 generic monad](../archetypes/A03-generic-monad.md)
**Sibling families:** [applicative-monad-instance](./applicative-monad-instance-family.md)
**Cross-topic:** [tree × generic-monad](../cross-matrix/tree-x-generic-monad.md) · [list × monad](../cross-matrix/list-x-monad.md)
**Theory:** [monad](../typeclasses/monad.md) · [generic combinators](../monads/generic-combinators.md)
**QuickCheck:** [monad attacks](../quickcheck/monad-attacks.md)
**Pitfalls:** [P-007 applyNTimes 0 returns [] not [x]](../pitfalls/HIGH-severity.md#p-007)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
