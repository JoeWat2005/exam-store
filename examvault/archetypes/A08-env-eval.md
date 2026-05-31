<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A08 — Environment-Based Evaluator**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · **A08** · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A08 — Environment-Based Evaluator

**Tier:** 1   |   **Stars:** ⭐⭐⭐⭐
**Mock appearance:** none direct   |   **Assignment appearance:** A3 (Free over State, indirectly)
**Combines with:** A01 · A03 · A14 · A19
**Search keywords:** eval · env · Env · lookup · Var · Lit · Let · interpreter · `Maybe Int` · `Maybe Value`

## What it tests
Whether you can write `eval :: Env -> Expr -> Maybe Value` that pattern-matches the AST, looks up variables in the environment, and EXTENDS the environment when binding `Let x e1 e2`.

## Recognition triggers
- A `data Expr = ... | Var String | ... | Let String Expr Expr | ...` is given
- A `type Env = [(String, Value)]` (or `String -> Maybe Value`) is alongside
- The signature `eval :: Env -> Expr -> Maybe Int` (or similar) is the target
- "looks up `x` in `Env`", "binds `x` to the result of evaluating `e1`"
- Expected behaviour: `eval [("x",3)] (Var "x") == Just 3`; `eval [] (Var "x") == Nothing`

## Canonical template
```haskell
type Env = [(String, Int)]

data Expr = Lit Int
          | Var String
          | Add Expr Expr
          | Mul Expr Expr
          | Let String Expr Expr

eval :: Env -> Expr -> Maybe Int
eval _   (Lit n)        = Just n
eval env (Var x)        = lookup x env
eval env (Add a b)      = do x <- eval env a
                             y <- eval env b
                             return (x + y)
eval env (Mul a b)      = (*) <$> eval env a <*> eval env b
eval env (Let x e1 e2)  = do v <- eval env e1
                             eval ((x, v) : env) e2
```

## Mutations (the examiner picks one)

### M1 — `eval :: Env -> Expr -> Maybe Int` (problem 148)
See canonical template — this IS the spec.
What changes: nothing. Memorise.

### M2 — Pure `evalExpr :: Expr -> Int` (no env, problem 89)
```haskell
data Expr = Val Int | Add Expr Expr | Mul Expr Expr | Sub Expr Expr | Neg Expr

evalExpr :: Expr -> Int
evalExpr (Val n)   = n
evalExpr (Add a b) = evalExpr a + evalExpr b
evalExpr (Mul a b) = evalExpr a * evalExpr b
evalExpr (Sub a b) = evalExpr a - evalExpr b
evalExpr (Neg e)   = negate (evalExpr e)
```
What changes: no environment, no failure, no Maybe. Strict structural recursion.

### M3 — Boolean-valued `Expr` (W7 style)
```haskell
data Expr = LitB Bool | LitI Int
          | Var String
          | Eq Expr Expr | Lt Expr Expr
          | If Expr Expr Expr

data Value = VB Bool | VI Int

eval :: [(String, Value)] -> Expr -> Maybe Value
eval _   (LitB b) = Just (VB b)
eval _   (LitI n) = Just (VI n)
eval env (Var x)  = lookup x env
eval env (Eq a b) = do x <- eval env a
                       y <- eval env b
                       case (x, y) of
                         (VI a', VI b') -> Just (VB (a' == b'))
                         (VB a', VB b') -> Just (VB (a' == b'))
                         _              -> Nothing
eval env (Lt a b) = do VI x <- eval env a
                       VI y <- eval env b
                       Just (VB (x < y))
eval env (If c t e) = do VB cv <- eval env c
                         if cv then eval env t else eval env e
```
What changes: typed values; the pattern `VI x <- eval env a` in a `do`-Maybe block silently returns `Nothing` on type mismatch (this is intentional and clever — uses Monad-fail).

### M4 — `Env` as a function (problem 148 alt)
```haskell
type EnvF = String -> Maybe Int

evalF :: EnvF -> Expr -> Maybe Int
evalF _   (Lit n)       = Just n
evalF env (Var x)       = env x
evalF env (Let x e1 e2) = do v <- evalF env e1
                             evalF (\y -> if y == x then Just v else env y) e2
```
What changes: `env` is a function, not a list. Extension is by lambda-shadowing.

### M5 — `Maybe Value` for divide-by-zero
```haskell
data Expr = Lit Int | Var String | Add Expr Expr | Div Expr Expr | Let String Expr Expr

evalDiv :: Env -> Expr -> Maybe Int
evalDiv env (Div a b) = do x <- evalDiv env a
                           y <- evalDiv env b
                           if y == 0 then Nothing else Just (x `div` y)
evalDiv _   (Lit n)   = Just n
evalDiv env (Var x)   = lookup x env
evalDiv env (Add a b) = (+) <$> evalDiv env a <*> evalDiv env b
evalDiv env (Let x e1 e2) = do v <- evalDiv env e1
                               evalDiv ((x,v):env) e2
```
What changes: `Div` has runtime-failure check on `y == 0` returning `Nothing`.

### M6 — `Either String Int` for typed errors
```haskell
evalE :: [(String, Int)] -> Expr -> Either String Int
evalE _   (Lit n)   = Right n
evalE env (Var x)   = case lookup x env of
                        Nothing -> Left ("unbound: " ++ x)
                        Just v  -> Right v
evalE env (Add a b) = (+) <$> evalE env a <*> evalE env b
```
What changes: error carries a message; same shape, swap `Maybe` for `Either String`.

### M7 — Reader-monad style (`Reader Env`)
```haskell
evalR :: Expr -> Reader Env (Maybe Int)
evalR (Lit n)   = pure (Just n)
evalR (Var x)   = do env <- ask
                     pure (lookup x env)
evalR (Add a b) = do x <- evalR a
                     y <- evalR b
                     pure ((+) <$> x <*> y)
evalR (Let x e1 e2) = do mv <- evalR e1
                         case mv of
                           Nothing -> pure Nothing
                           Just v  -> local ((x, v) :) (evalR e2)
```
What changes: env is implicit via Reader; `local` extends it scope-locally.

### M8 — `evalExpr` over an Expr with `Negate` and precedence (Data2)
```haskell
data Expr a = Value a | Add (Expr a) (Expr a) | Mul (Expr a) (Expr a) | Negate (Expr a)

eval :: Num a => Expr a -> a
eval (Value v)  = v
eval (Add a b)  = eval a + eval b
eval (Mul a b)  = eval a * eval b
eval (Negate e) = negate (eval e)
```
What changes: parametrised by `Num a`; no env; pure.

### M9 — `eval` with explicit pattern-match on `(:)` env lookup
```haskell
evalManual :: [(String, Int)] -> Expr -> Maybe Int
evalManual env (Var x) = look x env
  where look _ [] = Nothing
        look y ((k,v):rest) | y == k    = Just v
                            | otherwise = look y rest
```
What changes: hand-rolled `lookup` for variants where Prelude is forbidden.

### M10 — Add `If`/`While` constructs (A19 territory)
```haskell
data Cmd = Assign String Expr | Seq Cmd Cmd | If Expr Cmd Cmd | While Expr Cmd | Skip

runCmd :: Env -> Cmd -> Env
runCmd env (Assign x e)  = case eval env e of Just v -> (x, v) : env; Nothing -> env
runCmd env (Seq c1 c2)   = runCmd (runCmd env c1) c2
runCmd env (If c t e)    = case eval env c of Just 1 -> runCmd env t; _ -> runCmd env e
runCmd env c@(While c' body) =
  case eval env c' of
    Just 1 -> runCmd (runCmd env body) c    -- loop
    _      -> env
runCmd env Skip          = env
```
What changes: commands return new env (imperative); `eval` is the expression part.

## Worked examples from this course
- Problem sheet Set 9 (#89-90): `evalExpr`, `depthExpr` — M2, no env.
- Problem sheet Set 15 (#148): `eval :: Env -> Expr -> Maybe Int` — M1.
- Practice file `ewan20-31.hs`: typed eval with `Plus`/`Times`/`If`/`Lt` — M3.
- Assignment 3: `FreeState s a` interpretation uses the same eval-like recursion (Pure/Free).
- Week 7 problem sheet: typed environment eval with multiple value-types.

## QuickCheck attack surface
- **Unbound variable**: `eval [] (Var "x") == Nothing` — straightforward.
- **`Let` scoping**: `eval [] (Let "x" (Lit 3) (Add (Var "x") (Lit 4))) == Just 7`. Bug: forgetting to extend env (using `env` instead of `(x,v):env` in body) gives `Nothing`.
- **Shadow**: `eval [("x", 10)] (Let "x" (Lit 1) (Var "x")) == Just 1` — inner binding wins.
- **Operand failure propagates**: `eval [] (Add (Var "u") (Lit 1)) == Nothing` because LHS fails.
- **All-or-nothing `Maybe`**: any sub-expression returning `Nothing` makes the whole expression `Nothing`. Use `do` notation.
- **`Let` with failure in `e1`**: `Let "x" (Var "u") (Lit 0)` — body shouldn't even be tried; `Nothing` propagates.

## Pitfalls (marks-killers)
- **Forgetting to extend env**: `eval env (Let x e1 e2) = do v <- eval env e1; eval env e2` — `x` is never bound in `e2`. Should be `eval ((x,v) : env) e2`.
- **`Var "x"` returning literal**: `eval env (Var x) = Just 0` — student typo. Use `lookup x env`.
- **Cons-order in Let**: `((x, v) : env)` puts the new binding at the FRONT. `lookup` finds the first match, so this gives correct shadowing. Reversing this breaks shadow tests.
- **Using Either for control flow**: if the spec says `Maybe`, use Maybe. Using `Either String` works but auto-marker compares types.
- **Concrete numeric op vs `Num a =>`**: if signature is `Maybe Int`, return `Just (a + b :: Int)`. Don't pollute with `Num` constraints.
- **Pattern match `IVal v <- eval …` outside `Maybe`-do**: only works inside a Monad-fail context. Otherwise use `case … of IVal v -> …`.

## Combines-with deep dive

### A08 × A01 — the AST IS A01's territory
The Expr type IS a recursive ADT (A01). `eval` is structural recursion with an extra accumulating parameter (the env).

### A08 × A14 — eval with state + error
```haskell
evalME :: Expr -> StateT Env (Either String) Int
evalME (Lit n)   = pure n
evalME (Var x)   = do env <- get
                      case lookup x env of
                        Just v  -> pure v
                        Nothing -> lift (Left ("unbound " ++ x))
evalME (Let x e1 e2) = do v <- evalME e1; modify ((x, v) :); evalME e2
```

### A08 × A19 — extend the language with a new construct
Add `If c t e`, `While c body`, `Negate e`. For each, add an AST constructor AND an eval clause AND a parser rule.

## See also

**Combines with:** [A01 tree recursion](./A01-tree-recursion.md) · [A05 ADT translation](./A05-adt-translation.md) · [A14 multi-effect interp](./A14-multi-effect-interp.md) · [A19 extend interpreter](./A19-extend-interpreter.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md)
**Cross-topic:** [expr × maybe](../cross-matrix/expr-x-maybe.md) · [expr × state](../cross-matrix/expr-x-state.md)
**Theory:** [expr-reader interpreter](../interpreters/expr-reader.md) · [expr-reader-either interpreter](../interpreters/expr-reader-either.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [maybe/either attacks](../quickcheck/maybe-either-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
