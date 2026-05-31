<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Tree × Either**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · **tree × either** · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Tree × Either

**Why this combo:** Either is like Maybe but the failure carries a *message* — the name of the bad node, the expected type, the lookup that failed. The first `Left` short-circuits the whole traversal, propagating its error all the way up.

**Recognition triggers:**
- "Validate the tree; produce an error message if invalid"
- "Parse-result tree; report which node was malformed"
- "Compute, but report division by zero / undefined variable"
- "Either succeed with `BT b`, or fail with `String` describing where"

**Search keywords:** Either BT, validate tree, parse tree, Left error, Right success, mapMTree Either, monadic recursion error

## Pattern (validate-and-transform tree)

```haskell
data BT a = Empty | Fork a (BT a) (BT a) deriving Show

validateTree :: (a -> Either String b) -> BT a -> Either String (BT b)
validateTree _ Empty        = Right Empty
validateTree f (Fork x l r) = do
  y  <- f x
  l' <- validateTree f l
  r' <- validateTree f r
  return (Fork y l' r')

-- e.g.
checkPositive :: Int -> Either String Int
checkPositive n
  | n > 0     = Right n
  | otherwise = Left ("Non-positive value: " ++ show n)

validateTree checkPositive someTree
  -- Right tree if all positive; Left "Non-positive value: 0" if any non-positive
```

## Worked variants

### Lookup with named environment

```haskell
type Env = [(String, Int)]

evalVar :: Env -> String -> Either String Int
evalVar env name = case lookup name env of
  Just v  -> Right v
  Nothing -> Left ("Undefined variable: " ++ name)

evalTree :: Env -> BT String -> Either String (BT Int)
evalTree env = validateTree (evalVar env)
```

### Annotate with context (which subtree the error is in)

```haskell
validateWithCtx :: (a -> Either String b) -> BT a -> Either String (BT b)
validateWithCtx _ Empty        = Right Empty
validateWithCtx f (Fork x l r) = do
  y  <- annotate "root" (f x)
  l' <- annotate "left subtree"  (validateWithCtx f l)
  r' <- annotate "right subtree" (validateWithCtx f r)
  return (Fork y l' r')
  where
    annotate :: String -> Either String a -> Either String a
    annotate ctx (Left  e) = Left (ctx ++ ": " ++ e)
    annotate _   r         = r
```

### Either-with-Monoid-error (collect ALL errors instead of first)

The "collect all" semantic needs a different beast — Either with `Monoid e` (rare), or `Validation` (a custom type). Either-as-Monad always short-circuits on the first Left.

```haskell
-- Validation collects all errors:
data V e a = Bad [e] | OK a

instance Functor (V e) where
  fmap f (OK a)  = OK (f a)
  fmap _ (Bad e) = Bad e

instance Applicative (V e) where
  pure = OK
  OK f  <*> OK x  = OK (f x)
  Bad e <*> OK _  = Bad e
  OK _  <*> Bad e = Bad e
  Bad e <*> Bad d = Bad (e ++ d)   -- collect both

validateAll :: (a -> V String b) -> BT a -> V String (BT b)
validateAll _ Empty        = pure Empty
validateAll f (Fork x l r) =
  Fork <$> f x <*> validateAll f l <*> validateAll f r
```

This uses Applicative `<*>` not Monad `>>=` — that's the trick: Applicative can collect, Monad must short-circuit.

### Safe-evaluator for Expr

```haskell
data Expr = Lit Int | Var String | Div Expr Expr | Add Expr Expr

evalSafe :: [(String, Int)] -> Expr -> Either String Int
evalSafe _   (Lit n) = Right n
evalSafe env (Var x) = case lookup x env of
  Just v  -> Right v
  Nothing -> Left ("Unknown var: " ++ x)
evalSafe env (Add e1 e2) = do
  x <- evalSafe env e1
  y <- evalSafe env e2
  return (x + y)
evalSafe env (Div e1 e2) = do
  x <- evalSafe env e1
  y <- evalSafe env e2
  if y == 0 then Left "Division by zero" else Right (x `div` y)
```

## Mutations

- **Error type** → `String`, custom `data Err = ...`, `(NodePath, String)`, `[Error]`.
- **First-error vs all-errors** → Either vs Validation/Applicative.
- **Add context** → `annotate` helper threading path info.
- **Combine with Reader** for environment → see [expr-x-multi.md](expr-x-multi.md).
- **Recover from errors** via `<|>` (needs `Monoid e` for Alternative).

## QuickCheck attacks

```haskell
-- Right output preserves shape
prop_validate_shape :: BT Int -> Bool
prop_validate_shape t = case validateTree Right t of
  Right t' -> shape t' == shape t
  Left _   -> True   -- vacuously

-- If predicate is always-True, validation succeeds
prop_validate_total :: BT Int -> Bool
prop_validate_total t = validateTree Right t == Right t

-- If ANY node fails, the whole result is Left
prop_validate_strict :: BT Int -> Property
prop_validate_strict t = not (null (toList t)) ==>
  case validateTree (const (Left "x")) t of
    Left _  -> True
    Right _ -> False

-- Errors propagate from leftmost-first node
prop_validate_first :: BT Int -> Bool
prop_validate_first t = ...  -- depends on traversal order
```

## Pitfalls

- **Either e is a Monad in `e` fixed**, not in `a`. `instance Monad (Either e)` — the `e` is type-parameter-frozen.
- **`Left e >>= f = Left e`** — short-circuits. No way to recover except `<|>` (needs `Monoid e`).
- **Don't confuse Left with Right.** Right is success, Left is failure. (Mnemonic: "Right is right, Left is wrong.")
- **Validation isn't a Monad** — only Applicative. The whole point of Validation is `<*>` collects errors; `>>=` can't.
- **String errors get verbose** — use a dedicated error type if many cases.
- **Catch failures with `either`**:
  ```haskell
  either onLeft onRight :: Either e a -> r
  ```
  cleaner than nested case.
- **`mapM` for Either** short-circuits at first failure (unlike `traverse` for Validation, which collects).

## Either monad vs Maybe — when to choose

| | Maybe | Either e |
|---|---|---|
| Failure info | none | named/messaged |
| Type signature | `Maybe T` | `Either String T` or `Either Error T` |
| Recovery via `<\|>` | yes | only if `Monoid e` |
| Cost | none | one extra String/Error per failure |

Use Either when you care to report what went wrong; use Maybe when "present/absent" is all you need.

## See also

**Combined archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A08 env eval](../archetypes/A08-env-eval.md)
**Theory:** [binary tree](../trees/binary-tree.md) · [Either](../monads/either.md)
**Question families:** [tree-extract](../question-families/tree-extract-family.md) · [error-handling](../question-families/error-handling-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md) · [maybe-either attacks](../quickcheck/maybe-either-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
