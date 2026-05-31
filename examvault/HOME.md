> [examvault](./README.md) · **HOME**

# HOME — start here

Welcome. This is your **exam lookup vault**. Built for the Birmingham FP 2025/26 exam (2026-06-01, 2 hours, 5 × 10 marks, open book, vLab QuickCheck-marked).

If you opened this in the exam right now, jump to **[ONE-PAGE-PANIC](exam-day/ONE-PAGE-PANIC.md)**.
If you're cold and not sure where to start, read this page.

---

## How the vault works (the 60-second tour)

Every question on the exam can be located on **four axes**:

1. **Archetype** — the *shape* of the question (24 distinct shapes, A01–A24).
2. **Mutation** — the *dial* the examiner turns inside the archetype (hundreds of variants).
3. **Topic** — the *domain*: lists, trees, monads, interpreters, typeclasses.
4. **Type signature** — the *syntactic fingerprint* you see on the page.

Every leaf file in the vault is reachable from **at least three of the four axes**. That redundancy is the point: any phrase, sig, or topic the examiner uses will route you somewhere.

### The lookup loop (10-second drill)

```
Read the question → pick an axis → click the entry index → pick a file → copy template → adapt
```

The whole loop should take under 60 seconds. If it takes longer, you've gone too deep — back out to the index.

---

## Three entry doors (pick the one that fits)

| If you have... | Open |
|---|---|
| A phrase from the question stem (`"tree"`, `"label every node"`, `"applyN"`) | **[IF-YOU-SEE-X](indexes/IF-YOU-SEE-X.md)** — 344 trigger rows |
| Only the type signature (`Monad m => ... -> m a`) | **[TYPE-SIGNATURE-DATABASE](indexes/TYPE-SIGNATURE-DATABASE.md)** — 272 sig rows |
| A specific archetype number from memory | **[ARCHETYPE-INDEX](indexes/ARCHETYPE-INDEX.md)** — A01–A24 |
| Nothing — you've just sat down cold | **[BEGINNER-INDEX](indexes/BEGINNER-INDEX.md)** — linear reading path |
| The exam is starting RIGHT NOW | **[ONE-PAGE-PANIC](exam-day/ONE-PAGE-PANIC.md)** |

---

## The vault, in one paragraph

**238 markdown files. 24 archetypes (A01–A24). 293 mutations across 24 families. 21 cross-matrix files (Tree × Monad, Expr × Effect). 17 QuickCheck attack files. 68 anchored pitfalls (P-001 … P-068). 48 `haskell-basics/` cold-start pages. 15 entry indexes. 9 Python helper scripts. 6 knowledge graphs (JSON). One root `KNOWLEDGE-MAP.md` showing how all of this connects.**

Every file is breadcrumbed, sibling-strip-linked, and ends with a `See also` block. There are **~11,959 internal markdown links** (markdown links; the checker skips `scripts/` and `graphs/` and excludes `#`-anchors) and **3 known intentional template placeholders** (the only "broken" links the link-checker reports).

---

## A worked example — from question to answer in 4 hops

The exam paper says:

> Write `labelTree :: BT a -> State Int (BT (a, Int))` that assigns every node a fresh integer in in-order.

**Hop 1** (sig fingerprint) → [TYPE-SIGNATURE-DATABASE](indexes/TYPE-SIGNATURE-DATABASE.md) — `BT a -> State Int (...)` matches archetypes **A01 × A02**.

**Hop 2** (cross-domain) → [tree-x-state](cross-matrix/tree-x-state.md) — canonical `labelTree` template lives here.

**Hop 3** (mutation) → [state-counter-family](question-families/state-counter-family.md) — confirm whether it's in-order (M4) or pre-order (M5).

**Hop 4** (defensive) → [trees-attacks](quickcheck/trees-attacks.md) + [state-attacks](quickcheck/state-attacks.md) — edge cases to verify before submit.

Four clicks. Under 60 seconds.

---

## The 7 files to memorise paths for

If you only memorise seven paths, memorise these. They are pinned in [WHAT-TO-PIN](exam-day/WHAT-TO-PIN.md) and load the rest of the vault on demand:

| Path | When |
|------|------|
| [ONE-PAGE-PANIC](exam-day/ONE-PAGE-PANIC.md) | Pure panic mode — single screen |
| [IF-YOU-SEE-X](indexes/IF-YOU-SEE-X.md) | "I read the question; what archetype is it?" |
| [TYPE-SIGNATURE-DATABASE](indexes/TYPE-SIGNATURE-DATABASE.md) | "Only the type sig is given" |
| [ARCHETYPE-INDEX](indexes/ARCHETYPE-INDEX.md) | Tier ranking + per-archetype hop list |
| [MUTATION-INDEX](indexes/MUTATION-INDEX.md) | Every mutation across every family |
| [QUICKCHECK-ATTACKS](quickcheck/QUICKCHECK-ATTACKS.md) | Final pass before pressing submit |
| [HIGH-severity](pitfalls/HIGH-severity.md) | The 30 most-expensive marks-killers (P-001 … P-030) |

---

## How to move around the vault

- **Breadcrumb** at the top of every file — click `examvault` to come home.
- **Sibling strip** below the breadcrumb — shows you neighbours (other files in the same directory).
- **See also** at the bottom — branching links to related topics.
- **Search** — on vLab, use `Ctrl+F` over the open file or the JupyterLab file panel. Don't try to grep the whole tree by hand.

Beyond those, the **two flat indexes** to keep open in second tabs:

- [MASTER-INDEX](indexes/MASTER-INDEX.md) — top files per directory (plus exam-day & pitfalls in full), one line each.
- [NAVIGATION](NAVIGATION.md) — every directory README in the project.

---

## Knowledge map (4-axis mental model)

For the conceptual model of how the four axes interact, open [KNOWLEDGE-MAP](KNOWLEDGE-MAP.md). It's the single page that explains *why* the directory split is the way it is.

---

## Helper scripts

Nine Python scripts in `scripts/` accelerate lookups when you remember an archetype number, monad name, or sig shape but can't recall the file path.

```powershell
py -3 scripts/search_by_archetype.py A03      # A03 + combines-with + canonical files
py -3 scripts/search_by_type.py "Monad m =>"   # sig fingerprint → archetype
py -3 scripts/mock_q_lookup.py Q3              # Mock Q3 spec + marker quirk
py -3 scripts/prelude_lookup.py transpose      # what does transpose do, where used
py -3 scripts/study_planner.py 3               # 3-day revision plan
```

Full examples + every script: **[scripts/SCRIPTS-GUIDE.md](scripts/SCRIPTS-GUIDE.md)**.

On vLab use `python3` instead of `py -3`.

---

## Pitfalls — the marks-killers

The marker is QuickCheck. The five most expensive mistakes in our records, ranked:

1. **Type signature edited.** 0 on the question. *Always* copy-paste from `Types.hs`. [P-007](pitfalls/HIGH-severity.md#p-007)
2. **`isBST Empty = False`.** Empty is vacuously sorted. Should be `True`. [P-006](pitfalls/HIGH-severity.md#p-006)
3. **`applyNTimes _ _ 0 = return []`.** Mock Q2's marker tests `n=0`; off-by-one is silently lenient at higher n but brutal at 0. Should be `do x <- mx; return [x]`. [P-004](pitfalls/HIGH-severity.md#p-004)
4. **`gameOver` returns `False` on `(0,0)`.** Mock Q3's marker hardcodes a `(0,0)` test worth 4 of 10 marks. [P-009](pitfalls/HIGH-severity.md#p-009)
5. **`{-# LANGUAGE Safe #-}` pragma removed.** Whole file scores 0. [P-011](pitfalls/HIGH-severity.md#p-011)

Full ranking: [pitfalls/HIGH-severity.md](pitfalls/HIGH-severity.md) (30 entries) + [MEDIUM-severity.md](pitfalls/MEDIUM-severity.md) (21) + [LOW-severity.md](pitfalls/LOW-severity.md) (17).

---

## Allowed imports

Memorise this list. Importing anything else means 0 on the question:

```
Prelude            (implicit)
Data.List          (transpose, sort, nub, group, intercalate)
Data.Char          (isDigit, isAlpha, toLower, toUpper, ord, chr)
Data.Maybe         (fromMaybe, isJust, isNothing, catMaybes, mapMaybe)
Control.Monad      (when, unless, mapM, sequence, foldM, replicateM, void)
Control.Monad.State    (State, get, put, modify, runState, evalState, execState)
Control.Monad.Writer   (Writer, tell, runWriter, execWriter)
```

Plus the question's own `Types` module.

Full reference: [haskell-basics/allowed-builtins](haskell-basics/allowed-builtins.md).

---

## What this vault is NOT

- Not lecture notes — those live in [`../fp-learning-2025/files/LectureNotes/`](../fp-learning-2025/files/LectureNotes/).
- Not a Haskell tutorial — assumes you've done the course.
- Not exhaustive — optimised for *exam-day lookup*, not full course coverage.
- Not infallible — flag any inconsistency you find.

---

## What this vault IS

A weaponised lookup system. Your second brain under time pressure. Use it like one.

---

## Pre-exam reading order

| Time available | Read |
|---|---|
| 7+ days | [BEGINNER-INDEX](indexes/BEGINNER-INDEX.md) stages 0–5 + every Tier-1 archetype |
| 3 days | `py -3 scripts/study_planner.py 3` + Mock Q drill |
| 1 day | [LAST-HOUR-CHECKLIST](exam-day/LAST-HOUR-CHECKLIST.md) + re-read HIGH pitfalls + sleep |
| 2 hours | [ONE-PAGE-PANIC](exam-day/ONE-PAGE-PANIC.md) + memorise the 5 templates + sleep |

---

## See also

**Architecture explanation:** [ARCHITECTURE](ARCHITECTURE.md)
**How-to-use long version:** [HOW-TO-USE](HOW-TO-USE.md)
**Knowledge map:** [KNOWLEDGE-MAP](KNOWLEDGE-MAP.md)
**Stats:** [STATS](STATS.md)
**Navigation hub:** [NAVIGATION](NAVIGATION.md)
**Scripts guide:** [scripts/SCRIPTS-GUIDE](scripts/SCRIPTS-GUIDE.md)
**Final report:** [meta/FINAL-SWEEP-REPORT](meta/FINAL-SWEEP-REPORT.md)
