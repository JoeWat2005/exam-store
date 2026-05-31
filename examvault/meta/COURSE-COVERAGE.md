<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [meta](./README.md) · **COURSE-COVERAGE — lecture → archetype mapping**

<!-- siblings:start -->
> **Peers:** **COURSE-COVERAGE** · [COURSE-MAP](./COURSE-MAP.md) · [FINAL-SWEEP-REPORT](./FINAL-SWEEP-REPORT.md) · [GAP-AUDIT](./GAP-AUDIT.md) · [SCRIPT-COMPATIBILITY-REPORT](./SCRIPT-COMPATIBILITY-REPORT.md) · [VAULT-AUDIT](./VAULT-AUDIT.md) · [WIKI-UPGRADE-REPORT](./WIKI-UPGRADE-REPORT.md)
<!-- siblings:end -->






# COURSE-COVERAGE — lecture → archetype mapping

Every row maps **one lecture topic** to the archetype(s) under which it is *most likely* to appear in an exam question. Use this when you flip to a slide and want to know which archetype file to revise.

Probability is repeated from `COURSE-MAP.md`. **Primary archetype** is the dominant question shape for that topic; **Secondary** are mutations or cross-topic combinations.

Vault file paths assume the directory layout in `examvault/`:
- `archetypes/A##-*.md` — one file per archetype
- `monads/`, `trees/`, `typeclasses/`, `interpreters/`, `cross-matrix/` — topic-aligned reference files
- `pitfalls/` — common-mistake compilations
- `question-families/` — mutation enumerations

The "Linked Vault Files" column lists files that *should* be created by downstream subagents (Tree Specialist, Monad Specialist, etc.). Where a path is listed but the file doesn't yet exist, that is expected — this column is the contract for what other subagents must produce.

---

## Lecture → archetype table

| Lecture | Week | Topic slug | Primary archetype | Secondary archetypes | Exam prob. | Linked vault files |
|---------|:----:|------------|:-----------------:|----------------------|:----------:|--------------------|
| `types.md` | 1 | types | (support only) | A09 | ⭐⭐ | [TYPE-SIGNATURE-DATABASE](../indexes/TYPE-SIGNATURE-DATABASE.md) |
| `functions.md` (pattern match) | 1 | pattern-matching | A09 | A01, A05, A11 | ⭐⭐⭐⭐⭐ | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md), [non-exhaustive](../pitfalls/HIGH-severity.md#p-017) |
| `functions.md` (guards) | 1 | guards | A09 | A21 | ⭐⭐⭐ | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) |
| `polymorphism.md` | 2 | polymorphism | A09 | A03 | ⭐⭐⭐ | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md), [A03-generic-monad](../archetypes/A03-generic-monad.md) |
| `recursive_functions.md` | 3 | list-recursion | A09 | A04, A10 | ⭐⭐⭐⭐⭐ | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md), [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) |
| `Data1.md` (accumulators §) | 3 | accumulators | A09 | A10 | ⭐⭐⭐ | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md), [foldl-vs-foldr](../pitfalls/HIGH-severity.md#p-023) |
| `list_comprehensions.md` | 4 | list-comprehensions | A21 | A09, A04 | ⭐⭐⭐⭐ | [A21-comprehension-synthesis](../archetypes/A21-list-comp-synthesis.md), [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) |
| `higher-order_functions.md` | 5 | higher-order-functions | A03 | A10, A09, A06 | ⭐⭐⭐⭐⭐ | [A03-generic-monad](../archetypes/A03-generic-monad.md), [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) |
| `higher-order_functions.md` (folds §) | 5 | folds | A10 | A09 | ⭐⭐⭐⭐ | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) |
| `types.md` / `functions.md` (curry §) | 1–2 | currying | (support) | A03, A06 | ⭐⭐ | [TYPE-SIGNATURE-DATABASE](../indexes/TYPE-SIGNATURE-DATABASE.md) |
| `functions.md` (lambdas §) | 2 | lambdas | (support) | A10, A03 | ⭐⭐⭐ | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) |
| `higher-order_functions.md` (compose §) | 2 / 5 | function-composition | A10 | — | ⭐⭐⭐ | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) |
| `list_comprehensions.md` (Caesar §) | 4 | string-char | A07 | A09, A21 | ⭐⭐⭐ | [A07-codec-pair](../archetypes/A07-codec-pair.md), [string-cipher](../question-families/codec-family.md) |
| `Data1.md` (ADTs §) | 6 | custom-ADTs | A05 | A01, A11, A22 | ⭐⭐⭐⭐⭐ | [A05-adt-to-adt](../archetypes/A05-adt-translation.md), [binary-trees](../trees/binary-tree.md) |
| `typeclasses.md` (deriving §) | 6 | deriving | A22 | — | ⭐⭐⭐ | [deriving](../typeclasses/README.md) |
| `typeclasses.md`, `more-typeclasses.md` | 4 | typeclasses-basic | A22 | A09 | ⭐⭐⭐⭐ | [basic](../typeclasses/README.md), [A22-instance-for-adt](../archetypes/A22-typeclass-instance.md) |
| `monads.md` (Functor §) | 7 / 9 | Functor | A06 | A22, A20 | ⭐⭐⭐⭐⭐ | [A06-fam-instance](../archetypes/A06-functor-instance.md), [functor](../typeclasses/functor.md) |
| `monads.md` (Applicative §) | 9 / 10 | Applicative | A24 | A06, A16 | ⭐⭐⭐⭐ | [A24-applicative-instance](../archetypes/A24-applicative-instance.md), [applicative](../typeclasses/applicative.md) |
| `monads.md` (Monad §) | 9 | Monad | A03 | A06, A02, A14, A15 | ⭐⭐⭐⭐⭐ | [A03-generic-monad](../archetypes/A03-generic-monad.md), [README](../monads/README.md) |
| `even-more-typeclasses.md` (Foldable) | 6–7 | Foldable | A01 | A10 | ⭐⭐ | [foldable](../typeclasses/foldable.md), [A01-tree-structural-rec](../archetypes/A01-tree-recursion.md) |
| `monads.md` (mapM / traverse §) | 9 | Traversable | A03 | A06 | ⭐⭐ | [traversable](../typeclasses/traversable.md), [tree-x-monad](../cross-matrix/tree-x-generic-monad.md) |
| `monads.md` (parser §, Alternative) | 10 | Alternative | A16 | A24 | ⭐⭐⭐ | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) |
| `typeclasses.md` | 4 | Eq-Ord | A22 | A11 | ⭐⭐⭐ | [eq-ord](../typeclasses/eq-ord.md) |
| `Data2.md`, PS Week 7 | 4 / 7 | Show | A13 | A22 | ⭐⭐⭐⭐ | [A13-show-pretty-printer](../archetypes/A13-pretty-printer.md) |
| `more-typeclasses.md`, `even-more-typeclasses.md` | 4 | Num | A22 | A13 | ⭐⭐ | [num](../typeclasses/num.md) |
| `Data1.md` (Maybe §), `monads.md` | 6 / 9 | Maybe | A03 | A09, A06, A11 | ⭐⭐⭐⭐⭐ | [maybe](../monads/maybe.md), [A03-generic-monad](../archetypes/A03-generic-monad.md) |
| `Data1.md` (Either §) | 6 | Either | A06 | A09, A14 | ⭐⭐⭐ | [either](../monads/either.md) |
| `IOPrime.md` | 9–10 | IO | A03 | — | ⭐⭐ | [io](../monads/io.md) |
| `monads.md` (State §) | 9 | State | A02 | A03, A23, A14 | ⭐⭐⭐⭐⭐ | [A02-state-mini-game](../archetypes/A02-state-game.md), [state](../monads/state.md) |
| `monads.md` (Writer §) | 9 | Writer | A15 | A14 | ⭐⭐⭐ | [A15-writer-trace](../archetypes/A15-writer-trace.md), [writer](../monads/writer.md) |
| `monads.md` (Reader §) | 9–10 | Reader | A06 | A08 | ⭐⭐ | [reader](../monads/reader.md) |
| `monads.md` (List monad §) | 9 | List-monad | A21 | A03 | ⭐⭐⭐ | [list](../monads/list-monad.md), [A21-comprehension-synthesis](../archetypes/A21-list-comp-synthesis.md) |
| PS Week 9 calculator | 9 | MonadError | A14 | A08 | ⭐⭐⭐ | [monad-x-error](../cross-matrix/tree-x-either.md), [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md) |
| `monads.md`, Assignment 3 (`StateT`, `Free`) | 10 | monad-transformers | A14 | A03 | ⭐⭐ | [transformers](../monads/transformers.md) |
| Assignment 3 (`Free (FSum ...)`) | 10 | multi-effect | A14 | A02, A23 | ⭐⭐⭐ | [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md), [free](../monads/multi-effect.md) |
| `Data2.md` (expression trees §), PS Week 7 | 7 | expression-trees | A05 | A13, A19, A08 | ⭐⭐⭐⭐⭐ | [A05-adt-to-adt](../archetypes/A05-adt-translation.md), [expr](../interpreters/simple-arith.md) |
| `Data2.md` (BST §) | 6 | BST | A11 | A01 | ⭐⭐⭐ | [A11-bst-ops](../archetypes/A11-bst-ops.md), [bst](../trees/bst.md) |
| `Data2.md` (Rose §), MockTest Q1, Assignment 3 T1 | 6 / 10 | rose-trees | A01 | A05, A20 | ⭐⭐⭐⭐⭐ | [A01-tree-structural-rec](../archetypes/A01-tree-recursion.md), [rose](../trees/rose-tree.md) |
| `Data1.md` (BT §) | 6 | binary-trees | A01 | A06, A11, A20 | ⭐⭐⭐⭐⭐ | [A01-tree-structural-rec](../archetypes/A01-tree-recursion.md), [binary-trees](../trees/binary-tree.md) |
| `Data2.md`, PS Week 7 | 7 | interpreter-arith | A08 | A19 | ⭐⭐⭐ | [arith](../interpreters/simple-arith.md), [A08-env-evaluator](../archetypes/A08-env-eval.md) |
| PS Week 7 / 9 (env + Let) | 7 / 9 | interpreter-with-env | A08 | A19, A14 | ⭐⭐⭐⭐ | [A08-env-evaluator](../archetypes/A08-env-eval.md), [env](../interpreters/expr-reader.md) |
| PS Week 9 monadic calculator | 7 / 9 | interpreter-with-error | A14 | A08, A19 | ⭐⭐⭐⭐ | [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md), [error](../interpreters/expr-either.md) |
| `Sections/interpreter/` (xy language) | 10 | interpreter-imperative-storage | A19 | A14, A08 | ⭐⭐⭐ | [A19-extend-interpreter](../archetypes/A19-extend-interpreter.md), [imperative](../interpreters/imperative-eval.md) |
| `monads.md` (parser §), `interpreter/Parser.hs` | 10 | parser-combinators | A16 | A24, A06 | ⭐⭐⭐ | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) |
| `Laziness.md` | 8 | laziness | A18 | A20 | ⭐⭐⭐ | [A18-lazy-memoisation](../archetypes/A18-lazy-memo.md) |
| `Laziness.md` (infinite §) | 8 | infinite-data | A18 | — | ⭐⭐⭐ | [A18-lazy-memoisation](../archetypes/A18-lazy-memo.md) |
| `LazyNaturals.md` | 8 | lazy-naturals | A18 | A20 | ⭐⭐⭐ | [A18-lazy-memoisation](../archetypes/A18-lazy-memo.md), [strictness](../pitfalls/HIGH-severity.md#p-023) |
| `Life.md` | 2 / 11 | conway-life | A23 | A21 | ⭐ | [A23-mini-game](../archetypes/A23-mini-game.md) |
| `tictactoe.md`, PS Week 11 | 11 | tic-tac-toe | A23 | A21 | ⭐⭐ | [A23-mini-game](../archetypes/A23-mini-game.md) |
| `rigour.md` | 7 | rigour | A20 | — | ⭐⭐ | [A20-laws-iso-retract](../archetypes/A20-laws-iso.md), [laws](../monads/monad-laws.md) |
| `monads.md`, Assignment 3 | 10 | Free-monad | A14 | A20, A05 | ⭐⭐⭐ | [free](../monads/multi-effect.md), [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md) |

---

## Archetype × topic reverse index

For each archetype, the lectures most likely to spawn that question shape. Use this when an archetype is given (e.g. the exam paper shows a `Monad m =>` signature → A03) and you need to recall *which lecture* taught the kit.

| Archetype | Lectures that drive it |
|-----------|-------------------------|
| A01 Tree-ADT structural recursion | `Data1.md` BT, `Data2.md` Rose / BST, expression-trees |
| A02 State-monad mini-game | `monads.md` State, MockTest Q3, PS Week 9 |
| A03 Generic `Monad m =>` combinator | `monads.md`, MockTest Q2, problem 109 / 128 / 129 / 130 |
| A04 Matrix predicate (transpose) | `list_comprehensions.md`, MockTest Q4, problem 141 |
| A05 ADT-to-ADT translation | `Data2.md` expression-trees, MockTest Q5 (Expr→Circuit), Assignment 2 Ex 4–5 |
| A06 Functor/Applicative/Monad instance | `monads.md`, `even-more-typeclasses.md`, problems 121–126 |
| A07 Codec pair (encode/decode) | `list_comprehensions.md` Caesar, Assignment 2 (Morse), problem 147 (RLE) |
| A08 Environment evaluator | `Data2.md` expression-trees, PS Week 7, PS Week 9, problem 148 |
| A09 Prelude reimplementation | `recursive_functions.md`, `higher-order_functions.md`, problems 11–50 |
| A10 Fold reformulation | `higher-order_functions.md`, problems 41–50 |
| A11 BST operations | `Data2.md` BSTs, PS Week 6, problems 81–85 |
| A12 Representation conversion | `Data2.md` (lists / trees), Assignment 2 ramify/tabulate (also fits A05) |
| A13 Custom Show pretty-printer | `Data2.md`, PS Week 7, Assignment 1 (Grid Show with ANSI) |
| A14 Multi-effect interpreter | PS Week 9 calculator, Assignment 3 Tasks 2–4, problem 149 |
| A15 Writer trace | `monads.md` Writer, problems 107–108, Assignment 3 Task 2 |
| A16 Parser combinators | `monads.md` parsing §, problem 138–140, `interpreter/Parser.hs` |
| A17 Zipper navigation | Assignment 1 (`GridWithAPointer`), `Data2.md` directions/addresses |
| A18 Lazy memoisation | `Laziness.md`, PS Week 8 (`tstore`/`tfetch`), problem 136 |
| A19 Extend an interpreter | `Sections/interpreter/` xy language, PS Week 10, PS Week 7 |
| A20 Laws / iso / retract | `rigour.md`, Assignment 2 Ex 5 (`tabulate`/`ramify` retract), Assignment 3 Task 1 (`Rose ≅ Free [] a`) |
| A21 List comprehension synthesis | `list_comprehensions.md`, MockTest Q4 (diagonals), tic-tac-toe rows/cols, knightMoves |
| A22 Typeclass instance for ADT | `typeclasses.md`, `even-more-typeclasses.md`, problems 69, 121–126 |
| A23 Mini-game (Nim, TTT, Conway) | `tictactoe.md`, `Life.md`, MockTest Q3 (Nim), problem 144 / 150 |
| A24 Applicative instance | `monads.md` parsing §, problem 127, parser type |

---

## Coverage gaps

Lecture topics that are **not** well covered by the A01–A24 archetype set. These are candidates for either new archetypes or for the Archetype Analyst subagent to expand.

| Gap | Why it doesn't fit existing archetypes | Suggested resolution |
|-----|----------------------------------------|-----------------------|
| **`IOPrime.md` modelling exercise** (build your own `IO'` monad with primitive effects, `interact'`, `pipe`) | A03 covers `Monad m =>` usage but not the *construction* of an effect monad as data; A14 is closer but assumes Free + State | **RESOLVED → [monads/io.md § "Modelling IO as data (`IO'`)"](../monads/io.md#modelling-io-as-data-io-from-the-ioprime-lecture)**. The `IO'` data type + Functor/Applicative/Monad instances + `putChar'`/`getChar'`/`getLine'`/`pipe`/`interact'`/`translate` are reproduced there (compile-verified). Folded under A14 as the free-style effect-monad seed; no separate archetype needed. Low exam priority (⭐). |
| **`rigour.md` proof-style answers** (functional induction, monad-law verification, retract proofs without code) | A20 covers iso/retract but assumes a code skeleton. Pure-prose proofs aren't programming questions. | **RESOLVED → [A20-laws-iso.md](../archetypes/A20-laws-iso.md)**. The law-verification / iso / retract material (and how to turn each law into a QuickCheck property) lives there. Pure-prose proofs are very unlikely as a standalone 10-marker on an auto-marked QuickCheck exam — A20's QuickCheck-property framing is the exam-relevant form. |
| **`Life.md`** (Conway implementation) | A23 covers mini-games but `Life` is more about list-comprehension neighbourhood scanning than game state. Overlap with A21. | Cover under [A23-mini-game](../archetypes/A23-mini-game.md) with a "Conway variant" sub-section. Exam probability is ⭐ so deprioritise. |
| **Assignment 1 zipper / `GridWithAPointer`** (the focus-with-context pattern) | A17 covers zippers but isn't in the user-listed archetype topic spec for COURSE-MAP. | Confirmed: A17 *is* listed in the archetype numbers. Build [A17-zipper-navigation](../archetypes/A17-zipper.md) and link from `custom-ADTs`. |
| **Type-level reasoning** (read `:info`, infer most-general type without writing code) | None of A01–A24 are about reading types. | Lives under [TYPE-SIGNATURE-DATABASE](../indexes/TYPE-SIGNATURE-DATABASE.md) as a *recognition* skill, not an archetype. |
| **`tictactoe.md` minimax and α-β pruning** (game-tree search with `Tree`-of-grids) | A23 is "mini-game" but minimax is more sophisticated. A01 is structural recursion on trees but doesn't capture the search aspect. | **RESOLVED → [A23-mini-game.md](../archetypes/A23-mini-game.md)**. Game-tree search (build the move tree, then minimax/label) is covered there as the TicTacToe sub-section. Exam probability moderate (⭐⭐). |
| **Round-robin / sleep scheduling** (Assignment 3 Tasks 3–4) | A14 multi-effect covers the structure but not the *scheduler algorithm* specifically. | Cover under [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md) with a "scheduler" sub-section. |

---

## Notes on ambiguous lecture topics

Topics where the lecture material was unclear about scope or where the same concept appears across multiple lectures. Useful for the Archetype Analyst subagent to know.

- **Reader monad** is mentioned in `monads.md` but only really exercised in Assignment 3 (via `Free`) and Problem Sheet 13 of practice (problem 124). The lecture coverage is light — probability set to ⭐⭐. Could plausibly appear in the exam as a "define your own monad" question (A06).
- **Foldable** and **Traversable** are mentioned in `even-more-typeclasses.md` but not graded in any of the three assignments. Treated as ⭐⭐ unless the Vault Auditor finds graded evidence.
- **`Data2.md` permutation trees** (hard problem set § "Permutation trees, list permutations, and paths in such trees") is flagged as hard in the lecture and absent from assignments. Excluded from the main map; mention only if the user explicitly asks.
- **`functions.md` operators and sections** — only relevant as point-free flavour in higher-order; not a topic in its own right.
- **The `interpreter/` subdir** has `AbstractSyntax`, `ConcreteSyntax`, `Interpreter`, `Parser`, `Parsing`, `Runxy`. These are *one* topic (interpreter-imperative-storage). They are aggregated into one row above.
- **`Life.md`** is described as week 1 in some places (motivational) and week 11 in others (game-tree adjacent). The graded Game-of-Life implementation work happened weeks ago — assigned ⭐ probability because it has never appeared in a mock or graded assignment.

---

## How downstream subagents should use this file

1. **Archetype Analyst** — for each A## listed, find every linked vault file in the "Linked Vault Files" column and write the archetype card. The reverse index gives you the lectures to mine for canonical templates.
2. **Tree / Monad / Interpreter Specialists** — your file paths are listed in the table. The topic blocks in `COURSE-MAP.md` give you exact type signatures and question generators to reproduce verbatim.
3. **QuickCheck Specialist** — use the "Common mistakes" sections per topic as your attack surface; every common-mistake line is a property to write.
4. **Exam Setter** — use the ⭐⭐⭐⭐⭐ rows + their primary archetype to weight your mock paper.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
