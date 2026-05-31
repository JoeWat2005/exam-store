<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **CROSS-TOPIC-INDEX**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · **CROSS-TOPIC-INDEX** · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · [MASTER-INDEX](./MASTER-INDEX.md) · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# CROSS-TOPIC-INDEX

The exam's hardest questions are *combinations*. The vault's `trees/` and `monads/` directories cover each axis in isolation; the [`cross-matrix/`](../cross-matrix/README.md) directory covers the *intersections*. This page is a single-screen index of those crossings.

**How to use:** find the row (data structure) and column (effect / monad) that matches the question. Click the cell. If a cell is *not* covered, the closest covered cell is usually a 30-second adaptation away.

---

## The crossing matrix

Rows = data structure / domain. Columns = effect / monad. Each cell points to the cross-matrix file plus the one-line canonical technique.

|  | Maybe | Either | State | Writer | Reader | Monad m (generic) | List monad |
|---|---|---|---|---|---|---|---|
| **Binary Tree** (`BT a`) | [tree-x-maybe](../cross-matrix/tree-x-maybe.md) — safe lookup / path find | [tree-x-either](../cross-matrix/tree-x-either.md) — validate with error msg | [tree-x-state](../cross-matrix/tree-x-state.md) — label nodes with fresh IDs | [tree-x-writer](../cross-matrix/tree-x-writer.md) — log every visit | [tree-x-reader](../cross-matrix/tree-x-reader.md) — env-aware traversal | [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md) — `mapMTree`, `traverseTree` | — |
| **BST** | (use [tree-x-maybe](../cross-matrix/tree-x-maybe.md)) | (use [tree-x-either](../cross-matrix/tree-x-either.md)) | [bst-x-state](../cross-matrix/bst-x-state.md) — insert with fresh ID | [bst-x-writer](../cross-matrix/bst-x-writer.md) — trace insert/delete | (use [tree-x-reader](../cross-matrix/tree-x-reader.md)) | (use [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md)) | — |
| **Rose** (`Rose a`) | (use [tree-x-maybe](../cross-matrix/tree-x-maybe.md) with adaptation) | (similar) | [rose-x-state](../cross-matrix/rose-x-state.md) — number every node | [rose-x-writer](../cross-matrix/rose-x-writer.md) — DFS log | (similar) | (use [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md)) | — |
| **Expression Tree** (`Expr`) | [expr-x-maybe](../cross-matrix/expr-x-maybe.md) — partial eval | (similar to Maybe) | [expr-x-state](../cross-matrix/expr-x-state.md) — counters, fresh-vars | (see [interpreters/](../interpreters/README.md)) | [expr-reader](../interpreters/expr-reader.md) | (see [interpreters/](../interpreters/README.md)) | — |
| **List** (`[a]`) | [list-x-monad](../cross-matrix/list-x-monad.md) — `mapM`, `filterM` | (similar) | [list-x-state](../cross-matrix/list-x-state.md) — partition with counter | [list-x-writer](../cross-matrix/list-x-writer.md) — log per element | — | [list-x-monad](../cross-matrix/list-x-monad.md) | [list-x-list-monad](../cross-matrix/list-x-list-monad.md) — nondeterminism |
| **Multi-effect** (`StateT`, `ExceptT`) | — | — | [expr-x-multi](../cross-matrix/expr-x-multi.md) | [expr-x-multi](../cross-matrix/expr-x-multi.md) | [expr-x-multi](../cross-matrix/expr-x-multi.md) | — | — |
| **Game** | — | — | [game-state](../cross-matrix/game-state.md) — Nim / TTT / Conway | — | — | — | — |
| **Parser** | (subset of Maybe form) | [parser-x-either](../cross-matrix/parser-x-either.md) — descriptive errors | — | — | — | — | — |
| **Writer trace + Failure** | — | [writer-x-either](../cross-matrix/writer-x-either.md) — audit-up-to-failure | — | — | — | — | — |

> Canonical cells (most-exam-likely) are **bold-marked** in the cross-matrix README — see [cross-matrix/README](../cross-matrix/README.md).

---

## Recognition cues — phrase → combo

| If the question says... | Combo | File |
|---|---|---|
| "label every node with a fresh integer" | Tree × State | [tree-x-state](../cross-matrix/tree-x-state.md) |
| "every node gets a unique id" | Tree × State | [tree-x-state](../cross-matrix/tree-x-state.md) |
| "log every visit / traversal step" | Tree × Writer | [tree-x-writer](../cross-matrix/tree-x-writer.md) |
| "validate / may fail at any node" | Tree × Maybe (or Either) | [tree-x-maybe](../cross-matrix/tree-x-maybe.md) · [tree-x-either](../cross-matrix/tree-x-either.md) |
| "lookup-in-context" | Tree × Reader | [tree-x-reader](../cross-matrix/tree-x-reader.md) |
| "for any monad m" | Tree × generic-monad | [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md) |
| "enumerate all paths / valid options" | List × List-monad | [list-x-list-monad](../cross-matrix/list-x-list-monad.md) |
| "thread a counter through a list" | List × State | [list-x-state](../cross-matrix/list-x-state.md) |
| "evaluate Expr, may fail" | Expr × Maybe | [expr-x-maybe](../cross-matrix/expr-x-maybe.md) |
| "evaluate Expr with named variables" | Expr × Reader (or Multi) | [expr-reader](../interpreters/expr-reader.md) · [expr-x-multi](../cross-matrix/expr-x-multi.md) |
| "Nim / TicTacToe / game state" | Game × State | [game-state](../cross-matrix/game-state.md) |
| "parse + descriptive error" | Parser × Either | [parser-x-either](../cross-matrix/parser-x-either.md) |
| "log everything up to failure" | Writer × Either | [writer-x-either](../cross-matrix/writer-x-either.md) |
| "BST + insert with id" | BST × State | [bst-x-state](../cross-matrix/bst-x-state.md) |
| "BST + audit log" | BST × Writer | [bst-x-writer](../cross-matrix/bst-x-writer.md) |
| "interpreter that needs state + errors" | Multi-effect | [expr-x-multi](../cross-matrix/expr-x-multi.md) · [transformer-stack-order](../monads/transformer-stack-order.md) |
| "evaluate and log" | Expr × Writer | (see [interpreters/](../interpreters/README.md)) |

---

## Recognition cues — type sig → combo

The *shape* of the type signature alone is often enough.

| Sig fingerprint | Likely combo |
|---|---|
| `BT a -> State s (BT a)` | Tree × State |
| `BT a -> Writer w (BT a)` | Tree × Writer |
| `BT a -> Maybe r` | Tree × Maybe |
| `BT a -> Either e r` | Tree × Either |
| `Monad m => BT a -> m (BT b)` | Tree × generic-monad |
| `Expr -> Maybe Int` | Expr × Maybe |
| `Expr -> Env -> Maybe Int` | Expr × Reader (or curried Reader) |
| `Expr -> StateT s (Either e) Int` | Multi-effect (Mock-style calculator) |
| `[a] -> [b]` with non-deterministic semantics | List × List-monad |
| `Parser a` newtype = `String -> Either e (a, String)` | Parser × Either |
| `m a -> m a -> m a` (logging with possible failure) | Writer × Either |

See [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) for the full fingerprint catalogue.

---

## Per-row deep dive

### Binary Tree × {effect} (the headline row)

- **× Maybe:** [tree-x-maybe](../cross-matrix/tree-x-maybe.md) — partial functions over trees. `safeIndex`, `findPath`, `lookupNode`.
- **× Either:** [tree-x-either](../cross-matrix/tree-x-either.md) — same shape as Maybe, but with a typed error. `validate :: BT a -> Either Err (BT a)`.
- **× State:** [tree-x-state](../cross-matrix/tree-x-state.md) — *canonical*. `labelTree :: BT a -> State Int (BT (a, Int))`. **THE** A01 × A02 combo.
- **× Writer:** [tree-x-writer](../cross-matrix/tree-x-writer.md) — log structural traversal. `traceTree :: BT a -> Writer [String] (BT a)`.
- **× Reader:** [tree-x-reader](../cross-matrix/tree-x-reader.md) — env in scope at every node. Rare alone; usually escalates to multi.
- **× generic Monad:** [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md) — *canonical*. `mapMTree`, `traverseTree`, `filterMTree`, `foldMTree`. The Mock-Q2 archetype × the A01 archetype.

### Expression Tree × {effect}

- **× Maybe:** [expr-x-maybe](../cross-matrix/expr-x-maybe.md) — partial eval with `safeDiv`, `Var`-lookup.
- **× State:** [expr-x-state](../cross-matrix/expr-x-state.md) — eval counters, fresh-name supply.
- **× Multi:** [expr-x-multi](../cross-matrix/expr-x-multi.md) — env + storage + error + trace. The full course interpreter.
- See also [interpreters/](../interpreters/README.md) for the ordered progression Pure → Maybe → Either → Reader → State → Writer → Multi.

### List × {effect}

- **× Monad (generic):** [list-x-monad](../cross-matrix/list-x-monad.md) — `mapM`, `filterM`, `replicateM`, `forM` over any monad.
- **× State:** [list-x-state](../cross-matrix/list-x-state.md) — counter / accumulator threaded through.
- **× Writer:** [list-x-writer](../cross-matrix/list-x-writer.md) — log per element.
- **× List-monad:** [list-x-list-monad](../cross-matrix/list-x-list-monad.md) — non-determinism, `do`-block enumeration, knight-moves, `guard`.

### Specialised crossings

- **Game × State:** [game-state](../cross-matrix/game-state.md) — Nim (Mock Q3), TicTacToe, Conway's GoL state machine.
- **Parser × Either:** [parser-x-either](../cross-matrix/parser-x-either.md) — typed parse errors instead of `Nothing` / `Maybe`. Descriptive failures.
- **Writer × Either:** [writer-x-either](../cross-matrix/writer-x-either.md) — audit trail that survives failure. Log up to the point of error.

---

## Why the cross matters

Each cell teaches something neither piece alone teaches:

- **Tree + State** — tree shape preserved while every node is enriched with positional info.
- **Tree + Writer** — value computation alongside an audit log.
- **List + List** — fan-out search via `do`-block enumeration. No explicit recursion needed.
- **Expr + Multi** — a real interpreter with env lookup, mutable store, error handling, and trace.
- **Parser + Either** — turns `Nothing` ("something failed") into `Left "expected ; at line 3"` ("here's what failed").
- **Writer + Either** — debugging-friendly failure: you see the trace even when the computation aborts.

---

## Combo difficulty heat-map

How hard each combo is once you've mastered the two axes separately:

| Combo | Difficulty | Why |
|---|---|---|
| Tree × State | ★★ | Straight `do`-notation. `get` / `put` / `modify` at every node. |
| Tree × Writer | ★ | Just `tell` at each node before returning the rebuilt tree. |
| Tree × Maybe | ★★ | Pattern-bind in `do`; `MonadFail` does the propagation. |
| Tree × Either | ★★ | Same as Maybe but with a typed `Left`. |
| Tree × generic Monad | ★★★ | Must work *for any m* — no `runState` allowed. |
| List × List-monad | ★★★ | Mental switch: `do` over `[]` is the comprehension `[x | y <- ys]`. |
| Expr × State | ★★★ | Need to choose what counter resets at what scope. |
| Expr × Multi | ★★★★ | Transformer stack order matters (state survives or rolls back). |
| Parser × Either | ★★★ | Wrap the `Parser` `newtype`, redo `Functor` / `Applicative` / `Monad`. |
| Writer × Either | ★★★ | Order matters: `WriterT [String] (Either e) a` keeps log on failure; `ExceptT e (Writer [String]) a` loses it. |

For pure topic-axis depth before combining, hop to:
- [trees/README](../trees/README.md) (data-structure-only material)
- [monads/README](../monads/README.md) (effect-only material)

---

## See also

**Sibling indexes:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md)
**Source matrix directory:** [cross-matrix/README](../cross-matrix/README.md)
**Each axis alone:** [trees/](../trees/README.md) · [monads/](../monads/README.md) · [typeclasses/](../typeclasses/README.md)
**Worked interpreter progression:** [interpreters/README](../interpreters/README.md)
**Transformer stack order:** [transformer-stack-order](../monads/transformer-stack-order.md)
**Generic traversal:** [traversable](../typeclasses/traversable.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
