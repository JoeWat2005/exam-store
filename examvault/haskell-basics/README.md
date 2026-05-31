<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · **haskell-basics**

# haskell-basics

Cold-start refresher for Haskell fundamentals. If you've gone vague on a primitive, open the matching file here, refresh in <2 min, then go back to the archetype you were attacking.

Pages are intentionally short: 1 mental model, 1 syntax recap, 3 small examples, "exam use" pointer, common mistakes, and links to the deeper pages.

## Index

### Syntax
- [pattern-matching](./pattern-matching.md) — literal, constructor, wildcard, as-patterns
- [guards](./guards.md) — `|` predicate guards, `otherwise`
- [if-expressions](./if-expressions.md) — `if c then a else b`
- [let-in](./let-in.md) — local binding inside expression
- [where-clauses](./where-clauses.md) — local binding after expression
- [case-expressions](./case-expressions.md) — pattern match anywhere
- [tuples](./tuples.md) — pairs, triples, fst/snd
- [local-definitions](./local-definitions.md) — where vs let vs case

### Data
- [lists](./lists.md) — `[]`, `:`, list literal
- [strings](./strings.md) — `String = [Char]`, escapes
- [recursion](./recursion.md) — base case, recursive case, the discipline
- [accumulator-recursion](./accumulator-recursion.md) — `go acc xs` helper pattern
- [helper-functions](./helper-functions.md) — `where go` discovery technique
- [sorting](./sorting.md) — insertion / selection / bubble / quick / merge sorts (hand-rolled) + `isSorted` / permutation properties

### Comprehensions & HOFs
- [list-comprehensions](./list-comprehensions.md) — `[expr | gen, guard, let]`
- [higher-order-functions](./higher-order-functions.md) — functions that take/return functions
- [lambdas](./lambdas.md) — `\x -> ...`
- [function-composition](./function-composition.md) — `.`, `f . g`
- [currying](./currying.md) — `a -> b -> c` is `a -> (b -> c)`
- [partial-application](./partial-application.md) — supply some args, get a function

### Operators & sections
- [dollar-operator](./dollar-operator.md) — `f $ x` saves parentheses
- [dot-operator](./dot-operator.md) — `f . g`, sometimes `f . g . h`
- [sections](./sections.md) — `(+1)`, `(2*)`, `(`elem` xs)`

### Types
- [type-signatures](./type-signatures.md) — `f :: a -> b`, reading them
- [polymorphism](./polymorphism.md) — `a`, `b`, `Eq a =>`
- [algebraic-data-types](./algebraic-data-types.md) — `data X = A | B Int | C Y Y`
- [recursive-data-types](./recursive-data-types.md) — `data Tree a = Leaf | Node a (Tree a) (Tree a)`
- [deriving](./deriving.md) — `deriving (Eq, Show)` — what's free, what isn't

### Pre-monad effects
- [maybe-basics](./maybe-basics.md) — `data Maybe a = Nothing | Just a` intro (full ref: [`../monads/maybe.md`](../monads/maybe.md))
- [either-basics](./either-basics.md) — `data Either e a = Left e | Right a` intro (full ref: [`../monads/either.md`](../monads/either.md))
- [do-notation-basics](./do-notation-basics.md) — `do x <- m; return (f x)` desugar

### Standard HOFs
- [map](./map.md), [filter](./filter.md), [foldr](./foldr.md), [foldl](./foldl.md), [zip](./zip.md), [zipWith](./zipWith.md), [all-any](./all-any.md)

### Exam-day extras (added 2026-05-30)
- [safe-haskell](./safe-haskell.md) — what `{-# LANGUAGE Safe #-}` forbids and why
- [common-templates](./common-templates.md) — the 8 canonical patterns on one page; **most printable artefact in the vault**

### Testing & tools (added 2026-05-30 / 31)
- [testing-functions](./testing-functions.md) — pure functions, list-returning, HOFs, predicates, tuples
- [testing-recursive-functions](./testing-recursive-functions.md) — base + step + scale recipe
- [testing-monadic-functions](./testing-monadic-functions.md) — per-monad runner table
- [testing-tree-functions](./testing-tree-functions.md) — three-tier sample-tree categories
- [ghci-commands](./ghci-commands.md) — `:l`, `:r`, `:t`, `:i`, `:set +s`, multiline blocks
- [allowed-builtins](./allowed-builtins.md) — every Prelude / `Data.*` function permitted in the exam
- [ghc-error-decoder](./ghc-error-decoder.md) — **NEW** every common red-text error → translation → fix

## See also

**Archetypes:** see [`../archetypes/`](../archetypes/README.md) — every basics page links forward to the relevant archetype.
**Indexes:** [IF-YOU-SEE-X](../indexes/IF-YOU-SEE-X.md) · [KEYWORD-INDEX](../indexes/KEYWORD-INDEX.md)
**Pitfalls:** [HIGH severity](../pitfalls/HIGH-severity.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
