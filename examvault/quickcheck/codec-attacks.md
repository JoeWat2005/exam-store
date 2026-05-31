<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: encode / decode / codec / Morse / round-trip**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · **codec** · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: encode / decode / codec / Morse / round-trip

**Search keywords:** encode, decode, codec, Morse, encodeWord, decodeText, ramify, tabulate, round-trip, isomorphism, table lookup, prefix code, Tree-based decode

Assignment 2 is the canonical codec question (Morse code). The marker tests:
1. `encodeWord`, `encodeWords`, `encodeText` are correct
2. `decodeText` correctly reverses `encodeText`
3. `decodeTextWithTree` (using a `Tree`-based dictionary) matches the table version
4. `ramify cs` produces a valid `Tree`
5. `tabulate t` produces a valid `Table`
6. `ramify` and `tabulate` are inverses up to equivalence

## What the marker generates

Direct from `Assignment2Marking.hs`:

```haskell
arbitraryChar :: Gen Char
arbitraryChar = elements $ ['A'..'Z']++['0'..'9']
-- ↑ ONLY uppercase letters and digits — no lowercase, no spaces.

arbitraryWord :: Gen String
arbitraryWord = listOf1 arbitraryChar    -- non-empty

arbitraryText :: Gen Text
arbitraryText = resize 15 ((intercalate " ") <$> listOf1 arbitraryWord)
-- ↑ Multi-word text, words space-separated, total resize 15.

shrinkWord :: String -> [String]
shrinkWord xs = [take n xs | n <- [1 .. length xs - 1]]
```

Important shrinking strategy: shrunk inputs are PREFIXES of the original. So when you fail on `"HELLO"`, the marker shrinks down to `"H"` to give you a tiny counterexample.

```haskell
-- For decoding tests, the marker generates codes by encoding then testing:
arbitraryCodeChar = (\c -> Solutions.encodeText markingTable [c]) <$> arbitraryChar
arbitraryCodeWord = Solutions.encodeText markingTable <$> arbitraryWord
arbitraryCodeText = Solutions.encodeText markingTable <$> arbitraryText
```

So `decodeText` is tested with strings that are the OUTPUT of the reference `encodeText`. **You cannot rely on testing with arbitrary strings — only with valid encodings.**

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | Single character `"A"` | encodeWord "A" | Off-by-one in word/text logic | Word-level test should equal char-level |
| 2 | Single word `"HELLO"` | encodeWord vs encodeWords [w] | `encodeWords [w]` should equal `encodeWord w` | Single-word test (3 marks fallback) |
| 3 | Multiple words `"HELLO WORLD"` | encodeText | Words separated by mediumGap | Use `intercalate mediumGap` (the dot-dash separator for between words) |
| 4 | Empty word `""` | not generated but defensive | `head ""` crashes | Pattern-match early on `""` |
| 5 | Word with digits only `"123"` | tested | Char range is `A-Z` plus `0-9` | Make sure lookup handles digits |
| 6 | Decode `""` → `""` | base case | If you `head` the empty string, crash | Handle empty code first |
| 7 | Decode single-char encoding | round-trip | `decodeText t (encodeText t [c]) == [c]` | The 4-mark fallback test |
| 8 | Decode multi-word | round-trip | Spaces become `mediumGap` in encoded form | Re-split by mediumGap |
| 9 | `ramify cs` builds correct `Tree` | `ramify markingTable` should equal canonical reference | Bug in tree construction → all decode tests fail | Recursively split table by leading symbol |
| 10 | `tabulate` is inverse of `ramify` | `tabulate (ramify cs)` is a permutation of `cs` | If you build tabulate wrong, the set-equality fails | `p_seteq` so order doesn't matter |
| 11 | Round-trip on full text | `decodeText t (encodeText t s) == s` | If encoding loses info, decoding can't recover | Test the round-trip property locally |
| 12 | Tree with `Empty` branches | a `Tree` constructor may have one or both children `Empty` | If you don't pattern-match `Empty`, you crash on lookup | Handle `Empty` early |
| 13 | Decoding ambiguous code | shouldn't be generated, but the prefix property of Morse means it shouldn't be ambiguous | If you greedy-match too far, mismatches | Use the tree to disambiguate (each leaf is a complete code) |

## Property templates

```haskell
import Test.QuickCheck
import Data.List (intercalate)

-- Round-trip property (THE big one)
prop_encodeDecode :: String -> Bool
prop_encodeDecode s = decodeText markingTable (encodeText markingTable s) == s

-- Tree and table are equivalent
prop_treeTableAgree :: String -> Bool
prop_treeTableAgree s =
  decodeTextWithTree markingTree code == decodeText markingTable code
  where code = encodeText markingTable s
        markingTree = ramify markingTable

-- ramify and tabulate are inverses (set equality)
prop_ramifyTabulate :: Table -> Bool
prop_ramifyTabulate t = sort (tabulate (ramify t)) == sort t

-- encodeWord is the building block
prop_encodeWord_eqWords :: String -> Bool
prop_encodeWord_eqWords w = encodeWord markingTable w == encodeWords markingTable [w]

-- encodeText splits on spaces and encodes each word
prop_encodeText_eqWords :: String -> Bool
prop_encodeText_eqWords t = encodeText markingTable t == encodeWords markingTable (words t)
```

## Self-test before submission checklist

- [ ] `encodeWord` works on a single character
- [ ] `encodeWord` works on a 5-letter word
- [ ] `encodeWord` works on a word with digits
- [ ] `encodeWords [w] == encodeWord w` (single-word case)
- [ ] `encodeText "ONE TWO" == encodeWords markingTable ["ONE", "TWO"]`
- [ ] `decodeText markingTable (encodeText markingTable s) == s` for any well-formed `s`
- [ ] `decodeTextWithTree` returns same as `decodeText` for any code
- [ ] `ramify markingTable` doesn't error on the marking table
- [ ] `tabulate (ramify cs)` is a permutation of `cs`
- [ ] No `head` / `!!` on possibly-empty inputs
- [ ] All Tree constructors (`Empty`, `Branch`) handled in lookup

## Pitfalls that specifically lose QC marks

### Pitfall: empty input crashes
```haskell
-- WRONG:
encodeWord t (c:cs) = lookup c t ++ smallGap ++ encodeWord t cs
encodeWord t []     = ""    -- this MUST come first or be handled
-- Otherwise, crashes on empty word.

-- Actually the right pattern is:
encodeWord _ []     = ""
encodeWord t (c:cs) = lookup c t ++ smallGap ++ encodeWord t cs   -- but mind trailing gap!
```

### Pitfall: trailing separator
```haskell
-- WRONG: trailing smallGap
encodeWord t [c]    = lookup c t ++ smallGap   -- ← extra gap
encodeWord t (c:cs) = lookup c t ++ smallGap ++ encodeWord t cs

-- Fix: separator BETWEEN, not after
encodeWord t []     = ""
encodeWord t [c]    = lookup c t                          -- ← no trailing gap
encodeWord t (c:cs) = lookup c t ++ smallGap ++ encodeWord t cs

-- Or cleaner with intercalate:
encodeWord t cs = intercalate smallGap [lookup c t | c <- cs]
```

### Pitfall: confusing `smallGap` vs `mediumGap` vs `largeGap`
```haskell
-- smallGap  = " "       -- between letters in a word
-- mediumGap = "   "     -- between words in text
-- largeGap  = "       " -- not used in basic Morse but may appear in problem

-- WRONG: same gap for both levels
encodeWords t ws = intercalate smallGap (map (encodeWord t) ws)
-- Now you can't tell letter boundaries from word boundaries.

-- Fix:
encodeWords t ws = intercalate mediumGap (map (encodeWord t) ws)
```

### Pitfall: `ramify` ignores the structure of codes
```haskell
-- The Tree is built so that each step (Left/Right or '.'/'-') corresponds to a code symbol.
-- A character's code is the PATH from root to its leaf.
-- WRONG: just put all characters at root level
ramify cs = Branch (map (\(c, _) -> Leaf c) cs) Empty
-- Fix: recursive split by leading symbol of remaining code
```

### Pitfall: `tabulate` reverses path direction
```haskell
-- WRONG: builds code in reverse
tabulate Empty = []
tabulate (Branch _ l r) = ... -- if you prepend '-' for left instead of appending, code is reversed
-- The original ramify built code top-down. tabulate must rebuild it the same way.
```

### Pitfall: `decodeTextWithTree` doesn't restart at root after a leaf
```haskell
-- WRONG: stays at leaf after reaching it
decodeTextWithTree t s = go t s
  where go (Branch x _ _) (' ':rest) = x : go (Branch x _ _) rest  -- ← stays!
        go _ _ = ...
-- Fix: after emitting a character (at leaf), GO BACK TO ROOT
decodeTextWithTree root = go root
  where go (Leaf x) rest = x : go root rest   -- ← restart at root
        ...
```

### Pitfall: forgot the spec-defined "Tree" type has its own constructors
Assignment 2's `Tree` is:
```haskell
data Tree = Empty | Branch Atom Tree Tree
-- Atom is sometimes Char, sometimes Maybe Char.
-- Branch has a "value at this node" — for non-leaf intermediate nodes, this may be Nothing.
```

Check the actual `Types.hs` carefully.

### Pitfall: forgetting `markingTable` is fixed
```haskell
-- The marker uses ONE TABLE: markingTable. It's defined in Types.hs.
-- Your encodeWord/decodeText must use whatever table is passed in,
-- but the marker only ever passes markingTable.

-- So locally you can test:
encodeWord markingTable "HELLO"   -- but the function works for any Table
```

## See also

**Archetypes:** [A07 codec pair](../archetypes/A07-codec-pair.md) · [A05 ADT translation](../archetypes/A05-adt-translation.md)
**Question families:** [codec](../question-families/codec-family.md) · [adt-translation](../question-families/adt-translation-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
