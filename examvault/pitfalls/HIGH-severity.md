<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [pitfalls](./README.md) · **Pitfalls — HIGH severity (marks-killers)**

<!-- siblings:start -->
> **Peers:** **HIGH-severity** · [LOW-severity](./LOW-severity.md) · [MEDIUM-severity](./MEDIUM-severity.md) · [imports-pitfalls](./imports-pitfalls.md) · [per-topic-pitfalls](./per-topic-pitfalls.md) · [signature-pitfalls](./signature-pitfalls.md)
<!-- siblings:end -->






# Pitfalls — HIGH severity (marks-killers)

> **What counts as HIGH:** any mistake that loses **5 or more marks** in a single occurrence — typically by causing the auto-marker to assign zero to a whole sub-question, fail to compile, or reject the module outright. Read these once the night before. Make sure each one rings a bell.

These are the LANDMINES. The marker is QuickCheck + a strict module import. Any of these = catastrophic on that question.

---

<a id="p-001"></a>
## P-001 · Type signature changed (any character)

**Topic:** Signatures / Auto-marker
**Symptom:** The marker imports your module as `qualified MockTest as Student` and looks up each function by **exact name and type**. If your signature differs by ONE character — extra constraint, missing constraint, wrong type variable letter in a context — Haskell type-checks fine on your machine but the marker's `qualified` import sees the wrong type and either rejects the file or scores zero on that question.
**Cause:** Retyping the signature from memory; "improving" by adding `Ord a =>` "to be safe"; lowercasing the function name; reordering arguments.
**Fix:** **COPY-PASTE** the signature from the template. Don't retype. Don't decorate.
**Example wrong:**
```haskell
-- Template said:
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
-- Student typed:
applyNTimes :: (Monad m, Eq a) => m a -> (a -> m a) -> Int -> m [a]
```
**Example right:**
```haskell
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx mf 0 = do x <- mx; return [x]
applyNTimes mx mf n = do x <- mx; xs <- applyNTimes (mf x) mf (n-1); return (x:xs)
```
**Marks lost:** 10 (the whole question)
**Seen in:** every cohort. Documented in [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) U7.

---

<a id="p-002"></a>
## P-002 · Module declaration changed

**Topic:** Module header
**Symptom:** `presubmit.sh` fails or the marker's `qualified import MockTest as Student` returns `Could not find module 'MockTest'`. Zero on EVERY question.
**Cause:** Renaming the module to `MockTest2`, lowercasing it, exporting `(..)` instead of the listed names, removing an export.
**Fix:** Leave the module line exactly as the template wrote it. Don't add or remove anything from the export list.
**Example wrong:**
```haskell
module MockTest where        -- removed the explicit export list
-- or
module Mocktest ( ... )      -- lowercased the T
-- or
module MockTest ( isNBranching, prune ) where  -- omitted later questions' exports
```
**Example right:**
```haskell
module MockTest ( isNBranching
                , prune
                , applyNTimes
                , gameOver
                , takeTokens
                , isMagicSquare
                , circuit
                ) where
```
**Marks lost:** 50 (whole paper)
**Seen in:** common when students delete the export list "to clean up". The export list is LOAD-BEARING — the marker needs to import each name.

---

<a id="p-003"></a>
## P-003 · Import outside the allowed set

**Topic:** Imports / Safe Haskell
**Symptom:** Compile error during marking ("module not available in safe mode" or "could not find module"). Marker auto-fails the whole file.
**Cause:** The student adds `import Data.Map`, `import Data.Set`, `import Control.Monad.Except`, `import Data.IORef`, etc. — these are NOT in the allowed list (and most are not Safe-Haskell-clean).
**Fix:** Only ever import: `Prelude` (implicit), `Data.List`, `Data.Char`, `Data.Maybe`, `Control.Monad`, `Control.Monad.State`, `Control.Monad.Writer`. Plus any `Types.hs` provided by the question.
**Example wrong:**
```haskell
import Data.Map (Map)        -- NOT allowed
import qualified Data.Map as M
import Data.Set (Set)        -- NOT allowed
import System.IO.Unsafe      -- definitely not allowed (Safe forbids)
```
**Example right:**
```haskell
import Types
import Data.List
import Data.Char
import Data.Maybe
import Control.Monad
import Control.Monad.State
import Control.Monad.Writer
```
**Marks lost:** 50 (whole paper if it stops compiling)
**Seen in:** see `imports-pitfalls.md`. Detailed allowed list there.

---

<a id="p-004"></a>
## P-004 · Used `Control.Monad.Reader` or `Control.Monad.Except`

**Topic:** Imports / forbidden monads
**Symptom:** Compile error during marking. Or, worse, you wrote `throwError` and your file just doesn't have a definition for it.
**Cause:** Reader and Except are in `mtl` but not in the allowed set. Students reach for them when they "want the proper way" to do error handling — but the course uses bare `Maybe` and `Either`.
**Fix:** Use `Maybe` for failure ("throw error" = `Nothing`). Use `Either String` for error messages. Use a function argument `env ->` for read-only configuration (NOT `Reader`).
**Example wrong:**
```haskell
import Control.Monad.Except       -- FORBIDDEN
import Control.Monad.Reader       -- FORBIDDEN

eval :: Expr -> Reader Env (Either String Int)
eval (Var x) = do env <- ask; case lookup x env of ...
```
**Example right:**
```haskell
-- read-only config: just a plain argument
eval :: Env -> Expr -> Either String Int
eval env (Var x) = case lookup x env of
                     Nothing -> Left ("undefined: " ++ [x])
                     Just v  -> Right v
```
**Marks lost:** 10 (per question that uses them) — usually the whole paper because the file won't compile.
**Seen in:** A14 archetype — the exam multi-effect interpreter is `StateT s (Either e)` only if explicitly allowed; for self-contained Q's, use just `Either`.

---

<a id="p-005"></a>
## P-005 · Missing base case → infinite loop / non-exhaustive pattern

**Topic:** Universal recursion
**Symptom:** QuickCheck input shrinks to the smallest counterexample — `[]`, `Empty`, `Leaf x`, `0`. Your function either loops forever (time-out → 0 marks) or throws `Non-exhaustive patterns in function f`. The marker uses `deepseq` so it WILL force the error and you score 0 on that input class.
**Cause:** Writing only the recursive case. Or writing `f xs = …` thinking the wildcard pattern catches `[]`, but it has unreachable subexpressions inside that hit `head` / `tail`.
**Fix:** ALWAYS write the base case FIRST. Make it the first equation. Use the "what's the most defensive base case" table (in [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md)).
**Example wrong:**
```haskell
sumTree :: BT Int -> Int
sumTree (Fork x l r) = x + sumTree l + sumTree r
-- Missing Empty case!  Marker calls sumTree Empty → Non-exhaustive patterns
```
**Example right:**
```haskell
sumTree :: BT Int -> Int
sumTree Empty        = 0                            -- BASE FIRST
sumTree (Fork x l r) = x + sumTree l + sumTree r
```
**Marks lost:** 5-10 (whole sub-question)
**Seen in:** any tree / list recursion. `-fwarn-incomplete-patterns` will catch it if you actually read the warning.

---

<a id="p-006"></a>
## P-006 · Mock Q3 `gameOver` does not return `True` on `(0,0)`

**Topic:** State monad / hardcoded test
**Symptom:** You lose 4 marks on the nullary marker test. The marker's exact code is `prop_gameOverComplete = let (p, _) = runState Student.gameOver (0, 0) in p ~= True`. ONE test, hardcoded, no generator. If your `gameOver` returns False or crashes on `(0,0)`, you take a flat 4-mark hit even if your recursive logic is otherwise correct.
**Cause:** Reading "game over" as "after the game" — implementing it as a check on whether the LAST move was legal, instead of the obvious "are both heaps zero?". Or pattern-matching `(x, y)` with a guard that misses `x == 0 && y == 0`.
**Fix:** Direct implementation: `do (x,y) <- get; return (x == 0 && y == 0)`.
**Example wrong:**
```haskell
gameOver :: NimGame Bool
gameOver = do (x,y) <- get; return (x == 0 || y == 0)   -- 'or' not 'and'
-- on (0,0): returns True. on (0,5): returns True. WRONG: a game is only over when BOTH heaps are 0.
```
**Example right:**
```haskell
gameOver :: NimGame Bool
gameOver = do (x, y) <- get
              return (x == 0 && y == 0)
```
**Marks lost:** 4 (the hardcoded test) — and the cascade may gate other tests.
**Seen in:** Mock paper Q3. [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) §4.

---

<a id="p-007"></a>
## P-007 · Mock Q2 `applyNTimes mx mf 0` returns `[]` instead of `[x]`

**Topic:** Generic Monad combinator
**Symptom:** Lose 2 marks on the base-case test. Possible 8-mark cascade fail because the `IfSuccess` recursive test only runs if the base test passes.
**Cause:** Reading "apply n times" as "apply zero times = produce nothing". But the spec is "the result LIST contains the initial seed plus n further applications" — so the 0-times case still yields ONE element (the seed itself).
**Fix:** Base case `applyNTimes mx _ 0 = do x <- mx; return [x]`. NOT `return []`.
**Example wrong:**
```haskell
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes _  _  0 = return []                       -- WRONG
applyNTimes mx mf n = do x <- mx
                         xs <- applyNTimes (mf x) mf (n-1)
                         return (x : xs)
```
**Example right:**
```haskell
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
applyNTimes mx _  0 = do x <- mx; return [x]          -- yields the seed
applyNTimes mx mf n = do x <- mx
                         xs <- applyNTimes (mf x) mf (n-1)
                         return (x : xs)
```
**Marks lost:** 2 directly + risk of cascade up to 8.
**Seen in:** Mock Q2. [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) U9.

---

<a id="p-008"></a>
## P-008 · Numeric recursion uses `n == 0` not `n <= 0`

**Topic:** Recursion on a number
**Symptom:** `applyNTimes _ _ (-3)` infinite-loops; `myTake (-1) xs` infinite-loops. Marker shrinks to `n=-1` and gets a timeout. Zero on that test.
**Cause:** Pattern `0 = …` only matches exactly 0; the recursive case fires on `n = -1` and recurses to `n = -2`, then `-3`, …
**Fix:** Use a guard `| n <= 0` instead of pattern-matching just `0`. Always.
**Example wrong:**
```haskell
myTake 0 _      = []
myTake n (x:xs) = x : myTake (n-1) xs        -- myTake (-1) [1,2,3] loops
```
**Example right:**
```haskell
myTake n _   | n <= 0 = []
myTake _ []           = []
myTake n (x:xs)       = x : myTake (n-1) xs
```
**Marks lost:** 5+ (test times out)
**Seen in:** any number-driven recursion. [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) U8.

---

<a id="p-009"></a>
## P-009 · `isBST Empty = False` (vacuous truth bug)

**Topic:** BST / predicates over Empty
**Symptom:** The marker generates many random trees, asks `isBST t`. Half fail because you return False on the most common subtree (`Empty`). Zero or partial credit on `isBST`.
**Cause:** "An empty tree has no nodes, so it's not really a tree" intuition. WRONG — by convention, **predicates over empty collections are vacuously True** (just like `all p [] = True`).
**Fix:** `isBST Empty = True`. Always. Same goes for `isSorted []`, `isBalanced Empty`, `allEqual []`, etc.
**Example wrong:**
```haskell
isBST :: Ord a => BT a -> Bool
isBST Empty = False                          -- WRONG, vacuous truth
isBST (Fork v l r) = ...
```
**Example right:**
```haskell
isBST :: Ord a => BT a -> Bool
isBST = go Nothing Nothing
  where
    go _   _   Empty        = True            -- VACUOUS TRUTH
    go lo  hi  (Fork v l r) = maybe True (< v) lo
                           && maybe True (> v) hi
                           && go lo (Just v) l
                           && go (Just v) hi r
```
**Marks lost:** 4-8 (depends on what fraction of generated trees include Empty as a subtree — essentially all of them after shrinking)
**Seen in:** [VAULT-AUDIT](../meta/VAULT-AUDIT.md) — the OLD vault had this bug in its templates. Documented in `githubinitial.hs` student bug. **The auditor flagged this as a bug carried in the previous vault** — three different `isBST` implementations existed in the old `markdownvault/`, and one of them was the O(n²) `allLT`/`allGT` version that the pitfall file warned against. **Read the bound-threaded version above, not the old vault's.**

---

<a id="p-010"></a>
## P-010 · `deriving Functor` without the pragma — and the course wants it by hand anyway

**Topic:** Typeclass instance / Safe Haskell
**Symptom:** `deriving Functor` needs the `DeriveFunctor` pragma in your file; **Safe permits it on modern GHC** (it is `GeneralizedNewtypeDeriving` that Safe blocks, not `DeriveFunctor`). But the course wants the instance written by hand and the template may not enable `DeriveFunctor` — so if you add `deriving Functor` to a bare `data` line the compiler errors with "Can't make a derived instance ... You need DeriveFunctor", and adding the pragma yourself defeats the point of the exercise. Either way you risk a zero.
**Cause:** Trying to derive `Functor` to save typing the instance by hand.
**Fix:** WRITE the `Functor` instance by hand. It's three lines for any ADT. (Note: the old "DeriveFunctor conflicts with Safe" claim is FALSE on GHC 9.x — the real reasons are the missing pragma and the course's hand-rolled requirement.)
**Example wrong:**
```haskell
{-# LANGUAGE Safe #-}                            -- DeriveFunctor not enabled
data BT a = Empty | Fork a (BT a) (BT a)
  deriving Functor                               -- error: needs DeriveFunctor; and the course wants it by hand
```
**Example right:**
```haskell
{-# LANGUAGE Safe #-}
data BT a = Empty | Fork a (BT a) (BT a)

instance Functor BT where
  fmap _ Empty        = Empty
  fmap f (Fork x l r) = Fork (f x) (fmap f l) (fmap f r)
```
**Marks lost:** 5-10 (whole question if it won't compile)
**Seen in:** any time you redeclare an ADT in your answer (rare — usually `Types.hs` defines them).

---

<a id="p-011"></a>
## P-011 · `{-# LANGUAGE Safe #-}` pragma deleted or changed

**Topic:** Header / Safe Haskell
**Symptom:** `presubmit.sh` checks `ghc -XSafe -XNoGeneralizedNewtypeDeriving` compiles. If you've deleted the Safe pragma (or changed it to something else like `Trustworthy`), the safety check fails. Marker auto-zero on safety check.
**Cause:** Tidying up the header; thinking the pragma was decorative; copy-pasting a snippet from a non-exam project.
**Fix:** Don't touch the top of the template. The line above "DO NOT MAKE ANY CHANGES ABOVE THIS LINE" is canonical.
**Example wrong:**
```haskell
{-# LANGUAGE NoGeneralizedNewtypeDeriving #-}    -- deleted Safe
module MockTest ( ... ) where
```
**Example right:**
```haskell
{-# OPTIONS_GHC -fwarn-incomplete-patterns -Wno-x-partial #-}
{-# LANGUAGE NoGeneralizedNewtypeDeriving, Safe #-}
module MockTest ( ... ) where
```
**Marks lost:** 50 (whole paper)
**Seen in:** see `imports-pitfalls.md` for the full Safe explanation.

---

<a id="p-012"></a>
## P-012 · Custom `Show` makes `show` return non-string

**Topic:** Typeclass instance
**Symptom:** Type error at compile. `show :: a -> String` — if you write `show (Foo x) = x` where `x :: Int`, you've returned an Int.
**Cause:** Confusing `show` with a function that returns "whatever printable thing".
**Fix:** `show x = "Foo " ++ show x` — every recursive call returns String.
**Example wrong:**
```haskell
instance Show Expr where
  show (Val n)   = n                           -- Int returned, not String
  show (Add a b) = show a ++ "+" ++ show b
```
**Example right:**
```haskell
instance Show Expr where
  show (Val n)   = show n                      -- show :: Int -> String
  show (Add a b) = show a ++ "+" ++ show b
```
**Marks lost:** 5+ (compile fails — could cascade to whole paper)
**Seen in:** A13 archetype.

---

<a id="p-013"></a>
## P-013 · Function name changed (even by casing or pluralisation)

**Topic:** Signatures / Auto-marker
**Symptom:** `qualified import MockTest as Student` returns "Variable not in scope: Student.applyNtimes". Zero on that question.
**Cause:** Auto-correct turning `applyNTimes` into `applyNtimes`; "fixing" `isBST` to `isBst`; pluralising `gameOver` to `gameOvers`.
**Fix:** Copy the function name from the template. Same as P-001 — don't retype.
**Example wrong:**
```haskell
applyntimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
isBst :: Ord a => BT a -> Bool
isMagicsquare :: [[Int]] -> Bool
```
**Example right:**
```haskell
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
isBST :: Ord a => BT a -> Bool
isMagicSquare :: [[Int]] -> Bool
```
**Marks lost:** 10 per renamed function
**Seen in:** common in editors with aggressive auto-correct.

---

<a id="p-014"></a>
## P-014 · `isNBranching` shallow check — forgets to recurse on children

**Topic:** Rose tree predicates
**Symptom:** Marker generates `Branch [Branch [Leaf 1, Leaf 2], Branch [Leaf 1, Leaf 2, Leaf 3]]` with `n=2`. Your code returns True (the outer Branch has 2 children) but the inner-right Branch has 3. Lose 5+ marks on the recursion test.
**Cause:** Writing `length xs == n` and stopping. The Q1 marker checks ALL nodes uniformly.
**Fix:** ALWAYS `&& all (isNBranching n) xs` after the length check.
**Example wrong:**
```haskell
isNBranching _ (Leaf _)    = True
isNBranching n (Branch xs) = length xs == n               -- SHALLOW
```
**Example right:**
```haskell
isNBranching _ (Leaf _)    = True
isNBranching n (Branch xs) = length xs == n && all (isNBranching n) xs
```
**Marks lost:** 5-10
**Seen in:** Mock Q1. `ewan20.hs` student bug. `examples/mock-q1-rose.md`.

---

<a id="p-015"></a>
## P-015 · BST `delete` two-children case wrong — promotes Empty or duplicates

**Topic:** BST / two-children case
**Symptom:** Marker compares `deleteBST x t` to a reference. Yours either drops a node, duplicates one, or leaves `Empty` where it shouldn't. Lose 5+ marks on `delete` recursion tests.
**Cause:** Forgetting that the two-children case needs a successor/predecessor swap. Or doing it half-way: replacing the node's value with `largestOf l` but NOT removing that node from `l`.
**Fix:** `largestOf l` + `withoutLargest l` (rightmost-of-left rule) — both are needed.
**Example wrong:**
```haskell
deleteBST x (Fork v l r)
  | x < v = Fork v (deleteBST x l) r
  | x > v = Fork v l (deleteBST x r)
  | otherwise = case (l, r) of
      (Empty, Empty) -> Empty
      (l,     Empty) -> l
      (Empty, r    ) -> r
      _              -> Fork (largestOf l) l r          -- BUG: didn't remove largest!
```
**Example right:**
```haskell
deleteBST x (Fork v l r)
  | x < v = Fork v (deleteBST x l) r
  | x > v = Fork v l (deleteBST x r)
  | otherwise = case (l, r) of
      (Empty, Empty) -> Empty
      (l,     Empty) -> l
      (Empty, r    ) -> r
      _              -> Fork (largestOf l) (withoutLargest l) r
  where
    largestOf (Fork x _ Empty) = x
    largestOf (Fork _ _ r)     = largestOf r
    withoutLargest (Fork _ l Empty) = l
    withoutLargest (Fork x l r)     = Fork x l (withoutLargest r)
```
**Marks lost:** 5-8
**Seen in:** A11 archetype. [bst-attacks](../quickcheck/bst-attacks.md) #13.

---

<a id="p-016"></a>
## P-016 · Functor instance doesn't preserve shape (Empty maps to Fork, etc.)

**Topic:** Functor instance
**Symptom:** Functor laws fail: `fmap id /= id`. Marker tests `fmap id t == t` for arbitrary `t`. If you reshape the tree, this fails. Zero on `Functor` test.
**Cause:** Pattern-matching too aggressively (`fmap f Empty = Fork (f undefined) Empty Empty` — yes, students really do this); or confusing `fmap` with a fold.
**Fix:** Shape preservation is the FIRST functor law. Empty ↔ Empty. Fork ↔ Fork. Leaf ↔ Leaf. Branch ↔ Branch.
**Example wrong:**
```haskell
instance Functor BT where
  fmap _ Empty        = Empty
  fmap f (Fork x l r) = Fork (f x) (fmap f l) Empty       -- DROPPED right subtree
```
**Example right:**
```haskell
instance Functor BT where
  fmap _ Empty        = Empty
  fmap f (Fork x l r) = Fork (f x) (fmap f l) (fmap f r)
```
**Marks lost:** 8-10 (whole Functor question)
**Seen in:** A06 archetype.

---

<a id="p-017"></a>
## P-017 · Non-exhaustive pattern despite `-fwarn-incomplete-patterns`

**Topic:** Compile warning ignored
**Symptom:** The template has `-fwarn-incomplete-patterns`. GHC will tell you "Pattern match(es) are non-exhaustive". Many students see the WARNING but compile anyway, only to have QuickCheck hit the missing branch and crash.
**Cause:** Treating warnings as ignorable. Treating "it ran" as "it works".
**Fix:** Treat every incomplete-pattern warning as a marker bug. Add the missing branch BEFORE running anything.
**Example wrong:**
```haskell
weird :: Maybe Int -> Int
weird (Just x) = x
-- WARNING: non-exhaustive — Nothing not handled. Marker calls weird Nothing → CRASH.
```
**Example right:**
```haskell
weird :: Maybe Int -> Int
weird Nothing  = 0
weird (Just x) = x
```
**Marks lost:** 5-10 per affected function
**Seen in:** universal. [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) U1.

---

<a id="p-018"></a>
## P-018 · Using `head` / `tail` / `!!` without a guard → exception

**Topic:** Universal partiality
**Symptom:** Marker calls your function on an empty list. `head []` throws `Prelude.head: empty list`. The marker uses `deepseq` so it WILL see the exception. Zero on that test.
**Cause:** Treating Prelude's partial functions as total. Forgetting that QuickCheck reaches for empty inputs first.
**Fix:** Pattern-match instead. Or write `safeHead xs = case xs of [] -> Nothing; (x:_) -> Just x`. Never raw `head` on a list whose non-emptiness you can't prove from context.
**Example wrong:**
```haskell
firstEven :: [Int] -> Int
firstEven xs = head (filter even xs)         -- crashes on [1,3,5]
```
**Example right:**
```haskell
firstEven :: [Int] -> Maybe Int
firstEven xs = case filter even xs of
                 []    -> Nothing
                 (x:_) -> Just x
```
**Marks lost:** 5
**Seen in:** lists-attacks.md U1.

---

<a id="p-019"></a>
## P-019 · Mock Q5 ADT-translation: copy-paste between `p` and `q` cases

**Topic:** ADT translation
**Symptom:** Mock Q5 `circuit (Or p q) = ...` — the structurally correct answer uses BOTH `p` and `q` once on each side. Easy to copy the `np` formula and paste it for `nq` forgetting to swap `p → q`. Lose 4+ marks on the `Or` semantic test.
**Cause:** The `Or` case is `Nand np nq` where `np = Nand (circuit p) (circuit p)` AND `nq = Nand (circuit q) (circuit q)`. The repeated `(circuit p)` inside `np` is what tricks people into copy-pasting and writing `np = Nand (circuit p) (circuit p); nq = Nand (circuit p) (circuit p)`. The second one MUST be `q`.
**Fix:** Derive each case FROM THE TRUTH TABLE, not by copying. Or use `let pq = Nand (circuit p) (circuit q)` once.
**Example wrong:**
```haskell
circuit (Or p q) = Nand np nq
  where np = Nand (circuit p) (circuit p)
        nq = Nand (circuit p) (circuit p)   -- WRONG: should be q
```
**Example right:**
```haskell
circuit (Or p q) = Nand np nq
  where np = Nand (circuit p) (circuit p)
        nq = Nand (circuit q) (circuit q)
-- Equivalent and harder to typo:
-- circuit (Or p q) = let np = Nand (circuit p) (circuit p)
--                       nq = Nand (circuit q) (circuit q)
--                   in Nand np nq
```
**Marks lost:** 4-6 (the Or test)
**Seen in:** Mock Q5. `final10.hs` student bug. Documented in `examples/mock-q5-circuit.md`.

---

<a id="p-020"></a>
## P-020 · Three different `isBST` implementations in old vault (audit finding)

**Topic:** BST / inconsistency
**Symptom:** You copy `isBST` from one notes file, the helpers from another, get a compile error or silent wrong result. ~8 marks lost.
**Cause:** `notehost-vault/markdownvault/` contained THREE different `isBST` definitions: bound-threading (correct), `allLT`/`allGT` (O(n²) — the OLD pitfall file flagged this as WRONG), and `ordered . flattenInOrder` (correct but slower). A student doing copy-paste between files mixes incompatible helpers.
**Fix:** Use the bound-threading version (P-009 above). Don't mix with `allLT`/`allGT`. If you copy `flattenInOrder`-based, make sure you also copy the `ordered` helper from the same file.
**Example wrong (mixed):**
```haskell
isBST Empty = True                                    -- from file A
isBST t = allLT (flattenInOrder l) (Fork v l r) ...   -- from file B (and `allLT` is the O(n²) flagged-WRONG one!)
```
**Example right (canonical bound-threading):**
```haskell
isBST :: Ord a => BT a -> Bool
isBST = go Nothing Nothing
  where go _ _ Empty = True
        go lo hi (Fork v l r) = maybe True (< v) lo
                             && maybe True (> v) hi
                             && go lo (Just v) l
                             && go (Just v) hi r
```
**Marks lost:** 5-8 (silent wrong answer; or compile fail)
**Seen in:** [VAULT-AUDIT](../meta/VAULT-AUDIT.md) lines 24-25 explicitly call this out as a bug carried in the previous vault. **Surprising HIGH flag** because most students wouldn't realise their reference notes contradict themselves.

---

<a id="p-021"></a>
## P-021 · `IfFail` cascade misread — you fix the wrong thing

**Topic:** Marker structure
**Symptom:** Marker reports "test fooComplete failed: counterexample = X". Student panics, rewrites the whole function. But the test was an `IfFail` — i.e., a partial-credit fallback that runs ONLY when the main test fails. By "fixing the partial-credit test" you may break the main test for which you previously had structural correctness.
**Cause:** Misreading the marker structure (see [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) "How the marker actually structures tests").
**Fix:** When a test fails, locate the `condition = IfFail otherTest`. The OTHER test is the strict one; THIS test is the lenient fallback. Fix the STRICT test first.
**Example:** Mock Q2 has `prop_applyNTimes_outOfOrder` as an `IfFail` of `prop_applyNTimes`. If the strict test fails because elements are out of order, the cascade gives you partial credit. Don't rewrite the WHOLE function to chase the cascade test — fix the original.
**Marks lost:** 4-6 (you may sacrifice partial credit by misdiagnosing)
**Seen in:** [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) lines 100-122.

---

<a id="p-022"></a>
## P-022 · Forgetting to put base case FIRST

**Topic:** Pattern ordering
**Symptom:** Recursion fires on `[]` because the wildcard pattern matched first. Either non-termination or wrong result.
**Cause:** Writing `f xs = ...` then `f [] = ...` — order matters in Haskell pattern matching.
**Fix:** Put base cases FIRST. Always.
**Example wrong:**
```haskell
mySum :: [Int] -> Int
mySum (x:xs) = x + mySum xs
mySum []     = 0
-- compile WARNS "Pattern match has redundant cases"? No, it's reachable.
-- but if you write the recursive case more generally: `mySum xs = head xs + mySum (tail xs)`
-- then mySum [] crashes because head [] crashes BEFORE the second equation matches.
```
**Example right:**
```haskell
mySum :: [Int] -> Int
mySum []     = 0           -- BASE FIRST
mySum (x:xs) = x + mySum xs
```
**Marks lost:** 5-10 (depends on the function)
**Seen in:** any recursion. Standard discipline.

---

<a id="p-023"></a>
## P-023 · `deepseq` exposes lazy `undefined` you thought was hidden

**Topic:** Marker forcing
**Symptom:** Your function returns a tuple `(x, undefined)`; you assumed only the first field would be tested. Marker uses `student' = deepseq student student` — this forces EVERY field. Crash. Zero on that test.
**Cause:** Stubbing a half-finished function "lazily". The marker NEVER lets you skate on laziness.
**Fix:** If you must stub, return a defined-but-wrong value (e.g. `(x, [])` instead of `(x, undefined)`), so deepseq passes. Or delete the function and let the type error surface earlier.
**Example wrong:**
```haskell
splitGame :: Game -> (Bool, [Move])
splitGame g = (gameOver g, undefined)
```
**Example right:**
```haskell
splitGame :: Game -> (Bool, [Move])
splitGame g = (gameOver g, [])     -- defined; deepseq passes; you might score partial
```
**Marks lost:** 5+ on tests that touch the undefined field
**Seen in:** [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) "Surprising patterns" §2.

---

<a id="p-024"></a>
## P-024 · State action returns the wrong type — `()` vs the result

**Topic:** State monad return type
**Symptom:** Type error. Compile fail. Marker can't even load your file.
**Cause:** `takeTokens` returns `NimGame ()`, NOT `NimGame Bool`. Beginners write `takeTokens n h = do ... ; return True` and the type doesn't match.
**Fix:** Read the signature. `NimGame ()` means the result is unit. `do put (...)` ALREADY returns `State s ()`. Don't add `return True`.
**Example wrong:**
```haskell
takeTokens :: Int -> Heap -> NimGame ()
takeTokens n First = do (x,y) <- get
                        put (max 0 (x-n), y)
                        return True                  -- TYPE ERROR
```
**Example right:**
```haskell
takeTokens :: Int -> Heap -> NimGame ()
takeTokens n First  = do (x,y) <- get; put (max 0 (x-n), y)
takeTokens n Second = do (x,y) <- get; put (x, max 0 (y-n))
```
**Marks lost:** 10 (the whole Q3 takeTokens — compile fail)
**Seen in:** Mock Q3 takeTokens.

---

<a id="p-025"></a>
## P-025 · Returned `Bool` where `Maybe a` expected (or vice-versa)

**Topic:** Type signature comprehension
**Symptom:** Compile error: "couldn't match expected type `Maybe Int` with actual type `Bool`". Or the function "returns" `True` and the marker's tests don't even run.
**Cause:** Misreading the signature. `member :: Ord a => a -> BT a -> Bool` returns Bool, NOT `Maybe a`. `lookup :: a -> [(a,b)] -> Maybe b` returns `Maybe b`, NOT `b`.
**Fix:** Eyeball the signature first. Write the type sig + base case + ONE expression that produces the right shape, then fill in.
**Example wrong:**
```haskell
member :: Ord a => a -> BT a -> Bool
member x t = lookup x (flatten t)      -- WRONG: lookup gives Maybe, not Bool
```
**Example right:**
```haskell
member :: Ord a => a -> BT a -> Bool
member _ Empty        = False
member x (Fork v l r) | x == v = True
                     | x < v  = member x l
                     | otherwise = member x r
```
**Marks lost:** 10 (compile fail)
**Seen in:** universal.

---

<a id="p-026"></a>
## P-026 · Forgetting `{-# LANGUAGE Safe #-}` blocks all marker tests

**Topic:** Safe Haskell
**Symptom:** `presubmit.sh` step 2 (`ghc -XSafe -XNoGeneralizedNewtypeDeriving`) errors with "Safe Haskell rejects module: <reason>". Marker auto-zero on safety check.
**Cause:** Importing `System.IO.Unsafe`, `unsafeCoerce`, anything FFI; using `deriving Functor` without explicit `{-# LANGUAGE DeriveFunctor #-}`; using `Control.Monad.Reader` (not Safe in older mtl).
**Fix:** Use ONLY the allowed imports. Write all instances by hand. Run the Safe check locally.
**Marks lost:** 50 (whole paper)
**Seen in:** `imports-pitfalls.md` for full Safe explanation.

---

<a id="p-027"></a>
## P-027 · Letting GHCi runtime errors mask compile errors

**Topic:** Workflow
**Symptom:** You think the function works because `ghci> myFunc [1,2,3]` returns the right answer. You submit. Marker runs `myFunc []` → `Prelude.head: empty list`. Zero.
**Cause:** Only testing the happy path. Never running the marker's expected adversarial inputs.
**Fix:** After EVERY function, mentally run: `f []`, `f [x]`, `f Empty`, `f (Leaf x)`, `f 0`, `f (-1)`. If any of these crash → it's broken.
**Marks lost:** 5+ per function
**Seen in:** every cohort. The reason `pre-submit.md` insists on the 60-second checklist.

---

<a id="p-028"></a>
## P-028 · `presubmit.sh` exit code ignored

**Topic:** Pre-submit
**Symptom:** You run `./presubmit.sh MockTest`, see some output, assume it's OK. Marker rejects file. Zero.
**Cause:** `presubmit.sh` shows compile errors but doesn't always halt the script — you must check the FINAL exit code (echo `$?` should print `0`).
**Fix:** Always run `./presubmit.sh MockTest && echo OK || echo FAIL`. Only submit if it says OK.
**Marks lost:** 50 (whole paper if file doesn't compile under Safe)
**Seen in:** universal.

---

<a id="p-029"></a>
## P-029 · `do` block returning monadic value instead of bare value

**Topic:** Monad laws
**Symptom:** Type error. "Couldn't match type `State s (State s a)` with `State s a`".
**Cause:** Writing `do x <- get; return (get)` instead of `do x <- get; return x`. The `return` wraps once; if you `return` an already-wrapped value you double-wrap.
**Fix:** `return` takes a BARE value. The result of `<-` is bare. The result of a plain `do` expression is monadic — don't put `return` around it.
**Example wrong:**
```haskell
addOne :: State Int Int
addOne = do n <- get
            put (n+1)
            return get                  -- DOUBLE-WRAPPED. type: State Int (State Int Int)
```
**Example right:**
```haskell
addOne :: State Int Int
addOne = do n <- get
            put (n+1)
            return n                    -- bare n
```
**Marks lost:** 10 (compile fail)
**Seen in:** beginner State code.

---

<a id="p-030"></a>
## P-030 · Magic-square checks columns / diagonal in wrong direction

**Topic:** Matrix predicate
**Symptom:** Marker generates `[[8,1,6],[3,5,7],[4,9,2]]` (a real magic square — sum 15). Your code returns False because you computed the anti-diagonal as `[8,5,2]` instead of `[6,5,4]`. Lose 5+ marks on the matrix test.
**Cause:** `zipWith (!!) xss [0..]` gives the MAIN diagonal `[xss !! 0 !! 0, xss !! 1 !! 1, ...]`. The ANTI-diagonal is `zipWith (!!) (reverse xss) [0..]` OR `zipWith (!!) xss [n-1, n-2, ..0]`. Mix these up.
**Fix:** Use the canonical pair:
```haskell
diag1 = zipWith (!!) xss [0..]            -- main: top-left to bottom-right
diag2 = zipWith (!!) (reverse xss) [0..]  -- anti: bottom-left to top-right
```
**Example wrong:**
```haskell
diag2 = zipWith (!!) xss [n-1, n-2 .. 0]  -- where n = length xss
-- Off-by-one bugs everywhere; sometimes works, sometimes doesn't.
```
**Example right:**
```haskell
isMagicSquare :: [[Int]] -> Bool
isMagicSquare [] = False
isMagicSquare xss =
  let target = sum (head xss)
      rows   = all (\r -> sum r == target) xss
      cols   = all (\c -> sum c == target) (transpose xss)
      d1     = sum (zipWith (!!) xss [0..]) == target
      d2     = sum (zipWith (!!) (reverse xss) [0..]) == target
  in rows && cols && d1 && d2
```
**Marks lost:** 5
**Seen in:** Mock Q4. `examples/mock-q4-magic.md`.

---

## See also

- `MEDIUM-severity.md` — silent correctness bugs
- `LOW-severity.md` — style and efficiency
- `signature-pitfalls.md` — the auto-marker import contract
- [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) — what the marker generates
- [ONE-PAGE-PANIC](../exam-day/ONE-PAGE-PANIC.md) — when you blank

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
