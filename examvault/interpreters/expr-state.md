<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 5 — Expr → State s Int (counter / fresh supply)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · **expr-state** · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 5 — Expr → State s Int (counter / fresh supply)

**Effect:** `State s`
**Effect rationale:** evaluation needs to *thread* a mutable value (a counter, a stack, a heap, a fresh-name supply) through the recursion. `State s a = s -> (a, s)` makes this composition implicit.
**Type signature:** `eval :: Expr -> State Int Int`
**Search keywords:** state-eval · counter · fresh · labelTree · get · put · modify · State-monad · expr-state

## Setup
```haskell
import Control.Monad.State
```

## ADT used
```haskell
data Expr = Val Int
          | Add Expr Expr
          | Mul Expr Expr
          | Sub Expr Expr
          deriving (Eq, Show)
```

## Use case 1: counting operations
```haskell
-- count number of arithmetic operations performed
eval :: Expr -> State Int Int
eval (Val n)     = return n
eval (Add e1 e2) = do
  x <- eval e1
  y <- eval e2
  modify (+1)              -- one Add performed
  return (x + y)
eval (Mul e1 e2) = do
  x <- eval e1
  y <- eval e2
  modify (+1)
  return (x * y)
eval (Sub e1 e2) = do
  x <- eval e1
  y <- eval e2
  modify (+1)
  return (x - y)

-- runState (eval e) 0  =  (value, opCount)
```

## Use case 2: fresh-id labelling

This is the canonical State pattern: each sub-tree gets a fresh integer label.

```haskell
data TaggedExpr = TVal Int Int
                | TAdd Int TaggedExpr TaggedExpr
                | TMul Int TaggedExpr TaggedExpr
                deriving (Show)

fresh :: State Int Int
fresh = do
  n <- get
  put (n + 1)
  return n

label :: Expr -> State Int TaggedExpr
label (Val n) = do
  i <- fresh
  return (TVal i n)
label (Add e1 e2) = do
  i  <- fresh
  t1 <- label e1
  t2 <- label e2
  return (TAdd i t1 t2)
label (Mul e1 e2) = do
  i  <- fresh
  t1 <- label e1
  t2 <- label e2
  return (TMul i t1 t2)

-- evalState (label e) 0  :: TaggedExpr
```

## Use case 3: stack calculator (state is the stack)
```haskell
data Instr = Push Int | OpAdd | OpMul
type Stack = [Int]

step :: Instr -> State Stack ()
step (Push n) = modify (n :)
step OpAdd = do
  s <- get
  case s of
    (x:y:rest) -> put ((x + y) : rest)
    _          -> return ()
step OpMul = do
  s <- get
  case s of
    (x:y:rest) -> put ((x * y) : rest)
    _          -> return ()

runProg :: [Instr] -> State Stack ()
runProg = mapM_ step

-- execState (runProg [Push 2, Push 3, OpAdd]) []  =  [5]
```

## Per-constructor breakdown (counting variant)
| Ctor | Recurses | State update | Return |
|---|---|---|---|
| `Val n` | none | none | `n` |
| `Add e1 e2` | both | `modify (+1)` | `x + y` |
| `Mul e1 e2` | both | `modify (+1)` | `x * y` |
| `Sub e1 e2` | both | `modify (+1)` | `x - y` |

## How `State s` plumbs the state for you
```haskell
newtype State s a = State { runState :: s -> (a, s) }

return a = State (\s -> (a, s))           -- doesn't touch state
m >>= f  = State (\s -> let (a, s') = runState m s in runState (f a) s')
get      = State (\s -> (s, s))           -- read
put s'   = State (\_ -> ((), s'))         -- write
modify f = State (\s -> ((), f s))        -- read-modify-write
```
You never write `s -> ...` directly — `do { n <- get; put (n+1) }` threads the state.

## Runners
```haskell
runState   :: State s a -> s -> (a, s)    -- both
evalState  :: State s a -> s -> a         -- just the value
execState  :: State s a -> s -> s         -- just the final state
```

Pick by what the question asks:
- "the result" → `evalState`
- "the final state / counter / stack" → `execState`
- "both" → `runState`

## Mutations
- **Add Var with State for env mutation.** Var assignment becomes a state update; this is the imperative-language move.
- **Add failure.** `StateT s (Either e) a` — see [expr-state-either.md](expr-state-either.md).
- **Add log.** `WriterT [String] (State s) a` — see [expr-writer-state.md](expr-writer-state.md).
- **Make state polymorphic with `MonadState`.** `(MonadState Int m) => Expr -> m Int` lets you instantiate to State or to any transformer stack containing State.

## Pitfalls
- **`get` and `put` come from `Control.Monad.State`** — forget the import and they're not in scope.
- **`State` is *not* mutation, it's plumbing.** Each `>>=` threads the state explicitly via the closure. Don't think "I'm mutating `n`" — think "I'm composing state-transformers".
- **`runState`, `evalState`, `execState` confusion.** Memo: **r**un = both; **e**val = value; **ex**ec = state.
- **Returning a value while forgetting to update state.** `do n <- get; return (n+1)` does NOT increment state; it returns `n+1` as the value and leaves state unchanged. Use `modify (+1); return n`.
- **Refutable pattern-match on `get` is a *compile* error** — for plain `State`, writing `(x:xs) <- get` makes GHC demand `MonadFail Identity`, which does not exist, so the whole file fails to compile (scores 0) — it is *not* a runtime failure. Always do `s <- get` then `case s of ...`. (A failable monad like `MaybeT`/`StateT _ Maybe` would instead `fail`/give `Nothing` at runtime, but plain `State` never gets that far.)
- **Order of `modify` and recursion.** `modify` BEFORE recursion logs "I'm about to recurse"; AFTER logs "I finished". Spec usually wants after.
- **Treating `State` as if it had failure.** It doesn't — it's a total monad. For failure, stack it with `Maybe` or `Either`.

## QuickCheck attacks
- `evalState (eval e) 0 == evalPure e` — value must match pure eval.
- `execState (eval e) 0 == numNodes e - numLeaves e` — counter must equal number of internal ops.
- `execState (label e) 0 == sizeOf e` — fresh-id supply must equal node count.
- Each fresh id used by `label` must be **unique** — no two nodes share a tag.
- After `runProg`, the stack has exactly one element (well-formed program).

## Extend pattern
Question: "Add `Var String` reading from a `[(String, Int)]` state."
1. **AST:** `| Var String`
2. **Parser:** identifier rule.
3. **Eval (state holds the env):**
```haskell
eval :: Expr -> State [(String, Int)] Int
eval (Var x) = do
  env <- get
  case lookup x env of
    Just v  -> return v
    Nothing -> return 0     -- or use StateT _ Maybe for failure
```

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md) · [A02 state game](../archetypes/A02-state-game.md)
**Cross-topic:** [expr × state](../cross-matrix/expr-x-state.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [state-game](../question-families/state-game-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [state attacks](../quickcheck/state-attacks.md)
**Related (interpreters):** [expr state either](./expr-state-either.md) · [imperative storage](./imperative-storage.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
