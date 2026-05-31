<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [exam-day](./README.md) · **ONE-PAGE-PANIC**

<!-- siblings:start -->
> **Peers:** [EXAM-DAY-ROUTE](./EXAM-DAY-ROUTE.md) · [IN-EXAM-WORKFLOW](./IN-EXAM-WORKFLOW.md) · [LAST-HOUR-CHECKLIST](./LAST-HOUR-CHECKLIST.md) · **ONE-PAGE-PANIC** · [RECOGNITION-FLOWCHART](./RECOGNITION-FLOWCHART.md) · [TIME-BUDGET](./TIME-BUDGET.md) · [WHAT-TO-PIN](./WHAT-TO-PIN.md)
<!-- siblings:end -->






# ONE-PAGE-PANIC

> Single screen. If everything else fails, this is the screen.

## Allowed imports
`Prelude` (implicit), `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`. Plus `Types`. NOTHING ELSE.

## 5 templates (the ones that show up)

```haskell
-- §1 LIST CONS
f []     = base
f (x:xs) = combine x (f xs)

-- §4 BINARY TREE
f Empty        = base
f (Fork x l r) = combine x (f l) (f r)

-- §5 ROSE TREE
f (Leaf x)    = base x
f (Branch xs) = combine (map f xs)

-- §8 STATE
fresh = do n <- get; put (n+1); return n
takeTokens n First  = do (x,y) <- get; put (max 0 (x-n), y)   -- CLAMP
gameOver = do (x,y) <- get; return (x == 0 && y == 0)         -- AND

-- §14 GENERIC MONAD (Mock Q2)
applyNTimes mx _  0 = do x <- mx; return [x]                   -- [x] NOT []
applyNTimes mx mf n = do x <- mx; xs <- applyNTimes (mf x) mf (n-1); return (x:xs)
```

## Recognition shortcut (4 phrases → archetype)

| If question contains                 | Archetype | First-look                              |
|--------------------------------------|-----------|-----------------------------------------|
| "rose tree" / "binary tree"          | A01       | [A01-tree-recursion](../archetypes/A01-tree-recursion.md)      |
| "Monad m =>"                         | A03       | [A03-generic-monad](../archetypes/A03-generic-monad.md)       |
| "State" / "Nim" / "game" / "board"   | A02       | [A02-state-game](../archetypes/A02-state-game.md)          |
| "[[Int]]" / "matrix" / "magic"       | A04       | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md)    |
| "Expr -> Circuit" / two ADTs         | A05       | [A05-adt-translation](../archetypes/A05-adt-translation.md)     |
| "Functor"/"instance"                 | A06       | [A06-functor-instance](../archetypes/A06-functor-instance.md)    |
| "evaluator" / "eval" / "env"         | A08       | [A08-env-eval](../archetypes/A08-env-eval.md)            |

## 5 MARKS-KILLERS (don't make these)
1. **Type sig changed** → 0 on Q. COPY-PASTE FROM TEMPLATE.
2. **`isBST Empty = False`** → vacuous truth bug. Use `True`.
3. **`isNBranching n (Branch xs) = length xs == n`** missing `&& all (isNBranching n) xs`.
4. **`applyNTimes _ _ 0 = return []`** → must be `do x <- mx; return [x]`. **WHY:** Mock Q2 marker tests `applyNTimes 0` explicitly; off-by-one is silently lenient on n=1+, brutal on n=0.
5. **`gameOver` returns False on `(0,0)`** → 4 marks gone. It's a hardcoded test in the marker. Always `return (x == 0 && y == 0)`.
6. **Deep right-spine trees → stack overflow** on naive `flatten t ++ [x]` style. Use accumulator (`flatten t acc = ...`) or `foldr` for any tree question with "1000+ nodes" or "skewed".
7. **Mock Q5 `circuit` is semantically checked**, NOT structurally. Two different ASTs that produce the same boolean equivalence will both pass. Don't waste time matching the reference AST exactly.

## If stuck
1. Stub the function so it RETURNS something type-correct (NOT `undefined`).
   - `Empty` for `BT a`, `Leaf x` for `Rose a`, `[]` for `[a]`, `False` for `Bool`, `0` for `Int`.
2. Submit a valid file. Partial marks are still possible.
3. Move on. NEVER spend more than 25 minutes on one question.

## If GHC barks at you
**`Ctrl+F` the first line of the red text** in [ghc-error-decoder](../haskell-basics/ghc-error-decoder.md). Most messages map to a 1-line fix recipe (type mismatch, missing case, missing import, etc.).

## Pre-submit (do not skip)
```bash
./presubmit.sh MockTest && echo OK || echo FAIL
```
- Safe pragma still present? `{-# LANGUAGE NoGeneralizedNewtypeDeriving, Safe #-}`
- Module line unchanged?  `module MockTest ( ... ) where`
- Only allowed imports?
- Base case FIRST in every function?

## Last resort
Open [RECOGNITION-FLOWCHART](RECOGNITION-FLOWCHART.md) and walk from top.
Open [IF-YOU-SEE-X](../indexes/IF-YOU-SEE-X.md) and Ctrl-F any keyword from the question.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
