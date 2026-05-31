<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Recursion**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · **recursion** · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Recursion

## What this is
Solve a problem by reducing it to a smaller version of itself, plus a stopping rule.

## Mental model
Two equations: (1) base case — what to return at the smallest input; (2) recursive case — what to combine with the recursive result. Discipline: write the base case first.

## Syntax
```haskell
f base     = baseAnswer
f (x:xs)   = combine x (f xs)
-- or for trees
f Empty        = base
f (Fork x l r) = combine x (f l) (f r)
```

## Small examples
```haskell
>>> -- sum
>>> let s [] = 0; s (x:xs) = x + s xs in s [1..5]   ==> 15
>>> -- factorial
>>> let fact 0 = 1; fact n = n * fact (n-1) in fact 5   ==> 120
```

## Exam use
Every Q1 / Q5 of mock-style exams is recursion over an ADT. Get the equation skeleton down first, fill the right-hand side second.

## Common mistakes
- Missing base case ([P-005](../pitfalls/HIGH-severity.md#p-005)).
- Recursive call on the wrong sub-structure ([P-014](../pitfalls/HIGH-severity.md#p-014)).
- `n == 0` instead of `n <= 0` for numeric recursion ([P-008](../pitfalls/HIGH-severity.md#p-008)).

## See also
**Basics:** [pattern-matching](./pattern-matching.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [foldr](./foldr.md)
**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
