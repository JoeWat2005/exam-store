<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [meta](./README.md) · **notehost-vault audit**

<!-- siblings:start -->
> **Peers:** [COURSE-COVERAGE](./COURSE-COVERAGE.md) · [COURSE-MAP](./COURSE-MAP.md) · [FINAL-SWEEP-REPORT](./FINAL-SWEEP-REPORT.md) · [GAP-AUDIT](./GAP-AUDIT.md) · [SCRIPT-COMPATIBILITY-REPORT](./SCRIPT-COMPATIBILITY-REPORT.md) · **VAULT-AUDIT** · [WIKI-UPGRADE-REPORT](./WIKI-UPGRADE-REPORT.md)
<!-- siblings:end -->






# notehost-vault audit

Source: `C:/Users/cwatm/Desktop/functional programming/notehost-vault/markdownvault/` — 144 markdown files across 9 categories (roots + archetypes/, examples/, interpreters/, monads/, patterns/, practice/, syntax/, templates/, typeclasses/).

## Verdict — one paragraph

The previous vault is **best at lookup-velocity** and **archetype enumeration**. The three root files `if-you-see-x.md`, `common-templates.md`, and `type-signature-decoder.md` together form a genuinely usable phrase→pattern→sig three-way index, and `archetypes/00-priority.md` ranks 20 question shapes with credible reasoning. Every Tier-1 archetype has a canonical worked solution in `examples/mock-q[1-5]-*.md` with the exact student bug from `final10.hs`/`ewan20.hs` flagged. It is **worst at cohesion, depth, and verifiability** — the same content is duplicated across patterns/templates/archetypes/syntax with no clear rule on which is canonical, lots of links are decorative rather than load-bearing, BST/parser/interpreter coverage stops at "here's the template" without ever walking a tricky case, and nothing in the vault has been actually run against QuickCheck to confirm it matches the marker. It is a *paper plane* — flies far on first throw, but cannot survive a hard question.

## Strengths (port verbatim or adapt)

- **Mock-test worked solutions** (`examples/mock-q1-rose.md` through `mock-q5-circuit.md`): each is a one-screen file with spec → canonical solution → exact student bug → trace. This is the single most useful artefact in the whole vault — port verbatim, just verify each compiles. Quality is high because they hew to the actual mock paper.
- **Three-way root lookup index** (`if-you-see-x.md`, `type-signature-decoder.md`, `common-templates.md`): the trio works because they index by phrase, by type-sig shape, and by section number respectively. A student under pressure can hit any of the three without prior thought. Port the *idea* but rebuild — see weaknesses below.
- **Priority matrix** (`archetypes/00-priority.md`): tier-1/2/3/4 ranking with F·D·C·E scoring rubric and "Combines with" pointers. The likely-composition prediction (Q1 #01, Q2 #03, Q3 #02, Q4 #04/#08, Q5 #05/#06) matches the mock paper. Port the table, scrap the rubric (too vague).
- **Common-pitfalls master file** (`common-pitfalls.md`): severity-ranked 🔴/🟡/🟢 with specific named-student-bug references (`final10.hs` Or-with-p-not-q, `githubinitial.hs` isBST-Empty-False, `ewan20.hs` shallow-Rose-check). Concrete > abstract. Port the bug references; expand the QuickCheck reasoning.
- **Mental-model one-liners** at the top of every file (added recently): e.g. "State = hides an accumulator in a do-block." These genuinely help a panicking student re-anchor. Adopt this convention vault-wide.
- **State + Writer + Free triad** in [state](../monads/state.md), [writer](../monads/writer.md), [free](../monads/multi-effect.md): actually cover all the primitives, runners, and pitfalls. `free.md` is the only place the Round-Robin/Schedule A3 trick is documented at all. Port.
- **interpreter-extension.md** (the 3-layer change template): with `for`, `do-while`, `++`/`--` worked examples. This is the only file that bridges parser/AST/eval cleanly. Rare in student notes; keep.
- **prelude-cheatsheet.md** — 350 lines, 23 sections, every function the exam allows is here with type. Genuine reference value. Port; verify each signature against current GHC.
- **patterns/lazy-memoization.md + examples/fib-memo.md**: memoBT/memoList/fix triad is rare to see well-explained; this is one of the better files.

## Weaknesses

- **Massive content duplication with no canonical version** — the same template appears in `common-templates.md §4`, `tree-recursion.md`, `templates/tree-bt.md`, `patterns/tree-recursion.md`, `archetypes/01-tree-recursion.md`, `examples/mock-q1-rose.md`, and `practice/05-binary-and-rose-trees.md`. Seven files for the same BT recursion skeleton. The vault's own files admit it: `patterns/triggers.md` says "see the newer [if-you-see-x](../indexes/IF-YOU-SEE-X.md)"; `patterns/pitfalls.md` says "see the newer, more complete [common-pitfalls]"; `templates/type-decoder.md` says "see the newer [type-signature-decoder]". The new vault should pick ONE canonical home per concept and link in.
- **BST coverage stops at the easy cases** (`archetypes/11-bst.md`, `templates/tree-bt.md`, `common-templates.md §7`): all three show the same 4-case delete but **none walks the two-children-with-pred/succ-replacement carefully**. `templates/tree-bt.md` uses `largestBT . l` (rightmost-of-left), `archetypes/11-bst.md` uses `largestOf l` + `withoutLargest l`, `common-templates.md §7` uses yet a third spelling. No file proves the BST invariant is preserved. New vault must do one careful walkthrough.
- **`isBST` has THREE different implementations across the vault** — `archetypes/11-bst.md` uses bound-threading `(Nothing, Nothing)` Maybe-bounds, `templates/tree-bt.md` uses `allLT`/`allGT` helpers (O(n²) — explicitly the "WRONG" pattern flagged in `common-pitfalls.md`!), and `practice/05` uses `ordered . flattenInOrder`. The pitfall file warns against the template's own implementation. Pick one approach, justify it, kill the others.
- **Parser coverage is shallow** (`archetypes/16-parser.md`, `templates/parser-newtype.md`, `examples/expr-parser.md`): all show the same `expr/term/factor` toy. No coverage of (a) `chainl1` for left-associativity, (b) backtracking-vs-greedy `<|>` interaction with `try`, (c) parser-as-Applicative without Monad. Both the assignment and archetype say "the course uses `[(a, String)]` form" but `templates/parser-newtype.md` shows Maybe-form. Pick one.
- **No QuickCheck content at all** despite the vault claiming "exam is auto-marked by QuickCheck". The word "QuickCheck" appears 9 times across 144 files; never with an actual property statement, never showing a sample failure, never explaining the `-XSafe` pragma interaction or `marking-core` lifecycle. This is a glaring miss given the actual marking process.
- **Many "See also" lines are decorative**, not navigation: `common-templates.md` ends with "See also [If You See X] · [Type Signature Decoder] · [Common Pitfalls] · [Tree Recursion] · [State Monad]" — these are just the top-5 files; the link adds nothing. The pattern repeats. Replace with question-driven cross-refs ("when you've fixed the type sig, jump to template §X").
- **Search infrastructure is fictional**: every file says "use `bash search.sh <keyword>`" but `search.sh` is never defined in the markdown (it would live in `notehost-vault/`, not the vault itself). vLab is bash-only; Windows VS Code users hit `Ctrl+Shift+F` anyway. The instruction is dead weight that misleads in two directions.
- **`vlab-setup.sh` was referenced in notehost-vault but never shipped there** (linked from its `HOW-TO-USE.md` as "bash markdownvault/vlab-setup.sh", then dumping a `cat <<EOF` config inline — duplicating effort). **Resolved in examvault:** the script now exists at [`scripts/vlab-setup.sh`](../scripts/vlab-setup.sh), is executable, and passes `bash -n`; the link is live, not broken.
- **`practice/` is 10 files of dumped student solutions** with keywords-as-summary, no context on which problem they were solving or why each variant exists. `practice/09-mock-and-misc.md` is 287 lines of unsorted code from 6 different source files. Useful as a grep corpus, not as a study tool.
- **Archetype files are too thin** — most are 40-70 lines: Concept, Shape, Typical sigs, Solution (which often just *links elsewhere*), Traps, Combines, Seen. `archetypes/03-generic-monad.md` doesn't show a single example of how `applyNTimes` behaves differently in Maybe vs State vs IO. `archetypes/14-multi-effect.md` doesn't show the `Either`-only fallback path when `Control.Monad.Error.Class` is forbidden.
- **No "verify this compiles" gate** — many code blocks have subtle bugs an attentive student would copy in: e.g. `prelude-cheatsheet.md` says `forM, forM_ :: Monad m => [a] -> (a -> m b) -> m b` (signature for forM_ is wrong — drops the `_`), `examples/morse-codec.md` `split` definition is incomplete (`split _ [] = [[]]` then proceeds with a partial implementation). New vault needs every code block runnable.
- **Two different Rose tree ADTs** used inconsistently — `templates/tree-rose.md` declares `Rose a = Leaf a | Branch [Rose a]`; `practice/05-binary-and-rose-trees.md` redefines it twice in one file (first `Rose a = Branch a [Rose a]`, then `Rose a = Leafnode a | Branch [Rose a]`). A student copying half from one and half from another will produce non-compiling code. Pin the spec to the actual mock.
- **No coverage of Eq instance pitfalls** (eg. `instance Eq (Bool -> a)` requires `FlexibleInstances`); `custom-instances.md` mentions the pragma but [eq-ord-num](../typeclasses/eq-ord.md) doesn't.
- **GHCi tips file (`ghci-tips.md`)** has a broken signature table ("Couldn't match type 'a' with 'IO a'" — that's not how GHC error messages render) and recommends `:set +s` for "memory comparison" without showing the output format. Adequate but not polished.

## Missing topics (gap list)

For each gap: topic / why it matters / where it should land in examvault.

- **BST deletion two-children case with pred/succ replacement walkthrough** / shows up in W6 sheet and may appear as a Q5; current vault declares the 4-case but doesn't trace through "if both children non-empty, replace with rightmost-of-left subtree AND remove it" with an example board / `examvault/trees/bst-delete-walkthrough.md`.
- **QuickCheck property authoring** / the exam IS QuickCheck; students never see a `prop_*` definition in the entire vault. Should cover: simple property `prop_reverseInvolutive xs = reverse (reverse xs) == xs`, conditional `==>`, `forAll` for custom generators, `Arbitrary` instances for `BT`/`Rose`, common failure messages and how to read shrunk counterexamples / `examvault/quickcheck/`.
- **`-XSafe` pragma interaction** / assignment marking enforces it; vault doesn't explain what becomes unavailable (e.g. `unsafePerformIO`, `Generic` deriving in some cases), how it interacts with `-XNoGeneralizedNewtypeDeriving` / `examvault/quickcheck/safe-pragma.md` or `examvault/meta/`.
- **`marking-core` lifecycle** / assignments depend on it but the vault never mentions how the test harness invokes a student function or how it reports mark breakdowns / `examvault/quickcheck/`.
- **Left-associative parsers via `chainl1`** / W10 problem sheet uses it; current `expr` parser is right-associative which gives wrong arithmetic for `1-2-3` / `examvault/archetypes/parser.md`.
- **`mapM` vs `traverse` vs `for` decision** / vault mentions all three exist but doesn't explain why `traverse` is the Applicative generalisation and when you'd reach for it / `examvault/typeclasses/applicative.md`.
- **`MonadFail` in do-blocks** / `examples/env-eval-example.md` and [env-eval](../interpreters/expr-reader.md) rely on `IVal x <- eval env e1` pattern-matching failing to `Nothing` — but only because `Maybe` has a `MonadFail` instance. The fact that this is a `MonadFail` not Monad mechanism is never said, and it can bite if the eval monad is `Either` or a custom newtype / `examvault/monads/monadfail-pattern-bind.md`.
- **Writer space-leak via lazy `<>`** / vault recommends `Writer [String]` casually; doesn't warn that long `Writer` traces with strict accumulator can OOM / `examvault/monads/writer.md`.
- **Type-class dispatch order: `instance Functor (Either e)` fixes `e`** / mentioned once in passing in `functor.md`; should have a worked "why this fails" example for the student who writes `instance Functor Either` (without the partial application) / `examvault/typeclasses/kind-and-partial-application.md`.
- **Parser as `Applicative` only (no Monad)** / academically the cleanest version; W10 covers it. Vault only shows monadic parsers / `examvault/archetypes/parser.md`.
- **Mutual recursion idioms** / `tabulate`/`ramify` in `morse-codec.md` reference helpers `insertLeft`/`insertRight` and say "omitted — see Assignment2Solutions.hs". A student needs the full code or the recursion shape / `examvault/archetypes/codec.md`.
- **Free monad `Functor` superclass requirement** / mentioned in [free](../monads/multi-effect.md) pitfalls as "Functor f =>" required everywhere but no worked example shows where it goes / a worked file in `examvault/monads/free.md`.
- **`StateT s (Either e)` vs `ExceptT e (State s)` ordering**: [multi-effect](../monads/multi-effect.md) mentions "state changes may be lost depending on stack order" but doesn't show a concrete example demonstrating the difference / `examvault/monads/transformer-stack-order.md`.
- **`deriving Foldable, Traversable`** / W11 mentions them as the generalisation of `flatten` / `sequence`; vault never mentions either class / `examvault/typeclasses/foldable-traversable.md`.
- **Reading the assignment template/Signatures.hs** / `presubmit.sh` regenerates this file; understanding which sigs are pinned vs editable would help students who panic when they touch the wrong thing / `examvault/quickcheck/signatures-pinned.md`.
- **`Show` precedence (`showsPrec`)** / `archetypes/13-pretty-print.md` mentions "needs Int-arg `showsPrec`" but doesn't show how — Data2 lecture uses stratified `show3/show2/show1` instead, which is OK but only for one fixed grammar / `examvault/archetypes/pretty-print.md`.
- **`Read` instance** / nobody covers `read` in any depth; mentioned once in `prelude-cheatsheet.md` as "partial" but its actual use case (read user-supplied numbers in a parser-less calculator question) goes unmentioned / `examvault/typeclasses/`.
- **Worked walkthrough of a State-Monad-from-scratch instance** / the templates show the code; no file walks through *why* `State p >>= f = State $ \s -> let (x, s') = p s; State q = f x in q s'` is correct, which is the question-prone variant. `templates/monad-instance.md` just shows the code / `examvault/monads/state-instance-derivation.md`.
- **Trie/BST with `Maybe` payload (Morse-style)** / template `adt-declarations.md` declares it, but only `morse-codec.md` uses it, and never explains why the payload is `Maybe Char` rather than `Char` (because internal nodes have no character) / `examvault/archetypes/codec.md`.
- **Differences between mock 2025 and real-exam 2026 expectations** / the vault assumes mock-like format. If the 2026 paper deviates, no guidance / `examvault/exam-day/known-unknowns.md`.

## Duplicate / redundant content

Files that say the same thing — list pairs, note canonical choice.

- `if-you-see-x.md` ≡ `patterns/triggers.md` — same phrase→pattern mapping, two different table formats. The newer `if-you-see-x.md` is canonical (vault admits it). **Drop `patterns/triggers.md`.**
- `common-pitfalls.md` ≡ `patterns/pitfalls.md` — vault admits the newer is canonical. **Drop `patterns/pitfalls.md`.**
- `type-signature-decoder.md` ≡ `templates/type-decoder.md` — vault admits newer is canonical. **Drop `templates/type-decoder.md`.**
- `tree-recursion.md` (root) ≡ `patterns/tree-recursion.md` ≡ `templates/tree-bt.md` ≡ `templates/tree-rose.md` ≡ `archetypes/01-tree-recursion.md` ≡ `common-templates.md §4-5` — *six places* with same content. Keep ONE canonical reference (suggest `examvault/trees/bt-and-rose.md`) and have the rest be one-line "see X".
- `state-monad.md` (root) ≡ [state](../monads/state.md) ≡ `templates/state-game.md` + `templates/state-fresh.md` ≡ `archetypes/02-state-game.md` ≡ `common-templates.md §8` — five places. Keep `examvault/monads/state.md` canonical.
- `functor.md` (root) ≡ [functor](../typeclasses/functor.md) ≡ `syntax/functor.md` ≡ `templates/functor-instance.md` ≡ `archetypes/06-functor-instance.md` ≡ `common-templates.md §15` — six places.
- `mapm.md` ≡ `templates/mapM-tree.md` ≡ `patterns/map-mapM-traverse.md` ≡ `common-templates.md §16` — four places.
- [overview](../monads/README.md) ≡ `syntax/monads-overview.md` — different intros, same decision table.
- [env-eval](../interpreters/expr-reader.md) ≡ `examples/env-eval-example.md` ≡ `archetypes/08-env-eval.md` ≡ `common-templates.md §11` — four files all show the same `Let x e body` extension.
- `examples/mock-q1-rose.md` ≡ `templates/tree-rose.md` Mock Q1 ≡ `tree-recursion.md` Mock Q1 — same `isNBranching`/`prune` three times.
- `examples/mock-q3-nim.md` ≡ `templates/state-game.md` Nim ≡ `archetypes/02-state-game.md` Nim ≡ `examples/nim-game.md` extended Nim — four times.
- `examples/mock-q5-circuit.md` ≡ `archetypes/05-adt-translation.md` ≡ `patterns/adt-to-adt-translation.md` ≡ `common-templates.md §12` — four times.
- `practice/03` Caesar ≡ `examples/caesar-cipher.md` — same `shift`/`encode`/`decode`/`crack`.
- `practice/05` BST ops ≡ `archetypes/11-bst.md` ≡ `templates/tree-bt.md` — same `insertBST`/`deleteBST`/`memberBST` with *different* `isBST` impls.
- `syntax/functor.md` ≡ `syntax/maybe.md` (Functor section) ≡ [functor](../typeclasses/functor.md) ≡ `templates/functor-instance.md` Maybe — Maybe instance shows up four times.

Canonical choice for the new vault: ONE per concept, in the most natural directory; everything else is a one-line `→ see ../trees/bt.md` redirect (or omitted entirely).

## Inventory by directory

| Directory | File count | What it covers | Grade | Action |
|---|---|---|---|---|
| `/` (roots) | 14 | Master index, navigation, how-to, ONE-PAGE, solution-process, if-you-see-x, common-templates, type-sig decoder, common-pitfalls, exam-day, ghci-tips, prelude/data-list-char cheatsheets, tier-1 topic files (tree-recursion, state-monad, functor, mapm, list-comprehensions, higher-order-functions, interpreter-extension) | B | Rewrite-with-distillation. Several roots (HOW-TO-USE, NAVIGATION, SEARCH-INDEX, INDEX) overlap heavily — collapse to 2 files: a README and an exam-day card. `if-you-see-x`/`common-templates`/`type-sig` form the lookup trio — port the *idea* but verify every code block runs. |
| `archetypes/` | 22 | 20 ranked question-shapes (01-20) + priority matrix + README | B+ | Port-as-is for ranking + tier-1; rewrite tier-3/4 (they're stubs). The 5-section format (Concept/Shape/Sigs/Solution/Traps/Combines/Seen) is decent — keep it; just thicken each one. |
| `examples/` | 17 | Mock Q1-5 worked, A1-A3 worked, 4 lecture-derived, 5 skill demos | A- | Port-as-is. The Mock Q solutions are the single most valuable artefact in the vault. Verify each compiles. |
| `interpreters/` | 6 | Simple → Env → MonadError → Multi-effect → Imperative storage + overview | B | Rewrite. Coverage of pure→stateful→errorful escalation is good; depth is thin (no parser integration, no extension worked example beyond what `interpreter-extension.md` already has). |
| `monads/` | 11 | Overview + Maybe + Either + State + Writer + Reader + List + IO + MonadError + multi-effect + Free | B+ | Port `state.md`, `writer.md`, `free.md`, `monaderror.md` mostly as-is; thicken `multi-effect.md` and add the transformer-order example; `reader.md` is a stub. |
| `patterns/` | 12 | Cross-cutting idioms: list-rec, tree-rec, folds, accumulator, monadic-recursion, traversals, map-mapM, codec-pair, adt-to-adt, lazy-memo, triggers, pitfalls | C+ | Discard most. Vault itself flags `triggers.md` and `pitfalls.md` as obsolete. `lazy-memoization.md` is good; rest duplicate `templates/` or `archetypes/`. Keep `lazy-memoization`, `codec-pair`, `accumulator`, merge rest into archetypes or trees/. |
| `practice/` | 10 | Dumped student solutions from `practiceproblems/*.hs`, indexed by topic with keyword headers | C | Discard or *deeply* reorganise. As a grep corpus, OK; as a study tool, no narrative. Consider porting into a single `examvault/scripts/` `grep` source rather than 10 thin markdown wrappers. The keyword index at the top of each is the only useful artefact. |
| `syntax/` | 19 | Lambdas, let/in, where, backticks, function-composition, data, type, newtype, record, typeclasses, instances, functor, applicative, monad, do-notation, list-monad, maybe, either, map-filter-fold | B | Mostly port — they're the most beginner-friendly files in the vault (mental models + 3 examples + pitfalls + see-also). But duplicates lots of typeclasses/ content. Consider folding into a single `examvault/syntax/` directory or omitting altogether (this is what HaskellWiki / LYAH already do). |
| `templates/` | 13 | Pure copy-paste skeletons: list-cons, list-accumulator, tree-bt, tree-rose, mapM-tree, state-fresh, state-game, writer-trace, functor-instance, monad-instance, parser-newtype, adt-declarations, type-decoder | B+ | Port `tree-bt`, `tree-rose`, `state-game`, `state-fresh`, `mapM-tree`, `parser-newtype`, `monad-instance`, `adt-declarations` (these are genuine copy-paste templates). Drop `type-decoder` (subset of root). |
| `typeclasses/` | 6 | Functor, Applicative, Monad, Alternative, Eq-Ord-Num, custom-instances | B | Port — clean class-by-class refs. Already largely non-duplicative with monads/ (which is per-monad-instance). The mental-model intros are good. |

Total inventory: 144 files. Recommended ports: ~50. Recommended drops/merges: ~94.

## Naming and organisation issues

- **Archetype IDs (01-20) mixed with file naming convention** (`05-adt-translation.md`) is OK on local FS but breaks every link in JupyterLab on vLab if alphabetical sort vs numerical sort differs (it does — `01..09` then `10..20`, fine; but if the user adds `00-priority.md` it sorts first, which is intended but confusing).
- **Inconsistent capitalisation** in titles vs filenames: `mapm.md` has title "mapM / mapM_ / sequence / forM / traverse" but link text everywhere is `mapM` (with capital M). Sorts fine on Linux fs (case-sensitive) but Windows treats it case-insensitively — fine for now but a porting hazard.
- **Markdown nav breadcrumb** `→ [← INDEX](../README.md) · [↑ Category] · [NAVIGATION](../README.md)` works in VS Code preview, **fails on vLab** unless the user runs the `vlab-setup.sh` config (which notehost-vault never shipped; examvault now provides it at [`scripts/vlab-setup.sh`](../scripts/vlab-setup.sh)). Half the vault's UX depends on a one-off setup step a panicking student won't have done. New vault should pick a convention that works on raw text too.
- **Some files end with a stray code block, no See-also section** ([imperative-storage](../interpreters/imperative-storage.md) is OK; `examples/grid-zipper.md` is fine; but `archetypes/17-zipper.md` ends with "See also [ADT Declarations]" with one link only — convention-broken).
- **`practice/` files use a header convention** (`keywords:` + `search:` lines at top) absent from every other directory. Inconsistent: pick one or none.
- **[state](../monads/state.md) AND root `state-monad.md` exist** — they cross-link each other, but neither is officially canonical. Same for [overview](../monads/README.md) vs `syntax/monads-overview.md`. Naming collision.
- **The `Tree` ADT is redeclared per-file with different ctor names** — `BT a = Empty | Fork`, `Tree a = EmptyTree | Node`, `Bin a = Lf | Nd`, `BinTree a = EmptyTree | Node ...`, etc. The vault notes this is intentional (each practice file is self-contained per CLAUDE.md), but the **template** files should pick one for consistency and call out that the exam will use whatever's in `Types.hs`.
- **Search-index file (`SEARCH-INDEX.md`) is hand-maintained** — every new file requires a manual update to keep keywords in sync. The current file is already drifting (e.g. `MockTest-Practice` link points to a file at vault root that has no `markdownvault/` prefix in path; broken). Either generate from front-matter or drop.

## Highest-leverage carry-overs

Top 10 files (by exam-ROI) the new vault MUST replicate or improve. Ordered by per-mark impact assuming a 5-question paper.

1. **`examples/mock-q1-rose.md`** — direct Mock Q1; identical archetype to likely Q1; one-page spec + canonical solution + the exact bug from `ewan20.hs`. ~10 marks of exam-direct utility. Port verbatim.
2. **`examples/mock-q3-nim.md`** — direct Mock Q3; State monad game template; flags the `max 0 (x-n)` clamp bug. ~10 marks. Port verbatim.
3. **`examples/mock-q5-circuit.md`** — direct Mock Q5; the only file that traces the `nq = Nand (circuit p) (circuit p)` student bug to its line. ~10 marks. Port verbatim.
4. **`if-you-see-x.md`** — phrase-to-pattern lookup table; the file a student opens first. Tens of marks across the whole paper if it routes correctly. Port + verify every link.
5. **`common-templates.md`** — 20 skeletons in one file with §-numbered sections; copy-pasteable; this is the file pinned in the second VS Code tab. ~5 marks averaged across the paper. Port + run every code block.
6. **`type-signature-decoder.md`** — sig-shape table; especially helps Q2 (generic monad) and Q4 (matrix predicate) where the sig gives away the technique. ~5 marks. Port + verify.
7. **`common-pitfalls.md`** — the bug-by-severity ranking is concrete (with named-source-of-bug). The `isBST Empty = False` + shallow Rose check + Or-with-p-not-q triple alone is worth 5-10 marks across multiple questions. Port + expand.
8. **`state-monad.md` (root)** — Tier-1 lecture topic; covers all 10 patterns including the labelling traversal that's the most common Q3+Q1 combination. ~5 marks. Port — but merge with [state](../monads/state.md).
9. **`interpreter-extension.md`** — the 3-layer change template with `for`, `do-while`, `++`/`--` worked. Aligns directly with W10 Q1 and any "extend the interpreter" question. ~7 marks. Port verbatim.
10. **`archetypes/00-priority.md`** — the ranking matrix; tells the student which Q to do first under time pressure. Marginal but real; if a student saves 5 minutes by skipping Tier-4 first, that's ~3 marks. Port.

Honourable mentions: `prelude-cheatsheet.md` (forget-a-function recall), `mapm.md` (every monad question secretly uses this), [free](../monads/multi-effect.md) (only A3 reference), `examples/grid-zipper.md` (only A1 reference if A1 returns).

## Top 10 things to DROP

1. **`SEARCH-INDEX.md`** — hand-maintained keyword phonebook with broken links (e.g. `MockTest-Practice.md` references a file with the wrong path); pretends `bash search.sh` is available without ever providing the script. Replace with VS Code `Ctrl+Shift+F` instruction + nothing else.
2. **`NAVIGATION.md`** — flat alphabetical list of every file. Duplicates `INDEX.md`. Of zero use during an exam — a student doesn't browse alphabetically, they jump by topic. Combine with INDEX or delete.
3. **`patterns/triggers.md`** — explicitly superseded by `if-you-see-x.md` per its own header. Same content, two tables.
4. **`patterns/pitfalls.md`** — explicitly superseded by `common-pitfalls.md` per its own header.
5. **`templates/type-decoder.md`** — explicitly superseded by `type-signature-decoder.md` per its own header.
6. **`syntax/list-monad.md` AND [list-monad](../monads/list-monad.md)** — keep one, drop the other. They cover the same `do`/comprehension equivalence and knight-moves example.
7. **`syntax/maybe.md` AND `syntax/either.md`** — duplicate of [maybe](../monads/maybe.md) and [either](../monads/either.md). Two files per ADT × seven monads is too many.
8. **`practice/09-mock-and-misc.md`** (and arguably all of `practice/`) — 287-line code dump from six different student files with no narrative; reduces to "here is some code I once wrote". As a grep corpus it'd work better as a single `.hs` file, not 10 markdown wrappers.
9. **`HOW-TO-USE.md`** — 313 lines of meta-meta-instructions on how to use the vault (which is itself a meta-tool). A panicking student will not read 313 lines. Reduce to a 20-line README + the exam-day-plan.
10. **`exam-day-plan.md`** alongside **`SOLUTION-PROCESS.md`** alongside **`ONE-PAGE.md`** — three overlapping "what to do in the exam" files. Keep ONE; merge the others' content as appendices.

Bonus drops (would be #11-#15):
- `patterns/README.md`, `templates/README.md`, [README](../monads/README.md), etc. — the directory READMEs are mostly tables-of-contents that the file system already provides.
- [overview](../interpreters/README.md) — duplicate of [README](../interpreters/README.md).
- [overview](../monads/README.md) AND `syntax/monads-overview.md` — pick one.
- [README](../archetypes/README.md) — table of contents the `00-priority.md` matrix already provides.
- `tree-recursion.md` (root) — superseded by content in `patterns/tree-recursion.md` AND `templates/tree-bt.md`/`templates/tree-rose.md`.

## Summary table

| Category | Verdict |
|---|---|
| Lookup-velocity infrastructure (if-you-see-x, common-templates, type-sig-decoder) | Port the idea, rebuild the content |
| Mock-test worked solutions (`examples/mock-q*`) | Port verbatim — best in the vault |
| Archetype ranking + 20 question shapes | Port priority matrix; thicken the per-archetype files |
| Monad references (state, writer, free) | Port — best per-monad coverage |
| Interpreter coverage | Decent depth-1; missing depth-2 (parser-eval integration) |
| Tree coverage | Six duplicates of one template; missing tricky BST cases |
| BST | Has the algorithms; inconsistent `isBST` impls across files; needs ONE walkthrough |
| Parser combinators | Toy expr/term/factor only; missing chainl1, applicative-only |
| QuickCheck | Completely absent; the marker is QuickCheck and the vault never shows a `prop_*` |
| Practice/ | Drop — grep corpus dressed as study notes |
| Syntax/ | Friendly intros; duplicates typeclasses/ and monads/ |
| Templates/ | Useful copy-paste sources; drop the obsoleted type-decoder |
| Typeclasses/ | Port; thicken with kind-and-partial-application content |

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
