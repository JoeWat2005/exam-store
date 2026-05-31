<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Helper functions**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · **helper-functions** · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Helper functions

## What this is
Inner functions defined in `where` that carry extra state (accumulator, depth, environment) the top-level signature shouldn't expose.

## Mental model
When the public signature is `f :: T -> R` but you need to thread something extra through the recursion, introduce `go` (or `aux`) in `where` with the extra parameter. The public function calls `go t initial`.

## Syntax
```haskell
labelTree :: Tree a -> Tree (Int, a)
labelTree t = fst (go t 0)
  where
    go (Leaf x)   n = (Leaf (n,x), n+1)
    go (Branch l r) n = let (l', n')  = go l n
                            (r', n'') = go r n'
                        in (Branch l' r', n'')
```

## Small examples
```haskell
>>> -- counting with depth tracking
>>> let depth t = go t 0 where go Empty d = d; go (Fork _ l r) d = max (go l (d+1)) (go r (d+1))
>>> -- BFS-style with a queue
>>> let bfs t = go [t] where go [] = []; go (Empty:q) = go q; go (Fork x l r:q) = x : go (q++[l,r])
```

## Exam use
Every tree-labelling, every depth/path question, every codec round-trip uses helpers.

## Common mistakes
- Naming the helper the same as the outer function — infinite loop.
- Forgetting to thread the state through both recursive calls.

## See also
**Basics:** [where-clauses](./where-clauses.md) · [accumulator-recursion](./accumulator-recursion.md) · [local-definitions](./local-definitions.md)
**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A02 state game](../archetypes/A02-state-game.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
