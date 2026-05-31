<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [exam-day](./README.md) · **EXAM DAY ROUTE — minute-by-minute playbook**

<!-- siblings:start -->
> **Peers:** **EXAM-DAY-ROUTE** · [IN-EXAM-WORKFLOW](./IN-EXAM-WORKFLOW.md) · [LAST-HOUR-CHECKLIST](./LAST-HOUR-CHECKLIST.md) · [ONE-PAGE-PANIC](./ONE-PAGE-PANIC.md) · [RECOGNITION-FLOWCHART](./RECOGNITION-FLOWCHART.md) · [TIME-BUDGET](./TIME-BUDGET.md) · [WHAT-TO-PIN](./WHAT-TO-PIN.md)
<!-- siblings:end -->






# EXAM DAY ROUTE — minute-by-minute playbook

> 2 hours · 5 questions × 10 marks · vLab · auto-marked by QuickCheck
> 35+/50 = 1st class. Bank easy questions FIRST. Skip when stuck. Re-check at end.

This is the timeline. Read it twice the day before. On the day, glance once and execute.

---

## Before you walk in

### Night before
- Sleep 7+ hours. Tired brain misreads signatures.
- Final skim: `ONE-PAGE-PANIC.md`, `HIGH-severity.md`, `RECOGNITION-FLOWCHART.md`. Stop NEW material 24h before exam.
- Verify vLab login works. Verify `git pull` on `fp-learning-2025` succeeds.
- Verify Canvas can accept a test upload.

### Morning of
- Eat. Water bottle. Toilet break.
- Bring: nothing physical (open book on vLab); know your password.

---

## The 2-hour timeline (120 minutes)

### 00:00 — 00:02 · Setup (2 min)
```
- Log into vLab.
- Open terminal, cd to exam directory (announced on screen).
- ls — verify MockTest-Template.hs (or equivalent) is there.
- cp MockTest-Template.hs MockTest.hs       # NEVER EDIT THE TEMPLATE
- Open MockTest.hs in your editor (VS Code or vim).
- Open examvault tabs (per `WHAT-TO-PIN.md`):
    1. ONE-PAGE-PANIC.md
    2. indexes/IF-YOU-SEE-X.md
    3. indexes/TYPE-SIGNATURE-DATABASE.md
    4. archetypes/README.md
    5. quickcheck/QUICKCHECK-ATTACKS.md
    6. pitfalls/HIGH-severity.md
    7. pitfalls/signature-pitfalls.md
    8. exam-day/RECOGNITION-FLOWCHART.md
```

### 00:02 — 00:07 · Read all 5 questions, mark archetypes (5 min)
```
- Read Q1 to Q5 in order — SCAN ONLY, do not start coding.
- For each Q, write in the margin:
    Q1: A__   (archetype number from RECOGNITION-FLOWCHART.md)
    Q2: A__
    Q3: A__
    Q4: A__
    Q5: A__
- Mark each Q with E (easy), M (medium), H (hard) gut-feel confidence.
- Note any Q that uses an UNFAMILIAR construct — these go last.
```

### 00:07 — 00:08 · Pick attack order (1 min)
```
- Sort by confidence: E first, then M, then H.
- Write the order: e.g. "order: Q3, Q1, Q4, Q2, Q5".
- Q5 (usually ADT-translation) often tempting LAST because it's intricate.
- Q2 (generic Monad) often tempting FIRST because it's short.
- Resist anchoring to question order — trust your confidence rating.
```

### 00:08 — 00:33 · Q-easiest (25 min)
Per-question loop (see `IN-EXAM-WORKFLOW.md` for the detailed 6-step):
```
00:08 - Read spec carefully. Write type sig + Empty/base case stub.
00:09 - Open RECOGNITION-FLOWCHART, decide archetype.
00:10 - Open archetypes/A##.md, scan canonical template.
00:11 - Open question-families if relevant (canonical vs mutation).
00:12 - Implement. Compile-check at each function (Ctrl+S, run ghci :r).
00:25 - Test mentally with edge cases (Empty / [] / 0 / negative / singleton).
00:28 - Look at quickcheck/<topic>-attacks.md — eyeball each input class.
00:32 - Move on. Don't perfect. Mark "DONE" in margin.
```

### 00:33 — 00:58 · Q-2nd-easiest (25 min)
Same loop. By now your routine is warm.

### 00:58 — 01:23 · Q-3rd (25 min)
This is the median question. Likely M or H. If stuck after 10 minutes:
- Stub the function with `undefined`
- Make sure the file still compiles
- Move on to the next question
- RETURN if time at end

### 01:23 — 01:48 · Q-4th + Q-5th, allocated as you go (25 min)
The remaining two questions share this time.
- If both are easy, finish both.
- If one is the hardest, give it 15-20 min, stub the other if time runs out.
- **Never let one question eat more than 25 minutes.** Stub and move on.

### 01:48 — 01:55 · Skip-and-return pass (7 min)
```
- Re-attempt anything you stubbed with `undefined`.
- Re-check anything you marked "incomplete".
- If you can't make progress, leave it stubbed. A stubbed function that COMPILES is better than a broken one that doesn't.
```

### 01:55 — 02:00 · Final 5 minutes — PRE-SUBMIT (5 min)
```
01:55 — Run: ./presubmit.sh MockTest && echo OK || echo FAIL
01:55 — If FAIL, READ THE OUTPUT. Probably:
    - import error → remove the bad import
    - non-exhaustive pattern → add a base case stub
    - Safe-Haskell error → undo the unsafe thing
01:56 — If OK, scan pitfalls/README.md's 60-second checklist.
01:57 — Quick visual: every function has a base case; no `undefined` left; no
        imports outside the allowed set.
01:58 — Upload MockTest.hs to Canvas (or vLab submit script — follow exam rubric).
01:59 — Verify upload succeeded (Canvas shows the file under "Submitted").
02:00 — DONE. Walk out.
```

---

## Hard rules

### Rule 1: Never edit `Types.hs`
If you accidentally touch it, restore from the template. `cp ../MockTest/Types.hs .` if needed.

### Rule 2: Never delete the `{-# LANGUAGE Safe #-}` pragma
The whole top of the template (down to the "DO NOT MAKE ANY CHANGES ABOVE THIS LINE" marker) is sacred. If you delete or change a single character, you lose the entire paper.

### Rule 3: Never skip the 60-second pre-submit check
Even when time is tight. The check finds the marks-killers that you can't see while heads-down coding.

### Rule 4: Never leave `undefined` in a SUBMITTED file
If a question is stubbed, the function must at least RETURN something type-correct. `undefined` will crash on first call → 0 on that question. Better: return `[]` for `[a]`, `False` for `Bool`, `error "TODO"` if the spec permits errors (only Q3 takeTokens in mock).

Actually, for the marker: `undefined` only crashes when forced. With `deepseq`, anything you return WILL be forced. So:
- `Empty` for `BT a`
- `Leaf x` for `Rose a` where `x` is the input
- `[]` for any list result
- `False` for predicates (or `True` if the spec says vacuously)
- `0` for numbers
- `Right ([], 0)` for `Either e (a, s)` etc.

### Rule 5: Never search the WEB
- StackOverflow: BANNED.
- ChatGPT/AI: BANNED.
- Google: BANNED.
- Hoogle: ALLOWED (official Haskell type-signature search).
- Your notes (this examvault): ALLOWED.
- Course materials: ALLOWED.

If you forget a Prelude function's name, **search the vault first**: [IF-YOU-SEE-X](../indexes/IF-YOU-SEE-X.md) or [allowed-builtins](../haskell-basics/allowed-builtins.md). Then Hoogle.

---

## If something goes catastrophically wrong

### vLab crashes
1. Don't panic. Refresh once.
2. If still down, raise hand.
3. The invigilator will give you time back.
4. Your saved code is on the persistent volume (vLab keeps state).

### You opened the file but it's blank / corrupted
1. `cp MockTest-Template.hs MockTest.hs` (overwrite).
2. Re-implement from your archetype templates. Faster than panicking.

### You delete the Safe pragma by accident
1. Open the template (`MockTest-Template.hs`).
2. Copy the first 10 lines (everything down to "DO NOT MAKE ANY CHANGES").
3. Paste over your file's first 10 lines.
4. Verify imports are intact.

### You realise at 01:50 that Q1 has a bug
1. Don't rewrite. Look at the SPECIFIC failing case.
2. Fix the ONE pattern that's wrong.
3. Recompile. Move on.

### `presubmit.sh` says FAIL with 5 minutes left
1. Read the LAST error line in the output. It points to the file and line.
2. Most common: non-exhaustive pattern. Add a base case stub.
3. Second most common: import error. Delete the offending import.
4. Recompile. Resubmit.

---

## Time discipline

| Total Q time | Result |
|---|---|
| 25 min × 5 Qs = 125 min | OVERRUNS by 5 min. NO. |
| 24 min × 5 Qs = 120 min | Perfect on paper, no buffer. |
| 22 min × 5 Qs = 110 min | 10-min buffer for re-check. THIS IS THE TARGET. |
| 20 min × 5 Qs + 20 min rechk = 120 | Safe target with healthy buffer. |

**Target: 20-22 minutes per question, with 15-minute pre-submit buffer.**

If you're at 30 minutes on Q3 and still no progress: STUB AND MOVE ON. Your future self will thank you.

---

## What "DONE" looks like per question

Each question is DONE when:
1. The function compiles (no warnings about incomplete patterns).
2. Mental edge cases run: `[]`, `Empty`, `Leaf`, `0`, `-1`, singleton.
3. You've eyeballed the relevant `quickcheck/<topic>-attacks.md` file once.
4. You've written a comment `-- DONE` next to the function name. (Helps the re-check pass.)

DON'T mark DONE if:
- There's an `undefined` in the function body.
- There's an `error "TODO"` (will fire and zero the test).
- You haven't tested a single edge case mentally.

---

## See also

- `ONE-PAGE-PANIC.md` — when you blank
- `IN-EXAM-WORKFLOW.md` — the per-question 6-step loop
- `TIME-BUDGET.md` — 24-min × 5 detail
- `RECOGNITION-FLOWCHART.md` — read-to-archetype mapping
- `LAST-HOUR-CHECKLIST.md` — pre-exam routine
- `WHAT-TO-PIN.md` — vault tab order
- [README](../pitfalls/README.md) — 60-second pre-submit check

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
