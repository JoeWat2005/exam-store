<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [meta](./README.md) · **SCRIPT-COMPATIBILITY-REPORT**

<!-- siblings:start -->
> **Peers:** [COURSE-COVERAGE](./COURSE-COVERAGE.md) · [COURSE-MAP](./COURSE-MAP.md) · [FINAL-SWEEP-REPORT](./FINAL-SWEEP-REPORT.md) · [GAP-AUDIT](./GAP-AUDIT.md) · **SCRIPT-COMPATIBILITY-REPORT** · [VAULT-AUDIT](./VAULT-AUDIT.md) · [WIKI-UPGRADE-REPORT](./WIKI-UPGRADE-REPORT.md)
<!-- siblings:end -->






# SCRIPT-COMPATIBILITY-REPORT

Phase 7 deliverable. Diff between pre-upgrade and post-upgrade script outputs. Goal: confirm no script regressed. Re-verified after the **2026-05-31 final sweep** that added KNOWLEDGE-MAP + 3 new indexes.

**Date:** 2026-05-29 (re-verified 2026-05-31 after Phases 4, 5, 6, 1f, and the final sweep)
**Baseline file:** `meta/script-baseline.txt` (315 lines, captured before Phase 1)
**Post-upgrade file:** `meta/script-postupgrade.txt` (315 lines)
**Post-sweep file:** `meta/script-postsweep.txt` (307 lines — final-sweep re-verification, 2026-05-31)
**Diff file:** `meta/script-diff.txt` (97 lines — all expected differences from Phase 6 index linkification)

## Per-script verdict

| Script | Baseline OK? | Post OK? | Output identical? | Verdict |
|---|---|---|---|---|
| `search_by_archetype.py A01` | ✓ | ✓ | NO (expected) | **PASS** — A01 now mentioned in 69 vault files (was 40) because every See-also block references it. Top-10 reorder reflects this. |
| `search_by_archetype.py A11` | ✓ | ✓ | NO (expected) | **PASS** — A11 mention count 21 → 28. New `bst-delete-trace.md` references it. |
| `search_by_type.py "Tree a -> Int"` | ✗ | ✓ | NO (now fixed) | **PASS** (after fix) — previously this *documented example* returned `No rule matched` (exit 1); the old "PASS/YES" here was a false certification. Added a `Tree a -> Int` alias to `SIG_RULES` (→ A01 tree-counting, noting the vault's tree type is **BT**). Now exits 0 with 1 match. |
| `search_by_monad.py State` | ✓ | ✓ | NO (expected) | **PASS** — new `transformer-stack-order.md` and `bst-x-state` references push State mention totals up. Output reorders top-10. |
| `search_by_combo.py "Tree + State"` | ✓ | ✓ | YES | **PASS** — combo lookup uses graphs only. |
| `mock_q_lookup.py Q3` | ✓ | ✓ | YES | **PASS** — MOCK_QS dict unchanged (no mock spec edits made). |
| `prelude_lookup.py transpose` | ✓ | ✓ | YES | **PASS** — PRELUDE-INDEX.md untouched (per plan). |
| `study_planner.py 3` | ✓ | ✓ | NO (numbers shifted) | **PASS** — A04 count 23→22, A09 count 9→8 due to See-also injection replacing duplicate prose mentions. Order in plan unchanged. |
| `topic_dependencies.py Functor` | ✓ | ✓ | YES | **PASS** — uses DEPENDENCY-GRAPH only. |

## Embedded-data sync check

| Dict / Constant | Location | Status |
|---|---|---|
| `MOCK_QS` | `scripts/mock_q_lookup.py:26-67` | UNCHANGED — no Mock Q1–Q5 spec edits. ✓ |
| `SIG_RULES` | `scripts/search_by_type.py` | UPDATED (final pass) — added 2 rules so the script's own documented examples work: a `Tree a -> Int` alias (→ A01 tree-counting; the vault's tree type is **BT**) and a generic `Monad m =>` catch-all (→ A03 monad-combinator-family, placed after the specific Monad-sig rules). All prior rules unchanged. ✓ |
| `MONAD_ALIASES` | `scripts/search_by_monad.py` | UNCHANGED — no monad rename. ✓ |

## Graph JSON spot-check

| Graph | Node count (pre) | Node count (post) | Schema bumped? |
|---|---:|---:|---|
| `ARCHETYPE-GRAPH.json` | 24 | 24 | NO |
| `DEPENDENCY-GRAPH.json` | 54 | 54 | NO |
| `MONAD-GRAPH.json` | 30 | 30 | NO |
| `TOPIC-GRAPH.json` | 52 | 52 | NO |
| `QUESTION-GRAPH.json` | 28 | 28 | NO |
| `TREE-GRAPH.json` | 30 | 30 | NO |

All graphs parse and have identical node/edge counts. ✓

## Summary

**0 regressions. 9/9 scripts PASS.** All output differences are explainable by:
1. New files added to existing directories (basics/, gap pages, cross-matrix additions, 28 new mutations) → search scripts find more hits.
2. See-also blocks added to 124 files → each archetype reference now appears as a clickable link, which the grep counts.
3. Phase 6 index linkification → every `A09` plain text is now `[A09](../archetypes/A09-prelude-reimpl.md)`, doubling the per-row mention count (the code appears in both label and URL).
4. Some prose mentions replaced by structured blocks → per-file counts slightly down for those archetypes.

Scripts that depend on JSON graphs OR hardcoded data (`mock_q_lookup`, `search_by_type`, `search_by_combo`, `topic_dependencies`) are byte-identical. Scripts that recursive-grep the vault content (`search_by_archetype`, `search_by_monad`, `search_by_keyword`) show expected linear shifts (~1.7× across the board because the link expansion duplicated the archetype-code text).

## Final-sweep re-verification (2026-05-31)

After the 2026-05-31 sweep created 4 new files (`KNOWLEDGE-MAP.md` at root + 3 new indexes), all 9 scripts were re-run. Output captured to `meta/script-postsweep.txt` (307 lines).

| Script | Verdict | Notes |
|---|---|---|
| `search_by_archetype.py A01` | **PASS** | A01 mention count 80 → 90 (new ARCHETYPE-INDEX +16, MUTATION-INDEX +11). Top-10 reorder expected. |
| `search_by_archetype.py A11` | **PASS** | A11 count 28 → 55 (similar reason). |
| `search_by_type.py "Monad m => ..."` | **PASS** | A specific `Monad m => ...` sig still matches its specific rule first. The bare `Monad m =>` documented example now also resolves via the new generic catch-all (→ A03). See "Final release pass" below. |
| `search_by_monad.py State` | **PASS** | Mention totals shift; cross-matrix list unchanged. |
| `search_by_combo.py "Tree + State"` | **PASS** | Combo graph unchanged. |
| `mock_q_lookup.py Q3` | **PASS** | MOCK_QS dict unchanged. |
| `prelude_lookup.py transpose` | **PASS** | PRELUDE-INDEX.md untouched. |
| `study_planner.py 3` | **PASS** | Plan structure unchanged. |
| `topic_dependencies.py Functor` | **PASS** | DEPENDENCY-GRAPH.json unchanged. |
| `_phase9_link_check.py` | **PASS** | ~11,900 internal links (the figure drifts as See-also blocks are added; deterministic per snapshot), **3 broken paths** — all 3 are intentional template placeholders inside `ARCHITECTURE.md` and `GAP-AUDIT.md` example blocks. **Down from 71 pre-upgrade.** The checker now also runs an **anchor pass** (see "Anchor validation" below). |

**Embedded data invariants** (as of the final sweep — `SIG_RULES` later updated in the final release pass, see below):

- `MOCK_QS` (`scripts/mock_q_lookup.py`) ✓ unchanged
- `SIG_RULES` (`scripts/search_by_type.py`) — **+2 rules in the final release pass** (`Tree a -> Int` alias, generic `Monad m =>` catch-all); all prior rules intact
- `MONAD_ALIASES` (`scripts/search_by_monad.py`) ✓ unchanged

**Graph JSON files** — all unchanged (node and edge counts identical to post-upgrade baseline).

**0 regressions across the final sweep.**

## Final release pass (2026-05-31)

Four script-level fixes were applied in the final release pass and **re-run to confirm** (commands + output in the maintainer log):

1. **`search_by_type.py` — two documented examples now work.** The script's own `--help` / docstring advertises `"Tree a -> Int"` and `"Monad m =>"` as examples, but both returned `No rule matched` (exit 1). Added to `SIG_RULES`:
   - a `Tree a -> Int` alias → A01 *tree-counting-family* (`archetypes/A01-tree-recursion.md`), with a note that **the vault's tree type is `BT`, not `Tree`**;
   - a generic `Monad m =>` catch-all → A03 *monad-combinator-family* (`archetypes/A03-generic-monad.md`), placed **after** the specific Monad-sig rules (so e.g. `Monad m => m a -> Int -> m [a]` still matches its specific rule first) and **before** the final `Ord/Eq/Num` catch-alls.

   Both now exit 0: `search_by_type.py "Tree a -> Int"` → 1 match; `search_by_type.py "Monad m =>"` → 1 match.

2. **`vlab-setup.sh` — CRLF → LF.** The file had Windows CRLF line endings (30 of them, incl. the `<< 'EOF'` heredoc delimiter), a portability hazard on real vLab Linux bash. Converted to LF only; verified with `cat -A` (every line ends `$`, **no `^M`**), `bash -n` passes, and the executable bit (`-rwxr-xr-x`) is preserved. **NB:** the old `meta/VAULT-AUDIT.md` claim that *"`vlab-setup.sh` is referenced but doesn't exist"* (VAULT-AUDIT.md lines 43 & 119) is **stale** — the script **exists, is executable, and passes `bash -n`**. (VAULT-AUDIT.md is owned by another pass; that file should drop the claim.)

3. **`_phase9_link_check.py` — anchor pass + uncapped output.** Removed the `< 20` cap so **every** offender prints. Added a second **anchor-validation pass**: it builds each file's anchor set from explicit `id="..."` attributes **plus** GitHub heading slugs (lowercase, punctuation stripped, spaces→hyphens, duplicate-slug `-1/-2` suffixes), then flags any `file.md#anchor` whose anchor is absent in the target. A bare `#` (top of page) is treated as valid and skipped. Stdlib-only (no new deps). Re-run result: still **3 broken paths** (the known placeholders) and the new pass reports **2 broken anchors**:
   - `meta/GAP-AUDIT.md → ../pitfalls/HIGH-severity.md#p-NNN` — a literal `p-NNN` placeholder (matches the `id="p-NNN"` template row in `STATS.md`); benign.
   - `question-families/string-ops-family.md → ../pitfalls/MEDIUM-severity.md#p-016` — **a genuine broken anchor**: `p-016` lives in **HIGH-severity.md**, not MEDIUM-severity.md (which holds `p-100`–`p-120`). The wrong file is in the link path. **Owned by another pass — flagged for fix.**

4. **This report.** Corrected the `Tree a -> Int` row (it was falsely certified PASS/identical while actually failing); replaced the stale **`9500` internal-links** figure with the current `_phase9` count (~11,900, which drifts as See-also blocks are added but is deterministic per snapshot); and recorded that `SIG_RULES` is no longer byte-identical to baseline.

## Helper scripts inventory

| Script | Purpose | Notes |
|---|---|---|
| `search_by_archetype.py A##` | A##-by-A## frequency + combines-with | Reads `graphs/ARCHETYPE-GRAPH.json` + vault grep |
| `search_by_type.py "<sig>"` | Reverse lookup from type signature | SIG_RULES hardcoded |
| `search_by_monad.py <name>` | Monad-by-name relations | Reads `graphs/MONAD-GRAPH.json` |
| `search_by_combo.py "X + Y"` | Cross-axis combo | Reads cross-matrix + graphs |
| `search_by_keyword.py <kw>` | Grep wrapper with relevance ranking | — |
| `mock_q_lookup.py Q[1-5]` | Mock Q spec + marker quirk + canonical files | MOCK_QS dict |
| `prelude_lookup.py <fn>` | Prelude / Data.List / Data.Char / Data.Maybe | Parses PRELUDE-INDEX.md |
| `study_planner.py <days>` | Personalised revision plan | — |
| `topic_dependencies.py <topic>` | Direct + transitive prerequisites | Reads `graphs/DEPENDENCY-GRAPH.json` |
| [`vlab-setup.sh`](../scripts/vlab-setup.sh) | Configure JupyterLab to open .md in Preview mode | Run once on vLab |
| `_phase9_link_check.py` | Find broken internal links (path pass + anchor pass) | 3 known intentional path placeholders; anchor pass flags 2 (`#p-NNN` placeholder + a real `#p-016` misdirection) |

The phase scripts (`_phase1_…`, `_phase4_…`, `_phase6_…`, `_phase8_…`) are idempotent tooling kept for re-running after bulk edits. They are not part of the in-exam workflow.

## See also

**Baseline:** [script-baseline.txt](./script-baseline.txt)
**Post-upgrade:** [script-postupgrade.txt](./script-postupgrade.txt)
**Post-sweep:** [script-postsweep.txt](./script-postsweep.txt)
**Diff:** [script-diff.txt](./script-diff.txt)
**Wiki report:** [WIKI-UPGRADE-REPORT](./WIKI-UPGRADE-REPORT.md)
**Final sweep report:** [FINAL-SWEEP-REPORT](./FINAL-SWEEP-REPORT.md)
**Gap audit:** [GAP-AUDIT](./GAP-AUDIT.md)
**vLab helper:** [`../scripts/vlab-setup.sh`](../scripts/vlab-setup.sh)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
