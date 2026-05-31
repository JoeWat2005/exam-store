<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: codec**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · **codec** · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: codec

**Archetype:** A14 (encode/decode with a lookup table or tree)   |   **Stars:** ⭐⭐⭐   |   **Course week(s):** 6, 9
**Search keywords:** Caesar, Morse, RLE, run-length, base-N, encode, decode, encodeText, decodeTextWithTree, ramify, tabulate

## Generator template
```haskell
-- The seed: encode = mapping each input chunk to its output code, concatenating;
-- decode = scanning the input stream and translating back via a reverse map.
type Code = [Atom]
type Table = [(Char, Code)]

encode :: Table -> String -> Code
encode _ ""     = []
encode t (c:cs) = lookupCode t c ++ encode t cs

decode :: Table -> Code -> String
-- requires a more complex scan because codes vary in length
```

Three sub-shapes:
- **Per-char substitution** (Caesar, ROT13): O(1) lookup per char, output is same length.
- **Variable-length code table** (Morse, Huffman, base-N): decode scans for longest match.
- **Run-length** (RLE): encode/decode use group-and-pair.

## Mutations (the examiner picks one)

### Mutation 1 — shift (Caesar single char) (= problem 57)
**Spec:** Shift a letter by `n`, wrap around; non-letters unchanged.
**Sig:** `shift :: Int -> Char -> Char`
**Solution:**
```haskell
import Data.Char (ord, chr, isUpper, isLower)

shift :: Int -> Char -> Char
shift n c
  | isUpper c = rotate 'A' c
  | isLower c = rotate 'a' c
  | otherwise = c
  where
    rotate base ch = chr ((ord ch - ord base + n) `mod` 26 + ord base)
```
**QC trap:** `mod 26` works for negative `n` in Haskell (always non-negative). `shift n . shift (-n) == id` is the QC property.

### Mutation 2 — encode (Caesar whole string) (= problem 58)
**Sig:** `encode :: Int -> String -> String`
**Solution:**
```haskell
encode :: Int -> String -> String
encode n = map (shift n)
```
**QC trap:** `encode n . encode (-n) == id`. `encode 26 == id`. `encode 13 . encode 13 == id` (ROT13).

### Mutation 3 — caesarDecode (= problem 59)
**Sig:** `caesarDecode :: Int -> String -> String`
**Solution:**
```haskell
caesarDecode :: Int -> String -> String
caesarDecode n = encode (-n)
```
**QC trap:** Trivially `encode (-n)`. Some exam variants demand a *separate* implementation.

### Mutation 4 — encodeWord (Morse) (= Assignment 2 Ex 1.1)
**Spec:** Encode a single word; insert a shortGap after every char that isn't last.
**Sig:** `encodeWord :: Table -> String -> Code`
**Solution:**
```haskell
encodeWord :: Table -> String -> Code
encodeWord _ []     = []
encodeWord t [c]    = maybe [] id (lookup c t)
encodeWord t (c:cs) = maybe [] id (lookup c t) ++ shortGap ++ encodeWord t cs
```
**QC trap:** No trailing shortGap. Use `[c]` pattern to detect the last char.

### Mutation 5 — encodeText (Morse, multi-word) (= Assignment 2 Ex 1.3)
**Spec:** Encode space-separated words; space → mediumGap.
**Sig:** `encodeText :: Table -> String -> Code`
**Solution:**
```haskell
encodeText :: Table -> String -> Code
encodeText t s = intercalateCode mediumGap (map (encodeWord t) (words s))
  where
    intercalateCode _ []     = []
    intercalateCode _ [c]    = c
    intercalateCode sep (c:cs) = c ++ sep ++ intercalateCode sep cs
```
**QC trap:** Spec says no trailing space — handle empty input.

### Mutation 6 — decodeText (Morse via table) (= Assignment 2 Ex 2)
**Spec:** Inverse of encodeText.
**Sig:** `decodeText :: Table -> Code -> String`
**Solution:**
```haskell
decodeText :: Table -> Code -> String
decodeText t code = unwords (map (decodeWord t) (split mediumGap code))
  where
    decodeWord t' c = map (decodeChar t') (split shortGap c)
    decodeChar t' c = maybe '?' id (lookup c (map (\(a,b)->(b,a)) t'))

split :: Eq a => [a] -> [a] -> [[a]]
split sep xs = case breakOn sep xs of
                 (chunk, [])   -> [chunk]
                 (chunk, rest) -> chunk : split sep (drop (length sep) rest)

breakOn :: Eq a => [a] -> [a] -> ([a], [a])
breakOn _ []     = ([], [])
breakOn sep xs
  | sep `isPrefixOf` xs = ([], xs)
  | otherwise           = let (l, r) = breakOn sep (tail xs)
                          in  (head xs : l, r)
  where isPrefixOf p l = take (length p) l == p
```
**QC trap:** Splitting by `mediumGap` (7 silences) before `shortGap` (3 silences) matters — the longer separator must be split first.

### Mutation 7 — decodeTextWithTree (Morse via tree) (= Assignment 2 Ex 3)
**Spec:** Decode using a binary tree where left=Beep, right=Silence (or some such).
**Sig:** `decodeTextWithTree :: Tree -> Code -> String`
**Solution:**
```haskell
data Tree = Empty | Branch (Maybe Char) Tree Tree

decodeTextWithTree :: Tree -> Code -> String
decodeTextWithTree tree code = go tree code
  where
    go _ []                = []
    go (Branch (Just c) _ _) (Silence : rest) = c : go tree rest  -- emit and reset
    go (Branch _ l _) (Beep : rest)           = go l rest
    go (Branch _ _ r) (Silence : rest)        = go r rest
    go _ _                                    = []
```
**QC trap:** Exact tree shape varies. Resetting to the root after emitting a char is crucial. Beep/Silence interpretation per question.

### Mutation 8 — ramify (table → tree) (= Assignment 2 Ex 4)
**Spec:** Convert a `[(Char, Code)]` table into a `Tree` where each Code path lands the Char.
**Sig:** `ramify :: Table -> Tree`
**Solution:**
```haskell
ramify :: Table -> Tree
ramify = foldr insertEntry Empty
  where
    insertEntry (c, code) t = insert code c t
    insert []     c Empty               = Branch (Just c) Empty Empty
    insert []     c (Branch _ l r)      = Branch (Just c) l r
    insert (a:as) c Empty               = insertSide a as c (Branch Nothing Empty Empty)
    insert (a:as) c (Branch m l r)      = insertSide a as c (Branch m l r)
    insertSide Beep    as c (Branch m l r) = Branch m (insert as c l) r
    insertSide Silence as c (Branch m l r) = Branch m l (insert as c r)
    insertSide _ _ _ Empty = error "unreachable"
```
**QC trap:** Don't overwrite existing branches.

### Mutation 9 — rle (run-length encoding) (= problem 147)
**Spec:** Group consecutive duplicates into `(element, count)`.
**Sig:** `rle :: Eq a => [a] -> [(a, Int)]`
**Solution:**
```haskell
rle :: Eq a => [a] -> [(a, Int)]
rle []     = []
rle (x:xs) = (x, 1 + length leading) : rle rest
  where (leading, rest) = span (== x) xs
```
**QC trap:** `rle "aabbb"` is `[('a',2),('b',3)]`. `rle ""` is `[]`. `rle (replicate 1000 'x')` is `[('x',1000)]`. Use `span` not `takeWhile + dropWhile` separately.

### Mutation 10 — rld (run-length decoding)
**Spec:** Inverse of rle.
**Sig:** `rld :: [(a, Int)] -> [a]`
**Solution:**
```haskell
rld :: [(a, Int)] -> [a]
rld = concatMap (\(x, n) -> replicate n x)
```
**QC trap:** `rld . rle == id` for all input. `rle . rld` is identity only when input is "normalised" (no adjacent pairs with same element).

### Mutation 11 — base-N conversion (Int → [Int] in base b)
**Spec:** Render an integer in base `b` as a list of digits (most significant first).
**Sig:** `toBase :: Int -> Int -> [Int]`
**Solution:**
```haskell
toBase :: Int -> Int -> [Int]
toBase _ 0 = [0]
toBase b n = go n []
  where
    go 0 acc = acc
    go k acc = go (k `div` b) (k `mod` b : acc)
```
**QC trap:** Watch the zero case explicitly. For negative `n`, sign-handle separately.

## Hidden-predicate mutations
- "encode only chars matching p, pass others through" → conditional encode:
```haskell
encodeIf :: (Char -> Bool) -> Int -> String -> String
encodeIf p n = map (\c -> if p c then shift n c else c)
```
- "compress (RLE) only when the run is ≥ k long" → conditional grouping.

## Accumulator-style alternative
For Morse decode with the tree, you can use a single accumulator (current node):
```haskell
decodeAcc tree code = go tree [] code
  where
    go n acc []                = reverse acc
    go (Branch (Just c) _ _) acc (Silence:rest) = go tree (c:acc) rest
    -- ...
```

## Fold-style alternative
RLE can be expressed via `groupBy (==)`:
```haskell
import Data.List (group)
rle' xs = map (\g -> (head g, length g)) (group xs)
```
A clean one-liner — the exam may demand the explicit recursion.

## Cross-family combinations
- this family + `parser-family.md`: decoders are essentially parsers.
- this family + `tree-extract-family.md`: traverse the Morse tree.
- this family + `adt-translation-family.md`: `ramify` and `tabulate` are bidirectional translations between two ADTs.
- this family + `error-handling-family.md`: decoders return Maybe/Either on malformed input.

## QuickCheck universal attacks
- **encode . decode == id** on every well-formed input.
- **decode . encode == id** likewise (if codes are unambiguous).
- **Empty input:** every encoder/decoder yields empty output.
- **Single-char input:** simplest non-trivial round trip.
- **All-same input:** RLE compresses to one pair.
- **Caesar shift of 0:** identity.
- **Caesar 13 twice:** identity (ROT13 property).
- **Morse:** `decodeText t (encodeText t s) == s` for all `s` over valid charset.

## Pitfalls (per mutation)
- M1: not handling negative shift; not preserving case.
- M2: assuming `map shift` on a number — must be `map (shift n)`.
- M3: writing a full second implementation instead of `encode (-n)`.
- M4: putting `shortGap` after the *last* char.
- M5: extra mediumGap at start / end.
- M6: splitting on `shortGap` first (wrong — `mediumGap` contains it).
- M7: forgetting to reset to root after emitting a char.
- M8: insertion order matters; build-up of the tree must agree with traversal direction.
- M9: using `==` with `let (a:b:_) = ...` instead of `span`.
- M10: forgetting `concatMap` (writing `map` would give nested list).
- M11: not handling `0`.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 11 (M1–M11). The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 12 — rotN (parameterised Caesar shift — round-trip with parameter)

**Spec:** Encode/decode with a per-call shift `n`. The decode must use the same `n`.

**Type sig:** `rotEncode :: Int -> String -> String
rotDecode :: Int -> String -> String`

```haskell
rotEncode :: Int -> String -> String
rotEncode n = map (shift n)
  where shift k c
          | isUpper c = chr ((ord c - ord 'A' + k) `mod` 26 + ord 'A')
          | isLower c = chr ((ord c - ord 'a' + k) `mod` 26 + ord 'a')
          | otherwise = c

rotDecode :: Int -> String -> String
rotDecode n = rotEncode (-n)
```

**What changes vs seed:** Codec parameterised by an extra Int — the round-trip property must include the shift parameter. Different from Morse which is parameter-free.

**QC trap:** `mod 26` is essential: `rotEncode 27 'a' = 'b'` and `rotEncode (-1) 'a' = 'z'`. Without `mod`, negative shifts produce gibberish.

## See also

**Primary archetype:** [A07 codec pair](../archetypes/A07-codec-pair.md)
**Sibling families:** [adt-translation](./adt-translation-family.md)
**QuickCheck:** [codec attacks](../quickcheck/codec-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
