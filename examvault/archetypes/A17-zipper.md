<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A17 — Zipper Navigation**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · **A17** · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A17 — Zipper Navigation

**Tier:** 4   |   **Stars:** ⭐
**Mock appearance:** none   |   **Assignment appearance:** A1 (entire — `GridWithAPointer`)
**Combines with:** A13 · A22 · A01
**Search keywords:** zipper · focus · context · moveLeft · moveRight · moveUp · moveDown · cursor · put · GridWithAPointer

## What it tests
Whether you can split a data structure into "context-around-the-focus + focus + the-other-context" and write `move…` functions that shift the boundary by one — keeping all moves O(1).

## Recognition triggers
- A type definition with multiple fields representing "left", "focus", "right" (or above/below/etc.)
- Operations named `moveLeft`, `moveRight`, `moveUp`, `moveDown`
- `put :: a -> Z a -> Z a` (overwrite focus)
- Question explicitly mentions "cursor", "pointer", "current position"
- Boundary edge cases ("can't move past the left edge")
- `data Z a = Z [a] a [a]` or 2D variant

## Canonical template
```haskell
-- 1D zipper:
data ListZ a = ListZ { left :: [a], focus :: a, right :: [a] }

moveR :: ListZ a -> ListZ a
moveR (ListZ ls x (r:rs)) = ListZ (x:ls) r rs
moveR z                   = z       -- or error

moveL :: ListZ a -> ListZ a
moveL (ListZ (l:ls) x rs) = ListZ ls l (x:rs)
moveL z                   = z

put :: a -> ListZ a -> ListZ a
put y z = z { focus = y }
```

## Mutations (the examiner picks one)

### M1 — 1D list zipper (above)
See canonical. What changes: a single dimension; trivial to verify.

### M2 — `GridWithAPointer` (A1)
```haskell
newtype Grid a = Grid { grid :: [[a]] }
newtype GridWithAPointer a =
  GridWithAPointer (Grid a, [a], a, [a], Grid a)
  --                ^above   ^leftRevRow ^focus ^right  ^below

moveLeft :: GridWithAPointer a -> GridWithAPointer a
moveLeft (GridWithAPointer (gt, l:ls, x, rs, gb))
  = GridWithAPointer (gt, ls, l, x:rs, gb)
moveLeft _ = error "can't move left"

moveRight :: GridWithAPointer a -> GridWithAPointer a
moveRight (GridWithAPointer (gt, ls, x, r:rs, gb))
  = GridWithAPointer (gt, x:ls, r, rs, gb)
moveRight _ = error "can't move right"
```
What changes: 2D — five fields; `left` row is REVERSED (closest-to-focus first).

### M3 — `moveUp` / `moveDown` in 2D
```haskell
moveUp :: GridWithAPointer a -> GridWithAPointer a
moveUp (GridWithAPointer (Grid (row : above), ls, x, rs, Grid below))
  = let i = length ls
        (newL, newF : newR) = splitAt i row
        oldRow = reverse ls ++ [x] ++ rs
    in GridWithAPointer (Grid above, reverse newL, newF, newR, Grid (oldRow : below))
moveUp _ = error "can't move up"
```
What changes: 2D vertical move; need column index from `length ls` to split the new row.

### M4 — Tree zipper
```haskell
data Crumb a = LeftCrumb a (BT a) | RightCrumb a (BT a)
data TreeZ a = TreeZ (BT a) [Crumb a]

goLeft :: TreeZ a -> TreeZ a
goLeft (TreeZ (Fork x l r) crumbs) = TreeZ l (LeftCrumb x r : crumbs)

goUp :: TreeZ a -> TreeZ a
goUp (TreeZ t (LeftCrumb x r : crumbs))  = TreeZ (Fork x t r) crumbs
goUp (TreeZ t (RightCrumb x l : crumbs)) = TreeZ (Fork x l t) crumbs
```
What changes: tree-shaped zipper; crumb trail remembers branches not taken.

### M5 — `put` (overwrite focus)
```haskell
put :: a -> GridWithAPointer a -> GridWithAPointer a
put y (GridWithAPointer (gt, ls, _, rs, gb))
  = GridWithAPointer (gt, ls, y, rs, gb)
```
What changes: trivial; just replace `focus` field.

### M6 — `unzip` (rebuild plain Grid)
```haskell
toGrid :: GridWithAPointer a -> Grid a
toGrid (GridWithAPointer (Grid gt, ls, x, rs, Grid gb))
  = Grid (gt ++ [reverse ls ++ [x] ++ rs] ++ gb)
```
What changes: reverse the left context, splice focus, concat with above/below.

### M7 — `fromGrid` (lift Grid to GridWithAPointer)
```haskell
fromGrid :: Grid a -> GridWithAPointer a
fromGrid (Grid (row : rest))
  = GridWithAPointer (Grid [], [], head row, tail row, Grid rest)
fromGrid _ = error "empty grid"
```
What changes: focus on (0,0); above/left empty.

### M8 — `move` chain in `State`
```haskell
type GridM a = State (GridWithAPointer a)

moveR' :: GridM a ()
moveR' = modify moveRight
```
What changes: wraps in State for sequencing; useful with A02 territory.

### M9 — Cursor-aware `Show`
```haskell
instance Show a => Show (GridWithAPointer a) where
  show g = let Grid raw = toGrid g
               -- ... highlight position (row, col)
           in unlines (...)
```
What changes: A17 × A13; see A1 solution.

### M10 — Maybe-ified moves
```haskell
safeMoveLeft :: GridWithAPointer a -> Maybe (GridWithAPointer a)
safeMoveLeft (GridWithAPointer (gt, l:ls, x, rs, gb))
  = Just (GridWithAPointer (gt, ls, l, x:rs, gb))
safeMoveLeft _ = Nothing
```
What changes: failure-safe; useful for chaining with `>>=`.

## Worked examples from this course
- Assignment 1: ENTIRE — `GridWithAPointer`, `moveLeft`/`Right`/`Up`/`Down`, `put`, plus `putTatami*` operations.
- Practice file: none directly, but the zipper idea reappears in any "cursor" code.
- No problem sheet covers this directly.

## QuickCheck attack surface
- **Round-trip**: `moveLeft . moveRight == id` when at the interior; partial on boundary.
- **`put y . moveR . moveL == put y`**: focused position unchanged.
- **`toGrid . fromGrid == id`** on non-empty grids.
- **Boundary failure**: `moveLeft` on `(_, [], x, rs, _)` either errors or returns `Nothing`. Marker tests one or the other.
- **Idempotent put**: `put x (put y g) == put x g` (the second put overwrites the first).
- **`length` preservation**: applying any move sequence preserves total cell count.
- **2D `moveUp . moveDown` AT EDGE**: should be identity in interior, fail at edge.

## Pitfalls (marks-killers)
- **Left context orientation**: reversed (closest-to-focus first). Easy to flip. If you store `left` as "leftmost first", the moveLeft cons is wrong.
- **Boundary handling**: when `ls = []`, `moveLeft` has no head. Return original, error, or `Nothing` — match the spec.
- **Row split index off-by-one**: `splitAt i row` where `i = length ls` is the focus column index. Use this consistently.
- **`reverse ls ++ [x] ++ rs` to rebuild**: forgetting `reverse` gives a reversed row.
- **Forgetting one of the four moves**: write `moveLeft`, then mirror three times (`moveRight`, `moveUp`, `moveDown`). Each is structurally similar.
- **`error` vs `Maybe`**: A1 spec uses `error` for boundary; production code prefers `Maybe`.

## Combines-with deep dive

### A17 × A13 — Show with highlighted focus
Use ANSI escapes around `show focus` to mark the cursor:
```haskell
highlight :: Show a => a -> String
highlight x = "\ESC[44m" ++ show x ++ "\ESC[0m"
```
Then build the grid display with the focus cell highlighted.

### A17 × A22 — `Eq`/`Ord` for the zipper
```haskell
instance Eq a => Eq (GridWithAPointer a) where
  GridWithAPointer (a, b, c, d, e) == GridWithAPointer (a', b', c', d', e')
    = a == a' && b == b' && c == c' && d == d' && e == e'
```

### A17 × A01 — tree zipper (M4)
Per-node moves up/left/right; crumb trail records the path.

## See also

**Combines with:** [A01 tree recursion](./A01-tree-recursion.md) · [A06 functor instance](./A06-functor-instance.md)
**Question families:** [tree-transform](../question-families/tree-transform-family.md)
**Theory:** [tree zipper](../trees/tree-zipper.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
