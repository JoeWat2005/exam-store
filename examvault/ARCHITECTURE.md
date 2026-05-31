<!-- topnav:start -->
> **Quick nav:** [HOME](HOME.md) · [NAVIGATION](NAVIGATION.md) · [MASTER-INDEX](indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](./README.md) · **examvault architecture**

# examvault architecture

The vault is structured around four orthogonal axes:

1. **Archetype** — the question *shape* (A01..A24). What the examiner thinks of first.
2. **Mutation** — what they *change* in an archetype. Per-family records.
3. **Topic** — the *domain* (lists, trees, monads, interpreters). What the lecture taught.
4. **Type signature** — the syntactic *fingerprint*. What you see on the page.

Every leaf file is reachable from at least three axes (archetype, topic, type-signature). The `indexes/` directory is the cross-index.

## Reasoning behind directory split

| Concern | Where it lives | Why separated |
|---------|----------------|---------------|
| What does this archetype look like? | `archetypes/A**.md` | One canonical shape per archetype |
| What variants of this archetype get asked? | `question-families/*.md` | Mutations enumerated, not just one shape |
| How do I implement this on **trees**? | `trees/*.md` | Trees recur across many archetypes (counting, validation, transform, mapM) |
| How do I implement this with **State**? | [state](monads/state.md) | One spot for all State ops |
| What happens when **Tree meets State**? | [tree-x-monad](cross-matrix/tree-x-generic-monad.md) | Cross-product space; if separate, would explode in `trees/` or `monads/` |
| What does QuickCheck do to me? | `quickcheck/<topic>.md` | One attack surface per topic |
| What does the *type* alone tell me? | [TYPE-SIGNATURE-DATABASE](indexes/TYPE-SIGNATURE-DATABASE.md) | Reverse lookup from sig → families |
| Where is X in the *lecture* notes? | [COURSE-COVERAGE](meta/COURSE-COVERAGE.md) | Lecture → vault mapping |

## File anatomy

Every leaf file must contain:

```markdown
# Title — short label

**Archetype:** A##   |   **Type sig:** `...`   |   **Exam probability:** ⭐...⭐
**Family:** family-name.md   |   **Combines with:** other archetypes
**Search keywords:** keyword1 · keyword2 · ...

## Recognition triggers
- "phrase that means this archetype"
- type signature fingerprint
- known appearance (mock Q#, problem sheet ##, lecture ##)

## Canonical template
\`\`\`haskell
-- copy-pasteable skeleton
\`\`\`

## Mutations
1. Sub-variant 1 — sigs + code
2. Sub-variant 2 — sigs + code
...

## QuickCheck traps
- Edge case 1
- Edge case 2

## Pitfalls
- Common bug 1
- Common bug 2

## See also
- [related archetype](path)
- [related family](path)
```

## Knowledge graph

`graphs/*.json` contains the machine-readable graph. Nodes are archetypes/topics/templates; edges encode:
- `depends-on` — prerequisite knowledge
- `combines-with` — likely cross-topic pairings
- `mutates-into` — common examiner mutations
- `implemented-in` — file paths to canonical implementations
- `tested-by-qc` — QuickCheck attack surfaces

Used by `scripts/search_by_*.py` and reserved for future embedding/vector tooling.

<!-- footernav:start -->

---
> **Back to:** [HOME](HOME.md) · [NAVIGATION](NAVIGATION.md) · [MASTER-INDEX](indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
