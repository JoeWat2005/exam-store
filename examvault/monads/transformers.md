<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Monad Transformers**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · [generic-combinators](./generic-combinators.md) · [io](./io.md) · [list-monad](./list-monad.md) · [maybe](./maybe.md) · [monad-laws](./monad-laws.md) · [monaderror](./monaderror.md) · [multi-effect](./multi-effect.md) · [reader](./reader.md) · [state](./state.md) · [transformer-stack-order](./transformer-stack-order.md) · **transformers** · [writer](./writer.md)
<!-- siblings:end -->






# Monad Transformers

**Imports:** `Control.Monad.Trans.State`, `Control.Monad.Trans.Writer`, `Control.Monad.Trans.Reader`, `Control.Monad.Trans.Except`, `Control.Monad.Trans.Class` (for `lift`). **None of these are in the practice-allowed-imports list.**

## When you would NOT use a transformer

In the FP exam, the allowed imports are:
`Prelude`, `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`.

Only `Control.Monad.State` and `Control.Monad.Writer` are in scope, and those re-export `StateT`/`WriterT` but the exam never asks you to build a transformer stack explicitly. The preferred approach for multi-effect questions is:

**Use class constraints (`MonadState s m`, `MonadError e m`).** See [multi-effect.md](multi-effect.md).

This file is here for **reading** assignments that already define a stack, and for the rare question that says "write `StateT s m a` and explain `lift`".

## Quick reference table

| Transformer | Type | `runT` | `evalT` | `execT` | Lifts |
|---|---|---|---|---|---|
| `StateT s m a`  | `s -> m (a, s)` | `runStateT :: StateT s m a -> s -> m (a, s)`  | `evalStateT :: StateT s m a -> s -> m a` | `execStateT :: StateT s m a -> s -> m s` | `lift :: m a -> StateT s m a` |
| `WriterT w m a` | `m (a, w)`      | `runWriterT :: WriterT w m a -> m (a, w)`     | (no `evalWriterT`) | `execWriterT :: WriterT w m a -> m w` | `lift :: m a -> WriterT w m a` |
| `ReaderT r m a` | `r -> m a`      | `runReaderT :: ReaderT r m a -> r -> m a`     | — | — | `lift :: m a -> ReaderT r m a` |
| `ExceptT e m a` | `m (Either e a)`| `runExceptT :: ExceptT e m a -> m (Either e a)` | — | — | `lift :: m a -> ExceptT e m a` |

`lift` lives in `Control.Monad.Trans.Class`:
```haskell
class MonadTrans t where
  lift :: Monad m => m a -> t m a
```

## Order of the stack matters

```haskell
StateT s (Either e) a    ≡ s -> Either e (a, s)         -- error wins; state lost on Left
ExceptT e (State s) a    ≡ State s (Either e a)
                         ≡ s -> (Either e a, s)         -- state kept on Left
```

Same effects, opposite "what survives on error".

## 1-page worked example: `StateT Int (Either String) a`

Goal: a calculator that maintains an `Int` accumulator and may throw a `String` error on divide-by-zero.

### Setup

```haskell
import Control.Monad.State        -- re-exports StateT, lift, etc.
import Control.Monad.Trans.Except -- ExceptT (or use Either)
```

(For exam-style — without transformers — see [multi-effect.md](multi-effect.md).)

### The calculator

```haskell
data Cmd = StoreC Int | AddC Int | DivC Int

runCalc :: Cmd -> StateT Int (Either String) ()
runCalc (StoreC n) = put n
runCalc (AddC   n) = modify (+ n)
runCalc (DivC   0) = lift (Left "Division by zero")
runCalc (DivC   n) = modify (`div` n)

runProg :: [Cmd] -> Either String ((), Int)
runProg cmds = runStateT (mapM_ runCalc cmds) 0
```

Result type unpacks as:
- `Right ((), s_final)` — successful run, final state `s_final`.
- `Left "Division by zero"` — error; state is lost (because we used `StateT s (Either e)` and not the other order).

### Flipping the order

```haskell
runCalc' :: Cmd -> ExceptT String (State Int) ()
runCalc' (DivC 0) = throwError "Division by zero"
...

runProg' :: [Cmd] -> (Either String (), Int)
runProg' cmds = runState (runExceptT (mapM_ runCalc' cmds)) 0
```
Now you get `(Left "Division by zero", s_at_error)` — state is preserved.

## `lift` — used to inject a lower-monad action into the stack

```haskell
-- inside StateT Int IO ():
do
  s <- get
  lift (putStrLn ("State: " ++ show s))   -- IO action lifted into StateT Int IO
```

The number of `lift`s equals the number of layers above the one you're calling into.

## Pitfalls

- **NOT in allowed imports for practice exam.** Don't depend on `Control.Monad.Trans.*` for vLab auto-marker code unless the assignment template imports them.
- The class-constraint style (`MonadState s m`) handles `lift` automatically — that's why the course material prefers it.
- Stack order flips return-type shape. Be sure you know which one the spec wants.
- `runStateT` returns `m (a, s)` — you still need to run the inner `m`.
- `evalStateT` for `StateT s (Either e)` returns `Either e a` (no state).

## Worked examples

- For your-own-stack: not in this course directly.
- The mock test uses the class-based approach instead — see [multi-effect.md](multi-effect.md).

## See also

**Archetypes:** [A14 multi-effect interp](../archetypes/A14-multi-effect-interp.md) · [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Cross-topic:** [expr × multi](../cross-matrix/expr-x-multi.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md) · [writer-trace](../question-families/writer-trace-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)
**Related (monads):** [multi effect](./multi-effect.md) · [transformer stack order](./transformer-stack-order.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
