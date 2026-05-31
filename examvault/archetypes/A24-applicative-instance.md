<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A24 — Applicative Instance (NEW)**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · **A24**
<!-- siblings:end -->






# A24 — Applicative Instance (NEW)

**Tier:** 3   |   **Stars:** ⭐⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** none direct (Free is given as Monad)
**Combines with:** A06 · A03 · A16
**Search keywords:** Applicative · pure · `<*>` · liftA2 · ZipList · ap · Applicative laws · `(<$>)`

## Justification for inclusion as its own archetype
A06 covers the full Functor/Applicative/Monad stack, but problem 127 (`liftA2'`), the ZipList vs List instance distinction, and the Validation-style "accumulate errors" pattern all sit specifically at the Applicative layer — neither a pure Functor nor a full Monad. The exam might ask for ONLY the Applicative instance (without Monad), or test the difference between `<*>` and `>>=`. Worth its own archetype because:
1. Applicative is sometimes the RIGHT answer (parsers, validation) where Monad would be wrong.
2. The Applicative laws differ from Functor and Monad laws.
3. Problem 127 (`liftA2'`) is Applicative-only.
4. Validation example (accumulating errors) requires Applicative, NOT Monad.

## What it tests
Whether you can write `instance Applicative T where pure = …; (<*>) = …` for a custom type, distinguish Applicative-style sequencing from Monad-style binding, and use `<$>` + `<*>` for clean code.

## Recognition triggers
- "Write the `Applicative` instance" (alone, not chained with Monad)
- `pure :: a -> T a` and `(<*>) :: T (a -> b) -> T a -> T b` in the signature
- "without using the library `liftA2`"
- Validation / form-validation flavour: accumulate ALL errors, not just the first
- ZipList-style "zip the structures together"

## Canonical template
```haskell
instance Applicative T where
  pure :: a -> T a
  pure x = ...

  (<*>) :: T (a -> b) -> T a -> T b
  Ctor f <*> Ctor x = Ctor (f x)
  -- (per-constructor case analysis)
```

## Mutations (the examiner picks one)

### M1 — `Applicative MyMaybe`
```haskell
instance Applicative MyMaybe where
  pure = MyJust
  MyNothing  <*> _          = MyNothing
  _          <*> MyNothing  = MyNothing
  MyJust f   <*> MyJust x   = MyJust (f x)
```
What changes: Maybe-like; fail-on-any.

### M2 — `Applicative (Either e)`
```haskell
instance Applicative (Either e) where
  pure                 = Right
  Left e   <*> _       = Left e
  _        <*> Left e  = Left e
  Right f  <*> Right x = Right (f x)
```
What changes: first error wins; same shape as MyMaybe.

### M3 — `Validation` (Applicative-only — accumulate errors)
```haskell
data Validation e a = Failure [e] | Success a

instance Functor (Validation e) where
  fmap _ (Failure es) = Failure es
  fmap f (Success a)  = Success (f a)

instance Applicative (Validation e) where
  pure                            = Success
  Failure es <*> Failure es'      = Failure (es ++ es')   -- BOTH errors!
  Failure es <*> Success _        = Failure es
  Success _  <*> Failure es       = Failure es
  Success f  <*> Success x        = Success (f x)
```
What changes: Applicative ACCUMULATES; can't be made a lawful Monad (would short-circuit on first error).

### M4 — `Applicative ZipList`
```haskell
newtype ZipList a = ZipList [a]

instance Functor ZipList where
  fmap f (ZipList xs) = ZipList (map f xs)

instance Applicative ZipList where
  pure x                  = ZipList (repeat x)
  ZipList fs <*> ZipList xs = ZipList (zipWith ($) fs xs)
```
What changes: structurally aligned `<*>`; `pure` is infinite list.

### M5 — `Applicative (Reader r)`
```haskell
newtype Reader r a = Reader { runReader :: r -> a }

instance Applicative (Reader r) where
  pure x                    = Reader (\_ -> x)
  Reader rf <*> Reader rx   = Reader (\r -> rf r (rx r))
```
What changes: function-shaped; the read environment threads through both sub-computations.

### M6 — `Applicative` for a custom list
```haskell
data MyList a = Nil | Cons a (MyList a)

instance Functor MyList where
  fmap _ Nil         = Nil
  fmap f (Cons x xs) = Cons (f x) (fmap f xs)

instance Applicative MyList where
  pure x = Cons x Nil
  Nil       <*> _   = Nil
  Cons f fs <*> xs  = append (fmap f xs) (fs <*> xs)
    where append Nil ys         = ys
          append (Cons z zs) ys = Cons z (append zs ys)
```
What changes: like Prelude's list `<*>`: apply every function to every value.

### M7 — `liftA2'` from primitives (problem 127)
```haskell
liftA2' :: Applicative f => (a -> b -> c) -> f a -> f b -> f c
liftA2' f fa fb = (f <$> fa) <*> fb
```
What changes: builds binary lift from `<$>` and `<*>`.

### M8 — `pure` as `MyJust` AND `repeat`
Shows that `pure` is NOT unique; for ZipList it's `repeat x`, for List it's `[x]`. Either is correct, depending on the instance.

### M9 — `Applicative (Free f)` (sketch)
```haskell
instance Functor f => Applicative (Free f) where
  pure = Pure
  Pure f   <*> tx       = fmap f tx
  Free ffa <*> tx       = Free (fmap (<*> tx) ffa)
```
What changes: nested `fmap`; recursion inside the constraint.

### M10 — `Applicative (BT)` (sketch — non-standard)
```haskell
data BT a = Empty | Fork a (BT a) (BT a)

instance Applicative BT where
  pure x                       = Fork x Empty Empty   -- one of many choices
  Empty       <*> _            = Empty
  _           <*> Empty        = Empty
  Fork f _ _  <*> tx           = fmap f tx            -- one choice
```
What changes: trees have no canonical Applicative; expose the design choice.

## Worked examples from this course
- Problem sheet Set 13 (#121-128): Functor/Applicative/Monad for `MyMaybe`, `MyList`, `Identity`, `Reader`. Each instance has an Applicative.
- Problem sheet Set 13 (#127): `liftA2'` — M7.
- Practice file: `ewan31-40.hs` and others.
- Assignment 3: `Free f`'s Applicative is given.

## QuickCheck attack surface
- **Applicative identity**: `pure id <*> v == v` — auto-marker tests.
- **Applicative homomorphism**: `pure f <*> pure x == pure (f x)`.
- **Applicative interchange**: `u <*> pure y == pure ($ y) <*> u`.
- **Applicative composition**: `pure (.) <*> u <*> v <*> w == u <*> (v <*> w)`.
- **`fmap` consistency**: `fmap f x == pure f <*> x`.
- **For Validation**: `Failure [a] <*> Failure [b] == Failure [a, b]` (both errors collected — NOT `[a]` or `[b]` alone).
- **For ZipList**: lengths align; result length = min of input lengths.

## Pitfalls (marks-killers)
- **Confusing `pure` with `return`**: same for Monad, but Applicative-only types may not have a Monad.
- **Making Validation a Monad**: `>>=` MUST short-circuit on first error (Monad-fail), which loses the error-accumulation property. Validation cannot be lawful Monad with these semantics.
- **`<*>` argument order**: `f <$> a <*> b <*> c` applies `f` to results IN ORDER.
- **`pure` for ZipList is `repeat`**, NOT `[x]`: with `[x]`, `pure id <*> [1,2,3]` gives `[1]` not `[1,2,3]`.
- **Forgetting `Functor f =>` constraint** on `Applicative` for `Free f`.
- **Mixing `<$>` and `fmap`**: equivalent; `f <$> x = fmap f x`. Stick to one style.

## Combines-with deep dive

### A24 × A06 — full instance chain
After Applicative, write Monad. Most types have all three.

### A24 × A03 — generic monadic combinators with Applicative
`sequence` and `mapM` exist in Applicative form: `sequenceA :: Applicative f => [f a] -> f [a]`. Use when you don't need Monad.

```haskell
sequenceA' :: Applicative f => [f a] -> f [a]
sequenceA' []     = pure []
sequenceA' (x:xs) = (:) <$> x <*> sequenceA' xs
```

### A24 × A16 — parsers ARE Applicative
The Parser combinator chain — `do { x <- p1; y <- p2; return (x, y) }` — can equivalently be `(,) <$> p1 <*> p2`. Applicative-only parsers are simpler than monadic.

## See also

**Combines with:** [A03 generic monad](./A03-generic-monad.md) · [A06 functor instance](./A06-functor-instance.md) · [A22 typeclass instance](./A22-typeclass-instance.md)
**Question families:** [applicative-monad-instance](../question-families/applicative-monad-instance-family.md)
**Theory:** [Applicative typeclass](../typeclasses/applicative.md)
**QuickCheck:** [typeclass instance attacks](../quickcheck/typeclass-instance-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
