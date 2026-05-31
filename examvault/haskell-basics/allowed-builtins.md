<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Allowed built-ins**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · **allowed-builtins** · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Allowed built-ins

## The allowed import set (memorise)

The marker compiles with `-XSafe`. Only these modules are allowed (plus the question's own `Types` module if it provides one):

```haskell
import Data.List
import Data.Char
import Data.Maybe
import Control.Monad
import Control.Monad.State
import Control.Monad.Writer
-- Prelude is implicit
```

Anything else → import error → **zero marks** for the whole question (the file fails to compile). See [imports-pitfalls](../pitfalls/imports-pitfalls.md) for the full trap list, and [P-013](../pitfalls/HIGH-severity.md#p-013) for the canonical war story.

Below is a quick-reference of the functions you can rely on. Tiny example each; if a function has its own deeper page, the heading links to it.

---

## Prelude — list HOFs

### [`map`](./map.md)
```haskell
map :: (a -> b) -> [a] -> [b]
map (+1) [1,2,3]   ==> [2,3,4]
```
Apply a function to every element. Pure shape-preserving transform.

### [`filter`](./filter.md)
```haskell
filter :: (a -> Bool) -> [a] -> [a]
filter even [1..6]   ==> [2,4,6]
```
Keep elements matching the predicate.

### [`foldr`](./foldr.md)
```haskell
foldr :: (a -> b -> b) -> b -> [a] -> b
foldr (+) 0 [1,2,3]   ==> 6
foldr (:) [] xs       ==> xs        -- identity
```
Right-associative fold. The natural shape for any list-recursion.

### [`foldl`](./foldl.md)
```haskell
foldl :: (b -> a -> b) -> b -> [a] -> b
foldl (+) 0 [1,2,3]   ==> 6
foldl (-) 10 [1,2]    ==> 7         -- (10-1)-2
```
Left-associative fold. Often used as a `foldl'` accumulator in Hoogle answers, but plain `foldl` is allowed; on infinite lists it doesn't terminate.

### `foldr1`, `foldl1`
```haskell
foldr1 :: (a -> a -> a) -> [a] -> a    -- empty list: error
maximum xs == foldr1 max xs
```
Fold without a seed. **Errors on `[]`** — guard first.

### [`zip`](./zip.md), [`zipWith`](./zipWith.md)
```haskell
zip [1,2,3] "abc"      ==> [(1,'a'),(2,'b'),(3,'c')]
zipWith (+) [1,2] [10,20]   ==> [11,22]
```
Pair / combine two lists element-wise. Both stop at the shorter list.

### [`all`, `any`](./all-any.md)
```haskell
all even [2,4,6]   ==> True
any odd  [2,4,6]   ==> False
```
Boolean folds. `all p []` is `True` (vacuous); `any p []` is `False`.

### `and`, `or`
```haskell
and [True, True, False]   ==> False
or  [False, True]         ==> True
```
Same as `all id` / `any id`.

### `concat`, `concatMap`
```haskell
concat [[1,2],[3]]              ==> [1,2,3]
concatMap (\x -> [x,x]) [1,2]   ==> [1,1,2,2]
```
Flatten / map-then-flatten. `concatMap f = concat . map f`. Used a LOT in interpreter / list-monad work.

### `replicate`
```haskell
replicate :: Int -> a -> [a]
replicate 3 'x'   ==> "xxx"
```

### `take`, `drop`, `splitAt`
```haskell
take 3 [1..]      ==> [1,2,3]
drop 2 [1..5]     ==> [3,4,5]
splitAt 2 [1..5]  ==> ([1,2],[3,4,5])
```

### `takeWhile`, `dropWhile`, `span`, `break`
```haskell
takeWhile (<3) [1..5]   ==> [1,2]
dropWhile (<3) [1..5]   ==> [3,4,5]
span (<3) [1..5]        ==> ([1,2],[3,4,5])
break (>=3) [1..5]      ==> ([1,2],[3,4,5])
```

### `reverse`, `length`, `null`, `head`, `tail`, `last`, `init`
```haskell
reverse [1,2,3]   ==> [3,2,1]
length "abc"      ==> 3
null []           ==> True
head [1,2,3]      ==> 1     -- partial!
tail [1,2,3]      ==> [2,3] -- partial!
last [1,2,3]      ==> 3     -- partial!
init [1,2,3]      ==> [1,2] -- partial!
```
**Exam warning:** `head`, `tail`, `last`, `init` are all partial (crash on `[]`). Use pattern matching or `Data.Maybe`'s `listToMaybe` instead.

### `sum`, `product`, `minimum`, `maximum`
```haskell
sum [1..5]      ==> 15
product [1..5]  ==> 120
minimum [3,1,2] ==> 1
maximum [3,1,2] ==> 3
```
`minimum`/`maximum` are partial on `[]`.

### `elem`, `notElem`, `lookup`
```haskell
elem 3 [1,2,3]         ==> True
notElem 5 [1,2,3]      ==> True
lookup 'b' [('a',1),('b',2)]   ==> Just 2
```
`lookup` returns `Maybe v` — already safe.

### `iterate`, `cycle`, `repeat`
```haskell
take 5 (iterate (*2) 1)   ==> [1,2,4,8,16]
take 6 (cycle "ab")       ==> "ababab"
take 4 (repeat 0)         ==> [0,0,0,0]
```
Infinite list generators. **Don't print without `take`.**

### `zip3`, `zipWith3`
```haskell
zip3 [1,2] "ab" [True,False]   ==> [(1,'a',True),(2,'b',False)]
```

---

## Prelude — number & boolean

```haskell
even, odd          :: Integral a => a -> Bool
abs, signum, negate :: Num a => a -> a
min, max           :: Ord a => a -> a -> a
compare            :: Ord a => a -> a -> Ordering
div, mod, quot, rem :: Integral a => a -> a -> a
gcd, lcm           :: Integral a => a -> a -> a
fromIntegral       :: (Integral a, Num b) => a -> b
```

**Exam warning:** `div` rounds toward `-∞`, `quot` toward 0. `mod` and `rem` differ on negatives. For non-negative inputs they agree.

---

## Prelude — function combinators

```haskell
id        :: a -> a
const     :: a -> b -> a
flip      :: (a -> b -> c) -> b -> a -> c
(.)       :: (b -> c) -> (a -> b) -> a -> c
($)       :: (a -> b) -> a -> b
(&)       :: a -> (a -> b) -> b      -- Data.Function — not in Safe Prelude on older GHCs; check before using
seq       :: a -> b -> b
curry     :: ((a, b) -> c) -> a -> b -> c
uncurry   :: (a -> b -> c) -> (a, b) -> c
fst, snd  :: (a, b) -> a / b
```

[`.`](./dot-operator.md) for composition, [`$`](./dollar-operator.md) to drop parentheses.

---

## Data.List

```haskell
sort        :: Ord a => [a] -> [a]
sortBy      :: (a -> a -> Ordering) -> [a] -> [a]
sortOn      :: Ord b => (a -> b) -> [a] -> [a]
nub         :: Eq a => [a] -> [a]            -- remove duplicates
nubBy       :: (a -> a -> Bool) -> [a] -> [a]
group       :: Eq a => [a] -> [[a]]
groupBy     :: (a -> a -> Bool) -> [a] -> [[a]]
intercalate :: [a] -> [[a]] -> [a]           -- e.g. intercalate ", " ["a","b","c"]
intersperse :: a -> [a] -> [a]               -- intersperse ',' "abc" == "a,b,c"
transpose   :: [[a]] -> [[a]]                -- magic-square / matrix
permutations:: [a] -> [[a]]
subsequences:: [a] -> [[a]]
isPrefixOf  :: Eq a => [a] -> [a] -> Bool
isSuffixOf  :: Eq a => [a] -> [a] -> Bool
isInfixOf   :: Eq a => [a] -> [a] -> Bool
delete      :: Eq a => a -> [a] -> [a]
(\\)        :: Eq a => [a] -> [a] -> [a]     -- list difference
union, intersect
find        :: (a -> Bool) -> [a] -> Maybe a
findIndex   :: (a -> Bool) -> [a] -> Maybe Int
elemIndex   :: Eq a => a -> [a] -> Maybe Int
partition   :: (a -> Bool) -> [a] -> ([a],[a])
unfoldr     :: (b -> Maybe (a, b)) -> b -> [a]
tails, inits
scanl, scanr, scanl1, scanr1
```

Examples:

```haskell
sort [3,1,2]                     ==> [1,2,3]
sortOn negate [1,2,3]            ==> [3,2,1]
nub [1,1,2,2,3]                  ==> [1,2,3]
group "aaabbc"                   ==> ["aaa","bb","c"]
transpose [[1,2,3],[4,5,6]]      ==> [[1,4],[2,5],[3,6]]
intercalate ", " ["a","b","c"]   ==> "a, b, c"
partition even [1..6]            ==> ([2,4,6],[1,3,5])
find (>3) [1..5]                 ==> Just 4
```

**Exam-favourite:** `transpose` makes matrix-row / matrix-column logic trivial — magic squares (Mock Q4), Sudoku, TicTacToe.

---

## Data.Char

```haskell
isDigit, isAlpha, isAlphaNum, isSpace, isUpper, isLower, isPunctuation, isHexDigit
toUpper, toLower
digitToInt :: Char -> Int        -- '0'..'9' / 'a'..'f' / 'A'..'F'
intToDigit :: Int -> Char        -- 0..15
ord  :: Char -> Int              -- 'a' -> 97
chr  :: Int -> Char              -- 97 -> 'a'
```

```haskell
map toUpper "hello"          ==> "HELLO"
filter isDigit "ab12c3"      ==> "123"
ord 'A'                      ==> 65
chr 65                       ==> 'A'
```

Caesar/Morse codecs lean heavily on `ord`/`chr` for shift-by-N.

---

## Data.Maybe

```haskell
maybe       :: b -> (a -> b) -> Maybe a -> b
fromMaybe   :: a -> Maybe a -> a
isJust, isNothing :: Maybe a -> Bool
fromJust    :: Maybe a -> a                  -- partial!
catMaybes   :: [Maybe a] -> [a]
mapMaybe    :: (a -> Maybe b) -> [a] -> [b]
listToMaybe :: [a] -> Maybe a
maybeToList :: Maybe a -> [a]
```

```haskell
maybe 0 (+1) (Just 5)        ==> 6
maybe 0 (+1) Nothing         ==> 1
fromMaybe 0 (Just 5)         ==> 5
fromMaybe 0 Nothing          ==> 0
catMaybes [Just 1, Nothing, Just 2]   ==> [1,2]
mapMaybe (\n -> if n > 0 then Just (n*2) else Nothing) [-1,2,-3,4]   ==> [4,8]
```

**Exam warning:** `fromJust` is partial — use `fromMaybe`/`maybe`/pattern-match. The marker can throw `Nothing` at you and `fromJust Nothing` = `error`.

See [maybe-basics](./maybe-basics.md) and [maybe monad](../monads/maybe.md).

---

## Control.Monad

```haskell
return, pure        :: a -> m a
(>>=), (>>)         :: m a -> (a -> m b) -> m b
mapM, mapM_         :: Monad m => (a -> m b) -> [a] -> m [b] / m ()
forM, forM_         :: flip mapM
sequence, sequence_ :: Monad m => [m a] -> m [a] / m ()
replicateM, replicateM_ :: Int -> m a -> m [a] / m ()
when, unless        :: Applicative f => Bool -> f () -> f ()
void                :: Functor f => f a -> f ()
join                :: Monad m => m (m a) -> m a
foldM, foldM_       :: Monad m => (b -> a -> m b) -> b -> [a] -> m b / m ()
filterM             :: Monad m => (a -> m Bool) -> [a] -> m [a]
guard               :: Alternative f => Bool -> f ()
liftM, liftM2       :: same as fmap / liftA2
(<=<), (>=>)        :: Kleisli composition
```

```haskell
mapM print [1,2,3]               -- IO () prints three lines
sequence [Just 1, Just 2]        ==> Just [1,2]
sequence [Just 1, Nothing]       ==> Nothing
replicateM 3 (Just 'x')          ==> Just "xxx"
when (x > 0) (putStrLn "yay")
foldM (\acc x -> if x>0 then Just (acc+x) else Nothing) 0 [1,2,3]   ==> Just 6
filterM (\_ -> [True, False]) [1,2]   ==> [[1,2],[1],[2],[]]  -- powerset
```

`mapM`, `sequence`, `replicateM` are the workhorse "do this action over a list" combinators. See [A03 generic monad](../archetypes/A03-generic-monad.md) and [generic-combinators](../monads/generic-combinators.md).

---

## Control.Monad.State

```haskell
type State s a = StateT s Identity a
get      :: State s s
put      :: s -> State s ()
modify   :: (s -> s) -> State s ()
modify'  :: (s -> s) -> State s ()       -- strict
gets     :: (s -> a) -> State s a
state    :: (s -> (a, s)) -> State s a
runState   :: State s a -> s -> (a, s)
evalState  :: State s a -> s -> a
execState  :: State s a -> s -> s
```

```haskell
runState  (do { x <- get; put (x+1); return x }) 10   ==> (10, 11)
evalState (do { x <- get; put (x+1); return x }) 10   ==> 10        -- forget final state
execState (do { x <- get; put (x+1); return x }) 10   ==> 11        -- forget result
modify (+1) :: State Int ()
gets fst :: State (a,b) a
```

Mock Q3 (Nim) and every state-game variant (see [A02](../archetypes/A02-state-game.md), [state-game-family](../question-families/state-game-family.md)) use these.

---

## Control.Monad.Writer

```haskell
type Writer w a = WriterT w Identity a
tell      :: w -> Writer w ()
runWriter :: Writer w a -> (a, w)
execWriter:: Writer w a -> w
writer    :: (a, w) -> Writer w a
```

```haskell
runWriter (do { tell ["start"]; tell ["mid"]; return 42 })
   ==> (42, ["start","mid"])
execWriter (tell [1] >> tell [2])    ==> [1,2]
```

`tell` accumulates with `mappend` — usually `[]`/`++` or `Sum`/`+`. The log builds in **left-to-right** order.

Used by [A15 writer trace](../archetypes/A15-writer-trace.md) and any "log the steps" interpreter mutation.

---

## Tiny "what should I reach for?" cheat

| Need | Function |
|---|---|
| Apply f to every element | `map` |
| Keep elements matching p | `filter` |
| Combine list into one value | `foldr` or `foldl` |
| Combine two lists element-wise | `zipWith` |
| Test "all elements" / "any element" | `all` / `any` |
| Sort | `sort` (or `sortOn`) |
| Remove dupes | `nub` |
| Matrix columns | `transpose` |
| Lookup by key | `lookup` |
| Drop the `Maybe` with a default | `fromMaybe`, `maybe` |
| Drop the `Maybe` and bail | use a pattern match — avoid `fromJust` |
| Pull values out of `[Maybe a]` | `catMaybes` |
| Both filter and map | `mapMaybe` |
| Run an action n times | `replicateM` / `replicateM_` |
| Run an action over a list | `mapM` / `mapM_` |
| Convert `[m a]` into `m [a]` | `sequence` |
| Track a counter / world | `State` + `get` / `put` / `modify` |
| Build a running log | `Writer` + `tell` |
| Char → Int | `ord` |
| Int → Char | `chr` |

## Exam use

When in doubt: prefer recursion you wrote yourself over a library one-liner. The marker awards full marks for either, but a hand-rolled recursion has fewer surprise-import pitfalls. Reach for `transpose`, `sort`, `nub`, `lookup`, `mapM`, `replicateM`, `tell`, `get`/`put`/`modify` once you know they're allowed.

## See also

**Stricter import rules:** [imports-pitfalls](../pitfalls/imports-pitfalls.md) · [P-013 imports forbidden](../pitfalls/HIGH-severity.md#p-013)
**Standard HOFs in depth:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
**Prelude-only index:** [PRELUDE-INDEX](../indexes/PRELUDE-INDEX.md)
**Type-signature search:** [TYPE-SIGNATURE-DATABASE](../indexes/TYPE-SIGNATURE-DATABASE.md)
**Generic monad combinators:** [generic-combinators](../monads/generic-combinators.md) · [A03 generic monad](../archetypes/A03-generic-monad.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
