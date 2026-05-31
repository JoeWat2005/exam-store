<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: list-fold**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · **list-fold** · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: list-fold

**Archetype:** A02 (foldr/foldl over a list)   |   **Stars:** ⭐⭐   |   **Course week(s):** 5
**Search keywords:** foldr, foldl, scanr, scanl, sumWithFoldr, lengthWithFoldr, mapWithFoldr, filterWithFoldr, reverseWithFoldl, allWithFoldr

## Generator template
```haskell
-- The seed: every list-eating function whose result *only* depends on the
-- list elements (no extra state) can be expressed as foldr combine unit.
seed :: (a -> b -> b) -> b -> [a] -> b
seed _ z []     = z
seed f z (x:xs) = f x (seed f z xs)
-- Or: just `foldr`.
```

Mutations differ along three axes:
1. **Direction:** foldr (right-to-left) vs foldl (left-to-right, with seed accumulator).
2. **Output:** scalar (`sum`) vs list (`reverse`) vs prefix list (`scanl`).
3. **Combine:** strict (`foldl'`) vs lazy (`foldl`/`foldr`).

## Mutations (the examiner picks one)

### Mutation 1 — sumWithFoldr (= problem 41)
**Sig:** `sumWithFoldr :: Num a => [a] -> a`
**Solution:**
```haskell
sumWithFoldr :: Num a => [a] -> a
sumWithFoldr = foldr (+) 0
```
**QC trap:** On a *long* finite list, foldr (+) 0 builds a deeply-nested tree of `+` thunks. For real performance use `foldl' (+) 0` (strict left fold).

### Mutation 2 — lengthWithFoldr (= problem 42)
**Sig:** `lengthWithFoldr :: [a] -> Int`
**Solution:**
```haskell
lengthWithFoldr :: [a] -> Int
lengthWithFoldr = foldr (\_ n -> n + 1) 0
```
**QC trap:** Ignoring the element with `_` is the key — exam students sometimes write `(\x n -> x + 1)` and the type-checker yells about Num.

### Mutation 3 — mapWithFoldr (= problem 43)
**Sig:** `mapWithFoldr :: (a -> b) -> [a] -> [b]`
**Solution:**
```haskell
mapWithFoldr :: (a -> b) -> [a] -> [b]
mapWithFoldr f = foldr (\x acc -> f x : acc) []
```
**QC trap:** Result list is constructed right-to-left in the source code, but appears left-to-right in evaluation thanks to laziness of `(:)`. Works on infinite lists.

### Mutation 4 — filterWithFoldr (= problem 44)
**Sig:** `filterWithFoldr :: (a -> Bool) -> [a] -> [a]`
**Solution:**
```haskell
filterWithFoldr :: (a -> Bool) -> [a] -> [a]
filterWithFoldr p = foldr (\x acc -> if p x then x : acc else acc) []
```
**QC trap:** Same as mapWithFoldr — incremental output makes this work on infinite lists *if* the predicate accepts arbitrarily late elements.

### Mutation 5 — reverseWithFoldl (= problem 45)
**Sig:** `reverseWithFoldl :: [a] -> [a]`
**Solution:**
```haskell
reverseWithFoldl :: [a] -> [a]
reverseWithFoldl = foldl (\acc x -> x : acc) []
-- Or: foldl (flip (:)) []
```
**QC trap:** This is O(n). The right-fold `foldr (\x acc -> acc ++ [x]) []` is O(n²) — common student error. The exam *specifies* foldl because of this.

### Mutation 6 — allWithFoldr (= problem 46)
**Sig:** `allWithFoldr :: (a -> Bool) -> [a] -> Bool`
**Solution:**
```haskell
allWithFoldr :: (a -> Bool) -> [a] -> Bool
allWithFoldr p = foldr (\x acc -> p x && acc) True
```
**QC trap:** Short-circuits via lazy `&&` — works on infinite lists *as long as* some element fails the predicate.

### Mutation 7 — anyWithFoldr
**Sig:** `anyWithFoldr :: (a -> Bool) -> [a] -> Bool`
**Solution:**
```haskell
anyWithFoldr :: (a -> Bool) -> [a] -> Bool
anyWithFoldr p = foldr (\x acc -> p x || acc) False
```
**QC trap:** Dual of mutation 6. Unit is `False`, combine uses `||`.

### Mutation 8 — concatWithFoldr
**Sig:** `concatWithFoldr :: [[a]] -> [a]`
**Solution:**
```haskell
concatWithFoldr :: [[a]] -> [a]
concatWithFoldr = foldr (++) []
```
**QC trap:** Right-fold is right because each `++` happens at the cons-cell of an already-shrunken accumulator — O(n) total. The left version `foldl (++) []` is O(n²).

### Mutation 9 — scanrSum (running sums from right)
**Sig:** `scanrSum :: Num a => [a] -> [a]`
**Solution:**
```haskell
scanrSum :: Num a => [a] -> [a]
scanrSum = scanr (+) 0
```
**Spec:** `scanrSum [1,2,3] == [6,5,3,0]` — every suffix sum.
**QC trap:** Result has length `length xs + 1`. Last element is always the seed (0).

### Mutation 10 — scanlMax (running max from left)
**Sig:** `scanlMax :: Ord a => a -> [a] -> [a]`
**Solution:**
```haskell
scanlMax :: Ord a => a -> [a] -> [a]
scanlMax = scanl max
```
**Spec:** `scanlMax 0 [3,1,4,1,5,9,2,6] == [0,3,3,4,4,5,9,9,9]` — running maximum.
**QC trap:** First element of the result is *the seed*, not the first list element.

### Mutation 11 — composeFoldr (= problem 47, compose')
**Sig:** `compose' :: [a -> a] -> (a -> a)`
**Solution:**
```haskell
compose' :: [a -> a] -> (a -> a)
compose' = foldr (.) id
```
**QC trap:** Empty list yields `id`, NOT `const undefined`. This is the "functions form a monoid under composition with id as unit" pattern.

### Mutation 12 — foldr-via-foldl (the bridge problem)
**Sig:** `foldrViaFoldl :: (a -> b -> b) -> b -> [a] -> b`
**Solution:**
```haskell
foldrViaFoldl :: (a -> b -> b) -> b -> [a] -> b
foldrViaFoldl f z xs = foldl (\g x -> g . f x) id xs z
```
**QC trap:** Builds a *function pipeline* via foldl, then applies it to z. Famous interview trick — examiner may ask for this. Equivalent of `foldr f z = foldl (flip f) z . reverse` (which is also a valid answer).

## Hidden-predicate mutations
- "Sum of all squares of even numbers in the list" → fuse:
```haskell
sumOfSquaresOfEvens :: [Int] -> Int
sumOfSquaresOfEvens = foldr (\x acc -> if even x then x*x + acc else acc) 0
```
- This is `sum . map (^2) . filter even`, but the inlined fold is the most efficient and the exam-style answer.

## Accumulator-style alternative
For sums, lengths, products — replace `foldr` with `foldl'` (strict left fold, from Data.List):
```haskell
sumStrict :: Num a => [a] -> a
sumStrict = foldl' (+) 0
```
This is the canonical "fix the space leak" exam answer.

## Fold-style alternative
Already in fold style. For an `unfoldr` flavour — used when *generating* a list:
```haskell
import Data.List (unfoldr)

countDown :: Int -> [Int]
countDown = unfoldr (\n -> if n < 0 then Nothing else Just (n, n - 1))
```
Worth knowing — appears occasionally as a contrast.

## Cross-family combinations
- this family + `list-rewrite-family.md` — same functions, dual presentation.
- this family + Writer monad — `foldM` over a Writer log.
- this family + State monad — `foldM` for stateful folds; see `monad-combinator-family.md` for foldM.
- this family + `lazy-infinite-family.md` — `foldr` works on infinite lists *if combine is lazy* in its second argument.

## QuickCheck universal attacks
- **Empty list:** result must equal the seed (unit).
- **Singleton:** result equals `f x z`.
- **Foldr vs foldl distinction:** non-associative combine reveals direction. E.g. `foldr (-) 0 [1,2,3] = 2`, `foldl (-) 0 [1,2,3] = -6`.
- **Infinite input on foldr with lazy combine:** `take 5 (foldr (:) [] [1..])` works; `foldl` would diverge.
- **Strictness:** `foldl (+) 0 [1..10^7]` stack-overflows in lazy Haskell; `foldl' (+) 0 [1..10^7]` doesn't.

## Pitfalls (per mutation)
- M1: writing `foldr (+) 0 xs` vs `foldl (+) 0 xs` — both correct for `(+)` since associative, but the examiner watches for `foldl'`.
- M2: `foldr (+) 0` instead of `foldr (\_ n -> n + 1) 0` (wrong — that's sum).
- M3/M4: forgetting the `acc` parameter on the lambda.
- M5: writing `foldr (...)` instead of `foldl` — gives O(n²).
- M6: unit of `False` instead of `True`.
- M7: unit of `True` instead of `False`.
- M8: using `foldl` — O(n²).
- M9/M10: confusing `scanr` (suffix scans, includes seed at the end) with `scanl` (prefix scans, includes seed at the start).
- M11: empty list returns `undefined` instead of `id`.
- M12: getting the function composition order wrong — `g . f x` vs `f x . g`.

## See also

**Primary archetype:** [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)
**Sibling families:** [list-rewrite](./list-rewrite-family.md) · [list-comp](./list-comp-family.md)
**Cross-topic:** [list × list-monad](../cross-matrix/list-x-list-monad.md)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
