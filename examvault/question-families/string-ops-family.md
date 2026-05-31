<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: string-ops**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · [functor-instance](./functor-instance-family.md) · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · **string-ops** · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->





# Family: string-ops

**Archetype:** A09 (Prelude-reimpl) + A21 (list-comp) — string is `[Char]` so every list mutation lifts here   |   **Stars:** ⭐⭐   |   **Course week(s):** 5–6
**Search keywords:** palindrome, letterFreqs, anagram, vowels, occurrences, words, lines, isUpper, isLower, capitalise, reverseWords, ROT, Caesar

## Generator template
```haskell
-- String = [Char]. Every list pattern lifts. Add Data.Char predicates for cleaning.
-- Common shapes:
--   1. Predicate:        isXxx :: String -> Bool
--   2. Count / histogram: countXxx :: String -> Int  or  [(Char, Int)]
--   3. Transform:        toXxx :: String -> String
--   4. Decompose:        splitOn :: Char -> String -> [String]

seedPredicate :: String -> Bool
seedPredicate [] = True              -- usually
seedPredicate s  = combine (head s) (seedPredicate (tail s))

seedTransform :: String -> String
seedTransform = map f . filter g    -- usual flow
```

**Why this family exists:** strings come up as the most pedestrian exam shape (string predicate or basic transform) but they trip students who forget `Data.Char` predicates, Unicode behaviour of `toLower`, or that `"abc"` is `['a','b','c']`. Several mutations duplicate other families with a String wrapper — those cross-link rather than re-implement.

## Mutations (the examiner picks one)

### Mutation 1 — isPalindrome (= problem 55 family)
**Sig:** `isPalindrome :: String -> Bool`
**Spec:** Returns `True` iff the string reads the same forwards and backwards, ignoring case but considering all characters.
**Solution:**
```haskell
import Data.Char (toLower)

isPalindrome :: String -> Bool
isPalindrome s = norm == reverse norm
  where norm = map toLower s
```
**QC trap:** `""` and `"a"` should both return `True`. Some specs strip spaces too — read carefully (`filter (/= ' ')` if so).

### Mutation 2 — letterFreqs (= problem 56)
**Sig:** `letterFreqs :: String -> [(Char, Int)]`
**Spec:** Returns the count of each lower-case letter that appears. Letters not present should NOT appear in the output (some variants ask for the full `'a'..'z'` range with zeros).
**Solution:**
```haskell
import Data.Char (toLower, isAlpha)
import Data.List (group, sort)

letterFreqs :: String -> [(Char, Int)]
letterFreqs s = [ (head g, length g) | g <- group (sort cleaned) ]
  where cleaned = [ toLower c | c <- s, isAlpha c ]
```
**QC trap:** Output should be sorted by character; otherwise QC `==` against a reference list fails. `nub` is not the answer — `group . sort` is.

### Mutation 3 — anagram
**Sig:** `anagram :: String -> String -> Bool`
**Spec:** Two strings are anagrams iff they share the same multiset of letters (case-insensitive, ignoring spaces).
**Solution:**
```haskell
import Data.Char (toLower)
import Data.List (sort)

anagram :: String -> String -> Bool
anagram s t = norm s == norm t
  where norm = sort . map toLower . filter (/= ' ')
```
**QC trap:** Empty + empty = anagram. Two whitespace-only strings = anagram. Decide spec.

### Mutation 4 — countVowels
**Sig:** `countVowels :: String -> Int`
**Spec:** Count occurrences of `a, e, i, o, u` (case-insensitive).
**Solution:**
```haskell
import Data.Char (toLower)

countVowels :: String -> Int
countVowels = length . filter (`elem` "aeiou") . map toLower
```
**QC trap:** `'y'` is sometimes considered a vowel; the marker's spec wins.

### Mutation 5 — countSubstring (sliding window)
**Sig:** `countSubstring :: String -> String -> Int`
**Spec:** Count overlapping occurrences of the pattern in the text.
**Solution:**
```haskell
import Data.List (isPrefixOf)

countSubstring :: String -> String -> Int
countSubstring p s
  | length s < length p = 0
  | p `isPrefixOf` s    = 1 + countSubstring p (tail s)
  | otherwise           = countSubstring p (tail s)
```
**QC trap:** Empty pattern → infinite hits; guard with `p == ""` → 0 (or follow spec).

### Mutation 6 — capitalise
**Sig:** `capitalise :: String -> String`
**Spec:** Upper-case the first letter of each word, lower-case the rest.
**Solution:**
```haskell
import Data.Char (toUpper, toLower)

capitalise :: String -> String
capitalise = unwords . map capWord . words
  where
    capWord []     = []
    capWord (c:cs) = toUpper c : map toLower cs
```
**QC trap:** Multiple spaces collapse via `words` — `"a  b"` becomes `"A B"`. If the spec preserves whitespace, can't use `unwords . words`.

### Mutation 7 — reverseWords
**Sig:** `reverseWords :: String -> String`
**Spec:** Reverse the order of words; leave each word intact.
**Solution:**
```haskell
reverseWords :: String -> String
reverseWords = unwords . reverse . words
```
**QC trap:** Same whitespace-collapse trap as Mutation 6.

### Mutation 8 — wordCount (= problem 39)
**Sig:** `wordCount :: String -> Int`
**Spec:** Number of words.
**Solution:**
```haskell
wordCount :: String -> Int
wordCount = length . words
```
**QC trap:** `""` → `0`; `"   "` → `0`. Both correct.

### Mutation 9 — splitOn (delimiter split)
**Sig:** `splitOn :: Char -> String -> [String]`
**Spec:** Split a string on every occurrence of a delimiter character.
**Solution:**
```haskell
splitOn :: Char -> String -> [String]
splitOn _ [] = [""]
splitOn d (c:cs)
  | c == d    = "" : splitOn d cs
  | otherwise = let (w:ws) = splitOn d cs in (c:w) : ws
```
**QC trap:** `splitOn ',' ""` → `[""]` not `[]`. `splitOn ',' ","` → `["",""]`. Follow `words`/`lines` precedent.

### Mutation 10 — isAlphaOnly
**Sig:** `isAlphaOnly :: String -> Bool`
**Spec:** Every character is alphabetic.
**Solution:**
```haskell
import Data.Char (isAlpha)

isAlphaOnly :: String -> Bool
isAlphaOnly = all isAlpha
```
**QC trap:** `""` → `True` (vacuous). Some specs reject empty — read carefully.

### Mutation 11 — isPrefix / isInfix / isSuffix predicates
**Sig:** `isPrefix, isInfix, isSuffix :: String -> String -> Bool`
**Spec:** Same as `isPrefixOf`, `isInfixOf`, `isSuffixOf` from `Data.List` but written by hand.
**Solution:**
```haskell
isPrefix :: String -> String -> Bool
isPrefix []     _      = True
isPrefix _      []     = False
isPrefix (p:ps) (s:ss) = p == s && isPrefix ps ss

isSuffix :: String -> String -> Bool
isSuffix p s = isPrefix (reverse p) (reverse s)

isInfix :: String -> String -> Bool
isInfix p s = any (isPrefix p) (tails s)
  where tails []     = [[]]
        tails (x:xs) = (x:xs) : tails xs
```
**QC trap:** Empty pattern is prefix/infix/suffix of every string.

### Mutation 12 — caesarShift / caesarEncode / caesarDecode
**Sig:** `caesarShift :: Int -> String -> String`
**Spec:** Shift every letter by `n` (wrapping within its case); leave non-letters unchanged.
**Solution:**
```haskell
import Data.Char (ord, chr, isUpper, isLower)

caesarShift :: Int -> String -> String
caesarShift n = map shift
  where shift c | isUpper c = chr ((ord c - ord 'A' + n) `mod` 26 + ord 'A')
                | isLower c = chr ((ord c - ord 'a' + n) `mod` 26 + ord 'a')
                | otherwise = c
-- caesarShift 3 "abcXYZ!" == "defABC!"; caesarShift (-3) . caesarShift 3 == id
```
**QC trap:** `mod 26` makes negative and >26 shifts behave (`caesarShift (-1) "a" == "z"`). The round-trip is `caesarShift (-n) . caesarShift n == id`.

**Also covered (paired encode/decode) in [codec-family Mutations 1–3](./codec-family.md).** If the exam stem is "encode this with shift n / decode this with shift n / find the shift", open [codec-family.md](./codec-family.md) directly.

> **Family count:** string-ops = **12 mutations** (Mutations 1–12) **+ 1 cross-link** (Mutation 13, `words` reimpl → [list-rewrite-family](./list-rewrite-family.md)).

### Mutation 13 — `words` reimpl
**Cross-link:** See [list-rewrite-family Mutation 5+](./list-rewrite-family.md) for the rewrite-Prelude pattern. `words` is in that family conceptually.

If the exam asks "implement `myWords :: String -> [String]` without using `words`":
```haskell
myWords :: String -> [String]
myWords s = case dropWhile isSpace s of
  "" -> []
  s' -> w : myWords s''
        where (w, s'') = break isSpace s'
  where isSpace c = c == ' ' || c == '\t' || c == '\n'
```

## QuickCheck attack surface

- **Empty string** — every mutation must handle `""`.
- **All same character** — `"aaaa"` for palindrome (`True`), anagram, splitOn, countSubstring.
- **All whitespace** — exposes word-collapse bugs.
- **Unicode / non-ASCII** — `toLower` is locale-aware in some compilers; vLab is ASCII-clean, so this rarely matters.
- **Pattern longer than text** — `countSubstring "abcd" "ab"` → `0`.

See [lists-attacks](../quickcheck/lists-attacks.md) for the underlying string-as-list attacks.

## Pitfalls

- **[P-005 missing base case](../pitfalls/HIGH-severity.md#p-005)** — `""` is the empty list. Cover it.
- **Lazy `length`** — `length xs == 0` is O(n); use `null xs`. (Efficiency, not a marks-killer; see [HIGH-severity](../pitfalls/HIGH-severity.md).)
- **`words` collapses whitespace** — see Mutations 6 + 7.

## Combines with

- **A07** (codec pair) — Caesar / Morse / RLE all build on string mutations.
- **A21** (list-comp synthesis) — `letterFreqs` is a list-comp variant.
- **A03** (generic monad) — `mapM` on `String` returns `m [Char]`.

## See also

**Cross-link to codec:** [codec-family](./codec-family.md)
**Cross-link to list-rewrite:** [list-rewrite-family](./list-rewrite-family.md)
**Cross-link to list-comp:** [list-comp-family](./list-comp-family.md)
**Underlying basics:** [strings](../haskell-basics/strings.md) · [lists](../haskell-basics/lists.md)
**Char predicates:** [allowed-builtins](../haskell-basics/allowed-builtins.md)
**Attacks:** [lists-attacks](../quickcheck/lists-attacks.md)
**Pitfalls:** [HIGH-severity](../pitfalls/HIGH-severity.md) · [MEDIUM-severity](../pitfalls/MEDIUM-severity.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
