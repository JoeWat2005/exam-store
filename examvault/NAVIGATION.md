> [examvault](./README.md) · **NAVIGATION**

# NAVIGATION

Every directory in the project, with its README, file count, and a one-line description. Use this page when you forget where something lives.

For a single-page index of the top files per directory (plus exam-day & pitfalls in full), open [MASTER-INDEX](indexes/MASTER-INDEX.md). This page is the directory-level rollup.

---

## Root entry points (7 files)

| File | Purpose |
|---|---|
| [README.md](README.md) | Main vault entry — routing table, directory map, 7-file pin list. |
| [HOME.md](HOME.md) | Friendly first-visitor page — explains how the vault works in 60 seconds. |
| [HOW-TO-USE.md](HOW-TO-USE.md) | Long-form exam workflow — 5-step recognition loop. |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Why the directory split is the way it is. |
| [STATS.md](STATS.md) | Quantitative breakdown — every count. |
| [KNOWLEDGE-MAP.md](KNOWLEDGE-MAP.md) | The 4-axis mental model. |
| **NAVIGATION.md** | This file. |

---

## Sub-directories (13 dirs + 6 JSON graphs)

### `archetypes/` — the 24 exam question shapes

[archetypes/README.md](archetypes/README.md) · 25 files

The 24 archetypes A01–A24 ranked by F·D·C·E composite score. Each file is the canonical template + 5–10 mutations + QuickCheck attacks + pitfalls.

Highlights:
- [A01-tree-recursion](archetypes/A01-tree-recursion.md) — Tier 1, ⭐⭐⭐⭐⭐ (Mock Q1+Q5)
- [A02-state-game](archetypes/A02-state-game.md) — Tier 1, Mock Q3 Nim
- [A03-generic-monad](archetypes/A03-generic-monad.md) — Tier 1, Mock Q2 applyNTimes
- [A23-mini-game](archetypes/A23-mini-game.md) — Tier 2, includes Minimax + alpha-beta

### `question-families/` — the mutation atlas

[question-families/README.md](question-families/README.md) · 25 files (24 families + README)

Each family file holds 11–20+ structurally distinct mutations the examiner could pick. **The dial.**

Highlights:
- [tree-counting-family](question-families/tree-counting-family.md)
- [state-game-family](question-families/state-game-family.md)
- [monad-combinator-family](question-families/monad-combinator-family.md)
- [string-ops-family](question-families/string-ops-family.md) — new in Phase 12

### `trees/` — per-tree-type catalogues

[trees/README.md](trees/README.md) · 12 files

BT, BST, Rose, Expression tree — all standard operations + the BST delete walked trace + functor/fold/traversal/zipper extensions.

Highlights:
- [binary-tree](trees/binary-tree.md)
- [bst](trees/bst.md) + [bst-delete-trace](trees/bst-delete-trace.md)
- [rose-tree](trees/rose-tree.md)
- [expression-tree](trees/expression-tree.md)

### `monads/` — per-monad catalogues

[monads/README.md](monads/README.md) · 14 files

Maybe / Either / State / Writer / Reader / IO / List / MonadError + transformers + multi-effect + monad laws + the 25-combinator reference.

Highlights:
- [state](monads/state.md)
- [writer](monads/writer.md)
- [generic-combinators](monads/generic-combinators.md)
- [transformer-stack-order](monads/transformer-stack-order.md)

### `interpreters/` — eval progression

[interpreters/README.md](interpreters/README.md) · 17 files

The Pure → Maybe → Either → Reader → State → Writer → Multi-effect ladder + imperative-storage + extend-interpreter + parser-chainl1.

Highlights:
- [expr-reader-either](interpreters/expr-reader-either.md)
- [extend-interpreter](interpreters/extend-interpreter.md)
- [parser-chainl1](interpreters/parser-chainl1.md)

### `cross-matrix/` — data × effect

[cross-matrix/README.md](cross-matrix/README.md) · 21 files

Tree × {Maybe, Either, State, Writer, Reader, Monad-m}; BST × {State, Writer}; Rose × {State, Writer}; Expr × {Maybe, State, Multi}; List × everything; game × State; parser × Either; writer × Either.

Highlights:
- [tree-x-state](cross-matrix/tree-x-state.md) — canonical labelling
- [tree-x-generic-monad](cross-matrix/tree-x-generic-monad.md) — `mapMTree`
- [list-x-list-monad](cross-matrix/list-x-list-monad.md) — non-determinism
- [game-state](cross-matrix/game-state.md) — Nim / TTT / Conway

### `typeclasses/` — class-by-class

[typeclasses/README.md](typeclasses/README.md) · 11 files

Functor / Applicative / Monad / Alternative / Foldable / Traversable / Eq-Ord / Show / Num / Monoid.

Highlights:
- [functor](typeclasses/functor.md)
- [applicative](typeclasses/applicative.md)
- [traversable](typeclasses/traversable.md)

### `quickcheck/` — attack surface

[quickcheck/README.md](quickcheck/README.md) · 17 files

15 per-topic attack files (trees, BST, Rose, Expr, matrix, lists, Maybe/Either, State, Writer, monad, interp, codec, numeric, typeclass-instance) + the master QUICKCHECK-ATTACKS + PROPERTY-PATTERNS (real `prop_*` + Arbitrary instances).

Highlights:
- [QUICKCHECK-ATTACKS](quickcheck/QUICKCHECK-ATTACKS.md) — final pre-submit pass
- [PROPERTY-PATTERNS](quickcheck/PROPERTY-PATTERNS.md) — `Arbitrary` for BT / Rose / Expr

### `pitfalls/` — marks-killers

[pitfalls/README.md](pitfalls/README.md) · 7 files

Anchored P-001 … P-068 across HIGH (30) + MEDIUM (21) + LOW (17) severity tiers + per-topic + signature + imports pitfalls.

Highlights:
- [HIGH-severity](pitfalls/HIGH-severity.md) — the 30 most-expensive mistakes
- [signature-pitfalls](pitfalls/signature-pitfalls.md) — the 5 Mock-Q sigs verbatim
- [imports-pitfalls](pitfalls/imports-pitfalls.md) — what `-XSafe` forbids

### `indexes/` — entry doors

[indexes/README.md](indexes/README.md) · 15 files

Every reverse lookup the vault offers. **The most-loaded directory.**

| Index | One-line |
|---|---|
| [MASTER-INDEX](indexes/MASTER-INDEX.md) | Single-page Ctrl-F of the top files per directory (exam-day & pitfalls in full) |
| [IF-YOU-SEE-X](indexes/IF-YOU-SEE-X.md) | 344 trigger phrases → archetype |
| [KEYWORD-INDEX](indexes/KEYWORD-INDEX.md) | 412 keywords → file |
| [TYPE-SIGNATURE-DATABASE](indexes/TYPE-SIGNATURE-DATABASE.md) | 272 sig shapes → archetype |
| [TYPES-REFERENCE](indexes/TYPES-REFERENCE.md) | Every `Types.hs` ADT |
| [MOCK-Q-INDEX](indexes/MOCK-Q-INDEX.md) | Q1–Q5 spec + marker quirks + canonical |
| [PROBLEM-NUMBER-INDEX](indexes/PROBLEM-NUMBER-INDEX.md) | Problems 1–150 → archetype + file |
| [LECTURE-INDEX](indexes/LECTURE-INDEX.md) | Lecture → topic → archetype |
| [PRELUDE-INDEX](indexes/PRELUDE-INDEX.md) | 200+ Prelude / `Data.*` functions |
| [ASSIGNMENT-INDEX](indexes/ASSIGNMENT-INDEX.md) | A1 / A2 / A3 / MockTest |
| [BEGINNER-INDEX](indexes/BEGINNER-INDEX.md) | Linear cold-start reading path |
| [ARCHETYPE-INDEX](indexes/ARCHETYPE-INDEX.md) | A01–A24 per-archetype hop list |
| [CROSS-TOPIC-INDEX](indexes/CROSS-TOPIC-INDEX.md) | Data × monad matrix |
| [MUTATION-INDEX](indexes/MUTATION-INDEX.md) | Every mutation across every family |

### `haskell-basics/` — cold-start refresher

[haskell-basics/README.md](haskell-basics/README.md) · 48 files

Beginner-accessible primitives. Pattern matching, guards, recursion, HOFs, ADTs, monad basics, plus testing recipes, GHCi reference, allowed-builtins, and the new GHC-error-decoder.

Categories:
- **Syntax** (8) — pattern-matching, guards, if, let-in, where, case, tuples, local-defs
- **Data** (5) — lists, strings, recursion, accumulator-recursion, helper-functions
- **HOFs** (6) — list-comprehensions, higher-order-functions, lambdas, function-composition, currying, partial-application
- **Operators** (3) — `$`, `.`, sections
- **Types** (5) — type-signatures, polymorphism, ADTs, recursive-data-types, deriving
- **Effects** (3) — maybe-basics, either-basics, do-notation-basics
- **Std HOFs** (7) — map, filter, foldr, foldl, zip, zipWith, all-any
- **Testing & tools** (9) — testing-functions (×4), ghci-commands, allowed-builtins, safe-haskell, common-templates, [ghc-error-decoder](haskell-basics/ghc-error-decoder.md)

### `exam-day/` — last-mile workflows

[exam-day/README.md](exam-day/README.md) · 8 files

Night-before → during-exam → submit routing.

| File | Use when |
|---|---|
| [EXAM-DAY-ROUTE](exam-day/EXAM-DAY-ROUTE.md) | Minute-by-minute 2h playbook |
| [IN-EXAM-WORKFLOW](exam-day/IN-EXAM-WORKFLOW.md) | Per-question 22-min loop |
| [LAST-HOUR-CHECKLIST](exam-day/LAST-HOUR-CHECKLIST.md) | T-60 to T-0 routine |
| [ONE-PAGE-PANIC](exam-day/ONE-PAGE-PANIC.md) | Single-screen panic reference |
| [RECOGNITION-FLOWCHART](exam-day/RECOGNITION-FLOWCHART.md) | ASCII decision tree |
| [TIME-BUDGET](exam-day/TIME-BUDGET.md) | 2h allocation strategy |
| [WHAT-TO-PIN](exam-day/WHAT-TO-PIN.md) | 10 browser-tab priorities |

### `meta/` — vault audits + reports

[meta/README.md](meta/README.md) · 8 files

| File | Purpose |
|---|---|
| [COURSE-MAP](meta/COURSE-MAP.md) | Lecture → topic → archetype mapping |
| [COURSE-COVERAGE](meta/COURSE-COVERAGE.md) | Lecture-file → vault-file mapping |
| [VAULT-AUDIT](meta/VAULT-AUDIT.md) | Notehost-vault → examvault comparison |
| [GAP-AUDIT](meta/GAP-AUDIT.md) | Verified content gaps (G-01 … G-08) |
| [WIKI-UPGRADE-REPORT](meta/WIKI-UPGRADE-REPORT.md) | Phase 0–8 deliverables |
| [SCRIPT-COMPATIBILITY-REPORT](meta/SCRIPT-COMPATIBILITY-REPORT.md) | 9/9 scripts PASS |
| [FINAL-SWEEP-REPORT](meta/FINAL-SWEEP-REPORT.md) | Completion certificate |

### `scripts/` — Python helpers + vLab setup

[scripts/README.md](scripts/README.md) · 27 items: 24 `.py` (9 user-facing + 15 internal phase/audit) + vlab-setup.sh + 2 `.md`

Full usage with examples: **[scripts/SCRIPTS-GUIDE.md](scripts/SCRIPTS-GUIDE.md)**.

| Script | Purpose |
|---|---|
| `search_by_archetype.py A##` | A##'s combinations + frequency |
| `search_by_type.py "<sig>"` | Sig → archetype |
| `search_by_monad.py <name>` | Monad relationships |
| `search_by_combo.py "X + Y"` | Cross-axis lookup |
| `search_by_keyword.py <kw>` | Ranked keyword search |
| `mock_q_lookup.py Q[1-5]` | Mock-Q spec + marker quirk |
| `prelude_lookup.py <fn>` | `Prelude` / `Data.*` lookup |
| `study_planner.py <days>` | Personalised revision plan |
| `topic_dependencies.py <topic>` | Prerequisites |
| `vlab-setup.sh` | One-shot JupyterLab config |

### `graphs/` — machine-readable JSON (no README)

[graphs/](graphs/) · 6 JSON files

Used by `scripts/search_*.py`. Reserved for future embedding tooling.

| Graph | Nodes | Edges |
|---|---:|---:|
| TOPIC | 52 | 130 |
| ARCHETYPE | 24 | 282 |
| MONAD | 30 | 79 |
| TREE | 30 | 70 |
| QUESTION | 28 | 69 |
| DEPENDENCY | 54 | 98 |

---

## Every README in the project, alphabetically

For one-click hop:

- [archetypes/README.md](archetypes/README.md)
- [cross-matrix/README.md](cross-matrix/README.md)
- [exam-day/README.md](exam-day/README.md)
- [haskell-basics/README.md](haskell-basics/README.md)
- [indexes/README.md](indexes/README.md)
- [interpreters/README.md](interpreters/README.md)
- [meta/README.md](meta/README.md)
- [monads/README.md](monads/README.md)
- [pitfalls/README.md](pitfalls/README.md)
- [question-families/README.md](question-families/README.md)
- [quickcheck/README.md](quickcheck/README.md)
- [scripts/README.md](scripts/README.md)
- [trees/README.md](trees/README.md)
- [typeclasses/README.md](typeclasses/README.md)
- [README.md](README.md) — root

---

## See also

**Friendly entry:** [HOME](HOME.md)
**Long-form exam workflow:** [HOW-TO-USE](HOW-TO-USE.md)
**4-axis model:** [KNOWLEDGE-MAP](KNOWLEDGE-MAP.md)
**Master file index:** [MASTER-INDEX](indexes/MASTER-INDEX.md)
**Stats:** [STATS](STATS.md)
**Scripts examples:** [scripts/SCRIPTS-GUIDE](scripts/SCRIPTS-GUIDE.md)
