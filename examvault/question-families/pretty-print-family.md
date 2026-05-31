<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: pretty-print**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · **pretty-print** · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: pretty-print

**Archetype:** A16 (Show / display / paren-precedence pretty-printer)   |   **Stars:** ⭐⭐⭐   |   **Course week(s):** 7–8
**Search keywords:** Show, showsPrec, paren, precedence, display, pretty, render

## Generator template
```haskell
-- The seed: a paren-aware pretty-printer that respects operator precedence.
-- The `p` parameter is the precedence of the *parent* context.
-- If our own precedence is < p, we need to add parens.

class Pretty a where
  prettyPrec :: Int -> a -> String

pretty :: Pretty a => a -> String
pretty = prettyPrec 0

paren :: Bool -> String -> String
paren True  s = "(" ++ s ++ ")"
paren False s = s
```

## Mutations (the examiner picks one)

### Mutation 1 — show Color as hex (= problem 64)
**Spec:** `Red → "#FF0000"`, `Custom 12 34 56 → "#0C2238"`.
**Sig:** `instance Show Color where show = ...`
**Solution:**
```haskell
data Color = Red | Green | Blue | Custom Int Int Int

instance Show Color where
  show Red             = "#FF0000"
  show Green           = "#00FF00"
  show Blue            = "#0000FF"
  show (Custom r g b)  = '#' : concatMap hex [r, g, b]
    where
      hex n = pad2 (showHex' n)
      showHex' n = let (q, r') = n `divMod` 16
                   in  if q == 0 then [digit r']
                                 else showHex' q ++ [digit r']
      digit n | n < 10    = toEnum (n + fromEnum '0')
              | otherwise = toEnum (n - 10 + fromEnum 'A')
      pad2 s | length s == 1 = '0' : s
             | otherwise     = s
```
**QC trap:** Padding to two hex digits is the trickiest part. `Custom 0 0 0 → "#000000"`.

### Mutation 2 — pretty-print Expr (precedence-aware)
**Spec:** Render Expr with minimum parens given operator precedence.
**Sig:** `pretty :: Expr -> String`
**Solution:**
```haskell
data Expr = Val Int | Add Expr Expr | Mul Expr Expr | Sub Expr Expr | Neg Expr

pretty :: Expr -> String
pretty = go 0
  where
    -- prec: Add/Sub = 6 (left-assoc), Mul = 7, Neg = 8, Val/parens = 9
    go _ (Val n)
      | n < 0     = "(" ++ show n ++ ")"
      | otherwise = show n
    go p (Add a b) = paren (p > 6) (go 6 a ++ "+" ++ go 7 b)
    go p (Sub a b) = paren (p > 6) (go 6 a ++ "-" ++ go 7 b)
    go p (Mul a b) = paren (p > 7) (go 7 a ++ "*" ++ go 8 b)
    go p (Neg e)   = paren (p > 8) ("-" ++ go 8 e)
```
**QC trap:** Left vs right associativity — for left-assoc Add, the *right* child uses prec 7 (one higher), forcing parens around its `Add`/`Sub`.

### Mutation 3 — display BT (textual)
**Spec:** Print BT as nested S-expression.
**Sig:** `displayBT :: Show a => BT a -> String`
**Solution:**
```haskell
displayBT :: Show a => BT a -> String
displayBT Empty        = "_"
displayBT (Fork v l r) = "(" ++ show v ++ " " ++ displayBT l ++ " " ++ displayBT r ++ ")"
```
**QC trap:** `_` is a common convention for Empty. Reading the output back into a BT is the inverse parser — see `parser-family.md`.

### Mutation 4 — show Vec3 (= problem 65 style)
**Sig:** `instance Show Vec3`
**Solution:**
```haskell
data Vec3 = Vec3 Double Double Double

instance Show Vec3 where
  show (Vec3 x y z) = "<" ++ show x ++ "," ++ show y ++ "," ++ show z ++ ">"
```
**QC trap:** Trivial — just formatting. Watch for precision on Double.

### Mutation 5 — show Direction (custom textual)
**Sig:** `instance Show Direction`
**Solution:**
```haskell
data Direction = North | South | East | West

instance Show Direction where
  show North = "N"
  show South = "S"
  show East  = "E"
  show West  = "W"
```
**QC trap:** Same as deriving Show but shortened. Beware: this breaks `read . show == id` unless you also define Read.

### Mutation 6 — pretty-print Logic expression (Boolean)
**Spec:** Render Expr Logic with parens around lower-precedence subterms.
**Sig:** `prettyLogic :: Expr -> String`
**Solution:**
```haskell
data Expr = Var Char | Not Expr | And Expr Expr | Or Expr Expr | Implies Expr Expr

prettyLogic :: Expr -> String
prettyLogic = go 0
  where
    -- prec: Implies = 1, Or = 2, And = 3, Not = 4, Var = 5
    go _ (Var c)         = [c]
    go p (Not e)         = paren (p > 4) ("~" ++ go 4 e)
    go p (And a b)       = paren (p > 3) (go 3 a ++ "&" ++ go 4 b)
    go p (Or  a b)       = paren (p > 2) (go 2 a ++ "|" ++ go 3 b)
    go p (Implies a b)   = paren (p > 1) (go 2 a ++ "->" ++ go 1 b)
```
**QC trap:** Implies is *right*-associative. So `Implies a (Implies b c) ≡ a -> b -> c`. Watch the precedence direction.

### Mutation 7 — show Rose (indented)
**Spec:** Render rose tree with indentation per depth level.
**Sig:** `indented :: Show a => Rose a -> String`
**Solution:**
```haskell
data Rose a = Branch a [Rose a]

indented :: Show a => Rose a -> String
indented = go 0
  where
    go d (Branch v cs) = replicate (d*2) ' ' ++ show v ++ "\n"
                      ++ concatMap (go (d+1)) cs
```
**QC trap:** Trailing newlines / no trailing newlines — read the spec.

### Mutation 8 — showsPrec implementation (the Prelude pattern)
**Spec:** Define `showsPrec` directly using ShowS for efficiency.
**Sig:** `instance Show Expr where showsPrec = ...`
**Solution:**
```haskell
instance Show Expr where
  showsPrec p (Val n)   = showsPrec p n
  showsPrec p (Add a b) = showParen (p > 6) (showsPrec 6 a . showString "+" . showsPrec 7 b)
  showsPrec p (Mul a b) = showParen (p > 7) (showsPrec 7 a . showString "*" . showsPrec 8 b)
```
**QC trap:** ShowS = `String -> String` (difference list). Composes via `.`, avoiding the `(++)` blowup.

### Mutation 9 — pretty-print Bracket tree (= Assignment 2 Ex 6)
**Sig:** `brackets :: Bracket -> String`
**Solution:**
```haskell
data Bracket = Round [Bracket] | Curly [Bracket]

brackets :: Bracket -> String
brackets (Round ts) = "(" ++ concatMap brackets ts ++ ")"
brackets (Curly ts) = "{" ++ concatMap brackets ts ++ "}"
```
**QC trap:** Easy direction. The parser-direction `tree :: String -> Maybe Bracket` is hard — see `parser-family.md`.

### Mutation 10 — toJSON-like (recursive ADT to structured string)
**Spec:** Render a Value (Number / String / Array / Object) as JSON.
**Sig:** `toJSON :: Value -> String`
**Solution:**
```haskell
data Value = VNumber Int | VString String | VArray [Value] | VObject [(String, Value)]

toJSON :: Value -> String
toJSON (VNumber n)   = show n
toJSON (VString s)   = "\"" ++ s ++ "\""
toJSON (VArray vs)   = "[" ++ intercalate "," (map toJSON vs) ++ "]"
toJSON (VObject kvs) = "{" ++ intercalate "," (map kvJSON kvs) ++ "}"
  where
    kvJSON (k, v) = "\"" ++ k ++ "\":" ++ toJSON v

intercalate :: String -> [String] -> String
intercalate _ []     = ""
intercalate _ [s]    = s
intercalate sep (s:ss) = s ++ sep ++ intercalate sep ss
```
**QC trap:** String-escaping in real JSON is non-trivial — usually the exam skips escaping.

## Hidden-predicate mutations
- "Show only positive values, replace negatives with --" → conditional rendering.
- "Omit zero rows in a matrix display" → filter empties before render.

## Accumulator-style alternative
ShowS (`String -> String`) IS the accumulator alternative — see mutation 8. Linear-time concatenation.

## Fold-style alternative
For lists of items joined by separators:
```haskell
intercalate sep = foldr1 (\a b -> a ++ sep ++ b)   -- partial
intercalate sep = foldr (\a b -> if null b then a else a ++ sep ++ b) ""
```

## Cross-family combinations
- this family + `parser-family.md`: pretty ↔ parse round trip.
- this family + `adt-translation-family.md`: pretty-print after translate.
- this family + `env-eval-family.md`: pretty-print Expr to verify eval result.
- this family + `codec-family.md`: Morse `decodeText` ends with show.

## QuickCheck universal attacks
- **Round trip:** `read (pretty e) == e` when Read is defined.
- **Minimal parens:** `pretty e` should have exactly the parens needed.
- **Idempotence on simple cases:** `pretty (Val 5) == "5"`.
- **Show vs derived Show:** custom Show often replaces derived; check no surprises.
- **`unwords (lines (indented t)) == flatten t`** — for the indented mutation 7.

## Pitfalls (per mutation)
- M1: not padding hex to two digits.
- M2: left/right associativity wrong → too many parens.
- M3: forgetting Empty.
- M4: precision on doubles.
- M5: breaking read/show round trip.
- M6: Implies precedence (right vs left assoc).
- M7: depth-indentation off-by-one.
- M8: composition order of ShowS.
- M9: `concat` vs `concatMap`.
- M10: missing comma between elements.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — showsBT (showS-style accumulator for efficiency)

**Spec:** Implement `BT a -> ShowS` (i.e. `BT a -> String -> String`) to avoid O(n²) `++` for deeply nested trees.

**Type sig:** `showsBT :: Show a => BT a -> ShowS`

```haskell
showsBT :: Show a => BT a -> ShowS
showsBT Empty        = showString "Empty"
showsBT (Fork x l r) = showString "Fork "
                     . showsPrec 11 x . showString " ("
                     . showsBT l . showString ") ("
                     . showsBT r . showString ")"
```

**What changes vs seed:** Different evaluation strategy: `ShowS = String -> String` composes via `(.)`, avoiding the O(n²) string-concat blowup of naïve `show`. Same output shape, faster.

**QC trap:** `showsPrec 11 x` quotes negative numbers correctly — `show (-5)` is `"-5"` but inside `Fork` you need `(-5)` with parens. The `11` precedence forces parens.

## See also

**Primary archetype:** [A13 pretty printer](../archetypes/A13-pretty-printer.md)
**Theory:** [show](../typeclasses/show.md)
**QuickCheck:** [lists attacks](../quickcheck/lists-attacks.md)
**Pitfalls:** [P-012 custom Show non-string](../pitfalls/HIGH-severity.md#p-012)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
