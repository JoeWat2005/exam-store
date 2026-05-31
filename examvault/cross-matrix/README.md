<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · **cross-matrix**

# Cross-Matrix: Combining Trees/Lists/Expr with Monads

> **Mental model:** the exam's hardest questions are *combinations*. "Label every node of a Rose tree with a fresh integer" combines `Rose` (data structure) with `State` (effect). "Evaluate an expression and log every step" combines `Expr` with `Writer`. "Validate a tree of inputs" combines `BT` with `Either`. The vault's `trees/` and `monads/` directories cover each axis in isolation; this directory covers the *intersections*.

## The matrix

Rows = data structure. Columns = effect.

|              | Maybe                              | Either                              | State                              | Writer                              | Reader                              | Monad m (generic)                              | List monad                              |
|--------------|------------------------------------|-------------------------------------|------------------------------------|-------------------------------------|-------------------------------------|------------------------------------------------|-----------------------------------------|
| **BT / Tree** | [tree-x-maybe](tree-x-maybe.md)    | [tree-x-either](tree-x-either.md)   | [tree-x-state](tree-x-state.md)    | [tree-x-writer](tree-x-writer.md)   | [tree-x-reader](tree-x-reader.md)   | [tree-x-generic-monad](tree-x-generic-monad.md) | —                                       |
| **BST**      | (subset of BT)                     | (subset of BT)                      | [bst-x-state](bst-x-state.md)      | [bst-x-writer](bst-x-writer.md)     | (subset of BT)                      | (subset of BT)                                  | —                                       |
| **Rose**     | (subset of generic)                | (subset of generic)                 | [rose-x-state](rose-x-state.md)    | [rose-x-writer](rose-x-writer.md)   | (subset of generic)                 | (subset of generic)                             | —                                       |
| **Expr**     | [expr-x-maybe](expr-x-maybe.md)    | (similar to maybe)                  | [expr-x-state](expr-x-state.md)    | (covered in interpreters/)          | (covered in interpreters/)          | (covered in interpreters/)                      | —                                       |
| **List**     | [list-x-monad](list-x-monad.md)    | (similar)                           | [list-x-state](list-x-state.md)    | [list-x-writer](list-x-writer.md)   | —                                   | [list-x-monad](list-x-monad.md)                 | [list-x-list-monad](list-x-list-monad.md) |
| **Multi**    | —                                  | —                                   | [expr-x-multi](expr-x-multi.md)    | [expr-x-multi](expr-x-multi.md)     | [expr-x-multi](expr-x-multi.md)     | —                                               | —                                       |
| **Game**     | —                                  | —                                   | [game-state](game-state.md)        | —                                   | —                                   | —                                               | —                                       |
| **Parser**   | (subset)                           | [parser-x-either](parser-x-either.md) | —                                | —                                   | —                                   | —                                               | —                                       |
| **Writer + Either** | —                          | [writer-x-either](writer-x-either.md) | —                                | —                                   | —                                   | —                                               | —                                       |

## Files in this directory

| File | Combo | Pattern |
|---|---|---|
| [tree-x-maybe.md](tree-x-maybe.md) | BT/Tree × Maybe | safe lookup, partial eval, find path |
| [tree-x-either.md](tree-x-either.md) | BT × Either e | validation with error message |
| [tree-x-state.md](tree-x-state.md) | BT × State | **labelling, fresh IDs, numbering** (canonical) |
| [tree-x-writer.md](tree-x-writer.md) | BT × Writer | log traversal, count via Sum |
| [tree-x-reader.md](tree-x-reader.md) | BT × Reader | env-aware traversal |
| [tree-x-generic-monad.md](tree-x-generic-monad.md) | BT × Monad m | **`mapMTree`, `traverseTree`, `filterMTree`, `foldMTree`** (canonical) |
| [bst-x-state.md](bst-x-state.md) | BST × State | insert with fresh ID |
| [bst-x-writer.md](bst-x-writer.md) | BST × Writer | trace insert/delete |
| [rose-x-state.md](rose-x-state.md) | Rose × State | number every node |
| [rose-x-writer.md](rose-x-writer.md) | Rose × Writer | DFS log |
| [expr-x-maybe.md](expr-x-maybe.md) | Expr × Maybe | partial evaluators |
| [expr-x-state.md](expr-x-state.md) | Expr × State | counters/fresh-vars during eval |
| [expr-x-multi.md](expr-x-multi.md) | Expr × (env + storage + error + trace) | full interpreter stack |
| [list-x-monad.md](list-x-monad.md) | List × Monad | `mapM`, `filterM`, `replicateM`, `forM` |
| [list-x-state.md](list-x-state.md) | List × State | generate, partition with counter |
| [list-x-writer.md](list-x-writer.md) | List × Writer | log per element |
| [list-x-list-monad.md](list-x-list-monad.md) | List × List monad | **nondeterminism, guards** (canonical) |
| [game-state.md](game-state.md) | Game × State | Nim / TTT / Conway state machine |
| [parser-x-either.md](parser-x-either.md) | Parser × Either | **descriptive parse errors** (`ParseErr` type, typed failure modes) |
| [writer-x-either.md](writer-x-either.md) | Writer × Either | **audit trail + typed failure** (log up to point of failure) |

## Why the combo matters

The combo unlocks something neither piece alone can do:
- Tree + State → tree shape preserved, but every node enriched with positional info.
- Tree + Writer → tree-value computation alongside an audit log of every step.
- List + List → fan-out search (`do`-block enumeration).
- Expr + Multi → a real interpreter (env lookup, store, error, trace) — exactly the course interpreter.

## Recognition: which combo?

| Symptom in question | Combo |
|---|---|
| "every node gets a fresh integer" | tree × State |
| "log every traversal step" | tree/rose × Writer |
| "may fail at any node" | tree × Maybe (or Either) |
| "lookup-via-context" | tree × Reader |
| "generic over any monad m" | tree × generic-monad |
| "enumerate all paths/options" | list × list-monad |
| "thread state through a list" | list × State |
| "evaluate expression, may fail" | expr × Maybe |
| "evaluate expression with variable env" | expr × Reader (subset of multi) |
| "Nim/TicTacToe game state" | game × State |

## Search keywords

mapM tree, traverse tree, labelTree, fresh, numberTree, foldMTree, filterMTree, evalExpr Maybe, tree Reader, evalState tree, execWriter tree, list-monad guard, nondeterminism, replicateM, NimGame, BST insert State, Writer log tree

## See also

- [Trees](../trees/) — data-structure-only material
- [Monads](../monads/) — effect-only material
- [Typeclasses/traversable.md](../typeclasses/traversable.md) — the generic-monad shape
- [Archetype 03: Generic Monad](../archetypes/) (course archetype)
- [Archetype 02: State Game](../archetypes/)
- [Interpreters](../interpreters/) — Expr×Multi in production

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
