<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **case expressions**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · **case-expressions** · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# case expressions

## What this is
Pattern match in expression position. Same as multiple equations, but inline.

## Mental model
`case scrutinee of { pat1 -> e1; pat2 -> e2; ... }` is the primitive form; multi-equation functions desugar to it. Use it when you can't (or won't) introduce a new top-level function.

## Syntax
```haskell
case x of
  Nothing -> 0
  Just n  -> n * 2
```

## Small examples
```haskell
>>> case 'a' of { 'a' -> 1; _ -> 0 }   ==> 1
>>> map (\m -> case m of Just n -> n; Nothing -> 0) [Just 1, Nothing]   ==> [1,0]
>>> case lookup 'x' [('a',1),('x',5)] of { Just v -> v; _ -> -1 }   ==> 5
```

## Exam use
Useful inside `do`-blocks or `where`-helpers when you need to branch on a constructor without writing a separate equation.

## Common mistakes
- Forgetting `otherwise`-equivalent (wildcard `_`) → non-exhaustive.
- Trying to write guards inside `case` — use `case x of { p | g -> e; ... }`.

## See also
**Basics:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md)
**Archetypes:** [A03 generic monad](../archetypes/A03-generic-monad.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
