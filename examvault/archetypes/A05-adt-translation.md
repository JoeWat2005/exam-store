<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A05 — ADT-to-ADT Translation**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · **A05** · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A05 — ADT-to-ADT Translation

**Tier:** 1   |   **Stars:** ⭐⭐⭐⭐
**Mock appearance:** Q5   |   **Assignment appearance:** A2 (Code/Tree/Table interconvert)
**Combines with:** A01 · A08 · A12 · A19
**Search keywords:** translate · desugar · NAND · normalise · remove · convert AST · Expr -> Circuit · syntax simplification

## What it tests
Whether you can map every constructor of source ADT to a (potentially deeper) shape in the target ADT, recursing on sub-trees, and using `let`/`where` to share repeated subexpressions when the rewrite duplicates them.

## Recognition triggers
- Two ADTs are defined: source has many constructors, target has fewer
- "transform an expression into a circuit", "remove `Implies` and `Or`", "desugar into a core language"
- Type signature: `Source -> Target` where both are recursive
- The question provides **algebraic identities** to use (e.g. `¬p = p⊼p`, `p∧q = ¬(p⊼q)`)
- The expected output of an example is **much longer than the input** — duplication hints at NAND-style reduction.

## Canonical template
```haskell
data Source = SCtor1 ... | SCtor2 Source Source | ...
data Target = TCtor1 ... | TCtor2 Target Target | ...

translate :: Source -> Target
translate (SCtor1 x)      = TCtor1 (translate x)               -- 1-to-1
translate (SCtor2 e1 e2)  = TCtor2 (translate e1) (translate e2)
translate (SCtor3 e1 e2)  = let a = translate e1               -- share!
                                b = translate e2
                            in TCtor2 (TCtor2 a b) (TCtor1 a)
```

## Mutations (the examiner picks one)

### M1 — `circuit :: Expr -> Circuit` (Mock Q5, NAND-only)
```haskell
data Expr    = Var Char | Not Expr | And Expr Expr | Or Expr Expr | Implies Expr Expr
data Circuit = Input Char | Nand Circuit Circuit

circuit :: Expr -> Circuit
circuit (Var x)       = Input x
circuit (Not e)       = let c = circuit e in Nand c c
circuit (And e1 e2)   = let a = Nand (circuit e1) (circuit e2)
                        in Nand a a
circuit (Or e1 e2)    = circuit (Not (And (Not e1) (Not e2)))
circuit (Implies e1 e2) = circuit (Or (Not e1) e2)
```
What changes: nothing — this IS canonical. Note `Or`/`Implies` recurse via `circuit` (so the new sub-Expr is itself translated); `And`/`Not` build `Nand` directly. **Share `circuit e` once, then duplicate the Nand argument** to avoid exponential blow-up if `e` is huge.

### M2 — remove `Implies` only (single-pass simplifier)
```haskell
data Logic = LVar Char | LNot Logic | LAnd Logic Logic | LOr Logic Logic | LImp Logic Logic

removeImplies :: Logic -> Logic
removeImplies (LVar x)     = LVar x
removeImplies (LNot e)     = LNot (removeImplies e)
removeImplies (LAnd a b)   = LAnd (removeImplies a) (removeImplies b)
removeImplies (LOr a b)    = LOr  (removeImplies a) (removeImplies b)
removeImplies (LImp a b)   = LOr (LNot (removeImplies a)) (removeImplies b)
```
What changes: target type = source type; only one constructor is rewritten. Recursion on every constructor is mandatory.

### M3 — desugar `Let` into lambda + apply (lambda calculus)
```haskell
data Sugar = SLit Int | SVar String | SAdd Sugar Sugar | SLet String Sugar Sugar
data Core  = CLit Int | CVar String | CAdd Core Core   | CLam String Core | CApp Core Core

desugar :: Sugar -> Core
desugar (SLit n)        = CLit n
desugar (SVar x)        = CVar x
desugar (SAdd a b)      = CAdd (desugar a) (desugar b)
desugar (SLet x e1 e2)  = CApp (CLam x (desugar e2)) (desugar e1)
```
What changes: `Let` translates to `(λx. body) arg` — Core has no Let. Lambda and App are new in target.

### M4 — De Morgan push (`Not` propagation)
```haskell
pushNot :: Logic -> Logic
pushNot (LNot (LNot e))    = pushNot e
pushNot (LNot (LAnd a b))  = LOr  (pushNot (LNot a)) (pushNot (LNot b))
pushNot (LNot (LOr a b))   = LAnd (pushNot (LNot a)) (pushNot (LNot b))
pushNot (LNot e)           = LNot (pushNot e)
pushNot (LVar x)           = LVar x
pushNot (LAnd a b)         = LAnd (pushNot a) (pushNot b)
pushNot (LOr a b)          = LOr  (pushNot a) (pushNot b)
```
What changes: deeper pattern-matching (`LNot (LAnd a b)`) — recursion looks two ctors deep.

### M5 — CNF normalisation (multi-pass)
```haskell
toCNF :: Logic -> Logic
toCNF = distribute . pushNot . removeImplies
```
What changes: composition of three simpler translators; emphasises function composition `.`.

### M6 — `Code -> [(Char, Code)]` (A2-style table from concat)
```haskell
data Atom = Beep | Silence

tabulateCode :: [Atom] -> [(Char, [Atom])]
tabulateCode = ...    -- requires lookup of word-boundary; non-trivial
```
What changes: simpler — usually the codec direction A07.

### M7 — `Either` → `Maybe` (lossy translation)
```haskell
data E a b = LeftE a | RightE b
toMaybe :: E a b -> Maybe b
toMaybe (LeftE _)  = Nothing
toMaybe (RightE b) = Just b
```
What changes: non-recursive, but the principle (one clause per constructor) is the same.

### M8 — Binary tree → Rose tree
```haskell
toRose :: BT a -> Rose (Maybe a)
toRose Empty        = Leaf Nothing
toRose (Fork x l r) = Branch [Leaf (Just x), toRose l, toRose r]
```
What changes: re-encode in a new shape; the wider container needs `Maybe` to handle holes.

### M9 — Drop precedence: `Sugar` (with prec hints) → `Core` (flat)
```haskell
data Token = T_LPAREN | T_RPAREN | T_NUM Int | T_PLUS | T_TIMES
forget :: Expr -> [Token]
forget (Val n)     = [T_NUM n]
forget (Add a b)   = forget a ++ [T_PLUS] ++ forget b
forget (Mul a b)   = [T_LPAREN] ++ forget a ++ [T_TIMES] ++ forget b ++ [T_RPAREN]
```
What changes: target is a flat list, not a tree — same per-constructor structure, but combine with `++`.

### M10 — Circuit → Expr (the reverse of Mock Q5)
```haskell
exprOf :: Circuit -> Expr
exprOf (Input x)    = Var x
exprOf (Nand a b)   = Not (And (exprOf a) (exprOf b))
```
What changes: target has more constructors than source; one clause per source constructor.

## Worked examples from this course
- Mock Q5: `circuit :: Expr -> Circuit` — M1.
- Problem sheet Set 15 (#145): same `circuit` repeated.
- Problem sheet Set 9 (#89-90): `evalExpr` and `depthExpr` — eval-style, not translation, but same per-ctor pattern.
- Assignment 2: `ramify`, `tabulate` — translation between `Table` and `Tree` reps.
- Assignment 3 Q1: `toRose`, `fromRose` — translation between `Free [] a` and `Rose a` reps.

## QuickCheck attack surface
- **Smallest input per constructor**: `Var 'p'`, `Not (Var 'p')`, `And (Var 'p') (Var 'q')`, etc. Every constructor must have a clause; if you missed `Implies`, the marker forces a `Non-exhaustive` crash.
- **Deeply nested**: `Implies (Implies p q) r` — checks you recurse correctly into both halves.
- **Equivalence**: the marker may evaluate both sides with a truth-value environment and compare. For circuit: `evalExpr env e == evalCircuit env (circuit e)` for all envs. If your `Or` rewrite is wrong on one truth row, you lose marks.
- **No exponential blow-up**: marker may time out on `And (Var 'p') (Var 'p')` repeated 10 levels deep. Sharing via `let` saves you.
- **Idempotence**: `removeImplies . removeImplies == removeImplies` — once Implies is gone, applying again is a no-op.

## Pitfalls (marks-killers)
- **Copy-paste bug**: `circuit (Or e1 e2) = Nand (Nand (circuit e1) (circuit e1)) (Nand (circuit e2) (circuit e2))` — `e1` not `e2`! Real bug in `final10.hs`. Use `let np = …; nq = …` and reference by name.
- **Forgetting a constructor**: missing the `Implies` clause means GHC warns of `Non-exhaustive patterns`. If `-fwarn-incomplete-patterns` is set (it is on the Mock), the marker shells out with a runtime crash.
- **Wrong identity**: `p ∨ q ≡ ¬((¬p) ∧ (¬q))` is De Morgan. Don't try to derive it on the fly — the question gives you the identities; use exactly those.
- **Exponential code**: `circuit (And e1 e2) = Nand (Nand a b) (Nand a b)` evaluates `Nand a b` twice if you write `Nand (circuit e1) (circuit e2)` twice. `let pq = …` then `Nand pq pq` makes it linear.
- **Recursing only at leaves**: `circuit (Not e) = Nand (Input ?) (Input ?)` — only correct if `e` is a `Var`. Use `circuit e`, not `Input <char>`.
- **Confusing target constructor names**: `Input` vs `Var`, `Nand` vs `And`. Easy to mistype.

## Combines-with deep dive

### A05 × A01 — translation on rose tree
```haskell
flatten :: Rose a -> Rose (Maybe a)
flatten (Leaf x)     = Leaf (Just x)
flatten (Branch xs)  = Branch (Leaf Nothing : map flatten xs)
```

### A05 × A08 — translate then eval
```haskell
evalAfterDesugar :: Env -> Sugar -> Maybe Int
evalAfterDesugar env = eval env . desugar
  where eval env (CLit n)   = Just n
        eval env (CVar x)   = lookup x env
        eval env (CAdd a b) = (+) <$> eval env a <*> eval env b
        -- … lambda, app
```

### A05 × A19 — translation as a pass in an interpreter
After adding `Implies` to the parser, route through `removeImplies` before reaching `eval`:
```haskell
runProgram :: String -> Maybe Bool
runProgram = fmap evalLogic . fmap removeImplies . parse logic
```

## See also

**Combines with:** [A01 tree recursion](./A01-tree-recursion.md) · [A06 functor instance](./A06-functor-instance.md) · [A07 codec pair](./A07-codec-pair.md) · [A20 laws / iso](./A20-laws-iso.md)
**Question families:** [adt-translation](../question-families/adt-translation-family.md) · [codec](../question-families/codec-family.md)
**Cross-topic:** [expr × maybe](../cross-matrix/expr-x-maybe.md) · [tree × either](../cross-matrix/tree-x-either.md)
**Theory:** [expression tree](../trees/expression-tree.md)
**Pitfalls:** [P-019 Mock Q5 p/q copy-paste](../pitfalls/HIGH-severity.md#p-019) · [P-016 functor shape break](../pitfalls/HIGH-severity.md#p-016)
**QuickCheck:** [codec attacks](../quickcheck/codec-attacks.md) · [expr attacks](../quickcheck/expr-attacks.md)
**Mock-Q:** [Mock Q5 circuit](../indexes/MOCK-Q-INDEX.md#mock-q5)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
