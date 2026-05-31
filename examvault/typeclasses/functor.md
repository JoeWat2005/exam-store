<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [typeclasses](./README.md) · **Functor**

<!-- siblings:start -->
> **Peers:** [alternative](./alternative.md) · [applicative](./applicative.md) · [eq-ord](./eq-ord.md) · [foldable](./foldable.md) · **functor** · [monad](./monad.md) · [monoid](./monoid.md) · [num](./num.md) · [show](./show.md) · [traversable](./traversable.md)
<!-- siblings:end -->






# Functor

> **Mental model:** *Functor preserves structure.* `fmap` takes a pure `(a -> b)` and slips it inside the container, transforming every `a` to a `b` while leaving the shape (positions, ordering, nesting, constructor counts) untouched.

**Methods:** `fmap :: (a -> b) -> f a -> f b`. Also: `(<$>) = fmap` (infix synonym).

**Laws:**
- Identity:    `fmap id = id`
- Composition: `fmap (g . f) = fmap g . fmap f`

**Search keywords:** instance Functor, fmap, <$>, Functor BT, Functor Rose, Functor Pair, Functor Either, Functor Reader, Compose, Identity, Const

## Recognition triggers

The question hands you `data T ... = ...` and asks one of:
- "Make `T` a `Functor`"
- "Define `fmap` for `T`"
- "Implement `instance Functor T where ...`"
- "Why can't `T` be a Functor?" (rare — usually answer: contravariant occurrence of `a`)

The hint that it's a Functor (rather than Foldable / Traversable):
- The result type has the same shape as the input — only values inside change.

## Class

```haskell
class Functor f where
  fmap :: (a -> b) -> f a -> f b

(<$>) :: Functor f => (a -> b) -> f a -> f b
(<$>) = fmap
```

## Canonical templates per ADT

### Maybe-like

```haskell
data MyMaybe a = MyNothing | MyJust a

instance Functor MyMaybe where
  fmap _ MyNothing  = MyNothing
  fmap f (MyJust x) = MyJust (f x)
```

### List-like

```haskell
data MyList a = Nil | Cons a (MyList a)

instance Functor MyList where
  fmap _ Nil         = Nil
  fmap f (Cons x xs) = Cons (f x) (fmap f xs)
```

### Binary tree (BT — the course's #1 ADT)

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

instance Functor BT where
  fmap _ Empty        = Empty
  fmap f (Fork x l r) = Fork (f x) (fmap f l) (fmap f r)
```

### Rose tree (MockTest's tree variant)

```haskell
data Rose a = Leaf a | Branch [Rose a]

instance Functor Rose where
  fmap f (Leaf x)    = Leaf (f x)
  fmap f (Branch xs) = Branch (map (fmap f) xs)   -- map :: outer, fmap :: inner
```

The double-mapping `map (fmap f) xs` is the giveaway — you `map` over the *list* of children, but `fmap` over each child since each child is itself a `Rose`.

### Pair (homogeneous)

```haskell
data Pair a = Pair a a

instance Functor Pair where
  fmap f (Pair x y) = Pair (f x) (f y)
```

### Either (Functor in the RIGHT argument only)

```haskell
instance Functor (Either e) where
  fmap _ (Left  e) = Left  e
  fmap f (Right x) = Right (f x)
```

The `e` is fixed — only the right-hand `a` is mapped. The Left case is propagated unchanged. (Same shape: `Left` stays `Left`, `Right` stays `Right`.)

### Reader (function-as-Functor)

```haskell
instance Functor ((->) r) where
  fmap = (.)
-- fmap f g = f . g  -- post-compose with f
```

### Compose

```haskell
newtype Compose f g a = Compose { getCompose :: f (g a) }

instance (Functor f, Functor g) => Functor (Compose f g) where
  fmap h (Compose fga) = Compose (fmap (fmap h) fga)
```

Two `fmap`s: outer through `f`, inner through `g`.

### Identity

```haskell
newtype Identity a = Identity { runIdentity :: a }

instance Functor Identity where
  fmap f (Identity x) = Identity (f x)
```

### Const (a "phantom" Functor — `fmap` does NOTHING to the stored `m`)

```haskell
newtype Const m a = Const { getConst :: m }

instance Functor (Const m) where
  fmap _ (Const m) = Const m
```

The `a` parameter is phantom — there's no `a` inside, so `fmap` can't touch anything. This is the key building block for `length`, `foldMap`, etc.

### Expr (custom ADT — only when the `a` appears in payload, not in subexpr)

```haskell
data Expr a = Val a
            | Add (Expr a) (Expr a)
            | Mul (Expr a) (Expr a)

instance Functor Expr where
  fmap f (Val x)     = Val (f x)
  fmap f (Add e1 e2) = Add (fmap f e1) (fmap f e2)
  fmap f (Mul e1 e2) = Mul (fmap f e1) (fmap f e2)
```

## Rule for custom Functor

For each constructor:
1. List the `a`-typed slots → apply `f` to each.
2. List the `f a`-shaped recursive slots → call `fmap f` on each.
3. List `[f a]` list-of-recursive slots → `map (fmap f)` over each.
4. List slots that don't contain `a` (e.g. a fixed `String` label) → leave unchanged.
5. The constructor stays the same: `Empty` returns `Empty`, `Fork` returns `Fork`.

## Common variants

| Type | Notes |
|---|---|
| `Compose f g` | Two `fmap`s nested |
| `Identity` | Trivial — just unwrap, apply, rewrap |
| `Const m` | `fmap _ = id` (phantom `a`) |
| `Sum f g` | `Sum f g a = InL (f a) \| InR (g a)` — apply `fmap` to whichever side |
| `Product f g` | `Product f g a = Pair (f a) (g a)` — apply to both |

## Functor laws as QuickCheck props

```haskell
-- Identity
prop_fmap_id :: (Eq (f a), Functor f) => f a -> Bool
prop_fmap_id x = fmap id x == x

-- Composition
prop_fmap_compose :: (Eq (f c), Functor f) => Fun b c -> Fun a b -> f a -> Bool
prop_fmap_compose (Fun _ g) (Fun _ f) x =
  fmap (g . f) x == (fmap g . fmap f) x
```

These are exactly what the marker QuickChecks. If `Test.QuickCheck.Function`'s `Fun` is unfamiliar: it generates arbitrary functions for testing.

## Pitfalls

- **Shape change**: `fmap _ Empty = Fork x Empty Empty` is illegal — Functor MUST preserve constructor counts.
- **Wrong recursion**: `fmap f (Branch xs) = Branch (fmap f xs)` is wrong — `xs` is `[Rose a]`, not `Rose a`. Use `map (fmap f) xs`.
- **Either flipped**: `Functor (Either e)` maps the `Right`, NOT the `Left`. The `Left e` part is fixed.
- **Function direction**: `fmap @((->) r) = (.)` — `fmap f g = f . g`, not `g . f` (this is post-composition).
- **Const phantom**: don't try to "use" the `a` in `Const m` — there is no `a` inside.
- **Constraint propagation**: `instance Functor (Compose f g)` requires `(Functor f, Functor g) =>`.
- **Conflict with `Prelude.fmap`**: if you write a custom `Functor`-like class, hide `Prelude.fmap` or rename.

## QuickCheck attacks

The marker likely checks:
- `fmap id == id` (identity)
- `fmap (g . f) == fmap g . fmap f` (composition)
- For trees: `size (fmap f t) == size t` (shape preservation)
- For Either: `fmap f (Left e) == Left e` for all `e`

## See also

**Archetypes:** [A06 functor instance](../archetypes/A06-functor-instance.md) · [A22 typeclass instance](../archetypes/A22-typeclass-instance.md)
**Question families:** [functor-instance](../question-families/functor-instance-family.md)
**QuickCheck:** [typeclass-instance attacks](../quickcheck/typeclass-instance-attacks.md)
**Related (typeclasses):** [applicative](./applicative.md) · [monad](./monad.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
