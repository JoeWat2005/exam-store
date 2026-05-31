<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Recursive data types**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · **recursive-data-types** · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Recursive data types

## What this is
An ADT that mentions itself in one or more constructor fields.

## Mental model
Lists, trees, expression ASTs — all recursive ADTs. The recursion in the data definition mirrors the recursion in functions that consume it: one equation per constructor.

## Syntax
```haskell
data List a = Nil | Cons a (List a)
data BT a   = Empty | Fork a (BT a) (BT a)
data Rose a = Leaf a | Branch [Rose a]
```

## Small examples
```haskell
data BT a = Empty | Fork a (BT a) (BT a)

size :: BT a -> Int                       -- one equation per constructor
size Empty        = 0
size (Fork _ l r) = 1 + size l + size r

>>> size (Fork 1 (Fork 2 Empty Empty) (Fork 3 Empty Empty))   ==> 3
```

## Exam use
Every Q1 / Q5 of mock-style exams. Reading the data definition tells you the structure of your function.

## Common mistakes
- Missing base-case constructor → infinite type (won't typecheck).
- Recursive call on the WRONG sub-tree.

## See also
**Basics:** [algebraic-data-types](./algebraic-data-types.md) · [recursion](./recursion.md) · [pattern-matching](./pattern-matching.md)
**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A05 ADT translation](../archetypes/A05-adt-translation.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
