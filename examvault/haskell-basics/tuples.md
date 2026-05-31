<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **tuples**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · **tuples** · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# tuples

## What this is
Anonymous heterogeneous product. `(a,b)`, `(a,b,c)`, etc.

## Mental model
A tuple's type IS its shape — `(Int, String)` is a different type from `(String, Int)`. Destructure with pattern match: `(x,y) = pair`.

## Syntax
```haskell
fst (x,y) = x
snd (x,y) = y
fst3 (x,_,_) = x
```

## Small examples
```haskell
>>> fst (1,"hi")            ==> 1
>>> let (a,b) = (3,4) in a+b   ==> 7
>>> zip [1,2,3] "abc"          ==> [(1,'a'),(2,'b'),(3,'c')]
```

## Exam use
Game-state archetypes (Nim) carry `(remaining, players)` as a State tuple. Codec/parser results are `(parsed, leftover)`.

## Common mistakes
- Treating tuples like records — large tuples are a code smell.
- `fst` / `snd` only work on pairs, not triples.

## See also
**Basics:** [pattern-matching](./pattern-matching.md) · [recursion](./recursion.md)
**Archetypes:** [A02 state game](../archetypes/A02-state-game.md) · [A16 parser combinators](../archetypes/A16-parser-combinators.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
