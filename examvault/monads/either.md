<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Monad: Either**

<!-- siblings:start -->
> **Peers:** **either** · [generic-combinators](./generic-combinators.md) · [io](./io.md) · [list-monad](./list-monad.md) · [maybe](./maybe.md) · [monad-laws](./monad-laws.md) · [monaderror](./monaderror.md) · [multi-effect](./multi-effect.md) · [reader](./reader.md) · [state](./state.md) · [transformer-stack-order](./transformer-stack-order.md) · [transformers](./transformers.md) · [writer](./writer.md)
<!-- siblings:end -->






# Monad: Either

**Import:** built-in (`Prelude`); `Data.Either` for helpers.
**Type:** `data Either a b = Left a | Right b` — by convention, `Left` = error, `Right` = success.
**Combines with:** State (state-with-error), MonadError.
**Search keywords:** error, message, Left, Right, divide-by-zero, throw, validation, "with reason".

## Primitive operations

| Operation | Signature | Semantics | Pitfall |
|---|---|---|---|
| `Right`        | `b -> Either a b`                              | success constructor | — |
| `Left`         | `a -> Either a b`                              | failure constructor (carries `a`) | — |
| `(>>=)`        | `Either e a -> (a -> Either e b) -> Either e b` | `Left e >>= _ = Left e`; short-circuits | — |
| `pure / return`| `a -> Either e a`                              | `= Right` | — |
| `either`       | `(a -> c) -> (b -> c) -> Either a b -> c`      | eliminator | argument order: Left-fn first |
| `lefts`        | `[Either a b] -> [a]`                          | collect errors | — |
| `rights`       | `[Either a b] -> [b]`                          | collect successes | — |
| `partitionEithers` | `[Either a b] -> ([a],[b])`                | split | — |
| `fromLeft`     | `a -> Either a b -> a`                         | extract Left or default | — |
| `fromRight`    | `b -> Either a b -> b`                         | extract Right or default | — |

## Run functions

No `runEither`. You pattern-match `Left e | Right x` or `either onLeft onRight ex`. The return type itself communicates "may fail with message".

```haskell
either show id  :: Either String String -> String   -- handy
```

## When to reach for Either

- The question says "return `Left "some error"` when ...".
- An evaluator that must distinguish between *different* error kinds (e.g. divide-by-zero vs undefined variable).
- A parser that wants a diagnostic.
- Validation step that must report *which* thing failed.

## Canonical templates

### `zipEither` (problem 99) — the textbook drill
```haskell
zipEither :: [a] -> [b] -> Either String [(a, b)]
zipEither []     []     = Right []
zipEither []     _      = Left "first list shorter"
zipEither _      []     = Left "second list shorter"
zipEither (x:xs) (y:ys) = do
  rest <- zipEither xs ys
  pure ((x, y) : rest)
```

### Evaluator with typed error
```haskell
data Expr = Val Int | Add Expr Expr | Div Expr Expr | Var String

eval :: [(String, Int)] -> Expr -> Either String Int
eval _   (Val n)   = Right n
eval env (Add a b) = do
  x <- eval env a
  y <- eval env b
  pure (x + y)
eval env (Div a b) = do
  x <- eval env a
  y <- eval env b
  if y == 0 then Left "Division by zero" else Right (x `div` y)
eval env (Var s)   = case lookup s env of
  Nothing -> Left ("Undefined variable: " ++ s)
  Just n  -> Right n
```

### Multi-step parse with errors
```haskell
parseAll :: String -> Either String [Int]
parseAll "" = Right []
parseAll s  = do
  (n, rest) <- parseOne s
  ns        <- parseAll rest
  pure (n : ns)
```

### Convert `Maybe` to `Either`
```haskell
note :: e -> Maybe a -> Either e a
note _ (Just x) = Right x
note e Nothing  = Left e

-- e.g.: note "key missing" (lookup k env)
```

## Question families this monad belongs to

- [env-eval-family](../question-families/env-eval-family.md) — evaluator, Either variant (divide-by-zero, undefined var)
- [error-handling-family](../question-families/error-handling-family.md) — validation / fail-with-message chains
- [parser-family](../question-families/parser-family.md) — when not using the Parser combinator monad

## QuickCheck traps

- `zipEither [] []` must be `Right []`, NOT `Left "..."`.
- The *exact* error string is often part of the spec — copy it verbatim.
- Symmetry: `zipEither xs []` for `xs /= []` returns "second list shorter" (the OTHER list).
- Once you `Left _`, everything downstream is `Left _`. Don't write `case eval a of Right x -> ...; Left _ -> Right 0` "to recover" — it changes semantics.

## Pitfalls

- `Either e` has TWO type params; the `Monad` instance fixes `e`. You can NOT abstract over the error type and the value type independently in the instance.
- Pattern-match `Left/Right`, not `Just/Nothing`.
- `Left "x" /= Left "X"` — strings are case-sensitive; copy exactly from the problem.
- The `either` eliminator takes the *Left handler first*, not Right (confusing with `maybe`'s default-first).

## Worked examples

- Problem 99 — `zipEither`.
- Calculator with `MonadError` (see `multi-effect.md`).
- W5 problem-sheet evaluator that errors on bad inputs.

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md) · [A05 ADT translation](../archetypes/A05-adt-translation.md)
**Cross-topic:** [tree × either](../cross-matrix/tree-x-either.md) · [expr × maybe](../cross-matrix/expr-x-maybe.md)
**Question families:** [error-handling](../question-families/error-handling-family.md) · [env-eval](../question-families/env-eval-family.md)
**QuickCheck:** [maybe-either attacks](../quickcheck/maybe-either-attacks.md)
**Related (monads):** [maybe](./maybe.md) · [monaderror](./monaderror.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
