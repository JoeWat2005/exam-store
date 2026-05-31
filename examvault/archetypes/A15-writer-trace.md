<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A15 — Writer Trace**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · **A15** · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A15 — Writer Trace

**Tier:** 3   |   **Stars:** ⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** A3 (Q2 `trace` — uses State with extra log component, equivalent shape)
**Combines with:** A01 · A03 · A14 · A02
**Search keywords:** Writer · tell · runWriter · execWriter · trace · log · Sum · `[String]`

## What it tests
Whether you can use the Writer monad to accumulate side-channel logs (strings, counts, Sums) while the main computation returns a clean result — using `tell` at each step without breaking the return type.

## Recognition triggers
- "log every step", "trace each operation", "produce a string describing …"
- `Writer w a` or `WriterT w m a` in the type sig
- `tell` is allowed (or even required) by the spec
- The return type is a tuple `(result, log)` or `Writer log result`
- `Sum Int` / `[String]` / `String` (anything Monoid) appears as the `w` parameter

## Canonical template
```haskell
import Control.Monad.Writer

logStep :: Int -> Writer [String] Int
logStep n = do tell ["start with " ++ show n]
               let r = n * 2
               tell ["doubled to " ++ show r]
               return r
```

## Mutations (the examiner picks one)

### M1 — `logFactorial` (problem 107)
```haskell
logFactorial :: Int -> Writer [String] Int
logFactorial 0 = do tell ["base case 0! = 1"]; return 1
logFactorial n = do tell ["multiplying by " ++ show n]
                    r <- logFactorial (n - 1)
                    return (n * r)
```
What changes: recursive log; each call adds one line.

### M2 — `countSteps` (problem 108) — WHITELIST-SAFE primary
```haskell
-- Log one entry per step, then take length. ONLY Control.Monad.Writer needed.
countSteps :: Int -> Writer [String] Int
countSteps 1 = do tell ["step"]; return 1
countSteps n
  | even n    = do tell ["step"]; countSteps (n `div` 2)
  | otherwise = do tell ["step"]; countSteps (3 * n + 1)
-- length (execWriter (countSteps 27)) == 111
```
What changes: count = `length (execWriter ...)`. `Writer [()]` or carrying an
`Int` through `Control.Monad.State` (`modify (+1)`) work the same way.

> **WARNING — `Sum`/`Product`/`Any`/`All` are NOT whitelisted.** They are in
> `Data.Monoid`, which `Control.Monad.Writer` does **not** re-export (verified:
> `Sum` is "Not in scope" with only that import). `import Data.Monoid (Sum(..))`
> is **NOT on the allow-list → scores 0.** Use the `[String]`+`length` version
> above, or a local `newtype Count` with a hand-written `Monoid` (legal under
> `-XSafe`, no import):
> ```haskell
> newtype Count = Count Int
> getCount (Count n) = n
> instance Semigroup Count where Count a <> Count b = Count (a + b)
> instance Monoid    Count where mempty = Count 0
> ```
> Only use the `Sum` form below if the question's own Types module exports it:
> ```haskell
> import Data.Monoid (Sum(..))   -- NOT an allowed import on its own
> countStepsSum :: Int -> Writer (Sum Int) Int
> countStepsSum 1 = do tell (Sum 1); return 1
> countStepsSum n
>   | even n    = do tell (Sum 1); countStepsSum (n `div` 2)
>   | otherwise = do tell (Sum 1); countStepsSum (3 * n + 1)
> ```

### M3 — `logTraverse` on a tree (ewan31-40 style)
```haskell
data Dir = File String | SubDir String [Dir]

logTraverse :: Dir -> Writer [String] ()
logTraverse (File n _)        = tell ["File: " ++ n]
logTraverse (SubDir n cs)     = do tell ["Enter " ++ n]
                                   mapM_ logTraverse cs
                                   tell ["Leave " ++ n]
```
What changes: log on entry AND exit of each container; `mapM_` for the children.

### M4 — `withLog` (record every node visited)
```haskell
sumTreeLog :: Num a => BT a -> Writer [a] a
sumTreeLog Empty        = return 0
sumTreeLog (Fork x l r) = do tell [x]
                             a <- sumTreeLog l
                             b <- sumTreeLog r
                             return (x + a + b)
```
What changes: log accumulates VALUES, not strings; final log = all values in pre-order.

### M5 — `evalWithSteps` (calculator log)
```haskell
data E = Lit Int | Add E E | Mul E E

evalLog :: E -> Writer [String] Int
evalLog (Lit n)   = do tell ["lit " ++ show n]; return n
evalLog (Add a b) = do x <- evalLog a
                       y <- evalLog b
                       tell [show x ++ " + " ++ show y ++ " = " ++ show (x + y)]
                       return (x + y)
evalLog (Mul a b) = do x <- evalLog a
                       y <- evalLog b
                       tell [show x ++ " * " ++ show y ++ " = " ++ show (x * y)]
                       return (x * y)
```
What changes: combines A08 (eval) with W; one log line per step.

### M6 — `padded` logging (call depth)
```haskell
pad :: Int -> Writer [String] a -> Writer [String] a
pad d w = do let (a, log) = runWriter w
             tell (map (replicate d ' ' ++) log)
             return a
```
What changes: hijacks the inner Writer's log and indents each line; useful as a wrapper.

### M7 — `String` (not `[String]`) Writer
```haskell
logChars :: [Char] -> Writer String ()
logChars = mapM_ (\c -> tell [c])
```
What changes: w = `String` (Monoid via `++`); each tell appends one char.

### M8 — `Product` Writer
> **WARNING — `Product` is NOT whitelisted** (it's in `Data.Monoid`, not
> re-exported by `Control.Monad.Writer`). The version below scores 0 unless the
> question's Types module provides `Product`. Whitelist-safe alternative: log
> the factors into a `[Int]` and multiply with `product` at the end, or use a
> local `newtype Prod` with a hand-written `Monoid`.
```haskell
-- WHITELIST-SAFE: collect factors, multiply at the end
factWith :: Int -> Writer [Int] ()
factWith 0 = return ()
factWith n = do tell [n]; factWith (n - 1)
-- product (execWriter (factWith 5)) == 120

-- Only if Types provides Product:
import Data.Monoid (Product(..))   -- NOT an allowed import on its own
factWithP :: Int -> Writer (Product Int) ()
factWithP 0 = return ()
factWithP n = do tell (Product n); factWithP (n - 1)
```
What changes: multiplicative accumulator; with the safe version, `product (execWriter ...)` gives the factorial.

### M9 — Two writers combined
> Tuples of Monoids are Monoids, so you can carry two logs at once. To stay
> **whitelist-safe**, pair `[String]` with a counting log instead of `Sum`
> (here `[()]`, then `length` the second component):
```haskell
-- WHITELIST-SAFE: ([String], [()]) — count = length of the snd component
twoLogs :: Int -> Writer ([String], [()]) Int
twoLogs n = do tell (["step " ++ show n], [()])
               return n

-- Only if Types provides Sum:
-- twoLogs :: Int -> Writer ([String], Sum Int) Int   -- needs Data.Monoid (Sum(..)), NOT whitelisted
-- twoLogs n = do tell (["step " ++ show n], Sum 1); return n
```
What changes: tuple of Monoids is itself a Monoid; carry two logs at once.

### M10 — `WriterT` over `State` (A3 trace shape)
```haskell
type Trace s = WriterT [s] (State s)

logState :: Trace s ()
logState = do s <- lift get; tell [s]
```
What changes: combines Writer with State; tells the current state value.

## Worked examples from this course
- Problem sheet Set 11 (#107-108): `logFactorial`, `countSteps`.
- Practice file `ewan31-40.hs`: `logTraverse`, `countFiles`.
- Week 9 lecture: introduces Writer.
- Assignment 3 Q2: `trace` uses State `([s], s)` — same idea as Writer for `[s]` but glued into the state.

## QuickCheck attack surface
- **`execWriter` gives the log**: `execWriter (logFactorial 3)` produces the list of strings; marker checks exact match.
- **`runWriter` gives both**: with the whitelist-safe `Writer [String]` version, `length (execWriter (countSteps 5)) == 5` for Collatz from 5 = 5,16,8,4,2,1 = 5 steps. *(With the Sum variant it would be `snd (runWriter (countSteps 5)) == Sum 5`.)*
- **Empty log on base case**: `tell mempty == return ()`. Trivial base may or may not need a `tell` — read spec.
- **Order of `tell` matches order of execution**: `tell ["a"] >> tell ["b"] >> return ()` gives `["a","b"]`. Bug: `tell ["b"] >> tell ["a"]` gives `["b","a"]`.
- **Monoid identity**: `tell mempty` is a no-op. Useful in conditionals.

## Pitfalls (marks-killers)
- **`tell` requires a Monoid**: `tell 5` (raw `Int`) errors — `Int` is not a `Monoid`. Whitelist-safe fix: `tell [5]` (a `[Int]` log) or `tell ["..."]`. `Sum 5`/`Product 5` also work but need the non-whitelisted `Data.Monoid` — avoid unless Types provides it.
- **Forgetting `import Control.Monad.Writer`**: same as A02.
- **Using `=` instead of `<-`**: `r = logFactorial (n-1)` — `r` is now a Writer, not the result. Use `r <- logFactorial (n-1)`.
- **Calling `tell` outside a monad**: `tell "..."` at the top level of a pure function — type error.
- **`tell []` accidentally**: `tell []` adds an empty log entry (still a `[]`), but `tell [""]` adds `""`. Subtle.
- **Wrong runner**: `runWriter` gives `(a, w)`, `execWriter` gives `w`, `runWriterT` works inside the inner monad. Pick by what's required.

## Combines-with deep dive

### A15 × A01 — log per tree node
```haskell
labelLog :: BT a -> Writer [Int] (BT (Int, a))
labelLog Empty        = return Empty
labelLog (Fork x l r) = do l' <- labelLog l
                           tell [...]      -- step counter
                           r' <- labelLog r
                           return (Fork (?, x) l' r')
```

### A15 × A03 — generic `mapM` over a tree with Writer
Since Writer is a Monad, all the A03 combinators (`mapM`, `sequenceM`, `forM_`) work over it directly.

### A15 × A02 — log every state change
See M10. The combination `WriterT [s] (State s)` literally produces the A3 `trace` semantics.

### A15 × A14 — log AND error AND state
```haskell
allThree :: Cmd -> StateT Env (ExceptT String (Writer [String])) ()
```
Three-layer transformer (conceptual).

> **WARNING — `ExceptT` is NOT whitelisted.** It lives in
> `Control.Monad.Trans.Except` and is **not** in scope from any allowed import
> (verified: "Not in scope: type constructor `ExceptT`"). This signature scores
> **0** in the exam. For "log AND error AND state" with allowed imports, hand-roll
> the error layer: return `Either String a` *inside* a `StateT Env (Writer [String])`,
> i.e. `StateT Env (Writer [String]) (Either String a)`, and branch on the `Either`
> yourself (see the env-eval / error-handling families).

## See also

**Combines with:** [A01 tree recursion](./A01-tree-recursion.md) · [A02 state game](./A02-state-game.md) · [A08 env eval](./A08-env-eval.md) · [A14 multi-effect interp](./A14-multi-effect-interp.md)
**Question families:** [writer-trace](../question-families/writer-trace-family.md)
**Cross-topic:** [rose × writer](../cross-matrix/rose-x-writer.md) · [tree × writer](../cross-matrix/tree-x-writer.md) · [bst × writer](../cross-matrix/bst-x-writer.md) · [list × writer](../cross-matrix/list-x-writer.md)
**Theory:** [Writer monad](../monads/writer.md)
**QuickCheck:** [writer attacks](../quickcheck/writer-attacks.md)
**Mock-Q:** [Mock Q2 (Writer variant)](../indexes/MOCK-Q-INDEX.md#mock-q2)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
