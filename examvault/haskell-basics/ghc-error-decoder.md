<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **GHC error decoder**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · **ghc-error-decoder**
<!-- siblings:end -->






# GHC error decoder

## What this is
When GHC barks at you in red, the fastest path is *not* to read the whole message — it's to `Ctrl+F` the first identifying line on this page, read the translation, apply the fix, `:r`, move on.

Errors are grouped by what GHC was doing when it gave up. Within each group: **error pattern → translation → typical cause → fix**.

## Mental model
Every GHC error is one of five categories:

| Category | What broke | Strategy |
|---|---|---|
| **Type mismatch** | Two types don't unify. | Read what GHC *expected*; that's the slot. Read what it *got*; that's your value. Make them match. |
| **Scope / parse** | GHC can't find a name, or can't make sense of the source text. | Spelling, capitalisation, missing import, missing closing bracket, wrong indent. |
| **Pattern coverage** | A function doesn't handle every constructor. | Add the missing case. |
| **Instance** | No instance for `Show`, `Eq`, `Num`, etc. | Add `deriving`, supply a `Show` value, or pick a concrete monad. |
| **Ambiguity** | Two things have the same name in scope. | Qualified import, or remove one. |

90% of exam errors are category 1 (type) or 2 (scope/parse). Train your eye to spot which.

---

## Type-mismatch errors

### `Couldn't match expected type ‘X’ with actual type ‘Y’`

```text
<interactive>: error:
    • Couldn't match expected type ‘Int’ with actual type ‘[Char]’
    • In the first argument of ‘double’, namely ‘"hi"’
```

**Translation:** "you gave me a `String`, the slot needs an `Int`."

**Typical causes:**
- You passed the wrong argument (here: `double "hi"` when `double :: Int -> Int`).
- You forgot to `read` a `String` into a number.
- You wrote `[x]` when the signature wanted just `x` (or vice versa).
- You used `show` somewhere that wanted the unwrapped value.

**Fix recipe:**
1. Read the *expected* type — that's the signature slot.
2. Read the *actual* type — that's what you wrote.
3. Convert: `read s :: Int` to parse a string, `show n` to render to string, `head xs` to unwrap a singleton, `[x]` to wrap a single value.

See also: [type-signatures](./type-signatures.md) · [testing-functions § reading type errors](./testing-functions.md).

---

### `Couldn't match type ‘a’ with ‘Int’` (polymorphism collapse)

```text
• Couldn't match type ‘a’ with ‘Int’
      ‘a’ is a rigid type variable bound by
        the type signature for: f :: a -> a
```

**Translation:** "your signature says `f` works for *any* `a`, but in the body you assumed `a` is `Int`."

**Typical cause:** You wrote a polymorphic signature (`a -> a`) but the body uses `+ 1` or `* 2`. Those constrain `a` to a `Num` instance.

**Fix:**
- Tighten the signature: `f :: Int -> Int`, or
- Add the class constraint: `f :: Num a => a -> a`, or
- Don't use arithmetic — return `a` unchanged or via a function the caller supplies.

See also: [polymorphism](./polymorphism.md).

---

### `No instance for (Show ...)`

```text
<interactive>: error:
    • No instance for (Show (Int -> Int))
        arising from a use of ‘print’
```

**Translation:** "you tried to print something that has no `Show` instance. Functions and types you defined without `deriving Show` are the usual suspects."

**Typical causes:**
- You partially applied a function and let GHCi try to print the result (it's a function).
- Your custom ADT doesn't `deriving Show`.
- You tried to print a `IO a` action without running it.

**Fix:**
- Functions: use `:t` instead of evaluating. `:t myFilter even` instead of `myFilter even`.
- ADT: add `deriving Show` to the `data` declaration.
- `IO`: just type the action — GHCi runs it. Or wrap in `print` only for non-IO values.

See also: [deriving](./deriving.md) · [show](../typeclasses/show.md).

---

## Scope and parse errors

### `Variable not in scope: foo`

```text
<interactive>: error:
    • Variable not in scope: transpose :: [[a]] -> [[a]]
```

**Translation:** "I don't know what `foo` is."

**Typical causes (in order of frequency):**
1. **Missing import.** `transpose` lives in `Data.List`; add `import Data.List`.
2. **Typo.** `myLenght` instead of `myLength`. Re-read the spelling.
3. **Forgot to `:r`** after defining it in the source file.
4. **Wrong case.** Haskell is case-sensitive. `Just` is the constructor; `just` is undefined.
5. **Defined inside a `where` clause that's out of scope here.**

**Fix:** Confirm the spelling, confirm the import, `:r`, retry.

See also: [allowed-builtins](./allowed-builtins.md) · [imports-pitfalls](../pitfalls/imports-pitfalls.md).

---

### `Parse error on input ‘...’`

```text
parse error on input ‘=’
```

**Translation:** "the source text doesn't make grammatical sense here."

**Typical causes:**
- Missing closing bracket, paren, or quote earlier in the file.
- `=` used where `==` was meant (or vice versa).
- Indentation: the body of a `do` block, `where`, or `let` must be column-aligned.
- A bare expression at the top level. Top-level definitions must look like `name = expr`.

**Fix:** Find the line GHC pointed at, then read *upward* — the real error is often in the line above. Check brackets, indent, and operator spelling.

See also: [pattern-matching](./pattern-matching.md) · [helper-functions](./helper-functions.md).

---

### `Could not find module ‘Foo’`

```text
Could not find module ‘Control.Monad.Reader’
```

**Translation:** "GHC searched and the package providing this module isn't loaded."

**Typical cause on vLab:** You imported a module not in the *allowed list* — the exam permits only `Prelude`, `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`.

**Fix:** Remove the bad import; if the module's functions are essential, find an equivalent in the allowed list or write your own.

See also: [allowed-builtins](./allowed-builtins.md) · [imports-pitfalls](../pitfalls/imports-pitfalls.md) · [safe-haskell](./safe-haskell.md).

---

## Pattern coverage errors

### `Non-exhaustive patterns in function f`

```text
Non-exhaustive patterns in function isNBranching
```

**Translation:** "you defined `f` for some constructors but not all. GHC will succeed at compile time (only a warning), but the marker runs your function on the missing case and gets a runtime crash."

**Typical causes:**
- Forgot `Empty` case for a `BT`.
- Forgot `Leaf` case for a `Rose`.
- Pattern-matched on `(x:xs)` without handling `[]`.

**Fix:** Add the missing constructor as an explicit pattern:

```haskell
sizeBT :: BT a -> Int
sizeBT Empty       = 0           -- !! don't omit this line
sizeBT (Fork _ l r) = 1 + sizeBT l + sizeBT r
```

Run with `:set -Wall` to see the warning in GHCi (`-Wincomplete-patterns`).

See also: [pattern-matching](./pattern-matching.md) · [recursive-data-types](./recursive-data-types.md) · [P-001 base case](../pitfalls/HIGH-severity.md#p-001).

---

### `Pattern match(es) are overlapped`

```text
Pattern match(es) are overlapped
    In an equation for ‘f’: f Empty = ...
```

**Translation:** "a later pattern is shadowed by an earlier one — the later one will never fire."

**Typical cause:** Specific pattern (`Fork _ Empty Empty`) defined *after* the general one (`Fork _ l r`).

**Fix:** Reorder so specific cases come *first*.

See also: [pattern-matching](./pattern-matching.md).

---

## Instance and typeclass errors

### `No instance for (Eq SomeType) arising from a use of '=='`

```text
No instance for (Eq Color) arising from a use of ‘==’
```

**Translation:** "you tried `==` on a value of a type that doesn't have an `Eq` instance."

**Typical cause:** You wrote `data Color = R | G | B` without `deriving Eq`.

**Fix:** Add `deriving Eq` (or `deriving (Eq, Show, Ord)`) to the ADT.

```haskell
data Color = R | G | B deriving (Eq, Show)
```

See also: [deriving](./deriving.md) · [eq-ord](../typeclasses/eq-ord.md).

---

### `Ambiguous occurrence ‘foo’`

```text
Ambiguous occurrence ‘length’
    It could refer to either ‘Prelude.length’
                            or ‘MyModule.length’
```

**Translation:** "two things in scope share the name; I don't know which you mean."

**Typical cause:** You named your re-implementation `length` and it clashes with `Prelude.length`.

**Fix:** Rename to `myLength` (the standard convention in this course), or qualify the call: `Prelude.length xs`.

See also: [list-rewrite-family § naming](../question-families/list-rewrite-family.md).

---

### `Multiple declarations of ‘foo’`

```text
Multiple declarations of ‘sizeBT’
    Declared at: MyFile.hs:5
                 MyFile.hs:18
```

**Translation:** "you have two top-level definitions of `foo` in the same module."

**Typical cause:** Copy-pasted a definition while iterating; didn't delete the old version.

**Fix:** Delete one. Save. `:r`.

---

## Special / advanced

### `Could not deduce (Show a) from the context` (constraint-not-implied)

```text
Could not deduce (Show a) arising from a use of ‘show’
    from the context: Eq a
```

**Translation:** "your signature promised `Eq a`, but you use `show`, which needs `Show a`."

**Fix:** Widen the constraint: `(Eq a, Show a) =>`.

---

### `Saturated application` / `Couldn't match kind`

Rare at this level. Usually means you applied a type constructor to too few or too many type arguments (e.g. `Maybe Maybe` instead of `Maybe (Maybe a)`).

**Fix:** Add or remove a type argument. Use `:k` in GHCi to inspect kinds.

See also: [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md).

---

### `*** Exception:` at runtime (not a compile error)

```text
ghci> head []
*** Exception: Prelude.head: empty list
```

**Translation:** the code compiled but crashed at runtime. Your function is *partial*.

**Typical causes:**
- `head []`, `tail []`, `last []`, `init []`, `!!` index out of range.
- `fromJust Nothing`.
- Division `div x 0`.
- Non-exhaustive patterns (which compile, only warn).

**Fix:** Guard the call site, or use safe variants (`listToMaybe`, `fromMaybe`, your own `safeDiv`).

See also: [maybe-basics](./maybe-basics.md) · [P-006 isBST Empty](../pitfalls/HIGH-severity.md#p-006).

---

## When in doubt — diagnostic moves

If you can't decode an error in 30 seconds:

1. **Check `:t` on each subexpression.** Walk inward. `:t f`, then `:t (f x)`, etc. The point where the type goes wrong is the bug.
2. **Comment out the offending body, replace with `undefined`.** If GHC stops complaining, the body was the issue.
3. **Add an explicit type annotation:** `let n = 0 :: Int`. Sometimes GHC's default choice differs from what you meant.
4. **Reload from a clean GHCi (`:q`, `ghci MyFile.hs`).** Stale state confuses error messages occasionally.
5. **Read the line *above* the line GHC points at.** Often the real bug is one line earlier.

If none works in 90 seconds — *move on*. Note the question, complete easier parts of others, come back at the end.

## Exam use

Two minutes lost to red text is two minutes lost. Open this page in a second tab on vLab so the moment you hit an error you `Ctrl+F` the first 4 words of the message, jump to the entry, apply the fix, `:r`, and you're back on track.

## Common mistakes

- **Reading the whole error.** GHC's error messages are *long*. The first line is usually enough.
- **Editing without `:r`.** You're "fixing" the old code.
- **Not turning on `-Wall`.** Many runtime crashes (non-exhaustive patterns, unused) are caught at compile time with warnings.
- **Ignoring the line number.** GHC almost always points at the right line. Trust it.

## See also

**GHCi tour:** [ghci-commands](./ghci-commands.md)
**Allowed imports:** [allowed-builtins](./allowed-builtins.md) · [imports-pitfalls](../pitfalls/imports-pitfalls.md)
**Testing:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-tree-functions](./testing-tree-functions.md)
**Pitfalls that surface as errors:** [HIGH-severity](../pitfalls/HIGH-severity.md) · [signature-pitfalls](../pitfalls/signature-pitfalls.md)
**Type system:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [deriving](./deriving.md)
**Panic mode:** [ONE-PAGE-PANIC § when nothing compiles](../exam-day/ONE-PAGE-PANIC.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
