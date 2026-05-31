<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 6 — Expr → Reader Env Int (environment lookup)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · **expr-reader** · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 6 — Expr → Reader Env Int (environment lookup)

**Effect:** `Reader r` (or just an extra function argument — see legal-imports note)
**Effect rationale:** evaluation needs *read-only* access to an environment of variable bindings. `Reader r a = r -> a` is the function-as-context monad.
**Type signature:** `eval :: Expr -> Reader Env Int` (or equivalently `Env -> Expr -> Int` without the monad)
**Search keywords:** reader-eval · env · environment · variable-lookup · ask · local · assoc-list · function-env · Reader-monad · Env-Expr · Let-binding

## Legal-imports caveat

`Control.Monad.Reader` is **not in the practice-rules import list**. In exam answers, prefer one of:
- **Explicit env argument:** `eval :: Env -> Expr -> Int` — works without any new import.
- **Function-as-env:** `type Env = String -> Maybe Int` — uses only `Prelude`. The lecture's `Storage` is exactly this.

Both are equivalent to `Reader Env` in behaviour. The `Reader` monad version is included here because *conceptually* it's what's happening, and the marker may ask "what monad is this?".

---

## ADT used
```haskell
data Expr = Val Int
          | Var String
          | Add Expr Expr
          | Mul Expr Expr
          | Let String Expr Expr        -- Let x e1 e2 = "let x = e1 in e2"
          deriving (Eq, Show)
```

## Variant A: explicit env argument (recommended for exam)
```haskell
type Env = [(String, Int)]

eval :: Env -> Expr -> Int
eval env (Val n)        = n
eval env (Var x)        = case lookup x env of
                            Just v  -> v
                            Nothing -> error ("Unbound: " ++ x)
eval env (Add e1 e2)    = eval env e1 + eval env e2
eval env (Mul e1 e2)    = eval env e1 * eval env e2
eval env (Let x e1 e2)  = eval ((x, v) : env) e2
                          where v = eval env e1
```

If failure should be silent: `eval :: Env -> Expr -> Maybe Int`:
```haskell
eval :: Env -> Expr -> Maybe Int
eval env (Val n)       = Just n
eval env (Var x)       = lookup x env
eval env (Add e1 e2)   = do v1 <- eval env e1; v2 <- eval env e2; return (v1 + v2)
eval env (Mul e1 e2)   = do v1 <- eval env e1; v2 <- eval env e2; return (v1 * v2)
eval env (Let x e1 e2) = do v  <- eval env e1
                            eval ((x, v) : env) e2
```
Source: `practiceproblems/final10.hs` lines 161-180.

## Variant B: function-as-env (lecture style)
```haskell
type Env = String -> Maybe Int

emptyEnv :: Env
emptyEnv _ = Nothing

bind :: String -> Int -> Env -> Env
bind x v env y | x == y    = Just v
               | otherwise = env y

eval :: Env -> Expr -> Maybe Int
eval env (Val n)       = Just n
eval env (Var x)       = env x                        -- no `lookup`, just apply
eval env (Add e1 e2)   = do v1 <- eval env e1; v2 <- eval env e2; return (v1 + v2)
eval env (Mul e1 e2)   = do v1 <- eval env e1; v2 <- eval env e2; return (v1 * v2)
eval env (Let x e1 e2) = do v  <- eval env e1
                            eval (bind x v env) e2
```
This is exactly the lecture's `Storage` pattern but for `Int` instead of `Integer` (and with `Maybe` instead of `error`).

## Variant C: the actual Reader monad
```haskell
-- requires Control.Monad.Reader (NOT in the legal-imports list)
import Control.Monad.Reader

type Env = [(String, Int)]

eval :: Expr -> Reader Env (Maybe Int)
eval (Val n) = return (Just n)
eval (Var x) = do
  env <- ask
  return (lookup x env)
eval (Add e1 e2) = do
  m1 <- eval e1
  m2 <- eval e2
  return $ do v1 <- m1; v2 <- m2; return (v1 + v2)
eval (Let x e1 e2) = do
  m1 <- eval e1
  case m1 of
    Nothing -> return Nothing
    Just v  -> local ((x, v) :) (eval e2)

-- runReader (eval expr) initialEnv :: Maybe Int
```
Notice `local f` runs a sub-computation with `f`-modified env — that's exactly how `Let` extends scope. The nested `do` over `Maybe` is awkward; in practice you'd use `ReaderT Env Maybe Int`. See [expr-reader-either.md](expr-reader-either.md) for the cleaner two-effect version.

## Per-constructor breakdown
| Ctor | Behaviour |
|---|---|
| `Val n` | ignore env, return `n` |
| `Var x` | lookup `x` in env |
| `Add e1 e2` | recurse on both with same env |
| `Mul e1 e2` | same |
| `Let x e1 e2` | evaluate `e1` in current env to get `v`, then evaluate `e2` in **extended** env `(x,v):env` |

## How `Let` shadows
```
let x = 1 in (let x = 2 in x)            -- evaluates to 2
let x = 1 in (let x = 2 in (Var "x"))    -- env at lookup = [("x",2),("x",1)]
                                          -- `lookup` returns first match → 2
```
Shadowing is automatic when you prepend to a list — `lookup` finds the first matching key.

## Mutations
- **Add error message instead of `Maybe`.** See [expr-reader-either.md](expr-reader-either.md).
- **Add typed values (Int + Bool).** `Value = IVal Int | BVal Bool` and `eval :: Env -> Expr -> Maybe Value`. Pattern-match-bind `IVal x <- ...` triggers `Maybe`'s `fail` on type mismatch.
- **Closures.** Values include functions: `Value = IVal Int | Closure String Expr Env`. Now `Lam x body`, `App f arg`. (Beyond the exam scope but a fun extension.)
- **Recursive Let.** `Let x e1 e2` evaluates `e1` in the **extended** env so `x` can refer to itself: `eval (bind x v env) e1`. This is `letrec`.

## Pitfalls
- **`eval ((x,v) : env) body`, NOT `eval [(x,v)] body`.** The latter throws away the surrounding context. Always **prepend** to the existing env.
- **Function-env: `env x` instead of `lookup x env`.** Different syntax — function application, not Prelude `lookup`. Don't mix.
- **`lookup` from `Data.List` returns `Maybe`** — you can chain with do-notation in `Maybe`.
- **Reader's `local f` modifies env only for the sub-computation** — it does **not** persist. `local ((x,v) :) (eval e2)` extends env for `e2` only, just like `Let`.
- **Importing `Control.Monad.Reader` in an exam.** Not legal. Use explicit env or function-env.
- **Confusing Reader and State.** Reader is read-only — `ask` reads but you cannot `put` a new env. `local` *temporarily* swaps env. State allows `put` to permanently change.
- **Returning `Nothing` from `Var` when env is empty.** Correct for `Maybe`; for plain `Int`, you must `error` (or change the return type).
- **`do` over `Reader` returns `Reader Env (Maybe a)`** — two layers nested. Use `ReaderT` or hand-roll the env-argument style.

## QuickCheck attacks
- `eval emptyEnv (Var "x") == Nothing` — lookup in empty env.
- `eval [("x", 5)] (Var "x") == Just 5` — lookup hit.
- `eval [("x", 5)] (Let "x" (Val 10) (Var "x")) == Just 10` — shadowing.
- `eval env (Let "x" e1 (Var "y")) == eval env (Var "y")` — `Let` doesn't change unrelated names.
- `eval env (Add (Var "u") (Val 1)) == Nothing` when `u` is not in env — failure propagates.
- `eval env (Let x e1 e2)` must NOT modify `env` for callers — pure semantics.

## Extend pattern
Question: "Add `LetRec String Expr Expr` for recursive bindings."
1. **AST:** `| LetRec String Expr Expr`
2. **Parser:** keyword `letrec` or `rec` followed by `Let` body.
3. **Eval:**
```haskell
eval env (LetRec x e1 e2) =
  let v   = eval env' e1     -- evaluated in extended env (lazy: relies on Haskell's laziness)
      env' = (x, v) : env
  in eval env' e2
```
Requires the value to be representable (here `Int` is fine because we don't actually use `v` until lookup — laziness lets us tie the knot).

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md)
**Question families:** [env-eval](../question-families/env-eval-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)
**Related (interpreters):** [expr reader either](./expr-reader-either.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
