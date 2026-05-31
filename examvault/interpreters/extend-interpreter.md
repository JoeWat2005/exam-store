<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 13 — Extending an interpreter (TEMPLATE)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · **extend-interpreter** · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 13 — Extending an interpreter (TEMPLATE)

**Effect:** template, not an interpreter
**Effect rationale:** the most common exam mutation is "extend this evaluator to handle X". The change is **always** three-layered: AST + parser + eval. This file gives you the diff template.
**Type signature:** N/A — template
**Search keywords:** extend-interpreter · add-ctor · 3-layer-change · ast-parser-eval · interpreter-extension · how-to-extend · mutation · evaluator-add

> **Recognize the question:** if you see "extend the following evaluator so that it also handles X" — *that's this template*. Don't over-think; the change is mechanical.

---

## The 3-layer change

Every extension to an interpreter has exactly three parts:

```
LAYER 1: AST     - add a constructor to the data type
LAYER 2: PARSER  - add a parsing case to handle the new concrete syntax
LAYER 3: EVAL    - add an equation to eval/run handling the new ctor
```

If the question gives you the AST and asks for eval, you skip layer 2. If the question asks for parsing only, you skip layer 3. **All three layers are independent** — touching one doesn't force changes elsewhere (other than the connection point).

---

## Worked example: add `If e1 e2 e3` to a pure `Expr` evaluator

### Starting code

```haskell
data Expr = Val Int
          | Add Expr Expr
          | Mul Expr Expr
          deriving (Eq, Show)

eval :: Expr -> Int
eval (Val n)     = n
eval (Add e1 e2) = eval e1 + eval e2
eval (Mul e1 e2) = eval e1 * eval e2

-- parser (simplified)
expr :: Parser Expr
expr = ... -- chains of Val/Add/Mul
```

### Goal
Add `If e1 e2 e3` where `e1` is the condition (non-zero = true), `e2` is the then-branch, `e3` is the else-branch.

### Layer 1: AST

```haskell
data Expr = Val Int
          | Add Expr Expr
          | Mul Expr Expr
          | If Expr Expr Expr        -- NEW
          deriving (Eq, Show)
```

### Layer 2: Parser

Decide on the concrete syntax: `if c then t else e`. Add to the disjunction:

```haskell
expr :: Parser Expr
expr = ifExpr <|> ... -- existing rules

ifExpr :: Parser Expr
ifExpr = do
  symbol "if"
  c <- expr
  symbol "then"
  t <- expr
  symbol "else"
  e <- expr
  return (If c t e)
```

If your parser uses precedence layers (like the lecture's `expr1..expr7`), insert `ifExpr` at the highest level where it makes sense — usually `expr` itself, since `if` is a top-level expression.

### Layer 3: Eval

Add one equation:

```haskell
eval :: Expr -> Int
eval (Val n)     = n
eval (Add e1 e2) = eval e1 + eval e2
eval (Mul e1 e2) = eval e1 * eval e2
eval (If c t e)
  | eval c /= 0 = eval t
  | otherwise   = eval e
```

Done. Three changes; the rest is untouched.

---

## Template for the change (fill in the blanks)

```haskell
-- LAYER 1: AST
data Expr = ...                              -- existing ctors
          | NewCtor T1 T2 ...                -- NEW
          deriving (Eq, Show)

-- LAYER 2: Parser (decide concrete syntax first)
newCtorParser :: Parser Expr
newCtorParser = do
  symbol "<keyword or token>"
  arg1 <- <parser for T1>
  arg2 <- <parser for T2>
  return (NewCtor arg1 arg2)

-- Add to the top-level disjunction:
expr = ... <|> newCtorParser <|> ...

-- LAYER 3: Eval
eval (NewCtor x y ...) = <semantics>
```

---

## Which monad do I need? Quick decision

When the new ctor introduces a new *effect* (failure, env, log, mutation), you may need to **change the return type of eval**, not just add one equation.

| New ctor introduces... | Effect needed | Change |
|---|---|---|
| Pure operation (e.g. `Pow`, `Neg`, `If` with always-defined branches) | none | just add an equation |
| Can fail silently (e.g. `Div`) | `Maybe` | change `eval :: Expr -> Int` to `eval :: Expr -> Maybe Int`; rewrite all equations using do-notation |
| Can fail with message (e.g. `Var` with unbound) | `Either String` | change to `eval :: Expr -> Either String Int` |
| Reads variable (`Var x`) | env | change to `eval :: Env -> Expr -> Int` or `eval :: Env -> Expr -> Maybe Int` |
| Writes variable (`Asgn x e`) | state | change to `eval :: Expr -> State Store Int` or transformer stack |
| Prints / logs (`Print e`) | writer (or IO) | add Writer or IO layer |
| Conditional with side effects in branches | depends on rest | inherits the existing effect |

**Important:** if you change the type of `eval`, **every existing equation** must be rewritten in the new monad. That's tedious but mechanical: wrap each return in `return`, replace direct combinators with `<$>` / `<*>` or `do`-notation.

---

## Worked example with monad change: add `Div`

### Start: pure
```haskell
data Expr = Val Int | Add Expr Expr | Mul Expr Expr

eval :: Expr -> Int
eval (Val n)     = n
eval (Add e1 e2) = eval e1 + eval e2
eval (Mul e1 e2) = eval e1 * eval e2
```

### Add Div with failure-on-zero
**Layer 1 (AST):** `| Div Expr Expr`.
**Layer 2 (Parser):** new operator at `Mul` precedence.
**Layer 3 (Eval):** because `Div` can fail, change the return type:

```haskell
eval :: Expr -> Maybe Int
eval (Val n)     = Just n
eval (Add e1 e2) = do x <- eval e1; y <- eval e2; return (x + y)
eval (Mul e1 e2) = do x <- eval e1; y <- eval e2; return (x * y)
eval (Div e1 e2) = do x <- eval e1
                      y <- eval e2
                      if y == 0 then Nothing else Just (x `div` y)
```

Every existing equation was rewritten in `Maybe`. The structure is the same; the plumbing changed.

---

## Worked example: add `Var` (env lookup)

### Start: pure (no env)
```haskell
data Expr = Val Int | Add Expr Expr
eval :: Expr -> Int
eval (Val n)     = n
eval (Add e1 e2) = eval e1 + eval e2
```

### Add `Var`
**Layer 1:** `| Var String`.
**Layer 2:** identifier rule (lowercase token).
**Layer 3:** need an env. Choose `[(String, Int)]`:

```haskell
type Env = [(String, Int)]

eval :: Env -> Expr -> Maybe Int
eval _ (Val n)         = Just n
eval env (Var x)       = lookup x env
eval env (Add e1 e2)   = do x <- eval env e1; y <- eval env e2; return (x + y)
```

**Both** the type and every equation changed: env-parameter added, `Maybe` wrapper added.

---

## Worked example: add `Asgn x e` to an imperative program

### Start: lecture-style `Program` with `(:=)`
Already has assignment. To add a *new* statement, e.g. `Print Expr`:

**Layer 1:**
```haskell
data Program = ...
             | Print Expr               -- NEW
```

**Layer 2 (parser):**
```haskell
printStmt :: Parser Program
printStmt = do
  symbol "print"
  symbol "("
  e <- expr
  symbol ")"
  symbol ";"
  return (Print e)

program = assignment <|> block <|> whileStatement <|> ifStatement <|> printStmt
```

**Layer 3 (eval):**

If we accept that `run` becomes `IO`:
```haskell
run :: Program -> Storage -> IO Storage
run (Print e) m = do print (eval m e); return m
-- and lift every other branch into IO
```

If we want a pure log, use Writer:
```haskell
run :: Program -> Storage -> (Storage, [Integer])
run (Print e) m = (m, [eval m e])
-- and combine logs in Block
```

The choice depends on what the question allows.

---

## Checklist before submitting an extension

- [ ] **AST change:** new ctor exists, derives `Show` (and `Eq` if tested).
- [ ] **Parser change:** new rule added, included in the top-level disjunction or correct precedence layer.
- [ ] **Parser change:** doesn't break existing syntax (test by parsing an old example).
- [ ] **Eval change:** new equation handles the new ctor.
- [ ] **Eval change:** all existing equations type-check (especially if you changed the return type).
- [ ] **Type signature:** matches what the question asks (don't change the signature if the question forbids it).
- [ ] **QuickCheck:** new behaviour matches what the spec describes — check the spec phrasing exactly.
- [ ] **Pattern exhaustiveness:** `-fwarn-incomplete-patterns` doesn't fire — every ctor has a case.

---

## When the question DOESN'T change the AST

Sometimes the question is "use the existing AST but evaluate differently". E.g., "write a new `evalLog :: Expr -> Writer [String] Int` for the existing `Expr`."

In that case **only layer 3 changes**. The AST and parser are untouched. You just write a *different* evaluator.

---

## See also

**Archetypes:** [A19 extend interpreter](../archetypes/A19-extend-interpreter.md) · [A14 multi-effect interp](../archetypes/A14-multi-effect-interp.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)
**Related (interpreters):** [expr multi effect](./expr-multi-effect.md) · [expr state either](./expr-state-either.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
