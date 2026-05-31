<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: adt-translation**

<!-- siblings:start -->
> **Peers:** **adt-translation** · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: adt-translation

**Archetype:** A09 (recursive descent over ADT, building another ADT)   |   **Stars:** ⭐⭐⭐⭐   |   **Course week(s):** 6–8
**Search keywords:** circuit, Expr→Circuit, Logic normalise, desugar, Nand, translate, ADT-to-ADT

## Generator template
```haskell
-- The seed: walk every constructor of input ADT `A`, mapping each to
-- some pattern of constructors in output ADT `B`. Recursion mirrors structure.
seed :: A -> B
seed (Cons1 x)     = OutCons1 (seed x)
seed (Cons2 x y)   = OutCons2 (seed x) (seed y)
seed Constant      = OutDefault
```

Mutations: pick an input language, an output language, and a translation rule. The classic exam example is the Nand circuit (mock Q5).

## Mutations (the examiner picks one)

### Mutation 1 — circuit (= mock Q5 / problem 145)
**Spec:** Translate `Expr` (Var/Not/And/Or/Implies) into equivalent `Circuit` (Input/Nand). Use the identities:
- `¬p ≡ p ⊼ p`
- `p ∧ q ≡ ¬(p ⊼ q)`
- `p ∨ q ≡ ¬((¬p) ∧ (¬q))`
- `p ⇒ q ≡ (¬p) ∨ q`
**Sig:** `circuit :: Expr -> Circuit`
**Solution:**
```haskell
data Expr    = Var Char | Not Expr | And Expr Expr | Or Expr Expr | Implies Expr Expr
data Circuit = Input Char | Nand Circuit Circuit

circuit :: Expr -> Circuit
circuit (Var x)         = Input x
circuit (Not e)         = let c = circuit e in Nand c c
circuit (Or e1 e2)      = circuit (Not (And (Not e1) (Not e2)))
circuit (Implies e1 e2) = circuit (Or (Not e1) e2)
circuit (And e1 e2)     = let c = Nand (circuit e1) (circuit e2)
                          in  Nand c c
```
**QC trap:** Naive recursion `circuit (Not e) = Nand (circuit e) (circuit e)` *doubles* the work (each recursive call re-translates). The `let c = circuit e in Nand c c` form is essential for efficiency — and is what the official solution does.

### Mutation 2 — toNNF (negation-normal-form)
**Spec:** Push every `Not` inward so that `Not` only appears immediately before `Var`. Use De Morgan and `¬¬p = p`.
**Sig:** `toNNF :: Expr -> Expr`
**Solution:**
```haskell
toNNF :: Expr -> Expr
toNNF (Var x)               = Var x
toNNF (Not (Var x))         = Not (Var x)
toNNF (Not (Not e))         = toNNF e
toNNF (Not (And e1 e2))     = toNNF (Or  (Not e1) (Not e2))
toNNF (Not (Or  e1 e2))     = toNNF (And (Not e1) (Not e2))
toNNF (Not (Implies e1 e2)) = toNNF (And e1 (Not e2))
toNNF (And e1 e2)           = And (toNNF e1) (toNNF e2)
toNNF (Or  e1 e2)           = Or  (toNNF e1) (toNNF e2)
toNNF (Implies e1 e2)       = toNNF (Or (Not e1) e2)
toNNF _                     = error "incomplete"
```
**QC trap:** After NNF, no `Implies` remains and `Not` only wraps a `Var`. Use this as a QC property.

### Mutation 3 — exprToCalc / desugar to a simpler ADT
**Spec:** Translate `Expr (Add | Mul | Sub | Neg | Val)` to an ADT that only has `Add`, `Val`, and `Neg`.
**Sig:** `desugar :: Expr -> ExprSimple`
**Solution:**
```haskell
data Expr       = Val Int | Add Expr Expr | Mul Expr Expr | Sub Expr Expr | Neg Expr
data ExprSimple = VS Int  | AS ExprSimple ExprSimple | NS ExprSimple

desugar :: Expr -> ExprSimple
desugar (Val n)     = VS n
desugar (Add a b)   = AS (desugar a) (desugar b)
desugar (Sub a b)   = AS (desugar a) (NS (desugar b))
desugar (Neg e)     = NS (desugar e)
desugar (Mul a b)   = error "cannot desugar Mul without VS-multiplication"
```
**QC trap:** Mul cannot be desugared into Add and Neg without iteration. Often the question restricts to Sub-only desugar and forbids Mul.

### Mutation 4 — exprToList (linearise to a postfix list)
**Spec:** Output an `Expr` as a list of RPN tokens.
**Sig:** `toRPN :: Expr -> [Token]`
**Solution:**
```haskell
data Token = NumT Int | AddT | MulT | SubT | NegT

toRPN :: Expr -> [Token]
toRPN (Val n)   = [NumT n]
toRPN (Add a b) = toRPN a ++ toRPN b ++ [AddT]
toRPN (Mul a b) = toRPN a ++ toRPN b ++ [MulT]
toRPN (Sub a b) = toRPN a ++ toRPN b ++ [SubT]
toRPN (Neg e)   = toRPN e ++ [NegT]
```
**QC trap:** `evalRPN (toRPN e) == evalExpr e`. Naive `++` is O(n^2); use a difference-list accumulator if asked.

### Mutation 5 — toCNF / pushAndOverOr
**Spec:** Distribute `And` over `Or` to reach conjunctive normal form. Assumes input is already in NNF.
**Sig:** `toCNF :: Expr -> Expr`
**Solution:**
```haskell
toCNF :: Expr -> Expr
toCNF (Or e1 e2) = distribute (toCNF e1) (toCNF e2)
  where
    distribute (And a b) c = And (distribute a c) (distribute b c)
    distribute a (And b c) = And (distribute a b) (distribute a c)
    distribute a b         = Or a b
toCNF (And e1 e2) = And (toCNF e1) (toCNF e2)
toCNF e           = e
```
**QC trap:** Result can be exponentially larger than input. Don't run on big formulas.

### Mutation 6 — simplifyExpr (constant folding)
**Spec:** Collapse `Add (Val a) (Val b) → Val (a+b)`, similarly for Mul/Sub/Neg. Recurse first.
**Sig:** `simplify :: Expr -> Expr`
**Solution:**
```haskell
simplify :: Expr -> Expr
simplify (Add e1 e2) = case (simplify e1, simplify e2) of
                         (Val a, Val b) -> Val (a + b)
                         (s1, s2)       -> Add s1 s2
simplify (Mul e1 e2) = case (simplify e1, simplify e2) of
                         (Val a, Val b) -> Val (a * b)
                         (s1, s2)       -> Mul s1 s2
simplify (Sub e1 e2) = case (simplify e1, simplify e2) of
                         (Val a, Val b) -> Val (a - b)
                         (s1, s2)       -> Sub s1 s2
simplify (Neg e)     = case simplify e of
                         Val n -> Val (-n)
                         s     -> Neg s
simplify (Val n)     = Val n
```
**QC trap:** `evalExpr (simplify e) == evalExpr e`. Forgetting to recurse on subexpressions before pattern-matching loses optimisation opportunities.

### Mutation 7 — exprToTree (parse-tree visualisation)
**Spec:** Translate `Expr` to a labelled `BT String` for printing.
**Sig:** `toTree :: Expr -> BT String`
**Solution:**
```haskell
toTree :: Expr -> BT String
toTree (Val n)   = Fork (show n) Empty Empty
toTree (Add a b) = Fork "+"    (toTree a) (toTree b)
toTree (Mul a b) = Fork "*"    (toTree a) (toTree b)
toTree (Sub a b) = Fork "-"    (toTree a) (toTree b)
toTree (Neg e)   = Fork "neg"  (toTree e) Empty
```
**QC trap:** Unary `Neg` → use Empty as one child. Constants are leaves (both children Empty).

### Mutation 8 — circuitInverse (the reverse direction)
**Spec:** Convert a `Circuit` (Nand-only) back into an `Expr`.
**Sig:** `expressionOfCircuit :: Circuit -> Expr`
**Solution:**
```haskell
expressionOfCircuit :: Circuit -> Expr
expressionOfCircuit (Input c)    = Var c
expressionOfCircuit (Nand c1 c2) = Not (And (expressionOfCircuit c1) (expressionOfCircuit c2))
```
**QC trap:** This is *one* possible inverse, not unique. `circuit (expressionOfCircuit c)` is much bigger than `c`. The retract property only goes the other way.

### Mutation 9 — bracketTreeToString / tree-to-string (= Assignment 2 Ex 6)
**Spec:** Translate a `Bracket` tree to a string of `()/{}`.
**Sig:** `brackets :: Bracket -> String`
**Solution:**
```haskell
data Bracket = Round [Bracket] | Curly [Bracket]

brackets :: Bracket -> String
brackets (Round bs) = "(" ++ concatMap brackets bs ++ ")"
brackets (Curly bs) = "{" ++ concatMap brackets bs ++ "}"
```
**QC trap:** Easy direction. The hard direction is the parser (see `parser-family.md`).

### Mutation 10 — exprToString (pretty-print, no parens)
**Spec:** Render with minimum parens given precedence.
**Sig:** `pretty :: Expr -> String`
**Solution:**
```haskell
pretty :: Expr -> String
pretty = go 0
  where
    -- precedences: Add=1, Mul=2, Neg=3, Val=4
    go _ (Val n)   = show n
    go p (Add a b) = paren (p > 1) (go 1 a ++ "+" ++ go 2 b)
    go p (Mul a b) = paren (p > 2) (go 2 a ++ "*" ++ go 3 b)
    go p (Sub a b) = paren (p > 1) (go 1 a ++ "-" ++ go 2 b)
    go p (Neg e)   = paren (p > 3) ("-" ++ go 3 e)
    paren True  s = "(" ++ s ++ ")"
    paren False s = s
```
**QC trap:** `read (pretty e) :: Expr == e` (modulo Show instance). Threading the precedence parameter is the key technique.

## Hidden-predicate mutations
- "Translate only when condition" → conditional translation using `if p then translate e else preserve e`.
- "Translate to monadic ADT" → reuse the recursive scaffold but use `do`-notation:
```haskell
circuitM :: Expr -> State Int Circuit
```
gives every node a fresh wire id (cross to `state-counter-family.md`).

## Accumulator-style alternative
For circuits and CNF expansions, an explicit accumulator + memoisation avoids exponential blowup. A `Data.Map` cache is the textbook tool:
```haskell
circuitMemo :: Expr -> State (Map Expr Circuit) Circuit
```

> **WARNING - not an allowed import:** `Data.Map` / `Data.Map.Strict` are NOT on the exam whitelist (only `Prelude, Data.List, Data.Char, Data.Maybe, Control.Monad, Control.Monad.State, Control.Monad.Writer` plus the question's own Types module). Importing `Data.Map` scores **0**. Use an **association list** `[(Expr, Circuit)]` as the cache instead — `lookup` and cons (`(k,v) :`) replace `Map.lookup`/`Map.insert`:
> ```haskell
> -- allowed-imports cache: assoc list instead of Data.Map
> import Control.Monad.State   -- the only import this needs
>
> circuitMemo :: Expr -> State [(Expr, Circuit)] Circuit
> circuitMemo e = do
>   cache <- get
>   case lookup e cache of            -- needs Eq Expr (derive it on the type)
>     Just c  -> return c
>     Nothing -> do
>       c <- build e                  -- build the circuit for this node
>       modify ((e, c) :)             -- remember it
>       return c
> ```
> An assoc list is O(n) per lookup vs `Data.Map`'s O(log n), but at exam scale that is irrelevant — and it keeps you inside the whitelist. (`lookup` requires `Eq Expr`; add `deriving Eq` to the `Expr` type.)

## Fold-style alternative
Define a generic `foldExpr`:
```haskell
foldExpr :: (Int -> b)             -- Val
         -> (b -> b)               -- Neg
         -> (b -> b -> b)          -- Add
         -> (b -> b -> b)          -- Mul
         -> (b -> b -> b)          -- Sub
         -> Expr -> b
foldExpr v _   _   _   _   (Val n)   = v n
foldExpr v n   _   _   _   (Neg e)   = n (foldExpr v n undefined undefined undefined e)
-- (impractical to thread all five — usually defined recursively)
```
Usually not worth the abstraction here.

## Cross-family combinations
- this family + `env-eval-family.md`: translate Expr to Expr-with-Var (introduces variables).
- this family + `pretty-print-family.md`: translation often goes via a normal form, then pretty-print.
- this family + `parser-family.md`: parser produces an Expr, translator consumes it. Common assignment pattern.
- this family + `state-counter-family.md`: assign fresh "wire ids" during translation.

## QuickCheck universal attacks
- **Semantics-preserving:** `eval (translate e) == eval e`. Define eval on both sides.
- **Round-trip identity** (if available): `inverse (translate e) == e` (usually not exact — translate is not injective).
- **Constant expressions:** `Val n` translates to a *minimal* output.
- **Single-Var formula:** test edge of recursion (the leaf case).
- **Deeply nested Not:** mutation 1's circuit doubles cost — check size growth bound.
- **Distributive blowup:** mutation 5's toCNF can blow up — limit test size.

## Pitfalls (per mutation)
- M1: writing `Nand (circuit e) (circuit e)` instead of `let c = circuit e in Nand c c`.
- M2: missing the `Not (Not e) -> toNNF e` case → divergence.
- M3: trying to handle Mul.
- M4: getting RPN argument order wrong for non-commutative ops.
- M5: not recursing first → results not in CNF after one pass.
- M6: pattern-matching on raw `Add e1 e2` instead of `(simplify e1, simplify e2)`.
- M7: forgetting that `Val` is a leaf.
- M8: assuming the inverse is unique.
- M9: `concat` vs `concatMap`.
- M10: precedence comparison `>` vs `>=` controls left/right associativity.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — exprToList (flatten Expr to inorder list — A05 × A09)

**Spec:** Translate an arithmetic Expr into the list of its leaves in left-to-right order, dropping operator structure.

**Type sig:** `exprToList :: Expr -> [Int]`

```haskell
exprToList :: Expr -> [Int]
exprToList (Num n)     = [n]
exprToList (Add l r)   = exprToList l ++ exprToList r
exprToList (Mul l r)   = exprToList l ++ exprToList r
```

**What changes vs seed:** Same ADT shape as `circuit` but the target is a flat structure (`[Int]`) not another ADT. Translation flattens rather than transforms structurally — a different *data layout* than canonical ADT-to-ADT.

**QC trap:** `Add l r` and `Mul l r` produce the same list — semantically lossy. The marker may use this as a "show your function preserves the leaf ORDER" property; `r ++ l` is wrong.

### Mutation 12 — treeToBalancedList (rebalance via level-order — A05 × A12)

**Spec:** Translate a `BT a` to its level-order (BFS) list of values. Defines an equivalence class of trees up to shape.

**Type sig:** `treeToLevelList :: BT a -> [a]`

```haskell
treeToLevelList :: BT a -> [a]
treeToLevelList t = go [t]
  where
    go []                 = []
    go (Empty       : qs) = go qs
    go (Fork x l r  : qs) = x : go (qs ++ [l, r])
```

**What changes vs seed:** Different recursion shape: queue-based BFS (`++ [l, r]`) instead of stack-based DFS. Demonstrates that ADT translation isn't always structural recursion — sometimes it's a queue/state traversal.

**QC trap:** `qs ++ [l, r]` is O(n) per cons — total O(n²) for a balanced tree. Acceptable for exam scale but worth noting; use `Data.Sequence` if asked for efficient.

## See also

**Primary archetype:** [A05 ADT translation](../archetypes/A05-adt-translation.md)
**Sibling families:** [codec](./codec-family.md)
**Cross-topic:** [expr × maybe](../cross-matrix/expr-x-maybe.md) · [tree × either](../cross-matrix/tree-x-either.md)
**Theory:** [expression tree](../trees/expression-tree.md)
**QuickCheck:** [codec attacks](../quickcheck/codec-attacks.md) · [expr attacks](../quickcheck/expr-attacks.md)
**Pitfalls:** [P-019 Mock Q5 p/q copy-paste](../pitfalls/HIGH-severity.md#p-019)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
