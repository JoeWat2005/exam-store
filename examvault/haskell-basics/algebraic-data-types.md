<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Algebraic data types**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · **algebraic-data-types** · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Algebraic data types

## What this is
`data X = A | B Int | C Y String` — sum of products. Each constructor is independent; can carry zero or more typed fields.

## Mental model
A new type with explicit constructors. Pattern-match on the constructor to handle each case. The `data` keyword introduces a *new* type, distinct from its representation.

## Syntax
```haskell
data Color = Red | Green | Blue
data Shape = Circle Double | Rectangle Double Double

area :: Shape -> Double
area (Circle r)        = pi * r^2
area (Rectangle w h)   = w * h
```

## Small examples
```haskell
>>> area (Circle 2.0)        ==> 12.566...
>>> area (Rectangle 3.0 4.0)  ==> 12.0
>>> -- can derive Show, Eq automatically
>>> -- data X = ... deriving (Show, Eq)
```

## Exam use
Half of every exam — Mock Q1 (Rose tree), Q4 (Expression tree), Q5 (Circuit). The first move is always reading the constructors.

## Common mistakes
- Forgetting one constructor → non-exhaustive pattern warning + crash.
- Constructor and type with the same name (allowed; sometimes confuses).

## See also
**Basics:** [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md) · [pattern-matching](./pattern-matching.md)
**Archetypes:** [A05 ADT translation](../archetypes/A05-adt-translation.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
