<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Common templates — the 8 patterns**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · **common-templates** · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->





# Common templates

The 8 patterns that cover ~95% of exam questions. **Memorise these so you can type them in under 30 seconds without thinking.** Each pattern's name corresponds to its `ONE-PAGE-PANIC` section number.

## §1 — LIST CONS recursion
```haskell
f :: [a] -> r
f []     = base
f (x:xs) = combine x (f xs)
```
**Uses:** map, filter, fold reformulations, anything `[a] -> r`.
**Variants:** `(x:y:xs)` for adjacent pairs · `(x:xs) | p x` for guarded · dual `f [] _ = ...; f _ [] = ...` for two-list merges.
**Archetype:** [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)

## §2 — ACCUMULATOR recursion (tail form)
```haskell
f :: [a] -> r
f xs = go xs base
  where
    go []     acc = acc
    go (x:xs) acc = go xs (combine x acc)
```
**Uses:** anything "linear time" / "single pass" / "efficient" / "doesn't blow the stack".
**Watch:** result is built in *reverse* order in `acc`; use `foldl' . combine` or reverse at the end if order matters.
**Archetype:** [A09 (acc)](../archetypes/A09-prelude-reimpl.md) · [accumulator-recursion](./accumulator-recursion.md)

## §3 — LIST COMPREHENSION
```haskell
[ expr x y | x <- xs, y <- ys, p x y, let z = f x ]
```
**Uses:** quicksort, Pythagorean triples, factor lists, magic-square candidate generation.
**Watch:** generators are *nested loops* (Cartesian), not parallel iteration.
**Archetype:** [A21 list-comp synthesis](../archetypes/A21-list-comp-synthesis.md)

## §4 — BINARY TREE recursion
```haskell
data BT a = Empty | Fork a (BT a) (BT a)

f :: BT a -> r
f Empty        = base
f (Fork x l r) = combine x (f l) (f r)
```
**Uses:** size, height, mirror, flatten, map, count.
**Watch:** `Empty` returns `base`, NOT `error`. `mirror` swaps `l` and `r` in the combine step.
**Archetype:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)

## §5 — ROSE TREE recursion
```haskell
data Rose a = Leaf a | Branch [Rose a]

f :: Rose a -> r
f (Leaf x)    = baseLeaf x
f (Branch xs) = combine (map f xs)
```
**Uses:** Mock Q1 (`isNBranching`, `prune`), any "tree with variable arity".
**Watch:** `Branch []` is a legal value (empty branch); handle correctly in `combine`.
**Archetype:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) (Rose variant)

## §6 — ADT translation (per-ctor case-fold)
```haskell
data Source = A | B | C Source | D Source Source
data Target = X | Y | Z Target | W Target Target

translate :: Source -> Target
translate A        = X
translate B        = Y
translate (C s)    = Z (translate s)
translate (D s t)  = W (translate s) (translate t)
```
**Uses:** Mock Q5 (`circuit :: Expr -> Circuit`), Caesar, Morse decode, any "Convert X to Y".
**Watch:** `D` recurses on BOTH `s` AND `t` — easy to forget one ([P-019](../pitfalls/HIGH-severity.md#p-019)).
**Archetype:** [A05 ADT translation](../archetypes/A05-adt-translation.md)

## §7 — ENVIRONMENT EVALUATOR (Expr + Env)
```haskell
type Env = [(String, Int)]

eval :: Env -> Expr -> Maybe Int
eval _   (Num n)     = Just n
eval env (Var x)     = lookup x env
eval env (Add e1 e2) = do v1 <- eval env e1
                          v2 <- eval env e2
                          return (v1 + v2)
eval env (Let x e1 e2) = do v <- eval env e1
                            eval ((x, v) : env) e2     -- extend env BEFORE body
```
**Uses:** any "interpreter" / "evaluator" / "expression with variables".
**Watch:** `Let` extends env with the *evaluated* `v`, not the AST `e1`. Do-notation propagates `Nothing`.
**Archetype:** [A08 env eval](../archetypes/A08-env-eval.md)

## §8 — STATE monad (game / counter)
```haskell
import Control.Monad.State

data Heap = First | Second
type NimGame a = State (Int, Int) a

-- Counter
fresh :: State Int Int
fresh = do n <- get
           put (n + 1)
           return n

-- Game move with clamp (Mock Q3)
takeTokens :: Int -> Heap -> NimGame ()
takeTokens n First  = do (x, y) <- get; put (max 0 (x - n), y)
takeTokens n Second = do (x, y) <- get; put (x, max 0 (y - n))

-- Game-over predicate (Mock Q3 — note the AND)
gameOver :: NimGame Bool
gameOver = do (x, y) <- get
              return (x == 0 && y == 0)
```
**Signatures are mandatory:** `Heap = First | Second`, `type NimGame a = State (Int,Int) a`. `gameOver :: NimGame Bool` and `takeTokens :: Int -> Heap -> NimGame ()`. Writing `State NimGame ()` is a kind error (`NimGame` is already `State (Int,Int)`, not a state type).
**Uses:** Mock Q3 Nim, label tree, fresh-ID generation, any "thread an accumulator under a monadic interface".
**Watch:** `max 0 (...)` clamps; `==` then `&&` for game-over ([P-006](../pitfalls/HIGH-severity.md#p-006), [P-008](../pitfalls/HIGH-severity.md#p-008)).
**Archetype:** [A02 state game](../archetypes/A02-state-game.md)

## §14 — GENERIC MONAD (`Monad m =>`)
```haskell
-- Mock Q2 (canonical):
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx _  0 = do x <- mx; return [x]                       -- [x] NOT []
applyNTimes mx mf n = do x <- mx
                         xs <- applyNTimes (mf x) mf (n - 1)
                         return (x : xs)
```
**Uses:** Mock Q2 `applyNTimes`, `mapM'`, `replicateM'`, anything with `Monad m =>`.
**Watch:** base case `n == 0` returns `[x]` (singleton), NOT `[]` ([P-007](../pitfalls/HIGH-severity.md#p-007)). The marker tests `n = 0` explicitly.
**Archetype:** [A03 generic monad](../archetypes/A03-generic-monad.md)

---

## Bonus: WRITER monad trace
```haskell
import Control.Monad.Writer

factWithTrace :: Int -> Writer [String] Int
factWithTrace 0 = do tell ["fact 0 = 1"]
                     return 1
factWithTrace n = do tell ["fact " ++ show n ++ " = " ++ show n ++ " * fact " ++ show (n-1)]
                     r <- factWithTrace (n - 1)
                     return (n * r)
```
**Archetype:** [A15 writer trace](../archetypes/A15-writer-trace.md)

## Bonus: FUNCTOR instance (hand-written)
```haskell
instance Functor BT where
  fmap _ Empty        = Empty
  fmap f (Fork x l r) = Fork (f x) (fmap f l) (fmap f r)
```
Don't use `deriving Functor` — Safe pragma forbids it ([P-010](../pitfalls/HIGH-severity.md#p-010)).
**Archetype:** [A06 functor instance](../archetypes/A06-functor-instance.md)

---

## Quick recognition shortcut

| Question shape contains… | Reach for template |
|---|---|
| `[a] -> r` | §1 LIST CONS |
| "efficient" / "single pass" | §2 ACCUMULATOR |
| `[r | x <- xs, …]` | §3 LIST COMPREHENSION |
| `BT a -> r` / `Empty | Fork` | §4 BINARY TREE |
| `Rose a -> r` / `Leaf | Branch [Rose a]` | §5 ROSE TREE |
| `Source -> Target` (2 ADTs) | §6 ADT TRANSLATION |
| `Env -> Expr -> Maybe v` | §7 ENV EVALUATOR |
| `State s a` / `Nim` / `gameOver` | §8 STATE |
| `Monad m => … m [a]` | §14 GENERIC MONAD |
| `Writer w a` / `tell` / "log every step" | Bonus WRITER |
| `instance Functor T` | Bonus FUNCTOR |

## Print this page

This single page is the most printable artefact in the vault. ~80 lines of plain template code. Take a paper copy into the exam if vLab fails. Combine with [ONE-PAGE-PANIC](../exam-day/ONE-PAGE-PANIC.md) and [HIGH-severity P-001 through P-010](../pitfalls/HIGH-severity.md) for the minimum-viable printout.

## See also

**Archetypes:** [README](../archetypes/README.md) for the full 24-shape tier ranking
**Exam day:** [ONE-PAGE-PANIC](../exam-day/ONE-PAGE-PANIC.md) · [LAST-HOUR-CHECKLIST](../exam-day/LAST-HOUR-CHECKLIST.md) · [WHAT-TO-PIN](../exam-day/WHAT-TO-PIN.md)
**Pitfalls:** [HIGH-severity](../pitfalls/HIGH-severity.md) · [signature-pitfalls](../pitfalls/signature-pitfalls.md)
**Basics:** [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [pattern-matching](./pattern-matching.md) · [list-comprehensions](./list-comprehensions.md) · [do-notation-basics](./do-notation-basics.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
