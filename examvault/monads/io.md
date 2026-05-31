<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Monad: IO**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · [generic-combinators](./generic-combinators.md) · **io** · [list-monad](./list-monad.md) · [maybe](./maybe.md) · [monad-laws](./monad-laws.md) · [monaderror](./monaderror.md) · [multi-effect](./multi-effect.md) · [reader](./reader.md) · [state](./state.md) · [transformer-stack-order](./transformer-stack-order.md) · [transformers](./transformers.md) · [writer](./writer.md)
<!-- siblings:end -->






# Monad: IO

**Import:** built-in (`Prelude`).
**Type:** `IO a` — opaque. Conceptually `RealWorld -> (a, RealWorld)`.
**Combines with:** State (via `StateT s IO`), but in exam usually used alone.
**Search keywords:** print, putStrLn, getLine, readLn, main, interactive, animation, loop, until quit, prompt, ANSI, clear screen.

## Primitive operations

### Output

| Operation | Signature | Note |
|---|---|---|
| `putStr`   | `String -> IO ()`     | no trailing newline |
| `putStrLn` | `String -> IO ()`     | adds trailing `\n` |
| `putChar`  | `Char -> IO ()`       | single char |
| `print`    | `Show a => a -> IO ()`| `= putStrLn . show` |

### Input

| Operation | Signature | Note |
|---|---|---|
| `getLine`     | `IO String`                  | reads one line, no newline |
| `getChar`     | `IO Char`                    | one char (line-buffered usually) |
| `readLn`      | `Read a => IO a`             | parse one line into any `Read` |
| `getContents` | `IO String`                  | **lazy** whole-input stream |

### Generic

| Operation | Signature | Note |
|---|---|---|
| `return`/`pure` | `a -> IO a`                 | pure value into IO (no I/O performed) |
| `(>>=)`         | `IO a -> (a -> IO b) -> IO b` | sequence |
| `interact`      | `(String -> String) -> IO ()` | stream-filter `stdin` → `stdout` |

### `Control.Monad` helpers (very common with IO)

| Operation | Signature | Use |
|---|---|---|
| `mapM_`     | `Monad m => (a -> m b) -> [a] -> m ()`     | "do an IO for each" |
| `forM_`     | flipped `mapM_`                            | when the list is short, the body long |
| `replicateM`| `Int -> IO a -> IO [a]`                    | read N inputs |
| `when`      | `Bool -> IO () -> IO ()`                   | conditional IO |
| `unless`    | `Bool -> IO () -> IO ()`                   | negated `when` |

## Run functions

There is **no `runIO`**. `IO` is opaque; you cannot extract `a` purely. The runtime executes `main :: IO ()`. Inside IO, use `<-` to bind an `IO a` to an `a`.

```haskell
main :: IO ()
main = do
  name <- getLine          -- name :: String
  putStrLn ("Hi, " ++ name)
```

## When to reach for IO

- The signature has `IO` in it.
- "Read input from the user / print something".
- "Animate / clear the screen / pause".
- "Interactive game loop".
- Assignments with a `main` function.

If the body is *pure* you should NOT wrap it in IO — write a pure function and call it from `main`.

## Canonical templates

### Greet (problem 101)
```haskell
greet :: IO ()
greet = do
  putStrLn "What is your name?"
  name <- getLine
  putStrLn ("Hello, " ++ name ++ "!")
```

### Sum three numbers (problem 102)
```haskell
sumInput :: IO ()
sumInput = do
  a <- readLn
  b <- readLn
  c <- readLn
  print (a + b + c :: Int)
```

### Echo until "quit" (problem 103)
```haskell
echoUntilQuit :: IO ()
echoUntilQuit = do
  line <- getLine
  if line == "quit"
    then pure ()
    else do
      putStrLn line
      echoUntilQuit
```

### Print every element (problem 104)
```haskell
printList :: Show a => [a] -> IO ()
printList = mapM_ print
```

### Read N inputs (problem 110)
```haskell
threeNumbers :: IO [Int]
threeNumbers = replicateM 3 readLn
```

### Interactive game loop
```haskell
runGame :: Grid -> IO ()
runGame g
  | won g     = putStrLn "Done"
  | otherwise = do
      print g
      n <- readLn
      runGame (move g n)
```

### Animation (Life-style)
```haskell
import Control.Concurrent (threadDelay)

cls :: IO ()
cls = putStr "\ESC[2J"

goto :: (Int, Int) -> IO ()
goto (x, y) = putStr ("\ESC[" ++ show y ++ ";" ++ show x ++ "H")

life :: Grid -> IO ()
life g = do
  cls
  goto (1, 1)
  putGrid g
  threadDelay 200000          -- 0.2 sec
  life (step g)
```

### Highlighting with ANSI escapes (A1)
```haskell
highlight :: String -> String
highlight s = "\ESC[44m" ++ s ++ "\ESC[0m"
```

### `interact`-style filter
```haskell
main :: IO ()
main = interact (unlines . map reverse . lines)
```

## Modelling IO as data (`IO'` from the IOPrime lecture)

> **Exam-likelihood: LOW (⭐).** This is the optional/advanced `IOPrime.md` lecture topic — *constructing* an effect monad as data rather than *using* the real `IO`. Worth one read so a "define your own IO monad" question doesn't surprise you; otherwise skip. Uses only `Prelude`.

The trick: an effectful program is a tree of three possible steps — finish with a value, ask for a character, or emit a character. That tree is pure data, so its `Monad` instance is just sequencing of steps.

```haskell
data IO' a = Return a                  -- done, deliver an a
           | Input  (Char -> IO' a)    -- read a Char, continue
           | Output Char (IO' a)       -- write a Char, continue
```

```haskell
instance Functor IO' where
  fmap f (Return a)   = Return (f a)
  fmap f (Input g)    = Input  (\c -> fmap f (g c))
  fmap f (Output c k) = Output c (fmap f k)

instance Applicative IO' where
  pure = Return
  Return f   <*> x = fmap f x
  Input g    <*> x = Input  (\c -> g c <*> x)
  Output c k <*> x = Output c (k <*> x)

instance Monad IO' where
  return = pure
  Return a   >>= f = f a                       -- run f on the result
  Input g    >>= f = Input  (\c -> g c >>= f)  -- push the bind under the continuation
  Output c k >>= f = Output c (k >>= f)
```

Primitive effects and derived helpers:

```haskell
putChar' :: Char -> IO' ()
putChar' c = Output c (Return ())

getChar' :: IO' Char
getChar' = Input Return

getLine' :: IO' String
getLine' = do
  c <- getChar'
  if c == '\n' then return ""
               else do cs <- getLine'; return (c : cs)
```

```haskell
-- feed one program's output into another's input (process composition)
pipe :: IO' a -> IO' b -> IO' b
pipe (Output c p) (Input f) = pipe p (f c)
pipe (Output c p) q         = pipe p q
pipe (Return _)   q         = q
pipe (Input f)    q         = Input (\c -> pipe (f c) q)

-- run a program purely as a String -> String transformer (cf. real `interact`)
interact' :: IO' a -> String -> String
interact' (Return _)   _      = ""
interact' (Output c k) inp    = c : interact' k inp
interact' (Input f)    (x:xs) = interact' (f x) xs
interact' (Input _)    []     = ""

-- relabel every emitted character (e.g. a cipher on the output stream)
translate :: (Char -> Char) -> IO' a -> IO' a
translate _ (Return a)   = Return a
translate t (Input f)    = Input  (\c -> translate t (f c))
translate t (Output c k) = Output (t c) (translate t k)
```

Why it matters: `IO'` is the smallest example of the **free-monad / effect-as-data** idea behind Assignment 3's `Free`. If a question asks you to *implement* a monad over a constructor that pairs effects with a continuation, this is the shape.

## Question families this monad belongs to

- [`../question-families/state-game-family.md`](../question-families/state-game-family.md) — interactive game / main loops (the IO shell around a pure `State` core).
- [`../question-families/monad-combinator-family.md`](../question-families/monad-combinator-family.md) — `mapM_` / `replicateM` / `when` over `IO` are just the generic `Monad m =>` combinators specialised.

(IO has no dedicated family file — exam IO almost always wraps a pure simulation, so revise the family for the *inner* monad.)

## QuickCheck traps

- IO actions are not directly QuickCheck-testable. Assignment tests usually run the IO inside `unsafePerformIO` or use a fake-stdin harness.
- `replicateM 3 readLn` consumes exactly 3 lines; if you `replicateM 4` and only 3 are given, the marker hangs.
- `getLine` strips the `\n`. Don't compare against `"quit\n"`.

## Pitfalls

- `IO a` is OPAQUE — there is NO `runIO`.
- `return x` inside IO does NOT perform an effect; it just produces `x`.
- Don't reach for IO for things that don't actually need I/O (use State / Writer for pure simulations).
- Don't forget the `main :: IO ()` type signature in solutions that wrap a `main`.
- Lazy IO (`getContents`) interacts badly with `print` of partial results — usually safe in exam contexts but don't mix.
- `putStr` vs `putStrLn`: `putStr "x"` then `putStr "y"` produces `"xy"`, not `"x\ny"`.

## Worked examples

- Problems 101–104, 110.
- `fib3` in `monads.md` (printing during recursion).
- Assignment 1 Life animation.
- TicTacToe `main` loop (`tictactoe.hs`).

## See also

- [state.md](state.md) — use State when the "world" is pure (board, counter).
- [generic-combinators.md](generic-combinators.md) — `mapM_`, `replicateM`, `forM_` with IO.
- [list-monad.md](list-monad.md) — `mapM print xs` etc.

**Archetypes:** [A03 generic monad](../archetypes/A03-generic-monad.md) · [A23 mini-game](../archetypes/A23-mini-game.md)
**Cross-topic:** [game-state](../cross-matrix/game-state.md) — the IO loop around a pure `State` game.
**Question families:** [state-game](../question-families/state-game-family.md) · [monad-combinator](../question-families/monad-combinator-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
