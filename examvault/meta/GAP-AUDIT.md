<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [meta](./README.md) · **GAP-AUDIT**

<!-- siblings:start -->
> **Peers:** [COURSE-COVERAGE](./COURSE-COVERAGE.md) · [COURSE-MAP](./COURSE-MAP.md) · [FINAL-SWEEP-REPORT](./FINAL-SWEEP-REPORT.md) · **GAP-AUDIT** · [SCRIPT-COMPATIBILITY-REPORT](./SCRIPT-COMPATIBILITY-REPORT.md) · [VAULT-AUDIT](./VAULT-AUDIT.md) · [WIKI-UPGRADE-REPORT](./WIKI-UPGRADE-REPORT.md)
<!-- siblings:end -->






# GAP-AUDIT

> **This is the live gap register.** The 2026-05-31 final release-candidate audit (27 compile-gated subagents) superseded the Phase-0 register below.

## Final release-candidate audit — gap status (2026-05-31)

The audit compiled every copy-paste template against GHC 9.6.7 `-XSafe`. The gaps it found were **defects in existing content** (non-compiling or forbidden-import templates) rather than missing topics. All are fixed and re-verified — full list in [FINAL-SWEEP-REPORT](./FINAL-SWEEP-REPORT.md). Headline resolutions:

| Gap found | Severity | Status |
|---|---|---|
| `(x:y:rest) <- get` non-compiling (4 files; `MonadFail Identity`) | critical | **FIXED** → bind-then-`case` |
| A16 parser / A14 interpreter shipped forbidden-import templates | critical | **FIXED** → `Alternative` instance / hand-rolled `EvalM`, both warned |
| A18 memo template missing its `data BT` declaration | critical | **FIXED** |
| `bst` insert/delete `Ambiguous occurrence` vs `Data.List` | critical | **FIXED** → warning + `insertBST`/`deleteBST` |
| `paths` doubling; `countMatchingPath` over-count; `countMaxSoFar` sig | critical | **FIXED** + compile-verified |
| Two non-compiling `winner` templates (problem #150) | critical | **FIXED** |
| **Printable common-templates §8 had the wrong Nim signatures** | high | **FIXED** → official `Heap`/`NimGame` sigs |
| `Sum`/`Data.Monoid` "in scope via Control.Monad.Writer" false claim (9 pages) | high | **FIXED** → whitelist-safe primaries + warnings |
| 23 dead monad→family links; 15 broken pitfall anchors | high | **FIXED** |
| `search_by_type.py` own examples failing; `vlab-setup.sh` CRLF | high | **FIXED** → 9/9 scripts pass; LF endings |
| Sorting algorithms not covered | medium | **ADDED** → [sorting](../haskell-basics/sorting.md) |
| IOPrime `IO'` model / LazyNaturals `biggerThan` missing | medium | **ADDED** |
| Count contradictions (263 vs 291 mutations, 232 vs 236 files) | medium | **RECONCILED** → 238 / 293 / 24 |

### Genuinely-remaining (accepted) limitations
1. The exam may rename ADT constructors — substitution is mechanical ([signature-pitfalls](../pitfalls/signature-pitfalls.md)).
2. `A14` mutations M1–M10 remain mtl-shaped (recognition-only; the canonical template is now hand-rolled + warned).
3. `Sum`/`Product` Writer forms are Types-module-dependent (warned on every page).
4. `lazy-infinite` M6 `memoFib` index scheme is illustrative, not a guaranteed copy-paste.

---

*The Phase-0 register below is retained for history. Its counts (23 families / 235 mutations / cap 12 / a 144-file `notehost-vault/`) are pre-final-pass and superseded by the table above — `notehost-vault/` is now empty.*

Phase-0 audit driving the 2026-05-29 wiki-upgrade work. Each gap row will be updated in Phase 7 to **FILLED**, **DEFERRED**, or **RECLASSIFIED**.

## 1. Verified content gaps

| # | Topic | Search performed | Result | Exam-leverage | Phase | Status |
|---|---|---|---|---:|---|---|
| G-01 | `prop_…` real properties (not attack-prose) | `grep -rlE "prop_[a-zA-Z]"` | Found in 18 cross-matrix files + monad-laws + VAULT-AUDIT. **NO dedicated consolidation page; no examiner-grade `Arbitrary` instances for BT / Rose / Expr** | 5 | 3 | **FILLED** → [quickcheck/PROPERTY-PATTERNS.md](../quickcheck/PROPERTY-PATTERNS.md) |
| G-02 | `Arbitrary` instance code | `grep -rlE "\bArbitrary\b"` | Mentioned in 15 files; concentrated in `quickcheck/*-attacks.md` as prose. **No instance code (`arbitrary = sized $ \n -> …`) anywhere.** | 5 | 3 | **FILLED** → [quickcheck/PROPERTY-PATTERNS.md §3](../quickcheck/PROPERTY-PATTERNS.md) |
| G-03 | BST delete two-children worked trace (in-order successor / predecessor) | `grep -E "predecessor\|successor" trees/` | **0 matches in `trees/`** (one match in `monads/README.md` for an unrelated `Either` line). The 4-case `delete` is in `trees/bst.md` but no execution trace. | 4 | 3 | **FILLED** → [trees/bst-delete-trace.md](../trees/bst-delete-trace.md) |
| G-04 | Transformer stack order (`StateT s (Either e)` vs `ExceptT e (State s)`) | `grep -E "StateT.*Either\|ExceptT.*State" monads/` | **1 mention** in `monads/README.md` line 106 only. No worked comparison page. | 3 | 3 | **FILLED** → [monads/transformer-stack-order.md](../monads/transformer-stack-order.md) |
| G-05 | `chainl1` / `chainr1` parser combinator | `grep -E "chainl1\|chainr1"` | **0 matches across the whole vault.** Parser content exists in `interpreters/parser-overview.md` but no precedence-chained operator example. | 3 | 3 | **FILLED** → [interpreters/parser-chainl1.md](../interpreters/parser-chainl1.md) |
| G-06 | `MonadFail` in `do`-pattern bind | `grep "MonadFail"` | **0 matches.** Pattern-binds like `IVal x <- eval env e1` rely on it silently across env-eval examples. | 2 | 4 | **PARTIAL** — covered in [haskell-basics/do-notation-basics.md](../haskell-basics/do-notation-basics.md) common-mistakes; standalone page deferred |
| G-07 | `{-# LANGUAGE Safe #-}` pragma rules | `grep -E "-XSafe\|LANGUAGE Safe"` | **0 matches** in vault (the pragma rule exists in `pitfalls/HIGH-severity.md` as P-011 / P-026 but is not collated as a topic page). | 3 | 4 | **PARTIAL** — covered in [P-011](../pitfalls/HIGH-severity.md#p-011) and [P-026](../pitfalls/HIGH-severity.md#p-026); standalone topic page deferred |
| G-08 | Pitfall references by ID from archetypes / families / cross-matrix | `grep -rl "P-[0-9]{3}" archetypes question-families cross-matrix` | **0 files reference pitfalls by ID.** Phase 1 See-also blocks must inject these from scratch — not re-link existing references. | 4 | 1 | **FILLED** → archetype See-also blocks now include `[P-NNN ...](../pitfalls/HIGH-severity.md#p-NNN)` links |

## 2. Mutation counts per question-family

Heading convention: `### Mutation N — <name>` (verified). Hard cap is 12.

| Family | Mutations | Headroom | Phase-4 candidate? |
|---|---:|---:|---|
| adt-translation-family | 10 | 2 | yes |
| applicative-monad-instance-family | 10 | 2 | yes |
| bst-ops-family | 10 | 2 | yes |
| codec-family | 11 | 1 | yes |
| env-eval-family | 10 | 2 | yes |
| error-handling-family | 10 | 2 | yes |
| functor-instance-family | 10 | 2 | yes |
| lazy-infinite-family | 10 | 2 | yes |
| list-comp-family | 10 | 2 | yes |
| list-fold-family | **12** | 0 | **LOCKED** |
| list-rewrite-family | **12** | 0 | **LOCKED** |
| matrix-predicate-family | 10 | 2 | yes |
| monad-combinator-family | 10 | 2 | yes |
| parser-family | 10 | 2 | yes |
| pretty-print-family | 10 | 2 | yes |
| rose-ops-family | 10 | 2 | yes |
| state-counter-family | 10 | 2 | yes |
| state-game-family | 10 | 2 | yes |
| tree-counting-family | 10 | 2 | yes |
| tree-extract-family | 10 | 2 | yes |
| tree-transform-family | 10 | 2 | yes |
| tree-validation-family | 10 | 2 | yes |
| writer-trace-family | 10 | 2 | yes |

**Totals:** 23 families, 235 mutations, 21 families eligible, **theoretical max +41 mutations** if every slot earns its place under the structural-differentiation rule. Realistic Phase-4 target: ~25–30 high-quality additions.

## 3. Pitfall inventory (anchor targets for Phase 1)

Heading convention: `## P-NNN · <title>` (two hashes, middle-dot separator).

- `pitfalls/HIGH-severity.md` — P-001 … P-030 (30 anchors)
- `pitfalls/MEDIUM-severity.md` — ~21 anchors (verify in Phase 1)
- `pitfalls/LOW-severity.md` — ~17 anchors (verify in Phase 1)

Total anchor injections: ~68.

## 4. Mock-Q anchor targets

`indexes/MOCK-Q-INDEX.md` uses `## Q1 — …` headings. Inject `<a id="mock-q1"></a>` through `<a id="mock-q5"></a>` (5 anchors).

## 5. Linking opportunities catalogued

Files that already use markdown link syntax `[label](path)` (exemplars to propagate):
- `examvault/README.md` (root) — uses standard markdown links throughout the routing table.

Files that use backtick-paths (`` `../monads/state.md` ``) — must convert to clickable links:
- All `monads/*.md` See-also tails
- All `archetypes/A##-*.md` Combines-with sections (use bare A## prose)
- Most `cross-matrix/*-x-*.md` files
- `meta/COURSE-MAP.md` (1286 lines — high-value linkification target)

## 6. Source materials NOT yet ported

From `notehost-vault/markdownvault/` (144 files in old vault):
- Mock test worked solutions Q1–Q5 — may overlap with existing `indexes/MOCK-Q-INDEX.md` (246 lines). Phase-6 audit.
- Priority matrix (tier 1–4) — already in `archetypes/README.md`. RECLASSIFIED.
- Common-pitfalls with named-student-bug refs — present in `pitfalls/HIGH-severity.md`. RECLASSIFIED.

## 7. Script baseline (regression target)

Captured to `meta/script-baseline.txt` (315 lines). 9 scripts × ~35 lines stdout each. Phase 7 diff target.

## 8. Phase-1 link-injection budget (estimate)

| Directory | Files | Avg lines | See-also blocks to inject |
|---|---:|---:|---:|
| archetypes/ | 25 | 188 | 25 |
| question-families/ | 24 | 226 | 24 |
| cross-matrix/ | 19 | ~200 | 19 |
| trees/ | 11 | ~150 | 11 |
| monads/ | 13 | ~160 | 13 |
| typeclasses/ | 11 | ~140 | 11 |
| interpreters/ | 16 | ~180 | 16 |
| quickcheck/ | 16 | ~220 | 16 |
| pitfalls/ | 7 | ~400 | 7 |
| exam-day/ | 7 | ~170 | 7 |
| meta/ | 3 | ~500 | 3 |
| indexes/ | 9 | ~300 | 9 |
| **Total** | **161** | — | **161** |

Plus root README and HOW-TO-USE / ARCHITECTURE / STATS (4 files). Grand total: **~165 link-injection edits in Phase 1**.

## 9. Phase ordering (locked from plan)

0 → 1 → 2 → 3 → 4 → 5 → 6 → 7.

Phase boundaries are commit points. Each phase delivers value alone.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
