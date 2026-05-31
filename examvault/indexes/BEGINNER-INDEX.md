<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **BEGINNER-INDEX**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · **BEGINNER-INDEX** · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · [MASTER-INDEX](./MASTER-INDEX.md) · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# BEGINNER-INDEX

A *linear* reading path for someone who walked in cold. Open this when you are not yet comfortable enough to use [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) directly — most "find a page" indexes assume you already recognise the topic name.

If you have ≥ 8 hours: do it all. If you have 4 hours: skip to "Stage 4 — drill the 5 mock questions". If you have ≤ 2 hours: jump to [`exam-day/ONE-PAGE-PANIC.md`](../exam-day/ONE-PAGE-PANIC.md) and the canonical templates in [common-templates](../haskell-basics/common-templates.md).

---

## Stage 0 — The basics you can't dodge (≈ 60 min)

The syntax minimum. If you skip this, every later page lands harder.

1. [pattern-matching](../haskell-basics/pattern-matching.md)
2. [guards](../haskell-basics/guards.md)
3. [recursion](../haskell-basics/recursion.md) — the single most important page
4. [type-signatures](../haskell-basics/type-signatures.md) — learn to read `Monad m => (a -> m b) -> ...`
5. [lists](../haskell-basics/lists.md), [tuples](../haskell-basics/tuples.md), [strings](../haskell-basics/strings.md)
6. [algebraic-data-types](../haskell-basics/algebraic-data-types.md), [recursive-data-types](../haskell-basics/recursive-data-types.md)
7. [case-expressions](../haskell-basics/case-expressions.md), [let-in](../haskell-basics/let-in.md), [where-clauses](../haskell-basics/where-clauses.md)
8. [allowed-builtins](../haskell-basics/allowed-builtins.md) — what you can import; everything else is a 0-mark trap

Once these feel familiar, you can read any archetype page.

---

## Stage 1 — How to actually try things (≈ 30 min)

You will type code into GHCi for the whole exam. Get fluent at running and verifying.

1. [ghci-commands](../haskell-basics/ghci-commands.md) — the runtime
2. [testing-functions](../haskell-basics/testing-functions.md) — pure
3. [testing-recursive-functions](../haskell-basics/testing-recursive-functions.md) — recursion + edge cases
4. [testing-tree-functions](../haskell-basics/testing-tree-functions.md) — sample-tree recipes
5. [testing-monadic-functions](../haskell-basics/testing-monadic-functions.md) — `runState`, `evalState`, `runWriter`

---

## Stage 2 — Mid-level building blocks (≈ 90 min)

Now you can read the meaty stuff.

1. [higher-order-functions](../haskell-basics/higher-order-functions.md), [lambdas](../haskell-basics/lambdas.md), [function-composition](../haskell-basics/function-composition.md), [dollar-operator](../haskell-basics/dollar-operator.md), [dot-operator](../haskell-basics/dot-operator.md)
2. [map](../haskell-basics/map.md), [filter](../haskell-basics/filter.md), [foldr](../haskell-basics/foldr.md), [foldl](../haskell-basics/foldl.md)
3. [list-comprehensions](../haskell-basics/list-comprehensions.md)
4. [maybe-basics](../haskell-basics/maybe-basics.md), [either-basics](../haskell-basics/either-basics.md), [do-notation-basics](../haskell-basics/do-notation-basics.md)
5. [accumulator-recursion](../haskell-basics/accumulator-recursion.md), [helper-functions](../haskell-basics/helper-functions.md)
6. [deriving](../haskell-basics/deriving.md), [polymorphism](../haskell-basics/polymorphism.md), [currying](../haskell-basics/currying.md), [partial-application](../haskell-basics/partial-application.md)

---

## Stage 3 — Monads and typeclasses (≈ 90 min)

The exam will test at least one of these. Pick the ones from the matching mock question.

| You need this | Read these |
|---|---|
| Mock Q2 (`Monad m =>`) | [Monad typeclass](../typeclasses/monad.md) → [generic-combinators](../monads/generic-combinators.md) → [A03](../archetypes/A03-generic-monad.md) |
| Mock Q3 (State Nim) | [State monad](../monads/state.md) → [A02](../archetypes/A02-state-game.md) |
| Mock Q5 (Functor instance) | [Functor](../typeclasses/functor.md) → [A06](../archetypes/A06-functor-instance.md) |
| Maybe / Either questions | [Maybe](../monads/maybe.md), [Either](../monads/either.md) → [A14](../archetypes/A14-multi-effect-interp.md) |
| Writer / log questions | [Writer monad](../monads/writer.md) → [A15](../archetypes/A15-writer-trace.md) |
| Reader / env questions | [Reader monad](../monads/reader.md) → [A08](../archetypes/A08-env-eval.md) |
| List monad / non-determinism | [list-monad](../monads/list-monad.md) → [A21](../archetypes/A21-list-comp-synthesis.md) |
| Applicative instance | [Applicative](../typeclasses/applicative.md) → [A24](../archetypes/A24-applicative-instance.md) |
| Multi-effect / Free monad | [multi-effect](../monads/multi-effect.md) → [transformer-stack-order](../monads/transformer-stack-order.md) → [A14](../archetypes/A14-multi-effect-interp.md) |
| Custom Eq/Ord/Show | [eq-ord](../typeclasses/eq-ord.md) → [show](../typeclasses/show.md) → [A22](../archetypes/A22-typeclass-instance.md) |

Then read [monad-laws](../monads/monad-laws.md) once — you don't need to memorise the proofs, but you should recognise what `return x >>= f == f x` *says*.

---

## Stage 4 — Drill the 5 mock questions (≈ 90 min)

[MOCK-Q-INDEX](./MOCK-Q-INDEX.md) — Mock Q1 to Q5 verbatim with canonical solutions and *marker quirks*. Read each twice. Try to recreate the solution from scratch (with the page closed). Then read it once more.

Marker quirks you should know (from [MOCK-Q-INDEX](./MOCK-Q-INDEX.md)):

- **Q2:** the generator starts at `n=2`; off-by-one is silently lenient.
- **Q3:** `gameOver (0,0)` is hardcoded — 4 free marks.
- **Q5:** `circuit` is checked **semantically** (boolean equivalence), not structurally.

---

## Stage 5 — Pitfalls + QuickCheck attacks (≈ 60 min)

The marker hunts for these. Reading them once = ~10 marks saved.

1. [pitfalls/HIGH-severity](../pitfalls/HIGH-severity.md) — 30 marks-killers, P-001 to P-068 — skim all, deep-read first 25
2. [pitfalls/imports-pitfalls](../pitfalls/imports-pitfalls.md) — the import trap
3. [pitfalls/signature-pitfalls](../pitfalls/signature-pitfalls.md) — type-sig literal-match
4. [quickcheck/QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) — universal attack list
5. [quickcheck/PROPERTY-PATTERNS](../quickcheck/PROPERTY-PATTERNS.md) — Arbitrary instances + prop_ patterns

---

## Stage 6 — Exam day (the last 30 min before walking in)

1. [exam-day/ONE-PAGE-PANIC](../exam-day/ONE-PAGE-PANIC.md) — single-page panic mode
2. [exam-day/EXAM-DAY-ROUTE](../exam-day/EXAM-DAY-ROUTE.md) — what to do first
3. [exam-day/IN-EXAM-WORKFLOW](../exam-day/IN-EXAM-WORKFLOW.md) — per-question routine
4. [exam-day/RECOGNITION-FLOWCHART](../exam-day/RECOGNITION-FLOWCHART.md) — question text → archetype
5. [exam-day/TIME-BUDGET](../exam-day/TIME-BUDGET.md) — 24 min per question, 7 buffer

If you only read **one page**: [exam-day/ONE-PAGE-PANIC](../exam-day/ONE-PAGE-PANIC.md).

---

## When you're stuck — the lookup chain

```
exam question text
   │
   ▼
indexes/IF-YOU-SEE-X.md   ← match a trigger phrase
   │
   ▼
archetypes/A##-*.md       ← read the canonical template
   │
   ▼
question-families/*.md    ← find the matching mutation
   │
   ▼
trees/ or monads/ ...     ← if you need theory
   │
   ▼
pitfalls/HIGH-severity.md ← before submit
```

Bookmark these five paths now.

---

## What to skip if time is short

Tier-4 archetypes (low exam probability): [A17 zipper](../archetypes/A17-zipper.md), [A18 lazy memo](../archetypes/A18-lazy-memo.md), [A20 laws/iso](../archetypes/A20-laws-iso.md). Read once, don't drill.

Detailed parser theory: skim [A16 parser combinators](../archetypes/A16-parser-combinators.md), [parser-overview](../interpreters/parser-overview.md). Past papers haven't drilled parser combinators heavily.

Monad transformers in depth: the allowed-imports list **does not include** `Control.Monad.Trans.State` etc. You won't need `StateT` syntax. Skim [transformers](../monads/transformers.md) once.

---

## See also

**Master:** [MASTER-INDEX](./MASTER-INDEX.md)
**By trigger phrase:** [IF-YOU-SEE-X](./IF-YOU-SEE-X.md)
**By archetype:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md)
**By mutation:** [MUTATION-INDEX](./MUTATION-INDEX.md)
**Cross-domain:** [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md)
**Exam-day pin list:** [WHAT-TO-PIN](../exam-day/WHAT-TO-PIN.md)
**Overall vault layout:** [KNOWLEDGE-MAP](../KNOWLEDGE-MAP.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
