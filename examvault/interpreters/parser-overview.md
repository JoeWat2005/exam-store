<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [interpreters](./README.md) · **Interpreter 15 — Parser combinators (minimal reference)**

<!-- siblings:start -->
> **Peers:** [desugar-pipeline](./desugar-pipeline.md) · [expr-either](./expr-either.md) · [expr-maybe](./expr-maybe.md) · [expr-multi-effect](./expr-multi-effect.md) · [expr-reader-either](./expr-reader-either.md) · [expr-reader](./expr-reader.md) · [expr-state-either](./expr-state-either.md) · [expr-state](./expr-state.md) · [expr-writer-state](./expr-writer-state.md) · [expr-writer](./expr-writer.md) · [extend-interpreter](./extend-interpreter.md) · [imperative-eval](./imperative-eval.md) · [imperative-storage](./imperative-storage.md) · [parser-chainl1](./parser-chainl1.md) · **parser-overview** · [simple-arith](./simple-arith.md)
<!-- siblings:end -->






# Interpreter 15 — Parser combinators (minimal reference)

**Effect:** `Parser a = String -> [(a, String)]` (built-in `>>=` short-circuits, `<|>` provides alternatives)
**Effect rationale:** parsing is *non-deterministic consumption*. The `Parser` type can be modelled as `String -> [(a, String)]` — a function from remaining input to list of (value, remaining-input) results. Backtracking is automatic.
**Type signature:** `newtype Parser a = P (String -> [(a, String)])`
**Search keywords:** parser-combinator · parsing · monadic-parser · A16 · alt · do-notation · symbol · token · many · some · grammar · BNF · expr-parser

> The lecture provides `Parsing.hs` from Hutton's textbook. Practice problems 138-140 reimplement it. **You probably do not need to write this from scratch in the exam** — but you should be fluent reading the existing combinators and using them.

---

## The Parser type and basic instances

```haskell
newtype Parser a = P (String -> [(a, String)])

parse :: Parser a -> String -> [(a, String)]
parse (P p) inp = p inp

item :: Parser Char
item = P (\inp -> case inp of
                    []     -> []
                    (x:xs) -> [(x, xs)])

instance Functor Parser where
  fmap f p = P (\inp -> case parse p inp of
                          []        -> []
                          [(v,out)] -> [(f v, out)])

instance Applicative Parser where
  pure v = P (\inp -> [(v, inp)])
  pg <*> px = P (\inp -> case parse pg inp of
                           []        -> []
                           [(g,out)] -> parse (fmap g px) out)

instance Monad Parser where
  p >>= f = P (\inp -> case parse p inp of
                         []        -> []
                         [(v,out)] -> parse (f v) out)

instance Alternative Parser where
  empty = P (\_ -> [])
  p <|> q = P (\inp -> case parse p inp of
                         []        -> parse q inp
                         [(v,out)] -> [(v,out)])
```

Source: `fp-learning-2025/files/LectureNotes/Sections/interpreter/Parsing.hs`.

The `[(a, String)]` list is **always singleton or empty** in practice — Hutton's combinators pick the first result.

## Derived combinators

```haskell
sat       :: (Char -> Bool) -> Parser Char
digit     :: Parser Char
letter    :: Parser Char
alphanum  :: Parser Char
char      :: Char -> Parser Char
string    :: String -> Parser String
ident     :: Parser String       -- lowercase-start identifier
nat       :: Parser Int
int       :: Parser Int

space     :: Parser ()
token     :: Parser a -> Parser a       -- strips surrounding whitespace
identifier:: Parser String       -- token ident
natural   :: Parser Int          -- token nat
integer   :: Parser Int          -- token int
symbol    :: String -> Parser String    -- token (string s)

many      :: Parser a -> Parser [a]     -- zero or more
some      :: Parser a -> Parser [a]     -- one or more
```

The `token` combinator wraps any parser to ignore surrounding whitespace. `symbol "if"` parses the literal `"if"` allowing spaces around it.

## Grammar → parser mapping

For each BNF rule, write a `do`-block that mirrors the rule.

### Atom: `digit`
```
digitP ::= '0' | '1' | ... | '9'
```
```haskell
digitP :: Parser Char
digitP = sat isDigit
```

### Sequence: `parseNat`
```
nat ::= digit+
```
```haskell
parseNat :: Parser Int
parseNat = do
  ds <- some digit
  return (read ds)
```

### Alternative: comparison operators
```
cmp ::= "<=" | "<" | ">=" | ">"
```
```haskell
compOp :: Parser ([Expr] -> Expr)
compOp = parseOp "<=" Leq
     <|> parseOp "<"  Less
     <|> parseOp ">=" Geq
     <|> parseOp ">"  Greater
```
Order matters: try the **longer** match first (`"<="` before `"<"`).

### Recursion: `expr` chains
```
expr  ::= expr1 OrOp  expr  |  expr1
```
Factor into:
```haskell
expr :: Parser Expr
expr = do
  e1 <- expr1
  (do op <- orOp
      e  <- expr
      return (op [e1, e]))
    <|> return e1
```
or use the lecture's `binExpr` helper:
```haskell
binExpr :: Parser e -> Parser ([e] -> e) -> Parser e -> Parser e
binExpr expr' op expr =
  do e' <- expr'
     (do o <- op
         e <- expr
         return (o [e', e]))
       <|> return e'

expr  = binExpr expr1 orOp  expr
expr1 = binExpr expr2 andOp expr1
-- etc.
```

## Lecture's full parser (mini-recap)

From `fp-learning-2025/files/LectureNotes/Sections/interpreter/Parser.hs`:

```haskell
program =
      assignment
  <|> block
  <|> whileStatement
  <|> ifStatement

assignment = do
  i <- identif
  symbol ":="
  e <- expr
  symbol ";"
  return (i := e)

block = do
  symbol "{"
  ps <- many program
  symbol "}"
  return (Block ps)

whileStatement = do
  symbol "while"
  symbol "("
  e <- expr
  symbol ")"
  p <- program
  return (While e p)

ifStatement = do
  symbol "if"
  symbol "("
  e <- expr
  symbol ")"
  p1 <- program
  ((do symbol "else"
       p2 <- program
       return (IfElse e p1 p2))
   <|> return (If e p1))
```

`many program` parses zero-or-more programs. `<|>` lets us try `else` and fall back to no-else.

## Practice problem 140 — `parseAdd` style

```
expr   ::= term '+' expr | term
term   ::= factor '*' term | factor
factor ::= nat | '(' expr ')'
```
```haskell
parseExpr :: Parser Int
parseExpr = do
  t <- parseTerm
  (do _ <- char '+'
      e <- parseExpr
      return (t + e))
    <|> return t

parseTerm :: Parser Int
parseTerm = do
  f <- parseFactor
  (do _ <- char '*'
      t <- parseTerm
      return (f * t))
    <|> return f

parseFactor :: Parser Int
parseFactor = parseNat
          <|> do _ <- char '('
                 e <- parseExpr
                 _ <- char ')'
                 return e
```

Note: this parser **evaluates as it parses** (returns `Int` directly). For an AST, return `Expr` instead.

## Running a parser

```haskell
parseProgram :: String -> Program
parseProgram xs = case parse program xs of
  [(p, [])] -> p
  [(_, s)]  -> error ("syntax: unparsed string " ++ s)
  _         -> error "syntax: failed to parse program"
```

The two error cases:
- `[(p, leftover)]` — parsed something but didn't consume all input.
- `[]` — parser failed before consuming anything (or got stuck).

## Pitfalls
- **Order of alternatives matters.** `parseOp "<" Less <|> parseOp "<=" Leq` would never match `"<="` (the `<` would succeed first, consuming the `<`, leaving `=`). Always try **longer** matches first.
- **Left recursion.** `expr ::= expr op term | term` written directly would loop. Use the factored form `expr ::= term op expr | term` (right-recursion, parses right-associatively) or `binExpr` helper.
- **Precedence.** Lower precedence at the *outer* layer. The lecture's `expr` has Or at the lowest precedence (outermost) and `expr7` is atoms (highest).
- **Forgetting `token` / whitespace.** Bare `string "if"` requires no leading space. Use `symbol "if"` to allow flexible spacing.
- **`many` vs `some`.** `many` includes zero matches; `some` requires at least one.
- **Identifier keywords.** If an identifier could match a keyword (e.g. `if`), guard against it: `guard (not (elem cs keywords))`.
- **`do`-block parser fails silently.** If any step returns `[]`, the whole block returns `[]`. Backtrack via `<|>`.
- **Result type vs effect.** `Parser a` is a monad; `do x <- p; return (f x)` is `fmap f p`. Both fine; the `do` style is more common in the lecture.
- **`parse` vs `runParser`.** Hutton's library uses `parse`. Other libraries use `runParser`. Check the exact spelling.

## QuickCheck attacks
- For `parseProgram (show ast)` — if you have a `Show` that produces the concrete syntax, parse should give back the AST (round-trip).
- `parse parseNat "0" == [(0, "")]`, `parse parseNat "" == []`.
- `parse parseExpr "(1+2)*3" == [(9, "")]` if it evaluates, or `[(Mul (Add (Lit 1) (Lit 2)) (Lit 3), "")]` if it builds AST.
- Precedence: `parse expr "1+2*3"` should parse as `1 + (2 * 3)`, not `(1+2) * 3`.
- Whitespace: `parse program "  x := 5;  "` should succeed if `token` is used.
- Keyword guard: `parse identif "if"` should fail because `"if"` is a keyword.

## When NOT to write a parser

If the exam gives you an AST and asks you to evaluate it, **do not write a parser**. The question always says either "given the following AST" (no parser needed) or "parse the following concrete syntax" (parser required).

For exam-style "tweak the parser" questions:
- Add a new keyword: add to `keywords` list and a new statement parser.
- Add a new operator: add to the right precedence layer.
- Add a new literal: add to `expr7` (atomic level).

## See also

**Archetypes:** [A16 parser combinators](../archetypes/A16-parser-combinators.md)
**Question families:** [parser](../question-families/parser-family.md)
**QuickCheck:** [interp attacks](../quickcheck/interp-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
