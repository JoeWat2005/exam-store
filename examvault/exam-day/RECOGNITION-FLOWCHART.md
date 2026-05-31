<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [exam-day](./README.md) · **RECOGNITION FLOWCHART — read question → archetype**

<!-- siblings:start -->
> **Peers:** [EXAM-DAY-ROUTE](./EXAM-DAY-ROUTE.md) · [IN-EXAM-WORKFLOW](./IN-EXAM-WORKFLOW.md) · [LAST-HOUR-CHECKLIST](./LAST-HOUR-CHECKLIST.md) · [ONE-PAGE-PANIC](./ONE-PAGE-PANIC.md) · **RECOGNITION-FLOWCHART** · [TIME-BUDGET](./TIME-BUDGET.md) · [WHAT-TO-PIN](./WHAT-TO-PIN.md)
<!-- siblings:end -->






# RECOGNITION FLOWCHART — read question → archetype

> ASCII decision tree. Walk top-to-bottom. Each "yes" branch ends at an `A##` archetype number. Max 6 questions deep.

Read the question stem and the type signature. Then walk this tree.

---

```
START
│  (you've just read the question stem + type signature)
│
├── Q1: Does the question give a custom ADT with recursive constructors?
│   ├── YES ↓
│   │   ├── Q1a: Does ANOTHER ADT (different name) appear in the answer signature?
│   │   │   ├── YES → A05 (ADT-to-ADT translation; Mock Q5 family)
│   │   │   └── NO ↓
│   │   │       ├── Q1b: Does the answer signature say `instance T MyADT where`?
│   │   │       │   ├── YES → A06 (Functor / Monad / Applicative instance)
│   │   │       │   │       └─ subtype: A24 if it's specifically Applicative
│   │   │       │   │       └─ subtype: A22 if it's Eq/Ord/Show
│   │   │       │   └── NO ↓
│   │   │       │       ├── Q1c: Is the answer the SAME ADT (transform / predicate)?
│   │   │       │       │   ├── YES → A01 (tree recursion — the ADT is both input and shape of recursion)
│   │   │       │       │   │       └─ if Rose tree: A01 Rose variant
│   │   │       │       │   │       └─ if Binary tree: A01 BT variant
│   │   │       │       │   │       └─ if it mentions Ord and "insert/delete/member": A11 (BST)
│   │   │       │       │   └── NO → could be A12 (representation conversion)
│   │   │       │       │
│   │   └── (end of YES branch)
│   └── NO ↓
│
├── Q2: Does the type signature contain `Monad m =>`?
│   ├── YES → A03 (generic monad combinator; Mock Q2 family)
│   │       └─ if it ALSO has a fixed monad alongside (`State s`, etc.): combo A03 × A02
│   └── NO ↓
│
├── Q3: Does the answer use `State`, `get`/`put`, or a NimGame-like type alias?
│   ├── YES ↓
│   │   ├── Q3a: Is there a game / score / turn-taking context?
│   │   │   ├── YES → A02 (state-monad game; Mock Q3 family)
│   │   │   └── NO → A23 (mini-game / general state simulation)
│   │   └── (end)
│   └── NO ↓
│
├── Q4: Does the input type look like `[[Int]]`, `[[Bool]]`, or a grid?
│   ├── YES ↓
│   │   ├── Q4a: Is the answer a single Bool (predicate)?
│   │   │   ├── YES → A04 (matrix predicate; Mock Q4 family)
│   │   │   │       └─ "magic square", "rows + cols + diagonals"
│   │   │   └── NO ↓
│   │   │       ├── Q4b: Is the answer a Maybe/finding result?
│   │   │       │   ├── YES → A04 × A23 (TTT-winner-style)
│   │   │       │   └── NO → A21 (list-comprehension over grid)
│   │   └── (end)
│   └── NO ↓
│
├── Q5: Does the question say "evaluate", "eval", or pass an environment?
│   ├── YES ↓
│   │   ├── Q5a: Does it use `Maybe` / `Either` for failures?
│   │   │   ├── YES ↓
│   │   │   │   ├── Q5b: Does it use BOTH `State` AND `Either`?
│   │   │   │   │   ├── YES → A14 (multi-effect interpreter)
│   │   │   │   │   └── NO → A08 (env evaluator)
│   │   │   │   └── (end)
│   │   │   └── NO → A08 (pure env eval)
│   │   ├── Q5c: Does it say "extend the interpreter" / "add a new construct"?
│   │   │   └── YES → A19 (extend an interpreter)
│   │   └── (end)
│   └── NO ↓
│
├── Q6: Does the question involve parsing strings into ADTs?
│   ├── YES → A16 (parser combinators)
│   └── NO ↓
│
├── Q7: Does the answer use Writer / `tell` / logging?
│   ├── YES → A15 (writer trace)
│   └── NO ↓
│
├── Q8: Is the question about encode AND decode of the same type?
│   ├── YES → A07 (codec pair)
│   └── NO ↓
│
├── Q9: Does it say "reimplement", "without using", or "from scratch"?
│   ├── YES → A09 (Prelude reimplementation)
│   └── NO ↓
│
├── Q10: Does the type signature suggest a fold reformulation (`foldr`, `foldl`)?
│   ├── YES → A10 (fold reformulation)
│   └── NO ↓
│
├── Q11: Does it mention "show", "pretty print", "display"?
│   ├── YES → A13 (pretty printer)
│   └── NO ↓
│
├── Q12: Does it use `fix`, infinite trees, memoisation?
│   ├── YES → A18 (lazy memoisation)
│   └── NO ↓
│
├── Q13: Does it use "zipper", "focus", "navigation"?
│   ├── YES → A17 (zipper navigation)
│   └── NO ↓
│
├── Q14: Does it mention "isomorphism", "retract", "laws"?
│   ├── YES → A20 (laws / iso)
│   └── NO ↓
│
└── DEFAULT: Re-read the question. Open `indexes/IF-YOU-SEE-X.md` and Ctrl-F a keyword.
            If still stuck after 90 seconds, SKIP this question.
```

---

## Fast 4-step protocol (use this 80% of the time)

Skip the full flowchart on familiar shapes. Use this:

1. **Tree ADT defined in `Types.hs` or question?** → **A01** (usually with A05 or A06 partner).
2. **`State` / `get`/`put` / `NimGame` in signature?** → **A02** or **A23**.
3. **`Monad m =>` constraint?** → **A03** (Mock Q2 family).
4. **`[[Int]]` or grid input?** → **A04** (Mock Q4 family).

If none match in 60 seconds, walk the full flowchart above.

---

## Archetype legend

All 24 archetypes covered. Click through to `archetypes/A##.md` for canonical templates.

| # | Name                            | Tier |
|---|---------------------------------|------|
| **A01** | Tree-ADT structural recursion   | 1    |
| **A02** | State monad game / sim          | 1    |
| **A03** | Generic `Monad m =>`            | 1    |
| **A04** | Matrix predicate via transpose  | 1    |
| **A05** | ADT-to-ADT translation          | 1    |
| **A06** | Functor / Applicative / Monad instance | 1 |
| **A07** | Codec pair encode/decode        | 2    |
| **A08** | Environment evaluator           | 1    |
| **A09** | Reimplement Prelude             | 3    |
| **A10** | Fold reformulation              | 3    |
| **A11** | BST operations                  | 2    |
| **A12** | Representation conversion       | 2    |
| **A13** | Custom Show pretty-printer      | 3    |
| **A14** | State + Error interpreter       | 2    |
| **A15** | Writer trace                    | 3    |
| **A16** | Parser combinators              | 3    |
| **A17** | Zipper navigation               | 4    |
| **A18** | Lazy memoisation                | 4    |
| **A19** | Extend an interpreter           | 2    |
| **A20** | Iso / retract / laws            | 4    |
| **A21** | List-comp enumeration           | 2    |
| **A22** | Eq/Ord/Show typeclass instance  | 2    |
| **A23** | Generalised mini-game           | 2    |
| **A24** | Applicative instance            | 3    |

---

## When you can't decide between two archetypes

Most overlaps are documented in [README](../archetypes/README.md)'s heat map. Quick rules:

- **A01 vs A05**: same input type as output → A01. Different output ADT → A05.
- **A02 vs A23**: turn-taking with score → A02. General state with no game → A23.
- **A03 vs A24**: `Monad m =>` → A03. `Applicative f =>` → A24.
- **A04 vs A23**: numeric grid predicate → A04. Grid with game state → A04 × A23 combo.
- **A08 vs A14**: just `Maybe` failure → A08. Both `State` and `Either` → A14.

---

## See also

- [README](../archetypes/README.md) — priority ranking + heat map
- [IF-YOU-SEE-X](../indexes/IF-YOU-SEE-X.md) — phrase → archetype lookup
- [TYPE-SIGNATURE-DATABASE](../indexes/TYPE-SIGNATURE-DATABASE.md) — signature shape → archetype
- `IN-EXAM-WORKFLOW.md` — what to do after you've recognised
- `ONE-PAGE-PANIC.md` — when this fails you

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
