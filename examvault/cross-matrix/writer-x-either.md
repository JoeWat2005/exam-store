<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Writer × Either (logged computation that can fail)**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · [parser × either](./parser-x-either.md) · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · **writer × either**
<!-- siblings:end -->






# Cross: Writer × Either (logged computation that can fail)

**Why this combo:** sometimes you want both a **trace of what was computed** AND a **typed failure**. Pure `Writer` succeeds always. Pure `Either` has no log. Combined, you can produce an audit log up to the point of failure — useful for interpreters, validators, batch processors.

**Recognition triggers:**
- "Evaluate this expression, log every step, fail with a descriptive message"
- "Validate this list; output a log of what passed; halt at the first error"
- "Apply transformations and record both what was done and what went wrong"
- Sig like `eval :: Expr -> Either String (a, [String])` or `(Either String a, [String])`

**Search keywords:** Writer · Either · trace + error · log up to failure · WriterT ExceptT · audit log

## Stack ordering matters (see [transformer-stack-order](../monads/transformer-stack-order.md))

There are two natural shapes. Both can be useful; they differ on what survives a failure.

### Shape A — `WriterT [String] (Either e) a`

```haskell
import Control.Monad.Writer
import Control.Monad.Except

type LogE a = WriterT [String] (Either String) a

runLogE :: LogE a -> Either String (a, [String])
runLogE = runWriterT
```

When the inner `Either` fails, the **log is lost** along with the value. Result is `Left e`.

### Shape B — `ExceptT String (Writer [String]) a`

```haskell
type LogE2 a = ExceptT String (Writer [String]) a

runLogE2 :: LogE2 a -> (Either String a, [String])
runLogE2 = runWriter . runExceptT
```

When the `ExceptT` fails, the **log up to the failure point survives**. Result is `(Left e, log)`.

For "show me the audit trail even on failure", **Shape B is what you want**. For "give me a clean Right or nothing", Shape A is simpler.

## Without transformers — tuple form

For exam answers using only `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer` (the allowed imports), you can't use `WriterT`/`ExceptT` because those need `mtl`. The substitute: a hand-rolled product.

```haskell
-- Shape B equivalent without transformers:
type LogE a = ([String], Either String a)

bindLogE :: LogE a -> (a -> LogE b) -> LogE b
bindLogE (log1, Left e)   _ = (log1, Left e)
bindLogE (log1, Right a)  k = let (log2, r) = k a
                              in (log1 ++ log2, r)

returnLogE :: a -> LogE a
returnLogE a = ([], Right a)

tellLogE :: String -> LogE ()
tellLogE s = ([s], Right ())

throwLogE :: String -> LogE a
throwLogE e = ([], Left e)
```

This is essentially `Writer [String] (Either String a)` flattened. It satisfies the Monad laws.

## Worked example: tracing arithmetic evaluator with errors

```haskell
data Expr = Num Int | Add Expr Expr | Div Expr Expr deriving Show

-- Using Shape B (tuple form, allowed imports):
eval :: Expr -> ([String], Either String Int)
eval (Num n)     = ([show n], Right n)
eval (Add e1 e2) =
  case eval e1 of
    (log1, Left e)  -> (log1, Left e)
    (log1, Right v1) ->
      case eval e2 of
        (log2, Left e)  -> (log1 ++ log2, Left e)
        (log2, Right v2) ->
          let r = v1 + v2
          in (log1 ++ log2 ++ [show v1 ++ " + " ++ show v2 ++ " = " ++ show r], Right r)
eval (Div e1 e2) =
  case eval e1 of
    (log1, Left e)  -> (log1, Left e)
    (log1, Right v1) ->
      case eval e2 of
        (log2, Left e)  -> (log1 ++ log2, Left e)
        (log2, Right 0) -> (log1 ++ log2 ++ ["div by zero attempted"], Left "div by zero")
        (log2, Right v2) ->
          let r = v1 `div` v2
          in (log1 ++ log2 ++ [show v1 ++ " / " ++ show v2 ++ " = " ++ show r], Right r)
```

Run trace:

```
ghci> eval (Add (Num 4) (Div (Num 6) (Num 2)))
(["4","6","2","6 / 2 = 3","4 + 3 = 7"], Right 7)

ghci> eval (Add (Num 4) (Div (Num 6) (Num 0)))
(["4","6","0","div by zero attempted"], Left "div by zero")
```

The Add log entry doesn't appear in the failure case because evaluation aborted before reaching it. But the entries up to the failure are preserved. ✓

## Shape A vs B side-by-side

| Question | Shape A `WriterT log (Either e)` | Shape B `ExceptT e (Writer log)` |
|---|---|---|
| Type after run | `Either e (a, log)` | `(Either e a, log)` |
| Log on success | preserved | preserved |
| Log on failure | **lost** | **preserved up to failure** |
| Used when | You only care about logs when result is valid | You want a complete audit trail |
| Tuple-form equivalent | `Either e ([log], a)` | `([log], Either e a)` |

## QuickCheck properties

```haskell
prop_logged_success :: Int -> Bool
prop_logged_success n =
  let (log, r) = eval (Num n)
  in r == Right n && log == [show n]

prop_div_by_zero :: Int -> Bool
prop_div_by_zero n =
  let (log, r) = eval (Div (Num n) (Num 0))
  in r == Left "div by zero" && "div by zero attempted" `elem` log

prop_log_monotone :: Expr -> Property
prop_log_monotone e =
  let (log, _) = eval e
  in length log >= 0 .&&. all (not . null) log

prop_partial_log_preserved :: Int -> Property
prop_partial_log_preserved n =
  n /= 0 ==>
  let (log, _) = eval (Add (Num n) (Div (Num 1) (Num 0)))
  in show n `elem` log    -- log captured prefix of evaluation
```

## QuickCheck traps

- **Lazy log accumulation** (`Writer` with list monoid) — concatenating lists with `++` is O(n²) when done left-to-right. For long traces use `[Difflist]` or `Data.Sequence`. For exam-sized inputs `[String]` is fine.
- **Stack-overflow risk**: lazy `<>` on long `Writer` logs can OOM. Use `tell [s]` rather than `tell [s1, s2, s3, ...]` then `tell` again.
- **Forgetting to propagate** the partial log on failure — the wrong way returns `Left e` with empty log; the right way returns the log accumulated up to that point.
- **Confusing "log on failure" semantics** between the two shapes — clarify which one the problem statement is asking for.

## Common bugs

| Bug | Symptom | Fix |
|---|---|---|
| Returning `Left e` with empty `[]` log instead of accumulated log | Audit trail missing for failures | Use Shape B (tuple-form preserves log) and explicitly `log1 ++` the prefix on failure. |
| Stack `WriterT` outside `Either` for "log on failure" | Log dropped on Left | Swap to `ExceptT … (Writer …)`. |
| Forgetting to thread both `log1` and `log2` through Add/Div recursion | Half the log goes missing | Pattern: every recursive bind needs to concat its log with the prior. |

## See also

**Combined archetypes:** [A15 writer trace](../archetypes/A15-writer-trace.md) · [A08 env eval](../archetypes/A08-env-eval.md) · [A14 multi-effect interp](../archetypes/A14-multi-effect-interp.md) · [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Theory:** [Writer monad](../monads/writer.md) · [Either monad](../monads/either.md) · [transformers](../monads/transformers.md) · [transformer-stack-order](../monads/transformer-stack-order.md) · [multi-effect](../monads/multi-effect.md)
**Question families:** [writer-trace](../question-families/writer-trace-family.md) · [error-handling](../question-families/error-handling-family.md)
**Cross-topic:** [expr × multi](./expr-x-multi.md) · [tree × writer](./tree-x-writer.md)
**QuickCheck:** [writer attacks](../quickcheck/writer-attacks.md) · [maybe/either attacks](../quickcheck/maybe-either-attacks.md) · [interp attacks](../quickcheck/interp-attacks.md) · [property patterns](../quickcheck/PROPERTY-PATTERNS.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
