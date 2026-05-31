<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [pitfalls](./README.md) · **Pitfalls — LOW severity (style / efficiency / habits)**

<!-- siblings:start -->
> **Peers:** [HIGH-severity](./HIGH-severity.md) · **LOW-severity** · [MEDIUM-severity](./MEDIUM-severity.md) · [imports-pitfalls](./imports-pitfalls.md) · [per-topic-pitfalls](./per-topic-pitfalls.md) · [signature-pitfalls](./signature-pitfalls.md)
<!-- siblings:end -->






# Pitfalls — LOW severity (style / efficiency / habits)

> **What counts as LOW:** habits that rarely lose marks directly but waste time, make code harder to debug, or trip the marker on edge cases involving very large inputs. The QuickCheck marker uses small inputs (typically `chooseInt (1, 10)` or `sized` up to ~18), so most efficiency issues don't bite — but the ones that do are documented here.

The pattern: code that's correct but ugly or slow. Fix these AFTER the function works.

---

<a id="p-200"></a>
## P-200 · `myReverse xs = myReverse (tail xs) ++ [head xs]` is O(n²)

**Topic:** List efficiency
**Symptom:** On `[1..100]`, the naive reverse builds 99 intermediate lists via `++`, total O(n²) operations. The marker rarely tests at that size — but on Mock-style `sized` tests up to depth 18, this can time out.
**Cause:** Right-folding with `++` and not using an accumulator.
**Fix:** Use an accumulator helper `go`. O(n) overall.
**Example wrong:**
```haskell
myReverse []     = []
myReverse (x:xs) = myReverse xs ++ [x]            -- O(n²)
```
**Example right:**
```haskell
myReverse :: [a] -> [a]
myReverse xs = go xs []
  where go []     acc = acc
        go (x:xs) acc = go xs (x : acc)
```
**Marks lost:** 0 (usually) — but 5+ if marker has a large-input test
**Seen in:** A09 archetype reimplementations.

---

<a id="p-201"></a>
## P-201 · `(++ [x])` inside recursion → O(n²)

**Topic:** List efficiency
**Symptom:** Same as P-200 — `xs ++ [x]` traverses the WHOLE list every time you append one element.
**Cause:** "I want to add x to the end" — but Haskell's lists are singly-linked from the FRONT. Appending one element is O(n).
**Fix:** Prepend with `(x:)`, then reverse once at the end. Or use a DList / accumulator.
**Example wrong:**
```haskell
collect :: BT a -> [a]
collect Empty        = []
collect (Fork x l r) = collect l ++ [x] ++ collect r       -- the [x] sandwich is fine if balanced
-- but the truly wrong version:
collect (Fork x l r) = (collect l ++ collect r) ++ [x]     -- accumulate at end → O(n²)
```
**Example right:**
```haskell
-- In-order: list-concat is fine (each [x] is small)
collect Empty        = []
collect (Fork x l r) = collect l ++ x : collect r
```
**Marks lost:** 0 (usually)
**Seen in:** beginner accumulators.

---

<a id="p-202"></a>
## P-202 · `if-then-else` multi-line indentation breaks layout

**Topic:** Layout rule
**Symptom:** Parse error. GHC's layout rule treats indentation as significant — a misaligned `then` or `else` breaks the parser.
**Cause:** Writing `if cond` at column N, then `then` at column N+2, `else` at column N+5 with the rest of the function at column M < N.
**Fix:** Either use one line, or align `then` and `else` with the `if`, AND indent the body deeper.
**Example wrong:**
```haskell
classify x = if x > 0
then "positive"
  else if x < 0
  then "negative"
else "zero"
-- Parse error on `then` because layout columns don't match.
```
**Example right:**
```haskell
classify x | x > 0     = "positive"
           | x < 0     = "negative"
           | otherwise = "zero"
-- Or:
classify x = if x > 0
             then "positive"
             else if x < 0
                  then "negative"
                  else "zero"
```
**Marks lost:** 5+ (compile fail) — close to HIGH; this is LOW because it's caught immediately if you compile-check.
**Seen in:** beginner code.

---

<a id="p-203"></a>
## P-203 · Unnecessary parens around already-tight expressions

**Topic:** Readability
**Symptom:** Marker doesn't care; humans grading bonus do. `((map f) xs)` and `(f $ x)` are noise.
**Cause:** Belt-and-braces parenthesisation.
**Fix:** Trust precedence: function application binds tightest. `f x y` is `(f x) y`. `map f xs` is `(map f) xs`. No need to parenthesise.
**Marks lost:** 0
**Seen in:** universal beginner code.

---

<a id="p-204"></a>
## P-204 · `head` / `tail` on possibly-empty list without `safeHead`

**Topic:** Partial functions
**Symptom:** Marker rarely tests this if the function is correct in context — but if it does, you crash.
**Cause:** Treating `head` as safe.
**Fix:** Pattern-match `(x:_) -> x; [] -> default`. Or define `safeHead = listToMaybe`. The Prelude `Data.Maybe.listToMaybe` is allowed.
**Example wrong:**
```haskell
firstChild :: Rose a -> a
firstChild (Branch xs) = case head xs of Leaf y -> y; _ -> ...
-- crashes on Branch []
```
**Example right:**
```haskell
firstChild :: Rose a -> Maybe a
firstChild (Leaf x)           = Just x
firstChild (Branch [])        = Nothing
firstChild (Branch (Leaf y:_)) = Just y
firstChild (Branch (b:_))     = firstChild b
```
**Marks lost:** 0-1 (rare) — but see HIGH P-018 if function spec REQUIRES emptiness.
**Seen in:** lists-attacks.md.

---

<a id="p-205"></a>
## P-205 · `where` vs `let` choice — purely stylistic

**Topic:** Local definitions
**Symptom:** None — both compile and behave identically.
**Cause:** Stylistic preference.
**Fix:** Prefer `where` for clauses that span multiple cases (it's visible at the end). Prefer `let ... in` for single-expression locals.
**Marks lost:** 0
**Seen in:** universal.

---

<a id="p-206"></a>
## P-206 · Explicit recursion when `foldr` is cleaner

**Topic:** Readability
**Symptom:** None — both work.
**Cause:** Writing things out explicitly. Sometimes clearer; sometimes hiding the pattern.
**Fix:** If you see `f [] = base; f (x:xs) = combine x (f xs)`, that's literally `foldr combine base`. Use it if `combine` is short.
**Example wrong-ish:**
```haskell
mySum []     = 0
mySum (x:xs) = x + mySum xs
```
**Example better:**
```haskell
mySum = foldr (+) 0
```
**Marks lost:** 0
**Seen in:** A09 / A10.

---

<a id="p-207"></a>
## P-207 · `length xs == 0` instead of `null xs`

**Topic:** Style + efficiency
**Symptom:** Slightly slower (`length` traverses the whole list); reads less idiomatically.
**Cause:** Habits from imperative languages.
**Fix:** `null xs` is O(1) and clearer.
**Example wrong:**
```haskell
nonEmpty xs = length xs > 0
nonEmpty xs = length xs /= 0
```
**Example right:**
```haskell
nonEmpty xs = not (null xs)
```
**Marks lost:** 0 (usually) — could matter on large inputs but the marker rarely goes there.
**Seen in:** universal.

---

<a id="p-208"></a>
## P-208 · `if cond then True else False` (redundant)

**Topic:** Style
**Symptom:** Reads as "if-then-else returns the bool directly".
**Cause:** Translating `cond ? true : false` from imperative thinking.
**Fix:** `if cond then True else False` IS `cond`. Drop the if.
**Example wrong:**
```haskell
isPositive n = if n > 0 then True else False
```
**Example right:**
```haskell
isPositive n = n > 0
```
**Marks lost:** 0
**Seen in:** beginner code.

---

<a id="p-209"></a>
## P-209 · Naming conflicts with Prelude (shadowing `length`, `map`, etc.)

**Topic:** Naming
**Symptom:** Compile warning "This binding for `length' shadows the existing binding". You then call `length` in another helper and the WRONG version runs.
**Cause:** Reimplementing `myLength` but calling it `length`. Or worse, defining `length` locally without realising it shadows Prelude.
**Fix:** Prefix re-implementations with `my` or `naive`. NEVER shadow Prelude in a question unless explicitly asked.
**Example wrong:**
```haskell
length :: [a] -> Int             -- shadows Prelude.length
length [] = 0
length (_:xs) = 1 + length xs
-- elsewhere:
foo xs = take (length xs) xs    -- which length?  could be ambiguous
```
**Example right:**
```haskell
myLength :: [a] -> Int
myLength [] = 0
myLength (_:xs) = 1 + myLength xs
```
**Marks lost:** 0-2 (if it causes a subtle bug)
**Seen in:** A09.

---

<a id="p-210"></a>
## P-210 · Verbose `case`-of when guards work

**Topic:** Style
**Symptom:** None — both work.
**Cause:** Translating from `switch` syntax.
**Fix:** Guards on the LHS are usually cleaner than `case`-of when matching on Bool conditions.
**Example wrong-ish:**
```haskell
classify n = case compare n 0 of
               LT -> "negative"
               EQ -> "zero"
               GT -> "positive"
```
**Example better:**
```haskell
classify n | n > 0     = "positive"
           | n < 0     = "negative"
           | otherwise = "zero"
```
**Marks lost:** 0
**Seen in:** universal.

---

<a id="p-211"></a>
## P-211 · Forgetting to use `(\_ -> ...)` or `_` for unused arguments

**Topic:** Style / warnings
**Symptom:** Compile warning "Defined but not used: `x'". Doesn't fail the marker but clutters output.
**Cause:** Pattern-matching on an argument you don't use.
**Fix:** Use `_` for unused binds.
**Example wrong:**
```haskell
const x y = x                              -- 'y' unused → warning
```
**Example right:**
```haskell
const x _ = x
```
**Marks lost:** 0
**Seen in:** universal.

---

<a id="p-212"></a>
## P-212 · `(+1)` vs `+ 1` — operator section syntax

**Topic:** Sections
**Symptom:** `(- 1)` parses as the NUMBER -1, not "subtract 1"! This is a famous Haskell trap.
**Cause:** Sections are `(op x)` or `(x op)` for binary operators — but `(-)` is NOT a section; it's the literal "negate".
**Fix:** Use `subtract 1` instead of `(- 1)`. Or `\x -> x - 1`.
**Example wrong:**
```haskell
decrementAll = map (- 1) [1,2,3]                 -- TYPE ERROR: -1 :: Int, not Int -> Int
```
**Example right:**
```haskell
decrementAll = map (subtract 1) [1,2,3]          -- [0,1,2]
-- Or:
decrementAll = map (\x -> x - 1) [1,2,3]
```
**Marks lost:** 5 (compile fail) — close to HIGH; LOW because GHC catches it.
**Seen in:** beginner sections.

---

<a id="p-213"></a>
## P-213 · `(.)` vs `(.)` over-application

**Topic:** Function composition
**Symptom:** Type errors when you try to compose multiple-argument functions blindly.
**Cause:** `(.)` is for unary functions. `f . g $ x = f (g x)`. If `g` takes two arguments, `f . g` doesn't directly work — you need `(f .) . g` or `\x y -> f (g x y)`.
**Fix:** Don't force point-free style. Write `\x y -> f (g x y)` if it's clearer.
**Marks lost:** 0-1
**Seen in:** A10.

---

<a id="p-214"></a>
## P-214 · Letting GHCi linger with stale module after edit

**Topic:** Workflow
**Symptom:** You edit the file, switch to ghci, call the function — get the OLD result. Confused.
**Cause:** `:l` doesn't auto-reload on file change. Need `:r` to reload.
**Fix:** After ANY edit, run `:r` in ghci. Or use `:set +c` and trust.
**Marks lost:** 0 (waste of time only)
**Seen in:** universal.

---

<a id="p-215"></a>
## P-215 · `error` vs `undefined` for stubs

**Topic:** Stubs
**Symptom:** None — both crash. But `undefined` is shorter to type and more idiomatic.
**Cause:** Stylistic preference.
**Fix:** Use `undefined` for "fill this in later". Use `error "specific msg"` if you want a specific failure message for debugging.
**Marks lost:** 0 (both leave a crash if reached)
**Seen in:** universal.

---

<a id="p-216"></a>
## P-216 · Excessive comments where code is self-documenting

**Topic:** Style
**Symptom:** None.
**Cause:** Verbosity habits.
**Fix:** Code should explain itself. Comment only the NON-OBVIOUS choices (e.g. "vacuous truth" annotation on `isBST Empty = True`).
**Marks lost:** 0
**Seen in:** universal.

---

## See also

- `HIGH-severity.md` — marks-killers
- `MEDIUM-severity.md` — silent correctness bugs
- `per-topic-pitfalls.md` — Ctrl-F by topic

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
