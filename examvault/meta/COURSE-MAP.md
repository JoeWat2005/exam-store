<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [meta](./README.md) · **COURSE-MAP — Birmingham FP 2025/26**

<!-- siblings:start -->
> **Peers:** [COURSE-COVERAGE](./COURSE-COVERAGE.md) · **COURSE-MAP** · [FINAL-SWEEP-REPORT](./FINAL-SWEEP-REPORT.md) · [GAP-AUDIT](./GAP-AUDIT.md) · [SCRIPT-COMPATIBILITY-REPORT](./SCRIPT-COMPATIBILITY-REPORT.md) · [VAULT-AUDIT](./VAULT-AUDIT.md) · [WIKI-UPGRADE-REPORT](./WIKI-UPGRADE-REPORT.md)
<!-- siblings:end -->






# COURSE-MAP — Birmingham FP 2025/26

Index of every lecture topic. One block per topic. Used by every other vault file as the source of truth for week, dependencies, exam probability, and archetype links.

Lecture roots live under `fp-learning-2025/files/LectureNotes/Sections/`. All paths in this file are relative to that directory unless prefixed with `files/`.

Probability scale:
- 5 = appears in mock OR 3+ assignments OR is fundamental to every monadic question
- 4 = appears in 2 assignments OR pervasive across problem sheets
- 3 = appears in 1 assignment / 1 mock-style question
- 2 = recur in problem sheets but never assessed
- 1 = lectured for context, almost never asked standalone

---

## types

- **Lecture file:** `types.md` (week 1)
- **Course week:** 1
- **Exam probability:** ⭐⭐
- **Dependencies:** none
- **Related concepts:** polymorphism, pattern-matching, typeclasses-basic
- **Typical type signatures:**
  ```haskell
  f :: Int -> Bool
  g :: (a, b) -> a
  h :: [Char] -> Int
  ```
- **Question generators:**
  - "Give the most general type of `\f x -> f (f x)`"
  - "Why does `False == 'c'` fail to type-check?"
  - "Annotate this expression with the type ghci would infer"
  - "Translate the English sentence into a Haskell type"
- **Common mistakes:**
  - Forgetting the `Eq a =>` context when the function uses `==`
  - Writing `[Int -> Bool]` when you meant `[Int] -> Bool`
  - Confusing `(a, b) -> c` (function on a pair) with `a -> b -> c` (curried)
- **Related archetypes:** none directly — supports A09 by setting the sig
- **Search keywords:** type, signature, ::, inference, curried, polymorphic, tuple type

## pattern-matching

- **Lecture file:** `functions.md` (week 1)
- **Course week:** 1
- **Exam probability:** ⭐⭐⭐⭐⭐
- **Dependencies:** types
- **Related concepts:** guards, custom-ADTs, list-recursion, Maybe, Either
- **Typical type signatures:**
  ```haskell
  f :: [a] -> Int
  g :: Maybe a -> b -> b
  h :: Shape -> Double
  ```
- **Question generators:**
  - "Define `f` by pattern matching on `(Empty | Fork _ _ _)`"
  - "Give the missing case the compiler warns about (`-fwarn-incomplete-patterns`)"
  - "Rewrite this `if`-chain as a pattern-match"
  - "Pattern-match on `(x:y:rest)` to access the first two elements"
- **Common mistakes:**
  - Leaving `_` for the last list cons case and then needing the tail
  - Falling through on a constructor — non-exhaustive pattern at runtime
  - Pattern matching on `(_, _)` where `_` shadows a needed variable
- **Related archetypes:** A01, A05, A09, A11
- **Search keywords:** pattern, match, case, cons, deconstruct, exhaustive, fall through

## guards

- **Lecture file:** `functions.md` (week 1)
- **Course week:** 1
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** pattern-matching, types
- **Related concepts:** list-comprehensions (share `|` syntax), conditionals
- **Typical type signatures:**
  ```haskell
  sign :: Int -> Int
  between :: Int -> Int -> Int -> Bool
  classify :: Char -> String
  ```
- **Question generators:**
  - "Rewrite `if/then/else` as a guarded equation"
  - "Use `otherwise` to give an exhaustive default"
  - "Combine guards with `where` to share a computation"
- **Common mistakes:**
  - Forgetting `otherwise` — runtime crash on inputs that fall through
  - Using `=` instead of `|` between guards
  - Putting guards on the wrong side of pattern arguments
- **Related archetypes:** A09 (Prelude rewrites)
- **Search keywords:** guard, |, otherwise, conditional, where

## polymorphism

- **Lecture file:** `polymorphism.md` (week 2)
- **Course week:** 2
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** types
- **Related concepts:** typeclasses-basic, higher-order-functions, Functor
- **Typical type signatures:**
  ```haskell
  id  :: a -> a
  fst :: (a, b) -> a
  map :: (a -> b) -> [a] -> [b]
  ```
- **Question generators:**
  - "Give the most general type" (with type variables)
  - "Is this function more polymorphic than its signature suggests?"
  - "Define a polymorphic function with the same shape as `map` for trees"
  - "Why must `f :: a -> a` be a bounded set of functions" (parametricity)
- **Common mistakes:**
  - Specialising to `Int` when the body never inspects the value
  - Confusing parametric polymorphism with ad-hoc polymorphism (typeclasses)
  - Adding a redundant `Show a =>` constraint
- **Related archetypes:** A09, A03
- **Search keywords:** polymorphic, type variable, parametric, generic, forall

## list-recursion

- **Lecture file:** `recursive_functions.md` (week 3)
- **Course week:** 3
- **Exam probability:** ⭐⭐⭐⭐⭐
- **Dependencies:** pattern-matching, types
- **Related concepts:** accumulators, folds, higher-order-functions, list-comprehensions
- **Typical type signatures:**
  ```haskell
  myLength :: [a] -> Int
  myMap    :: (a -> b) -> [a] -> [b]
  zipWith' :: (a -> b -> c) -> [a] -> [b] -> [c]
  ```
- **Question generators:**
  - "Reimplement `<Prelude function>` without using the library"
  - "Write a recursive function that returns a *summary* (Int / Bool) of a list"
  - "Multiple recursion: two list arguments, base case on each"
  - "Recurse over `[[a]]` (rows of a matrix)"
- **Common mistakes:**
  - Missing the empty-list base case
  - Forgetting `(x:xs)` destructure and using `x:[]`
  - Stack overflow from non-tail recursion on long lists (when expected to use an accumulator)
- **Related archetypes:** A09, A04, A10
- **Search keywords:** recursion, [], (x:xs), base case, prelude, structural

## accumulators

- **Lecture file:** `recursive_functions.md` and `Data1.md#an-aside-on-accumulators`
- **Course week:** 3
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** list-recursion
- **Related concepts:** folds (`foldl`), tail recursion, fastReverse
- **Typical type signatures:**
  ```haskell
  reverse'   :: [a] -> [a]
  reverse''  :: [a] -> [a] -> [a]   -- helper carrying acc
  toInt      :: String -> Int
  ```
- **Question generators:**
  - "Write an O(n) reverse using an accumulator helper"
  - "Convert a digits list to a number left-to-right with an accumulator"
  - "Spot why this `O(n^2)` becomes `O(n)` with an accumulator"
- **Common mistakes:**
  - Returning the accumulator without reversing when traversal direction matters
  - Initialising the accumulator with `undefined` instead of identity element
  - Forgetting to thread acc through both branches of a recursion
- **Related archetypes:** A09, A10
- **Search keywords:** accumulator, acc, fastReverse, tail recursion, helper

## list-comprehensions

- **Lecture file:** `list_comprehensions.md` (week 4)
- **Course week:** 4
- **Exam probability:** ⭐⭐⭐⭐
- **Dependencies:** list-recursion, guards
- **Related concepts:** string-char (Caesar runs through these), List-monad
- **Typical type signatures:**
  ```haskell
  pyths     :: Int -> [(Int, Int, Int)]
  positions :: Eq a => a -> [a] -> [Int]
  scalar    :: Num a => [a] -> [a] -> a
  ```
- **Question generators:**
  - "Write `f :: ... -> [(Int,Int,Int)]` that lists triples with a predicate"
  - "Use `zip [0..]` then comprehension to extract positions / pairs"
  - "Caesar-cipher style: comprehension over a string with a transformation"
  - "Dependent generator: inner generator uses outer bound"
- **Common mistakes:**
  - Using `,` between generator and guard (should be `,` everywhere but reading as `and`)
  - Forgetting that later generators *can* depend on earlier ones (use it!)
  - Confusing `[x | x <- xs, p x]` with `filter p xs` — same result but examiner may demand the comprehension form
- **Related archetypes:** A21, A09, A04
- **Search keywords:** comprehension, <-, generator, guard, qualifier, pyth, perfect, caesar

## higher-order-functions

- **Lecture file:** `higher-order_functions.md` (week 5)
- **Course week:** 5
- **Exam probability:** ⭐⭐⭐⭐⭐
- **Dependencies:** polymorphism, list-recursion
- **Related concepts:** folds, lambdas, function-composition, currying, Functor
- **Typical type signatures:**
  ```haskell
  map    :: (a -> b) -> [a] -> [b]
  filter :: (a -> Bool) -> [a] -> [a]
  twice  :: (a -> a) -> a -> a
  ```
- **Question generators:**
  - "Write `f` so that `f g xs` applies `g` in some non-trivial way"
  - "Define using only `map`, `filter`, `foldr` — no explicit recursion"
  - "Take a function-as-argument and an ADT, transform"
  - "Compose two unrelated functions into one"
- **Common mistakes:**
  - Returning a function when a value was wanted (forgot to apply final arg)
  - Wrong type for the function arg: `(a -> Bool)` vs `(a -> a)` vs `(a -> b -> a)`
  - Using `map` where a `foldr` is needed (because result type isn't `[b]`)
- **Related archetypes:** A03, A10, A09, A06
- **Search keywords:** higher-order, HOF, (a -> b), function argument, apply

## folds

- **Lecture file:** `higher-order_functions.md#the-foldr-function`
- **Course week:** 5
- **Exam probability:** ⭐⭐⭐⭐
- **Dependencies:** higher-order-functions, list-recursion
- **Related concepts:** accumulators (`foldl`), Foldable typeclass
- **Typical type signatures:**
  ```haskell
  foldr :: (a -> b -> b) -> b -> [a] -> b
  foldl :: (b -> a -> b) -> b -> [a] -> b
  sumWithFoldr   :: Num a => [a] -> a
  mapWithFoldr   :: (a -> b) -> [a] -> [b]
  ```
- **Question generators:**
  - "Reformulate `map`/`filter`/`length`/`reverse` using only `foldr`"
  - "Express this recursive function as a single `foldr` call"
  - "Choose `foldr` vs `foldl` and justify"
  - "Foldr on a non-list ADT (binary tree)" — gateway to Foldable
- **Common mistakes:**
  - Swapping argument order in the lambda: `\acc x ->` vs `\x acc ->`
  - Using `foldl` on infinite/long lists (strictness)
  - Wrong base/identity element (e.g. `0` for `product`)
- **Related archetypes:** A10, A09
- **Search keywords:** fold, foldr, foldl, reduce, catamorphism, identity element

## currying

- **Lecture file:** `types.md#curried-functions` and `functions.md`
- **Course week:** 1–2
- **Exam probability:** ⭐⭐
- **Dependencies:** types, higher-order-functions
- **Related concepts:** sections, lambdas, function-composition
- **Typical type signatures:**
  ```haskell
  add   :: Int -> Int -> Int
  add'  :: (Int, Int) -> Int
  curry   :: ((a, b) -> c) -> a -> b -> c
  uncurry :: (a -> b -> c) -> (a, b) -> c
  ```
- **Question generators:**
  - "Curry / uncurry this signature"
  - "Why does `add 3 4` parse as `(add 3) 4`?"
  - "Use partial application to build a specialised function"
- **Common mistakes:**
  - Treating `Int -> Int -> Int` as taking a pair
  - Parenthesising wrongly: `(a -> b) -> c` vs `a -> (b -> c)`
- **Related archetypes:** none directly — supports A03, A06
- **Search keywords:** curry, partial application, section, ->

## lambdas

- **Lecture file:** `functions.md#lambda-expressions`
- **Course week:** 2
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** higher-order-functions
- **Related concepts:** currying, function-composition
- **Typical type signatures:**
  ```haskell
  (\x -> x + 1)        :: Num a => a -> a
  (\x y -> x)          :: a -> b -> a
  ```
- **Question generators:**
  - "Rewrite this named helper as a lambda inside a `foldr`"
  - "Give the type of `\f -> f . f`"
  - "Capture-avoiding: which variables are free?"
- **Common mistakes:**
  - Forgetting `\` at the start
  - Confusing `\x -> y -> ...` (one arg returning a fn) with `\x y -> ...`
- **Related archetypes:** A10, A03
- **Search keywords:** lambda, \, anonymous function

## function-composition

- **Lecture file:** `higher-order_functions.md#the-composition-operator` and `functions.md`
- **Course week:** 2 / 5
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** higher-order-functions, currying
- **Related concepts:** folds, point-free style
- **Typical type signatures:**
  ```haskell
  (.) :: (b -> c) -> (a -> b) -> a -> c
  compose' :: [a -> a] -> (a -> a)
  ```
- **Question generators:**
  - "Compose a list of unary functions into one"
  - "Rewrite this lambda in point-free style using `.`"
  - "Express `bstSort = flattenInOrder . fromList`"
- **Common mistakes:**
  - Order: `(f . g) x = f (g x)`, not `g (f x)`
  - Trying to compose binary functions without partial application
- **Related archetypes:** A10
- **Search keywords:** compose, ., point-free, pipeline

## string-char

- **Lecture file:** `list_comprehensions.md#extended-programming-example---the-caesar-cipher`
- **Course week:** 4
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** list-comprehensions, list-recursion
- **Related concepts:** Data.Char (`ord`, `chr`, `toUpper`, `isLower`), folds
- **Typical type signatures:**
  ```haskell
  shift  :: Int -> Char -> Char
  encode :: Int -> String -> String
  crack  :: String -> String
  letterFreqs :: String -> [(Char, Int)]
  ```
- **Question generators:**
  - "Caesar-encode / decode" (problem sheet week 5)
  - "Letter-frequency table over a string"
  - "Stringy `phoneToString` / `stringToPhone` (T9-style)"
  - "Predicate on `Char` filters / counts a string"
- **Common mistakes:**
  - Shifting non-letters (must pass through unchanged)
  - Wrapping past `'Z'` / `'z'` with wrong modulus (26, not 25)
  - Mixing `Char` and `Int` arithmetic without `ord`/`chr`
- **Related archetypes:** A07 (codec), A09, A21
- **Search keywords:** Caesar, cipher, shift, ord, chr, isLower, freq, T9

## custom-ADTs

- **Lecture file:** `Data1.md#user-defined-data-types`
- **Course week:** 6
- **Exam probability:** ⭐⭐⭐⭐⭐
- **Dependencies:** pattern-matching, types
- **Related concepts:** deriving, typeclasses-basic, binary-trees, expression-trees, Maybe, Either
- **Typical type signatures:**
  ```haskell
  data Shape   = Circle Double | Rectangle Double Double | Triangle Double Double Double
  data Maybe a = Nothing | Just a
  data BT a    = Empty | Fork a (BT a) (BT a)
  ```
- **Question generators:**
  - "Define an ADT for X, then write `f :: T -> ...`"
  - "Translate an English description into a data declaration with constructor names"
  - "Add a new constructor and update all consumers" (interpreter extension)
  - "Define a `newtype` wrapper with a derived `Eq` / `Show`"
- **Common mistakes:**
  - Constructor names not starting with a capital letter
  - Using `=` instead of `|` between constructors
  - Forgetting recursion in the type (`Fork a (BT a) (BT a)` — must reference itself)
  - Confusing type parameter position: `BT a` vs `BT Int`
- **Related archetypes:** A01, A05, A11, A22
- **Search keywords:** data, ADT, constructor, |, newtype, deriving

## deriving

- **Lecture file:** `Data1.md` and `typeclasses.md`
- **Course week:** 6 / 4
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** custom-ADTs, typeclasses-basic
- **Related concepts:** Eq, Ord, Show, Enum, Bounded, Functor (with `DeriveFunctor`)
- **Typical type signatures:**
  ```haskell
  data WeekDay = Mon | Tue | Wed | Thu | Fri | Sat | Sun
    deriving (Eq, Ord, Show, Enum, Bounded)
  ```
- **Question generators:**
  - "Which typeclasses can be derived for this ADT, and what does each give?"
  - "Why does `deriving Ord` give the comparison order it does?"
  - "Why can't you `deriving Functor` without `{-# LANGUAGE DeriveFunctor #-}`?"
- **Common mistakes:**
  - Deriving `Show` then writing a manual `instance Show` — conflicts
  - Assuming `deriving Eq` gives structural equality up to permutation (it doesn't — order matters)
  - Forgetting `Safe` interacts with `GeneralizedNewtypeDeriving` (assignments use `-XNoGeneralizedNewtypeDeriving`)
- **Related archetypes:** A22
- **Search keywords:** deriving, Eq, Ord, Show, Enum, Bounded, automatic instance

## typeclasses-basic

- **Lecture file:** `typeclasses.md` and `more-typeclasses.md`
- **Course week:** 4
- **Exam probability:** ⭐⭐⭐⭐
- **Dependencies:** polymorphism, custom-ADTs
- **Related concepts:** Eq, Ord, Show, Num, Functor, Applicative, Monad
- **Typical type signatures:**
  ```haskell
  class MyEq a where
    (===) :: a -> a -> Bool
  instance MyEq Bool where ...
  instance (MyEq a, MyEq b) => MyEq (a, b) where ...
  ```
- **Question generators:**
  - "Define a new class with one method, give 2-3 instances"
  - "Give a recursive instance: `(MyEq a) => MyEq [a]`"
  - "Add `[()]` (or another type) to `Num`"
  - "Inheritance: extend `Eq` with `Ord`"
- **Common mistakes:**
  - Method body in `class` instead of `instance`
  - Forgetting context constraint when instance recurses (`MyEq a =>`)
  - Overlapping instances when both `instance C Int` and `instance C a` exist
- **Related archetypes:** A22, A09
- **Search keywords:** class, instance, =>, dictionary, ad-hoc polymorphism

## Functor

- **Lecture file:** `monads.md` (intro) and `Data2.md`
- **Course week:** 7 / 9
- **Exam probability:** ⭐⭐⭐⭐⭐
- **Dependencies:** typeclasses-basic, custom-ADTs, higher-order-functions
- **Related concepts:** Applicative, Monad, mapBT, deriving (DeriveFunctor)
- **Typical type signatures:**
  ```haskell
  class Functor f where
    fmap :: (a -> b) -> f a -> f b
  instance Functor BT where ...
  instance Functor (Either e) where ...
  ```
- **Question generators:**
  - "Write `Functor` for this ADT" (Maybe, Rose, BT, custom container)
  - "Verify the two Functor laws by structural induction"
  - "Combine `fmap` with `(<$>)` to transform inside a Maybe / IO"
  - "Why does `Either a` (left-fixed) have a Functor but `(,) a` swaps?"
- **Common mistakes:**
  - Mapping over the wrong type parameter (e.g. left of `Either` instead of right)
  - Not preserving structure: `fmap f Empty = Empty` (not `Fork ...`)
  - Re-deriving the Functor laws incorrectly (identity, composition)
- **Related archetypes:** A06, A22, A20
- **Search keywords:** Functor, fmap, <$>, container, identity law, composition law

## Applicative

- **Lecture file:** `monads.md` (intro / parsing) and `even-more-typeclasses.md`
- **Course week:** 9 / 10
- **Exam probability:** ⭐⭐⭐⭐
- **Dependencies:** Functor
- **Related concepts:** Monad, Alternative, parser combinators, liftA2
- **Typical type signatures:**
  ```haskell
  class Functor f => Applicative f where
    pure  :: a -> f a
    (<*>) :: f (a -> b) -> f a -> f b
  liftA2' :: Applicative f => (a -> b -> c) -> f a -> f b -> f c
  ```
- **Question generators:**
  - "Write the `Applicative` instance for a given Functor"
  - "Reimplement `liftA2`, `sequenceA` without `Monad`"
  - "Why does the parser type need Applicative *before* you can use `<*>`?"
  - "Express a computation as `f <$> ma <*> mb <*> mc`"
- **Common mistakes:**
  - Defining `pure = id` or `pure = return` confusingly
  - Wrong `<*>`: must run effect of the function-side, then the value-side
  - Using `Applicative` where `Monad` is actually needed (data-dependent control flow)
- **Related archetypes:** A24, A06, A16
- **Search keywords:** Applicative, pure, <*>, ap, liftA2, applicative-style

## Monad

- **Lecture file:** `monads.md` (whole file)
- **Course week:** 9
- **Exam probability:** ⭐⭐⭐⭐⭐
- **Dependencies:** Functor, Applicative, typeclasses-basic
- **Related concepts:** Maybe, Either, State, Writer, IO, List-monad, MonadError, do-notation
- **Typical type signatures:**
  ```haskell
  class Applicative m => Monad m where
    return :: a -> m a
    (>>=)  :: m a -> (a -> m b) -> m b
  instance Monad MyMaybe where ...
  join'    :: Monad m => m (m a) -> m a
  sequenceM :: Monad m => [m a] -> m [a]
  ```
- **Question generators:**
  - "Write `Monad` instance for X"
  - "Generic `Monad m =>` combinator: `applyNTimes`, `whileM`, `sequenceM`"
  - "Translate this `do` block into `>>=` form"
  - "Why do we need Monad and not just Applicative for X?"
- **Common mistakes:**
  - Returning `Just x` directly in a `do` block instead of `pure x` / `return x`
  - Confusing `>>` (discard) with `>>=`
  - Trying to escape a monad (`m a -> a`) without `runState` / `runReader`
  - Writing `do { x <- ma; ma; ... }` and using stale `x` (forgot to bind)
- **Related archetypes:** A03, A06, A02, A14, A15, A20
- **Search keywords:** Monad, >>=, return, pure, do, bind, join

## Foldable

- **Lecture file:** `even-more-typeclasses.md` and `Data1.md`
- **Course week:** 6–7
- **Exam probability:** ⭐⭐
- **Dependencies:** Functor, custom-ADTs
- **Related concepts:** Traversable, folds
- **Typical type signatures:**
  ```haskell
  class Foldable t where
    foldr :: (a -> b -> b) -> b -> t a -> b
  instance Foldable BT where ...
  ```
- **Question generators:**
  - "Define `Foldable` for this ADT" (BT, Rose)
  - "Use `foldMap` to derive sum / count from the foldable"
  - "Why does Foldable not require Functor in modern Haskell?"
- **Common mistakes:**
  - Not visiting all subtrees (incomplete recursion)
  - Wrong base value for `foldr` (using `0` instead of identity for the monoid)
- **Related archetypes:** A01, A10
- **Search keywords:** Foldable, foldr, foldMap, sum, traverse

## Traversable

- **Lecture file:** `monads.md` (mapM section) and `even-more-typeclasses.md`
- **Course week:** 9
- **Exam probability:** ⭐⭐
- **Dependencies:** Functor, Foldable, Monad/Applicative
- **Related concepts:** mapM, sequence, mapMTree
- **Typical type signatures:**
  ```haskell
  class (Functor t, Foldable t) => Traversable t where
    traverse :: Applicative f => (a -> f b) -> t a -> f (t b)
  mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)
  ```
- **Question generators:**
  - "Write `mapM`-like over a binary / rose tree"
  - "Sequence a `BT (Maybe a)` to `Maybe (BT a)`"
  - "Define `traverse` for an ADT"
- **Common mistakes:**
  - Confusing `traverse` (returns `f (t b)`) with `fmap` (returns `t b`)
  - Forgetting `<*>` for the recursive branches
- **Related archetypes:** A03, A06
- **Search keywords:** Traversable, traverse, sequence, mapM

## Alternative

- **Lecture file:** `monads.md` (parser section)
- **Course week:** 10
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** Applicative
- **Related concepts:** parser-combinators, Maybe-as-fail, list-as-many-results
- **Typical type signatures:**
  ```haskell
  class Applicative f => Alternative f where
    empty :: f a
    (<|>) :: f a -> f a -> f a
  some  :: Alternative f => f a -> f [a]
  many  :: Alternative f => f a -> f [a]
  ```
- **Question generators:**
  - "Write `Alternative` for `Parser`"
  - "Use `<|>` to choose between two parser branches"
  - "Why does `some` not loop on `pure x`?"
- **Common mistakes:**
  - Defining `empty = error "..."` instead of an actual failure
  - `<|>` left-biased — beware of giving the wrong branch precedence
- **Related archetypes:** A16, A24
- **Search keywords:** Alternative, <|>, empty, some, many, choice

## Eq-Ord

- **Lecture file:** `typeclasses.md` and `more-typeclasses.md`
- **Course week:** 4
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** typeclasses-basic
- **Related concepts:** deriving, BST (uses Ord)
- **Typical type signatures:**
  ```haskell
  (==)    :: Eq a => a -> a -> Bool
  compare :: Ord a => a -> a -> Ordering
  ```
- **Question generators:**
  - "Write `instance Ord T` that orders by some field"
  - "Why does `Ord` extend `Eq`?"
  - "Implement `quicksort` using only `Ord`"
- **Common mistakes:**
  - Manual `Ord` instance that doesn't satisfy transitivity
  - Forgetting `Eq` superclass when writing `Ord` manually
- **Related archetypes:** A22, A11
- **Search keywords:** Eq, Ord, compare, Ordering, <, <=

## Show

- **Lecture file:** `typeclasses.md` and `Data2.md` (expression-trees)
- **Course week:** 4 / 7
- **Exam probability:** ⭐⭐⭐⭐
- **Dependencies:** typeclasses-basic, custom-ADTs
- **Related concepts:** Read (rarely asked), pretty-printing
- **Typical type signatures:**
  ```haskell
  class Show a where
    show :: a -> String
  instance Show NumExpr where ...
  instance Show GridWithAPointer where ...   -- Assignment 1
  ```
- **Question generators:**
  - "Write a custom `Show` for an expression tree with operator precedence"
  - "Pretty-print a grid / table with column padding"
  - "Pretty-print using ANSI escape codes for highlighting"
  - "Show a `Color = Custom Int Int Int` as `#0C2238`"
- **Common mistakes:**
  - Always parenthesising (the precedence challenge — see Week 7 sheet)
  - Forgetting to handle the recursive constructors
  - Showing internal newlines without `unlines`
- **Related archetypes:** A13, A22
- **Search keywords:** Show, show, pretty, precedence, ANSI, escape

## Num

- **Lecture file:** `more-typeclasses.md#the-type-class-num` and `even-more-typeclasses.md`
- **Course week:** 4
- **Exam probability:** ⭐⭐
- **Dependencies:** typeclasses-basic
- **Related concepts:** expression-trees (NumExpr), `fromInteger`
- **Typical type signatures:**
  ```haskell
  class Num a where
    (+), (-), (*) :: a -> a -> a
    negate, abs, signum :: a -> a
    fromInteger :: Integer -> a
  ```
- **Question generators:**
  - "Add `[()]` (unary natural numbers) to `Num`"
  - "Define `Num NumExpr` so that arithmetic literals construct expressions"
  - "Why does `1 + 2 :: Vec3` need a `Num Vec3` instance?"
- **Common mistakes:**
  - Forgetting `fromInteger` — numeric literals fail to type-check
  - Treating `signum` as `Int -> Int` only (it's `a -> a`)
- **Related archetypes:** A22, A13
- **Search keywords:** Num, fromInteger, +, *, numeric literal

## Maybe

- **Lecture file:** `Data1.md#the-maybe-type-constructor` and `monads.md`
- **Course week:** 6 / 9
- **Exam probability:** ⭐⭐⭐⭐⭐
- **Dependencies:** custom-ADTs, pattern-matching
- **Related concepts:** Monad, Either, safeDiv, lookup, BST
- **Typical type signatures:**
  ```haskell
  data Maybe a = Nothing | Just a
  safeDiv  :: Int -> Int -> Maybe Int
  safeHead :: [a] -> Maybe a
  lookup   :: Eq a => a -> [(a, b)] -> Maybe b
  ```
- **Question generators:**
  - "Wrap a partial function as total with `Maybe`"
  - "Chain `Maybe` computations with `do` / `>>=`"
  - "Catch `Nothing` and provide a default with `fromMaybe`"
  - "Reimplement `catMaybes`, `mapMaybe`"
- **Common mistakes:**
  - Pattern matching `Just x` and forgetting the `Nothing` case
  - Using `fromJust` (partial) — never in safe code
  - Mixing `Maybe` and `Either` semantics
- **Related archetypes:** A03, A09, A06, A11
- **Search keywords:** Maybe, Just, Nothing, safe, fromMaybe, catMaybes

## Either

- **Lecture file:** `Data1.md#the-either-type-constructor`
- **Course week:** 6
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** custom-ADTs, Maybe
- **Related concepts:** Monad, MonadError
- **Typical type signatures:**
  ```haskell
  data Either a b = Left a | Right b
  zipEither :: [a] -> [b] -> Either String [(a, b)]
  eval      :: MonadError String m => CalcExpr -> m Int
  ```
- **Question generators:**
  - "Like Maybe but carry an error message"
  - "Write `Functor / Applicative / Monad` for `Either e`"
  - "Use `Left` as the failure branch in a parser"
- **Common mistakes:**
  - Forgetting Functor / Monad on `Either e` is right-biased
  - Returning `Left "..."` everywhere — defeats the type
- **Related archetypes:** A06, A09, A14
- **Search keywords:** Either, Left, Right, error, biased

## IO

- **Lecture file:** `IOPrime.md`
- **Course week:** 9–10
- **Exam probability:** ⭐⭐
- **Dependencies:** Monad
- **Related concepts:** State (analogously side-effectful), `interact`, `readLn`
- **Typical type signatures:**
  ```haskell
  greet     :: IO ()
  threeNumbers :: IO [Int]
  echoUntilQuit :: IO ()
  ```
- **Question generators:**
  - "Read N inputs and produce output" (mostly problem-sheet only)
  - "Use `mapM_ print` to display a list"
  - "Mock the IO monad with `IO'` data type (lecture notes)"
- **Common mistakes:**
  - Forgetting that `getLine :: IO String`, not `String`
  - Using `print` where `putStrLn` is wanted (extra quotes)
  - QuickCheck doesn't test IO directly — exam-unlikely as a graded 10-marker
- **Related archetypes:** A03 (only via generic `Monad m`)
- **Search keywords:** IO, getLine, putStrLn, readLn, mapM_, interact

## State

- **Lecture file:** `monads.md#using-the-state-monad-to-get-another-algorithm-for-the-fibonacci-function`
- **Course week:** 9
- **Exam probability:** ⭐⭐⭐⭐⭐
- **Dependencies:** Monad
- **Related concepts:** Writer, Reader, do-notation, mini-game pattern
- **Typical type signatures:**
  ```haskell
  type State s a = ...    -- from Control.Monad.State
  get    :: State s s
  put    :: s -> State s ()
  modify :: (s -> s) -> State s ()
  runState :: State s a -> s -> (a, s)
  ```
- **Question generators:**
  - "Implement a mini-game (Nim, calculator, stack) in `State`"
  - "Label a tree in-order with a fresh counter (`State Int`)"
  - "Convert imperative Java/while-loop into State"
  - "Run `n` steps of Fibonacci with state `(prev, curr)`"
- **Common mistakes:**
  - Returning a stateful action instead of running it (forgot `runState`/`execState`/`evalState`)
  - `get` then `put (modified)` instead of `modify`
  - Using `State` when `Reader` is enough (state never written)
- **Related archetypes:** A02, A03, A23, A14
- **Search keywords:** State, get, put, modify, runState, execState, evalState

## Writer

- **Lecture file:** `monads.md#producing-a-log-of-the-computation-with-the-writer-monad`
- **Course week:** 9
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** Monad, typeclasses-basic (Monoid)
- **Related concepts:** State, Foldable
- **Typical type signatures:**
  ```haskell
  type Writer w a = ...     -- requires Monoid w
  tell :: w -> Writer w ()
  logFactorial :: Int -> Writer [String] Int
  countSteps   :: Int -> Writer (Sum Int) Int
  ```
- **Question generators:**
  - "Log every recursive call with `tell`"
  - "Compute X while accumulating a `Sum Int` counter"
  - "Use `[String]` as the writer log of trace messages"
- **Common mistakes:**
  - Forgetting `Monoid w` constraint
  - Using `tell s` where `s` is not a monoid (raw `Int` instead of `Sum Int`)
  - Discarding the log when running (`fst (runWriter ...)` drops it)
- **Related archetypes:** A15, A14
- **Search keywords:** Writer, tell, Sum, Monoid, log, trace

## Reader

- **Lecture file:** `monads.md` (mentioned; deeper in Assignment 3 / problem sheet 13)
- **Course week:** 9–10
- **Exam probability:** ⭐⭐
- **Dependencies:** Monad
- **Related concepts:** State, env-evaluator
- **Typical type signatures:**
  ```haskell
  newtype Reader r a = Reader { runReader :: r -> a }
  ask    :: Reader r r
  local  :: (r -> r) -> Reader r a -> Reader r a
  ```
- **Question generators:**
  - "Define your own `Reader` (Functor / Applicative / Monad)"
  - "Pass an environment through nested expression evaluation"
  - "When does `Reader` suffice vs needing `State`?"
- **Common mistakes:**
  - Re-implementing `ask` as `pure r` (wrong)
  - Updating the env mutably — should use `local`
- **Related archetypes:** A06, A08
- **Search keywords:** Reader, ask, local, environment, runReader

## List-monad

- **Lecture file:** `monads.md#example-the-list-monad`
- **Course week:** 9
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** Monad, list-comprehensions
- **Related concepts:** Alternative, do-notation, knightMoves
- **Typical type signatures:**
  ```haskell
  knightMoves :: (Int, Int) -> [(Int, Int)]
  allPairs    :: [a] -> [(a, a)]
  -- equivalent to a list comprehension
  ```
- **Question generators:**
  - "Write knight moves using list-`do`"
  - "Cartesian product / all pairs via list monad"
  - "Why does `[1,2,3] >>= \x -> [x, x*10]` produce `[1,10,2,20,3,30]`?"
- **Common mistakes:**
  - Using `do` over lists when a comprehension is clearer (or vice versa) — examiner may want a specific form
  - Returning `[x]` from inner action when `x` was meant
- **Related archetypes:** A21, A03
- **Search keywords:** list monad, [], non-determinism, do, knight, pairs

## MonadError

- **Lecture file:** Problem sheet week 9 (calculator), `monads.md`
- **Course week:** 9
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** Monad, Either
- **Related concepts:** interpreter-with-error, monad-transformers
- **Typical type signatures:**
  ```haskell
  class Monad m => MonadError e m where
    throwError :: e -> m a
    catchError :: m a -> (e -> m a) -> m a
  eval :: MonadError String m => CalcExpr -> m Int
  ```
- **Question generators:**
  - "Calculator with divide-by-zero throws a `String` error"
  - "Look up a variable in env, throw if undefined"
  - "Generic eval over any `MonadError String m`"
- **Common mistakes:**
  - Specialising to `Either String` early — examiner wants the abstraction
  - Forgetting that `MonadError` requires `Monad` superclass
  - Throwing the wrong error type (must match the parameter `e`)
- **Related archetypes:** A14, A08
- **Search keywords:** MonadError, throwError, catchError, exception, divide by zero

## monad-transformers

- **Lecture file:** `monads.md` (touched) and Assignment 3 `Free`
- **Course week:** 10
- **Exam probability:** ⭐⭐
- **Dependencies:** Monad, Reader, State, Writer
- **Related concepts:** Free monad, multi-effect, `lift`
- **Typical type signatures:**
  ```haskell
  newtype StateT s m a = StateT { runStateT :: s -> m (a, s) }
  lift :: Monad m => m a -> t m a
  ```
- **Question generators:**
  - "Combine State and Writer in one stack"
  - "Lift an inner monadic action"
  - "Why is the order of transformers significant?"
- **Common mistakes:**
  - Mis-stacking — `StateT s (Either e)` vs `ExceptT e (State s)` give different semantics
  - Forgetting `lift` when calling an inner-layer action
- **Related archetypes:** A14, A03
- **Search keywords:** transformer, StateT, lift, monad stack

## multi-effect

- **Lecture file:** `monads.md` and Assignment 3 (`Free (FSum (State s) Yield)`)
- **Course week:** 10
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** Monad, State, monad-transformers
- **Related concepts:** Free monad, interpreter-imperative-storage, schedulers
- **Typical type signatures:**
  ```haskell
  type YieldState s a = Free (FSum (State s) Yield) a
  trace      :: FreeState s a -> State ([s], s) a
  roundRobin :: [YieldState s ()] -> State s ()
  schedule   :: [SleepState s ()] -> State s ()
  ```
- **Question generators:**
  - "Implement round-robin scheduling over a list of `Free` programs"
  - "Trace every intermediate state of a stateful computation"
  - "Combine yield + state with `FSum` and a `Free` monad"
- **Common mistakes:**
  - Failing to recurse on `Free` constructor (drops sub-computation)
  - Wrong order of effects when sleep counters and state interleave
  - Treating `Yield ()` as `pure ()` (it isn't — it's a constructor)
- **Related archetypes:** A14, A02, A23
- **Search keywords:** multi-effect, Free, FSum, yield, schedule, round-robin

## expression-trees

- **Lecture file:** `Data2.md#expression-trees` and ProblemSheet-Week7
- **Course week:** 7
- **Exam probability:** ⭐⭐⭐⭐⭐
- **Dependencies:** custom-ADTs, pattern-matching, Show
- **Related concepts:** interpreter-arith, interpreter-with-env, Num, A05
- **Typical type signatures:**
  ```haskell
  data Expr = Val Int | Add Expr Expr | Mul Expr Expr | Sub Expr Expr | Neg Expr
  evalExpr   :: Expr -> Int
  depthExpr  :: Expr -> Int
  data Expr  = Var Char | Not Expr | And Expr Expr | Or Expr Expr | Implies Expr Expr
  circuit    :: Expr -> Circuit             -- Mock Q5
  ```
- **Question generators:**
  - "Evaluate an arithmetic / logical expression tree"
  - "Translate an `Expr` into a different ADT" (mock Q5: Expr→Circuit)
  - "Pretty-print with operator precedence"
  - "Compute depth / size / variable-set of an expression"
- **Common mistakes:**
  - Missing a constructor case (warn-incomplete-patterns)
  - Wrong precedence in pretty-print
  - Forgetting to recurse on both `e1` and `e2` for binary constructors
- **Related archetypes:** A05, A13, A19, A08
- **Search keywords:** Expr, Add, Mul, evalExpr, NumExpr, circuit, Nand

## BST

- **Lecture file:** `Data2.md#binary-search-trees`
- **Course week:** 6
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** binary-trees, Eq-Ord
- **Related concepts:** BST sort, Maybe (`delete`), in-order traversal
- **Typical type signatures:**
  ```haskell
  isBST     :: Ord a => BT a -> Bool
  insertBST :: Ord a => a -> BT a -> BT a
  memberBST :: Ord a => a -> BT a -> Bool
  deleteBST :: Ord a => a -> BT a -> BT a
  fromList  :: Ord a => [a] -> BT a
  ```
- **Question generators:**
  - "Check BST invariant" (often "linear time, without flattening")
  - "Insert preserving BST invariant"
  - "Delete with replacement by largest-of-left-subtree"
  - "Combine `largestOf` + `withoutLargest` into one function returning a pair"
- **Common mistakes:**
  - `isBST` that only checks immediate child — needs upper/lower bound propagation
  - Inserting equal element twice (BST usually deduplicates)
  - Returning a non-BST after delete (wrong replacement)
- **Related archetypes:** A11, A01
- **Search keywords:** BST, isBST, insert, delete, member, Ord

## rose-trees

- **Lecture file:** `Data2.md#rose-trees` and Assignment 3
- **Course week:** 6 / 10
- **Exam probability:** ⭐⭐⭐⭐⭐
- **Dependencies:** custom-ADTs, list-recursion
- **Related concepts:** binary-trees, Free (`Free [] a`), Mock Q1
- **Typical type signatures:**
  ```haskell
  data Rose a = Branch a [Rose a]               -- Data2 form (always-value)
  data Rose a = Leaf a | Branch [Rose a]        -- MockTest / Assignment 3 form (value at leaves)
  sizeRose    :: Rose a -> Int
  heightRose  :: Rose a -> Int
  flattenRose :: Rose a -> [a]
  isNBranching :: Int -> Rose a -> Bool         -- MockTest Q1
  prune       :: Int -> Rose a -> Rose a        -- MockTest Q1
  toRose      :: Free [] a -> Rose a            -- Assignment 3 Task 1
  fromRose    :: Rose a -> Free [] a
  ```
- **Question generators:**
  - "Predicate on every branch / leaf"
  - "Bounded transformation (`prune n`)"
  - "Address-based lookup (Problem Sheet 6: `validAddresses`, `getAtAddress`)"
  - "Iso / retract between Rose and Free []"
- **Common mistakes:**
  - **Crucial**: examiner mutates between the two Rose definitions (`Branch a [Rose a]` vs `Leaf a | Branch [Rose a]`). Read the question!
  - Treating `Branch []` as a leaf (it isn't, in the always-value variant)
  - Forgetting `map (prune n) forest` recursion in `prune`
- **Related archetypes:** A01, A05, A20
- **Search keywords:** Rose, Branch, Leaf, prune, isNBranching, forest, n-ary

## binary-trees

- **Lecture file:** `Data1.md#binary-trees`
- **Course week:** 6
- **Exam probability:** ⭐⭐⭐⭐⭐
- **Dependencies:** custom-ADTs, pattern-matching, list-recursion
- **Related concepts:** BST, traversals, Functor BT, mapM BT, expression-trees
- **Typical type signatures:**
  ```haskell
  data BT a = Empty | Fork a (BT a) (BT a)
  sizeBT       :: BT a -> Int
  heightBT     :: BT a -> Int
  flattenInOrder :: BT a -> [a]
  mirror       :: BT a -> BT a
  mapBT        :: (a -> b) -> BT a -> BT b
  countBT      :: Eq a => a -> BT a -> Int
  ```
- **Question generators:**
  - "Count something derived from a predicate over a `BT`"
  - "Define one of the three traversal orders"
  - "Mirror / map / fmap"
  - "Count occurrences satisfying a predicate at leaves / forks"
  - "Define `Functor` / `Foldable` for `BT`"
- **Common mistakes:**
  - `heightBT Empty == 0` vs `== -1` — read the spec
  - "Leaves" defined as `Fork _ Empty Empty` not as `Leaf` constructor (no `Leaf` here!)
  - Forgetting to recurse on both subtrees
- **Related archetypes:** A01, A06, A11, A20
- **Search keywords:** BT, Fork, Empty, tree, traverse, mirror, height

## interpreter-arith

- **Lecture file:** `Data2.md#expression-trees` and PS Week 7
- **Course week:** 7
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** expression-trees, pattern-matching
- **Related concepts:** interpreter-with-env, interpreter-with-error
- **Typical type signatures:**
  ```haskell
  data Expr = Val Int | Add Expr Expr | Mul Expr Expr | ...
  evalExpr :: Expr -> Int
  ```
- **Question generators:**
  - "Pure evaluator with no side-effects"
  - "Add a new constructor (Sub, Div, Neg)"
  - "Evaluate to `Maybe Int` for partial operations"
- **Common mistakes:**
  - Treating `Div` as `Int` without `Maybe` wrap
  - Wrong operator precedence on Show
- **Related archetypes:** A08, A19
- **Search keywords:** eval, Expr, evaluator, arithmetic

## interpreter-with-env

- **Lecture file:** PS Week 7 (env exprs) and ProblemSheet-Week9 calculator
- **Course week:** 7 / 9
- **Exam probability:** ⭐⭐⭐⭐
- **Dependencies:** Maybe, expression-trees, Reader/State
- **Related concepts:** interpreter-with-error, BST, Practice problem 148
- **Typical type signatures:**
  ```haskell
  data Expr = Lit Int | Var String | Add Expr Expr | Mul Expr Expr | Let String Expr Expr
  type Env  = [(String, Int)]
  eval :: Env -> Expr -> Maybe Int
  ```
- **Question generators:**
  - "Add a `Let` binding that extends the env for the body"
  - "Lookup variable in env, `Nothing` if undefined"
  - "Add `If` with boolean predicate"
- **Common mistakes:**
  - Not extending the env before evaluating the body of `Let`
  - Shadowing — when a `Var` exists both in inner and outer scope
  - Returning `Just 0` instead of `Nothing` on missing var
- **Related archetypes:** A08, A19, A14
- **Search keywords:** env, environment, lookup, Var, Let, eval, scope

## interpreter-with-error

- **Lecture file:** `Data2.md` + PS Week 9 monadic calculator
- **Course week:** 7 / 9
- **Exam probability:** ⭐⭐⭐⭐
- **Dependencies:** MonadError, Either, expression-trees
- **Related concepts:** interpreter-with-env, interpreter-imperative-storage
- **Typical type signatures:**
  ```haskell
  data CalcExpr = Val Int | Add CalcExpr CalcExpr | Mult ... | Div ... | Sub ...
  eval :: MonadError String m => CalcExpr -> m Int
  ```
- **Question generators:**
  - "Divide-by-zero throws"
  - "Catch errors with `catchError`"
  - "Generic over any `MonadError String m`"
- **Common mistakes:**
  - Specialising to `Either String` in the body
  - Forgetting `Val` is a non-failing case (always `pure`)
- **Related archetypes:** A14, A08, A19
- **Search keywords:** MonadError, throw, division by zero, calculator

## interpreter-imperative-storage

- **Lecture file:** `LectureNotes/Sections/interpreter/` (Overview, AbstractSyntax, Interpreter)
- **Course week:** 10
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** custom-ADTs, State, expression-trees
- **Related concepts:** Parser, Runxy CLI
- **Typical type signatures:**
  ```haskell
  type Identifier = String
  type Storage    = [(Identifier, Integer)]
  data Program    = Identifier := Expr | If Expr Program Program | While Expr Program | Block [Program]
  update :: Identifier -> Integer -> Storage -> Storage
  eval   :: Storage -> Expr -> Integer
  run    :: Program -> Storage -> Storage
  ```
- **Question generators:**
  - "Add `for` / `do-while` / `if-else` to the imperative interpreter (Week 10 sheet)"
  - "Extend `Expr` with a new operator and update `eval`"
  - "Implement `while` via fixed-point recursion on storage"
- **Common mistakes:**
  - Variable not in storage — using `error` instead of returning failure
  - `while` body never updates the variable that the predicate checks → infinite loop
  - Updating storage but not threading it through subsequent statements
- **Related archetypes:** A19, A14, A08
- **Search keywords:** interpreter, imperative, Storage, while, assign, Program, Runxy

## parser-combinators

- **Lecture file:** `monads.md#monadic-parsing` and `interpreter/Parser.hs`
- **Course week:** 10
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** Functor, Applicative, Monad, Alternative
- **Related concepts:** interpreter-imperative-storage, ADT parsing
- **Typical type signatures:**
  ```haskell
  newtype Parser a = P (String -> [(a, String)])
  parse :: Parser a -> String -> [(a, String)]
  item  :: Parser Char
  sat   :: (Char -> Bool) -> Parser Char
  digitP   :: Parser Char
  parseNat  :: Parser Int
  parseExpr :: Parser Int
  ```
- **Question generators:**
  - "Define Functor / Applicative / Monad / Alternative for `Parser`"
  - "Parse arithmetic with `+ *` respecting precedence"
  - "Parse a small DSL (JSON-lite, XML-lite, bracket trees) — see Assignment 2 Ex 6"
- **Common mistakes:**
  - Forgetting `Alternative` for `<|>`
  - Parsing only the first character without consuming the rest
  - Returning multiple parses when only the first should win — left-biased `<|>`
- **Related archetypes:** A16, A24, A06
- **Search keywords:** Parser, parse, item, sat, <|>, some, many, expression grammar

## laziness

- **Lecture file:** `Laziness.md`
- **Course week:** 8
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** higher-order-functions, recursion
- **Related concepts:** infinite-data, lazy-naturals, memoisation
- **Typical type signatures:**
  ```haskell
  ones :: [Int]
  fibs :: [Integer]
  fix' :: (a -> a) -> a
  ```
- **Question generators:**
  - "Define an infinite list lazily (`ones`, `fibs`)"
  - "Use `zipWith` self-referentially for `fibs`"
  - "Memoise a function with `tstore` / `tfetch` over an infinite tree"
  - "Explain why `fix' f = let x = f x in x` works"
- **Common mistakes:**
  - Using `foldl` on infinite list (forces traversal)
  - Forgetting `seq` / strictness when actually needed
  - Mistaking memoisation gain — must store in tree, not closure
- **Related archetypes:** A18, A20
- **Search keywords:** lazy, infinite, fix, memo, tstore, tfetch, fibs

## infinite-data

- **Lecture file:** `Laziness.md`
- **Course week:** 8
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** laziness, list-recursion
- **Related concepts:** lazy-naturals, primes sieve
- **Typical type signatures:**
  ```haskell
  ones      :: [Int]
  primes    :: [Int]
  iterate'  :: (a -> a) -> a -> [a]
  ```
- **Question generators:**
  - "Sieve of Eratosthenes as an infinite stream"
  - "Take from an infinite list"
  - "Define an infinite tree of values"
- **Common mistakes:**
  - Filtering an infinite stream with a predicate that never holds — hangs
  - Returning `length xs` on infinite → bottom
- **Related archetypes:** A18
- **Search keywords:** infinite, stream, sieve, primes, iterate

## lazy-naturals

- **Lecture file:** `LazyNaturals.md`
- **Course week:** 8
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** laziness, custom-ADTs
- **Related concepts:** infinite-data
- **Typical type signatures:**
  ```haskell
  data Nat = Zero | Succ Nat deriving (Show, Eq, Ord)
  addNat   :: Nat -> Nat -> Nat
  infty    :: Nat
  lengthNat :: [a] -> Nat
  toNat    :: Int -> Nat
  ```
- **Question generators:**
  - "Define `infty = Succ infty` and explain how comparison terminates"
  - "Write `lengthNat` such that comparing with a finite bound doesn't loop"
  - "Why is `addNat infty zero = infty`?"
- **Common mistakes:**
  - Pattern matching strictly forces evaluation — `Succ n` with strict `n` defeats laziness
  - Implementing `(<=)` left-strict
- **Related archetypes:** A18, A20
- **Search keywords:** Nat, Zero, Succ, infty, lazy comparison

## conway-life

- **Lecture file:** `Life.md`
- **Course week:** 2 / 11 (week 1 motivational, returned to with `cellExpr`)
- **Exam probability:** ⭐
- **Dependencies:** list-comprehensions, pattern-matching
- **Related concepts:** tictactoe (grid representation)
- **Typical type signatures:**
  ```haskell
  type Board = [(Int, Int)]
  step  :: Board -> Board
  show' :: Board -> String
  ```
- **Question generators:**
  - "Count live neighbours of a cell"
  - "Implement one `step` of the rules"
  - "Render the board" (rare in exam)
- **Common mistakes:**
  - Counting the cell itself as its own neighbour
  - Wrong neighbour offsets (must be 8, not 4)
- **Related archetypes:** A23 (mini-game) — low exam priority
- **Search keywords:** Life, Conway, cellular automaton, neighbours, step

## tic-tac-toe

- **Lecture file:** `tictactoe.md`
- **Course week:** 11
- **Exam probability:** ⭐⭐
- **Dependencies:** game-trees, minimax, list-comprehensions
- **Related concepts:** rose-trees (game trees), Practice 150
- **Typical type signatures:**
  ```haskell
  type Grid   = [[Player]]   -- or ([Move],[Move]) in PS11
  data Player = O | B | X    -- with Ord so O < B < X
  winner   :: Grid -> Maybe Player
  bestMove :: Grid -> Player -> Grid
  ```
- **Question generators:**
  - "Detect winner on rows/columns/diagonals"
  - "Generalise to `n × n`"
  - "Score a board from a player's perspective"
  - "Modify the rules to lose-by-three-in-a-row (Week 11 variant)"
- **Common mistakes:**
  - Hard-coded `size = 3` everywhere — exam may want size-polymorphic
  - Off-by-one in diagonal indexing
  - Treating `B` (blank) as `Nothing` (mismatched representations)
- **Related archetypes:** A23, A21
- **Search keywords:** tictactoe, Grid, winner, minimax, three in a row

## rigour

- **Lecture file:** `rigour.md`
- **Course week:** 7
- **Exam probability:** ⭐⭐
- **Dependencies:** all of the above
- **Related concepts:** monad-laws, iso/retract proofs (Data1, Assignment 2 Ex 5)
- **Typical type signatures:** none specific — talks about specifications and proofs
- **Question generators:**
  - "State the monad laws"
  - "Prove `fmap id = id` for this Functor"
  - "Show `f . g = id` and `g . f` is a permutation (retract not iso) — Assignment 2 Ex 5"
  - "Write a QuickCheck property capturing this spec"
- **Common mistakes:**
  - Conflating iso (`f . g = id` and `g . f = id`) with retract (`f . g = id` only)
  - QuickCheck property that fails to generate the relevant inputs
  - Stating "by induction" without doing both base and step
- **Related archetypes:** A20
- **Search keywords:** rigour, spec, law, prove, iso, retract, QuickCheck property

## Free-monad

- **Lecture file:** `monads.md` and Assignment 3
- **Course week:** 10
- **Exam probability:** ⭐⭐⭐
- **Dependencies:** Monad, Functor, custom-ADTs
- **Related concepts:** multi-effect, rose-trees (`Rose ≅ Free [] a`), interpreters
- **Typical type signatures:**
  ```haskell
  data Free f a = Pure a | Free (f (Free f a))
  liftF  :: Functor f => f a -> Free f a
  unfree :: Monad m   => Free m a -> m a
  toRose :: Free [] a -> Rose a
  ```
- **Question generators:**
  - "Show `Rose ≅ Free [] a` via `toRose`/`fromRose`"
  - "Use `Free (State s)` to record an execution trace"
  - "Build a scheduler over `Free (FSum (State s) Yield)`"
- **Common mistakes:**
  - Confusing `Pure` (lift a value) with the functor's own pure
  - Not recursing through `Free (fmap (>>= f) ffa)` correctly
- **Related archetypes:** A14, A20, A05
- **Search keywords:** Free, Pure, liftF, unfree, freer

---

## Course-level notes

- **Allowed imports in exam:** `Prelude`, `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`. `Control.Monad.Except`, `Control.Monad.Reader` appear in problem sheets but **may not be imported** in the mock — verify per question whether the exam paper preloads them via a `Types.hs`.
- **vLab quirks:** `Safe` pragma + `NoGeneralizedNewtypeDeriving`. `Functor`-deriving needs `{-# LANGUAGE DeriveFunctor #-}` and isn't blocked by `Safe`.
- **Marking:** auto-marked with QuickCheck — every solution must compile on vLab and match the exact type signature in the template.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
