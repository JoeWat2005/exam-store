<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Function composition**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · **function-composition** · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Function composition

## What this is
`(f . g) x = f (g x)` — apply `g` then `f`. Pronounce "after".

## Mental model
Composition lets you build pipelines without naming intermediates. Reads right-to-left, which is the opposite of pipe operators in other languages.

## Syntax
```haskell
(.) :: (b -> c) -> (a -> b) -> (a -> c)
(f . g) x = f (g x)
```

## Small examples
```haskell
>>> let shout = map toUpper . reverse
>>> shout "hello"                ==> "OLLEH"
>>> map (negate . (*2)) [1,2,3]  ==> [-2,-4,-6]
>>> -- point-free style
>>> let sumSquares = sum . map (^2)
```

## Exam use
Reformulating verbose lambdas into `f . g . h` is a common A10 fold-reformulation step. Also the parser-combinator style.

## Common mistakes
- Confusing `.` with `$` — `.` chains functions, `$` applies.
- Over-eager point-free can make code unreadable.

## See also
**Basics:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [higher-order-functions](./higher-order-functions.md)
**Archetypes:** [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
