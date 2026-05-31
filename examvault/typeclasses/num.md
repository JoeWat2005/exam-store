<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [typeclasses](./README.md) · **Num**

<!-- siblings:start -->
> **Peers:** [alternative](./alternative.md) · [applicative](./applicative.md) · [eq-ord](./eq-ord.md) · [foldable](./foldable.md) · [functor](./functor.md) · [monad](./monad.md) · [monoid](./monoid.md) · **num** · [show](./show.md) · [traversable](./traversable.md)
<!-- siblings:end -->






# Num

> **Mental model:** `Num` is the typeclass that makes *integer literals work for your type*. When Haskell sees `5 :: T`, it calls `fromInteger 5 :: T`. The other methods (`+`, `*`, `-`, `negate`, `abs`, `signum`) define arithmetic. Writing a custom `Num` instance is rare in exams but not impossible — Bool-as-ring, Peano nats, and "values + units" are the textbook examples.

**Methods (MINIMAL):** `(+), (*), abs, signum, fromInteger, (negate | (-))`.

**Search keywords:** instance Num, fromInteger, Num Bool, Peano, ring, abs, signum

## Recognition triggers

- "Make `T` accept integer literals" (`5 :: T` should work)
- "Define `+` for `T`"
- "Verify the ring laws for `T`"
- Lecture's Bool-as-Boolean-ring example.

## Class

```haskell
class Num a where
  (+), (-), (*) :: a -> a -> a
  negate, abs, signum :: a -> a
  fromInteger :: Integer -> a

  -- defaults:
  x - y    = x + negate y
  negate x = 0 - x
```

`fromInteger` is how `5 :: T` becomes a `T`-value: GHC reads `5` as `Integer` then calls `fromInteger`.

## Required laws (ring-like)

- Commutative monoid for `(+, 0)`: `(x + y) + z = x + (y + z)`, `x + 0 = x`, `x + y = y + x`, `x + negate x = 0`.
- Semigroup for `(*, 1)`: `(x * y) * z = x * (y * z)`, `x * 1 = x`.
- Distributivity: `x * (y + z) = x * y + x * z`.
- Sign discipline: `abs x * signum x = x`.

Haskell does NOT enforce these — but `deriving (Num)` doesn't exist, and conforming instances are expected to satisfy them.

## Canonical templates

### Bool as Boolean ring (course example)

```haskell
instance Num Bool where
  False + y = y
  True  + y = not y          -- + = XOR

  (*) = (&&)                 -- * = AND

  negate = id                -- self-inverse in a Boolean ring
  abs    = id
  signum = id

  fromInteger 0 = False
  fromInteger _ = True
```

Verifies all ring laws:
```haskell
testRing = and
  [ x + 0 == x
  , x + (-x) == 0
  , x * 1 == x
  , (x + y) + z == x + (y + z)
  , x + y == y + x
  , x * y == y * x
  , (x * y) * z == x * (y * z)
  , a * (x + y) == a * x + a * y
  , (x + y) * a == x * a + y * a
  | a <- bools, x <- bools, y <- bools, z <- bools]
  where bools = [False, True]
```

### Peano-style Nat (`[()]`)

```haskell
-- A natural is encoded as a list of units; length is the value.
instance Num [()] where
  m + n         = m ++ n
  m * n         = concat (replicate (length m) n)
  abs    = id
  signum []     = []
  signum _      = [()]
  fromInteger n = replicate (fromInteger n) ()
  negate = id    -- Nats don't have negation; this is a "fake" instance
```

(Strictly speaking this isn't a ring — `negate` is bogus — but the course presents it as an exercise.)

### Vector (componentwise)

```haskell
data Vec3 = Vec3 Double Double Double

instance Num Vec3 where
  Vec3 x1 y1 z1 + Vec3 x2 y2 z2 = Vec3 (x1+x2) (y1+y2) (z1+z2)
  Vec3 x1 y1 z1 * Vec3 x2 y2 z2 = Vec3 (x1*x2) (y1*y2) (z1*z2)   -- componentwise!
  negate (Vec3 x y z) = Vec3 (-x) (-y) (-z)
  abs    (Vec3 x y z) = Vec3 (abs x) (abs y) (abs z)
  signum (Vec3 x y z) = Vec3 (signum x) (signum y) (signum z)
  fromInteger n       = let d = fromInteger n in Vec3 d d d
```

### Modular ring (Z/nZ)

```haskell
data Mod7 = Mod7 Int

instance Num Mod7 where
  Mod7 a + Mod7 b = Mod7 ((a + b) `mod` 7)
  Mod7 a * Mod7 b = Mod7 ((a * b) `mod` 7)
  negate (Mod7 a) = Mod7 ((-a) `mod` 7)
  abs    = id
  signum (Mod7 0) = Mod7 0
  signum _        = Mod7 1
  fromInteger n   = Mod7 (fromInteger n `mod` 7)
```

### Complex

```haskell
data C = C Double Double      -- C re im

instance Num C where
  C a b + C c d = C (a + c) (b + d)
  C a b * C c d = C (a*c - b*d) (a*d + b*c)
  negate (C a b) = C (-a) (-b)
  abs (C a b)    = C (sqrt (a*a + b*b)) 0
  signum z@(C a b)
    | a == 0 && b == 0 = C 0 0
    | otherwise        = let C m _ = abs z in C (a/m) (b/m)
  fromInteger n = C (fromInteger n) 0
```

## What `fromInteger` makes possible

```haskell
ghci> True + 0
True                     -- Num Bool instance kicks in; 0 = fromInteger 0 = False
```

Once your type is a `Num`, you can use any integer literal *of your type* as a value of it. This is how `5 :: Double` works.

## Pitfalls

- **MINIMAL is non-trivial.** You need at least `(+), (*), abs, signum, fromInteger, (negate | (-))`. Forgetting one fails compilation.
- **`fromInteger 0`** must give the additive identity. For Bool: `False`. For Vec3: `Vec3 0 0 0`.
- **`abs * signum = id`** is the contract. For most types: `abs` non-negative, `signum ∈ {-1, 0, 1}` (or `True`/`False` analogue).
- **No `Eq` requirement.** `Num` doesn't extend `Eq` — you can have a Num that isn't comparable. Useful for things like Symbolic.
- **Negation in non-rings.** For Nats (which lack negatives) you can't honestly define `negate`. The course's `[()]` instance has `negate = id`, which is mathematically wrong but compiles.
- **`Fractional`/`Integral` extend `Num`.** If your type isn't a field, don't make it Fractional (no `(/)`).
- **Don't conflate `*` with composition.** `(*)` for `Num` is the type's multiplication. For matrices that *is* composition; for vectors it's componentwise (or dot product — your choice).

## Custom Num laws as QuickCheck props

```haskell
prop_add_assoc  :: (Num a, Eq a) => a -> a -> a -> Bool
prop_add_assoc  x y z = (x + y) + z == x + (y + z)

prop_add_comm   :: (Num a, Eq a) => a -> a -> Bool
prop_add_comm   x y = x + y == y + x

prop_add_id     :: (Num a, Eq a) => a -> Bool
prop_add_id     x = x + 0 == x

prop_mul_assoc  :: (Num a, Eq a) => a -> a -> a -> Bool
prop_mul_assoc  x y z = (x * y) * z == x * (y * z)

prop_distrib    :: (Num a, Eq a) => a -> a -> a -> Bool
prop_distrib    x y z = x * (y + z) == x * y + x * z

prop_signum_abs :: (Num a, Eq a) => a -> Bool
prop_signum_abs x = abs x * signum x == x
```

## QuickCheck attacks

- All ring laws above.
- `fromInteger 0 + x == x` (additive identity).
- `fromInteger 1 * x == x` (multiplicative identity).
- For Bool: matches XOR/AND truth tables.
- For mod-n: results stay in [0, n-1].

## When NOT to write `instance Num`

- If your type has only addition (no multiplication) — use Monoid / Group.
- If you don't need integer literals — use plain functions `add`, `mul`, etc.
- If conformance to ring laws is questionable — write your own class, e.g. `class SemiRing a`.

## See also

**QuickCheck:** [numeric attacks](../quickcheck/numeric-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
