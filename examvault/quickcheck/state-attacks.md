<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: State monad**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · **state** · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: State monad

**Search keywords:** State, runState, execState, evalState, get, put, modify, gets, NimBoard, gameOver, takeTokens, Mock Q3, Assignment 3 Q2 trace, Q3 yield, schedule, restore pointer, underflow

Mock Q3 (Nim) and Assignment 3 Q2/Q3/Q4 are State-monad questions. The marker tests by running `runState`/`execState`/`evalState` against the reference.

## What the marker generates

### Mock Q3 (Nim) generators:

```haskell
type NimBoard = (Int, Int)
data Heap = First | Second

instance Arbitrary Heap where
  arbitrary = elements [First, Second]

genBoardWithNeitherHeapEmpty = do
  m <- chooseInt (1, 35)
  n <- chooseInt (1, 35)
  return (m, n)

genIntegerBiasedTowardsZero = frequency [(4, return 0), (16, chooseInt (0, 35))]

genBoardWithOneHeapPossiblyEmpty = do
  m <- genIntegerBiasedTowardsZero
  n <- if m == 0 then chooseInt (1, 35) else genIntegerBiasedTowardsZero
  return (m, n)
```

- Heap sizes drawn from `1..35`.
- 20% of "boards with one possibly-empty heap" actually have a zero heap.

The hardcoded test:
```haskell
prop_gameOverComplete = let (p, _) = runState Student.gameOver (0, 0) in p ~= True
```

**This is literally just "does `gameOver` return `True` on `(0,0)`?". 4 marks. Free.**

The takeTokens tests:
```haskell
genTripleNumGreater = do
  (h1, h2) <- genBoardWithNeitherHeapEmpty
  h <- arbitrary
  k <- chooseInt (1, 10)
  let n = case h of { First -> h1+k ; Second -> h2+k }
  return ((h1, h2), n, h)
```

So `n` is `k` MORE than the chosen heap. Tests that "take more than present" clamps correctly.

### Assignment 3 Q2 (trace):

```haskell
prop_traceCorrectOutput n =
  evalState (Student.trace (fibF n)) ([], (0,1))
  ~= evalState (fibS n) (0,1)

prop_traceCountsStateChangesCorrectly n =
  (length $ fst $ execState (Student.trace (fibF n)) ([], (0,1)))
  ~= 2 * n
```

The state is `([(Int,Int)], (Int,Int))` — log of states paired with current state. `trace` runs a fib computation but records every intermediate state.

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | Both heaps zero `(0, 0)` | hardcoded test | `gameOver (0, 0)` must return `True`. 4 free marks if you remember. | `gameOver = do (a, b) <- get; pure (a == 0 && b == 0)` |
| 2 | One heap zero `(0, 5)` or `(5, 0)` | tested | `gameOver` should return `False` (game continues) | Standard AND check |
| 3 | Both heaps nonzero `(3, 4)` | always tested | `gameOver` should return `False` | Same |
| 4 | `takeTokens k h` where `k > heap[h]` | "take more than present" | Should clamp the heap to 0, not negative | `if k >= current then put 0 else put (current - k)` |
| 5 | `takeTokens k h` where `k == heap[h]` | "take exactly all" | Heap should be 0 after | Boundary correct |
| 6 | `takeTokens 0 h` | "take nothing" | Should be a no-op | `if k <= 0 then pure ()` (defensive) |
| 7 | `takeTokens` from `First` vs `Second` | both heaps tested | Symmetry — make sure `Second` updates the second component, not first | `case h of { First -> modify (\(a, b) -> (max 0 (a-k), b)); Second -> ... }` |
| 8 | Negative `k` (shouldn't happen but...) | not in test gen but be defensive | If `k < 0`, your `current - k` increases the heap! | Guard with `max 0` or `if k > 0` |
| 9 | `runState` extraction | `runState comp s0` returns `(result, finalState)` | Confusing `runState` (returns both) with `evalState` (just result) and `execState` (just state) | Pick the right one based on test |
| 10 | `evalState m s0` | returns just the `a` from `m :: State s a` | If you wanted the state, this throws it away | Use `execState` for state-only |
| 11 | `execState m s0` | returns just the final state | If you wanted the value, this throws it away | Use `evalState` |
| 12 | Polymorphic state type | trace uses `State ([s], s) ()` — log of states + current | Confusing nested state type | Read the type carefully; `get` returns `([s], s)` |

## Mock Q3 canonical solutions

```haskell
gameOver :: NimGame Bool
gameOver = do
  (a, b) <- get
  pure (a == 0 && b == 0)

takeTokens :: Int -> Heap -> NimGame ()
takeTokens k First = modify $ \(a, b) ->
  if k >= a then (0, b) else (a - k, b)
takeTokens k Second = modify $ \(a, b) ->
  if k >= b then (a, 0) else (a, b - k)
```

Or with `get`/`put`:
```haskell
takeTokens k h = do
  (a, b) <- get
  case h of
    First  -> put (max 0 (a - k), b)
    Second -> put (a, max 0 (b - k))
```

`max 0 (a - k)` is a cleaner way to clamp than `if`.

## Property templates

```haskell
import Test.QuickCheck
import Control.Monad.State

-- gameOver on (0,0) is True
prop_gameOver_zero :: Bool
prop_gameOver_zero = evalState gameOver (0, 0) == True

-- gameOver on non-empty board is False
prop_gameOver_nonempty :: Int -> Int -> Property
prop_gameOver_nonempty m n = (m > 0 || n > 0) ==>
  evalState gameOver (m, n) == False

-- takeTokens correctly removes from First
prop_takeTokens_First :: NonNegative Int -> NonNegative Int -> NonNegative Int -> Bool
prop_takeTokens_First (NonNegative k) (NonNegative a) (NonNegative b) =
  let ((), board') = runState (takeTokens k First) (a, b)
  in  board' == (max 0 (a - k), b)

prop_takeTokens_Second :: NonNegative Int -> NonNegative Int -> NonNegative Int -> Bool
prop_takeTokens_Second (NonNegative k) (NonNegative a) (NonNegative b) =
  let ((), board') = runState (takeTokens k Second) (a, b)
  in  board' == (a, max 0 (b - k))

-- takeTokens 0 is a no-op (defensive)
prop_takeTokens_zero :: Int -> Int -> Bool
prop_takeTokens_zero a b =
  let ((), board') = runState (takeTokens 0 First) (a, b)
  in  board' == (a, b)
```

## Self-test before submission checklist

- [ ] `gameOver` on `(0, 0)` returns `True`
- [ ] `gameOver` on any board with at least one nonzero heap returns `False`
- [ ] `takeTokens k First` modifies the FIRST element of the tuple
- [ ] `takeTokens k Second` modifies the SECOND element
- [ ] If `k > heap[h]`, the heap becomes 0, NOT negative
- [ ] If `k == heap[h]`, the heap becomes 0
- [ ] `takeTokens 0 _` is a no-op
- [ ] Used `runState` / `execState` / `evalState` correctly (right one for the property)
- [ ] No accidentally-imported `Data.Map.modify` etc.
- [ ] Type signature character-identical to template

## Pitfalls that specifically lose QC marks

### Pitfall: underflow makes heaps negative
```haskell
-- WRONG: -3 is allowed
takeTokens k First = modify $ \(a, b) -> (a - k, b)
-- For k=5, board=(2, 3): result is (-3, 3). Heap negative.
-- gameOver might then mis-classify.
-- Fix: clamp
takeTokens k First = modify $ \(a, b) -> (max 0 (a - k), b)
```

### Pitfall: `gameOver` checks only one heap
```haskell
-- WRONG: only checks first
gameOver = do
  (a, _) <- get
  pure (a == 0)
-- Fails for (0, 5) — heap not empty, but a=0 → True incorrectly
-- Fix: AND check
gameOver = do (a, b) <- get; pure (a == 0 && b == 0)
```

### Pitfall: wrong monad in signature
```haskell
-- WRONG (Maybe instead of State):
gameOver :: Maybe Bool
-- Fix: NimGame is a type alias for State NimBoard
gameOver :: NimGame Bool
gameOver :: State NimBoard Bool   -- same thing
```

### Pitfall: confused `runState` / `evalState` / `execState`
```haskell
-- runState : State s a -> s -> (a, s)        -- both
-- evalState : State s a -> s -> a            -- value only
-- execState : State s a -> s -> s            -- state only

-- If a property is on the FINAL STATE, use execState:
prop x = execState (takeTokens k h) (a, b) == ...

-- If a property is on the RESULT VALUE, use evalState:
prop = evalState gameOver (0, 0) == True

-- If a property is on BOTH, use runState:
prop x = runState gameOver (0, 0) == (True, (0, 0))
```

### Pitfall: forgetting the state changes from `tell`-like effects in Writer-over-State
```haskell
-- Assignment 3 trace puts state into a list:
trace :: ... -> State ([s], s) a
-- The "log" is the first component, the "live state" is the second.
-- If you confuse them, the order is reversed.
```

### Pitfall: not restoring pointer after `putTatami` (Assignment 1)
```haskell
-- Assignment 1 putTatamiUp = moveDown . put n . moveUp . put n
-- ↑ This restores the pointer to where it started.
-- WRONG: forgets to restore
putTatamiUp n = put n . moveUp . put n   -- pointer ends up
-- The marker has a partial-credit test that ONLY checks the grid, ignoring pointer:
-- prop_PutTatamiUp_PtrNotRestored
-- So if you forget restoration, you score the partial test (4 marks instead of 8).
```

### Pitfall: `modify` requires a pure function
```haskell
-- WRONG: tries to use `do` inside modify
takeTokens k h = modify $ \board -> do { ... }
-- modify takes (s -> s), not (s -> m s).
-- Fix: use get and put if you need do-notation
takeTokens k h = do
  board <- get
  put (... modify board ...)
```

### Pitfall: forgetting the symmetry between `First` and `Second`
```haskell
-- WRONG (copy-paste bug):
takeTokens k First  = modify $ \(a, b) -> (max 0 (a - k), b)
takeTokens k Second = modify $ \(a, b) -> (max 0 (a - k), b)   -- ← same as First!
-- Fix: change a to b
takeTokens k Second = modify $ \(a, b) -> (a, max 0 (b - k))
```

## Connection to Assignment 3

### Q2 trace - records all states
```haskell
trace :: State (s, s) a -> State ([s], s) a
-- The marker checks:
-- 1. evalState (trace m) ([], s0) == evalState m s0       -- result preserved
-- 2. length log == 2*n for n state changes                 -- log size
-- 3. log is a permutation of reference log                 -- order-independent partial credit
-- 4. log matches reference exactly                         -- exact order
```

### Q3 roundRobin - empty list base case
```haskell
prop_emptyListCorrect n = execState (Student.roundRobin []) n
                          ~= execState (Solutions.roundRobin []) n
-- For empty thread list, what's the final state?
-- Spec: same as initial state. `roundRobin [] = pure ()` essentially.
```

### Q4 schedule - single-thread vs multi-thread
The marker has separate tests for 1 thread vs 2-5 threads. If multi-thread is broken but single-thread works, you still score 5 marks.

## See also

**Archetypes:** [A02 state game](../archetypes/A02-state-game.md)
**Cross-topic:** [tree × state](../cross-matrix/tree-x-state.md) · [game-state](../cross-matrix/game-state.md)
**Question families:** [state-game](../question-families/state-game-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
