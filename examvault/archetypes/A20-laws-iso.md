<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A20 — Isomorphism / Retract / Typeclass Laws (Theory)**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · **A20** · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A20 — Isomorphism / Retract / Typeclass Laws (Theory)

**Tier:** 4   |   **Stars:** ⭐
**Mock appearance:** none   |   **Assignment appearance:** A2 Ex 5 specs `ramify ∘ tabulate = id` (retract); A3 Q1 specs both directions (iso)
**Combines with:** A07 · A12 · A06 · A22
**Search keywords:** isomorphism · retract · law · prove · show that · `f . g = id` · Functor laws · Monad laws · equational reasoning · structural induction

## What it tests
Whether you can VERIFY that two functions are mutually inverse (iso) or partially inverse (retract), AND whether you can prove typeclass laws (Functor, Monad) by structural induction on the data type.

## Recognition triggers
- "Show that `f . g = id`"
- "Prove that the Functor laws hold for your instance"
- "Establish that X is a retract of Y"
- "The types are NOT isomorphic, but …"
- Question stems with "verify", "prove", "show"
- W12 lecture is on "rigour" / equational reasoning

## Canonical template (proof skeleton)
```haskell
-- To prove   to . from = id   on   T a:
-- by structural induction on the argument t :: T a:
--
-- Base case (t = Lf x):
--   (to . from) (Lf x)
-- =  to (from (Lf x))                 -- def of (.)
-- =  to (Pure x)                      -- def of from
-- =  Lf x                             -- def of to
-- =  id (Lf x)                        -- def of id
--
-- Step case (t = Br ts):
-- Assume:  to . from ts = ts          (IH applies to each child)
--   (to . from) (Br ts)
-- =  to (Free (map from ts))          -- def of from
-- =  Br (map to (map from ts))        -- def of to
-- =  Br (map (to . from) ts)          -- map fusion
-- =  Br (map id ts)                   -- IH
-- =  Br ts                            -- map id
-- =  id (Br ts)                       ✓
```

## Mutations (the examiner picks one)

### M1 — `fromRose . toRose = id` (A3 Q1)
```
-- Base: fromRose (toRose (Pure x))
--      = fromRose (Lf x)
--      = Pure x ✓
-- Step: fromRose (toRose (Free xs))
--      = fromRose (Br (map toRose xs))
--      = Free (map fromRose (map toRose xs))
--      = Free (map (fromRose . toRose) xs)
--      = Free (map id xs)        -- IH
--      = Free xs ✓
```

### M2 — `ramify ∘ tabulate = id` (A2 Ex 5, retract)
This direction holds: traversing a tree to build a table, then building the tree from the table, reconstructs the same tree (modulo placeholder Empty subtrees, which the spec already produces).

The OTHER direction does NOT hold: `tabulate (ramify table)` is only a PERMUTATION of `table` — order changes because `tabulate` is in-order DFS.

### M3 — Functor identity law: `fmap id = id`
```
-- For MyMaybe:
-- fmap id MyNothing = MyNothing = id MyNothing ✓
-- fmap id (MyJust x) = MyJust (id x) = MyJust x = id (MyJust x) ✓
```

### M4 — Functor composition: `fmap (g . f) = fmap g . fmap f`
```
-- For MyMaybe (case MyJust x):
-- LHS: fmap (g . f) (MyJust x) = MyJust ((g . f) x) = MyJust (g (f x))
-- RHS: (fmap g . fmap f) (MyJust x)
--    = fmap g (fmap f (MyJust x))
--    = fmap g (MyJust (f x))
--    = MyJust (g (f x))   ✓
-- For MyNothing both sides give MyNothing ✓
```

### M5 — Monad left identity: `return x >>= f = f x`
```
-- For MyMaybe:
-- return x >>= f
-- = MyJust x >>= f
-- = f x       -- by def of >>= for MyJust
-- ✓
```

### M6 — Monad right identity: `m >>= return = m`
```
-- For MyMaybe:
-- MyNothing >>= return = MyNothing ✓
-- MyJust x >>= return = return x = MyJust x ✓
```

### M7 — Monad associativity
```
-- (m >>= f) >>= g  =  m >>= (\x -> f x >>= g)
-- Case m = MyNothing: both sides MyNothing ✓
-- Case m = MyJust x:
--   LHS: (MyJust x >>= f) >>= g
--      = f x >>= g
--   RHS: MyJust x >>= (\y -> f y >>= g)
--      = (\y -> f y >>= g) x
--      = f x >>= g  ✓
```

### M8 — Retract: `WorkingDay` of `WeekDay`
```haskell
toWeekDay :: WorkingDay -> WeekDay
toWeekDay Mon' = Mon ; ...

toWorkingDay :: WeekDay -> WorkingDay
toWorkingDay Sat = Fri'           -- fallback (lossy)
toWorkingDay Sun = Mon'           -- fallback (lossy)
toWorkingDay d   = matching        -- direct

-- toWorkingDay . toWeekDay = id   ✓
-- toWeekDay . toWorkingDay ≠ id   (Sat / Sun lost)
```

### M9 — `decode (encode s) = s` for Caesar
```
-- decode n (encode n s)
-- = map (shift (-n)) (map (shift n) s)
-- = map (shift (-n) . shift n) s
-- = map id s    -- since shift (-n) (shift n c) = c for all c
-- = s ✓
```

### M10 — `tabulate (ramify table) ≠ table` (counter-example)
```
-- Take table = [('A', [Beep]), ('B', [Silence])].
-- ramify table builds Branch Nothing (Leaf 'A') (Leaf 'B').
-- tabulate that gives [('A', [Beep]), ('B', [Silence])].
-- (Order may differ depending on impl — that's the permutation point.)
```

## Worked examples from this course
- Week 12 lecture: "rigour", equational reasoning, type retracts.
- Week 5 / 11: type retracts examples (`WorkingDay` of `WeekDay`).
- Assignment 2 Ex 5: `ramify . tabulate = id` claim with `tabulate (ramify t)` being only a permutation.
- Assignment 3 Q1: full iso for `toRose` / `fromRose`.
- Practice file: occasional "prove …" exercises.

## QuickCheck attack surface
For theory questions, QuickCheck-style equational reasoning is the marker:
- **Roundtrip on random input**: marker generates random `Rose a` of depth 5, checks `to (from r) == r`.
- **Both directions for iso, one direction for retract**: marker explicitly tests BOTH and rejects whichever direction doesn't hold.
- **Empty case**: must work on `Empty`, `Pure x`, smallest values.
- **Single element**: covered by base case.
- **Counter-example to non-laws**: marker may ask for an `x` such that `f (g x) /= x` — explicit witness.

## Pitfalls (marks-killers)
- **Claiming iso when only retract**: marks docked for over-claim. Read spec: "may be only a permutation" is a hint that `from . to ≠ id`.
- **Hand-waving the inductive step**: must explicitly invoke the IH "by induction" on the recursive call.
- **Missing the empty case**: structural induction has multiple base cases (often `Empty`, `[]`, `MyNothing`).
- **Using equational steps that aren't justified**: each `=` should cite "by def of f" or "by IH" or "by lemma X".
- **Forgetting `id` definition**: `id x = x` — sometimes you need to spell this out to bridge LHS and RHS.
- **Map fusion**: `map f (map g xs) = map (f . g) xs` — citeable lemma; don't skip.

## Combines-with deep dive

### A20 × A07 — proving codec round-trips
Every A07 exercise has a hidden A20 component: the round-trip law.

### A20 × A12 — proving rep-conv direction (iso vs retract)
Same skeleton as M1/M2. Identify which direction holds.

### A20 × A06 — proving Functor / Monad laws for your instance
Every custom `Functor` / `Monad` should be law-abiding. Marker may explicitly test.

### A20 × A22 — proving Eq is reflexive / Ord is transitive
For custom `Eq`/`Ord` instances on ADTs.

## See also

**Combines with:** [A05 ADT translation](./A05-adt-translation.md) · [A06 functor instance](./A06-functor-instance.md) · [A07 codec pair](./A07-codec-pair.md)
**Question families:** [codec](../question-families/codec-family.md)
**Theory:** [monad laws](../monads/monad-laws.md)
**QuickCheck:** [typeclass instance attacks](../quickcheck/typeclass-instance-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
