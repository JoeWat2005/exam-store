<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [typeclasses](./README.md) · **Applicative**

<!-- siblings:start -->
> **Peers:** [alternative](./alternative.md) · **applicative** · [eq-ord](./eq-ord.md) · [foldable](./foldable.md) · [functor](./functor.md) · [monad](./monad.md) · [monoid](./monoid.md) · [num](./num.md) · [show](./show.md) · [traversable](./traversable.md)
<!-- siblings:end -->






# Applicative

> **Mental model:** Functor lifts a *1-argument* pure function into a context. Applicative lifts an *n-argument* pure function into a context: `f <$> mx <*> my <*> mz` applies pure `f :: a -> b -> c -> d` to wrapped values `mx :: m a`, `my :: m b`, `mz :: m c`, sequencing their effects left-to-right.

**Methods:** `pure :: a -> f a`, `(<*>) :: f (a -> b) -> f a -> f b`. Subclass of [Functor](functor.md).

**Laws:**
- Identity:    `pure id <*> v = v`
- Composition: `pure (.) <*> u <*> v <*> w = u <*> (v <*> w)`
- Homomorphism: `pure f <*> pure x = pure (f x)`
- Interchange: `u <*> pure y = pure ($ y) <*> u`

**Search keywords:** instance Applicative, pure, <\*>, liftA2, Applicative Maybe, Applicative List, Applicative Reader, Applicative Parser, ZipList, Compose

## Recognition triggers

- Question asks for `instance Applicative T where ...`
- Wording: "apply a wrapped function", "lift a 2-argument function", "combine two wrapped values"
- Used as stepping stone to declaring `Monad T` (you need Applicative as a base class).

## Class

```haskell
class Functor f => Applicative f where
  pure  :: a -> f a
  (<*>) :: f (a -> b) -> f a -> f b
```

## Canonical templates per ADT

### Maybe

```haskell
instance Applicative Maybe where
  pure              = Just
  Nothing  <*> _    = Nothing
  (Just f) <*> mx   = fmap f mx
```

### List (CARTESIAN — every f with every x)

```haskell
instance Applicative [] where
  pure x    = [x]
  fs <*> xs = [f x | f <- fs, x <- xs]
  -- equivalent: concat (map (\f -> map f xs) fs)
```

### ZipList (POSITIONAL — zip-pair function with value)

```haskell
newtype ZipList a = ZipList { getZipList :: [a] }

instance Applicative ZipList where
  pure x                        = ZipList (repeat x)   -- infinite!
  ZipList fs <*> ZipList xs     = ZipList (zipWith ($) fs xs)
```

This is why `[]` and `ZipList` are *different* applicatives over the same underlying functor.

### Reader

```haskell
instance Applicative ((->) r) where
  pure x    = \_ -> x
  rf <*> rx = \e -> rf e (rx e)   -- thread environment to both
```

### Either

```haskell
instance Applicative (Either e) where
  pure                = Right
  Left  e  <*> _      = Left e
  Right f  <*> mx     = fmap f mx
```

### Parser (course-style)

```haskell
newtype Parser a = P { parse :: String -> [(a, String)] }

instance Applicative Parser where
  pure x      = P (\s -> [(x, s)])
  P p <*> P q = P (\s -> [(f x, s'') | (f, s')  <- p s
                                     , (x, s'') <- q s'])
```

### Pair (homogeneous, applies the same fn to both slots)

```haskell
data Pair a = Pair a a

instance Applicative Pair where
  pure x                  = Pair x x
  Pair f g <*> Pair x y   = Pair (f x) (g y)
```

### Compose

```haskell
instance (Applicative f, Applicative g) => Applicative (Compose f g) where
  pure x                          = Compose (pure (pure x))
  Compose ff <*> Compose xx       = Compose (liftA2 (<*>) ff xx)
```

### Identity

```haskell
instance Applicative Identity where
  pure                            = Identity
  Identity f <*> Identity x       = Identity (f x)
```

### Const (only Applicative when `m` is a Monoid)

```haskell
instance Monoid m => Applicative (Const m) where
  pure _                          = Const mempty
  Const m1 <*> Const m2           = Const (m1 <> m2)
```

## n-ary lifting idioms

```haskell
liftA2 :: Applicative f => (a -> b -> c) -> f a -> f b -> f c
liftA2 f a b = f <$> a <*> b
-- or equivalently:
liftA2 f a b = pure f <*> a <*> b

liftA3 :: Applicative f => (a -> b -> c -> d) -> f a -> f b -> f c -> f d
liftA3 f a b c = f <$> a <*> b <*> c
```

The idiomatic n-ary lift: `f <$> a <*> b <*> c <*> ...`

## Sequencing without binding

```haskell
(*>) :: Applicative f => f a -> f b -> f b      -- discard left, keep right
(<*) :: Applicative f => f a -> f b -> f a      -- keep left, discard right

a *> b = (\_ b' -> b') <$> a <*> b
a <* b = (\a' _  -> a') <$> a <*> b
```

In parsers: `lexeme = token <* whitespace` (parse token, swallow trailing space).

## Rule for custom Applicative

- `pure x` = put `x` in the *minimal-effect* shape (Nothing-free, Empty-free, succeeding).
- `<*>` = sequence the effects of left and right argument, then apply the extracted function to the extracted value.

For a data type with effects, the effect order in `<*>` matters:
- State: left effect runs first, then right.
- Writer: monoid accumulates left then right.
- List: outer loop is functions, inner is values.

## Applicative laws as QuickCheck props

```haskell
prop_app_identity :: (Eq (f a), Applicative f) => f a -> Bool
prop_app_identity v = (pure id <*> v) == v

prop_app_homomorphism :: (Eq (f b), Applicative f, ...) => Fun a b -> a -> Bool
prop_app_homomorphism (Fun _ f) x =
  (pure f <*> pure x :: f b) == pure (f x)

prop_app_interchange :: (Eq (f b), Applicative f) => f (Fun a b) -> a -> Bool
prop_app_interchange u y =
  (fmap apply u <*> pure y) == (pure ($ y) <*> fmap apply u)
```

## Pitfalls

- **`<*>` not commutative.** `f <*> g` ≠ `g <*> f` (in general — for State, side-effects swap; for Maybe, `Nothing <*> anything = Nothing` short-circuits on the LEFT).
- **`ZipList` ≠ `[]`.** Same data, different instance. ZipList's `pure` is `repeat x` (infinite) and `<*>` is `zipWith ($)`.
- **Must declare Functor first.** `class Functor f => Applicative f` means you can't `instance Applicative T` without `instance Functor T`.
- **List `pure x = [x]`**, not `[]`. The empty list is `Alternative`'s `empty`, not the Applicative's `pure`.
- **Reader `pure = const`** = `\_ -> x` (ignore the environment).
- **Parser `<*>` threads `s` through left then right** — the `s'` from the left becomes the input to the right.

## QuickCheck attacks

- Identity, homomorphism, interchange, composition laws.
- For Maybe: `Nothing <*> Just x == Nothing` (left short-circuit).
- For List: `pure (+1) <*> [1,2,3] == [2,3,4]` (singleton lift).
- For State: order of effects.

## See also

**Archetypes:** [A24 applicative instance](../archetypes/A24-applicative-instance.md) · [A22 typeclass instance](../archetypes/A22-typeclass-instance.md)
**Question families:** [applicative-monad-instance](../question-families/applicative-monad-instance-family.md)
**QuickCheck:** [typeclass-instance attacks](../quickcheck/typeclass-instance-attacks.md)
**Related (typeclasses):** [functor](./functor.md) · [monad](./monad.md) · [alternative](./alternative.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
