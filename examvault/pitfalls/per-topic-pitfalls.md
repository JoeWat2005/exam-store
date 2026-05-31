<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [pitfalls](./README.md) · **Pitfalls — Per-topic index (Ctrl-F me)**

<!-- siblings:start -->
> **Peers:** [HIGH-severity](./HIGH-severity.md) · [LOW-severity](./LOW-severity.md) · [MEDIUM-severity](./MEDIUM-severity.md) · [imports-pitfalls](./imports-pitfalls.md) · **per-topic-pitfalls** · [signature-pitfalls](./signature-pitfalls.md)
<!-- siblings:end -->






# Pitfalls — Per-topic index (Ctrl-F me)

> One Ctrl-F page. Topic header + bulleted pitfall ids. Open this file as a vault tab during the exam; jump to a topic, then open the severity file for the full pitfall.

Format: `Severity P-### · short trigger`. Click through to the severity file for code.

---

## Lists / Cons recursion
- HIGH P-005 · base case missing — `f (x:xs) = ...` without `f [] = ...`
- HIGH P-008 · numeric recursion uses `n == 0` not `n <= 0` — infinite loop on negatives
- HIGH P-018 · `head` / `tail` on possibly-empty list
- HIGH P-022 · base case written AFTER recursive case (still legal but error-prone)
- MEDIUM P-101 · `zipEither` returns wrong "shorter list" message
- MEDIUM P-112 · `foldr` vs `foldl` swap
- MEDIUM P-119 · `concatMap` confused with `map`
- LOW P-200 · O(n²) reverse — `myReverse (x:xs) = myReverse xs ++ [x]`
- LOW P-201 · `(++ [x])` in recursion → O(n²)
- LOW P-207 · `length xs == 0` vs `null xs`
- LOW P-209 · shadowing Prelude `length`/`map`/etc.
- LOW P-212 · `(- 1)` parses as -1 not "subtract 1"

## Binary Trees (`BT a = Empty | Fork a (BT a) (BT a)`)
- HIGH P-005 · missing `Empty` base case
- HIGH P-016 · `fmap` doesn't preserve shape (Empty maps to Fork or vice-versa)
- HIGH P-022 · base case order — `Empty` should be FIRST
- HIGH P-027 · only test happy path, not `Empty`
- MEDIUM P-104 · `mapBT` swaps left/right
- MEDIUM P-107 · pre-order vs in-order flatten
- MEDIUM P-108 · `leaves Empty = 1` (should be 0)
- MEDIUM P-115 · `mapMTree` rebuilds with `Empty` in wrong slot

## Rose Trees (`Rose a = Leaf a | Branch [Rose a]`)
- HIGH P-014 · `isNBranching` shallow check — `length xs == n` MISSING `&& all (isNBranching n) xs`
- HIGH P-005 · `Branch []` not handled (`Branch` is unbounded children)
- MEDIUM P-119 · `concatMap` vs `map` for flatten
- (Two ADT variants in the wild — see [VAULT-AUDIT](../meta/VAULT-AUDIT.md); Mock uses `Leaf | Branch`)

## BST
- HIGH P-009 · `isBST Empty = False` — must be `True` (vacuous truth)
- HIGH P-015 · `delete` two-children case mis-handled
- HIGH P-020 · three different `isBST` impls in old vault — pick bound-threading version
- HIGH P-018 · `head`/`tail` in min/max helpers without guards
- MEDIUM P-107 · `flatten` not in-order → BST sorting test fails
- MEDIUM P-117 · `lookup` returns `Maybe` — bind directly without case-on

## State monad
- HIGH P-006 · Mock Q3 `gameOver` not returning True on `(0,0)`
- HIGH P-024 · `takeTokens` returns wrong type (`Bool` instead of `()`)
- HIGH P-029 · `do x <- mx; return mx` double-wraps
- MEDIUM P-105 · `takeTokens` doesn't clamp at 0 — underflow
- MEDIUM P-111 · `runState` vs `evalState` vs `execState` confusion
- MEDIUM P-118 · running the same action twice instead of binding once

## Writer monad
- MEDIUM P-110 · `tell` ordering — log appears after action instead of before
- (Watch for `Monoid w` constraint required in signatures)

## Maybe / Either
- HIGH P-018 · `fromJust` without guard
- MEDIUM P-100 · `chainDivisions` not using `do` on Maybe — wrong short-circuit
- MEDIUM P-101 · `zipEither` wrong shorter-list message
- MEDIUM P-117 · `lookup` returns `Maybe` — bare-bind type error
- MEDIUM P-120 · pattern-bind in `do` is INTENTIONAL — don't "fix" it

## Generic Monad (`Monad m =>`)
- HIGH P-007 · `applyNTimes _ _ 0` returns `[]` instead of `pure [x]` (Mock Q2)
- MEDIUM P-102 · recursion threads `mx` instead of `(mf x)` — off-by-one in chain
- MEDIUM P-115 · `mapMTree` shape mistake — `Empty` in wrong slot

## ADT translation (Mock Q5 family)
- HIGH P-019 · Mock Q5 `Or p q` copy-paste — `p` repeated where `q` belongs
- MEDIUM P-103 · same as above but milder cases (where some Or-tests still pass)
- MEDIUM P-109 · `Implies` case forgotten — non-exhaustive pattern crash

## Functor / Monad instances
- HIGH P-010 · `deriving Functor` requires `DeriveFunctor` — incompatible with Safe
- HIGH P-012 · custom `Show` returns non-string
- HIGH P-016 · `fmap` not preserving shape (Functor identity law)
- MEDIUM P-114 · `map f . map g` vs `map (f . g)` — usually fine, sometimes signals deeper bug
- MEDIUM P-116 · custom Monad `>>=` not threading state

## Matrix predicates (Mock Q4)
- HIGH P-030 · anti-diagonal computed wrong direction
- MEDIUM P-106 · rows confused with cols (`transpose` direction)

## Interpreter / Env eval
- HIGH P-004 · using `Control.Monad.Reader` / `Except` — FORBIDDEN imports
- MEDIUM P-117 · `lookup` returns `Maybe` — must `case`-on it
- MEDIUM P-120 · `do IVal x <- eval ...` pattern-bind is INTENTIONAL

## Signatures / Module
- HIGH P-001 · type signature changed (any character)
- HIGH P-002 · module declaration changed (renamed, lost export)
- HIGH P-013 · function name changed (casing, pluralisation)
- HIGH P-025 · returned `Bool` where `Maybe a` expected (or vice-versa)
- See `signature-pitfalls.md` for full coverage

## Imports / Safe Haskell
- HIGH P-003 · imports outside allowed set
- HIGH P-004 · `Control.Monad.Reader` / `Except` — forbidden
- HIGH P-010 · `deriving Functor` (needs DeriveFunctor, incompatible with Safe)
- HIGH P-011 · `{-# LANGUAGE Safe #-}` pragma deleted
- HIGH P-026 · Safe pragma blocks all tests
- See `imports-pitfalls.md` for full coverage

## Compile warnings (not errors but they bite)
- HIGH P-017 · `-fwarn-incomplete-patterns` ignored
- HIGH P-022 · base case after recursive case
- HIGH P-023 · `deepseq` exposes lazy `undefined`
- HIGH P-028 · `presubmit.sh` exit code ignored

## Marker structure (cascade-aware)
- HIGH P-021 · `IfFail` cascade misread — fix the wrong test
- HIGH P-023 · `deepseq` forces hidden `undefined`
- See [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) lines 100-122 for full cascade explanation

## Style / efficiency (low-stakes)
- LOW P-200 · O(n²) reverse
- LOW P-201 · `(++ [x])` in recursion
- LOW P-202 · `if-then-else` indentation breaks layout
- LOW P-203 · unnecessary parentheses
- LOW P-204 · `head`/`tail` without guards (low when context implies non-empty)
- LOW P-205 · `where` vs `let` (no impact)
- LOW P-206 · explicit recursion when `foldr` is cleaner
- LOW P-207 · `length xs == 0` vs `null xs`
- LOW P-208 · `if cond then True else False` (redundant)
- LOW P-209 · shadowing Prelude
- LOW P-210 · verbose `case`-of when guards work
- LOW P-211 · unused arguments warning
- LOW P-212 · `(- 1)` parses as -1
- LOW P-213 · `(.)` over-application
- LOW P-214 · stale ghci module
- LOW P-215 · `error` vs `undefined` for stubs
- LOW P-216 · excessive comments

---

## See also

- `HIGH-severity.md` — full code examples for HIGH pitfalls
- `MEDIUM-severity.md` — full code for MEDIUM
- `LOW-severity.md` — full code for LOW
- `archetypes/A##.md` — canonical solutions per archetype

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
