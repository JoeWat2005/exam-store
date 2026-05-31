<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 4 — Expr → Writer [String] Int (trace each step)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · **expr-writer** · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 4 — Expr → Writer [String] Int (trace each step)

**Effect:** `Writer [String]`
**Effect rationale:** evaluation produces a value AND a side-effect *log* of each step. `Writer w` carries a monoid `w` that is **accumulated** as the computation runs. Used for tracing, logging, accumulating arguments, or any "tell me what you did" effect.
**Type signature:** `eval :: Expr -> Writer [String] Int`
**Search keywords:** writer-eval · trace · log · accumulator · tell · Control.Monad.Writer · running-trace · expr-writer

## Setup
```haskell
import Control.Monad.Writer
```

## ADT used
```haskell
data Expr = Val Int
          | Add Expr Expr
          | Mul Expr Expr
          | Sub Expr Expr
          deriving (Eq, Show)
```

## Full implementation
```haskell
eval :: Expr -> Writer [String] Int
eval (Val n) = do
  tell ["Val " ++ show n ++ " = " ++ show n]
  return n
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
eval (Sub e1 e2) = do
  x <- eval e1
  y <- eval e2
  let r = x - y
  tell ["Sub " ++ show x ++ " " ++ show y ++ " = " ++ show r]
  return r
```

## Running it
```haskell
runWriter :: Writer w a -> (a, w)
execWriter :: Writer w a -> w        -- just the log

example :: Expr
example = Add (Mul (Val 2) (Val 3)) (Val 4)

-- runWriter (eval example) = (10, [ "Val 2 = 2"
--                                 , "Val 3 = 3"
--                                 , "Mul 2 3 = 6"
--                                 , "Val 4 = 4"
--                                 , "Add 6 4 = 10" ])
```

The log is built **bottom-up** because each sub-call writes its message before returning to the parent. Order of `tell` matters.

## Per-constructor breakdown
| Ctor | Recurses on | Tell | Return |
|---|---|---|---|
| `Val n` | none | `["Val n = n"]` | `n` |
| `Add e1 e2` | both | `["Add x y = r"]` (after sub-evals) | `x + y` |
| `Mul e1 e2` | both | `["Mul x y = r"]` | `x * y` |
| `Sub e1 e2` | both | `["Sub x y = r"]` | `x - y` |

## Why `Writer` works mechanically
```haskell
-- Writer w a = (a, w)  in essence
return :: Monoid w => a -> Writer w a
return a = writer (a, mempty)

tell :: Monoid w => w -> Writer w ()
tell w = writer ((), w)

-- bind:  (a,w1) >>= f  =  let (b,w2) = f a in (b, w1 <> w2)
```
So when you do `x <- eval e1; tell [...]; ...`, the log from `eval e1` is **appended** to whatever you `tell` afterwards. The list-monoid `mappend` is `(++)`.

## Variant: counter-style Writer with `Sum Int`

Counting operations rather than listing them — useful when the question says "count the number of multiplications performed":

```haskell
import Data.Monoid (Sum(..))

countMul :: Expr -> Writer (Sum Int) Int
countMul (Val n)     = return n
countMul (Add e1 e2) = do x <- countMul e1; y <- countMul e2; return (x + y)
countMul (Mul e1 e2) = do x <- countMul e1
                          y <- countMul e2
                          tell (Sum 1)
                          return (x * y)
countMul (Sub e1 e2) = do x <- countMul e1; y <- countMul e2; return (x - y)

-- runWriter (countMul ...) :: (Int, Sum Int)
-- getSum (snd (runWriter ...)) :: Int
```

## Variant: tracing both arguments and result, structured

```haskell
data LogEntry = Entered Expr | Returned Int

evalLog :: Expr -> Writer [LogEntry] Int
evalLog e = do
  tell [Entered e]
  v <- evalCore e
  tell [Returned v]
  return v

evalCore :: Expr -> Writer [LogEntry] Int
evalCore (Val n)     = return n
evalCore (Add e1 e2) = (+) <$> evalLog e1 <*> evalLog e2
evalCore (Mul e1 e2) = (*) <$> evalLog e1 <*> evalLog e2
evalCore (Sub e1 e2) = (-) <$> evalLog e1 <*> evalLog e2
```

## Mutations
- **Switch the monoid.** `Writer (Sum Int)`, `Writer (Product Int)`, `Writer (Max Int)`, `Writer (Set String)`, `Writer [LogEntry]` — pick whichever has the right `<>`.
- **Add failure.** Combine with `Maybe` or `Either`: `Expr -> WriterT [String] Maybe Int`. State has runners; Writer doesn't really need one beyond `runWriter`.
- **Add state.** `WriterT [String] (State Int) Int` — log AND mutate. See [expr-writer-state.md](expr-writer-state.md).

## Pitfalls
- **`tell` only works when the inner type is `Monoid`.** A bare `Int` is not. Use `Sum Int` or `[Int]`.
- **Forgetting `import Control.Monad.Writer`.** Both `Writer` and `tell` need it.
- **`runWriter` vs `execWriter`.** `runWriter :: Writer w a -> (a, w)`; `execWriter :: Writer w a -> w` (just the log).
- **The log accumulates as `mappend`, not in any reversed order.** For `[String]` it is `(++)`, so the **first** `tell` produces the **first** elements.
- **Confusing `tell w` with `return w`.** `tell w` writes `w` to the log and returns `()`. `return w` returns `w` as the value and writes `mempty` to the log.
- **Strict-vs-lazy writer.** `Control.Monad.Writer.Strict` and `.Lazy` exist; for long computations the lazy version can leak space — but in the exam either works.
- **Inserting `tell` in the wrong place.** `tell` BEFORE the sub-recursion logs "I started"; `tell` AFTER logs "I finished". Pick deliberately.

## QuickCheck attacks
- Value correctness: `fst (runWriter (eval e)) == evalPure e` — the *value* must equal a pure evaluation.
- Log length: for an expression with N internal nodes, the log has N entries (one per `tell`).
- Order: log is built left-to-right by recursion order. Test that `execWriter (eval (Add a b))` starts with the log of `a`.
- Empty case: `execWriter (eval (Val n))` should be `["Val n = n"]` (one entry) or `[]` if you only log internal ops.
- Associativity: rebracket the expr but the log differs — be careful what the spec asks for.

## Extend pattern
Question: "Add `Var String` that logs the lookup and uses an env `[(String, Int)]`."
1. **AST:** `| Var String`
2. **Parser:** identifier rule.
3. **Eval:**
```haskell
eval :: [(String, Int)] -> Expr -> Writer [String] Int
eval env (Var x) = case lookup x env of
  Just v  -> do tell ["Var " ++ x ++ " -> " ++ show v]; return v
  Nothing -> do tell ["Var " ++ x ++ " UNBOUND, defaulting to 0"]; return 0
-- (or use Writer + Maybe to fail properly)
```

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md) · [A15 writer trace](../archetypes/A15-writer-trace.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [writer-trace](../question-families/writer-trace-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [writer attacks](../quickcheck/writer-attacks.md)
**Related (interpreters):** [expr writer state](./expr-writer-state.md) · [expr state](./expr-state.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
