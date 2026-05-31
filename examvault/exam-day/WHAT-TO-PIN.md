<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [exam-day](./README.md) · **WHAT TO PIN — vault tab order for vLab**

<!-- siblings:start -->
> **Peers:** [EXAM-DAY-ROUTE](./EXAM-DAY-ROUTE.md) · [IN-EXAM-WORKFLOW](./IN-EXAM-WORKFLOW.md) · [LAST-HOUR-CHECKLIST](./LAST-HOUR-CHECKLIST.md) · [ONE-PAGE-PANIC](./ONE-PAGE-PANIC.md) · [RECOGNITION-FLOWCHART](./RECOGNITION-FLOWCHART.md) · [TIME-BUDGET](./TIME-BUDGET.md) · **WHAT-TO-PIN**
<!-- siblings:end -->






# WHAT TO PIN — vault tab order for vLab

> The 10 tabs you open BEFORE the exam starts. Order = priority (1 = open first, look at most).
>
> **Pinned tabs persist across vLab sessions if you use VS Code's preview/pin feature.** In JupyterLab, use the "Pin Tab" right-click option.

---

## Priority pin order

### 1. `examvault/exam-day/ONE-PAGE-PANIC.md`
**Why first:** The single-screen reference. If you blank out, this is the screen you stare at to reset. Contains the 5 templates, 5 marks-killers, and recognition shortcuts.

### 2. `examvault/indexes/IF-YOU-SEE-X.md`
**Why second:** Ctrl-F any phrase from a question → archetype number. Fastest way to anchor.

### 3. `examvault/indexes/TYPE-SIGNATURE-DATABASE.md`
**Why third:** Signature shape → archetype + canonical implementation. When the question text is short but the signature is given, jump here.

### 4. `examvault/archetypes/README.md`
**Why fourth:** Priority ranking + heat map of which archetypes combine. Pinned because the README links to every individual `A##.md`.

### 5. `examvault/quickcheck/QUICKCHECK-ATTACKS.md`
**Why fifth:** The "what the marker generates" reference. Open after writing each function to mentally walk through attacks.

### 6. `examvault/pitfalls/HIGH-severity.md`
**Why sixth:** Read once at start to remind yourself of marks-killers. Reference if a function "works in ghci but might still fail".

### 7. `examvault/pitfalls/signature-pitfalls.md`
**Why seventh:** When `presubmit.sh` complains about Signatures.hs, this is where you look.

### 8. `examvault/exam-day/RECOGNITION-FLOWCHART.md`
**Why eighth:** Walk-through for ambiguous questions. The systematic decision tree.

### 9. `examvault/exam-day/EXAM-DAY-ROUTE.md`
**Why ninth:** Glance at when transitioning between questions to verify you're on the timeline.

### 10. `examvault/exam-day/IN-EXAM-WORKFLOW.md`
**Why tenth:** Reference for the 6-step per-question loop.

---

## Pinned tabs persist across vLab sessions

If you use VS Code (recommended on vLab):
- Right-click each tab → "Keep Tab Open" (or `Ctrl+K Enter`).
- Pinned tabs survive `Ctrl+W` and browser refresh.
- On `git pull`, pinned tabs reload to the new content.

If you use JupyterLab:
- Right-click tab → "Pin Tab".
- Pinned tabs survive logout/login.

If you use vim:
- Open the files in separate buffers: `:e file1` then `:e file2` ... 
- Switch with `:bnext` / `:bprev` or `:ls` to list.

---

## Open BEFORE the exam window starts

Pin all 10 during the 60-minute pre-exam window. When the exam begins:
- Tab 1 is your first action: glance at ONE-PAGE-PANIC.
- Tab 9 (EXAM-DAY-ROUTE) tells you to read all 5 Qs.
- You're already set up.

---

## Tabs to OPEN during the exam (as needed)

These are too specific to pin in advance. Open them when the archetype matches.

| Archetype | Open file                                                          |
|-----------|--------------------------------------------------------------------|
| A01       | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) + [trees-attacks](../quickcheck/trees-attacks.md) + [rose-attacks](../quickcheck/rose-attacks.md) |
| A02       | [A02-state-game](../archetypes/A02-state-game.md) + [state-attacks](../quickcheck/state-attacks.md)     |
| A03       | [A03-generic-monad](../archetypes/A03-generic-monad.md) + [monad-attacks](../quickcheck/monad-attacks.md)  |
| A04       | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) + [matrix-attacks](../quickcheck/matrix-attacks.md) |
| A05       | [A05-adt-translation](../archetypes/A05-adt-translation.md) + [expr-attacks](../quickcheck/expr-attacks.md) |
| A06       | [A06-functor-instance](../archetypes/A06-functor-instance.md) + [typeclass-instance-attacks](../quickcheck/typeclass-instance-attacks.md) |
| A07       | [A07-codec-pair](../archetypes/A07-codec-pair.md) + [codec-attacks](../quickcheck/codec-attacks.md)     |
| A08       | [A08-env-eval](../archetypes/A08-env-eval.md) + [interp-attacks](../quickcheck/interp-attacks.md)      |
| A11       | [A11-bst-ops](../archetypes/A11-bst-ops.md) + [bst-attacks](../quickcheck/bst-attacks.md)          |
| A14       | [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md) + [interp-attacks](../quickcheck/interp-attacks.md) |

After each question, CLOSE the archetype-specific tabs to declutter. Keep the priority 1-10 tabs pinned throughout.

---

## Editor pane setup

Recommended VS Code layout (on vLab):
```
+-------------------+-------------------+
| Editor: MockTest  | Tab 1: ONE-PAGE   |
| .hs (50% width)   | Tab 2: IF-YOU-SEE |
|                   | (50% width)       |
|                   |                   |
+-------------------+-------------------+
| Terminal: ghci    | Tab 8: RECOG-     |
| MockTest.hs       | FLOWCHART         |
| (50% width)       | (50% width)       |
+-------------------+-------------------+
```

`Ctrl+\` (backtick) splits panes in VS Code. Drag tabs into the new pane.

In vim, use `:vsplit` for vertical splits.

---

## Backup plan: print these to PDF

If vLab JupyterLab/VS Code is acting up:
1. Open each priority 1-10 file in a browser tab.
2. `Ctrl+P` → "Save as PDF".
3. Save to your local Downloads.
4. If vLab dies, open the PDFs locally for reference (you still need vLab for code).

The TEXT files are tiny (~10KB each), so PDFs are 1-2 pages.

---

## A pinning shortcut for the morning

Save this as `~/pin_tabs.sh` on vLab:

```bash
#!/bin/bash
# Open all priority tabs in VS Code
cd ~/examvault
code exam-day/ONE-PAGE-PANIC.md
code indexes/IF-YOU-SEE-X.md
code indexes/TYPE-SIGNATURE-DATABASE.md
code archetypes/README.md
code quickcheck/QUICKCHECK-ATTACKS.md
code pitfalls/HIGH-severity.md
code pitfalls/signature-pitfalls.md
code exam-day/RECOGNITION-FLOWCHART.md
code exam-day/EXAM-DAY-ROUTE.md
code exam-day/IN-EXAM-WORKFLOW.md
echo "All priority tabs open. Pin them with Ctrl+K Enter."
```

Then `chmod +x ~/pin_tabs.sh && ~/pin_tabs.sh` opens everything in one go.

---

## See also

- `EXAM-DAY-ROUTE.md` — what to do once tabs are pinned
- `LAST-HOUR-CHECKLIST.md` — full pre-exam routine
- `ONE-PAGE-PANIC.md` — Tab 1 contents

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
