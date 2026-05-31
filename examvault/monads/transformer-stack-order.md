<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Transformer stack order**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · [generic-combinators](./generic-combinators.md) · [io](./io.md) · [list-monad](./list-monad.md) · [maybe](./maybe.md) · [monad-laws](./monad-laws.md) · [monaderror](./monaderror.md) · [multi-effect](./multi-effect.md) · [reader](./reader.md) · [state](./state.md) · **transformer-stack-order** · [transformers](./transformers.md) · [writer](./writer.md)
<!-- siblings:end -->






# Transformer stack order — `StateT s (Either e)` vs `ExceptT e (State s)`

When you stack two monads, the **order of the stack determines which effect "wins" on failure**. With `StateT s (Either e) a`, if you fail, the state is lost. With `ExceptT e (State s) a`, the state survives the failure. They have the same Haskell type up to a wrapper but operationally diverge.

This page shows the two stacks running on the same program and tracks who keeps what when something fails.

## The two stacks

```haskell
import Control.Monad.State    -- StateT, MonadState
import Control.Monad.Except   -- ExceptT, MonadError, throwError

type Prog1 a = StateT  Int (Either String) a   -- state THEN error
type Prog2 a = ExceptT String (State  Int)  a   -- error THEN state
```

Reading "outside in" tells you the order of effects:

| Stack | Outer | Inner | What `run<Outer>` returns |
|---|---|---|---|
| `StateT s (Either e) a` | `StateT s` | `Either e`  | `Either e (a, s)` — Left loses everything |
| `ExceptT e (State s) a` | `ExceptT e` | `State s` | `(Either e a, s)` — state survives Left |

## A minimal program with both a state update and a failure

```haskell
incThenFail :: (MonadState Int m, MonadError String m) => m ()
incThenFail = do
  modify (+1)             -- state goes 0 → 1
  throwError "boom"        -- now we fail
```

Same `do`-block, both stacks. Now run it.

### Run on `Prog1 = StateT Int (Either String)`

```haskell
runProg1 :: Either String ((), Int)
runProg1 = runStateT incThenFail 0
-- result: Left "boom"
```

State is gone. `Left "boom"` carries no state component. The increment to `1` happened in the `StateT` layer's inner computation, but the moment the inner `Either` short-circuits to `Left`, the wrapping `StateT` has nothing to project. The whole computation collapses to a `Left`.

### Run on `Prog2 = ExceptT String (State Int)`

```haskell
runProg2 :: (Either String (), Int)
runProg2 = runState (runExceptT incThenFail) 0
-- result: (Left "boom", 1)
```

State survived. The outer `ExceptT` short-circuits the value to `Left`, but the inner `State` is still running and carries the `Int` through to the final result. The increment is observable.

## Side-by-side trace

```
        StateT Int (Either e) ()           ExceptT e (State Int) ()
        ─────────────────────────────       ─────────────────────────────
state:  0                                   0
       ┌─ modify (+1) ──┐                  ┌─ modify (+1) ──┐
state:  1                                   1
       │                │                  │                │
       │  throwError    │                  │  throwError    │
       │  ↓             │                  │  ↓             │
       │  Left "boom"   │                  │  Left "boom"   │ ← outer
       │  ↑             │                  │                │
       │  collapses     │                  │  state still   │
       │  StateT        │                  │  visible       │
       └────────────────┘                  └────────────────┘
final:  Left "boom"                         (Left "boom", 1)
        ↑                                   ↑       ↑
        state lost                          error   state preserved
```

## Practical guidance: which order do I want?

**Want the state preserved on failure** (e.g. parser that has consumed input and wants to report the position) → `ExceptT e (State s) a`.

**Want all-or-nothing — state rolled back on failure** (e.g. transactional update) → `StateT s (Either e) a` or `StateT s (Either e) a`.

For the Birmingham FP exam, **Assignment 3's multi-effect interpreter uses the state-preserving order** (`ExceptT` outside `State`), because if evaluation fails mid-program you still want to see the heap as it was at the point of failure.

## The `lift` story

Plain `State` operations have to be `lift`ed once into `StateT`:

```haskell
-- In ExceptT e (State Int), to read the state:
get :: State Int Int             -- pure State action
-- needs:
lift get :: ExceptT e (State Int) Int
```

The `MonadState` / `MonadError` typeclasses auto-derive lifting for you in either order, so you can write `modify (+1)` and `throwError "x"` in the same `do` block without manually `lift`ing — as the polymorphic `incThenFail` above does. Run-time, the difference is the stack order.

## Why `StateT (State ...)` doesn't compose

You can't have two `State` layers with different `s` types stacked without manually disambiguating which `get`/`put` you mean. Each layer gets its own `s`. In practice you stack one `State` and one of {Except, Writer, Reader}, never two of the same.

## QuickCheck properties

```haskell
-- For StateT s (Either e):
prop_stateT_failed_loses_state :: Int -> Property
prop_stateT_failed_loses_state s0 =
  let r = runStateT (do modify (+1); throwError "x") s0 :: Either String ((), Int)
  in r === Left "x"

-- For ExceptT e (State s):
prop_exceptT_failed_keeps_state :: Int -> Property
prop_exceptT_failed_keeps_state s0 =
  let (r, s) = runState (runExceptT (do modify (+1); throwError "x")) s0 :: (Either String (), Int)
  in r === Left "x" .&&. s === s0 + 1
```

Both should pass. If they don't, your stack ordering is reversed from what you think.

## See also

**Theory:** [transformers overview](./transformers.md) · [multi-effect](./multi-effect.md) · [State monad](./state.md) · [Either monad](./either.md) · [MonadError](./monaderror.md)
**Archetypes:** [A14 multi-effect interp](../archetypes/A14-multi-effect-interp.md) · [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Interpreters:** [expr-state-either](../interpreters/expr-state-either.md) · [expr-writer-state](../interpreters/expr-writer-state.md) · [expr-multi-effect](../interpreters/expr-multi-effect.md)
**Question families:** [error-handling](../question-families/error-handling-family.md) · [env-eval](../question-families/env-eval-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [state attacks](../quickcheck/state-attacks.md) · [maybe/either attacks](../quickcheck/maybe-either-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
