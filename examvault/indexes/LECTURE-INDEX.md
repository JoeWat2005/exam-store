<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **LECTURE-INDEX**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · **LECTURE-INDEX** · [MASTER-INDEX](./MASTER-INDEX.md) · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# LECTURE-INDEX

Lecture file → vault files. When you flip to a lecture and want to know "which archetype does this drive?"

**Source:** `fp-learning-2025/files/LectureNotes/Sections/`

> Format: `lecture filename` · `topic` · `week` · `primary archetype` · `secondary archetypes` · `vault files that cover it` · `exam probability`.

---

## Week 1 — types, functions, patterns, guards

| Lecture | Topic | Wk | Primary | Secondary | Vault files | Prob. |
|---|---|---|---|---|---|---|
| `types.md` | types, currying, polymorphic intro | 1 | (support) | [A09](../archetypes/A09-prelude-reimpl.md) | [COURSE-MAP](../meta/COURSE-MAP.md), [TYPE-SIGNATURE-DATABASE](../indexes/TYPE-SIGNATURE-DATABASE.md) | ⭐⭐ |
| `functions.md` | pattern-matching, guards, lambdas | 1 | [A09](../archetypes/A09-prelude-reimpl.md) | [A01](../archetypes/A01-tree-recursion.md), [A05](../archetypes/A05-adt-translation.md), [A11](../archetypes/A11-bst-ops.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md), `pitfalls/` | ⭐⭐⭐⭐⭐ |
| `polymorphism.md` | parametric polymorphism | 2 | [A09](../archetypes/A09-prelude-reimpl.md) | [A03](../archetypes/A03-generic-monad.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md), [A03-generic-monad](../archetypes/A03-generic-monad.md) | ⭐⭐⭐ |

## Week 2 — lambdas, composition

| Lecture | Topic | Wk | Primary | Secondary | Vault files | Prob. |
|---|---|---|---|---|---|---|
| `functions.md` (lambdas §) | lambda exprs | 2 | (support) | [A10](../archetypes/A10-fold-reformulation.md), [A03](../archetypes/A03-generic-monad.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) | ⭐⭐⭐ |
| `higher-order_functions.md` (composition §) | function composition `.` | 2 / 5 | [A10](../archetypes/A10-fold-reformulation.md) | — | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) | ⭐⭐⭐ |

## Week 3 — recursion, accumulators

| Lecture | Topic | Wk | Primary | Secondary | Vault files | Prob. |
|---|---|---|---|---|---|---|
| `recursive_functions.md` | list recursion | 3 | [A09](../archetypes/A09-prelude-reimpl.md) | [A04](../archetypes/A04-matrix-predicate.md), [A10](../archetypes/A10-fold-reformulation.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | ⭐⭐⭐⭐⭐ |
| `Data1.md` (accumulators §) | tail recursion, fastReverse | 3 | [A09](../archetypes/A09-prelude-reimpl.md) | [A10](../archetypes/A10-fold-reformulation.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md), [foldl-vs-foldr](../pitfalls/HIGH-severity.md#p-023) | ⭐⭐⭐ |

## Week 4 — list comprehensions, typeclasses

| Lecture | Topic | Wk | Primary | Secondary | Vault files | Prob. |
|---|---|---|---|---|---|---|
| `list_comprehensions.md` | comprehensions, qualifiers | 4 | [A21](../archetypes/A21-list-comp-synthesis.md) | [A09](../archetypes/A09-prelude-reimpl.md), [A04](../archetypes/A04-matrix-predicate.md) | [A21-list-comp-synthesis](../archetypes/A21-list-comp-synthesis.md), [list-comp-family](../question-families/list-comp-family.md) | ⭐⭐⭐⭐ |
| `list_comprehensions.md` (Caesar §) | string-char Caesar | 4 | [A07](../archetypes/A07-codec-pair.md) | [A09](../archetypes/A09-prelude-reimpl.md), [A21](../archetypes/A21-list-comp-synthesis.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md), [codec-family](../question-families/codec-family.md) | ⭐⭐⭐ |
| `typeclasses.md` | basic typeclass, Eq/Ord | 4 | [A22](../archetypes/A22-typeclass-instance.md) | [A09](../archetypes/A09-prelude-reimpl.md) | `typeclasses/`, [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | ⭐⭐⭐⭐ |
| `more-typeclasses.md` | Num, Show extensions | 4 | [A22](../archetypes/A22-typeclass-instance.md) | [A13](../archetypes/A13-pretty-printer.md) | [num](../typeclasses/num.md), [show](../typeclasses/show.md) | ⭐⭐ |
| `even-more-typeclasses.md` | Foldable, Traversable | 6–7 | [A01](../archetypes/A01-tree-recursion.md) | [A10](../archetypes/A10-fold-reformulation.md) | [foldable](../typeclasses/foldable.md), [traversable](../typeclasses/traversable.md) | ⭐⭐ |

## Week 5 — higher-order functions, folds

| Lecture | Topic | Wk | Primary | Secondary | Vault files | Prob. |
|---|---|---|---|---|---|---|
| `higher-order_functions.md` | HOF, sections | 5 | [A03](../archetypes/A03-generic-monad.md) | [A10](../archetypes/A10-fold-reformulation.md), [A09](../archetypes/A09-prelude-reimpl.md), [A06](../archetypes/A06-functor-instance.md) | [A03-generic-monad](../archetypes/A03-generic-monad.md), [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) | ⭐⭐⭐⭐⭐ |
| `higher-order_functions.md` (folds §) | `foldr`/`foldl` | 5 | [A10](../archetypes/A10-fold-reformulation.md) | [A09](../archetypes/A09-prelude-reimpl.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md), [list-fold-family](../question-families/list-fold-family.md) | ⭐⭐⭐⭐ |

## Week 6 — custom data types, BT, BST, Rose, Maybe, Either

| Lecture | Topic | Wk | Primary | Secondary | Vault files | Prob. |
|---|---|---|---|---|---|---|
| `Data1.md` (ADT §) | data declarations | 6 | [A05](../archetypes/A05-adt-translation.md) | [A01](../archetypes/A01-tree-recursion.md), [A11](../archetypes/A11-bst-ops.md), [A22](../archetypes/A22-typeclass-instance.md) | [A05-adt-translation](../archetypes/A05-adt-translation.md), [binary-tree](../trees/binary-tree.md) | ⭐⭐⭐⭐⭐ |
| `Data1.md` (BT §) | binary trees | 6 | [A01](../archetypes/A01-tree-recursion.md) | [A06](../archetypes/A06-functor-instance.md), [A11](../archetypes/A11-bst-ops.md), [A20](../archetypes/A20-laws-iso.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md), [binary-tree](../trees/binary-tree.md) | ⭐⭐⭐⭐⭐ |
| `Data1.md` (Maybe §) | Maybe type ctor | 6 | [A03](../archetypes/A03-generic-monad.md) | [A09](../archetypes/A09-prelude-reimpl.md), [A06](../archetypes/A06-functor-instance.md), [A11](../archetypes/A11-bst-ops.md) | [maybe](../monads/maybe.md), [A03-generic-monad](../archetypes/A03-generic-monad.md) | ⭐⭐⭐⭐⭐ |
| `Data1.md` (Either §) | Either type ctor | 6 | [A06](../archetypes/A06-functor-instance.md) | [A09](../archetypes/A09-prelude-reimpl.md), [A14](../archetypes/A14-multi-effect-interp.md) | [either](../monads/either.md) | ⭐⭐⭐ |
| `Data2.md` (BST §) | binary search trees | 6 | [A11](../archetypes/A11-bst-ops.md) | [A01](../archetypes/A01-tree-recursion.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md), [bst](../trees/bst.md) | ⭐⭐⭐ |
| `Data2.md` (Rose §) | Rose trees | 6 / 10 | [A01](../archetypes/A01-tree-recursion.md) | [A05](../archetypes/A05-adt-translation.md), [A20](../archetypes/A20-laws-iso.md) | [rose-tree](../trees/rose-tree.md), [A01-tree-recursion](../archetypes/A01-tree-recursion.md) | ⭐⭐⭐⭐⭐ |
| `typeclasses.md` (deriving §) | deriving Eq/Ord/Show/Enum/Bounded | 6 / 4 | [A22](../archetypes/A22-typeclass-instance.md) | — | [README](../typeclasses/README.md) | ⭐⭐⭐ |

## Week 7 — expression trees, rigour, interpreters

| Lecture | Topic | Wk | Primary | Secondary | Vault files | Prob. |
|---|---|---|---|---|---|---|
| `Data2.md` (Expr §) | expression trees | 7 | [A05](../archetypes/A05-adt-translation.md) | [A13](../archetypes/A13-pretty-printer.md), [A19](../archetypes/A19-extend-interpreter.md), [A08](../archetypes/A08-env-eval.md) | [A05-adt-translation](../archetypes/A05-adt-translation.md), [expression-tree](../trees/expression-tree.md) | ⭐⭐⭐⭐⭐ |
| PS Week 7 | interpreter arith | 7 | [A08](../archetypes/A08-env-eval.md) | [A19](../archetypes/A19-extend-interpreter.md) | [simple-arith](../interpreters/simple-arith.md), [A08-env-eval](../archetypes/A08-env-eval.md) | ⭐⭐⭐ |
| PS Week 7 | env-interpreter (Let, Var) | 7 | [A08](../archetypes/A08-env-eval.md) | [A19](../archetypes/A19-extend-interpreter.md), [A14](../archetypes/A14-multi-effect-interp.md) | [A08-env-eval](../archetypes/A08-env-eval.md), [expr-reader](../interpreters/expr-reader.md) | ⭐⭐⭐⭐ |
| `rigour.md` | proofs, induction, monad laws | 7 | [A20](../archetypes/A20-laws-iso.md) | — | [A20-laws-iso](../archetypes/A20-laws-iso.md), [monad-laws](../monads/monad-laws.md) | ⭐⭐ |

## Week 8 — laziness, infinite data

| Lecture | Topic | Wk | Primary | Secondary | Vault files | Prob. |
|---|---|---|---|---|---|---|
| `Laziness.md` | laziness, fix, memoise | 8 | [A18](../archetypes/A18-lazy-memo.md) | [A20](../archetypes/A20-laws-iso.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md), [lazy-infinite-family](../question-families/lazy-infinite-family.md) | ⭐⭐⭐ |
| `Laziness.md` (infinite §) | infinite data, sieve | 8 | [A18](../archetypes/A18-lazy-memo.md) | — | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | ⭐⭐⭐ |
| `LazyNaturals.md` | Nat = Zero | Succ | 8 | [A18](../archetypes/A18-lazy-memo.md) | [A20](../archetypes/A20-laws-iso.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md), [strictness](../pitfalls/HIGH-severity.md#p-023) | ⭐⭐⭐ |

## Week 9 — monads

| Lecture | Topic | Wk | Primary | Secondary | Vault files | Prob. |
|---|---|---|---|---|---|---|
| `monads.md` (Functor §) | Functor / fmap | 7 / 9 | [A06](../archetypes/A06-functor-instance.md) | [A22](../archetypes/A22-typeclass-instance.md), [A20](../archetypes/A20-laws-iso.md) | [A06-functor-instance](../archetypes/A06-functor-instance.md), [functor](../typeclasses/functor.md) | ⭐⭐⭐⭐⭐ |
| `monads.md` (Applicative §) | Applicative / `<*>` | 9 / 10 | [A24](../archetypes/A24-applicative-instance.md) | [A06](../archetypes/A06-functor-instance.md), [A16](../archetypes/A16-parser-combinators.md) | [A24-applicative-instance](../archetypes/A24-applicative-instance.md), [applicative](../typeclasses/applicative.md) | ⭐⭐⭐⭐ |
| `monads.md` (Monad §) | Monad / `>>=` / do | 9 | [A03](../archetypes/A03-generic-monad.md) | [A06](../archetypes/A06-functor-instance.md), [A02](../archetypes/A02-state-game.md), [A14](../archetypes/A14-multi-effect-interp.md), [A15](../archetypes/A15-writer-trace.md) | [A03-generic-monad](../archetypes/A03-generic-monad.md), `monads/` | ⭐⭐⭐⭐⭐ |
| `monads.md` (State §) | State monad | 9 | [A02](../archetypes/A02-state-game.md) | [A03](../archetypes/A03-generic-monad.md), [A23](../archetypes/A23-mini-game.md), [A14](../archetypes/A14-multi-effect-interp.md) | [A02-state-game](../archetypes/A02-state-game.md), [state](../monads/state.md) | ⭐⭐⭐⭐⭐ |
| `monads.md` (Writer §) | Writer monad | 9 | [A15](../archetypes/A15-writer-trace.md) | [A14](../archetypes/A14-multi-effect-interp.md) | [A15-writer-trace](../archetypes/A15-writer-trace.md), [writer](../monads/writer.md) | ⭐⭐⭐ |
| `monads.md` (Reader §) | Reader monad | 9–10 | [A06](../archetypes/A06-functor-instance.md) | [A08](../archetypes/A08-env-eval.md) | [reader](../monads/reader.md) | ⭐⭐ |
| `monads.md` (List monad §) | list non-determinism | 9 | [A21](../archetypes/A21-list-comp-synthesis.md) | [A03](../archetypes/A03-generic-monad.md) | [list-monad](../monads/list-monad.md), [A21-list-comp-synthesis](../archetypes/A21-list-comp-synthesis.md) | ⭐⭐⭐ |
| `monads.md` (mapM/traverse §) | Traversable | 9 | [A03](../archetypes/A03-generic-monad.md) | [A06](../archetypes/A06-functor-instance.md) | [traversable](../typeclasses/traversable.md), [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md) | ⭐⭐ |
| PS Week 9 calculator | MonadError, calculator with /0 | 9 | [A14](../archetypes/A14-multi-effect-interp.md) | [A08](../archetypes/A08-env-eval.md) | [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md), [expr-state-either](../interpreters/expr-state-either.md) | ⭐⭐⭐ |
| `IOPrime.md` | IO modelling | 9–10 | [A03](../archetypes/A03-generic-monad.md) | — | [io](../monads/io.md) | ⭐⭐ |

## Week 10 — parser, multi-effect, interpreter project

| Lecture | Topic | Wk | Primary | Secondary | Vault files | Prob. |
|---|---|---|---|---|---|---|
| `monads.md` (parser §) | parser combinators | 10 | [A16](../archetypes/A16-parser-combinators.md) | [A24](../archetypes/A24-applicative-instance.md), [A06](../archetypes/A06-functor-instance.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md), [alternative](../typeclasses/alternative.md) | ⭐⭐⭐ |
| `monads.md` (Alternative §) | Alternative class | 10 | [A16](../archetypes/A16-parser-combinators.md) | [A24](../archetypes/A24-applicative-instance.md) | [alternative](../typeclasses/alternative.md) | ⭐⭐⭐ |
| `monads.md` (transformers §) | StateT etc. | 10 | [A14](../archetypes/A14-multi-effect-interp.md) | [A03](../archetypes/A03-generic-monad.md) | [transformers](../monads/transformers.md) | ⭐⭐ |
| Assignment 3 (Free §) | Free monad | 10 | [A14](../archetypes/A14-multi-effect-interp.md) | [A20](../archetypes/A20-laws-iso.md), [A05](../archetypes/A05-adt-translation.md) | [multi-effect](../monads/multi-effect.md), [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md) | ⭐⭐⭐ |
| [Overview](../../fp-learning-2025/files/LectureNotes/Sections/interpreter/Overview.md) | imperative interpreter | 10 | [A19](../archetypes/A19-extend-interpreter.md) | [A14](../archetypes/A14-multi-effect-interp.md), [A08](../archetypes/A08-env-eval.md) | [A19-extend-interpreter](../archetypes/A19-extend-interpreter.md), [imperative-eval](../interpreters/imperative-eval.md) | ⭐⭐⭐ |
| [AbstractSyntax](../../fp-learning-2025/files/LectureNotes/Sections/interpreter/AbstractSyntax.md) | AST design | 10 | [A19](../archetypes/A19-extend-interpreter.md) | [A05](../archetypes/A05-adt-translation.md) | [imperative-eval](../interpreters/imperative-eval.md) | ⭐⭐ |
| [Interpreter](../../fp-learning-2025/files/LectureNotes/Sections/interpreter/Interpreter.md) | run :: Program -> Storage -> Storage | 10 | [A19](../archetypes/A19-extend-interpreter.md) | [A14](../archetypes/A14-multi-effect-interp.md) | [imperative-eval](../interpreters/imperative-eval.md) | ⭐⭐⭐ |
| `interpreter/Parser.hs` | parser stage | 10 | [A16](../archetypes/A16-parser-combinators.md) | — | [parser-overview](../interpreters/parser-overview.md) | ⭐⭐ |
| [Runxy](../../fp-learning-2025/files/LectureNotes/Sections/interpreter/Runxy.md) | CLI integration | 10 | — | [A19](../archetypes/A19-extend-interpreter.md) | [extend-interpreter](../interpreters/extend-interpreter.md) | ⭐ |

## Week 11 — game programming, Life, tictactoe

| Lecture | Topic | Wk | Primary | Secondary | Vault files | Prob. |
|---|---|---|---|---|---|---|
| `tictactoe.md` | game logic, grid | 11 | [A23](../archetypes/A23-mini-game.md) | [A21](../archetypes/A21-list-comp-synthesis.md) | [A23-mini-game](../archetypes/A23-mini-game.md) | ⭐⭐ |
| `Life.md` | Conway's Game of Life | 2 / 11 | [A23](../archetypes/A23-mini-game.md) | [A21](../archetypes/A21-list-comp-synthesis.md) | [A23-mini-game](../archetypes/A23-mini-game.md) | ⭐ |
| PS Week 11 lose-three-in-row | TTT variants | 11 | [A23](../archetypes/A23-mini-game.md) | [A21](../archetypes/A21-list-comp-synthesis.md) | [A23-mini-game](../archetypes/A23-mini-game.md) | ⭐⭐ |

---

## Lectures by exam priority (highest to lowest)

⭐⭐⭐⭐⭐ — almost certainly tested:
- `functions.md` pattern matching
- `recursive_functions.md` list recursion
- `higher-order_functions.md` HOF + folds
- `Data1.md` ADT § + BT § + Maybe §
- `Data2.md` Rose § + Expr §
- `monads.md` Functor / Monad / State sections

⭐⭐⭐⭐ — very likely:
- `list_comprehensions.md`
- `Data2.md` BST §
- `monads.md` Applicative / Writer / MonadError sections
- PS Week 7 / 9 (interpreter + monadic calculator)

⭐⭐⭐ — possible:
- `Laziness.md` + `LazyNaturals.md`
- Parser combinators (`monads.md` parser §)
- `interpreter/` Overview + Interpreter
- PS Week 11 TTT
- `rigour.md` (proofs)

⭐⭐ — low probability:
- `IOPrime.md`
- `Life.md`
- `even-more-typeclasses.md` Foldable / Traversable specifically

---

## Quick-jump: lecture → archetype

| Lecture | Archetypes drive it |
|---|---|
| `Data1.md` BT | [A01](../archetypes/A01-tree-recursion.md) |
| `Data2.md` Rose | [A01](../archetypes/A01-tree-recursion.md) |
| `Data2.md` Expr | [A05](../archetypes/A05-adt-translation.md), [A08](../archetypes/A08-env-eval.md) |
| `Data2.md` BST | [A11](../archetypes/A11-bst-ops.md) |
| `monads.md` State | [A02](../archetypes/A02-state-game.md) |
| `monads.md` Writer | [A15](../archetypes/A15-writer-trace.md) |
| `monads.md` Reader | [A06](../archetypes/A06-functor-instance.md) / [A08](../archetypes/A08-env-eval.md) |
| `monads.md` Functor | [A06](../archetypes/A06-functor-instance.md) |
| `monads.md` Applicative | [A24](../archetypes/A24-applicative-instance.md) |
| `monads.md` Monad | [A03](../archetypes/A03-generic-monad.md) |
| `monads.md` parser | [A16](../archetypes/A16-parser-combinators.md) |
| `monads.md` List | [A21](../archetypes/A21-list-comp-synthesis.md) |
| PS Week 9 calculator | [A14](../archetypes/A14-multi-effect-interp.md) |
| `Laziness.md` | [A18](../archetypes/A18-lazy-memo.md) |
| `LazyNaturals.md` | [A18](../archetypes/A18-lazy-memo.md) |
| `tictactoe.md` | [A23](../archetypes/A23-mini-game.md) |
| `Life.md` | [A23](../archetypes/A23-mini-game.md) |
| `list_comprehensions.md` | [A21](../archetypes/A21-list-comp-synthesis.md) |
| `rigour.md` | [A20](../archetypes/A20-laws-iso.md) |
| `interpreter/` | [A19](../archetypes/A19-extend-interpreter.md) |
| Assignment 3 Free | [A14](../archetypes/A14-multi-effect-interp.md) |

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
