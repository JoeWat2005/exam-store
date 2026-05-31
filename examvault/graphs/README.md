<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · **graphs**

# graphs

Machine-readable knowledge graphs (`.json`), **reserved for the `scripts/search_by_*.py` tooling** — they encode the vault's nodes and edges so the scripts can answer "what combines with X", "what must I learn before Y", "which monads stack". This is **not** student-facing copy-paste material: nothing here is exam code. If you are revising by hand, use the prose pages (`archetypes/`, `monads/`, `trees/`, `question-families/`) instead; the data below is the *index those pages are derived from*. Each file carries a `_meta` block describing its schema, node-fields, and edge-types.

| Graph | Nodes | Purpose |
|---|---|---|
| [`ARCHETYPE-GRAPH.json`](./ARCHETYPE-GRAPH.json) | A01–A24 archetypes | combines-with / mutates-into / primary-files edges; sourced from the cross-archetype heat-map. Drives "what pairs with this archetype". |
| [`DEPENDENCY-GRAPH.json`](./DEPENDENCY-GRAPH.json) | course topics | prerequisite topology (`A → B` = learn A before B); used for study-order planning. |
| [`MONAD-GRAPH.json`](./MONAD-GRAPH.json) | monads + transformers | subsumes / can-stack-with / implements (which typeclasses each monad satisfies); drives transformer-stacking queries. |
| [`QUESTION-GRAPH.json`](./QUESTION-GRAPH.json) | question-families | family → archetype, related-family, and problem-number instances; the mutation atlas in graph form. |
| [`TOPIC-GRAPH.json`](./TOPIC-GRAPH.json) | lecture topics | depends-on / related-to / implemented-in / drives-archetype; sourced from `meta/COURSE-MAP.md` + `meta/COURSE-COVERAGE.md`. |
| [`TREE-GRAPH.json`](./TREE-GRAPH.json) | tree types (BT, BST, Rose, Expr, …) | operation-on / cross-with-monad / subtype-of edges; maps each tree type to its available operations and crossings. |

See [`meta/SCRIPT-COMPATIBILITY-REPORT.md`](../meta/SCRIPT-COMPATIBILITY-REPORT.md) for which scripts consume which graph, and the field contract each script relies on. **Do not change a graph's `_meta` schema or field names without updating the consuming script** — the parsers key off them.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
