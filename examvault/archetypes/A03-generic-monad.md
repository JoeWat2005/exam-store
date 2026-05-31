<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A03 — Generic `Monad m =>` Combinator**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · **A03** · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A03 — Generic `Monad m =>` Combinator

**Tier:** 1   |   **Stars:** ⭐⭐⭐⭐⭐
**Mock appearance:** Q2   |   **Assignment appearance:** A3 (Q2 `trace`)
**Combines with:** A01 · A02 · A06 · A08 · A24
**Search keywords:** Monad m · polymorphic · do · return · `<-` · pure · sequenceM · mapM · replicateM · join

## What it tests
Whether you can recurse over a list / count / structure using ONLY `do`, `<-`, `return`, `pure`, `>>=` — no monad-specific primitive (`get`, `tell`, `throwError`, `print`) is allowed because the type is polymorphic in `m`.

## Recognition triggers
- Type signature begins with a class constraint: `Monad m =>` or `Applicative f =>`
- "exactly once" wording: "apply mf to mx exactly n times"
- "intermediate results / values" — return type is `m [a]`, not `m a`
- The signature has more than one `m` in it: `m a -> (a -> m a) -> Int -> m [a]`
- No `import Control.Monad.State` or similar in the question's needed imports
- The example trace uses `IO`: `applyNTimes (return 0) addAndPrint 4` prints lines — code under test runs in `IO`, but the SAME code must work in `Maybe`.

## Canonical template
```haskell
-- A monadic recursion that produces n+1 values.
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx _  0 = do x <- mx; return [x]
applyNTimes mx mf n = do x  <- mx
                         xs <- applyNTimes (mf x) mf (n - 1)
                         return (x : xs)
```

> **This is the simplest `applyNTimes` in the vault** — straight forward recursion, no `reverse`/`head` tricks. Prefer it over the backwards-building variant in [generic-combinators](../monads/generic-combinators.md).

## Mutations (the examiner picks one)

### M1 — `applyNTimes` (Mock Q2)
```haskell
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx _  0 = (\x -> [x]) <$> mx
applyNTimes mx mf n = do x  <- mx
                         xs <- applyNTimes (mf x) mf (n - 1)
                         return (x : xs)
```
What changes: nothing — this IS canonical. `n=0` returns the singleton `[x]` (n+1 = 1 value).

### M2 — `mapM'` (problem 130)
```haskell
mapM' :: Monad m => (a -> m b) -> [a] -> m [b]
mapM' _ []     = return []
mapM' f (x:xs) = do y  <- f x
                    ys <- mapM' f xs
                    return (y : ys)
```
What changes: drive the recursion on the input LIST instead of a counter.

### M3 — `sequenceM` (problem 129)
```haskell
sequenceM :: Monad m => [m a] -> m [a]
sequenceM []     = return []
sequenceM (m:ms) = do x  <- m
                      xs <- sequenceM ms
                      return (x : xs)
```
What changes: action is already inside the list; just chain them.

### M4 — `replicateM'`
```haskell
replicateM' :: Monad m => Int -> m a -> m [a]
replicateM' 0 _ = return []
replicateM' n m = do x  <- m
                     xs <- replicateM' (n - 1) m
                     return (x : xs)
```
What changes: count-driven, ignores list, runs the SAME action `n` times.

### M5 — `join'` (problem 128)
```haskell
join' :: Monad m => m (m a) -> m a
join' mma = do ma <- mma
               ma
```
What changes: no recursion, one `<-`, then the inner action is the body. (Equivalent: `mma >>= id`.)

### M6 — `liftA2'` (problem 127, Applicative)
```haskell
liftA2' :: Applicative f => (a -> b -> c) -> f a -> f b -> f c
liftA2' f fa fb = f <$> fa <*> fb
```
What changes: only Applicative, no recursion, idiomatic `<$>`/`<*>`.

### M7 — `forM_'`
```haskell
forM_' :: Monad m => [a] -> (a -> m b) -> m ()
forM_' []     _ = return ()
forM_' (x:xs) f = f x >> forM_' xs f
```
What changes: like `mapM'` but throws away results; uses `>>` chained.

### M8 — `whenM'`
```haskell
whenM' :: Monad m => m Bool -> m () -> m ()
whenM' mp action = do p <- mp
                      if p then action else return ()
```
What changes: condition is itself monadic; conditionally run the action.

### M9 — `iterateM'`
```haskell
iterateM' :: Monad m => Int -> (a -> m a) -> a -> m [a]
iterateM' 0 _ x = return [x]
iterateM' n f x = do y  <- f x
                     ys <- iterateM' (n - 1) f y
                     return (x : ys)
```
What changes: like M1 but starts from a pure value, not an action; sometimes asked this way.

### M10 — `foldM'`
```haskell
foldM' :: Monad m => (b -> a -> m b) -> b -> [a] -> m b
foldM' _ z []     = return z
foldM' f z (x:xs) = do z' <- f z x
                       foldM' f z' xs
```
What changes: accumulator-style; each step takes the running value plus the next element.

## Worked examples from this course
- Mock Q2: `applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]` — M1.
- Problem sheet Set 13 (#127-130): `liftA2'`, `join'`, `sequenceM`, `mapM'`.
- Problem sheet Set 11 (#109): `mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)` — A03 × A01.
- Assignment 3 Q2: `trace :: FreeState s a -> State ([s],s) a` — must NOT use State-specific primitives in the recursion structure; only the lift converting `m a` to `State (t, s) a` is concrete.

## QuickCheck attack surface
- **n = 0**: produces a singleton list. Bug: `pure []` (zero items) instead of `pure [x]` (one item).
- **n = 1**: produces `[x, mf x]`. Bug: `(mf x : applyNTimes …)` forgetting initial `x`.
- **Side effects exactly once**: the marker runs in `IO` (or `State`) and checks the number of `print`s / writes equals `n`. If you call `mf x` twice (e.g. accidentally `let y = mf x in do x' <- mf x; …`) you get double the side effects → fail.
- **Order of `tell` / `put` matches order of returned list**: e.g. for `addAndPrint` the printed lines must precede the returned list.
- **Polymorphism**: the same function is tested across `IO`, `Maybe`, `State`. Using `get` or `print` makes it fail at type-check for `Maybe`.
- For `mapM` shape: `length (mapM' f xs)` (where `m=Identity`) `== length xs`.

## Pitfalls (marks-killers)
- **Using a monad-specific primitive**: `get`, `put`, `tell`, `throwError`, `print`, `liftIO` — all forbidden when `Monad m =>`. Fail at type-check time.
- **Calling `mf` twice**: a common bug is `do x <- mx; xs <- applyNTimes (mf x) mf (n-1); return (x : xs)` — fine. But `do x <- mx; xs <- applyNTimes mx mf (n-1); return (x : mf x : xs)` produces `n+1` values but the actions ran `2n+1` times. The marker counts side effects.
- **Forgetting `return [x]` vs `return x`**: base case has to wrap in a list because the type promises `m [a]`.
- **`pure (x:xs)` outside the `do`**: `xs` is bound inside the do; you must `return (x:xs)` inside it, after the `<-`.
- **Off-by-one in `n`**: the spec says "n+1 values total" — your base case sets the count. If `n=0` returns `[]` you're off by one.

## Combines-with deep dive

### A03 × A01 — `mapM` on a tree
```haskell
mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)
mapMTree _ Empty        = return Empty
mapMTree f (Fork x l r) = do x' <- f x
                             l' <- mapMTree f l
                             r' <- mapMTree f r
                             return (Fork x' l' r')
```

### A03 × A06 — `Monad m => sequenceM` on a custom container
```haskell
sequenceRose :: Monad m => Rose (m a) -> m (Rose a)
sequenceRose (Leaf m)     = Leaf <$> m
sequenceRose (Branch xs)  = Branch <$> mapM sequenceRose xs
```

### A03 × A08 — eval polymorphic in error / state monad
```haskell
evalM :: Monad m => (String -> m Int) -> Expr -> m Int
evalM env (Var x)   = env x
evalM env (Add a b) = do x <- evalM env a
                         y <- evalM env b
                         return (x + y)
```

## See also

**Combines with:** [A01 tree recursion](./A01-tree-recursion.md) · [A24 applicative instance](./A24-applicative-instance.md)
**Question families:** [monad-combinator](../question-families/monad-combinator-family.md) · [applicative-monad-instance](../question-families/applicative-monad-instance-family.md)
**Cross-topic:** [tree × generic monad](../cross-matrix/tree-x-generic-monad.md) · [list × monad](../cross-matrix/list-x-monad.md)
**Theory:** [Monad typeclass](../typeclasses/monad.md) · [generic combinators](../monads/generic-combinators.md)
**Pitfalls:** [P-007 applyNTimes 0 returns [] not [x]](../pitfalls/HIGH-severity.md#p-007)
**QuickCheck:** [monad attacks](../quickcheck/monad-attacks.md)
**Mock-Q:** [Mock Q2 applyNTimes](../indexes/MOCK-Q-INDEX.md#mock-q2)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
