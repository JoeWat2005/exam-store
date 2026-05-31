<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [typeclasses](./README.md) · **Alternative**

<!-- siblings:start -->
> **Peers:** **alternative** · [applicative](./applicative.md) · [eq-ord](./eq-ord.md) · [foldable](./foldable.md) · [functor](./functor.md) · [monad](./monad.md) · [monoid](./monoid.md) · [num](./num.md) · [show](./show.md) · [traversable](./traversable.md)
<!-- siblings:end -->






# Alternative

> **Mental model:** *Choice with failure.* `empty` is "no result"; `(<|>)` is "try the left, if it fails fall through to the right". Heart of parser combinators — `expr <|> term <|> factor` tries alternatives in order.

**Methods:** `empty :: f a`, `(<|>) :: f a -> f a -> f a`. Subclass of [Applicative](applicative.md).

**Laws:**
- Left identity:   `empty <|> x = x`
- Right identity:  `x <|> empty = x`
- Associativity:   `(x <|> y) <|> z = x <|> (y <|> z)`

So `(<|>, empty)` is a monoid on `f a` for every `a`.

**Search keywords:** Alternative, empty, <|>, MonadPlus, mzero, mplus, many, some, optional, asum, msum

## Recognition triggers

- "Implement parser alternatives"
- "Try this; if it fails, try that"
- "Implement `<|>` for `T`"
- "Return all successes / pick the first success"

## Class

```haskell
class Applicative f => Alternative f where
  empty :: f a
  (<|>) :: f a -> f a -> f a

  many  :: f a -> f [a]    -- 0 or more (default impl uses <|>)
  some  :: f a -> f [a]    -- 1 or more

  many v = some v <|> pure []
  some v = (:) <$> v <*> many v
```

## Canonical templates

### Maybe

```haskell
instance Alternative Maybe where
  empty               = Nothing
  Nothing <|> r       = r
  l       <|> _       = l           -- left-biased: first Just wins
```

### List (concatenate alternatives)

```haskell
instance Alternative [] where
  empty = []
  (<|>) = (++)
```

### Parser (course-style)

```haskell
instance Alternative Parser where
  empty       = P (\_ -> [])
  P p <|> P q = P (\s -> case p s of
                           []  -> q s   -- fall through
                           rs  -> rs)   -- left succeeded
```

### Either (only when error is a Monoid — rarely useful)

```haskell
instance Monoid e => Alternative (Either e) where
  empty                  = Left mempty
  Left e1 <|> Left e2    = Left (e1 <> e2)
  Left _  <|> r          = r
  l       <|> _          = l
```

## Derived combinators

```haskell
optional :: Alternative f => f a -> f (Maybe a)
optional p = (Just <$> p) <|> pure Nothing

asum :: (Alternative f, Foldable t) => t (f a) -> f a
asum = foldr (<|>) empty
-- Try a list of alternatives; first success wins.

guard :: Alternative f => Bool -> f ()
guard True  = pure ()
guard False = empty
-- Used in monad comprehensions / list-monad guards.
```

## Use cases

- **Parser**: `term = number <|> parenthesized expr <|> variable`
- **Lookup with fallback**: `lookup k m1 <|> lookup k m2 <|> Just defaultValue`
- **Validation**: try strict parse, fall back to lenient.
- **List monad guards**: `do x <- xs; guard (x > 0); return x` filters via Alternative.

## Pitfalls

- **Maybe is left-biased.** `Just 1 <|> Just 2 = Just 1`. Returns first success.
- **List `<|>` is `++`** — combines ALL successes, not "first wins".
- **Parser ordering matters.** `expr <|> term` first tries `expr`; if `expr` partial-matches and consumes input, `term` may not see what it expects. Course's simple Parser doesn't backtrack — order from most-specific to least.
- **`many` on a no-progress parser loops forever.** `many (pure ())` never terminates. The parser inside must consume input.
- **`empty` must satisfy laws.** Not every Applicative is Alternative.
- **`MonadPlus` is the Monad-flavored variant.** Same methods (`mzero`, `mplus`) — Maybe and List have both; check `Control.Monad`.

## Alternative laws as QuickCheck props

```haskell
prop_alt_left_id  :: (Alternative f, Eq (f a)) => f a -> Bool
prop_alt_left_id  x = (empty <|> x) == x

prop_alt_right_id :: (Alternative f, Eq (f a)) => f a -> Bool
prop_alt_right_id x = (x <|> empty) == x

prop_alt_assoc :: (Alternative f, Eq (f a)) => f a -> f a -> f a -> Bool
prop_alt_assoc x y z = ((x <|> y) <|> z) == (x <|> (y <|> z))
```

## QuickCheck attacks

- Monoid laws on `(<|>, empty)`.
- For Maybe: `Just x <|> y == Just x` (left bias).
- For List: `xs <|> ys == xs ++ ys`.
- For Parser: `parse (p <|> q) s == parse p s` if `parse p s` is non-empty.
- `many empty == pure []` (terminates with `pure []`).

## See also

**Archetypes:** [A16 parser combinators](../archetypes/A16-parser-combinators.md)
**Question families:** [parser](../question-families/parser-family.md)
**Related (typeclasses):** [applicative](./applicative.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
