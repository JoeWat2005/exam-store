<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Monad: Maybe**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · [generic-combinators](./generic-combinators.md) · [io](./io.md) · [list-monad](./list-monad.md) · **maybe** · [monad-laws](./monad-laws.md) · [monaderror](./monaderror.md) · [multi-effect](./multi-effect.md) · [reader](./reader.md) · [state](./state.md) · [transformer-stack-order](./transformer-stack-order.md) · [transformers](./transformers.md) · [writer](./writer.md)
<!-- siblings:end -->






# Monad: Maybe

**Import:** built-in (`Prelude`); `Data.Maybe` for helpers.
**Type:** `data Maybe a = Nothing | Just a`
**Combines with:** Either (richer), lists (`catMaybes`), MonadError.
**Search keywords:** safe, partial, lookup, may-fail, Nothing, divide-by-zero, short-circuit, optional.

## Primitive operations

| Operation | Signature | Semantics | Pitfall |
|---|---|---|---|
| `Just`         | `a -> Maybe a`                       | success constructor | — |
| `Nothing`      | `Maybe a`                            | failure value | — |
| `(>>=)`        | `Maybe a -> (a -> Maybe b) -> Maybe b` | `Nothing >>= _ = Nothing`; short-circuits | — |
| `pure / return`| `a -> Maybe a`                       | `= Just` | — |
| `maybe`        | `b -> (a -> b) -> Maybe a -> b`      | eliminator (default + fn) | argument order: default first |
| `fromMaybe`    | `a -> Maybe a -> a`                  | extract or default | — |
| `isJust`/`isNothing` | `Maybe a -> Bool`              | predicate | — |
| `fromJust`     | `Maybe a -> a`                       | extract or `error` | **partial — crashes on Nothing** |
| `catMaybes`    | `[Maybe a] -> [a]`                   | drop the `Nothing`s | — |
| `mapMaybe`     | `(a -> Maybe b) -> [a] -> [b]`       | `catMaybes . map f` fused | — |
| `listToMaybe`  | `[a] -> Maybe a`                     | `Just head` or `Nothing` on `[]` | — |
| `maybeToList`  | `Maybe a -> [a]`                     | `[x]` or `[]` | — |

## Run functions

There is no `runMaybe`. You pattern-match `Nothing | Just x` or use `maybe d f m` / `fromMaybe d m`. The *return type* `Maybe a` itself tells the caller "may fail".

## When to reach for Maybe

- "Return `Nothing` if the input is invalid" (any negative-arg guard).
- "`safeHead`, `safeDiv`, `safeIndex`, `safeSqrt`" (problems 91–94).
- "Look up a key" — `lookup :: Eq a => a -> [(a,b)] -> Maybe b`.
- Tree delete/insert that may fail.
- Chained partial computations: "divide left-to-right; fail on any zero" (problem 95).
- Trie payload at internal nodes: `Branch (Maybe Char) Tree Tree` (Morse).

## Canonical templates

### Safe wrapper (the simplest case)
```haskell
safeHead :: [a] -> Maybe a
safeHead []    = Nothing
safeHead (x:_) = Just x

safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv x y = Just (x `div` y)
```

### Chained via `do` (the WHOLE POINT of Maybe-as-monad)
```haskell
chainDivisions :: Int -> [Int] -> Maybe Int   -- problem 95
chainDivisions x []     = Just x
chainDivisions x (d:ds) = do
  q <- safeDiv x d
  chainDivisions q ds
```

### `case`-on-recursive (equivalent, ugly)
```haskell
chainDivisions x (d:ds) = case safeDiv x d of
  Nothing -> Nothing
  Just q  -> chainDivisions q ds
```

### Two recursive Maybes combined
```haskell
evalMaybe :: Expr -> Maybe Int
evalMaybe (Val n)   = Just n
evalMaybe (Add a b) = do
  x <- evalMaybe a
  y <- evalMaybe b
  pure (x + y)
evalMaybe (Div a b) = do
  x <- evalMaybe a
  y <- evalMaybe b
  if y == 0 then Nothing else Just (x `div` y)
```

### `firstJust` / `find`-like
```haskell
firstJust :: [Maybe a] -> Maybe a            -- problem 96
firstJust []           = Nothing
firstJust (Just x : _) = Just x
firstJust (_      : xs) = firstJust xs
```

### Reimplementing `catMaybes` / `mapMaybe`
```haskell
catMaybes' :: [Maybe a] -> [a]               -- problem 97
catMaybes' []             = []
catMaybes' (Nothing : xs) = catMaybes' xs
catMaybes' (Just x  : xs) = x : catMaybes' xs

mapMaybe' :: (a -> Maybe b) -> [a] -> [b]    -- problem 98
mapMaybe' _ []     = []
mapMaybe' f (x:xs) = case f x of
  Nothing -> mapMaybe' f xs
  Just y  -> y : mapMaybe' f xs
```

## Question families this monad belongs to

- [error-handling-family](../question-families/error-handling-family.md) — safe functions (`safeDiv`, `safeIndex`) and `lookup`-style partial results
- [env-eval-family](../question-families/env-eval-family.md) — evaluator, Maybe variant

## QuickCheck traps

- `safeDiv x 0 == Nothing` (test the 0 case).
- `safeHead [] == Nothing`.
- `safeIndex xs n` where `n < 0` or `n >= length xs` must be `Nothing`.
- `chainDivisions x [0]` must be `Nothing`, NOT throw an exception.
- Empty-list cases for `firstJust`, `catMaybes'`, `mapMaybe'`.

## Pitfalls

- Using `fromJust` in solutions — the auto-marker will hit a `Nothing` and crash you. Use `do`-notation or `maybe`/`fromMaybe`.
- `do { x <- ma; pure (f x) }` is more idiomatic than `case ma of Just x -> Just (f x); Nothing -> Nothing` — and the marker often wants the do-form.
- Forgetting that division can divide a *negative* zero result: `safeDiv (-1) 0` is still `Nothing`, not `Just (-0)`.
- `maybe` arg order: `maybe DEFAULT FUNCTION mb`. Easy to flip with `fromMaybe`.

## Worked examples

- Problems 91–98 are direct drills.
- Problem 100 — `parseDigit :: Char -> Maybe Int`, then `parseNumber :: String -> Maybe Int`.
- Problem 109 — `mapMTree` with `m = Maybe` answers "tree-validate, fail on any bad cell".
- BST delete (Set 8) often uses `Maybe (BT a)`.

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md) · [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md)
**Cross-topic:** [tree × maybe](../cross-matrix/tree-x-maybe.md) · [expr × maybe](../cross-matrix/expr-x-maybe.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md)
**QuickCheck:** [maybe-either attacks](../quickcheck/maybe-either-attacks.md)
**Related (monads):** [either](./either.md) · [generic combinators](./generic-combinators.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
