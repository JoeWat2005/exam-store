<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Pattern matching**

<!-- siblings:start -->
> **Syntax:** **pattern-matching** · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Pattern matching

## What this is
Destructure data by matching against constructors, literals, or variables, picking one equation per shape.

## Mental model
Each equation matches in order top-to-bottom. The first one that matches wins. Variables bind; wildcards (`_`) discard.

## Syntax
```haskell
f Empty        = base
f (Fork x l r) = combine x (f l) (f r)
f 0       = baseInt
f (x:xs)  = ...
f _       = fallback
```

## Small examples
```haskell
>>> myLength []        ==> 0
>>> myLength [1,2,3]   ==> 3
>>> case Just 5 of { Just x -> x; Nothing -> 0 }   ==> 5
```

## Exam use
Every ADT / list / Maybe / Either question is solved by `f <Constructor> = ...` equations. Reading the constructors IS reading the algorithm.

## Common mistakes
- Missing base case → infinite loop ([P-005](../pitfalls/HIGH-severity.md#p-005)).
- Equations in wrong order — specific pattern after general one ([P-022](../pitfalls/HIGH-severity.md#p-022)).
- Non-exhaustive coverage with `-fwarn-incomplete-patterns` on ([P-017](../pitfalls/HIGH-severity.md#p-017)).

## See also
**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md)
**Basics:** [recursion](./recursion.md) · [guards](./guards.md) · [case-expressions](./case-expressions.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
