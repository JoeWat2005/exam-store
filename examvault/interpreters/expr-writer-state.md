<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 9 — Expr → Writer + State (trace + counter)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · **expr-writer-state** · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 9 — Expr → Writer + State (trace + counter)

**Effect:** Writer + State
**Effect rationale:** evaluation needs to **log every step** (Writer) AND **track a counter** (State) — e.g. a tag for each logged sub-expression. No failure path.
**Type signature:** `eval :: Expr -> WriterT [String] (State Int) Int` *(concrete)* or `(MonadWriter [String] m, MonadState Int m) => Expr -> m Int` *(polymorphic)*
**Search keywords:** writer-state · log-counter · WriterT-State · trace-id · numbered-log · fresh-tag · interpret-with-trace

## Setup
```haskell
import Control.Monad.State
import Control.Monad.Writer
```

## ADT used
```haskell
data Expr = Val Int
          | Add Expr Expr
          | Mul Expr Expr
          deriving (Eq, Show)
```

## Polymorphic implementation (mtl-style)
```haskell
eval :: (MonadWriter [String] m, MonadState Int m) => Expr -> m Int
eval (Val n) = do
  i <- fresh
  tell ["[" ++ show i ++ "] Val " ++ show n]
  return n
eval (Add e1 e2) = do
  x <- eval e1
  y <- eval e2
  i <- fresh
  let r = x + y
  tell ["[" ++ show i ++ "] Add " ++ show x ++ " " ++ show y ++ " = " ++ show r]
  return r
eval (Mul e1 e2) = do
  x <- eval e1
  y <- eval e2
  i <- fresh
  let r = x * y
  tell ["[" ++ show i ++ "] Mul " ++ show x ++ " " ++ show y ++ " = " ++ show r]
  return r

fresh :: MonadState Int m => m Int
fresh = do
  n <- get
  put (n + 1)
  return n
```

## Concrete stack
```haskell
type EvalM = WriterT [String] (State Int)

run :: Expr -> ((Int, [String]), Int)
run e = runState (runWriterT (eval e)) 0
-- run (Add (Val 1) (Val 2))
--   = (( 3            -- value
--      , [ "[0] Val 1"
--        , "[1] Val 2"
--        , "[2] Add 1 2 = 3" ]
--      )
--    , 3              -- final counter (3 entries)
--    )
```

The result is `((value, log), counterFinal)` because `runWriterT` peels off the Writer, leaving a `State` action; `runState` peels off the State.

## Alternative stack: `StateT Int (Writer [String])`
```haskell
type EvalM' = StateT Int (Writer [String])

run' :: Expr -> ((Int, Int), [String])
run' e = runWriter (runStateT (eval e) 0)
-- result: ((value, finalCounter), log)
```

Both stacks give equivalent observable behaviour for Writer + State (no error layer), so the choice is cosmetic — but the **shape** of the result type differs as shown.

## Manual / explicit implementation (no transformers)

For strict exam-rule compliance you write a record-style "carry both":
```haskell
type LogState = ([String], Int)        -- (log accumulator, fresh-id counter)

eval :: Expr -> State LogState Int
eval (Val n) = do
  i <- fresh'
  modify (\(log, c) -> (log ++ ["[" ++ show i ++ "] Val " ++ show n], c))
  return n
eval (Add e1 e2) = do
  x <- eval e1
  y <- eval e2
  i <- fresh'
  let r = x + y
  modify (\(log, c) -> (log ++ ["[" ++ show i ++ "] Add " ++ show x ++ " " ++ show y ++ " = " ++ show r], c))
  return r
-- ...

fresh' :: State LogState Int
fresh' = do
  (log, c) <- get
  put (log, c + 1)
  return c
```
This works but is uglier. Prefer the transformer / mtl form unless imports are restricted.

## Per-constructor breakdown
| Ctor | Writer | State | Return |
|---|---|---|---|
| `Val n` | `tell ["[i] Val n"]` | `fresh` for i | `n` |
| `Add e1 e2` | `tell ["[i] Add x y = r"]` after sub-evals | `fresh` for i | `x + y` |
| `Mul e1 e2` | `tell ["[i] Mul x y = r"]` after sub-evals | `fresh` for i | `x * y` |

## How the effects compose

Writer and State are **independent** in the sense that neither short-circuits — they always accumulate / mutate. So:
- The log gets every `tell` you make, in order.
- The counter increments on every `fresh`.
- The final value is the result of the recursion.

No effect dominates the others; they all run to completion. Compare to State+Either where Either's `throwError` cuts the chain.

## Mutations
- **Add failure.** Now you have all three — see [expr-multi-effect.md](expr-multi-effect.md).
- **Different state.** Instead of `Int`, use `[(String, Int)]` for env-state, or `Stack` for stack-machine.
- **Different writer.** `Writer (Sum Int)` for counting, `Writer (Set String)` for tracking unique names, etc.
- **Drop the fresh-id and use State for something else** (e.g. env, stack).

## Pitfalls
- **`tell` requires Monoid; the State doesn't.** Don't try to `tell (5 :: Int)` — `Int` is not `Monoid` unless wrapped in `Sum`/`Product`.
- **`fresh` returns the **old** counter** (before incrementing) — that's usually what you want for "0-indexed labels". For "1-indexed", `do modify (+1); get`.
- **Stack-order confusion.** `WriterT w (State s)` ≅ `s -> ((a, w), s)`. `StateT s (Writer w)` ≅ `s -> ((a, s), w)`. Same info, different tuple shape — check what the spec wants.
- **`lift` confusion.** `lift :: m a -> WriterT w m a` — lifts a State action into WriterT. You usually don't need it with mtl class-constraint style.
- **Forgetting `runWriterT` / `runStateT` (with capital T).** Outer transformer needs the T variant; only the innermost monad uses the bare runner.
- **Order of `tell` and recursion.** `tell` BEFORE recursion logs "I'm about to recurse"; AFTER logs "I finished". Choose consistently.
- **`tell []` is a no-op** — useful for branches where you don't want to log.

## QuickCheck attacks
- Value matches pure eval: `fst (fst (run e)) == evalPure e`.
- Log length equals number of nodes in `e` (`size e`).
- Counter equals log length.
- Each `i` in the log is unique and increases monotonically: `[0, 1, 2, ...]`.
- Log entries appear in **post-order** (children before parent) because each ctor evaluates sub-exprs first then `tell`s.
- For a degenerate `Val n`: log is one entry, counter is 1.

## Extend pattern
Question: "Add `Var String` that logs lookups."
1. **AST:** `| Var String`
2. **Eval:** add an env argument (or extend state to `(LogState, Env)`):
```haskell
eval (Var x) = do
  -- assume env passed in or read from state
  env <- ... -- depends on how env is stored
  i <- fresh
  case lookup x env of
    Just v  -> do tell ["[" ++ show i ++ "] Var " ++ x ++ " -> " ++ show v]; return v
    Nothing -> do tell ["[" ++ show i ++ "] Var " ++ x ++ " UNBOUND"]; return 0
```
If you want **failure** on unbound, you need the third effect Either — see [expr-multi-effect.md](expr-multi-effect.md).

## See also

**Archetypes:** [A14 multi-effect interp](../archetypes/A14-multi-effect-interp.md) · [A15 writer trace](../archetypes/A15-writer-trace.md)
**Question families:** [writer-trace](../question-families/writer-trace-family.md) · [env-eval](../question-families/env-eval-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [writer attacks](../quickcheck/writer-attacks.md) · [state attacks](../quickcheck/state-attacks.md)
**Related (interpreters):** [expr writer](./expr-writer.md) · [expr state](./expr-state.md) · [expr multi effect](./expr-multi-effect.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
