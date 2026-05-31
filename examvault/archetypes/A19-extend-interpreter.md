<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A19 — Extend an Interpreter**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · **A19** · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A19 — Extend an Interpreter

**Tier:** 2   |   **Stars:** ⭐⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** A3 (extending `Free` with Yield, Sleep)
**Combines with:** A05 · A08 · A14 · A16
**Search keywords:** extend · add construct · while · for · if · interpreter · AST · parser · eval · run

## What it tests
Whether you can add a new language construct (statement or expression) to an existing interpreter by touching all three layers: **AST** (new constructor), **Parser** (new rule), **Evaluator** (new case in `run` / `eval`). And whether you understand that omitting one layer breaks the whole pipeline.

## Recognition triggers
- You're GIVEN a working interpreter (parser + AST + eval)
- The question says "add support for `while`/`for`/`if`/`Try-Catch`/`new operator`"
- You must NOT change existing constructs (regression)
- Test cases include the new construct interleaved with existing ones
- "the parser/eval/AST is given; extend it"

## Canonical 3-layer change
```
1. AST     — `data Cmd = … | NewCtor Param₁ Param₂`
2. Parser  — new `<|>` alternative; fit into precedence
3. Eval    — new clause in `run` / `eval`
```

## Mutations (the examiner picks one)

### M1 — Add `If` to an expression-eval
```haskell
-- AST
data Expr = ... | If Expr Expr Expr     -- cond, then, else

-- Parser
ifExpr :: Parser Expr
ifExpr = do string "if"
            c <- expr
            string "then"
            t <- expr
            string "else"
            e <- expr
            return (If c t e)

-- Eval
eval env (If c t e) = case eval env c of
                        Just 1 -> eval env t
                        Just _ -> eval env e
                        Nothing -> Nothing
```
What changes: ternary; 0/1 interpreted as false/true (or use `Bool`).

### M2 — Add `While` to imperative interpreter (W10 Q1)
```haskell
data Cmd = ... | While Expr Cmd

whileStmt :: Parser Cmd
whileStmt = do string "while"; c <- expr
               string "do";    b <- cmd
               string "end"
               return (While c b)

run env (While c b) =
  case eval env c of
    Just v | v /= 0 -> let env' = run env b in run env' (While c b)
           | otherwise -> env
    Nothing -> env   -- or error
```
What changes: recursive on itself in eval (`While c b` calls itself after running body).

### M3 — Add `For` (W10 Q1 variant)
```haskell
data Cmd = ... | For String Expr Expr Cmd   -- for i = lo to hi do body

forStmt :: Parser Cmd
forStmt = do string "for"; i <- identif
             string "=";   lo <- expr
             string "to";  hi <- expr
             string "do";  b <- cmd
             return (For i lo hi b)

run env (For i lo hi b) =
  case (eval env lo, eval env hi) of
    (Just l, Just h) -> loop env l h
    _                -> env
  where loop env n h
          | n > h     = env
          | otherwise = let env' = (i, n) : env
                            env'' = run env' b
                        in loop env'' (n + 1) h
```
What changes: counter loop; explicit recursion in eval.

### M4 — Add `Negate` to an expression
```haskell
data Expr = ... | Negate Expr

negFactor = char '-' *> (Negate <$> factor)

eval env (Negate e) = fmap negate (eval env e)
```
What changes: unary operator; parser slots into `factor` precedence level.

### M5 — Add `Implies` to a logic interpreter
```haskell
data Logic = ... | Implies Logic Logic

impliesP :: Parser Logic
impliesP = chainr1 disjP (string "=>" *> pure Implies)

evalLogic env (Implies a b) = do x <- evalLogic env a
                                 y <- evalLogic env b
                                 return (not x || y)
```
What changes: right-associative operator (use `chainr1`); meaning ¬p ∨ q.

### M6 — Add `Try-Catch` to multi-effect interpreter (A14 territory)
```haskell
data Cmd = ... | Try Cmd Cmd     -- try body catch handler

run (Try body handler) = run body `catchError` (\_ -> run handler)
```
What changes: adds error-recovery; needs `MonadError`.

### M7 — Add `Print` to IO-flavoured eval
```haskell
data Cmd = ... | Print Expr

run env (Print e) = case eval env e of
                      Just v  -> putStrLn (show v) >> return env
                      Nothing -> return env
```
What changes: `IO` return; for an `IO`-eval, side effect inside `run`.

### M8 — Add `Yield` to free-monad interpreter (A3-style)
```haskell
data Yield a = Yield a deriving Functor

yield :: YieldState s ()
yield = liftF $ FRight (Yield ())

-- Then roundRobin handles Yield specially.
```
What changes: a new functor sum component; round-robin scheduler clause.
> **Note on `deriving Functor`:** it needs the `DeriveFunctor` pragma in your file; Safe permits it on modern GHC, but the course wants the instance written by hand and the template may not enable `DeriveFunctor` — so write the instance yourself:
> ```haskell
> instance Functor Yield where
>   fmap f (Yield a) = Yield (f a)
> ```

### M9 — Add a comparator (`<=`, `>=`) to expression parser
```haskell
data BoolExpr = ... | LE Expr Expr | GE Expr Expr

compareP = chainl1 (LE <$> expr <* string "<=") ...
```
What changes: new operator at the right precedence; eval clause `LE a b = a <= b`.

### M10 — Add `let` binding to a pure-eval language
```haskell
data Expr = ... | Let String Expr Expr

letE :: Parser Expr
letE = do string "let"; x <- identif
          string "="; e1 <- expr
          string "in"; e2 <- expr
          return (Let x e1 e2)

eval env (Let x e1 e2) = case eval env e1 of
                           Just v -> eval ((x, v) : env) e2
                           Nothing -> Nothing
```
What changes: new binding form; env extension on the body.

## Worked examples from this course
- Week 10 Q1: extending the calculator with `if`, `while`, `do-while`, `for`.
- Assignment 3: extending `Free`-based scheduler with `Yield` (Q3) and `Sleep` (Q4).
- Practice file `ai_mock.hs`: occasional small extensions.

## QuickCheck attack surface
- **Existing tests still pass**: the marker re-runs all PREVIOUS test cases. If your extension breaks an existing constructor, you lose all those marks too.
- **New construct interleaved**: e.g. `if (x < 5) then (x = x + 1) else (x = x * 2)`. Tests both layers integrating.
- **Parser fails on bad syntax**: `if x then y` (missing else) should fail to parse.
- **Eval propagates errors**: in M1, if `c` is `Nothing`, return `Nothing` (no silent success).
- **Scoping new bindings**: `For i = 0 to 5 do (print i)` — `i` is in scope INSIDE body, NOT outside.

## Pitfalls (marks-killers)
- **Forgetting one layer**: parse adds new construct but eval doesn't handle it → "parses but doesn't run, gets 0 on eval test".
- **Precedence misplacement**: `while-stmt` inside `factor` parsers makes nothing match.
- **Non-exhaustive eval after extension**: marker uses `-fwarn-incomplete-patterns`. If you added an AST constructor and forgot the eval clause, GHC warns and the marker fails.
- **Scope leak**: `For i …` then reading `i` after the loop should yield the OLD value (or `Nothing`), not the loop's final value.
- **Side effect ordering**: `Print` before the value is computed vs after.
- **Reusing existing constructors**: don't shadow `If` with a different meaning; add `IfElse` or rename.

## Combines-with deep dive

### A19 × A05 — translate before eval
Add `Implies` to source AST, then `removeImplies` (A05) before reaching the unchanged eval:
```haskell
runProgram = eval . removeImplies . parse
```
This separates the new construct from the eval — only the parser+translator change.

### A19 × A16 — parser extension
The parser-layer change usually adds an alternative inside `expr1`, `expr2`, … depending on precedence.

### A19 × A14 — extension with new effect
Adding `Try-Catch` (M6) requires the underlying monad to support `MonadError`.

## See also

**Combines with:** [A08 env eval](./A08-env-eval.md) · [A14 multi-effect interp](./A14-multi-effect-interp.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md)
**Cross-topic:** [expr × multi](../cross-matrix/expr-x-multi.md) · [expr × state](../cross-matrix/expr-x-state.md)
**Theory:** [extend interpreter](../interpreters/extend-interpreter.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
