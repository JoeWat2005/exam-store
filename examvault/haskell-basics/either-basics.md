<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Either basics**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · **either-basics** · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Either basics

## What this is
`data Either e a = Left e | Right a` — success (`Right`) or failure with a message (`Left`).

## Mental model
Like `Maybe` but the failure carries information. Convention: `Right` is the success value, `Left` carries the error. Full reference: [`../monads/either.md`](../monads/either.md).

## Syntax
```haskell
data Either e a = Left e | Right a

safeDivE :: Int -> Int -> Either String Int
safeDivE _ 0 = Left "div by zero"
safeDivE x y = Right (x `div` y)
```

## Small examples
```haskell
>>> safeDivE 10 2     ==> Right 5
>>> safeDivE 10 0     ==> Left "div by zero"
>>> case safeDivE 10 0 of { Right n -> n; Left _ -> -1 }   ==> -1
```

## Exam use
Custom error types in interpreters (`Either EvalErr Value`). Used in Mock-style Q5 if the marker wants descriptive failure messages.

## Common mistakes
- Bias: `fmap` and Monad instances only touch the `Right` side. `Left e` is short-circuit.
- `Left` carries error, but the type variable `e` is on the LEFT in `Either e a` — easy to swap.

## See also
**Basics:** [maybe-basics](./maybe-basics.md) · [algebraic-data-types](./algebraic-data-types.md)
**Theory:** [Either monad](../monads/either.md) · [MonadError](../monads/monaderror.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
