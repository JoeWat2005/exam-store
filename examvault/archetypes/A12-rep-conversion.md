<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A12 — Representation Conversion**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · **A12** · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A12 — Representation Conversion

**Tier:** 2   |   **Stars:** ⭐⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** A2 (ramify/tabulate), A3 (toRose/fromRose)
**Combines with:** A07 · A20 · A05
**Search keywords:** representation · isomorphic · retract · convert · ramify · tabulate · toRose · fromRose · to/from

## What it tests
Whether you can write two functions converting between two reps of "the same" data structure — possibly only one direction lossless (retract), and whether you can identify which direction is the iso and which is the retract.

## Recognition triggers
- Two equivalent data types are defined
- Functions named `toX` / `fromX`, or `ramify` / `tabulate`, or `toFoo` / `unFoo`
- Question says "the types are NOT isomorphic, but `f . g == id`" — that's a retract clue
- Both reps appear in the same module
- "Show that …" or "Establish a retract …"

## Canonical template
```haskell
-- A and B are two reps of the same data
to   :: A -> B
to   = ...

from :: B -> A
from = ...

-- iso:    to . from = id  AND  from . to = id
-- retract: to . from = id  but  from . to ≠ id  in general
```

## Mutations (the examiner picks one)

### M1 — `toRose` / `fromRose` (A3 Q1, iso)
```haskell
data Free f a = Pure a | Free (f (Free f a))
data Rose a   = Lf a | Br [Rose a]

toRose :: Free [] a -> Rose a
toRose (Pure x)  = Lf x
toRose (Free xs) = Br (map toRose xs)

fromRose :: Rose a -> Free [] a
fromRose (Lf x)  = Pure x
fromRose (Br xs) = Free (map fromRose xs)
```
What changes: parallel constructors `Lf↔Pure`, `Br↔Free`; both directions are total and inverse.

### M2 — `ramify` / `tabulate` (A2 Ex 4-5, retract only)
```haskell
data Tree = Empty | Branch (Maybe Char) Tree Tree
type Table = [(Char, [Bool])]   -- False = left, True = right

ramify :: Table -> Tree
ramify = foldr insertCode Empty
  where insertCode (ch, code) = insertAt code ch

tabulate :: Tree -> Table
tabulate t = go [] t
  where go _    Empty                  = []
        go pth (Branch Nothing  l r)   = go (pth ++ [False]) l ++ go (pth ++ [True]) r
        go pth (Branch (Just c) l r)   = (c, pth) : go (pth ++ [False]) l ++ go (pth ++ [True]) r
```
What changes: `ramify (tabulate t) == t` holds (retract); `tabulate (ramify table)` is only a permutation of `table`.

### M3 — `intToNat` / `natToInt` (Lazy Nat)
```haskell
data Nat = Zero | Succ Nat

intToNat :: Int -> Nat
intToNat 0 = Zero
intToNat n = Succ (intToNat (n - 1))

natToInt :: Nat -> Int
natToInt Zero     = 0
natToInt (Succ n) = 1 + natToInt n
```
What changes: iso on `n >= 0`; partial on negatives.

### M4 — `listToBT` / `btToList` (in-order)
```haskell
btToList :: BT a -> [a]
btToList Empty        = []
btToList (Fork x l r) = btToList l ++ [x] ++ btToList r

listToBT :: Ord a => [a] -> BT a
listToBT = foldr insertBST Empty
```
What changes: only a retract — `btToList . listToBT == sort . nub`, not original list.

### M5 — `cardinal` / `direction` (encode 4-way as Int)
```haskell
data Dir = N | E | S | W

dirToInt :: Dir -> Int
dirToInt N = 0; dirToInt E = 1; dirToInt S = 2; dirToInt W = 3

intToDir :: Int -> Maybe Dir
intToDir 0 = Just N
intToDir 1 = Just E
intToDir 2 = Just S
intToDir 3 = Just W
intToDir _ = Nothing
```
What changes: iso on the subset {0,1,2,3}; partial on the larger type.

### M6 — `toMatrix` / `toList` (2D ↔ flat)
```haskell
toMatrix :: Int -> [a] -> [[a]]
toMatrix _ [] = []
toMatrix n xs = take n xs : toMatrix n (drop n xs)

fromMatrix :: [[a]] -> [a]
fromMatrix = concat
```
What changes: iso when length divides cleanly; retract `fromMatrix . toMatrix n == id`.

### M7 — `setToList` / `listToSet` (Set as sorted list)
```haskell
newtype Set a = Set [a]

setToList :: Set a -> [a]
setToList (Set xs) = xs

listToSet :: Ord a => [a] -> Set a
listToSet = Set . sort . nub
```
What changes: retract; `listToSet . setToList == id` on a well-formed Set.

### M8 — `Maybe a` ↔ `[a]` (zero-or-one)
```haskell
maybeToList :: Maybe a -> [a]
maybeToList Nothing  = []
maybeToList (Just x) = [x]

listToMaybe :: [a] -> Maybe a
listToMaybe []     = Nothing
listToMaybe (x:_)  = Just x
```
What changes: retract: `listToMaybe . maybeToList == id`; the inverse drops everything after position 0.

### M9 — `(a -> b)` ↔ `[(a, b)]` (function ↔ assoc list)
```haskell
funToList :: [a] -> (a -> b) -> [(a, b)]
funToList dom f = [(x, f x) | x <- dom]

listToFun :: Eq a => b -> [(a, b)] -> (a -> b)
listToFun def xs y = maybe def id (lookup y xs)
```
What changes: depends on `dom` being given; iso when keys cover the function domain.

### M10 — `Bracket` ↔ `String` (A2 Ex 6, partial)
```haskell
brackets :: Bracket -> String
brackets (Round ts) = "(" ++ concatMap brackets ts ++ ")"
brackets (Curly ts) = "{" ++ concatMap brackets ts ++ "}"

tree :: String -> Maybe Bracket
tree s = case parseB s of [(t, "")] -> Just t; _ -> Nothing
```
What changes: `tree . brackets == Just`; the inverse is only partial (rejects ill-formed strings).

## Worked examples from this course
- Assignment 2 Ex 4-5: `ramify` / `tabulate` — retract — M2.
- Assignment 2 Ex 6: `brackets` / `tree` — partial inverse — M10.
- Assignment 3 Q1: `toRose` / `fromRose` — iso — M1.
- Problem sheet Set 15 (#146): `ramify` / `tabulate` repeated.
- Week 5 / 11: type retracts lecture.

## QuickCheck attack surface
- **Iso check both directions**: `to . from = id` AND `from . to = id`. Marker will run BOTH.
- **Retract check**: only `to . from = id`. The other direction fails on at least one example.
- **Edge: empty / leaf**: both directions on the smallest input. `toRose (Pure x) == Lf x` and back.
- **Single-element list**: `intToNat 0 == Zero`, `intToNat 1 == Succ Zero`.
- **Composition**: `(to . from . to . from) x == to (from x)` — idempotent retract.
- **Large random input**: marker generates a random `Rose a` of depth 5, checks `fromRose (toRose r) == r`. If you got `Br` / `Free` mixed up, fails immediately.

## Pitfalls (marks-killers)
- **Confusing iso with retract**: writing both directions and claiming iso when only retract holds. The auto-marker checks the actual property.
- **Forgetting `map` in the recursive call**: `toRose (Free xs) = Br xs` — type error. Should be `Br (map toRose xs)`.
- **Cross-wiring constructors**: `toRose (Free xs) = Lf …` instead of `Br …`. Catastrophic but easy to miss in long files.
- **Partial function on the inverse**: `intToDir 99` — if you write `intToDir _ = N`, you violate the iso. Return `Nothing` (use `Maybe`).
- **`++ [path]` building paths**: O(n²); use difference lists or reverse-and-cons for big trees.
- **State / list duplication**: `tabulate` should NOT call `nub`; the trees have unique labels (except for Empty pseudo-branches).

## Combines-with deep dive

### A12 × A07 — codec is a special-case rep-conv
Every codec (A07) is a rep-conv (A12) with extra structure (delimiters / lookup tables).

### A12 × A20 — proving the round-trip
```haskell
-- by structural induction on Rose a:
-- Base: fromRose (toRose (Lf x)) = fromRose (Lf x) = Pure x = … wait, that's wrong.
-- Actually:  toRose (fromRose (Lf x)) = toRose (Pure x) = Lf x ✓
-- Step: toRose (fromRose (Br xs))
--       = toRose (Free (map fromRose xs))
--       = Br (map toRose (map fromRose xs))
--       = Br (map (toRose . fromRose) xs)
--       = Br (map id xs)               -- by induction hypothesis
--       = Br xs ✓
```

### A12 × A05 — translation IS one direction of rep-conv
If the two reps differ in expressiveness (Sugar vs Core), the translation direction is A05; the inverse (if it exists) completes the iso.

## See also

**Combines with:** [A05 ADT translation](./A05-adt-translation.md) · [A07 codec pair](./A07-codec-pair.md) · [A09 prelude reimpl](./A09-prelude-reimpl.md)
**Question families:** [codec](../question-families/codec-family.md) · [list-rewrite](../question-families/list-rewrite-family.md)
**QuickCheck:** [codec attacks](../quickcheck/codec-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
