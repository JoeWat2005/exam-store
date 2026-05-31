<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [typeclasses](./README.md) · **Semigroup and Monoid**

<!-- siblings:start -->
> **Peers:** [alternative](./alternative.md) · [applicative](./applicative.md) · [eq-ord](./eq-ord.md) · [foldable](./foldable.md) · [functor](./functor.md) · [monad](./monad.md) · **monoid** · [num](./num.md) · [show](./show.md) · [traversable](./traversable.md)
<!-- siblings:end -->






# Semigroup and Monoid

> **Mental model:** A `Semigroup` says "I have an associative binary op `<>`". A `Monoid` adds "and an identity element `mempty`". This is the algebra of *combining things in order*: appending lists, summing numbers, joining logs, picking maxima. Every `Writer` log, every `Foldable` aggregation, every parser-combinator concatenation rests on Monoid.

**Semigroup method:** `(<>) :: a -> a -> a`. Associative.
**Monoid methods:** `mempty :: a`, `mappend :: a -> a -> a` (= `<>`), `mconcat :: [a] -> a`.

**Monoid laws:**
- Left identity:  `mempty <> x = x`
- Right identity: `x <> mempty = x`
- Associativity:  `(x <> y) <> z = x <> (y <> z)`

**Search keywords:** instance Semigroup, instance Monoid, <>, mempty, mappend, mconcat, Sum, Product, Max, Min, Any, All, First, Last, Endo, Dual

## Recognition triggers

- "Combine `T` values" or "an identity element for `T`"
- "Make `T` a Monoid (so we can use it with `Writer`/`foldMap`)"
- Question requires `Foldable.foldMap` or `Writer`'s log monoid
- "Define `(<>)` for `T`"

## Class

```haskell
class Semigroup a where
  (<>) :: a -> a -> a

class Semigroup a => Monoid a where
  mempty  :: a
  mappend :: a -> a -> a
  mappend = (<>)
  mconcat :: [a] -> a
  mconcat = foldr (<>) mempty
```

(In modern Haskell `Semigroup` is required before `Monoid`.)

## Standard instances

### Lists

```haskell
instance Semigroup [a] where
  (<>) = (++)

instance Monoid [a] where
  mempty = []
```

### Strings (same as lists of Char)

```haskell
"foo" <> "bar" = "foobar"
mempty :: String = ""
```

### Numeric — must wrap in Sum / Product

`Int` itself is NOT a Monoid (two natural choices: `+` or `*`). Use newtypes:

```haskell
newtype Sum a     = Sum     { getSum     :: a }
newtype Product a = Product { getProduct :: a }

instance Num a => Semigroup (Sum a) where
  Sum x <> Sum y = Sum (x + y)
instance Num a => Monoid (Sum a) where
  mempty = Sum 0

instance Num a => Semigroup (Product a) where
  Product x <> Product y = Product (x * y)
instance Num a => Monoid (Product a) where
  mempty = Product 1
```

Use:
```haskell
getSum     (foldMap Sum     [1..10]) == 55
getProduct (foldMap Product [1..5])  == 120
```

### Booleans — Any / All

```haskell
newtype Any = Any { getAny :: Bool }
newtype All = All { getAll :: Bool }

instance Semigroup Any where
  Any x <> Any y = Any (x || y)
instance Monoid Any where
  mempty = Any False

instance Semigroup All where
  All x <> All y = All (x && y)
instance Monoid All where
  mempty = All True
```

### Ordering — Max / Min (need `Bounded a`)

```haskell
newtype Max a = Max { getMax :: a }
newtype Min a = Min { getMin :: a }

instance Ord a => Semigroup (Max a) where
  Max x <> Max y = Max (max x y)
instance (Ord a, Bounded a) => Monoid (Max a) where
  mempty = Max minBound

instance Ord a => Semigroup (Min a) where
  Min x <> Min y = Min (min x y)
instance (Ord a, Bounded a) => Monoid (Min a) where
  mempty = Min maxBound
```

### Maybe — `First` / `Last`

```haskell
newtype First a = First { getFirst :: Maybe a }
newtype Last  a = Last  { getLast  :: Maybe a }

instance Semigroup (First a) where
  First Nothing <> r = r
  l             <> _ = l           -- leftmost Just wins
instance Monoid (First a) where
  mempty = First Nothing

instance Semigroup (Last a) where
  l <> Last Nothing = l
  _ <> r            = r            -- rightmost Just wins
instance Monoid (Last a) where
  mempty = Last Nothing
```

### Maybe (the "lifted" monoid — combine Just-payloads)

```haskell
instance Semigroup a => Semigroup (Maybe a) where
  Nothing <> r = r
  l <> Nothing = l
  Just x <> Just y = Just (x <> y)
instance Semigroup a => Monoid (Maybe a) where
  mempty = Nothing
```

### Function — Endo (function composition)

```haskell
newtype Endo a = Endo { appEndo :: a -> a }

instance Semigroup (Endo a) where
  Endo f <> Endo g = Endo (f . g)
instance Monoid (Endo a) where
  mempty = Endo id
```

This is how `foldr` is recovered from `foldMap`:
```haskell
foldr f z t = appEndo (foldMap (Endo . f) t) z
```

### Dual — reverse a monoid

```haskell
newtype Dual a = Dual { getDual :: a }

instance Semigroup a => Semigroup (Dual a) where
  Dual x <> Dual y = Dual (y <> x)     -- flipped!
instance Monoid a => Monoid (Dual a) where
  mempty = Dual mempty
```

Useful for "fold from the right": `foldMap (Dual . f)`.

### Tuples (componentwise)

```haskell
instance (Semigroup a, Semigroup b) => Semigroup (a, b) where
  (x1, y1) <> (x2, y2) = (x1 <> x2, y1 <> y2)
instance (Monoid a, Monoid b) => Monoid (a, b) where
  mempty = (mempty, mempty)
```

### Unit

```haskell
instance Semigroup () where
  () <> () = ()
instance Monoid () where
  mempty = ()
```

## Custom Monoid templates

### Set-like (deduplicating union)

```haskell
data MySet a = MySet [a]

instance Eq a => Semigroup (MySet a) where
  MySet xs <> MySet ys = MySet (nub (xs ++ ys))
instance Eq a => Monoid (MySet a) where
  mempty = MySet []
```

### Sum-with-bound (saturating add)

```haskell
newtype Bounded10 = B10 Int

instance Semigroup Bounded10 where
  B10 x <> B10 y = B10 (min 10 (x + y))
instance Monoid Bounded10 where
  mempty = B10 0
```

## How `Monoid` interacts with other classes

| Class | Uses Monoid for |
|---|---|
| `Foldable` | `foldMap` target |
| `Writer w` | `tell` accumulates via `<>` |
| `Alternative` | (different algebra, but parallels) |
| `Applicative (Const m)` | combines `m`s with `<>` |

## Pitfalls

- **`Int` is NOT a Monoid.** Use `Sum Int` or `Product Int`. The exam may ask "why isn't Int a monoid?" — answer: two natural choices (`+`, `*`); Haskell forces you to disambiguate via newtype.
- **`Maybe a` has TWO monoid candidates.** The "lifted" one (combine `Just`s via inner `<>`) requires `Semigroup a`. `First` and `Last` give "leftmost/rightmost wins" without that constraint.
- **`Endo` composition direction.** `Endo f <> Endo g = Endo (f . g)`, NOT `g . f`. (Conventional.)
- **`mempty` ambiguity.** `mempty :: ?` needs type annotation: `mempty :: [Int]`, `mempty :: Sum Int`.
- **Don't define `mempty = []`** for non-list types — `mempty` is generic.
- **Associativity** must hold for `<>`. Easy to mess up with set-like dedup; check.
- **Newtype overhead is zero** at runtime — `Sum 3 :: Sum Int` has the same representation as `3 :: Int`.

## Monoid laws as QuickCheck props

```haskell
prop_monoid_left_id  :: (Monoid a, Eq a) => a -> Bool
prop_monoid_left_id  x = mempty <> x == x

prop_monoid_right_id :: (Monoid a, Eq a) => a -> Bool
prop_monoid_right_id x = x <> mempty == x

prop_monoid_assoc    :: (Monoid a, Eq a) => a -> a -> a -> Bool
prop_monoid_assoc    x y z = (x <> y) <> z == x <> (y <> z)

prop_mconcat_consistent :: (Monoid a, Eq a) => [a] -> Bool
prop_mconcat_consistent xs = mconcat xs == foldr (<>) mempty xs
```

## QuickCheck attacks

- Identity (left/right) and associativity.
- For `Sum/Product`: matches `+`/`*` on the wrapped numeric.
- For `Endo`: `appEndo (Endo f <> Endo g) x == f (g x)`.
- For `First`: leftmost Just survives.
- For `Dual a`: applying to `mconcat` reverses the input list.

## Cheat sheet — which monoid for which purpose?

| Need | Type | mempty | <> |
|---|---|---|---|
| Sum numbers | `Sum a` | `Sum 0` | `Sum (x+y)` |
| Multiply | `Product a` | `Product 1` | `Product (x*y)` |
| List log | `[a]` | `[]` | `(++)` |
| String log | `String` | `""` | `(++)` |
| Max with bound | `Max a` | `Max minBound` | `Max (max x y)` |
| Min with bound | `Min a` | `Min maxBound` | `Min (min x y)` |
| OR booleans | `Any` | `Any False` | `Any (\|\|)` |
| AND booleans | `All` | `All True` | `All (&&)` |
| First Just | `First a` | `First Nothing` | leftmost |
| Last Just | `Last a` | `Last Nothing` | rightmost |
| Function compose | `Endo a` | `Endo id` | `(.)` |
| Reverse a monoid | `Dual a` | `Dual mempty` | flipped |

## See also

**Archetypes:** [A15 writer trace](../archetypes/A15-writer-trace.md)
**Question families:** [writer-trace](../question-families/writer-trace-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
