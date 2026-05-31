<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 12 — `run :: Program -> Storage -> Storage` (Birmingham imperative `xy` language)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · **imperative-eval** · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 12 — `run :: Program -> Storage -> Storage` (Birmingham imperative `xy` language)

**Effect:** function-storage transformer
**Effect rationale:** programs are *storage transformers*: take a starting memory, produce an ending memory. `:=` writes, `If` / `IfElse` / `While` branch, `Block` sequences. No monad needed — direct recursion with explicit state.
**Type signature:** `run :: Program -> Storage -> Storage`
**Search keywords:** imperative · xy-language · run · while · assignment · block · if-else · :=  · birmingham-interpreter · storage-transformer · program-eval

## Setup
```haskell
import AbstractSyntax        -- in the lecture project
-- For a self-contained exam answer, include the data definitions inline:

type Identifier = String
type Storage    = Identifier -> Integer

data OpName = Or | And | Eq | Leq | Less | Geq | Greater
            | Add | Sub | Mul | Div | Mod | Not
            deriving (Show)

data Expr = Constant Integer
          | Var Identifier
          | Op OpName [Expr]
          deriving (Show)

data Program = Identifier := Expr        -- assignment (infix ctor)
             | Block [Program]
             | While Expr Program
             | If Expr Program
             | IfElse Expr Program Program
             deriving (Show)
```
Source: `fp-learning-2025/files/LectureNotes/Sections/interpreter/AbstractSyntax.hs`.

## Helpers (from [imperative-storage.md](imperative-storage.md))
```haskell
emptyStorage :: Storage
emptyStorage i = error ("Uninitialized variable " ++ i)

update :: Identifier -> Integer -> Storage -> Storage
update i x m = \j -> if i == j then x else m j

number :: Bool -> Integer
number False = 0; number True = 1

boolean :: Integer -> Bool
boolean 0 = False; boolean _ = True
```

## Expression evaluation
```haskell
eval :: Storage -> Expr -> Integer
eval m (Constant n) = n
eval m (Var i)      = m i
eval m (Op o es)    = opEval o [eval m e | e <- es]

opEval :: OpName -> [Integer] -> Integer
opEval Add     [x, y] = x + y
opEval Sub     [x, y] = x - y
opEval Mul     [x, y] = x * y
opEval Div     [x, y] = x `div` y
opEval Mod     [x, y] = x `mod` y
opEval Eq      [x, y] = number (x == y)
opEval Leq     [x, y] = number (x <= y)
opEval Less    [x, y] = number (x <  y)
opEval Geq     [x, y] = number (x >= y)
opEval Greater [x, y] = number (x >  y)
opEval And     [x, y] = number (boolean x && boolean y)
opEval Or      [x, y] = number (boolean x || boolean y)
opEval Not     [x]    = number (not (boolean x))
opEval op      xs     = error ("Interpreter bug: " ++ show op ++ " on " ++ show xs)
```

## The runner — direct style
```haskell
run :: Program -> Storage -> Storage

run (i := e) m =
  update i (eval m e) m

run (IfElse e p q) m
  | boolean (eval m e) = run p m
  | otherwise          = run q m

run (If e p) m
  | boolean (eval m e) = run p m
  | otherwise          = m

run (While e p) m
  | boolean (eval m e) = m''
  | otherwise          = m
  where
    m'  = run p m
    m'' = run (While e p) m'

run (Block []) m =
  m

run (Block (p : ps)) m =
  m''
  where
    m'  = run p m
    m'' = run (Block ps) m'
```

The constructors:

| Ctor | Behaviour |
|---|---|
| `i := e` | evaluate `e`, write to `i`, keep going from updated storage |
| `IfElse e p q` | if `e` truthy, run `p`; else run `q`; same starting storage either way |
| `If e p` | if `e` truthy, run `p`; else leave storage unchanged |
| `While e p` | if `e` truthy, run `p` then recurse; else stop |
| `Block []` | no-op |
| `Block (p:ps)` | run `p` first, then `Block ps` on the result |

## The runner — point-free / combinator style (`run'`)

Express each ctor as a value of type `Storage -> Storage`:

```haskell
assign :: Identifier -> Expr -> Storage -> Storage
assign i e = \m -> update i (eval m e) m

ifElse :: (s -> Bool) -> (s -> s) -> (s -> s) -> (s -> s)
ifElse p f g = \m -> if p m then f m else g m

while :: (s -> Bool) -> (s -> s) -> (s -> s)
while p f = g where g m = if p m then g (f m) else m

block :: [s -> s] -> s -> s
block []     m = m
block (f:fs) m = block fs (f m)

booleanValue :: Expr -> (Storage -> Bool)
booleanValue e = \m -> boolean (eval m e)

run' :: Program -> Storage -> Storage
run' (i := e)       = assign i e
run' (IfElse e p q) = ifElse (booleanValue e) (run' p) (run' q)
run' (If e p)       = ifElse (booleanValue e) (run' p) id
run' (While e p)    = while  (booleanValue e) (run' p)
run' (Block ps)     = block  (map run' ps)
```

> The lecture remark: this shows **imperative programming is functional programming** — each statement is a *value* of type `Storage -> Storage`.

## Worked example — `fibonacci.xy`

Source program:
```
{
  y := 0;
  z := 1;
  while (x > 0)
  {
    x := x - 1;
    t := y + z;
    y := z;
    z := t;
  }
}
```

Initial storage: `update "x" 11 emptyStorage`.

After parsing and running:
```haskell
run program (update "x" 11 emptyStorage)        -- final storage
   "y"                                            -- = 89  (Fib(11))
```

Run on the lecture command-line:
```
$ runhaskell Runxy.hs fibonacci.xy 11
89
```

## Per-constructor diagram

```
i := e        m -----> update i (eval m e) m
                       (one new entry in storage)

IfElse e p q
              ?
            cond m
            /       \
        true         false
       run p m     run q m

If e p
              ?
            cond m
            /       \
        true         false
       run p m       m       (unchanged)

While e p     m -- loop until cond false --> m_final
              repeat: m_{n+1} = run p m_n

Block [p1,...,pn]  m
              m -> run p1 -> m1 -> run p2 -> m2 -> ... -> mn
```

## Mutations
- **Add boolean type (don't encode in Integer).** `type Storage = String -> Maybe Value`, `data Value = IntV Integer | BoolV Bool`.
- **Add IO** (`print`, `read`). Now `run :: Program -> Storage -> IO Storage`.
- **Add error mode.** Replace `eval` with `eval :: Storage -> Expr -> Maybe Integer` and `run` with `run :: Program -> Storage -> Maybe Storage`.
- **Add functions / procedures.** Storage holds function values; new `Call f args` ctor in `Program`.
- **Add scope.** Storage becomes a stack of frames: `[String -> Integer]`.

## Pitfalls
- **`i := e` uses infix ctor syntax.** Match with `(i := e)` — parens required.
- **Forgetting to thread the updated storage in `Block`.** Each statement must see the result of the **previous** statement, not the original storage.
- **`While` is partial.** It can loop forever. Don't `quickCheck` an infinite-loop case.
- **`IfElse` uses `boolean (eval m e)`.** `eval m e == 0` means false; anything else means true. The lecture uses `number False = 0; number True = 1`, and `boolean` is the inverse retract.
- **`If` without else.** Returns the **original** `m`, not `emptyStorage` or `error`.
- **Mixing `run` and `run'`** in answers: they're observationally equal but you shouldn't claim one form when you wrote the other.
- **`run (i := e) m`** is `update i (eval m e) m`, NOT `update i (eval emptyStorage e) m`. `eval` needs the current `m` to look up `Var`s in `e`.
- **`Block ps`** is left-to-right; reversing gives wrong semantics for sequenced statements.

## QuickCheck attacks
- `run (Block []) m == m` — empty block is identity.
- `run (i := Constant 5) m i == 5` — assignment writes.
- `run (i := Constant 5) m j == m j` for `i /= j` — assignment leaves other keys alone.
- `run (If (Constant 0) p) m == m` — false condition means no change.
- `run (IfElse (Constant 1) p q) == run p` (as functions) — true condition picks `then`.
- `run program initStorage` on `fibonacci.xy` with `x=11` gives `89` at `"y"`.
- Idempotency: `If (Var x == Var x) p` is equivalent to `p` (assuming `x` is initialised).

## Extend pattern
Question: "Add `Print Expr` that doesn't change storage."
1. **AST:** add `| Print Expr` to `Program`.
2. **Parser:** rule for `print(...)` — add to the disjunction in `program`.
3. **Eval:** `run` now needs `IO`:
```haskell
run :: Program -> Storage -> IO Storage
run (Print e) m = do print (eval m e); return m
-- and lift all other branches into IO
```
This is a **big change** — `run` is no longer pure. Alternative: collect prints in a `Writer [Integer]` layer:
```haskell
run :: Program -> Storage -> (Storage, [Integer])
run (Print e) m = (m, [eval m e])
run (Block (p:ps)) m = let (m', log1) = run p m
                          (m'', log2) = run (Block ps) m'
                      in (m'', log1 ++ log2)
-- ...
```
Or use `Writer` monad directly.

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md)
**Question families:** [env-eval](../question-families/env-eval-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)
**Related (interpreters):** [imperative storage](./imperative-storage.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
