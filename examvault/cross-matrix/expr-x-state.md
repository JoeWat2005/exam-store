<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Expr × State**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · **expr × state** · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Expr × State

**Why this combo:** evaluate an expression AND maintain a counter / fresh-variable supply / cell store. State threads the side-info through every sub-expression; the structure of `evalE` stays the same, just every `<-` is in State now.

**Recognition triggers:**
- "Count how many operations were performed"
- "Generate fresh variables during evaluation"
- "Track a stack / call depth"
- "Simulate a tiny memory cell read/write inside Expr"

**Search keywords:** Expr State, eval counter, fresh var, evalState Expr, store Expr

## Pattern (eval-and-count operations)

```haskell
import Control.Monad.State

data Expr = Lit Int | Add Expr Expr | Sub Expr Expr | Mul Expr Expr

evalCount :: Expr -> State Int Int
evalCount (Lit n)     = return n
evalCount (Add e1 e2) = do
  x <- evalCount e1
  y <- evalCount e2
  modify (+1)              -- record one Add operation
  return (x + y)
evalCount (Sub e1 e2) = do
  x <- evalCount e1
  y <- evalCount e2
  modify (+1)
  return (x - y)
evalCount (Mul e1 e2) = do
  x <- evalCount e1
  y <- evalCount e2
  modify (+1)
  return (x * y)

-- Run:
runState (evalCount e) 0   -- (result, ops_count)
```

## Worked variants

### Fresh-variable supply during transformation

```haskell
data Expr = Var String | Lit Int | Add Expr Expr | Let String Expr Expr

-- Alpha-rename: replace each binding with a fresh name
fresh :: State Int String
fresh = do n <- get; put (n + 1); return ("v" ++ show n)

alphaRename :: Expr -> State Int Expr
alphaRename (Var x)     = return (Var x)
alphaRename (Lit n)     = return (Lit n)
alphaRename (Add e1 e2) = do
  e1' <- alphaRename e1
  e2' <- alphaRename e2
  return (Add e1' e2')
alphaRename (Let x e1 e2) = do
  x'  <- fresh                            -- gensym
  e1' <- alphaRename e1
  e2' <- alphaRename (substitute x x' e2)
  return (Let x' e1' e2')

substitute :: String -> String -> Expr -> Expr
substitute old new (Var y)       = Var (if y == old then new else y)
substitute old new (Lit n)       = Lit n
substitute old new (Add e1 e2)   = Add (substitute old new e1) (substitute old new e2)
substitute old new (Let y e1 e2)
  | y == old  = Let y (substitute old new e1) e2     -- shadowed
  | otherwise = Let y (substitute old new e1) (substitute old new e2)
```

### Cell store — a tiny imperative-ish DSL inside Expr

```haskell
data Cmd = Set String Int | Get String | Add' Cmd Cmd

type Store = [(String, Int)]

runCmd :: Cmd -> State Store Int
runCmd (Set k v)   = do
  modify ((k, v) :)         -- prepend, shadows earlier
  return v
runCmd (Get k)     = do
  st <- get
  case lookup k st of
    Just v  -> return v
    Nothing -> return 0
runCmd (Add' c1 c2) = do
  x <- runCmd c1
  y <- runCmd c2
  return (x + y)
```

### Combine State + Maybe (count operations OR fail)

```haskell
-- Hand-rolled — production would use StateT
type EvalSM a = State Int (Maybe a)

evalSM :: Expr -> EvalSM Int
evalSM (Lit n) = return (Just n)
evalSM (Div e1 e2) = do
  m1 <- evalSM e1
  m2 <- evalSM e2
  modify (+1)
  case (m1, m2) of
    (Just x, Just y) | y /= 0 -> return (Just (x `div` y))
    _                          -> return Nothing
```

### Track max-depth (use modify-with-max)

```haskell
type DepthState = (Int, Int)   -- (current_depth, max_seen)

evalDepth :: Expr -> State DepthState Int
evalDepth (Lit n) = do
  modify (\(c, m) -> (c, max c m))
  return n
evalDepth (Add e1 e2) = do
  modify (\(c, m) -> (c + 1, max (c+1) m))
  x <- evalDepth e1
  y <- evalDepth e2
  modify (\(c, m) -> (c - 1, m))
  return (x + y)
```

(Common in compiler analyses: max-stack-depth.)

### Count by operator type

```haskell
type OpCounts = (Int, Int, Int)   -- (add, sub, mul)

evalCountByOp :: Expr -> State OpCounts Int
evalCountByOp (Lit n)     = return n
evalCountByOp (Add e1 e2) = do
  modify (\(a,s,m) -> (a+1, s, m))
  x <- evalCountByOp e1
  y <- evalCountByOp e2
  return (x + y)
-- ...similarly for Sub, Mul
```

## Mutations

- **What to count**: total ops / by operator / by depth / by variable use.
- **State type**: `Int` / `(Int, Int)` / record / `Map String Int`.
- **Add Maybe** for failure → see [tree-x-maybe.md](tree-x-maybe.md) hybrid.
- **Add Writer** for log → use tuple state or transformer (or [expr-x-multi.md](expr-x-multi.md)).
- **Fresh-variable** generation during inlining.

## QuickCheck attacks

```haskell
-- Result equals pure eval
prop_evalCount_matches_pure :: Expr -> Bool
prop_evalCount_matches_pure e =
  evalState (evalCount e) 0 == pureEval e

-- Op count equals manual count
prop_opCount_matches :: Expr -> Bool
prop_opCount_matches e =
  execState (evalCount e) 0 == countOpsManual e

-- For closed Expr, alphaRename preserves semantics
prop_alphaRename_preserves :: Expr -> Bool
prop_alphaRename_preserves e =
  pureEval (evalState (alphaRename e) 0) == pureEval e

-- Fresh names all distinct
prop_alphaRename_distinct :: Expr -> Bool
prop_alphaRename_distinct e =
  let renamed = evalState (alphaRename e) 0
      names   = collectLetNames renamed
  in nub names == names
```

## Pitfalls

- **`modify (+1)` placement matters.** Before vs after recursive calls changes when you count (pre-eval vs post-eval).
- **`return` not `Just`** inside State — `return x = State (\s -> (x, s))`.
- **`fresh` must `put`** to advance — forgetting `put` means same name twice.
- **State doesn't fail** — if the Expr might fail, combine with Maybe (or use Either).
- **Combining State and Maybe directly is awkward** without transformers — for clarity, tuple state with a `Maybe a` value, or escalate to `expr-x-multi.md`.
- **`evalState` for value, `execState` for state, `runState` for both.** Pick the right runner.
- **Counter at 0 unless asked otherwise.**

## See also

**Combined archetypes:** [A08 env eval](../archetypes/A08-env-eval.md) · [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Theory:** [expression tree](../trees/expression-tree.md) · [State](../monads/state.md)
**Question families:** [env-eval](../question-families/env-eval-family.md) · [state-game](../question-families/state-game-family.md)
**QuickCheck:** [expr attacks](../quickcheck/expr-attacks.md) · [state attacks](../quickcheck/state-attacks.md) · [interp attacks](../quickcheck/interp-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
