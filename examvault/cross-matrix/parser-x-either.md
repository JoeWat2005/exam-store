<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [cross-matrix](./README.md) · **Cross: Parser × Either (custom error type)**

<!-- siblings:start -->
> **Peers:** [bst × state](./bst-x-state.md) · [bst × writer](./bst-x-writer.md) · [expr × maybe](./expr-x-maybe.md) · [expr × multi](./expr-x-multi.md) · [expr × state](./expr-x-state.md) · [game-state](./game-state.md) · [list × list-monad](./list-x-list-monad.md) · [list × monad](./list-x-monad.md) · [list × state](./list-x-state.md) · [list × writer](./list-x-writer.md) · **parser × either** · [rose × state](./rose-x-state.md) · [rose × writer](./rose-x-writer.md) · [tree × either](./tree-x-either.md) · [tree × generic-monad](./tree-x-generic-monad.md) · [tree × maybe](./tree-x-maybe.md) · [tree × reader](./tree-x-reader.md) · [tree × state](./tree-x-state.md) · [tree × writer](./tree-x-writer.md) · [writer × either](./writer-x-either.md)
<!-- siblings:end -->






# Cross: Parser × Either (custom error type)

**Why this combo:** the default `Parser a = Parser (String -> Maybe (a, String))` parser fails silently with `Nothing`. For interpreter/codec tasks you often want **descriptive errors** — "expected `+` at position 7" — which means switching the inner `Maybe` to `Either ParseErr`. Same parser combinators, richer failure mode.

**Recognition triggers:**
- "Return a meaningful error if parsing fails"
- "Report the position of the syntax error"
- "Distinguish between unexpected EOF and unexpected character"
- Sig like `parse :: String -> Either String (a, String)`

**Search keywords:** parser · Either · custom error · ParseErr · MonadError · descriptive failure · position tracking

## Type definition

```haskell
data ParseErr = UnexpectedEOF
              | Unexpected Char
              | ExpectedButGot String Char
              | Custom String
  deriving (Eq, Show)

newtype Parser a = Parser { parse :: String -> Either ParseErr (a, String) }
```

The shape `String -> Either ParseErr (a, String)` is identical to `String -> Maybe (a, String)` except `Either ParseErr` carries a typed error.

## Functor / Applicative / Monad instances

The instances are the same shape as the `Maybe` parser but pass the error through.

```haskell
instance Functor Parser where
  fmap f (Parser p) = Parser $ \s -> case p s of
    Right (a, s') -> Right (f a, s')
    Left  e       -> Left e

instance Applicative Parser where
  pure x = Parser $ \s -> Right (x, s)
  Parser pf <*> Parser pa = Parser $ \s -> do
    (f, s1) <- pf s        -- in the Either monad
    (a, s2) <- pa s1
    return (f a, s2)

instance Monad Parser where
  return = pure
  Parser pa >>= k = Parser $ \s -> do
    (a, s1) <- pa s
    parse (k a) s1
```

`do`-notation inside `parse` runs in the `Either ParseErr` monad — `Left e` short-circuits without trying the rest.

## Primitives

```haskell
item :: Parser Char
item = Parser $ \s -> case s of
  ""     -> Left UnexpectedEOF
  (c:cs) -> Right (c, cs)

sat :: (Char -> Bool) -> Parser Char
sat p = Parser $ \s -> case s of
  ""     -> Left UnexpectedEOF
  (c:cs) | p c -> Right (c, cs)
         | otherwise -> Left (Unexpected c)

char :: Char -> Parser Char
char c = Parser $ \s -> case s of
  ""     -> Left UnexpectedEOF
  (x:xs) | x == c -> Right (c, xs)
         | otherwise -> Left (ExpectedButGot [c] x)

throwParseError :: ParseErr -> Parser a
throwParseError e = Parser $ \_ -> Left e
```

Compare with the `Maybe` parser's `item`: identical shape, but `Nothing` becomes `Left UnexpectedEOF`. **Every failure mode now carries a name.**

## Alternative — backtracking with error preservation

```haskell
import Control.Applicative

instance Alternative Parser where
  empty = throwParseError (Custom "empty")
  Parser p <|> Parser q = Parser $ \s -> case p s of
    Right r -> Right r
    Left _  -> q s        -- discard left's error if right succeeds
```

**Design choice:** on backtracking, do you discard the left error, keep it, or merge both? The simple version above discards. A more sophisticated parser keeps the error that consumed the most input — see "longest match wins" parsing.

## Worked example: parser for `let x = 5 in x + 1`

```haskell
data LetExpr = Num Int | Var String | LetE String LetExpr LetExpr | Add LetExpr LetExpr
  deriving (Show, Eq)

token :: Parser a -> Parser a
token p = many (sat isSpace) *> p

reserved :: String -> Parser ()
reserved w = token (string w) *> pure ()

identifier :: Parser String
identifier = token (some (sat isAlpha))

number :: Parser Int
number = token (read <$> some (sat isDigit))

letExpr :: Parser LetExpr
letExpr =
  do reserved "let"
     x   <- identifier
     reserved "="
     e1  <- letExpr
     reserved "in"
     e2  <- letExpr
     return (LetE x e1 e2)
  <|> addExpr

addExpr :: Parser LetExpr
addExpr = atom `chainl1` (Add <$ token (char '+'))

atom :: Parser LetExpr
atom = (Num <$> number)
   <|> (Var <$> identifier)

runParse :: String -> Either ParseErr LetExpr
runParse s = case parse letExpr s of
  Right (e, "") -> Right e
  Right (_, rs) -> Left (Custom ("trailing input: " ++ rs))
  Left e        -> Left e
```

Sample runs:

```
ghci> runParse "let x = 5 in x + 1"
Right (LetE "x" (Num 5) (Add (Var "x") (Num 1)))

ghci> runParse "let x = 5 in"
Left UnexpectedEOF

ghci> runParse "let 7 = 5 in 7"
Left (Unexpected '7')        -- identifier expected
```

## Common operations summary

| Operation | `Maybe` parser | `Either` parser |
|---|---|---|
| Success | `Just (a, s')` | `Right (a, s')` |
| Failure | `Nothing` (anonymous) | `Left e` (typed) |
| Branch | `<\|>` tries right on Nothing | `<\|>` tries right on Left _ |
| Bubble error up | impossible (info lost) | `Left e` survives every `bind` |
| Custom abort | restart with `empty` | `throwParseError (Custom "...")` |

## QuickCheck properties

```haskell
prop_parse_letRoundTrip :: LetExpr -> Bool
prop_parse_letRoundTrip e = case runParse (pretty e) of
  Right e' -> e' == e
  Left  _  -> False

prop_parse_typedError :: Property
prop_parse_typedError =
  parse letExpr "let 7 = 5 in 7" === Left (Unexpected '7')

prop_parse_eofVsBadChar :: Property
prop_parse_eofVsBadChar =
  parse (char 'a') ""  === Left UnexpectedEOF .&&.
  parse (char 'a') "b" === Left (ExpectedButGot "a" 'b')
```

These properties confirm that errors are not just *present* but *typed correctly* — the marker can compare your error to the expected error.

## QuickCheck traps

- `Arbitrary ParseErr` — must include all four constructors with frequencies, especially `UnexpectedEOF` (often forgotten).
- Round-trip property requires `pretty :: LetExpr -> String` that produces parseable output; many students get this almost-right but not exactly.
- A parser that returns `Right (_, leftover)` when input wasn't fully consumed is a partial-parse trap — wrap with the `runParse` helper above.

## See also

**Combined archetypes:** [A16 parser combinators](../archetypes/A16-parser-combinators.md) · [A08 env eval](../archetypes/A08-env-eval.md) · [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Theory:** [parser overview](../interpreters/parser-overview.md) · [parser chainl1](../interpreters/parser-chainl1.md) · [Either monad](../monads/either.md) · [MonadError](../monads/monaderror.md) · [Alternative typeclass](../typeclasses/alternative.md)
**Question families:** [parser](../question-families/parser-family.md) · [error-handling](../question-families/error-handling-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md) · [maybe/either attacks](../quickcheck/maybe-either-attacks.md) · [property patterns](../quickcheck/PROPERTY-PATTERNS.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
