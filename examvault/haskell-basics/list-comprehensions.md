<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **List comprehensions**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** **list-comprehensions** · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# List comprehensions

## What this is
Generator + filter + expression syntax that desugars to `concatMap`.

## Mental model
`[ e | g, p, let b ]` — read as: for each binding from generator `g`, keep if predicate `p` holds, possibly let-bind `b`, evaluate `e`. Multiple generators iterate left-to-right (outer is leftmost).

## Syntax
```haskell
[ (x,y) | x <- [1..3], y <- [1..3], x /= y, let s = x+y ]
-- ==> [(1,2,3),(1,3,4),(2,1,3),(2,3,5),(3,1,4),(3,2,5)]
--     filtered out where x == y
```

## Small examples
```haskell
>>> [x*x | x <- [1..5], even x]            ==> [4,16]
>>> [(x,y) | x <- [1..3], y <- [x..3]]      ==> [(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]
>>> [c | c <- "Hello", c `notElem` "l"]      ==> "Heo"
```

## Exam use
Quicksort, Pythagorean triples, Cartesian product, factor lists, magic-square candidate generation — all of [A21 list-comp synthesis](../archetypes/A21-list-comp-synthesis.md).

## Common mistakes
- Forgetting that generators are NESTED loops, not parallel iteration.
- Reusing a variable name inside the comprehension shadows.

## See also
**Basics:** [higher-order-functions](./higher-order-functions.md) · [map](./map.md) · [filter](./filter.md)
**Archetypes:** [A21 list comp synthesis](../archetypes/A21-list-comp-synthesis.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
