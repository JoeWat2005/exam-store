<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: Rose trees**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · **rose** · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: Rose trees

**Search keywords:** Rose, Leaf, Branch, [Rose a], n-branching, isNBranching, prune, Mock Q1, branching factor, Branch [], 0-branching, vacuous, multi-way tree, Free, Pure, Free []

The Mock Test Q1 uses `Rose`. This is the canonical rose-tree pattern.

## What the marker generates

Direct from `MockTestTestCases.hs`:

```haskell
data Rose a = Leaf a | Branch [Rose a]

-- The "true" generator (N-branching tree):
genNBranching n = sized $ \m -> do
    k <- chooseInt (0, m)
    go k n where
      go 0 n = Leaf <$> arbitrary
      go k n = do
        k' <- chooseInt (0, k - 1)
        Branch <$> replicateM n (go k' n)
```

- The generator picks a max-depth `k` then builds a tree where every `Branch` has exactly `n` children. Leaves can appear at any level.

```haskell
-- The "arbitrary" generator (NOT necessarily N-branching):
gen_not_NBranching n = sized $ \m -> do
    k <- chooseInt (0, m)
    go k n where
      go 0 n = Leaf <$> arbitrary
      go k n = do
        k' <- chooseInt (0, k - 1)
        n' <- chooseInt (0, maxBranches)  -- maxBranches = 9
        Branch <$> replicateM n' (go k' n)
```

- Each `Branch` has `n' ∈ [0, 9]` children — so **`Branch []` IS in the input space**.

```haskell
-- Base case generator (1 leaf only):
genRoseBaseCase = do
       n <- genLess10                          -- n ∈ [0, 9]
       t <- Leaf <$> arbitrary
       return (n, t)
```

- This is for the 2-mark base case test. The marker tries `(n, Leaf x)` for `n ∈ [0, 9]`. Your `isNBranching n (Leaf _)` must return `True` for any `n`.

```haskell
-- Recursive case generator:
genRoseRecursiveCase = do
       h <- chooseInt (3, 4)
       resize h $ do
         n <- genLess10
         t <- replicateM n (genNBranching n)
         return (n, Branch t)
```

- A `Branch` with exactly `n` children, each being an N-branching tree of depth 3-4. Sets you up to test that you correctly use `length xs == n && all (isNBranching n) xs`.

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | `Leaf x` (any value, any n) | `(5, Leaf 42)` | Base case wrong → 2-mark gate test fails → recursive case test not run at all | `isNBranching _ (Leaf _) = True` |
| 2 | `Branch []` with `n == 0` | `(0, Branch [])` | Pattern non-exhaustive; or you return `False` because "no children" | `length [] == 0 && all _ [] == True` → returns `True`. Default `length xs == n && all (isNBranching n) xs` handles it. |
| 3 | `Branch []` with `n > 0` | `(3, Branch [])` | Wrongly returns `True` because you only checked subtrees, not root | `length xs == n` returns `False`. Good. |
| 4 | `Branch [Leaf 1, Leaf 2]` with `n == 2` | `(2, Branch [Leaf 1, Leaf 2])` | Off-by-one in length check | `length xs == 2 && all (isNBranching 2) [Leaf 1, Leaf 2]` — leaves pass vacuously |
| 5 | Branch with too-few children | `(3, Branch [Leaf 1, Leaf 2])` | `length xs == n` correctly returns False | Standard check |
| 6 | Branch with too-many children | `(2, Branch [Leaf 1, Leaf 2, Leaf 3])` | Same | Standard check |
| 7 | **Branch correct at root but wrong deep inside** | `(2, Branch [Leaf 1, Branch [Leaf 1, Leaf 2, Leaf 3]])` | If you only check root, you say `True` — WRONG | `all (isNBranching n) xs` catches this |
| 8 | Deep N-branching tree (5-10 levels) | size knob 10, depth 5-10 | Stack overflow on accumulator-heavy code | `all` short-circuits; fine |
| 9 | Tree with `n = 0` (no branching at all) | `(0, Branch [])` is 0-branching | If you assume `n >= 1` you exclude this | Make sure `n == 0` is handled |
| 10 | Tree with `n = 1` (every branch has one child) | `(1, Branch [Branch [Branch [Leaf 0]]])` | Skewed-spine — should pass | `length xs == 1 && all ... xs` |
| 11 | `prune n (Leaf x)` | `(5, Leaf 42)` | Spec says identity. If you return `Leaf x` for any `n`, good. If you transform it, bad. | `prune _ (Leaf x) = Leaf x` |
| 12 | `prune n (Branch xs)` with `length xs > n` | `(2, Branch [Leaf 1, Leaf 2, Leaf 3])` → should give `Branch [pruned Leaf 1, pruned Leaf 2]` | Forgetting to recurse into children leaves them with too many children further down | `prune n (Branch xs) = Branch (take n (map (prune n) xs))` |
| 13 | `prune n (Branch xs)` with `length xs < n` | `(5, Branch [Leaf 1])` | Take is safe — `take 5 [x] = [x]` | Standard `take` handles this |
| 14 | `prune 0 _` | `(0, Branch [Leaf 1, Leaf 2])` → `Branch []` | Returning `Empty` (wrong constructor) or crashing | `take 0 _ = []` so result is `Branch []` |
| 15 | `prune n` is checked semantically: result must be `(n-1)-branching` after pruning to `n-1` | `prop_PruneNBranching` calls `isNBranching (n-1) (prune (n-1) t)` and checks it's `True` | If you only prune the root, inner branches keep their original count | Recurse all the way down |
| 16 | Polymorphism: `Rose a` not just `Rose Int` | `Rose Char`, `Rose String` | Don't bake `Int` into your signature | Use the template's signature verbatim |

## Property templates

```haskell
import Test.QuickCheck
import Control.Monad (replicateM)

data Rose a = Leaf a | Branch [Rose a] deriving (Show, Eq)

-- N-branching gen modelled on Mock Q1
genNBranching :: Arbitrary a => Int -> Gen (Rose a)
genNBranching n = sized $ \m -> do
    k <- chooseInt (0, m)
    go k
  where
    go 0 = Leaf <$> arbitrary
    go k = do
      k' <- chooseInt (0, k - 1)
      Branch <$> replicateM n (go k')

-- Base case must always return True
prop_isNBranching_baseLeaf :: Int -> Int -> Bool
prop_isNBranching_baseLeaf n x = isNBranching n (Leaf x)

-- An N-branching tree IS N-branching
prop_isNBranching_constructedTrue :: Property
prop_isNBranching_constructedTrue = forAll (chooseInt (0, 5)) $ \n ->
  forAll (genNBranching n :: Gen (Rose Int)) $ \t ->
    isNBranching n t

-- prune is idempotent for leaves
prop_prune_leafId :: Int -> Int -> Bool
prop_prune_leafId n x = prune n (Leaf x) == Leaf x

-- prune to (n-1) of an N-branching tree gives (n-1)-branching
prop_prune_makes_n_minus_1 :: Property
prop_prune_makes_n_minus_1 = forAll (chooseInt (1, 5)) $ \n ->
  forAll (genNBranching n :: Gen (Rose Int)) $ \t ->
    isNBranching (n - 1) (prune (n - 1) t)

-- Round-trip: prune n already-N-branching is identity (mostly)
prop_prune_keep_self :: Property
prop_prune_keep_self = forAll (chooseInt (0, 5)) $ \n ->
  forAll (genNBranching n :: Gen (Rose Int)) $ \t ->
    prune n t == t   -- if n matches branching, take n is identity
```

## Self-test before submission checklist

- [ ] `isNBranching n (Leaf x) == True` for ALL `n`, ALL `x`
- [ ] `isNBranching 0 (Branch []) == True`
- [ ] `isNBranching n (Branch []) == False` for `n > 0`
- [ ] `isNBranching n (Branch xs)` checks BOTH `length xs == n` AND `all (isNBranching n) xs`
- [ ] `prune n (Leaf x) == Leaf x` for ALL `n`
- [ ] `prune n (Branch xs)` recurses with `map (prune n) xs` BEFORE taking
- [ ] `prune 0 (Branch [...]) == Branch []`
- [ ] After `prune (n-1) t`, the result is `(n-1)-branching`
- [ ] Function works for negative `n` too (or has guard), if not specified to be non-negative
- [ ] Polymorphic — no `Int` baked in unless spec restricts

## Pitfalls that specifically lose QC marks

### Pitfall: base case returns False
```haskell
-- WRONG: thinks a leaf cannot be N-branching
isNBranching n (Leaf _) = False
-- The 2-mark base case test asserts True for ANY n on a Leaf.
-- Fix:
isNBranching _ (Leaf _) = True
```

### Pitfall: only checks the root branching count
```haskell
-- WRONG: doesn't recurse into children
isNBranching _ (Leaf _) = True
isNBranching n (Branch xs) = length xs == n
-- For Branch [Branch [Leaf 1, Leaf 2, Leaf 3], Branch []] with n=2:
-- root has 2 children, passes — but inner Branch has 3, second inner has 0
-- Fix:
isNBranching n (Branch xs) = length xs == n && all (isNBranching n) xs
```

### Pitfall: `prune` only prunes top level
```haskell
-- WRONG:
prune n (Leaf x)    = Leaf x
prune n (Branch xs) = Branch (take n xs)
-- For Branch [Branch [Leaf 1, Leaf 2, Leaf 3, Leaf 4]] with n=2:
-- root pruned to 1 child (since only 1) ← fine
-- inner Branch still has 4 children ← BUG
-- Fix:
prune n (Leaf x)    = Leaf x
prune n (Branch xs) = Branch (take n (map (prune n) xs))
```

### Pitfall: order of `take` and `map`
```haskell
-- BOTH WORK and give the same result, but:
prune n (Branch xs) = Branch (take n (map (prune n) xs))  -- recurses on ALL, then takes
prune n (Branch xs) = Branch (map (prune n) (take n xs))  -- takes FIRST, then recurses
-- Second version is slightly more efficient (saves recursion on dropped children).
-- BUT — they produce IDENTICAL results because pruning is structural.
-- Either is fine for marks.
```

### Pitfall: wrong constructor name
```haskell
-- WRONG (using BST constructors):
isNBranching n Empty = True              -- Empty isn't in Rose
isNBranching n (Node x l r) = ...
-- Use Rose constructors:
isNBranching n (Leaf _) = ...
isNBranching n (Branch xs) = ...
```

### Pitfall: importing `Data.Sequence (Seq(Empty))` and shadowing
The user has been bitten by this:
```haskell
import Data.Sequence (Seq(Empty))   -- imports Empty constructor
-- Now `Empty` refers to Seq, not your Rose / BST type. Confusing errors.
```
**Don't import unused things from editor auto-complete.**

### Pitfall: `length` on rose tree children is fine but...
```haskell
isNBranching n (Branch xs) = length xs == n && ...
-- `length xs` is O(n) but xs is the children list, not the whole tree.
-- For QC-sized trees this is fine.
```

## Connection to Free monad (Assignment 3 Q1)

Assignment 3 uses `Free [] a` which is structurally equivalent to `Rose a`:

```haskell
data Free f a = Pure a | Free (f (Free f a))
-- Free [] a ≅ Rose a:
--   Pure x       ≅ Leaf x
--   Free [...]   ≅ Branch [...]
```

The marker tests `toRose . fromRose == id` and `fromRose . toRose == id`. The attacks are identical: `Pure x` = `Leaf x`, `Free []` = `Branch []`. The same edge cases apply.

```haskell
prop_roundTripRose r       = toRose (fromRose r) === r
prop_roundTripFree f       = fromRose (toRose f) === f
prop_structurePreserved r  = roseShape (toRose (fromRose r)) === roseShape r
```

## See also

**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Cross-topic:** [rose × state](../cross-matrix/rose-x-state.md) · [rose × writer](../cross-matrix/rose-x-writer.md)
**Question families:** [rose-ops](../question-families/rose-ops-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
