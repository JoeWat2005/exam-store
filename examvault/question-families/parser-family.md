<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: parser**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · **parser** · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: parser

**Archetype:** A16 (parser combinators)   |   **Stars:** ⭐⭐⭐⭐⭐   |   **Course week(s):** 11
**Search keywords:** Parser, item, sat, digit, parseNat, parseExpr, sepBy, chainl, precedence, parseDigit, well-bracketed

> **WARNING - not an allowed import:** `Control.Applicative` (for `Alternative`, `empty`, `<|>`, `some`, `many`) is **NOT** on the exam whitelist — importing it scores **0**. The whole combinator kit below is usable in the exam ONLY when the question's own Parser/Types module already provides the `Parser` type and its `Alternative` instance for you. If you must build a parser from scratch with only whitelisted imports, hand-roll over `Maybe`/`State` instead (define your own `(<|>)`/`empty`/`many`/`some` as ordinary functions — no `Control.Applicative` needed).

## Generator template
```haskell
import Control.Applicative   -- WARNING: NOT whitelisted (see banner) — scores 0 unless supplied by the question's Parser module
import Data.Char (isDigit, isSpace)

newtype Parser a = P (String -> [(a, String)])

parse :: Parser a -> String -> [(a, String)]
parse (P f) = f

-- Functor/Applicative/Alternative/Monad instances are the seed for everything
instance Functor Parser where
  fmap g (P f) = P $ \s -> [ (g a, s') | (a, s') <- f s ]
instance Applicative Parser where
  pure x = P $ \s -> [(x, s)]
  P fp <*> P xp = P $ \s -> [ (f a, s'') | (f, s') <- fp s, (a, s'') <- xp s' ]
instance Alternative Parser where
  empty = P $ \_ -> []
  P f <|> P g = P $ \s -> case f s of
                            [] -> g s
                            xs -> xs
instance Monad Parser where
  return = pure
  P f >>= k = P $ \s -> [ r | (a, s') <- f s, r <- parse (k a) s' ]
```

Then everything is "use these combinators".

## Mutations (the examiner picks one)

### Mutation 1 — item / sat / digit (= problem 138)
**Sig:** `item :: Parser Char`, `sat :: (Char -> Bool) -> Parser Char`, `digitP :: Parser Char`
**Solution:**
```haskell
item :: Parser Char
item = P $ \s -> case s of
                   ""    -> []
                   c:cs  -> [(c, cs)]

sat :: (Char -> Bool) -> Parser Char
sat p = do c <- item
           if p c then return c else empty

digitP :: Parser Char
digitP = sat isDigit
```
**QC trap:** `item` on empty string returns `[]` (failure). `sat` uses `empty` from Alternative to signal failure.

### Mutation 2 — parseNat (= problem 139)
**Spec:** Parse one or more digits into an Int.
**Sig:** `parseNat :: Parser Int`
**Solution:**
```haskell
parseNat :: Parser Int
parseNat = do
  ds <- some digitP
  return (read ds)
```
**QC trap:** `some` requires at least one match. `many` allows zero. Use `some` here — natural numbers have at least one digit.

### Mutation 3 — char / string (literal parsers)
**Sig:** `char :: Char -> Parser Char`, `string :: String -> Parser String`
**Solution:**
```haskell
char :: Char -> Parser Char
char c = sat (== c)

string :: String -> Parser String
string ""     = return ""
string (c:cs) = do _ <- char c
                   _ <- string cs
                   return (c:cs)
```
**QC trap:** `string ""` parses any input successfully, returning "". Consume nothing. This is intentional.

### Mutation 4 — token (eat surrounding whitespace)
**Sig:** `token :: Parser a -> Parser a`
**Solution:**
```haskell
spaces :: Parser ()
spaces = do _ <- many (sat isSpace)
            return ()

token :: Parser a -> Parser a
token p = do _ <- spaces
             x <- p
             _ <- spaces
             return x
```
**QC trap:** Consuming whitespace *after* the token can swallow the whitespace before the next token unnecessarily. The convention is "skip leading whitespace before each token, none after". Read spec.

### Mutation 5 — sepBy / sepBy1
**Spec:** Parse a list of items separated by a separator.
**Sig:** `sepBy :: Parser a -> Parser sep -> Parser [a]`
**Solution:**
```haskell
sepBy :: Parser a -> Parser sep -> Parser [a]
p `sepBy` sep = (p `sepBy1` sep) <|> return []

sepBy1 :: Parser a -> Parser sep -> Parser [a]
p `sepBy1` sep = do
  x  <- p
  xs <- many (sep *> p)
  return (x:xs)
```
**QC trap:** `sepBy1` requires at least one match; `sepBy` allows empty. The `*>` operator (from Applicative) discards the separator.

### Mutation 6 — chainl1 (left-associative binary operator chain)
**Spec:** Parse `a op a op a ...` left-associatively.
**Sig:** `chainl1 :: Parser a -> Parser (a -> a -> a) -> Parser a`
**Solution:**
```haskell
chainl1 :: Parser a -> Parser (a -> a -> a) -> Parser a
chainl1 p op = do
  x <- p
  rest x
  where
    rest x = (do
      f <- op
      y <- p
      rest (f x y)) <|> return x
```
**QC trap:** Left-association is built into the accumulator pattern. For right-association, recurse on the tail instead.

### Mutation 7 — parseExpr (precedence-aware) (= problem 140)
**Spec:** Parse arithmetic with `+` and `*` respecting precedence.
**Sig:** `parseExpr :: Parser Int`
**Solution:**
```haskell
parseExpr :: Parser Int
parseExpr = do
  t <- parseTerm
  (do _ <- char '+'; e <- parseExpr; return (t + e)) <|> return t

parseTerm :: Parser Int
parseTerm = do
  f <- parseFactor
  (do _ <- char '*'; t <- parseTerm; return (f * t)) <|> return f

parseFactor :: Parser Int
parseFactor = parseNat <|> (do _ <- char '('; e <- parseExpr; _ <- char ')'; return e)
```
**QC trap:** Right-recursive (gives right-associativity for `+`). For left-associativity use chainl1. Grammar from spec: `expr ::= term '+' expr | term`.

### Mutation 8 — parseBool / parseKeyword
**Sig:** `parseBool :: Parser Bool`
**Solution:**
```haskell
parseBool :: Parser Bool
parseBool = (string "True"  >> return True)
         <|> (string "False" >> return False)
```
**QC trap:** Order matters in `<|>`. If you tried "T" before "True", you'd misparse. Use longer alternatives first.

### Mutation 9 — well-bracketed (= Assignment 2 Ex 6)
**Spec:** Parse a string of `()/{}` into a Bracket tree.
**Sig:** `tree :: String -> Maybe Bracket`
**Solution:**
```haskell
data Bracket = Round [Bracket] | Curly [Bracket]

parseBracket :: Parser Bracket
parseBracket = parseRound <|> parseCurly
  where
    parseRound = do _ <- char '('
                    bs <- many parseBracket
                    _ <- char ')'
                    return (Round bs)
    parseCurly = do _ <- char '{'
                    bs <- many parseBracket
                    _ <- char '}'
                    return (Curly bs)

tree :: String -> Maybe Bracket
tree s = case parse parseBracket s of
           [(b, "")] -> Just b
           _         -> Nothing
```
**QC trap:** The empty string must fail (no bracket tree). Check that the result consumes the *entire* input ("").

### Mutation 10 — parseFloat / parseSigned (combining sub-parsers)
**Spec:** Parse signed decimal numbers.
**Sig:** `parseFloat :: Parser Double`
**Solution:**
```haskell
parseFloat :: Parser Double
parseFloat = do
  sign <- (char '-' >> return (-1)) <|> return 1
  int  <- some digitP
  frac <- (do _ <- char '.'
              fs <- some digitP
              return ("." ++ fs)) <|> return ""
  return (sign * read (int ++ frac))
```
**QC trap:** Optional fractional part needs `<|> return ""` to allow integer input.

## Hidden-predicate mutations
- "Parse only if some semantic check holds" → use `do x <- ...; if check x then return x else empty`.
- "Restrict to a subset of input chars" → `sat (`elem` allowedChars)`.

## Accumulator-style alternative
`chainl1` is *itself* an accumulator pattern in parser form. For deeply nested grammars, the explicit accumulator is more efficient than naive recursion.

## Fold-style alternative
```haskell
parseAddFold :: Parser Int
parseAddFold = do
  ns <- parseNat `sepBy1` char '+'
  return (sum ns)
```
Cleaner — uses sepBy1, but loses operator precedence for mixed `+`/`*`.

## Cross-family combinations
- this family + `pretty-print-family.md`: pretty ↔ parse round trip.
- this family + `adt-translation-family.md`: parser → AST → translate.
- this family + `env-eval-family.md`: parser → eval.
- this family + `codec-family.md`: decoders are parsers.

## QuickCheck universal attacks
- **Round trip:** `parse parseExpr (pretty e) == [(e', "")]` where `e' == e` (modulo precedence-induced rebalancing).
- **Total parsing:** result must consume the entire input — `[(_, "")]`.
- **Failure on garbage:** parser of `[]` on bad input.
- **Identity:** `parse (return x) s == [(x, s)]`.
- **Monad laws:** the Parser type satisfies them.

## Pitfalls (per mutation)
- M1: returning `[]` for non-empty match.
- M2: using `many` instead of `some`.
- M3: `string ""` consuming a character.
- M4: consuming trailing whitespace mid-stream.
- M5: `sepBy` returning `[]` on first item failure.
- M6: getting associativity wrong.
- M7: precedence grammar wrong — flat `parseExpr = parseNat <|> ... <|> ...` doesn't respect precedence.
- M8: `<|>` order matters for prefixes.
- M9: not checking remainder is "".
- M10: not handling optional fractional part.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — chainr1 (right-associative operator chain)

**Spec:** Parse `a op a op a ...` **right**-associatively — the right-assoc dial-flip of `chainl1` (Mutation 6). `a op (a op (a op …))` instead of `((a op a) op a)`.

**Type sig:** `chainr1 :: Parser a -> Parser (a -> a -> a) -> Parser a`

```haskell
chainr1 :: Parser a -> Parser (a -> a -> a) -> Parser a
chainr1 p op = do x <- p
                  (do f <- op; y <- chainr1 p op; return (f x y)) <|> return x
```

*One-line note:* right-assoc dial-flip of `chainl1` — instead of an accumulator that folds left, it recurses on the tail and applies the operator on the way back up, so `f` associates to the right.

**What changes vs seed:** No accumulator helper — the recursion is on the *rest* of the input (`chainr1 p op` on the tail), and `f x y` is built after the recursive call returns, giving right-nesting. This is the structurally-different counterpart to Mutation 6's left-fold `chainl1`.

**QC trap:** Swapping `chainl1` for `chainr1` flips `(a-b)-c` to `a-(b-c)` — e.g. `parse (chainr1 nat (char '-' >> return (-))) "10-2-3"` yields `11` (= `10-(2-3)`) as its first result, whereas `chainl1` yields `5` (= `(10-2)-3`). The marker distinguishes them with a non-associative operator like `-`.

## See also

**Primary archetype:** [A16 parser combinators](../archetypes/A16-parser-combinators.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
