<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Monad: State**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · [generic-combinators](./generic-combinators.md) · [io](./io.md) · [list-monad](./list-monad.md) · [maybe](./maybe.md) · [monad-laws](./monad-laws.md) · [monaderror](./monaderror.md) · [multi-effect](./multi-effect.md) · [reader](./reader.md) · **state** · [transformer-stack-order](./transformer-stack-order.md) · [transformers](./transformers.md) · [writer](./writer.md)
<!-- siblings:end -->






# Monad: State

**Import:** `import Control.Monad.State`
**Type:** `newtype State s a = State { runState :: s -> (a, s) }` (conceptual; the real one in `mtl` is a transformer).
**Combines with:** Writer (`StateT`), Either (state-with-error, multi-effect), IO.
**Search keywords:** state, counter, label, fresh, gensym, mutable, threaded, accumulator, board, game, stack, push, pop, Nim, modify, get, put.

This is the **Critical** exam monad — Mock Q3 lives here.

## Primitive operations

| Operation | Signature | Semantics | Pitfall |
|---|---|---|---|
| `get`        | `State s s`                                  | read current state | — |
| `put`        | `s -> State s ()`                            | overwrite state | discards previous state |
| `modify`     | `(s -> s) -> State s ()`                     | `get >>= put . f` | strict variant `modify'` not in scope |
| `gets`       | `(s -> a) -> State s a`                      | project from state | — |
| `state`      | `(s -> (a, s)) -> State s a`                 | raw constructor | rarely needed |
| `pure x`     | `State s a`                                  | `s -> (x, s)` | does NOT touch state |

## Run functions — WHICH ONE TO CALL

The runner type tells you what you keep. **Pick by what the question asks to return.**

| Runner | Signature | Returns | Use when |
|---|---|---|---|
| `runState`  | `State s a -> s -> (a, s)` | both result and final state | question asks for both |
| `evalState` | `State s a -> s -> a`      | just the result `a`         | "compute the value" |
| `execState` | `State s a -> s -> s`      | just the final state        | "count" / "final board" |

Mnemonic: **e**val keeps the *r***e**sult; **e**xec keeps the **e**nd-state.

## When to reach for State

- "Label every node of a tree with a unique increasing integer" (`labelTree`, problem 112).
- "Count the number of leaves / calls" (`countLeaves`, problem 113).
- "Fresh id per name" (`uniqueIds`, problem 119; `fresh`, problem 111).
- Stack/heap simulation (`pushAll`, `evalCalc`, problems 114, 118).
- Game with mutable board: Nim, tic-tac-toe state, Life.
- Imperative-style loops translated functionally (problem 117: Fibonacci by `(prev, curr)` state).
- Any "thread an accumulator through recursion" question where Writer feels wrong because you also need to *read* the accumulator.

## Canonical templates

### Fresh counter (gensym) — problem 111
```haskell
fresh :: State Int Int
fresh = do
  n <- get
  put (n + 1)
  pure n
```

### Tree labelling — problem 112
```haskell
data BT a = Empty | Fork a (BT a) (BT a)

labelTree :: BT a -> BT (Int, a)
labelTree t = evalState (go t) 0
 where
  go :: BT a -> State Int (BT (Int, a))
  go Empty        = pure Empty
  go (Fork x l r) = do
    l' <- go l            -- label LEFT first  (in-order)
    n  <- fresh
    r' <- go r            -- then RIGHT
    pure (Fork (n, x) l' r')
```
Want pre-order? `fresh` first, then recurse. Post-order? `fresh` last.

### Leaf counter — problem 113
```haskell
countLeaves :: BT a -> State Int ()
countLeaves Empty                    = pure ()
countLeaves (Fork _ Empty Empty)     = modify (+1)
countLeaves (Fork _ l r)             = do
  countLeaves l
  countLeaves r

numLeaves :: BT a -> Int
numLeaves t = execState (countLeaves t) 0
```

### Stack / Push — problem 114
```haskell
pushAll :: [a] -> State [a] ()
pushAll []     = pure ()
pushAll (x:xs) = do
  modify (x :)
  pushAll xs
```

### Stack calculator — problem 118
```haskell
data CalcCmd = Push Int | Add | Sub | Mul

calc :: [CalcCmd] -> State [Int] ()
calc []     = pure ()
calc (c:cs) = do
  step c
  calc cs
 where
  step (Push n) = modify (n :)
  step Add      = binop (+)
  step Sub      = binop (-)
  step Mul      = binop (*)
  binop op = do
    s <- get
    case s of
      (a:b:rest) -> put (op b a : rest)
      _          -> return ()
```

### Fibonacci by state-pair — problem 117
```haskell
fibState :: Int -> State (Int, Int) ()
fibState 0 = pure ()
fibState n = do
  (x, y) <- get
  put (y, x + y)
  fibState (n - 1)

-- runState (fibState 10) (0, 1) == ((), (55, 89))
```

### Game state with predicate + mutator — Mock Q3 (CANONICAL — copy verbatim)
```haskell
type NimBoard = (Int, Int)
type NimGame a = State NimBoard a

data Heap = First | Second

gameOver :: NimGame Bool
gameOver = do
  (heap1, heap2) <- get
  return $ heap1 == 0 && heap2 == 0

takeTokens :: Int -> Heap -> NimGame ()
takeTokens i h = do
  (heap1, heap2) <- get
  case h of
    First  -> put $ (max 0 (heap1 - i), heap2)
    Second -> put $ (heap1, max 0 (heap2 - i))
```
Note: `max 0 (n - i)` clamps at zero — don't underflow into negatives. The marker tests this.

### Average via (count, total)
```haskell
average :: [Double] -> Double          -- problem 115
average xs = let (c, t) = execState (mapM_ step xs) (0, 0)
             in t / fromIntegral c
 where
  step :: Double -> State (Int, Double) ()
  step x = modify (\(c, t) -> (c + 1, t + x))
```

### Unique IDs per string — problem 119
```haskell
uniqueIds :: [String] -> State Int [(String, Int)]
uniqueIds []     = pure []
uniqueIds (x:xs) = do
  n  <- fresh
  ys <- uniqueIds xs
  pure ((x, n) : ys)
```

## Question families this monad belongs to

- [state-counter](../question-families/state-counter-family.md)
- [state-game](../question-families/state-game-family.md)

## QuickCheck traps

- `takeTokens i h` where `i > current heap` must **clamp at 0**, not go negative. (`max 0 (h - i)`.)
- `runState (gameOver) (0, 0) == (True, (0, 0))`.
- `runState (gameOver) (0, 1) == (False, (0, 1))`.
- `labelTree Empty == Empty` (the empty case).
- Order of labelling matters — in-order vs pre-order vs post-order will fail an auto-marker that hard-codes one.
- `execState` vs `evalState` confusion — if the marker expects an `Int` count and you return `((), Int)`, it'll fail.

## Pitfalls

- **`State s a` — `s` is FIRST type param.** `State (Int, Int) ()` not `State () (Int, Int)`.
- Forget `import Control.Monad.State` → auto-marker won't compile.
- `put (n+1)` re-reads is wrong; use `modify (+1)`.
- `pure x` does NOT change state; if you wanted to write the value to the state, use `put x`.
- `runState m s0` returns `(a, s_final)` — destructure carefully: `let (result, _) = runState ...`.
- `mapM_` is your friend for state-modifying loops; don't hand-roll `forM_` recursion unless the question wants it.
- A refutable pattern on (`<- get`) is a compile error in plain `State` (no `MonadFail`). Always do `s <- get` then `case s of ...`. Writing `(a:b:s) <- get` makes GHC demand `MonadFail Identity`, which does not exist, so the whole file fails to compile (scores 0). `case get of ...` is also wrong — `get` is an action, not a pure value.
- Two `State` *types* in the same file: don't mix `State Int` and `State (Int, Int)` in the same do-block.

## Worked examples

- **Mock Q3** (Nim) — copy `gameOver` and `takeTokens` from above verbatim.
- Problems 111–119 are direct State drills.
- `fibState` (inline above, problem 117) shows the Java-imperative-translation pattern: thread `(prev, curr)` through the state.
- The leaf counter (inline above, problem 113) uses `modify (+1)` to count.

## See also

**Archetypes:** [A02 state game](../archetypes/A02-state-game.md) · [A23 mini-game](../archetypes/A23-mini-game.md)
**Cross-topic:** [tree × state](../cross-matrix/tree-x-state.md) · [bst × state](../cross-matrix/bst-x-state.md) · [rose × state](../cross-matrix/rose-x-state.md) · [expr × state](../cross-matrix/expr-x-state.md) · [list × state](../cross-matrix/list-x-state.md) · [game-state](../cross-matrix/game-state.md)
**Question families:** [state-game](../question-families/state-game-family.md) · [state-counter](../question-families/state-counter-family.md)
**Interpreters:** [expr-state interpreter](../interpreters/expr-state.md)
**QuickCheck:** [state attacks](../quickcheck/state-attacks.md)
**Related (monads):** [transformers](./transformers.md) · [multi effect](./multi-effect.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
