<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: typeclass instances (Functor, Monad, Eq, Show, etc.)**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · **typeclass-instance** · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: typeclass instances (Functor, Monad, Eq, Show, etc.)

**Search keywords:** instance, Functor, Monad, Applicative, Foldable, Eq, Ord, Show, law, fmap id, fmap composition, return, pure, bind, associativity, left identity, right identity, reflexivity

When the spec asks you to write an `instance Functor MyType where ...` (or Monad, Eq, Show, etc.), the marker may check the **laws** via QC. Each law is a property template.

## What the marker generates

The marker has `Arbitrary` instances for the type you wrote an instance for (or it derives one). It then runs the LAW properties — `fmap id == id`, `fmap (f . g) == fmap f . fmap g`, etc.

For Show, the marker may parse your output and check it can be `read` back, or it may compare against a reference Show.

For Eq, the marker checks reflexivity, symmetry, transitivity — and equality after operations (insert, delete, etc.).

## Functor laws

```haskell
-- Law 1: fmap id == id
prop_functorId :: f a -> Bool
prop_functorId x = fmap id x == x

-- Law 2: fmap (f . g) == fmap f . fmap g
prop_functorComp :: (a -> b) -> (c -> a) -> f c -> Bool
prop_functorComp f g x = fmap (f . g) x == fmap f (fmap g x)
```

If you write `fmap` for a list-like type, both laws must hold. If they fail, your instance is wrong by definition.

### Functor attack surface

| # | Attack | Example bug | Fix |
|---|--------|------------|-----|
| 1 | `fmap id` doesn't equal `id` | You apply `f` somewhere extra | `fmap` should only apply `f` to the "values" once each |
| 2 | `fmap (f . g)` not equal to `fmap f . fmap g` | You compose in wrong order | Standard `fmap f . fmap g x = fmap f (fmap g x)` |
| 3 | `fmap` not structure-preserving | A `Branch` becomes a `Leaf` somehow | Map values, not structure |
| 4 | `fmap` evaluation strictness | Lazy `fmap` is forced eagerly | Mostly fine; deepseq applies |

## Monad laws (and Applicative + Monad inclusion)

```haskell
-- Law 1: left identity: return x >>= f == f x
prop_monadLeftId :: a -> (a -> m b) -> Bool
prop_monadLeftId x f = (return x >>= f) == f x

-- Law 2: right identity: m >>= return == m
prop_monadRightId :: m a -> Bool
prop_monadRightId m = (m >>= return) == m

-- Law 3: associativity: (m >>= f) >>= g == m >>= (\x -> f x >>= g)
prop_monadAssoc :: m a -> (a -> m b) -> (b -> m c) -> Bool
prop_monadAssoc m f g = ((m >>= f) >>= g) == (m >>= (\x -> f x >>= g))
```

### Monad attack surface

| # | Attack | Example bug | Fix |
|---|--------|------------|-----|
| 1 | Left identity fails | `return x` does more than wrap `x` | `return = Pure` or `return x = [x]` etc. — pure value |
| 2 | Right identity fails | `>>= return` loses information | Bind to `return` should be identity |
| 3 | Associativity fails | Sequential binds non-equivalent to nested binds | Standard monad implementation; usually free if you implement bind structurally |
| 4 | `do`-notation desugaring | `do { x <- m; f x }` vs `m >>= f` | Should be the same |
| 5 | Applicative consistency | `pure f <*> x == fmap f x` | Required by Applicative-Monad inclusion |

## Eq laws

```haskell
-- Reflexivity
prop_eqRefl :: a -> Bool
prop_eqRefl x = x == x

-- Symmetry
prop_eqSym :: a -> a -> Bool
prop_eqSym x y = (x == y) == (y == x)

-- Transitivity
prop_eqTrans :: a -> a -> a -> Property
prop_eqTrans x y z = (x == y && y == z) ==> (x == z)
```

For tree-like types, equality is by structure. For BSTs, equality is sometimes by elements (set semantics) — read spec.

### Eq attack surface

| # | Attack | Example bug | Fix |
|---|--------|------------|-----|
| 1 | Reflexivity fails for `NaN` | `NaN /= NaN` | Don't include Doubles unless allowed |
| 2 | Symmetry fails | Bug in implementation comparing only one direction | `x == y == y == x` (both must call `==`) |
| 3 | Transitivity fails | Float arithmetic | Same |
| 4 | `Eq` for tree by elements vs structure | `Node 5 Empty (Node 3 _ _)` vs `Node 3 (Node 5 _ _) _` | Usually structural for explicit data types; semantic for BSTs |

## Show

The marker may:
- Parse your output and check it back
- Compare against a reference `Show`
- Check `read . show == id` (a.k.a. Show-Read round-trip)

For Assignment 1, the marker has a parser for the colored output and checks dimensions/values:
```haskell
parseRow :: String -> Bool -> Maybe ([(Int, Bool)], Bool)
parseRow ('\ESC' : '[' : '4' : '4' : 'm' : xs) _ = parseRow xs True
parseRow ('\ESC' : '[' : '0' : 'm' : xs) _       = parseRow xs False
```

So your Show must use the exact ANSI codes `\ESC[44m` and `\ESC[0m`.

### Show attack surface

| # | Attack | Example bug | Fix |
|---|--------|------------|-----|
| 1 | Missing ANSI codes | You print plain text | Use the EXACT codes the marker expects |
| 2 | Off-by-one row count | Forgot the pointer row | Total rows = top + 1 + bottom |
| 3 | Off-by-one col count | Forgot to count both left and right of pointer | Total cols = left + 1 + right |
| 4 | Multiple highlights | Two `\ESC[44m` in output | Only ONE element highlighted (the pointer) |
| 5 | Trailing newline | Last row has no newline | Spec-dependent |

## Ord laws

```haskell
prop_ordRefl :: a -> Bool
prop_ordRefl x = compare x x == EQ

prop_ordAntisym :: a -> a -> Bool
prop_ordAntisym x y = (compare x y == EQ) == (compare y x == EQ)

prop_ordTrans :: a -> a -> a -> Property
prop_ordTrans x y z = (compare x y == LT && compare y z == LT) ==>
                     (compare x z == LT)
```

## Foldable laws

```haskell
prop_foldMapNeutral :: t a -> Bool
prop_foldMapNeutral t = foldMap (const mempty) t == mempty
```

## Property templates (instance-flavoured)

```haskell
import Test.QuickCheck

-- General test for Functor (parameterise on your type)
prop_FunctorId :: (Functor f, Eq (f a)) => f a -> Bool
prop_FunctorId x = fmap id x == x

prop_FunctorComp :: (Functor f, Eq (f c))
                 => (a -> b) -> (c -> a) -> f c -> Bool
prop_FunctorComp f g x = fmap (f . g) x == fmap f (fmap g x)

-- Show-Read round-trip (only if instance Read also exists)
prop_showRead :: (Show a, Read a, Eq a) => a -> Bool
prop_showRead x = read (show x) == x

-- Eq reflexivity
prop_eqRefl :: Eq a => a -> Bool
prop_eqRefl x = x == x
```

## Self-test before submission checklist

For ANY instance you write:

- [ ] All required methods are defined (don't rely on defaults you didn't check)
- [ ] No `undefined` methods
- [ ] Type signatures of methods (if you wrote them) match the class signature

For `Functor`:
- [ ] `fmap id x == x` for any `x`
- [ ] `fmap (f . g) x == fmap f (fmap g x)` for any `f`, `g`, `x`

For `Monad` (and `Applicative`):
- [ ] `return x >>= f == f x` (left identity)
- [ ] `m >>= return == m` (right identity)
- [ ] `(m >>= f) >>= g == m >>= (\x -> f x >>= g)` (associativity)
- [ ] `pure == return`
- [ ] `pure f <*> x == fmap f x` (applicative-functor consistency)

For `Eq`:
- [ ] `x == x` always
- [ ] `x == y` iff `y == x`
- [ ] `x == y && y == z` implies `x == z`

For `Show`:
- [ ] Output matches the format the marker expects (read the prop file)
- [ ] If marker checks `read . show == id`, that holds

For `Ord`:
- [ ] `compare x x == EQ`
- [ ] All four orderings (`LT`, `EQ`, `GT`, `LT`) returned correctly
- [ ] Implements either `compare` OR `<=` (don't need both unless you choose to)

## Pitfalls that specifically lose QC marks

### Pitfall: derived `Eq` does the wrong thing
```haskell
data Tree a = Empty | Node a (Tree a) (Tree a) deriving Eq
-- This makes Empty /= Node x Empty Empty (good, structural)
-- BUT: two BSTs with the same elements but different shapes are not equal.
-- For BST semantics, may need manual Eq:
instance Eq (Tree Int) where
  t1 == t2 = sort (flatten t1) == sort (flatten t2)
```

### Pitfall: `Show` instance breaks Read-Show round-trip
```haskell
-- WRONG: pretty Show that can't be parsed back
instance Show MyType where
  show x = "MyType { ... pretty ... }"
-- If marker tests `read . show == id`, this fails.
-- Fix: deriving Show, or write a Show that mirrors the constructor syntax.
```

### Pitfall: Monad instance where bind isn't structural
```haskell
-- WRONG: tries to flatten with `concat` but type doesn't allow
instance Monad MyContainer where
  return x = ...
  m >>= f = ... concat ... -- ??
-- If MyContainer has internal structure, bind needs to thread that structure.
-- See Free monad in Assignment 3 for the canonical pattern.
```

### Pitfall: `fmap` swaps subtrees
```haskell
-- WRONG: copy-pasted from mirror
instance Functor Tree where
  fmap f Empty = Empty
  fmap f (Node x l r) = Node (f x) (fmap f r) (fmap f l)   -- ← swapped l/r
-- This breaks fmap (f . g) == fmap f . fmap g because shape changes.
-- Fix: don't swap.
instance Functor Tree where
  fmap f Empty = Empty
  fmap f (Node x l r) = Node (f x) (fmap f l) (fmap f r)
```

### Pitfall: forgot Applicative is a superclass of Monad in GHC 9
```haskell
-- Modern GHC requires Applicative if you want Monad:
instance Monad MyType where ...
-- Compiler error: "No instance for (Applicative MyType)"
-- Fix:
instance Functor MyType where ...
instance Applicative MyType where
  pure = ...
  f <*> x = ...
instance Monad MyType where
  m >>= f = ...
```

### Pitfall: `return` and `pure` should be the same
```haskell
instance Applicative MyType where
  pure x = Pure x
instance Monad MyType where
  return x = Free [Pure x]   -- DIFFERENT from pure — bug!
-- Fix: either omit `return` (default is `pure`) or make them identical.
-- Best: don't define `return` in modern Haskell, just let it default to `pure`.
```

### Pitfall: lawful `Eq` but not `Ord`
```haskell
-- If you write `instance Ord Tree`, ALL three laws of Ord must hold.
-- The marker may test compare x x == EQ, antisymmetry, transitivity.
```

## See also

**Archetypes:** [A06 functor instance](../archetypes/A06-functor-instance.md) · [A22 typeclass instance](../archetypes/A22-typeclass-instance.md) · [A24 applicative instance](../archetypes/A24-applicative-instance.md)
**Question families:** [functor-instance](../question-families/functor-instance-family.md) · [applicative-monad-instance](../question-families/applicative-monad-instance-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
