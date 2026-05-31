<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

# SCRIPTS-GUIDE

> [examvault](../README.md) · [scripts](./README.md) · **SCRIPTS-GUIDE**

Examples-first guide to every script in `examvault/scripts/`. Each script gets: one-line purpose, full CLI signature, 2–3 worked examples with actual output, what data the script reads, and common gotchas.

For a tighter inventory, see [`scripts/README.md`](README.md).

---

## How to run the scripts

### Windows (the user's machine)

```powershell
cd "C:\Users\cwatm\Desktop\functional programming\examvault"
py -3 scripts\search_by_archetype.py A01
```

### vLab (the exam environment, JupyterLab terminal)

```bash
cd ~/examvault
python3 scripts/search_by_archetype.py A01
```

### All other Linux / macOS

```bash
python3 scripts/search_by_archetype.py A01
```

All scripts use only the **Python standard library** — no `pip install` required. They read JSON graphs from `graphs/`, vault markdown files for grep, and a few hardcoded dictionaries inside the scripts themselves.

> **Common mistake:** `python` on Windows often points at the Python 2 launcher or fails silently. Always use `py -3` on Windows.

---

## 1. `search_by_archetype.py` — archetype lookup

**Purpose:** Given an archetype number (A01–A24), shows its tier, stars, primary files, combinations, and how often it's mentioned across the vault.

**Usage:**
```text
py -3 scripts/search_by_archetype.py <A##>
```

**Example 1 — Tier-1 archetype A03 (Mock Q2):**

```text
> py -3 scripts/search_by_archetype.py A03

Query: 'A03'
======================================================================

  A03 - Generic Monad m => combinator
  Tier:     1   Stars: *****
  F/D/C/E:  M/H/H/H
  Primary files:
    - archetypes/A03-generic-monad.md
    - monads/generic-combinators.md
  Combines with (weight >= 3):
    - A01  (w=5)  mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)
    - A02  (w=4)  State combinators are Monad m =>
    - A06  (w=3)  Monad instances tested via generic combinators
    - A08  (w=3)  generic env eval Monad m =>
    - A14  (w=3)  generic multi-effect Monad m =>
    - A20  (w=3)  Monad laws verified via QuickCheck
    - A24  (w=3)  Applicative + Monad combinator family
  Mentioned in 68 vault files (top 10 by frequency):
    - indexes/IF-YOU-SEE-X.md  (36×)
    - indexes/TYPE-SIGNATURE-DATABASE.md  (31×)
    ...
```

**Example 2 — Tier-2 archetype A11 (BST):**

```text
> py -3 scripts/search_by_archetype.py A11

  A11 - BST operations
  Tier:     2   Stars: ***
  F/D/C/E:  M/M/M/M
  Primary files:
    - archetypes/A11-bst-ops.md
    - trees/bst.md
  Combines with (weight >= 3):
    - A01  (w=5)  BST is a BT
  ...
```

**What it reads:** `graphs/ARCHETYPE-GRAPH.json` (24 nodes, 282 edges) + recursive grep across `*.md`.

**Common gotchas:**
- Use uppercase A (e.g. `A01` not `a01`).
- Two digits required (`A02` not `A2`).

---

## 2. `search_by_type.py` — type-signature reverse lookup

**Purpose:** Given a Haskell type signature shape, returns the matching archetype + canonical files.

**Usage:**
```text
py -3 scripts/search_by_type.py "<sig>"
```

**Example 1 — generic monad combinator:**

```text
> py -3 scripts/search_by_type.py "Monad m => m a -> ... -> m [a]"

Matched: applyNTimes / mapM / sequence shape
Archetype: A03 - Generic Monad m =>
Primary files:
  - archetypes/A03-generic-monad.md
  - monads/generic-combinators.md
  - question-families/monad-combinator-family.md
```

**Example 2 — matrix predicate:**

```text
> py -3 scripts/search_by_type.py "[[Int]] -> Bool"

Matched: matrix predicate
Archetype: A04 - Matrix predicate via transpose
Primary files:
  - archetypes/A04-matrix-predicate.md
  - question-families/matrix-predicate-family.md
```

**Example 3 — no match:**

```text
> py -3 scripts/search_by_type.py "Tree a -> Int"

No rule matched signature: 'Tree a -> Int'

Try a more general shape, e.g.:
  python search_by_type.py "Tree a -> Int"
  python search_by_type.py "Monad m =>"
  python search_by_type.py "[[Int]] -> Bool"
```

**What it reads:** `SIG_RULES` — a hardcoded dictionary at the top of the script with ~30 patterns.

**Common gotchas:**
- Quote the signature — shell will eat the `->` and `=>` otherwise.
- Use the *shape* not the exact sig — `"Tree a -> Int"` works, but the database is patterns, not literals.

---

## 3. `search_by_monad.py` — monad relationship lookup

**Purpose:** For a given monad, shows what it implements, what stacks with it, transformers, and cross-matrix files.

**Usage:**
```text
py -3 scripts/search_by_monad.py <name>
```

**Example 1 — State monad:**

```text
> py -3 scripts/search_by_monad.py State

Monad: State (State s)
Description: newtype State s a = State { runState :: s -> (a, s) }; threaded mutable state.
Files: monads/state.md

Related monads / classes (edges):
  [implements] Functor, Applicative, Monad, MonadState
  [can-stack-with] Either (calculator with state + error)
  [can-stack-with] Writer (state + log)
  [can-stack-with] Maybe (state with possible failure)
  [can-stack-with] Reader (env + state)
  [transformer-of (incoming)] StateT
  ...

Cross-matrix files involving this monad:
  - cross-matrix/bst-x-state.md
  - cross-matrix/tree-x-state.md
  - cross-matrix/rose-x-state.md
  - cross-matrix/list-x-state.md
  - cross-matrix/expr-x-state.md
  - cross-matrix/game-state.md
```

**Example 2 — Writer monad:**

```text
> py -3 scripts/search_by_monad.py Writer

Monad: Writer (Writer w)
Description: newtype Writer w a = Writer { runWriter :: (a, w) }; logs to a Monoid.
Files: monads/writer.md
...
```

**What it reads:** `graphs/MONAD-GRAPH.json` (30 nodes, 79 edges).

**Common gotchas:**
- Use canonical name (`State`, `Maybe`, `Either`) — `monads/state.md` content uses that capitalisation.

---

## 4. `search_by_combo.py` — cross-axis combination

**Purpose:** Given two terms ("Tree + State"), finds the cross-matrix file and co-occurrence locations.

**Usage:**
```text
py -3 scripts/search_by_combo.py "<X> + <Y>"
```

**Example 1 — Tree × Writer (logging traversal):**

```text
> py -3 scripts/search_by_combo.py "Tree + Writer"

Combination: 'tree' + 'writer'
======================================================================

Cross-matrix files:
  - cross-matrix/tree-x-writer.md

Archetype mapping:
  'tree'               -> A01
  'writer'             -> A15

Archetype combines-with weight: 3
  Note: log-traversal
  -> This is a strong combination. Open both archetype files:
    - archetypes/A01-*.md
    - archetypes/A15-*.md

Files where both terms co-occur (within 500 chars; top 15 by proximity):
     7c  cross-matrix/tree-x-writer.md
    16c  pitfalls/README.md
    45c  archetypes/README.md
```

**Example 2 — Expr × Multi (full interpreter):**

```text
> py -3 scripts/search_by_combo.py "Expr + Multi"

Cross-matrix files:
  - cross-matrix/expr-x-multi.md
...
```

**What it reads:** `graphs/ARCHETYPE-GRAPH.json` combines-with edges + `cross-matrix/*.md` filename pattern.

**Common gotchas:**
- Quote the argument — the `+` needs to be a literal.
- Lowercase OK — the script normalises.

---

## 5. `search_by_keyword.py` — keyword grep ranked

**Purpose:** Ranks vault files by frequency of a keyword.

**Usage:**
```text
py -3 scripts/search_by_keyword.py <keyword>
```

**Example 1 — `applyNTimes`:**

```text
> py -3 scripts/search_by_keyword.py applyNTimes

Query: 'applyNTimes'
Total matches: 191 across 35 files
======================================================================

File-level summary (top 15 by hit count):
   48×  quickcheck/monad-attacks.md
   22×  pitfalls/HIGH-severity.md
   20×  question-families/monad-combinator-family.md
   15×  archetypes/A03-generic-monad.md
   11×  pitfalls/signature-pitfalls.md
    7×  indexes/MOCK-Q-INDEX.md
    7×  pitfalls/MEDIUM-severity.md
    7×  quickcheck/writer-attacks.md
   ...
```

**Example 2 — `isBST`:**

```text
> py -3 scripts/search_by_keyword.py isBST

Query: 'isBST'
Total matches: ...
   ×  trees/bst.md
   ×  question-families/bst-ops-family.md
   ...
```

**What it reads:** Recursive grep across vault.

**Common gotchas:**
- Case-sensitive on Linux/vLab. `isBST` and `isbst` are different.

---

## 6. `mock_q_lookup.py` — Mock-Q spec + marker quirk

**Purpose:** Returns the Mock Q's spec, marker behaviour, and canonical file list.

**Usage:**
```text
py -3 scripts/mock_q_lookup.py Q[1-5]
```

**Example 1 — Q3 (Nim):**

```text
> py -3 scripts/mock_q_lookup.py Q3

Query: 'Q3'
Matched 1 Mock Q entries.
======================================================================

  Q3 - Nim with State (gameOver + takeTokens)
  Archetype: A02
  Signature(s):
    gameOver :: NimGame Bool
    takeTokens :: Int -> Heap -> NimGame ()
  Marker quirk:
    `gameOver` has a hardcoded (0,0) test worth 4 free marks:
    literally `gameOver = pure True` gets 4/10. `takeTokens` MUST
    clamp at 0 (max 0 (a-n)) — marker tests overshooting.
  Files:
    - archetypes/A02-state-game.md
    - monads/state.md
    - cross-matrix/game-state.md
    - question-families/state-game-family.md
```

**Example 2 — Q5 (circuit):**

```text
> py -3 scripts/mock_q_lookup.py Q5

  Q5 - circuit (Expr -> Circuit, NAND-only)
  Archetype: A05
  Marker quirk:
    Mock Q5 `circuit` is checked **semantically** (boolean equivalence
    over all assignments), NOT structurally. Two different ASTs that
    produce the same boolean output both pass.
  ...
```

**What it reads:** `MOCK_QS` — hardcoded dictionary inside the script with the verbatim Mock paper specs.

**Common gotchas:**
- Use `Q3` not `q3`. The script accepts either, but be consistent.

---

## 7. `prelude_lookup.py` — Prelude function reference

**Purpose:** Returns the type, description, usage, and pitfall for any function in `PRELUDE-INDEX.md`.

**Usage:**
```text
py -3 scripts/prelude_lookup.py <function-name>
```

**Example 1 — `transpose`:**

```text
> py -3 scripts/prelude_lookup.py transpose

Query: 'transpose'
Matched 1 entries.
======================================================================

  transpose
    Section:  Data.List — extras
    Sig:      [[a]] -> [[a]]
    What:     rows ↔ cols
    Used in:  problem 141 magic square
    Pitfall:  preserves jaggedness
```

**Example 2 — `foldM`:**

```text
> py -3 scripts/prelude_lookup.py foldM

  foldM
    Section:  Control.Monad
    Sig:      Monad m => (b -> a -> m b) -> b -> [a] -> m b
    What:     monadic foldl
    Used in:  problems 109, 117 (state-fold), monad-combinator-family M6
    Pitfall:  base case is `return z`, not `[]`
```

**What it reads:** `indexes/PRELUDE-INDEX.md` parsed line-by-line.

**Common gotchas:**
- Exact match. `traverse` works; `traversal` does not.

---

## 8. `study_planner.py` — personalised revision plan

**Purpose:** Generates a day-by-day study plan based on tier ranking.

**Usage:**
```text
py -3 scripts/study_planner.py <days>
```

**Example 1 — 3-day plan:**

```text
> py -3 scripts/study_planner.py 3

Study plan for 3 days
======================================================================
Tiers (from archetypes/README.md):
  Tier 1 - almost certainly tested (A01, A02, A03, A04, A05, A06, A08)
  Tier 2 - very likely         (A07, A11, A12, A14, A19, A21, A22, A23)
  Tier 3 - possible            (A09, A10, A13, A15, A16, A24)
  Tier 4 - low probability     (A17, A18, A20)
======================================================================

Day 1:
    - A01 *****  Tree-ADT structural recursion
        Read: archetypes/A01-tree-recursion.md
        Plus: trees/binary-tree.md
    - A02 *****  State-monad mini-game
        Read: archetypes/A02-state-game.md
        Plus: monads/state.md
    - A03 *****  Generic Monad m => combinator
        Read: archetypes/A03-generic-monad.md
        Plus: monads/generic-combinators.md
    ...
```

**Example 2 — 1-day (emergency):**

```text
> py -3 scripts/study_planner.py 1

Day 1: PANIC MODE
    - read exam-day/ONE-PAGE-PANIC.md
    - re-read pitfalls/HIGH-severity.md (top 10)
    - re-drill Mock Q1 + Mock Q3 cold
    - sleep
```

**What it reads:** `archetypes/README.md` (tier table).

**Common gotchas:**
- Integer required.

---

## 9. `topic_dependencies.py` — prerequisite chain

**Purpose:** Given a topic, shows direct and transitive prerequisites.

**Usage:**
```text
py -3 scripts/topic_dependencies.py <topic>
```

**Example 1 — Functor:**

```text
> py -3 scripts/topic_dependencies.py Functor

Topic: Functor - Functor
Description: fmap class.
Introduced: Week 7
Tags: advanced
Files: typeclasses/functor.md
======================================================================

Direct prerequisites (you must know these first):
  [prerequisite-of] typeclasses-basic  (w=5)
  [prerequisite-of] higher-order-functions  (w=4)
  [prerequisite-of] custom-ADTs  (w=4)

Transitive prerequisites (full chain, unique):
  - typeclasses-basic
  - higher-order-functions
  - custom-ADTs
  - pattern-matching
  - types
```

**Example 2 — Monad:**

```text
> py -3 scripts/topic_dependencies.py Monad

Topic: Monad
Direct prerequisites:
  - Applicative
  - Functor

Transitive prerequisites:
  - Applicative, Functor, typeclasses-basic, higher-order-functions, ...
```

**What it reads:** `graphs/DEPENDENCY-GRAPH.json` (54 nodes, 98 edges).

**Common gotchas:**
- Capitalise the topic. `Functor`, `Monad`, `State`, `Writer`.

---

## 10. `vlab-setup.sh` — JupyterLab Markdown Preview config

**Purpose:** One-shot bash script that configures JupyterLab on vLab to open `.md` files in Preview mode by default. Persists across sessions.

**Usage:**
```bash
bash scripts/vlab-setup.sh
# then refresh the JupyterLab tab (Ctrl+R)
```

**What it does:**
- Writes `~/.jupyter/lab/user-settings/@jupyterlab/docmanager-extension/plugin.jupyterlab-settings`
- Sets `defaultViewers.markdown = "Markdown Preview"`

**To revert:**
```bash
rm ~/.jupyter/lab/user-settings/@jupyterlab/docmanager-extension/plugin.jupyterlab-settings
```

**Common gotchas:**
- Must refresh the browser tab after running for the change to take effect.

---

## Phase scripts (tooling, not in-exam workflow)

The `_phase*` scripts in `scripts/` (e.g. `_phase8_siblings.py`, `_phase9_link_check.py`) are **idempotent tooling** for bulk vault edits. Don't run them during the exam. They exist so the vault stays consistent when content is added.

| Phase script | What it does |
|---|---|
| `_phase1_breadcrumb.py` | Inject breadcrumb on every page |
| `_phase1_seealso.py` | Inject canonical See-also blocks |
| `_phase1f_body_linkify.py` | Convert backtick paths to clickable links |
| `_phase2_basics.py` | Bulk-create `haskell-basics/` pages |
| `_phase4_mutations.py` | Bulk-add new mutations from a manifest |
| `_phase6_indexes.py` | Linkify text in index tables |
| `_phase8_siblings.py` | Inject sibling navigation strip |
| `_phase9_link_check.py` | Find broken internal links |

For full provenance, see [meta/WIKI-UPGRADE-REPORT.md](../meta/WIKI-UPGRADE-REPORT.md).

---

## Quick reference

| If you want to... | Run |
|---|---|
| Find A##'s combinations | `search_by_archetype.py A##` |
| Map a sig to an archetype | `search_by_type.py "<sig>"` |
| See what a monad stacks with | `search_by_monad.py <Name>` |
| Find the Tree×State / Expr×Either / … file | `search_by_combo.py "<X> + <Y>"` |
| Find files mentioning a keyword | `search_by_keyword.py <kw>` |
| Get Mock Q spec + quirk | `mock_q_lookup.py Q[1-5]` |
| Look up a Prelude function | `prelude_lookup.py <fn>` |
| Get a revision plan | `study_planner.py <days>` |
| Know what to learn first | `topic_dependencies.py <topic>` |
| Configure vLab Markdown Preview | `bash vlab-setup.sh` |
| Verify links after editing | `py -3 _phase9_link_check.py` |

---

## Quick "everything green?" smoke tests

> **Note on `search_by_type.py` and `prelude_lookup.py`:** these scripts return exit code `1` when no match is found (the same convention `grep` uses). For the smoke test we pass inputs that we know match a rule, so a non-zero exit means a real failure rather than "no match".

### Bash / Git Bash / vLab Linux terminal

```bash
# Prints OK or FAIL for each of the 9 scripts.
for s in search_by_archetype:A01 \
         "search_by_type:[[Int]] -> Bool" \
         search_by_monad:State \
         "search_by_combo:Tree + State" \
         search_by_keyword:applyNTimes \
         mock_q_lookup:Q3 \
         prelude_lookup:transpose \
         study_planner:3 \
         topic_dependencies:Functor; do
  name=${s%%:*}; arg=${s#*:}
  python3 "scripts/$name.py" "$arg" > /dev/null 2>&1 \
    && echo "OK   $name" \
    || echo "FAIL $name"
done
```

### PowerShell (Windows)

```powershell
# Same idea, native PowerShell syntax.
$tests = @(
  @("search_by_archetype.py", "A01"),
  @("search_by_type.py",      "[[Int]] -> Bool"),
  @("search_by_monad.py",     "State"),
  @("search_by_combo.py",     "Tree + State"),
  @("search_by_keyword.py",   "applyNTimes"),
  @("mock_q_lookup.py",       "Q3"),
  @("prelude_lookup.py",      "transpose"),
  @("study_planner.py",       "3"),
  @("topic_dependencies.py",  "Functor")
)

foreach ($t in $tests) {
  $name = $t[0]; $arg = $t[1]
  py -3 "scripts\$name" "$arg" > $null 2>&1
  if ($LASTEXITCODE -eq 0) { Write-Host "OK   $name" }
  else                     { Write-Host "FAIL $name" }
}
```

Expected output (either shell): nine `OK   <name>` lines, no `FAIL`.

---

## See also

**Scripts directory:** [scripts/](.) · [README](README.md)
**Home:** [HOME](../HOME.md)
**Navigation hub:** [NAVIGATION](../NAVIGATION.md)
**Architecture:** [ARCHITECTURE](../ARCHITECTURE.md)
**Knowledge map:** [KNOWLEDGE-MAP](../KNOWLEDGE-MAP.md)
**Per-script verdicts:** [meta/SCRIPT-COMPATIBILITY-REPORT](../meta/SCRIPT-COMPATIBILITY-REPORT.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
