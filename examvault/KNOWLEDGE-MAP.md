<!-- topnav:start -->
> **Quick nav:** [HOME](HOME.md) · [NAVIGATION](NAVIGATION.md) · [MASTER-INDEX](indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](./README.md) · **KNOWLEDGE-MAP**

# KNOWLEDGE-MAP

A single-page overview of the four orthogonal axes the vault is built on. **Use this when** you want to understand *how* the vault is organised, not just *what* it contains.

For the routing table ("which file do I open?") see [README.md](README.md). For task-mode routing ("I'm in the exam right now") see [HOW-TO-USE.md](HOW-TO-USE.md).

---

## The four axes

```
                 ┌───────────────────────────────────────────────┐
                 │                                               │
                 │    ARCHETYPE         MUTATION                 │
                 │    (the shape)       (the dial)               │
                 │       │                  │                    │
                 │       ▼                  ▼                    │
                 │     A01..A24      293 mutations               │
                 │                                               │
                 │                                               │
                 │    TOPIC             TYPE SIGNATURE           │
                 │    (the domain)      (the fingerprint)        │
                 │       │                  │                    │
                 │       ▼                  ▼                    │
                 │   trees/, monads/    `Monad m => ... -> m a`  │
                 │   interpreters/      `BT a -> Int`            │
                 │   typeclasses/       `Expr -> Maybe Int`      │
                 │                                               │
                 └───────────────────────────────────────────────┘
```

Every leaf file is reachable from at least three of the four axes — that redundancy is what makes the vault usable under exam pressure (any cold-start phrase routes you somewhere).

---

## Axis 1 — Archetype

The *shape* of the exam question. There are 24 archetypes (A01–A24). Every past exam question and the entire mock test can be classified.

- **Entry:** [indexes/ARCHETYPE-INDEX](indexes/ARCHETYPE-INDEX.md) — A01…A24 with template, mutations, and crossings.
- **Per-archetype:** [`archetypes/A##-*.md`](archetypes/README.md) — 1 canonical file each.
- **Priority + composition:** [archetypes/README](archetypes/README.md) — F·D·C·E scoring, recognition flowchart.
- **Mock paper:** [indexes/MOCK-Q-INDEX](indexes/MOCK-Q-INDEX.md) — five-question composition seen in the 2024/25 mock.

If you have only one mental hook for the exam, it should be the archetype number.

---

## Axis 2 — Mutation

What the examiner *changes* inside an archetype. There are 293 mutations across 24 families (25 cap per family). The examiner picks one row from one family.

- **Entry:** [indexes/MUTATION-INDEX](indexes/MUTATION-INDEX.md) — every mutation listed.
- **Per-family:** [`question-families/*.md`](question-families/README.md) — 5–12 mutations each with code.
- **Mutation difficulty:** [MUTATION-INDEX § Difficulty tiers](indexes/MUTATION-INDEX.md#difficulty-tiers-across-families).
- **Phase-4 additions:** see [meta/WIKI-UPGRADE-REPORT](meta/WIKI-UPGRADE-REPORT.md) — 28 new mutations introduced in the 2026-05-29 sweep.

---

## Axis 3 — Topic

The domain the lecture taught. The course covers lists, trees, recursion, ADTs, list comprehensions, higher-order functions, monads (Maybe / Either / State / Writer / Reader / List / IO), transformers, interpreters, parser combinators, lazy evaluation, and typeclasses (Functor / Applicative / Monad / Foldable / Traversable / Eq / Ord / Show / Num / Monoid).

- **Tree topic:** [trees/](trees/README.md) — BT, BST, Rose, Expression tree, zipper.
- **Monad topic:** [monads/](monads/README.md) — per-monad files + laws + transformers + multi-effect.
- **Interpreter topic:** [interpreters/](interpreters/README.md) — Pure → Maybe → Either → Reader → State → Writer → Multi.
- **Typeclass topic:** [typeclasses/](typeclasses/README.md) — class-by-class.
- **Crossing axes:** [cross-matrix/](cross-matrix/README.md) — data structure × effect.
- **Course mapping:** [meta/COURSE-MAP](meta/COURSE-MAP.md) — lecture file → topic → archetype.
- **Lecture-level coverage:** [meta/COURSE-COVERAGE](meta/COURSE-COVERAGE.md).

For *beginners* there's a separate refresher tree at [haskell-basics/](haskell-basics/README.md) (48 cold-start pages).

---

## Axis 4 — Type signature

The syntactic fingerprint on the exam page. Often the signature alone reveals the technique.

- **Entry:** [indexes/TYPE-SIGNATURE-DATABASE](indexes/TYPE-SIGNATURE-DATABASE.md) — every sig pattern → archetype.
- **Per-sig recognition:** [haskell-basics/type-signatures](haskell-basics/type-signatures.md).
- **ADT shapes used in the course:** [indexes/TYPES-REFERENCE](indexes/TYPES-REFERENCE.md).
- **The seven Mock signatures:** [pitfalls/signature-pitfalls](pitfalls/signature-pitfalls.md).

---

## The 8 entry indexes (alphabetically)

| Index | Use when |
|---|---|
| [ARCHETYPE-INDEX](indexes/ARCHETYPE-INDEX.md) | You know the archetype number |
| [BEGINNER-INDEX](indexes/BEGINNER-INDEX.md) | You're cold; want a linear reading order |
| [CROSS-TOPIC-INDEX](indexes/CROSS-TOPIC-INDEX.md) | The question crosses two axes (e.g. "label tree with State") |
| [IF-YOU-SEE-X](indexes/IF-YOU-SEE-X.md) | You have a phrase from the question stem |
| [KEYWORD-INDEX](indexes/KEYWORD-INDEX.md) | You remember a Haskell keyword (`do`, `where`, `case`) |
| [MASTER-INDEX](indexes/MASTER-INDEX.md) | One-page Ctrl-F of every file |
| [MUTATION-INDEX](indexes/MUTATION-INDEX.md) | You know the archetype, want the variant list |
| [TYPE-SIGNATURE-DATABASE](indexes/TYPE-SIGNATURE-DATABASE.md) | Only the type sig is given |

Specialist indexes when the above don't fit:

| Index | Use when |
|---|---|
| [PROBLEM-NUMBER-INDEX](indexes/PROBLEM-NUMBER-INDEX.md) | The lecturer referenced practice problem #N |
| [LECTURE-INDEX](indexes/LECTURE-INDEX.md) | You remember which lecture covered it |
| [PRELUDE-INDEX](indexes/PRELUDE-INDEX.md) | You forgot a Prelude / `Data.List` / `Data.Char` function |
| [ASSIGNMENT-INDEX](indexes/ASSIGNMENT-INDEX.md) | Recalling A1 / A2 / A3 |
| [MOCK-Q-INDEX](indexes/MOCK-Q-INDEX.md) | Working through the 2024 mock |

---

## Vault directory at a glance

| Directory | Files | What it carries | Axis |
|---|---:|---|---|
| [archetypes/](archetypes/README.md) | 25 | A01–A24 canonical templates + priority README | Archetype |
| [question-families/](question-families/README.md) | 25 | 293 mutations across 24 families | Mutation |
| [trees/](trees/README.md) | 12 | BT / BST / Rose / Expr per-op catalogues | Topic |
| [monads/](monads/README.md) | 14 | Per-monad files + laws + transformers | Topic |
| [interpreters/](interpreters/README.md) | 17 | Eval progression Pure → Multi-effect + parser | Topic |
| [typeclasses/](typeclasses/README.md) | 11 | Functor → Monad → Foldable → Traversable | Topic |
| [cross-matrix/](cross-matrix/README.md) | 21 | Topic × Effect (Tree×State, etc.) | Cross |
| [haskell-basics/](haskell-basics/README.md) | 48 | Cold-start refresher (pattern-matching, recursion, …) | Topic |
| [quickcheck/](quickcheck/QUICKCHECK-ATTACKS.md) | 17 | Per-topic attack DB + Property patterns | Defensive |
| [pitfalls/](pitfalls/HIGH-severity.md) | 7 | 68 anchored marks-killers (P-001 … P-068) | Defensive |
| [indexes/](indexes/README.md) | 15 | The 15 entry indexes (see above) | Routing |
| [exam-day/](exam-day/README.md) | 8 | ONE-PAGE-PANIC, EXAM-DAY-ROUTE, TIME-BUDGET | Routing |
| [meta/](meta/README.md) | 8 | COURSE-MAP, COURSE-COVERAGE, audits | Routing |
| [graphs/](graphs/) | 6 | JSON knowledge graphs (218 nodes, 728 edges) | Routing |
| [scripts/](scripts/README.md) | 9 user-facing (24 `.py` total) | Python helpers (`search_by_*`, `study_planner`, …) + phase/audit scripts | Routing |

---

## How the axes connect — one worked example

You read on the exam paper:

> Write `labelTree :: BT a -> State Int (BT (a, Int))` that gives every node a fresh integer in in-order.

Hop 1 — **Type sig** → [TYPE-SIGNATURE-DATABASE](indexes/TYPE-SIGNATURE-DATABASE.md) — `BT a -> State Int ...` matches **A01 × A02** ([Tree-recursion × State-game]).

Hop 2 — **Cross** → [tree-x-state](cross-matrix/tree-x-state.md) — canonical `labelTree` template.

Hop 3 — **Archetype** → [A01](archetypes/A01-tree-recursion.md) for the recursion shape; [A02](archetypes/A02-state-game.md) for the State usage.

Hop 4 — **Mutation** → [state-counter-family](question-families/state-counter-family.md) Mutation 4 (in-order) vs Mutation 5 (pre-order) — examiner pick.

Hop 5 — **Topic depth** → [state.md](monads/state.md) for `get` / `put` / `modify`, [binary-tree.md](trees/binary-tree.md) for traversal shapes.

Hop 6 — **Defensive** → [trees-attacks.md](quickcheck/trees-attacks.md) (edge: `Empty`); [state-attacks.md](quickcheck/state-attacks.md) (edge: empty tree → `0` counter unchanged).

Hop 7 — **Submit** → [exam-day/IN-EXAM-WORKFLOW.md](exam-day/IN-EXAM-WORKFLOW.md) + [pitfalls/signature-pitfalls.md](pitfalls/signature-pitfalls.md).

Seven hops, all under 30 seconds each.

---

## Knowledge graphs (JSON)

For programmatic / embedding use:

| Graph | Nodes | Edges | Purpose |
|---|---:|---:|---|
| `TOPIC-GRAPH.json` | 52 | 130 | Topic prerequisites |
| `ARCHETYPE-GRAPH.json` | 24 | 282 | Archetype combinations |
| `MONAD-GRAPH.json` | 30 | 79 | Monad relationships |
| `TREE-GRAPH.json` | 30 | 70 | Tree-type relationships |
| `QUESTION-GRAPH.json` | 28 | 69 | Question families |
| `DEPENDENCY-GRAPH.json` | 54 | 98 | Cross-file prerequisites |

Used by `scripts/search_*.py`. Reserved for future embedding / vector tooling.

---

## See also

**Routing table:** [README](README.md)
**Exam workflow:** [HOW-TO-USE](HOW-TO-USE.md)
**Architecture rationale:** [ARCHITECTURE](ARCHITECTURE.md)
**Stats + count:** [STATS](STATS.md)
**Course mapping:** [meta/COURSE-MAP](meta/COURSE-MAP.md)
**Course coverage audit:** [meta/COURSE-COVERAGE](meta/COURSE-COVERAGE.md)
**Last-hour plan:** [exam-day/LAST-HOUR-CHECKLIST](exam-day/LAST-HOUR-CHECKLIST.md)
**Panic mode:** [exam-day/ONE-PAGE-PANIC](exam-day/ONE-PAGE-PANIC.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](HOME.md) · [NAVIGATION](NAVIGATION.md) · [MASTER-INDEX](indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
