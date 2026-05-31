<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 7 — Expr → Env + Either String (env + error)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · **expr-reader-either** · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 7 — Expr → Env + Either String (env + error)

**Effect:** Reader + Either (env + error)
**Effect rationale:** **most common multi-effect interpreter**. We need to look up variables (Reader) AND fail with a message on unbound variable or divide-by-zero (Either). This is the realistic shape of a real-world expression evaluator.
**Type signature:** `eval :: Env -> Expr -> Either String Int`
**Search keywords:** reader-either · env-either · unbound-var · safe-eval · ReaderT-Either · expr-eval-error · multi-effect · let-binding · division-by-zero

## ADT used
```haskell
data Expr = Val Int
          | Var String
          | Add Expr Expr
          | Mul Expr Expr
          | Sub Expr Expr
          | Div Expr Expr
          | Let String Expr Expr
          deriving (Eq, Show)

type Env = [(String, Int)]
```

## Implementation A: explicit env argument (recommended)
This is what you write in the exam. No transformers, no special imports.

```haskell
eval :: Env -> Expr -> Either String Int
eval env (Val n) = Right n
eval env (Var x) = case lookup x env of
  Just v  -> Right v
  Nothing -> Left ("Unbound variable: " ++ x)
eval env (Add e1 e2) = do
  x <- eval env e1
  y <- eval env e2
  return (x + y)
eval env (Mul e1 e2) = do
  x <- eval env e1
  y <- eval env e2
  return (x * y)
eval env (Sub e1 e2) = do
  x <- eval env e1
  y <- eval env e2
  return (x - y)
eval env (Div e1 e2) = do
  x <- eval env e1
  y <- eval env e2
  if y == 0
    then Left "Division by zero"
    else Right (x `div` y)
eval env (Let x e1 e2) = do
  v <- eval env e1
  eval ((x, v) : env) e2          -- env extension on the next recursive call
```

`env` is passed explicitly — no monad needed for it. The `do`-notation gives us `Either`'s short-circuit behaviour for free.

## Implementation B: `ReaderT Env (Either String)` (mtl-style)
For exam answers this is overkill — but it shows the *structure*:

```haskell
import Control.Monad.Reader
import Control.Monad.Except
-- neither is in the legal-imports list, so this is illustrative

type EvalM = ReaderT Env (Either String)

eval :: Expr -> EvalM Int
eval (Val n) = return n
eval (Var x) = do
  env <- ask
  case lookup x env of
    Just v  -> return v
    Nothing -> throwError ("Unbound variable: " ++ x)
eval (Add e1 e2) = (+) <$> eval e1 <*> eval e2
eval (Mul e1 e2) = (*) <$> eval e1 <*> eval e2
eval (Sub e1 e2) = (-) <$> eval e1 <*> eval e2
eval (Div e1 e2) = do
  x <- eval e1
  y <- eval e2
  if y == 0 then throwError "Division by zero" else return (x `div` y)
eval (Let x e1 e2) = do
  v <- eval e1
  local ((x, v) :) (eval e2)

runEval :: Expr -> Env -> Either String Int
runEval e env = runReaderT (eval e) env
```

`local f m` is the Reader counterpart of "extend env when running `m`" — exactly what `Let` needs.

## Implementation C: polymorphic class constraints
```haskell
-- requires both Reader and MonadError imports
eval :: (MonadReader Env m, MonadError String m) => Expr -> m Int
eval (Val n)     = return n
eval (Var x)     = do env <- ask
                      maybe (throwError ("Unbound: " ++ x)) return (lookup x env)
eval (Add e1 e2) = (+) <$> eval e1 <*> eval e2
eval (Div e1 e2) = do x <- eval e1
                      y <- eval e2
                      if y == 0 then throwError "Division by zero"
                                else return (x `div` y)
eval (Let x e1 e2) = do v <- eval e1
                        local ((x,v) :) (eval e2)
```
Run with any concrete stack: `ReaderT Env (Either String) Int`, `ReaderT Env (ExceptT String Identity) Int`, etc.

## Per-constructor breakdown
| Ctor | Env | Error |
|---|---|---|
| `Val n` | ignore | none |
| `Var x` | lookup | `Left "Unbound: x"` if missing |
| `Add / Mul / Sub` | passthrough | propagate sub-errors |
| `Div e1 e2` | passthrough | `Left "Division by zero"` if `y == 0` |
| `Let x e1 e2` | extended for body | propagate; `e1` errors propagate too |

## Worked example
```
expr = Let "x" (Val 5)
         (Add (Var "x")
              (Div (Val 10) (Sub (Var "x") (Val 5))))     -- 10 / (5-5) = 10/0

eval [] expr
 = -- Let "x" (Val 5) body
   do v <- eval [] (Val 5)              -- = Right 5
      eval [("x", 5)] body
 = eval [("x",5)] (Add (Var "x") (Div (Val 10) (Sub (Var "x") (Val 5))))
 = do a <- eval [("x",5)] (Var "x")              -- Right 5
      b <- eval [("x",5)] (Div ...)              -- evaluates inner
                                                  -- Sub (Var "x") (Val 5) -> Right 0
                                                  -- Div: y==0 -> Left "Division by zero"
      return (a + b)
 = Left "Division by zero"
```
Errors propagate. Env stays correct throughout.

## Mutations
- **Use `Maybe` instead of `Either String`** — same shape, no message. See [expr-reader.md](expr-reader.md).
- **Add state for storage assignment.** Now you have Reader + State + Either — see [expr-multi-effect.md](expr-multi-effect.md).
- **Use `Data.Map.Map String Int` instead of assoc list** — `Map.lookup` returns `Maybe`, otherwise same.
- **Static-check first.** Run a `freeVars :: Expr -> [String]` pre-pass and reject if not subset of env keys; then `eval` can use `error` safely.

## Pitfalls
- **Forgetting to thread `env` into recursive calls.** Easy to write `eval env e1 + eval e2` (no env on the second). Always pass `env`.
- **Putting `Let`'s extended env on the *wrong* sub-expression.** `Let x e1 e2`: `e1` is evaluated in the **outer** env (so `x` is not yet bound), `e2` is evaluated in the **extended** env. Swapping these gives recursive Let semantics, which is **different**.
- **`local f m` only applies inside `m`** — after `local f (eval e2)` finishes, the env is back to original. This matches Let's lexical scope.
- **Ordering of errors.** Unbound variable error fires before division-by-zero error if the variable is on the left of `Div`. The marker may pin this.
- **Mixing `Maybe` and `Either` in the same evaluator.** Pick one. `Either String Int` is strictly more informative.
- **Using `MonadReader` / `MonadError` imports under exam rules.** Not allowed. Stay with explicit-env + `Either`.
- **`do v <- eval env e1; eval ((x,v):env) e2`** — make sure `v <- ...` precedes the recursive call. Order matters in do-notation.

## QuickCheck attacks
- `eval [] (Var "x") == Left "Unbound variable: x"`.
- `eval [("x", 5)] (Var "x") == Right 5`.
- `eval env (Let "x" (Val 1) (Var "x")) == Right 1`, even when `"x"` not in `env`.
- `eval [("x", 1)] (Let "x" (Val 99) (Var "x")) == Right 99` — shadowing.
- `eval [("x", 1)] (Let "x" (Val 99) (Var "y")) == Left "Unbound variable: y"` — Let doesn't affect unrelated names.
- `eval env (Div e1 (Val 0)) == Left "Division by zero"`.
- `eval env (Add (Var "u") (Div e (Val 0)))` — order of failure matters; left-most first if eval is L→R.
- `Let` doesn't *leak* — env after `Let` evaluation is what it was before, so successive Lets must shadow correctly.

## Extend pattern
Question: "Add `If Expr Expr Expr` where condition is non-zero = true."
1. **AST:** `| If Expr Expr Expr`
2. **Parser:** `if (cond) then ... else ...` rule.
3. **Eval:**
```haskell
eval env (If c t e) = do
  cv <- eval env c
  if cv /= 0 then eval env t else eval env e
```
Note: `If` does NOT extend env; it picks a branch in the same env.

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md) · [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [maybe-either attacks](../quickcheck/maybe-either-attacks.md)
**Related (interpreters):** [expr reader](./expr-reader.md) · [expr state either](./expr-state-either.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
