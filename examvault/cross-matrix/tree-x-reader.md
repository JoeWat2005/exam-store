<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Tree × Reader**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · **tree × reader** · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Tree × Reader

**Why this combo:** Reader provides a *read-only environment* (a configuration, a dictionary, a context) accessible from every node of a tree without explicit threading. Wherever in the tree's recursion you need the env, you `ask` for it — no need to pass it as an extra argument.

**Recognition triggers:**
- "Look up node label in an environment"
- "Tree depends on a configuration / scope"
- "Translate a tree by an env-driven substitution"
- "Compute with shared, immutable context"

**Search keywords:** Reader BT, ask, asks, local, Reader env tree, lookup env tree

## Pattern (env-aware tree mapping)

```haskell
import Control.Monad.Reader

data BT a = Empty | Fork a (BT a) (BT a)
type Env  = [(String, Int)]

translate :: BT String -> Reader Env (BT Int)
translate Empty        = return Empty
translate (Fork x l r) = do
  env <- ask
  let v = case lookup x env of
            Just n  -> n
            Nothing -> 0
  l' <- translate l
  r' <- translate r
  return (Fork v l' r')

-- Run:
runReader (translate t) [("a",1),("b",2),("c",3)]
```

## Worked variants

### Use `asks` for projection from env

```haskell
translate' :: BT String -> Reader Env (BT Int)
translate' Empty        = return Empty
translate' (Fork x l r) = do
  v  <- asks (fromMaybe 0 . lookup x)
  l' <- translate' l
  r' <- translate' r
  return (Fork v l' r')
```

`asks f = fmap f ask` — applies `f` to the env and returns the result.

### Depth-tracking via `local`

```haskell
depthAware :: BT a -> Reader Int (BT (Int, a))
depthAware Empty        = return Empty
depthAware (Fork x l r) = do
  d  <- ask                                           -- current depth
  l' <- local (+1) (depthAware l)                     -- recurse with d+1
  r' <- local (+1) (depthAware r)
  return (Fork (d, x) l' r')

-- Run:
runReader (depthAware t) 0   -- root at depth 0
```

`local f act` runs `act` with env `f env`.

### Read-only configuration object

```haskell
data Config = Config { caseSensitive :: Bool, defaultVal :: Int }

evalWithCfg :: BT String -> Reader Config (BT Int)
evalWithCfg Empty        = return Empty
evalWithCfg (Fork s l r) = do
  cs  <- asks caseSensitive
  dfl <- asks defaultVal
  let key = if cs then s else map toLower s
  let val = case lookup key someTable of Just v -> v; _ -> dfl
  l' <- evalWithCfg l
  r' <- evalWithCfg r
  return (Fork val l' r')
```

### Reader combined with Maybe (env-aware failure)

```haskell
import Control.Monad.Trans.Reader

translateMaybe :: BT String -> Reader Env (Maybe (BT Int))
translateMaybe Empty        = return (Just Empty)
translateMaybe (Fork x l r) = do
  env <- ask
  case lookup x env of
    Nothing -> return Nothing
    Just v  -> do
      ml <- translateMaybe l
      mr <- translateMaybe r
      return $ do
        l' <- ml
        r' <- mr
        return (Fork v l' r')
```

(Reader+Maybe combined; in real code you'd use `ReaderT Env Maybe`, but that's monad transformers — beyond exam scope.)

### Function-as-Reader idiom (no explicit Reader import)

Reader IS just `((->) r)`. So you can write:

```haskell
translate :: BT String -> Env -> BT Int
translate Empty        _   = Empty
translate (Fork x l r) env = Fork (fromMaybe 0 (lookup x env))
                                  (translate l env)
                                  (translate r env)
```

The Reader monad is sugar for this — same semantics, less plumbing.

## Mutations

- **Env type**: list of pairs / `Map` / `Set` / a custom record.
- **Add depth via `local`** — accumulate context as you descend.
- **Add scope via `local (\\env -> env ++ newBindings)`** — extend env for subtree.
- **Combine with Writer for "log lookups"** → see [expr-x-multi.md](expr-x-multi.md).
- **Combine with State for "track which keys were used"**.

## QuickCheck attacks

```haskell
-- Same env always gives same result
prop_reader_pure :: BT String -> Env -> Bool
prop_reader_pure t env =
  runReader (translate t) env == runReader (translate t) env

-- Shape preserved
prop_reader_shape :: BT String -> Env -> Bool
prop_reader_shape t env = shape (runReader (translate t) env) == shape t

-- Empty env produces defaults
prop_reader_empty_env :: BT String -> Bool
prop_reader_empty_env t =
  let result = runReader (translate t) []
  in all (== 0) (toList result)

-- local does not leak out
prop_local_isolates :: BT a -> Int -> Bool
prop_local_isolates t d =
  runReader (do local (+1) (return ()); ask) d == d   -- d, NOT d+1
```

## Pitfalls

- **`ask`** returns the WHOLE env; `asks f` returns `f env`. Use `asks` when you want a projection.
- **`local` is scoped** — it only affects the action inside, NOT subsequent code in the same do-block.
- **Reader passes env to ALL recursive calls automatically** — you don't need to thread it.
- **`Reader e a = e -> a`** — `runReader m e = m e`.
- **No `tell` here** — that's Writer.
- **No mutation** — Reader is read-only; you can't "update" env (except via `local` for scoped changes).
- **Bare-function Reader** is often clearer than `Reader e` — pick whichever the marker wants.
- **Confusing `local f` with `withReader f`** — `local f` modifies env for inner action; `withReader f` transforms an existing Reader-action.

## Reader's `local` vs threading env manually

```haskell
-- With Reader and local: env auto-threaded, scoped change.
descend :: Tree -> Reader Env Int
descend t = local extendEnv $ ...

-- Manual: must pass env+changes every recursion.
descend :: Tree -> Env -> Int
descend t env = ... rec t (extendEnv env) ...
```

Reader hides the parameter — neat for deep recursions.

## See also

**Combined archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A08 env eval](../archetypes/A08-env-eval.md)
**Theory:** [binary tree](../trees/binary-tree.md) · [Reader](../monads/reader.md)
**Question families:** [tree-extract](../question-families/tree-extract-family.md) · [env-eval](../question-families/env-eval-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
