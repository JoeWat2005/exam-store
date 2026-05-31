<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: matrix-predicate**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · **matrix-predicate** · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: matrix-predicate

**Archetype:** A08 (predicate over `[[a]]` — rows/columns/diagonals)   |   **Stars:** ⭐⭐⭐   |   **Course week(s):** 5–6
**Search keywords:** isMagicSquare, sudoku, transpose, diagonal, [[a]], grid, board, n×n, winner

## Generator template
```haskell
import Data.List (transpose)

-- The seed: a Bool predicate on [[a]] checking that every row, every column,
-- and possibly the diagonals satisfy some property.
seed :: ([a] -> Bool) -> [[a]] -> Bool
seed p xss = all p xss
          && all p (transpose xss)
          && all p (diagonals xss)
  where
    diagonals m = [mainDiag m, mainDiag (map reverse m)]
    mainDiag = zipWith (!!) m [0..] . id  -- placeholder
```

Each mutation picks:
- which lines must be checked (rows, cols, diagonals, all 9-cell sub-blocks),
- what property each line must have (equal sum, all distinct, all `True`, one Player wins).

## Mutations (the examiner picks one)

### Mutation 1 — isMagicSquare (= mock Q4 / problem 141)
**Spec:** Every row, column and both main diagonals sum to the same value.
**Sig:** `isMagicSquare :: [[Int]] -> Bool`
**Solution:**
```haskell
import Data.List (transpose)

isMagicSquare :: [[Int]] -> Bool
isMagicSquare xss = all (== target) allSums
  where
    rows       = map sum xss
    cols       = map sum (transpose xss)
    diag1      = sum (zipWith (!!) xss [0..])
    diag2      = sum (zipWith (!!) xss [length xss - 1, length xss - 2 .. 0])
    target     = head rows
    allSums    = rows ++ cols ++ [diag1, diag2]
```
**QC trap:** Use `head rows` (or any rowsum) as the target — *all* sums must equal it. Don't pick magic 15 or 34 unless n is fixed. Empty input excluded by spec.

### Mutation 2 — isSudokuRowValid (no duplicates in 1..9)
**Spec:** A row of nine ints is valid iff it's some permutation of [1..9] (or contains 0s for blanks plus all distinct non-zero values).
**Sig:** `isSudokuRowValid :: [Int] -> Bool`
**Solution:**
```haskell
isSudokuRowValid :: [Int] -> Bool
isSudokuRowValid xs = let nonzero = filter (/= 0) xs
                     in length nonzero == length (removeDup nonzero)
                     && all (\x -> 1 <= x && x <= 9) nonzero
  where
    removeDup []     = []
    removeDup (y:ys) = y : removeDup (filter (/= y) ys)
```
**QC trap:** A blank (0) is allowed and *doesn't* count as a duplicate. A row `[1,1,2,...]` is invalid even if it sums to 45.

### Mutation 3 — isSudokuValid (rows + cols + 9 sub-blocks)
**Spec:** All 9 rows, 9 columns, 9 3×3 sub-blocks are valid.
**Sig:** `isSudokuValid :: [[Int]] -> Bool`
**Solution:**
```haskell
isSudokuValid :: [[Int]] -> Bool
isSudokuValid g = all isSudokuRowValid g
              && all isSudokuRowValid (transpose g)
              && all isSudokuRowValid (subBlocks g)
  where
    subBlocks m = [concat (take 3 (drop (3*r) (map (take 3 . drop (3*c)) m))) | r <- [0..2], c <- [0..2]]
```
**QC trap:** The 3×3 sub-blocks slicing is the trick. A correct grid that fails because rows OK but a sub-block isn't is the typical test case.

### Mutation 4 — winner (= problem 150)
**Spec:** Return `Just p` if player `p` has three in a row anywhere.
**Sig:** `winner :: Grid -> Maybe Player`
**Solution:**
```haskell
import Data.List (transpose)
import Data.Maybe (listToMaybe)

data Player = X | O deriving (Eq, Show)
type Grid   = [[Maybe Player]]

winner :: Grid -> Maybe Player
winner g = listToMaybe [p | line <- rows ++ cols ++ diags
                          , Just p <- [allSame line]]
  where
    rows  = g
    cols  = transpose g
    diags = [zipWith (!!) g [0..], zipWith (!!) g [n-1, n-2 .. 0]]
    n     = length g
    allSame (Just p : rest) | all (== Just p) rest = Just p
    allSame _                                       = Nothing
```
**QC trap:** Generalise to n×n by checking `length line == n` and `all (== Just p)`. The 3-in-a-row spec is just `n == 3`. (`allSame` already handles any line length, since `all` over the tail covers whatever `transpose`/`diags` produce.)

### Mutation 5 — isValidLatinSquare
**Spec:** Each row and each column is a permutation of [1..n] where n is the side length.
**Sig:** `isValidLatinSquare :: [[Int]] -> Bool`
**Solution:**
```haskell
isValidLatinSquare :: [[Int]] -> Bool
isValidLatinSquare g = all isPerm g && all isPerm (transpose g)
  where
    n = length g
    isPerm xs = length xs == n
             && sort xs == [1..n]
```
(needs `import Data.List (sort)`)
**QC trap:** No diagonal check. Empty grid is vacuously valid.

### Mutation 6 — gridContains (membership across rows)
**Spec:** Does any row contain the target?
**Sig:** `gridContains :: Eq a => a -> [[a]] -> Bool`
**Solution:**
```haskell
gridContains :: Eq a => a -> [[a]] -> Bool
gridContains x g = any (elem x) g
```
**QC trap:** Trivially-simple mutation — examiner uses it as a warm-up. Watch for "any" vs "all". 

### Mutation 7 — rowSums equal each other but not diagonals
**Spec:** Rows and columns sum equal but diagonals don't have to.
**Sig:** `isSemiMagic :: [[Int]] -> Bool`
**Solution:**
```haskell
isSemiMagic :: [[Int]] -> Bool
isSemiMagic xss = let rows = map sum xss
                      cols = map sum (transpose xss)
                  in all (== head rows) (rows ++ cols)
```
**QC trap:** Strictly weaker than `isMagicSquare`. Every magic square is semi-magic; not vice versa.

### Mutation 8 — countLiveNeighbours (Conway-style)
**Spec:** Given grid coordinates, count live neighbours.
**Sig:** `countLive :: [[Bool]] -> (Int, Int) -> Int`
**Solution:**
```haskell
countLive :: [[Bool]] -> (Int, Int) -> Int
countLive g (r, c) = length
  [ () | dr <- [-1, 0, 1]
       , dc <- [-1, 0, 1]
       , (dr, dc) /= (0, 0)
       , let r' = r + dr; c' = c + dc
       , 0 <= r' && r' < h
       , 0 <= c' && c' < w
       , g !! r' !! c' ]
  where
    h = length g
    w = if null g then 0 else length (head g)
```
**QC trap:** Don't count the cell itself. Out-of-bounds neighbours are dead (not counted). Use guards `0 <= r' && r' < h`.

### Mutation 9 — isWinningRow (parameterised win-line length)
**Spec:** Generalise winner to: does any row/col/diag have `k` matching consecutive non-Nothing entries?
**Sig:** `isWinningRow :: Eq a => Int -> [Maybe a] -> Maybe a`
**Solution:**
```haskell
isWinningRow :: Eq a => Int -> [Maybe a] -> Maybe a
isWinningRow k xs = go xs
  where
    go ys
      | length ys < k = Nothing
      | otherwise     = case take k ys of
          (Just p : rest) | all (== Just p) rest -> Just p
          _                                       -> go (tail ys)
```
**QC trap:** "Consecutive" matters. `[Just X, Nothing, Just X, Just X, Just X]` has 3 in a row at indices 2,3,4. Check via windowing, not just `all`.

### Mutation 10 — isSquareGrid
**Spec:** Predicate that the grid is square.
**Sig:** `isSquareGrid :: [[a]] -> Bool`
**Solution:**
```haskell
isSquareGrid :: [[a]] -> Bool
isSquareGrid g = let n = length g in all ((== n) . length) g
```
**QC trap:** Used as a precondition to all the others. Empty grid (`[]`) is square (0×0).

## Hidden-predicate mutations
- "All rows satisfy p AND all columns satisfy p" → `all p g && all p (transpose g)`.
- "At least one row satisfies p" → `any p g`.
- "Specific number of matching rows" → `length (filter p g) == k`.

## Accumulator-style alternative
For `winner` you can accumulate winning Maybe's across all lines:
```haskell
winnerAcc :: Grid -> Maybe Player
winnerAcc g = foldr (\line acc -> if isWin line then Just (lineP line) else acc) Nothing allLines
  where ...
```
Not usually preferred — the list-comprehension or `find` version is clearer.

## Fold-style alternative
`isMagicSquare` rewritten via foldr:
```haskell
isMagicSquare' xss = let target = sum (head xss)
                    in  all ((==target) . sum) (xss ++ transpose xss)
                     && checkDiags target xss
```
Cleaner, less explicit.

## Cross-family combinations
- this family + `list-comp-family.md`: most matrix predicates are list comprehensions over indices.
- this family + State monad: filling Sudoku (problem-sheet Week 11 style).
- this family + Functor: mapping over `[[a]]` is `(map . map)`.
- this family + `lazy-infinite-family.md`: Conway's Game of Life as an infinite stream of grids.

## QuickCheck universal attacks
- **Empty grid:** most predicates vacuously True. Edge-case check.
- **1×1 grid:** trivially magic, trivially Latin, trivially winning if non-empty.
- **All-identical entries:** `isMagicSquare` True (n*v sums equal). `isSudoku` False (duplicates).
- **transpose . transpose == id:** sanity for rows/cols logic.
- **transpose (magic) is also magic** (for the symmetric magic-square definition).
- **Reverse columns of a Latin square:** still Latin.

## Pitfalls (per mutation)
- M1: forgetting one of the diagonals; using `take n . map head` style instead of `zipWith (!!) m [0..]`.
- M2: counting 0 as a duplicate.
- M3: wrong sub-block slicing — easy to write `take 3 . drop (3*r)` wrong.
- M4: missing diagonals; missing cases for partial wins.
- M5: not checking row length == n.
- M6: writing `any (any (==x)) g` (correct but verbose).
- M7: copying `isMagicSquare` and forgetting to drop the diagonals.
- M8: counting the centre cell (the cell itself).
- M9: using `all (==Just p)` over the *whole* row instead of windows of size `k`.
- M10: `length` on an infinite row hangs — assume finite.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — isMagicAntiSquare (anti-diagonal sum check — different geometric layout)

**Spec:** Same as `isMagicSquare` but the magic constraint applies to the anti-diagonal (top-right to bottom-left) instead of the main diagonal.

**Type sig:** `isMagicAntiSquare :: [[Int]] -> Bool`

```haskell
isMagicAntiSquare :: [[Int]] -> Bool
isMagicAntiSquare m
  | not (square m) = False
  | otherwise =
      let s    = sum (head m)
          rows = all ((== s) . sum) m
          cols = all ((== s) . sum) (transpose m)
          antiD = sum (zipWith (!!) m [n-1, n-2 .. 0])
      in rows && cols && antiD == s
  where n = length m

square :: [[a]] -> Bool
square m = let n = length m in all ((== n) . length) m
```

**What changes vs seed:** Same fold shape but changes the index sequence on the diagonal extraction — `[n-1, n-2 .. 0]` instead of `[0..n-1]`. Different *data layout traversal*.

**QC trap:** `[n-1, n-2 .. 0]` for `n = 0` gives `[-1, -2 .. 0]` which is empty — but you reach the empty check earlier via `square`. Without the guard, `head m` on an empty matrix crashes.

### Mutation 12 — isLatinSquare (no repeats per row + column — different predicate kind)

**Spec:** True iff every row and every column contains each of `1..n` exactly once. A different family of constraints than magic squares (sums vs distinctness).

**Type sig:** `isLatinSquare :: [[Int]] -> Bool`

```haskell
isLatinSquare :: [[Int]] -> Bool
isLatinSquare m
  | not (square m) = False
  | otherwise =
      let n      = length m
          target = [1..n]
          rowsOk = all (\row -> sort row == target) m
          colsOk = all (\col -> sort col == target) (transpose m)
      in rowsOk && colsOk
  where square m = let n = length m in all ((== n) . length) m
```

**What changes vs seed:** Different predicate family: distinctness rather than sum. Forces a `sort` (or `nub` + `length`) — a new helper not used by `isMagicSquare`.

**QC trap:** `sort xs == [1..n]` is sufficient AND necessary for "exactly `1..n` once each". `nub xs == xs` is weaker (no duplicates but might be `[5,6,7]`).

## See also

**Primary archetype:** [A04 matrix predicate](../archetypes/A04-matrix-predicate.md)
**QuickCheck:** [matrix attacks](../quickcheck/matrix-attacks.md)
**Pitfalls:** [P-030 magic square wrong direction](../pitfalls/HIGH-severity.md#p-030)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
