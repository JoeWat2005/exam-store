<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 2 — Expr → Maybe Int (silent failure)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · **expr-maybe** · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 2 — Expr → Maybe Int (silent failure)

**Effect:** `Maybe`
**Effect rationale:** evaluation may fail (division by zero, unbound variable, type mismatch) but the question does not require a failure *message* — just success-or-fail. `Maybe` is the lightest monad that gives short-circuit-on-fail.
**Type signature:** `eval :: Expr -> Maybe Int`
**Search keywords:** maybe-eval · partial · Nothing · Div · safe-division · do-notation · Maybe-monad · short-circuit · expr-eval

## ADT used
```haskell
data Expr = Val Int
          | Add Expr Expr
          | Mul Expr Expr
          | Sub Expr Expr
          | Div Expr Expr          -- new: may fail on /0
          deriving (Eq, Show)
```

## Full implementation
```haskell
eval :: Expr -> Maybe Int
eval (Val n)     = Just n
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
    then Nothing
    else Just (x `div` y)
```

## Per-constructor breakdown
| Ctor | Recurses on | Effect | Combine |
|---|---|---|---|
| `Val n` | none | none | `Just n` |
| `Add e1 e2` | both | propagate Nothing | `Just (x+y)` |
| `Mul e1 e2` | both | propagate Nothing | `Just (x*y)` |
| `Sub e1 e2` | both | propagate Nothing | `Just (x-y)` |
| `Div e1 e2` | both | **introduce** Nothing if `y==0` | `Just (x \`div\` y)` |

## How do-notation does the work for you
Without do-notation:
```haskell
eval (Add e1 e2) =
  case eval e1 of
    Nothing -> Nothing
    Just x  -> case eval e2 of
      Nothing -> Nothing
      Just y  -> Just (x + y)
```
With do-notation:
```haskell
eval (Add e1 e2) = do
  x <- eval e1     -- if eval e1 == Nothing, whole block returns Nothing
  y <- eval e2     -- ditto for eval e2
  return (x + y)
```
The bind operator `>>=` for `Maybe` is exactly the short-circuit:
```haskell
Nothing  >>= _ = Nothing
Just x   >>= f = f x
```

## Worked example
```
e = Div (Val 6) (Sub (Val 3) (Val 3))      -- 6 / (3-3) = 6/0

eval e
 = do x <- eval (Val 6)
      y <- eval (Sub (Val 3) (Val 3))      -- = Just 0
      if y == 0 then Nothing else Just (x `div` y)
 = do x <- Just 6
      y <- Just 0
      if 0 == 0 then Nothing else Just (6 `div` 0)
 = Nothing
```

## Variant: with variables
```haskell
data Expr = Val Int | Var String | Add Expr Expr | Div Expr Expr

eval :: [(String, Int)] -> Expr -> Maybe Int
eval env (Val n)     = Just n
eval env (Var x)     = lookup x env                    -- already returns Maybe
eval env (Add e1 e2) = do x <- eval env e1
                          y <- eval env e2
                          return (x + y)
eval env (Div e1 e2) = do x <- eval env e1
                          y <- eval env e2
                          if y == 0 then Nothing else Just (x `div` y)
```

## Mutations
- Want a failure *message* instead of just `Nothing` → switch to `Either String Int`. See [expr-either.md](expr-either.md).
- Want to log every step → add Writer on top, see [expr-writer.md](expr-writer.md).
- Want variables that may be unbound → already covered above; lookup returns `Maybe`.
- Want booleans (`If c t e`) → typed values, `Maybe Value` where `Value = IVal Int | BVal Bool`.

## Pitfalls
- **`case rec of Just x -> ...` long-hand is OK but verbose.** Prefer do-notation — it's what the marker expects and it's what makes `Maybe` look like the failure-handling monad it is.
- **Computing `x \`div\` y` BEFORE checking `y == 0`** — that's a runtime exception, not `Nothing`. Always check the divisor first.
- **Returning `Nothing` instead of `Just (...)` for the success case.** Trivial typo that costs marks.
- **Forgetting `return` / `Just` wrap in the success branch of `Div`.** `if y == 0 then Nothing else x \`div\` y` is a type error — the else branch must be `Just (x \`div\` y)` or `return (x \`div\` y)`.
- **Treating `Maybe` as having an error message** — it doesn't; `Nothing` is opaque. If the question says "with reason", use `Either String`.
- **`do { x <- eval e1; y <- eval e2; ... }` on one line:** make sure each `<-` is its own statement, separated by `;` or a newline.
- **Lazy gotcha:** `do { _ <- eval e1; eval e2 }` still evaluates `e1` *in the Maybe-monad sense* — if `e1` fails, `e2` is not evaluated. This is the correct short-circuit, but be aware that `_ <-` is **not** the same as `let _ = ...`.

## QuickCheck attacks
- `eval (Div e (Val 0)) == Nothing` for **any** `e` — divisor zero must fail.
- `eval (Div (Val 0) (Val 0)) == Nothing` — the numerator is zero too, but divisor still zero ⇒ Nothing.
- `eval (Add (Div (Val 1) (Val 0)) (Val 1)) == Nothing` — failure must propagate up through `Add`.
- `eval (Div (Val x) (Val y))` should equal `Just (x \`div\` y)` whenever `y /= 0`.
- Random trees that have **no** `Div` should never return `Nothing`.
- Variable lookup: `Var x` with `x` not in env → `Nothing`, propagates.

## Extend pattern
Question: "Add `Mod Expr Expr` which fails if the modulus is 0."
1. **AST:** `| Mod Expr Expr`
2. **Parser:** new operator at `Mul` precedence (`%`).
3. **Eval:**
```haskell
eval (Mod e1 e2) = do
  x <- eval e1
  y <- eval e2
  if y == 0 then Nothing else Just (x `mod` y)
```

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md)
**Cross-topic:** [expr × maybe](../cross-matrix/expr-x-maybe.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [maybe-either attacks](../quickcheck/maybe-either-attacks.md)
**Related (interpreters):** [expr either](./expr-either.md) · [expr state](./expr-state.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
