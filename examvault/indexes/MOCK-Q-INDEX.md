<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **MOCK-Q-INDEX**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · [MASTER-INDEX](./MASTER-INDEX.md) · **MOCK-Q-INDEX** · [MUTATION-INDEX](./MUTATION-INDEX.md) · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# MOCK-Q-INDEX

Mock Test Q1–Q5 — spec verbatim, archetype, surprising marker behaviour, canonical solution file.

**Source:** `fp-learning-2025/files/Assignments/MockTest/MockTest-Template.hs` + `MockTestMarking.hs` + `MockTestTestCases.hs`.

> **Critical:** every exam question is built by *mutating* one of these archetypes. Memorise the spec AND the marker quirks.

---

## Module header (DO NOT CHANGE)

```haskell
{-# OPTIONS_GHC -fwarn-incomplete-patterns -Wno-x-partial #-}
{-# LANGUAGE NoGeneralizedNewtypeDeriving, Safe #-}

module MockTest ( isNBranching, prune, applyNTimes
                , gameOver, takeTokens, isMagicSquare, circuit ) where

import Types
import Data.List
```

`Types.hs` provides: `Rose`, `NimGame`, `NimBoard`, `Heap`, `Expr`, `Circuit`, plus `Control.Monad.State` re-exports.

---

<a id="mock-q1"></a>
## Q1 — `isNBranching`, `prune` (Rose tree)

**Spec verbatim:**
> `data Rose a = Leaf a | Branch [Rose a]`
> `isNBranching :: Int -> Rose a -> Bool` — True iff every `Branch` has exactly `n` children.
> `prune :: Int -> Rose a -> Rose a` — keep the first `n` children of every branch.

**Archetype:** A01 (tree-ADT structural recursion).
**Mutations applied:** M1 (predicate) for `isNBranching`; M2 (rebuild) for `prune`.

**Canonical solution:**
```haskell
isNBranching :: Int -> Rose a -> Bool
isNBranching _ (Leaf _)    = True
isNBranching n (Branch xs) = length xs == n && all (isNBranching n) xs

prune :: Int -> Rose a -> Rose a
prune _ (Leaf x)    = Leaf x
prune n (Branch xs) = Branch (take n (map (prune n) xs))
```

**Marker behaviour (no significant quirks):**
- Generator: `sized` Rose trees, depth up to ~10.
- `isNBranching n (Leaf _) == True` — vacuous; if you make `Leaf` return `False`, you fail every test.
- `prune` does NOT recurse into pruned children; you must `map prune` THEN `take`.
- The marker does **not** test `n = 0` as a corner case for `prune` (would give `Branch []`).

**Files:**
- [A01-tree-recursion](../archetypes/A01-tree-recursion.md) (M1, M2 mutations)
- [rose-tree](../trees/rose-tree.md)
- [rose-ops-family](../question-families/rose-ops-family.md)
- [rose-attacks](../quickcheck/rose-attacks.md)

---

<a id="mock-q2"></a>
## Q2 — `applyNTimes` (generic Monad combinator)

**Spec verbatim:**
> `applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]`
> Apply `mf` to `mx` exactly `n` times, returning all intermediate results (n+1 values total). Each monadic action runs exactly once.

**Archetype:** A03 (generic `Monad m =>` combinator).

**Canonical solution:**
```haskell
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx mf 0 = do
  x <- mx
  pure [x]
applyNTimes mx mf n = do
  x <- mx
  xs <- applyNTimes (mf x) mf (n - 1)
  pure (x : xs)
```

**⚠️ SURPRISING MARKER BEHAVIOUR (top tip):**
- The marker's *recursive* generator draws `n` from `2..10`, but its other two property generators draw `n` from `1..10`, so **`n = 1` is tested** and the `n = 0` base case has its own test. **Off-by-one is NOT lenient** — returning `n` items instead of `n+1` fails at `n = 1`. Get the `n+1` count exactly right.
- The hardest test is "each monadic action runs exactly once" — `mf x` must be invoked exactly `n` times, no more, no less. Test with `Writer (Sum Int) a` and assert the count.
- The base case is `n = 0` returns `[x]` not `[]` — read the spec again.
- The marker does NOT generate `n < 0` — undefined behaviour there is fine, but be safe.

**Files:**
- [A03-generic-monad](../archetypes/A03-generic-monad.md) (canonical)
- [generic-combinators](../monads/generic-combinators.md)
- [monad-attacks](../quickcheck/monad-attacks.md)
- [list-x-monad](../cross-matrix/list-x-monad.md)

---

<a id="mock-q3"></a>
## Q3 — `gameOver`, `takeTokens` (Nim with State)

**Spec verbatim:**
> `type NimBoard = (Int, Int)`
> `type NimGame a = State NimBoard a`
> `data Heap = First | Second`
> `gameOver :: NimGame Bool` — True iff both heaps are zero.
> `takeTokens :: Int -> Heap -> NimGame ()` — subtract `n` tokens from heap `h`, never going below 0.

**Archetype:** A02 (state monad mini-game).

**Canonical solution:**
```haskell
gameOver :: NimGame Bool
gameOver = do
  (a, b) <- get
  pure (a == 0 && b == 0)

takeTokens :: Int -> Heap -> NimGame ()
takeTokens n First  = modify (\(a, b) -> (max 0 (a - n), b))
takeTokens n Second = modify (\(a, b) -> (a, max 0 (b - n)))
```

**⚠️ SURPRISING MARKER BEHAVIOUR (top tip):**
- **`gameOver` has a hardcoded `(0,0)` test worth 4 free marks.** If you literally just write `gameOver = pure True`, you get 4/10 — no joke. The marker tests `evalState gameOver (0,0) == True` as the very first assertion, and the property test follows.
- `takeTokens` MUST clamp at 0 (`max 0 (a - n)`). The marker tries `takeTokens 100 First` on `(3, 5)` and expects `(0, 5)`, not `(-97, 5)`.
- The marker does not test negative `n` to `takeTokens` — implementation may go either way there.
- The marker uses `execState` to inspect the final state; if you use `put` instead of `modify` you may overwrite incorrectly.

**Files:**
- [A02-state-game](../archetypes/A02-state-game.md) (canonical)
- [game-state](../cross-matrix/game-state.md)
- [state](../monads/state.md)
- [state-game-family](../question-families/state-game-family.md)
- [state-attacks](../quickcheck/state-attacks.md)

---

<a id="mock-q4"></a>
## Q4 — `isMagicSquare` (matrix predicate)

**Spec verbatim:**
> `isMagicSquare :: [[Int]] -> Bool`
> True iff every row, column, and main diagonal sum to the same number. Use `Data.List.transpose`.

**Archetype:** A04 (matrix predicate via transpose).

**Canonical solution:**
```haskell
isMagicSquare :: [[Int]] -> Bool
isMagicSquare xs =
  let n        = length xs
      rows     = map sum xs
      cols     = map sum (transpose xs)
      diag     = sum [xs !! i !! i         | i <- [0 .. n - 1]]
      antiDiag = sum [xs !! i !! (n-1-i)   | i <- [0 .. n - 1]]
      target   = head rows
   in all (== target) rows
   && all (== target) cols
   && diag     == target
   && antiDiag == target
```

**Marker behaviour:**
- 1×1 matrices are True (vacuously).
- Empty matrix `[]` — marker either skips or returns True; check the spec text once more before locking in.
- Anti-diagonal is tested separately — some solutions forget it.
- Non-square `[[Int]]` — marker may generate jagged matrices to trip you. Either filter them out or accept your code might fail; both are graded leniently here.

**Files:**
- [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) (canonical)
- [matrix-predicate-family](../question-families/matrix-predicate-family.md)
- [matrix-attacks](../quickcheck/matrix-attacks.md)

---

<a id="mock-q5"></a>
## Q5 — `circuit` (Expr → Circuit ADT translation)

**Spec verbatim:**
> `data Expr    = Var Char | Not Expr | And Expr Expr | Or Expr Expr | Implies Expr Expr`
> `data Circuit = Input Char | Nand Circuit Circuit`
> `circuit :: Expr -> Circuit`
> Convert any `Expr` into an equivalent `Circuit` using only `Nand`.
> Identities: `¬p = p⊼p`, `p∧q = ¬(p⊼q)`, `p∨q = ¬((¬p)∧(¬q))`, `p⇒q = (¬p)∨q`.

**Archetype:** A05 (ADT-to-ADT translation).

**Canonical solution:**
```haskell
circuit :: Expr -> Circuit
circuit (Var c)         = Input c
circuit (Not e)         = let c = circuit e in Nand c c
circuit (And e1 e2)     = let c1 = circuit e1
                              c2 = circuit e2
                              n  = Nand c1 c2
                           in Nand n n
circuit (Or e1 e2)      = circuit (Not (And (Not e1) (Not e2)))
circuit (Implies e1 e2) = circuit (Or (Not e1) e2)
```

**⚠️ SURPRISING MARKER BEHAVIOUR (top tip):**
- The marker checks `circuit` **semantically**, NOT structurally. It evaluates the resulting `Circuit` for every possible variable assignment and compares the truth table against `Expr`.
- A **verbose-but-correct** translation gets full marks. You don't need to find the minimal `Nand` representation.
- You may freely recurse (call `circuit` on a derived `Expr`) — the marker doesn't care about complexity.
- The marker generates `Expr` of depth ~18 with only `Not` and `And`, so make sure your `Not` and `And` cases work standalone.
- **DO NOT** try to evaluate `Expr` to `Bool` somewhere and embed — that's a category error. The translation must be `Expr -> Circuit`, NOT `Expr -> Bool`.

**Files:**
- [A05-adt-translation](../archetypes/A05-adt-translation.md) (canonical)
- [adt-translation-family](../question-families/adt-translation-family.md)
- [desugar-pipeline](../interpreters/desugar-pipeline.md)
- [expr-attacks](../quickcheck/expr-attacks.md)

---

## Summary table

| Q | Archetype | Top mark-leaving trap | Free-marks shortcut |
|---|-----------|----------------------|---------------------|
| Q1 | [A01](../archetypes/A01-tree-recursion.md) | Leaf in `isNBranching` returning False | n/a |
| Q2 | [A03](../archetypes/A03-generic-monad.md) | Off-by-one (`n` vs `n+1` items) → only 8/10 | `n=0 → pure [x]` |
| Q3 | [A02](../archetypes/A02-state-game.md) | `takeTokens` going below 0 | `gameOver = pure True` already scores 4/10 |
| Q4 | [A04](../archetypes/A04-matrix-predicate.md) | Missing anti-diagonal | n/a |
| Q5 | [A05](../archetypes/A05-adt-translation.md) | Trying to evaluate `Expr` to `Bool` | Verbose Nand expansions are fully accepted |

---

## Generator details (for QC-aware practice)

- **Q1 generator:** sized Rose, leaves drawn from arbitrary `a`, depth ~0-10. Tests with `n = 0..4`.
- **Q2 generator:** monads tested include `Maybe`, `[]`, `State Int`, `Writer (Sum Int)`. The recursive/"runs exactly once" test draws `n` from `2..10`; the other two property generators draw `n` from `1..10`. So **`n = 1` IS tested** — only `n = 0` is excluded from the *recursive* test (the `n = 0` base case has its own dedicated test). An off-by-one (`n` items instead of `n+1`) therefore fails at `n = 1`; it is **not** silently lenient.
- **Q3 generator:** boards from `(0..50, 0..50)`. Includes `(0, 0)` explicitly.
- **Q4 generator:** mix of n×n squares with values in `[-20..20]`. 1×1 included.
- **Q5 generator:** `Expr` from a custom `Arbitrary` with depth ~12-18.

---

## Pre-submit checklist (for the mock or exam paper)

- [ ] Module header bytes unchanged (Safe pragma, `NoGeneralizedNewtypeDeriving`)
- [ ] Module exports list unchanged
- [ ] All seven type signatures **character-for-character identical**
- [ ] No additional imports beyond what's permitted
- [ ] No `undefined` left
- [ ] `presubmit.sh MockTest` passes
- [ ] `ghc -fno-code -XSafe -XNoGeneralizedNewtypeDeriving MockTest.hs` compiles silently

## See also
- [README](../archetypes/README.md) — 5-question composition prediction
- [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) — universal 60-second pre-submit checklist
- [ASSIGNMENT-INDEX](../indexes/ASSIGNMENT-INDEX.md) — assignments and their quirks

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
