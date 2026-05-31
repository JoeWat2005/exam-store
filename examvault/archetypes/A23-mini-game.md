<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A23 — Generalised Mini-Game (Nim / TTT / Conway) (NEW)**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · **A23** · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A23 — Generalised Mini-Game (Nim / TTT / Conway) (NEW)

**Tier:** 2   |   **Stars:** ⭐⭐⭐⭐
**Mock appearance:** Q3 (Nim) + Q4 (TTT-ish setup)   |   **Assignment appearance:** A3 (game-like scheduler), A1 (board-based)
**Combines with:** A02 · A04 · A01 · A21
**Search keywords:** game · Nim · TTT · tic-tac-toe · Conway · board · move · turn · player · winner · gameOver

## Justification for inclusion as its own archetype
The Mock test has TWO game-related questions (Q3 Nim, Q4 magic square aka board predicate). Problem 150 is TTT winner. Combined with Conway's Game of Life from Week 1 lecture and the round-robin scheduler in A3 Q3, "game state" is a course-wide pattern. While A02 covers the State-monad mechanics and A04 covers the grid predicate, neither covers the FULL game shape: `data Player`, `type Board`, `winner :: Board -> Maybe Player`, `move :: Move -> Board -> Maybe Board`, `validMoves :: Board -> [Move]`. This deserves a unifying archetype.

## What it tests
Whether you can structure a complete tiny game: define the player/board/move types, write `winner` / `gameOver` predicates, write `applyMove` validation, and produce `validMoves` for enumeration. The exam version drops one of these as a 10-mark question.

## Recognition triggers
- "the game of Nim", "tic-tac-toe", "Conway's Game of Life", "minesweeper"
- `data Player = X | O` or similar
- `type Board = [[Maybe Player]]` or `(Int, Int)` (Nim) or `Set (Int, Int)` (Conway)
- "the player whose turn it is", "the game is over when …"
- "Write a function `winner :: Board -> Maybe Player`"
- "Write a function `move :: Move -> Board -> Maybe Board`"
- Combination of A02 + A04 patterns

## Canonical template
```haskell
data Player = X | O deriving (Eq, Show)
type Cell   = Maybe Player
type Grid   = [[Cell]]
data Move   = Move Int Int   -- row, col

winner :: Grid -> Maybe Player
winner g = ...                -- A04 territory

applyMove :: Player -> Move -> Grid -> Maybe Grid
applyMove p (Move r c) g
  | not (validCoord g r c)        = Nothing
  | not (cellEmpty g r c)         = Nothing
  | otherwise                     = Just (updateGrid r c (Just p) g)

validMoves :: Grid -> [Move]
validMoves g = [Move r c | (r, row) <- zip [0..] g
                          , (c, cell) <- zip [0..] row
                          , cell == Nothing]
```

## Mutations (the examiner picks one)

### M1 — TTT `winner` (problem 150)
```haskell
import Data.List (transpose)

winner :: [[Maybe Player]] -> Maybe Player
winner g =
  let rows = g
      cols = transpose g
      d1   = zipWith (!!) g [0..]
      d2   = zipWith (!!) (reverse g) [0..]
  in firstWin (rows ++ cols ++ [d1, d2])
  where
    firstWin []     = Nothing
    firstWin (l:ls) = case threeSame l of Just p -> Just p; Nothing -> firstWin ls
    threeSame [Just p, Just q, Just r] | p == q && q == r = Just p
    threeSame _                                            = Nothing
```
What changes: A04 mutation specialised to 3-in-a-row.

### M2 — Nim `gameOver` and `takeTokens` (Mock Q3 — see A02)
```haskell
gameOver :: NimGame Bool
gameOver = do (a, b) <- get; return (a == 0 && b == 0)

takeTokens :: Int -> Heap -> NimGame ()
takeTokens n First  = modify (\(a, b) -> (max 0 (a - n), b))
takeTokens n Second = modify (\(a, b) -> (a, max 0 (b - n)))
```
What changes: state-monad game; A02 territory.

### M3 — Conway one-step
```haskell
type Coord  = (Int, Int)
type Board  = [Coord]    -- list of live cells

neighbours :: Coord -> [Coord]
neighbours (x, y) = [(x+dx, y+dy) | dx <- [-1..1], dy <- [-1..1], (dx,dy) /= (0,0)]

step :: Board -> Board
step b = [c | c <- candidates, lives c]
  where
    candidates = nub (b ++ concatMap neighbours b)
    n c = length [c' | c' <- neighbours c, c' `elem` b]
    lives c
      | c `elem` b  = n c `elem` [2, 3]    -- survival
      | otherwise   = n c == 3              -- birth
```
What changes: rules differ; uses set-style operations.

### M4 — `validMoves` for TTT
```haskell
validMoves :: Grid -> [(Int, Int)]
validMoves g = [(r, c) | (r, row) <- zip [0..] g
                       , (c, cell) <- zip [0..] row
                       , cell == Nothing]
```
What changes: A21 list-comp; enumerates empty positions.

### M5 — `applyMove` with validation
```haskell
data Move = Place Int Int

applyMove :: Player -> Move -> Grid -> Maybe Grid
applyMove p (Place r c) g
  | r < 0 || r >= length g            = Nothing
  | c < 0 || c >= length (head g)     = Nothing
  | g !! r !! c /= Nothing            = Nothing
  | otherwise                         = Just (updateAt r (updateAt c (const (Just p))) g)
  where updateAt i f xs = [if k == i then f x else x | (k, x) <- zip [0..] xs]
```
What changes: returns `Maybe` for legality.

### M6 — `playGame` driver
```haskell
playGame :: Grid -> Player -> [Move] -> Maybe (Maybe Player)
playGame g _ []     = Just (winner g)
playGame g p (m:ms) = case applyMove p m g of
                       Nothing -> Nothing
                       Just g' -> case winner g' of
                                    Just w  -> Just (Just w)
                                    Nothing -> playGame g' (other p) ms
  where other X = O
        other O = X
```
What changes: sequential play; alternation; short-circuit on win.

### M7 — Minimax (extreme variant)
```haskell
score :: Grid -> Int
score g = case winner g of
            Just X  -> 1
            Just O  -> -1
            Nothing -> 0

minimax :: Player -> Grid -> Int
minimax p g | gameOver g = score g
            | p == X     = maximum [minimax O g' | m <- validMoves g, Just g' <- [applyMove X m g]]
            | otherwise  = minimum [minimax X g' | m <- validMoves g, Just g' <- [applyMove O m g]]
```
What changes: full game search; combinable with A18 for memoisation.

### M8 — `gameOver` for any board (predicate vs winner)
```haskell
gameOver :: Grid -> Bool
gameOver g = winner g /= Nothing || null (validMoves g)
```
What changes: combines two earlier sub-functions.

### M9 — Nim with N heaps (generalisation)
```haskell
type NimN = State [Int]

takeN :: Int -> Int -> NimN ()
takeN heap n = modify (zipWith adjust [0..])
  where adjust i x | i == heap = max 0 (x - n)
                   | otherwise = x

gameOverN :: NimN Bool
gameOverN = do hs <- get; return (all (== 0) hs)
```
What changes: generalises Mock Q3 to arbitrary number of heaps.

### M10 — `Battleship` hit-or-miss
```haskell
data Cell = Empty | Ship | Hit | Miss

shootAt :: (Int, Int) -> [[Cell]] -> [[Cell]]
shootAt (r, c) b = [ [ if (i, j) == (r, c)
                       then hitOrMiss cell
                       else cell
                     | (j, cell) <- zip [0..] row ]
                   | (i, row) <- zip [0..] b ]
  where hitOrMiss Ship = Hit
        hitOrMiss x    = Miss   -- including already-hit
```
What changes: small update operator on a grid; not a winner game but same shape.

## Minimax deep dive (M7 expanded — old-vault content ported)

The classic game-AI algorithm. Birmingham's tic-tac-toe lecture (`tictactoe.md`, 27 KB, 6 video lectures) builds this from scratch. It's also Problem 150's natural follow-up. Worth knowing because (a) it's a clean application of A01 (game tree IS a recursive ADT), (b) it composes A18 memoisation, (c) Q5 of an exam could ask for any of: scoring, game-tree construction, best-move extraction, depth-limited variant.

> **Lecture variant (Hutton formulation) — match this shape if you're given the lecture scaffold.** Hutton's tic-tac-toe uses a 3-valued player type with the ordering `data Player = O | B | X deriving (Eq, Ord, Show)` — crucially **`O < B < X`**, so `minimum`/`maximum` on labels directly pick O's and X's best outcomes (B = blank/draw sits between). The pipeline is four named functions:
> - `gametree :: Grid -> Player -> Tree Grid` — build the full move tree (a rose `Tree a = Node a [Tree a]`).
> - `prune :: Int -> Tree a -> Tree a` — cut the tree to a depth (TTT needs no pruning; bigger games do).
> - `minimax :: Tree Grid -> Tree (Grid, Player)` — label every node with its eventual best `Player`: a leaf is its own winner (`O`/`X`/`B`); a `Node` whose turn is O takes `minimum` of its children's labels, otherwise `maximum`.
> - `bestmove :: Grid -> Player -> Grid` — run `minimax (gametree g p)`, read the root label, and return a child grid whose label equals it.
>
> If the exam gives you `gametree`/`prune`/`minimax`/`bestmove` stubs with `O | B | X`, use THIS layout (labels are `Player`, not `Int` scores) rather than the `Int`-scoring `scoreTree`/`bestMove` version below — they are equivalent but the marker tests the named functions it gave you.

### The pure-functional minimax

```haskell
data GameTree = Leaf Int | Node Player [GameTree]
  -- Leaf carries a *terminal score*; Node carries the player-to-move + children.

-- 1. Build the game tree from a board.
gameTree :: Player -> Grid -> GameTree
gameTree p g
  | gameOver g = Leaf (score g)
  | otherwise  = Node p [ gameTree (other p) g'
                        | m <- validMoves g
                        , Just g' <- [applyMove p m g] ]
  where other X = O; other O = X

-- 2. Score the tree.
scoreTree :: GameTree -> Int
scoreTree (Leaf s)    = s
scoreTree (Node X cs) = maximum (map scoreTree cs)      -- X wants to maximise
scoreTree (Node O cs) = minimum (map scoreTree cs)      -- O wants to minimise

-- 3. Best move at the root.
bestMove :: Player -> Grid -> Maybe Move
bestMove p g
  | gameOver g = Nothing
  | otherwise  = Just (snd (best [ (scoreTree (gameTree (other p) g'), m)
                                 | m <- validMoves g
                                 , Just g' <- [applyMove p m g] ]))
  where best = if p == X then maximumBy (comparing fst) else minimumBy (comparing fst)
        other X = O; other O = X
```

**Why this split is good:** `gameTree` is a structural recursion (A01). `scoreTree` is a fold over the tree (A10). `bestMove` is just argmax/argmin over the children. **Three small functions, each one shape from the archetype catalogue.**

### Depth-limited minimax (for Conway-sized boards)

The full game tree of TTT has ~250 000 nodes (fast). For Connect-4 it's 1.6 × 10^12 (impossible). Cap the depth and use a heuristic at the cap:

```haskell
gameTreeD :: Int -> Player -> Grid -> GameTree
gameTreeD 0 _ g            = Leaf (heuristic g)
gameTreeD d p g
  | gameOver g             = Leaf (score g)
  | otherwise              = Node p [ gameTreeD (d - 1) (other p) g'
                                    | m <- validMoves g
                                    , Just g' <- [applyMove p m g] ]
  where other X = O; other O = X

-- heuristic: count "two-in-a-row with an open third" for X minus for O.
heuristic :: Grid -> Int
heuristic _ = 0    -- problem-specific; leave as TODO for student
```

### Alpha-beta pruning (the optimisation worth knowing)

Stop exploring a branch once you've proved it can't improve on what we've already found. Doesn't change the answer, just speeds it up dramatically.

```haskell
alphabeta :: Int -> Int -> GameTree -> Int
alphabeta a b (Leaf s)    = s
alphabeta a b (Node X cs) = go a b cs
  where go a b []      = a
        go a b (c:cs)
          | a' >= b   = a'       -- beta cut
          | otherwise = go a' b cs
          where a' = max a (alphabeta a b c)
alphabeta a b (Node O cs) = go a b cs
  where go a b []      = b
        go a b (c:cs)
          | a >= b'   = b'       -- alpha cut
          | otherwise = go a b' cs
          where b' = min b (alphabeta a b c)

bestMoveAB :: Player -> Grid -> Maybe Move
bestMoveAB p g
  | gameOver g = Nothing
  | otherwise  = Just (snd (bst [ (alphabeta (-2) 2 (gameTree (other p) g'), m)
                                | m <- validMoves g, Just g' <- [applyMove p m g] ]))
  where bst = if p == X then maximumBy (comparing fst) else minimumBy (comparing fst)
        other X = O; other O = X
```

Initial `a` / `b` bounds for TTT: `-2` to `2` (scores are -1, 0, 1; -2/2 are safely outside).

### Memoised minimax (A23 × A18)

If the same board can be reached by multiple move sequences (Connect-4, draughts), `gameTree` recomputes — exponential blow-up. Memoise on the board:

```haskell
import Data.List (lookup)

type Memo = [(Grid, Int)]

memoMinimax :: Player -> Grid -> (Int, Memo)
memoMinimax p g = go p g []
  where
    go p g memo = case lookup g memo of
      Just s  -> (s, memo)
      Nothing -> let (s, memo') = compute p g memo
                 in (s, (g, s) : memo')
    compute p g memo
      | gameOver g = (score g, memo)
      | otherwise  = (combine p [s | m <- validMoves g
                                   , Just g' <- [applyMove p m g]
                                   , let (s, _) = go (other p) g' memo], memo)
    combine X = maximum
    combine O = minimum
    other X = O; other O = X
```

(Production code uses `Data.Map` for O(log n) lookup, but `Data.Map` is NOT allowed under Safe — assoc-list with `lookup` is.)

### QuickCheck properties

```haskell
prop_score_terminal :: Grid -> Property
prop_score_terminal g = gameOver g ==> score g `elem` [-1, 0, 1]

prop_bestMove_legal :: Player -> Grid -> Property
prop_bestMove_legal p g = not (gameOver g) ==>
  case bestMove p g of
    Just m  -> applyMove p m g /= Nothing
    Nothing -> False    -- shouldn't happen if game isn't over

prop_alphabeta_matches_naive :: Player -> Grid -> Bool
prop_alphabeta_matches_naive p g =
  alphabeta (-2) 2 (gameTree p g) == scoreTree (gameTree p g)
```

The third one is the key insight: alpha-beta is just an **optimisation** that produces the same answer. The property tests this exactly.

### Common bugs

- **Empty `[]` from `validMoves`** when board is full → `maximum []` crashes. Guard with `null (validMoves g) → score g`.
- **Player alternation lost** during recursion → minimax picks for the wrong player at each level. Pass `(other p)` to the recursive call.
- **`bestMove` returns "wrong" tie-breaks** — when two moves have equal score, the marker may expect the first. Use `maximumBy` with a stable comparator.
- **Memo table key includes the player** — same board, different player to move = different value. Key should be `(Grid, Player)` not just `Grid`.

## Worked examples from this course
- Mock Q3: Nim — M2.
- Mock Q4: magic square — A04 territory but related "board predicate".
- Problem sheet Set 15 (#144): Nim repeated.
- Problem sheet Set 15 (#150): TTT `winner` — M1.
- Week 1 lecture: Conway's Game of Life animation.
- Assignment 1: Grid + tatami placement (game-like board manipulation).
- Assignment 3: roundRobin / schedule — game-like thread scheduling.

## QuickCheck attack surface
- **Initial board has no winner**: `winner (replicate 3 (replicate 3 Nothing)) == Nothing`.
- **Three-in-a-row row**: marker generates `[[Just X, Just X, Just X], [_,_,_], [_,_,_]]`, checks `Just X`.
- **Three-in-a-row anti-diagonal**: `[[_, _, Just X], [_, Just X, _], [Just X, _, _]]` → `Just X`. Anti-diag bug = 0 marks.
- **Block self-win**: TTT, if applyMove X (1,1) on `[[X,_,_], [_,_,_], [O,O,_]]` is valid → `Just X`.
- **Out-of-bounds move**: `applyMove X (5,5) g == Nothing`.
- **Move into occupied cell**: `applyMove X (0,0) board` where (0,0) is `Just O` → `Nothing`.
- **Player alternation**: in `playGame`, X moves on even index, O on odd.
- **`gameOver` on full board**: even without a winner, all-cells-filled → `True`.

## Pitfalls (marks-killers)
- **Forgetting the anti-diagonal**: A04 trap repeated.
- **Mutating instead of replacing**: Haskell lists are immutable; updateAt rebuilds.
- **Off-by-one in row/col indexing**: `g !! r !! c` — if board is 3x3, `r ∈ [0, 1, 2]`.
- **Validating after applying**: validate FIRST (`r < 0 || cell /= Nothing`), then apply. Don't apply then check.
- **Player alternation bug**: switching players inside the move function vs outside.
- **`Set Cell` for Conway vs `[[Cell]]` for TTT**: the rep matters; choose the one the spec gives.
- **Generation of `validMoves` includes filled cells**: needs `cell == Nothing` guard.

## Combines-with deep dive

### A23 × A02 — game in State monad
Nim is A23 × A02 wholesale (Mock Q3).

### A23 × A04 — winner via transpose
TTT winner is A23 × A04 wholesale (problem 150).

### A23 × A21 — list-comp for valid moves
See M4. Standard pattern.

### A23 × A01 — game tree for minimax
The game tree is a recursive ADT: `data GameTree = Leaf Score | Branch Player [GameTree]` — A01 territory.

## See also

**Combines with:** [A02 state game](./A02-state-game.md) · [A03 generic monad](./A03-generic-monad.md)
**Question families:** [state-game](../question-families/state-game-family.md) · [state-counter](../question-families/state-counter-family.md)
**Cross-topic:** [game-state](../cross-matrix/game-state.md)
**Theory:** [State monad](../monads/state.md)
**QuickCheck:** [state attacks](../quickcheck/state-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
