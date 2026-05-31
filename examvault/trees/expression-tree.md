<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [trees](./README.md) · **Expression Trees — `data Expr = ...`**

<!-- siblings:start -->
> **Peers:** [binary-tree](./binary-tree.md) · [bst-delete-trace](./bst-delete-trace.md) · [bst](./bst.md) · **expression-tree** · [rose-tree](./rose-tree.md) · [tree-counting](./tree-counting.md) · [tree-fold](./tree-fold.md) · [tree-functor](./tree-functor.md) · [tree-traversals](./tree-traversals.md) · [tree-validation](./tree-validation.md) · [tree-zipper](./tree-zipper.md)
<!-- siblings:end -->






# Expression Trees — `data Expr = ...`

Expression trees are mini-ASTs. They show up as: pure eval (problem 89), depth/size (90), Mock Q5 (Expr → Circuit translation, archetype A05), Let-binding interpreters (148), and the main interpreters/ family.

## The standard exam shape

```haskell
data Expr = Val Int                       -- literal integer
          | Add Expr Expr                 -- e + e'
          | Sub Expr Expr                 -- e - e'
          | Mul Expr Expr                 -- e * e'
          | Div Expr Expr                 -- e `div` e' (may fail!)
          | Neg Expr                      -- negate e
          | Var String                    -- variable reference
          | Let String Expr Expr          -- let x = e in body
          deriving (Show, Eq)
```
This is the "kitchen-sink" version. Real questions use a subset — Mock Q5 uses a *boolean* Expr (Var/Not/And/Or/Implies), problem 148 uses Lit/Var/Add/Mul/Let. **Read the question's declaration first.**

## eval — pure, no errors

```haskell
eval :: Expr -> Int
eval (Val n)     = n
eval (Add e1 e2) = eval e1 + eval e2
eval (Sub e1 e2) = eval e1 - eval e2
eval (Mul e1 e2) = eval e1 * eval e2
eval (Div e1 e2) = eval e1 `div` eval e2     -- crashes on div by 0
eval (Neg e)     = negate (eval e)
eval (Var _)     = error "free variable; use evalEnv"
eval (Let _ _ _) = error "Let needs an env"
```
Works fine if the Expr language is just `Val/Add/Sub/Mul/Neg`. Problem 89 stops here.

## evalMaybe — wrap failure in Maybe

```haskell
evalMaybe :: Expr -> Maybe Int
evalMaybe (Val n)     = Just n
evalMaybe (Neg e)     = negate <$> evalMaybe e
evalMaybe (Add e1 e2) = (+) <$> evalMaybe e1 <*> evalMaybe e2
evalMaybe (Sub e1 e2) = (-) <$> evalMaybe e1 <*> evalMaybe e2
evalMaybe (Mul e1 e2) = (*) <$> evalMaybe e1 <*> evalMaybe e2
evalMaybe (Div e1 e2) = do
    a <- evalMaybe e1
    b <- evalMaybe e2
    if b == 0 then Nothing else Just (a `div` b)
evalMaybe (Var _)     = Nothing
evalMaybe (Let _ _ _) = Nothing
```
The Applicative `<$> ... <*>` style is the cleanest way to lift a 2-arg op into Maybe. See [../monads/maybe.md](../monads/maybe.md).

## evalEnv — variable bindings via environment

```haskell
type Env = [(String, Int)]

evalEnv :: Env -> Expr -> Maybe Int
evalEnv _   (Val n)     = Just n
evalEnv env (Var x)     = lookup x env
evalEnv env (Neg e)     = negate <$> evalEnv env e
evalEnv env (Add e1 e2) = (+) <$> evalEnv env e1 <*> evalEnv env e2
evalEnv env (Sub e1 e2) = (-) <$> evalEnv env e1 <*> evalEnv env e2
evalEnv env (Mul e1 e2) = (*) <$> evalEnv env e1 <*> evalEnv env e2
evalEnv env (Div e1 e2) = do
    a <- evalEnv env e1
    b <- evalEnv env e2
    if b == 0 then Nothing else Just (a `div` b)
evalEnv env (Let x e1 body) = do
    v <- evalEnv env e1
    evalEnv ((x,v):env) body                 -- extend env, then eval body
```
The Let case is THE characteristic move: evaluate the binding, then evaluate the body in the *extended* environment.

This is problem 148 verbatim. See [../interpreters/env-eval.md](../interpreters/expr-reader.md) for the full archetype writeup.

## Structural functions (depth, size, vars)

```haskell
depth :: Expr -> Int
depth (Val _)       = 0
depth (Var _)       = 0
depth (Neg e)       = 1 + depth e
depth (Add e1 e2)   = 1 + max (depth e1) (depth e2)
depth (Sub e1 e2)   = 1 + max (depth e1) (depth e2)
depth (Mul e1 e2)   = 1 + max (depth e1) (depth e2)
depth (Div e1 e2)   = 1 + max (depth e1) (depth e2)
depth (Let _ e b)   = 1 + max (depth e) (depth b)
```

```haskell
size :: Expr -> Int
size (Val _)     = 1
size (Var _)     = 1
size (Neg e)     = 1 + size e
size (Add e1 e2) = 1 + size e1 + size e2
size (Sub e1 e2) = 1 + size e1 + size e2
size (Mul e1 e2) = 1 + size e1 + size e2
size (Div e1 e2) = 1 + size e1 + size e2
size (Let _ e b) = 1 + size e + size b
```

```haskell
vars :: Expr -> [String]
vars (Val _)     = []
vars (Var x)     = [x]
vars (Neg e)     = vars e
vars (Add e1 e2) = vars e1 ++ vars e2
vars (Sub e1 e2) = vars e1 ++ vars e2
vars (Mul e1 e2) = vars e1 ++ vars e2
vars (Div e1 e2) = vars e1 ++ vars e2
vars (Let _ e b) = vars e ++ vars b
-- doesn't deduplicate; use `nub . vars` if you need a set
-- doesn't handle scoping; for free-vars you remove `x` from `vars b`
```

```haskell
freeVars :: Expr -> [String]
freeVars (Val _)     = []
freeVars (Var x)     = [x]
freeVars (Neg e)     = freeVars e
freeVars (Add e1 e2) = freeVars e1 `union` freeVars e2
freeVars (Sub e1 e2) = freeVars e1 `union` freeVars e2
freeVars (Mul e1 e2) = freeVars e1 `union` freeVars e2
freeVars (Div e1 e2) = freeVars e1 `union` freeVars e2
freeVars (Let x e b) = freeVars e `union` (freeVars b \\ [x])
-- `import Data.List (union, (\\))`
```

## simplify — constant folding + algebraic identities

```haskell
simplify :: Expr -> Expr
simplify (Val n)     = Val n
simplify (Var x)     = Var x
simplify (Neg e)     = case simplify e of
    Val n  -> Val (negate n)
    Neg e' -> e'                                          -- double-negation
    e'     -> Neg e'

simplify (Add e1 e2) = case (simplify e1, simplify e2) of
    (Val 0, e')   -> e'                                    -- 0 + e = e
    (e', Val 0)   -> e'
    (Val a, Val b) -> Val (a + b)                          -- constant fold
    (e', e'')     -> Add e' e''

simplify (Sub e1 e2) = case (simplify e1, simplify e2) of
    (e', Val 0)   -> e'                                    -- e - 0 = e
    (Val a, Val b) -> Val (a - b)
    (e', e'')     -> Sub e' e''

simplify (Mul e1 e2) = case (simplify e1, simplify e2) of
    (Val 0, _)    -> Val 0                                 -- 0 * e = 0
    (_, Val 0)    -> Val 0
    (Val 1, e')   -> e'                                    -- 1 * e = e
    (e', Val 1)   -> e'
    (Val a, Val b) -> Val (a * b)
    (e', e'')     -> Mul e' e''

simplify (Div e1 e2) = case (simplify e1, simplify e2) of
    (e', Val 1)              -> e'                         -- e / 1 = e
    (Val 0, _)               -> Val 0                      -- 0 / e = 0  (assumes e ≠ 0)
    (Val a, Val b) | b /= 0  -> Val (a `div` b)
    (e', e'')                -> Div e' e''

simplify (Let x e b) = Let x (simplify e) (simplify b)
```
Note: this is a **one-pass** simplifier. To reach a fixed point, iterate until `simplify e == e`.

## derivative — symbolic differentiation w.r.t. a variable

```haskell
deriv :: String -> Expr -> Expr
deriv _ (Val _)     = Val 0
deriv v (Var x)     | v == x    = Val 1
                    | otherwise = Val 0
deriv v (Neg e)     = Neg (deriv v e)
deriv v (Add e1 e2) = Add (deriv v e1) (deriv v e2)
deriv v (Sub e1 e2) = Sub (deriv v e1) (deriv v e2)
deriv v (Mul e1 e2) =                                       -- product rule
    Add (Mul (deriv v e1) e2)
        (Mul e1 (deriv v e2))
deriv v (Div e1 e2) =                                       -- quotient rule
    Div (Sub (Mul (deriv v e1) e2)
             (Mul e1 (deriv v e2)))
        (Mul e2 e2)
deriv _ (Let _ _ _) = error "deriv on Let: do substitution first"

-- usual pipeline:  simplify . deriv "x"
```

## Pretty printer (with precedence)

```haskell
instance Show Expr where
  showsPrec _ (Val n)     = shows n
  showsPrec _ (Var x)     = showString x
  showsPrec p (Neg e)     = showParen (p > 10) $
      showString "-" . showsPrec 11 e
  showsPrec p (Add e1 e2) = showParen (p > 6) $
      showsPrec 6 e1 . showString " + " . showsPrec 7 e2
  showsPrec p (Sub e1 e2) = showParen (p > 6) $
      showsPrec 6 e1 . showString " - " . showsPrec 7 e2
  showsPrec p (Mul e1 e2) = showParen (p > 7) $
      showsPrec 7 e1 . showString " * " . showsPrec 8 e2
  showsPrec p (Div e1 e2) = showParen (p > 7) $
      showsPrec 7 e1 . showString " / " . showsPrec 8 e2
  showsPrec p (Let x e b) = showParen (p > 0) $
      showString "let " . showString x . showString " = "
      . showsPrec 0 e . showString " in " . showsPrec 0 b
```
Precedence levels match Haskell's: `+ -` at 6 (left-assoc), `* /` at 7, unary `-` at 10. Use `showParen` to add parens only when binding is *looser* than the surrounding context.

The simpler always-parenthesised version (matches Data2.md lecture):
```haskell
showExpr :: Expr -> String
showExpr (Val n)     = show n
showExpr (Var x)     = x
showExpr (Neg e)     = "negate(" ++ showExpr e ++ ")"
showExpr (Add e1 e2) = "(" ++ showExpr e1 ++ "+" ++ showExpr e2 ++ ")"
showExpr (Sub e1 e2) = "(" ++ showExpr e1 ++ "-" ++ showExpr e2 ++ ")"
showExpr (Mul e1 e2) = "(" ++ showExpr e1 ++ "*" ++ showExpr e2 ++ ")"
showExpr (Div e1 e2) = "(" ++ showExpr e1 ++ "/" ++ showExpr e2 ++ ")"
showExpr (Let x e b) = "let " ++ x ++ " = " ++ showExpr e ++ " in " ++ showExpr b
```

## Mock Q5 hint — Expr → Circuit translation (archetype A05)

Mock Q5 has a **boolean** Expr (Var Char / Not / And / Or / Implies) and a Circuit type with only Input and Nand. You translate one ADT into another by recursion, exploiting identities:

```haskell
data Expr    = Var Char | Not Expr | And Expr Expr | Or Expr Expr | Implies Expr Expr
data Circuit = Input Char | Nand Circuit Circuit

circuit :: Expr -> Circuit
circuit (Var x)         = Input x
circuit (Not e)         = let c = circuit e in Nand c c              -- ¬p = p ⊼ p
circuit (And e1 e2)     = let n = Nand (circuit e1) (circuit e2)
                          in  Nand n n                                -- p ∧ q = ¬(p⊼q)
circuit (Or e1 e2)      = circuit (Not (And (Not e1) (Not e2)))      -- p ∨ q = ¬((¬p)∧(¬q))
circuit (Implies e1 e2) = circuit (Or (Not e1) e2)                   -- p ⇒ q = (¬p) ∨ q
```
Two valid styles: (a) translate directly to Circuit (And/Or/Implies cases), or (b) reduce to Not+And first then translate. The lecture solution mixes both.

Full walk-through in [../archetypes/05-adt-translation.md](../archetypes/A05-adt-translation.md). Translation is a recurring archetype — Mock Q5 is the same shape as `ramify`/`tabulate` (Assignment 2, problem 146).

## QuickCheck attack surface

```haskell
-- generators
instance Arbitrary Expr where
  arbitrary = sized go
    where
      go 0 = oneof [Val <$> arbitrary, Var <$> (pure "x")]
      go n = oneof
        [ Val <$> arbitrary
        , Neg <$> go (n-1)
        , Add <$> go (n `div` 2) <*> go (n `div` 2)
        , Sub <$> go (n `div` 2) <*> go (n `div` 2)
        , Mul <$> go (n `div` 2) <*> go (n `div` 2)
        ]

-- properties
prop_simplifyEval e          = evalMaybe e == evalMaybe (simplify e)
prop_simplifyShrinks e       = size (simplify e) <= size e
prop_simplifyIdempotent e    = simplify (simplify e) == simplify e
prop_evalNegDouble e         = evalMaybe (Neg (Neg e)) == evalMaybe e
prop_addCommutes e1 e2       = evalMaybe (Add e1 e2) == evalMaybe (Add e2 e1)
prop_evalEnvOK env e         = let f = freeVars e
                               in all (`elem` map fst env) f
                                  ==> isJust (evalEnv env e)
```

## Mutations (this is fertile ground for examiners)

| Mutation | What changes |
|----------|--------------|
| Add `Pow Expr Expr` | new constructor; update eval/simplify/depth/etc. (each fn grows by one clause) |
| Add `If Expr Expr Expr` | conditional; eval needs `Bool` somehow — use `0 ≠ 0` as truth, or change `Int` to `Either Int Bool` |
| Switch to `Expr Double` and add `Sin/Cos` | parameterised type `Expr a` |
| Add side effects (`Print Expr`) | move from `Maybe` to `Writer [String]` or `IO` |
| Add mutable state (`Set Var Expr` + `Get Var`) | move to `State Env` |
| Throw on Var-not-found instead of Nothing | move to `Either String` or `MonadError` |
| Static type-check before eval | second pass `typecheck :: Expr -> Maybe Type` |

Each of these slides Expr into a richer interpreter category. See [../interpreters/](../interpreters/) for the spectrum.

## Pitfalls

- `eval (Div e1 e2)` crashes when `eval e2 == 0`. Always use `evalMaybe` if Div is in the language.
- `Let` shadowing: `Let x e1 (Let x e2 body)` — inner binding wins; the env-prepend `(x,v):env` and `lookup` getting the first match handles this correctly.
- Free vs. bound vars: `vars (Let "x" e b)` is `vars e ++ vars b` (includes the bound x). `freeVars (Let "x" e b)` is `freeVars e \\ vars b` removed — use `union` and `\\` from Data.List.
- `simplify` is one-pass; nested simplifications may not reach a normal form. Iterate `until (\e -> simplify e == e)` if needed.
- Don't forget the `Var` and `Let` cases when adding new structural ops — easy to leave them out and get a compile warning about non-exhaustive patterns.
- Pretty-printer precedence: get `Sub` wrong (right-assoc by mistake) and `1 - 2 - 3` prints as `1 - (2 - 3)` which evaluates to `2`, not `-4`.

## Cross-references

- Interpreter family (simple → env → MonadError → multi-effect): [../interpreters/](../interpreters/)
- Env-eval archetype walkthrough: [../archetypes/08-env-eval.md](../archetypes/A08-env-eval.md)
- ADT translation (Mock Q5): [../archetypes/05-adt-translation.md](../archetypes/A05-adt-translation.md)
- Maybe monad / Applicative lifting: [../monads/maybe.md](../monads/maybe.md)
- Parser → AST (problem 142): [../archetypes/16-parser.md](../archetypes/A16-parser-combinators.md)
- Lecture: `fp-learning-2025/files/LectureNotes/Sections/Data2.md` §Expression trees
- Problems: 89 (evalExpr), 90 (depthExpr), 145 (Mock Q5 circuit), 148 (evalWithEnv)

## See also

**Archetypes:** [A05 ADT translation](../archetypes/A05-adt-translation.md) · [A08 env eval](../archetypes/A08-env-eval.md)
**Cross-topic:** [expr × maybe](../cross-matrix/expr-x-maybe.md) · [expr × state](../cross-matrix/expr-x-state.md) · [expr × multi](../cross-matrix/expr-x-multi.md)
**Question families:** [adt-translation](../question-families/adt-translation-family.md) · [env-eval](../question-families/env-eval-family.md)
**QuickCheck:** [expr attacks](../quickcheck/expr-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
