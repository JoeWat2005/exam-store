<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Monad Laws**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · [generic-combinators](./generic-combinators.md) · [io](./io.md) · [list-monad](./list-monad.md) · [maybe](./maybe.md) · **monad-laws** · [monaderror](./monaderror.md) · [multi-effect](./multi-effect.md) · [reader](./reader.md) · [state](./state.md) · [transformer-stack-order](./transformer-stack-order.md) · [transformers](./transformers.md) · [writer](./writer.md)
<!-- siblings:end -->






# Monad Laws

Any `instance Monad m` MUST satisfy three laws. These are not enforced by the type system, but the auto-marker for instance-questions (#121–#124) WILL check them — typically via QuickCheck.

## The three laws

### 1. Left identity
```
return x >>= f   ≡   f x
```
"Wrapping then immediately binding does nothing."

### 2. Right identity
```
m >>= return     ≡   m
```
"Binding `return` at the end of a chain does nothing."

### 3. Associativity
```
(m >>= f) >>= g   ≡   m >>= (\x -> f x >>= g)
```
"You can re-parenthesise `>>=` chains freely."

## QuickCheck-property form

These are directly testable. Use `Eq (m a)` or, when `m a` isn't `Eq` (e.g. `IO`, function-monads), compare runners.

### For `Maybe`
```haskell
import Test.QuickCheck

prop_leftId  :: Int -> (Int -> Maybe Int) -> Bool
prop_leftId  x f = (return x >>= f) == f x

prop_rightId :: Maybe Int -> Bool
prop_rightId m = (m >>= return) == m

prop_assoc   :: Maybe Int -> (Int -> Maybe Int) -> (Int -> Maybe Int) -> Bool
prop_assoc m f g = ((m >>= f) >>= g) == (m >>= (\x -> f x >>= g))
```
Run with `quickCheck prop_leftId`.

### For `Either e` (with `Eq e`)
```haskell
prop_leftId  :: Int -> (Int -> Either String Int) -> Bool
prop_leftId  x f = (return x >>= f) == f x

prop_rightId :: Either String Int -> Bool
prop_rightId m = (m >>= return) == m

prop_assoc   :: Either String Int
              -> (Int -> Either String Int)
              -> (Int -> Either String Int)
              -> Bool
prop_assoc m f g = ((m >>= f) >>= g) == (m >>= (\x -> f x >>= g))
```

### For lists `[]`
```haskell
prop_leftId_list :: Int -> (Int -> [Int]) -> Bool
prop_leftId_list x f = (return x >>= f) == f x

prop_rightId_list :: [Int] -> Bool
prop_rightId_list m = (m >>= return) == m
```

### For `State s` (no Eq instance — compare via `runState`)
```haskell
prop_leftId_state :: Int -> Int -> Bool
prop_leftId_state x s0 =
  runState (return x >>= (\v -> pure (v + 1))) s0
  ==
  runState ((\v -> pure (v + 1)) x) s0
```
Pattern: run BOTH sides with the same `s0`, compare the resulting `(a, s)`.

### For `Writer w` (works because `Writer w a` is `Eq` if `a, w` are)
```haskell
prop_leftId_writer :: Int -> Bool
prop_leftId_writer x = runWriter (return x >>= f) == runWriter (f x)
 where
  f n = do tell ["x"]; pure (n + 1)
```

### For Function-monad `((->) r)` (extensional — test on samples)
```haskell
prop_leftId_fn :: Int -> Int -> Bool
prop_leftId_fn r x = ((return x >>= f) r) == (f x r)
 where f n = (+ n)
```

## Why the laws matter

- The laws make `do`-notation re-orderable in safe ways.
- The marker for `instance Monad MyMaybe` (problem 121) typically QuickChecks all three.
- A "wrong" but type-correct definition (e.g. `pure x = Just x; m >>= f = Nothing`) compiles fine but FAILS the laws and the marker.

## Common law-violating mistakes (in student instances)

### Violating left identity
```haskell
instance Monad MyMaybe where
  return _ = MyNothing            -- WRONG — left-id violated
  ...
```

### Violating right identity (List)
```haskell
instance Monad MyList where
  return x = Cons x (Cons x Nil)  -- WRONG — return must put EXACTLY ONE
  ...
```

### Violating associativity (using `++` wrong in list)
```haskell
xs >>= f = foldr (++) [] (map (reverse . f) xs)   -- WRONG, reverses results
```

## Functor and Applicative laws (recap)

If you're asked to define `Functor`/`Applicative`/`Monad` for a type:

### Functor laws
```
fmap id      ≡  id
fmap (g . f) ≡  fmap g . fmap f
```

### Applicative laws
```
pure id <*> v             ≡  v
pure f <*> pure x         ≡  pure (f x)
u <*> pure y              ≡  pure ($ y) <*> u
u <*> (v <*> w)           ≡  pure (.) <*> u <*> v <*> w
```

### Monad–Applicative compatibility
```
pure   ≡  return
m <*> n  ≡  do { f <- m; x <- n; pure (f x) }    -- = ap m n
```

## Worked examples

- Problem 121 — `MyMaybe`: prove the three laws by hand AND test by QuickCheck.
- Problem 122 — `MyList`.
- Problem 123 — `Identity` (trivially satisfies all three).
- Problem 124 — `Reader r` (extensionality required).

## See also

**Archetypes:** [A20 laws / iso](../archetypes/A20-laws-iso.md) · [A22 typeclass instance](../archetypes/A22-typeclass-instance.md)
**QuickCheck:** [typeclass-instance attacks](../quickcheck/typeclass-instance-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
