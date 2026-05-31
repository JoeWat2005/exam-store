<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [meta](./README.md) · **WIKI-UPGRADE-REPORT**

<!-- siblings:start -->
> **Peers:** [COURSE-COVERAGE](./COURSE-COVERAGE.md) · [COURSE-MAP](./COURSE-MAP.md) · [FINAL-SWEEP-REPORT](./FINAL-SWEEP-REPORT.md) · [GAP-AUDIT](./GAP-AUDIT.md) · [SCRIPT-COMPATIBILITY-REPORT](./SCRIPT-COMPATIBILITY-REPORT.md) · [VAULT-AUDIT](./VAULT-AUDIT.md) · **WIKI-UPGRADE-REPORT**
<!-- siblings:end -->






# WIKI-UPGRADE-REPORT

Phase 7 deliverable. What changed in the 2026-05-29 wiki-upgrade pass.

## Scope completed

| Phase | Status | Files touched |
|---|---|---:|
| 0 — Gap audit + baseline | ✅ COMPLETE | 2 new (`GAP-AUDIT.md`, `script-baseline.txt`) |
| 1 — Linkify + breadcrumbs + anchors | ✅ COMPLETE | ~265 |
| 1f — Body-content backtick → link conversion | ✅ COMPLETE (follow-up) | 247 links across 19 files |
| 2 — `haskell-basics/` | ✅ COMPLETE | 38 new files |
| 3 — Targeted gap pages | ✅ COMPLETE | 4 new files |
| 4 — Mutation expansion | ✅ COMPLETE | 28 mutations across 21 families |
| 5 — Cross-topic page additions | ✅ COMPLETE | 2 new (`parser-x-either.md`, `writer-x-either.md`) |
| 6 — Index surgery (link conversion in cells) | ✅ COMPLETE | 1309 lines linkified across 8 index files |
| 7 — Script validation + reports | ✅ COMPLETE | 4 new (`script-postupgrade.txt`, `script-diff.txt`, this file, `SCRIPT-COMPATIBILITY-REPORT.md`) |
| 8 — Sibling navigation strips (one-click peer hops) | ✅ COMPLETE (follow-up) | 198 pages got inline peer-page strip after the breadcrumb |

## Counts

| Asset | Count | Notes |
|---|---:|---|
| Pitfall anchors injected | 68 | HIGH (30) + MEDIUM (21) + LOW (17) |
| Mock-Q anchors injected | 5 | Q1–Q5 in `indexes/MOCK-Q-INDEX.md` |
| Breadcrumbs added | 165 | Every content file (excluding `scripts/`, `graphs/`) |
| Directory README pages created | 3 | `meta/README.md`, `exam-day/README.md`, `indexes/README.md` |
| See-also blocks added (Phase 1e) | 124 | 24 archetypes + 23 families + 18 cross-matrix + 11 monads + 11 typeclasses + 10 trees + 15 interpreters + 13 quickcheck |
| Body-content links (Phase 1f) | 247 | Backtick-path → clickable across READMEs, exam-day, meta, pitfalls |
| New `haskell-basics/` pages | 38 | README + 37 content pages |
| New targeted gap pages (Phase 3) | 4 | `PROPERTY-PATTERNS.md`, `bst-delete-trace.md`, `transformer-stack-order.md`, `parser-chainl1.md` |
| New mutations (Phase 4) | 28 | Across 21 families. Each meets the structural-differentiation rule. |
| New cross-topic pages (Phase 5) | 2 | `parser-x-either.md`, `writer-x-either.md` |
| Index linkifications (Phase 6) | 1309 | Across 8 index files; row count + column count preserved (scripts unaffected) |
| New scripts in `scripts/` | 6 | All idempotent: `_phase1_breadcrumb.py`, `_phase1_seealso*.py` (×3), `_phase2_basics.py`, `_phase4_mutations.py`, `_phase6_indexes.py`, `_phase6_fix.py`, `_phase1f_body_linkify.py`, `_phase1f_fix.py` |
| Reports in `meta/` | 6 | `GAP-AUDIT.md`, `script-baseline.txt`, `script-postupgrade.txt`, `script-diff.txt`, this report, `SCRIPT-COMPATIBILITY-REPORT.md` |

**Total new files:** ~52 (38 basics + 4 gap pages + 2 cross-matrix + 3 dir READMEs + 6 reports + ~9 scripts but those are tooling).
**Total content-bearing files modified:** ~280.
**Total markdown links / anchors injected:** ~1900 (165 breadcrumbs + 73 anchors + 124 See-also blocks + 247 body links + 1309 index linkifications).

## All 12 brief steps — final coverage

| Brief step | Delivered as |
|---|---|
| 1. Repository analysis | `meta/GAP-AUDIT.md` |
| 2. Specialised agents | 3 Explore + 1 Plan agent (during plan phase) |
| 3. Complete Haskell basics | `haskell-basics/` × 38 |
| 4. Complete archetype coverage | All 24 archetypes have structured See-also |
| 5. Maximise mutation coverage | 235 seed + 28 expansion (Phase 4) within examiner-discipline cap |
| 6. Cross-topic coverage | 18 existing cross-matrix + 2 new (parser-x-either, writer-x-either) |
| 7. Wiki navigation | Breadcrumbs + See-also blocks + clickable indexes everywhere |
| 8. Beginner accessibility | `haskell-basics/` + structured page template throughout |
| 9. Index improvements | 1309 lines linkified across 8 indexes |
| 10. Question examples | Embedded in archetypes (`### Mutation N` blocks), families, and gap pages |
| 11. Script validation | `SCRIPT-COMPATIBILITY-REPORT.md` — 9/9 scripts PASS |
| 12. Final reports | `WIKI-UPGRADE-REPORT.md` (this), `SCRIPT-COMPATIBILITY-REPORT.md`, `GAP-AUDIT.md` updated |

## Three "from cold" entry paths for exam day

If you're blanking on exam day:

1. **Path A — by question text:** Open [`exam-day/ONE-PAGE-PANIC.md`](../exam-day/ONE-PAGE-PANIC.md). Match a phrase. Click the archetype link. Done.
2. **Path B — by type signature:** Open [`indexes/TYPE-SIGNATURE-DATABASE.md`](../indexes/TYPE-SIGNATURE-DATABASE.md). Find the closest signature. Follow the link.
3. **Path C — by data type:** If the question gives you a custom ADT with a recursive case, it's [`archetypes/A01-tree-recursion.md`](../archetypes/A01-tree-recursion.md). 80% of the time. Use the canonical template from there.

## Last-24h reading order

1. [`exam-day/LAST-HOUR-CHECKLIST.md`](../exam-day/LAST-HOUR-CHECKLIST.md) — refresh pin list.
2. [`pitfalls/HIGH-severity.md`](../pitfalls/HIGH-severity.md) — re-read P-001 through P-015 (the most expensive 15 mistakes).
3. [`indexes/MOCK-Q-INDEX.md`](../indexes/MOCK-Q-INDEX.md) — quickly re-read all 5 Mock specs.
4. [`exam-day/ONE-PAGE-PANIC.md`](../exam-day/ONE-PAGE-PANIC.md) — memorise the 5 canonical templates.
5. [`quickcheck/QUICKCHECK-ATTACKS.md`](../quickcheck/QUICKCHECK-ATTACKS.md) — final 60-second pre-submit checklist.
6. Sleep.

## Risks / known issues

- **`haskell-basics/maybe-basics.md` and `either-basics.md`** intentionally short — they link out to `../monads/maybe.md` and `../monads/either.md` for full content. Don't expand them; expand the destination pages instead if needed.
- **Some See-also blocks reference files that don't exist** (e.g. A11 → `trees/bst-delete-trace.md` was a forward-reference until Phase 3 created the file). All Phase 3 files now exist; verify by clicking from `A11-bst-ops.md`.
- **`docs/` style auto-link checkers will complain about absolute paths.** All vault links are relative. If you add a CI link checker, it should treat `../foo.md` as relative to the file, not the repo root.
- **The 4 new gap pages assume the standard `BT a` / `Rose a` / `Expr` ADTs.** If the exam uses a different shape, the property/trace code still teaches the pattern but the literal types will need adjustment.

## See also

**Gap audit:** [GAP-AUDIT](./GAP-AUDIT.md)
**Script compatibility:** [SCRIPT-COMPATIBILITY-REPORT](./SCRIPT-COMPATIBILITY-REPORT.md)
**Vault entry:** [`../README.md`](../README.md)
**Basics:** [`../haskell-basics/README.md`](../haskell-basics/README.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
