<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 14 — Desugar pipeline (surface → core → eval)**

<!-- siblings:start -->
> **Peers:** **desugar-pipeline** · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 14 — Desugar pipeline (surface → core → eval)

**Effect:** translation, not evaluation
**Effect rationale:** instead of evaluating `Implies` (or `Let`, or `Or`) directly, you **rewrite** it into a smaller core language that already has the necessary primitives. Then you evaluate the core. Two phases: **desugar** and **eval**. Mock Q5 (`Expr -> Circuit`) is *the desugar phase only* — no eval.
**Type signature:** `desugar :: Surface -> Core`, then `eval :: Core -> result`
**Search keywords:** desugar · surface-core · two-phase · ADT-translation · Mock-Q5 · Implies · circuit · Nand · rewrite · normalize · expr-to-circuit

> **Recognise the question:** "translate this `Expr` into a `Circuit` using only `Nand`" — that's Mock Q5. **It's a desugar phase**: no input value, no environment, no monad. You're just rewriting one tree into another.

---

## The two-phase model

```
+----------+   desugar    +-------+    eval    +--------+
|  Surface | ----------> | Core  | ---------> | Value  |
+----------+              +-------+            +--------+
   has user-friendly      has minimal       interpreter
   ctors: Let, Or,        ctors: only       runs on Core
   Implies, While...      the essentials
```

The benefit of separating these:
- **Surface** grows freely with sugar for ergonomics.
- **Core** stays small, so `eval` is short and easy to verify.
- **Desugar** is a pure tree-to-tree translation, easy to test and prove.

---

## Mock Q5 — desugar Expr to Circuit

**Source** (`MockTestSolutions.hs` lines 90-95):

```haskell
data Expr    = Var Char
             | Not Expr
             | And Expr Expr
             | Or  Expr Expr
             | Implies Expr Expr
             deriving (Eq, Show)

data Circuit = Input Char
             | Nand Circuit Circuit
             deriving (Eq, Show)

circuit :: Expr -> Circuit
circuit (Var x)        = Input x
circuit (Not e)        = Nand (circuit e) (circuit e)
circuit (Or e1 e2)     = circuit (Not (And (Not e1) (Not e2)))
circuit (Implies e1 e2) = circuit (Or (Not e1) e2)
circuit (And e1 e2)    = let e = Nand (circuit e1) (circuit e2) in Nand e e
```

This is **all desugar**, no eval. We translate every Boolean primitive into NAND-only form because that's what Circuit knows about.

### Why each rewrite is correct

| Surface | Desugars to | Why |
|---|---|---|
| `Var x` | `Input x` | base case |
| `Not e` | `Nand e e` (after recursive desugar of `e`) | `Nand p p = ¬(p ∧ p) = ¬p` |
| `Or e1 e2` | desugar of `Not (And (Not e1) (Not e2))` | De Morgan: `e1 ∨ e2 = ¬(¬e1 ∧ ¬e2)` |
| `Implies e1 e2` | desugar of `Or (Not e1) e2` | `p → q = ¬p ∨ q` |
| `And e1 e2` | `let n = Nand (desugar e1) (desugar e2) in Nand n n` | `Nand n n = ¬n = ¬¬(p ∧ q) = p ∧ q` |

Notice `Or` and `Implies` use **recursive calls to `circuit`** on the rewritten surface form — they don't construct `Circuit` directly, they re-enter desugar with a simpler surface expression. This is the cleanest pattern for nested sugars.

### Pattern: "rewrite then desugar"
```haskell
circuit (BigSugar e1 e2 e3) = circuit (Equivalent ... e1 ... e2 ... e3 ...)
```
Use this when a sugar is naturally expressed as another sugar.

### Pattern: "build directly"
```haskell
circuit (PrimitiveSugar e1 e2) = Nand (circuit e1) (circuit e2)
```
Use this for sugars closest to the core, where you can construct the result without rewriting.

---

## Generic desugar template

```haskell
data Surface = Lit Int
             | Add Surface Surface
             | Sub Surface Surface
             | Neg Surface              -- sugar for 0 - e
             | Let String Surface Surface -- sugar for substitution
             deriving (Eq, Show)

data Core = CLit Int
          | CVar String
          | CAdd Core Core
          | CSub Core Core
          deriving (Eq, Show)

desugar :: Surface -> Core
desugar (Lit n)        = CLit n
desugar (Add e1 e2)    = CAdd (desugar e1) (desugar e2)
desugar (Sub e1 e2)    = CSub (desugar e1) (desugar e2)
desugar (Neg e)        = CSub (CLit 0) (desugar e)               -- 0 - e
desugar (Let x e1 e2)  = -- substitution-based: replace Var x in e2 with desugar e1
  substitute x (desugar e1) (desugar e2)

substitute :: String -> Core -> Core -> Core
substitute x v (CVar y)     | x == y    = v
                            | otherwise = CVar y
substitute x v (CLit n)     = CLit n
substitute x v (CAdd e1 e2) = CAdd (substitute x v e1) (substitute x v e2)
substitute x v (CSub e1 e2) = CSub (substitute x v e1) (substitute x v e2)

-- Then evaluate the Core (which is smaller / simpler):
eval :: Core -> Maybe Int        -- Maybe because CVar may be free
eval (CLit n)     = Just n
eval (CVar _)     = Nothing       -- free variable
eval (CAdd e1 e2) = do x <- eval e1; y <- eval e2; return (x + y)
eval (CSub e1 e2) = do x <- eval e1; y <- eval e2; return (x - y)
```

The user writes `desugar then eval`:
```haskell
run :: Surface -> Maybe Int
run = eval . desugar
```

---

## Worked example: `Let "x" (Lit 5) (Add (Var "x") (Lit 3))`

```
desugar (Let "x" (Lit 5) (Add (Var "x") (Lit 3)))
  = substitute "x" (CLit 5) (desugar (Add (Var "x") (Lit 3)))
  = substitute "x" (CLit 5) (CAdd (CVar "x") (CLit 3))
  = CAdd (CLit 5) (CLit 3)

eval (CAdd (CLit 5) (CLit 3))
  = do x <- eval (CLit 5)        -- Just 5
       y <- eval (CLit 3)        -- Just 3
       return (5 + 3)
  = Just 8
```

The Let was eliminated by substitution before evaluation. The Core never sees `Let`.

---

## Alternative: keep Let in Core (env-based)

You don't *have* to desugar `Let` — you can keep it and handle it with an env at eval time. The desugar approach is preferred when:
- The core has fewer ctors → simpler eval.
- You want to optimise the AST (constant folding, dead-code elimination) before evaluation.
- The core has a different runtime model (circuit, machine code, JIT).

For Mock Q5, the Core (`Circuit`) is *intentionally* tiny — only `Nand` and `Input`. Translation to it forces us to express everything via NAND, which is the point.

---

## Per-constructor breakdown for desugar
| Ctor | Rewrites to |
|---|---|
| **Base ctors** (Var, Lit, etc.) | wrap in matching core ctor |
| **Direct primitives** (And → Nand pattern) | construct core ctor with recursively-desugared args |
| **Sugar that's an alias** (Implies → Or after Not) | call `desugar` on the rewritten surface form |
| **Sugar that's a substitution** (Let) | apply `substitute` to the body |

---

## Mutations
- **Add another sugar.** E.g. `Xor e1 e2` desugars to `Or (And e1 (Not e2)) (And (Not e1) e2)` then recursively. One new clause in `desugar`.
- **Make desugar fail.** `desugar :: Surface -> Maybe Core` if some surface forms are invalid (e.g. shadowing prohibited).
- **Add a normaliser.** After desugar, run a `simplify :: Core -> Core` that constant-folds `CAdd (CLit 1) (CLit 2)` to `CLit 3`. Composition: `simplify . desugar`.
- **Combine desugar with type-check.** `desugar :: Surface -> Either TypeError Core` runs both passes.

---

## Pitfalls
- **Forgetting to recursively desugar sub-trees.** `circuit (Not e) = Nand e e` is **wrong** — should be `Nand (circuit e) (circuit e)`.
- **Confusing surface and core ctors.** When the surface and core have similar names, prefix one (e.g. `CAdd` vs `Add`) to avoid clashing.
- **Re-evaluating sub-trees.** In Mock Q5's `Not`, `Nand (circuit e) (circuit e)` evaluates `e` *twice* if you're not careful — fine for circuits (they're just data), but for *expressions with side effects* you'd want a `let`.
- **Mistaking desugar for eval.** Mock Q5 produces a `Circuit`, not a `Bool`. The result is still a tree.
- **Substitution and variable capture.** If you desugar `Let x (Var "y") (Lam "y" (Var "x"))`, naive substitution captures `y`. The exam usually avoids this by not testing capture; if you must, use fresh names.
- **Desugar-into-itself recursion.** `desugar (Implies e1 e2) = desugar (Or (Not e1) e2)` — make sure this terminates. It does because `Or (Not e1) e2` is a *smaller* surface tree (no Implies).
- **Treating desugar as monadic.** It usually isn't — it's a pure tree-to-tree function. Don't reach for `Maybe` or `State` unless the spec requires.

---

## QuickCheck attacks
- Mock Q5: `evalCircuit (circuit e) env == evalExpr e env` — desugar must preserve semantics.
- Termination: `circuit` always halts (every recursive call is on a strictly smaller tree).
- Size: `size (circuit e) <= 4 * size e` or similar bound — circuits expand by a constant factor.
- Shape: `circuit (Var x) == Input x`, `circuit (Not (Not e)) == Nand n n` where `n = Nand n' n'` — double-Not desugars to four NANDs.
- For Let-style: `desugar (Let x e1 e2)` must evaluate to the same value as `e2` with `x = e1`.

---

## See also

**Archetypes:** [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Question families:** [env-eval](../question-families/env-eval-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)
**Related (interpreters):** [extend interpreter](./extend-interpreter.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
