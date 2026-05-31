<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 11 — Storage as `String -> Integer` (Birmingham lecture)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · **imperative-storage** · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 11 — Storage as `String -> Integer` (Birmingham lecture)

**Effect:** none — storage is a *function*, not a monad
**Effect rationale:** the Birmingham lecture deliberately picks **function-as-storage** so that "memory" is a pure-functional value. Variable lookup is function application; update is lambda-shadow.
**Type signature:** `type Storage = Identifier -> Integer`
**Search keywords:** storage · function-as-env · String-Integer · lecture-storage · empty-storage · update · birmingham-interpreter · imperative-storage · function-memory

> **The choice that matters:** the lecture uses option (3) below, **not** the assoc-list. The whole interpreter is written around it. If a question references "the lecture interpreter", expect this representation.

## Three ways to represent storage

| Option | Type | Lookup | Update | Empty key behaviour |
|---|---|---|---|---|
| 1 | `[(Identifier, Integer)]` | `lookup i m :: Maybe Integer` | `(i, x) : m` (shadowing prepend) | returns `Nothing` |
| 2 | `Data.Map.Map Identifier Integer` | `Map.lookup i m` | `Map.insert i x m` | returns `Nothing` |
| 3 | **`Identifier -> Integer`** ← lecture pick | `m i` | `\j -> if i == j then x else m j` | `error "Uninitialized variable"` |

Lecture source: `fp-learning-2025/files/LectureNotes/Sections/interpreter/Interpreter.hs` line 6 onwards.

## Full type and operations

```haskell
type Identifier = String
type Storage    = Identifier -> Integer

emptyStorage :: Storage
emptyStorage i = error ("Uninitialized variable " ++ i)

update :: Identifier -> Integer -> Storage -> Storage
update i x m = m'
  where
    m' :: Storage
    m' j | i == j    = x
         | otherwise = m j
```

That's it. **`update` returns a new function** that shadows the old one at the one key `i`. The old storage is untouched (functional purity).

## Booleans as integers

The lecture language has booleans only as integers (like C):
```haskell
number :: Bool -> Integer
number False = 0
number True  = 1

boolean :: Integer -> Bool
boolean 0 = False
boolean _ = True
```
Round-trip: `boolean (number b) == b` for any `Bool`, but **not** `number (boolean n) == n` for any `Integer` — only for `0` and `1`. The lecture calls this a "retract": `Bool` is a retract of `Integer`.

## Worked example: a sequence of updates

```haskell
m0 = emptyStorage
m1 = update "x" 5 m0     -- m1 "x" = 5; m1 "y" = error
m2 = update "y" 7 m1     -- m2 "x" = 5; m2 "y" = 7
m3 = update "x" 99 m2    -- m3 "x" = 99; m3 "y" = 7  (m2 is unchanged!)
```

The closure semantics give us perfect history: each `update` builds a chain of functions, each shadowing the previous at one key.

## Equivalent assoc-list version (for comparison)

```haskell
type Storage' = [(String, Integer)]

emptyStorage' :: Storage'
emptyStorage' = []

lookup'  :: String -> Storage' -> Maybe Integer
lookup'  = lookup        -- Prelude

update' :: String -> Integer -> Storage' -> Storage'
update' x v env = (x, v) : env       -- shadow-prepend (oldest at end)
```

Differences:
- Lookup may **fail** (returns `Maybe`); function-storage just **errors** on missing key.
- `lookup'` is O(n); function-storage is O(1) but accumulates closure layers (also O(n) worst case in chain depth).
- You can `length env` to count entries; function-storage gives no introspection.
- `Show` instance: assoc-list has one; function-storage cannot be shown.

## Pros / cons of function-as-storage

**Pros:**
- Pure functional — no mutable cell.
- Lookup is `m i` — trivial.
- Update is a simple closure capture.
- Storage chains preserve history (alpha-equivalent to a snapshot).
- Plays nicely with `Reader` / function monad.

**Cons:**
- No iteration / enumeration of keys — you can't ask "what variables are defined?"
- No `Show` / `Eq` — testing equality requires probing specific keys.
- Errors on missing key are runtime crashes, not Type-safe `Maybe`.
- Chain depth grows with updates; in long-running programs this can be slow.

## Point-free combinators

The lecture also defines storage transformers as values:
```haskell
assign :: Identifier -> Expr -> Storage -> Storage
assign i e = \m -> update i (eval m e) m

ifElse :: (s -> Bool) -> (s -> s) -> (s -> s) -> (s -> s)
ifElse p f g = h
  where h m = if p m then f m else g m

while :: (s -> Bool) -> (s -> s) -> (s -> s)
while p f = g
  where g m = if p m then g (f m) else m

block :: [s -> s] -> s -> s
block []     m = m
block (f:fs) m = block fs (f m)
```

These make `run` a translator from `Program` to `Storage -> Storage` — see [imperative-eval.md](imperative-eval.md).

## Mutations
- **Change to assoc-list.** Replace `Storage = String -> Integer` with `Storage = [(String, Integer)]`. Adjust `update` to `(i, x) :`, lookup to `lookup`, returns `Maybe`.
- **Add typed values.** `type Storage = String -> Maybe Value` where `Value = IntV Integer | BoolV Bool`.
- **Add scoping / call stack.** `Storage = [String -> Integer]` — a list of nested frames, lookup walks the stack.
- **Replace `error` with `Maybe`.** `emptyStorage = \_ -> 0` (default-zero) or `Storage = String -> Maybe Integer` (failable).

## Pitfalls
- **`emptyStorage = const 0`** would silently default uninitialised vars to 0 — the lecture explicitly uses `error` to catch bugs early.
- **`update` argument order.** `update i x m` — identifier, value, then existing storage. Don't swap `i` and `x`.
- **Inner `m'` reuses the outer `m`.** `m' j = m j` for `j /= i` refers to the closed-over `m`. Don't accidentally rebind.
- **`Storage` is not `Show`-able** by default — it's a function. To "print storage", probe specific keys.
- **Chain depth.** Repeated `update i 1 (update i 2 (update i 3 emptyStorage))` builds a chain of three closures even though only the outermost wins. For exam scope this is fine.
- **Confusing `Storage` and `Env`.** Same shape, different roles: `Storage` is **mutable** state of an imperative language; `Env` is **read-only** binding of an expression language. The lecture only has one because it's the imperative language.

## QuickCheck attacks
- `update i x emptyStorage i == x` — what you put is what you read.
- `update i x m j == m j` for `i /= j` — other keys are unchanged.
- `update i x (update i y m) i == x` — most-recent update wins.
- `update i x emptyStorage j == error _` for `j /= i` — uninitialised vars error.
- For assoc-list version: `lookup i (update i x m) == Just x`.

## See also

**Archetypes:** [A02 state game](../archetypes/A02-state-game.md) · [A08 env eval](../archetypes/A08-env-eval.md)
**Cross-topic:** [expr × state](../cross-matrix/expr-x-state.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [state-game](../question-families/state-game-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [state attacks](../quickcheck/state-attacks.md)
**Related (interpreters):** [imperative eval](./imperative-eval.md) · [expr state](./expr-state.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
