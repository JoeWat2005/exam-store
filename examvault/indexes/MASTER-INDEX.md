> [examvault](../README.md) · [indexes](./README.md) · **MASTER-INDEX**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · **MASTER-INDEX** · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# MASTER-INDEX

Single-page Ctrl-F index of every file in the examvault. Open this first.

**Vault root:** `examvault/` · **Total .md files:** 238 · 293 mutations across 24 families · **Last updated:** 2026-05-31

> Use Ctrl-F. Look for the keyword from your question or the filename. Every entry has a one-line "use when" so you know if it's the right hop.

---

## Root — entry pages

| File | Use when |
|------|----------|
| [README](../README.md) | Main routing table, directory map, the 7-file pin list. |
| [HOME](../HOME.md) | Friendly first-visitor page — explains the four axes in 60 seconds. |
| [NAVIGATION](../NAVIGATION.md) | Every directory README, one click each. |
| [HOW-TO-USE](../HOW-TO-USE.md) | Long-form exam workflow + 5-step recognition loop. |
| [KNOWLEDGE-MAP](../KNOWLEDGE-MAP.md) | The 4-axis mental model (archetype / mutation / topic / sig). |
| [ARCHITECTURE](../ARCHITECTURE.md) | Why the directory split is the way it is. |
| [STATS](../STATS.md) | Quantitative breakdown — every count. |

## meta/ — course-level orientation

| File | Use when |
|------|----------|
| [COURSE-MAP](../meta/COURSE-MAP.md) | You want the canonical lecture → topic → type-sig → archetype mapping. One block per topic. |
| [COURSE-COVERAGE](../meta/COURSE-COVERAGE.md) | You want lecture file → primary archetype + linked vault files. Reverse direction of COURSE-MAP. |
| [VAULT-AUDIT](../meta/VAULT-AUDIT.md) | You want to know what's missing / over-covered. Auditing the vault itself. |
| [FINAL-SWEEP-REPORT](../meta/FINAL-SWEEP-REPORT.md) | Completion certificate for the 13-phase wiki upgrade. |
| [SCRIPT-COMPATIBILITY-REPORT](../meta/SCRIPT-COMPATIBILITY-REPORT.md) | 9/9 helper-script PASS verdicts. |

## archetypes/ — the 24 exam question shapes

| File | Tier | Use when |
|------|------|----------|
| [README](../archetypes/README.md) | — | You want the priority ranking, recognition flowchart, cross-archetype heat-map, 5-question composition prediction. |
| [A01-tree-recursion](../archetypes/A01-tree-recursion.md) | 1 ⭐⭐⭐⭐⭐ | Custom tree ADT with structural recursion (BT/Rose/Expr). Mock Q1+Q5. |
| [A02-state-game](../archetypes/A02-state-game.md) | 1 ⭐⭐⭐⭐⭐ | State monad mini-game (Nim, Stack-calc, Mock Q3). |
| [A03-generic-monad](../archetypes/A03-generic-monad.md) | 1 ⭐⭐⭐⭐⭐ | `Monad m =>` combinator (applyNTimes, mapM, replicateM). Mock Q2. |
| [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | 1 ⭐⭐⭐⭐ | `[[Int]] -> Bool` predicate via transpose. Mock Q4 magic square. |
| [A05-adt-translation](../archetypes/A05-adt-translation.md) | 1 ⭐⭐⭐⭐ | ADT-to-ADT structural translation (Mock Q5 Expr→Circuit). |
| [A06-functor-instance](../archetypes/A06-functor-instance.md) | 1 ⭐⭐⭐⭐ | Write `instance Functor T` (or Applicative/Monad) for custom T. |
| [A07-codec-pair](../archetypes/A07-codec-pair.md) | 2 ⭐⭐⭐⭐ | Encode/decode pair (Morse, Caesar, RLE). |
| [A08-env-eval](../archetypes/A08-env-eval.md) | 1 ⭐⭐⭐⭐ | `Env -> Expr -> r` environment evaluator (Let, Var, scope). |
| [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | 3 ⭐⭐⭐ | Re-implement a Prelude function recursively (myLength, myMap). |
| [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) | 3 ⭐⭐⭐ | Reformulate via foldr/foldl. |
| [A11-bst-ops](../archetypes/A11-bst-ops.md) | 2 ⭐⭐⭐ | BST insert/delete/member/isBST. |
| [A12-rep-conversion](../archetypes/A12-rep-conversion.md) | 2 ⭐⭐⭐ | Representation conversion (List ↔ Tree, Tree ↔ Table). |
| [A13-pretty-printer](../archetypes/A13-pretty-printer.md) | 3 ⭐⭐ | Custom Show with operator precedence. |
| [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md) | 2 ⭐⭐⭐ | State + Error interpreter (PS Week 9 calculator). |
| [A15-writer-trace](../archetypes/A15-writer-trace.md) | 3 ⭐⭐ | Writer monad trace (logFactorial, countSteps). |
| [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | 3 ⭐⭐ | Parser combinators (Functor/Applicative/Monad/Alternative for Parser). |
| [A17-zipper](../archetypes/A17-zipper.md) | 4 ⭐ | Zipper navigation (Assignment 1 GridWithAPointer). |
| [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | 4 ⭐ | Lazy memoisation (memoFib via infinite tree). |
| [A19-extend-interpreter](../archetypes/A19-extend-interpreter.md) | 2 ⭐⭐⭐ | Extend imperative interpreter with new constructor. |
| [A20-laws-iso](../archetypes/A20-laws-iso.md) | 4 ⭐ | Iso / retract / monad-law proofs. |
| [A21-list-comp-synthesis](../archetypes/A21-list-comp-synthesis.md) | 2 ⭐⭐⭐ | List comprehension synthesis (pyths, perfects, all pairs). |
| [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | 2 ⭐⭐⭐ | Eq/Ord/Show/MyEq instance for ADT. |
| [A23-mini-game](../archetypes/A23-mini-game.md) | 2 ⭐⭐⭐⭐ | Generalised mini-game (TTT, Conway, Nim variants). |
| [A24-applicative-instance](../archetypes/A24-applicative-instance.md) | 3 ⭐⭐ | Write `instance Applicative T` (often parser). |

## monads/ — one file per monad

| File | Use when |
|------|----------|
| [README](../monads/README.md) | You want the cheat-sheet for every monad in scope (sig, primitives, when to reach). |
| [maybe](../monads/maybe.md) | Maybe — partial functions, lookup, safeHead/Div/Sqrt, fromMaybe, catMaybes, mapMaybe. |
| [either](../monads/either.md) | Either — error with message, right-biased Functor/Monad, zipEither. |
| [state](../monads/state.md) | State — get/put/modify/gets, runState/evalState/execState mnemonic. Mock Q3. |
| [writer](../monads/writer.md) | Writer — tell, Sum/Product monoids, log accumulation. logFactorial. |
| [reader](../monads/reader.md) | Reader — ask/local, env-aware computation. |
| [io](../monads/io.md) | IO — getLine/readLn/putStrLn/mapM_, exam-rare. |
| [list-monad](../monads/list-monad.md) | List monad — non-determinism, knightMoves, do-over-list vs comprehension. |
| [monaderror](../monads/monaderror.md) | MonadError — throwError/catchError, calculator with /0. |
| [multi-effect](../monads/multi-effect.md) | Multi-effect — Free monads, FSum, schedulers (Assignment 3). |
| [transformers](../monads/transformers.md) | Monad transformers — StateT, ExceptT, ReaderT, lift. |
| [generic-combinators](../monads/generic-combinators.md) | Generic `Monad m =>` combinators (applyNTimes, sequenceM, mapM', join, when, unless). |
| [monad-laws](../monads/monad-laws.md) | Monad laws (left-id, right-id, assoc) + QC properties. |

## trees/ — every tree shape and operation

| File | Use when |
|------|----------|
| [README](../trees/README.md) | You want the master tree cheat-sheet (BT vs BST vs Rose vs Expr definitions). |
| [binary-tree](../trees/binary-tree.md) | `data BT a = Empty | Fork a (BT a) (BT a)` — size, height, mirror, mapBT, countBT. |
| [bst](../trees/bst.md) | BST invariant, isBST (bound-threaded), insert/delete/member. |
| [rose-tree](../trees/rose-tree.md) | Both Rose variants. isNBranching, prune, addresses. Mock Q1. |
| [expression-tree](../trees/expression-tree.md) | Expr ADTs (arithmetic + logical). evalExpr, depthExpr, varSet. |
| [tree-counting](../trees/tree-counting.md) | All counting flavours (size, leaves, internal, weight-by-predicate). |
| [tree-fold](../trees/tree-fold.md) | Generic catamorphism `foldBT`, `foldRose` shapes. |
| [tree-functor](../trees/tree-functor.md) | Functor/Foldable/Traversable instances for tree types. |
| [tree-traversals](../trees/tree-traversals.md) | In/Pre/Post-order, level-order, with-context. |
| [tree-validation](../trees/tree-validation.md) | Validation predicates (isBST, isBalanced, isFull, isNBranching). |
| [tree-zipper](../trees/tree-zipper.md) | Tree zipper representation + up/down/left/right. |

## interpreters/ — one file per Expr × effect combo

| File | Use when |
|------|----------|
| [README](../interpreters/README.md) | Interpreter index — pick by what effects you need. |
| [simple-arith](../interpreters/simple-arith.md) | Pure `evalExpr :: Expr -> Int`. Problem 89. |
| [expr-maybe](../interpreters/expr-maybe.md) | Expr → Maybe (partial: division, missing var). |
| [expr-either](../interpreters/expr-either.md) | Expr → Either e (error with message). |
| [expr-state](../interpreters/expr-state.md) | Expr × State (fresh-name during eval, counter). |
| [expr-writer](../interpreters/expr-writer.md) | Expr × Writer (trace log). |
| [expr-reader](../interpreters/expr-reader.md) | Expr × Reader (env-as-context). |
| [expr-state-either](../interpreters/expr-state-either.md) | Expr × (State + Either) — calculator with errors. |
| [expr-reader-either](../interpreters/expr-reader-either.md) | Expr × (Reader + Either) — env eval with errors. |
| [expr-writer-state](../interpreters/expr-writer-state.md) | Expr × (Writer + State) — log + counter. |
| [expr-multi-effect](../interpreters/expr-multi-effect.md) | Expr × all effects — full interpreter (PS Week 9). |
| [imperative-eval](../interpreters/imperative-eval.md) | Imperative `Program -> Storage -> Storage`. Course interpreter. |
| [imperative-storage](../interpreters/imperative-storage.md) | Storage update / lookup, := operator. |
| [parser-overview](../interpreters/parser-overview.md) | Parser stage of the interpreter (Parser.hs). |
| [desugar-pipeline](../interpreters/desugar-pipeline.md) | Multi-pass interpreter (desugar → eval). |
| [extend-interpreter](../interpreters/extend-interpreter.md) | [A19](../archetypes/A19-extend-interpreter.md) — add new ctor in 3 layers (AST + parser + eval). |

## cross-matrix/ — data × effect combinations

| File | Use when |
|------|----------|
| [README](../cross-matrix/README.md) | You want the data × effect matrix; recognition cues for which combo. |
| [tree-x-maybe](../cross-matrix/tree-x-maybe.md) | BT × Maybe (safe lookup, find path). |
| [tree-x-either](../cross-matrix/tree-x-either.md) | BT × Either (validation with message). |
| [tree-x-state](../cross-matrix/tree-x-state.md) | BT × State — **label every node** canonical pattern. |
| [tree-x-writer](../cross-matrix/tree-x-writer.md) | BT × Writer — log traversal, count via Sum. |
| [tree-x-reader](../cross-matrix/tree-x-reader.md) | BT × Reader — env-aware traversal. |
| [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md) | BT × `Monad m =>` — **mapMTree, traverseTree**. Problem 109. |
| [bst-x-state](../cross-matrix/bst-x-state.md) | BST × State — insert with fresh ID. |
| [bst-x-writer](../cross-matrix/bst-x-writer.md) | BST × Writer — trace insert/delete. |
| [rose-x-state](../cross-matrix/rose-x-state.md) | Rose × State — number every node. |
| [rose-x-writer](../cross-matrix/rose-x-writer.md) | Rose × Writer — DFS log. |
| [expr-x-maybe](../cross-matrix/expr-x-maybe.md) | Expr × Maybe — partial evaluators. |
| [expr-x-state](../cross-matrix/expr-x-state.md) | Expr × State — counters/fresh-vars during eval. |
| [expr-x-multi](../cross-matrix/expr-x-multi.md) | Expr × (env + storage + error + trace). |
| [list-x-monad](../cross-matrix/list-x-monad.md) | List × Monad — mapM, filterM, replicateM, forM. |
| [list-x-state](../cross-matrix/list-x-state.md) | List × State — generate + count threaded. |
| [list-x-writer](../cross-matrix/list-x-writer.md) | List × Writer — log per element. |
| [list-x-list-monad](../cross-matrix/list-x-list-monad.md) | List × List — nondeterminism, guards. |
| [game-state](../cross-matrix/game-state.md) | Game × State — Nim / TTT / Conway state machine. |

## question-families/ — mutation atlases

| File | Use when |
|------|----------|
| [README](../question-families/README.md) | Heat-map of which 5 families are most likely; archetype↔family map. |
| [list-rewrite-family](../question-families/list-rewrite-family.md) | "implement my…" / cons-recursion mutations. |
| [list-fold-family](../question-families/list-fold-family.md) | foldr/foldl mutations. |
| [list-comp-family](../question-families/list-comp-family.md) | Pythagorean, perfects, multi-generator comprehensions. |
| [tree-counting-family](../question-families/tree-counting-family.md) | Count/size/sum mutations. Problems 71/73/78/80. |
| [tree-validation-family](../question-families/tree-validation-family.md) | Predicate mutations (isBST, isBalanced, isNBranching). |
| [tree-transform-family](../question-families/tree-transform-family.md) | mirror/prune/map-with-fn mutations. |
| [tree-extract-family](../question-families/tree-extract-family.md) | flatten/in-order/leaves mutations. |
| [bst-ops-family](../question-families/bst-ops-family.md) | Insert/delete/member/balance mutations. |
| [rose-ops-family](../question-families/rose-ops-family.md) | Rose-specific mutations. Mock Q1. |
| [functor-instance-family](../question-families/functor-instance-family.md) | Functor instance for custom containers. |
| [applicative-monad-instance-family](../question-families/applicative-monad-instance-family.md) | Applicative + Monad instance mutations. |
| [monad-combinator-family](../question-families/monad-combinator-family.md) | applyNTimes, sequenceM, mapM' mutations. Mock Q2. |
| [state-game-family](../question-families/state-game-family.md) | Nim, calculator, stack mutations. Mock Q3. |
| [state-counter-family](../question-families/state-counter-family.md) | fresh, labelTree, uniqueIds mutations. |
| [writer-trace-family](../question-families/writer-trace-family.md) | logFactorial, count-steps, audit mutations. |
| [string-ops-family](../question-families/string-ops-family.md) *(new in Phase 12)* | Palindrome, letterFreqs, anagram, splitOn, capitalise, reverseWords. Cross-links codec/list-rewrite. |
| [error-handling-family](../question-families/error-handling-family.md) | safeDiv, safeIndex, chain-with-Maybe/Either mutations. |
| [matrix-predicate-family](../question-families/matrix-predicate-family.md) | Magic square, TTT winner, Sudoku-style. Mock Q4. |
| [adt-translation-family](../question-families/adt-translation-family.md) | Expr→Circuit, desugaring. Mock Q5. |
| [env-eval-family](../question-families/env-eval-family.md) | Let-binding, var lookup, Reader-style. Problem 148. |
| [codec-family](../question-families/codec-family.md) | Morse, Caesar, RLE encode/decode. |
| [pretty-print-family](../question-families/pretty-print-family.md) | Show with precedence, ANSI, grid render. |
| [parser-family](../question-families/parser-family.md) | Parser of arithmetic/bracketed/grammar. |
| [lazy-infinite-family](../question-families/lazy-infinite-family.md) | ones, fibs, primes, sieve, memo. |

## quickcheck/ — what the marker will hit

| File | Use when |
|------|----------|
| [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) | The 60-second pre-submit checklist. Universal attacks. |
| [README](../quickcheck/README.md) | Index — per-topic attack files. |
| [lists-attacks](../quickcheck/lists-attacks.md) | List attacks: `[]`, singleton, duplicates, sorted, reversed. |
| [trees-attacks](../quickcheck/trees-attacks.md) | BT attacks: `Empty`, single Leaf, skewed-deep. |
| [bst-attacks](../quickcheck/bst-attacks.md) | BST: `Empty = True`, delete-two-children, delete-missing. |
| [rose-attacks](../quickcheck/rose-attacks.md) | Rose: `Branch []`, `Leaf`, `n=0`, mixed-branching. |
| [expr-attacks](../quickcheck/expr-attacks.md) | Expr: `Var x`, only-Not chain, free-of-And. |
| [monad-attacks](../quickcheck/monad-attacks.md) | Generic Monad: `n=0`, `pure []`, order of effects. |
| [state-attacks](../quickcheck/state-attacks.md) | State: `(0,0)` board, underflow, non-restoring. Mock Q3 trap. |
| [writer-attacks](../quickcheck/writer-attacks.md) | Writer: tell-then-pure order, accumulation direction. |
| [maybe-either-attacks](../quickcheck/maybe-either-attacks.md) | Maybe/Either: empty input → Nothing, first-failure. |
| [codec-attacks](../quickcheck/codec-attacks.md) | Codec: empty string, single-char, round-trip. |
| [interp-attacks](../quickcheck/interp-attacks.md) | Interpreter: div-by-zero, undefined var, shadowing. |
| [matrix-attacks](../quickcheck/matrix-attacks.md) | Matrix: 1×1, non-square, anti-diagonal. |
| [numeric-attacks](../quickcheck/numeric-attacks.md) | Numeric: div-by-zero, negative, overflow. |
| [typeclass-instance-attacks](../quickcheck/typeclass-instance-attacks.md) | Typeclass: Functor laws, Monad laws, == reflexivity. |

## typeclasses/ — instance reference

| File | Use when |
|------|----------|
| [README](../typeclasses/README.md) | Recognition: which typeclass does the question want? |
| [functor](../typeclasses/functor.md) | Functor for Maybe-like, List-like, BT, Rose, Pair, Either, Reader, Compose. |
| [applicative](../typeclasses/applicative.md) | Applicative for Maybe, List, Reader, Parser, ZipList, Compose. |
| [monad](../typeclasses/monad.md) | Monad for Maybe, List, Reader, State, Writer, Parser + the Functor/Applicative trio. |
| [alternative](../typeclasses/alternative.md) | Alternative for Maybe, List, Parser. |
| [foldable](../typeclasses/foldable.md) | Foldable for BT, Rose, Expr, Pair. |
| [traversable](../typeclasses/traversable.md) | Traversable for BT, Rose; relationship to mapM. |
| [eq-ord](../typeclasses/eq-ord.md) | Manual Eq/Ord instance, compare discipline. |
| [show](../typeclasses/show.md) | Show with precedence (showsPrec). |
| [num](../typeclasses/num.md) | Num for Bool ring, Peano nats, NumExpr. |
| [monoid](../typeclasses/monoid.md) | Semigroup/Monoid: `<>`, mempty, Sum/Product/Max/Min/[a]. |

## exam-day/ — last-hour materials

| File | Use when |
|------|----------|
| [README](../exam-day/README.md) | Directory index — the exam-day page set, in reading order. |
| [EXAM-DAY-ROUTE](../exam-day/EXAM-DAY-ROUTE.md) | Minute-by-minute playbook for the whole 2-hour sitting. |
| [IN-EXAM-WORKFLOW](../exam-day/IN-EXAM-WORKFLOW.md) | The per-question 6-step loop (recognise → template → fill → test). |
| [RECOGNITION-FLOWCHART](../exam-day/RECOGNITION-FLOWCHART.md) | Read the question → archetype, as a decision flowchart. |
| [TIME-BUDGET](../exam-day/TIME-BUDGET.md) | 24-minute × 5 strategy + skip-and-return rules. |
| [LAST-HOUR-CHECKLIST](../exam-day/LAST-HOUR-CHECKLIST.md) | What to revise in the final hour before the exam. |
| [WHAT-TO-PIN](../exam-day/WHAT-TO-PIN.md) | Which vault tabs to open in vLab, in pin order. |
| [ONE-PAGE-PANIC](../exam-day/ONE-PAGE-PANIC.md) | When you blank — the single-page emergency card. |

## pitfalls/ — mistakes ranked by severity

| File | Use when |
|------|----------|
| [README](../pitfalls/README.md) | Pitfalls index + the 60-second pre-submit check. |
| [HIGH-severity](../pitfalls/HIGH-severity.md) | Marks-killers (P-001–P-030): zero a whole question / fail to compile. Read the night before. |
| [MEDIUM-severity](../pitfalls/MEDIUM-severity.md) | Silent correctness bugs (P-100+): compile fine, fail one QC input class, 1–4 marks each. |
| [LOW-severity](../pitfalls/LOW-severity.md) | Style / efficiency habits (P-200+): rarely lose marks, fix after it works. |
| [imports-pitfalls](../pitfalls/imports-pitfalls.md) | The allowed-imports list + Safe-Haskell rejections explained. |
| [signature-pitfalls](../pitfalls/signature-pitfalls.md) | The auto-marker import contract — exact-signature / name discipline. |
| [per-topic-pitfalls](../pitfalls/per-topic-pitfalls.md) | One Ctrl-F page: topic header → pitfall ids. Open as a tab mid-exam. |

## indexes/ — lookup layer (this directory)

| File | Use when |
|------|----------|
| [MASTER-INDEX](../indexes/MASTER-INDEX.md) | This file. |
| [IF-YOU-SEE-X](../indexes/IF-YOU-SEE-X.md) | Phrase from question → archetype number. |
| [TYPE-SIGNATURE-DATABASE](../indexes/TYPE-SIGNATURE-DATABASE.md) | Sig shape → archetype + family. Includes all 150 problem sigs. |
| [KEYWORD-INDEX](../indexes/KEYWORD-INDEX.md) | Alphabetical keyword → vault files. |
| [PROBLEM-NUMBER-INDEX](../indexes/PROBLEM-NUMBER-INDEX.md) | Problems 1-150 from `Haskell-Practice-Problems.md`. |
| [LECTURE-INDEX](../indexes/LECTURE-INDEX.md) | Lecture file → vault files. |
| [PRELUDE-INDEX](../indexes/PRELUDE-INDEX.md) | Every Prelude/Data.List/Data.Char/Data.Maybe function. |
| [MOCK-Q-INDEX](../indexes/MOCK-Q-INDEX.md) | Mock Q1–Q5 spec + surprising marker behaviour. |
| [ASSIGNMENT-INDEX](../indexes/ASSIGNMENT-INDEX.md) | Assignments 1, 2, 3 topic + quirks. |

## graphs/ — machine-readable knowledge graphs

| File | Use when |
|------|----------|
| `graphs/TOPIC-GRAPH.json` | Topic dependency & relation graph (JSON). |
| `graphs/ARCHETYPE-GRAPH.json` | [A01](../archetypes/A01-tree-recursion.md)–[A24](../archetypes/A24-applicative-instance.md) combines-with matrix (JSON, 24×24). |
| `graphs/MONAD-GRAPH.json` | Monad + transformer stack graph (JSON). |
| `graphs/TREE-GRAPH.json` | Tree types + operations (JSON). |
| `graphs/QUESTION-GRAPH.json` | Question families + problem instances (JSON). |
| `graphs/DEPENDENCY-GRAPH.json` | Prerequisite topology (JSON). |

## scripts/ — Python search & planning helpers

| File | Use when |
|------|----------|
| [README](../scripts/README.md) | Quick start summary. |
| **[SCRIPTS-GUIDE](../scripts/SCRIPTS-GUIDE.md)** | **Full worked examples + sample output for every script (bash + PowerShell smoke tests).** |
| [vlab-setup.sh](../scripts/vlab-setup.sh) | One-shot JupyterLab Markdown-Preview config — run once per fresh vLab env. |
| `scripts/search_by_type.py` | `Tree a -> Int` → families + archetypes + files. |
| `scripts/search_by_archetype.py` | [A02](../archetypes/A02-state-game.md) or "State Monad" → all files referencing it. |
| `scripts/search_by_keyword.py` | "Nim" / "applyNTimes" → grep across vault. |
| `scripts/search_by_monad.py` | "State" → every file mentioning it. |
| `scripts/search_by_combo.py` | "Tree + State" → cross-matrix files + archetype combos. |
| `scripts/study_planner.py` | N days → ranked daily plan. |
| `scripts/topic_dependencies.py` | "Functor" → prerequisites + downstream. |
| `scripts/mock_q_lookup.py` | "Q1" or "isNBranching" → Mock context + marker quirks. |
| `scripts/prelude_lookup.py` | Function name → sig + use + appearances. |

## haskell-basics/ — cold-start refresher (top picks — SUBSET, not all 48)

> This lists only the most-reached-for pages. **For all 48, see [haskell-basics/README.md](../haskell-basics/README.md)** (categorised index).

| File | Use when |
|------|----------|
| [README](../haskell-basics/README.md) | Categorised index — all 48 pages by topic. |
| [common-templates](../haskell-basics/common-templates.md) | 8 canonical Haskell patterns on one printable sheet. |
| [allowed-builtins](../haskell-basics/allowed-builtins.md) | Every Prelude / `Data.*` function permitted in the exam. |
| [ghci-commands](../haskell-basics/ghci-commands.md) | `:l` / `:r` / `:t` / `:i` / `:set +s` / multiline blocks. |
| **[ghc-error-decoder](../haskell-basics/ghc-error-decoder.md)** | **Red GHC text → translation → fix recipe. Open mid-exam.** |
| [sorting](../haskell-basics/sorting.md) | Insertion / selection / bubble / quick / merge sorts (hand-rolled) + `isSorted` / permutation properties. |
| [testing-functions](../haskell-basics/testing-functions.md) | Pure-function GHCi recipes. |
| [testing-monadic-functions](../haskell-basics/testing-monadic-functions.md) | Per-monad runner table (`runState` / `runWriter` / etc.). |
| [testing-tree-functions](../haskell-basics/testing-tree-functions.md) | Sample BT / Rose values + golden / asymmetric / balanced checks. |
| [safe-haskell](../haskell-basics/safe-haskell.md) | What `{-# LANGUAGE Safe #-}` forbids and why. |

---

## Fastest entry points (memorise these)

1. **First glance at exam question:** [README](../archetypes/README.md) → recognition flowchart → A##.
2. **Phrase trigger:** [IF-YOU-SEE-X](../indexes/IF-YOU-SEE-X.md) → 1-row table → archetype + file.
3. **Type signature only:** [TYPE-SIGNATURE-DATABASE](../indexes/TYPE-SIGNATURE-DATABASE.md) → grouped by shape → archetype.
4. **Pre-submit:** [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) → 60-second checklist.
5. **Combo question (Tree × State etc.):** `cross-matrix/<combo>.md`.
