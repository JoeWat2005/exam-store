<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [exam-day](./README.md) · **TIME BUDGET — 24-minute × 5 strategy + skip-and-return**

<!-- siblings:start -->
> **Peers:** [EXAM-DAY-ROUTE](./EXAM-DAY-ROUTE.md) · [IN-EXAM-WORKFLOW](./IN-EXAM-WORKFLOW.md) · [LAST-HOUR-CHECKLIST](./LAST-HOUR-CHECKLIST.md) · [ONE-PAGE-PANIC](./ONE-PAGE-PANIC.md) · [RECOGNITION-FLOWCHART](./RECOGNITION-FLOWCHART.md) · **TIME-BUDGET** · [WHAT-TO-PIN](./WHAT-TO-PIN.md)
<!-- siblings:end -->






# TIME BUDGET — 24-minute × 5 strategy + skip-and-return

> 2h = 120 min. 5 Qs × 10 marks each. Target: 22 min/Q + 10 min buffer.

## The math

| Allocation             | Time   | Cumulative |
|------------------------|--------|------------|
| Setup + scan all Qs    | 7 min  | 0:07       |
| Pick attack order      | 1 min  | 0:08       |
| Q1 (your easiest)      | 22 min | 0:30       |
| Q2                     | 22 min | 0:52       |
| Q3                     | 22 min | 1:14       |
| Q4                     | 22 min | 1:36       |
| Q5 (your hardest)      | 14 min | 1:50       |
| Skip-and-return pass   | 5 min  | 1:55       |
| Pre-submit + upload    | 5 min  | 2:00       |

That's tight. Use the 10-minute slack you accumulate by finishing some questions early.

---

## Per-question budget (22 min target)

| Phase                       | Time  | Cumulative |
|-----------------------------|-------|------------|
| Read spec carefully         | 1 min | 0:01       |
| Identify archetype          | 1 min | 0:02       |
| Open template, scan         | 1 min | 0:03       |
| Write type sig + base case  | 2 min | 0:05       |
| Implement recursive case    | 8 min | 0:13       |
| Test edge cases mentally    | 3 min | 0:16       |
| Test in ghci                | 3 min | 0:19       |
| Final review + comment      | 3 min | 0:22       |

If you're at 0:13 and the recursive case is broken, you have 9 minutes left. Use them to ATTEMPT a fix. If it's still broken at 0:20, **stub and move on**.

---

## Skip-and-return rules

### When to skip
1. After reading the spec, you can't even identify the archetype after 90 seconds.
2. You started but you're 12 minutes in with no compiling function.
3. You've made progress but the recursive case doesn't pass YOUR ghci sanity check after 18 minutes total.

### How to skip
```haskell
-- Replace the function body with a type-correct stub:
foo :: Int -> BT a -> BT a
foo n t = t   -- STUB: identity. Move on. Return later.

-- Or for Bool:
isFoo :: BT a -> Bool
isFoo _ = True   -- vacuous

-- Or for lists:
collect :: BT a -> [a]
collect _ = []
```

The file MUST compile. No `undefined`. No `error "TODO"`.

### Mark in margin
Write `Q3: SKIP — return at 1:30` so you don't forget.

### When to return
After all 5 questions have at least a stub, AND you have 10+ minutes left.

---

## What "22 min" actually means per Q

### Q1: Tree recursion (typical)
- Read: 1 min ("rose tree", `isNBranching`, `prune`)
- Archetype: A01 — 30 sec
- Template lookup: 30 sec (you've memorised the shape)
- Write `isNBranching` (2 base cases + recursive `&& all (isNBranching n)`): 4 min
- Test mentally: 2 min
- Write `prune` (same shape, `Branch (map (prune n) (take n xs))`): 5 min
- Test: 2 min
- Edge cases (Branch [], Leaf): 2 min
- Compile + ghci sanity: 2 min
- **Total: 19 min**. You'll likely finish under 20.

### Q2: Generic Monad
- Read: 1 min
- Archetype: A03 — 30 sec
- Template: 1 min (memorise `do x <- mx; xs <- applyNTimes (mf x) mf (n-1); return (x:xs)`)
- Implement: 5 min
- The 0-case trap (`do x <- mx; return [x]`): 2 min
- Test with `addAndPrint`: 2 min
- Edge cases: 2 min
- **Total: 14 min**. Easiest of the 5 usually.

### Q3: State game
- Read: 2 min (spec usually has scoring rules)
- Archetype: A02 — 30 sec
- Implement `gameOver`: 1 min (just `do (x,y) <- get; return (x == 0 && y == 0)`)
- Implement `takeTokens`: 5 min (CLAMP, two heap branches)
- Test: 3 min
- Edge cases — `(0,0)`, negative take: 3 min
- **Total: 15 min**. Easy if you've memorised.

### Q4: Matrix predicate
- Read: 2 min (rules of magic square — sums of rows, cols, both diagonals)
- Archetype: A04 — 30 sec
- Implement: 6 min (transpose + zipWith + diagonal)
- Anti-diagonal: 2 min
- Test: 3 min
- Edge cases — 1x1, non-square (should fail), all-zeros: 3 min
- **Total: 17 min**.

### Q5: ADT translation
- Read: 3 min (the AST + target ADT)
- Archetype: A05 — 30 sec
- Per-ctor implementation: 12 min (4-5 ctors, each ~2-3 min)
- TEST EACH ON A SPECIFIC EXAMPLE (use semantic test like Mock Q5 marker does): 4 min
- **Total: 20 min**. The trickiest, hence saved for last when warmed up.

### Combined: 19 + 14 + 15 + 17 + 20 = 85 minutes
+ setup (8) + skip-return (5) + presubmit (5) = 103 minutes
+ 17 minutes of buffer for the inevitable "wait, this isn't typechecking" moments.

---

## When to abandon a question and SUBMIT the stub

After exactly **25 minutes** on any single question without a passing ghci sanity check, STUB IT. No exceptions. Move on.

A clean stub scores 0-2 marks (because of "function exists, signature right" partial credit). A broken function scores 0 with risk of crashing the whole file. The stub is the BETTER outcome.

---

## End-of-exam triage (last 15 min)

If you have 15 min left and:
- All 5 done → presubmit + review HIGH pitfalls list, look for the marks-killers
- 4 done + 1 stubbed → spend 10 min on stub; if no progress, leave stub, presubmit
- 3 done + 2 stubbed → 5 min each on 2 stubs; presubmit at 1:55
- 2 done + 3 broken → presubmit NOW. Make sure the file compiles. Submit. You're scoring on the 2 done + partial on stubs.

**Never re-write a passing function in the final 15 minutes.** You're more likely to break it than improve it.

---

## See also

- `EXAM-DAY-ROUTE.md` — full timeline
- `IN-EXAM-WORKFLOW.md` — per-question 6-step loop
- `ONE-PAGE-PANIC.md` — when you blank

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
