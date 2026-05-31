<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Monad: Reader**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · [generic-combinators](./generic-combinators.md) · [io](./io.md) · [list-monad](./list-monad.md) · [maybe](./maybe.md) · [monad-laws](./monad-laws.md) · [monaderror](./monaderror.md) · [multi-effect](./multi-effect.md) · **reader** · [state](./state.md) · [transformer-stack-order](./transformer-stack-order.md) · [transformers](./transformers.md) · [writer](./writer.md)
<!-- siblings:end -->






# Monad: Reader

**Import:** `import Control.Monad.Reader` — **but this is NOT in the practice-problem allowed imports**. In the exam, define Reader yourself or use the function-as-Reader instance (`(->) r`), which is in `Prelude`.
**Type:** `newtype Reader r a = Reader { runReader :: r -> a }`
**Combines with:** State, MonadError (multi-effect stacks).
**Search keywords:** environment, config, ask, asks, local, read-only, implicit parameter, function monad, `(->) r`.

## Why this file exists

Reader rarely appears in the exam as `Reader r a` directly. It DOES appear:
- as **problem 124** asking you to define the Functor/Applicative/Monad instances by hand;
- as the **function-monad** `((->) r)` in instance questions (problem 124 family);
- conceptually inside multi-effect stacks.

If your only goal is "pass an env around", a plain function `env -> result` is usually cleaner than wrapping in Reader.

## Primitive operations

| Operation | Signature | Semantics | Pitfall |
|---|---|---|---|
| `ask`   | `Reader r r`                              | get the environment           | — |
| `asks`  | `(r -> a) -> Reader r a`                  | `fmap f ask` — project from env | — |
| `local` | `(r -> r) -> Reader r a -> Reader r a`    | run sub-action with modified env | — |
| `pure x`| `a -> Reader r a`                         | constant `x`, ignores env       | — |

## Run functions

| Runner | Signature | Returns |
|---|---|---|
| `runReader` | `Reader r a -> r -> a` | the result (no log, no state) |

## When to reach for Reader

- Question 124 explicitly asks for the instances.
- An evaluator that needs a read-only environment (variable bindings) AND you don't want to pass it as a parameter.
- Sub-computations that should see a *modified* environment temporarily (`local f m`).

## Canonical templates

### Hand-rolled Reader (problem 124 — copy verbatim)
```haskell
newtype Reader r a = Reader { runReader :: r -> a }

instance Functor (Reader r) where
  -- fmap :: (a -> b) -> Reader r a -> Reader r b
  fmap g (Reader k) = Reader (\e -> g (k e))

instance Applicative (Reader r) where
  -- pure :: a -> Reader r a
  pure x = Reader (\_ -> x)
  -- (<*>) :: Reader r (a -> b) -> Reader r a -> Reader r b
  Reader rf <*> Reader rx = Reader (\e -> rf e (rx e))

instance Monad (Reader r) where
  -- return = pure       (default — don't redefine)
  -- (>>=) :: Reader r a -> (a -> Reader r b) -> Reader r b
  Reader rk >>= f = Reader (\e -> runReader (f (rk e)) e)
```

### Function-as-Reader (no newtype)
```haskell
-- Prelude already has these instances for the function type ((->) r)
instance Functor ((->) r) where
  fmap = (.)

instance Applicative ((->) r) where
  pure  = const
  rf <*> rx = \e -> rf e (rx e)

instance Monad ((->) r) where
  return  = const
  m >>= f = \e -> f (m e) e
```

### `ask` and `asks`
```haskell
ask :: Reader r r
ask = Reader (\e -> e)

asks :: (r -> a) -> Reader r a
asks f = Reader f
```

### Reader-style env evaluator
```haskell
type Env = [(String, Int)]
data Expr = Val Int | Var String | Add Expr Expr

eval :: Expr -> Reader Env Int
eval (Val n)   = pure n
eval (Var s)   = do
  env <- ask
  case lookup s env of
    Just v  -> pure v
    Nothing -> pure 0
eval (Add a b) = do
  x <- eval a
  y <- eval b
  pure (x + y)

-- runReader (eval (Add (Var "x") (Val 1))) [("x", 41)] == 42
```

### `local` — running a sub-computation in a changed env
```haskell
addBinding :: (String, Int) -> Reader Env a -> Reader Env a
addBinding b = local (b :)
```

## Question families this monad belongs to

- [env-eval-family](../question-families/env-eval-family.md) — env-as-context evaluators (Reader-style lookup, `local` scoping)
- [functor-instance-family](../question-families/functor-instance-family.md) — instance-writing for the `(->) r` / Reader functor

## QuickCheck traps

- `pure x` must ignore the env: `runReader (pure 42) anyEnv == 42`.
- `ask >>= pure == ask` (return is right-identity).
- For the function-monad: `(m >>= f) e == f (m e) e` — easy to type-misalign.

## Pitfalls

- `Reader r a` — `r` is FIRST type param; `Monad (Reader r)` fixes `r`.
- The Monad instance is for `Reader r`, NOT `Reader`. You can't write `instance Monad Reader where ...`.
- `Control.Monad.Reader` is **not in the practice-allowed-imports list**, so don't write `import Control.Monad.Reader`. Roll your own newtype.
- If you only need a function `env -> a`, you don't really need the Reader newtype — just pass the env. Reader pays off only when you chain many env-dependent computations.

## Worked examples

- Problem 124 — write the three instances.
- Optional: turn a `Env -> Maybe Value` evaluator into Reader-style.

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md)
**Cross-topic:** [tree × reader](../cross-matrix/tree-x-reader.md)
**Question families:** [env-eval](../question-families/env-eval-family.md)
**Related (monads):** [multi effect](./multi-effect.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
