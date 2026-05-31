<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **all / any**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · **all-any**
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# all / any

## What this is
`all :: (a -> Bool) -> [a] -> Bool` — every element satisfies. `any :: (a -> Bool) -> [a] -> Bool` — at least one does.

## Mental model
Both short-circuit. `all p []` is `True` (vacuous); `any p []` is `False`. Built on `foldr (&&)` and `foldr (||)`.

## Syntax
```haskell
all :: (a -> Bool) -> [a] -> Bool
all p = foldr (\x acc -> p x && acc) True

any :: (a -> Bool) -> [a] -> Bool
any p = foldr (\x acc -> p x || acc) False
```

## Small examples
```haskell
>>> all even [2,4,6]      ==> True
>>> all even [2,3,4]      ==> False
>>> any (> 10) [1,5,11]   ==> True
>>> all (== 0) []         ==> True   -- vacuous truth
```

## Exam use
Magic-square row/column checks, BST validation, predicate verification. The `all p children` pattern in `isNBranching`-style recursion.

## Common mistakes
- `all p []` returns `True` — often the right semantics (every child of a `Leaf` satisfies `p`).
- Using `all`/`any` where a fold with a guard would suffice (style).

## See also
**Basics:** [foldr](./foldr.md) · [higher-order-functions](./higher-order-functions.md)
**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A04 matrix predicate](../archetypes/A04-matrix-predicate.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
