<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A14 — Multi-Effect Interpreter (State + Error)**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · **A14** · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A14 — Multi-Effect Interpreter (State + Error)

**Tier:** 2   |   **Stars:** ⭐⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** none direct (Free over `FSum` in A3 is conceptually similar)
**Combines with:** A02 · A05 · A08 · A19
**Search keywords:** StateT · ExceptT · throwError · catchError · do-notation · multiple effects · `MonadState` · `MonadError` · runStateT

## What it tests
Whether you can combine TWO effects (mutable state + failure / error) in a single computation, using either monad transformers (`StateT Int (Either String) a`) or mtl-style class constraints (`(MonadState Int m, MonadError String m) => m ()`).

## Recognition triggers
- TWO effects are needed at once: "read the state AND fail on division by zero"
- A `Cmd` ADT includes `Div`, `Load`, `Store` AND `Throw`
- Type signature shape: `Cmd -> StateT s (Either e) ()` or `(MonadState s m, MonadError e m) => Cmd -> m ()`
- Question imports `Control.Monad.State` AND `Control.Monad.Except`
- Worked example shows a chain of `modify`/`get` interleaved with `throwError`/`catchError`

> **WARNING - not an allowed import:** `Control.Monad.Except` (for `ExceptT`, `throwError`, `catchError`, `MonadError`) is **NOT** on the exam whitelist — importing it scores **0**. The whitelist has `Control.Monad.State` but **no** error/except module. So the primary template below is **hand-rolled** out of `State`-into-`Either` by hand, using only Prelude + (optionally) `Control.Monad.State`. Only use the `StateT … (Either …)` / `ExceptT` form if the question's own Types module hands you that stack.

## Canonical template (hand-rolled, allowed imports only)
Model "state that can fail" as a function `Stack -> Either String (a, Stack)`. No transformers, no `throwError` — failure is just `Left`, success is `Right`. This needs **zero** imports.
```haskell
type Stack  = [Int]
type EvalM a = Stack -> Either String (a, Stack)

-- sequencing by hand (this is exactly StateT Stack (Either String) >>=, written out)
retE :: a -> EvalM a
retE x = \s -> Right (x, s)

bindE :: EvalM a -> (a -> EvalM b) -> EvalM b
bindE m f = \s -> case m s of
                    Left e        -> Left e
                    Right (a, s') -> f a s'

throw :: String -> EvalM a       -- failure: ignore the state, return Left
throw e = \_ -> Left e

push :: Int -> EvalM ()
push n = \s -> Right ((), n : s)

pop :: EvalM Int
pop = \s -> case s of
              []     -> Left "stack underflow"
              (x:xs) -> Right (x, xs)

binop :: (Int -> Int -> Int) -> EvalM ()
binop op = pop `bindE` \y ->
           pop `bindE` \x ->
           push (op x y)

safeDiv :: EvalM ()
safeDiv = pop `bindE` \y ->
          pop `bindE` \x ->
          if y == 0 then throw "/0"        -- NOT bare `Left "/0"` — EvalM is a function, so you need `\_ -> Left "/0"`
                    else push (x `div` y)
```
`runEvalM m s = m s` returns `Either String (a, Stack)`: `Left "…"` on error (state discarded), `Right (result, finalStack)` on success.

### If-allowed aside — `StateT s (Either e)` + `throwError` (ONLY if the Types module supplies it)
> Forbidden under the standard whitelist (`Control.Monad.Except` scores 0). Shown only because some hand-out Types modules re-export it.
```haskell
import Control.Monad.State          -- whitelisted
import Control.Monad.Except         -- WARNING: NOT whitelisted — scores 0 unless provided

type EvalM' = StateT Stack (Either String)

pop' :: EvalM' Int
pop' = do s <- get
          case s of
            []     -> throwError "stack underflow"
            (x:xs) -> put xs >> return x

safeDiv' :: EvalM' ()
safeDiv' = do y <- pop'; x <- pop'
              if y == 0 then throwError "/0" else modify (\st -> (x `div` y) : st)
```

## Mutations (the examiner picks one)

### M1 — Stack calculator with `/0` error
See canonical template — this IS canonical.

### M2 — Eval expression in State + Error
```haskell
evalSE :: Expr -> StateT Env (Either String) Int
evalSE (Lit n)     = pure n
evalSE (Var x)     = do env <- get
                        maybe (throwError ("unbound " ++ x)) pure (lookup x env)
evalSE (Add a b)   = (+) <$> evalSE a <*> evalSE b
evalSE (Div a b)   = do x <- evalSE a; y <- evalSE b
                        if y == 0 then throwError "/0" else pure (x `div` y)
evalSE (Let x e b) = do v <- evalSE e; modify ((x, v) :); evalSE b
```
What changes: AST-style; combines A08 with multi-effect.

### M3 — Imperative `Cmd` with mutable Env
```haskell
data Cmd = Set String Expr | Seq Cmd Cmd | If Expr Cmd Cmd | While Expr Cmd | Throw String

run :: Cmd -> StateT Env (Either String) ()
run (Set x e)     = do v <- evalSE e; modify ((x, v) :)
run (Seq c1 c2)   = run c1 >> run c2
run (If c t e)    = do v <- evalSE c
                       if v /= 0 then run t else run e
run (While c b)   = do v <- evalSE c
                       when (v /= 0) (run b >> run (While c b))
run (Throw msg)   = throwError msg
```
What changes: `Cmd`-level effects; `evalSE` is the expression-level sub-eval (M2).

### M4 — mtl-style with class constraints
```haskell
divM :: (MonadState Int m, MonadError String m) => Int -> m ()
divM 0 = throwError "/0"
divM n = modify (`div` n)
```
What changes: polymorphic over any monad with both effects; works with `StateT s (Either e)` or any compatible transformer stack.

### M5 — Concrete `StateT s (Either e)` (no mtl)
```haskell
modifyS :: (s -> s) -> StateT s (Either e) ()
modifyS f = StateT (\s -> Right ((), f s))

throw :: e -> StateT s (Either e) a
throw e = StateT (\_ -> Left e)
```
What changes: hand-rolled — useful when imports are forbidden in the exam.

### M6 — `Writer + State` (logged calculator)
```haskell
type LogCalc = WriterT [String] (State Int)

setS :: Int -> LogCalc ()
setS n = do put n; tell ["set " ++ show n]

addS :: Int -> LogCalc ()
addS n = do modify (+ n); tell ["+" ++ show n]
```
What changes: trace + state, no error; logs every action.

### M7 — `IO + State` (read inputs)
```haskell
type IOSt = StateT Int IO

readAndAdd :: IOSt ()
readAndAdd = do liftIO (putStr "n? ")
                n <- liftIO readLn
                modify (+ n)
```
What changes: `liftIO` to perform `IO` inside a state-augmented monad.

### M8 — Three effects: State + Error + Writer
```haskell
type FullM = StateT Stack (ExceptT String (Writer [String]))

logStep :: String -> FullM ()
logStep s = lift (lift (tell [s]))   -- two lifts to skip State & Except layers
```
What changes: nested transformers; need to track lift levels.

### M9 — `Maybe` instead of `Either`
```haskell
divMaybe :: Int -> StateT Int Maybe ()
divMaybe 0 = StateT (\_ -> Nothing)
divMaybe n = modify (`div` n)
```
What changes: error is just `Nothing`; no message.

### M10 — Catch + recover
```haskell
trySafe :: Cmd -> StateT Env (Either String) ()
trySafe c = run c `catchError` (\_ -> return ())  -- swallow errors silently
```
What changes: `catchError` to recover; ignores all errors.

## Worked examples from this course
- Practice file `ewan31-40.hs`: `evalCalc`, `runCalc` with `MonadError` constraint.
- Week 9 lecture: introduces multi-effect interpreters.
- Assignment 3: `FreeState s a` over `FSum (State s) Yield`/`Sleep` — same idea (combine two effects via the Free + FSum construction) but presented through Free monad.

## QuickCheck attack surface
- **`runStateT` on success**: `runStateT (push 1 >> push 2 >> safeDiv) [] == Left "stack underflow"` (because we popped from empty).
- **`runStateT` on failure**: `runStateT safeDiv [10, 0] == Left "/0"`.
- **State after partial execution**: does state revert on error? In `StateT s (Either e)`, the state at the point of `throwError` is discarded. In `ExceptT e (State s)`, it's preserved. Marker may test this.
- **Catch and continue**: `catchError throwError (\_ -> push 99)` should leave 99 on the stack.
- **Order of effects matters**: `StateT s (ExceptT e (Identity)) a` ≠ `ExceptT e (State s) a` — different semantics for error + state.

## Pitfalls (marks-killers)
- **Wrong transformer order**: `StateT s (Either e) a` is the typical exam answer. The state-error interplay differs from `ExceptT e (State s) a`.
- **Forgetting `lift`**: inside `StateT s (Either e)`, calling `Left "err"` directly type-errors. Use `throwError` or `lift (Left …)`.
- **`return ()` vs `pure ()`**: equivalent; the marker accepts either.
- **`get` and `put` ambiguous**: with mtl + multiple State layers, you need to specify which layer (use `lift get`, `lift (lift get)`).
- **No imports allowed**: if the exam disallows `Control.Monad.Except`, hand-roll `StateT s (Either e)` (M5).
- **Forgetting `modify` clamp**: like A02, must clamp where applicable (`max 0`).

## Combines-with deep dive

### A14 × A02 — pure state vs state+error
Start with A02's pure `State` calculator; upgrade `Div` to use `Either`. Same shape, extra effect.

### A14 × A08 — eval that can fail
M2 / M3 show how `eval :: Env -> Expr -> Maybe Int` extends to `evalSE :: Expr -> StateT Env (Either String) Int`.

### A14 × A19 — extending an interpreter with try/catch
Adding `Try cmd handler` to an existing interpreter:
1. AST: `data Cmd = … | Try Cmd Cmd`
2. Parser: `try …  catch …  end`
3. Eval: `run (Try c h) = run c `catchError` \_ -> run h`

## See also

**Combines with:** [A08 env eval](./A08-env-eval.md) · [A19 extend interpreter](./A19-extend-interpreter.md) · [A15 writer trace](./A15-writer-trace.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md) · [writer-trace](../question-families/writer-trace-family.md)
**Cross-topic:** [expr × multi](../cross-matrix/expr-x-multi.md)
**Theory:** [multi-effect interpreter](../interpreters/expr-multi-effect.md) · [multi-effect monad](../monads/multi-effect.md) · [transformer stack order](../monads/transformer-stack-order.md) · [transformers](../monads/transformers.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
