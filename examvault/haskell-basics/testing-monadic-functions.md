<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Testing monadic functions**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · **testing-monadic-functions** · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Testing monadic functions

## What this is
A function returning `Maybe a`, `Either e a`, `State s a`, `Writer w a`, etc. is not directly printable — you have to **run** the action to extract a value. This page is the cheat sheet of "what runner do I call?"

## Mental model

Different monads have different runners:

| Monad | Runner | Returns |
|---|---|---|
| `Maybe a` | `id` (already a value) | `Maybe a` |
| `Either e a` | `id` | `Either e a` |
| `State s a` | `runState`/`evalState`/`execState` | `(a, s)` / `a` / `s` |
| `Writer w a` | `runWriter`/`execWriter` | `(a, w)` / `w` |
| `Reader r a` | `runReader` | `a` |
| `IO a` | just type it at the prompt | side effects + value |
| `[a]` (list monad) | `id` | `[a]` |

If you forget the runner, GHCi will tell you:

```text
ghci> :t (do { x <- get; return x })
... :: State s s

ghci> (do { x <- get; return x })       -- !! can't show
<interactive>: error:
    • No instance for (Show ...)
```

Wrap in a runner.

## Recipe: Maybe-returning functions

```haskell
safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv x y = Just (x `div` y)
```

```text
ghci> safeDiv 10 2
Just 5

ghci> safeDiv 10 0
Nothing

ghci> isJust (safeDiv 10 2)
True

ghci> fromMaybe (-1) (safeDiv 10 0)
-1

ghci> map (\d -> safeDiv 10 d) [1,2,0,5]
[Just 10,Just 5,Nothing,Just 2]
```

Test both branches explicitly: a `Just` result *and* a `Nothing` result.

## Recipe: Either-returning functions

`Left` carries the error, `Right` the success. By convention, `Right` is correct.

```haskell
safeDivE :: Int -> Int -> Either String Int
safeDivE _ 0 = Left "div by zero"
safeDivE x y = Right (x `div` y)
```

```text
ghci> safeDivE 10 2
Right 5

ghci> safeDivE 10 0
Left "div by zero"

ghci> case safeDivE 10 0 of
        Left err -> "Error: " ++ err
        Right n  -> show n
"Error: div by zero"
```

`Either e` short-circuits on `Left` exactly like `Maybe` on `Nothing` — sequences of binds stop at the first failure.

## Recipe: State monad — choose your runner

```haskell
import Control.Monad.State
import Control.Monad (replicateM)   -- replicateM lives here, NOT in Control.Monad.State

counter :: State Int Int
counter = do
  n <- get
  put (n + 1)
  return n
```

Three runners; pick by what you care about:

```text
ghci> runState counter 0
(0, 1)                       -- (returned-value, final-state)

ghci> evalState counter 0
0                            -- returned value, drop final state

ghci> execState counter 0
1                            -- final state, drop returned value
```

**Rule of thumb:**
- Use `runState` while debugging (you see everything).
- Use `evalState` when only the answer matters (e.g. `labelTree` returns the labelled tree, doesn't need the counter).
- Use `execState` when only the side-state matters (e.g. building up a stack, you want the stack at the end).

### Test multiple calls in sequence

```text
ghci> runState (do { a <- counter; b <- counter; return (a, b) }) 0
((0, 1), 2)
```

### Test with non-zero starting state

```text
ghci> runState counter 100
(100, 101)

ghci> evalState (replicateM 5 counter) 0
[0,1,2,3,4]
```

> **Note:** `replicateM` lives in `Control.Monad` (an allowed import), **not** in `Control.Monad.State`. Importing only `Control.Monad.State` leaves `replicateM` out of scope ("Variable not in scope"). Add `import Control.Monad` too.

### Verify a state-game step

```haskell
takeTokens :: Int -> NimGame ()
takeTokens i = do
  (h1, h2) <- get
  put (max 0 (h1 - i), h2)
```

```text
ghci> execState (takeTokens 2) (5, 5)
(3, 5)

ghci> execState (takeTokens 10) (5, 5)     -- clamping
(0, 5)

ghci> execState (takeTokens (-1)) (5, 5)   -- spec edge: negative
(6, 5)                                      -- !! probably not intended
```

The last call exposes a spec edge: should taking `-1` add a token? Different exams answer differently.

## Recipe: Writer monad

```haskell
import Control.Monad.Writer

logged :: Writer [String] Int
logged = do
  tell ["step 1"]
  tell ["step 2"]
  return 42
```

```text
ghci> runWriter logged
(42, ["step 1","step 2"])

ghci> execWriter logged
["step 1","step 2"]
```

The log accumulates **left-to-right**: the first `tell` ends up at the front of the list. If your expected output has the log in the opposite order, you've used `++ [...]` somewhere or recursed in the wrong direction.

### Test log composition

```text
ghci> runWriter (tell [1] >> tell [2] >> tell [3])
((), [1,2,3])

ghci> runWriter (mapM (\n -> tell [n] >> return n) [1..3])
([1,2,3], [1,2,3])
```

If the second result's log is `[3,2,1]`, the iteration is right-to-left — possible bug.

## Recipe: combined Writer + State

For an interpreter that both logs and tracks a counter, use a tuple in the state and pure functions — the `Control.Monad.Writer` + `Control.Monad.State` import combo can't compose without transformers.

Two patterns work without transformers:

**Pattern A — State of a tuple:**

```haskell
-- state = (counter, accumulating-log)
trace :: Expr -> State (Int, [String]) Int
trace (Lit n) = do
  modify (\(c, log) -> (c+1, ("lit " ++ show n) : log))
  return n
trace (Add a b) = do
  x <- trace a
  y <- trace b
  modify (\(c, log) -> (c+1, ("add " ++ show (x+y)) : log))
  return (x + y)
```

```text
ghci> runState (trace (Add (Lit 1) (Lit 2))) (0, [])
(3, (3, ["add 3","lit 2","lit 1"]))
```

(The log builds in *reverse* this way; flip it at the end if needed.)

**Pattern B — return a tuple manually:**

```haskell
trace' :: Expr -> (Int, [String])
trace' (Lit n)   = (n, ["lit " ++ show n])
trace' (Add a b) = let (x, l1) = trace' a
                       (y, l2) = trace' b
                   in (x + y, l1 ++ l2 ++ ["add " ++ show (x+y)])
```

```text
ghci> trace' (Add (Lit 1) (Lit 2))
(3, ["lit 1","lit 2","add 3"])
```

Pattern B gives you correct left-to-right log without a `reverse`.

See [transformer-stack-order](../monads/transformer-stack-order.md) and [A14](../archetypes/A14-multi-effect-interp.md) for the full story.

## Recipe: Reader monad

```haskell
import Control.Monad.Reader   -- not in allowed imports on this course;
                              -- emulate with: type Reader r a = r -> a
```

Since `Control.Monad.Reader` is **not** in the allowed list, use the function-form Reader (or hand-roll):

```haskell
lookupKey :: String -> [(String, Int)] -> Maybe Int
lookupKey k env = lookup k env

evalVar :: String -> [(String, Int)] -> Maybe Int
evalVar = lookupKey
```

```text
ghci> evalVar "x" [("x", 10), ("y", 20)]
Just 10
```

For Reader-as-monad styling, the env is the *last* argument — partial application gives a Reader-shaped function. See [reader](../monads/reader.md).

## Recipe: IO functions

`IO ()` and `IO a` actions print and return at the same prompt:

```text
ghci> putStrLn "hello"
hello

ghci> let action = do { putStrLn "in:"; x <- getLine; return (length x) }
ghci> action
in:
hello world
11
```

For pure-but-IO-typed code, you can usually replace `IO` with `Maybe`/`Either` and test the pure half. See [io](../monads/io.md).

## Recipe: List monad

The list monad is non-determinism. `do x <- xs; y <- ys; return (x,y)` is the Cartesian product.

```text
ghci> do { x <- [1,2]; y <- "ab"; return (x,y) }
[(1,'a'),(1,'b'),(2,'a'),(2,'b')]

ghci> [(x,y) | x <- [1,2], y <- "ab"]      -- list-comp equivalent
[(1,'a'),(1,'b'),(2,'a'),(2,'b')]
```

If a step `<-` is `[]`, the whole branch dies — equivalent to `Nothing` in `Maybe`.

```text
ghci> do { x <- [1,2]; y <- []; return (x,y) }
[]
```

See [list-monad](../monads/list-monad.md) and [list-x-list-monad](../cross-matrix/list-x-list-monad.md).

## Property tests for monads

```text
-- monad laws — should all be True
ghci> let f = \x -> Just (x+1)
ghci> (return 1 >>= f) == f 1
True
ghci> (Just 1 >>= return) == Just 1
True

-- State law: get >>= put == return ()
ghci> runState (get >>= put) 5 == runState (return ()) 5
True
```

See [monad-laws](../monads/monad-laws.md).

## Common mistakes

- **Forgetting the runner.** `runState`, `evalState`, `execState` choose between (a,s) / a / s — students often pick the wrong one.
- **Treating `Writer` as a list builder.** The log accumulates with `mappend`; if your monoid is `[]`, you get **left-to-right** order — the first `tell` is at the front.
- **`fromJust Nothing`** at the prompt → crash. Always test with `Nothing` explicitly.
- **Importing `Control.Monad.Reader`** → import error, the whole file rejected. Not in the allowed list. [P-013](../pitfalls/HIGH-severity.md#p-013).
- **Pattern-bind in do** like `Just x <- m` silently uses `MonadFail`; if `m` is `Nothing` you get a runtime error in `IO`, or `mzero` in `Maybe`. Be explicit with `case`.
- **Testing only the golden path on a monadic action.** The marker hits with `Nothing`, `Left`, empty state — run those before submit.

## Exam use

Mock Q3 (state Nim) is `evalState`/`execState` against a small `(h1,h2)` board. Mock Q2 (`Monad m => ...`) requires testing in *several* concrete monads — at minimum `Just`, `Nothing`, and `IO` (mapM print).

Pin recipe:
```
ghci> runState  myAction myInitState     -- see (result, final-state)
ghci> evalState myAction myInitState     -- see just result
ghci> execState myAction myInitState     -- see just final-state
ghci> runWriter myWriter                 -- see (result, accumulated-log)
ghci> myMaybeFn input                    -- see Just _ or Nothing
ghci> myEitherFn input                   -- see Right _ or Left _
```

## See also

**Sibling testing pages:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-tree-functions](./testing-tree-functions.md)
**Monad theory:** [State](../monads/state.md) · [Writer](../monads/writer.md) · [Maybe](../monads/maybe.md) · [Either](../monads/either.md) · [Reader](../monads/reader.md) · [IO](../monads/io.md) · [List](../monads/list-monad.md) · [generic-combinators](../monads/generic-combinators.md)
**Monad laws:** [monad-laws](../monads/monad-laws.md)
**Archetypes:** [A02 state game](../archetypes/A02-state-game.md) · [A03 generic monad](../archetypes/A03-generic-monad.md) · [A14 multi-effect](../archetypes/A14-multi-effect-interp.md) · [A15 writer trace](../archetypes/A15-writer-trace.md)
**QuickCheck:** [state-attacks](../quickcheck/state-attacks.md) · [writer-attacks](../quickcheck/writer-attacks.md) · [monad-attacks](../quickcheck/monad-attacks.md) · [maybe-either-attacks](../quickcheck/maybe-either-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
