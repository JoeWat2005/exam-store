<!-- topnav:start -->
> **Quick nav:** [HOME](HOME.md) · [NAVIGATION](NAVIGATION.md) · [MASTER-INDEX](indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](./README.md) · **examvault stats**

# examvault stats

**Generated:** 2026-05-29 · **Updated:** 2026-05-31 (post final sweep + GHC error decoder)

Quantitative breakdown of everything in the vault. Use this page to answer "how many of X do I have?" / "which family is densest?" / "where am I undercovered?". Numbers are auto-grepped at update time, not hand-curated.

---

## High-level totals

| Metric | Value |
|---|---:|
| Total `.md` files | 238 |
| Internal markdown links | **~11,959** (markdown links; checker skips `scripts/` and `graphs/` and excludes `#`-anchors) |
| Broken internal links | 3 (intentional template placeholders) |
| Archetypes (A01–A24) | 24 |
| Question families | **24** (includes Phase-12 `string-ops-family`) |
| **Mutations across all families** | **293** (cap 25 / family) |
| Cross-matrix files (data × monad) | 21 |
| Per-topic QuickCheck attack files | 15 (+ master + PROPERTY-PATTERNS) |
| Pitfalls anchored (HIGH + MEDIUM + LOW) | 30 + 21 + 17 = **68** |
| `haskell-basics/` pages | 48 |
| Helper Python scripts | 9 user-facing + phase tooling |
| Machine-readable graphs (JSON) | 6 |

---

## File counts by directory

| Directory | Files | Coverage |
|-----------|------:|----------|
| `archetypes/` | 25 | 24 archetypes (A01–A24) + priority README |
| `question-families/` | 25 | 293 mutations across 24 families (cap 25/family) |
| `trees/` | 12 | BT / BST / Rose / Expr + functor/fold/traversal/zipper + bst-delete-trace |
| `monads/` | 14 | 7 base monads + transformers + multi-effect + laws + 25-combinator reference + transformer-stack-order |
| `interpreters/` | 17 | Pure → multi-effect progression + imperative-storage + extend/desugar/parse + parser-chainl1 |
| `cross-matrix/` | 21 | Tree×{Maybe,Either,State,Writer,Reader,Monad-m}; BST×{State,Writer}; Rose×{State,Writer}; Expr×{Maybe,State,Multi}; List×{Monad,State,Writer,List-Monad}; game-state; parser×Either; writer×Either |
| `typeclasses/` | 11 | Functor / Applicative / Monad / Alternative / Foldable / Traversable / Eq-Ord / Show / Num / Monoid |
| `quickcheck/` | 17 | Master + 14 per-topic + numeric + typeclass-instance attacks + PROPERTY-PATTERNS |
| `pitfalls/` | 7 | 30 HIGH + 21 MEDIUM + 17 LOW + per-topic + signature + imports (68 anchored `<a id="p-NNN">`) |
| `indexes/` | 15 | MASTER, IF-YOU-SEE-X, TYPE-SIG-DB, KEYWORD, PROBLEM-#, LECTURE, PRELUDE, MOCK-Q, ASSIGNMENT, TYPES-REFERENCE, BEGINNER, ARCHETYPE, CROSS-TOPIC, MUTATION, README |
| `graphs/` | 6 JSON + 1 README | TOPIC, ARCHETYPE, MONAD, TREE, QUESTION, DEPENDENCY + README |
| `scripts/` | 26 | 9 user-facing Python helpers + 15 internal phase/audit scripts (24 `.py` total) + vlab-setup.sh + README |
| `exam-day/` | 8 | ROUTE / PANIC / TIME-BUDGET / FLOWCHART / LAST-HOUR / IN-EXAM-WORKFLOW / WHAT-TO-PIN + README |
| `meta/` | 8 | COURSE-MAP / COURSE-COVERAGE / VAULT-AUDIT / GAP-AUDIT / WIKI-UPGRADE-REPORT / SCRIPT-COMPATIBILITY-REPORT / FINAL-SWEEP-REPORT / README |
| `haskell-basics/` | 48 | 37 syntax/data/HOFs/operators/types/effects/std-HOFs + README + safe-haskell + common-templates + 4 testing pages + ghci-commands + allowed-builtins + **ghc-error-decoder** + sorting |
| **root** | **7** | README, HOME, HOW-TO-USE, ARCHITECTURE, STATS, KNOWLEDGE-MAP, NAVIGATION |
| **Total `.md`** | **238** | excluding 6 JSON graphs and the 24 Python helper/phase scripts |

---

## Mutations per question-family

The dial the examiner turns. **293 mutations** across 24 families; cap is 25/family, average 12.21.

| Family | Mutations | Cap | Archetype | Tier |
|---|---:|---:|---|---|
| [adt-translation](question-families/adt-translation-family.md) | 12 | 25 | A05 | 1 |
| [applicative-monad-instance](question-families/applicative-monad-instance-family.md) | 11 | 25 | A06 / A24 | 1 / 3 |
| [bst-ops](question-families/bst-ops-family.md) | 12 | 25 | A11 | 2 |
| [codec](question-families/codec-family.md) | 12 | 25 | A07 | 2 |
| [env-eval](question-families/env-eval-family.md) | 11 | 25 | A08 / A14 | 1 / 2 |
| [error-handling](question-families/error-handling-family.md) | 12 | 25 | A14 | 2 |
| [functor-instance](question-families/functor-instance-family.md) | 11 | 25 | A06 / A22 | 1 / 2 |
| [lazy-infinite](question-families/lazy-infinite-family.md) | 12 | 25 | A18 | 4 |
| [list-comp](question-families/list-comp-family.md) | 11 | 25 | A21 | 2 |
| [list-fold](question-families/list-fold-family.md) | 12 | 25 | A10 | 3 |
| [list-rewrite](question-families/list-rewrite-family.md) | 12 | 25 | A09 | 3 |
| [matrix-predicate](question-families/matrix-predicate-family.md) | 12 | 25 | A04 | 1 |
| [monad-combinator](question-families/monad-combinator-family.md) | 12 | 25 | A03 | 1 |
| [parser](question-families/parser-family.md) | 11 | 25 | A16 | 3 |
| [pretty-print](question-families/pretty-print-family.md) | 11 | 25 | A13 | 3 |
| [rose-ops](question-families/rose-ops-family.md) | 11 | 25 | A01 | 1 |
| [state-counter](question-families/state-counter-family.md) | 11 | 25 | A02 | 1 |
| [state-game](question-families/state-game-family.md) | 12 | 25 | A02 / A23 | 1 / 2 |
| [string-ops](question-families/string-ops-family.md) | 13 | 25 | A09 / A21 | 2 |
| [tree-counting](question-families/tree-counting-family.md) | 17 | 25 | A01 | 1 |
| [tree-extract](question-families/tree-extract-family.md) | 11 | 25 | A01 / A12 | 1 / 2 |
| [tree-transform](question-families/tree-transform-family.md) | 16 | 25 | A01 | 1 |
| [tree-validation](question-families/tree-validation-family.md) | 17 | 25 | A01 | 1 |
| [writer-trace](question-families/writer-trace-family.md) | 11 | 25 | A15 | 3 |
| **Totals** | **293** | 600 | | |

**Densest families:** tree-validation and tree-counting (17 each), then tree-transform (16) and string-ops (13). **Headroom remaining:** the 25/family cap is generous — most families sit at 11–12 and would each need a genuinely new structural variant to grow further.

---

## Archetype tier distribution

24 archetypes scored on the F · D · C · E composite (Frequency × Difficulty × Conceptual weight × Exam-likelihood).

| Tier | Star rating | Count | Archetypes |
|---|---|---:|---|
| **1 — almost certainly tested** | ⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐ | 7 | A01, A02, A03, A04, A05, A06, A08 |
| **2 — very likely** | ⭐⭐⭐⭐ / ⭐⭐⭐ | 8 | A07, A11, A12, A14, A19, A21, A22, A23 |
| **3 — possible** | ⭐⭐⭐ / ⭐⭐ | 6 | A09, A10, A13, A15, A16, A24 |
| **4 — low probability** | ⭐ | 3 | A17, A18, A20 |
| **Total** | | **24** | |

**Tier-1 expected to consume 50/50 marks of a typical paper** (5 × 10-mark questions).

---

## Mutations attributed per archetype (rough share)

Each archetype is exercised by 1–4 mutation families. A mutation may count toward multiple archetypes when it crosses concerns; this table uses the *primary* family.

| Archetype | Primary mutation count | Source family(ies) |
|---|---:|---|
| A01 — Tree recursion | **62** | tree-counting (17) + tree-validation (17) + tree-transform (16) + tree-extract (11) + rose-ops (11) |
| A02 — State game | **23** | state-game (12) + state-counter (11) |
| A03 — Generic monad | **12** | monad-combinator |
| A04 — Matrix predicate | **12** | matrix-predicate |
| A05 — ADT translation | **12** | adt-translation |
| A06 — Functor / Applicative instance | **22** | functor-instance (11) + applicative-monad-instance (11) |
| A07 — Codec pair | **12** | codec |
| A08 — Env eval | **11** | env-eval |
| A09 — Prelude re-impl | **25** | list-rewrite (12) + string-ops (13, shared with A21) |
| A10 — Fold reformulation | **12** | list-fold |
| A11 — BST ops | **12** | bst-ops |
| A12 — Representation conversion | 11 | tree-extract (shared) |
| A13 — Pretty-print | **11** | pretty-print |
| A14 — Multi-effect interp | 23 | env-eval (11) + error-handling (12) (shared) |
| A15 — Writer trace | **11** | writer-trace |
| A16 — Parser combinators | **11** | parser |
| A17 — Zipper | — | (one-shot, no family) |
| A18 — Lazy memo | **12** | lazy-infinite |
| A19 — Extend interpreter | — | (uses A08 + A14 families) |
| A20 — Iso / laws | — | (theory, see monad-laws.md) |
| A21 — List comp synthesis | **11** | list-comp (+ string-ops shared with A09) |
| A22 — Typeclass instance | 11 | functor-instance (shared) |
| A23 — Mini-game | 23 | state-game (shared) |
| A24 — Applicative-only instance | 11 | applicative-monad-instance (shared) |

A01 (tree recursion) dominates: 5 families and 62 mutations roll up to it. Mock Q1 + Q5 are both A01 variants, so this matches the heat-map.

---

## Monad coverage

13 dedicated `monads/*.md` files (excluding README):

| File | Topic | Pages link in |
|---|---|---:|
| [maybe.md](monads/maybe.md) | partial functions, lookup | 60+ |
| [either.md](monads/either.md) | typed errors | 40+ |
| [state.md](monads/state.md) | mutable threaded state | 70+ |
| [writer.md](monads/writer.md) | logging | 35+ |
| [reader.md](monads/reader.md) | env in scope | 25+ |
| [io.md](monads/io.md) | side effects | 15+ |
| [list-monad.md](monads/list-monad.md) | non-determinism | 30+ |
| [monaderror.md](monads/monaderror.md) | `throwError` / `catchError` | 25+ |
| [multi-effect.md](monads/multi-effect.md) | Free monad + scheduling (A3) | 25+ |
| [transformers.md](monads/transformers.md) | StateT / ExceptT / ReaderT | 20+ |
| [transformer-stack-order.md](monads/transformer-stack-order.md) | StateT (Either) vs ExceptT (State) | 12+ |
| [generic-combinators.md](monads/generic-combinators.md) | applyNTimes, mapM', etc. (25 combinators) | 40+ |
| [monad-laws.md](monads/monad-laws.md) | left-id / right-id / assoc + QC | 15+ |

---

## Tree coverage

11 dedicated `trees/*.md` files (excluding README):

| File | Coverage |
|---|---|
| [binary-tree.md](trees/binary-tree.md) | `BT a = Empty \| Fork a (BT a) (BT a)` — size, height, mirror, mapBT, countBT |
| [bst.md](trees/bst.md) | BST invariant, isBST (bound-threaded), insert/delete/member |
| [bst-delete-trace.md](trees/bst-delete-trace.md) | The 4-case delete walked step-by-step on a sample board |
| [rose-tree.md](trees/rose-tree.md) | `Rose a = Leaf a \| Branch [Rose a]` — sizeRose, height, flatten, mock-Q1 ops |
| [expression-tree.md](trees/expression-tree.md) | `Expr = Lit \| Var \| Add \| Mul \| Let` — evaluators / desugars |
| [tree-counting.md](trees/tree-counting.md) | All count variants in one place |
| [tree-fold.md](trees/tree-fold.md) | Generic `foldBT`, `foldRose` |
| [tree-functor.md](trees/tree-functor.md) | Functor instance derivation for each tree shape |
| [tree-traversals.md](trees/tree-traversals.md) | Pre/in/post/BFS for BT and Rose |
| [tree-validation.md](trees/tree-validation.md) | All `is...` predicates (isBalanced, isComplete, isHeap, …) |
| [tree-zipper.md](trees/tree-zipper.md) | Zipper for BT (A17 + A1 GridWithAPointer) |

---

## Typeclass coverage

10 dedicated `typeclasses/*.md` files (excluding README):

| File | Coverage |
|---|---|
| [functor.md](typeclasses/functor.md) | `fmap` law, kind `* -> *`, BT/Rose/Maybe/Either |
| [applicative.md](typeclasses/applicative.md) | `pure`, `<*>`, ZipList vs Maybe |
| [monad.md](typeclasses/monad.md) | `>>=`, `return`, do-notation desugar |
| [alternative.md](typeclasses/alternative.md) | `empty`, `<\|>`, parser combinators |
| [foldable.md](typeclasses/foldable.md) | `foldr`, `foldMap`, derived for ADTs |
| [traversable.md](typeclasses/traversable.md) | `traverse`, `sequenceA`, mapM-generalised |
| [eq-ord.md](typeclasses/eq-ord.md) | `==`, `compare`, deriving caveats |
| [show.md](typeclasses/show.md) | `show`, `showsPrec`, precedence handling |
| [num.md](typeclasses/num.md) | `+ - * fromInteger`, polymorphic literals |
| [monoid.md](typeclasses/monoid.md) | `mempty`, `<>`, Sum / Product / Endo |

---

## Cross-matrix coverage (data × effect)

21 cross-matrix files covering the most exam-likely combinations:

|  | Maybe | Either | State | Writer | Reader | Monad m | List monad |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **BT / Tree** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| **BST** | (subset) | (subset) | ✓ | ✓ | (subset) | (subset) | — |
| **Rose** | (subset) | (subset) | ✓ | ✓ | (subset) | (subset) | — |
| **Expr** | ✓ | (≈ Maybe) | ✓ | (in interp) | (in interp) | (in interp) | — |
| **List** | ✓ | (≈ Maybe) | ✓ | ✓ | — | ✓ | ✓ |
| **Multi** | — | — | ✓ (expr-x-multi) | ✓ (same) | ✓ (same) | — | — |
| **Game** | — | — | ✓ (game-state) | — | — | — | — |
| **Parser** | (subset) | ✓ (parser-x-either) | — | — | — | — | — |
| **Writer trace + failure** | — | ✓ (writer-x-either) | — | — | — | — | — |

**Coverage shape:** Tree × everything is fully populated (the headline row). Expr × {Maybe, State, Multi} covers the interpreter progression. List × {everything} for non-determinism and stateful enumeration. Specialised: parser × Either, writer × Either.

---

## QuickCheck attack inventory

17 files in `quickcheck/`:

| Attack file | What gets attacked |
|---|---|
| [QUICKCHECK-ATTACKS.md](quickcheck/QUICKCHECK-ATTACKS.md) | Master: 60-second pre-submit checklist + cross-cutting attacks |
| [PROPERTY-PATTERNS.md](quickcheck/PROPERTY-PATTERNS.md) | `prop_*` patterns + Arbitrary instances for BT / Rose / Expr |
| [trees-attacks.md](quickcheck/trees-attacks.md) | Empty, single-fork, asymmetric, deep right-spine |
| [bst-attacks.md](quickcheck/bst-attacks.md) | Empty, duplicate insert, delete-root, delete-two-children |
| [rose-attacks.md](quickcheck/rose-attacks.md) | Leaf-only, single-branch, deep nesting |
| [expr-attacks.md](quickcheck/expr-attacks.md) | Unbound Var, div-by-zero, nested Let shadowing |
| [matrix-attacks.md](quickcheck/matrix-attacks.md) | `[[]]`, ragged, single row, single column |
| [lists-attacks.md](quickcheck/lists-attacks.md) | `[]`, singleton, duplicates, sorted, reverse-sorted |
| [maybe-either-attacks.md](quickcheck/maybe-either-attacks.md) | `Nothing` / `Left` short-circuit, fmap on `Nothing` |
| [state-attacks.md](quickcheck/state-attacks.md) | Empty input → state unchanged; `runState` vs `evalState` vs `execState` |
| [writer-attacks.md](quickcheck/writer-attacks.md) | Log order under failure, monoid identity |
| [monad-attacks.md](quickcheck/monad-attacks.md) | Generic `mapM`, `replicateM`, applyNTimes |
| [interp-attacks.md](quickcheck/interp-attacks.md) | Eval correctness, free-var collection |
| [codec-attacks.md](quickcheck/codec-attacks.md) | encode . decode = id round-trip |
| [numeric-attacks.md](quickcheck/numeric-attacks.md) | maxBound, minBound, overflow, divMod by 0 |
| [typeclass-instance-attacks.md](quickcheck/typeclass-instance-attacks.md) | Functor / Applicative / Monad laws as `prop_*` |

Plus README routing.

---

## Pitfall inventory

68 anchored pitfalls across 3 severity tiers + 4 specialised files:

| File | Anchors | Examples |
|---|---:|---|
| [HIGH-severity.md](pitfalls/HIGH-severity.md) | **30** (P-001 … P-030) | base-case missed, `isBST Empty = False`, signature changed, `pure` vs `return` |
| [MEDIUM-severity.md](pitfalls/MEDIUM-severity.md) | **21** | foldl space-leak, list-comp generator order, transformer stack order |
| [LOW-severity.md](pitfalls/LOW-severity.md) | **17** | strictness annoyances, Show-instance precedence, zipper asymmetry |
| [per-topic-pitfalls.md](pitfalls/per-topic-pitfalls.md) | — | Topic-specific: trees, BST, monads, interpreters |
| [signature-pitfalls.md](pitfalls/signature-pitfalls.md) | — | The 5 Mock-Q sigs verbatim — read before each Q |
| [imports-pitfalls.md](pitfalls/imports-pitfalls.md) | — | Forbidden modules, `-XSafe` interactions |
| README | — | Routing |

Every archetype's See-also block references the relevant `P-NNN` IDs.

---

## Index sizes

15 entry indexes. Sizes reflect their role: routing indexes are smaller, content indexes are bigger.

| Index | Lines | Role |
|---|---:|---|
| [ARCHETYPE-INDEX.md](indexes/ARCHETYPE-INDEX.md) | 306 | A01–A24 with template + mutations + crossings + attacks + pitfalls per archetype |
| [ASSIGNMENT-INDEX.md](indexes/ASSIGNMENT-INDEX.md) | 188 | A1 / A2 / A3 / MockTest → archetype + family |
| [BEGINNER-INDEX.md](indexes/BEGINNER-INDEX.md) | 159 | Linear cold-start reading order |
| [CROSS-TOPIC-INDEX.md](indexes/CROSS-TOPIC-INDEX.md) | 159 | Data structure × monad matrix |
| [IF-YOU-SEE-X.md](indexes/IF-YOU-SEE-X.md) | 424 | **344** trigger rows — in-exam workhorse |
| [KEYWORD-INDEX.md](indexes/KEYWORD-INDEX.md) | 512 | **412** keyword → file mappings |
| [LECTURE-INDEX.md](indexes/LECTURE-INDEX.md) | 180 | Lecture → topic → archetype |
| [MASTER-INDEX.md](indexes/MASTER-INDEX.md) | 262 | Single-page Ctrl-F over every file |
| [MOCK-Q-INDEX.md](indexes/MOCK-Q-INDEX.md) | 259 | Mock Q1–Q5 verbatim + canonical solutions + marker quirks |
| [MUTATION-INDEX.md](indexes/MUTATION-INDEX.md) | 539 | Every mutation across 24 families |
| [PRELUDE-INDEX.md](indexes/PRELUDE-INDEX.md) | 307 | Prelude / `Data.List` / `Data.Char` / `Data.Maybe` reference |
| [PROBLEM-NUMBER-INDEX.md](indexes/PROBLEM-NUMBER-INDEX.md) | 261 | **187** rows: problems 1–150 → archetype + family + file |
| [TYPE-SIGNATURE-DATABASE.md](indexes/TYPE-SIGNATURE-DATABASE.md) | 392 | **272** sig-shape rows → archetype + technique |
| [TYPES-REFERENCE.md](indexes/TYPES-REFERENCE.md) | 224 | Every `Types.hs` ADT from Mock + assignments |
| [README.md](indexes/README.md) | 22 | Directory router |
| **Total** | **4 192** | |

---

## haskell-basics breakdown (48 pages)

By category:

| Category | Pages | List |
|---|---:|---|
| Syntax | 8 | pattern-matching, guards, if-expressions, let-in, where-clauses, case-expressions, tuples, local-definitions |
| Data | 6 | lists, strings, recursion, accumulator-recursion, helper-functions, sorting |
| Comprehensions & HOFs | 6 | list-comprehensions, higher-order-functions, lambdas, function-composition, currying, partial-application |
| Operators & sections | 3 | dollar-operator, dot-operator, sections |
| Types | 5 | type-signatures, polymorphism, algebraic-data-types, recursive-data-types, deriving |
| Pre-monad effects | 3 | maybe-basics, either-basics, do-notation-basics |
| Standard HOFs | 7 | map, filter, foldr, foldl, zip, zipWith, all-any |
| Testing & tools | 9 | testing-functions, testing-recursive-functions, testing-monadic-functions, testing-tree-functions, ghci-commands, allowed-builtins, safe-haskell, common-templates, **ghc-error-decoder** |
| README | 1 | index |
| **Total** | **48** | |

---

## Coverage relative to course

- **11/11 weekly problem sheets:** covered via archetypes + question-families
- **150/150 practice problems:** indexed in [PROBLEM-NUMBER-INDEX](indexes/PROBLEM-NUMBER-INDEX.md)
- **5/5 Mock Test questions:** indexed verbatim with marker quirks in [MOCK-Q-INDEX](indexes/MOCK-Q-INDEX.md)
- **3/3 assignments + Mock:** covered in [ASSIGNMENT-INDEX](indexes/ASSIGNMENT-INDEX.md)
- **~20/20 lecture sections:** covered in [COURSE-MAP](meta/COURSE-MAP.md)

Gap audit: see [meta/GAP-AUDIT.md](meta/GAP-AUDIT.md). All 8 verified content gaps FILLED or PARTIAL (1 deliberately partial).

---

## Phase-by-phase additions log

| Phase | Date | Delivered |
|---|---|---|
| 0 | 2026-05-29 | `meta/GAP-AUDIT.md`, `meta/script-baseline.txt` |
| 1 | 2026-05-29 | 165 breadcrumbs, 73 anchors (68 pitfalls + 5 Mock-Q), 124 See-also blocks |
| 1f | 2026-05-29 | 247 body-content backtick paths → clickable |
| 2 | 2026-05-29 | `haskell-basics/` + 37 content pages |
| 3 | 2026-05-29 | 4 gap pages (`PROPERTY-PATTERNS`, `bst-delete-trace`, `transformer-stack-order`, `parser-chainl1`) |
| 4 | 2026-05-29 | 28 new mutations across 21 families (cap 12 each) |
| 5 | 2026-05-29 | 2 cross-matrix (`parser-x-either`, `writer-x-either`) |
| 6 | 2026-05-29 | 1309 lines linkified across 8 indexes |
| 7 | 2026-05-29 | `WIKI-UPGRADE-REPORT`, `SCRIPT-COMPATIBILITY-REPORT`, updated `GAP-AUDIT` |
| 8 | 2026-05-29 | Sibling-navigation strips on 198 pages |
| 9 (audit) | 2026-05-30 | ONE-PAGE-PANIC + LAST-HOUR-CHECKLIST patches; 18 new IF-YOU-SEE-X rows; **68 of 71 broken links fixed**; new TYPES-REFERENCE, safe-haskell, common-templates; A23-mini-game expanded with Minimax (alpha-beta + memo) |
| 10 (final sweep) | 2026-05-31 | `KNOWLEDGE-MAP.md` (root) + `ARCHETYPE-INDEX` / `CROSS-TOPIC-INDEX` / `MUTATION-INDEX` + `FINAL-SWEEP-REPORT`; dead links 71 → 3 (template placeholders) |
| 11 (T-1 polish) | 2026-05-31 | `haskell-basics/ghc-error-decoder.md` — 10 most common GHC errors → translation → fix; sibling injector regenerated (213 pages); `_phase8_siblings.py` BASICS_GROUPS extended with "Testing & tools" |
| 12 (comprehensive final) | 2026-05-31 | **HOME.md** + **NAVIGATION.md** + **scripts/SCRIPTS-GUIDE.md** + **string-ops-family.md** (13 mutations). Mutation cap raised 12 → 25. +5 mutations each to tree-counting, tree-validation, tree-transform (and +1 each to error-handling, lazy-infinite). Total mutations 263 → 293. README + index counts updated. Sibling injector ran on 214 pages. |
| 13 (always-on navigation) | 2026-05-31 | **`scripts/_phase13_navigation.py`**: injects a `Quick nav` strip at the top of every page (HOME · NAVIGATION · MASTER-INDEX) and a `Back to` footer at the bottom. 233 pages updated; HOME / NAVIGATION / MASTER-INDEX skipped (self-targets). Total internal links measured at ~11,959 (broken still 3 — template placeholders). |

---

## Helper scripts

9 user-facing Python scripts, all using only the Python standard library:

| Script | Reads | Purpose |
|---|---|---|
| `search_by_archetype.py A##` | `graphs/ARCHETYPE-GRAPH.json` + vault grep | A##'s neighbours + mention frequency |
| `search_by_type.py "sig"` | hardcoded `SIG_RULES` | Sig fingerprint → archetype + family |
| `search_by_monad.py <name>` | `graphs/MONAD-GRAPH.json` | Monad neighbours + cross-matrix files |
| `search_by_combo.py "X + Y"` | `graphs/*` | Cross-axis combo lookup |
| `search_by_keyword.py <kw>` | vault grep | Ranked keyword frequency |
| `mock_q_lookup.py Q[1-5]` | hardcoded `MOCK_QS` | Mock-Q spec + marker quirk + canonical files |
| `prelude_lookup.py <fn>` | `indexes/PRELUDE-INDEX.md` | Function signature + usage + pitfall |
| `study_planner.py <days>` | `archetypes/README.md` tier ranking | Personalised revision plan |
| `topic_dependencies.py <topic>` | `graphs/DEPENDENCY-GRAPH.json` | Direct + transitive prerequisites |

Plus `vlab-setup.sh` (one-shot JupyterLab config) and 15 internal phase/audit scripts (`_phase*` / `_audit*`), for 24 `.py` files in total.

---

## Knowledge graphs

6 JSON graphs in `graphs/` (218 nodes, 728 edges total):

| Graph | Nodes | Edges | Purpose |
|---|---:|---:|---|
| TOPIC-GRAPH | 52 | 130 | Topic prerequisites |
| ARCHETYPE-GRAPH | 24 | 282 | Archetype combinations |
| MONAD-GRAPH | 30 | 79 | Monad relationships |
| TREE-GRAPH | 30 | 70 | Tree-type relationships |
| QUESTION-GRAPH | 28 | 69 | Question families |
| DEPENDENCY-GRAPH | 54 | 98 | Cross-file prerequisites |
| **Total** | **218** | **728** | |

Used by `scripts/search_*.py`. Reserved for future embedding / vector tooling.

---

## Vault vs. previous-generation `notehost-vault/`

| Capability | notehost-vault | examvault |
|------------|----------------|-----------|
| Files | 144 | 238 |
| Archetypes | 20 | 24 (+ list-comp, typeclass-instance, mini-game, applicative-only) |
| Mutations per archetype | 1–3 | 5–12 |
| Cross-domain (Tree×Monad etc.) | scattered | dedicated `cross-matrix/` (21 files) |
| QuickCheck attack surface | one pitfall file | 17 attack files + Property patterns + Arbitrary instances |
| Machine-readable graphs | none | 6 JSON graphs (218 nodes, 728 edges) |
| Search scripts | broken `search.sh` shim | 9 working Python helpers |
| Type-signature reverse lookup | 1 table in `if-you-see-x` | dedicated [TYPE-SIGNATURE-DATABASE](indexes/TYPE-SIGNATURE-DATABASE.md) — 272 entries |
| Marker-quirk documentation | none | 5 Mock-Q quirks integrated throughout |
| Pitfall ranking | mixed | HIGH / MEDIUM / LOW with P-### IDs and marks-cost |
| Problem-number index | none | 150 problems → archetype + file |
| GHC error decoder | none | new: [ghc-error-decoder](haskell-basics/ghc-error-decoder.md) |
| Indexes | 1 master | 15 specialised |

---

## See also

**Architecture rationale:** [ARCHITECTURE](ARCHITECTURE.md)
**Knowledge-map:** [KNOWLEDGE-MAP](KNOWLEDGE-MAP.md)
**Course coverage:** [meta/COURSE-COVERAGE](meta/COURSE-COVERAGE.md)
**Gap audit:** [meta/GAP-AUDIT](meta/GAP-AUDIT.md)
**Completion report:** [meta/FINAL-SWEEP-REPORT](meta/FINAL-SWEEP-REPORT.md)
**Script verdicts:** [meta/SCRIPT-COMPATIBILITY-REPORT](meta/SCRIPT-COMPATIBILITY-REPORT.md)
**Per-archetype map:** [indexes/ARCHETYPE-INDEX](indexes/ARCHETYPE-INDEX.md)
**Per-mutation map:** [indexes/MUTATION-INDEX](indexes/MUTATION-INDEX.md)
**Per-cross map:** [indexes/CROSS-TOPIC-INDEX](indexes/CROSS-TOPIC-INDEX.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](HOME.md) · [NAVIGATION](NAVIGATION.md) · [MASTER-INDEX](indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
