<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Expr × Multi-Effect (env + storage + error + trace)**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · **expr × multi** · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Expr × Multi-Effect (env + storage + error + trace)

**Why this combo:** a real interpreter needs ALL FOUR effects at once: read-only variable environment (Reader), mutable cell store (State), runtime error (Either/MonadError), execution trace (Writer). The course's interpreter (`interpreter/Interpreter.md`) is exactly this.

**Recognition triggers:**
- "Implement an interpreter for a language with variables / assignment / errors"
- "Mini calculator that prints / logs / fails"
- "Tracing evaluator for a small DSL"
- "Eval expression in an environment, may fail, with audit log"

**Search keywords:** interpreter, MonadError, MonadState, MonadReader, MonadWriter, RWS, StateT ReaderT, multi-effect, runxy

## Pattern (the course's RWST-style stack)

```haskell
import Control.Monad.State
import Control.Monad.Reader
import Control.Monad.Writer
import Control.Monad.Except      -- or just use Either

-- The "effect contract":
type Env   = [(String, Int)]
type Store = [(String, Int)]
type Trace = [String]

-- Without transformers — use a single monad with tuple state and Either:
type M a = State (Env, Store, Trace) (Either String a)
```

But the cleaner course approach (still without transformers) is to use **`Control.Monad` class constraints**:

```haskell
eval :: ( MonadReader Env m
        , MonadState Store m
        , MonadWriter Trace m
        , MonadError String m
        ) => Expr -> m Int

eval (Lit n) = do
  tell ["Lit " ++ show n]
  return n

eval (Var x) = do
  env   <- ask
  store <- get
  case lookup x env of
    Just v  -> do tell ["Var " ++ x ++ " = " ++ show v]; return v
    Nothing -> case lookup x store of
      Just v  -> do tell ["Cell " ++ x ++ " = " ++ show v]; return v
      Nothing -> throwError ("Unknown: " ++ x)

eval (Add e1 e2) = do
  x <- eval e1
  y <- eval e2
  tell ["Add " ++ show x ++ " + " ++ show y]
  return (x + y)

eval (Div e1 e2) = do
  x <- eval e1
  y <- eval e2
  if y == 0 then throwError "Division by zero"
  else do tell ["Div " ++ show x ++ " / " ++ show y]; return (x `div` y)

eval (Let x e1 e2) = do
  v <- eval e1
  local ((x, v) :) (eval e2)            -- extend env for inner

eval (Assign x e) = do
  v <- eval e
  modify ((x, v) :)                     -- update store
  tell ["Assigned " ++ x ++ " = " ++ show v]
  return v
```

## Worked variants

### Restricted: Reader + Maybe (env-aware partial eval)

```haskell
eval :: Expr -> ReaderT Env Maybe Int
eval (Lit n)       = return n
eval (Var x)       = do env <- ask; lift (lookup x env)
eval (Add e1 e2)   = (+) <$> eval e1 <*> eval e2
eval (Div e1 e2)   = do
  x <- eval e1
  y <- eval e2
  if y == 0 then lift Nothing else return (x `div` y)
```

### Restricted: State + Writer (counter + log, no error)

```haskell
type SW a = State Int (a, [String])

-- Or with class constraints:
eval :: (MonadState Int m, MonadWriter [String] m) => Expr -> m Int
eval (Lit n) = do
  modify (+1)
  tell ["Lit " ++ show n]
  return n
eval (Add e1 e2) = do
  x <- eval e1; y <- eval e2
  modify (+1)
  tell ["Add"]
  return (x + y)
```

### Restricted: State + Maybe (counter or fail, no log)

```haskell
type SM a = StateT Int Maybe a

eval :: Expr -> SM Int
eval (Lit n) = do
  modify (+1)
  return n
eval (Div e1 e2) = do
  x <- eval e1
  y <- eval e2
  modify (+1)
  if y == 0 then StateT (\_ -> Nothing) else return (x `div` y)
```

### Cell store: assignment + read + computation

```haskell
data Stmt = Assign String Expr
          | Read   String         -- read a cell
          | Seq    Stmt Stmt
          | IfZ    Expr Stmt Stmt

execS :: Stmt -> StateT Store (Writer [String]) ()
execS (Assign x e) = do
  v <- evalE e                    -- evalE :: Expr -> StateT Store (Writer ...) Int
  modify ((x, v) :)
  tell ["Set " ++ x ++ " := " ++ show v]
execS (Read x) = do
  st <- get
  case lookup x st of
    Just v  -> tell ["Read " ++ x ++ " = " ++ show v]
    Nothing -> tell ["Read " ++ x ++ ": uninitialised"]
execS (Seq s1 s2) = do
  execS s1
  execS s2
execS (IfZ e s1 s2) = do
  v <- evalE e
  tell ["IfZ " ++ show v]
  if v == 0 then execS s1 else execS s2
```

## Running multi-effect computations

```haskell
-- The course's `runxy` runner:
runEval :: M a -> (Env, Store, Trace) -> ((Either String a, Trace), Store)
runEval m envStoreTrace = runState (runWriterT (runReaderT m env)) store
  where (env, store, _) = envStoreTrace

-- Or hand-rolled — explicit tuple state plus Either:
runHand :: Expr -> Env -> Store -> (Either String Int, Store, [String])
runHand e env st = ...
```

In practice the order of `runReaderT . runStateT . runWriterT` matters — different orders give different `Either`/`State`/`Writer` semantics. (See course `interpreter/Runxy.md`.)

## Mutations

- **Drop a layer**: Reader alone / State alone / Writer alone / Either alone — these are the 1D versions of [expr-x-state.md](expr-x-state.md), [tree-x-reader.md](tree-x-reader.md), etc.
- **Swap effect**: Replace Either with `[String]` errors via Validation.
- **Change Reader contents**: function-based env, scoped via `local`.
- **Change State contents**: simple Int counter / Map / cell store / state + recent ops.

## QuickCheck attacks

```haskell
-- For closed expr in empty env, evaluation matches pure eval
prop_closed_pure :: ClosedExpr -> Bool
prop_closed_pure (Closed e) =
  let (Right v, _) = runM (eval e) emptyEnv emptyStore
  in v == pureEval e

-- Log length ≤ expression size
prop_log_size :: Expr -> Property
prop_log_size e =
  let (_, log) = runM (eval e) emptyEnv emptyStore
  in length log <= sizeExpr e * 2

-- Errors are diagnosable
prop_eval_error :: Expr -> Property
prop_eval_error e =
  case runM (eval e) emptyEnv emptyStore of
    (Left msg, _) -> not (null msg)
    (Right _, _)  -> True
```

## Pitfalls

- **Effect ordering matters.** `StateT s (Writer w) a` vs `WriterT w (State s) a` give different recoveries — the inner monad's effect "wins" on early termination.
- **Class constraints vs concrete transformers.** Class constraints (`MonadReader Env m =>`) are flexible; concrete (`ReaderT Env (StateT Store (Writer [String])) Int`) is explicit. Course exam more likely to use one or the other — read carefully.
- **`local` for Reader is SCOPED.** `local f act` modifies env only for `act`, not after.
- **`tell` accumulates** — log grows monotonically in execution order.
- **`throwError` short-circuits** — like `Nothing`/`Left`.
- **Layered runners**: order of `runX` calls = inverse of layer order in the type. `ReaderT Env (StateT Store (Writer Trace))` → `runWriter . runStateT store . runReaderT env`.
- **Imports.** `Control.Monad.Reader`, `Control.Monad.State`, `Control.Monad.Writer`, `Control.Monad.Except` are needed. (For exam: `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer` are typically allowed — `Except` may NOT be.)

## Constraint-only signature — the simplest exam answer

```haskell
eval :: ( Monad m
        , MonadState Env m
        , MonadWriter [String] m
        ) => Expr -> m Int
eval (Lit n)     = return n
eval (Var x)     = do
  env <- get
  case lookup x env of
    Just v  -> return v
    Nothing -> error ("undefined: " ++ x)    -- or use throwError
eval (Add e1 e2) = do
  x <- eval e1
  y <- eval e2
  tell ["Add " ++ show x ++ "+" ++ show y]
  return (x + y)
```

Caller picks the concrete monad. Same definition handles many.

## See also

**Combined archetypes:** [A14 multi-effect interp](../archetypes/A14-multi-effect-interp.md) · [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Theory:** [expression tree](../trees/expression-tree.md) · [multi-effect](../monads/multi-effect.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md) · [writer-trace](../question-families/writer-trace-family.md)
**QuickCheck:** [expr attacks](../quickcheck/expr-attacks.md) · [interp attacks](../quickcheck/interp-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
