<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [pitfalls](./README.md) · **Pitfalls — Type Signatures (the auto-marker contract)**

<!-- siblings:start -->
> **Peers:** [HIGH-severity](./HIGH-severity.md) · [LOW-severity](./LOW-severity.md) · [MEDIUM-severity](./MEDIUM-severity.md) · [imports-pitfalls](./imports-pitfalls.md) · [per-topic-pitfalls](./per-topic-pitfalls.md) · **signature-pitfalls**
<!-- siblings:end -->






# Pitfalls — Type Signatures (the auto-marker contract)

> The marker imports your module as `qualified MockTest as Student`. It then references `Student.applyNTimes`, `Student.gameOver`, etc. — by **exact name and exact type**. Any deviation = "Variable not in scope: `Student.foo`" or a type-mismatch error → ZERO MARKS on that question.

This is the single most preventable category of marks loss. Read once. Internalise.

---

## The rule

**COPY-PASTE every type signature from the template. Don't retype. Don't decorate. Don't optimise.**

---

## Mock Test signatures — VERBATIM (the actual marker contract)

These are the 5 question signatures from `MockTest-Template.hs`. Memorise the shapes; the exam will give you very similar signatures.

```haskell
-- Question 1 (Rose tree)
isNBranching :: Int -> Rose a -> Bool
prune        :: Int -> Rose a -> Rose a

-- Question 2 (Generic Monad)
applyNTimes  :: Monad m => m a -> (a -> m a) -> Int -> m [a]

-- Question 3 (State monad / Nim)
gameOver     :: NimGame Bool
takeTokens   :: Int -> Heap -> NimGame ()

-- Question 4 (Matrix predicate)
isMagicSquare :: [[Int]] -> Bool

-- Question 5 (ADT translation)
circuit :: Expr -> Circuit
```

Where, in `Types.hs`:

```haskell
data Rose a = Leaf a | Branch [Rose a] deriving Show
type NimBoard = (Int, Int)
type NimGame a = State NimBoard a
data Heap = First | Second
data Expr    = Var Char | Not Expr | And Expr Expr | Or Expr Expr | Implies Expr Expr deriving (Eq, Show)
data Circuit = Input Char | Nand Circuit Circuit deriving (Eq, Show)
```

---

## Common deviations — DO NOT MAKE

### D1. Adding constraints

The marker imports your function with the EXACT constraint set. Adding `Eq a =>`, `Ord a =>`, `Show a =>` to "be safer" makes the marker's instantiation at, say, `Int -> Rose () -> Bool` fail because `()` is not `Ord`.

```haskell
-- WRONG
isNBranching :: (Eq a, Ord a) => Int -> Rose a -> Bool

-- RIGHT (no constraint — the function ignores `a`)
isNBranching :: Int -> Rose a -> Bool
```

### D2. Removing constraints

If the template says `Monad m =>`, you can't remove it. The marker passes a `Monad`-constrained value; without the constraint your code may even fail to type-check.

```haskell
-- WRONG
applyNTimes :: m a -> (a -> m a) -> Int -> m [a]

-- RIGHT
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
```

### D3. Renaming type variables

`Monad m =>` with `m` vs `Monad t =>` with `t` is logically identical, but the marker's `qualified import` matches by structure — usually OK, but a DIFFERENT-shape sig (e.g. `forall a. ...` vs no quantifier) can break. Don't risk it.

```haskell
-- WRONG (technically works but uses ScopedTypeVariables-adjacent syntax)
applyNTimes :: forall a m. Monad m => m a -> (a -> m a) -> Int -> m [a]

-- RIGHT
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
```

### D4. Argument reordering

The marker calls `Student.applyNTimes mx mf n`. If you swapped to `applyNTimes n mx mf`, the marker's call type-fails or returns garbage.

```haskell
-- WRONG (swap)
applyNTimes :: Monad m => Int -> m a -> (a -> m a) -> m [a]

-- RIGHT
applyNTimes :: Monad m => m a -> (a -> m a) -> Int -> m [a]
```

### D5. Type alias substitution

Template said `NimGame Bool`. You expanded it to `State (Int, Int) Bool`. Logically identical — but the marker's reference uses the type alias, and substituting may trip equality checks downstream (especially when GHC infers a slightly different type via constraints).

```haskell
-- WRONG (technically OK but unsafe)
gameOver :: State (Int, Int) Bool

-- RIGHT (template-verbatim alias)
gameOver :: NimGame Bool
```

### D6. Function name casing

Haskell is case-sensitive. `isNBranching` ≠ `isNbranching` ≠ `isnbranching`.

```haskell
-- WRONG
isnBranching :: Int -> Rose a -> Bool
isNbranching :: Int -> Rose a -> Bool
isNBRANCHING :: Int -> Rose a -> Bool

-- RIGHT
isNBranching :: Int -> Rose a -> Bool
```

### D7. Pluralisation / minor renames

```haskell
-- WRONG
gameOvers     :: NimGame Bool     -- pluralised
takeTok       :: Int -> Heap -> NimGame ()    -- abbreviated
isMagic       :: [[Int]] -> Bool                -- shortened
applyNTimesM  :: Monad m => ...                 -- "M" suffix added
```

### D8. Forgetting an export

The export list in `module MockTest ( … ) where` lists the names. If you delete one (or comment it out), the marker can't import it.

```haskell
-- WRONG
module MockTest ( isNBranching, prune ) where        -- only 2 of 7

-- RIGHT
module MockTest ( isNBranching
                , prune
                , applyNTimes
                , gameOver
                , takeTokens
                , isMagicSquare
                , circuit
                ) where
```

### D9. Adding new exports for "helpers"

Don't add `, helper1, helper2` to the export list. Helpers should be local (in `where` clauses) or unexported. Adding exports is harmless but indicates you misunderstand the contract — and might add a name that conflicts with the marker.

### D10. Generalising `Int` to `Num a => a`

```haskell
-- WRONG (over-generalised)
prune :: Num a => a -> Rose b -> Rose b

-- RIGHT (template-verbatim)
prune :: Int -> Rose a -> Rose a
```

The marker passes a concrete `Int`. Generalising compiles but the marker's call `Student.prune 3 (Branch [...])` will refuse to defaultpick `Int` if `a` is fully polymorphic in a typeclass context.

### D11. Adding `IO` or other monads

```haskell
-- WRONG (added IO for "convenience")
isMagicSquare :: [[Int]] -> IO Bool

-- RIGHT
isMagicSquare :: [[Int]] -> Bool
```

The marker uses the signature literally. Adding `IO` is type-incompatible.

---

## The `Types.hs` import — NEVER MODIFY

`Types.hs` for each exam is pinned. The header says:

```
-- DO **NOT** MODIFY THIS FILE
```

You may NOT:
- Change `data Rose a = Leaf a | Branch [Rose a]` to use different ctor names
- Add deriving clauses
- Reorder constructors
- Add new type aliases
- Add or remove imports from Types.hs

You MUST:
- Import `Types` from your answer file (it should already be there)
- Use the EXACT constructor names the file gives you

If your local IDE deletes `Types.hs` "because it's autogenerated", restore it from the template before submitting.

---

## The `Signatures.hs` regeneration trick (presubmit)

`presubmit.sh` regenerates a `Signatures.hs` that re-exports each required function with its exact signature. Then it tries to compile a tiny stub that imports both `MockTest` and `Signatures` and uses them in matched positions. If your signature differs from the template's, this stub fails to compile.

**Implication:** if `presubmit.sh` complains about `Signatures.hs`, you've changed a signature. Diff against the template line-by-line.

---

## How to verify your signatures match (60-second drill)

1. Open the template (`MockTest-Template.hs` or equivalent).
2. Open your answer (`MockTest.hs`).
3. For each function:
   - Eye your type sig line.
   - Eye the template's type sig line.
   - Compare character-by-character. NO deviations.
4. Compare the `module MockTest ( … ) where` line. Same.
5. Compare the import block. Same (or you've added an allowed import).

If anything differs, REVERT to the template's version and add only the implementation body.

---

## Function name discipline — "do not change function name even by casing"

Beyond the obvious:
- Don't add suffixes (`isNBranching'` ≠ `isNBranching`)
- Don't introduce a wrapper (`isNBranching n t = isNBranchingHelper n t` is fine as long as the OUTER `isNBranching` exists with the right type)
- Don't redefine a function in a `where` block AND at top level
- Don't typo the underscore — `is_n_branching` ≠ `isNBranching`

---

## The "constraint accidentally inferred" trap

If you OMIT a type signature, GHC infers one. The inferred sig may have extra `Eq a =>` constraints (because you used `==`) or `Show a =>` constraints (because you used `show`). The marker then can't call your function at types lacking those instances.

**Always write the type signature explicitly. Don't let GHC infer.**

```haskell
-- WRONG (no sig — GHC infers (Eq a) =>)
helper xs = filter (\x -> x == head xs) xs    -- inferred: Eq a => [a] -> [a]

-- RIGHT (explicit sig matches what marker expects)
helper :: Eq a => [a] -> [a]                  -- OR don't write this if marker expects no constraint
helper xs = filter (\x -> x == head xs) xs
```

If the template provides a sig with no constraint, your IMPLEMENTATION must also have no constraint. Rewrite to avoid `==` etc.

---

## Cross-references

- `HIGH-severity.md` P-001, P-002, P-013, P-025 — full code examples for the worst signature bugs
- `imports-pitfalls.md` — the import discipline (separate trap)
- [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) U7 — what the marker tests on signature mismatch
- `archetypes/A##.md` — canonical types for each archetype
- [ONE-PAGE-PANIC](../exam-day/ONE-PAGE-PANIC.md) — quick reference

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
