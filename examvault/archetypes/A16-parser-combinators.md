<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A16 — Parser Combinators**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · **A16** · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A16 — Parser Combinators

**Tier:** 3   |   **Stars:** ⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** A2 (Ex 6 bracket tree — parser-like via Maybe state)
**Combines with:** A06 · A01 · A19 · A05
**Search keywords:** Parser · newtype · `String -> [(a, String)]` · sat · item · token · many · some · `<|>` · expr · term · factor

## What it tests
Whether you can build the parser-combinator machinery (`Parser` newtype, `Functor`/`Applicative`/`Monad`/`Alternative` instances, `item`, `sat`), then use them to parse a grammar with precedence (typically arithmetic expressions).

## Recognition triggers
- `newtype Parser a = P (String -> [(a, String)])` or `Maybe (a, String)`
- Grammar in BNF: `expr ::= term '+' expr | term`, `term ::= factor '*' term | factor`, `factor ::= nat | '(' expr ')'`
- "Build a parser for arithmetic expressions"
- `many`, `some`, `<|>`, `chainl1` mentioned
- Test cases like `parse expr "1+2*3" == [(7, "")]`

> **WARNING - not an allowed import:** `Control.Applicative` (for `Alternative`, `empty`, `<|>`, `some`, `many`) is **NOT** on the exam whitelist — importing it scores **0**. This combinator `Parser` is therefore usable ONLY if the question's own Types module already supplies the `Parser` type *and* its instances for you. If you have to build the parser from scratch under exam conditions, prefer a hand-rolled `Maybe`/`State` parser (everything below works with `newtype Parser a = P (String -> Maybe (a, String))` and plain `case`/`do` — no `Alternative` needed).

## Canonical template
```haskell
import Control.Applicative (Alternative(..))   -- WARNING: NOT whitelisted (see banner) — scores 0 unless provided by the Types module
import Control.Monad (MonadPlus(..))
import Data.Char (isDigit, isSpace)

newtype Parser a = P { parse :: String -> [(a, String)] }

instance Functor Parser where
  fmap f (P p) = P (\s -> [(f a, s') | (a, s') <- p s])

instance Applicative Parser where
  pure a = P (\s -> [(a, s)])
  P pf <*> P pa = P (\s -> [(f a, s2) | (f, s1) <- pf s, (a, s2) <- pa s1])

instance Monad Parser where
  P p >>= f = P (\s -> concat [parse (f a) s' | (a, s') <- p s])

instance Alternative Parser where
  empty       = P (\_ -> [])
  P p <|> P q = P (\s -> p s ++ q s)

instance MonadPlus Parser   -- empty body: mzero = empty, mplus = (<|>) via defaults
```
Note: the mutations below still write `mzero`/`mplus`; the empty-body `MonadPlus` instance supplies those from `Alternative` (`mzero = empty`, `mplus = (<|>)`), so they compile unchanged. You may also write `empty`/`<|>` directly.

## Mutations (the examiner picks one)

### M1 — primitives
```haskell
item :: Parser Char
item = P (\s -> case s of [] -> []; (c:cs) -> [(c, cs)])

sat :: (Char -> Bool) -> Parser Char
sat p = do c <- item
           if p c then return c else mzero

digitP :: Parser Char
digitP = sat isDigit

char :: Char -> Parser Char
char c = sat (== c)
```
What changes: building blocks; never re-use, just compose.

### M2 — `many` and `some`
```haskell
many' :: Parser a -> Parser [a]
many' p = some' p `mplus` return []

some' :: Parser a -> Parser [a]
some' p = do x  <- p
             xs <- many' p
             return (x:xs)
```
What changes: mutual recursion: `some` requires at least one, `many` allows zero.

### M3 — `nat` (parse one or more digits, problem 139)
```haskell
nat :: Parser Int
nat = do cs <- some' digitP
         return (read cs)
```
What changes: wraps `read`; uses `some'`.

### M4 — `token` (strip whitespace)
```haskell
space :: Parser ()
space = many' (sat isSpace) >> return ()

token :: Parser a -> Parser a
token p = space *> p <* space
```
What changes: skips surrounding whitespace; wrap every primitive with `token` for readable grammars.

### M5 — `expr` arithmetic (problem 140)
```haskell
expr :: Parser Int
expr = do t <- term
          (do char '+'; e <- expr; return (t + e)) `mplus` return t

term :: Parser Int
term = do f <- factor
          (do char '*'; t <- term; return (f * t)) `mplus` return f

factor :: Parser Int
factor = nat `mplus` do char '('; e <- expr; char ')'; return e
```
What changes: right-recursive (avoids left recursion); precedence enforced by `expr → term → factor` nesting.

### M6 — `chainl1` (left-assoc binary op)
```haskell
chainl1 :: Parser a -> Parser (a -> a -> a) -> Parser a
chainl1 p op = do x <- p; rest x
  where rest x = (do f <- op; y <- p; rest (f x y)) `mplus` return x
```
What changes: left-fold with operator parser between; classical solution to left-recursive grammars.

### M7 — `string` (literal match)
```haskell
string :: String -> Parser String
string []     = return []
string (c:cs) = do _  <- char c
                   _  <- string cs
                   return (c:cs)
```
What changes: matches a literal multi-char token; recursion on the expected chars.

### M8 — `parens p`
```haskell
parens :: Parser a -> Parser a
parens p = do _ <- char '('
              x <- p
              _ <- char ')'
              return x
```
What changes: bracket wrapper; reusable across grammars.

### M9 — Boolean expression parser
```haskell
data B = T | F | NotB B | AndB B B | OrB B B

bexpr :: Parser B
bexpr = bterm `chainl1` (string "or" *> pure OrB)

bterm :: Parser B
bterm = bfactor `chainl1` (string "and" *> pure AndB)

bfactor :: Parser B
bfactor = (string "not" *> (NotB <$> bfactor))
       `mplus` (string "true"  *> pure T)
       `mplus` (string "false" *> pure F)
       `mplus` parens bexpr
```
What changes: chained operator precedence with `chainl1`; longer alternatives.

### M10 — Brackets parser (A2 Ex 6)
```haskell
data Bracket = Round [Bracket] | Curly [Bracket]

parseBracket :: Parser Bracket
parseBracket = do c <- char '(' `mplus` char '{'
                  bs <- many' parseBracket
                  c2 <- if c == '(' then char ')' else char '}'
                  return (if c == '(' then Round bs else Curly bs)

tree :: String -> Maybe Bracket
tree s = case parse parseBracket s of
           [(b, "")] -> Just b
           _         -> Nothing
```
What changes: mutually recursive grammar; specific to brackets.

## Worked examples from this course
- Problem sheet Set 14 (#138-140): the whole parser-combinator chain.
- Assignment 2 Ex 6: well-bracketed strings — different shape, but parser-like.
- Week 10 lecture: parser combinators; optional Q1.
- Practice file `final10.hs` / `ai_mock.hs`: occasional small parsers.

## QuickCheck attack surface
> The canonical template uses the **list** parser (`<|>` = `p s ++ q s`), so `parse` returns the **full list of every parse**, fully-consumed result first. Do **not** assert a singleton — match the whole list, or pick out the fully-consumed answer with `[ v | (v, "") <- parse expr s ]` / take the first element. (A `Maybe`-based parser would instead give a singleton or `Nothing`.)
- **Empty input**: `parse expr "" == []` (failure) or `[(?, "")]` for `eps` — depends on definition.
- **Single number**: `parse expr "42" == [(42, ""), (4, "2")]` — full result first, then the partial parse of just `4`.
- **Operator precedence**: `parse expr "1+2*3" == [(7, ""), (3, "*3"), (1, "+2*3")]` (mul binds tighter; the `7` is first because it consumes all input).
- **Parenthesised**: `parse expr "(1+2)*3" == [(9, ""), (3, "*3")]`.
- **Failure**: `parse expr "1+" == []` or `[(1, "+")]` (partial consume).
- **Whitespace**: `parse expr "1 + 2" == [(3, "")]` only if `token` is used.
- **Left recursion absence**: `parse expr "1+2+3+4"` doesn't infinite-loop.
- **`many` returns empty list on no match**: `parse (many digitP) "abc" == [([], "abc")]`.

## Pitfalls (marks-killers)
- **Left recursion**: `expr = do {e <- expr; …}` — infinite loop. Refactor to `term '+' expr` form, or use `chainl1`.
- **Greedy `<|>` order**: alternatives MUST be most-specific first. `nat `mplus` longerLiteralStartingWithDigit` — longer alternative would never be tried.
- **Missing `token` wrapper**: `parse expr "1 + 2"` fails because the space isn't consumed.
- **`return x` outside `do`**: `(do … return x) mplus return y` — outer return creates a parser that always succeeds; that may not be intended.
- **`<*>` argument order**: `f <$> p1 <*> p2 <*> p3` applies `f` to results in order. Mixing this up gives weird types.
- **`Maybe (a, String)` vs `[(a, String)]`**: course uses LIST. Live-code examples sometimes use Maybe. Stick to list for compositionality.
- **Forgetting `import Control.Monad`** for `mzero`/`mplus`.

## Combines-with deep dive

### A16 × A06 — building the typeclass instances
Writing the parser IS writing Functor/Applicative/Monad/Alternative instances for `Parser`. A06 territory.

### A16 × A01 — parsing into an AST
Output of `expr` is usually a structured AST. Each grammar production builds a constructor.

### A16 × A19 — adding a new construct to the language
Adding `if-then-else` to a parser:
```haskell
ifExpr :: Parser Expr
ifExpr = do string "if";   c <- expr
            string "then"; t <- expr
            string "else"; e <- expr
            return (If c t e)
```

## See also

**Combines with:** [A24 applicative instance](./A24-applicative-instance.md) · [A08 env eval](./A08-env-eval.md)
**Question families:** [parser](../question-families/parser-family.md)
**Theory:** [parser overview](../interpreters/parser-overview.md) · [chainl1 + backtracking](../interpreters/parser-chainl1.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
