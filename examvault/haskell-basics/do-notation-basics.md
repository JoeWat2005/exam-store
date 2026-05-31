<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **do notation basics**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · **do-notation-basics**
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# do notation basics

## What this is
Syntactic sugar for monadic bind: `do x <- m; rest` desugars to `m >>= \x -> rest`.

## Mental model
Sequences monadic effects (Maybe, Either, State, IO, List). The `x <- m` extracts the value; `return x` (or `pure x`) wraps a pure value back in.

## Syntax
```haskell
do x <- Just 3
   y <- Just 4
   return (x + y)
-- ==> Just 7

do x <- Nothing  -- short-circuits
   y <- Just 4
   return (x + y)
-- ==> Nothing
```

Same shape in `Either` — `Left e` short-circuits and carries the error value:
```haskell
do x <- Right 3
   y <- Right 4
   return (x + y)        :: Either String Int
-- ==> Right 7

do x <- Right 3
   _ <- Left "boom"      -- short-circuits with this error
   y <- Right 4
   return (x + y)        :: Either String Int
-- ==> Left "boom"
```

## Small examples
```haskell
>>> do { x <- [1,2]; y <- [3,4]; return (x,y) }   ==> [(1,3),(1,4),(2,3),(2,4)]
>>> do { x <- Right 3; y <- Right 4; return (x+y) } :: Either String Int   ==> Right 7
>>> -- IO
>>> do { name <- getLine; putStrLn ("hi " ++ name) }
```

## Exam use
Every interpreter, every State-monad game, every parser, every multi-effect computation uses `do`-notation.

## Common mistakes
- Using `let x = ...` (no `<-`) for non-monadic binds inside `do`.
- Forgetting `return` at the end when the do-block must produce `m a`.
- Pattern bind `(Just x) <- m` relies on `MonadFail` — type-changes break it silently.

## See also
**Basics:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md)
**Theory:** [Monad typeclass](../typeclasses/monad.md) · [State monad](../monads/state.md)
**Archetypes:** [A03 generic monad](../archetypes/A03-generic-monad.md) · [A08 env eval](../archetypes/A08-env-eval.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
