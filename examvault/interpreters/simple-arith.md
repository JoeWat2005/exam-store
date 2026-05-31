<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 1 — Simple arithmetic (pure)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · **simple-arith**
<!-- siblings:end -->






# Interpreter 1 — Simple arithmetic (pure)

**Effect:** none (pure)
**Effect rationale:** total function, no failure, no env, no log — just `Expr -> Int`. The base case all other interpreters extend.
**Type signature:** `eval :: Expr -> Int`
**Search keywords:** simple-eval · arith · pure · tree-recursion · base-case · Expr · evaluator · ADT-walk · structural-recursion

## ADT used
```haskell
data Expr = Val Int
          | Add Expr Expr
          | Mul Expr Expr
          | Sub Expr Expr
          | Neg Expr
          deriving (Eq, Show)
```

## Full implementation
```haskell
eval :: Expr -> Int
eval (Val n)     = n
eval (Add e1 e2) = eval e1 + eval e2
eval (Mul e1 e2) = eval e1 * eval e2
eval (Sub e1 e2) = eval e1 - eval e2
eval (Neg e)     = negate (eval e)
```

That is the **entire** interpreter. One equation per constructor, each calling `eval` on its sub-expressions and combining with a Haskell operator.

## Per-constructor breakdown
| Ctor | Recursion | Combine |
|---|---|---|
| `Val n` | none — base case | return the int |
| `Add e1 e2` | recurse on `e1`, `e2` | `(+)` |
| `Mul e1 e2` | recurse on `e1`, `e2` | `(*)` |
| `Sub e1 e2` | recurse on `e1`, `e2` | `(-)` |
| `Neg e` | recurse on `e` | `negate` |

The shape never changes: one equation per ctor, the recursion structure mirrors the ADT.

## Worked example
```
e = Add (Mul (Val 2) (Val 3)) (Val 4)

eval e
 = eval (Mul (Val 2) (Val 3)) + eval (Val 4)
 = (eval (Val 2) * eval (Val 3)) + 4
 = (2 * 3) + 4
 = 10
```

## Variant: lifted Op-list constructor (lecture style)

The Birmingham lecture uses an `Op` constructor with a list of sub-expressions instead of one ctor per operator:

```haskell
data OpName = Add | Sub | Mul | Div | Mod | Eq | Leq | And | Or | Not | ...
data Expr   = Constant Integer
            | Var Identifier
            | Op OpName [Expr]

eval :: Storage -> Expr -> Integer
eval m (Constant x) = x
eval m (Var i)      = m i
eval m (Op o es)    = opEval o [eval m e | e <- es]

opEval :: OpName -> [Integer] -> Integer
opEval Add [x, y] = x + y
opEval Sub [x, y] = x - y
opEval Mul [x, y] = x * y
opEval Not [x]    = number (not (boolean x))
-- ...
```

Source: `fp-learning-2025/files/LectureNotes/Sections/interpreter/Interpreter.hs`.

This style trades pattern exhaustiveness for compactness — one `eval` clause covers all operators, but `opEval` becomes partial (the lecture handles this with a catch-all `error` clause).

## Variant: depth / size (alternate "eval")
Any algebra over `Expr` is a tree fold. Replace the operator and you get a different metric:
```haskell
depth :: Expr -> Int
depth (Val _)     = 0
depth (Add e1 e2) = 1 + max (depth e1) (depth e2)
depth (Mul e1 e2) = 1 + max (depth e1) (depth e2)
depth (Neg e)     = 1 + depth e

size :: Expr -> Int
size (Val _)     = 1
size (Add e1 e2) = 1 + size e1 + size e2
size (Mul e1 e2) = 1 + size e1 + size e2
size (Neg e)     = 1 + size e
```

## Mutations
- Add `Div Expr Expr` with division-by-zero → switch to `Expr -> Maybe Int`. See [expr-maybe.md](expr-maybe.md).
- Add `Var String` → need an env. See [expr-reader.md](expr-reader.md).
- Add `Let String Expr Expr` → env that extends. See [expr-reader.md](expr-reader.md).
- Add `Print Expr` → side effect, need `Writer`. See [expr-writer.md](expr-writer.md).
- Add booleans (`BoolVal`, `If`, `And`, `Or`) → typed values. See [expr-reader.md](expr-reader.md) typed-values variant.

## Pitfalls
- **Forgetting a constructor.** GHC will warn if you have `-fwarn-incomplete-patterns`. Always check you have one equation per ctor — easy to forget `Neg` or a binary that wasn't in the spec.
- **Confusing the recursion shape.** `Add e1 e2` recurses on **both** sub-expressions; `Neg e` recurses on **one**. Don't write `eval (Neg e1 e2)` when the ctor takes one arg.
- **Operator precedence accidents in Haskell source.** `eval e1 + eval e2` is fine; `eval $ e1 + e2` is **wrong** (`(+)` doesn't work on `Expr`).
- **Using `(:)` instead of an Op constructor.** `Expr` is not a list — recursion is on its ctor positions, not list cons.
- **Mistaking `Val` for `Var`.** `Val n` is a literal `Int`; `Var s` is a variable name. Different ctors.
- **Trying to make `eval` polymorphic in the value type prematurely.** `eval :: Expr -> a` doesn't typecheck — the operators only work for specific types (`Num`, `Eq`).

## QuickCheck attacks
- Single-constructor input: `eval (Val 0) == 0`
- Distributivity: `eval (Mul a (Add b c)) == eval (Mul a b) + eval (Mul a c)` — must be a law of `eval`.
- Negation involution: `eval (Neg (Neg e)) == eval e`.
- Identity: `eval (Add e (Val 0)) == eval e`.
- Random deep trees: `eval` should not stack-overflow on a left-skewed `Add` chain.

## Extend pattern
Question: "Add a constructor `Pow Expr Expr` representing exponentiation."
1. **AST:** add `| Pow Expr Expr` to `data Expr`.
2. **Parser:** add a case to the operator parsing layer (precedence higher than `Mul`). Defer to [parser-overview.md](parser-overview.md).
3. **Eval:** add equation `eval (Pow e1 e2) = eval e1 ^ eval e2`.

Full template in [extend-interpreter.md](extend-interpreter.md).

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md)
**Cross-topic:** [expr × maybe](../cross-matrix/expr-x-maybe.md)
**Question families:** [env-eval](../question-families/env-eval-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)
**Related (interpreters):** [expr maybe](./expr-maybe.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
