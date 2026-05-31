<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [meta](./README.md) · **FINAL-SWEEP-REPORT**

<!-- siblings:start -->
> **Peers:** [COURSE-COVERAGE](./COURSE-COVERAGE.md) · [COURSE-MAP](./COURSE-MAP.md) · **FINAL-SWEEP-REPORT** · [GAP-AUDIT](./GAP-AUDIT.md) · [SCRIPT-COMPATIBILITY-REPORT](./SCRIPT-COMPATIBILITY-REPORT.md) · [VAULT-AUDIT](./VAULT-AUDIT.md) · [WIKI-UPGRADE-REPORT](./WIKI-UPGRADE-REPORT.md)
<!-- siblings:end -->




# FINAL-SWEEP-REPORT

**Completion certificate for the FINAL RELEASE-CANDIDATE AUDIT — 2026-05-31 (T-1 before the exam).**

This pass is different from every earlier one. Earlier passes *built* the vault. This pass treated it as a **release candidate** and asked one question: *"If I walked into the exam tomorrow with only examvault, what would still cost marks?"* — then fixed it. The work was distributed across **27 specialist subagents** in three waves, and **every Haskell change was compiled** against the real exam toolchain (GHC 9.6.7, `-XSafe`) before being accepted.

---

## TL;DR

| Metric | Value |
|---|---:|
| Total `.md` files | **238** (was 236; +`haskell-basics/sorting.md`, +`graphs/README.md`) |
| Mutations | **293** across **24** families (cap 25) |
| Archetypes | 24 (A01–A24) |
| Broken internal links (path) | **3** (intentional template placeholders) |
| Broken internal links (anchor) | **1** (intentional `#p-NNN` placeholder); the real anchor bug found this pass is fixed |
| Helper scripts | 9/9 PASS (both previously-broken `search_by_type` examples now work) |
| Haskell templates compiled this pass | **~60** snippets, all green under `-XSafe` + allowed imports |
| Verdict | **Release-ready.** Every critical copy-paste defect found has been fixed and re-verified. |

---

## Method — multi-agent, compile-gated

| Wave | Agents | What they did |
|---|---:|---|
| **Audit** | 12 | Independent specialists (coverage, code-correctness, exam-setter, archetype, mutation, navigation, link-integrity, beginner, quickcheck, script-validation, consistency, basics-testing). Each *inspected the repo and compiled the templates* — they did not trust the vault's self-description. |
| **Fix** | 12 | Disjoint-file fix agents, each required to compile-verify every Haskell change under `-XSafe` with only the allowed imports before reporting done. |
| **Cleanup** | 3 | Follow-up sweep (out-of-scope items the fix agents flagged), the Writer-`Sum` cross-matrix sweep, and the count/label reconciliation. |

The decisive tool was the compiler. GHC 9.6.7 / mtl-2.3.1 (the course's toolchain) was confirmed present, so "this template is correct" meant "this template was pasted into a `{-# LANGUAGE Safe #-}` module with allowed imports only and it compiled and produced the documented output."

---

## What the audit found (and this pass fixed)

The vault's **structure** was already excellent — 0 orphan pages, 0 dead-ends, the "exactly 3 broken links" claim held for path-links, the scripts ran, and the beginner pages were well-pitched. The damage was concentrated in **copy-paste Haskell that did not compile or was silently wrong** — the single worst defect class, because the student pastes it and loses the marks.

### Tier 1 — non-compiling / wrong templates (would score 0 on the question)

| # | Defect | Where | Fix |
|---|---|---|---|
| 1 | `(x:y:rest) <- get` is a **compile error** in plain `State` (no `MonadFail Identity`) | stack-calculator in `A02`, `expr-state`, `monads/state`, `state-game-family`; false advice on `state.md` | rewrite to `s <- get; case s of …`; corrected the pitfall text |
| 2 | Parser archetype **doesn't compile** (`MonadPlus` needs `Alternative`, which needs a non-whitelisted import) | `A16-parser-combinators` | rewrote to an `Alternative` instance + a prominent "`Control.Applicative` is NOT whitelisted" warning; fixed the false `parse expr "1+2*3"` claim |
| 3 | Interpreter canonical imports **`Control.Monad.Except`** (forbidden) | `A14-multi-effect-interp` | made a hand-rolled `EvalM a = Stack -> Either String (a, Stack)` the primary template; demoted the transformer form |
| 4 | Memo template uses `Fork`/`BT` with **no `data` declaration** | `A18-lazy-memo` | added `data BT a = Fork a (BT a) (BT a)`; made the trigger comment consistent |
| 5 | BST `insert`/`delete` **`Ambiguous occurrence`** once `Data.List` is imported | `trees/bst` | warning box + `insertBST`/`deleteBST` aliases |
| 6 | `paths` **silently doubles** every root-to-leaf path | `trees/binary-tree` | corrected to leaf-terminating recursion |
| 7 | `countMatchingPath` **over-counts** (phantom path at every `Empty` child) | `tree-counting-family` M14 | corrected; verified returns 1 on a one-path tree |
| 8 | `countMaxSoFar` advertised `Ord a =>` but body needs `Bounded` (`minBound`) → won't compile | `tree-counting-family` M9 | rewrote to seed from the root; signature now honest |
| 9 | Two non-compiling `winner` templates (`Maybe Player` vs `[[Maybe Player]]` type error) | `state-game-family` M9, `matrix-predicate-family` | corrected both; added the missing `listToMaybe`/`transpose` imports |
| 10 | `takeTokensWithLog` + `rewindMoves` — undefined `Player`, `NimGame` used as a value (kind error) | `state-game-family` M11/M12 | retyped to operate on `NimBoard` with the family's `Heap` |
| 11 | **The printable "carry-in" sheet had the wrong Nim signatures** (`State NimGame ()` is a kind error) | `haskell-basics/common-templates` §8 | fixed to the official `takeTokens :: Int -> Heap -> NimGame ()` / `gameOver :: NimGame Bool` |

### Tier 2 — forbidden-import traps (auto-score 0 even though the logic is fine)

- **`Sum`/`Product`/`Any`/`All` are not whitelisted** and are *not* re-exported by `Control.Monad.Writer` on current mtl (`import Control.Monad.Writer` alone → *"Not in scope: Sum"*). The vault claimed they were in scope. Fixed in `monads/writer`, `A15`, `typeclasses/foldable`, `writer-trace-family`, **and** all four `cross-matrix/*-x-writer` pages + `quickcheck/writer-attacks` — each now leads with a whitelist-safe template (`Writer [()]`/`[String]` + `length`, `State Int`, or a local `newtype` `Monoid`) and warns about the `Data.Monoid` form.
- Banned-import warnings + allowed-imports alternatives added wherever a mutation imported `Data.Map`, `Control.Monad.Reader`, `Control.Monad.Except`, `Control.Monad.Trans.Writer`, or `Control.Applicative`.
- `numeric-attacks` offered `import Data.Number (isNaN)` (not in base; `isNaN` is in Prelude) → removed.
- State testing recipe used `replicateM` under `Control.Monad.State` alone (not in scope) → added `import Control.Monad`.

### Tier 3 — findability, correctness of the index, and content gaps

- **23 dead** "question-family" links across the 8 monad pages → repointed to the real `*-family.md`.
- **15 broken pitfall anchors** (a numbering collision: `p-016…p-029` live only in `HIGH-severity.md`) → repointed; the link-checker now validates anchors too.
- `search_by_type.py`'s own two documented examples (`"Tree a -> Int"`, `"Monad m =>"`) failed → added the matching rules; **9/9 scripts now pass**.
- `vlab-setup.sh` had CRLF endings (a real vLab/Linux hazard) → converted to LF.
- Count reconciliation: the vault contradicted itself (`263` vs `291` mutations, `232` vs `236` files, four different link totals). Now consistent at **238 .md / 293 mutations / 24 families / cap 25 / 48 haskell-basics**.
- `rose-ops` M6 had **wrong code labelled "Solution"** (`mapRose id`) → swapped; correct version is the solution, the bug is a clearly-labelled callout.
- `P-010` "`deriving Functor` is forbidden under Safe" was **false** (it's `GeneralizedNewtypeDeriving` that Safe blocks) → reworded across 4 pages.
- `parser-family` header said Archetype **A17** (the zipper) → corrected to **A16**.

### New content added this pass

- **`haskell-basics/sorting.md`** — the five hand-rolled sorts (insertion, selection, bubble, quick, merge), each compile-verified, with `isSorted` / permutation / length QuickCheck properties and the classic pitfalls (quicksort dropping pivot-duplicates; merge sort's mandatory `[x]` base case). Wired into the README, all three lookup indexes, the list-family See-also blocks, and every basics sibling strip.
- **IOPrime `IO'`-as-data** model added to `monads/io.md` (the one lecture topic the vault advertised but never implemented).
- **LazyNaturals `biggerThan` / `checkLengthBiggerThan`** — the lecture's central fast-length-comparison — added to `lazy-infinite-family`.
- **`chainr1`**, **`collectErrors`**, the **`Validation` accumulating applicative**, the **function functor `((->) r)`**, and **`qsort`-via-comprehension** replaced five duplicate "+1" mutations with genuinely-distinct exam shapes.
- **`graphs/README.md`** created (the one directory that lacked one).

---

## Validation (re-run after all fixes)

- **Link checker** (`scripts/_phase9_link_check.py`, now with an anchor-validation pass): `Broken (path): 3` — the three intentional `(path)` template placeholders in `ARCHITECTURE.md` and `GAP-AUDIT.md`; `Broken (anchor): 1` — the intentional `#p-NNN` placeholder. No real breakage.
- **Scripts:** 9/9 run clean from inside `examvault/`, including `search_by_type "Tree a -> Int"` and `"Monad m =>"`.
- **Counts re-grepped:** 238 `.md`; 293 `### Mutation` headers across 24 families; 68 pitfall anchors.
- **Independent spot-compiles** (not just trusting the agents): the corrected `countMatchingPath` returns `1` on a one-path tree; `winner` returns `Just X`; the five sorts return `[1,2,3,3,3,5,7,8,9]` (duplicates preserved) — all under `-XSafe`.

---

## Remaining known limitations (honest)

These are deliberately-accepted, not oversights:

1. **The exam may rename the ADT constructors.** All vault code uses the mock's names (`BT = Empty | Fork`, `Rose = Leaf | Branch`, `Heap = First | Second`). If the real `Types.hs` differs, substitution is mechanical — flagged in [signature-pitfalls](../pitfalls/signature-pitfalls.md) and [IN-EXAM-WORKFLOW](../exam-day/IN-EXAM-WORKFLOW.md).
2. **`A14` mutations M1–M10 still show transformer/mtl shapes.** The canonical template is now the hand-rolled allowed-imports version and the page warns prominently; the mtl mutations are *recognition-only* for when the question supplies the stack.
3. **`Sum`/`Product` Writer forms are correct only if the question's `Types` module provides them.** Every such block now says so; the default template is whitelist-safe.
4. **`lazy-infinite` Mutation 6 (`memoFib`)** keeps a hand-wavy index scheme — usable as a concept, not a guaranteed copy-paste; flagged on the page.
5. **Link/file counts drift ±1 run-to-run** (writing a count into a page is itself a counted link). The headline figures use `~` for the link total; the stable invariant is the broken-link count.

---

## Recommended emergency revision route

Triage by hours left. All paths terminate at ONE-PAGE-PANIC, the LAST-HOUR-CHECKLIST, or the Mock-Q drill.

**≤ 60 minutes** → [ONE-PAGE-PANIC](../exam-day/ONE-PAGE-PANIC.md) (memorise the 5 templates) + [HIGH-severity P-001…P-007](../pitfalls/HIGH-severity.md) + one weakest Mock-Q quirk + sleep.

**2–4 hours** → [LAST-HOUR-CHECKLIST](../exam-day/LAST-HOUR-CHECKLIST.md) + re-do **Mock Q3 (Nim)** cold + re-read all 30 HIGH pitfalls + [common-templates](../haskell-basics/common-templates.md) (now with the corrected Nim sigs).

**6–12 hours** → [BEGINNER-INDEX](../indexes/BEGINNER-INDEX.md) stages 4–5 + all five Mock Qs cold against [TIME-BUDGET](../exam-day/TIME-BUDGET.md) + each Tier-1 archetype once via [ARCHETYPE-INDEX](../indexes/ARCHETYPE-INDEX.md).

**1–3 days** → `py scripts/study_planner.py 3`; drill your 4 weakest mutation families off-template from [MUTATION-INDEX](../indexes/MUTATION-INDEX.md); re-do every Mock Q and score yourself.

**≥ 7 days** → [BEGINNER-INDEX](../indexes/BEGINNER-INDEX.md) end-to-end + every Tier-1/Tier-2 archetype.

---

## Completion criteria

| Criterion | Status |
|---|---|
| examvault is self-contained | ✓ |
| Course coverage verified against lecture notes / sheets / assignments / MockTest | ✓ (12-agent audit) |
| Every copy-paste template compiles under `-XSafe` + allowed imports | ✓ (compile-gated fixes) |
| Forbidden-import traps removed or warned | ✓ |
| Navigation: links comprehensive, anchors valid, no orphans/dead-ends | ✓ |
| Scripts still work | ✓ (9/9) |
| Sorting algorithms added | ✓ ([sorting](../haskell-basics/sorting.md)) |
| Testing-in-GHCi + GHCi commands + allowed-builtins covered | ✓ |
| Counts consistent across hub pages | ✓ (238 / 293 / 24) |
| Reports updated | ✓ (this + [GAP-AUDIT](./GAP-AUDIT.md) + [SCRIPT-COMPATIBILITY-REPORT](./SCRIPT-COMPATIBILITY-REPORT.md)) |

**Release-candidate audit complete.** Stop editing; revise.

---

## See also

**Sibling reports:** [GAP-AUDIT](./GAP-AUDIT.md) · [SCRIPT-COMPATIBILITY-REPORT](./SCRIPT-COMPATIBILITY-REPORT.md) · [COURSE-COVERAGE](./COURSE-COVERAGE.md) · [VAULT-AUDIT](./VAULT-AUDIT.md) · [WIKI-UPGRADE-REPORT](./WIKI-UPGRADE-REPORT.md)
**Vault entry:** [HOME](../HOME.md) · [KNOWLEDGE-MAP](../KNOWLEDGE-MAP.md) · [HOW-TO-USE](../HOW-TO-USE.md)
**Exam-day routes:** [ONE-PAGE-PANIC](../exam-day/ONE-PAGE-PANIC.md) · [LAST-HOUR-CHECKLIST](../exam-day/LAST-HOUR-CHECKLIST.md) · [IN-EXAM-WORKFLOW](../exam-day/IN-EXAM-WORKFLOW.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
