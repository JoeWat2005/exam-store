<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: binary & rose trees (structure)**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · **trees** · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: binary & rose trees (structure)

> **⚠ Constructor-name banner.** The examples below use a generic `Tree`/`Node` for readability, but **the course type is**
> ```haskell
> data BT a = Empty | Fork a (BT a) (BT a)
> ```
> — so `Node` here ≡ `Fork`, and the binary-tree empty case ≡ `Empty`. **Always substitute the exact constructor names from the question's own `Types` module** (it may use `BT`/`Fork`, `Tree`/`Node`, `Bin`/`Lf`/`Nd`, …). Never redefine the type yourself. The most-copied snippets (`size`, `mirror`, `flatten`, `mapBT`) are written in `BT`/`Empty`/`Fork` below so they paste straight onto the course type.

**Search keywords:** tree, BinTree, BinaryTree, Tree, BT, Empty, Leaf, Node, Fork, Branch, Lf, Br, skewed, balanced, deep, stack overflow, mirror, size, height, flatten, mapBT, foldBT, recurse

(BST-specific attacks live in `bst-attacks.md`. Rose-tree-specific attacks live in `rose-attacks.md`. This file is about structural attacks that apply to *any* tree.)

## What the marker generates

The marker has at least three tree shapes it deploys (assembled from Mock Q1, Assignment 2 Q3, Assignment 3 Q1):

```haskell
-- Mock Q1 rose-tree generator:
genNBranching n = sized $ \m -> do
    k <- chooseInt (0, m)
    go k n where
      go 0 n = Leaf <$> arbitrary
      go k n = do
        k' <- chooseInt (0, k - 1)
        Branch <$> replicateM n (go k' n)
```

So you get trees with **height up to `m`** (the size knob, default 10–30) and **exactly `n` children per branch** for the "true" case. The "false" case picks an arbitrary number of children `0..9` per branch.

```haskell
-- Assignment 3 binary-tree generator (Rose Int):
genRoseW = RoseW <$> genRoseSized
  where
    genRoseSized = sized gen
    gen 0 = Lf <$> arbitrary
    gen n = frequency
        [ (1, Lf <$> arbitrary)
        , (3, Br <$> resize (n `div` 2) (listOf (gen (n `div` 2))))
        ]
```

- Frequency `(1, Lf)` vs `(3, Br)` means **branches are 3x more common than leaves** at each node. Expect bushy trees, not skinny chains.
- `resize (n `div` 2)` halves the size knob at each step. Depth is logarithmic.

```haskell
-- Assignment 2 Bracket tree (effectively a non-empty-children-list tree):
goodBrackets tb = do
  n <- frequency [(3^k, return (16-k)) | k <- [0..16]]
  l <- vectorOf n (goodBrackets tb)
  ...
```

The `frequency [(3^k, return (16-k)) | k <- [0..16]]` is a power-law distribution favouring smaller children counts. Expect mostly small `Branch []` to `Branch [_,_]`, occasionally larger.

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | Empty tree | `Empty` for `BT a = Empty \| Fork a (BT a) (BT a)` | Non-exhaustive pattern → `*** Exception: Non-exhaustive patterns` | First clause: `f Empty = baseValue` |
| 2 | Empty `Leaf` rose tree (single leaf) | `Leaf x` for Mock Q1 | **Marker tests this FIRST** as a 2-mark gate. If you fail it, the recursive case test is skipped entirely. | `f (Leaf _) = baseValue` (the base case is dictated by the spec — `isNBranching n (Leaf _) = True`) |
| 3 | `Branch []` (empty children list) | `Branch []` | If you do `head children` or `xs !! 0`, you crash on this. For "is N-branching", `Branch []` is N-branching iff `n == 0`. | Pattern-match `Branch xs` and handle `xs == []` (or use `length xs`) |
| 4 | Single-node tree | `Fork x Empty Empty` | Off-by-one in size/depth counts | `size (Fork _ l r) = 1 + size l + size r` (correctly returns 1) |
| 5 | Skewed left | `Fork x (Fork y (Fork z Empty Empty) Empty) Empty` | Stack overflow on deep recursion; height/depth computed wrong | Use `max (height l) (height r) + 1` not just `height l + 1` |
| 6 | Skewed right | `Fork x Empty (Fork y Empty (Fork z Empty Empty))` | Same as above; also forgotten in iterators that go left-first | Test both shapes |
| 7 | Perfectly balanced | `Fork 4 (Fork 2 (Fork 1 e e) (Fork 3 e e)) (Fork 6 ...)` | Hides off-by-one because both sides equal | Test asymmetric tree too |
| 8 | Very deep (>1000 nodes) | Mock Q1 size knob 30 yields ~30-level branches per arm | `foldr` stack OK because lazy; `foldl'` better for accumulation | For `Bool` predicates, `all` short-circuits — safe |
| 9 | Duplicate values | `Fork 5 (Fork 5 e e) (Fork 5 e e)` | "find x" returns the wrong copy; counts wrong | Spec-dependent; usually OK if you use structural recursion |
| 10 | `Branch [Leaf _]` (one-child branch) | `Branch [Leaf 1]` | For "is N-branching": is this 1-branching? Yes if `n=1`. | Handled if you correctly compare `length xs == n` |
| 11 | Mixed-arity (Rose only) | `Branch [Leaf 1, Branch [], Leaf 2]` | Predicate "all subtrees are N-branching" — `Branch []` is only N-branching for `n == 0` | `all (isNBranching n) xs` does the right thing |
| 12 | Tree with `Char` instead of `Int` | `Fork 'a' Empty Empty` | Marker tests with both. Make sure your function is polymorphic when spec says so. | Don't accidentally specialise to `Int` |

## The four most-copied binary-tree functions (in course `BT`/`Empty`/`Fork`)

Paste these straight onto `data BT a = Empty | Fork a (BT a) (BT a)`. Every base case is `Empty`; every recursive case fires on **both** sub-trees.

```haskell
size :: BT a -> Int
size Empty        = 0
size (Fork _ l r) = 1 + size l + size r

mirror :: BT a -> BT a
mirror Empty        = Empty
mirror (Fork x l r) = Fork x (mirror r) (mirror l)   -- swap l/r at every node

flatten :: BT a -> [a]                               -- in-order
flatten Empty        = []
flatten (Fork x l r) = flatten l ++ [x] ++ flatten r

mapBT :: (a -> b) -> BT a -> BT b
mapBT _ Empty        = Empty
mapBT f (Fork x l r) = Fork (f x) (mapBT f l) (mapBT f r)  -- keeps l/r (does NOT swap)
```

## Property templates

```haskell
import Test.QuickCheck

-- Polymorphic test for tree size
prop_sizeNonNeg :: BT Int -> Bool
prop_sizeNonNeg t = size t >= 0

prop_sizeEmptyZero :: Bool
prop_sizeEmptyZero = size (Empty :: BT Int) == 0

prop_sizeSingleton :: Int -> Bool
prop_sizeSingleton x = size (Fork x Empty Empty) == 1

-- Mirror is involutive
prop_mirrorInvolutive :: BT Int -> Bool
prop_mirrorInvolutive t = mirror (mirror t) == t

-- Flatten gives back all elements
prop_flattenSize :: BT Int -> Bool
prop_flattenSize t = length (flatten t) == size t

-- mapBT preserves shape
prop_mapBTSize :: (Int -> Int) -> BT Int -> Bool
prop_mapBTSize f t = size (mapBT f t) == size t

prop_mapBTIdentity :: BT Int -> Bool
prop_mapBTIdentity t = mapBT id t == t

prop_mapBTComposition :: (Int -> Int) -> (Int -> Int) -> BT Int -> Bool
prop_mapBTComposition f g t = mapBT (f . g) t == mapBT f (mapBT g t)
```

### Generator for QuickCheck on `BT a`

If you want to test locally, define an `Arbitrary` instance modelled on the marker's:

```haskell
instance Arbitrary a => Arbitrary (BT a) where
  arbitrary = sized go
    where
      go 0 = pure Empty
      go n = frequency
        [ (1, pure Empty)
        , (3, Fork <$> arbitrary
                   <*> go (n `div` 2)
                   <*> go (n `div` 2)) ]
```

For Rose trees mirroring Mock Q1:

```haskell
instance Arbitrary a => Arbitrary (Rose a) where
  arbitrary = sized go
    where
      go 0 = Leaf <$> arbitrary
      go n = frequency
        [ (1, Leaf <$> arbitrary)
        , (3, Branch <$> resize (n `div` 2)
                                (listOf (go (n `div` 2)))) ]
```

## Self-test before submission checklist

- [ ] handles `Empty` / `Leaf x` (base case)
- [ ] handles single-node `Node x Empty Empty`
- [ ] handles `Branch []` for rose trees (zero-children case)
- [ ] handles skewed-left tree (does not assume `r` is non-empty)
- [ ] handles skewed-right tree (does not assume `l` is non-empty)
- [ ] handles deep tree (>30 levels — no stack overflow)
- [ ] handles tree with duplicate values
- [ ] recursion fires on EVERY subtree, not just the root
- [ ] result type matches signature (e.g. `Tree a -> [a]` returns `[]` for `Empty`, not `[undefined]`)
- [ ] polymorphic if spec says so (no `Int` baked in)

## Pitfalls that specifically lose QC marks

### Pitfall: predicate evaluated only at root
```haskell
-- WRONG: doesn't check that subtrees also satisfy the property
isNBranching n (Leaf _)     = True
isNBranching n (Branch xs)  = length xs == n
-- QC test: Branch [Leaf 1, Branch [Leaf 1, Leaf 2]] with n=1
-- length xs == 1 ✓ at root, but inner Branch has 2 children
-- Fix:
isNBranching n (Leaf _)     = True
isNBranching n (Branch xs)  = length xs == n && all (isNBranching n) xs
```

### Pitfall: mirror swaps l/r recursively but `size` shouldn't
```haskell
-- WRONG: mistakenly swaps
size (Fork _ l r) = 1 + size r + size l   -- harmless because + is commutative
-- vs
mapBT f (Fork x l r) = Fork (f x) (mapBT f r) (mapBT f l)
-- ↑ THIS swaps the tree — wrong for mapBT, right for mirror
```

### Pitfall: `Branch []` mis-classified
```haskell
-- WRONG: assumes Branch always has children
isNBranching n (Branch (x:xs)) = length (x:xs) == n && all (isNBranching n) (x:xs)
-- For Branch [], no pattern matches → exception
-- Fix:
isNBranching n (Branch xs) = length xs == n && all (isNBranching n) xs
-- length [] == 0, so Branch [] is 0-branching, not n-branching for n > 0
```

### Pitfall: forgot the Leaf base case for an "all leaves are X" check
```haskell
-- WRONG: returns False for Leaf
allLeavesPositive (Leaf x)    = x > 0   -- correct
allLeavesPositive (Branch xs) = all allLeavesPositive xs
-- BUT for vacuous case: what's allLeavesPositive (Branch [])?
-- all _ [] == True (good!)
-- BUT what does spec want? "no leaves at all" — vacuously satisfied
```

### Pitfall: deep recursion blows stack on left-accumulated count
```haskell
-- POTENTIALLY UNSAFE:
countNodes Empty = 0
countNodes (Fork _ l r) = 1 + countNodes l + countNodes r
-- For very skewed trees, the spine eats stack.
-- In practice, QC trees aren't deep enough to matter, but for very deep balanced trees
-- consider an accumulator-based version.
```

### Pitfall: structure-changing operation (prune)
Mock Q1 `prune n t`:
- Base case: `prune n (Leaf x) = Leaf x` — leaves are unchanged.
- Recursive: `prune n (Branch xs) = Branch (take n (map (prune n) xs))` — keep first `n` children, prune each.
- **The marker tests `prune n` then checks `isNBranching n result == True`.** So if you forget to recurse into pruned children, an inner branch might still have too many children.

```haskell
-- WRONG: only prunes top level
prune n (Branch xs) = Branch (take n xs)
-- Fix:
prune n (Leaf x)    = Leaf x
prune n (Branch xs) = Branch (take n (map (prune n) xs))
```

### Pitfall: forgot that `Leaf` ALSO needs to be handled in `prune`
The marker's `prop_Prune_base` is literally:
```haskell
prop_Prune_base (n, t@(Leaf x)) = Student.prune n t ~= t
```
So if your `prune` does anything other than identity on a `Leaf`, you fail this 2-mark test.

## See also

**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Cross-topic:** [tree × state](../cross-matrix/tree-x-state.md) · [tree × writer](../cross-matrix/tree-x-writer.md)
**Question families:** [tree-counting](../question-families/tree-counting-family.md) · [tree-validation](../question-families/tree-validation-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
