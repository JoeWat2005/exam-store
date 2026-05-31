<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [typeclasses](./README.md) · **Traversable**

<!-- siblings:start -->
> **Peers:** [alternative](./alternative.md) · [applicative](./applicative.md) · [eq-ord](./eq-ord.md) · [foldable](./foldable.md) · [functor](./functor.md) · [monad](./monad.md) · [monoid](./monoid.md) · [num](./num.md) · [show](./show.md) · **traversable**
<!-- siblings:end -->






# Traversable

> **Mental model:** `traverse` is `fmap` with an effect. Where `fmap f` applies `(a -> b)` pointwise and gives `t b`, `traverse f` applies `(a -> m b)` pointwise and gives `m (t b)` — the *effects collected*, the *structure preserved*. It's the cleanest way to walk a tree (or any structure) running a monadic action at every node and assembling the results back into the same shape.

**Methods (minimal):** `traverse :: Applicative f => (a -> f b) -> t a -> f (t b)` OR `sequenceA :: Applicative f => t (f a) -> f (t a)`.

**Laws:**
- Naturality:  `t . traverse f = traverse (t . f)` for applicative transformation `t`
- Identity:    `traverse Identity = Identity`
- Composition: `traverse (Compose . fmap g . f) = Compose . fmap (traverse g) . traverse f`

**Search keywords:** Traversable, traverse, sequenceA, sequence, mapM, mapM_, Traversable BT, Traversable Rose, for, forM

## Recognition triggers

- "Traverse `T` with an effectful function"
- "Make `T` Traversable"
- "Implement `mapM` for `T`" (`mapM = traverse` for monads)
- "Run an `IO`/`Maybe`/`State` action at each leaf and collect results"
- The signature has shape `(a -> m b) -> T a -> m (T b)` — that IS `traverse`.

## Class

```haskell
class (Functor t, Foldable t) => Traversable t where
  traverse  :: Applicative f => (a -> f b) -> t a -> f (t b)
  sequenceA :: Applicative f => t (f a) -> f (t a)

  -- Defaults:
  traverse f  = sequenceA . fmap f
  sequenceA   = traverse id

  -- Free synonyms:
  mapM      :: Monad m => (a -> m b) -> t a -> m (t b)   -- = traverse
  sequence  :: Monad m => t (m a)    -> m (t a)          -- = sequenceA
```

## Why Functor + Foldable are required as superclasses

- `Functor`: traverse subsumes fmap (`traverse (Identity . f) ≡ Identity . fmap f`)
- `Foldable`: traverse subsumes foldMap (`traverse (Const . f) ≡ Const . foldMap f`)

So if you have a Traversable, you have both for free.

## Canonical templates per ADT

### Binary tree (BT)

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

instance Traversable BT where
  traverse _ Empty        = pure Empty
  traverse f (Fork x l r) =
    Fork <$> f x <*> traverse f l <*> traverse f r
```

The trick: `Fork <$> f x <*> traverse f l <*> traverse f r` lifts the 3-argument `Fork` constructor over the applicative `f`, sequencing the three effects.

### Rose tree

```haskell
data Rose a = Leaf a | Branch [Rose a]

instance Traversable Rose where
  traverse f (Leaf x)    = Leaf <$> f x
  traverse f (Branch xs) = Branch <$> traverse (traverse f) xs
  -- outer traverse on [Rose a] (uses [] Traversable)
  -- inner traverse on each Rose a
```

Same double-traverse pattern as Functor's `map (fmap f)` and Foldable's `foldMap (foldMap f)`.

### Pair (homogeneous)

```haskell
data Pair a = Pair a a

instance Traversable Pair where
  traverse f (Pair x y) = Pair <$> f x <*> f y
```

### Maybe-like

```haskell
data MyMaybe a = MyNothing | MyJust a

instance Traversable MyMaybe where
  traverse _ MyNothing  = pure MyNothing
  traverse f (MyJust x) = MyJust <$> f x
```

### Either

```haskell
instance Traversable (Either e) where
  traverse _ (Left  e) = pure (Left e)
  traverse f (Right x) = Right <$> f x
```

### Expr

```haskell
data Expr a = Var a | Lit Int | Add (Expr a) (Expr a) | Mul (Expr a) (Expr a)

instance Traversable Expr where
  traverse _ (Lit n)     = pure (Lit n)
  traverse f (Var v)     = Var <$> f v
  traverse f (Add e1 e2) = Add <$> traverse f e1 <*> traverse f e2
  traverse f (Mul e1 e2) = Mul <$> traverse f e1 <*> traverse f e2
```

## Recipe for any custom Traversable

For each constructor `C s1 s2 ... sn`:
- Identify which slots contain `a` (or recursive `T a`).
- Lift the constructor: `C <$> slot1 <*> slot2 <*> ... <*> slotN`
- For each `a`-slot: replace with `f slot`.
- For each recursive slot of type `T a`: replace with `traverse f slot`.
- For each non-`a` slot: wrap in `pure`.
- For each `[T a]` slot: use `traverse (traverse f) xs`.

### Worked: a tree with labelled forks

```haskell
data Lbl a = Empty
           | Branch String (Lbl a) a (Lbl a)
           -- ctor: String + Lbl + a + Lbl

instance Traversable Lbl where
  traverse _ Empty = pure Empty
  traverse f (Branch s l x r) =
    Branch s                  -- String → pure-applied
      <$> traverse f l        -- Lbl recurses
      <*> f x                 -- the a is f'd
      <*> traverse f r        -- Lbl recurses
```

`Branch s` is partially applied at the `<$>` step — `s` is just baked in as a pure value.

## Relationship to `mapM` and `sequence`

```haskell
mapM     :: (Monad m, Traversable t) => (a -> m b) -> t a -> m (t b)
mapM      = traverse

sequence :: (Monad m, Traversable t) => t (m a) -> m (t a)
sequence  = sequenceA
```

So `mapM` for trees IS `traverse` for trees. Many course problems are phrased as `mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)` — that's `traverse` constrained to Monad. The Applicative version is strictly more general.

### Worked example — labelling a tree with State

```haskell
labelM :: BT a -> State Int (BT (Int, a))
labelM = traverse $ \x -> do
  n <- get
  put (n + 1)
  pure (n, x)

-- Use:
labelTree t = evalState (labelM t) 0
```

Same structure works for Maybe, Writer, Either, IO. See [tree-x-state.md](../cross-matrix/tree-x-state.md).

## Effects ordering — in-order vs pre-order

The order of `<*>` chains determines effect order:

```haskell
-- In-order (left, x, right):
Fork <$> traverse f l <*> f x <*> traverse f r

-- Pre-order (x, left, right):
(\x l r -> Fork x l r) <$> f x <*> traverse f l <*> traverse f r

-- Post-order (left, right, x):
(\l r x -> Fork x l r) <$> traverse f l <*> traverse f r <*> f x
```

For Functor laws all these give the same tree structure; for State/Writer they accumulate state in different orders.

## Pitfalls

- **Wrong constructor lift.** Must use `<$>` for the first arg, `<*>` for subsequent. `Fork <*> f x <*> ...` is a type error.
- **Rose double-traverse.** `Branch <$> traverse (traverse f) xs` — easy to miss the outer `traverse`.
- **`pure` for `Empty` / non-`a` constructors.** `traverse _ Empty = Empty` is wrong — must be `pure Empty`.
- **Constraints.** `instance Traversable T` requires `Functor T` AND `Foldable T`.
- **Effect ordering matters for State, Writer, IO.** Changing `<*>` order changes when side-effects run.
- **`mapM` vs `traverse`.** `mapM` is just `traverse` with a Monad constraint. Prefer `traverse`.
- **Don't write `sequence . map f` instead of `traverse f`.** Equivalent but less idiomatic.

## Traversable laws as QuickCheck props

```haskell
-- Identity
prop_trav_id :: (Traversable t, Eq (t a)) => t a -> Bool
prop_trav_id t = runIdentity (traverse Identity t) == t

-- Naturality (via Compose)
prop_trav_naturality :: ... = traverse (Compose . fmap g . f)
                          === Compose . fmap (traverse g) . traverse f
```

In practice the marker checks that:
- `traverse f` for `Identity` recovers `fmap f`.
- `traverse f` for `Const m` recovers `foldMap f`.
- Shape preservation: `length (traverse f t) == 1` (one t-shape inside the applicative).

## QuickCheck attacks

- `traverse Identity t == Identity t` (identity law).
- `traverse f` followed by `traverse g` factors via `Compose`.
- For State-effect traverse: `evalState (traverse f t) s0` shape == `fmap (eval . f) t` shape.
- `mapM return t == return t` (when used over Monad).

## See also

> **This page is the Traversable template home.** If a question says "make `T` Traversable" / "implement `traverse`/`mapM` for `T`", build it from the templates above. [A06 functor instance](../archetypes/A06-functor-instance.md) covers **only** Functor / Applicative / Monad instances — it has **no** `traverse` template — so route Traversable questions here, not to A06.

**Archetypes:** [A06 functor instance](../archetypes/A06-functor-instance.md) — sibling instance archetype (Functor/Applicative/Monad only; **not** Traversable).
**Related (typeclasses):** [foldable](./foldable.md) · [functor](./functor.md) · [applicative](./applicative.md) (traverse needs an Applicative effect)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
