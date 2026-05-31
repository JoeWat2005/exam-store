<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: env-eval**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · **env-eval** · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: env-eval

**Archetype:** A10 (evaluate an Expr with variables/environment)   |   **Stars:** ⭐⭐⭐⭐   |   **Course week(s):** 8–10
**Search keywords:** evalExpr, evalWithEnv, Var, Let, scope, environment, lookup, shadow, recursive let

## Generator template
```haskell
-- The seed: walk an Expr, evaluate. Variable case looks up in an environment;
-- Let case extends the environment.
type Env = [(String, Int)]

seed :: Env -> Expr -> Maybe Int
seed _   (Lit n)       = Just n
seed env (Var x)       = lookup x env
seed env (Add a b)     = (+) <$> seed env a <*> seed env b
seed env (Let x e1 e2) = do v <- seed env e1
                            seed ((x, v) : env) e2
```

The four key dimensions:
1. **Failure mode:** Maybe (Nothing on undefined Var) vs Either String (error message) vs exception.
2. **Let scoping:** non-recursive (eval e1 in *current* env) vs recursive (eval e1 in *extended* env).
3. **Shadowing:** newer bindings hide older ones (lookup hits first).
4. **Effects:** pure vs Reader env vs State env.

## Mutations (the examiner picks one)

### Mutation 1 — evalExpr (no variables, just arithmetic) (= problem 89)
**Spec:** Evaluate constant arithmetic expression.
**Sig:** `evalExpr :: Expr -> Int`
**Solution:**
```haskell
data Expr = Val Int | Add Expr Expr | Mul Expr Expr | Sub Expr Expr | Neg Expr

evalExpr :: Expr -> Int
evalExpr (Val n)     = n
evalExpr (Add a b)   = evalExpr a + evalExpr b
evalExpr (Mul a b)   = evalExpr a * evalExpr b
evalExpr (Sub a b)   = evalExpr a - evalExpr b
evalExpr (Neg e)     = negate (evalExpr e)
```
**QC trap:** Pure — no environment. `Add (Val 2) (Mul (Val 3) (Val 4)) == 14`.

### Mutation 2 — evalWithEnv (Var lookup, Maybe) (= problem 148)
**Spec:** Standard let-binding evaluation. Undefined vars return Nothing.
**Sig:** `eval :: Env -> Expr -> Maybe Int`
**Solution:**
```haskell
data Expr = Lit Int | Var String | Add Expr Expr | Mul Expr Expr | Let String Expr Expr
type Env  = [(String, Int)]

eval :: Env -> Expr -> Maybe Int
eval _   (Lit n)       = Just n
eval env (Var x)       = lookup x env
eval env (Add a b)     = do v1 <- eval env a; v2 <- eval env b; return (v1 + v2)
eval env (Mul a b)     = do v1 <- eval env a; v2 <- eval env b; return (v1 * v2)
eval env (Let x e1 e2) = do v <- eval env e1
                            eval ((x, v) : env) e2
```
**QC trap:** The new binding `(x, v)` *prepends* to `env` so that subsequent `lookup` hits the new value first — this gives correct shadowing.

### Mutation 3 — evalEither (typed errors)
**Spec:** Same but with `Either String` so unknown variables give an error message.
**Sig:** `eval :: Env -> Expr -> Either String Int`
**Solution:**
```haskell
eval :: Env -> Expr -> Either String Int
eval _   (Lit n)       = Right n
eval env (Var x)       = maybe (Left ("undefined: " ++ x)) Right (lookup x env)
eval env (Add a b)     = (+) <$> eval env a <*> eval env b
eval env (Mul a b)     = (*) <$> eval env a <*> eval env b
eval env (Let x e1 e2) = do v <- eval env e1
                            eval ((x, v) : env) e2
```
**QC trap:** `Either String` is also a monad — `do` works the same.

### Mutation 4 — evalRecursiveLet (`letrec`)
**Spec:** `Let x e1 e2` evaluates `e1` in the *extended* environment (so e1 can reference x for fixed-point definitions).
**Sig:** `evalRec :: Env -> Expr -> Maybe Int`
**Solution:**
```haskell
evalRec :: Env -> Expr -> Maybe Int
evalRec env (Lit n)       = Just n
evalRec env (Var x)       = lookup x env
evalRec env (Add a b)     = (+) <$> evalRec env a <*> evalRec env b
evalRec env (Mul a b)     = (*) <$> evalRec env a <*> evalRec env b
evalRec env (Let x e1 e2) = do v <- evalRec env' e1  -- key: env' here, not env
                               evalRec env' e2
  where
    env' = (x, undefined) : env  -- placeholder; only Maybe-int — can't truly tie the knot
```
**QC trap:** Truly recursive let needs `Data.IORef` or laziness on a richer domain (Lazy Int = computation thunks). For `Int` you can fake it only when `e1` doesn't actually reference `x` first.

### Mutation 5 — evalDivision (typed errors, divide-by-zero)
**Spec:** Add `Div Expr Expr` constructor; result is Nothing if denominator evaluates to 0.
**Sig:** `eval :: Env -> Expr -> Maybe Int`
**Solution:**
```haskell
data Expr = Lit Int | Var String | Add Expr Expr | Div Expr Expr | Let String Expr Expr

eval :: Env -> Expr -> Maybe Int
eval _   (Lit n)       = Just n
eval env (Var x)       = lookup x env
eval env (Add a b)     = (+) <$> eval env a <*> eval env b
eval env (Div a b)     = do v1 <- eval env a
                            v2 <- eval env b
                            if v2 == 0 then Nothing else Just (v1 `div` v2)
eval env (Let x e1 e2) = do v <- eval env e1
                            eval ((x, v) : env) e2
```
**QC trap:** Combining Maybe with the failure of divide-by-zero — the `if v2 == 0 then Nothing` is sleek but must be inside the `do`.

### Mutation 6 — evalReader (Reader monad form)
**Spec:** Same as mutation 2 but uses Reader Env.
**Sig:** `eval :: Expr -> Reader Env (Maybe Int)`

> **WARNING - not an allowed import:** `Control.Monad.Reader` is **NOT** on the exam whitelist — importing it scores **0**. (Whitelisted monad modules are only `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`.) Use one of the two whitelisted alternatives below; only write the `Reader`/`asks`/`local` version if the question's own Types module provides it.

**Primary (allowed) — pass the env as an explicit argument** (this is exactly what Reader does under the hood, and it is what canonical Mutation 2 already does):
```haskell
eval :: Env -> Expr -> Maybe Int
eval _   (Lit n)       = Just n
eval env (Var x)       = lookup x env
eval env (Add a b)     = (+) <$> eval env a <*> eval env b
eval env (Let x e1 e2) = do v <- eval env e1
                            eval ((x, v) : env) e2     -- "local" = recurse with an extended env
```

**Allowed alternative — hand-rolled `Reader` newtype** (only Prelude; reproduces `ask`/`asks`/`local`):
```haskell
newtype Reader r a = Reader { runReader :: r -> a }
instance Functor (Reader r) where
  fmap f (Reader g) = Reader (f . g)
instance Applicative (Reader r) where
  pure x = Reader (\_ -> x)
  Reader f <*> Reader g = Reader (\r -> f r (g r))
instance Monad (Reader r) where
  Reader g >>= k = Reader (\r -> runReader (k (g r)) r)

asks  :: (r -> a) -> Reader r a;        asks f = Reader f
local :: (r -> r) -> Reader r a -> Reader r a
local f (Reader g) = Reader (g . f)

eval :: Expr -> Reader Env (Maybe Int)
eval (Lit n)       = return (Just n)
eval (Var x)       = asks (lookup x)
eval (Add a b)     = do mv1 <- eval a
                        mv2 <- eval b
                        return ((+) <$> mv1 <*> mv2)
eval (Let x e1 e2) = do mv <- eval e1
                        case mv of
                          Just v  -> local ((x, v):) (eval e2)
                          Nothing -> return Nothing
```

**Forbidden form (`Control.Monad.Reader`) — shown only for recognition; scores 0 unless the Types module supplies it:**
```haskell
import Control.Monad.Reader   -- WARNING: NOT whitelisted — scores 0
-- same body as the hand-rolled version above (asks / local come from the library)
```
**QC trap:** `local`/extending the env is the *right* tool for scoped binding in the Let case. Don't `put`-style mutate. In the explicit-argument version, "local" is just recursing with `(x,v):env`.

### Mutation 7 — evalAsString (eval returning a string)
**Spec:** Eval and produce a string representation, e.g. for showing a trace.
**Sig:** `evalShow :: Env -> Expr -> Maybe String`
**Solution:**
```haskell
evalShow :: Env -> Expr -> Maybe String
evalShow env e = fmap show (eval env e)
```
**QC trap:** Trivial — exam usually uses this as a 2-mark warm-up.

### Mutation 8 — shadowingTest (semantics property)
**Spec:** Define `eval` such that inner Let shadows outer Let with the same name.
**Sig:** part of mutation 2's eval — see invariant.
**Property:**
```haskell
prop_shadow :: Bool
prop_shadow = eval [] expr == Just 10
  where expr = Let "x" (Lit 1)
              (Let "x" (Lit 10) (Var "x"))
```
**QC trap:** Confirms `(x,v) : env` prepending. If you wrote `env ++ [(x,v)]` you'd get the *outer* `x` and fail this property.

### Mutation 9 — evalStateful (variable mutation)
**Spec:** Add `Assign String Expr` and `Seq Expr Expr` constructors; use State Env.
**Sig:** `eval :: Expr -> State Env Int`
**Solution:**
```haskell
data Expr = Lit Int | Var String | Add Expr Expr | Assign String Expr | Seq Expr Expr

eval :: Expr -> State Env Int
eval (Lit n)       = return n
eval (Var x)       = do env <- get
                        case lookup x env of
                          Just v  -> return v
                          Nothing -> error "undefined"
eval (Add a b)     = (+) <$> eval a <*> eval b
eval (Assign x e)  = do v <- eval e
                        modify ((x, v) :)
                        return v
eval (Seq e1 e2)   = eval e1 >> eval e2
```
**QC trap:** Assignment mutates the environment globally. After `Assign "x" 5`, *every later* lookup of `x` returns 5.

### Mutation 10 — evalFreeVars (collect free variables)
**Spec:** Return the set of variables that are referenced but not bound by an enclosing Let.
**Sig:** `freeVars :: Expr -> [String]`
**Solution:**
```haskell
freeVars :: Expr -> [String]
freeVars (Lit _)       = []
freeVars (Var x)       = [x]
freeVars (Add a b)     = uniqueU (freeVars a ++ freeVars b)
freeVars (Mul a b)     = uniqueU (freeVars a ++ freeVars b)
freeVars (Let x e1 e2) = uniqueU (freeVars e1 ++ filter (/= x) (freeVars e2))
  where uniqueU = foldr (\v acc -> if v `elem` acc then acc else v:acc) []
```
**QC trap:** `Let x ...` binds `x` in `e2` only, not in `e1` (non-recursive let). Free vars of `e1` are *not* shielded.

## Hidden-predicate mutations
- "Eval only if all variables are in env" → `freeVars e \\ map fst env == []` precheck.
- "Evaluation modulo arithmetic mod k" → wrap every result in `(`mod` k)`. Just changes the operators.

## Accumulator-style alternative
For interpreters, the State monad *is* the accumulator. Pure equivalent:
```haskell
evalAcc :: Env -> Expr -> (Int, Env)
evalAcc env (Lit n)     = (n, env)
evalAcc env (Assign x e) = let (v, env') = evalAcc env e
                           in  (v, (x, v) : env')
-- etc.
```
Threading by hand reveals what State is doing.

## Fold-style alternative
Define `foldExpr` once, then eval is a one-liner over the fold algebra. See `adt-translation-family.md` for the shape. Rarely used because most Expr ADTs vary across questions.

## Cross-family combinations
- this family + `adt-translation-family.md`: translate → simplify → eval pipeline
- this family + `state-counter-family.md`: alpha-renaming generates fresh names during eval
- this family + `writer-trace-family.md`: log every Let binding and Var lookup
- this family + `error-handling-family.md`: Maybe vs Either choice for error reporting

## QuickCheck universal attacks
- **No variables:** behaves like mutation 1's evalExpr.
- **Var with empty env:** Nothing / Left "undefined".
- **Nested Let same name:** inner shadows outer.
- **Var in let body refers to outer binding:** `Let "x" e (Var "x")` evaluates `e`.
- **Eval-after-substitution equivalence:** `eval env (subst sigma e) == eval (sigma applied to env) e`.
- **Free-bound separation:** `eval env e == eval (filter ((`elem` freeVars e) . fst) env) e`.

## Pitfalls (per mutation)
- M1: forgetting one arithmetic constructor.
- M2: appending to env instead of prepending (breaks shadowing).
- M3: confusing `Right` / `Left` direction.
- M4: misunderstanding what recursive let semantics actually requires.
- M5: missing the `if v2 == 0` check.
- M6: not using `local` for the Let case.
- M7: too easy — exam usually has a twist.
- M8: writing the invariant test but not enforcing it in eval.
- M9: not handling `Var` for undefined name.
- M10: thinking `freeVars (Let x e1 e2)` excludes `x` from both `e1` and `e2` (it only excludes from `e2`).


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — evalMaybeWithDefault (Maybe fallback default for unknown vars)

**Spec:** Same as canonical `eval :: Env -> Expr -> Maybe Int` but unknown variables fall back to a default value rather than failing.

**Type sig:** `evalWithDefault :: Int -> Env -> Expr -> Int`

```haskell
type Env = [(String, Int)]
data Expr = Num Int | Var String | Add Expr Expr | Mul Expr Expr

evalWithDefault :: Int -> Env -> Expr -> Int
evalWithDefault _ _   (Num n)   = n
evalWithDefault d env (Var x)   = case lookup x env of
                                    Just v  -> v
                                    Nothing -> d
evalWithDefault d env (Add l r) = evalWithDefault d env l + evalWithDefault d env r
evalWithDefault d env (Mul l r) = evalWithDefault d env l * evalWithDefault d env r
```

**What changes vs seed:** Drops the `Maybe` wrapper: failure becomes a default. Effect stack simplifies from `Reader + Maybe` to just `Reader`. Different effect stack.

**QC trap:** `d = 0` is sometimes implicit and sometimes wrong — for `Mul`, default 0 collapses any expression containing an unknown variable to 0. Document/clarify the default's semantics.

## See also

**Primary archetype:** [A08 env eval](../archetypes/A08-env-eval.md)
**Sibling families:** [error-handling](./error-handling-family.md)
**Cross-topic:** [expr × state](../cross-matrix/expr-x-state.md) · [expr × maybe](../cross-matrix/expr-x-maybe.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [maybe-either attacks](../quickcheck/maybe-either-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
