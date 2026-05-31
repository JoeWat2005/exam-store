<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [typeclasses](./README.md) · **Show**

<!-- siblings:start -->
> **Peers:** [alternative](./alternative.md) · [applicative](./applicative.md) · [eq-ord](./eq-ord.md) · [foldable](./foldable.md) · [functor](./functor.md) · [monad](./monad.md) · [monoid](./monoid.md) · [num](./num.md) · **show** · [traversable](./traversable.md)
<!-- siblings:end -->






# Show

> **Mental model:** `Show` says "I know how to render this value as a `String` (specifically a Haskell-source-like representation)." The default `deriving Show` gives constructor-tagged output. Write a custom `instance Show` only when you want pretty-printed / domain-specific output (e.g. infix operators, parens-by-precedence, trees as diagrams).

**Methods (minimal):** `show :: a -> String` OR `showsPrec :: Int -> a -> ShowS`.

**Search keywords:** instance Show, show, showsPrec, ShowS, showString, precedence, deriving Show, pretty printer

## Recognition triggers

- "Pretty-print `T`"
- "Print expression with proper parentheses"
- "Render `T` to look like the source"
- The exam variant: a small DSL printed with operator precedence (cf. `interpreter/ConcreteSyntax.md`).

## Class

```haskell
type ShowS = String -> String      -- difference-list of chars

class Show a where
  show       :: a -> String
  showsPrec  :: Int -> a -> ShowS
  showList   :: [a] -> ShowS

  -- defaults:
  show x         = showsPrec 0 x ""
  showsPrec _ x  = showString (show x)
```

You generally define either `show` (simple) or `showsPrec` (precedence-aware).

## ShowS helpers

```haskell
showString    :: String -> ShowS
showString s  = (s ++)            -- prepend s

showChar      :: Char -> ShowS
showChar c    = (c :)             -- prepend c

showParen     :: Bool -> ShowS -> ShowS
showParen b s = if b then showChar '(' . s . showChar ')' else s

-- ShowS composition is just function composition:
showString "foo" . showString " " . showString "bar"
  -- builds "foo bar" lazily
```

The difference-list (`ShowS = String -> String`) lets you compose printers in O(1) by chaining functions, then materialise to a String at the end. Avoids O(n²) `++`.

## Canonical templates

### Simple — show as Haskell source

```haskell
data Color = Red | Green | Blue

instance Show Color where
  show Red   = "Red"
  show Green = "Green"
  show Blue  = "Blue"
```

### Tree (in-order text)

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

instance Show a => Show (BT a) where
  show Empty        = "_"
  show (Fork x l r) = "(" ++ show l ++ " " ++ show x ++ " " ++ show r ++ ")"
```

### Expression with operator precedence (the CRITICAL exam pattern)

```haskell
data Expr = Lit Int
          | Add Expr Expr        -- prec 6
          | Mul Expr Expr        -- prec 7
          | Neg Expr             -- prec 8

instance Show Expr where
  showsPrec _ (Lit n)     = shows n
  showsPrec p (Add e1 e2) = showParen (p > 6) $
    showsPrec 6 e1 . showString " + " . showsPrec 7 e2
  showsPrec p (Mul e1 e2) = showParen (p > 7) $
    showsPrec 7 e1 . showString " * " . showsPrec 8 e2
  showsPrec p (Neg e)     = showParen (p > 8) $
    showString "-" . showsPrec 9 e
```

Rules for precedence-aware printing:
- Each operator has a precedence number.
- `showsPrec p` means "I'm being printed in a context with surrounding precedence `p`".
- Wrap in parens iff `p > my-precedence`.
- For left-associative `op` at precedence `n`: left child gets `showsPrec n`, right child gets `showsPrec (n+1)`.
- For right-associative: swap.

### Pretty-printed tree (multi-line)

```haskell
showTree :: Show a => BT a -> String
showTree = go 0
  where
    go _ Empty         = ""
    go d (Fork x l r)  =
      replicate (d * 2) ' ' ++ show x ++ "\n" ++
      go (d+1) l ++
      go (d+1) r
```

### Custom infix list-like

```haskell
data MyList a = Nil | Cons a (MyList a)

instance Show a => Show (MyList a) where
  show Nil         = "[]"
  show (Cons x xs) = show x ++ " : " ++ show xs
```

## When to use `showsPrec` vs `show`

| Use case | Method |
|---|---|
| Simple data, no operators | `show` directly |
| Operator with precedence (Add/Mul) | `showsPrec` with `showParen` |
| Large nested structures (perf) | `showsPrec` (avoids O(n²) ++) |
| Reproducing Haskell source form | `showsPrec` (so it round-trips with `Read`) |

## `shows` shortcut

```haskell
shows :: Show a => a -> ShowS
shows = showsPrec 0
```

Used in chains like `shows x . showString ", " . shows y`.

## Pitfalls

- **`show` for negative literals.** `show (-3)` would give `"-3"`. If that appears inside a larger expression, surrounding code may need parens — `showsPrec` handles this.
- **Precedence levels.** The standard Haskell ops use the precedences from `Prelude`:
  - `(.)` 9, `(^)` 8, `(*)`/`(/)` 7, `(+)`/`(-)` 6, `(:)` 5, `(==)` 4, `(&&)` 3, `(||)` 2, `(>>=)` 1.
- **Default `showList` for `[a]` is "[x,y,z]"** — override only if you want different list syntax for your type as elements.
- **Don't reimplement `String` rendering with `++` everywhere.** Use `ShowS` for composability.
- **`shows` vs `show`.** `shows x` returns `ShowS` (composable); `show x` returns `String` (terminal).
- **`deriving Show` is usually fine** — only override when you have an actual reason (operators, layout).
- **Show must round-trip with Read** is *the convention* but not enforced. Custom Show often breaks readability.

## `show` law (informal)

There isn't a single algebraic law, but the convention is:

```haskell
read . show == id           -- where applicable (round-trip)
```

Custom `Show` instances often violate this — that's fine for pretty-printing, but be aware.

## QuickCheck attacks

- Round-trip: `read (show x) == x` (for derived instances).
- Length: `length (show x) > 0` for non-trivial values.
- Constructor coverage: `show` produces a non-empty string for every ctor.

## Pretty-printing recipe (the exam answer)

For an `Expr` data type with operators:

1. Assign each operator a precedence number from Haskell's table.
2. Define `instance Show Expr` using `showsPrec`.
3. For each constructor:
   - If it's an atom (literal, var): `shows v`.
   - If it's an operator at precedence `n`:
     - `showParen (p > n) $ showsPrec n e1 . showString " op " . showsPrec (n+1) e2` (left-assoc).
     - Swap for right-assoc.
4. Test round-trip with `read (show e) == e`.

## See also

**Archetypes:** [A13 pretty printer](../archetypes/A13-pretty-printer.md)
**Question families:** [pretty-print](../question-families/pretty-print-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
