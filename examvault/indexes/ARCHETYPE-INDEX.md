<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **ARCHETYPE-INDEX**

<!-- siblings:start -->
> **Peers:** **ARCHETYPE-INDEX** · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · [MASTER-INDEX](./MASTER-INDEX.md) · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# ARCHETYPE-INDEX

A single-page map of all 24 archetypes A01–A24. **Use this when** you already know which archetype the question is, but want to remember every related file in one hop (canonical template, mutation library, attack surface, pitfalls, cross-domain partners).

For an archetype you don't yet know, route through [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) (phrase trigger) or [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) (sig fingerprint) first.

---

## Tier-ranked summary

⭐ count is the composite F · D · C · E score from [`archetypes/README.md`](../archetypes/README.md).

| ⭐ | # | Archetype | Where it appears | Primary template | Mutation library |
|---|---|---|---|---|---|
| ⭐⭐⭐⭐⭐ | A01 | Tree-ADT structural recursion | Mock Q1, Mock Q5, A2/A3 | [A01](../archetypes/A01-tree-recursion.md) | [tree-counting](../question-families/tree-counting-family.md), [tree-validation](../question-families/tree-validation-family.md), [tree-transform](../question-families/tree-transform-family.md), [tree-extract](../question-families/tree-extract-family.md) |
| ⭐⭐⭐⭐⭐ | A02 | State-monad mini-game | Mock Q3 (Nim) | [A02](../archetypes/A02-state-game.md) | [state-game](../question-families/state-game-family.md) |
| ⭐⭐⭐⭐⭐ | A03 | Generic `Monad m =>` combinator | Mock Q2 (`applyNTimes`) | [A03](../archetypes/A03-generic-monad.md) | [monad-combinator](../question-families/monad-combinator-family.md) |
| ⭐⭐⭐⭐ | A04 | Matrix `[[Int]] -> Bool` predicate | Mock Q4 (magic square) | [A04](../archetypes/A04-matrix-predicate.md) | [matrix-predicate](../question-families/matrix-predicate-family.md) |
| ⭐⭐⭐⭐ | A05 | ADT → ADT translation | Mock Q5 (Expr → Circuit) | [A05](../archetypes/A05-adt-translation.md) | [adt-translation](../question-families/adt-translation-family.md) |
| ⭐⭐⭐⭐ | A06 | Functor / Applicative / Monad instance | A3 Free monad | [A06](../archetypes/A06-functor-instance.md) | [functor-instance](../question-families/functor-instance-family.md), [applicative-monad-instance](../question-families/applicative-monad-instance-family.md) |
| ⭐⭐⭐⭐ | A07 | Codec encode / decode | A2 Morse, problem 147 RLE | [A07](../archetypes/A07-codec-pair.md) | [codec](../question-families/codec-family.md) |
| ⭐⭐⭐⭐ | A08 | Environment evaluator (`Env -> Expr -> r`) | Problem 148, Week 7 | [A08](../archetypes/A08-env-eval.md) | [env-eval](../question-families/env-eval-family.md) |
| ⭐⭐⭐ | A09 | Re-implement Prelude function | Practice set 1 | [A09](../archetypes/A09-prelude-reimpl.md) | [list-rewrite](../question-families/list-rewrite-family.md) |
| ⭐⭐⭐ | A10 | Fold reformulation | Practice set 3 | [A10](../archetypes/A10-fold-reformulation.md) | [list-fold](../question-families/list-fold-family.md) |
| ⭐⭐⭐ | A11 | BST insert / delete / member / isBST | Practice set 8, Week 6 | [A11](../archetypes/A11-bst-ops.md) | [bst-ops](../question-families/bst-ops-family.md) |
| ⭐⭐⭐ | A12 | Representation conversion (List ↔ Tree) | Practice set 8 | [A12](../archetypes/A12-rep-conversion.md) | [tree-extract](../question-families/tree-extract-family.md) |
| ⭐⭐ | A13 | Custom Show / pretty-printer | Problem 64 | [A13](../archetypes/A13-pretty-printer.md) | [pretty-print](../question-families/pretty-print-family.md) |
| ⭐⭐⭐ | A14 | State + Error interpreter (multi-effect) | Week 9 calculator | [A14](../archetypes/A14-multi-effect-interp.md) | [env-eval](../question-families/env-eval-family.md), [error-handling](../question-families/error-handling-family.md) |
| ⭐⭐ | A15 | Writer monad trace | Problems 107, 108 | [A15](../archetypes/A15-writer-trace.md) | [writer-trace](../question-families/writer-trace-family.md) |
| ⭐⭐ | A16 | Parser combinators (Functor/Applicative/Monad) | Week 10 | [A16](../archetypes/A16-parser-combinators.md) | [parser](../question-families/parser-family.md) |
| ⭐ | A17 | Zipper navigation | A1 GridWithAPointer | [A17](../archetypes/A17-zipper.md) | — (one-shot puzzle) |
| ⭐ | A18 | Lazy memoisation (memoFib) | Problems 131–137 | [A18](../archetypes/A18-lazy-memo.md) | [lazy-infinite](../question-families/lazy-infinite-family.md) |
| ⭐⭐⭐ | A19 | Extend an existing interpreter | A2 / Week 10 | [A19](../archetypes/A19-extend-interpreter.md) | [env-eval](../question-families/env-eval-family.md) |
| ⭐ | A20 | Iso / retract / monad-law proofs (theory) | Week 11 | [A20](../archetypes/A20-laws-iso.md) | — (theory, see [monad-laws](../monads/monad-laws.md)) |
| ⭐⭐⭐ | A21 | List comprehension synthesis | Problems 31–40 | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp](../question-families/list-comp-family.md) |
| ⭐⭐⭐ | A22 | Eq / Ord / Show instance | Problems 63–70 | [A22](../archetypes/A22-typeclass-instance.md) | [functor-instance](../question-families/functor-instance-family.md) |
| ⭐⭐⭐⭐ | A23 | Generalised mini-game (Conway, TTT) | Problem 150 | [A23](../archetypes/A23-mini-game.md) | [state-game](../question-families/state-game-family.md) |
| ⭐⭐ | A24 | Applicative-only instance (parser style) | Week 10 | [A24](../archetypes/A24-applicative-instance.md) | [applicative-monad-instance](../question-families/applicative-monad-instance-family.md) |

> **5-question composition guess** (from [archetypes/README.md](../archetypes/README.md)): Q1 = A01, Q2 = A03, Q3 = A02/A23, Q4 = A04/A08, Q5 = A05/A06.

---

## Per-archetype full hop list

For each archetype: the canonical template, the mutation library, the topic deep-dive, the cross-domain neighbours, the QuickCheck attacks, and the relevant pitfalls. Mid-question, click whichever you need.

### A01 — Tree-ADT structural recursion · ⭐⭐⭐⭐⭐

- **Template:** [A01-tree-recursion](../archetypes/A01-tree-recursion.md)
- **Mutations:** [tree-counting](../question-families/tree-counting-family.md) · [tree-validation](../question-families/tree-validation-family.md) · [tree-transform](../question-families/tree-transform-family.md) · [tree-extract](../question-families/tree-extract-family.md)
- **Topic depth:** [binary-tree](../trees/binary-tree.md) · [rose-tree](../trees/rose-tree.md) · [tree-functor](../trees/tree-functor.md) · [tree-fold](../trees/tree-fold.md)
- **Combines with:** [tree-x-state](../cross-matrix/tree-x-state.md) · [tree-x-writer](../cross-matrix/tree-x-writer.md) · [tree-x-either](../cross-matrix/tree-x-either.md) · [tree-x-maybe](../cross-matrix/tree-x-maybe.md) · [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md)
- **Attacks:** [trees-attacks](../quickcheck/trees-attacks.md)
- **Pitfalls:** [P-005 Missing base case → infinite loop / non-exhaustive](../pitfalls/HIGH-severity.md#p-005) (the `Empty`/`Leaf` base case missed → non-termination) · [P-017 Non-exhaustive pattern](../pitfalls/HIGH-severity.md#p-017) (a constructor case omitted or mistyped against `Types.hs`)
- **Basics refresher:** [recursive-data-types](../haskell-basics/recursive-data-types.md) · [recursion](../haskell-basics/recursion.md) · [pattern-matching](../haskell-basics/pattern-matching.md)
- **Testing:** [testing-tree-functions](../haskell-basics/testing-tree-functions.md)

### A02 — State-monad mini-game · ⭐⭐⭐⭐⭐

- **Template:** [A02-state-game](../archetypes/A02-state-game.md)
- **Mutations:** [state-game](../question-families/state-game-family.md)
- **Topic depth:** [state](../monads/state.md) · [generic-combinators](../monads/generic-combinators.md)
- **Combines with:** [game-state](../cross-matrix/game-state.md) · [bst-x-state](../cross-matrix/bst-x-state.md) · [list-x-state](../cross-matrix/list-x-state.md)
- **Attacks:** [state-attacks](../quickcheck/state-attacks.md)
- **Pitfalls:** [P-006 Mock Q3 gameOver does not return True on (0,0)](../pitfalls/HIGH-severity.md#p-006) (the hardcoded `(0,0)` test worth 4 marks) · [P-024 State action returns wrong type (() vs result)](../pitfalls/HIGH-severity.md#p-024) (returning `()` when the spec wants a `Bool`/value)
- **Basics refresher:** [do-notation-basics](../haskell-basics/do-notation-basics.md)
- **Testing:** [testing-monadic-functions](../haskell-basics/testing-monadic-functions.md)

### A03 — Generic `Monad m =>` combinator · ⭐⭐⭐⭐⭐

- **Template:** [A03-generic-monad](../archetypes/A03-generic-monad.md)
- **Mutations:** [monad-combinator](../question-families/monad-combinator-family.md)
- **Topic depth:** [generic-combinators](../monads/generic-combinators.md) · [monad](../typeclasses/monad.md) · [monad-laws](../monads/monad-laws.md)
- **Combines with:** [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md) · [list-x-monad](../cross-matrix/list-x-monad.md)
- **Attacks:** [monad-attacks](../quickcheck/monad-attacks.md)
- **Pitfalls:** [P-007 Mock Q2 applyNTimes 0 returns [] instead of [x]](../pitfalls/HIGH-severity.md#p-007) (the `n=0` case must yield `[x]`, not `[]`) · [P-008 Numeric recursion uses n==0 not n<=0](../pitfalls/HIGH-severity.md#p-008) (guard the count-down with `n <= 0`, not `n == 0`)
- **Basics refresher:** [higher-order-functions](../haskell-basics/higher-order-functions.md) · [do-notation-basics](../haskell-basics/do-notation-basics.md)
- **Testing:** [testing-monadic-functions](../haskell-basics/testing-monadic-functions.md)

### A04 — Matrix `[[Int]] -> Bool` predicate · ⭐⭐⭐⭐

- **Template:** [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md)
- **Mutations:** [matrix-predicate](../question-families/matrix-predicate-family.md)
- **Topic depth:** [PRELUDE-INDEX](./PRELUDE-INDEX.md) → `transpose`, `Data.List`
- **Combines with:** [list-x-list-monad](../cross-matrix/list-x-list-monad.md) (search over the grid)
- **Attacks:** [matrix-attacks](../quickcheck/matrix-attacks.md)
- **Pitfalls:** [P-030 Magic-square checks columns/diagonal wrong direction](../pitfalls/HIGH-severity.md#p-030) (Mock Q4: get the column / diagonal axis right) · [P-005 Missing base case → infinite loop / non-exhaustive](../pitfalls/HIGH-severity.md#p-005) (handle empty `[[]]` / ragged rows so the recursion terminates)
- **Basics refresher:** [list-comprehensions](../haskell-basics/list-comprehensions.md) · [all-any](../haskell-basics/all-any.md)

### A05 — ADT → ADT translation · ⭐⭐⭐⭐

- **Template:** [A05-adt-translation](../archetypes/A05-adt-translation.md)
- **Mutations:** [adt-translation](../question-families/adt-translation-family.md)
- **Topic depth:** [expression-tree](../trees/expression-tree.md) · [desugar-pipeline](../interpreters/desugar-pipeline.md)
- **Combines with:** [expr-x-maybe](../cross-matrix/expr-x-maybe.md) · [expr-x-state](../cross-matrix/expr-x-state.md)
- **Attacks:** [expr-attacks](../quickcheck/expr-attacks.md)
- **Pitfalls:** [P-019 Mock Q5 ADT-translation copy-paste p/q cases](../pitfalls/HIGH-severity.md#p-019) (Expr → Circuit: don't copy-paste the `p`/`q` sub-cases; checked semantically)
- **Basics refresher:** [recursive-data-types](../haskell-basics/recursive-data-types.md) · [algebraic-data-types](../haskell-basics/algebraic-data-types.md)

### A06 — Functor / Applicative / Monad instance · ⭐⭐⭐⭐

- **Template:** [A06-functor-instance](../archetypes/A06-functor-instance.md)
- **Mutations:** [functor-instance](../question-families/functor-instance-family.md) · [applicative-monad-instance](../question-families/applicative-monad-instance-family.md)
- **Topic depth:** [functor](../typeclasses/functor.md) · [applicative](../typeclasses/applicative.md) · [monad](../typeclasses/monad.md) · [monad-laws](../monads/monad-laws.md)
- **Combines with:** [A24](../archetypes/A24-applicative-instance.md)
- **Attacks:** [typeclass-instance-attacks](../quickcheck/typeclass-instance-attacks.md) · [PROPERTY-PATTERNS](../quickcheck/PROPERTY-PATTERNS.md)
- **Pitfalls:** [P-010 deriving Functor without the pragma](../pitfalls/HIGH-severity.md#p-010) (`deriving Functor` needs the pragma; `-XSafe` blocks GeneralizedNewtypeDeriving) · [P-016 Functor instance doesn't preserve shape](../pitfalls/HIGH-severity.md#p-016) (the Functor law: `fmap` must keep the structure intact)
- **Basics refresher:** [polymorphism](../haskell-basics/polymorphism.md) · [type-signatures](../haskell-basics/type-signatures.md)

### A07 — Codec encode / decode · ⭐⭐⭐⭐

- **Template:** [A07-codec-pair](../archetypes/A07-codec-pair.md)
- **Mutations:** [codec](../question-families/codec-family.md)
- **Topic depth:** Caesar, Morse, RLE — see family file. ADT shape: BST with `Maybe Char` payload.
- **Combines with:** [A05](../archetypes/A05-adt-translation.md) (`ramify` table → tree)
- **Attacks:** [codec-attacks](../quickcheck/codec-attacks.md)
- **Pitfalls:** [P-014 isNBranching shallow check (forgets to recurse)](../pitfalls/HIGH-severity.md#p-014) (recurse fully into children; a one-level check passes shallow trees but fails the marker)

### A08 — Environment evaluator · ⭐⭐⭐⭐

- **Template:** [A08-env-eval](../archetypes/A08-env-eval.md)
- **Mutations:** [env-eval](../question-families/env-eval-family.md)
- **Topic depth:** [expr-reader](../interpreters/expr-reader.md) · [expr-reader-either](../interpreters/expr-reader-either.md) · [interpreters/README](../interpreters/README.md)
- **Combines with:** [expr-x-state](../cross-matrix/expr-x-state.md) · [expr-x-multi](../cross-matrix/expr-x-multi.md)
- **Attacks:** [interp-attacks](../quickcheck/interp-attacks.md)
- **Pitfalls:** [P-017 Non-exhaustive pattern](../pitfalls/HIGH-severity.md#p-017) (an unbound `Var` or unhandled `Expr` case crashes the evaluator — cover every constructor)

### A09 — Re-implement Prelude function · ⭐⭐⭐

- **Template:** [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md)
- **Mutations:** [list-rewrite](../question-families/list-rewrite-family.md)
- **Topic depth:** [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [allowed-builtins](../haskell-basics/allowed-builtins.md)
- **Attacks:** [lists-attacks](../quickcheck/lists-attacks.md)
- **Pitfalls:** Don't call the Prelude version you're meant to reimplement.
- **Basics refresher:** [recursion](../haskell-basics/recursion.md) · [accumulator-recursion](../haskell-basics/accumulator-recursion.md)

### A10 — Fold reformulation · ⭐⭐⭐

- **Template:** [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md)
- **Mutations:** [list-fold](../question-families/list-fold-family.md)
- **Topic depth:** [foldr](../haskell-basics/foldr.md) · [foldl](../haskell-basics/foldl.md)
- **Attacks:** [lists-attacks](../quickcheck/lists-attacks.md)
- **Pitfalls:** [P-112 foldr vs foldl confusion](../pitfalls/MEDIUM-severity.md#p-112) (`foldr (-) 0` ≠ `foldl (-) 0`; default `foldr` to build, `foldl'` for numbers)

### A11 — BST operations · ⭐⭐⭐

- **Template:** [A11-bst-ops](../archetypes/A11-bst-ops.md)
- **Mutations:** [bst-ops](../question-families/bst-ops-family.md)
- **Topic depth:** [bst](../trees/bst.md) · [bst-delete-trace](../trees/bst-delete-trace.md)
- **Combines with:** [bst-x-state](../cross-matrix/bst-x-state.md) · [bst-x-writer](../cross-matrix/bst-x-writer.md)
- **Attacks:** [bst-attacks](../quickcheck/bst-attacks.md)
- **Pitfalls:** [P-009 isBST Empty = False (vacuous truth)](../pitfalls/HIGH-severity.md#p-009) (Empty is vacuously sorted — must be `True`) · [P-015 BST delete two-children case wrong](../pitfalls/HIGH-severity.md#p-015) (need `largestOf l` **and** `withoutLargest l`)

### A12 — Representation conversion · ⭐⭐⭐

- **Template:** [A12-rep-conversion](../archetypes/A12-rep-conversion.md)
- **Mutations:** [tree-extract](../question-families/tree-extract-family.md)
- **Topic depth:** [binary-tree](../trees/binary-tree.md) · [rose-tree](../trees/rose-tree.md)
- **Attacks:** [trees-attacks](../quickcheck/trees-attacks.md)
- **Pitfalls:** [P-016 Functor instance doesn't preserve shape](../pitfalls/HIGH-severity.md#p-016) (a conversion that round-trips must be shape-preserving — `fmap id = id`, `toTree . toList = id`)

### A13 — Custom Show / pretty-printer · ⭐⭐

- **Template:** [A13-pretty-printer](../archetypes/A13-pretty-printer.md)
- **Mutations:** [pretty-print](../question-families/pretty-print-family.md)
- **Topic depth:** [show](../typeclasses/show.md)
- **Attacks:** [typeclass-instance-attacks](../quickcheck/typeclass-instance-attacks.md) (Show is covered there)
- **Pitfalls:** [P-012 Custom Show returns non-string](../pitfalls/HIGH-severity.md#p-012) (`show (Val n) = show n`, not `n`; every recursive call yields `String`)

### A14 — Multi-effect interpreter · ⭐⭐⭐

- **Template:** [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md)
- **Mutations:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md)
- **Topic depth:** [multi-effect](../monads/multi-effect.md) · [transformers](../monads/transformers.md) · [transformer-stack-order](../monads/transformer-stack-order.md) · [imperative-storage](../interpreters/imperative-storage.md)
- **Combines with:** [expr-x-multi](../cross-matrix/expr-x-multi.md)
- **Attacks:** [interp-attacks](../quickcheck/interp-attacks.md)
- **Pitfalls:** [P-004 Used Control.Monad.Reader or Control.Monad.Except](../pitfalls/HIGH-severity.md#p-004) (multi-effect: use plain `Either`/`StateT s (Either e)`, never `Control.Monad.Reader`/`Except`)

### A15 — Writer monad trace · ⭐⭐

- **Template:** [A15-writer-trace](../archetypes/A15-writer-trace.md)
- **Mutations:** [writer-trace](../question-families/writer-trace-family.md)
- **Topic depth:** [writer](../monads/writer.md)
- **Combines with:** [tree-x-writer](../cross-matrix/tree-x-writer.md) · [list-x-writer](../cross-matrix/list-x-writer.md) · [writer-x-either](../cross-matrix/writer-x-either.md)
- **Attacks:** [writer-attacks](../quickcheck/writer-attacks.md)
- **Pitfalls:** [P-110 Writer log ordering](../pitfalls/MEDIUM-severity.md#p-110) (`tell` BEFORE vs AFTER the recursion decides enter/leave order)

### A16 — Parser combinators · ⭐⭐

- **Template:** [A16-parser-combinators](../archetypes/A16-parser-combinators.md)
- **Mutations:** [parser](../question-families/parser-family.md)
- **Topic depth:** [parser-overview](../interpreters/parser-overview.md) · [parser-chainl1](../interpreters/parser-chainl1.md)
- **Combines with:** [parser-x-either](../cross-matrix/parser-x-either.md)
- **Attacks:** [interp-attacks](../quickcheck/interp-attacks.md) (parser failures share interpreter attack surface)
- **Pitfalls:** [P-005 Missing base case → infinite loop / non-exhaustive](../pitfalls/HIGH-severity.md#p-005) (a greedy/left-recursive parser that never consumes input loops; always have a terminating branch)

### A17 — Zipper navigation · ⭐

- **Template:** [A17-zipper](../archetypes/A17-zipper.md)
- **Combines with:** Assignment 1 GridWithAPointer
- **Pitfalls:** [P-016 Functor instance doesn't preserve shape](../pitfalls/HIGH-severity.md#p-016) (zipper round-trip: `left . right = id` must preserve the structure; the marker checks the operation really is the identity)

### A18 — Lazy memoisation · ⭐

- **Template:** [A18-lazy-memo](../archetypes/A18-lazy-memo.md)
- **Mutations:** [lazy-infinite](../question-families/lazy-infinite-family.md)
- **Pitfalls:** [P-023 deepseq exposes lazy undefined](../pitfalls/HIGH-severity.md#p-023) (the cache relies on laziness, but `deepseq` forces every field — don't leave thunks the marker will crash on)

### A19 — Extend an interpreter · ⭐⭐⭐

- **Template:** [A19-extend-interpreter](../archetypes/A19-extend-interpreter.md)
- **Topic depth:** [extend-interpreter](../interpreters/extend-interpreter.md) · [desugar-pipeline](../interpreters/desugar-pipeline.md)
- **Pitfalls:** [P-109 new constructor → missing interpreter case](../pitfalls/MEDIUM-severity.md#p-109) (adding `Implies`/etc. to the ADT without a matching equation → non-exhaustive crash; desugar it: `circuit (Implies p q) = circuit (Or (Not p) q)`)

### A20 — Iso / retract / monad-law proofs · ⭐

- **Template:** [A20-laws-iso](../archetypes/A20-laws-iso.md)
- **Topic depth:** [monad-laws](../monads/monad-laws.md) · [PROPERTY-PATTERNS](../quickcheck/PROPERTY-PATTERNS.md)
- **Pitfalls:** [P-026 Forgetting Safe pragma blocks all marker tests](../pitfalls/HIGH-severity.md#p-026) (even a laws/iso answer scores 0 if the `{-# LANGUAGE Safe #-}` pragma is missing)

### A21 — List comprehension synthesis · ⭐⭐⭐

- **Template:** [A21-list-comp-synthesis](../archetypes/A21-list-comp-synthesis.md)
- **Mutations:** [list-comp](../question-families/list-comp-family.md)
- **Topic depth:** [list-comprehensions](../haskell-basics/list-comprehensions.md)
- **Pitfalls:** [P-027 GHCi runtime errors mask compile errors](../pitfalls/HIGH-severity.md#p-027) (a comprehension that loads in GHCi can still fail the marker on `[]`/`[x]` — a runtime slip hides the real fault; run the adversarial inputs)

### A22 — Typeclass instance (Eq / Ord / Show) · ⭐⭐⭐

- **Template:** [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md)
- **Mutations:** see [functor-instance](../question-families/functor-instance-family.md)
- **Topic depth:** [eq-ord](../typeclasses/eq-ord.md) · [show](../typeclasses/show.md) · [num](../typeclasses/num.md)
- **Attacks:** [typeclass-instance-attacks](../quickcheck/typeclass-instance-attacks.md)
- **Pitfalls:** [P-012 Custom Show returns non-string](../pitfalls/HIGH-severity.md#p-012) (when hand-writing the Show instance, every branch returns `String` — `show n`, never the bare `Int`)

### A23 — Generalised mini-game · ⭐⭐⭐⭐

- **Template:** [A23-mini-game](../archetypes/A23-mini-game.md) (Minimax, alpha-beta, depth-limit, memoise)
- **Mutations:** [state-game](../question-families/state-game-family.md)
- **Topic depth:** [state](../monads/state.md) · [game-state](../cross-matrix/game-state.md)
- **Attacks:** [state-attacks](../quickcheck/state-attacks.md)

### A24 — Applicative-only instance · ⭐⭐

- **Template:** [A24-applicative-instance](../archetypes/A24-applicative-instance.md)
- **Mutations:** [applicative-monad-instance](../question-families/applicative-monad-instance-family.md)
- **Topic depth:** [applicative](../typeclasses/applicative.md)
- **Attacks:** [typeclass-instance-attacks](../quickcheck/typeclass-instance-attacks.md)
- **Pitfalls:** [P-029 do block returns monadic value instead of bare value](../pitfalls/HIGH-severity.md#p-029) (`return` takes a BARE value; don't wrap an already-`<-`-bound or already-monadic value twice)

---

## Likely 2-archetype combinations

The hardest exam questions combine archetypes. Top compositions, ranked by how often the mock + assignments exercise them:

| Combination | Where seen | File |
|---|---|---|
| A01 × A02 (Tree × State) | Tree labelling, fresh-IDs | [tree-x-state](../cross-matrix/tree-x-state.md) |
| A01 × A03 (Tree × Generic Monad) | `mapMTree`, `traverseTree` | [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md) |
| A01 × A15 (Tree × Writer) | log every traversal step | [tree-x-writer](../cross-matrix/tree-x-writer.md) |
| A05 × A08 (ADT translation × Eval) | desugar + evaluate | [desugar-pipeline](../interpreters/desugar-pipeline.md) |
| A08 × A14 (Env eval × Multi-effect) | full interpreter | [expr-x-multi](../cross-matrix/expr-x-multi.md) |
| A11 × A02 (BST × State) | fresh insert | [bst-x-state](../cross-matrix/bst-x-state.md) |
| A16 × A24 (Parser × Applicative) | applicative-only parser | [parser-overview](../interpreters/parser-overview.md) |
| A16 × A07 (Parser × Codec) | parse + decode | [codec-family](../question-families/codec-family.md) |
| A03 × A21 (Generic Monad × List comp) | `do` over list monad | [list-x-list-monad](../cross-matrix/list-x-list-monad.md) |
| A05 × A13 (ADT translation × Pretty-printer) | translate then show | [A13](../archetypes/A13-pretty-printer.md) |

See [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) for the full row-by-column matrix.

---

## Find-by-mock-question

If you're using this index *during* the mock-paper re-runs:

| Mock Q | Archetype | Open |
|---|---|---|
| Q1 (Rose: isNBranching / prune) | A01 | [A01](../archetypes/A01-tree-recursion.md) → [rose-ops-family](../question-families/rose-ops-family.md) |
| Q2 (applyNTimes :: Monad m =>) | A03 | [A03](../archetypes/A03-generic-monad.md) → [monad-combinator-family](../question-families/monad-combinator-family.md) |
| Q3 (Nim — gameOver, takeTokens) | A02 | [A02](../archetypes/A02-state-game.md) → [state-game-family](../question-families/state-game-family.md) |
| Q4 (isMagicSquare) | A04 | [A04](../archetypes/A04-matrix-predicate.md) → [matrix-predicate-family](../question-families/matrix-predicate-family.md) |
| Q5 (Expr → Circuit) | A05 | [A05](../archetypes/A05-adt-translation.md) → [adt-translation-family](../question-families/adt-translation-family.md) |

Verbatim Mock specs: [MOCK-Q-INDEX](./MOCK-Q-INDEX.md).

---

## See also

**Mutation atlas:** [MUTATION-INDEX](./MUTATION-INDEX.md) — every mutation across all 24 families.
**Cross-topic matrix:** [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) — data-structure × monad fully tabulated.
**Phrase → archetype:** [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) — 240+ trigger rows.
**Type → archetype:** [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) — sig fingerprint.
**Priority + composition:** [archetypes/README](../archetypes/README.md) — F·D·C·E scoring + flowchart.
**Tier 1 deep dive:** [A01](../archetypes/A01-tree-recursion.md) · [A02](../archetypes/A02-state-game.md) · [A03](../archetypes/A03-generic-monad.md) · [A04](../archetypes/A04-matrix-predicate.md) · [A05](../archetypes/A05-adt-translation.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
