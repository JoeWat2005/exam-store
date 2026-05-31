<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Deriving**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · **deriving**
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Deriving

## What this is
Auto-generate type-class instances: `data X = ... deriving (Eq, Ord, Show, Read)`.

## Mental model
GHC writes the boilerplate for you. Standard derivable classes: `Eq`, `Ord`, `Show`, `Read`, `Enum`, `Bounded` (some only for specific shapes).

## Syntax
```haskell
data Color = Red | Green | Blue deriving (Eq, Ord, Show, Read)
```

## Small examples
```haskell
>>> Red == Red             ==> True
>>> compare Red Blue       ==> LT
>>> show Green             ==> "Green"
>>> read "Red" :: Color    ==> Red
```

## Exam use
Useful for QuickCheck (`Eq` so the marker can compare; `Show` so it can print counterexamples). `deriving Functor` needs the `DeriveFunctor` pragma in your file; Safe permits it on modern GHC, but the course wants the instance written by hand and the template may not enable `DeriveFunctor` — so write the instance yourself — see [P-010](../pitfalls/HIGH-severity.md#p-010).

## Common mistakes
- `deriving Functor` needs the `DeriveFunctor` pragma in your file; Safe permits it on modern GHC, but the course wants the instance written by hand and the template may not enable `DeriveFunctor` — so write the instance yourself.
- Derived `Show` formats as code, not user-friendly — write your own if needed.

## See also
**Basics:** [algebraic-data-types](./algebraic-data-types.md)
**Typeclasses:** [Eq/Ord](../typeclasses/eq-ord.md) · [Show](../typeclasses/show.md)
**Pitfalls:** [P-010 deriving Functor](../pitfalls/HIGH-severity.md#p-010)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
