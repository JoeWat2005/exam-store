<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · **pitfalls**

# Pitfalls — Index + 60-second Pre-Submit Check

> The mistakes graded students keep making. Every pitfall here is **concrete** (wrong code + right code) and **priced** (marks lost). Read by severity, not topic.

## How to read these files

- **`HIGH-severity.md`** — marks-killers. One mistake here loses 5+ marks. Read this the night before the exam. P-001 to P-030.
- **`MEDIUM-severity.md`** — silent correctness bugs. Lose 1-4 marks each. The "almost right" category. P-100 to P-199.
- **`LOW-severity.md`** — style / efficiency. Rarely costs marks but kills readability. P-200 to P-299.
- **`per-topic-pitfalls.md`** — Ctrl-F index by topic (Trees / State / Writer / …). Use during the exam after you've recognised the archetype.
- **`signature-pitfalls.md`** — type signature traps. The auto-marker rejects any deviation; read once, internalise.
- **`imports-pitfalls.md`** — what NOT to import + the Safe-Haskell trap.

## Pitfall ID format

Every pitfall has a stable id `P-###`. Cross-references throughout the vault use these. Severity bands:

| Range      | Severity | Cost           |
|------------|----------|----------------|
| P-001..029 | HIGH     | 5-10 marks each|
| P-100..199 | MEDIUM   | 1-4 marks each |
| P-200..299 | LOW      | 0-1 marks each |

## The 60-second pre-submit check

Print this. Run it OUT LOUD before clicking submit. Each line is a known marks-killer.

### Compile gate (do these FIRST — fix everything before opening ghci)

- [ ] **C1.** `ghc -fno-code MockTest.hs` — no errors, no warnings about incomplete patterns
- [ ] **C2.** `ghc -XSafe -XNoGeneralizedNewtypeDeriving -fno-code MockTest.hs` — Safe mode passes
- [ ] **C3.** `{-# LANGUAGE Safe #-}` pragma is **STILL THERE** at top (P-011)
- [ ] **C4.** Module name matches filename exactly (`module MockTest where` in `MockTest.hs`) (P-002)
- [ ] **C5.** Only allowed imports present (Prelude implicit, plus `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`) (P-003)
- [ ] **C6.** `./presubmit.sh MockTest` (or `AssignmentN`) exits 0

### Signature gate (instant-fail otherwise — see `signature-pitfalls.md`)

- [ ] **S1.** Every function signature is **character-for-character** identical to the template. Copy-paste, NEVER retype (P-001)
- [ ] **S2.** No accidental constraints added (`Ord a =>` where template said no constraint)
- [ ] **S3.** No accidental constraints removed (template said `Monad m =>` — keep it)
- [ ] **S4.** No accidental rename (lowercase first letter, plural-vs-singular, etc.) (P-013)

### Universal edge cases (universal attacks — see [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) U1-U10)

- [ ] **E1.** `[]` / `Empty` / `Branch []` / `Nothing` / `""` / `(0,0)` base case handled (P-005, P-009)
- [ ] **E2.** Singleton case tested (`[x]`, `Leaf x`, `Branch [Leaf x]`)
- [ ] **E3.** No `head`/`tail`/`last`/`init`/`!!` without a pattern-match guard
- [ ] **E4.** Arithmetic functions tested on `0`, negative, large
- [ ] **E5.** Division uses `if y == 0 then ...` guard (P-007 family)
- [ ] **E6.** Numeric recursion handles `n <= 0`, not just `n == 0` (P-008)
- [ ] **E7.** Predicates over Empty: ask "is this vacuous truth?" (P-009 for `isBST`)
- [ ] **E8.** `applyNTimes _ _ 0` returns `pure [x]`, NOT `pure []` (P-007)

### Question-specific (for Mock paper layout — adapt to your paper)

- [ ] **M1.** Q1 isNBranching recurses with `&& all (isNBranching n) xs` (P-014)
- [ ] **M2.** Q2 `applyNTimes` base case is `n == 0` returning `do x <- mx; return [x]` (P-007)
- [ ] **M3.** Q3 `gameOver` returns `True` on `(0,0)` — this is a hardcoded marker test worth 4 marks (P-006)
- [ ] **M4.** Q3 `takeTokens` clamps with `max 0 (x-n)` — never goes negative (P-105)
- [ ] **M5.** Q5 ADT translation — copy-paste between `p` and `q` cases CAREFULLY (P-103)

### File hygiene

- [ ] **H1.** No `undefined` left
- [ ] **H2.** No `error "todo"` left
- [ ] **H3.** No `import Test.QuickCheck` or stray IDE auto-imports (P-004 family)
- [ ] **H4.** No commented-out blocks that may confuse the parser

## Pitfall → canonical fix index

| Topic              | Pitfalls                                                | Canonical fix file                          |
|--------------------|---------------------------------------------------------|---------------------------------------------|
| Tree recursion     | P-005, P-009, P-014, P-104, P-108                       | [A01-tree-recursion](../archetypes/A01-tree-recursion.md)          |
| BST                | P-009, P-015, P-101, P-107                              | [A11-bst-ops](../archetypes/A11-bst-ops.md), `trees/`       |
| State games        | P-006, P-105, P-110                                     | [A02-state-game](../archetypes/A02-state-game.md)              |
| Generic Monad      | P-007, P-100, P-102                                     | [A03-generic-monad](../archetypes/A03-generic-monad.md)           |
| ADT translation    | P-103, P-109                                            | [A05-adt-translation](../archetypes/A05-adt-translation.md)         |
| Functor instance   | P-012, P-016                                            | [A06-functor-instance](../archetypes/A06-functor-instance.md)        |
| Matrix predicate   | P-106                                                   | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md)        |
| Writer trace       | P-111                                                   | [A15-writer-trace](../archetypes/A15-writer-trace.md)            |
| Signatures         | P-001, P-013                                            | [signature-pitfalls](signature-pitfalls.md)            |
| Imports / Safe     | P-003, P-004, P-010, P-011                              | [imports-pitfalls](imports-pitfalls.md)              |

## See also

- [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) — what the marker actually generates
- [VAULT-AUDIT](../meta/VAULT-AUDIT.md) — known bugs that lived in the old vault
- [ONE-PAGE-PANIC](../exam-day/ONE-PAGE-PANIC.md) — the screen you open when blank

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
