<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Expr × Maybe**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · **expr × maybe** · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Expr × Maybe

**Why this combo:** an interpreter for an Expr ADT that may *fail* — division by zero, unknown variable, type mismatch. Maybe gives you fail/succeed with no message; the `do`-block in Maybe propagates `Nothing` automatically.

**Recognition triggers:**
- "Evaluate the expression; return Nothing on error"
- "Partial interpreter (no error message)"
- "Lookup variables; Nothing if missing"
- "May divide by zero"

**Search keywords:** Expr Maybe, partial evaluator, safeDiv, lookupVar Maybe, evalMaybe Expr

## Pattern (basic partial evaluator)

```haskell
data Expr = Lit Int
          | Var String
          | Add Expr Expr
          | Sub Expr Expr
          | Mul Expr Expr
          | Div Expr Expr

type Env = [(String, Int)]

evalE :: Env -> Expr -> Maybe Int
evalE _   (Lit n)     = Just n
evalE env (Var x)     = lookup x env
evalE env (Add e1 e2) = do
  x <- evalE env e1
  y <- evalE env e2
  return (x + y)
evalE env (Sub e1 e2) = do
  x <- evalE env e1
  y <- evalE env e2
  return (x - y)
evalE env (Mul e1 e2) = do
  x <- evalE env e1
  y <- evalE env e2
  return (x * y)
evalE env (Div e1 e2) = do
  x <- evalE env e1
  y <- evalE env e2
  if y == 0 then Nothing else Just (x `div` y)
```

Two failure modes: `Var` missing in env → `Nothing` (via `lookup`); `Div by 0` → `Nothing` (explicit check). The `do`-block propagates either automatically.

## Worked variants

### Partial evaluator on a tree-shaped Expr

```haskell
-- For when Expr lives inside a BT (combine tree-x-maybe and expr-x-maybe)
data Expr = Lit Int | Add Expr Expr

evalTree :: BT Expr -> Maybe (BT Int)
evalTree Empty = Just Empty
evalTree (Fork e l r) = do
  v  <- evalE [] e
  l' <- evalTree l
  r' <- evalTree r
  return (Fork v l' r')
```

### Safe simplifier (partial constant folding)

```haskell
simplify :: Expr -> Maybe Expr
simplify (Lit n)       = Just (Lit n)
simplify (Var x)       = Just (Var x)
simplify (Add e1 e2)   = do
  e1' <- simplify e1
  e2' <- simplify e2
  case (e1', e2') of
    (Lit a, Lit b) -> Just (Lit (a + b))
    _              -> Just (Add e1' e2')
simplify (Div e1 e2)   = do
  e1' <- simplify e1
  e2' <- simplify e2
  case e2' of
    Lit 0   -> Nothing
    Lit b   -> case e1' of
                 Lit a -> Just (Lit (a `div` b))
                 _     -> Just (Div e1' e2')
    _       -> Just (Div e1' e2')
```

### Lookup with explicit failure message (use Either instead — see tree-x-either.md)

`Maybe` discards the reason. If "which variable was missing" matters, escalate to `Either String Int`.

### Boolean expressions with short-circuit

```haskell
data BExpr = BVar String | BNot BExpr | BAnd BExpr BExpr | BOr BExpr BExpr

evalB :: [(String, Bool)] -> BExpr -> Maybe Bool
evalB env (BVar x)     = lookup x env
evalB env (BNot e)     = not <$> evalB env e
evalB env (BAnd e1 e2) = do
  x <- evalB env e1
  if not x then return False         -- short-circuit
           else evalB env e2
evalB env (BOr e1 e2)  = do
  x <- evalB env e1
  if x then return True
       else evalB env e2
```

### Combine Maybe with state (counter of operations performed) — see [expr-x-state.md](expr-x-state.md)

### Sub-expression eval may itself be conditional

```haskell
data Expr = If Expr Expr Expr | ...

evalE env (If c t e) = do
  b <- evalBool env c   -- if condition fails, Nothing
  if b then evalE env t else evalE env e
```

## Mutations

- **Variable type**: `String` / `Char` / `Int`.
- **Add type check** (Bool vs Int) → Maybe `Either` to surface error type.
- **Add reader env** → use `ReaderT Env Maybe`.
- **Add writer log** → `WriterT [String] Maybe`.
- **Lazy short-circuit** vs strict.
- **Sub-expression** evaluator vs **whole-program** evaluator.

## QuickCheck attacks

```haskell
-- For closed expressions (no Var), evaluation always succeeds
prop_closed_succeeds :: ClosedExpr -> Bool
prop_closed_succeeds (Closed e) = isJust (evalE [] e)

-- Result agrees with reference impl
prop_eval_matches_ref :: Expr -> Env -> Bool
prop_eval_matches_ref e env =
  evalE env e == evalRef env e

-- Failure causes: divide-by-zero or unknown var
prop_failure_diagnosable :: Expr -> Env -> Property
prop_failure_diagnosable e env =
  evalE env e == Nothing ==>
    (hasZeroDiv e env || hasUnknownVar e env)

-- Simplification preserves value
prop_simplify_preserves :: Expr -> Env -> Property
prop_simplify_preserves e env = case simplify e of
  Just e' -> evalE env e == evalE env e'
  Nothing -> True
```

## Pitfalls

- **`do` over Maybe IS automatic propagation.** Don't write `case ... of Just x -> ...; Nothing -> Nothing` for every operator — use `do`.
- **Forgetting the `Nothing` branch of Div** — `Just (x `div` y)` when `y == 0` *will* run on Haskell's `div` (which throws an exception, NOT returns Nothing). Always guard `y == 0`.
- **`<$>` for unary**, `<*>` for binary that's pure-once-evaluated. For `Add`:
  ```haskell
  Add e1 e2 -> (+) <$> evalE env e1 <*> evalE env e2
  ```
  Equivalent to the do-block, more compact.
- **lookup returns Maybe** — `lookup x env :: Maybe Int` — already in Maybe; no conversion needed.
- **Don't pattern-match on `Just`/`Nothing` inside `do`** — use `<-` to extract.
- **`return n`** in a Maybe context = `Just n`. Less clear; prefer `pure n` or `Just n` explicitly.

## See also

**Combined archetypes:** [A05 ADT translation](../archetypes/A05-adt-translation.md) · [A08 env eval](../archetypes/A08-env-eval.md)
**Theory:** [expression tree](../trees/expression-tree.md) · [Maybe](../monads/maybe.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md)
**QuickCheck:** [expr attacks](../quickcheck/expr-attacks.md) · [maybe-either attacks](../quickcheck/maybe-either-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
