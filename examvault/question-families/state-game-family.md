<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: state-game**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · **state-game** · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: state-game

**Archetype:** A02 (State Monad Game / Simulation)   |   **Stars:** ⭐⭐⭐⭐   |   **Course week(s):** 10
**Search keywords:** State, NimGame, gameOver, takeTokens, TicTacToe, Conway, cards, fresh, label, runState, execState

## Generator template
```haskell
import Control.Monad.State

-- The seed: a State action that reads (get), inspects, writes (put), returns
-- a result. The "world" is a domain object (board, deck, counter, log).
type Game a = State World a

action :: Game ResultType
action = do
  w <- get
  let (result, w') = step w
  put w'
  return result
```

Every mutation in this family is "pick a World, pick a step rule, return either Bool, Int, or ()".

## Mutations (the examiner picks one)

### Mutation 1 — gameOver (= mock Q3 part 1)
**Spec:** Predicate: both heaps in Nim are zero.
**Sig:** `gameOver :: NimGame Bool`
**Solution:**
```haskell
type NimBoard = (Int, Int)
type NimGame  = State NimBoard

gameOver :: NimGame Bool
gameOver = do
  (h1, h2) <- get
  return (h1 == 0 && h2 == 0)
```
**QC trap:** `runState gameOver (0,0) == (True, (0,0))`. State unchanged — `get` doesn't write.

### Mutation 2 — takeTokens (= mock Q3 part 2)
**Spec:** Remove `i` tokens from heap `h`, never go below 0.
**Sig:** `takeTokens :: Int -> Heap -> NimGame ()`
**Solution:**
```haskell
data Heap = First | Second

takeTokens :: Int -> Heap -> NimGame ()
takeTokens i h = do
  (h1, h2) <- get
  case h of
    First  -> put (max 0 (h1 - i), h2)
    Second -> put (h1, max 0 (h2 - i))
```
**QC trap:** Use `max 0 (h - i)` to clamp. Don't use `if i > h then 0 else h - i` (works but less idiomatic). Negative `i` *adds* tokens — usually not intended; check spec.

### Mutation 3 — fresh (= problem 111)
**Spec:** Read the current counter, increment, return the old value.
**Sig:** `fresh :: State Int Int`
**Solution:**
```haskell
fresh :: State Int Int
fresh = do
  n <- get
  put (n + 1)
  return n
```
Or as a one-liner: `fresh = state (\n -> (n, n + 1))`.
**QC trap:** Returns the *old* value, not the new one. Classic post-increment vs pre-increment confusion.

### Mutation 4 — labelTree (= problem 112)
**Spec:** Label every value in a binary tree with a unique increasing integer, in-order.
**Sig:** `labelTree :: BT a -> BT (Int, a)`
**Solution:**
```haskell
labelTree :: BT a -> BT (Int, a)
labelTree t = evalState (go t) 0
  where
    go Empty        = return Empty
    go (Fork v l r) = do
      l' <- go l
      i  <- fresh
      r' <- go r
      return (Fork (i, v) l' r')
```
**QC trap:** Order of monadic actions defines the label order. In-order means `l' <- ...; i <- fresh; r' <- ...`. Pre-order would have `i <- fresh` first.

### Mutation 5 — pushAll (= problem 114)
**Spec:** Push every element onto the state-stack in order.
**Sig:** `pushAll :: [a] -> State [a] ()`
**Solution:**
```haskell
pushAll :: [a] -> State [a] ()
pushAll []     = return ()
pushAll (x:xs) = do
  modify (x:)
  pushAll xs
```
**QC trap:** Final stack has elements in *reverse* push order — last-pushed is at the top.

### Mutation 6 — fibState (= problem 117)
**Spec:** Run `n` steps of Fibonacci with state `(prev, curr)`.
**Sig:** `fibState :: Int -> State (Int, Int) ()`
**Solution:**
```haskell
fibState :: Int -> State (Int, Int) ()
fibState 0 = return ()
fibState n = do
  (a, b) <- get
  put (b, a + b)
  fibState (n - 1)
```
**QC trap:** Initial state should be `(0, 1)`. After `n` steps, state is `(fib n, fib (n+1))`. Off-by-one mistakes common.

### Mutation 7 — evalCalc / stack calculator (= problem 118)
**Spec:** Execute a sequence of stack-machine commands; state is the value stack.
**Sig:** `calc :: [CalcCmd] -> State [Int] ()`
**Solution:**
```haskell
data CalcCmd = Push Int | Add | Sub | Mul

calc :: [CalcCmd] -> State [Int] ()
calc []            = return ()
calc (Push n : cs) = modify (n :) >> calc cs
calc (Add    : cs) = binop (+) >> calc cs
calc (Sub    : cs) = binop (-) >> calc cs
calc (Mul    : cs) = binop (*) >> calc cs

binop :: (Int -> Int -> Int) -> State [Int] ()
binop op = do
  s <- get
  case s of
    (x:y:rest) -> put (op y x : rest)
    _          -> return ()
```
**QC trap:** Operand order matters: for `Sub`, `[2,5]` (top to bottom) gives `5 - 2 = 3`, not `2 - 5`. Empty / one-element stack on binary op crashes — exam may want a Maybe-valued version.

### Mutation 8 — uniqueIds (= problem 119)
**Spec:** Assign each string a unique id using State as counter.
**Sig:** `uniqueIds :: [String] -> State Int [(String, Int)]`
**Solution:**
```haskell
uniqueIds :: [String] -> State Int [(String, Int)]
uniqueIds []     = return []
uniqueIds (s:ss) = do
  i  <- fresh
  ys <- uniqueIds ss
  return ((s, i) : ys)
```
**QC trap:** `mapM (\s -> do i <- fresh; return (s,i)) ss` is equivalent and shorter. Both correct.

### Mutation 9 — TicTacToe winner (= problem 150)
**Spec:** Find the winning Player given a Grid; no state actually needed but variants thread State.
**Sig:** `winner :: Grid -> Maybe Player`
**Solution:**
```haskell
import Data.List (transpose)

data Player = X | O deriving (Eq, Show)
type Grid   = [[Maybe Player]]

winner :: Grid -> Maybe Player
winner g = case filter isWin allLines of
             (line:_) -> head line
             _        -> Nothing
  where
    allLines = g ++ transpose g ++ diags g
    diags m  = [zipWith (!!) m [0..], zipWith (!!) m [length m - 1, length m - 2 .. 0]]
    isWin [Just p, Just q, Just r] = p == q && q == r
    isWin _                        = False
```
**QC trap:** Generalising to `n × n` is a frequent follow-up. Watch for off-by-one in diagonals.

### Mutation 10 — Conway one step (= advanced — appears in problem-sheet Week 5)
**Spec:** Apply one Conway's Life step to a grid.
**Sig:** `conwayStep :: [[Bool]] -> [[Bool]]`
**Solution:**
```haskell
conwayStep :: [[Bool]] -> [[Bool]]
conwayStep g =
  [ [ liveNext alive (countLive r c)
    | (c, alive) <- zip [0..] row ]
  | (r, row) <- zip [0..] g ]
  where
    h = length g
    w = if null g then 0 else length (head g)
    at r c | 0 <= r && r < h && 0 <= c && c < w = g !! r !! c
           | otherwise                          = False
    countLive r c = length [ () | dr <- [-1,0,1], dc <- [-1,0,1]
                                , (dr, dc) /= (0,0), at (r+dr) (c+dc) ]
    liveNext True  n = n == 2 || n == 3
    liveNext False n = n == 3
```
**QC trap:** `at` must handle out-of-bounds (treat as dead). Don't include the cell itself in the neighbour count.

## Hidden-predicate mutations
- "stop when predicate holds" → `whileM p action`:
```haskell
whileM :: Monad m => m Bool -> m a -> m ()
whileM cond act = do
  b <- cond
  when b (act >> whileM cond act)
```
- "tally how many actions ran" → State that's a pair (game-state, counter).

## Accumulator-style alternative
For deterministic state machines, you can dodge the monad entirely:
```haskell
calcPure :: [CalcCmd] -> [Int] -> [Int]
calcPure []         st     = st
calcPure (Push n:cs) st    = calcPure cs (n : st)
calcPure (Add   :cs) (x:y:r) = calcPure cs (y + x : r)
-- etc.
```
The exam usually mandates State, but mixing styles helps debug.

## Fold-style alternative
A list-of-commands processor is naturally `foldM`:
```haskell
calcFold :: [CalcCmd] -> State [Int] ()
calcFold = mapM_ step
  where
    step (Push n) = modify (n :)
    step Add      = modify (\(x:y:r) -> y + x : r)
    step Sub      = modify (\(x:y:r) -> y - x : r)
    step Mul      = modify (\(x:y:r) -> y * x : r)
```
Cleaner; pick this if the examiner says "use `mapM_`".

## Cross-family combinations
- this family + `tree-counting-family.md` → `countLeaves :: BT a -> State Int ()` (problem 113)
- this family + `tree-transform-family.md` → `labelTree` (mutation 4 above)
- this family + `writer-trace-family.md` → State+Writer interpreter
- this family + `error-handling-family.md` → StateT over Maybe for "fail any time"

## QuickCheck universal attacks
- **Empty world / zero counter:** every action should leave it consistent.
- **`gameOver` after `takeTokens`:** if you take everything, the game is over.
- **Two reads in a row:** `do x <- get; y <- get; return (x == y)` — must always be True.
- **`put x >> get == put x >> return x`** — get returns whatever was last put.
- **State law:** `get >>= put == return ()`.
- **Replay determinism:** running the same actions on the same start state gives the same end state — pure!

## Pitfalls (per mutation)
- M1: forgetting that `get` doesn't change state.
- M2: returning negative tokens; not using `max 0`.
- M3: returning the *new* counter instead of old.
- M4: order of `<-` lines determines labelling order — easy to misalign.
- M5: stack grows in wrong order if you misorder `modify`.
- M6: missing the 0 base case → infinite loop.
- M7: operand order on Sub/Div.
- M8: forgetting to use `fresh` (writing `i = 0` accidentally).
- M9: confusing rows / columns / diagonals indices.
- M10: out-of-bounds neighbours; counting the cell itself.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — takeTokensWithLog (State + Writer fused — tuple form)

**Spec:** Take `n` tokens from a player; log the action; mutate the game state. Returns the action description in a log alongside the new state.

**Type sig:** `takeTokensWithLog :: Int -> Heap -> NimBoard -> (NimBoard, [String])`

Operate directly on the board (`NimBoard = (Int, Int)`) and pattern-match the
existing `Heap` (`First`/`Second`). Returns the new board plus a one-line log.
(Don't use `NimGame` here — `NimGame = State NimBoard` is a *type*, not a value
you can pass or return.)

```haskell
takeTokensWithLog :: Int -> Heap -> NimBoard -> (NimBoard, [String])
takeTokensWithLog n First  (a, b) =
  let a' = max 0 (a - n)
  in ((a', b), ["P1 took " ++ show n ++ " from heap A, now " ++ show a'])
takeTokensWithLog n Second (a, b) =
  let b' = max 0 (b - n)
  in ((a, b'), ["P2 took " ++ show n ++ " from heap B, now " ++ show b'])
```

**What changes vs seed:** Effect stack changes: adds a Writer-style log alongside the State. Tuple form because `Control.Monad.Writer` mixed with `Control.Monad.State` is awkward without transformers.

**QC trap:** Log should reflect the CLAMPED value (`a'`), not the requested deduction (`n`). Taking 5 from a heap of 3 should log "now 0", not "took 5".

### Mutation 12 — rewindMove (undo by replaying prefix — different data layout)

**Spec:** Given a history list of moves and a starting state, return the state after every prefix. Lets you 'rewind' to any earlier point.

**Type sig:** `rewindMoves :: [(Int, Heap)] -> NimBoard -> [NimBoard]`

Operate on the board (`NimBoard = (Int, Int)`) and the family's `Heap`
(`First`/`Second`). `NimGame = State NimBoard` is a type of kind `* -> *`, so
`NimGame -> [NimGame]` is a kind error — and there is no `Player` type in this
family. Thread the raw board through `scanl` instead.

```haskell
rewindMoves :: [(Int, Heap)] -> NimBoard -> [NimBoard]
rewindMoves moves s0 = scanl step s0 moves
  where
    step s (n, h) = case h of
      First  -> let (a, b) = s in (max 0 (a-n), b)
      Second -> let (a, b) = s in (a, max 0 (b-n))
```

**What changes vs seed:** Data layout changes: history is `[(Int, Heap)]` not a single move, and the result is a *list* of states (`scanl` pattern) rather than one.

**QC trap:** `scanl` includes the initial state; if the marker expects `[s1, s2, …]` (post-move only) you need `scanl1` or `tail . scanl …`. Off-by-one is the marker bait.

## See also

**Primary archetype:** [A02 state game](../archetypes/A02-state-game.md)
**Sibling families:** [state-counter](./state-counter-family.md)
**Cross-topic:** [game-state](../cross-matrix/game-state.md) · [rose × state](../cross-matrix/rose-x-state.md) · [tree × state](../cross-matrix/tree-x-state.md)
**Theory:** [state](../monads/state.md)
**QuickCheck:** [state attacks](../quickcheck/state-attacks.md)
**Pitfalls:** [P-006 Mock Q3 gameOver(0,0)](../pitfalls/HIGH-severity.md#p-006) · [P-024 state action wrong type](../pitfalls/HIGH-severity.md#p-024)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
