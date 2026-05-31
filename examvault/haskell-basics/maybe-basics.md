<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Maybe basics**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** **maybe-basics** · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Maybe basics

## What this is
`data Maybe a = Nothing | Just a` — a value of type `a` that might be absent.

## Mental model
Represents "computation that can fail without an error message". Pattern-match: `Just x` extracts; `Nothing` is the failure case. Full reference: [`../monads/maybe.md`](../monads/maybe.md).

## Syntax
```haskell
data Maybe a = Nothing | Just a

safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv x y = Just (x `div` y)
```

## Small examples
```haskell
>>> safeDiv 10 2            ==> Just 5
>>> safeDiv 10 0            ==> Nothing
>>> fromMaybe 0 (Just 5)    ==> 5
>>> fromMaybe 0 Nothing     ==> 0
```

## Exam use
Lookup functions (`lookup`, `find`), safe arithmetic, and parser results all return `Maybe`. Monadic chain via `do`-notation is in [`../monads/maybe.md`](../monads/maybe.md).

## Common mistakes
- `fromJust` crashes on `Nothing` — never use without a guard.
- Forgetting that `Just []` is a non-empty `Maybe` containing an empty list.

## See also
**Basics:** [either-basics](./either-basics.md) · [pattern-matching](./pattern-matching.md) · [do-notation-basics](./do-notation-basics.md)
**Theory:** [Maybe monad](../monads/maybe.md)
**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
