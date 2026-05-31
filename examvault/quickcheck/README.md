<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · **quickcheck**

# QuickCheck Attack Vault

**Purpose:** make the QuickCheck attack surface for the FP exam *legible*. Scan before you submit. Find the bug the marker will find before it does.

## What this folder is

The Birmingham FP 2025/26 exam (and all assignments) are auto-marked. The marker is a Haskell program that uses [QuickCheck](https://hackage.haskell.org/package/QuickCheck) to generate hundreds of random inputs for your function and compares your output to a reference solution. **One uncovered edge case can wipe a full sub-question.**

This vault catalogues what the marker actually generates, taken straight from `MockTestTestCases.hs`, `Assignment1TestCases.hs`, `Assignment2TestCases.hs`, and `Assignment3TestCases.hs`. Every attack listed here is a real input class the marker is known to use.

## Files

| File | Topic | When to open |
|------|-------|--------------|
| `QUICKCHECK-ATTACKS.md` | MASTER reference — summary table, universal attacks, 60-second pre-submit checklist | Always, last thing before submit |
| `lists-attacks.md` | `[]`, singleton, duplicates, sorted, reverse-sorted | Any list-recursion question |
| `trees-attacks.md` | `Leaf`/`Branch`/`Empty`/`Node`, skewed, deep | Any binary or rose tree question |
| `bst-attacks.md` | `isBST`, `insert`, `member`, `delete` | BST question (the `Empty = True` trap) |
| `rose-attacks.md` | `Rose a = Leaf a \| Branch [Rose a]`, `Branch []`, n-branching | Mock Q1 and any rose-tree variant |
| `expr-attacks.md` | `Var`, `Not`, `And`, `Or`, `Implies`, eval, semantics | Mock Q5 / any expression-tree question |
| `monad-attacks.md` | `mapM`, `applyNTimes`, base case for `n=0`, `pure []` | Mock Q2 and any `Monad m =>` question |
| `state-attacks.md` | `runState`, `execState`, `evalState`, `(0,0)`, underflow | Mock Q3 / Nim / Assignment 3 |
| `writer-attacks.md` | `Writer [Int] Int`, `tell`, order of `tell` calls | Mock Q2 (Writer version), Assignment 3 trace |
| `maybe-either-attacks.md` | `Nothing`, `Just []`, `Left`, `Right`, parser-style | Any `Maybe`/`Either` question, Assignment 2 brackets |
| `codec-attacks.md` | encode/decode round-trip, prefix code ambiguity | Assignment 2 (Morse code) |
| `interp-attacks.md` | div-by-zero, missing variable, shadowing, recursive Let | Any interpreter question |
| `matrix-attacks.md` | `1x1`, rectangular, anti-diagonal, magic | Mock Q4 / Assignment 1 grid |
| `numeric-attacks.md` | divide-by-zero, negative roots, overflow | Any numeric function |
| `typeclass-instance-attacks.md` | Functor/Monad/Eq laws checked via QC | Any `instance` you write |
| [PROPERTY-PATTERNS.md](./PROPERTY-PATTERNS.md) | **`prop_…` shapes + `Arbitrary` instances for BT / Rose / Expr** — the property code you'd write yourself | When you want to sanity-check your own solution before submit |

## How QuickCheck actually works (the 90-second version)

```haskell
prop_reverseInvolutive :: [Int] -> Bool
prop_reverseInvolutive xs = reverse (reverse xs) == xs
```

When the marker runs `quickCheck prop_reverseInvolutive`, QC:

1. Generates ~100 random `[Int]` values via the `Arbitrary` instance.
2. For each, asserts the property is `True` (or returns `property True` / `Right`).
3. If any one fails, it **shrinks** the failing input to the smallest counterexample.
4. Reports `*** Failed!` plus the counterexample.

Key markers in the test files you should learn to recognise:

| Idiom | Meaning |
|-------|---------|
| `~=` (custom) | "approximately equals" — used in marking, deepseq-forces both sides then `==` |
| `===` | QC's polymorphic equals — prints both sides on fail |
| `==>` | implication — discard generated inputs that don't satisfy the precondition |
| `counterexample msg p` | attach a custom failure message to property `p` |
| `forAll gen prop` | use `gen` instead of the default `Arbitrary` instance |
| `makeUnaryPropWith p g s` | the marker's wrapper — uses generator `g` and shrinker `s` |
| `chooseInt (lo, hi)` | random `Int` in `[lo, hi]` inclusive |
| `frequency [(n, gen), ...]` | weighted choice between generators |
| `sized $ \n -> ...` | gen that depends on the size knob (deeper trees as `n` grows) |
| `suchThat g p` | keep generating until `p x` is `True` — used a lot for "non-magic squares" etc. |
| `deepseq x x` | force x fully — used to make sure exceptions fire before equality check |

The marker often uses **custom generators**, not the default `Arbitrary`. This is good news — you can read them and know exactly what's coming.

## How to read each attack file

Each attack file follows the same shape:

```
# QuickCheck attacks: <topic>
**Search keywords:** ...
## What the marker generates    -- summary of the actual generator code
## Attack surface               -- table: input class, example, what fails, how to fix
## Property templates           -- copy-pasteable for local testing
## Self-test before submission checklist
## Pitfalls that specifically lose QC marks
## See also
```

The **"What fails if you forget it"** column is the highest-value content. It's the actual error message you'd see if you submitted without handling that case.

## Workflow

1. **Before starting a question:** open the relevant attack file. Read the "Attack surface" table. Mentally map each row to a clause in your function.
2. **While writing:** keep the file open. When you write a base case, find it in the table.
3. **Before saving / before `stack repl`:** run through the "Self-test before submission checklist".
4. **Last thing before submitting:** open `QUICKCHECK-ATTACKS.md`, run through the 60-second universal checklist.

## Allowed imports for QuickCheck

Submitted code uses **only**: `Prelude`, `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`.

But while *testing locally*, you can `import Test.QuickCheck` and run any property in this vault — the marker has it available, you do too. **Do not** leave the import in your submission file.

## See also

- `../monads/` — the patterns for `mapM`/`applyNTimes`/`Writer`/`State`
- `../trees/` — recursion templates that survive the attacks
- `../interpreter/` — Expr/Circuit/Free patterns
- `../exam-day/` — the route to follow on the 2-hour exam

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
