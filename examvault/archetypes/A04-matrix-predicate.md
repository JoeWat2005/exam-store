<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A04 — Matrix / Grid Predicate via Transpose**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · **A04** · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A04 — Matrix / Grid Predicate via Transpose

**Tier:** 1   |   **Stars:** ⭐⭐⭐⭐
**Mock appearance:** Q4   |   **Assignment appearance:** A1 (Grid layout), none for the predicate shape
**Combines with:** A21 · A23 · A09
**Search keywords:** matrix · grid · transpose · diagonal · rows · columns · isMagicSquare · winner · zipWith index

## What it tests
Whether you can compose `transpose`, `zipWith (!!)`, `reverse`, `all`, `sum`, and `map` to validate a property that ranges over rows AND columns AND diagonals — without writing a fresh loop for each direction.

## Recognition triggers
- Input type `[[Int]]`, `[[a]]`, `Grid`, `Board`
- Question mentions "rows", "columns", "diagonals" — at least two of those three
- "Magic square", "Sudoku", "tic-tac-toe winner", "Latin square", "every row sums to the same"
- Type signature shape: `[[Int]] -> Bool`, `[[Maybe Player]] -> Maybe Player`, `[[a]] -> Bool`
- Allowed imports include `Data.List` (you need `transpose`)
- Examples are given as `[[8,1,6],[3,5,7],[4,9,2]]` — clearly square grid

## Canonical template
```haskell
import Data.List (transpose)

isMagicSquare :: [[Int]] -> Bool
isMagicSquare [] = False
isMagicSquare xss =
  let target = sum (head xss)
      rows   = xss
      cols   = transpose xss
      diag1  = zipWith (!!) xss        [0..]    -- top-left → bottom-right
      diag2  = zipWith (!!) (reverse xss) [0..] -- bottom-left → top-right
      allLines = diag1 : diag2 : rows ++ cols
  in all (\xs -> sum xs == target) allLines
```

## Mutations (the examiner picks one)

### M1 — `isMagicSquare` (Mock Q4)
```haskell
isMagicSquare :: [[Int]] -> Bool
isMagicSquare xss =
  let s = sum (head xss)
      d1 = sum (zipWith (!!) xss [0..])
      d2 = sum (zipWith (!!) (reverse xss) [0..])
  in all (\r -> sum r == s) xss
  && all (\c -> sum c == s) (transpose xss)
  && d1 == s && d2 == s
```
What changes: nothing — this IS canonical.

### M2 — `isLatinSquare` (every row & col is a permutation of [1..n])
```haskell
import Data.List (sort)

isLatinSquare :: [[Int]] -> Bool
isLatinSquare xss =
  let n = length xss
      target = [1..n]
      rowOk = all (\r -> sort r == target) xss
      colOk = all (\c -> sort c == target) (transpose xss)
  in rowOk && colOk
```
What changes: uses `sort` for set-equality; drops the diagonal check.

### M3 — TTT `winner :: Grid -> Maybe Player`
```haskell
type Grid = [[Maybe Player]]

winner :: Grid -> Maybe Player
winner g =
  let rows = g
      cols = transpose g
      d1   = zipWith (!!) g [0..]
      d2   = zipWith (!!) (reverse g) [0..]
      lines' = rows ++ cols ++ [d1, d2]
  in foldr (\ln acc -> threeInARow ln `mplus` acc) Nothing lines'
  where
    threeInARow xs = case sequence xs of                    -- Maybe [Player]
                       Just (p:rest) | all (== p) rest -> Just p
                       _                                -> Nothing
```
What changes: returns the winning value, not just `Bool`; reduce with `firstJust` over all eight lines.

### M4 — anti-diagonal explicit (no `reverse`)
```haskell
antiDiag :: [[a]] -> [a]
antiDiag xss = [xss !! i !! (n - 1 - i) | i <- [0..n-1]]
  where n = length xss
```
What changes: list-comprehension version; useful when you want to be explicit about indices.

### M5 — Sudoku row+box check (no diagonals)
```haskell
import Data.List (group, sort)

allRowsOk, allColsOk, allBoxesOk :: [[Int]] -> Bool
allRowsOk  = all noDup
allColsOk  = all noDup . transpose
allBoxesOk g = all noDup [box i j | i<-[0,3,6], j<-[0,3,6]]
  where box i j = [g !! r !! c | r <- [i..i+2], c <- [j..j+2]]

noDup xs = all ((== 1) . length) (group (sort xs))
```
What changes: 3x3 "boxes" replace diagonals; need block extraction.

### M6 — fully square (validate it's actually n×n)
```haskell
isSquare :: [[a]] -> Bool
isSquare []  = True
isSquare xss = all ((== length xss) . length) xss
```
What changes: precondition guard; combine with M1: `isMagicSquare xss = isSquare xss && actuallyMagic xss`.

### M7 — predicate "all rows equal sum" (sums-only)
```haskell
allRowsSameSum :: [[Int]] -> Bool
allRowsSameSum [] = True
allRowsSameSum (xs:xss) = all ((== sum xs) . sum) xss
```
What changes: minimal — only rows, no transpose. Useful as a sub-step.

### M8 — column maximum / minimum
```haskell
colMaxima :: Ord a => [[a]] -> [a]
colMaxima = map maximum . transpose
```
What changes: a transform, not a predicate; one-liner via `transpose`.

### M9 — symmetric matrix check
```haskell
isSymmetric :: Eq a => [[a]] -> Bool
isSymmetric xss = xss == transpose xss
```
What changes: literally that. Equality-as-predicate.

### M10 — n-queens "no two same column" (Latin-like)
```haskell
queensSafe :: [Int] -> Bool          -- column position per row
queensSafe qs = let n = length qs
                in length (nub qs) == n
                && length (nub (zipWith (+) qs [0..])) == n
                && length (nub (zipWith (-) qs [0..])) == n
```
What changes: no full grid; column + both diagonals encoded as `qs+row`, `qs-row`.

## Worked examples from this course
- Mock Q4: `isMagicSquare` — M1.
- Problem sheet Set 15 (#141): `isMagicSquare` repeated.
- Problem sheet Set 15 (#150): `winner :: Grid -> Maybe Player` — M3.
- Assignment 1: `Grid` is just `[[a]]` underneath; the layout / pretty-printing is A13. The grid moves themselves use `transpose`-like reasoning to compute updates.

## QuickCheck attack surface
- **Empty grid** `[]` and **single-cell** `[[5]]`: 1×1 is trivially magic (sum of singleton = itself); empty often spec'd to `False`.
- **Off-by-one on diagonals**: 4×4 case `[[1..4],[5..8],[9..12],[13..16]]` has diag `[1,6,11,16]`. Marker checks `head xss = [1,2,3,4]` and `(!!) 0 = 1`. If you accidentally used `[1..]` starting from 1 instead of 0, your diagonal is shifted.
- **Non-square input**: `[[1,2,3],[4,5]]` — `transpose` succeeds but `(!!)` indexing crashes. Most markers exclude non-square; some specifically include it as a `False` test.
- **Both diagonals**: `[[2,7,6],[9,5,1],[4,3,8]]` is magic on rows, cols, ONE diagonal; the other diagonal sums to `2+5+8=15` ✓. Counter-example: a grid where main diag matches but anti diag doesn't.
- **Negative numbers**: `[[1,-1,0],[-1,0,1],[0,1,-1]]` — sums to 0 each line. Verifies you didn't assume positive.

## Pitfalls (marks-killers)
- **`reverse` for anti-diagonal**: the rows are flipped, not columns. `zipWith (!!) (reverse xss) [0..]` works because row `n-1` is now at index `0`, etc. Common bug: `zipWith (!!) xss [n-1, n-2 .. 0]`.
- **Missing one diagonal**: spec says "two main diagonals" — most students remember the main but forget the anti.
- **Computing `target` from a row that doesn't exist**: `sum (head xss)` crashes on `[]`. Guard with `null xss || ...`.
- **Using `head` and `last`**: GHC's `-Wno-x-partial` flag is set in Mock, but cleaner is `head xss = head (rows)` etc.
- **`map sum` vs `sum`**: a typical typo is `sum xss` instead of `map sum xss` — collapses everything into one number.
- **`transpose` requires `Data.List`** — don't forget the import (or hand-roll it as in Mock solution).

## Combines-with deep dive

### A04 × A21 — generate magic squares by list comp
```haskell
allMagicNxN :: Int -> [[[Int]]]
allMagicNxN n =
  let vals = [1 .. n*n]
  in [reshape n p | p <- permutations vals, isMagicSquare (reshape n p)]
  where reshape m = takeWhile (not . null) . unfoldr (Just . splitAt m)
```

### A04 × A09 — hand-rolled `transpose`
```haskell
transpose' :: [[a]] -> [[a]]
transpose' []         = []
transpose' ([]   : _) = []
transpose' xss        = map head xss : transpose' (map tail xss)
```

### A04 × A23 — TTT board update
```haskell
playAt :: (Int, Int) -> Player -> Grid -> Grid
playAt (r, c) p g = [ [ if (i,j) == (r,c) then Just p else cell
                       | (j, cell) <- zip [0..] row ]
                     | (i, row) <- zip [0..] g ]
```

## See also

**Combines with:** [A09 prelude reimpl](./A09-prelude-reimpl.md) · [A21 list comp synthesis](./A21-list-comp-synthesis.md)
**Question families:** [matrix-predicate](../question-families/matrix-predicate-family.md)
**Pitfalls:** [P-030 magic square wrong direction](../pitfalls/HIGH-severity.md#p-030)
**QuickCheck:** [matrix attacks](../quickcheck/matrix-attacks.md)
**Mock-Q:** [Mock Q4 magic square](../indexes/MOCK-Q-INDEX.md#mock-q4)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
