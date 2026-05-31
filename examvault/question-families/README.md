<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · **question-families**

# Question Families — Exam Mutation Vault

Most students study *archetypes* (one canonical solution per topic). Few study *mutations* (the dial the examiner actually turns). This directory is the mutation atlas: each family file holds one generator and 5–10 sibling problems that share its recursion structure but differ in spec/twist.

## How to use

1. Identify the *shape* of the exam stem (recursive tree predicate? interpret an ADT? thread a state?).
2. Look it up in the **stem-keyword lookup table** below.
3. Open the matching family file and skim the mutations. The examiner picked *one* of those rows.
4. Use the listed pitfalls + QC universal attacks to debug.

---

## Heat map: which 5 families are MOST likely to appear

Based on the 2024 mock test (which mirrors exam structure) and Assignments 1–3:

| Rank | Family | Mock/Assignment basis | Stars |
|------|--------|------------------------|-------|
| 1 | `monad-combinator-family.md` | Mock Q2 (applyNTimes), Assignment 3 (Free monad combinators) | ⭐⭐⭐⭐ |
| 2 | `state-game-family.md` | Mock Q3 (Nim), Assignment 3 (roundRobin scheduler) | ⭐⭐⭐⭐ |
| 3 | `rose-ops-family.md` | Mock Q1 (isNBranching, prune), Assignment 3 (toRose/fromRose) | ⭐⭐⭐ |
| 4 | `adt-translation-family.md` | Mock Q5 (circuit), Assignment 2 (ramify/tabulate) | ⭐⭐⭐⭐ |
| 5 | `matrix-predicate-family.md` | Mock Q4 (isMagicSquare), problem 150 (TicTacToe) | ⭐⭐⭐ |

If exam time is short, study those five first.

The next-most-likely (B-tier, almost every exam picks one):

| Rank | Family | Basis |
|------|--------|-------|
| 6 | `tree-counting-family.md` | Problems 71, 73, 78, 80 — every list of practice problems opens here |
| 7 | `env-eval-family.md` | Problems 89, 148 — interpreters are the bread-and-butter of FP exams |
| 8 | `tree-validation-family.md` | Problems 81 (isBST), 143 (isNBranching) |
| 9 | `codec-family.md` | Assignment 2 (Morse), problem 147 (RLE) |
| 10 | `applicative-monad-instance-family.md` | Problems 121–124 — almost guaranteed at least one custom instance |

---

## Archetype → families lookup table

Each archetype maps to 1–3 families. When you recognise an exam question as "this is archetype A##", check those families.

| Archetype | Description | Primary family | Related |
|-----------|-------------|----------------|---------|
| A01 | Recursion on `[a]` (`[]` vs `x:xs`) | `list-rewrite-family.md` | `list-fold-family.md` |
| A02 | foldr/foldl over list | `list-fold-family.md` | `list-rewrite-family.md` |
| A03 | Structural fold over BT/Rose | `tree-counting-family.md` | `rose-ops-family.md` |
| A04 | Structural predicate over BT/Rose | `tree-validation-family.md` | `bst-ops-family.md`, `rose-ops-family.md` |
| A05 | Structural map / prune | `tree-transform-family.md` | `bst-ops-family.md`, `rose-ops-family.md` |
| A06 | BT/Rose → list (flatten) | `tree-extract-family.md` | `rose-ops-family.md` |
| A07 | List comprehension with multi-generator | `list-comp-family.md` | `matrix-predicate-family.md` |
| A08 | Grid/matrix predicate ([[a]]) | `matrix-predicate-family.md` | `list-comp-family.md` |
| A09 | ADT → ADT translation | `adt-translation-family.md` | `pretty-print-family.md`, `codec-family.md` |
| A10 | Eval Expr with variables/env | `env-eval-family.md` | `adt-translation-family.md`, `error-handling-family.md` |
| A11 | Monadic combinator (apply n times, mapM…) | `monad-combinator-family.md` | `state-game-family.md`, `writer-trace-family.md` |
| A12 | State / Writer monad on domain world | `state-game-family.md` | `state-counter-family.md`, `writer-trace-family.md` |
| A13 | Custom typeclass instance | `functor-instance-family.md` | `applicative-monad-instance-family.md` |
| A14 | Encode/decode with table | `codec-family.md` | `adt-translation-family.md`, `parser-family.md` |
| A15 | Maybe / Either error handling | `error-handling-family.md` | `env-eval-family.md` |
| A16 | Show / display / pretty-print | `pretty-print-family.md` | `adt-translation-family.md`, `parser-family.md` |
| A17 | Parser combinators | `parser-family.md` | `pretty-print-family.md`, `codec-family.md` |
| A18 | Lazy / infinite data | `lazy-infinite-family.md` | `monad-combinator-family.md` |

---

## Exam-stem keyword lookup table

Given the exam stem says **X**, look at family **Y**.

| Stem keyword | Family |
|---|---|
| "count" / "how many" / "number of" | `tree-counting-family.md` or `list-rewrite-family.md` (sum) |
| "True iff" / "predicate" / "decide if" | `tree-validation-family.md` or `matrix-predicate-family.md` |
| "mirror" / "swap" / "transform every node" | `tree-transform-family.md` |
| "in-order" / "pre-order" / "post-order" / "flatten" | `tree-extract-family.md` |
| "Pythagorean" / "factors" / "perfect" / "all pairs" | `list-comp-family.md` |
| "re-implement Prelude" / "without using length" | `list-rewrite-family.md` |
| "using foldr" / "using foldl" / "scan" | `list-fold-family.md` |
| "sequence" / "mapM" / "replicateM" / "apply n times" | `monad-combinator-family.md` |
| "Nim" / "TicTacToe" / "state monad" / "game" | `state-game-family.md` |
| "fresh" / "labelTree" / "counter" / "unique id" | `state-counter-family.md` |
| "magic square" / "Sudoku" / "winner" / "grid" / "transpose" | `matrix-predicate-family.md` |
| "circuit" / "Nand" / "translate Expr" / "desugar" | `adt-translation-family.md` |
| "Var" / "Let" / "environment" / "evaluate Expr" / "scope" | `env-eval-family.md` |
| "Morse" / "Caesar" / "RLE" / "encode/decode" | `codec-family.md` |
| "BST" / "insert/delete/member" / "binary search" | `bst-ops-family.md` |
| "Rose tree" / "isNBranching" / "prune" / "n children" | `rose-ops-family.md` |
| "Functor" / "fmap" / "instance Functor" | `functor-instance-family.md` |
| "Applicative" / "<*>" / "Monad" / ">>=" / "custom instance" | `applicative-monad-instance-family.md` |
| "Writer" / "tell" / "log" / "trace" / "audit" | `writer-trace-family.md` |
| "safe" / "Maybe" / "Either" / "error" / "divide by zero" | `error-handling-family.md` |
| "Show" / "display" / "pretty" / "render" / "precedence" | `pretty-print-family.md` |
| "Parser" / "parse" / "well-bracketed" / "grammar" | `parser-family.md` |
| "infinite" / "ones" / "fibs" / "iterate" / "lazy" / "fix" | `lazy-infinite-family.md` |

---

## Family-to-mutation-count summary

> Cap raised from 12 to 25 per family in Phase 12. Current totals reflect the Phase-4 expansion (+28) and Phase-12 expansion (+28 from the new `string-ops-family` and tree-family mutation deepening).

| Family | Mutations | Hidden-pred? | Acc alt? | Fold alt? |
|---|---|---|---|---|
| tree-counting-family | 17 | yes | yes | yes |
| tree-validation-family | 17 | yes | yes | partial |
| tree-transform-family | 16 | yes | partial | yes |
| tree-extract-family | 11 | yes | yes | yes |
| list-rewrite-family | 12 | yes | yes | yes |
| list-fold-family | 12 | yes | yes (foldl') | n/a |
| list-comp-family | 11 | yes | n/a | yes |
| monad-combinator-family | 12 | yes | yes (CPS) | yes |
| state-game-family | 12 | yes | yes (pure) | yes (mapM_) |
| state-counter-family | 11 | yes | yes (pure) | n/a |
| matrix-predicate-family | 12 | yes | partial | partial |
| adt-translation-family | 12 | yes | yes (memo) | partial |
| env-eval-family | 11 | yes | yes (State) | partial |
| codec-family | 12 | yes | yes | yes (group) |
| bst-ops-family | 12 | yes | yes | partial |
| rose-ops-family | 11 | yes | yes | yes |
| functor-instance-family | 11 | n/a | n/a | partial |
| applicative-monad-instance-family | 11 | n/a | n/a | yes |
| writer-trace-family | 11 | yes | yes (pure pair) | yes (foldM) |
| error-handling-family | 12 | yes | yes (foldM) | yes |
| pretty-print-family | 11 | yes | yes (ShowS) | partial |
| parser-family | 11 | yes | yes (chainl1) | partial |
| lazy-infinite-family | 12 | n/a | yes (unfoldr) | yes (CPS) |
| **string-ops-family** (new in Phase 12) | **13** | yes | partial | partial |
| **TOTAL** | **293** | | | |

---

## Reading order (if you do them all)

For exam preparation in 5–7 days:

**Day 1 — the warm-ups:**
- `list-rewrite-family.md`
- `list-fold-family.md`
- `list-comp-family.md`

**Day 2 — the BT empire:**
- `tree-counting-family.md`
- `tree-validation-family.md`
- `tree-transform-family.md`
- `tree-extract-family.md`

**Day 3 — extensions to BT/rose:**
- `bst-ops-family.md`
- `rose-ops-family.md`

**Day 4 — monads, instances:**
- `functor-instance-family.md`
- `applicative-monad-instance-family.md`
- `monad-combinator-family.md`

**Day 5 — state and writer:**
- `state-game-family.md`
- `state-counter-family.md`
- `writer-trace-family.md`
- `error-handling-family.md`

**Day 6 — the heavy stuff (translation, env-eval, codec):**
- `adt-translation-family.md`
- `env-eval-family.md`
- `codec-family.md`
- `matrix-predicate-family.md`

**Day 7 — exam-specific (laziness, pretty/parse, string ops):**
- `pretty-print-family.md`
- `parser-family.md`
- `lazy-infinite-family.md`
- `string-ops-family.md` *(new in Phase 12 — palindrome, letterFreqs, anagram, splitOn, capitalise, …)*

Plus the **mock test cold** at the very end.

---

## Cross-cutting principles

These show up in *every* family:

1. **Empty case first.** Every recursion has an empty/base case. Get it wrong and nothing else matters.
2. **Pattern-match order.** Specific cases (`Fork _ Empty Empty`) before general ones (`Fork _ l r`). Otherwise the specific case is unreachable.
3. **Predicate parameter:** the examiner's favourite twist is "instead of value equality, take a predicate". See "Hidden-predicate mutations" in every file.
4. **Accumulator vs structural recursion:** examiner sometimes asks "why is your version slow?" → answer with the accumulator alternative.
5. **`flatten` is universal:** many predicates can be expressed as `predOnList . flatten`. Sometimes that's the simplest answer.
6. **Monad laws as QC properties:** every monad instance must satisfy left-id, right-id, associativity. Free property tests.
7. **Avoid `length` when O(1) info suffices.** `null xs` instead of `length xs == 0`, etc.

---

## What this directory does NOT cover

- IO problems (problems 101–104, 110): no mutations because IO doesn't generate a family — the spec varies wildly.
- One-shot puzzles (problems 60 crack, 64 hex, 137 fix specifically): partly mentioned but not given families because they're shape-unique.
- Course-specific paperwork (presubmit.sh, package.yaml structure): see `fp-learning-2025/files/Assignments/*/README.md`.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
