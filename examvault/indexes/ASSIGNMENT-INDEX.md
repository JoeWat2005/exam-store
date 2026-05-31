<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **ASSIGNMENT-INDEX**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · **ASSIGNMENT-INDEX** · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · [MASTER-INDEX](./MASTER-INDEX.md) · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# ASSIGNMENT-INDEX

Birmingham FP 2025/26 assignments 1, 2, 3 — topic, marking quirks, archetypes, vault files.

**Source:** `fp-learning-2025/files/Assignments/Assignment{1,2,3}/`

> Assignments are graded by `stack repl` + QuickCheck, exactly like the mock + exam. Pattern-recognition transfers directly.

---

## Assignment 1 — GridWithAPointer (Show + Zipper)

**Topic theme:** Custom `Show` with ANSI colour codes (A13) + zipper-like navigation over a grid (A17).
**Files:** `Assignment1/Assignment1.hs`, `Types.hs`, `Marking.hs`.

**Core data type:**
```haskell
data GridWithAPointer = G {
    grid    :: [[Maybe Int]],
    pointer :: (Int, Int)
}
```

**Tasks (high-level):**
1. `Show GridWithAPointer` — pretty-print with the pointed cell highlighted (ANSI escape codes).
2. Move pointer N/S/E/W within bounds. Each direction throws an error if at the edge.
3. Solve a sudoku-style puzzle (mark cells, retract on dead-end, etc.).
4. Detect "uncoverable" grids (hardcoded list).

**Archetypes:**
- A13 (custom Show) — primary for Task 1.
- A17 (zipper-style navigation) — primary for Tasks 2, 3.
- A22 (typeclass instance for ADT).

### ⚠️ SURPRISING MARKER QUIRKS (top tips)

- **Assignment 1 uses `monadicIO` + `catch` to test that some functions THROW errors at boundaries.** The marker expects `moveN/S/E/W` to *crash* when called at the grid edge. If you return `Nothing` or "don't move", you LOSE marks. The exception type matters less than the fact that one occurs.
- **Uncoverable grids are hardcoded:** the marker tests these eight grid sizes specifically:
  ```haskell
  uncoverable = [(7,10),(10,7),(8,11),(8,12),(9,12),(13,10),(14,10),(15,10)]
  ```
  (This sequence is OEIS A068920 — non-coverable rectangles with the L-tromino in some sense — but the marker just compares against the list literal.)
- Your `Show` instance must use the EXACT ANSI escape codes — `"\ESC[31m"` for red etc. The marker compares strings.
- The Safe pragma forbids `unsafePerformIO`. If you sneak it in, presubmit will fail.

**Files in vault:**
- [A13-pretty-printer](../archetypes/A13-pretty-printer.md)
- [A17-zipper](../archetypes/A17-zipper.md)
- [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md)
- [show](../typeclasses/show.md)

---

## Assignment 2 — Morse codec, Tree ↔ Table

**Topic theme:** Bidirectional conversion (A07 codec, A12 representation) + ADT translation (A05).
**Files:** `Assignment2/Assignment2.hs`, `Types.hs`, `Marking.hs`.

**Core data types:**
```haskell
data Tree   = Empty | Branch (Maybe Char) Tree Tree
type Table  = [(Char, [Bool])]
type Morse  = String
```

**Tasks (high-level):**
1. `tabulate :: Tree -> Table` — extract code list from a Morse-style decoding tree.
2. `ramify :: Table -> Tree` — rebuild the tree from a list of codes.
3. Round-trip property `tabulate (ramify t) ≈ t` modulo permutation (it's a **retract**, not an iso — Ex 5 explores this).
4. Morse encode/decode using the tree as the decoder + the table as the encoder.
5. Parser for Morse format (Ex 6).

**Archetypes:**
- A12 (representation conversion) — primary for tabulate/ramify.
- A07 (codec pair) — primary for Morse encode/decode.
- A20 (laws / iso / retract) — primary for Ex 5 proof.
- A16 (parser combinators) — Ex 6 if attempted.

### ⚠️ MARKING QUIRKS

- The round-trip is a **retract** (one-direction only): `tabulate . ramify = id` on Tables, but `ramify . tabulate /= id` on Trees in general (because Empty branches collapse).
- The marker generates Tables with valid prefix-code property — your `ramify` doesn't need to handle malformed input gracefully, but it MUST NOT loop.
- `False = left`, `True = right` is a hard convention — do NOT swap.
- The marker tests Trees with `Branch Nothing l r` and `Branch (Just c) l r` separately; missing the Nothing case is a frequent loss of marks.

**Files in vault:**
- [A07-codec-pair](../archetypes/A07-codec-pair.md)
- [A12-rep-conversion](../archetypes/A12-rep-conversion.md)
- [A20-laws-iso](../archetypes/A20-laws-iso.md)
- [codec-family](../question-families/codec-family.md)

---

## Assignment 3 — Free monad, schedulers (multi-effect)

**Topic theme:** `Free` monad, `Rose ≅ Free [] a`, multi-effect scheduler.
**Files:** `Assignment3/Assignment3.hs`, `Types.hs`, `Marking.hs`.

**Core data types:**
```haskell
data Free f a = Pure a | Free (f (Free f a))
data FSum f g a = InL (f a) | InR (g a)

type FreeState s a    = Free (State s) a
type YieldState s a   = Free (FSum (State s) Yield) a
type SleepState s a   = Free (FSum (State s) (FSum Yield Sleep)) a
```

**Tasks (high-level):**
1. `toRose :: Free [] a -> Rose a` and `fromRose :: Rose a -> Free [] a` — show isomorphism.
2. `trace :: FreeState s a -> State ([s], s) a` — accumulate the history of states.
3. `roundRobin :: [YieldState s ()] -> State s ()` — schedule a list of yield-aware programs.
4. `schedule :: [SleepState s ()] -> State s ()` — extend with sleep counters.

**Archetypes:**
- A20 (iso) — primary for Task 1.
- A14 (multi-effect / Free) — primary for Tasks 2–4.
- A15 (Writer trace-like) — Task 2 has a writer-flavoured trace.
- A02 (State) — every task threads State.

### ⚠️ MARKING QUIRKS

- The marker tests `toRose . fromRose = id` AND `fromRose . toRose = id` — full iso both ways.
- `roundRobin` must run the **first** action until it yields or completes; on yield, **move to back**; on done, **drop**. Wrong order (e.g. running each one step then rotating) silently passes some tests but fails on long programs.
- `Yield ()` is a CONSTRUCTOR, not `pure ()` — be careful in pattern matching.
- `schedule` introduces a sleep counter at each yield; decrementing before yielding vs. after gives different behaviour. The marker tests with sleep > 0 and expects "wait, then wake".
- `Free` instances are derived — don't manually write `Functor`/`Applicative`/`Monad` for `Free f` unless the marker explicitly asks (it usually doesn't, the instances come from `Types.hs`).

**Files in vault:**
- [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md)
- [A20-laws-iso](../archetypes/A20-laws-iso.md)
- [multi-effect](../monads/multi-effect.md)
- [state](../monads/state.md)
- [expr-multi-effect](../interpreters/expr-multi-effect.md)

---

## Cross-cutting properties of all three assignments

| Property | All three? | Note |
|---|---|---|
| Safe pragma + `NoGeneralizedNewtypeDeriving` | Yes | Don't remove. |
| Type signatures auto-checked via `Signatures.hs` re-export | Yes | `presubmit.sh` rebuilds and re-compares. |
| Marking suite: `echo 'main' | stack repl` | Yes | Runs QuickCheck on each function. |
| 100-mark structure (varies by task) | Yes | Sub-tests have weight per spec. |
| `language: GHC2024` | Yes | Use modern Haskell. |
| Dependencies: `QuickCheck`, `marking-core`, `deepseq`, `containers` | Yes | All declared in `package.yaml`. |
| `presubmit.sh` enforces: plain-compile, safe-compile, sig-unchanged | Yes | Run before submission. |

---

## Pre-submit checklist for any assignment

1. **`ghc -fno-code Assignment1.hs`** — no errors, no warnings (incomplete patterns matter).
2. **`ghc -fno-code -XSafe -XNoGeneralizedNewtypeDeriving Assignment1.hs`** — must compile in Safe mode.
3. **`{-# LANGUAGE Safe #-}` pragma intact** at top.
4. **Module name = file name** exactly.
5. **No new imports beyond what's in the template.** If a Marking file imports something extra, that's *theirs*, not yours.
6. **`./presubmit.sh AssignmentN`** exits 0.
7. **`echo 'main' | stack repl`** runs the marker.
8. **No `undefined`** in any function body.
9. **All function signatures unchanged** character-for-character.
10. **The export list** in the module header is unchanged.

---

## How to use during the exam

The exam re-uses the assignment's archetype-set with mutations. If you've internalised the three assignments + the mock test, you have ~95% of the exam shape.

| If exam Q-shape resembles | Look at |
|---|---|
| Mock Q1 (Rose tree predicate + transform) | [MOCK-Q-INDEX](../indexes/MOCK-Q-INDEX.md) Q1 |
| Mock Q2 (`Monad m =>`) | [MOCK-Q-INDEX](../indexes/MOCK-Q-INDEX.md) Q2 |
| Mock Q3 (State game) | [MOCK-Q-INDEX](../indexes/MOCK-Q-INDEX.md) Q3 |
| Mock Q4 (matrix) | [MOCK-Q-INDEX](../indexes/MOCK-Q-INDEX.md) Q4 |
| Mock Q5 (ADT-to-ADT) | [MOCK-Q-INDEX](../indexes/MOCK-Q-INDEX.md) Q5 |
| Assignment 1 (zipper-style) | [A17-zipper](../archetypes/A17-zipper.md) |
| Assignment 2 (tabulate/ramify) | [A12-rep-conversion](../archetypes/A12-rep-conversion.md) |
| Assignment 3 (Free + scheduler) | [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md) |

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
