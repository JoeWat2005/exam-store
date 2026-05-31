<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: expression trees (Expr, Circuit, propositional)**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · **expr** · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: expression trees (Expr, Circuit, propositional)

**Search keywords:** Expr, Var, Not, And, Or, Implies, Circuit, Input, Nand, semExpr, semCirc, semantic equivalence, propositional logic, Mock Q5, circuit, only Not, only And, free of

The Mock Test Q5 is the canonical expression-tree question. Translates `Expr` to a NAND-only `Circuit`. The marker checks **semantic equivalence**, not structural equality, which is the key insight.

## What the marker generates

Direct from `MockTestTestCases.hs`:

```haskell
data Expr = Var Char | Not Expr | And Expr Expr | Or Expr Expr | Implies Expr Expr

-- Variables limited to a..f (so QC can enumerate all 64 assignments):
arbitraryVar = elements ['a'..'f'] >>= return . Var

-- Size-bounded recursive generator:
sizedArbitraryExpr 0 = arbitraryVar
sizedArbitraryExpr n = frequency
    [ (3, arbitraryVar)             -- 3x more often a Var
    , (2, genCon And)
    , (2, genCon Or)
    , (2, genCon Implies)
    , (2, genNeg) ]
  where genCon c = c <$> sizedArbitraryExpr (n `div` 2) <*> sizedArbitraryExpr (n `div` 2)
        genNeg   = Not <$> sizedArbitraryExpr (n - 1)

-- Top-level: n drawn from 1..7
arbitrary = elements [1..7] >>= sizedArbitraryExpr

-- For specialised tests:
arbitraryExprOnlyNot = chooseInt (0, 9) >>= sizedArbitraryExprOnlyNot   -- nested Not chains
arbitraryExprOnlyAnd = chooseInt (0, 18) >>= sizedArbitraryExprOnlyAnd  -- And-only, depth up to 18!
arbitraryExprFreeOf conn = chooseInt (0, 18) >>= sizedArbitraryExprFreeOf n conn  -- avoids ONE specific connective
```

So the marker tests:
- **Q5.1 (2 marks): `Not (Var x)`** — simplest non-trivial case.
- **Q5.2-4 (6 marks): `And/Or/Implies (Var x) (Var y)`** — single binary connective at root.
- **Q5.5 (4 marks): only `And` connectives, depth up to 18.**
- **Q5.6-7 (8 marks): expressions free of one specific connective.**

The semantic check tries EVERY assignment of T/F to every variable mentioned:

```haskell
tryToRefuteEquivalence c e =
  catMaybes $ (\ctx -> if semCirc c ctx == semExpr e ctx then Nothing else Just ctx)
              <$> allSublists is
  where is = nub (inputs c ++ vars e)
```

`allSublists is` enumerates `2^|is|` contexts. With 6 vars, that's 64 contexts — exhaustive.

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | `Var x` alone | `Var 'a'` | Spec: usually `circuit (Var x) = Input x`. If you wrap it weirdly, semantics still pass — but the marker may not test single-Var as a primary test, just as a base case | `circuit (Var x) = Input x` |
| 2 | `Not (Var x)` | `Not (Var 'a')` | Need `Nand (Input x) (Input x)` (since `not p = nand p p`). Forgetting this kills 2 marks. | `circuit (Not e) = let c = circuit e in Nand c c` |
| 3 | `And (Var x) (Var y)` | `And (Var 'a') (Var 'b')` | `and p q = not (nand p q) = nand (nand p q) (nand p q)`. | `circuit (And p q) = let n = Nand (circuit p) (circuit q) in Nand n n` |
| 4 | `Or (Var x) (Var y)` | `Or (Var 'a') (Var 'b')` | `or p q = nand (not p) (not q) = nand (nand p p) (nand q q)`. | `circuit (Or p q) = Nand (Nand (circuit p) (circuit p)) (Nand (circuit q) (circuit q))` |
| 5 | `Implies (Var x) (Var y)` | `Implies (Var 'a') (Var 'b')` | `implies p q = or (not p) q = nand p (not q) = nand p (nand q q)`. | `circuit (Implies p q) = Nand (circuit p) (Nand (circuit q) (circuit q))` |
| 6 | Nested `Not (Not (... (Var x)))` | depth 9 | If you don't recurse on the inner expression, you crash | `circuit (Not e) = ... circuit e ...` (recursion is structural) |
| 7 | Deep `And`-only chain | depth 18 | Stack overflow rare; QC's `chooseInt (0, 18)` and `div 2` keep depth bounded | OK as long as recursion is structural |
| 8 | "Free of `And`" — only Or/Implies/Not | various | Tests that you handle the OTHER connectives correctly | Make sure each constructor has a case |
| 9 | "Free of `Or`" — only And/Implies/Not | various | Same | Same |
| 10 | "Free of `Implies`" — only And/Or/Not | various | Same | Same |
| 11 | `Var '0'` or other unusual chars | unlikely but `vars` collects them | `Input` preserves the char | Pass through |
| 12 | Repeated variable | `And (Var 'a') (Var 'a')` | Semantically should be `Var 'a'`. Your circuit's semantics must still match. | Don't try to simplify — just translate structurally |
| 13 | Constant-true after simplification | `Or (Var 'a') (Not (Var 'a'))` | Tautology — your circuit must equal True under all assignments | Don't simplify; translate. The structural translation gives a circuit that evaluates correctly. |
| 14 | Constant-false: `And p (Not p)` | contradiction | Same — must evaluate to False | Same |
| 15 | Non-exhaustive patterns | forgot one of Var/Not/And/Or/Implies | Marker uses ALL constructors | `circuit` MUST have a case for each |

## The 5 essential translations

Memorise these. They're the entire question.

| Connective | Boolean identity | NAND translation |
|------------|------------------|------------------|
| `not p` | `not p = nand p p` | `Nand p p` |
| `p && q` | `and p q = not (nand p q)` | `Nand (Nand p q) (Nand p q)` |
| `p \|\| q` | `or p q = nand (not p) (not q)` | `Nand (Nand p p) (Nand q q)` |
| `p ==> q` | `implies p q = or (not p) q = nand p (not q)` | `Nand p (Nand q q)` |
| `Var x` | itself | `Input x` |

Worked translation:
```haskell
circuit :: Expr -> Circuit
circuit (Var x)         = Input x
circuit (Not e)         = let c = circuit e in Nand c c
circuit (And p q)       = let cp = circuit p
                              cq = circuit q
                              n  = Nand cp cq
                          in  Nand n n
circuit (Or p q)        = Nand (Nand (circuit p) (circuit p))
                               (Nand (circuit q) (circuit q))
circuit (Implies p q)   = Nand (circuit p)
                               (Nand (circuit q) (circuit q))
```

## Property templates

```haskell
import Test.QuickCheck
import Data.List (nub)

-- Semantic equivalence check (what the marker actually uses)
semCirc :: Circuit -> [Char] -> Bool
semCirc (Input x)    ctx = x `elem` ctx
semCirc (Nand c1 c2) ctx = not (semCirc c1 ctx && semCirc c2 ctx)

semExpr :: Expr -> [Char] -> Bool
semExpr (Var x)       ctx = x `elem` ctx
semExpr (Not e)       ctx = not (semExpr e ctx)
semExpr (And p q)     ctx = semExpr p ctx && semExpr q ctx
semExpr (Or p q)      ctx = semExpr p ctx || semExpr q ctx
semExpr (Implies p q) ctx = not (semExpr p ctx) || semExpr q ctx

allContexts :: [Char] -> [[Char]]
allContexts cs = subsequences cs
  where subsequences []     = [[]]
        subsequences (c:cs) = let s = subsequences cs in s ++ map (c:) s

prop_circuitEquivalent :: Expr -> Bool
prop_circuitEquivalent e =
  let c   = circuit e
      cs  = nub (varsExpr e ++ inputsCirc c)
  in  all (\ctx -> semCirc c ctx == semExpr e ctx) (allContexts cs)
  where
    varsExpr (Var x)       = [x]
    varsExpr (Not e)       = varsExpr e
    varsExpr (And p q)     = varsExpr p ++ varsExpr q
    varsExpr (Or p q)      = varsExpr p ++ varsExpr q
    varsExpr (Implies p q) = varsExpr p ++ varsExpr q
    inputsCirc (Input x)    = [x]
    inputsCirc (Nand c1 c2) = inputsCirc c1 ++ inputsCirc c2

-- Specific easy cases
prop_circuit_notVar :: Char -> Bool
prop_circuit_notVar c = prop_circuitEquivalent (Not (Var c))

prop_circuit_andVars :: Char -> Char -> Bool
prop_circuit_andVars c1 c2 = prop_circuitEquivalent (And (Var c1) (Var c2))
```

## Self-test before submission checklist

- [ ] `circuit (Var x)` returns `Input x` (or equivalent)
- [ ] `circuit (Not (Var x))` evaluates to NOT x under all assignments
- [ ] `circuit (And (Var 'a') (Var 'b'))` evaluates to `a && b` under all 4 assignments
- [ ] `circuit (Or (Var 'a') (Var 'b'))` evaluates to `a \|\| b` under all 4 assignments
- [ ] `circuit (Implies (Var 'a') (Var 'b'))` evaluates to `not a \|\| b` under all 4 assignments
- [ ] `circuit (Not (Not (Var 'a')))` evaluates to `a`
- [ ] All five constructors (Var/Not/And/Or/Implies) have a case
- [ ] Function recurses on subexpressions (no shallow translation)
- [ ] No `error` / `undefined`
- [ ] Polymorphic? No — Expr is concrete with `Char` variables

## Pitfalls that specifically lose QC marks

### Pitfall: forgetting one connective
```haskell
-- WRONG: missed Implies
circuit (Var x)   = Input x
circuit (Not e)   = ...
circuit (And p q) = ...
circuit (Or p q)  = ...
-- For Implies (Var 'a') (Var 'b'): non-exhaustive pattern → error
-- Marker test fails with the smallest Implies counterexample.
```

### Pitfall: structural copy-paste bug
From the user's own `final10.hs` (exact bug, ~5 marks lost):
```haskell
-- WRONG: copy-paste, forgot to change p to q
circuit (Or p q) = Nand np nq
  where np = Nand (circuit p) (circuit p)
        nq = Nand (circuit p) (circuit p)   -- ← should be 'q'!
-- This computes Or p p = p, which is wrong for any q ≠ p.
-- Fix: re-derive each case from the boolean identity.
```

### Pitfall: simplifying instead of translating
```haskell
-- WRONG: tries to simplify Not (Not e) to e
circuit (Not (Not e)) = circuit e
circuit (Not e)       = let c = circuit e in Nand c c
-- This works! But it's brittle:
-- If a deeper Not (Not (Not (Var x))) comes in,
-- the outer Not matches, recurses to circuit (Not (Not (Var x))),
-- which matches the first clause and gives circuit (Var x) = Input x — OK
-- BUT: if there's any rewriting bug, you lose semantic equivalence.
-- SAFE: structural translation only.
```

### Pitfall: thinking the marker rewards "small" circuits
The semantic check just checks equivalence over all contexts. Your circuit can have 10,000 Nands and still score full marks **iff** it computes the same Boolean function. Don't optimise; correctness first.

### Pitfall: re-using `circuit p` not knowing it's recomputed
```haskell
circuit (And p q) = Nand (Nand (circuit p) (circuit q)) (Nand (circuit p) (circuit q))
-- Here `circuit p` and `circuit q` appear twice each. Haskell is lazy so it
-- might or might not be shared. Either way, the marker only checks SEMANTICS,
-- not structure. Both are fine.

-- Cleaner with `let`:
circuit (And p q) =
  let cp = circuit p
      cq = circuit q
      n  = Nand cp cq
  in  Nand n n
```

### Pitfall: missing `Var` base case
```haskell
-- WRONG: only handles compound expressions
circuit (Not e)   = ...
circuit (And p q) = ...
-- For Var 'a' alone: non-exhaustive
-- Fix: ALWAYS include circuit (Var x) = Input x first
```

### Pitfall: `Eq Circuit` may not exist in the spec
The Mock Test marker uses **semantic equivalence**, not `Eq`. Even if `Circuit` has `deriving Eq`, the marker doesn't use it on `circuit` (it does derive Eq in Mock Q5 — for the `==` checks in error messages — but the test asks `semCirc c ctx == semExpr e ctx`).

## See also

**Archetypes:** [A05 ADT translation](../archetypes/A05-adt-translation.md) · [A08 env eval](../archetypes/A08-env-eval.md)
**Cross-topic:** [expr × maybe](../cross-matrix/expr-x-maybe.md) · [expr × state](../cross-matrix/expr-x-state.md)
**Question families:** [adt-translation](../question-families/adt-translation-family.md) · [env-eval](../question-families/env-eval-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
