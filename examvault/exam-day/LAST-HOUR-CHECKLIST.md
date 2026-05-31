<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [exam-day](./README.md) · **LAST HOUR CHECKLIST — the hour before the exam**

<!-- siblings:start -->
> **Peers:** [EXAM-DAY-ROUTE](./EXAM-DAY-ROUTE.md) · [IN-EXAM-WORKFLOW](./IN-EXAM-WORKFLOW.md) · **LAST-HOUR-CHECKLIST** · [ONE-PAGE-PANIC](./ONE-PAGE-PANIC.md) · [RECOGNITION-FLOWCHART](./RECOGNITION-FLOWCHART.md) · [TIME-BUDGET](./TIME-BUDGET.md) · [WHAT-TO-PIN](./WHAT-TO-PIN.md)
<!-- siblings:end -->






# LAST HOUR CHECKLIST — the hour before the exam

> Pre-exam routine. Get vLab working. Glance at the panic page. Do NOT learn new material.

## T-60 minutes — vLab setup

```bash
# Log into vLab. Open a terminal.
ssh username@vlab.oc1.aws.cs.bham.ac.uk
# (Or use the web GUI — same effect.)

# Verify the repo is up to date
cd ~/fp-learning-2025
git pull
# Expect: "Already up to date" OR a normal fast-forward merge.
# IF YOU SEE CONFLICTS: do NOT reset. Raise hand, ask invigilator.

# Verify exam directory exists (it will be created at exam start by the announcement)
ls files/Assignments/
# Look for the exam folder (likely "Exam2026" or similar)

# Verify presubmit.sh works on the mock
cd files/Assignments/MockTest
./presubmit.sh MockTest
# Expect: exit code 0. If "command not found", run `chmod +x presubmit.sh`.

# Verify ghci loads
ghci MockTest-Template.hs
# Expect: type prompts. Quit with :q.

# Verify your editor of choice opens
code MockTest-Template.hs    # or vim, or emacs
```

If ANY of these fails: raise hand. The invigilator can help. **Don't try to debug for more than 5 minutes** — get help.

## T-50 minutes — Canvas / submission system check

```
1. Log into Canvas.
2. Navigate to FP module → exam assignment.
3. Verify "Submit" / "Upload File" button is visible.
4. (Optional) Upload a dummy file (e.g. an empty MockTest.hs) to verify the upload mechanism. You can re-submit later.
5. Do NOT submit your real file yet. The exam window has not started.
```

## T-40 minutes — Pin vault tabs

See `WHAT-TO-PIN.md` for the full list. Quick version, open in this order:

```
Tab 1: exam-day/ONE-PAGE-PANIC.md
Tab 2: indexes/IF-YOU-SEE-X.md
Tab 3: indexes/TYPE-SIGNATURE-DATABASE.md
Tab 4: archetypes/README.md
Tab 5: quickcheck/QUICKCHECK-ATTACKS.md
Tab 6: pitfalls/HIGH-severity.md
Tab 7: pitfalls/signature-pitfalls.md
Tab 8: exam-day/RECOGNITION-FLOWCHART.md
Tab 9: exam-day/EXAM-DAY-ROUTE.md
Tab 10: exam-day/IN-EXAM-WORKFLOW.md
```

In VS Code on vLab JupyterLab: right-click each tab → "Keep Tab Open" or "Pin Tab". Pinned tabs persist if you accidentally close the browser.

## T-30 minutes — Final skim

> **MEMORISE THIS LIST RIGHT NOW** — allowed imports:
> `Prelude` (implicit), `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`. Plus the question's `Types` module. **NOTHING ELSE.**
> Anything else (`Data.Map`, `Data.Set`, `Control.Monad.Except`, `Control.Monad.Reader`, `Text.Read`) = compile fail = 0 on that question. Write this on your vLab notepad before you do anything else.

Read in this order (5 min each):

### 1. [ONE-PAGE-PANIC](ONE-PAGE-PANIC.md) (5 min)
The 5 templates. The 5 marks-killers. Recognition shortcuts.

### 2. [HIGH-severity](../pitfalls/HIGH-severity.md) first 10 entries (5 min)
- P-001 type sig changed
- P-002 module declaration changed
- P-003 import outside allowed set
- P-006 gameOver on (0,0)
- P-007 applyNTimes _ _ 0 returns [x]
- P-009 isBST Empty = True
- P-014 isNBranching recurse with `&& all`
- P-019 Mock Q5 Or-case p-vs-q

### 3. [signature-pitfalls](../pitfalls/signature-pitfalls.md) (5 min)
The 5 Mock signatures verbatim. The "do not deviate" rules.

### 4. Walk through one Mock question mentally (5 min)
Open [A02-state-game](../archetypes/A02-state-game.md) (Mock Q3 Nim) and trace:
- `gameOver`: `do (x,y) <- get; return (x == 0 && y == 0)`
- `takeTokens n First`: `do (x,y) <- get; put (max 0 (x-n), y)`
- `takeTokens n Second`: `do (x,y) <- get; put (x, max 0 (y-n))`

If you can recite this from memory, you're ready.

### 5. [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) 60-second checklist (5 min)
The "before you click submit" section. Print mental image.

## T-10 minutes — last thoughts

- DON'T look at new material.
- DON'T re-read the whole vault. You'll only confuse yourself.
- DO take 3 deep breaths.
- DO remind yourself: 35/50 = 1st. You don't need 50.
- DO remind yourself: stub-and-move-on is BETTER than perfectionism.

## Sleep advice (the night before)

- 7+ hours.
- No alcohol.
- No new caffeine experiments.
- Phone in another room.
- Set TWO alarms (in case one fails).
- Lay out clothes / vLab credentials the night before.

## Eat the morning of

- Carbs + protein. Not just coffee.
- Water bottle BEFORE you start (you can't refill mid-exam without raising hand).

## Mental model: the exam is a tournament, not a marathon

- You have 5 INDEPENDENT chances at 10 marks each.
- Failing one Q doesn't affect the others.
- Stub-and-move-on COSTS you marks on that Q only.
- Spending too long on one Q LOSES you marks on the next.

The student who finishes all 5 with 60% accuracy beats the student who finishes 3 perfectly and stubs 2.

## NO new material in last 60 minutes

Studying in the last hour:
- 5 minutes of skim: helpful.
- 30 minutes of new content: ACTIVELY HARMFUL. You confuse yourself.
- 60 minutes of "panic-cramming": you walk in tired and confused.

After the T-10 minute mark, close your laptop. Walk around. Empty your head.

## When the exam starts

1. Read the announcement carefully (location of files, special instructions).
2. Follow `EXAM-DAY-ROUTE.md` 00:00-onwards verbatim.
3. Trust your preparation.

## If you panic at any point

1. Look at `ONE-PAGE-PANIC.md`.
2. Pick the easiest function in front of you.
3. Write the type sig + base case.
4. The next step will follow.

## See also

- `EXAM-DAY-ROUTE.md` — what to do in the exam itself
- `ONE-PAGE-PANIC.md` — when you blank
- `WHAT-TO-PIN.md` — vault tab order
- [README](../pitfalls/README.md) — 60-second pre-submit check

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
