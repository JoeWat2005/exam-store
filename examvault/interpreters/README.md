<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · **interpreters**

# interpreters/ — Eval, AST-walker, and small-language interpreter patterns

> **One-line model:** an interpreter is *tree recursion that returns a value*. The AST is a recursive ADT, `eval` walks each constructor, sub-results are combined. Each new effect (failure, env, state, log) wraps the return type in a different monad — but the **shape** of `eval` is identical across all of them.

This directory is the **examvault for Q5-style interpreter / ADT-translation questions** and for the Birmingham-lecture imperative-language interpreter (`Storage = String -> Integer`).

Lecture source: `fp-learning-2025/files/LectureNotes/Sections/interpreter/`
Practice problems: 138-140 (parser), Mock Q5 (Expr -> Circuit desugar), Set 12 (State eval).

---

## Legal imports for the exam

Per the practice rules: only `Prelude`, `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`.

**NOT** legal: `Control.Monad.Reader`, `Control.Monad.Except`, `Control.Monad.Error.Class`, `Control.Monad.Trans.*`.

Implication: anywhere this vault uses `MonadError` or `MonadReader`, treat those as *explanatory* — in exam answers prefer the **concrete monad**: `Either String a` instead of `MonadError String m =>`, the **function-as-env** `String -> Maybe v` instead of `Reader`. We keep the class-constraint versions because the exam *may* ask "what is the most general type?" and they crystallise the structure.

---

## The progression diagram (effects stacked one at a time)

```
                       (problem evolves)
                       --------------->
   pure       +Maybe       +Either       +Reader      +Reader        +Writer
   Expr -> I   Expr -> M I  Expr -> E I   Env -> M I   +Either        +State
                                                       (env+err)      +Either
   |           |            |             |            |              |
   |           Div fails    Div with msg  Variables    Variables      Trace+store
   |           Var fails    Var unbound                + errors       + errors
   v           v            v             v            v              v
[simple]    [maybe]      [either]      [reader]    [reader-either] [multi]
```

ASCII version of the layering, where each step **only adds** to the previous:

```
Layer 0:  Pure                  eval :: Expr -> Int
Layer 1:  +Maybe (silent fail)  eval :: Expr -> Maybe Int
Layer 2:  +Either (msg fail)    eval :: Expr -> Either String Int
Layer 3:  +Writer (trace)       eval :: Expr -> Writer [String] Int
Layer 4:  +State (counter)      eval :: Expr -> State Int Int
Layer 5:  +Reader (env)         eval :: Expr -> Reader Env Int
Layer 6:  +Reader+Either        eval :: Expr -> ReaderT Env (Either String) Int
Layer 7:  +State+Either         eval :: Expr -> StateT s (Either e) Int
Layer 8:  +Writer+State         eval :: Expr -> WriterT [String] (State Int) Int
Layer 9:  Multi (3 effects)     (MonadState s m, MonadError e m, MonadWriter w m) =>
                                Expr -> m Int
```

Each file in this directory implements one layer.

---

## Decision table — "which file matches my question?"

| Question phrase | File |
|---|---|
| "evaluate this expression" / `Expr -> Int` | [simple-arith.md](simple-arith.md) |
| "may divide by zero" / "return Nothing on failure" | [expr-maybe.md](expr-maybe.md) |
| "return an error message" / `Either String` / `throwError` | [expr-either.md](expr-either.md) |
| "log/trace every step" / "record sub-computations" | [expr-writer.md](expr-writer.md) |
| "counter" / "fresh variable supply" / "label every node" | [expr-state.md](expr-state.md) |
| "evaluate with respect to an environment" / `Env -> Expr -> ...` | [expr-reader.md](expr-reader.md) |
| "variable lookup may fail" / env + error | [expr-reader-either.md](expr-reader-either.md) |
| "mutable storage, division by zero" | [expr-state-either.md](expr-state-either.md) |
| "trace + counter" / Writer + State | [expr-writer-state.md](expr-writer-state.md) |
| "state + error + log" / 3-effect interpreter | [expr-multi-effect.md](expr-multi-effect.md) |
| "small imperative language" / `:=` / While / Block | [imperative-storage.md](imperative-storage.md) · [imperative-eval.md](imperative-eval.md) |
| "extend the evaluator to handle X" | [extend-interpreter.md](extend-interpreter.md) |
| "rewrite Implies in terms of Or" / "Expr -> Circuit" / Mock Q5 | [desugar-pipeline.md](desugar-pipeline.md) |
| "write a parser for ..." / `Parser a` | [parser-overview.md](parser-overview.md) |

---

## Birmingham-specific: `Storage = String -> Integer` vs `[(String, Integer)]`

The lecture **deliberately** picks the **function** representation, not the association list. This matters for exam answers because the marker may take the lecture wording literally.

| Repr | Type | Lookup | Update | Empty | Pros | Cons |
|---|---|---|---|---|---|---|
| **Function** (lecture choice) | `String -> Integer` | `m i` | `\j -> if i==j then x else m j` | `\i -> error ("Uninit " ++ i)` | Pure-functional, no list traversal, fast lookup | Cannot enumerate keys, errors on uninitialised access |
| **Assoc list** | `[(String, Integer)]` | `lookup x env` returns `Maybe` | `(x,v) : env` (shadowing) | `[]` | Can enumerate, Show-able, `Maybe` is type-safe | O(n) lookup, lookup must propagate `Maybe` |

> **In the lecture interpreter:** `Storage` is `String -> Integer`. Lookup is just **function application**. Update is **lambda-shadow**. This is what `imperative-storage.md` and `imperative-eval.md` describe.
> **In Set 12 / `final10.hs` / most exam env problems:** `Env = [(String, Int)]`. Lookup is `lookup x env :: Maybe Int`. This is what `expr-reader.md` describes (a function env is the polymorphic / Reader version).

If the question gives you the type, use that. If the question is open-ended, the assoc list is easier to write under time pressure and shows up in more lecture material.

---

## File index

| File | Effect | Sig |
|---|---|---|
| [simple-arith.md](simple-arith.md) | pure | `Expr -> Int` |
| [expr-maybe.md](expr-maybe.md) | Maybe | `Expr -> Maybe Int` |
| [expr-either.md](expr-either.md) | Either | `Expr -> Either String Int` |
| [expr-writer.md](expr-writer.md) | Writer | `Expr -> Writer [String] Int` |
| [expr-state.md](expr-state.md) | State | `Expr -> State Int Int` |
| [expr-reader.md](expr-reader.md) | Reader / Env | `Env -> Expr -> Int` |
| [expr-reader-either.md](expr-reader-either.md) | Reader + Either | `Env -> Expr -> Either String Int` |
| [expr-state-either.md](expr-state-either.md) | State + Either | `Expr -> StateT s (Either String) Int` |
| [expr-writer-state.md](expr-writer-state.md) | Writer + State | `Expr -> WriterT [String] (State Int) Int` |
| [expr-multi-effect.md](expr-multi-effect.md) | three effects | `(MonadState s m, MonadError e m, MonadWriter w m) => Expr -> m Int` |
| [imperative-storage.md](imperative-storage.md) | function-storage | `Storage = String -> Integer` |
| [imperative-eval.md](imperative-eval.md) | imperative run | `Program -> Storage -> Storage` |
| [extend-interpreter.md](extend-interpreter.md) | TEMPLATE | "add ctor → parser → eval" |
| [desugar-pipeline.md](desugar-pipeline.md) | translation | `Surface -> Core`, `Expr -> Circuit` |
| [parser-overview.md](parser-overview.md) | Parser | combinator basics + grammar |

---

## Quick lookup: which monad does each effect need?

| Effect you need | Monad | Operation |
|---|---|---|
| short-circuit on failure, no message | `Maybe` | `Nothing`, `do x <- m; ...` |
| short-circuit with message | `Either e` | `Left "msg"`, `do x <- m; ...` |
| read-only context | `Reader r` (or just an extra arg) | `ask`, `local f m` |
| mutable counter, store, stack | `State s` | `get`, `put`, `modify` |
| accumulate log / trace | `Writer w` (w must be `Monoid`) | `tell`, `writer (a, w)` |
| state AND error | `StateT s (Either e)` | mix |
| reader AND error | `ReaderT r (Either e)` | mix |
| state AND log | `WriterT w (State s)` | mix |

---

## See also
- Archetypes: [A08 env-eval](../archetypes/A08-env-eval.md), [A14 multi-effect](../archetypes/A14-multi-effect-interp.md), [A19 extend-interpreter](../archetypes/A19-extend-interpreter.md), [A05 ADT translation](../archetypes/A05-adt-translation.md)
- Cross-matrix: [expr × monad](../cross-matrix/expr-x-multi.md)
- Pattern: [tree recursion](../archetypes/A01-tree-recursion.md)
- Lecture: `fp-learning-2025/files/LectureNotes/Sections/interpreter/`
- Practice: problems 138-140 (parser), Mock Q5 (desugar)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
