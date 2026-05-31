<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: applicative-monad-instance**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · **applicative-monad-instance** · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: applicative-monad-instance

**Archetype:** A13 (Applicative + Monad instances for a custom ADT)   |   **Stars:** ⭐⭐⭐⭐   |   **Course week(s):** 9–10
**Search keywords:** Applicative, Monad, pure, ap, return, bind, instance, Maybe, List, State, Reader

## Generator template
```haskell
-- The seed: every Applicative/Monad instance follows the same skeleton.
-- Applicative needs `pure` and `(<*>)`.
-- Monad needs `return` (= pure) and `(>>=)`.
instance Functor F => Applicative F where
  pure x      = ...   -- "single value"
  af <*> ax   = ...   -- "apply function inside f to value inside f"

instance Applicative F => Monad F where
  return      = pure
  ma >>= k    = ...   -- "feed result of ma into k"
```

Each mutation is a specific F.

## Mutations (the examiner picks one)

### Mutation 1 — MyMaybe (Applicative + Monad) (= problem 121)
**Sig:**
```haskell
instance Applicative MyMaybe
instance Monad MyMaybe
```
**Solution:**
```haskell
data MyMaybe a = MyNothing | MyJust a

instance Functor MyMaybe where
  fmap _ MyNothing  = MyNothing
  fmap f (MyJust x) = MyJust (f x)

instance Applicative MyMaybe where
  pure                       = MyJust
  MyNothing <*> _            = MyNothing
  _ <*> MyNothing            = MyNothing
  MyJust f <*> MyJust x      = MyJust (f x)

instance Monad MyMaybe where
  return                     = pure
  MyNothing >>= _            = MyNothing
  MyJust x  >>= k            = k x
```
**QC trap:** Both `Nothing` cases must be handled in `<*>`. Bind on Nothing short-circuits without calling `k`.

### Mutation 2 — MyList (= problem 122)
**Solution:**
```haskell
data MyList a = Nil | Cons a (MyList a)

instance Applicative MyList where
  pure x                       = Cons x Nil
  Nil <*> _                    = Nil
  _ <*> Nil                    = Nil
  Cons f fs <*> xs             = appendL (fmap f xs) (fs <*> xs)
    where
      appendL Nil ys           = ys
      appendL (Cons x xs) ys   = Cons x (appendL xs ys)

instance Monad MyList where
  return = pure
  Nil >>= _              = Nil
  Cons x xs >>= k        = appendL (k x) (xs >>= k)
    where
      appendL Nil ys           = ys
      appendL (Cons x xs) ys   = Cons x (appendL xs ys)
```
**QC trap:** `<*>` produces the Cartesian product of fs and xs in the right order: `[f,g] <*> [1,2] = [f 1, f 2, g 1, g 2]`.

### Mutation 3 — Identity (= problem 123)
**Solution:**
```haskell
newtype Identity a = Identity a

instance Functor Identity where
  fmap f (Identity x) = Identity (f x)

instance Applicative Identity where
  pure                            = Identity
  Identity f <*> Identity x       = Identity (f x)

instance Monad Identity where
  return                          = pure
  Identity x >>= k                = k x
```
**QC trap:** Trivial — just unwrap, apply, rewrap. Useful as a sanity check on understanding.

### Mutation 4 — Reader (= problem 124)
**Solution:**
```haskell
newtype Reader r a = Reader { runReader :: r -> a }

instance Functor (Reader r) where
  fmap f (Reader g) = Reader (f . g)

instance Applicative (Reader r) where
  pure x                   = Reader (\_ -> x)
  Reader rf <*> Reader rx  = Reader (\r -> rf r (rx r))

instance Monad (Reader r) where
  return                   = pure
  Reader rx >>= k          = Reader (\r -> runReader (k (rx r)) r)
```
**QC trap:** Both `rf r` and `rx r` use the *same* `r`. That's what makes Reader "broadcast" the environment.

### Mutation 5 — State (custom version)
**Solution:**
```haskell
newtype State s a = State { runState :: s -> (a, s) }

instance Functor (State s) where
  fmap f (State g) = State (\s -> let (a, s') = g s in (f a, s'))

instance Applicative (State s) where
  pure x = State (\s -> (x, s))
  State sf <*> State sx = State (\s -> let (f, s')  = sf s
                                           (a, s'') = sx s'
                                       in  (f a, s''))

instance Monad (State s) where
  return = pure
  State g >>= k = State (\s -> let (a, s') = g s
                               in  runState (k a) s')
```
**QC trap:** State threads `s` left-to-right. The order of `sf` then `sx` matters: `pure (,) <*> getCounter <*> getCounter` gives `(0, 1)`, not `(0, 0)`.

### Mutation 6 — Writer (with Monoid w)
**Solution:**
```haskell
newtype Writer w a = Writer { runWriter :: (a, w) }

instance Functor (Writer w) where
  fmap f (Writer (a, w)) = Writer (f a, w)

instance Monoid w => Applicative (Writer w) where
  pure x                              = Writer (x, mempty)
  Writer (f, w1) <*> Writer (x, w2)   = Writer (f x, w1 <> w2)

instance Monoid w => Monad (Writer w) where
  return                              = pure
  Writer (x, w1) >>= k                = let Writer (y, w2) = k x
                                        in  Writer (y, w1 <> w2)
```
**QC trap:** Log accumulation order: `w1 <> w2` (earlier action first). Use `Semigroup`/`Monoid` constraint correctly.

### Mutation 7 — Free f (= Assignment 3 setup)
**Solution:**
```haskell
data Free f a = Pure a | Free (f (Free f a))

instance Functor f => Functor (Free f) where
  fmap g (Pure x)   = Pure (g x)
  fmap g (Free fxs) = Free (fmap (fmap g) fxs)

instance Functor f => Applicative (Free f) where
  pure                  = Pure
  Pure g <*> x          = fmap g x
  Free fg <*> x         = Free (fmap (<*> x) fg)

instance Functor f => Monad (Free f) where
  return                = pure
  Pure x >>= k          = k x
  Free fx >>= k         = Free (fmap (>>= k) fx)
```
**QC trap:** Each `>>=` adds one layer. Recursive `fmap (>>= k)` applies it inside `f`. The two `fmap`s are easy to confuse — outer is for `f`, inner is for `Free f`.

### Mutation 8 — Either e
**Solution:**
```haskell
-- Already in Prelude. As reimplementation:
data MyEither e a = MyLeft e | MyRight a

instance Functor (MyEither e) where
  fmap _ (MyLeft e)  = MyLeft e
  fmap f (MyRight x) = MyRight (f x)

instance Applicative (MyEither e) where
  pure                                 = MyRight
  MyLeft e  <*> _                      = MyLeft e
  MyRight _ <*> MyLeft e               = MyLeft e
  MyRight f <*> MyRight x              = MyRight (f x)

instance Monad (MyEither e) where
  return                               = pure
  MyLeft e  >>= _                      = MyLeft e
  MyRight x >>= k                      = k x
```
**QC trap:** First Left wins in `<*>`. Bind short-circuits on Left.

### Mutation 9 — Pair e (with Monoid e)
**Spec:** `Pair e a` accumulates `e` (like Writer but no log split).
**Solution:**
```haskell
data Pair e a = Pair e a

instance Functor (Pair e) where
  fmap f (Pair e a) = Pair e (f a)

instance Monoid e => Applicative (Pair e) where
  pure x                              = Pair mempty x
  Pair e1 f <*> Pair e2 x             = Pair (e1 <> e2) (f x)

instance Monoid e => Monad (Pair e) where
  return                              = pure
  Pair e1 x >>= k                     = let Pair e2 y = k x
                                        in  Pair (e1 <> e2) y
```
**QC trap:** This is essentially `Writer` with arguments swapped.

### Mutation 10 — ZipList-style Applicative (non-monad)
**Spec:** Lists where `<*>` zips instead of cross-products. NB: ZipList is NOT a monad.
**Solution:**
```haskell
newtype ZipList a = ZipList { getZipList :: [a] }

instance Functor ZipList where
  fmap f (ZipList xs) = ZipList (map f xs)

instance Applicative ZipList where
  pure x                                  = ZipList (repeat x)
  ZipList fs <*> ZipList xs               = ZipList (zipWith ($) fs xs)
```
**QC trap:** `pure x` is `repeat x` (infinite). No Monad instance exists. Useful to mention as an exam discussion point.

## Hidden-predicate mutations
Rarely seen — most variations are about *which* type is the instance. The "trick" is usually:
- "prove your <*> agrees with `ap`" (`ap mf mx = mf >>= \f -> mx >>= \x -> return (f x)`).
- "prove your Monad satisfies left-identity, right-identity, associativity".

## Accumulator-style alternative
Not applicable — instance methods are essentially mechanical.

## Fold-style alternative
For lists: `sequence = foldr (\m ms -> (:) <$> m <*> ms) (pure [])`. Useful — see `monad-combinator-family.md`.

## Cross-family combinations
- this family + `functor-instance-family.md` — strict prerequisite.
- this family + `state-game-family.md` — once you have the State instance you can game with it.
- this family + `writer-trace-family.md` — Writer is mutation 6.
- this family + `error-handling-family.md` — Maybe and Either monads.

## QuickCheck universal attacks
- **Functor laws:** `fmap id == id`, `fmap (f . g) == fmap f . fmap g`.
- **Applicative laws:**
  - identity: `pure id <*> v == v`
  - composition: `pure (.) <*> u <*> v <*> w == u <*> (v <*> w)`
  - homomorphism: `pure f <*> pure x == pure (f x)`
  - interchange: `u <*> pure y == pure ($ y) <*> u`
- **Monad laws:**
  - left-identity: `return x >>= k == k x`
  - right-identity: `m >>= return == m`
  - associativity: `(m >>= k) >>= h == m >>= (\x -> k x >>= h)`
- **Consistency:** `ap == <*>` for any Monad. (Free property if both instances exist.)

## Pitfalls (per mutation)
- M1: missing one of the two Nothing cases in `<*>`.
- M2: getting the order wrong (xs Cartesian-product semantics).
- M3: forgetting to unwrap.
- M4: passing different `r` to rf and rx.
- M5: not threading the state correctly through both arms.
- M6: log concatenation order.
- M7: inner vs outer fmap confusion.
- M8: missing the Left short-circuit.
- M9: confusing Monoid for `e` vs `a`.
- M10: thinking ZipList is a Monad (it isn't).
- M11: copying Either's first-error `<*>` (loses the accumulation); or adding a Monad instance (Validation has none).


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — Validation (accumulating Applicative, deliberately NOT a Monad)

**Spec:** Like `Either e`, but `(<*>)` *accumulates* all the failures via a `Semigroup e` instead of stopping at the first one. There is **no lawful `Monad` instance** — bind would have to pick one branch's error and discard the other, breaking the "collect everything" behaviour, so the examiner asks only for `Functor` + `Applicative`.

**Type sig:**
```haskell
data Validation e a = Failure e | Success a
instance Functor (Validation e)
instance Semigroup e => Applicative (Validation e)
```

```haskell
data Validation e a = Failure e | Success a

instance Functor (Validation e) where
  fmap _ (Failure e) = Failure e
  fmap f (Success a) = Success (f a)

instance Semigroup e => Applicative (Validation e) where
  pure = Success
  Failure e1 <*> Failure e2 = Failure (e1 <> e2)
  Failure e  <*> _          = Failure e
  _          <*> Failure e  = Failure e
  Success f  <*> Success a  = Success (f a)
```

**What changes vs seed:** Same two-constructor shape as `Either` (M8), but the error channel is **combined**, not short-circuited. The `Failure <*> Failure` case is the whole point — it `<>`s both errors. Needs the `Semigroup e` constraint; the seed/M8 versions don't. With an error type like `[String]`, `(+) <$> Failure ["a"] <*> Failure ["b"] == Failure ["a","b"]` — Either would give only `Left "a"`.

**QC trap:** Forgetting the `Failure e1 <*> Failure e2` case (and just reusing the Either pattern of "first Left wins") loses errors — the accumulation property fails. **Do NOT add a `Monad` instance:** `Validation` is a textbook Applicative-that-is-not-a-Monad, because `>>=` cannot keep accumulating once it has to choose a branch. The whitelisted `Semigroup`/`<>` is all you need (no extra imports).

## See also

**Primary archetype:** [A24 applicative instance](../archetypes/A24-applicative-instance.md)
**Sibling families:** [functor-instance](./functor-instance-family.md) · [monad-combinator](./monad-combinator-family.md)
**Theory:** [applicative](../typeclasses/applicative.md) · [monad](../typeclasses/monad.md)
**QuickCheck:** [typeclass-instance attacks](../quickcheck/typeclass-instance-attacks.md) · [monad attacks](../quickcheck/monad-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
