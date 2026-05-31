<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A06 — Functor / Applicative / Monad Instance**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · **A06** · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A06 — Functor / Applicative / Monad Instance

**Tier:** 1   |   **Stars:** ⭐⭐⭐⭐
**Mock appearance:** none direct   |   **Assignment appearance:** A3 (Free given but `Functor f =>` constraint used everywhere)
**Combines with:** A01 · A03 · A22 · A24
**Search keywords:** Functor · fmap · Applicative · pure · `<*>` · Monad · `>>=` · instance · custom type · MyMaybe · Identity · Reader

## What it tests
Whether you can write `instance Functor T where fmap = …` (and Applicative/Monad) for a custom ADT — preserving the constructor structure while transforming the stored values, and respecting the laws.

## Recognition triggers
- Code block starts with `instance Functor T where` or `instance Monad (T x) where`
- A custom data type `data T a = …` is given
- The question reads "Make `T` an instance of `Functor` / `Applicative` / `Monad`"
- The signature shows `fmap :: (a -> b) -> T a -> T b` or `(>>=) :: T a -> (a -> T b) -> T b`
- The data type has type parameter `a` and recursive structure storing `a`s
- Problem labelled "Functor for X" / "Monad for X"

## Canonical template
```haskell
-- For any data T a = Ctor a (T a) (T a) | Base
instance Functor T where
  fmap _ Base          = Base
  fmap f (Ctor x l r)  = Ctor (f x) (fmap f l) (fmap f r)

instance Applicative T where
  pure x                  = Ctor x Base Base
  Base       <*> _        = Base
  Ctor f _ _ <*> tx       = fmap f tx     -- often: zip/distribute structures
```

## Mutations (the examiner picks one)

### M1 — `Functor MyMaybe` (problem 70, 121)
```haskell
data MyMaybe a = MyNothing | MyJust a

instance Functor MyMaybe where
  fmap _ MyNothing  = MyNothing
  fmap f (MyJust x) = MyJust (f x)
```
What changes: no recursion; one clause per constructor.

### M2 — `Monad MyMaybe`
```haskell
instance Applicative MyMaybe where
  pure                       = MyJust
  MyNothing  <*> _           = MyNothing
  _          <*> MyNothing   = MyNothing
  MyJust f   <*> MyJust x    = MyJust (f x)

instance Monad MyMaybe where
  MyNothing  >>= _ = MyNothing
  MyJust x   >>= f = f x
```
What changes: builds on M1's Functor; `>>=` runs the next action only when there's a value.

### M3 — `Functor BT` (problem 125)
```haskell
data BT a = Empty | Fork a (BT a) (BT a)

instance Functor BT where
  fmap _ Empty        = Empty
  fmap f (Fork x l r) = Fork (f x) (fmap f l) (fmap f r)
```
What changes: tree-shaped; recurse on subtrees with `fmap f`, not the function being defined.

### M4 — `Functor Rose` (problem 126)
```haskell
data Rose a = Leaf a | Branch [Rose a]

instance Functor Rose where
  fmap f (Leaf x)     = Leaf (f x)
  fmap f (Branch xs)  = Branch (map (fmap f) xs)
```
What changes: list of subtrees needs `map (fmap f)` — double `fmap`-ish style; common confusion with `fmap f xs`.

### M5 — `Functor / Applicative / Monad Identity` (problem 123)
```haskell
newtype Identity a = Identity a

instance Functor Identity     where fmap f (Identity x) = Identity (f x)
instance Applicative Identity where pure = Identity
                                    Identity f <*> Identity x = Identity (f x)
instance Monad Identity       where Identity x >>= f = f x
```
What changes: trivial wrapper; all three instances are one-liners.

### M6 — `Functor (Reader r)` (problem 124)
```haskell
newtype Reader r a = Reader { runReader :: r -> a }

instance Functor (Reader r) where
  fmap f (Reader g) = Reader (f . g)

instance Applicative (Reader r) where
  pure x                = Reader (\_ -> x)
  Reader rf <*> Reader rx = Reader (\r -> rf r (rx r))

instance Monad (Reader r) where
  Reader rx >>= f = Reader (\r -> runReader (f (rx r)) r)
```
What changes: type parameter `r` is FIXED; you write `instance Functor (Reader r)` not `instance Functor Reader`.

### M7 — `Functor MyList` (problem 122)
```haskell
data MyList a = Nil | Cons a (MyList a)

instance Functor MyList where
  fmap _ Nil         = Nil
  fmap f (Cons x xs) = Cons (f x) (fmap f xs)

instance Applicative MyList where
  pure x = Cons x Nil
  Nil       <*> _   = Nil
  Cons f fs <*> xs  = appendL (fmap f xs) (fs <*> xs)
    where appendL Nil ys         = ys
          appendL (Cons z zs) ys = Cons z (appendL zs ys)

instance Monad MyList where
  Nil       >>= _ = Nil
  Cons x xs >>= f = appendL (f x) (xs >>= f)
```
What changes: list-shaped; Monad requires `concatMap` semantics (use `appendL` helper).

### M8 — `Functor (Either e)` (e is fixed)
```haskell
instance Functor (Either e) where
  fmap _ (Left  e) = Left e
  fmap f (Right a) = Right (f a)
```
What changes: only the `Right` half is mapped; `Left` (the error) passes through.

### M9 — `Functor for sum of functors` (`FSum`)
```haskell
data FSum f g a = FLeft (f a) | FRight (g a)

instance (Functor f, Functor g) => Functor (FSum f g) where
  fmap h (FLeft fa)  = FLeft  (fmap h fa)
  fmap h (FRight ga) = FRight (fmap h ga)
```
What changes: nested `fmap`s within constraints `(Functor f, Functor g)`. Used in A3 for the scheduler.

### M10 — `Functor (Free f)` (A3 spec)
```haskell
data Free f a = Pure a | Free (f (Free f a))

instance Functor f => Functor (Free f) where
  fmap g (Pure a)  = Pure (g a)
  fmap g (Free ff) = Free (fmap (fmap g) ff)
```
What changes: doubly-recursive; outer `fmap` is on `f`, inner is the instance being defined.

## Worked examples from this course
- Problem sheet Set 7 (#70): `Functor MyMaybe` — M1.
- Problem sheet Set 13 (#121-126): full Functor / Applicative / Monad chain for `MyMaybe`, `MyList`, `Identity`, `Reader`, `BT`, `Rose`.
- Assignment 3: `Free f`'s `Functor`/`Monad` instances are GIVEN. `FSum f g`'s `Functor` is also given. Students don't write them but must understand them to use `liftF`, `>>=`.
- Practice file `ewan31-40.hs`: `Functor Bin`, `Functor (FSum f g)`.

## QuickCheck attack surface
- **Functor identity law**: `fmap id == id` — auto-marker runs for random tree, checks structural equality.
- **Functor composition law**: `fmap (g . f) == fmap g . fmap f`.
- **`pure` then `fmap`**: `fmap f (pure x) == pure (f x)`.
- **Empty / base constructor**: `fmap f Empty == Empty`; `fmap f MyNothing == MyNothing`.
- **Shape preservation**: `size (fmap f t) == size t` — `fmap` must not change the constructor skeleton.
- **Monad law: left identity**: `return x >>= f == f x`.
- **Monad law: right identity**: `m >>= return == m`.
- **Monad law: associativity**: `(m >>= f) >>= g == m >>= (\x -> f x >>= g)`.

## Pitfalls (marks-killers)
- **Mutating the constructor**: `fmap f (Fork x l r) = Empty` — wrong. fmap may change values, NEVER the constructor.
- **Forgetting to recurse**: `fmap f (Fork x l r) = Fork (f x) l r` — left & right are unchanged. Subtree values stay `a`s, but the type is `T b`. Type error.
- **`fmap f xs` instead of `map (fmap f) xs`**: list of trees needs the inner `fmap` first (over each subtree), then the outer `map` over the list. Common bug for `Functor Rose`.
- **Missing constraint on Free**: `instance Functor (Free f) where` — doesn't compile because Free's structure needs `fmap` on `f`. Must be `instance Functor f => Functor (Free f) where`.
- **`pure = id` for non-singleton wrappers**: `pure x = Empty` is wrong. `pure x` must produce a "trivial container" — `MyJust x`, `Leaf x`, `Identity x`.
- **Applicative without Functor**: every Applicative must be a Functor (with `fmap = (<*>) . pure`). You can't declare Applicative without first declaring Functor.

## Combines-with deep dive

### A06 × A01 — Functor for a custom tree
See M3 / M4. The instance IS structural recursion with `fmap f` as the recursive call.

### A06 × A03 — `Monad m => sequenceM` instantiated on your type
After making `MyMaybe` a Monad, `sequenceM :: Monad m => [m a] -> m [a]` works at `[MyMaybe a] -> MyMaybe [a]`. Auto-marker likely tests both `Maybe` and your `MyMaybe`.

### A06 × A22 — typeclass instances for ADTs
A22 is the Eq/Ord/Show variant; A06 is the `(* -> *)` variant. Same per-constructor structure.

### A06 × A24 — Applicative as the bridge
Before writing `Monad`, write `Applicative`. The `pure` definition usually appears in both.

## See also

**Combines with:** [A01 tree recursion](./A01-tree-recursion.md) · [A05 ADT translation](./A05-adt-translation.md) · [A22 typeclass instance](./A22-typeclass-instance.md) · [A24 applicative instance](./A24-applicative-instance.md)
**Question families:** [functor-instance](../question-families/functor-instance-family.md) · [applicative-monad-instance](../question-families/applicative-monad-instance-family.md)
**Theory:** [Functor typeclass](../typeclasses/functor.md) · [tree functor](../trees/tree-functor.md)
**Pitfalls:** [P-010 deriving Functor needs unsafe](../pitfalls/HIGH-severity.md#p-010) · [P-016 doesn't preserve shape](../pitfalls/HIGH-severity.md#p-016)
**QuickCheck:** [typeclass instance attacks](../quickcheck/typeclass-instance-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
