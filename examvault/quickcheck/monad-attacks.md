<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: polymorphic monads (`Monad m =>`)**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · **monad** · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: polymorphic monads (`Monad m =>`)

**Search keywords:** Monad, mapM, applyNTimes, do, pure, return, base case, recursive monad, polymorphic, n=0, empty list, monad-specific primitives, type error, order of effects

Mock Q2 `applyNTimes` is the canonical "polymorphic monad recursion" question. The marker tests with the Writer monad but your function MUST type-check against any `Monad m`.

## What the marker generates

Direct from `MockTestTestCases.hs`:

```haskell
newtype Q2Wrapper = Wrap (Writer [Int] Int)

q2_mf :: Int -> Writer [Int] Int
q2_mf n = do
  tell [2 * n]
  pure (n + 1)

genWriter :: Gen Q2Wrapper
genWriter = do
  n <- chooseInt (0, 15)
  pure $ Wrap $ do { tell [n] ; pure n }
```

So the marker creates a "starter" computation `mx = do { tell [n]; pure n }` and an "advance" function `mf` that writes `2*current` and returns `current+1`. It then calls `applyNTimes mx mf k` for various `k`.

The base case test:
```haskell
prop_applyNTimes_baseCase (Wrap mx) = student ~= solution
 where
  student  = runWriter $ Student.applyNTimes mx q2_mf 0
  solution = runWriter $ (:[]) <$> mx
```

**Critical:** at `n = 0`, the marker expects `[x]` (a one-element list with the starter value), NOT `[]`. This is the most-likely-to-fail base case in the whole exam.

The recursive case test:
```haskell
prop_applyNTimes_recursiveCase (Wrap mx) n =
  let solution = runWriter $ do xs <- Student.applyNTimes mx q2_mf (n - 1)
                                x  <- q2_mf (last xs)
                                pure $ xs ++ [x]
  in  ...
```

So `applyNTimes mx mf n` should return `applyNTimes mx mf (n-1) ++ [mf (last that)]`.

The order-doesn't-matter test:
```haskell
prop_applyNTimes_outOfOrder (Wrap mx) n = p_permOf student solution
```

Some partial credit if you have all the right values but in the wrong order.

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | `n == 0` | `applyNTimes mx mf 0` | Spec is "apply 0 times" — expects `[starter]`, NOT `[]`. Off-by-one base case. | Base case: `applyNTimes mx _ 0 = do x <- mx; pure [x]` (or equivalently `(:[]) <$> mx`) |
| 2 | `n == 1` | `applyNTimes mx mf 1` | Expects `[starter, mf starter]`. If your base case returns `[]`, your recursion gives `[mf undefined]` — type error or wrong | Base case correct + standard recursion `xs <- applyNTimes mx mf (n-1); x <- mf (last xs); pure (xs ++ [x])` |
| 3 | `n == 2` | `applyNTimes mx mf 2` | Same recursive pattern | Same |
| 4 | `n` negative | `applyNTimes mx mf (-3)` | Infinite recursion | Guard: `applyNTimes mx _ n \| n <= 0 = ...` (use `<=`, not `==`) |
| 5 | Polymorphic type | function works for ANY `Monad m` | If your function uses `tell` or `get` directly, type error against pure `Monad` | Use only `>>=`, `>>`, `return`/`pure`, and the supplied `mf` |
| 6 | Order of effects | `Writer` accumulates left-to-right | If you `pure (xs ++ [x])` BEFORE `tell`, the log is empty | The `do`-notation order is the effect order |
| 7 | Strict vs lazy | `last xs` on a never-forced `xs` | Infinite list / not-yet-evaluated | `runWriter` forces the whole computation |
| 8 | `mf` may itself have effects | every `mf` call writes/changes state | Forgetting that `mf x` returns `m a`, not `a` | Always bind: `x <- mf (last xs)` |
| 9 | Tail recursion not required | QC bounds `n` to `chooseInt (1, 10)` | Don't over-engineer | Naive structural recursion is fine |
| 10 | Type signature mismatch | template gives `Monad m =>` constraint | Removing it specialises to Writer only; adding `Eq` etc. is wrong | Copy signature exactly |

## The Mock Q2 canonical solution shape

```haskell
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx _  n | n <= 0 = do
                        x <- mx
                        pure [x]                  -- base case: ONE-element list
applyNTimes mx mf n = do
    xs <- applyNTimes mx mf (n - 1)               -- recurse
    x  <- mf (last xs)                            -- apply mf to most recent
    pure (xs ++ [x])                              -- append
```

Notes:
- `n <= 0` not `n == 0` — defends against negative `n`.
- `do x <- mx; pure [x]` is the base case — this is `(:[]) <$> mx`.
- The recursive case appends at the END, not the beginning.
- The marker also accepts permutations of the output list (partial credit).

## Property templates

```haskell
import Test.QuickCheck
import Control.Monad.Writer

-- Test with the canonical (Writer [Int] Int)
mx :: Writer [Int] Int
mx = do tell [10]; pure 10

mf :: Int -> Writer [Int] Int
mf n = do tell [2 * n]; pure (n + 1)

-- Base case: n = 0 returns [starter]
prop_applyNTimes_zero :: Bool
prop_applyNTimes_zero = runWriter (applyNTimes mx mf 0) == ([10], [10])

-- n = 1: starter then one application
prop_applyNTimes_one :: Bool
prop_applyNTimes_one = runWriter (applyNTimes mx mf 1) == ([10, 11], [10, 20])

-- length is n + 1
prop_applyNTimes_length :: Property
prop_applyNTimes_length = forAll (chooseInt (0, 10)) $ \n ->
  let (xs, _) = runWriter (applyNTimes mx mf n)
  in  length xs == n + 1

-- Each successive element is mf of previous
prop_applyNTimes_chain :: Property
prop_applyNTimes_chain = forAll (chooseInt (1, 10)) $ \n ->
  let (xs, _) = runWriter (applyNTimes mx mf n)
  in  and [xs !! (i+1) == fst (runWriter (mf (xs !! i))) | i <- [0 .. n-1]]
```

## Self-test before submission checklist

- [ ] `applyNTimes mx mf 0` returns the one-element list, not empty
- [ ] `applyNTimes mx mf 1` has length 2 (starter + one application)
- [ ] `applyNTimes mx mf n` has length `n + 1`
- [ ] Uses ONLY `Monad m =>` operations (no `tell`, `get`, `put` baked in)
- [ ] Works in any monad (test in `Maybe`, `[]`, `Writer`, `State`)
- [ ] Base case condition uses `<=` not `==` (defends against negative n)
- [ ] Type signature character-identical to template

## Pitfalls that specifically lose QC marks

### Pitfall: base case returns empty list
```haskell
-- WRONG:
applyNTimes _ _ 0 = pure []
-- For n=0, marker expects [x] not []. Fail base case test (2 marks).
-- Also fails recursive case because last [] = error.
-- Fix:
applyNTimes mx _ 0 = do { x <- mx; pure [x] }
```

### Pitfall: forgot to use `mx` in base case
```haskell
-- WRONG:
applyNTimes mx _ 0 = pure [undefined]  -- ???
-- Wait this won't even typecheck nicely.
-- The starter value comes from mx itself:
applyNTimes mx _ 0 = (:[]) <$> mx     -- runs mx, wraps result in [x]
-- Equivalently:
applyNTimes mx _ 0 = mx >>= \x -> pure [x]
```

### Pitfall: using `tell` inside a polymorphic function
```haskell
-- WRONG: doesn't typecheck for general Monad m
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx mf n | n <= 0 = do
    x <- mx
    tell [x]   -- ← tell is only in Writer, not general Monad
    pure [x]
-- Compiler error: No instance for (MonadWriter [a] m).
-- Fix: use only mx and mf (no monad-specific primitives).
```

### Pitfall: forgetting to bind `mf` result
```haskell
-- WRONG: tries to use mf x as a value, not a computation
applyNTimes mx mf n = do
    xs <- applyNTimes mx mf (n-1)
    pure (xs ++ [mf (last xs)])    -- mf returns m a, not a — type error
-- Fix: bind it
applyNTimes mx mf n = do
    xs <- applyNTimes mx mf (n - 1)
    x  <- mf (last xs)
    pure (xs ++ [x])
```

### Pitfall: appending at the wrong end
```haskell
-- WRONG (reverses order):
applyNTimes mx mf n = do
    x  <- mf (?)                   -- can't even — no prior x
    xs <- applyNTimes mx mf (n-1)
    pure (x : xs)
-- Off-by-one in chain direction.
-- Fix: recurse first, then append at end with ++ [x]
```

### Pitfall: making `n = 1` the base case instead of `n = 0`
```haskell
-- WRONG: shifts indices
applyNTimes mx _  1 = (:[]) <$> mx          -- base at 1
applyNTimes mx mf n = ...                   -- recurse for n > 1
-- For n = 0, falls through to the catch-all which assumes n > 0.
-- Result: pattern fails at applyNTimes mx mf (n-1) for n=1 → recurses to n=0
--          which has no clause → exception.
-- Fix: base case at n <= 0
```

### Pitfall: forgetting `mapM` analogues
For `mapM f []`:
```haskell
-- WRONG: undefined behaviour
mapM f [] = undefined
-- mapM with empty list MUST return pure []
-- Standard library:
mapM _ []     = pure []
mapM f (x:xs) = do
    y <- f x
    ys <- mapM f xs
    pure (y : ys)
```

### Pitfall: order of effects matters in Writer / State combinations
```haskell
-- Writer accumulates left-to-right in do-notation:
do
  tell [1]
  tell [2]
  pure 0   -- log is [1, 2]

-- If you accidentally:
do
  x <- pure 0
  tell [2]
  tell [1]   -- log is [2, 1]

-- Test order-of-effects properties explicitly.
```

### Pitfall: subtle "the marker accepts permutations"
The Mock Q2 marker has TWO tests:
- 4-mark `prop_applyNTimes_correct` — exact match
- 6-mark `prop_applyNTimes_outOfOrder` — permutation match

If your function gets the **values** right but in the **wrong order**, you score 6 marks from the permutation test even though you fail the exact test. So even a partially-wrong solution can get most marks.

## See also

**Archetypes:** [A03 generic monad](../archetypes/A03-generic-monad.md)
**Cross-topic:** [tree × generic-monad](../cross-matrix/tree-x-generic-monad.md) · [list × monad](../cross-matrix/list-x-monad.md)
**Question families:** [monad-combinator](../question-families/monad-combinator-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
