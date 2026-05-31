<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Parser: chainl1, backtracking, precedence**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · **parser-chainl1** · [parser-overview](./parser-overview.md) · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Parser combinators — `chainl1`, backtracking, operator precedence

`parser-overview.md` covers the basics (parser type, `Functor`/`Applicative`/`Monad` instances, primitive `item` and `sat`). This page covers what's needed for **operator-precedence parsing** — the shape that comes up in exam Expr-tree questions.

Parser type used throughout (the course's standard form):

```haskell
newtype Parser a = Parser { parse :: String -> Maybe (a, String) }

instance Functor Parser where
  fmap f (Parser p) = Parser $ \s -> fmap (\(a,s') -> (f a, s')) (p s)

instance Applicative Parser where
  pure x = Parser $ \s -> Just (x, s)
  Parser pf <*> Parser pa = Parser $ \s -> do
    (f, s1) <- pf s
    (a, s2) <- pa s1
    return (f a, s2)

instance Monad Parser where
  return = pure
  Parser pa >>= k = Parser $ \s -> do
    (a, s1) <- pa s
    parse (k a) s1
```

Standard primitives:

```haskell
item :: Parser Char
item = Parser $ \s -> case s of
  ""     -> Nothing
  (c:cs) -> Just (c, cs)

sat :: (Char -> Bool) -> Parser Char
sat p = do c <- item; if p c then return c else empty

char :: Char -> Parser Char
char c = sat (== c)

digit :: Parser Char
digit = sat isDigit

nat :: Parser Int
nat = read <$> some digit
```

## `<|>` and `try` (backtracking)

`<|>` from `Alternative` tries the left parser; if it fails, tries the right:

```haskell
import Control.Applicative

instance Alternative Parser where
  empty = Parser (const Nothing)
  Parser p <|> Parser q = Parser $ \s -> case p s of
    Just r  -> Just r
    Nothing -> q s
```

**Crucial:** with `Maybe`-based parsers, `<|>` already backtracks "for free" because `Nothing` carries no consumed input. Megaparsec / Parsec users see `try` to *explicitly* backtrack — in this course's parser, every `<|>` is implicitly backtracking. **You don't need `try`.**

```haskell
keyword :: Parser String
keyword = string "let"  <|> string "in"  <|> string "case"
```

If `string "let"` fails after consuming "l" and "e", the implicit Maybe failure means the next branch starts again from the original input. (In Parsec it would fail to consume on a mismatch only with `try`.)

## `chainl1` — left-associative operator parsing

For `1 + 2 + 3 + 4` (which should parse left-associative: `((1+2)+3)+4`), use:

```haskell
chainl1 :: Parser a -> Parser (a -> a -> a) -> Parser a
chainl1 p op = do
  x <- p
  rest x
  where
    rest x = (do f <- op
                 y <- p
                 rest (f x y))
             <|> return x
```

Read: parse one `p`, then in a loop try `op` + `p` and re-bracket on the left. Stop when no more `op` matches.

For right-associative (`a ^ b ^ c = a ^ (b ^ c)`):

```haskell
chainr1 :: Parser a -> Parser (a -> a -> a) -> Parser a
chainr1 p op = do
  x <- p
  (do f <- op; y <- chainr1 p op; return (f x y)) <|> return x
```

## Operator-precedence example: `1 + 2 * 3`

The standard recipe — one parser per precedence level, lowest-precedence at the top:

```haskell
data Expr = Num Int | Add Expr Expr | Mul Expr Expr deriving Show

expr   :: Parser Expr
expr   = term   `chainl1` addOp

term   :: Parser Expr
term   = factor `chainl1` mulOp

factor :: Parser Expr
factor = (Num <$> nat)
       <|> (char '(' *> expr <* char ')')

addOp :: Parser (Expr -> Expr -> Expr)
addOp = Add <$ char '+'

mulOp :: Parser (Expr -> Expr -> Expr)
mulOp = Mul <$ char '*'
```

Trace on input `"1+2*3"`:

```
expr "1+2*3"
  = term `chainl1` addOp
  = (factor `chainl1` mulOp) `chainl1` addOp

  term:  factor "1+2*3" → (Num 1, "+2*3")
         rest (Num 1):  mulOp fails on '+' → return Num 1

  expr: rest (Num 1):
        addOp '+' succeeds → '+' consumed, "2*3"
        term "2*3":
          factor "2*3" → (Num 2, "*3")
          rest (Num 2):
            mulOp '*' succeeds, "3"
            factor "3" → (Num 3, "")
            rest (Num 3): all ops fail → return Num 3
            back in rest (Num 2): bracketed Mul (Num 2) (Num 3)
          rest (Mul (Num 2) (Num 3)): all fail → return
        back in rest (Num 1): bracketed Add (Num 1) (Mul (Num 2) (Num 3))
        rest (Add ...): addOp fails (input empty) → return
  result: (Add (Num 1) (Mul (Num 2) (Num 3)), "")
```

✓ Precedence respected by structure: `*` binds tighter because it's parsed at the inner level.

## Applicative-only variant (no `do`)

For `chainl1` written without Monad:

```haskell
chainl1A :: Parser a -> Parser (a -> a -> a) -> Parser a
chainl1A p op = foldl (\acc (f, y) -> f acc y) <$> p <*> many ((,) <$> op <*> p)
```

Trade-off: shorter, but harder to read. The `do`-notation version above is the exam-friendly form.

## Failure recovery

If a parser fails partway, `<|>` falls back to the alternative. For a graceful "parse error at position X" message you'd need to switch to `Either`-based parsers (which carry an error) or add a position counter. The course doesn't require this — your parser returns `Nothing` and the caller decides what to do.

## QuickCheck properties

```haskell
prop_parse_complete :: Expr -> Bool
prop_parse_complete e = parse expr (pretty e) == Just (e, "")

prop_precedence_add_mul :: Int -> Int -> Int -> Bool
prop_precedence_add_mul a b c =
  parse expr (show a ++ "+" ++ show b ++ "*" ++ show c) ==
  Just (Add (Num a) (Mul (Num b) (Num c)), "")

prop_left_assoc :: Int -> Int -> Int -> Bool
prop_left_assoc a b c =
  parse expr (show a ++ "+" ++ show b ++ "+" ++ show c) ==
  Just (Add (Add (Num a) (Num b)) (Num c), "")
```

Round-trip property `parse . pretty == id` (modulo Maybe wrapping) is the gold standard.

## Common bugs

| Bug | Symptom | Fix |
|---|---|---|
| `expr = expr + term` (left-recursive direct definition) | Infinite loop on first call | Use `chainl1`. |
| `expr = term + expr` (right-recursive) | Wrong associativity — `1+2+3` parses as `1+(2+3)` | Use `chainl1` for left-assoc, `chainr1` for right. |
| `term = factor` at lowest level | No multiplication precedence | Put `mulOp`-chaining BETWEEN `factor` and `expr`. |
| `factor = nat <\|> (char '(' *> expr)` (no closing paren) | Hangs / wrong parse | Add `<* char ')'` to consume the closing paren. |
| Forgetting `*>` vs `>>`, or `<$` vs `<$>` | Type errors | `*>` is `Applicative` sequence; `<$` is `f <$ p` = `const f <$> p`. |

## See also

**Theory:** [parser overview](./parser-overview.md) · [Alternative typeclass](../typeclasses/alternative.md) · [Applicative typeclass](../typeclasses/applicative.md) · [Monad typeclass](../typeclasses/monad.md)
**Archetypes:** [A16 parser combinators](../archetypes/A16-parser-combinators.md) · [A24 applicative instance](../archetypes/A24-applicative-instance.md) · [A08 env eval](../archetypes/A08-env-eval.md)
**Question families:** [parser](../question-families/parser-family.md) · [env-eval](../question-families/env-eval-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [property patterns](../quickcheck/PROPERTY-PATTERNS.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
