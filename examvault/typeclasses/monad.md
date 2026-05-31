<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [typeclasses](./README.md) · **Monad**

<!-- siblings:start -->
> **Peers:** [alternative](./alternative.md) · [applicative](./applicative.md) · [eq-ord](./eq-ord.md) · [foldable](./foldable.md) · [functor](./functor.md) · **monad** · [monoid](./monoid.md) · [num](./num.md) · [show](./show.md) · [traversable](./traversable.md)
<!-- siblings:end -->






# Monad

> **Mental model:** Applicative sequences *independent* effects. Monad sequences *dependent* effects — the second computation can *depend on* the result of the first via `x <- mx; my x`. `do`-notation is just sugar over `>>=`. Each Monad's instance decides what "effect" means: failure (Maybe), state (State), nondeterminism (`[]`), I/O, error, log.

**Methods:** `return :: a -> m a`, `(>>=) :: m a -> (a -> m b) -> m b`. Subclass of [Applicative](applicative.md).

**Laws:**
- Left identity:    `return x >>= f = f x`
- Right identity:   `m >>= return  = m`
- Associativity:    `(m >>= f) >>= g = m >>= (\x -> f x >>= g)`

**Search keywords:** instance Monad, return, >>=, do-notation, Monad Maybe, Monad List, Monad State, Monad Reader, Monad Writer, Monad Parser

## Recognition triggers

- "Make `T` a `Monad`" → write Functor + Applicative + Monad trio
- "Define `(>>=)` for `T`"
- "Show `do`-notation desugars to bind"
- Question gives you ADT + asks for monad effect (often: failure, state, log)

## Class

```haskell
class Applicative m => Monad m where
  return :: a -> m a            -- canonically = pure
  (>>=)  :: m a -> (a -> m b) -> m b
```

In modern Haskell `return = pure` always; you *can* override but shouldn't.

## The Functor / Applicative / Monad trio

To declare `instance Monad M`, you MUST also declare `instance Functor M` and `instance Applicative M`. Canonical pattern:

```haskell
data M a = ...

instance Functor M where
  fmap f mx = mx >>= return . f                -- via monad

instance Applicative M where
  pure       = return
  mf <*> mx  = mf >>= \f -> mx >>= \x -> return (f x)

instance Monad M where
  return = ...
  (>>=)  = ...
```

You only have to define `return` and `(>>=)` from scratch — Functor and Applicative can be derived as shown.

## do-notation desugaring (CRITICAL)

```haskell
do x <- m1                ≡   m1 >>= \x -> do
   rest                              rest

do m1                     ≡   m1 >> rest    -- (m1 >>= \_ -> rest)
   rest

do x <- m1; return x      ≡   m1

do return x; rest         ≡   rest

do let y = e              ≡   let y = e in do
   rest                              rest
```

If asked to "translate this do-block to >>= form", apply these rules top-down, line by line. Each `<-` becomes `>>= \var ->`.

### Worked desugaring

```haskell
do x <- mx
   y <- f x
   return (x + y)
```
desugars to
```haskell
mx >>= \x ->
  f x >>= \y ->
    return (x + y)
```

## Canonical templates per ADT

### Maybe (short-circuit on Nothing)

```haskell
instance Functor Maybe where
  fmap _ Nothing  = Nothing
  fmap f (Just x) = Just (f x)

instance Applicative Maybe where
  pure              = Just
  Nothing  <*> _    = Nothing
  (Just f) <*> mx   = fmap f mx

instance Monad Maybe where
  return        = Just
  Nothing >>= _ = Nothing
  Just x  >>= f = f x
```

### List (non-determinism — fan out then concat)

```haskell
instance Monad [] where
  return x = [x]
  xs >>= f = concat (map f xs)
  -- equivalent: [y | x <- xs, y <- f x]
```

### Reader

```haskell
instance Monad ((->) r) where
  return = const
  m >>= f = \e -> f (m e) e
```

### State (hand-rolled)

```haskell
newtype State s a = State { runState :: s -> (a, s) }

instance Functor (State s) where
  fmap f (State p) = State $ \s -> let (x, s') = p s in (f x, s')

instance Applicative (State s) where
  pure x = State (\s -> (x, s))
  State pf <*> State px = State $ \s ->
    let (f, s')  = pf s
        (x, s'') = px s'
    in (f x, s'')

instance Monad (State s) where
  return x = State (\s -> (x, s))
  State p >>= f = State $ \s ->
    let (x, s')  = p s
        State q  = f x
    in q s'
```

### Writer (hand-rolled)

```haskell
newtype Writer w a = Writer { runWriter :: (a, w) }

instance Monoid w => Functor (Writer w) where
  fmap f (Writer (x, w)) = Writer (f x, w)

instance Monoid w => Applicative (Writer w) where
  pure x = Writer (x, mempty)
  Writer (f, w1) <*> Writer (x, w2) = Writer (f x, w1 <> w2)

instance Monoid w => Monad (Writer w) where
  return = pure
  Writer (x, w1) >>= f =
    let Writer (y, w2) = f x
    in Writer (y, w1 <> w2)
```

### Parser

```haskell
instance Monad Parser where
  return x  = P (\s -> [(x, s)])
  P p >>= f = P (\s -> concat [parse (f x) s' | (x, s') <- p s])
```

### Either (Left short-circuits — like Maybe with payload)

```haskell
instance Monad (Either e) where
  return         = Right
  Left e  >>= _  = Left e
  Right x >>= f  = f x
```

### Custom ADT — a "Failable" monad

```haskell
data F a = OK a | Err String

instance Functor F where
  fmap _ (Err s) = Err s
  fmap f (OK x)  = OK (f x)

instance Applicative F where
  pure                = OK
  Err s   <*> _       = Err s
  OK f    <*> mx      = fmap f mx

instance Monad F where
  return        = OK
  OK x   >>= f  = f x
  Err s  >>= _  = Err s
```

## Monad laws as QuickCheck props

```haskell
prop_left_id :: (Eq (m b), Monad m, ...) => a -> Fun a (m b) -> Bool
prop_left_id x (Fun _ f) = (return x >>= f) == f x

prop_right_id :: (Eq (m a), Monad m) => m a -> Bool
prop_right_id m = (m >>= return) == m

prop_assoc :: (Eq (m c), Monad m, ...)
           => m a -> Fun a (m b) -> Fun b (m c) -> Bool
prop_assoc m (Fun _ f) (Fun _ g) =
  ((m >>= f) >>= g) == (m >>= (\x -> f x >>= g))
```

These three laws are precisely what the marker checks.

## Pitfalls

- **Forget the trio.** Modern Haskell REQUIRES `Functor M` and `Applicative M` before `instance Monad M`. Auto-marker will reject if missing.
- **Use `pure` and `return` consistently.** Set `return = pure` and stop worrying.
- **List `>>=` must `concat`.** `xs >>= f = map f xs` is wrong (gives `[m a]` not `m a`). Use `concat (map f xs)`.
- **State threading.** Inside `>>=` you must thread `s -> s' -> s''` — extracting from left and passing to right.
- **Writer mempty.** `pure x = Writer (x, mempty)` — `mempty` requires `Monoid w` constraint on the instance.
- **Reader `>>=` shape.** `m >>= f = \e -> f (m e) e` — must pass `e` to BOTH `m` and the result `f (m e)`.
- **Do-block over the wrong monad.** A `do x <- mx` in a function returning `Maybe` must have all RHS in `Maybe`.
- **`return == Just`** for Maybe, NOT `Nothing`. `return` is the *success* injection.

## QuickCheck attacks

- Left identity, right identity, associativity (above).
- For Maybe: `Nothing >>= f == Nothing` for any `f`.
- For List: `[1,2,3] >>= return == [1,2,3]`.
- For State: state threading via `evalState`/`execState`.
- For trees-as-monad: `t >>= return == t` (right identity).

## Worked example — translating a do-block

Question: rewrite using `>>=` only.

```haskell
ex :: Maybe Int
ex = do x <- Just 3
        y <- Just 4
        return (x + y)
```

Desugaring step by step:

```haskell
ex = Just 3 >>= \x ->
     Just 4 >>= \y ->
     return (x + y)
```

Or fully without lambdas (associativity):

```haskell
ex = Just 3 >>= (\x -> Just 4 >>= (\y -> return (x + y)))
```

## See also

**Archetypes:** [A03 generic monad](../archetypes/A03-generic-monad.md) · [A22 typeclass instance](../archetypes/A22-typeclass-instance.md)
**Cross-topic:** [tree × generic-monad](../cross-matrix/tree-x-generic-monad.md)
**Question families:** [monad-combinator](../question-families/monad-combinator-family.md) · [applicative-monad-instance](../question-families/applicative-monad-instance-family.md)
**QuickCheck:** [monad attacks](../quickcheck/monad-attacks.md) · [typeclass-instance attacks](../quickcheck/typeclass-instance-attacks.md)
**Related (typeclasses):** [functor](./functor.md) · [applicative](./applicative.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
