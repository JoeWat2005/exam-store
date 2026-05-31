<!-- topnav:start -->
> **Quick nav:** [HOME](HOME.md) · [NAVIGATION](NAVIGATION.md) · [MASTER-INDEX](indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](./README.md) · **How to use examvault**

# How to use examvault

If you read one document, read this one.

---

## The model

The Birmingham FP exam isn't tested by giving you random Haskell problems. It tests a small set of **archetypes** — recognisable question shapes — and the examiner picks ONE **mutation** of each.

```
Archetype A03 (Generic Monad combinator)
   ├── Mutation: applyNTimes (Mock Q2)
   ├── Mutation: mapM' / sequence'
   ├── Mutation: replicateM' / forM'
   ├── Mutation: iterateM
   └── Mutation: filterM with predicate effect
```

So your exam workflow is not *invent* but *recognise → retrieve → adapt*.

---

## The 5-step exam workflow

For every question (~20 minutes each, target):

### Step 1 — READ (1 minute)
Read the question once. Underline:
- Type signatures given
- Custom data types
- Phrases like "may fail", "track state", "preserve structure", "every node"

### Step 2 — RECOGNISE (1 minute)
Two paths:

| Got a phrase? | → [IF-YOU-SEE-X](indexes/IF-YOU-SEE-X.md) (220+ trigger rows) |
| Got just a sig? | → [TYPE-SIGNATURE-DATABASE](indexes/TYPE-SIGNATURE-DATABASE.md) |

Output: **A##** — an archetype number (A01–A24).

If unsure, walk [RECOGNITION-FLOWCHART](exam-day/RECOGNITION-FLOWCHART.md) from the top.

### Step 3 — PULL TEMPLATE (1 minute)
Open `archetypes/A##-*.md`. Every archetype file contains:
- Canonical template (copy-pasteable)
- 5–10 distinct mutations
- QuickCheck attack surface
- Pitfalls

### Step 4 — CHECK FOR CROSS-DOMAIN (30 seconds)
Is this archetype combined with another?
- "label every node" → tree × state → [tree-x-state](cross-matrix/tree-x-state.md)
- "validate with error message" → tree × either → [tree-x-either](cross-matrix/tree-x-either.md)
- "eval Expr with env" → see [expr-reader](interpreters/expr-reader.md) or [expr-reader-either](interpreters/expr-reader-either.md)

### Step 5 — ADAPT + VERIFY (15 minutes)
- Copy template → rename constructors → plug in the question's spec
- Compile-check often (`ghci` reload)
- Before moving on, scan `quickcheck/<topic>-attacks.md` for that archetype — touch every input class
- Run `./presubmit.sh` — never skip this

---

## What goes where (decision tree)

```
"I just read the question."
│
├── Step 1: archetype recognition
│   ├── Phrase trigger?     → indexes/IF-YOU-SEE-X.md
│   ├── Only the type sig?  → indexes/TYPE-SIGNATURE-DATABASE.md
│   └── Neither?            → exam-day/RECOGNITION-FLOWCHART.md
│
├── Step 2: pull the template
│   └── archetypes/A##-<name>.md
│
├── Step 3: pull the mutation library
│   └── question-families/<family>.md
│
├── Step 4: domain deep-dive (if needed)
│   ├── Trees:        trees/<binary-tree | bst | rose-tree | expression-tree | ...>.md
│   ├── Monads:       monads/<maybe | either | state | writer | ...>.md
│   ├── Interpreters: interpreters/<expr-X | extend-interpreter | desugar-pipeline>.md
│   ├── Typeclasses:  typeclasses/<functor | applicative | monad | ...>.md
│   └── Cross-domain: cross-matrix/<tree-x-Y | expr-x-Y | ...>.md
│
├── Step 5: defensive — before submit
│   ├── QuickCheck:        quickcheck/<topic>-attacks.md
│   ├── Pitfalls high:     pitfalls/HIGH-severity.md
│   ├── Pitfalls per topic: pitfalls/per-topic-pitfalls.md
│   ├── Signature check:   pitfalls/signature-pitfalls.md
│   └── Imports check:     pitfalls/imports-pitfalls.md
│
└── Step 6: ship it
    └── exam-day/EXAM-DAY-ROUTE.md (the 2-hour timeline)
```

---

## Common starting points by question type

**"Write a function on `BT a`"**
1. [A01-tree-recursion](archetypes/A01-tree-recursion.md) (template)
2. [binary-tree](trees/binary-tree.md) (full op catalogue)
3. [trees-attacks](quickcheck/trees-attacks.md) (edge cases)

**"Write `f :: Monad m => ...`"**
1. [A03-generic-monad](archetypes/A03-generic-monad.md) (template)
2. [generic-combinators](monads/generic-combinators.md) (mapM, sequence, replicateM, etc.)
3. [monad-attacks](quickcheck/monad-attacks.md)

**"Write `f :: ... -> State s ...`"**
1. [A02-state-game](archetypes/A02-state-game.md) OR `A23-mini-game.md`
2. [state](monads/state.md)
3. [state-attacks](quickcheck/state-attacks.md)

**"Convert Expr to Circuit / normalise / desugar"**
1. [A05-adt-translation](archetypes/A05-adt-translation.md)
2. [desugar-pipeline](interpreters/desugar-pipeline.md)
3. [expr-attacks](quickcheck/expr-attacks.md)

**"Implement `instance Functor T`"**
1. [A06-functor-instance](archetypes/A06-functor-instance.md)
2. [functor](typeclasses/functor.md)
3. [typeclass-instance-attacks](quickcheck/typeclass-instance-attacks.md)

**"Evaluate Expr with env / failures / both"**
1. [README](interpreters/README.md) (decision tree)
2. The specific interpreter file (`expr-maybe.md` / `expr-reader-either.md` / etc.)
3. [interp-attacks](quickcheck/interp-attacks.md)

**"Predicate over `[[Int]]`"**
1. [A04-matrix-predicate](archetypes/A04-matrix-predicate.md)
2. [matrix-predicate-family](question-families/matrix-predicate-family.md)
3. [matrix-attacks](quickcheck/matrix-attacks.md)

---

## Pre-exam revision plan

Use `py -3 scripts/study_planner.py <days>` for a personalised plan. Defaults:

| Days left | What |
|-----------|------|
| 14+ | Read every archetype + every monad file. Practise 5 problems from each tier 1 archetype. |
| 7   | Drill mock test cold. Read all HIGH pitfalls. One full pass on cross-matrix. |
| 3   | RE-do mock test. Skim ONE-PAGE-PANIC + RECOGNITION-FLOWCHART. Verify vLab works. |
| 1   | Last hour checklist. Sleep. |

---

## What this vault is NOT

- Not lecture notes — the textbook is `fp-learning-2025/files/LectureNotes/`
- Not a Haskell tutorial — assumes you've done the course
- Not exhaustive — it's optimised for exam-day lookup, not full course coverage
- Not auto-updated — if the lecturer changes the syllabus, the vault won't notice

---

## What this vault IS

A weaponised lookup system. Treat it as your second brain under time pressure.

<!-- footernav:start -->

---
> **Back to:** [HOME](HOME.md) · [NAVIGATION](NAVIGATION.md) · [MASTER-INDEX](indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
