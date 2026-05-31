<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Higher-order functions**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · **higher-order-functions** · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Higher-order functions

## What this is
Functions that take or return other functions.

## Mental model
Haskell functions are first-class values. `map`, `filter`, `foldr` are the canonical examples — each takes a function as one of its arguments and applies it across a structure.

## Syntax
```haskell
twice :: (a -> a) -> a -> a
twice f x = f (f x)

flip :: (a -> b -> c) -> b -> a -> c
flip f y x = f x y
```

## Small examples
```haskell
>>> twice (+3) 4         ==> 10
>>> map (+1) [1,2,3]     ==> [2,3,4]
>>> filter odd [1..10]   ==> [1,3,5,7,9]
>>> foldr (+) 0 [1..5]   ==> 15
```

## Exam use
Every Day-5 problem. Plus archetype [A10 fold reformulation](../archetypes/A10-fold-reformulation.md) which IS "rewrite this recursive function as a higher-order fold".

## Common mistakes
- Reading `a -> b -> c` as "takes two args and returns c" — actually `a -> (b -> c)` (curried).
- Sectioning ambiguity: `(- 3)` is negative three, not subtract-three; use `subtract 3`.

## See also
**Basics:** [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
**Archetypes:** [A10 fold reformulation](../archetypes/A10-fold-reformulation.md) · [A03 generic monad](../archetypes/A03-generic-monad.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
