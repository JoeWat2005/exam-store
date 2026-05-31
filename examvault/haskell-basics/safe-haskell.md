<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Safe Haskell**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · **safe-haskell** · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->





# Safe Haskell

## What this is
Every assignment + Mock template begins with `{-# LANGUAGE NoGeneralizedNewtypeDeriving, Safe #-}`. The `Safe` pragma is GHC's "this module uses no unsafe escape hatches" guarantee. If you accidentally use a forbidden feature, GHC refuses to compile — and the marker scores **0** on that file. This page is the rule list.

## Mental model
`Safe` is a contract: "I, this module, promise to be type-safe, referentially transparent, and module-system-respecting." GHC enforces the promise by **rejecting any feature that could violate it**. The marker uses `Safe` to ensure your code can't reach outside the sandbox.

## The pragma line — DO NOT TOUCH

```haskell
{-# LANGUAGE NoGeneralizedNewtypeDeriving, Safe #-}
module MockTest ( ... ) where
```

[P-011](../pitfalls/HIGH-severity.md#p-011) — deleting or changing this line is an automatic zero. The presubmit script checks it.
[P-026](../pitfalls/HIGH-severity.md#p-026) — same.

## What `Safe` forbids

| Feature | Why forbidden | Workaround |
|---|---|---|
| `import System.IO.Unsafe` (`unsafePerformIO`) | Lets you fake purity. Breaks referential transparency. | Don't reach for IO at all in pure functions. |
| `import Foreign.*` (FFI) | Calls C — outside Haskell's type system. | Not needed for this course. |
| `import GHC.Exts` (primitives) | Exposes runtime internals. | Stick to high-level types. |
| `{-# LANGUAGE GeneralizedNewtypeDeriving #-}` | Can derive `Monad` for newtypes around non-monads — caller might assume laws hold when they don't. | Hand-write the instance. |
| `deriving Functor` | **NOT actually forbidden by Safe** on modern GHC — `DeriveFunctor` is Safe-compatible. The catch: it needs the `DeriveFunctor` pragma in your file, and the template may not enable it, so a bare `deriving Functor` fails to compile. The course also wants the instance by hand. | Hand-write `instance Functor T where fmap …`. |
| `{-# LANGUAGE TemplateHaskell #-}` | Compile-time code generation breaks the safety surface. | Not needed. |
| Imports of `Trustworthy`-marked modules **not on the allowed list** | If a module is `Trustworthy`, the *module author* vouched for safety. The marker only trusts the 7-module allowed list. | Use only `Prelude`, `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`. |

## What `Safe` allows — your full toolkit

- Any pure function in `Prelude`.
- Pattern matching, guards, `let`, `where`, `case`, list comprehensions, lambdas.
- All standard ADTs, classes, deriving `Eq` / `Ord` / `Show` / `Read`.
- The allowed monads (`Maybe`, `Either`, `State`, `Writer`, list, `IO`).
- Writing your own `Functor` / `Applicative` / `Monad` / `Eq` / `Ord` / `Show` instances **by hand**.

## The forbidden imports list

If your import line is anything other than these:

```haskell
import Data.List         -- sort, nub, foldl', transpose, ...
import Data.Char         -- isDigit, toUpper, ord, chr, ...
import Data.Maybe        -- fromMaybe, mapMaybe, catMaybes, ...
import Control.Monad     -- when, unless, forM, replicateM, ...
import Control.Monad.State    -- get, put, modify, evalState, ...
import Control.Monad.Writer   -- tell, runWriter, execWriter, ...
import Types             -- the question's own ADTs
```

…then either it's forbidden under `Safe`, not on the allowed list, or both. See [P-003](../pitfalls/HIGH-severity.md#p-003) and [P-004](../pitfalls/HIGH-severity.md#p-004).

**Common forbidden imports** students reach for and get burned by:

- `Data.Map` / `Data.Set` (from `containers` — not on the allowed list). Use assoc-lists + `lookup`.
- `Control.Monad.Reader` / `Control.Monad.Except`. Pass extra args manually for Reader. Use `Either` directly for Except.
- `Text.Read` (for `readMaybe`). Use a hand-rolled parser or pattern-match on `reads`.
- `Data.IORef`, `Data.STRef`. State monad covers what you need.

## Common student errors

- **Deleting the pragma** "to debug" then forgetting to restore it ([P-011](../pitfalls/HIGH-severity.md#p-011)).
- **`deriving Functor`** in a tree instance — `DeriveFunctor` needs its pragma in your file; Safe permits it on modern GHC, but the template may not enable `DeriveFunctor` and the course wants the instance by hand, so a bare `deriving Functor` fails to compile ([P-010](../pitfalls/HIGH-severity.md#p-010)). Write the instance manually:
  ```haskell
  instance Functor BT where
    fmap _ Empty        = Empty
    fmap f (Fork x l r) = Fork (f x) (fmap f l) (fmap f r)
  ```
- **Adding `import Data.Map`** then realising too late.
- **Using `newtype Mine = Mine Int deriving Monad`** — `GeneralizedNewtypeDeriving` is explicitly disabled by the pragma.

## How to verify locally

```bash
# Will tell you the moment you compile if something is forbidden:
ghc -XSafe MockTest.hs
# OR
stack ghc -- -XSafe MockTest.hs

# The presubmit script does this for you:
./presubmit.sh MockTest
```

## Exam use
- **Start every solution by COPY-PASTING the template's pragma line**. Never retype it.
- If GHC says `Safe Haskell could not be inferred`, you've added a forbidden feature — back it out.
- Before you submit, re-check the pragma is still there and unchanged.

## Search keywords
Safe · LANGUAGE Safe · -XSafe · NoGeneralizedNewtypeDeriving · DeriveFunctor · Trustworthy · forbidden imports · marker rejection · presubmit

## See also
**Pitfalls:** [P-003 forbidden import](../pitfalls/HIGH-severity.md#p-003) · [P-004 forbidden monad import](../pitfalls/HIGH-severity.md#p-004) · [P-010 deriving Functor needs the pragma](../pitfalls/HIGH-severity.md#p-010) · [P-011 pragma deleted](../pitfalls/HIGH-severity.md#p-011) · [P-026 missing Safe pragma](../pitfalls/HIGH-severity.md#p-026)
**Other:** [imports-pitfalls](../pitfalls/imports-pitfalls.md) · [signature-pitfalls](../pitfalls/signature-pitfalls.md)
**Basics:** [type-signatures](./type-signatures.md) · [deriving](./deriving.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
