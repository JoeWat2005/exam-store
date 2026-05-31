<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 3 — Expr → Either String Int (failure with message)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · **expr-either** · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 3 — Expr → Either String Int (failure with message)

**Effect:** `Either String`
**Effect rationale:** evaluation may fail AND the question requires a reason / message. `Either e` carries a `Left` payload of the failure reason; `Right` is success. Functionally identical short-circuit behaviour to `Maybe`, but the failure now has information.
**Type signature:** `eval :: Expr -> Either String Int`
**Search keywords:** either-eval · MonadError · throwError · failure-message · Left · Right · division-by-zero · safe-eval · expr-either

## ADT used
```haskell
data Expr = Val Int
          | Var String
          | Add Expr Expr
          | Mul Expr Expr
          | Sub Expr Expr
          | Div Expr Expr
          deriving (Eq, Show)
```

## Full implementation (concrete `Either`)
```haskell
eval :: Expr -> Either String Int
eval (Val n)     = Right n
eval (Var x)     = Left ("Unbound variable: " ++ x)   -- pure eval has no env yet
eval (Add e1 e2) = do
  x <- eval e1
  y <- eval e2
  return (x + y)
eval (Mul e1 e2) = do
  x <- eval e1
  y <- eval e2
  return (x * y)
eval (Sub e1 e2) = do
  x <- eval e1
  y <- eval e2
  return (x - y)
eval (Div e1 e2) = do
  x <- eval e1
  y <- eval e2
  if y == 0
    then Left "Division by zero"
    else Right (x `div` y)
```

## Full implementation (polymorphic, using `MonadError`)
```haskell
-- requires Control.Monad.Except, NOT a legal import for the practice rules
-- shown for completeness only
evalGeneric :: MonadError String m => Expr -> m Int
evalGeneric (Val n)     = return n
evalGeneric (Var x)     = throwError ("Unbound variable: " ++ x)
evalGeneric (Add e1 e2) = do x <- evalGeneric e1; y <- evalGeneric e2; return (x + y)
evalGeneric (Mul e1 e2) = do x <- evalGeneric e1; y <- evalGeneric e2; return (x * y)
evalGeneric (Sub e1 e2) = do x <- evalGeneric e1; y <- evalGeneric e2; return (x - y)
evalGeneric (Div e1 e2) = do x <- evalGeneric e1
                             y <- evalGeneric e2
                             if y == 0 then throwError "Division by zero"
                                       else return (x `div` y)
```
For exam answers: prefer the concrete `Either String Int` version. The polymorphic one is conceptually identical and useful for understanding the *shape* of "interpreter with error message".

## Per-constructor breakdown
| Ctor | Recurses on | Effect | Combine |
|---|---|---|---|
| `Val n` | none | none | `Right n` / `return n` |
| `Var x` | none | introduces failure (if no env) | `Left "Unbound x"` / `throwError "..."` |
| `Add e1 e2` | both | propagate | `return (x+y)` |
| `Mul e1 e2` | both | propagate | `return (x*y)` |
| `Sub e1 e2` | both | propagate | `return (x-y)` |
| `Div e1 e2` | both | **introduce** on `y==0` | `Left "Division by zero"` / `throwError "..."` |

## How `Either e` short-circuits
```haskell
instance Monad (Either e) where
  return = Right
  Left  e >>= _ = Left e        -- any computation after Left e returns Left e
  Right a >>= f = f a
```
So `do x <- Left "err"; rest` becomes `Left "err"`, regardless of `rest`. Same as `Maybe`, but the failure value is non-trivial.

## Worked example
```
e = Add (Val 1) (Div (Val 6) (Val 0))

eval e
 = do x <- eval (Val 1)            -- = Right 1
      y <- eval (Div (Val 6) (Val 0))
      return (x + y)
 -- inner Div:
 -- = do x' <- Right 6
 --      y' <- Right 0
 --      if 0 == 0 then Left "Division by zero" else Right ...
 --   = Left "Division by zero"
 -- so the outer becomes:
 = do x <- Right 1
      y <- Left "Division by zero"
      return (x + y)
 = Left "Division by zero"
```

## Mutations
- **Detailed error messages with sub-expr.** `Left ("Division by zero in " ++ show e1)` — embeds the offending sub-tree.
- **Use a richer error type.** Replace `String` with `data EvalError = DivByZero | UnboundVar String | TypeMismatch String` and `eval :: Expr -> Either EvalError Int`.
- **Combine with env.** See [expr-reader-either.md](expr-reader-either.md).
- **Catch errors mid-evaluation.** Use `Right defaultValue` as a "default if Left" via `case eval e of Left _ -> ...; Right v -> ...`.

## Pitfalls
- **`Left` is failure, `Right` is success.** Easy to flip. Memo: "right is right".
- **Forgetting the error wraps in `Left "..."`.** `if y == 0 then "Division by zero" else ...` is a type error — strings aren't `Either`.
- **Mixing `Maybe` and `Either` semantics.** `Either e` does not have `Nothing` — `Left e` plays that role.
- **Forgetting `return` / `Right` on success in `Div`.** The else-branch must be `Right (x \`div\` y)` or `return (x \`div\` y)`.
- **Importing `Control.Monad.Except` in an exam.** The practice import list does NOT allow it. Use plain `Either e a`.
- **Trying to `throwError` without the right import.** Either use the import (if legal) or `Left "msg"` directly.
- **Asymmetric error info.** If your error type is `String`, the failure is `Left "..."`, not `Left ('!', "...")` or similar tuple.

## QuickCheck attacks
- `eval (Div e (Val 0)) == Left "Division by zero"` — exact message must match.
- `eval (Add (Val 1) (Div e (Val 0))) == Left "Division by zero"` — propagation.
- `eval (Mul (Div e (Val 0)) (Val 0)) == Left "Division by zero"` — short-circuit fires on the **first** Left, not the second.
- Order of evaluation: if your impl evaluates `e2` first, `eval (Div (Var "x") (Val 0))` could yield `Left "Unbound variable: x"` instead of `Left "Division by zero"`. **The test cases may pin the order.** Lecture / spec usually evaluates left-to-right.
- For a clean tree with no `Div` and no `Var`, must return `Right (...)`.

## Extend pattern
Question: "Add `Mod Expr Expr` which fails with `"Modulo by zero"`."
1. **AST:** `| Mod Expr Expr`
2. **Parser:** operator at `Mul` precedence.
3. **Eval:**
```haskell
eval (Mod e1 e2) = do
  x <- eval e1
  y <- eval e2
  if y == 0
    then Left "Modulo by zero"
    else Right (x `mod` y)
```

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md)
**Question families:** [error-handling](../question-families/error-handling-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [maybe-either attacks](../quickcheck/maybe-either-attacks.md)
**Related (interpreters):** [expr maybe](./expr-maybe.md) · [expr reader either](./expr-reader-either.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
