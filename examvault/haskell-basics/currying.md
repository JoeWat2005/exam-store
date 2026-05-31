<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Currying**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · **currying** · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Currying

## What this is
Multi-argument functions are actually nested single-argument functions: `f :: a -> b -> c` is `f :: a -> (b -> c)`.

## Mental model
`add 1 2` is `(add 1) 2`. Currying enables partial application: `add 1` is a function waiting for the second argument.

## Syntax
```haskell
add :: Int -> Int -> Int
add x y = x + y

-- same as:
add' :: Int -> (Int -> Int)
add' x = \y -> x + y
```

## Small examples
```haskell
>>> let inc = (+) 1
>>> inc 5             ==> 6
>>> map (+10) [1,2,3] ==> [11,12,13]
>>> -- flip swaps argument order
>>> let subFromTen = flip (-) 10
>>> subFromTen 25     ==> 15
```

## Exam use
Used implicitly all the time: every `map (f x)` partially-applies `f`. Explicit `flip`/`curry`/`uncurry` shows up in HOF reformulations.

## Common mistakes
- `curry`/`uncurry` confusion: `curry :: ((a,b) -> c) -> (a -> b -> c)`, `uncurry` the inverse.
- Operator sections look like partial applications and they are.

## See also
**Basics:** [partial-application](./partial-application.md) · [higher-order-functions](./higher-order-functions.md) · [sections](./sections.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
