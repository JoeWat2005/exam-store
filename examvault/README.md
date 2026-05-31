<!-- topnav:start -->
> **Quick nav:** [HOME](HOME.md) · [NAVIGATION](NAVIGATION.md) · [MASTER-INDEX](indexes/MASTER-INDEX.md)
<!-- topnav:end -->

# examvault

**Birmingham FP 2025/26 · exam ~2026-06-01 · 2h · 5 × 10 marks · vLab QuickCheck-marked · open book**

A *generator-aware* exam lookup system. The exam composes 5 questions from a small set of **archetypes** and a small set of **mutations** on those archetypes. Under exam pressure, your job is:

`recognise the archetype → find the template → apply the mutation → dodge the QuickCheck traps`.

This vault is built to make every step take under 60 seconds.

---

## ⚙️ First time on vLab? Run this in the JupyterLab terminal

```bash
cd ~/examvault            # or wherever you put the vault
bash scripts/vlab-setup.sh
# Then refresh the JupyterLab browser tab (Ctrl+R)
```

After the refresh, every `.md` file opens in **Preview mode** automatically (formatted, with clickable links) instead of as raw markdown source. **Do this once per fresh vLab environment** — the setting persists in `~/.jupyter/` across sessions, but a *brand-new* vLab spin-up needs it again.

Verify the scripts work:
```bash
python3 scripts/search_by_archetype.py A01     # should print A01 tier, files, neighbours
python3 scripts/mock_q_lookup.py Q3            # should print Q3 spec + marker quirk
```

If those print results, you're good. Full smoke test: see [`scripts/SCRIPTS-GUIDE.md`](scripts/SCRIPTS-GUIDE.md).

---

## Start here

| If you are… | Read first |
|-------------|-----------|
| First-time visitor | **[HOME](HOME.md)** — friendly tour |
| Looking for any directory's README | **[NAVIGATION](NAVIGATION.md)** — every README, one click |
| Reading the long-form workflow | [HOW-TO-USE](HOW-TO-USE.md) |
| Practising the day before | [LAST-HOUR-CHECKLIST](exam-day/LAST-HOUR-CHECKLIST.md) |
| In the exam right now | [ONE-PAGE-PANIC](exam-day/ONE-PAGE-PANIC.md) |
| Stuck on a single question | [IF-YOU-SEE-X](indexes/IF-YOU-SEE-X.md) → [`archetypes/`](archetypes/) |
| Cold on a Haskell primitive | [`haskell-basics/`](haskell-basics/README.md) — 48 quick-refresher pages |
| Hit by red GHC text | [ghc-error-decoder](haskell-basics/ghc-error-decoder.md) — translation + fix |
| Want a single-page mental model | [KNOWLEDGE-MAP](KNOWLEDGE-MAP.md) — the four axes |
| Setting up vLab | [imports-pitfalls](pitfalls/imports-pitfalls.md) + [`scripts/vlab-setup.sh`](scripts/vlab-setup.sh) |
| Planning revision time | `py -3 scripts/study_planner.py <days>` |
| Want scripts examples | [scripts/SCRIPTS-GUIDE](scripts/SCRIPTS-GUIDE.md) — full worked output |

---

## Directory map (238 .md files · 293 mutations · ~11,960 internal links)

| Dir | Files | Purpose |
|-----|------:|---------|
| `meta/` | 8 | COURSE-MAP, COURSE-COVERAGE, VAULT-AUDIT, GAP-AUDIT, WIKI-UPGRADE-REPORT, SCRIPT-COMPATIBILITY-REPORT, FINAL-SWEEP-REPORT |
| `archetypes/` | 25 | The 24 exam-question shapes (A01–A24) + priority ranking + recognition flowchart |
| `question-families/` | 25 | 24 families · **293 mutations** (cap raised to 25/family in Phase 12) · includes new **string-ops-family** |
| `trees/` | 12 | BinTree / BST / Rose / Expr — full operation catalogues + bst-delete worked trace |
| `monads/` | 14 | Maybe / Either / State / Writer / Reader / IO / List / MonadError / transformers / multi-effect / laws / 25-combinator reference / transformer-stack-order |
| `interpreters/` | 17 | Simple → +Maybe → +Either → +Reader → +State → +Writer → multi-effect → imperative-storage → extend/desugar/parse + parser-chainl1 |
| `cross-matrix/` | 21 | Tree×Monad, BST×State, Expr×everything, List×everything, game-state, parser×Either, writer×Either |
| `typeclasses/` | 11 | Functor / Applicative / Monad / Alternative / Foldable / Traversable / Eq-Ord / Show / Num / Monoid |
| `quickcheck/` | 17 | Per-topic edge-case attack DB + PROPERTY-PATTERNS (Arbitrary instances + prop_ patterns) |
| `pitfalls/` | 7 | HIGH / MEDIUM / LOW severity marks-killers (anchor-indexed P-001…P-068) + signature + imports pitfalls |
| `indexes/` | 15 | MASTER · IF-YOU-SEE-X · TYPE-SIGNATURE-DATABASE · KEYWORD · PROBLEM-NUMBER · LECTURE · PRELUDE · MOCK-Q · ASSIGNMENT · TYPES-REFERENCE · BEGINNER · ARCHETYPE · CROSS-TOPIC · MUTATION + README |
| `graphs/` | 6 | Machine-readable JSON: TOPIC · ARCHETYPE · MONAD · TREE · QUESTION · DEPENDENCY |
| `scripts/` | 18 | 9 user-facing Python helpers · vlab-setup.sh · SCRIPTS-GUIDE.md · phase scripts (idempotent) |
| `exam-day/` | 8 | EXAM-DAY-ROUTE · ONE-PAGE-PANIC · TIME-BUDGET · RECOGNITION-FLOWCHART · LAST-HOUR-CHECKLIST · IN-EXAM-WORKFLOW · WHAT-TO-PIN + README |
| `haskell-basics/` | 48 | Cold-start refresher pages (pattern-matching, guards, recursion, HOFs, ADTs, monad basics, testing-* × 4, ghci-commands, allowed-builtins, **ghc-error-decoder**) |
| **Root** | **7** | README, HOME, NAVIGATION, HOW-TO-USE, ARCHITECTURE, STATS, KNOWLEDGE-MAP |

---

## The 7 files to memorise paths for

| Path | When |
|------|------|
| [ONE-PAGE-PANIC](exam-day/ONE-PAGE-PANIC.md) | Pure panic mode |
| [IF-YOU-SEE-X](indexes/IF-YOU-SEE-X.md) | "I read the question, what archetype is it?" |
| [TYPE-SIGNATURE-DATABASE](indexes/TYPE-SIGNATURE-DATABASE.md) | "Only the type sig is given" |
| [README](archetypes/README.md) | Tier ranking + 5-question likely composition |
| [QUICKCHECK-ATTACKS](quickcheck/QUICKCHECK-ATTACKS.md) | Final pass before pressing submit |
| [HIGH-severity](pitfalls/HIGH-severity.md) | The marks-killers you must never make |
| [signature-pitfalls](pitfalls/signature-pitfalls.md) | The 5 Mock signatures verbatim |

---

## The exam's actual shape

Inferred from `fp-learning-2025/files/Assignments/MockTest/`:

| # | Marks | Mock archetype | Most likely exam variant |
|---|-------|----------------|---------------------------|
| Q1 | 10 | Rose tree, two sub-parts (predicate + transform) | **A01** Tree Recursion — `BT/BST/Rose` |
| Q2 | 10 | `Monad m =>` combinator returning `m [a]` | **A03** Generic Monad |
| Q3 | 10 | State-monad mini-game (Nim) | **A02** State Game — predicate + mutator |
| Q4 | 10 | `[[Int]] -> Bool` matrix predicate (magic square) | **A04** Matrix OR **A08** Env-Eval |
| Q5 | 10 | ADT-to-ADT recursive translation (Expr → Circuit) | **A05** ADT Translation OR **A06** Functor Instance |

Allowed imports — **memorise this list, anything else means zero marks**:
`Prelude` (implicit), `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`. Plus the question's own `Types` module.

Marker behaviours you wouldn't guess from reading the spec — see [MOCK-Q-INDEX](indexes/MOCK-Q-INDEX.md):
- Mock Q2's generator starts at n=2 — off-by-one is silently lenient
- Mock Q3 `gameOver` has a hardcoded `(0,0)` test worth 4 free marks
- Mock Q5 `circuit` is checked **semantically** (boolean equivalence over all assignments), NOT structurally

---

## Helper scripts

Run from `examvault/scripts/`:

```powershell
py -3 search_by_type.py "Monad m => m a -> ... -> m [a]"
py -3 search_by_keyword.py "applyNTimes"
py -3 search_by_combo.py "Tree + State"
py -3 mock_q_lookup.py Q3
py -3 study_planner.py 7
py -3 prelude_lookup.py transpose
py -3 topic_dependencies.py Functor
```

All scripts use only the Python standard library — no `pip install` needed.

---

## Knowledge graphs

`graphs/*.json` — machine-readable for future tooling (jq / embeddings / vector search):
- 52-node topic graph
- 24-node archetype graph (282 edges — complete combines-with adjacency)
- 30-node monad + transformer graph
- 30-node tree-types graph
- 28-node question-family graph
- 54-node dependency (prerequisite) graph

---

## Search keywords (for vault grep)

archetype · mutation · question-family · type-signature · QuickCheck · pitfall · cross-matrix · interpreter · monad · monad-transformer · multi-effect · State · Writer · Reader · Maybe · Either · MonadError · IO · List-monad · tree · BST · Rose · Expr · Functor · Applicative · Monad · Foldable · Traversable · Alternative · Monoid · Eq · Ord · Show · matrix · transpose · ADT-translation · circuit · codec · Caesar · Morse · RLE · parser · BNF · fold · foldr · foldl · list-comprehension · higher-order · lazy · infinite · memo · zipper · presubmit · Safe · vLab

<!-- footernav:start -->

---
> **Back to:** [HOME](HOME.md) · [NAVIGATION](NAVIGATION.md) · [MASTER-INDEX](indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
