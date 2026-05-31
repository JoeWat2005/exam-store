<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A22 — Generic Typeclass Instance (Eq / Ord / Show / Read) (NEW)**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · **A22** · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A22 — Generic Typeclass Instance (Eq / Ord / Show / Read) (NEW)

**Tier:** 2   |   **Stars:** ⭐⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** A1 (custom Show), A2 (Tree derives Eq)
**Combines with:** A06 · A13 · A11 · A01
**Search keywords:** instance Eq · instance Ord · instance Show · class · MyEq · custom class · `===` · without deriving

## Justification for inclusion as its own archetype
A06 covers `* -> *` typeclasses (Functor / Applicative / Monad), but the course also tests `*` typeclasses (Eq, Ord, Show), and crucially DEFINING your own typeclass (problem 69's `MyEq`). The skill set is different: no `fmap`, but pattern-matching on multiple constructors symmetrically (Eq) or asymmetrically (Ord, Show). Problem 69, problem 64 (custom Show), problem 68 (Set with Ord-derived membership) all live here, not in A06. Worth a separate archetype to make the recognition triggers crisp.

## What it tests
Whether you can write `instance Eq T where (==) = …` (or Ord/Show) for a custom ADT, AND whether you can DEFINE your own typeclass with its own method.

## Recognition triggers
- `instance Eq T where (==) = …` (or Ord, Show)
- "Make `T` an instance of `Eq` without using deriving"
- `class MyEq a where (===) :: a -> a -> Bool`
- "Define a class `Foo` …"
- A data type WITHOUT `deriving (Eq, Show)` annotation
- Question explicitly says "no deriving"

## Canonical template
```haskell
data T = TBase | TStep Int T

instance Eq T where
  TBase           == TBase           = True
  TStep n1 t1     == TStep n2 t2     = n1 == n2 && t1 == t2
  _               == _               = False

instance Ord T where
  compare TBase           TBase           = EQ
  compare TBase           _               = LT
  compare _               TBase           = GT
  compare (TStep n1 t1)   (TStep n2 t2)   = compare (n1, t1) (n2, t2)

instance Show T where
  show TBase         = "TBase"
  show (TStep n t)   = "TStep " ++ show n ++ " (" ++ show t ++ ")"
```

## Mutations (the examiner picks one)

### M1 — `class MyEq` from scratch (problem 69)
```haskell
class MyEq a where
  (===) :: a -> a -> Bool

instance MyEq Bool where
  True  === True  = True
  False === False = True
  _     === _     = False

instance MyEq Int where
  m === n = m == n
```
What changes: defines the class AND multiple instances.

### M2 — `MyEq` for pairs (problem 69 cont.)
```haskell
instance (MyEq a, MyEq b) => MyEq (a, b) where
  (a1, b1) === (a2, b2) = a1 === a2 && b1 === b2
```
What changes: compound constraint; uses `===` (your method) recursively, NOT `==`.

### M3 — `MyEq` for lists
```haskell
instance MyEq a => MyEq [a] where
  []     === []     = True
  (x:xs) === (y:ys) = x === y && xs === ys
  _      === _      = False
```
What changes: constraint on element type; structural recursion on cons.

### M4 — `Eq BT a` from scratch
```haskell
instance Eq a => Eq (BT a) where
  Empty           == Empty           = True
  Fork x1 l1 r1   == Fork x2 l2 r2   = x1 == x2 && l1 == l2 && r1 == r2
  _               == _               = False
```
What changes: instance for `* -> *` type but with `* -> *` Eq (kind needs `Eq a`).

### M5 — `Ord` for `WeekDay` (problem 62)
```haskell
data WeekDay = Mon | Tue | Wed | Thu | Fri | Sat | Sun

instance Ord WeekDay where
  compare a b = compare (ix a) (ix b)
    where ix Mon = 0; ix Tue = 1; ix Wed = 2; ix Thu = 3
          ix Fri = 4; ix Sat = 5; ix Sun = 6
```
What changes: maps to a comparable type (Int); compare on the indices.

### M6 — `Show Vec3` (problem 65)
```haskell
data Vec3 = Vec3 Double Double Double

instance Show Vec3 where
  show (Vec3 x y z) = "(" ++ show x ++ ", " ++ show y ++ ", " ++ show z ++ ")"
```
What changes: tuple-like display; constructor name suppressed.

### M7 — `class Container c where empty, insert, member`
```haskell
class Container c where
  empty  :: c a
  insert :: Eq a => a -> c a -> c a
  member :: Eq a => a -> c a -> Bool

instance Container [] where
  empty             = []
  insert x xs       = if x `elem` xs then xs else x : xs
  member            = elem
```
What changes: custom multi-method class; instance for an existing type.

### M8 — `Ord Color` lexicographic
```haskell
data Color = Red | Green | Blue | Custom Int Int Int

instance Eq Color where
  Red == Red               = True
  Green == Green           = True
  Blue == Blue             = True
  Custom r1 g1 b1 == Custom r2 g2 b2 = r1 == r2 && g1 == g2 && b1 == b2
  _ == _                   = False

instance Ord Color where
  Red `compare` Red         = EQ
  Red `compare` _           = LT
  _   `compare` Red         = GT
  Green `compare` Green     = EQ
  Green `compare` _         = LT
  -- … etc.
```
What changes: many constructors; pattern-match all pairs (or fall through with `_`).

### M9 — `Set a` membership via `Ord` (problem 68)
```haskell
newtype Set a = Set [a]      -- invariant: sorted, no duplicates

memberS :: Ord a => a -> Set a -> Bool
memberS x (Set xs) = go xs
  where go []                    = False
        go (y:ys) | x == y       = True
                  | x < y        = False         -- sorted, won't appear later
                  | otherwise    = go ys
```
What changes: uses `Ord` constraint to optimise; early termination.

### M10 — `class Default a where def`
```haskell
class Default a where
  def :: a

instance Default Int        where def = 0
instance Default [a]        where def = []
instance Default (Maybe a)  where def = Nothing
instance (Default a, Default b) => Default (a, b) where def = (def, def)
```
What changes: niladic method (no argument); constraint-propagation for products.

## Worked examples from this course
- Problem sheet Set 7 (#62): `WeekDay` `Eq`/`Ord` (probably derived, but spec allows hand-roll).
- Problem sheet Set 7 (#64): `Color` custom Show — M6, M8.
- Problem sheet Set 7 (#65): `Vec3` ops — M6.
- Problem sheet Set 7 (#66-68): `Stack`, `Queue`, `Set` — typeclass-style data structures.
- Problem sheet Set 7 (#69): `MyEq` — M1, M2, M3.
- Assignment 1: custom Show for `GridWithAPointer` and `Grid`.
- Assignment 2: `data Tree = Empty | Branch (Maybe Char) Tree Tree deriving (Show, Eq)` — uses derived, but a no-deriving variant could be exam-set.

## QuickCheck attack surface
- **Reflexivity** of Eq: `x == x == True` for arbitrary `x`.
- **Symmetry** of Eq: `x == y == y == x`.
- **Transitivity** of Eq: `x == y && y == z ==> x == z`.
- **Antisymmetry** of Ord: `x <= y && y <= x ==> x == y`.
- **Totality** of Ord: `x <= y || y <= x == True`.
- **Show is consistent with `read`**: `read (show x) == x` (only if `Read` is also defined).
- **Compound type tests**: `(1, 2) == (1, 2)`, `[1, 2] == [1, 2]`.
- **Single character difference**: `[1, 2] == [1, 3] == False`.

## Pitfalls (marks-killers)
- **Missing `_ == _ = False` clause**: GHC warns of `Non-exhaustive` on `Empty == Fork…`. Adds a default `False`.
- **Using `(==)` instead of `===`** in MyEq's instance bodies — defeats the exercise. The body must use the class's own method.
- **Forgetting `Eq a =>` constraint** on `instance Eq (T a)` for parametric types.
- **Confusing `compare` and `(==)`**: `Ord` requires `compare` (returns `Ordering`); `Eq` requires `(==)` (returns `Bool`).
- **Lexicographic order on multi-field constructors**: `compare (TStep n1 t1) (TStep n2 t2) = compare (n1, t1) (n2, t2)` uses tuple's built-in lex order. Manually you'd write `let c = compare n1 n2 in if c == EQ then compare t1 t2 else c`.
- **`Show` for recursive types**: must NOT infinite-loop on cyclic data (lazy data); use bounded depth or rely on the data being acyclic.

## Combines-with deep dive

### A22 × A11 — Eq/Ord for BST keys
The BST type needs `Ord a =>` everywhere. If `a` is itself a custom type, you write A22-style instances.

### A22 × A06 — full typeclass package
A custom container often needs both `Functor` (A06) AND `Eq`/`Show` (A22). Write both.

### A22 × A13 — Show for the same type
A22 covers `instance Show T` at a structural level; A13 is the same idea with pretty-printing twists (ANSI, indentation).

## See also

**Combines with:** [A06 functor instance](./A06-functor-instance.md) · [A24 applicative instance](./A24-applicative-instance.md)
**Question families:** [applicative-monad-instance](../question-families/applicative-monad-instance-family.md) · [functor-instance](../question-families/functor-instance-family.md)
**Theory:** [Monad typeclass](../typeclasses/monad.md) · [Applicative typeclass](../typeclasses/applicative.md) · [Functor typeclass](../typeclasses/functor.md)
**QuickCheck:** [typeclass instance attacks](../quickcheck/typeclass-instance-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
