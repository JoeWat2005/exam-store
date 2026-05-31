<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [typeclasses](./README.md) · **Eq and Ord**

<!-- siblings:start -->
> **Peers:** [alternative](./alternative.md) · [applicative](./applicative.md) · **eq-ord** · [foldable](./foldable.md) · [functor](./functor.md) · [monad](./monad.md) · [monoid](./monoid.md) · [num](./num.md) · [show](./show.md) · [traversable](./traversable.md)
<!-- siblings:end -->






# Eq and Ord

> **Mental model:** `Eq` = "can these two values be tested for equality?". `Ord` = "can these two values be compared for less-than / greater-than?". `Ord` extends `Eq` — every `Ord` instance must also be `Eq`. For most ADTs you `deriving (Eq, Ord)`; you write the instance by hand only when you need custom rules (e.g. case-insensitive strings, semantic equality, custom ordering).

**Eq methods:** `(==), (/=) :: a -> a -> Bool`. MINIMAL = one of `(==)` or `(/=)`.
**Ord methods:** `compare :: a -> a -> Ordering`, `(<), (<=), (>=), (>) :: a -> a -> Bool`, `min, max :: a -> a -> a`. MINIMAL = `compare` or `(<=)`.

**Eq laws:**
- Reflexivity:   `x == x = True`
- Symmetry:      `x == y = y == x`
- Transitivity:  `x == y && y == z ==> x == z`

**Ord laws:**
- Transitivity, antisymmetry, totality (any two values are comparable).
- Consistency with Eq: `compare x y == EQ ⟺ x == y`.

**Search keywords:** instance Eq, instance Ord, compare, Ordering, LT EQ GT, deriving Eq Ord, lex order, antisymmetry

## Recognition triggers

- "Define `(==)` for `T`"
- "Implement `compare` for `T`"
- "Why does `deriving Ord` give this order?" (it uses ctor declaration order)
- "Sort a list of `T` by..." (need Ord)
- "Make `T` work with `Map`/`Set`" (need Ord)

## Class

```haskell
class Eq a where
  (==), (/=) :: a -> a -> Bool

  -- Defaults, mutually defined:
  x /= y = not (x == y)
  x == y = not (x /= y)

class Eq a => Ord a where
  compare              :: a -> a -> Ordering
  (<), (<=), (>=), (>) :: a -> a -> Bool
  max, min             :: a -> a -> a
```

The `Ordering` type:
```haskell
data Ordering = LT | EQ | GT
              deriving (Eq, Ord, Show, Bounded, Enum)
```

## Default `Eq` / `Ord` from `compare`

```haskell
x == y    = compare x y == EQ
x /= y    = compare x y /= EQ
x <= y    = compare x y /= GT
x <  y    = compare x y == LT
x >= y    = compare x y /= LT
x >  y    = compare x y == GT
max x y   = if x >= y then x else y
min x y   = if x <= y then x else y
```

So if you implement just `compare`, every other method is free.

## Canonical templates

### Custom enum

```haskell
data Color = Red | Green | Blue

instance Eq Color where
  Red   == Red   = True
  Green == Green = True
  Blue  == Blue  = True
  _     == _     = False

instance Ord Color where
  compare Red   Red   = EQ
  compare Red   _     = LT
  compare _     Red   = GT
  compare Green Green = EQ
  compare Green _     = LT
  compare _     Green = GT
  compare Blue  Blue  = EQ
```

(Or just `deriving (Eq, Ord)` — but the order would be `Red < Green < Blue` based on declaration order.)

### Custom list-like

```haskell
data MyList a = Nil | Cons a (MyList a)

instance Eq a => Eq (MyList a) where
  Nil       == Nil       = True
  Cons x xs == Cons y ys = x == y && xs == ys
  _         == _         = False

instance Ord a => Ord (MyList a) where
  compare Nil         Nil         = EQ
  compare Nil         _           = LT
  compare _           Nil         = GT
  compare (Cons x xs) (Cons y ys) = case compare x y of
    EQ    -> compare xs ys
    other -> other
```

This is the classic lexicographic order — note the case-on-compare idiom.

### BT (lex by in-order traversal — example)

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

instance Eq a => Eq (BT a) where
  Empty        == Empty        = True
  Fork x l r   == Fork y p q   = x == y && l == p && r == q
  _            == _            = False

instance Ord a => Ord (BT a) where
  compare Empty       Empty         = EQ
  compare Empty       _             = LT
  compare _           Empty         = GT
  compare (Fork x l r) (Fork y p q) = case compare x y of
    EQ -> case compare l p of
      EQ -> compare r q
      o  -> o
    o  -> o
```

### Pair

```haskell
instance (Eq a, Eq b) => Eq (Pair a b) where
  Pair x1 y1 == Pair x2 y2 = x1 == x2 && y1 == y2

instance (Ord a, Ord b) => Ord (Pair a b) where
  compare (Pair x1 y1) (Pair x2 y2) = case compare x1 x2 of
    EQ -> compare y1 y2
    o  -> o
```

### Either

```haskell
instance (Eq a, Eq b) => Eq (Either a b) where
  Left  x == Left  y = x == y
  Right x == Right y = x == y
  _       == _       = False

instance (Ord a, Ord b) => Ord (Either a b) where
  compare (Left  x) (Left  y) = compare x y
  compare (Left  _) (Right _) = LT          -- Left < Right (by ctor order)
  compare (Right _) (Left  _) = GT
  compare (Right x) (Right y) = compare x y
```

### Ord-of-Ord — tree of trees

If `BT a` is `Ord` (as above), then `BT (BT a)` is `Ord` automatically — the same `instance Ord a => Ord (BT a)` applies with `a := BT a` (assuming the recursive type works out; usually you don't need to repeat).

## `compare` discipline

When writing `compare` for a tagged ADT:
1. Same constructor on both sides: recurse via `case compare ... of EQ -> ... ; o -> o`.
2. Different constructors: order by ctor declaration order (mimicking `deriving Ord`).
3. Always pattern-match exhaustively — the `_ _` fallthrough hides bugs.

Idiomatic case-on-compare cascade:

```haskell
compare (X a1 b1 c1) (X a2 b2 c2) =
  case compare a1 a2 of
    EQ -> case compare b1 b2 of
      EQ -> compare c1 c2
      o  -> o
    o  -> o
```

## `comparing` and `on` helpers

```haskell
import Data.Ord     (comparing)
import Data.Function ((`on`))

comparing :: Ord b => (a -> b) -> a -> a -> Ordering
comparing f x y = compare (f x) (f y)

-- Sort by some field:
sortBy (comparing fst) [(3,"a"), (1,"b"), (2,"c")]

-- Equivalent via on:
sortBy (compare `on` fst) [...]
```

Useful when you want to order by one field of a record/tuple.

## Pitfalls

- **`deriving Ord` uses ctor declaration order.** So `data Player = X | O | B` would give `X < O < B`. If you want `B < O < X` you must rearrange or write `instance Ord` by hand. (This bit course minimax problems.)
- **Don't forget `Eq` before `Ord`.** `class Eq a => Ord a` — declaring `instance Ord T` without `instance Eq T` is an error.
- **`Eq` allows custom semantic equality** (e.g. case-insensitive strings) but you must preserve symmetry/transitivity.
- **`compare x y` may be EQ even when `x` and `y` are structurally different** (custom Ord). That's allowed if you want; but it interacts oddly with `==`.
- **`min` and `max` are total for Ord.** They must be defined for any two values, no `Maybe`.
- **Constraint propagation:** `instance Eq a => Eq (T a)` — without the constraint you can't `==` inside.
- **Use `case compare ... of EQ -> ... ; o -> o`**, NOT three separate `compare` calls (efficiency + clarity).

## Eq + Ord laws as QuickCheck props

```haskell
prop_eq_refl  :: Eq a => a -> Bool
prop_eq_refl  x = x == x

prop_eq_symm  :: Eq a => a -> a -> Bool
prop_eq_symm  x y = (x == y) == (y == x)

prop_eq_trans :: Eq a => a -> a -> a -> Property
prop_eq_trans x y z = (x == y && y == z) ==> x == z

prop_ord_total :: Ord a => a -> a -> Bool
prop_ord_total x y = compare x y `elem` [LT, EQ, GT]

prop_ord_antisym :: Ord a => a -> a -> Bool
prop_ord_antisym x y =
  (compare x y == EQ) == (compare y x == EQ)

prop_ord_consistent_eq :: (Ord a, Eq a) => a -> a -> Bool
prop_ord_consistent_eq x y = (compare x y == EQ) == (x == y)
```

## QuickCheck attacks

- Reflexivity / symmetry / transitivity of `==`.
- Consistency: `compare x y == EQ ⟺ x == y`.
- Totality: every pair has exactly one of `LT, EQ, GT`.
- `min x y == min y x` (commutative under EQ).
- For derived instances: matches expected ctor order.

## See also

**Archetypes:** [A11 BST ops](../archetypes/A11-bst-ops.md)
**Question families:** [bst-ops](../question-families/bst-ops-family.md)
**QuickCheck:** [bst attacks](../quickcheck/bst-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
