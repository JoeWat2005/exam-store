<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Accumulator recursion**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · **accumulator-recursion** · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Accumulator recursion

## What this is
Pass a running result as an extra argument; the helper recurses with the accumulator updated.

## Mental model
Lets you turn a structural recursion into a tail recursion: instead of building the answer on the way back UP, build it on the way DOWN. Common idiom: a `go` helper hidden in `where`.

## Syntax
```haskell
myReverse :: [a] -> [a]
myReverse xs = go xs []
  where
    go []     acc = acc
    go (x:xs) acc = go xs (x:acc)
```

## Small examples
```haskell
>>> myReverse [1,2,3]   ==> [3,2,1]
>>> -- foldl IS the accumulator pattern
>>> let sumAcc = foldl (+) 0
>>> sumAcc [1..100]    ==> 5050
```

## Exam use
Whenever the problem says "efficient", "linear time", "single pass" — use an accumulator with `go` or `foldl'`.

## Common mistakes
- `foldl` (not `foldl'`) on long lists → space leak. Use `foldl' (+) 0` with `Data.List`.
- Forgetting to reverse the accumulator at the end when order matters.

## See also
**Basics:** [recursion](./recursion.md) · [helper-functions](./helper-functions.md) · [foldl](./foldl.md)
**Archetypes:** [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
