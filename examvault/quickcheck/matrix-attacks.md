<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: matrices ([[a]] / Grid)**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · **matrix** · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: matrices ([[a]] / Grid)

**Search keywords:** matrix, [[a]], magic square, isMagicSquare, transpose, rows, columns, diagonal, anti-diagonal, grid, 1x1, square, Mock Q4, Assignment 1, sum, ragged, rectangular

Mock Q4 (magic squares) and Assignment 1 (Tatami grid) are matrix questions. The marker generates square and rectangular grids.

## What the marker generates

### Mock Q4 (magic squares):
```haskell
genSquare :: Int -> Gen [[Int]]
genSquare n = replicateM n (replicateM n arbitrary)

genSingleSquare :: Gen [[Int]]
genSingleSquare = genSquare 1   -- 1x1

genNonMagicSquare :: Gen [[Int]]
genNonMagicSquare = do
  size <- chooseInt (2, 5)        -- 2x2 to 5x5
  genSquare size `suchThat` (\x -> not $ Solutions.isMagicSquare x)
```

Plus three hardcoded magic squares (3x3, 4x4, 5x5):
```haskell
magic3x3 = [[8,1,6],[3,5,7],[4,9,2]]
magic4x4 = [[1,15,14,4],[12,6,7,9],[8,10,11,5],[13,3,2,16]]
magic5x5 = [[17,24,1,8,15],[23,5,7,14,16],[4,6,13,20,22],[10,12,19,21,3],[11,18,25,2,9]]
```

The marker definition of "magic":
- All rows sum to the same value
- All columns sum to the same value
- BOTH diagonals (main and anti) sum to the same value

The "semi-magic" fallback test (4 marks) drops the diagonal requirement:
```haskell
isSemiMagic xss = all (== sum (head xss)) allsums
 where rowsums = map sum xss
       columnsums = map sum (transpose xss)
       allsums = rowsums ++ columnsums   -- ← NO diagonals
```

### Assignment 1 (Tatami grid):
```haskell
genGrid gen rows cols = Grid <$> replicateM rows (replicateM cols gen)
genGridWithAPointer gen rows cols = ... -- with focus pointer
genGridWithAPointerAtTopLeft = ...      -- specific for cover
```

For "uncoverable" grids, the marker uses a HARDCODED list:
```haskell
elements [(7,10),(10,7),(8,11),(8,12),(9,12),(13,10),(14,10),(15,10)]
```

These are the OEIS A068920 dimensions.

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | `1x1` square `[[42]]` | hardcoded test | "Sum of 1 row equals sum of 1 column equals diagonal of single element" — trivially magic. If you require size >= 3, you fail. | `isMagicSquare [[x]] = True` |
| 2 | `2x2` square | tested via `genSquare 2` | Diagonals are just the corners; small case | Standard |
| 3 | `3x3` magic square (`magic3x3`) | hardcoded test, 8 marks | If you fail this, you almost certainly fail others | Use the def: all rows, cols, diagonals sum equal |
| 4 | `3x3` non-magic | random with `suchThat (not . isMagic)` | Returns True incorrectly | Same |
| 5 | Empty matrix `[]` | not generated but defensive | `head []` crashes | First clause: `f [] = ...` |
| 6 | Matrix with empty rows `[[], [], []]` | not generated but possible | crashes | First clause |
| 7 | Non-square matrix `[[1,2], [3,4,5]]` | not a "square" — spec usually disallows | If you don't check squareness, you may compute wrong | `all ((== n) . length) rows` where `n = length rows` |
| 8 | Rectangular but uniform `[[1,2,3], [4,5,6]]` | not square | Spec: should this fail? Usually for Mock Q4 you can assume it IS square. | Read spec |
| 9 | All same values `[[5,5,5], [5,5,5], [5,5,5]]` | sums all equal | "Semi-magic" passes (all rows = 15, cols = 15, diags = 15) | This IS magic by the def. |
| 10 | Sum overflow | very large numbers | Integer is unbounded in Haskell so OK | Standard |
| 11 | Negative numbers | `[[-1, 5], [-3, 7]]` | Sum can be negative; still works | Standard |
| 12 | Magic 4x4 (`magic4x4`) | hardcoded | Same as 3x3 | Same |
| 13 | Magic 5x5 (`magic5x5`) | hardcoded | Same | Same |
| 14 | Rows-equal but cols-not | semi-magic-row only | Should return False for full magic, True for semi-magic | Check ALL three (rows + cols + diagonals) |
| 15 | Rows+cols-equal but diagonals-not | semi-magic | Same — fail full, pass semi | Same |
| 16 | Forgot anti-diagonal | only main diagonal | Spec wants BOTH diagonals | `zipWith (!!) (reverse xss) [0..]` for anti |
| 17 | Anti-diagonal indices wrong | `zipWith (!!) xss [n-1, n-2, ...]` | Off-by-one in indexing | Use `[length xss - 1, length xss - 2, ..., 0]` or `reverse` |

## The five sums you must check

For magic square of size `n`:
```haskell
n = length xss
target = sum (head xss)
rowsums    = map sum xss                       -- n sums
colsums    = map sum (transpose xss)           -- n sums
mainDiag   = sum [xss !! i !! i | i <- [0..n-1]]
antiDiag   = sum [xss !! i !! (n-1-i) | i <- [0..n-1]]
isMagic = all (== target) (rowsums ++ colsums ++ [mainDiag, antiDiag])
```

## Property templates

```haskell
import Test.QuickCheck
import Data.List (transpose)

-- Singleton magic
prop_singleton :: Int -> Bool
prop_singleton x = isMagicSquare [[x]]

-- The three known magic squares
prop_knownMagic :: Bool
prop_knownMagic = all isMagicSquare [magic3x3, magic4x4, magic5x5]
  where
    magic3x3 = [[8,1,6],[3,5,7],[4,9,2]]
    magic4x4 = [[1,15,14,4],[12,6,7,9],[8,10,11,5],[13,3,2,16]]
    magic5x5 = [[17,24,1,8,15],[23,5,7,14,16],[4,6,13,20,22],[10,12,19,21,3],[11,18,25,2,9]]

-- All zeros n×n: rows sum to 0, cols sum to 0, diags sum to 0 → magic
prop_zerosMagic :: Property
prop_zerosMagic = forAll (chooseInt (1, 6)) $ \n ->
  isMagicSquare (replicate n (replicate n 0)) == True

-- Constant matrix is magic
prop_constantMagic :: Int -> Property
prop_constantMagic c = forAll (chooseInt (1, 6)) $ \n ->
  isMagicSquare (replicate n (replicate n c))

-- Identity-like sum bug check
prop_identityNotMagic :: Bool
prop_identityNotMagic =
  not (isMagicSquare [[1,0,0],[0,1,0],[0,0,1]])
  -- rows: [1,1,1] ✓
  -- cols: [1,1,1] ✓
  -- main diag: 3
  -- anti diag: 1
  -- → not magic
```

## Self-test before submission checklist

- [ ] `isMagicSquare [[x]]` returns `True` for any x (singleton case)
- [ ] `isMagicSquare magic3x3` returns `True`
- [ ] `isMagicSquare magic4x4` returns `True`
- [ ] `isMagicSquare magic5x5` returns `True`
- [ ] `isMagicSquare` checks ALL rows
- [ ] `isMagicSquare` checks ALL columns (via `transpose`)
- [ ] `isMagicSquare` checks the MAIN diagonal
- [ ] `isMagicSquare` checks the ANTI-diagonal (the often-forgotten one)
- [ ] All five sums are compared against the SAME target
- [ ] Returns `False` for non-magic
- [ ] Doesn't crash on empty or non-square matrices

## Pitfalls that specifically lose QC marks

### Pitfall: forgetting anti-diagonal
```haskell
-- WRONG: only checks main diagonal
isMagicSquare xss = let target = sum (head xss)
                        rows = map sum xss
                        cols = map sum (transpose xss)
                        mainDiag = sum (zipWith (!!) xss [0..])
                    in  all (== target) (rows ++ cols ++ [mainDiag])
-- For [[1,0,2], [0,1,0], [2,0,1]]:
--   rows: [3,1,3] — not all equal so this case isn't magic anyway.
-- For a custom example that passes rows+cols+main but not anti:
--   isMagicSquare returns True incorrectly.
-- Fix: include anti-diagonal
```

### Pitfall: anti-diagonal indices off-by-one
```haskell
-- WRONG: index from 1
antiDiag = sum [xss !! i !! (n - i) | i <- [0..n-1]]
-- For n=3, i=0: xss !! 0 !! 3 — index out of range
-- Fix:
antiDiag = sum [xss !! i !! (n - 1 - i) | i <- [0..n-1]]
```

### Pitfall: `head []` on empty matrix
```haskell
-- WRONG: assumes non-empty
isMagicSquare xss = let target = sum (head xss) in ...
-- For [] crashes.
-- Defensive:
isMagicSquare [] = True   -- vacuously? or spec-dependent
isMagicSquare xss = ...
```

### Pitfall: confusing rows with cols
```haskell
-- transpose swaps:
transpose [[1,2,3], [4,5,6]] = [[1,4], [2,5], [3,6]]
-- So:
rows xss    = xss
cols xss    = transpose xss

-- Don't write:
rows = transpose cols    -- ← wrong direction unless cols = transpose rows initially
```

### Pitfall: non-square check missing
```haskell
-- For rectangular matrices, the diagonal isn't well-defined.
-- WRONG: doesn't check squareness, crashes on rectangular
isMagicSquare xss = ... mainDiag = [xss !! i !! i | i <- [0..n-1]] ...
-- For [[1,2], [3,4,5]] (size 2x{2,3}), n=2 but xss!!0 has 2 elems, xss!!1 has 3 — at least no crash for n=2, but for [[1], [2,3]], xss!!0!!1 crashes.

-- Defensive: check that all rows have length n
isSquare xss = let n = length xss in all ((== n) . length) xss
isMagicSquare xss = isSquare xss && (... magic check ...)
```

### Pitfall: not using `transpose` (rolling your own column extractor)
```haskell
-- WRONG (slow and buggy):
cols xss = map (\j -> map (!! j) xss) [0 .. length (head xss) - 1]
-- Subtle bug: `head xss` crashes on []
-- Fix: import Data.List (transpose) and use it.
```

## Assignment 1 grid specifics

Assignment 1 uses a custom `Grid` and `GridWithAPointer` (zipper). Edge cases:
- Pointer at left edge: `moveLeft` should ERROR (not return invalid grid)
- Pointer at right edge: `moveRight` should ERROR
- Same for top/bottom
- `cover` on 1×1: ERROR (can't tile)
- `cover` on odd×odd: ERROR (uncoverable)
- `cover` on the OEIS uncoverable list: ERROR
- `cover` on coverable: actually produce a valid tiling

The marker uses `monadicIO $ do ... catch ...` to test that the error IS thrown.

## See also

**Archetypes:** [A04 matrix predicate](../archetypes/A04-matrix-predicate.md)
**Question families:** [matrix-predicate](../question-families/matrix-predicate-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
