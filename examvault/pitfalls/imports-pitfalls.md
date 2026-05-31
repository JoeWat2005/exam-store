<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [pitfalls](./README.md) · **Pitfalls — Imports + Safe Haskell**

<!-- siblings:start -->
> **Peers:** [HIGH-severity](./HIGH-severity.md) · [LOW-severity](./LOW-severity.md) · [MEDIUM-severity](./MEDIUM-severity.md) · **imports-pitfalls** · [per-topic-pitfalls](./per-topic-pitfalls.md) · [signature-pitfalls](./signature-pitfalls.md)
<!-- siblings:end -->






# Pitfalls — Imports + Safe Haskell

> The exam enforces a closed import set AND `{-# LANGUAGE Safe #-}`. Both must hold simultaneously. Most students lose marks here either by reaching for a forbidden module (Reader, Except, Data.Map) or by accidentally deleting the Safe pragma.

This file is the single source of truth for "what may I import" and "what may I use".

---

## The allowed-imports list (verbatim from `CLAUDE.md` and the Practice spec)

```haskell
-- IMPLICIT (always there)
Prelude

-- EXPLICITLY ALLOWED
Data.List
Data.Char
Data.Maybe
Control.Monad
Control.Monad.State
Control.Monad.Writer

-- AND
Types       -- the provided per-exam types module
```

That's it. **Nothing else.**

If the question's `package.yaml` or `Types.hs` lists additional dependencies (e.g. `QuickCheck`, `marking-core`, `deepseq`, `containers`), those are for the MARKER, not for you. Your answer file imports only the above.

---

## Common forbidden imports (and what to use instead)

### `Control.Monad.Reader`
Forbidden. The course uses **plain function arguments** for read-only configuration.
```haskell
-- WRONG
import Control.Monad.Reader
eval :: Expr -> Reader Env Int
eval (Var x) = do env <- ask; ...

-- RIGHT (env is a plain argument)
eval :: Env -> Expr -> Int
eval env (Var x) = ...
```

### `Control.Monad.Except`, `Control.Monad.Error.Class`
Forbidden. Use **`Either e`** explicitly.
```haskell
-- WRONG
import Control.Monad.Except
eval :: Expr -> Either String Int          -- the type is fine, but the *imports* aren't
eval (Div a b) = do x <- eval a; y <- eval b
                    if y == 0 then throwError "/0" else return (x `div` y)
                    --        ^ requires Control.Monad.Except

-- RIGHT (use Left/Right directly)
eval :: Expr -> Either String Int
eval (Div a b) = do x <- eval a; y <- eval b
                    if y == 0 then Left "/0" else Right (x `div` y)
```

If the question DOES allow MonadError (multi-effect interpreter only — and it's in `Types.hs` if so), then use it. Otherwise, plain `Either`.

### `Data.Map`, `Data.Set`, `Data.Sequence`, `Data.IntMap`, `Data.Array`
All forbidden. Use **association lists** (`[(k, v)]`) and `lookup`.
```haskell
-- WRONG
import qualified Data.Map as M
type Env = M.Map String Int

-- RIGHT
type Env = [(String, Int)]
-- lookup :: Eq a => a -> [(a, b)] -> Maybe b is in Prelude
```

### `Data.IORef`, `Data.STRef`, `System.IO`, anything `IO`-flavoured
Forbidden (and Safe-incompatible). The exam questions are pure or use State/Writer.

### `Test.QuickCheck`, `Test.Hspec`, anything testing-related
Forbidden in your answer file. The marker has its own QuickCheck instance.

### `Debug.Trace`
Forbidden. Use comments / `error "stop"` strategically while developing.

### `System.Win32`, `System.Process`, `Foreign.*`, FFI
Forbidden. Safe Haskell rejects all of these.

### `unsafePerformIO`, `unsafeCoerce`
Forbidden by Safe.

### `qualified` imports of anything not in the allowed list
Forbidden. Even if you `import qualified Data.Map as M`, the import itself fails.

---

## The IDE-auto-import garbage trap

Common ones IDEs ADD on autocomplete that you must DELETE:

```haskell
import System.Win32 (COORD(xPos))     -- VS Code on Windows
import Data.Sequence (Seq(Empty))     -- 'Empty' conflicts with YOUR own ctor!
import Data.Tree (flatten)            -- conflicts with YOUR own flatten
import qualified Data.Map.Strict as M
import GHC.Generics                   -- accidental
```

**Discipline:** after writing each function, scan the imports. If anything's there beyond the allowed list, DELETE.

---

## `{-# LANGUAGE Safe #-}` — what it forbids

`Safe` Haskell rejects modules that use any of:
- `unsafePerformIO`, `unsafeCoerce`, `unsafeIOToST` — completely banned
- Foreign Function Interface (`foreign import …`) — banned
- `Template Haskell` (`$(…)`, splices) — banned
- `GeneralizedNewtypeDeriving` (in some GHC versions, fully banned; in others, restricted)
- `DeriveAnyClass` with non-Safe classes
- Importing any module marked `Unsafe` or unannotated
- `OverlappingInstances`, `IncoherentInstances`
- `RankNTypes` with impredicative polymorphism in certain forms

`presubmit.sh` enforces `Safe` via `ghc -XSafe -XNoGeneralizedNewtypeDeriving -fno-code MockTest.hs`. **The `-XNoGeneralizedNewtypeDeriving` is explicit because Safe alone would still allow it in some configurations.**

### Specific Safe-Haskell traps you might hit

- **`deriving Functor`** requires `{-# LANGUAGE DeriveFunctor #-}` — and the combination of Safe + DeriveFunctor was flagged unsafe in older GHCs. **Write Functor instances by hand.**
- **`deriving Show`** is fine (it's built-in for tractable cases).
- **`deriving Eq, Ord`** are fine.
- **Lambda-case** (`\case`) needs `{-# LANGUAGE LambdaCase #-}` — but you don't need it; use `\x -> case x of`.
- **Pattern synonyms, `Generic`, `TypeFamilies`** — all unnecessary; don't reach for them.

---

## How to test imports compile under `-XSafe`

```bash
ghc -XSafe -XNoGeneralizedNewtypeDeriving -fno-code MockTest.hs
```

Expected output: `[1 of 2] Compiling Types` then `[2 of 2] Compiling MockTest` with no errors and no warnings about safety.

If it says:
- **"Could not find module 'X'"** — your import isn't in the allowed list, OR you mistyped.
- **"X.hs:N:M: Module is not Safe-Inferred"** — you imported something Safe rejects (`Data.Map`, `System.IO`, etc.).
- **"Safe Haskell rejects: deriving Functor"** — see above; remove deriving, write instance by hand.
- **"Pattern match(es) are non-exhaustive"** — this is a warning, but `-fwarn-incomplete-patterns` is in the OPTIONS_GHC line. Fix it.

---

## The full presubmit script behaviour (`presubmit.sh AssignmentN`)

The script does three things:
1. Compile plain: `ghc -fno-code AssignmentN.hs` — must succeed.
2. Compile under Safe: `ghc -XSafe -XNoGeneralizedNewtypeDeriving -fno-code AssignmentN.hs` — must succeed.
3. Regenerate `Signatures.hs` and verify EVERY function in the template has a matching signature in your file.

If any of these fail, the script exits non-zero. **Always check the exit code:**

```bash
./presubmit.sh MockTest
echo $?      # must be 0
# or, combined:
./presubmit.sh MockTest && echo OK || echo FAIL
```

`presubmit.sh` is POSIX sh. On Windows, use Git Bash or WSL. On vLab, it Just Works.

---

## Local quick-check (without presubmit)

If you don't have `presubmit.sh` (or want a faster cycle):

```bash
# 1. plain compile
ghc -fno-code MockTest.hs

# 2. Safe compile
ghc -XSafe -XNoGeneralizedNewtypeDeriving -fno-code MockTest.hs

# 3. ghci sanity
echo ':type isNBranching' | ghci MockTest.hs
# verify the type printed matches the template
```

---

## When the question says `import X` is OK

If `MockTest-Template.hs` (or whatever the per-exam template is) already imports `Data.List`, you're fine to use it. Don't ADD imports — but the template's existing imports are pre-blessed.

The Mock template imports:
```haskell
import Types
import Data.List
```

That's it. `Types` brings in `Control.Monad` and `Control.Monad.State` transitively via:
```haskell
module Types (module Types, module Control.Monad, module Control.Monad.State) where
```

So in your answer, you have `Data.List`, `Control.Monad`, `Control.Monad.State` available WITHOUT additional imports. You may add `Data.Char`, `Data.Maybe`, `Control.Monad.Writer` if needed — but only if you ACTUALLY use them.

---

## Pitfall cross-references

- HIGH P-003 · import outside allowed set
- HIGH P-004 · `Reader` / `Except` forbidden
- HIGH P-010 · `deriving Functor` + Safe conflict
- HIGH P-011 · Safe pragma deleted
- HIGH P-026 · Safe pragma blocks tests

---

## See also

- `signature-pitfalls.md` — the type signature contract
- [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) 60-second checklist
- `archetypes/A##.md` — every archetype tells you which imports it needs
- `examvault/meta/COURSE-COVERAGE.md` — what the course actually allows

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
