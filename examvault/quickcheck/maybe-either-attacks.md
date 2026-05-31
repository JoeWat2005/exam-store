<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: Maybe & Either**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · **maybe-either** · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: Maybe & Either

**Search keywords:** Maybe, Just, Nothing, Either, Left, Right, fromMaybe, fromJust, mapMaybe, catMaybes, lookup, find, parse, MonadFail, MonadError, partial function, short-circuit

## What the marker generates

For `Maybe a`:
- ~30% `Nothing`, ~70% `Just x` (from default `Arbitrary`).
- `x` drawn from the inner type's `Arbitrary`.

For `Either e a`:
- Roughly 50/50 `Left e` / `Right a`.
- Both `e` and `a` from their `Arbitrary` instances.

For string-based "parse" problems (Assignment 2 brackets):
```haskell
goodBrackets tb = ...    -- well-formed
badBrackets t = do
  n <- choose (0, length s)
  k <- elements ["(", "{", "}", ")"]
  return $ take n s ++ k ++ drop (n + 1) s
  where s = brackets t
```

So `badBrackets` corrupts a good string by INSERTING (not replacing) a random bracket. The marker has tests for both well-bracketed (expect `Just _`) and ill-bracketed (expect `Nothing`).

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | `Nothing` input | `Nothing` | `fromJust Nothing` crashes; pattern `Just x` non-exhaustive | First clause: handle `Nothing` |
| 2 | `Just []` (Just empty) | `Just []` | "Just is non-empty" assumptions wrong | Test for emptiness inside Just |
| 3 | `Just x` for some x | `Just 5` | Standard | Standard |
| 4 | Empty string `""` | `tree ""` | Spec: `tree "" = Nothing`. If you return `Just (Round [])`, you fail this 2-mark test. | First clause: `parse "" = Nothing` |
| 5 | Single character `"("` | unbalanced single | Spec: not well-bracketed → `Nothing` | Recursion termination |
| 6 | `Left e` input | `Left "error"` | Pattern `Right x` non-exhaustive; or you treat the error as a value | First clause: handle `Left` |
| 7 | `Right x` input | `Right 5` | Standard | Standard |
| 8 | `Just` chained with `fmap` | `fmap f (Just x) = Just (f x)` | Off-by-one if you assume `Just _ -> _` | Use library `fmap` |
| 9 | `do` over Maybe | `do x <- m; pure (x + 1)` | If `m == Nothing`, whole `do` is `Nothing` (short-circuits) | Maybe's bind handles this |
| 10 | `mapMaybe` filter-and-map | `mapMaybe f [a, b, c]` | If `f a = Nothing`, it's dropped | Read spec: drop or fail-whole? |
| 11 | `sequence [Just 1, Nothing, Just 3]` | mixed | Returns `Nothing` (one bad apple) | This is the desired behaviour usually |
| 12 | `lookup key []` | empty assoc list | `Nothing` | Standard |
| 13 | `lookup key (alist with duplicates)` | first match wins | If you use `find`, same | Standard |

## Property templates

```haskell
import Test.QuickCheck
import Data.Maybe

-- fromMaybe default behaviour
prop_fromMaybe_Nothing :: Int -> Bool
prop_fromMaybe_Nothing d = fromMaybe d Nothing == d

prop_fromMaybe_Just :: Int -> Int -> Bool
prop_fromMaybe_Just d x = fromMaybe d (Just x) == x

-- Functor laws
prop_maybeFmapId :: Maybe Int -> Bool
prop_maybeFmapId m = fmap id m == m

prop_maybeFmapComp :: Maybe Int -> Bool
prop_maybeFmapComp m = fmap ((+1) . (*2)) m == (fmap (+1) . fmap (*2)) m

-- Monad: Nothing short-circuits
prop_maybeNothingShortCircuit :: Maybe Int -> Bool
prop_maybeNothingShortCircuit m =
  (do _ <- Nothing; _ <- m; pure (42 :: Int)) == Nothing

-- Either left preserves
prop_eitherLeftPreserves :: String -> Bool
prop_eitherLeftPreserves e =
  (do _ <- (Left e :: Either String Int); pure 42) == Left e
```

## Assignment 2 brackets-style property

```haskell
import Test.QuickCheck

-- Empty string is not well-bracketed
prop_tree_empty :: Bool
prop_tree_empty = tree "" == Nothing

-- Well-bracketed round-trip
prop_tree_wellbracketed :: Property
prop_tree_wellbracketed = forAll genGoodBrackets $ \b ->
  let s = brackets b
  in  tree s == Just b

-- Insertion of any bracket-char breaks well-bracketedness
prop_tree_break :: Property
prop_tree_break = forAll genGoodBrackets $ \b ->
  forAll (chooseInt (0, length (brackets b))) $ \n ->
  forAll (elements "({})" ) $ \c ->
  let s' = take n (brackets b) ++ [c] ++ drop n (brackets b)
  in  case tree s' of
        Just b' -> brackets b' == s'   -- if parses, must be exact
        Nothing -> True                 -- expected: most of these don't parse
```

## Self-test before submission checklist

- [ ] Handles `Nothing` explicitly (with `case` or pattern)
- [ ] Handles `Just x` for general `x`
- [ ] Handles `Just []` if the inner type is a list
- [ ] Handles `Left e` explicitly (Either case)
- [ ] Handles `Right x` explicitly (Either case)
- [ ] For string parsing: handles `""` (returns `Nothing` if appropriate)
- [ ] For string parsing: handles single-char inputs
- [ ] `do`-notation over Maybe/Either short-circuits correctly
- [ ] No `fromJust` without prior `isJust` or pattern match
- [ ] No `head $ catMaybes` patterns (silently drops Nothings)

## Pitfalls that specifically lose QC marks

### Pitfall: `fromJust` on a possibly-Nothing
```haskell
-- WRONG:
findValue x xs = fromJust (lookup x xs)
-- QC tries x not in xs → crash
-- Fix:
findValue x xs = case lookup x xs of
  Just v  -> v
  Nothing -> error "missing"      -- only if spec allows
-- Better: change return type to Maybe
findValue x xs = lookup x xs
```

### Pitfall: pattern `Just (x:xs)` skips `Just []`
```haskell
-- WRONG: non-exhaustive on Just []
firstOrZero (Just (x:_)) = x
firstOrZero Nothing      = 0
-- Crashes on Just [].
-- Fix:
firstOrZero (Just (x:_)) = x
firstOrZero _            = 0
```

### Pitfall: catchall hides bugs
```haskell
-- WRONG: catchall return Nothing too eagerly
parse "" = Nothing
parse _  = Nothing   -- ← oops, this catches EVERYTHING
-- Move the catchall to LAST clause.
```

### Pitfall: `Right` on `Either` accidentally swapped
```haskell
-- WRONG: Either convention is Left=error, Right=success
divide _ 0 = Right "div by zero"      -- ← swapped, should be Left
divide x y = Left (x / y)              -- ← swapped, should be Right
-- Fix:
divide _ 0 = Left "div by zero"
divide x y = Right (x / y)
```

### Pitfall: chaining Maybes without `do`
```haskell
-- WRONG (verbose, error-prone):
combine m1 m2 = case m1 of
  Nothing -> Nothing
  Just x  -> case m2 of
    Nothing -> Nothing
    Just y  -> Just (x + y)
-- Right (cleaner):
combine m1 m2 = do
  x <- m1
  y <- m2
  pure (x + y)
```

### Pitfall: empty string in Assignment 2 brackets
```haskell
-- WRONG: returns Just (Round []) for ""
tree "" = Just (Round [])
-- Marker test: tree "" ~= Nothing (2 marks)
-- Fix:
tree "" = Nothing
```

### Pitfall: ill-bracketed input returns `Just <something>`
```haskell
-- For input "((" — well-bracketed? No (unmatched).
-- Spec: tree "((" = Nothing
-- If you return Just (Round [Round []]) without checking, you fail.
-- Fix: parse + verify; if remaining string after parsing is non-empty, return Nothing.
```

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md)
**Cross-topic:** [tree × maybe](../cross-matrix/tree-x-maybe.md) · [expr × maybe](../cross-matrix/expr-x-maybe.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [error-handling](../question-families/error-handling-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
