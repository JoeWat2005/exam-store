<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · **monads**

# Monads — Exam Lookup Index

Open-book lookup table for FP exam. Each monad has its own file. This README is the entry point.

**Importable (per practice problem rules):**
`Prelude`, `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`.

**NOT importable** (so DO NOT use): `Control.Monad.Reader`, `Control.Monad.Except`, `Control.Monad.Error.Class`, `Control.Monad.Trans.*`. Reader is in this vault for completeness/typeclass-instance questions only.

---

## 1. Decision table — "what is the question asking for?" → monad

| Question phrase | Use | File |
|---|---|---|
| "may fail / return Nothing / not defined" | `Maybe a` | [maybe.md](maybe.md) |
| "fail with an error message / Left ..." | `Either e a` | [either.md](either.md) |
| "tag the tree / fresh id / counter / accumulator threaded through" | `State s a` | [state.md](state.md) |
| "mutable variable / stack / heap / game board" | `State s a` | [state.md](state.md) |
| "log / trace / collect arguments / sum of recursive calls" | `Writer w a` | [writer.md](writer.md) |
| "print / read input / interactive / main / putStrLn / getLine" | `IO a` | [io.md](io.md) |
| "all possible / non-determinism / list of choices / knight moves / Pythagorean triples" | `[a]` (list monad) | [list-monad.md](list-monad.md) |
| "for any monad m / `Monad m => ...` in the signature" | generic, see | [generic-combinators.md](generic-combinators.md) |
| "`throwError` / divide-by-zero in evaluator / class constraint" | `Either` or `MonadError` | [monaderror.md](monaderror.md) |
| "evaluator with both errors AND state / stack + error" | multi-effect class constraints | [multi-effect.md](multi-effect.md) |
| "read-only env / config / `ask`" | `Reader r a` (function monad) | [reader.md](reader.md) |
| "labelTree / number every node / unique id per name" | `State Int` + `fresh` | [state.md](state.md) |
| "Nim / take-stones / game board with predicate" | `State NimBoard` | [state.md](state.md) — Mock Q3 |
| "monadic recursion over tree" | `mapM`/`forM` or polymorphic-m skeleton | [generic-combinators.md](generic-combinators.md) |

---

## 2. Comparison table — the 7 core monads

| Monad | Failure on | Side effect | `pure` | `>>=` short-circuits on | Runner(s) | Importance |
|---|---|---|---|---|---|---|
| `Maybe a` | `Nothing` | none — partiality only | `Just` | `Nothing` | pattern match / `fromMaybe`/`maybe` | High (Set 10) |
| `Either e a` | `Left e` | error payload | `Right` | `Left _` | pattern match / `either` | High (Set 10, calc) |
| `State s a` | n/a (total) | mutable `s` | `\x -> \u -> (x,u)` | (never short-circuits) | `runState` / `evalState` / `execState` | Critical — Mock Q3 |
| `Writer w a` | n/a | append to `w :: Monoid` | `\x -> (x, mempty)` | (never short-circuits) | `runWriter` / `execWriter` | High (Set 11) |
| `IO a` | n/a | real-world I/O | `return` | (never short-circuits) | `main` only (no `runIO`) | Medium (assignments) |
| `Reader r a` | n/a | read-only `r` | `const x` | (never short-circuits) | `runReader` | Low (instance questions) |
| `[a]` (list) | `[]` | all branches | `\x -> [x]` | `[]` | pattern match / `head`/`null` | Medium (Set 11 #105) |

---

## 3. Recognition trigger phrases (extracted from real question stems)

| If you see... | Reach for |
|---|---|
| "may not be defined" | `Maybe` |
| "if zero, divide-by-zero" | `Either String` or `Maybe` |
| "for any choice of m" + `Monad m =>` | polymorphic skeleton, look at `applyNTimes` |
| "track the next fresh id" | `State Int` |
| "label every node of the tree" | `State Int`, recurse via `do`, `fresh` |
| "log every step" / "record the trace" | `Writer [String]` |
| "count the number of multiplications" | `Writer (Sum Int)` |
| "print" / "read input" / "until the user types..." | `IO` |
| "all moves a knight can make" | list monad / list comprehension |
| "stack calculator" | `State [Int]` (the stack is the state) |
| "find the configuration where..." | list monad + `guard` |
| "evaluator that may fail AND mutates a store" | multi-effect (MonadState + MonadError) |
| "`do x <- m; ...`" with arbitrary `m` | generic, in scope for any monad |

---

## 4. Generic combinators (Control.Monad)

Full reference: [generic-combinators.md](generic-combinators.md). Quick list:

```haskell
mapM        :: Monad m => (a -> m b) -> [a] -> m [b]
mapM_       :: Monad m => (a -> m b) -> [a] -> m ()
forM        :: Monad m => [a] -> (a -> m b) -> m [b]    -- flip mapM
forM_       :: Monad m => [a] -> (a -> m b) -> m ()
sequence    :: Monad m => [m a] -> m [a]
sequence_   :: Monad m => [m a] -> m ()
replicateM  :: Monad m => Int -> m a -> m [a]
replicateM_ :: Monad m => Int -> m a -> m ()
when        :: Applicative f => Bool -> f () -> f ()
unless      :: Applicative f => Bool -> f () -> f ()
void        :: Functor f => f a -> f ()
foldM       :: Monad m => (b -> a -> m b) -> b -> [a] -> m b
filterM     :: Applicative m => (a -> m Bool) -> [a] -> m [a]
zipWithM    :: Applicative m => (a -> b -> m c) -> [a] -> [b] -> m [c]
zipWithM_   :: Applicative m => (a -> b -> m c) -> [a] -> [b] -> m ()
(>=>)       :: Monad m => (a -> m b) -> (b -> m c) -> a -> m c   -- Kleisli compose
(<=<)       :: Monad m => (b -> m c) -> (a -> m b) -> a -> m c
(>>)        :: Monad m => m a -> m b -> m b
(=<<)       :: Monad m => (a -> m b) -> m a -> m b
join        :: Monad m => m (m a) -> m a
guard       :: Alternative f => Bool -> f ()
```

---

## 5. Monad-transformer quick reference (for multi-effect)

The course strongly prefers **class-based constraints** (mtl-style) over explicit transformers in solution code, because the legal imports list does NOT include `Control.Monad.Trans.*`. Use:

```haskell
eval :: (MonadState Storage m, MonadError String m) => Expr -> m Int
```

Concrete monomorphisations the marker can verify:
- `StateT s (Either e) a`   — state + error, error wins
- `Either e (s -> (a, s))`  — state lost on error
- `ReaderT r (State s) a`   — env + state

Transformer reference (for understanding only): [transformers.md](transformers.md).
Multi-effect cookbook (what you actually write): [multi-effect.md](multi-effect.md).

---

## 6. Files in this directory

| File | What it answers |
|---|---|
| [maybe.md](maybe.md)                   | "may fail without message" |
| [either.md](either.md)                 | "may fail WITH message" |
| [state.md](state.md)                   | "mutable variable, counter, board" |
| [writer.md](writer.md)                 | "log / accumulator" |
| [reader.md](reader.md)                 | "read-only env" — instance questions |
| [io.md](io.md)                         | "interactive / `main`" |
| [list-monad.md](list-monad.md)         | "non-determinism / search" |
| [monaderror.md](monaderror.md)         | `MonadError` class |
| [transformers.md](transformers.md)     | `StateT`/`WriterT`/`ExceptT`/`ReaderT` (rare in exam) |
| [multi-effect.md](multi-effect.md)     | "state + error simultaneously" |
| [monad-laws.md](monad-laws.md)         | the 3 laws + QuickCheck checks |
| [generic-combinators.md](generic-combinators.md) | `mapM`, `sequence`, `replicateM`, `when`, ... |

---

## 7. Practice-problem index by monad

| Problems | Monad |
|---|---|
| 91–100  | Maybe / Either (Set 10) |
| 101–104, 110 | IO |
| 105, 106 | List monad |
| 107, 108 | Writer |
| 109 | generic `Monad m => ...` |
| 111–120 | State (Set 12) |
| 121–124, 126 | hand-rolled Monad instances |
| 127–130 | generic combinators (`liftA2`, `join`, `sequence`, `mapM`) |
| 138–140 | parser monad (Set 14) |
| Mock Q2 (`applyNTimes`) | generic `Monad m =>` |
| Mock Q3 (`gameOver`, `takeTokens`) | `State NimBoard` |

---

## 8. Order of attack under exam pressure

1. **Identify the monad** by the trigger phrase table above.
2. **Open that file** and copy the canonical template.
3. **Type-check the signature** against what the question asks. The runner type (`runState` returns `(a,s)`, `evalState` returns `a`, `execState` returns `s`) tells you what to call at the end.
4. **Don't over-engineer**: prefer concrete `Either String Int` over `MonadError String m =>` unless the question explicitly asks for class polymorphism.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
