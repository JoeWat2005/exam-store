<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A13 — Custom Show / Pretty-Printer**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · **A13** · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A13 — Custom Show / Pretty-Printer

**Tier:** 3   |   **Stars:** ⭐⭐
**Mock appearance:** none   |   **Assignment appearance:** A1 (GridWithAPointer with ANSI background)
**Combines with:** A17 · A22 · A01
**Search keywords:** show · Show instance · pretty print · ANSI · escape · `\ESC[` · format · padRight · hex

## What it tests
Whether you can write `instance Show T where show t = …` producing a clean, recursive textual rendering — with proper escapes, padding, or precedence-aware bracketing.

## Recognition triggers
- `instance Show T where` is the target
- "render", "display", "show", "format", "pretty-print"
- Expected output uses non-default characters: `#FF0000`, `\ESC[44m…`, `1 + (2 * 3)`
- The data type has multiple constructors, each needing distinct output
- `deriving Show` is conspicuously absent on the data type

## Canonical template
```haskell
data T = Lit Int | Comb T T | Wrap T

instance Show T where
  show (Lit n)      = show n
  show (Comb a b)   = "(" ++ show a ++ " + " ++ show b ++ ")"
  show (Wrap t)     = "<" ++ show t ++ ">"
```

## Mutations (the examiner picks one)

### M1 — Color → hex (problem 64)
```haskell
data Color = Red | Green | Blue | Custom Int Int Int

instance Show Color where
  show Red             = "#FF0000"
  show Green           = "#00FF00"
  show Blue            = "#0000FF"
  show (Custom r g b)  = "#" ++ toHex r ++ toHex g ++ toHex b

toHex :: Int -> String
toHex n = [hex (n `div` 16), hex (n `mod` 16)]
  where hex i = "0123456789ABCDEF" !! i
```
What changes: closed enum (Red/Green/Blue) → literal strings; open constructor (Custom) → computed string. **`replicate '0'`-pad** if you want 2-char hex.

### M2 — Expr with precedence (Data2)
```haskell
data Expr = Val Int | Add Expr Expr | Mul Expr Expr | Negate Expr

instance Show Expr where
  show = showP 0
    where
      showP _ (Val n)       = show n
      showP p (Negate e)    = paren (p > 2) ("-" ++ showP 2 e)
      showP p (Mul a b)     = paren (p > 1) (showP 1 a ++ " * " ++ showP 1 b)
      showP p (Add a b)     = paren (p > 0) (showP 0 a ++ " + " ++ showP 0 b)
      paren True s  = "(" ++ s ++ ")"
      paren False s = s
```
What changes: extra precedence parameter; uses it to decide bracketing.

### M3 — ANSI-highlighted (A1)
```haskell
hilight :: Show a => a -> String
hilight x = "\ESC[44m" ++ show x ++ "\ESC[0m"

newtype ShowHelper a = ShowHelper (a, Bool)

instance Show a => Show (ShowHelper a) where
  show (ShowHelper (x, False)) = show x
  show (ShowHelper (x, True))  = "\ESC[44m" ++ show x ++ "\ESC[0m"
```
What changes: wraps display in escape sequences; needs careful column-width counting later (`stripANSI`).

### M4 — Grid pretty-print (A1)
```haskell
newtype Grid a = Grid [[a]]

instance Show a => Show (Grid a) where
  show (Grid g) = unlines (map showRow g)
    where
      showRow row = unwords (map (\x -> padRight maxW (show x)) row)
      maxW = maximum (concat [[length (show x) | x <- row] | row <- g])
      padRight n s = s ++ replicate (n - length s) ' '
```
What changes: column-aligned; uses `unlines`/`unwords`/`replicate`/`padRight`.

### M5 — BT tree as indented text
```haskell
showTree :: Show a => BT a -> String
showTree = go 0
  where go _   Empty        = ""
        go ind (Fork x l r) = replicate ind ' ' ++ show x ++ "\n"
                              ++ go (ind + 2) l
                              ++ go (ind + 2) r
```
What changes: depth-indented recursion; one line per node.

### M6 — JSON-style render
```haskell
data J = JNull | JBool Bool | JNum Int | JStr String | JArr [J] | JObj [(String, J)]

instance Show J where
  show JNull       = "null"
  show (JBool b)   = if b then "true" else "false"
  show (JNum n)    = show n
  show (JStr s)    = "\"" ++ escape s ++ "\""
  show (JArr xs)   = "[" ++ intercalate "," (map show xs) ++ "]"
  show (JObj kvs)  = "{" ++ intercalate "," [show k ++ ":" ++ show v | (k,v) <- kvs] ++ "}"

escape :: String -> String
escape = concatMap (\c -> if c == '"' then "\\\"" else [c])
```
What changes: recursive containers (`JArr`, `JObj`) with explicit recursion via `intercalate`.

### M7 — `Circuit` as boolean formula
```haskell
showCircuit :: Circuit -> String
showCircuit (Input c)  = [c]
showCircuit (Nand a b) = "(" ++ showCircuit a ++ " NAND " ++ showCircuit b ++ ")"
```
What changes: simple infix; parens always (no precedence).

### M8 — `Show Rose a` with vertical bars
```haskell
showRose :: Show a => Rose a -> String
showRose = go ""
  where
    go pre (Leaf x)     = pre ++ "└─ " ++ show x ++ "\n"
    go pre (Branch xs)  = pre ++ "├─ Branch\n"
                          ++ concatMap (go (pre ++ "│  ")) xs
```
What changes: builds a directory-like tree display via prefix string.

### M9 — `Vec3` with parens
```haskell
data Vec3 = Vec3 Double Double Double

instance Show Vec3 where
  show (Vec3 x y z) = "(" ++ show x ++ ", " ++ show y ++ ", " ++ show z ++ ")"
```
What changes: tuple-like display for a custom type.

### M10 — Override of derived Show for special cases
```haskell
data Day = Day { dayName :: String, dayNumber :: Int }

instance Show Day where
  show (Day n k) = show k ++ " (" ++ n ++ ")"
```
What changes: combine fields into a domain-specific format.

## Worked examples from this course
- Problem sheet Set 7 (#64): `Color` → hex — M1.
- Assignment 1: `Show (GridWithAPointer a)` with ANSI highlighting of the focus — M3/M4.
- Data2 lecture: precedence-aware Show for `Expr` — M2.
- Practice files: occasional custom Show for debug.

## QuickCheck attack surface
- **Exact string match**: marker compares `show t == expected`. One character off (extra space, wrong escape) → 0 marks.
- **Round-trip with Read**: usually NOT required, but some specs say `read (show x) == x`. Test on basic Int values.
- **Empty/leaf case**: `show Empty == ""` vs `"Empty"` vs `"-"` — read the spec exactly.
- **Precedence**: `show (Mul (Add 1 2) 3) == "(1 + 2) * 3"` — parens around `+` because lower precedence than `*`. Bug: drops parens → `1 + 2 * 3` evaluates differently.
- **Negative numbers**: `show (Val (-5))` — does it show `-5` or `(-5)`? `showsPrec` style usually wraps in parens at prec > 6.
- **Special chars**: `show '\\'` is `"\\\\"` (because the Haskell-string literal `"\\"` is one backslash).

## Pitfalls (marks-killers)
- **Mixing `Show a` (the typeclass) with `show :: T -> String`**: `instance Show Color where show = ...` — fine. `show x = ...` (free `x`) — type-binding error.
- **Calling `show` recursively without instance**: if the inner field isn't `Show`, won't compile. Add the `Show a =>` constraint.
- **Forgetting precedence parens**: `Negate (Add 1 2)` should print as `-(1 + 2)`, not `-1 + 2`.
- **Newlines in expected output**: `unlines` adds a trailing `\n`. If the spec doesn't want it, use `intercalate "\n"`.
- **ANSI escape syntax**: Haskell `"\ESC[44m"` is one character (`\ESC`) + 4 literal chars. Don't write `"^[" ++ ...`.
- **`show x` vs `showsPrec p x`**: the latter takes precedence. If you override `show` but the marker calls `showsPrec`, you get the default behaviour.

## Combines-with deep dive

### A13 × A17 — Show for a zipper
The zipper's display puts a highlight on the focus position. See A1 (`GridWithAPointer`'s Show).

### A13 × A22 — full typeclass package
A custom type often needs `Eq`, `Ord`, `Show` all hand-written. A13 = `Show`; A22 covers the rest.

### A13 × A01 — Show for a recursive ADT
Per-constructor `show` IS structural recursion. Same skeleton as `eval`/`size`.

## See also

**Combines with:** [A05 ADT translation](./A05-adt-translation.md) · [A09 prelude reimpl](./A09-prelude-reimpl.md)
**Question families:** [pretty-print](../question-families/pretty-print-family.md)
**Theory:** [Show typeclass](../typeclasses/show.md)
**Pitfalls:** [P-012 custom Show returns non-string](../pitfalls/HIGH-severity.md#p-012)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
