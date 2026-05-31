<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [pitfalls](./README.md) · **Pitfalls — MEDIUM severity (silent correctness bugs)**

<!-- siblings:start -->
> **Peers:** [HIGH-severity](./HIGH-severity.md) · [LOW-severity](./LOW-severity.md) · **MEDIUM-severity** · [imports-pitfalls](./imports-pitfalls.md) · [per-topic-pitfalls](./per-topic-pitfalls.md) · [signature-pitfalls](./signature-pitfalls.md)
<!-- siblings:end -->






# Pitfalls — MEDIUM severity (silent correctness bugs)

> **What counts as MEDIUM:** correctness bugs that pass the compiler, fail one or two specific QuickCheck input classes, and cost **1-4 marks per occurrence**. The "almost right" category. Most students lose more total marks here than in HIGH because these are easy to overlook.

The pattern: the code is structurally right, the type checks, the happy path works — but the marker's edge-case generator finds the bug.

---

<a id="p-100"></a>
## P-100 · `chainDivisions` not using `do` on Maybe (or wrong short-circuit)

**Topic:** Maybe monad
**Symptom:** Function returns `Nothing` for the wrong reason, or returns `Just` when it should be `Nothing` because you `fromMaybe`'d a partial result.
**Cause:** Writing nested `case` expressions instead of `do`-notation. The auto-short-circuit of `do` on Maybe is the whole point.
**Fix:** Use `do { x <- mx; y <- my; return (...) }`. Maybe's `>>=` handles short-circuit for you.
**Example wrong:**
```haskell
chainDivisions :: [Int] -> Int -> Maybe Int
chainDivisions [] acc     = Just acc
chainDivisions (0:xs) _   = Nothing
chainDivisions (x:xs) acc =
  let r = acc `div` x
  in chainDivisions xs r                  -- silently ignores the case where r underflows
```
**Example right:**
```haskell
chainDivisions :: [Int] -> Int -> Maybe Int
chainDivisions []     acc = Just acc
chainDivisions (0:_)  _   = Nothing
chainDivisions (x:xs) acc = chainDivisions xs (acc `div` x)
-- Or with do for explicit chaining when each step can fail:
safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv a b = Just (a `div` b)
chainDivisions' [] acc = Just acc
chainDivisions' (x:xs) acc = do r <- safeDiv acc x
                                chainDivisions' xs r
```
**Marks lost:** 2-3
**Seen in:** A03 / A14. [maybe-either-attacks](../quickcheck/maybe-either-attacks.md).

---

<a id="p-101"></a>
## P-101 · `zipEither` returns wrong "shorter list" message

**Topic:** Either short-circuit
**Symptom:** Marker compares your error message string. "first shorter" vs "second shorter" mismatch → false negative.
**Cause:** Reversing which list ran out first. `zipEither [] xs` means the FIRST list is empty (shorter); it's the SECOND that has elements left.
**Fix:** Read the spec carefully. Convention: empty-LHS means LHS is shorter.
**Example wrong:**
```haskell
zipEither [] []         = Right []
zipEither [] _          = Left "second shorter"     -- WRONG direction
zipEither _  []         = Left "first shorter"      -- WRONG direction
zipEither (x:xs)(y:ys)  = do rest <- zipEither xs ys; return ((x,y):rest)
```
**Example right:**
```haskell
zipEither :: [a] -> [b] -> Either String [(a,b)]
zipEither []    []     = Right []
zipEither []    _      = Left "first shorter"   -- first ran out
zipEither _     []     = Left "second shorter"
zipEither (x:xs)(y:ys) = do rest <- zipEither xs ys; return ((x,y):rest)
```
**Marks lost:** 2
**Seen in:** [maybe-either-attacks](../quickcheck/maybe-either-attacks.md).

---

<a id="p-102"></a>
## P-102 · Generic monad combinator with wrong recursion order (right-fold vs left-fold)

**Topic:** Generic Monad
**Symptom:** `applyNTimes` returns the right elements but in reverse order. Marker uses `===` (strict equality), not `p_permOf` — order matters.
**Cause:** Building the result via `xs ++ [x]` instead of `x : xs`. Or threading the recursion through the WRONG step (`mf x` vs `mx` again).
**Fix:** The canonical recursion: each step takes the CURRENT value `x`, recursively builds the rest from `mf x`, then prepends `x`.
**Example wrong:**
```haskell
applyNTimes mx mf 0 = do x <- mx; return [x]
applyNTimes mx mf n = do x <- mx
                         xs <- applyNTimes mx mf (n-1)        -- WRONG: should be (mf x), not mx
                         return (x : xs)
```
**Example right:**
```haskell
applyNTimes mx _  0 = do x <- mx; return [x]
applyNTimes mx mf n = do x  <- mx
                         xs <- applyNTimes (mf x) mf (n-1)    -- next iter uses (mf x)
                         return (x : xs)
```
**Marks lost:** 4 (cascade fail of all recursive tests)
**Seen in:** Mock Q2. `examples/mock-q2-monad.md`.

---

<a id="p-103"></a>
## P-103 · Mock Q5 — `Or` case copy-paste with `p` repeated where `q` belongs

**Topic:** ADT translation
**Symptom:** Marker generates `Or (Var 'a') (Var 'b')`, evaluates `semCirc` of your output, finds it differs from `semExpr (Or ...)` on inputs `{a=False, b=True}`. Marker reports the counterexample.
**Cause:** The `Or p q` desugars to NAND of two NANDs. The structure has `circuit p` AND `circuit q` symmetrically — but visually it's tempting to copy-paste `np = Nand (circuit p) (circuit p)` and then write `nq = Nand (circuit p) (circuit p)` forgetting to change to `q`.
**Fix:** Derive each line FROM the Boolean identity (Or p q = Not (Not p AND Not q) = Nand (Not p) (Not q) = Nand (Nand p p) (Nand q q)). Or use `let` to share.
**Example wrong:**
```haskell
circuit (Or p q) = Nand np nq
  where np = Nand (circuit p) (circuit p)
        nq = Nand (circuit p) (circuit p)        -- LANDMINE: should be q
```
**Example right:**
```haskell
circuit (Or p q) = Nand np nq
  where np = Nand (circuit p) (circuit p)
        nq = Nand (circuit q) (circuit q)
```
**Marks lost:** 2-4 (depending on whether other Or-cases trigger as well)
**Seen in:** Mock Q5. `final10.hs` student bug. **Note:** this is so close to HIGH it's almost there. Treating it as MEDIUM because the rest of `circuit` may still score; HIGH version (P-019) covers the wider trap.

---

<a id="p-104"></a>
## P-104 · `mapBT` swapped left and right subtrees

**Topic:** Functor / Tree map
**Symptom:** Marker compares `mapBT f t == fmap f t` (or reference). Your tree mirrors itself silently every call.
**Cause:** Copy-pasting from a `mirror` implementation; treating `mapBT` as if it were `mirror`.
**Fix:** Constructor on RHS must be IDENTICAL to LHS pattern. `Fork x l r` ↔ `Fork (f x) (mapBT f l) (mapBT f r)` — NEVER swap `l` and `r`.
**Example wrong:**
```haskell
mapBT _ Empty        = Empty
mapBT f (Fork x l r) = Fork (f x) (mapBT f r) (mapBT f l)    -- swapped
```
**Example right:**
```haskell
mapBT _ Empty        = Empty
mapBT f (Fork x l r) = Fork (f x) (mapBT f l) (mapBT f r)
```
**Marks lost:** 4 (Functor laws fail)
**Seen in:** beginner trees.

---

<a id="p-105"></a>
## P-105 · State Nim — `takeTokens` does not clamp at 0 (underflow)

**Topic:** State games
**Symptom:** Marker generates `n > x` (player wants to take more than heap has). Your `put (x-n, y)` gives `(negative, y)`. Subsequent `gameOver` test fails because heap is `-3`, not `0`. Lose 2-4 marks.
**Cause:** Treating `x - n` as the new heap. Forgetting the spec rule "you can't take more than there are".
**Fix:** `max 0 (x - n)`. Always.
**Example wrong:**
```haskell
takeTokens n First = do (x,y) <- get; put (x - n, y)
```
**Example right:**
```haskell
takeTokens n First  = do (x,y) <- get; put (max 0 (x-n), y)
takeTokens n Second = do (x,y) <- get; put (x, max 0 (y-n))
```
**Marks lost:** 2-3
**Seen in:** Mock Q3. [state-attacks](../quickcheck/state-attacks.md).

---

<a id="p-106"></a>
## P-106 · Matrix predicate confuses rows with columns

**Topic:** Matrix transpose
**Symptom:** Magic-square test fails on non-symmetric grids (those where rows and columns sum differently). Marker generates a non-magic example; yours says "is magic".
**Cause:** `cols = transpose rows` is right. But writing `rows = transpose cols` and using `rows` later swaps everything.
**Fix:** Name them clearly. Test mentally: `transpose [[1,2,3],[4,5,6]] == [[1,4],[2,5],[3,6]]`.
**Example wrong:**
```haskell
isMagicSquare xss =
  let rows   = transpose xss                        -- WRONG: that's columns!
      cols   = xss                                  -- WRONG: rows are the input
      target = sum (head rows)
      ...
```
**Example right:**
```haskell
isMagicSquare xss =
  let target = sum (head xss)
      rowSums = map sum xss
      colSums = map sum (transpose xss)
      ...
```
**Marks lost:** 3
**Seen in:** Mock Q4.

---

<a id="p-107"></a>
## P-107 · `flatten` / `inorder` produces wrong order (pre-order when in-order expected)

**Topic:** Tree flatten
**Symptom:** Marker compares `flatten t` against `sort (flatten t)` for BST tests. Yours gives `[5,3,1,7,9]` instead of `[1,3,5,7,9]`.
**Cause:** Writing `[x] ++ flatten l ++ flatten r` (pre-order) when the spec is `flatten l ++ [x] ++ flatten r` (in-order).
**Fix:** Default to in-order unless told otherwise. The defining property: `flatten . insertBST x . t = sort (x : flatten t)` only with in-order.
**Example wrong:**
```haskell
flatten Empty        = []
flatten (Fork x l r) = x : flatten l ++ flatten r              -- PRE-order
```
**Example right:**
```haskell
flatten Empty        = []
flatten (Fork x l r) = flatten l ++ [x] ++ flatten r            -- IN-order
```
**Marks lost:** 3 (cascade through BST tests)
**Seen in:** trees-attacks.md.

---

<a id="p-108"></a>
## P-108 · `leaves Empty = 1` (should be 0)

**Topic:** Tree counting
**Symptom:** Marker tests `leaves (Fork 1 Empty (Leaf 2)) == 1`. Yours returns 2 because you counted both Empty siblings of the single leaf node.
**Cause:** Confusing "Empty subtree" with "leaf node". A LEAF is a `Fork x Empty Empty` (depending on definition); an Empty alone is NOT a leaf.
**Fix:** Distinguish 3 cases for `leaves`:
```haskell
leaves Empty                = 0
leaves (Fork _ Empty Empty) = 1
leaves (Fork _ l r)         = leaves l + leaves r
```
**Example wrong:**
```haskell
leaves Empty        = 1                                       -- WRONG
leaves (Fork _ l r) = leaves l + leaves r
```
**Example right:** (as above)
**Marks lost:** 2-3
**Seen in:** trees-attacks.md.

---

<a id="p-109"></a>
## P-109 · `circuit` doesn't desugar `Implies` — leaves it as a missing case

**Topic:** ADT translation completeness
**Symptom:** Marker generates `Implies (Var 'a') (Var 'b')`. Your function pattern-matches `Var`, `Not`, `And`, `Or` but not `Implies`. Non-exhaustive pattern → exception → 0 on that input class.
**Cause:** Forgetting that `Implies` is a constructor (because the math identity `p → q = ¬p ∨ q` lets you rewrite it). But the recursive call must explicitly destructure `Implies`.
**Fix:** Rewrite by calling the existing translation:
```haskell
circuit (Implies p q) = circuit (Or (Not p) q)
```
**Example wrong:**
```haskell
circuit (Var x)   = Input x
circuit (Not p)   = Nand (circuit p) (circuit p)
circuit (And p q) = ...
circuit (Or p q)  = ...
-- WHERE IS Implies?
```
**Example right:**
```haskell
circuit (Implies p q) = circuit (Or (Not p) q)        -- recursive desugar
```
**Marks lost:** 3 (the Implies test)
**Seen in:** Mock Q5.

---

<a id="p-110"></a>
## P-110 · Writer log ordering — `tell` after `pure` instead of before

**Topic:** Writer monad ordering
**Symptom:** Marker generates a small `Writer` action that traces its sub-actions. Yours produces `["leave A", "enter A"]` instead of `["enter A", "leave A"]`. Order mismatch — lose 2 marks.
**Cause:** Writing `do pure x; tell ["enter A"]; ... ; tell ["leave A"]; return result` — but actually the `tell` AFTER the result computation runs LAST.
**Fix:** Decide the convention BEFORE writing. Standard: log BEFORE the action ("enter A"), log AFTER the action ("leave A"). The `do`-block executes top-to-bottom.
**Example wrong:**
```haskell
logTraverse (SubDir n cs) = do
  mapM_ logTraverse cs
  tell ["Enter " ++ n]              -- AFTER the recursion: enter logs AFTER leaves
  tell ["Leave " ++ n]
```
**Example right:**
```haskell
logTraverse (SubDir n cs) = do
  tell ["Enter " ++ n]
  mapM_ logTraverse cs
  tell ["Leave " ++ n]
```
**Marks lost:** 2-3
**Seen in:** A15. [writer-attacks](../quickcheck/writer-attacks.md).

---

<a id="p-111"></a>
## P-111 · `runState` vs `evalState` vs `execState` confusion

**Topic:** State runners
**Symptom:** Marker expects `(a, s)` tuple; you return `a` alone (used `evalState`). Or expects `a`; you return `(a, s)`. Type error or wrong shape.
**Cause:** Forgetting which runner gives which projection.
**Fix:** Memorise:
- `runState  :: State s a -> s -> (a, s)` — the FULL pair.
- `evalState :: State s a -> s -> a` — just the VALUE.
- `execState :: State s a -> s -> s` — just the FINAL state.
**Example wrong:**
```haskell
labelTree :: BT a -> BT (Int, a)
labelTree t = runState (go t) 0       -- WRONG: returns (BT (Int,a), Int), not BT (Int,a)
```
**Example right:**
```haskell
labelTree :: BT a -> BT (Int, a)
labelTree t = evalState (go t) 0     -- discard final counter, keep tree
```
**Marks lost:** 4 (whole label sub-question)
**Seen in:** state monad questions, especially labelling.

---

<a id="p-112"></a>
## P-112 · `foldr` vs `foldl` confusion

**Topic:** Folds
**Symptom:** `foldr (-) 0 [1,2,3]` is 2, NOT -6. Marker expects one, you wrote the other.
**Cause:** `foldr op b [x1, x2, x3] = x1 `op` (x2 `op` (x3 `op` b))` (right-associative). `foldl op b [x1, x2, x3] = ((b `op` x1) `op` x2) `op` x3` (left-associative).
**Fix:** Default to `foldr` for "build a structure" (it preserves order, works on infinite lists). Default to `foldl'` for "compute a number" (stricter, more efficient). Don't use `foldl` (lazy) — it leaks space.
**Example wrong:**
```haskell
mySum :: [Int] -> Int
mySum = foldr (-) 0     -- BUG: subtraction is not commutative; wrong order
```
**Example right:**
```haskell
mySum :: [Int] -> Int
mySum = foldr (+) 0     -- + is commutative; either fold works
```
**Marks lost:** 2-4
**Seen in:** A10 archetype.

---

<a id="p-113"></a>
## P-113 · Forgotten parentheses around `(n-1)` in recursive call

**Topic:** Function application precedence
**Symptom:** Compile error "couldn't match Int with Int -> a". Function application binds tighter than `-`.
**Cause:** Writing `f n-1` which is `(f n) - 1`, not `f (n-1)`.
**Fix:** Always parenthesise recursive arguments that involve arithmetic.
**Example wrong:**
```haskell
factorial 0 = 1
factorial n = n * factorial n-1     -- parsed as (factorial n) - 1, type error
```
**Example right:**
```haskell
factorial 0 = 1
factorial n = n * factorial (n-1)
```
**Marks lost:** 5 (compile fail) — close to HIGH; this is MEDIUM because GHC catches it before submission if you compile-check.
**Seen in:** beginner recursion.

---

<a id="p-114"></a>
## P-114 · `map f . map g` vs `map (f . g)` — identity laws

**Topic:** Functor laws
**Symptom:** Functor law tests `fmap (f . g) = fmap f . fmap g` — should be equal but yours differs due to a subtle bug elsewhere.
**Cause:** Usually a symptom of a deeper Functor bug. `map f . map g` and `map (f . g)` ARE the same in Haskell — the issue is when one of them shadows a custom `fmap`.
**Fix:** When in doubt, prefer `fmap` to `map` for `Maybe`/tree-like things. Reserve `map` for `[]`.
**Marks lost:** 1-2
**Seen in:** A06 archetype.

---

<a id="p-115"></a>
## P-115 · `mapMTree` rebuilds with `Empty` in wrong slot

**Topic:** Monadic traversal
**Symptom:** Tree structure is destroyed. Marker compares shape; mismatch.
**Cause:** Pattern-matching `Fork x l r` but rebuilding as `Fork v' Empty r'` instead of `Fork v' l' r'`.
**Fix:** Shape preservation. Always rebuild with all three of `(f x)`, `mapMTree f l`, `mapMTree f r`.
**Example wrong:**
```haskell
mapMTree _ Empty        = return Empty
mapMTree f (Fork x l r) = do
  v' <- f x
  r' <- mapMTree f r
  return (Fork v' Empty r')      -- DROPPED LEFT
```
**Example right:**
```haskell
mapMTree _ Empty        = return Empty
mapMTree f (Fork x l r) = do
  v' <- f x
  l' <- mapMTree f l
  r' <- mapMTree f r
  return (Fork v' l' r')
```
**Marks lost:** 4 (whole `mapMTree` test)
**Seen in:** A01 × A03.

---

<a id="p-116"></a>
## P-116 · Monad instance — `>>=` not threading state correctly

**Topic:** Custom monad instance
**Symptom:** Functor laws pass but Monad laws fail — `m >>= return = m` violated.
**Cause:** Custom State-like monad with `>>=` that loses the state on the second step.
**Fix:** Write Monad instance MECHANICALLY. For `State s a = State (s -> (a, s))`:
```haskell
return x = State (\s -> (x, s))
(State p) >>= f = State (\s -> let (a, s') = p s
                                   State q = f a
                               in q s')
```
**Marks lost:** 3-5
**Seen in:** A06 / A24.

---

<a id="p-117"></a>
## P-117 · `lookup` returns `Maybe` — bound directly without case-on

**Topic:** Maybe handling
**Symptom:** Compile error. `lookup x env` returns `Maybe Int` but you've assigned it to `Int`.
**Cause:** Bare-binding the Maybe result. `let v = lookup x env` gives `v :: Maybe Int`, not `Int`.
**Fix:** Pattern-match or `case`:
```haskell
case lookup x env of
  Nothing -> Left ("unknown " ++ [x])
  Just v  -> Right v
```
**Marks lost:** 5 (compile fail) — close to HIGH.
**Seen in:** A08 env evaluator.

---

<a id="p-118"></a>
## P-118 · `do x <- mx; mx` runs `mx` twice (intentional but unintended)

**Topic:** Monad referential transparency
**Symptom:** State action runs twice, modifying state more than expected.
**Cause:** Forgetting that `<-` binds the result, but if you mention `mx` again, the ACTION runs again.
**Fix:** Bind once, reuse `x`. `do x <- mx; pure (use x)`, not `do x <- mx; mx`.
**Example wrong:**
```haskell
runStep :: NimGame ()
runStep = do x <- gameOver
             when (not x) (takeTokens 1 First >> gameOver >> pure ())
             --                                    ^^ runs gameOver TWICE per call
```
**Example right:**
```haskell
runStep = do over <- gameOver
             when (not over) (takeTokens 1 First)
```
**Marks lost:** 2-3
**Seen in:** A02 / A23.

---

<a id="p-119"></a>
## P-119 · `concatMap` confused with `map (concat .)` or `concat . map`

**Topic:** List monad / flatten
**Symptom:** Nested list when flat expected, or vice versa.
**Cause:** `concatMap f = concat . map f` — uses `f :: a -> [b]`. If `f` returns a single value, use `map`. If `f` returns a list, use `concatMap` to flatten.
**Fix:** Type-check mentally: `concatMap :: (a -> [b]) -> [a] -> [b]`.
**Example wrong:**
```haskell
flattenR (Branch xs) = map flattenR xs      -- returns [[a]], not [a]
```
**Example right:**
```haskell
flattenR (Branch xs) = concatMap flattenR xs
```
**Marks lost:** 3
**Seen in:** Rose tree flatten.

---

<a id="p-120"></a>
## P-120 · Pattern binding in `do`-block is INTENTIONAL — don't "fix" it

**Topic:** MonadFail in do
**Symptom:** You see `do IVal x <- eval env e1` and think "this is unsafe pattern matching" — replace with `case eval env e1 of IVal x -> ...`. Then your `Maybe` handling breaks because you didn't reproduce the auto-fail behaviour.
**Cause:** `IVal x <- ...` in a `do`-block over `Maybe` triggers `MonadFail` — if the pattern doesn't match, you get `Nothing`. This is the IDIOM for typed evaluators.
**Fix:** LEAVE IT ALONE. It's intentional. Document with a comment if you must.
**Example wrong (re-fix that breaks it):**
```haskell
eval env (Add e1 e2) = do
  v1 <- eval env e1
  v2 <- eval env e2
  case (v1, v2) of                                       -- "more explicit"...
    (IVal x, IVal y) -> Just (IVal (x + y))
    _                -> Nothing                          -- but the do-pattern already did this!
```
**Example right (idiomatic):**
```haskell
eval env (Add e1 e2) = do
  IVal x <- eval env e1                                   -- pattern-bind, MonadFail handles mismatch
  IVal y <- eval env e2
  return (IVal (x + y))
```
**Marks lost:** 0 (it works) — but you waste time
**Seen in:** A08, A14.

---

## See also

- `HIGH-severity.md` — marks-killers
- `LOW-severity.md` — style / efficiency
- `per-topic-pitfalls.md` — Ctrl-F index by topic
- [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) — full marker breakdown

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
