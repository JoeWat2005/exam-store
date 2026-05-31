<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A07 — Codec Pair (encode / decode round-trip)**

<!-- siblings:start -->
> **Peers:** [A01](./A01-tree-recursion.md) · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · **A07** · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A07 — Codec Pair (encode / decode round-trip)

**Tier:** 2   |   **Stars:** ⭐⭐⭐⭐
**Mock appearance:** none direct   |   **Assignment appearance:** A2 (whole — Morse encode/decode, ramify/tabulate)
**Combines with:** A01 · A12 · A20 · A05
**Search keywords:** encode · decode · round-trip · inverse · RLE · Morse · lookup · split · table · tree

## What it tests
Whether you can write two mutually-inverse functions (or one direction satisfying a retract property), correctly using a lookup table, intercalating separators, and splitting on those same separators.

## Recognition triggers
- "such that `decode (encode x) == x`" appears in the spec
- Two function signatures whose types are mirror images: `A -> B` and `B -> A`
- "intercalate", "concat", "split", "separator", "delimiter" appear
- A `lookup`-style table is provided: `[(Key, Value)]`
- Test examples specifically check encoded-then-decoded equals original
- The same `Table` (or `Tree`) parameter appears in both functions

## Canonical template
```haskell
type Table k v = [(k, v)]

encode :: Table k [u] -> [k] -> [u]
encode tab = concat . map (\k -> case lookup k tab of
                                   Just us -> us
                                   Nothing -> [])

decode :: Eq u => Table k [u] -> [u] -> [k]
decode tab us = go us
  where invert = [(v, k) | (k, v) <- tab]
        go []  = []
        go xs  = case findPrefix invert xs of
                   Just (k, rest) -> k : go rest
                   Nothing        -> []
```

## Mutations (the examiner picks one)

### M1 — Caesar `encode` / `decode` (Set 6 #57-59)
```haskell
import Data.Char (ord, chr, isUpper, isLower)

shift :: Int -> Char -> Char
shift n c
  | isUpper c = chr ((ord c - ord 'A' + n) `mod` 26 + ord 'A')
  | isLower c = chr ((ord c - ord 'a' + n) `mod` 26 + ord 'a')
  | otherwise = c

encode :: Int -> String -> String
encode n = map (shift n)

decode :: Int -> String -> String
decode n = map (shift (-n))
```
What changes: char-wise codec; no separators. Round-trip is `decode n . encode n == id`.

### M2 — RLE / RLD (problem 147)
```haskell
rle :: Eq a => [a] -> [(a, Int)]
rle []     = []
rle (x:xs) = let (same, rest) = span (== x) (x:xs)
             in (x, length same) : rle rest

rld :: [(a, Int)] -> [a]
rld = concatMap (\(x, n) -> replicate n x)
```
What changes: encode is a `span`/grouping; decode is `concatMap replicate`. Round-trip from `rle` only — `rld (rle "aaab") = "aaab"` but `rle (rld [('a',0)]) = []`.

### M3 — Morse `encodeWord` (Assignment 2)
```haskell
import Data.List (intercalate)

type Table = [(Char, Code)]
type Code  = [Atom]
shortGap :: Code
shortGap = replicate 2 Silence

encodeWord :: Table -> String -> Code
encodeWord _   []     = []
encodeWord tab [c]    = lookupOr [] c tab
encodeWord tab (c:cs) = lookupOr [] c tab ++ shortGap ++ encodeWord tab cs

lookupOr :: Eq k => v -> k -> [(k, v)] -> v
lookupOr d k = maybe d id . lookup k
```
What changes: separator (`shortGap`) interspersed between letters but NOT trailing.

### M4 — Morse `decodeText` (Assignment 2)
```haskell
decodeText :: Table -> Code -> String
decodeText tab cd =
  let words' = split mediumGap cd
  in intercalate " " (map (decodeWord tab) words')

decodeWord :: Table -> Code -> String
decodeWord tab cd =
  let letters = split shortGap cd
  in mapMaybe (`lookup` invTab) letters
  where invTab = [(v, k) | (k, v) <- tab]

split :: Eq a => [a] -> [a] -> [[a]]
split _   []     = [[]]
split sep xs
  | sep `isPrefixOf` xs = [] : split sep (drop (length sep) xs)
  | otherwise           = case split sep (tail xs) of
                            (w:ws) -> (head xs : w) : ws
                            []     -> [[head xs]]
```
What changes: nested codec (words inside lines), TWO separators (medium gap between words, short gap between letters).

### M5 — `ramify` / `tabulate` (A2 Ex 4-5)
```haskell
data Tree = Empty | Branch (Maybe Char) Tree Tree

ramify :: Table -> Tree
ramify = foldr insertCode Empty
  where
    insertCode (ch, code) = go code
    go []           t                       = case t of
      Empty                    -> Branch (Just '?') Empty Empty   -- placeholder
      Branch _ l r             -> Branch (Just '?') l r
    go (Beep:cs)    Empty              = Branch Nothing (go cs Empty) Empty
    go (Beep:cs)    (Branch m l r)     = Branch m (go cs l) r
    go (Silence:cs) Empty              = Branch Nothing Empty (go cs Empty)
    go (Silence:cs) (Branch m l r)     = Branch m l (go cs r)

tabulate :: Tree -> Table
tabulate t = go [] t
  where go _    Empty                  = []
        go pth (Branch Nothing  l r)   = go (pth ++ [Beep]) l ++ go (pth ++ [Silence]) r
        go pth (Branch (Just c) l r)   = (c, pth) : go (pth ++ [Beep]) l ++ go (pth ++ [Silence]) r
```
What changes: bidirectional but only `ramify ∘ tabulate = id` (retract, not iso). Path is built top-down.

### M6 — Base-2 encode / decode
```haskell
toBits :: Int -> [Int]
toBits 0 = [0]
toBits n = reverse (go n)
  where go 0 = []
        go k = (k `mod` 2) : go (k `div` 2)

fromBits :: [Int] -> Int
fromBits = foldl (\acc b -> acc * 2 + b) 0
```
What changes: numeric; both endpoints inverse on positive ints.

### M7 — JSON-style escape / unescape
```haskell
escape :: String -> String
escape []         = []
escape ('"':cs)   = '\\' : '"' : escape cs
escape ('\\':cs)  = '\\' : '\\' : escape cs
escape (c:cs)     = c : escape cs

unescape :: String -> String
unescape []                = []
unescape ('\\':'"':cs)     = '"'  : unescape cs
unescape ('\\':'\\':cs)    = '\\' : unescape cs
unescape (c:cs)            = c : unescape cs
```
What changes: special-character substitution; escape adds bytes, unescape removes them.

### M8 — `toRose` / `fromRose` (A3 Q1)
```haskell
data Rose a = Lf a | Br [Rose a]
data Free f a = Pure a | Free (f (Free f a))

toRose   :: Free [] a -> Rose a
toRose   (Pure x)  = Lf x
toRose   (Free xs) = Br (map toRose xs)

fromRose :: Rose a -> Free [] a
fromRose (Lf x)  = Pure x
fromRose (Br xs) = Free (map fromRose xs)
```
What changes: structural, no separator; parallel constructors `Lf↔Pure`, `Br↔Free`.

### M9 — Path-string ↔ list of `Direction`s
```haskell
data Dir = L | R | U | D
encodePath :: [Dir] -> String
encodePath = map (\d -> case d of L -> 'L'; R -> 'R'; U -> 'U'; D -> 'D')

decodePath :: String -> Maybe [Dir]
decodePath = mapM (\c -> lookup c [('L',L),('R',R),('U',U),('D',D)])
```
What changes: decoder uses `Maybe` (`mapM` on Maybe) to fail on bad char.

### M10 — Vector compression `(value, run)` for a constant predicate
```haskell
encodeRuns :: Eq a => [a] -> [(a, Int)]
encodeRuns = map (\g -> (head g, length g)) . groupBy (==)
  where groupBy eq []     = []
        groupBy eq (x:xs) = let (s, r) = span (eq x) xs in (x:s) : groupBy eq r
```
What changes: same as M2 but using a group-by; decoder is identical to `rld`.

## Worked examples from this course
- Assignment 2: all six tasks (`encodeWord`, `encodeWords`, `encodeText`, `decodeText`, `decodeTextWithTree`, `ramify`, `tabulate`) — multi-mutation deluxe.
- Problem sheet Set 6 (#57-60): Caesar shift / encode / decode / crack.
- Problem sheet Set 15 (#146): `ramify` / `tabulate` repeated.
- Problem sheet Set 15 (#147): RLE / RLD.
- Assignment 3 Q1: `toRose` / `fromRose` — M8.

## QuickCheck attack surface
- **Round-trip**: `decode (encode x) == x` for arbitrary `x` — the headline property.
- **Empty input**: `encode []` should return `[]`; `decode []` should return `[]`.
- **Single element / single character**: edge case for `intercalate` (no separator).
- **Trailing separator bug**: `encodeWord tab "AB" = enc 'A' ++ shortGap ++ enc 'B'` — no trailing `shortGap`. If you add one, `decode` sees an extra empty word.
- **Lookup miss**: `lookup` returns `Nothing` for unknown chars. Are you using `maybe [] id` or `fromMaybe []`? If you use `fromJust`, marker crashes on unknown input.
- **Ambiguous prefix**: in `decode`, if two codes share a prefix, your greedy match must pick the LONGEST. (For Morse this isn't an issue if the table is prefix-free; for arbitrary tables it can be.)
- **Retract vs iso**: `ramify (tabulate t) == t` is the retract direction. `tabulate (ramify table)` is only a PERMUTATION of `table` (not equal). Marker checks both.

## Pitfalls (marks-killers)
- **`fromJust` on a Maybe**: if `lookup` returns `Nothing`, crashes. Use `case lookup k tab of …` or `maybe default id`.
- **Trailing separator**: appending `shortGap` after every letter (including the last) doubles up the next gap. Use the "between, not after" idiom: `intercalate shortGap (map encOne xs)`.
- **Swapped table**: when building inverse, `[(v, k) | (k, v) <- tab]` — not `[(k, v) | (v, k) <- tab]`.
- **Greedy vs minimal split**: `split sep` must match `sep` as a literal SUBSTRING, not just `==`. Use `isPrefixOf sep`.
- **`intercalate` on empty list**: `intercalate sep [] = []` — fine. But `intercalate sep [""]` is `""`, not `sep` — careful.
- **Encoding char-by-char and forgetting sep**: `encodeText tab = concat . map (lookup …)` — missing intercalation. Then `decodeText` can't split.

## Combines-with deep dive

### A07 × A01 — codec where one side is a tree
See M5. `decodeTextWithTree` walks the tree following the code:
```haskell
decodeTextWithTree :: Tree -> Code -> String
decodeTextWithTree root = go root
  where
    go (Branch (Just c) _ _) []  = [c]
    go _ []                      = []
    go (Branch mc _ _) (Silence:Silence:Silence:cs) = maybe "" pure mc ++ " " ++ go root cs
    go t (Silence:cs)            = decodeTextWithTree root cs  -- end of letter
    go (Branch _ l _) (Beep:cs)  = go l cs
    -- (sketch — production needs careful gap handling)
```

### A07 × A12 — same data, two representations
`Table ↔ Tree` IS A12 in addition to A07. The round-trip law makes it a codec.

### A07 × A20 — proving the round-trip
`decodeText t (encodeText t s) = s` is a candidate equational-reasoning exam question.

## See also

**Combines with:** [A05 ADT translation](./A05-adt-translation.md) · [A12 rep conversion](./A12-rep-conversion.md) · [A20 laws / iso](./A20-laws-iso.md)
**Question families:** [codec](../question-families/codec-family.md)
**QuickCheck:** [codec attacks](../quickcheck/codec-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
