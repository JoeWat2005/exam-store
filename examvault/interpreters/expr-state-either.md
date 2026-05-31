<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 8 — Expr → State + Either (storage + error)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · **expr-state-either** · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 8 — Expr → State + Either (storage + error)

**Effect:** State + Either (mutable storage + error)
**Effect rationale:** programs both **read and write** to a store (`State`) AND can fail with a message (`Either`). This is the calculator / mini-VM shape. Example: `runCalc` from `ewan31-40.hs`.
**Type signature:** `eval :: Cmd -> StateT Store (Either String) ()` *(concrete)* or `(MonadState s m, MonadError e m) => Cmd -> m ()` *(polymorphic)*
**Search keywords:** state-either · stateT-either · runCalc · storage-error · calculator · stack-machine · mtl-style · multi-effect

## Setup
```haskell
import Control.Monad.State
-- Either / throwError can be from Control.Monad.Except (NOT in legal imports)
-- For exam: use plain `Either String a` and wrap manually
```

## ADT — calculator commands (linear, like a list of statements)
```haskell
data CalcCmd = EnterC
             | StoreC Int CalcCmd
             | AddC   Int CalcCmd
             | MultC  Int CalcCmd
             | DivC   Int CalcCmd
             | SubC   Int CalcCmd
```
A program is a chain; `EnterC` is the terminator. State is the running total (`Int`).

## Implementation: polymorphic mtl-style (`ewan31-40.hs`)
```haskell
runCalc :: (MonadState Int m, MonadError String m) => CalcCmd -> m ()
runCalc EnterC = return ()

runCalc (StoreC x next) = do
  put x
  runCalc next

runCalc (AddC x next) = do
  current <- get
  put (current + x)
  runCalc next

runCalc (MultC x next) = do
  current <- get
  put (current * x)
  runCalc next

runCalc (SubC x next) = do
  current <- get
  put (current - x)
  runCalc next

runCalc (DivC x next) =
  if x == 0
    then throwError "Division by zero"
    else do
      current <- get
      put (current `div` x)
      runCalc next
```
This is the polymorphic form. Pin the monad with a concrete stack to run it.

## Concrete monad: `StateT Int (Either String)`
```haskell
type Calc = StateT Int (Either String)

run :: CalcCmd -> Either String (Int, Int)
run cmd = runStateT (runCalc cmd) 0
-- result: Right (returnedUnit, finalState)  or  Left "err"
```

`runStateT :: StateT s m a -> s -> m (a, s)` — when `m = Either e`, that's `s -> Either e (a, s)`.

## Implementation: expression-style, mutable env (Birmingham-like)
For an `Expr` AST with `Var` that can be *assigned*, we need state and error:
```haskell
data Expr = Val Int
          | Var String
          | Asgn String Expr        -- "x := e"
          | Add Expr Expr
          | Div Expr Expr
          | Seq Expr Expr           -- "e1 ; e2", returns value of e2

type Store = [(String, Int)]

eval :: Expr -> StateT Store (Either String) Int
eval (Val n) = return n
eval (Var x) = do
  store <- get
  case lookup x store of
    Just v  -> return v
    Nothing -> lift (Left ("Unbound: " ++ x))
eval (Asgn x e) = do
  v <- eval e
  modify ((x, v) :)            -- shadow-prepend; replace by Data.Map if needed
  return v
eval (Add e1 e2) = (+) <$> eval e1 <*> eval e2
eval (Div e1 e2) = do
  x <- eval e1
  y <- eval e2
  if y == 0 then lift (Left "Division by zero")
            else return (x `div` y)
eval (Seq e1 e2) = eval e1 >> eval e2
```
`lift (Left ...)` raises the error through `StateT` into the `Either` layer. With `MonadError`, you'd write `throwError "..."` directly.

## Implementation: concrete only, no transformers
For *strict* exam-rule compliance (only legal imports), do it by hand:

```haskell
-- state monad combined manually with Either; this is the "everything explicit" form
newtype Eval a = Eval { runEval :: Store -> Either String (a, Store) }

instance Functor Eval where
  fmap f (Eval g) = Eval $ \s -> case g s of
    Left e        -> Left e
    Right (a, s') -> Right (f a, s')

instance Applicative Eval where
  pure x = Eval $ \s -> Right (x, s)
  (<*>)  = ap

instance Monad Eval where
  return = pure
  Eval g >>= f = Eval $ \s -> case g s of
    Left e        -> Left e
    Right (a, s') -> runEval (f a) s'

throwE :: String -> Eval a
throwE e = Eval $ \_ -> Left e

getE :: Eval Store
getE = Eval $ \s -> Right (s, s)

putE :: Store -> Eval ()
putE s' = Eval $ \_ -> Right ((), s')
```
Then `eval :: Expr -> Eval Int` looks like the StateT version. This is what you write when transformers are forbidden.

## How `StateT s (Either e)` differs from `ExceptT e (State s)`

**This is the classic interview / exam trap.**

```haskell
StateT s (Either e) a  ≅  s -> Either e (a, s)
ExceptT e (State s) a  ≅  s -> (Either e a, s)
```

| Stack | Effect on throw | Notes |
|---|---|---|
| `StateT s (Either e)` | State **lost** on throw — you get `Left e` and no final state | Most common for calculators; "rollback on error" |
| `ExceptT e (State s)` | State **kept** — you get `(Left e, s)` so the state at-time-of-throw is preserved | Useful for diagnostics |

The mtl class constraints `(MonadState s m, MonadError e m) => ...` are agnostic to stack order — but **the choice of concrete stack changes observable behaviour**. The marker can test which one you picked.

## Pitfalls
- **Stack order matters.** `StateT s (Either e)` and `ExceptT e (State s)` give different results on error. Pin the concrete stack to what the spec wants.
- **`get`/`put` are in `Control.Monad.State`.** `throwError` is in `Control.Monad.Except` (NOT a legal import). If you can't import it, use the concrete `Eval` style above, or `lift (Left "...")` from `StateT`.
- **`lift` confusion.** From `StateT`, `lift :: m a -> StateT s m a`. So `lift (Left e) :: StateT s (Either e) a`. Without `lift`, your `Left e` won't typecheck.
- **Validate the operand BEFORE dividing.** `if x == 0 then throwError "..." else do ...` — never `let r = current \`div\` x` before the check.
- **Forgetting to thread `next`.** Each `runCalc cmd next = do ...; runCalc next` — the recursion must explicitly pass `next`.
- **`(current `div` x)` style.** Backticks for infix; `div current x` for prefix. Both equivalent.
- **Running an empty program.** `runCalc EnterC` should be `return ()`, not error.
- **Type of `runStateT`.** Returns `m (a, s)` — with `m = Either e`, that's `Either e (a, s)`. The `(a, s)` is **inside** the `Either`.

## QuickCheck attacks
- `run EnterC == Right ((), 0)` — empty program leaves initial state untouched.
- `run (StoreC 7 EnterC) == Right ((), 7)`.
- `run (DivC 0 EnterC) == Left "Division by zero"`.
- After `Left`, no further side effects: `run (StoreC 5 (DivC 0 (StoreC 100 EnterC)))` — state should NOT be 100 in the `Left` case.
- For `StateT s (Either e)`: state is lost on throw — only `Left e` is observed.
- Order of effects: `AddC 3 (DivC 0 EnterC)` should fail with no observable state change beyond initial.

## Extend pattern
Question: "Add a `PrintC CalcCmd` that logs the current state."
1. **AST:** `| PrintC CalcCmd`
2. **Parser:** keyword `print` or similar.
3. **Eval:** now we need a *third* effect: Writer! See [expr-multi-effect.md](expr-multi-effect.md). The constraint becomes `(MonadState Int m, MonadError String m, MonadWriter [String] m)`. Implementation:
```haskell
runCalc (PrintC next) = do
  current <- get
  tell ["State = " ++ show current]
  runCalc next
```

## See also

**Archetypes:** [A14 multi-effect interp](../archetypes/A14-multi-effect-interp.md) · [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Cross-topic:** [expr × multi](../cross-matrix/expr-x-multi.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [state attacks](../quickcheck/state-attacks.md)
**Related (interpreters):** [expr state](./expr-state.md) · [expr multi effect](./expr-multi-effect.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
