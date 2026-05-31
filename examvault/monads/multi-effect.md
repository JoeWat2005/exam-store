<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Multi-Effect (mtl-style class constraints)**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · [generic-combinators](./generic-combinators.md) · [io](./io.md) · [list-monad](./list-monad.md) · [maybe](./maybe.md) · [monad-laws](./monad-laws.md) · [monaderror](./monaderror.md) · **multi-effect** · [reader](./reader.md) · [state](./state.md) · [transformer-stack-order](./transformer-stack-order.md) · [transformers](./transformers.md) · [writer](./writer.md)
<!-- siblings:end -->






# Multi-Effect (mtl-style class constraints)

When the question needs TWO or more effects (e.g. "state AND error"), the FP-course-idiomatic answer is **stacked class constraints**, not explicit transformers. The function code is identical to the single-effect case — only the type signature changes.

## The pattern

```haskell
f :: (MonadState s m, MonadError e m) => Input -> m Output
f x = do
  s <- get                   -- needs MonadState
  when (bad x) (throwError "X")  -- needs MonadError
  put (update s x)
  pure (result s x)
```

You **don't say which `m`** — the caller picks. Typically the caller monomorphises to:
- `StateT s (Either e) a`  — error wins, state lost on `Left`.
- `ExceptT e (State s) a`  — state kept on `Left`.

## Common combinations

```haskell
(MonadState s m, MonadError e m) => m a    -- calculator with error
(MonadState s m, MonadWriter w m) => m a   -- state + log
(MonadReader r m, MonadError e m) => m a   -- env + may fail
(MonadReader r m, MonadState s m) => m a   -- env + state
```

## When NOT to use multi-effect

- If the question gives one type, just use that concrete one. Don't over-abstract.
- The practice-allowed imports include `Control.Monad.State` and `Control.Monad.Writer` but NOT `Control.Monad.Reader` / `Control.Monad.Except`. If the question expects you to use those classes, the exam paper will tell you so.

## Canonical templates

### Calculator with state + error (Mock-style)
```haskell
import Control.Monad.State
import Control.Monad.Error.Class    -- ONLY if allowed

data Cmd = EnterC | StoreC Int Cmd | AddC Int Cmd | DivC Int Cmd

runCalc :: (MonadState Int m, MonadError String m) => Cmd -> m ()
runCalc EnterC          = pure ()
runCalc (StoreC x next) = do
  put x
  runCalc next
runCalc (AddC   x next) = do
  cur <- get
  put (cur + x)
  runCalc next
runCalc (DivC   x next)
  | x == 0    = throwError "Division by zero"
  | otherwise = do
      cur <- get
      put (cur `div` x)
      runCalc next
```

Monomorphise at the test site:
```haskell
type Stack a = StateT Int (Either String) a   -- if transformers allowed
runProg :: Cmd -> Either String ((), Int)
runProg c = runStateT (runCalc c) 0
```

### Storage-style evaluator (textbook example)
```haskell
type Storage = [(String, Int)]
data Expr = Val Int | Var String | Add Expr Expr | Let String Expr Expr

eval :: (MonadState Storage m, MonadError String m) => Expr -> m Int
eval (Val n)   = pure n
eval (Var x)   = do
  store <- get
  case lookup x store of
    Just v  -> pure v
    Nothing -> throwError ("unbound: " ++ x)
eval (Add a b) = do
  x <- eval a
  y <- eval b
  pure (x + y)
eval (Let x e body) = do
  v <- eval e
  modify ((x, v) :)
  eval body
```

### State + Writer (log every assignment)
```haskell
runCalc :: (MonadState Int m, MonadWriter [String] m) => Cmd -> m ()
runCalc (StoreC x next) = do
  tell ["store " ++ show x]
  put x
  runCalc next
runCalc (AddC x next) = do
  tell ["add " ++ show x]
  modify (+ x)
  runCalc next
runCalc EnterC = pure ()
```

## Order of `runStateT` / `runExceptT` — RESULT TYPE FLIPS

This is the most-easily-missed pitfall.

| Stack | Run order | Result type |
|---|---|---|
| `StateT s (Either e)` | `runStateT calc s0` | `Either e (a, s)` — error eats state |
| `ExceptT e (State s)` | `runState (runExceptT calc) s0` | `(Either e a, s)` — state survives error |

Same effects, opposite outcome on error. Choose by what the question wants you to keep when an exception fires.

## Why polymorphic `m`

- Caller picks the concrete monad → easy to test alternative stacks.
- One body of code services many test interpretations.
- Lets the marker swap `StateT s (Either e)` for `WriterT w (State s)` without you rewriting.

## Pitfalls

- **Imports**: `Control.Monad.Error.Class`, `Control.Monad.Except`, `Control.Monad.Reader` — **none of these are in the practice-allowed-imports**. Confirm with the exam paper before using.
- `throwError` exits — state changes since the last `catchError` ARE lost (or kept, depending on stack order — see table above).
- Mixing `MonadError String m` with `MonadError Int m` in the same constraint set is a TYPE ERROR — there's only one error type per monad.
- The class instances for `Either e` come for free; if you write your own monad and want it to support `throwError`, you need an instance.
- You CAN'T just write `MonadFail` instead of `MonadError String` — different semantics.

## QuickCheck traps

- Auto-marker for `runCalc` checks the *final state* AND the *error message*. Off-by-one in error spelling fails.
- A `DivC 0` test verifies that the state at the moment of error is whatever the stack order dictates — pick the right runner.
- A test that runs `Let x (Val 1) (Add (Var x) (Var x))` verifies that `modify ((x, v) :)` was actually written, not just simulated.

## Worked examples

- `runCalc` (state + error) — mock-style.
- `eval` Storage interpreter — see `../interpreters/multi-effect-eval.md`.

## See also

**Archetypes:** [A14 multi-effect interp](../archetypes/A14-multi-effect-interp.md) · [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Cross-topic:** [expr × multi](../cross-matrix/expr-x-multi.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [writer-trace](../question-families/writer-trace-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)
**Related (monads):** [transformers](./transformers.md) · [transformer stack order](./transformer-stack-order.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
