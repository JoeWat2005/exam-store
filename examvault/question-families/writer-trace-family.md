<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: writer-trace**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · **writer-trace**
<!-- siblings:end -->






# Family: writer-trace

**Archetype:** A12 (Writer monad — log accumulation)   |   **Stars:** ⭐⭐⭐   |   **Course week(s):** 10
**Search keywords:** Writer, tell, logFactorial, countSteps, Sum, [String], trace, WriterT, audit log

## Generator template
```haskell
import Control.Monad.Writer

-- The seed: an action that produces a result while accumulating a log.
-- The log type is a Monoid (often [String], or Sum Int for counters).
seed :: Writer LogType ResultType
seed = do
  tell logEntry
  -- ... more computations ...
  return result
```

Two common log types:
- **`[String]`** — natural for human-readable traces. For counters, log one entry
  per event into `[String]` (or `[()]`) and take `length` — **whitelist-safe**.
- **`Sum Int`** — convenient for counters (`tell (Sum 1)`), **but it lives in
  `Data.Monoid`, which is NOT whitelisted and is NOT re-exported by
  `Control.Monad.Writer` → scores 0.** Use it only if the question's own Types
  module provides `Sum`; otherwise use the `[String]`/`[()]` + `length` approach,
  carry an `Int` via `Control.Monad.State`, or a local `newtype` with a
  hand-written `Monoid` (legal under `-XSafe`, no import).

## Mutations (the examiner picks one)

### Mutation 1 — logFactorial (= problem 107)
**Spec:** Compute factorial; for each step `k`, `tell ["multiplying by " ++ show k]`.
**Sig:** `logFactorial :: Int -> Writer [String] Int`
**Solution:**
```haskell
import Control.Monad.Writer

logFactorial :: Int -> Writer [String] Int
logFactorial 0 = do tell ["base case: 0! = 1"]
                    return 1
logFactorial n = do tell ["multiplying by " ++ show n]
                    k <- logFactorial (n - 1)
                    return (n * k)
```
**QC trap:** Log is accumulated in the order `tell` is called. Recursion-first or tell-first affects log order. `execWriter (logFactorial 3)` should give a list of three messages.

### Mutation 2 — countSteps (Collatz) (= problem 108)
**Spec:** Compute Collatz length; log one entry per step. Return the count via the log length.
**Sig (whitelist-safe):** `countSteps :: Int -> Writer [String] Int`
**Solution (primary — only `Control.Monad.Writer`):**
```haskell
countSteps :: Int -> Writer [String] Int
countSteps 1 = return 1
countSteps n
  | even n    = do tell ["step"]; countSteps (n `div` 2)
  | otherwise = do tell ["step"]; countSteps (3*n + 1)
-- length (execWriter (countSteps 27)) == 111
```
> **`Sum` variant scores 0 unless Types provides it** — `import Data.Monoid (Sum(..))`
> is not whitelisted:
> ```haskell
> import Data.Monoid (Sum(..))   -- NOT an allowed import on its own
> countStepsSum :: Int -> Writer (Sum Int) Int
> countStepsSum 1 = return 1
> countStepsSum n
>   | even n    = do tell (Sum 1); countStepsSum (n `div` 2)
>   | otherwise = do tell (Sum 1); countStepsSum (3*n + 1)
> ```
**QC trap:** With the safe version, count = `length . execWriter . countSteps`
(the final 1 isn't `tell`'d). With the `Sum` variant it would be
`getSum . execWriter . countStepsSum`.

### Mutation 3 — traceEval (log every Expr evaluation step)
**Spec:** Evaluate Expr; tell a string for each sub-evaluation.
**Sig:** `traceEval :: Expr -> Writer [String] Int`
**Solution:**
```haskell
data Expr = Val Int | Add Expr Expr | Mul Expr Expr

traceEval :: Expr -> Writer [String] Int
traceEval (Val n)   = do tell ["Val " ++ show n]
                         return n
traceEval (Add a b) = do tell ["Add"]
                         x <- traceEval a
                         y <- traceEval b
                         tell ["= " ++ show (x + y)]
                         return (x + y)
traceEval (Mul a b) = do tell ["Mul"]
                         x <- traceEval a
                         y <- traceEval b
                         tell ["= " ++ show (x * y)]
                         return (x * y)
```
**QC trap:** The trace shows pre-order tells (enter the node) and post-order tells (after recursion). Picking which depends on spec.

### Mutation 4 — audit (log only branches that match a predicate)
**Spec:** Walk a BT; tell every value satisfying p.
**Sig:** `auditBT :: (a -> Bool) -> BT a -> Writer [a] ()`
**Solution:**
```haskell
auditBT :: (a -> Bool) -> BT a -> Writer [a] ()
auditBT _ Empty        = return ()
auditBT p (Fork v l r) = do
  when (p v) (tell [v])
  auditBT p l
  auditBT p r
```
**QC trap:** Need `import Control.Monad (when)`. `execWriter (auditBT p t)` gives the matched values in pre-order.

### Mutation 5 — numbered log (counter + log)
**Spec:** Maintain a fresh counter while logging — each entry gets a unique number.
**Sig:** `numberedTrace :: [String] -> Writer [(Int, String)] ()`
**Solution:**
```haskell
import Control.Monad.State
import Control.Monad.Writer

numberedTrace :: [String] -> StateT Int (Writer [(Int, String)]) ()
numberedTrace []     = return ()
numberedTrace (s:ss) = do
  i <- get
  lift (tell [(i, s)])
  put (i + 1)
  numberedTrace ss
```
**QC trap:** Needs monad transformers (StateT over Writer). The imports shown
(`Control.Monad.State`, `Control.Monad.Writer`) ARE whitelisted and re-export
`StateT`/`lift`, so this compiles. **But do NOT switch to `Control.Monad.Trans.State`
or `Control.Monad.Trans.Writer`** (the `transformers` package) — those are **NOT
whitelisted and score 0** even though they expose the same names. If transformers
are forbidden by the spec, fold the counter manually via accumulating state in a
`(Int, [(Int,String)])` Writer.

### Mutation 6 — concurrentWriter (two streams of logs)
**Spec:** Two interleaved actions; logs should reflect the order they ran.
**Solution:**
```haskell
twoStreams :: Writer [String] ()
twoStreams = do
  tell ["a-1"]; tell ["a-2"]
  tell ["b-1"]; tell ["b-2"]
```
**QC trap:** No actual concurrency — `tell` is strictly sequential. The "concurrent" is conceptual; useful for explaining what Writer does NOT do.

### Mutation 7 — WriterT over Maybe (the log is DISCARDED on `Nothing`)
**Spec (corrected):** Layer Writer over Maybe with `WriterT [String] Maybe`.
**`WriterT [String] Maybe` DISCARDS the log on `Nothing`** — when the inner
`Maybe` short-circuits, the accumulated `tell`s are thrown away with it. **To
RETAIN the log on failure you must flip the stack to `MaybeT (Writer [String])`**
(Writer on the *outside*), so the `Writer` keeps running and the failure is just a
`Nothing` *result* alongside the full log.

**Sig:** `logDiv :: Int -> Int -> WriterT [String] Maybe Int`

> **WARNING — `Control.Monad.Trans.Writer` / `Control.Monad.Trans.Maybe` are NOT
> whitelisted.** Those belong to the `transformers` package; importing them scores
> **0**. The whitelisted `Control.Monad.Writer` (mtl) already re-exports `WriterT`,
> `runWriterT`, `tell`, and `lift`, so import THAT. There is **no whitelisted source
> for `MaybeT`** (it is "Not in scope" from every allowed import) — so the
> log-retaining `MaybeT (Writer [String])` variant is shown for understanding only
> and is **not exam-legal** unless the question's own Types module provides `MaybeT`.

**Solution (whitelist-safe import; log discarded on failure):**
```haskell
import Control.Monad.Writer   -- mtl; re-exports WriterT, runWriterT, tell, lift

logDiv :: Int -> Int -> WriterT [String] Maybe Int
logDiv n 0 = do tell ["divide by zero attempted: " ++ show n ++ " / 0"]
                lift Nothing
logDiv n d = do tell ["computing " ++ show n ++ " / " ++ show d]
                return (n `div` d)
-- runWriterT (logDiv 6 0) == Nothing          -- log LOST with the Nothing
-- runWriterT (logDiv 6 2) == Just (3, ["computing 6 / 2"])
```

**Log-retaining contrast (NOT whitelisted — concept only):**
```haskell
-- import Control.Monad.Trans.Maybe   -- NOT whitelisted (transformers)
-- import Control.Monad.Writer        -- whitelisted
-- logDiv' :: Int -> Int -> MaybeT (Writer [String]) Int
-- logDiv' n 0 = do lift (tell ["divide by zero attempted: " ++ show n]); MaybeT (return Nothing)
-- logDiv' n d = do lift (tell ["computing " ++ show n ++ " / " ++ show d]); return (n `div` d)
-- runWriter (runMaybeT (logDiv' 6 0)) == (Nothing, ["divide by zero attempted: 6"])  -- log KEPT
```

**QC trap:** The marker can check both: with `WriterT [String] Maybe`, a `Nothing`
gives `runWriterT ... == Nothing` (no log at all); only `MaybeT (Writer [String])`
yields `(Nothing, [..full log..])`. Picking the wrong stack order = wrong answer.

### Mutation 8 — logFib (log the calls during recursive fib)
**Spec:** Compute fib n while logging "fib k" for each call.
**Sig:** `logFib :: Int -> Writer [String] Integer`
**Solution:**
```haskell
logFib :: Int -> Writer [String] Integer
logFib 0 = do tell ["fib 0"]; return 0
logFib 1 = do tell ["fib 1"]; return 1
logFib n = do tell ["fib " ++ show n]
              a <- logFib (n - 1)
              b <- logFib (n - 2)
              return (a + b)
```
**QC trap:** Demonstrates the exponential call count of naïve fib via the log size.

### Mutation 9 — letBindingLog (log every let-binding made during eval)
**Spec:** Combine env-eval with Writer.
**Sig:** `evalWithLog :: Env -> Expr -> Writer [String] (Maybe Int)`
**Solution:**
```haskell
evalWithLog :: Env -> Expr -> Writer [String] (Maybe Int)
evalWithLog _   (Lit n)       = do tell ["lit " ++ show n]; return (Just n)
evalWithLog env (Var x)       = do tell ["lookup " ++ x]; return (lookup x env)
evalWithLog env (Add a b)     = do
  m1 <- evalWithLog env a
  m2 <- evalWithLog env b
  return ((+) <$> m1 <*> m2)
evalWithLog env (Let x e1 e2) = do
  m1 <- evalWithLog env e1
  case m1 of
    Just v  -> do tell ["bind " ++ x ++ " = " ++ show v]
                  evalWithLog ((x,v) : env) e2
    Nothing -> return Nothing
```
**QC trap:** Returning `Maybe` *inside* the Writer is a different pattern than WriterT (mutation 7). Both work; this one always returns *some* value, just possibly Nothing.

### Mutation 10 — log replay
**Spec:** Given a list of log entries, replay each tell.
**Sig:** `replay :: [LogEntry] -> Writer [LogEntry] ()`
**Solution:**
```haskell
replay :: [String] -> Writer [String] ()
replay = mapM_ (\s -> tell [s])
```
Or: `replay xs = tell xs` — works because [String] is a monoid.
**QC trap:** The one-liner `tell xs` produces the same log as the mapM_ version, but the latter splits into individual `tell` calls. They're observationally identical.

## Hidden-predicate mutations
- "Log only if value matches predicate" → `when (p v) (tell [...])` (see mutation 4).
- "Log only the last `n` entries" → use a *bounded* log type (e.g. `BoundedList`).

## Accumulator-style alternative
You can fake Writer with a pure pair-returning function:
```haskell
logFactorialPure :: Int -> ([String], Int)
logFactorialPure 0 = (["base"], 1)
logFactorialPure n = let (log, k) = logFactorialPure (n - 1)
                     in  (("step " ++ show n) : log, n * k)
```
This is exactly what Writer does under the hood.

## Fold-style alternative
For accumulating a log over a list, `foldM` with a writer:
```haskell
foldWithLog :: (b -> a -> Writer [String] b) -> b -> [a] -> Writer [String] b
foldWithLog = foldM
```
This is just `foldM` specialised to Writer.

## Cross-family combinations
- this family + `state-game-family.md`: State + Writer for game with audit log.
- this family + `env-eval-family.md`: Mutation 9 above.
- this family + `monad-combinator-family.md`: mapM_ with tell.
- this family + `error-handling-family.md`: WriterT over Maybe / MaybeT over Writer.

## QuickCheck universal attacks
- **`execWriter (return x) == mempty`** — pure value, no log.
- **`tell w1 >> tell w2 ≡ tell (w1 <> w2)`** — tell monoid.
- **`length (execWriter (logFactorial n)) == n`** — count log entries.
- **`fst (runWriter (logFactorial n)) == factorial n`** — result correctness.
- **`length (execWriter (countSteps n))` is Collatz length(n)** — log + correctness (whitelist-safe `countSteps`; with the `Sum` variant it would be `getSum (execWriter ...)`).

## Pitfalls (per mutation)
- M1: putting `tell` after `return` (the log entry for the current step is missed).
- M2: using `Sum` at all — it needs the non-whitelisted `Data.Monoid` (scores 0). Count via `length` of a `[String]`/`[()]` log instead; only use `Sum` if Types provides it (then don't forget the `getSum` wrap/unwrap).
- M3: choosing wrong tell location (pre-order vs post-order).
- M4: forgetting `when` import.
- M5: getting confused which monad layer is "outer".
- M6: thinking Writer means concurrency.
- M7: log lost on Nothing vs preserved.
- M8: exponential blowup in log size.
- M9: returning `Maybe Int` instead of `Writer [String] Int`.
- M10: thinking the two forms are observably different.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — foldWithTrace (fold over a list with each step logged)

**Spec:** Fold a binary operation over a list, logging each step's accumulator update.

**Type sig:** `foldWithTrace :: Show a => (a -> a -> a) -> a -> [a] -> Writer [String] a`

```haskell
foldWithTrace :: Show a => (a -> a -> a) -> a -> [a] -> Writer [String] a
foldWithTrace _ z []     = do
  tell ["start: " ++ show z]
  return z
foldWithTrace f z (x:xs) = do
  tell ["step: combining " ++ show z ++ " and " ++ show x]
  let z' = f z x
  tell ["  -> " ++ show z']
  foldWithTrace f z' xs
```

**What changes vs seed:** Effect stack: pure `foldl` becomes monadic Writer-traced. Each step contributes 2 log entries — structural change to the algorithm's logging frequency.

**QC trap:** Order of `tell` calls matters: `[step-message, result-message]` is in the order shown above. Swapping gives a confusing log. Property: number of tell entries = 2 * length + 1.

## See also

**Primary archetype:** [A15 writer trace](../archetypes/A15-writer-trace.md)
**Cross-topic:** [rose × writer](../cross-matrix/rose-x-writer.md) · [tree × writer](../cross-matrix/tree-x-writer.md) · [bst × writer](../cross-matrix/bst-x-writer.md) · [list × writer](../cross-matrix/list-x-writer.md)
**Theory:** [writer](../monads/writer.md)
**QuickCheck:** [writer attacks](../quickcheck/writer-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
