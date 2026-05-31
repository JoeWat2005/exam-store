<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: Writer monad**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · **writer**
<!-- siblings:end -->






# QuickCheck attacks: Writer monad

**Search keywords:** Writer, tell, runWriter, execWriter, mappend, monoid log, [Int] log, order of tell, Mock Q2 Writer, Assignment 3 trace log

Mock Q2 uses Writer. Assignment 3 Q2 (trace) effectively combines Writer-into-State (state with a log).

> **WARNING — not an allowed import:** the templates on this page deliberately use `Writer [Int]`/`Writer [String]` logs, which need only `Control.Monad.Writer`. If a question tempts you toward a numeric/boolean monoid, note that `Sum`/`Product`/`Any`/`All` are in `Data.Monoid` (and `Max`/`Min` in `Data.Semigroup`), which are NOT on the exam whitelist and are NOT re-exported by `Control.Monad.Writer` (`import Control.Monad.Writer` alone gives 'Not in scope: Sum'). To count/total with only allowed imports, use a `Writer [()]`/`Writer [String]` log + `length`, carry an `Int` via `Control.Monad.State`, or define a local `newtype` with a hand-written `Monoid`. Use the `Sum` form only if the question's own `Types` module provides it.

## What the marker generates

Mock Q2:
```haskell
newtype Q2Wrapper = Wrap (Writer [Int] Int)

genWriter = do
  n <- chooseInt (0, 15)
  pure $ Wrap $ do { tell [n] ; pure n }
```

So the marker's "starter" computation `mx` writes `[n]` to the log and returns `n`. The marker can compose these and check that your log is correct.

`q2_mf` writes `2 * current` to the log:
```haskell
q2_mf n = do tell [2 * n]; pure (n + 1)
```

So a sequence `mx >> mf >> mf` should log `[n, 2n, 2(n+1)] = [n, 2n, 2n+2]` and return `n+2`.

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | `tell []` | does nothing to log | If you "skip" tell when log is empty, that's still fine; identity append | OK to omit `tell []` — it's a no-op |
| 2 | `tell [x]` | appends `[x]` | Most common — straightforward | `tell [computedValue]` |
| 3 | Multiple `tell` in sequence | `do tell [1]; tell [2]; tell [3]` → log `[1,2,3]` | Order matters! Earlier `tell` = earlier in log | Effects are sequenced by `>>` / `do` |
| 4 | `tell` AFTER `pure` | `do x <- pure 5; tell [x]` | log `[5]`, value `()` ... wait Wirter result is whatever last is | The last `pure x` gives the value; tells along the way build log |
| 5 | `tell` BEFORE recursive call | log of inner call comes after | If you tell first then recurse, your tell is earlier in log | Choose carefully — for "tells in chronological order", tell first then recurse; for "tells in reverse order", do the opposite |
| 6 | `runWriter` returns `(value, log)` | needed for testing | confusing `runWriter` with `execWriter` (log only) | `runWriter (do tell [1]; pure 42) == (42, [1])` |
| 7 | `execWriter` returns just log | for "what was logged?" | If you use `runWriter` when you want just log, you have to discard `fst` | `execWriter m == snd (runWriter m)` |
| 8 | Empty computation | `pure x :: Writer [Int] Int` | log is `[]`. | `runWriter (pure 5 :: Writer [Int] Int) == (5, [])` |
| 9 | Log is a monoid | `[]` is identity for `++` | If you accidentally use `Set`, the order is lost | Writer over `[a]` preserves order; over `Set` does not |
| 10 | Polymorphic Writer | `Writer w a` for any `Monoid w` | Functions assuming `[Int]` won't generalise | Use `tell` (Monoid-polymorphic) not `mappend` |
| 11 | Mock Q2 partial credit: permutation match | "all values present but order may differ" | If you log in reverse, you get 6 marks via permutation but lose 4 marks via exact-match | Order matters for full marks |

## Property templates

```haskell
import Test.QuickCheck
import Control.Monad.Writer

-- pure has empty log
prop_pure_emptyLog :: Int -> Bool
prop_pure_emptyLog x = execWriter (pure x :: Writer [Int] Int) == []

-- tell builds log
prop_tell_logBuild :: [Int] -> Bool
prop_tell_logBuild xs =
  execWriter (mapM_ (\x -> tell [x]) xs :: Writer [Int] ())
  == xs

-- Sequential tells concatenate
prop_tellSeq :: Int -> Int -> Bool
prop_tellSeq a b = execWriter (do tell [a]; tell [b]) == [a, b]

-- Tell-then-bind: log preserved
prop_tellThenBind :: Int -> Bool
prop_tellThenBind n =
  let (v, w) = runWriter (do tell [n]; pure (n + 1))
  in  v == n + 1 && w == [n]

-- Bind-then-tell: log built in order
prop_bindThenTell :: Int -> Bool
prop_bindThenTell n =
  let (v, w) = runWriter (do { x <- pure n; tell [x]; pure (x + 1) })
  in  v == n + 1 && w == [n]
```

## Self-test before submission checklist

- [ ] `runWriter (pure x)` returns `(x, mempty)` (empty log)
- [ ] `tell` appends to the log in the **current order**, not reverse
- [ ] When recursing: did you tell BEFORE or AFTER the recursive call? Check the spec
- [ ] `runWriter` for `(value, log)`, `execWriter` for log only, `evalWriter` doesn't exist but `fst . runWriter` does
- [ ] Used `tell [x]` (single-element list), not `tell x` (which won't even typecheck for `Writer [Int] _`)
- [ ] Function is polymorphic over `Writer` (uses only `tell` and bind) — not `Writer [Int]` baked in unless spec says so

## Pitfalls that specifically lose QC marks

### Pitfall: log built in wrong order
```haskell
-- WRONG: recursive call FIRST, then tell — log has root at the END
logTree (Leaf x)    = tell [x]
logTree (Branch xs) = do
    mapM_ logTree xs
    tell [length xs]    -- ← logged after children
-- vs:
logTree' (Branch xs) = do
    tell [length xs]    -- ← logged before children
    mapM_ logTree' xs
-- Different log order. Pick the right one based on what the spec says
-- (e.g. "log in pre-order traversal").
```

### Pitfall: `tell x` instead of `tell [x]`
```haskell
-- WRONG (assuming Writer [Int]):
tell 5    -- type error: expected [Int], got Int
-- Fix:
tell [5]
```

### Pitfall: assuming Writer log is a Set
```haskell
-- Writer over [Int] PRESERVES DUPLICATES and ORDER:
runWriter (do tell [1]; tell [1]; tell [2]) == ((), [1, 1, 2])
-- If you want deduplication, do it AFTER runWriter, not during.
```

### Pitfall: using `tell` in a polymorphic `Monad m` function
```haskell
-- WRONG: only Writer has tell
foo :: Monad m => m a -> m a
foo mx = do tell ["called"]; mx    -- type error
-- Fix: this function shouldn't use tell. If it needs to, change signature:
foo :: (MonadWriter [String] m) => m a -> m a
```

### Pitfall: forgot to consume the Writer
```haskell
-- WRONG (in ghci):
ghci> do { tell [1]; pure 5 } :: Writer [Int] Int
<interactive>:1:1: No instance for (Show (Writer [Int] Int))
-- Fix: run it
ghci> runWriter (do { tell [1]; pure 5 } :: Writer [Int] Int)
(5, [1])
```

### Pitfall: in Mock Q2, recursive case order
The marker's expected recursive case is:
```haskell
applyNTimes mx mf n = do
    xs <- applyNTimes mx mf (n - 1)
    x  <- mf (last xs)
    pure (xs ++ [x])
```

- `applyNTimes mx mf (n-1)` runs and accumulates log `L_{n-1}`.
- `mf (last xs)` runs and tells `[2 * last xs]`.
- So final log is `L_{n-1} ++ [2 * last xs]`.

If you do it the other way around:
```haskell
applyNTimes mx mf n = do
    x  <- mf (?)                      -- can't — no prior x
    xs <- applyNTimes mx mf (n - 1)
    pure (x : xs)
```
You can't, because `mf` needs a value. But suppose you split it differently:
```haskell
applyNTimes mx mf n = do
    xs <- applyNTimes mx mf (n - 1)
    let prev = last xs
    x  <- mf prev
    pure (xs ++ [x])
-- This is the same — fine.
```

### Pitfall: `mapM_` vs `mapM`
```haskell
-- mapM  : (a -> m b) -> [a] -> m [b]   -- collects results
-- mapM_ : (a -> m b) -> [a] -> m ()    -- discards results

-- For tell-only loops:
mapM_ (\x -> tell [x]) xs       -- you don't need the results

-- For accumulating:
ys <- mapM (\x -> tell [x] >> pure (f x)) xs   -- you want the [f x]
```

## See also

**Archetypes:** [A15 writer trace](../archetypes/A15-writer-trace.md)
**Cross-topic:** [tree × writer](../cross-matrix/tree-x-writer.md) · [rose × writer](../cross-matrix/rose-x-writer.md)
**Question families:** [writer-trace](../question-families/writer-trace-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
