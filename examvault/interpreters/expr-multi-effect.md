<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 10 — Expr with State + Error + Writer (three-effect)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · **expr-multi-effect** · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 10 — Expr with State + Error + Writer (three-effect)

**Effect:** State + Either + Writer (three effects)
**Effect rationale:** the real shape of a serious interpreter: **mutable storage** (State), **failure with message** (Either / MonadError), **trace log** (Writer). The exam is most likely to ask for two of these; this file shows all three so any pair is a subset.
**Type signature:** `eval :: (MonadState Store m, MonadError String m, MonadWriter [String] m) => Expr -> m Int` *(polymorphic)* or `eval :: Expr -> StateT Store (WriterT [String] (Either String)) Int` *(concrete)*
**Search keywords:** multi-effect · three-effect · state-error-writer · mtl-style · transformer-stack · StateT-WriterT · trace-and-fail · expr-mega

## Setup
```haskell
import Control.Monad.State
import Control.Monad.Writer
-- Control.Monad.Except is NOT in the legal-imports list; throwError won't compile
-- For exam: use the concrete stack with manual `Left "..."` raising, OR
-- write the polymorphic version assuming the marker accepts it (check the spec)
```

## ADT
```haskell
data Expr = Val Int
          | Var String                  -- read from store
          | Asgn String Expr            -- write to store
          | Add Expr Expr
          | Mul Expr Expr
          | Div Expr Expr
          | Seq Expr Expr               -- evaluate left for side-effects, return right
          deriving (Eq, Show)

type Store = [(String, Int)]
```

## Approach A: typeclass constraints (polymorphic)
```haskell
eval :: (MonadState Store m, MonadError String m, MonadWriter [String] m)
     => Expr -> m Int

eval (Val n) = do
  tell ["Val " ++ show n]
  return n

eval (Var x) = do
  store <- get
  case lookup x store of
    Just v -> do
      tell ["Var " ++ x ++ " -> " ++ show v]
      return v
    Nothing -> do
      tell ["Var " ++ x ++ " UNBOUND"]
      throwError ("Unbound variable: " ++ x)

eval (Asgn x e) = do
  v <- eval e
  modify ((x, v) :)
  tell ["Asgn " ++ x ++ " = " ++ show v]
  return v

eval (Add e1 e2) = do
  x <- eval e1
  y <- eval e2
  let r = x + y
  tell ["Add " ++ show x ++ " " ++ show y ++ " = " ++ show r]
  return r

eval (Mul e1 e2) = do
  x <- eval e1
  y <- eval e2
  let r = x * y
  tell ["Mul " ++ show x ++ " " ++ show y ++ " = " ++ show r]
  return r

eval (Div e1 e2) = do
  x <- eval e1
  y <- eval e2
  if y == 0
    then do
      tell ["Div: about to fail (divisor = 0)"]
      throwError "Division by zero"
    else do
      let r = x `div` y
      tell ["Div " ++ show x ++ " " ++ show y ++ " = " ++ show r]
      return r

eval (Seq e1 e2) = do
  _ <- eval e1
  eval e2
```
The constraints `(MonadState Store m, MonadError String m, MonadWriter [String] m)` say "any monad that supports all three". The body uses `get`/`put`/`modify`, `throwError`, `tell` freely.

## Approach B: explicit transformer stack (concrete)
```haskell
type EvalM = StateT Store (WriterT [String] (Either String))

-- runner: feeds initial store, returns Either (Result, FinalLog, ...)
runEval :: Expr -> Store -> Either String ((Int, Store), [String])
runEval e initStore =
  runWriterT (runStateT (eval e) initStore)
```

The body of `eval` is **identical** to Approach A. Only the runner changes.

For each layer, what `runX` returns:
- `runStateT :: StateT s m a -> s -> m (a, s)`
- `runWriterT :: WriterT w m a -> m (a, w)`
- `Either e` is the base monad.

So composing inner-to-outer:
```
runStateT (eval e) initStore :: WriterT [String] (Either String) (Int, Store)
runWriterT (...)              :: Either String ((Int, Store), [String])
```
The `Either String` is at the **outside** because it's the *base* — that means on `throwError`, **both state and log are lost**: you just see `Left e`.

## Approach B': swap stack order — keep log on failure
```haskell
type EvalM' = StateT Store (ExceptT String (Writer [String]))

runEval' :: Expr -> Store -> ((Either String (Int, Store)), [String])
runEval' e initStore =
  runWriter (runExceptT (runStateT (eval e) initStore))
```
Here `Either` (via `ExceptT`) is *between* State and Writer. Writer is the base.

On failure:
- Log **is preserved** (Writer is below ExceptT).
- State **is lost** (StateT is above ExceptT).

So changing stack order **changes what you observe on `throwError`**. The exam might pin a specific behaviour — read carefully.

| Stack | On `throwError`, you see |
|---|---|
| `StateT s (WriterT w (Either e))` | `Left e` — no state, no log |
| `StateT s (ExceptT e (Writer w))` | `(Left e, log)` — log preserved |
| `ExceptT e (WriterT w (State s))` | `((Left e, log), s)` — everything preserved |

## Comparison: typeclass vs explicit
| Aspect | Typeclass `(MonadX m, MonadY m, ...) =>` | Explicit `StateT s (WriterT w (Either e))` |
|---|---|---|
| Code reuse | Same body works with any stack | Body tied to one stack |
| Runner | Choose at use-site | Hardcoded |
| Behaviour on `throwError` | Determined by chosen stack | Fixed by chosen stack |
| Imports | Need `mtl` class hierarchy | Need transformer libraries |
| Exam suitability | Good if you understand stack semantics | Easier to reason about; pinpoints behaviour |

## Per-constructor breakdown
| Ctor | State | Writer | Error |
|---|---|---|---|
| `Val n` | none | `tell ["Val n"]` | none |
| `Var x` | `get`, lookup | `tell ["Var x -> v" / "UNBOUND"]` | `throwError` if missing |
| `Asgn x e` | `modify ((x,v) :)` | `tell ["Asgn x = v"]` | propagate |
| `Add / Mul` | none | `tell [op-line]` after sub-evals | propagate |
| `Div e1 e2` | none | `tell` either success or "about to fail" | `throwError "Division by zero"` if y=0 |
| `Seq e1 e2` | none | propagate | propagate |

## Pitfalls
- **Picking the wrong stack.** `StateT s (Either e)` ≠ `ExceptT e (State s)` on failure (state lost vs preserved). Likewise for Writer.
- **Mixing class constraints and transformer monomorphisation.** Either declare `eval :: (MonadState s m, ...) => ...` (polymorphic) OR `eval :: StateT s ... a` (concrete). Not both.
- **`runX` order matches stack order from the outside in.** `type T = StateT s (WriterT w (Either e))` ⇒ `runStateT` first (peels State), then `runWriterT` (peels Writer), leaving `Either e (...)`.
- **`throwError` requires `MonadError`.** Without it, use `lift . lift $ Left "..."` from inside `StateT s (WriterT w (Either e))` — fragile and hard to read.
- **Legal imports forbid `Control.Monad.Except` / `Trans`.** If those are forbidden, write the manual `newtype Eval a = Eval { runEval :: Store -> Either String (a, Store, [String]) }` form (one combined monad).
- **`tell w` AFTER `throwError`** is silently dropped if the Either layer is below Writer (Approach B). Put logging **before** the throw if you want to preserve evidence.
- **State changes are also dropped** when Either is below State (Approach B). Be deliberate.

## QuickCheck attacks
- Correctness: `runEval e [] == Right ((v, store), log)` where `v` matches a pure eval.
- Failure: `runEval (Div e (Val 0)) []` returns `Left "Division by zero"`.
- State on success: after `Asgn "x" (Val 5)`, the final store contains `("x", 5)`.
- Log monotonicity: the log accumulates left-to-right, in the order `eval` visits sub-expressions.
- Sequence: `Seq (Asgn "x" (Val 1)) (Var "x")` returns `1` AND the store has `("x", 1)`.
- Failure mid-sequence: `Seq (Asgn "x" (Val 1)) (Div e (Val 0))` — depending on stack, the store may or may not be observable.

## Extend pattern
Question: "Add `If Expr Expr Expr` where condition non-zero = true."
1. **AST:** `| If Expr Expr Expr`
2. **Parser:** `if (cond) then ... else ...`.
3. **Eval:**
```haskell
eval (If c t e) = do
  cv <- eval c
  tell ["If condition = " ++ show cv]
  if cv /= 0 then eval t else eval e
```
The if-branch *doesn't extend* state; both branches see the same store.

## Worked example
```
program = Seq (Asgn "x" (Val 5)) (Div (Var "x") (Val 0))

eval program (initial store [])
 -- Seq: eval e1, then eval e2
 -- Asgn "x" (Val 5):
 --   v <- eval (Val 5)       -- 5
 --   modify ((x,5) :)         -- store = [("x",5)]
 --   tell ["Asgn x = 5"]
 --   return 5
 -- Then eval (Div (Var "x") (Val 0)):
 --   x <- eval (Var "x")  -- 5; store unchanged; tell ["Var x -> 5"]
 --   y <- eval (Val 0)    -- 0; tell ["Val 0"]
 --   y == 0 ⇒ tell ["Div: about to fail"]; throwError "Division by zero"

For StateT s (WriterT w (Either e)) stack: result = Left "Division by zero"
                                            (no store, no log observable)
For ExceptT e (WriterT w (State s)) stack: result = ((Left "...", log), store=[("x",5)])
```

## See also

**Archetypes:** [A14 multi-effect interp](../archetypes/A14-multi-effect-interp.md) · [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Cross-topic:** [expr × multi](../cross-matrix/expr-x-multi.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md) · [writer-trace](../question-families/writer-trace-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)
**Related (interpreters):** [expr state either](./expr-state-either.md) · [expr writer state](./expr-writer-state.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
