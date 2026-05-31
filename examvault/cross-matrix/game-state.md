<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Game × State (Nim, TTT, Conway, generalised)**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · **game-state** · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Game × State (Nim, TTT, Conway, generalised)

**Why this combo:** any state machine — Nim, Tic-Tac-Toe, Conway's Life, a tiny adventure game — is naturally modelled in State. The State is the board; each action is a `State Board ()` (or `State Board Result`). The course's MockTest Q3 was Nim over State; the lecture's Conway's-life is the same shape on a grid.

**Recognition triggers:**
- "Implement the game logic"
- "Take an action and update the state"
- "Check if the game is over"
- "Compute next generation / next turn"
- Custom type synonym `type GameMonad a = State Board a`.

**Search keywords:** game State, NimGame, TicTacToe State, Conway State, State Board, takeTokens, gameOver, modify board

## Pattern (Nim — the MockTest Q3 idiom)

```haskell
import Control.Monad.State

type NimBoard = (Int, Int)        -- two heaps
type NimGame a = State NimBoard a

data Heap = First | Second

-- Is the game over?
gameOver :: NimGame Bool
gameOver = do
  (h1, h2) <- get
  return (h1 == 0 && h2 == 0)

-- Take i tokens from heap h (saturating at 0)
takeTokens :: Int -> Heap -> NimGame ()
takeTokens i h = do
  (h1, h2) <- get
  case h of
    First  -> put (max 0 (h1 - i), h2)
    Second -> put (h1, max 0 (h2 - i))
```

Run with `runState`, `evalState`, or `execState`:
```haskell
runState (do takeTokens 2 First; gameOver) (3, 2)
  -- ((False), (1, 2))
```

## Worked variants

### Tic-Tac-Toe state machine

```haskell
data Cell  = E | X | O    deriving (Eq, Show)
type Board = [[Cell]]      -- 3x3

type TTT a = State Board a

emptyBoard :: Board
emptyBoard = replicate 3 (replicate 3 E)

placeMark :: Cell -> (Int, Int) -> TTT Bool
placeMark m (r, c) = do
  board <- get
  let row    = board !! r
      curCol = row !! c
  if curCol /= E
    then return False     -- illegal
    else do
      let newRow   = take c row ++ [m] ++ drop (c+1) row
          newBoard = take r board ++ [newRow] ++ drop (r+1) board
      put newBoard
      return True

isWin :: Cell -> TTT Bool
isWin m = do
  b <- get
  return $ any (all (== m)) (rows b ++ cols b ++ diagonals b)
  where
    rows       = id
    cols       = transpose
    diagonals b = [[b!!i!!i | i <- [0..2]], [b!!i!!(2-i) | i <- [0..2]]]
```

### Conway's Life (board evolution)

```haskell
type Cells = [[Bool]]
type Life  = State Cells

step :: Life ()
step = do
  cs <- get
  let next = [[stepCell cs r c | c <- [0..width-1]] | r <- [0..height-1]]
  put next

stepCell :: Cells -> Int -> Int -> Bool
stepCell cs r c =
  let alive = neighbours cs r c
  in case (cs !! r !! c, alive) of
       (True,  n) | n == 2 || n == 3 -> True
       (False, 3)                    -> True
       _                             -> False
```

### Adventure-game step

```haskell
data RoomState = Room { health :: Int, gold :: Int, inv :: [String] }

type Adventure a = State RoomState a

takeDamage :: Int -> Adventure ()
takeDamage n = modify (\s -> s { health = health s - n })

collect :: String -> Adventure ()
collect item = modify (\s -> s { inv = item : inv s })

isAlive :: Adventure Bool
isAlive = gets ((> 0) . health)
```

### Generic game loop (drive a State by an input list)

```haskell
runMoves :: [m] -> (m -> State s ()) -> State s ()
runMoves moves apply = mapM_ apply moves

-- Or with foldM:
playGame :: [Heap] -> NimGame Bool
playGame moves = do
  mapM_ (takeTokens 1) moves
  gameOver

-- Drive:
evalState (playGame [First, Second, First, First]) (3, 2)
```

### Score-tracking + game state (tuple state)

```haskell
type ScoredGame = State (Board, Int)        -- board + score

gainPoints :: Int -> ScoredGame ()
gainPoints n = modify (\(b, s) -> (b, s + n))
```

### Multi-player turn (cycle over players)

```haskell
data Player = P1 | P2 deriving (Eq, Show)

nextPlayer :: Player -> Player
nextPlayer P1 = P2
nextPlayer P2 = P1

type Turn   = State (Player, NimBoard)

playTurn :: Int -> Heap -> Turn Bool
playTurn i h = do
  (p, b) <- get
  let (h1, h2) = b
      b' = case h of
             First  -> (max 0 (h1 - i), h2)
             Second -> (h1, max 0 (h2 - i))
  put (nextPlayer p, b')
  return (b' == (0, 0))
```

## Mutations

- **Game shape**: Nim / TTT / Life / adventure / arcade.
- **Board representation**: tuple / list of lists / Map / custom.
- **State contains**: board only / board + score / board + turn / board + log.
- **Combine with Writer** for game log; with Reader for config.
- **Conditional turn**: `when (not over) $ do ...`.

## QuickCheck attacks

```haskell
-- gameOver true iff both heaps zero
prop_gameOver :: NimBoard -> Bool
prop_gameOver b = evalState gameOver b == (fst b == 0 && snd b == 0)

-- takeTokens never makes a heap negative
prop_takeTokens_clamped :: NimBoard -> Int -> Heap -> Bool
prop_takeTokens_clamped b i h =
  let (h1', h2') = execState (takeTokens i h) b
  in h1' >= 0 && h2' >= 0

-- Sum of heaps after takeTokens is at most original sum
prop_takeTokens_monotone :: NimBoard -> Int -> Heap -> Bool
prop_takeTokens_monotone b i h =
  let (h1', h2') = execState (takeTokens i h) b
      (h1, h2)   = b
  in h1' + h2' <= h1 + h2

-- Idempotent: gameOver in a finished board stays True after any (legal) move
-- (only meaningful if takeTokens does nothing when both zero)
```

## Pitfalls

- **Negative heaps.** `max 0 (h - i)` is the clamp idiom — forgetting it lets `takeTokens 5 (3,0) First` give `(-2, 0)`.
- **`get` THEN `put`**: don't `put (... get ...)` (that's `modify`).
- **`modify`** is cleaner: `modify (\(h1, h2) -> (max 0 (h1-i), h2))`.
- **Initial state**: `runState (...) (3, 2)`, NOT just `runState (...)`. Two args.
- **`evalState` for "result of game"**, `execState` for "final board", `runState` for both.
- **Multiple players**: must track who's whose turn — usually in state.
- **`type GameMonad a = State Board a`** — using type alias makes signatures readable.
- **`gameOver` is a query, not an action** — returns Bool, doesn't change state.

## Game state vs other state uses

| | Game state | Counter state | Cell store |
|---|---|---|---|
| What's in s | board, score, turn | int | map of vars |
| Reads via | get / gets | get | lookup |
| Updates via | put / modify | modify (+1) | modify (insert) |
| Read by | gameOver, isWin | display | eval Var |

## See also

**Combined archetypes:** [A02 state game](../archetypes/A02-state-game.md) · [A23 mini-game](../archetypes/A23-mini-game.md)
**Theory:** [State](../monads/state.md)
**Question families:** [state-game](../question-families/state-game-family.md) · [state-counter](../question-families/state-counter-family.md)
**QuickCheck:** [state attacks](../quickcheck/state-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
