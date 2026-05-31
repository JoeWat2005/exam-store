<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **foldr**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · **foldr** · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# foldr

## What this is
`foldr :: (a -> b -> b) -> b -> [a] -> b` — combine list elements right-to-left with a seed.

## Mental model
Replace every `(:)` with your function and every `[]` with the seed. `foldr f z [a,b,c]` = `f a (f b (f c z))`. Right-associative — natural for list-building combinators.

## Syntax
```haskell
foldr :: (a -> b -> b) -> b -> [a] -> b
foldr _ z []     = z
foldr f z (x:xs) = f x (foldr f z xs)
```

## Small examples
```haskell
>>> foldr (+) 0 [1,2,3]               ==> 6
>>> foldr (:) [] [1,2,3]              ==> [1,2,3]   -- identity
>>> foldr (\x acc -> if even x then x:acc else acc) [] [1..6]   ==> [2,4,6]
```

## Exam use
Archetype [A10 fold reformulation](../archetypes/A10-fold-reformulation.md) — rewrite explicit recursion as a `foldr`. Used everywhere lists are reduced to a single value or a new list.

## Common mistakes
- Use `foldr` when the step builds a (potentially infinite) list lazily; use `foldl'` for strict numeric reductions.
- Argument order: step function takes `element` then `accumulator`.

## See also
**Basics:** [foldl](./foldl.md) · [higher-order-functions](./higher-order-functions.md) · [recursion](./recursion.md)
**Typeclasses:** [Foldable](../typeclasses/foldable.md)
**Archetypes:** [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
