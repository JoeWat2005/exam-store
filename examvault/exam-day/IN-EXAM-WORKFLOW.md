<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [exam-day](./README.md) · **IN-EXAM WORKFLOW — per-question 6-step loop**

<!-- siblings:start -->
> **Peers:** [EXAM-DAY-ROUTE](./EXAM-DAY-ROUTE.md) · **IN-EXAM-WORKFLOW** · [LAST-HOUR-CHECKLIST](./LAST-HOUR-CHECKLIST.md) · [ONE-PAGE-PANIC](./ONE-PAGE-PANIC.md) · [RECOGNITION-FLOWCHART](./RECOGNITION-FLOWCHART.md) · [TIME-BUDGET](./TIME-BUDGET.md) · [WHAT-TO-PIN](./WHAT-TO-PIN.md)
<!-- siblings:end -->






# IN-EXAM WORKFLOW — per-question 6-step loop

> Do this loop for each of the 5 questions. Target: 22 minutes per question. Skip step 7 unless stuck.

---

## The loop

```
1. READ (60s)             — write type sig + base case stub in answer file
2. RECOGNISE (60s)        — use IF-YOU-SEE-X / RECOGNITION-FLOWCHART → archetype number
3. PULL (60s)             — open archetypes/A##.md, scan canonical template
4. CHECK MUTATIONS (60s)  — open question-families/<archetype>/<mutation>.md
5. ADAPT (10-15 min)      — rename ctors, plug spec in, compile-check at each step
6. EDGE CASES (2 min)     — quickcheck/<topic>-attacks.md → eyeball every input class
7. STUB OUT (if stuck > 10 min on step 5) — leave a type-correct stub, MOVE ON
```

---

## Step 1: READ (60 seconds)

In your answer file (`MockTest.hs` or equivalent), find the function under the question:

```haskell
---------------------------------------------------------------------------------
-- QUESTION 1
---------------------------------------------------------------------------------

isNBranching :: Int -> Rose a -> Bool
isNBranching n t = undefined        -- this is the stub the template gave you
```

Replace the body. Leave the signature ALONE.

Add a base case ON THE FIRST LINE of the body:

```haskell
isNBranching :: Int -> Rose a -> Bool
isNBranching _ (Leaf _) = True       -- BASE CASE FIRST
isNBranching n (Branch xs) = undefined   -- recursive case TBD
```

This gives you a compilable skeleton in 60 seconds. The function won't WORK yet, but it has the shape.

## Step 2: RECOGNISE (60 seconds)

Open `RECOGNITION-FLOWCHART.md` (it should already be pinned). Walk top-to-bottom.

For Q1 in the Mock:
- "Does the question give a custom ADT with recursive constructors?" → YES (Rose).
- "Does ANOTHER ADT appear in the answer signature?" → NO (only Rose).
- "Does the answer signature say `instance T MyADT where`?" → NO.
- "Is the answer the SAME ADT?" → "Rose a -> Bool" / "Rose a -> Rose a" — YES.
- → **A01** (tree recursion, Rose variant).

Write `A01` in a comment above your function:

```haskell
-- A01 Rose
isNBranching :: Int -> Rose a -> Bool
isNBranching _ (Leaf _) = True
```

## Step 3: PULL (60 seconds)

Open [A01-tree-recursion](../archetypes/A01-tree-recursion.md). Find the Rose template:

```haskell
f :: Rose a -> r
f (Leaf x)    = base x
f (Branch xs) = combine (map f xs)
```

For `isNBranching n`:
- `base x = True` (a Leaf is vacuously n-branching)
- `combine` should check the length AND recurse: `\rs -> length xs == n && and rs`
- But actually: pattern-match on the wrapper, use `all (isNBranching n) xs`:

```haskell
isNBranching _ (Leaf _) = True
isNBranching n (Branch xs) = length xs == n && all (isNBranching n) xs
```

Type that in. Compile.

## Step 4: CHECK MUTATIONS (60 seconds)

If the question has a non-standard twist (rare, but possible — e.g. "n-branching MOST levels but allow some leaves at any level"), check `question-families/<archetype>/<mutation>.md` if it exists for the archetype.

For Mock Q1, the question is the canonical case. No mutation. Move on.

## Step 5: ADAPT (10-15 minutes)

Implement the actual function. Test in ghci as you go:

```bash
ghci MockTest.hs
> :r
> isNBranching 2 (Leaf 0)
True
> isNBranching 2 (Branch [Leaf 1, Leaf 2])
True
> isNBranching 2 (Branch [Leaf 1])
False
> isNBranching 2 (Branch [Branch [Leaf 1, Leaf 2], Branch [Leaf 1, Leaf 2]])
True
> isNBranching 2 (Branch [Branch [Leaf 1, Leaf 2], Branch [Leaf 1, Leaf 2, Leaf 3]])
False   -- the right inner Branch has 3 children
```

If any of these don't match, adjust the function. Common bugs:
- Forgot `&& all (isNBranching n) xs` → returns True on the last test
- Used `&& any` instead of `&& all` → wrong logic
- Type sig changed → compile fails

## Step 6: EDGE CASES (2 minutes)

Open [rose-attacks](../quickcheck/rose-attacks.md). Eyeball every input class:

```
1. Leaf alone (n=0, n=1, n=5)
2. Branch [] (the empty branch — what does the marker say about this?)
3. Branch [Leaf x] (1 child — should match n=1)
4. Branch [Branch []] (empty grandchild)
5. Deep nesting (5+ levels)
6. Mixed Leaf and Branch siblings (Branch [Leaf x, Branch [...]])
```

Mentally trace your function on each. If any breaks, fix.

For `isNBranching`:
- `Leaf 0` (n=anything): True. ✓
- `Branch []` (n=0): `length [] == 0 = True; all _ [] = True` — True. ✓
- `Branch []` (n=1): `length [] == 1 = False` — False. ✓
- `Branch [Leaf x]` (n=1): `length [Leaf x] == 1 = True; all (isNBranching 1) [Leaf x] = True` — True. ✓
- Deep: works because the recursion is uniform.

## Step 7: STUB OUT (only if stuck > 10 min on step 5)

If step 5 has eaten 10 minutes and ghci is still red, STUB:

```haskell
isNBranching :: Int -> Rose a -> Bool
isNBranching _ _ = True       -- STUB: lazy default. Will fail tests on n != 0
                              -- but file COMPILES → other Qs still graded.

prune :: Int -> Rose a -> Rose a
prune _ t = t                 -- STUB: identity. Will fail tests.
```

Then move to the next question. Don't look back until the skip-and-return pass.

---

## Per-question quick-reference card

### Q1 (typically tree recursion)
1. READ: signature `f :: ... -> Rose a -> ...`
2. RECOGNISE: A01
3. PULL: §5 of common-templates
4. ADAPT: pattern-match Leaf and Branch; recurse with `map` or `all` on Branch xs
5. EDGE: `Leaf x`, `Branch []`, deep nesting

### Q2 (typically generic Monad)
1. READ: signature has `Monad m =>`
2. RECOGNISE: A03
3. PULL: §14 of common-templates
4. ADAPT: base case `n == 0` returns `do x <- mx; return [x]` (NOT `pure []`)
5. EDGE: `n = 0` (one-element), `n = 1` (two-element), negative n

### Q3 (typically State game)
1. READ: signature mentions `NimGame` or `State s`
2. RECOGNISE: A02
3. PULL: §8 of common-templates
4. ADAPT: `gameOver = do (x,y) <- get; return (x == 0 && y == 0)`;
          `takeTokens` clamps with `max 0`
5. EDGE: `(0,0)` for gameOver, `n > x` for takeTokens, both heaps

### Q4 (typically matrix predicate)
1. READ: signature `[[Int]] -> Bool` or similar grid
2. RECOGNISE: A04
3. PULL: §13 of common-templates
4. ADAPT: target = sum of first row; check rows, cols (transpose), both diagonals
5. EDGE: empty grid (return False), 1×1 (trivial True), non-square (return False)

### Q5 (typically ADT translation)
1. READ: two ADTs; signature `SourceADT -> TargetADT`
2. RECOGNISE: A05
3. PULL: §12 of common-templates
4. ADAPT: per-ctor recursion. **Be careful with copy-paste between similar cases** (P-019).
5. EDGE: each ctor needs a separate match; for Mock Q5, `Implies` desugars to `Or (Not p) q`

---

## Compilation discipline

After EVERY function:
1. Save the file.
2. In ghci: `:r` to reload.
3. Check for warnings (especially incomplete-patterns).
4. Type-check by calling the function: `:type isNBranching`.
5. Run a single test: `isNBranching 2 (Leaf 0)`.

If any of those produce errors, fix BEFORE moving to the next function. A broken function might mask warnings in others.

## Common ghci shortcuts

```
:r            -- reload (after edit)
:t expr       -- type of expression
:i name       -- info (constructor / typeclass)
:q            -- quit
:set +s       -- show timing
:set prompt "ghci> "
:! cmd        -- run shell command
```

## Mental hygiene during the exam

- Breathe between questions. 30 seconds of nothing = better than 30 seconds of frantic typing.
- DON'T re-read the same line 5 times. Move on, come back.
- DON'T compare yourself to others. Only your file matters.
- Time elapsed > expected? Stub and move on. Now.

## When you hit a compile error you don't understand

1. Read the error message — line and column.
2. Look at THAT line. Often a missing `)` or `,` or `do`.
3. If still stuck after 60 seconds, comment out the function:
```haskell
{-
isNBranching :: Int -> Rose a -> Bool
isNBranching = ...
-}

-- Stub:
isNBranching :: Int -> Rose a -> Bool
isNBranching _ _ = True
```
4. File compiles. You can come back.

## When QuickCheck (in ghci) finds a counterexample

```
*** Failed! Falsifiable (after N tests):
Branch [Leaf 1, Branch []]
```

This is a SAMPLE — the failure shows the smallest case that breaks. Reason backwards:
- What was the expected output for `Branch [Leaf 1, Branch []]`?
- What did your code return?
- Why is there a difference?

Don't immediately fix. UNDERSTAND first, then fix.

---

## See also

- `EXAM-DAY-ROUTE.md` — full timeline
- `TIME-BUDGET.md` — 22-min × 5 strategy
- `RECOGNITION-FLOWCHART.md` — read-to-archetype mapping
- `ONE-PAGE-PANIC.md` — when you blank
- `archetypes/A##.md` — canonical solutions per archetype
- `quickcheck/<topic>-attacks.md` — what the marker generates per topic

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
