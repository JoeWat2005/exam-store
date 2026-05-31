<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **foldl**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · **foldl** · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# foldl

## What this is
`foldl :: (b -> a -> b) -> b -> [a] -> b` — combine list elements left-to-right with a seed.

## Mental model
Left-associative: `foldl f z [a,b,c]` = `f (f (f z a) b) c`. For strict numeric accumulators, prefer `foldl'` from `Data.List` to avoid space leaks.

## Syntax
```haskell
foldl :: (b -> a -> b) -> b -> [a] -> b
foldl _ z []     = z
foldl f z (x:xs) = foldl f (f z x) xs

-- Prefer foldl' for numeric accumulation:
-- import Data.List (foldl')
```

## Small examples
```haskell
>>> foldl (+) 0 [1,2,3]               ==> 6
>>> foldl (\acc x -> x:acc) [] [1,2,3]    ==> [3,2,1]   -- reverses!
>>> foldl' (*) 1 [1..5]               ==> 120
```

## Exam use
Use when the seed needs to be the FIRST argument of the step function (e.g. building an accumulator with prepend). For sums/products on long lists use `foldl'`.

## Common mistakes
- Lazy `foldl` on long numeric lists → stack overflow. Use `foldl'`.
- Argument order: step takes `accumulator` then `element` (opposite of `foldr`).

## See also
**Basics:** [foldr](./foldr.md) · [accumulator-recursion](./accumulator-recursion.md)
**Archetypes:** [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
