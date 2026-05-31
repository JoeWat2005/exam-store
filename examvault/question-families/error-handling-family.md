<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: error-handling**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · **error-handling** · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: error-handling

**Archetype:** A15 (Maybe / Either / MonadError patterns)   |   **Stars:** ⭐⭐⭐   |   **Course week(s):** 8
**Search keywords:** Maybe, Either, safeHead, safeDiv, safeSqrt, safeIndex, chainDivisions, mapMaybe, MonadError

## Generator template
```haskell
-- The seed: a partial operation, returning Maybe/Either to indicate failure.
seed :: Input -> Maybe Output
seed bad   = Nothing
seed good  = Just (result good)
```

The family includes three failure paradigms:
- **`Maybe`** — failure is binary, no error info.
- **`Either e`** — failure has an error message (Left).
- **`MonadError e m`** — throwError / catchError for richer recovery.

## Mutations (the examiner picks one)

### Mutation 1 — safeHead (= problem 91)
**Sig:** `safeHead :: [a] -> Maybe a`
**Solution:**
```haskell
safeHead :: [a] -> Maybe a
safeHead []    = Nothing
safeHead (x:_) = Just x
```
**QC trap:** `safeHead [] == Nothing`, `safeHead [x] == Just x`. Trivial — gateway to the family.

### Mutation 2 — safeDiv (= problem 92)
**Sig:** `safeDiv :: Int -> Int -> Maybe Int`
**Solution:**
```haskell
safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv a b = Just (a `div` b)
```
**QC trap:** Only divisor 0 fails. Negative divisors are fine.

### Mutation 3 — safeSqrt (= problem 93)
**Sig:** `safeSqrt :: Double -> Maybe Double`
**Solution:**
```haskell
safeSqrt :: Double -> Maybe Double
safeSqrt x | x < 0     = Nothing
           | otherwise = Just (sqrt x)
```
**QC trap:** `safeSqrt 0 == Just 0`. The boundary case is OK.

### Mutation 4 — safeIndex (= problem 94)
**Sig:** `safeIndex :: [a] -> Int -> Maybe a`
**Solution:**
```haskell
safeIndex :: [a] -> Int -> Maybe a
safeIndex xs n
  | n < 0 || n >= length xs = Nothing
  | otherwise               = Just (xs !! n)
```
**QC trap:** `length` traverses the whole list — O(n). For a more idiomatic version:
```haskell
safeIndex []     _ = Nothing
safeIndex (x:_)  0 = Just x
safeIndex (_:xs) n | n > 0 = safeIndex xs (n - 1)
                   | otherwise = Nothing
```

### Mutation 5 — chainDivisions (= problem 95)
**Spec:** Use `do`-notation on Maybe to divide repeatedly; first zero breaks the chain.
**Sig:** `chainDivisions :: Int -> [Int] -> Maybe Int`
**Solution:**
```haskell
chainDivisions :: Int -> [Int] -> Maybe Int
chainDivisions a []     = Just a
chainDivisions a (d:ds) = do
  q <- safeDiv a d
  chainDivisions q ds
```
**QC trap:** `chainDivisions 100 [] == Just 100`. `chainDivisions 100 [0, 5] == Nothing` (first divisor is 0, no further computation).

### Mutation 6 — firstJust (= problem 96)
**Sig:** `firstJust :: [Maybe a] -> Maybe a`
**Solution:**
```haskell
firstJust :: [Maybe a] -> Maybe a
firstJust []              = Nothing
firstJust (Just x : _)    = Just x
firstJust (Nothing : ys)  = firstJust ys
```
**QC trap:** Returns the *first* Just, not the last. Empty list returns Nothing.

### Mutation 7 — catMaybes' / mapMaybe' (= problems 97, 98)
**Sig:** `catMaybes' :: [Maybe a] -> [a]`
**Solution:**
```haskell
catMaybes' :: [Maybe a] -> [a]
catMaybes' []                = []
catMaybes' (Just x  : xs)    = x : catMaybes' xs
catMaybes' (Nothing : xs)    = catMaybes' xs

mapMaybe' :: (a -> Maybe b) -> [a] -> [b]
mapMaybe' _ []     = []
mapMaybe' f (x:xs) = case f x of
                       Just y  -> y : mapMaybe' f xs
                       Nothing -> mapMaybe' f xs
```
**QC trap:** `mapMaybe' f xs == catMaybes' (map f xs)`. Equivalent under the law.

### Mutation 8 — zipEither (Either-typed error) (= problem 99)
**Sig:** `zipEither :: [a] -> [b] -> Either String [(a,b)]`
**Solution:**
```haskell
zipEither :: [a] -> [b] -> Either String [(a,b)]
zipEither [] []         = Right []
zipEither [] _          = Left "first list shorter"
zipEither _ []          = Left "second list shorter"
zipEither (x:xs) (y:ys) = case zipEither xs ys of
                            Right rest -> Right ((x,y) : rest)
                            Left e     -> Left e
```
**QC trap:** Error message depends on *which* list ran out. With monadic `do` notation:
```haskell
zipEither (x:xs) (y:ys) = do
  rest <- zipEither xs ys
  return ((x,y) : rest)
```
This propagates the error automatically.

### Mutation 9 — parseDigit / parseNumber (= problem 100)
**Sig:** `parseDigit :: Char -> Maybe Int` and `parseNumber :: String -> Maybe Int`
**Solution:**
```haskell
import Data.Char (isDigit, digitToInt)

parseDigit :: Char -> Maybe Int
parseDigit c | isDigit c = Just (digitToInt c)
             | otherwise = Nothing

parseNumber :: String -> Maybe Int
parseNumber [] = Nothing
parseNumber cs = go 0 cs
  where
    go acc []     = Just acc
    go acc (c:rest) = do
      d <- parseDigit c
      go (acc * 10 + d) rest
```
**QC trap:** Empty string returns Nothing (not Just 0). `parseNumber "12a3"` returns Nothing as soon as 'a' fails.

### Mutation 10 — throwError variant (MonadError)
**Spec:** Use richer error handling than bare `Maybe`.
**Sig:** `eval :: Env -> Expr -> Either String Int`

> **WARNING - not an allowed import:** `Control.Monad.Except` (for `MonadError`, `throwError`, `catchError`, `ExceptT`) is **NOT** on the exam whitelist — importing it scores **0**. There is no whitelisted error/except module. Use the **concrete `Either String`** rewrite below (`Either e` is already a `Monad`, so `do`/`return` work and `Left`/`Right` replace `throwError`/`return`). Only write the `MonadError` polymorphic version if the question's own Types module provides it.

**Primary (allowed) — concrete `Either String`** (`Left` is `throwError`, `Right`/`return` succeed):
```haskell
eval :: Env -> Expr -> Either String Int
eval _   (Lit n)   = Right n
eval env (Var x)   = case lookup x env of
                       Just v  -> Right v
                       Nothing -> Left ("undefined: " ++ x)   -- = throwError
eval env (Add a b) = do v1 <- eval env a
                        v2 <- eval env b
                        return (v1 + v2)
```
To *catch* (the `catchError` analogue) on concrete `Either`, just pattern-match: `case eval env e of Left _ -> recover; Right v -> use v`.

**Forbidden form (`Control.Monad.Except`) — for recognition only; scores 0 unless the Types module supplies it:**
```haskell
import Control.Monad.Except   -- WARNING: NOT whitelisted — scores 0

eval :: MonadError String m => Env -> Expr -> m Int
eval _   (Lit n)   = return n
eval env (Var x)   = case lookup x env of
                       Just v  -> return v
                       Nothing -> throwError ("undefined: " ++ x)
eval env (Add a b) = do v1 <- eval env a
                        v2 <- eval env b
                        return (v1 + v2)
```
**QC trap:** Same logic as `Either`; the polymorphic `MonadError` version works in *any* such monad (useful for transformer stacks) — but it is **not exam-legal** without the import. The concrete `Either String` version is the safe answer.

## Hidden-predicate mutations
- "Maybe → Either" upgrade: just add `Left e` arguments. Often the spec gives you Maybe and asks you to convert.
- "Catch and recover": wrap with `catchError` in MonadError contexts.

## Accumulator-style alternative
For chains:
```haskell
chainDivisionsAcc :: Int -> [Int] -> Maybe Int
chainDivisionsAcc = foldM safeDiv
```
This is the canonical `foldM` form — once you see it, you remember it.

## Fold-style alternative
```haskell
firstJustFold = foldr (\m acc -> case m of Just _ -> m; Nothing -> acc) Nothing
catMaybesFold = foldr (\m acc -> case m of Just x -> x : acc; Nothing -> acc) []
```
Both clean folds.

## Cross-family combinations
- this family + `monad-combinator-family.md`: `sequence :: [Maybe a] -> Maybe [a]`.
- this family + `state-game-family.md`: StateT over Maybe for "game might be invalid".
- this family + `writer-trace-family.md`: log failed operations.
- this family + `env-eval-family.md`: error reporting in interpreters.

## QuickCheck universal attacks
- **`fmap Just == id <$> pure`** — sanity.
- **Empty/zero inputs:** safeHead [], safeDiv x 0, etc.
- **Composition:** `safeDiv x y >>= safeDiv z` chains.
- **Identity:** `Just x >>= f == f x` (monad law).
- **Annihilation:** `Nothing >>= f == Nothing` for any f.
- **Either vs Maybe:** `maybeToEither e == either Left Right . fromMaybe (Left e)`.

## Pitfalls (per mutation)
- M1: pattern matching `(x:_)` vs `[x]` — different semantics.
- M2: returning Nothing for negative divisors when only zero should fail.
- M3: `<` 0 vs `<=` 0 (zero is fine).
- M4: using `length` (O(n)) when recursive is cleaner.
- M5: not handling the empty-divisors case.
- M6: returning the last Just instead of first.
- M7: using `map` instead of recursive concatenation.
- M8: returning Right [] when one list is non-empty.
- M9: returning Just 0 for empty string.
- M10: forgetting MonadError constraint.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — safeEvalEither (Either with structured error type)

**Spec:** Evaluate an arithmetic Expr, but instead of `Maybe Int` return `Either EvalError Int` with a typed error for unknown vars, division by zero, etc.

**Type sig:** `data EvalError = UnknownVar String | DivByZero deriving (Eq, Show)
safeEvalE :: Env -> Expr -> Either EvalError Int`

```haskell
data EvalError = UnknownVar String | DivByZero deriving (Eq, Show)

safeEvalE :: Env -> Expr -> Either EvalError Int
safeEvalE _   (Num n)   = Right n
safeEvalE env (Var x)   = maybe (Left (UnknownVar x)) Right (lookup x env)
safeEvalE env (Add l r) = (+) <$> safeEvalE env l <*> safeEvalE env r
safeEvalE env (Div l r) = do
  vl <- safeEvalE env l
  vr <- safeEvalE env r
  if vr == 0 then Left DivByZero else Right (vl `div` vr)
```

**What changes vs seed:** Effect stack changes from `Maybe Int` to `Either EvalError Int`. Same overall shape but errors carry structured information — supports diagnostics.

**QC trap:** `maybe (Left …) Right (lookup …)` is the right idiom — `fromMaybe undefined` will crash on unknown vars. Distinguish `UnknownVar` (lookup failure) from `DivByZero` (semantic failure).

### Mutation 12 — collectErrors (accumulate ALL errors, vs `sequence`'s short-circuit)

**Spec:** Given `[Either e a]`, return `Right` of all the successes **only if every element succeeded**; otherwise return `Left` of the list of **all** errors encountered (not just the first). This is the *validation* / accumulate-all dial-flip of `sequence`.

**Type sig:** `collectErrors :: [Either e a] -> Either [e] [a]`

```haskell
collectErrors :: [Either e a] -> Either [e] [a]
collectErrors xs = case [e | Left e <- xs] of
                     [] -> Right [a | Right a <- xs]
                     es -> Left es
```

**What changes vs seed:** Unlike `sequence :: [Either e a] -> Either e [a]`, which **stops at the first `Left`** and returns that single error, `collectErrors` scans the whole list and gathers **every** `Left` into `Left [e]`. Same short-circuit-vs-accumulate distinction as `Applicative`-validation libraries — but hand-rolled with two list comprehensions, no extra imports.

**QC trap:** Contrast against `sequence`:
- `sequence  [Left "a", Right 1, Left "b"] == Left "a"`  — first error only, rest of the list ignored.
- `collectErrors [Left "a", Right 1, Left "b"] == Left ["a","b"]`  — every error.
- On all-success they agree on the payload: `collectErrors [Right 1, Right 2] == Right [1,2]` (cf. `sequence … == Right [1,2]`).
The result type differs too: `Either e [a]` (sequence) vs `Either [e] [a]` (collectErrors).

## See also

**Primary archetype:** [A08 env eval / A05 ADT translation](../archetypes/A08-env-eval.md)
**Sibling families:** [env-eval](./env-eval-family.md)
**Cross-topic:** [expr × maybe](../cross-matrix/expr-x-maybe.md) · [tree × either](../cross-matrix/tree-x-either.md)
**QuickCheck:** [maybe-either attacks](../quickcheck/maybe-either-attacks.md) · [interp attacks](../quickcheck/interp-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
