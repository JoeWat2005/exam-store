<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Monad: MonadError (class)**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · [generic-combinators](./generic-combinators.md) · [io](./io.md) · [list-monad](./list-monad.md) · [maybe](./maybe.md) · [monad-laws](./monad-laws.md) · **monaderror** · [multi-effect](./multi-effect.md) · [reader](./reader.md) · [state](./state.md) · [transformer-stack-order](./transformer-stack-order.md) · [transformers](./transformers.md) · [writer](./writer.md)
<!-- siblings:end -->






# Monad: MonadError (class)

**Import:** `Control.Monad.Except` or `Control.Monad.Error.Class` — **NEITHER is in the practice-allowed-imports list**. So in exam: only use this when the question explicitly says you may, OR fall back to concrete `Either e a`.
**Type:** `class Monad m => MonadError e m where ...`
**Combines with:** State (multi-effect calc), Writer.
**Search keywords:** throwError, catchError, error class, mtl, polymorphic error, throw, except.

## Class definition

```haskell
class Monad m => MonadError e m where
  throwError :: e -> m a
  catchError :: m a -> (e -> m a) -> m a
```

## Canonical instances

| `m` | error semantics |
|---|---|
| `Either e`           | concrete, `Left` = error |
| `ExceptT e m`        | layered with another monad `m` |
| `IO`                 | via `IOError` (not common in this course) |

The exam-relevant instance is `Either e`. If the question is **not** explicitly asking for polymorphism, prefer the concrete `Either e a` and don't import `Control.Monad.Except`.

## When to reach for the class (vs concrete Either)

Use class form when:
- The signature in the problem statement says `MonadError e m =>`.
- You're combining with another effect class (`MonadState s m`) and need polymorphism (see [multi-effect.md](multi-effect.md)).

Otherwise: use `Either String Int` directly — fewer imports, same answer.

## Canonical templates

### Eval with polymorphic error
```haskell
import Control.Monad.Except       -- only if allowed

eval :: MonadError String m => Expr -> m Int
eval (Val n)   = pure n
eval (Add a b) = do x <- eval a; y <- eval b; pure (x + y)
eval (Div a b) = do
  x <- eval a
  y <- eval b
  if y == 0
    then throwError "Division by zero"
    else pure (x `div` y)

-- Monomorphise at the call site:
runEval :: Expr -> Either String Int
runEval = eval
```

### Concrete-Either variant (PREFERRED when allowed-imports are tight)
```haskell
eval :: Expr -> Either String Int
eval (Val n)   = Right n
eval (Add a b) = do x <- eval a; y <- eval b; Right (x + y)
eval (Div a b) = do
  x <- eval a
  y <- eval b
  if y == 0 then Left "Division by zero" else Right (x `div` y)
```
Identical code shape; just `Right`/`Left` instead of `pure`/`throwError`.

### `catchError` for recovery
```haskell
safeEval :: MonadError String m => Expr -> m Int
safeEval e = eval e `catchError` \_ -> pure 0
```

## Run functions

`MonadError` itself has no runner — you run by monomorphising to a concrete instance:
- `eval :: Expr -> Either String Int`  → pattern match the result.
- `eval :: ExceptT String (State s) Int` → `runExceptT . runStateT`.

## Question families this monad belongs to

- [env-eval-family](../question-families/env-eval-family.md) — evaluator, error variant
- [error-handling-family](../question-families/error-handling-family.md) — throw/catch, multi-effect error propagation

## QuickCheck traps

- `throwError "X" /= throwError "x"` — exact string.
- `Right x >>= f` vs `Left e >>= f` — make sure the `Left` short-circuits.
- A test that runs `eval (Div (Val 1) (Val 0))` MUST get `Left "Division by zero"` (or whichever exact spelling the spec gives).

## Pitfalls

- **`Control.Monad.Except` / `Control.Monad.Error.Class` are NOT in the allowed-imports for practice problems.** Read the spec first: if you can't import them, drop down to concrete `Either e a`.
- `throwError` exits immediately — anything you wrote to a state below it is *kept or discarded depending on the stack order* (see [multi-effect.md](multi-effect.md)).
- The class has TWO params (`e` and `m`); the instance `MonadError e (Either e)` fixes them simultaneously.

## Worked examples

- "Calculator that may divide by zero" (calculator question family).
- `runCalc` in `multi-effect.md` (state + error).

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md)
**Question families:** [error-handling](../question-families/error-handling-family.md)
**QuickCheck:** [maybe-either attacks](../quickcheck/maybe-either-attacks.md)
**Related (monads):** [either](./either.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
