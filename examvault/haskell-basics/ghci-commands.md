<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **GHCi commands**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · **ghci-commands** · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# GHCi commands

## What this is
GHCi is the interactive Haskell REPL. Most exam testing happens inside it: load a file, query a type, evaluate an expression, reload after edits.

## Starting and exiting

| Command | What it does |
|---|---|
| `ghci` | Start GHCi with no file loaded. |
| `ghci MyFile.hs` | Start GHCi and load `MyFile.hs` immediately. |
| `:quit` / `:q` | Exit GHCi (also `Ctrl+D`). |

## Loading and reloading files

| Command | Shorthand | What it does |
|---|---|---|
| `:load MyFile.hs` | `:l MyFile.hs` | Load a source file. Replaces any previously loaded modules. |
| `:reload` | `:r` | Re-read all loaded files. Run this after **every** edit — GHCi will not pick up changes otherwise. |
| `:add Foo.hs` | — | Load an additional file into the session. |
| `:cd /path/dir` | — | Change working directory. Useful if you started GHCi in the wrong folder. |

**Most common exam mistake:** edit a file, run a test, see the old answer because you forgot `:r`. Train the muscle: edit → save → `:r` → test.

## Inspecting types and definitions

| Command | What it does |
|---|---|
| `:type expr` / `:t expr` | Show the inferred type. Doesn't evaluate. |
| `:info Name` / `:i Name` | Show the type, where it's defined, and any class instances. |
| `:browse Module` | List everything `Module` exports. |
| `:kind T` / `:k T` | Show the kind of a type constructor (`* -> *` etc.). |

```text
ghci> :t map
map :: (a -> b) -> [a] -> [b]

ghci> :t \x -> x + 1
\x -> x + 1 :: Num a => a -> a

ghci> :i Maybe
type Maybe :: * -> *
data Maybe a = Nothing | Just a
        -- Defined in `GHC.Maybe'
instance Applicative Maybe -- Defined in `GHC.Base'
instance Functor Maybe     -- Defined in `GHC.Base'
instance Monad Maybe       -- Defined in `GHC.Base'
-- ...
```

`:t` is your fastest sanity check: type-error feedback in one line, before you waste minutes on a definition that returns the wrong shape.

## Evaluating expressions

Plain expressions just run:

```text
ghci> 2 + 2
4
ghci> map (+1) [1,2,3]
[2,3,4]
ghci> reverse "hello"
"olleh"
```

To bind a name in the session, use `let` (no `in`):

```text
ghci> let xs = [1..10]
ghci> sum xs
55
ghci> let double n = n * 2
ghci> double 21
42
```

## Multi-line input

Wrap a multi-line block with `:{` … `:}`:

```text
ghci> :{
ghci| let f 0 = 1
ghci|     f n = n * f (n - 1)
ghci| :}
ghci> f 5
120
```

Useful for defining `data` declarations and multi-equation functions interactively without going back to the source file.

## Useful `:set` flags

| Setting | Effect |
|---|---|
| `:set +s` | Print time + memory after every evaluation. |
| `:set -Wall` | Turn on **all** warnings — catches missing patterns, unused bindings, shadowing. |
| `:set -Wno-x-y-z` | Turn off a specific warning. |
| `:set prompt "λ> "` | Change the prompt (cosmetic). |
| `:unset +s` | Turn timing off. |

Persistent settings: put them in `~/.ghci`.

```text
ghci> :set +s
ghci> sum [1..1000000]
500000500000
(0.05 secs, 88,063,824 bytes)
```

## Language extensions

The assignment templates use `{-# LANGUAGE Safe #-}` and `GHC2024`. You usually don't need to set extensions interactively, but if you do:

```text
ghci> :set -XScopedTypeVariables
```

Common exam-relevant extensions:
- `-XSafe` — same as the `{-# LANGUAGE Safe #-}` pragma. Forbids `unsafePerformIO`, custom `Show` via FFI, etc. Don't disable in assignments.
- `-XScopedTypeVariables` — lets a `forall a.` in a signature scope into the body. Rarely needed at this level.
- `-XGHC2024` — the default language set the assignments compile against. Already on.

## Inspecting imports

```text
ghci> :show imports
import Prelude            -- implicit
import Data.List
ghci> :show modules
MyFile     ( MyFile.hs, interpreted )
```

If a function isn't found, `:show imports` reveals whether you imported the wrong module.

## Help

```text
ghci> :?       -- list all GHCi commands
ghci> :help    -- same thing
```

## Common GHCi mistakes

- **Forgot to `:r`.** Edit was saved, but GHCi still has the old module. Reload.
- **Loaded the wrong file.** Two files in the same folder with overlapping definitions — `:show modules` to confirm.
- **Used `let x = 5 in expr`** at the prompt. At the top level inside GHCi, `let` has no `in`.
- **Imported a forbidden module** to test something, then forgot to remove it before submitting. The marker runs with `-XSafe` and only the allowed imports (see [allowed-builtins](./allowed-builtins.md)).
- **Multi-line block without `:{ :}`.** Pasting a multi-line `do` block usually works because of GHCi's leading-whitespace heuristic, but for multi-equation definitions you must wrap.
- **Trying to `print` something without a `Show` instance.** Add `deriving Show` to the ADT in the file, save, `:r`.

## Tiny test-flow recipe

```text
$ ghci MyFile.hs
ghci> :t myFunction              -- does the signature match the spec?
ghci> myFunction sampleInput1     -- run the golden-path test
ghci> myFunction edgeCase         -- empty / singleton / Nothing / etc.
ghci> :r                          -- after every edit
```

## Exam use

GHCi is the entire submission loop on vLab. Load → test → fix → `:r` → re-test → submit. There is no other test runner you need to memorise; the marker is automatic and runs server-side.

If `:r` shows red text — the file does **not** compile — stop and fix that first. The marker awards 0 marks for a non-compiling file even if 4/5 functions are correct.

## See also

**Testing recipes:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md)
**When GHC barks:** [ghc-error-decoder](./ghc-error-decoder.md) — every red-text error → translation → fix
**Allowed imports:** [allowed-builtins](./allowed-builtins.md) · [imports-pitfalls](../pitfalls/imports-pitfalls.md)
**Safe pragma:** [safe-haskell](./safe-haskell.md) · [P-011 Safe pragma removed](../pitfalls/HIGH-severity.md#p-011)
**vLab setup helper:** [`../scripts/vlab-setup.sh`](../scripts/vlab-setup.sh)
**Exam workflow:** [IN-EXAM-WORKFLOW](../exam-day/IN-EXAM-WORKFLOW.md) · [LAST-HOUR-CHECKLIST](../exam-day/LAST-HOUR-CHECKLIST.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
