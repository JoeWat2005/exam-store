<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A02 — State Monad Game / Simulation**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · **A02** · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A02 — State Monad Game / Simulation

**Tier:** 1   |   **Stars:** ⭐⭐⭐⭐⭐
**Mock appearance:** Q3   |   **Assignment appearance:** A3 (Q3, Q4 with Free)
**Combines with:** A03 · A14 · A15 · A23
**Search keywords:** State · get · put · modify · runState · execState · evalState · NimGame · gameOver · move

## What it tests
Whether you can model a board/game/counter as state, write predicate functions (`StateMonad Bool`) and action functions (`StateMonad ()`), and pick the right runner — without ever writing the state-threading by hand.

## Recognition triggers
- "We will play this inside a state monad …"
- "the state of the game is …"
- type signature shape: `State S a`, or a `type GameM a = State S a` alias
- "Write a function `gameOver :: GameM Bool` which decides …"
- "Write a function `move :: P -> GameM ()` which changes the state …"
- The question shows a `data Heap = First | Second` or similar — the move function will pattern-match on it.
- `runState`, `execState`, `evalState` in the example trace.

## Canonical template
```haskell
import Control.Monad.State

type Board   = (Int, Int)           -- whatever state the game keeps
type GameM a = State Board a

gameOver :: GameM Bool
gameOver = do (a, b) <- get
              return (a == 0 && b == 0)

doMove :: Int -> Side -> GameM ()
doMove n First  = do (a, b) <- get; put (max 0 (a - n), b)
doMove n Second = do (a, b) <- get; put (a, max 0 (b - n))
```

## Mutations (the examiner picks one)

### M1 — Nim two-heap (Mock Q3)
```haskell
type NimGame a = State (Int,Int) a
data Heap      = First | Second

gameOver :: NimGame Bool
gameOver = do (a,b) <- get; return (a == 0 && b == 0)

takeTokens :: Int -> Heap -> NimGame ()
takeTokens n First  = modify (\(a,b) -> (max 0 (a - n), b))
takeTokens n Second = modify (\(a,b) -> (a, max 0 (b - n)))
```
What changes: nothing — this IS the canonical. Memorise. **Clamp at 0**.

### M2 — fresh counter (`fresh :: State Int Int`)
```haskell
fresh :: State Int Int
fresh = do n <- get; put (n + 1); return n
```
What changes: returns the OLD state, mutates to the new. Used as a name supply.

### M3 — stack-as-state (`pushAll`, `evalCalc`)
```haskell
pushAll :: [a] -> State [a] ()
pushAll = mapM_ (\x -> modify (x:))

popState :: State [a] (Maybe a)
popState = do s <- get
              case s of
                []     -> return Nothing
                (x:xs) -> put xs >> return (Just x)
```
What changes: state IS a list. Mutator uses `:`, popping does pattern-matching after `get`.

### M4 — average accumulator (problem 115)
```haskell
average :: [Double] -> Double
average xs = let (cnt, tot) = execState (mapM_ step xs) (0, 0.0)
             in tot / fromIntegral cnt
  where step x = modify (\(n, t) -> (n + 1, t + x))
```
What changes: the state is a pair `(count, total)`. Run with `execState` to get final state, then post-process.

### M5 — Fibonacci as repeated state step (problem 117)
```haskell
fibState :: Int -> State (Int, Int) ()
fibState 0 = return ()
fibState n = do (a, b) <- get
                put (b, a + b)
                fibState (n - 1)
```
What changes: explicit recursion driving the state forward. Reachable via `execState (fibState n) (0,1)`.

### M6 — stack calculator (problem 118)
```haskell
data CalcCmd = Push Int | AddC | SubC | MulC

calc :: [CalcCmd] -> State [Int] ()
calc = mapM_ step where
  step (Push n) = modify (n:)
  step AddC     = binop (+)
  step SubC     = binop (-)
  step MulC     = binop (*)
  binop op = do
    s <- get
    case s of
      (y:x:rest) -> put (op x y : rest)
      _          -> return ()
```
What changes: each command is a tiny state mutator; `mapM_` runs them in order.

### M7 — unique-id generator (problem 119)
```haskell
uniqueIds :: [String] -> State Int [(String, Int)]
uniqueIds []     = return []
uniqueIds (s:ss) = do i  <- get; put (i + 1)
                      rs <- uniqueIds ss
                      return ((s, i) : rs)
```
What changes: combines M2 (fresh) with list-recursion; returns mapping, not unit.

### M8 — sim with termination check inside (`rollUntil`)
```haskell
rollUntil :: Int -> State Int Int
rollUntil target = do r <- get
                      put (if r == 6 then 1 else r + 1)
                      if r == target then return 0
                                     else fmap (+1) (rollUntil target)
```
What changes: combine read with conditional recursive call; counter is the return value, state is the stream.

### M9 — labelling tree (A01 × A02)
```haskell
labelTree :: BT a -> State Int (BT (Int, a))
labelTree Empty        = return Empty
labelTree (Fork x l r) = do l' <- labelTree l
                            n  <- get; put (n + 1)
                            r' <- labelTree r
                            return (Fork (n, x) l' r')
```
What changes: state threads through a tree traversal; chosen traversal order determines numbering (in-order here).

### M10 — TTT move (A02 × A04)
```haskell
type Grid    = [[Maybe Player]]
type TttGame = State Grid

playMove :: (Int, Int) -> Player -> TttGame Bool
playMove (i,j) p = do g <- get
                      let g' = updateAt i (updateAt j (const (Just p))) g
                      put g'
                      return (winner g' == Just p)
  where updateAt k f xs = [if n == k then f x else x | (n, x) <- zip [0..] xs]
```
What changes: state is the board (2D), mutator picks one cell, return signals win.

## Worked examples from this course
- Mock Q3: `gameOver`, `takeTokens` — M1 wholesale.
- Problem sheet Set 12 (#111-120): `fresh`, `labelTree`, `countLeaves`, `pushAll`, `average`, `rollUntil`, `fibState`, `calc`, `uniqueIds`, `countOccurrences`.
- Problem sheet Set 15 (#144): Nim repeated.
- Assignment 3 Q3 (roundRobin) and Q4 (schedule): cooperative scheduler — state is the shared resource that threads read and write.

## QuickCheck attack surface
- **Negative argument** to take/move: `takeTokens (-3) First` — should NOT under-flow. The clamp `max 0 (...)` saves you.
- **Over-take**: `takeTokens 100 First` on heap `(5, 7)` — must end at `(0, 7)`, not `(-95, 7)`.
- **`gameOver` on initial state**: e.g. `runState gameOver (0,0) == (True, (0,0))`.
- **Both heaps need clamping** — if you wrote `(heap1 - i, heap2)` with no `max 0`, half the tests fail.
- **State threading**: `evalState (do takeTokens 3 First; takeTokens 2 First; get) (10, 5) == (5, 5)` — checks that consecutive moves see each other's writes.
- For label-tree variants: `length (flatten (labelTree t)) == size t` AND labels are all distinct.

## Pitfalls (marks-killers)
- **Forgetting `import Control.Monad.State`**: assignments forbid imports, so it's pre-imported in `Types.hs`. Mock & Assignment templates put it there; if you write your own helper file, add it.
- **`State a s` vs `State s a`**: `s` is the state, comes FIRST. `NimGame Bool` desugars to `State (Int,Int) Bool`.
- **Underflow on clamp**: `heap1 - i` when `i > heap1` gives a negative number. Use `max 0 (heap1 - i)`.
- **Runner confusion**: `runState` gives `(result, finalState)`, `evalState` gives `result`, `execState` gives `finalState`. Pick by what the question asks.
- **`modify` vs `get`/`put`**: `modify f = do s <- get; put (f s)`. Both fine; use whichever is cleaner.
- **Return type for action-only moves**: `()`, not `Bool`. `gameOver` returns `Bool`; `takeTokens` returns `()`.

## Combines-with deep dive

### A02 × A14 — state + error (calculator that can divide)
```haskell
divStep :: Int -> StateT Int (Either String) ()
divStep 0 = lift (Left "/0")
divStep n = modify (`div` n)
```

### A02 × A15 — state with trace log
```haskell
takeAndLog :: Int -> Heap -> StateT (Int,Int) (Writer [String]) ()
takeAndLog n h = do modify (apply n h)
                    tell ["took " ++ show n ++ " from " ++ show (heapName h)]
```

### A02 × A03 — generic `MonadState s m =>` movers
```haskell
takeTokens' :: MonadState (Int,Int) m => Int -> Heap -> m ()
takeTokens' n h = modify (apply n h)
```

## See also

**Combines with:** [A01 tree recursion](./A01-tree-recursion.md) · [A03 generic monad](./A03-generic-monad.md) · [A04 matrix predicate](./A04-matrix-predicate.md) · [A23 mini-game](./A23-mini-game.md)
**Question families:** [state-game](../question-families/state-game-family.md) · [state-counter](../question-families/state-counter-family.md)
**Cross-topic:** [rose × state](../cross-matrix/rose-x-state.md) · [tree × state](../cross-matrix/tree-x-state.md) · [bst × state](../cross-matrix/bst-x-state.md) · [game-state](../cross-matrix/game-state.md)
**Theory:** [State monad](../monads/state.md)
**Pitfalls:** [P-006 Mock Q3 gameOver(0,0)](../pitfalls/HIGH-severity.md#p-006) · [P-008 n<=0 not n==0](../pitfalls/HIGH-severity.md#p-008) · [P-024 state action wrong type](../pitfalls/HIGH-severity.md#p-024)
**QuickCheck:** [state attacks](../quickcheck/state-attacks.md)
**Mock-Q:** [Mock Q3 Nim](../indexes/MOCK-Q-INDEX.md#mock-q3)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
