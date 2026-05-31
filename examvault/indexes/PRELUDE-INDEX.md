<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **PRELUDE-INDEX**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · [MASTER-INDEX](./MASTER-INDEX.md) · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · **PRELUDE-INDEX** · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# PRELUDE-INDEX

Every `Prelude` / `Data.List` / `Data.Char` / `Data.Maybe` / `Control.Monad` / `Control.Monad.State` / `Control.Monad.Writer` function that matters for the exam.

> Student opens this to remember a function name during the exam. Format: `name` · `signature` · `what it does` · `which template uses it` · `pitfall`.

**Allowed imports in exam (verify per question):**
- `Prelude` (always implicit)
- `Data.List`
- `Data.Char`
- `Data.Maybe`
- `Control.Monad`
- `Control.Monad.State`
- `Control.Monad.Writer`

`Control.Monad.Except`, `Control.Monad.Reader` may NOT be imported in the mock — check the exam paper for whether `Types.hs` preloads them.

---

## Prelude — fundamental

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `id` | `a -> a` | identity | many | nothing |
| `const` | `a -> b -> a` | const-fn | folds, `comparing` | swaps args you might not expect |
| `flip` | `(a -> b -> c) -> b -> a -> c` | swap args | folds | problem 10 reimplements it |
| `(.)` | `(b -> c) -> (a -> b) -> a -> c` | composition | point-free | order: `(f.g) x = f (g x)` |
| `($)` | `(a -> b) -> a -> b` | application | avoid parens | low precedence |
| `seq` | `a -> b -> b` | force eval of 1st arg | strictness | rarely needed |
| `undefined` | `a` | bottom | placeholder | **NEVER leave in submission** |
| `error` | `String -> a` | crash | rarely | marker may catch |
| `otherwise` | `Bool` (= True) | guards | every `if/else as guards` | don't redefine |

## Prelude — comparison

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `(==)` `(/=)` | `Eq a => a -> a -> Bool` | equality | constant | needs `Eq` |
| `compare` | `Ord a => a -> a -> Ordering` | three-way comp | BST, sort | LT/EQ/GT |
| `(<)` `(<=)` `(>)` `(>=)` | `Ord a => a -> a -> Bool` | order | guards | `Ordering` |
| `min` `max` | `Ord a => a -> a -> a` | pairwise | tree height | problem 4 forbids `max` |
| `minimum` `maximum` | `Ord a => [a] -> a` | list extrema | tree-min/max | partial on `[]` |
| `(&&)` `(||)` | `Bool -> Bool -> Bool` | logical | guards | short-circuits |
| `not` | `Bool -> Bool` | negation | guards | nothing |

## Prelude — arithmetic

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `(+) (-) (*)` | `Num a => a -> a -> a` | arithmetic | constant | `Num a` required |
| `(/)` | `Fractional a => a -> a -> a` | division (real) | rarely | not for `Int` |
| `div` `mod` `quot` `rem` | `Integral a => a -> a -> a` | integer div | factors, leap year | `div 0` crashes — guard! |
| `negate` `abs` `signum` | `Num a => a -> a` | unary | sign problem | `signum` returns `a`, not `Int` |
| `fromIntegral` | `(Integral a, Num b) => a -> b` | cast | mixing types | only `Integral → Num` |
| `^` `^^` `**` | `Num/Fractional/Floating` | power | rarely | `^^` for `Fractional`, `**` for `Floating` |
| `succ` `pred` | `Enum a => a -> a` | next/prev | `[Char]` enums | crash on bounds |
| `fromEnum` `toEnum` | `Enum a => ...` | ↔ Int | `Char` ↔ Int | inverse of each other |
| `even` `odd` | `Integral a => a -> Bool` | parity | filters | nothing |
| `gcd` `lcm` | `Integral a => a -> a -> a` | number theory | rarely | nothing |

## Prelude — lists (basic)

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `(:)` | `a -> [a] -> [a]` | cons | constant | constructor |
| `(++)` | `[a] -> [a] -> [a]` | append | `flatten` | O(n) in left arg |
| `head` `tail` | `[a] -> a` / `[a] -> [a]` | first/rest | partial on `[]` | **never call without pattern check** |
| `last` `init` | `[a] -> a` / `[a] -> [a]` | last/all-but-last | problems 22/23 | partial on `[]` |
| `null` | `[a] -> Bool` | empty? | predicate base case | prefer over `length == 0` |
| `length` | `[a] -> Int` | count | constant | strict in spine |
| `reverse` | `[a] -> [a]` | reverse | problem 14 forbids it | O(n) |
| `take` `drop` | `Int -> [a] -> [a]` | first n / drop n | problems 18/19 | negative n → identity-ish (see spec!) |
| `splitAt` | `Int -> [a] -> ([a], [a])` | take + drop | `msort` | nothing |
| `replicate` | `Int -> a -> [a]` | repeat n times | problem 21 | n ≤ 0 → `[]` |
| `repeat` | `a -> [a]` | infinite repeat | lazy work | infinite list |
| `cycle` | `[a] -> [a]` | infinite cycle | rarely | infinite, `cycle []` loops |

## Prelude — lists (higher-order)

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `map` | `(a -> b) -> [a] -> [b]` | each | constant | preserves length |
| `filter` | `(a -> Bool) -> [a] -> [a]` | keep | constant | order-preserving |
| `foldr` | `(a -> b -> b) -> b -> [a] -> b` | right-fold | A10 | works on infinite if combine is lazy |
| `foldl` | `(b -> a -> b) -> b -> [a] -> b` | left-fold | accumulator | strictness needed — prefer `foldl'` from Data.List |
| `foldr1` `foldl1` | non-empty fold | `[a] -> a` (with `Op a a a`) | rarely | crashes on `[]` |
| `scanl` `scanr` | scanning fold | `[(b)]` | running totals | non-empty result |
| `iterate` | `(a -> a) -> a -> [a]` | repeated apply | problem 48 | infinite |
| `concat` | `[[a]] -> [a]` | flatten one level | problem 17 | preserves order |
| `concatMap` | `(a -> [b]) -> [a] -> [b]` | map+concat | list monad bind | `xs >>= f` for lists |
| `mapMaybe` | `(a -> Maybe b) -> [a] -> [b]` | filter+map | problem 98 | from `Data.Maybe` |
| `zip` `unzip` | `[a] -> [b] -> [(a,b)]` / inverse | pair up | problem 20 | stops at shorter |
| `zip3` `unzip3` | triple variant | as above | rarely | |
| `zipWith` | `(a -> b -> c) -> [a] -> [b] -> [c]` | pair with fn | `fibs` | stops at shorter |
| `zipWith3` | binary→3-ary | as above | rarely | |
| `unzip` | `[(a,b)] -> ([a],[b])` | split | rarely | |
| `lookup` | `Eq a => a -> [(a,b)] -> Maybe b` | assoc lookup | env eval, BST→list | problem 24 |
| `elem` `notElem` | `Eq a => a -> [a] -> Bool` | membership | constant | problem 16 |
| `all` `any` | `(a -> Bool) -> [a] -> Bool` | predicate over | constant | `all p []` is True; `any p []` is False |
| `and` `or` | `[Bool] -> Bool` | logical | rarely | identities `True` / `False` |
| `sum` `product` | `Num a => [a] -> a` | aggregate | constant | identities `0` / `1` |

## Prelude — strings / show / read

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `show` | `Show a => a -> String` | to string | I/O, pretty-print | for negative numbers it adds parens |
| `read` | `Read a => String -> a` | parse | rarely | partial — use `reads` |
| `reads` | `Read a => String -> [(a, String)]` | parse with rest | rarely | empty list = parse fail |
| `print` | `Show a => a -> IO ()` | print + newline | I/O | adds quotes to Strings |
| `putStr` `putStrLn` | `String -> IO ()` | print | I/O | no quotes added |
| `getLine` | `IO String` | read line | I/O | no newline at end |
| `getContents` | `IO String` | read all of stdin | rarely | lazy |
| `interact` | `(String -> String) -> IO ()` | filter stdin | rarely | lazy I/O |
| `readLn` | `Read a => IO a` | read+parse a line | problem 110 | partial on bad input |
| `lines` `unlines` | `String -> [String]` / inverse | split by newline | rarely | `unlines` adds trailing `\n` |
| `words` `unwords` | `String -> [String]` / inverse | split by space | problem 39 | nothing |

## Prelude — IO

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `return` | `Monad m => a -> m a` | wrap | every monad | NOT `Just x` etc. — use `pure` |
| `(>>)` | `Monad m => m a -> m b -> m b` | seq (discard) | I/O sequences | not `>>=` |
| `(>>=)` | `Monad m => m a -> (a -> m b) -> m b` | bind | every monad | the key combinator |
| `(=<<)` | flipped bind | rarely | nothing |
| `mapM_` | `Monad m => (a -> m b) -> [a] -> m ()` | for each, discard | problem 104 | underscore = discard |
| `mapM` | `Monad m => (a -> m b) -> [a] -> m [b]` | for each, collect | problem 130 | preserves order |
| `sequence_` | `Monad m => [m a] -> m ()` | run all | rarely | underscore variant |
| `sequence` | `Monad m => [m a] -> m [a]` | run all, collect | problem 129 | preserves order |
| `forM_` `forM` | flipped mapM_/mapM | rarely | reads naturally |
| `when` | `Monad m => Bool -> m () -> m ()` | conditional effect | rarely | `when True m = m` |
| `unless` | `Monad m => Bool -> m () -> m ()` | inverse `when` | rarely | nothing |
| `replicateM_` `replicateM` | `Monad m => Int -> m a -> m ()/m [a]` | n actions | problem 110 | preserves order |

## Prelude — Maybe / Either / Functor / Applicative

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `Nothing` `Just` | `Maybe a` ctors | partial fn return | constant | pattern match both |
| `Left` `Right` | `Either a b` ctors | error or success | error-handling | right-biased Functor/Monad |
| `maybe` | `b -> (a -> b) -> Maybe a -> b` | default+fold | rarely | nothing |
| `either` | `(a -> c) -> (b -> c) -> Either a b -> c` | case dispatch | rarely | nothing |
| `fmap` `(<$>)` | `Functor f => (a -> b) -> f a -> f b` | map under | every functor | preserves structure |
| `pure` | `Applicative f => a -> f a` | lift | every applicative | prefer over `return` in new code |
| `(<*>)` | `Applicative f => f (a -> b) -> f a -> f b` | apply | every applicative | left-to-right effect |
| `(<$)` `(<*) (*>)` | discard variants | rarely | nothing |
| `liftA2` | `Applicative f => (a -> b -> c) -> f a -> f b -> f c` | lift binary | problem 127 | NOT in Prelude until base 4.10 |

## Data.List — extras

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `transpose` | `[[a]] -> [[a]]` | rows ↔ cols | problem 141 magic square | preserves jaggedness |
| `nub` | `Eq a => [a] -> [a]` | dedupe (preserve order) | problem 29 alternative | O(n²) |
| `sort` | `Ord a => [a] -> [a]` | sort | many | nothing |
| `sortBy` | `(a -> a -> Ordering) -> [a] -> [a]` | custom sort | rarely | use `comparing` for keys |
| `sortOn` | `Ord b => (a -> b) -> [a] -> [a]` | sort by key | rarely | nothing |
| `group` | `Eq a => [a] -> [[a]]` | group adjacent equal | problem 147 RLE | use with `sort` for any-pos |
| `groupBy` | `(a -> a -> Bool) -> [a] -> [[a]]` | group with predicate | rarely | comparison must be equiv |
| `permutations` | `[a] -> [[a]]` | all permutations | rarely | n! |
| `subsequences` | `[a] -> [[a]]` | all subseqs | rarely | 2^n |
| `intercalate` | `[a] -> [[a]] -> [a]` | join with sep | pretty-print | (rare) |
| `intersperse` | `a -> [a] -> [a]` | put sep between | rarely | nothing |
| `partition` | `(a -> Bool) -> [a] -> ([a],[a])` | split by pred | problem 50 | preserves order |
| `find` | `(a -> Bool) -> [a] -> Maybe a` | first satisfying | rarely | nothing |
| `findIndex` `elemIndex` | `Eq a => a -> [a] -> Maybe Int` | first pos | rarely | nothing |
| `findIndices` `elemIndices` | all positions | `Eq a => a -> [a] -> [Int]` | problem 37 (positions) alternative | nothing |
| `tails` `inits` | `[a] -> [[a]]` | all suffixes / prefixes | rarely | includes empty |
| `isPrefixOf` `isSuffixOf` `isInfixOf` | `Eq a => [a] -> [a] -> Bool` | substring tests | rarely | nothing |
| `delete` | `Eq a => a -> [a] -> [a]` | first occurrence | rarely | nothing |
| `(\\)` | `Eq a => [a] -> [a] -> [a]` | list difference | rarely | O(n×m) |
| `union` `intersect` | `Eq a => [a] -> [a] -> [a]` | set ops | rarely | preserves order |
| `unfoldr` | `(b -> Maybe (a, b)) -> b -> [a]` | inverse fold | rarely | corecursion |
| `foldl'` | strict left fold | `(b -> a -> b) -> b -> [a] -> b` | accumulator | avoid stack overflow |
| `scanl` `scanr` | scanning folds | `[b]` of intermediates | running tally | nothing |
| `replicate` | already in Prelude | — | — | — |
| `genericLength` | `Num i => [a] -> i` | length with type-flex | rarely | usually overkill |

## Data.Char

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `ord` | `Char -> Int` | char → code | Caesar | nothing |
| `chr` | `Int -> Char` | code → char | Caesar | partial outside Unicode |
| `isDigit` `isAlpha` `isAlphaNum` | `Char -> Bool` | predicates | parsing | nothing |
| `isUpper` `isLower` | `Char -> Bool` | case predicates | Caesar | nothing |
| `isSpace` | `Char -> Bool` | whitespace | parsing | catches `\t`, `\n` |
| `isPrint` `isControl` | `Char -> Bool` | display | rarely | nothing |
| `digitToInt` | `Char -> Int` | digit char → int | problem 100 parseDigit | partial — guard with `isDigit` |
| `intToDigit` | `Int -> Char` | inverse | rarely | partial — 0..15 only |
| `toUpper` `toLower` | `Char -> Char` | case conversion | problem 51 | identity on non-letters |

## Data.Maybe

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `Nothing` `Just` | constructors | — | constant | pattern match |
| `maybe` | `b -> (a -> b) -> Maybe a -> b` | catamorphism | rarely | default-then-fn |
| `fromMaybe` | `a -> Maybe a -> a` | default | rarely | safe extraction |
| `fromJust` | `Maybe a -> a` | extract | **AVOID** | partial — never in safe code |
| `isJust` `isNothing` | `Maybe a -> Bool` | predicates | rarely | nothing |
| `catMaybes` | `[Maybe a] -> [a]` | strip Nothings | problem 97 | preserves order |
| `mapMaybe` | `(a -> Maybe b) -> [a] -> [b]` | filter+map | problem 98 | same as `catMaybes . map f` |
| `listToMaybe` | `[a] -> Maybe a` | first or Nothing | rarely | nothing |
| `maybeToList` | `Maybe a -> [a]` | inverse | rarely | nothing |

## Control.Monad

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `return` `pure` | `Monad m => a -> m a` | wrap | every monad | use `pure` in modern code |
| `(>>=)` | `Monad m => m a -> (a -> m b) -> m b` | bind | every monad | foundation |
| `(>>)` | `Monad m => m a -> m b -> m b` | discard left | I/O | `m >> n = m >>= const n` |
| `join` | `Monad m => m (m a) -> m a` | flatten | problem 128 | `>>= id` |
| `mapM` `mapM_` | `Monad m => (a -> m b) -> [a] -> m [b]/()` | each | problem 130 | preserves order |
| `forM` `forM_` | flipped mapM | rarely | nothing |
| `sequence` `sequence_` | `Monad m => [m a] -> m [a]/()` | run all | problem 129 | nothing |
| `filterM` | `Monad m => (a -> m Bool) -> [a] -> m [a]` | monadic filter | rarely | nothing |
| `foldM` | `Monad m => (b -> a -> m b) -> b -> [a] -> m b` | monadic fold | rarely | nothing |
| `replicateM` `replicateM_` | `Monad m => Int -> m a -> m [a]/()` | n actions | problem 110 | n≤0 → `pure []` |
| `when` `unless` | `Monad m => Bool -> m () -> m ()` | conditional | rarely | nothing |
| `void` | `Functor f => f a -> f ()` | discard result | rarely | `() <$ ma` |
| `liftM` `liftM2` | `Monad m => (a -> b) -> m a -> m b` etc. | lift fn | rarely | use `fmap` / `liftA2` instead |
| `guard` | `Alternative f => Bool -> f ()` | drop branch | list-monad comprehensions | needs `Alternative` |
| `mzero` `mplus` | `MonadPlus m => ...` | failure / merge | rarely | use `empty` / `<|>` |
| `forever` | `Monad m => m a -> m b` | loop forever | rarely | infinite |

## Control.Monad.State

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `State s a` | (newtype-ish) | state-carrying | problem 111+ | use `evalState`/`execState` to escape |
| `get` | `State s s` | read state | every State | nothing |
| `put` | `s -> State s ()` | write state | every State | discards old state |
| `modify` | `(s -> s) -> State s ()` | apply fn to state | every State | `get >>= put . f` |
| `modify'` | strict modify | rarely | not always in scope |
| `gets` | `(s -> a) -> State s a` | project | rarely | `f <$> get` |
| `state` | `(s -> (a, s)) -> State s a` | raw | rarely | nothing |
| `runState` | `State s a -> s -> (a, s)` | run, both | rarely | keeps both |
| `evalState` | `State s a -> s -> a` | run, value | rarely | keeps result |
| `execState` | `State s a -> s -> s` | run, state | counting / labelling | keeps state |
| `withState` | `(s -> s) -> State s a -> State s a` | preprocess state | rarely | nothing |

## Control.Monad.Writer

| Name | Signature | What | Used in | Pitfall |
|---|---|---|---|---|
| `Writer w a` | (newtype-ish) | value+log | problem 107+ | needs `Monoid w` |
| `tell` | `Monoid w => w -> Writer w ()` | emit log | every Writer | nothing |
| `runWriter` | `Writer w a -> (a, w)` | extract pair | rarely | nothing |
| `execWriter` | `Writer w a -> w` | extract log | rarely | nothing |
| `writer` | `(a, w) -> Writer w a` | raw | rarely | nothing |
| `listen` | `Writer w a -> Writer w (a, w)` | observe log | rarely | rarely needed in exam |
| `censor` | `(w -> w) -> Writer w a -> Writer w a` | modify log | rarely | nothing |
| `Sum n` | `Num a => Sum a` | monoid wrapper for `+` | problem 108 | from `Data.Monoid` |
| `Product n` | analogous | rarely | `*` monoid |
| `getSum` `getProduct` | unwrap | when extracting Writer log | nothing |

## Things you CANNOT import in exam (without checking)

| Module | Why you might think you can | What to use instead |
|---|---|---|
| `Data.Map` | very useful for env | use `[(k, v)]` assoc list |
| `Data.Set` | sometimes wanted | use sorted list / `[]` |
| `Data.Sequence` | rare | use `[]` |
| `Numeric.showHex` | hex pretty-print | hand-roll hex digits (problem 64) |
| `Text.Read` | safer read | use `reads` from Prelude |
| `Control.Monad.Except` / `Control.Monad.Reader` | maybe preloaded by Types.hs | check the question paper |
| `Test.QuickCheck` | for writing properties | marker imports it, you don't need to |
| `System.*` | I/O extras | not needed |

---

## Pitfalls compendium (Prelude-level)

1. **`head []` / `tail []` / `last []` / `init []`** — partial. Pattern-match first.
2. **`div` / `mod` by zero** — crash. Guard.
3. **`fromJust`** — partial. Don't.
4. **`foldl` on infinite list** — hangs (uses strictness wrong). Use `foldr` for infinite or `foldl'` for finite.
5. **`length` on infinite list** — bottom.
6. **`read "foo"`** — partial. Use `reads` and pattern match.
7. **`-3` in pattern** — parses as `(-)` applied; use `n | n == -3` or `Negative 3` newtype.
8. **`(+ 1)` section** but **`(- 1)` doesn't** (it's negation). Use `subtract 1` or `(\x -> x - 1)`.
9. **`mapM` is strict in the spine** — for infinite lists prefer streaming.
10. **`take n` with `n < 0`** returns `[]` — don't rely on it crashing.
11. **`replicate n x` with `n ≤ 0`** returns `[]` — don't rely on it crashing.
12. **`show` of a `String`** adds quotes — use `putStr` not `print` for raw output.
13. **`print` of a `Float`** may produce `1.5e-2` — use a formatter.
14. **`isUpper '+'` / `isAlpha '0'`** — both `False`, but easy to misremember. Check.
15. **`zip` and `zipWith` stop at shorter** — won't pad. If you want padding, write it yourself.
16. **`reverse (reverse xs)`** is O(n) — not identity in big-O.

---

## See also
- [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) — when the problem says "reimplement X without using X".
- [IF-YOU-SEE-X](IF-YOU-SEE-X.md) — for the inverse direction (phrase → function).
- [PROBLEM-NUMBER-INDEX](PROBLEM-NUMBER-INDEX.md) — which problem reimplements which.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
