<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · **archetypes**

# Archetypes

24 archetypes covering the exam-question shapes for the Birmingham FP 2025/26 module. Each archetype = the SHAPE of a typical 10-mark exam question.

Composite score: **F**(requency) × **D**(ifficulty) × **C**(onceptual weight) × **E**(xam-likelihood). H/M/L per factor.

## Priority ranking (composite F·D·C·E)

### Tier 1 — almost certainly tested
| # | Archetype | F | D | C | E | ⭐ | Why tier 1 |
|---|-----------|---|---|---|---|---|---|
| [A01](A01-tree-recursion.md) | Tree-ADT structural recursion | H | M | H | H | ⭐⭐⭐⭐⭐ | Mock Q1+Q5, A2 whole, A3 Q1, sets 8/9/15 |
| [A02](A02-state-game.md) | State monad game / sim | H | M | H | H | ⭐⭐⭐⭐⭐ | Mock Q3 (Nim), A3 Q3/Q4, set 12 |
| [A03](A03-generic-monad.md) | Generic `Monad m =>` | M | H | H | H | ⭐⭐⭐⭐⭐ | Mock Q2 (`applyNTimes`), set 13 |
| [A04](A04-matrix-predicate.md) | Matrix predicate via transpose | M | L | M | H | ⭐⭐⭐⭐ | Mock Q4 (magic square), set 15 |
| [A05](A05-adt-translation.md) | ADT-to-ADT translation | M | M | H | H | ⭐⭐⭐⭐ | Mock Q5 (Expr→Circuit), set 15 |
| [A06](A06-functor-instance.md) | Functor/Applicative/Monad instance | M | M | H | H | ⭐⭐⭐⭐ | Set 13 (#121-126), A3 Free |
| [A08](A08-env-eval.md) | Environment evaluator | M | M | H | H | ⭐⭐⭐⭐ | Sets 9/15 (#148), Week 7 |

### Tier 2 — very likely
| # | Archetype | F | D | C | E | ⭐ |
|---|-----------|---|---|---|---|---|
| [A07](A07-codec-pair.md) | Codec pair encode/decode | M | M | H | M | ⭐⭐⭐⭐ |
| [A11](A11-bst-ops.md) | BST operations | M | M | M | M | ⭐⭐⭐ |
| [A12](A12-rep-conversion.md) | Representation conversion | M | M | H | M | ⭐⭐⭐ |
| [A14](A14-multi-effect-interp.md) | State + Error interpreter | L | M | H | M | ⭐⭐⭐ |
| [A19](A19-extend-interpreter.md) | Extend an interpreter | L | M | H | M | ⭐⭐⭐ |
| [A21](A21-list-comp-synthesis.md) | List-comp enumeration | M | L | M | M | ⭐⭐⭐ |
| [A22](A22-typeclass-instance.md) | Eq/Ord/Show typeclass instance | M | L | M | M | ⭐⭐⭐ |
| [A23](A23-mini-game.md) | Generalised mini-game | M | M | H | M | ⭐⭐⭐⭐ |
| [A09](A09-prelude-reimpl.md) | Reimplement Prelude | H | L | L | M | ⭐⭐⭐ |

### Tier 3 — possible
| # | Archetype | F | D | C | E | ⭐ |
|---|-----------|---|---|---|---|---|
| [A10](A10-fold-reformulation.md) | Fold reformulation | M | L | H | M | ⭐⭐⭐ |
| [A13](A13-pretty-printer.md) | Custom Show pretty-printer | L | M | L | M | ⭐⭐ |
| [A15](A15-writer-trace.md) | Writer trace | L | L | M | L | ⭐⭐ |
| [A16](A16-parser-combinators.md) | Parser combinators | L | H | H | L | ⭐⭐ |
| [A24](A24-applicative-instance.md) | Applicative instance | L | M | H | L | ⭐⭐ |

### Tier 4 — low probability
| # | Archetype | F | D | C | E | ⭐ |
|---|-----------|---|---|---|---|---|
| [A17](A17-zipper.md) | Zipper navigation | L | M | M | L | ⭐ |
| [A18](A18-lazy-memo.md) | Lazy memoisation | L | H | H | L | ⭐ |
| [A20](A20-laws-iso.md) | Iso / retract / laws (theory) | L | M | M | L | ⭐ |

## Likely 5-question composition

Based on the mock test composition (Rose tree, generic Monad, State game, matrix predicate, ADT translation) and the fact that the exam re-uses the mock's archetype set with mutations:

| Slot | Most likely | Backup | Combo |
|------|-------------|--------|-------|
| **Q1** | A01 (tree recursion — 2 sub-parts: predicate + transform) | A11 (BST) | A01 × A05 |
| **Q2** | A03 (`Monad m =>` combinator) | A24 (Applicative) | A03 × A01 |
| **Q3** | A02 (State-monad game) or A23 (mini-game whole) | A14 (multi-effect) | A02 × A23 |
| **Q4** | A04 (matrix predicate) or A08 (env eval) | A07 (codec) | A04 × A23, A08 × A05 |
| **Q5** | A05 (ADT translation) or A06 (Functor instance) | A22 (Eq/Ord instance) | A05 × A01, A06 × A01 |

## Recognition flowchart

```
                       ┌─ Begin: read the question stem ─┐
                       │                                  │
                       ▼                                  │
        ┌──────────────────────────────────┐              │
        │ Q1: Is there a custom data       │              │
        │     type with recursive ctors?   │              │
        └────────┬──────────────────┬──────┘              │
                 │ YES              │ NO                  │
                 ▼                  ▼                     │
    ┌─────────────────────┐  ┌─────────────────┐          │
    │ Q1a: Does it have   │  │ Q1b: [[Int]] or │          │
    │     `instance T`?   │  │   Grid input?   │          │
    └─┬─────────────────┬─┘  └──┬────────────┬─┘          │
      │ YES Functor/Eq  │ NO    │ YES        │ NO         │
      ▼                 ▼       ▼            ▼            │
 ┌─────────┐   ┌─────────────┐  ┌──────┐   ┌──────────┐   │
 │ A06/A22 │   │ Q2: Is the  │  │ A04  │   │ Q3: Is   │   │
 │ A24     │   │ AST type    │  │ A23  │   │ Monad m  │   │
 └─────────┘   │ + a target  │  └──────┘   │ in sig?  │   │
               │ type?       │             └──┬─────┬─┘   │
               └────┬─────┬──┘                │ YES │ NO  │
                    │ YES │ NO                ▼     ▼     │
                    ▼     ▼              ┌──────┐  ┌────┐ │
                  ┌────┐ ┌─────────────┐ │ A03  │  │ Q4 │ │
                  │ A05│ │ Q2a: AST    │ │ A24  │  └─┬──┘ │
                  └────┘ │   + Env arg?│ └──────┘    │    │
                         └─┬────────┬──┘             ▼    │
                           │ YES    │ NO        ┌────────────────┐
                           ▼        ▼           │ Q4: State sig? │
                         ┌────┐  ┌────┐         └────┬─────────┬─┘
                         │A08 │  │A01 │              │ YES     │ NO
                         │A14 │  └────┘              ▼         ▼
                         └────┘                   ┌────┐    ┌────┐
                                                  │A02 │    │ Q5 │
                                                  │A23 │    │... │
                                                  └────┘    │... │
                                                            └────┘
                          (Q5: list comp keyword?       → A21
                           parser combinator keyword?  → A16
                           memo / infinite tree?       → A18
                           Writer / log?               → A15
                           zipper / focus?             → A17
                           prove / iso / retract?      → A20)
```

A faster 4-step protocol:

1. **Tree type defined?** → A01 (probably with A05/A06 add-on).
2. **`State` or `get`/`put` in signature?** → A02 / A23.
3. **`Monad m =>` constraint?** → A03 / A24.
4. **`[[Int]]` or grid input?** → A04 / A23.

If none match in 60s: A07 / A08 / A11 / A12 / A22.

## How to use during the exam

**Step 1 — Read all 5 questions (5 min).** Map each to an archetype. Write `A##` in the margin. Don't start any yet.

**Step 2 — Order by confidence (1 min).** Tackle your strongest archetype first; that bankrolls confidence.

**Step 3 — For each question, open the archetype mentally:**
- Canonical template → adapt by renaming.
- Match the question stem to a Mutation (M1-M10) within the archetype.
- Apply the QuickCheck attack surface checklist BEFORE submitting.
- Re-read Pitfalls before moving on.

## Cross-archetype heat map

Frequency of co-occurrence within course material (Mock + Assignments + Problem Sheets). H/M/L = strength of combination.

|          | A01 | A02 | A03 | A04 | A05 | A06 | A07 | A08 | A11 | A14 | A21 | A23 |
|----------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| **A01**  |  —  |  H  |  H  |  L  |  H  |  H  |  M  |  H  |  H  |  L  |  L  |  M  |
| **A02**  |  H  |  —  |  M  |  L  |  L  |  L  |  L  |  M  |  L  |  H  |  L  |  H  |
| **A03**  |  H  |  M  |  —  |  L  |  L  |  M  |  L  |  M  |  L  |  M  |  L  |  L  |
| **A04**  |  L  |  L  |  L  |  —  |  L  |  L  |  L  |  L  |  L  |  L  |  M  |  H  |
| **A05**  |  H  |  L  |  L  |  L  |  —  |  L  |  M  |  M  |  L  |  L  |  L  |  L  |
| **A06**  |  H  |  L  |  M  |  L  |  L  |  —  |  L  |  L  |  L  |  L  |  L  |  L  |
| **A07**  |  M  |  L  |  L  |  L  |  M  |  L  |  —  |  L  |  L  |  L  |  L  |  L  |
| **A08**  |  H  |  M  |  M  |  L  |  M  |  L  |  L  |  —  |  L  |  H  |  L  |  L  |
| **A11**  |  H  |  L  |  L  |  L  |  L  |  L  |  L  |  L  |  —  |  L  |  M  |  L  |
| **A14**  |  L  |  H  |  M  |  L  |  L  |  L  |  L  |  H  |  L  |  —  |  L  |  L  |
| **A21**  |  L  |  L  |  L  |  M  |  L  |  L  |  L  |  L  |  M  |  L  |  —  |  M  |
| **A23**  |  M  |  H  |  L  |  H  |  L  |  L  |  L  |  L  |  L  |  L  |  M  |  —  |

### Hotspot combos to memorise
- **A01 × A03**: `mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)` — directly testable.
- **A01 × A05**: Mock Q5 `circuit :: Expr -> Circuit`.
- **A01 × A06**: Functor for BT / Rose.
- **A02 × A14**: state + error calculator.
- **A02 × A23**: Mock Q3 (Nim as game state).
- **A04 × A23**: TTT winner.
- **A08 × A14**: eval with `Maybe`/`Either`.
- **A05 × A19**: extending an interpreter with a translation pass.
- **A07 × A12**: Morse encode/decode is also a Tree↔Table conversion.

## Where to look next
- `../question-families/` — per-question-type templates.
- `../trees/` — A01/A11/A18 family.
- `../monads/` — A02/A03/A14/A15.
- `../interpreters/` — A05/A08/A14/A19.
- `../typeclasses/` — A06/A22/A24.
- `../quickcheck/` — per-archetype QC attack surfaces.
- `../exam-day/` — 60-second recognition card.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
