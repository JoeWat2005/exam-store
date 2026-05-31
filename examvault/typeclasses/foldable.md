<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [typeclasses](./README.md) · **Foldable**

<!-- siblings:start -->
> **Peers:** [alternative](./alternative.md) · [applicative](./applicative.md) · [eq-ord](./eq-ord.md) · **foldable** · [functor](./functor.md) · [monad](./monad.md) · [monoid](./monoid.md) · [num](./num.md) · [show](./show.md) · [traversable](./traversable.md)
<!-- siblings:end -->






# Foldable

> **Mental model:** *Reduce a structure to a single summary value, throwing away the shape.* You define ONE of `foldMap` or `foldr` — every other Foldable method (length, sum, toList, maximum, any, all, elem) comes for free.

**Methods (minimal):** `foldMap :: Monoid m => (a -> m) -> t a -> m` OR `foldr :: (a -> b -> b) -> b -> t a -> b`.

**Laws (none beyond consistency):** `foldMap f = foldr (mappend . f) mempty`.

**Search keywords:** Foldable, foldMap, foldr, foldl, toList, Foldable BT, Foldable Rose, length, sum, product, any, all, elem, maximum, minimum

## Recognition triggers

- "Define `sum` / `length` / `toList` for `T`"
- "Make `T` Foldable so that..."
- "What's the `Monoid` used here?" (foldMap target)
- Question hands you ADT and asks for *aggregate* operations.

## Class

```haskell
class Foldable t where
  foldMap :: Monoid m => (a -> m) -> t a -> m
  foldr   :: (a -> b -> b) -> b -> t a -> b

  -- Derived (free):
  fold    :: Monoid m => t m -> m
  foldl   :: (b -> a -> b) -> b -> t a -> b
  toList  :: t a -> [a]
  null    :: t a -> Bool
  length  :: t a -> Int
  elem    :: Eq a => a -> t a -> Bool
  sum     :: Num a => t a -> a
  product :: Num a => t a -> a
  maximum :: Ord a => t a -> a
  minimum :: Ord a => t a -> a
```

## Minimal definition strategy

**Define `foldMap` if your structure has a natural traversal order.** Then `foldr` is automatic:

```haskell
foldr f z t = appEndo (foldMap (Endo . f) t) z
```

**Define `foldr` if you're more comfortable with classic list-style folds.** Then `foldMap` follows:

```haskell
foldMap f t = foldr (mappend . f) mempty t
```

## Canonical templates per ADT

### Binary tree (BT) — in-order via foldMap

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

instance Foldable BT where
  foldMap _ Empty        = mempty
  foldMap f (Fork x l r) = foldMap f l <> f x <> foldMap f r
```

This gives you in-order traversal. Variants:
- Pre-order: `f x <> foldMap f l <> foldMap f r`
- Post-order: `foldMap f l <> foldMap f r <> f x`

With this single definition you can do:
```haskell
toList t      -- in-order list of values
sum t         -- sum (requires Num a)
length t      -- count of values
elem 3 t      -- search
maximum t     -- max value
```

### Rose tree

```haskell
data Rose a = Leaf a | Branch [Rose a]

instance Foldable Rose where
  foldMap f (Leaf x)    = f x
  foldMap f (Branch xs) = foldMap (foldMap f) xs
  -- outer foldMap on the LIST (uses [] Foldable)
  -- inner foldMap on each Rose
```

The double `foldMap (foldMap f) xs` parallels the `map (fmap f)` pattern in Functor — you delegate to the list's Foldable, then to each child's Foldable.

### Expr (typical interpreter ADT — collect free variables)

```haskell
data Expr v = Var v
            | Lit Int
            | Add (Expr v) (Expr v)
            | Mul (Expr v) (Expr v)

instance Foldable Expr where
  foldMap _ (Lit _)     = mempty
  foldMap f (Var v)     = f v
  foldMap f (Add e1 e2) = foldMap f e1 <> foldMap f e2
  foldMap f (Mul e1 e2) = foldMap f e1 <> foldMap f e2

-- Now: free variables = foldMap (:[]) expr
-- Now: number of vars  = length (foldMap (:[]) expr)   -- whitelist-safe
--   (the Sum version  = getSum (foldMap (\_ -> Sum 1) expr)  needs Data.Monoid — see warning below)
```

### Pair (homogeneous)

```haskell
data Pair a = Pair a a

instance Foldable Pair where
  foldMap f (Pair x y) = f x <> f y
```

### Maybe-like

```haskell
data MyMaybe a = MyNothing | MyJust a

instance Foldable MyMaybe where
  foldMap _ MyNothing  = mempty
  foldMap f (MyJust x) = f x
```

### Either (only the Right is foldable)

```haskell
instance Foldable (Either e) where
  foldMap _ (Left _)  = mempty
  foldMap f (Right x) = f x
```

### Const (phantom — nothing to fold)

```haskell
instance Foldable (Const m) where
  foldMap _ _ = mempty
```

## How `foldr` follows from `foldMap`

You can think of `foldMap f t` as "the values mapped to a monoid, concatenated in traversal order". Then:

```haskell
foldr g z t = foldr g z (toList t)   -- conceptually
            = foldMap (\x -> Endo (g x)) t `appEndo` z   -- via Endo trick
```

In practice you define ONE; you don't need to derive the other manually.

## Direct `foldr` instances (if you prefer)

### BT
```haskell
instance Foldable BT where
  foldr _ z Empty        = z
  foldr f z (Fork x l r) = foldr f (f x (foldr f z r)) l   -- in-order
```

### Rose
```haskell
instance Foldable Rose where
  foldr f z (Leaf x)    = f x z
  foldr f z (Branch xs) = foldr (\t acc -> foldr f acc t) z xs
```

## Useful aggregations via Foldable

> **WARNING — the Monoid wrappers below are NOT all whitelisted.**
> `Sum`/`Product`/`Any`/`All`/`First`/`Last` live in **`Data.Monoid`**, and
> `Max`/`Min` live in **`Data.Semigroup`** — **neither module is on the exam
> allow-list** (importing them scores 0), and `Control.Monad.Writer` does not
> re-export them. Prefer the **import-free** forms below; reach for the wrappers
> only if the question's own Types module already provides them.

```haskell
-- toList for any Foldable (import-free)
toList = foldr (:) []          -- or  foldMap (:[])

-- count nodes (import-free): length of the toList
size t = length (foldr (:) [] t)

-- collect all values (import-free)
allValues t = foldr (:) [] t

-- any / all (import-free): Prelude's any/all already work on any Foldable
anyP p t = any p t             -- no wrappers needed
allP p t = all p t

-- find first (import-free)
findFirst p t = case filter p (foldr (:) [] t) of (x:_) -> Just x; [] -> Nothing
```

A direct recursive count (no Foldable at all) is just as exam-safe:

```haskell
size :: BT a -> Int
size Empty        = 0
size (Fork _ l r) = 1 + size l + size r
```

> **Only if Types provides them** — the `Data.Monoid`/`Data.Semigroup` forms:
> ```haskell
> import Data.Monoid    (Sum(..), Any(..), All(..), First(..))  -- NOT whitelisted
> import Data.Semigroup (Max(..), Min(..))                       -- NOT whitelisted
> size t       = getSum (foldMap (\_ -> Sum 1) t)
> anyP p       = getAny . foldMap (Any . p)
> allP p       = getAll . foldMap (All . p)
> findFirst p  = getFirst . foldMap (\x -> First (if p x then Just x else Nothing))
> maxOf t      = getMax (foldMap Max t)   -- also needs a non-empty / Bounded story
> ```

## Pitfalls

- **Foldable ≠ Functor.** `foldMap` cannot change the structure — it only summarises. (`fmap` preserves, `foldMap` flattens.)
- **`foldMap _ Empty = mempty`**, not `[]` — `mempty` is generic; specific Monoid decides what "empty result" means.
- **`Monoid m =>` constraint** is REQUIRED on `foldMap`'s definition (it appears in the class).
- **Rose tree double-foldMap** trips students — `foldMap (foldMap f) xs` (outer for list, inner for child rose).
- **Either folds only the Right** — same as Functor.
- **Don't reimplement `length`**: it comes free from Foldable. If you must spell it out whitelist-safely, use `length . foldr (:) []` (the `foldMap (const (Sum 1))` form needs the non-whitelisted `Data.Monoid`).
- **`sum` ambiguity**: `Foldable.sum :: Num a => t a -> a` — your `t` must contain values of a `Num` type.

## Foldable consistency as QuickCheck props

```haskell
prop_foldMap_consistent :: (Foldable t, Monoid m, Eq m) => Fun a m -> t a -> Bool
prop_foldMap_consistent (Fun _ f) t =
  foldMap f t == foldr (mappend . f) mempty t

prop_toList_length :: Foldable t => t a -> Bool
prop_toList_length t = length (toList t) == length t

prop_sum_via_toList :: (Foldable t, Num a, Eq a) => t a -> Bool
prop_sum_via_toList t = sum t == sum (toList t)
```

## QuickCheck attacks

- `foldMap` consistent with `foldr`.
- `toList . pure == [x]` for `Applicative + Foldable`.
- `length t == size_by_hand t`.
- `sum (fmap (+1) t) == sum t + length t` (Functor-Foldable interaction).

## See also

**Archetypes:** [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)
**Question families:** [list-fold](../question-families/list-fold-family.md)
**Related (typeclasses):** [traversable](./traversable.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
