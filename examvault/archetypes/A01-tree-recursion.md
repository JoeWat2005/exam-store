<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [archetypes](./README.md) · **A01 — Tree-ADT Structural Recursion**

<!-- siblings:start -->
> **Peers:** **A01** · [A02](./A02-state-game.md) · [A03](./A03-generic-monad.md) · [A04](./A04-matrix-predicate.md) · [A05](./A05-adt-translation.md) · [A06](./A06-functor-instance.md) · [A07](./A07-codec-pair.md) · [A08](./A08-env-eval.md) · [A09](./A09-prelude-reimpl.md) · [A10](./A10-fold-reformulation.md) · [A11](./A11-bst-ops.md) · [A12](./A12-rep-conversion.md) · [A13](./A13-pretty-printer.md) · [A14](./A14-multi-effect-interp.md) · [A15](./A15-writer-trace.md) · [A16](./A16-parser-combinators.md) · [A17](./A17-zipper.md) · [A18](./A18-lazy-memo.md) · [A19](./A19-extend-interpreter.md) · [A20](./A20-laws-iso.md) · [A21](./A21-list-comp-synthesis.md) · [A22](./A22-typeclass-instance.md) · [A23](./A23-mini-game.md) · [A24](./A24-applicative-instance.md)
<!-- siblings:end -->






# A01 — Tree-ADT Structural Recursion

**Tier:** 1   |   **Stars:** ⭐⭐⭐⭐⭐
**Mock appearance:** Q1, Q5   |   **Assignment appearance:** A2 (whole), A3 (Q1)
**Combines with:** A02 · A03 · A05 · A06 · A08 · A11 · A15
**Search keywords:** tree · ADT · structural recursion · BT · Rose · forest · pattern match constructors

## What it tests
Whether you can read a custom recursive ADT, write one equation per constructor, and combine the results from recursive calls correctly — the single most reusable Haskell skill.

## Recognition triggers
- "Consider the following data type … `data T = … | … (T) (T) …`"
- "Write a function `_ :: T -> _` which …"
- type signature shape: `T -> Int`, `T -> Bool`, `T -> [a]`, `T a -> T b`
- "predicate", "count", "flatten", "mirror", "depth", "height", "label", "every node"
- The question gives a custom data type T with constructors `Leaf | Branch …` or `Empty | Fork …` or `Lf | Nd …` — yes, that's this archetype.
- You see a `forest :: [T]` field — the recursive case will need `map f forest` or `all p forest`.

## Canonical template
```haskell
-- Generic shape (binary):
data BT a = Empty | Fork a (BT a) (BT a)

f :: BT a -> r
f Empty        = base
f (Fork x l r) = combine x (f l) (f r)

-- Generic shape (rose / forest):
data Rose a = Leaf a | Branch [Rose a]

g :: Rose a -> r
g (Leaf x)      = baseLeaf x
g (Branch xs)   = combineBranch (map g xs)
```

## Mutations (the examiner picks one)

### M1 — predicate (`isNBranching`, Mock Q1)
```haskell
isNBranching :: Int -> Rose a -> Bool
isNBranching _ (Leaf _)      = True
isNBranching n (Branch xs)   = length xs == n && all (isNBranching n) xs
```
What changes: result is `Bool`, base is `True`, recursive case `&&`s a local check with `all rec children`.

### M2 — transformation that re-builds the tree (`prune`, Mock Q1)
```haskell
prune :: Int -> Rose a -> Rose a
prune _ (Leaf x)    = Leaf x
prune n (Branch xs) = Branch (take n (map (prune n) xs))
```
What changes: result is same shape; recurse THEN trim. `take n . map rec` not `map rec . take n` (both work here but reverse becomes wrong for `dropWhile`-style).

### M3 — measure: `size` (count nodes)
```haskell
sizeBT :: BT a -> Int
sizeBT Empty        = 0
sizeBT (Fork _ l r) = 1 + sizeBT l + sizeBT r
```
What changes: numeric base 0, additive combine. Use `1` not the stored value.

### M4 — measure with max: `height`
```haskell
heightBT :: BT a -> Int
heightBT Empty        = 0
heightBT (Fork _ l r) = 1 + max (heightBT l) (heightBT r)
```
What changes: `+` becomes `max`. **Empty = 0** (course convention), so a singleton fork has height 1.

### M5 — flatten (collect values to list)
```haskell
flattenInOrder :: BT a -> [a]
flattenInOrder Empty        = []
flattenInOrder (Fork x l r) = flattenInOrder l ++ [x] ++ flattenInOrder r
```
What changes: result is `[a]`, combine with `++`. Switch the position of `[x]` to get pre/post-order.

### M6 — map (preserve shape, change values)
```haskell
mapBT :: (a -> b) -> BT a -> BT b
mapBT _ Empty        = Empty
mapBT f (Fork x l r) = Fork (f x) (mapBT f l) (mapBT f r)
```
What changes: type-level transformation; constructor passes through unchanged; `f` applied to stored value only.

### M7 — mirror (structural transform with swap)
```haskell
mirror :: BT a -> BT a
mirror Empty        = Empty
mirror (Fork x l r) = Fork x (mirror r) (mirror l)
```
What changes: recurse on l/r but plug them in the OPPOSITE slot. Combination of M6's shape-preservation with a constructor-level twist.

### M8 — extract leaves only
```haskell
leavesBT :: BT a -> [a]
leavesBT Empty                 = []
leavesBT (Fork x Empty Empty)  = [x]
leavesBT (Fork _ l r)          = leavesBT l ++ leavesBT r
```
What changes: an extra pattern for "leaf forks". Three clauses, NOT two — easy to forget.

### M9 — depth / level-aware (carry an index down)
```haskell
labelDepth :: Int -> Rose a -> Rose (a, Int)
labelDepth d (Leaf x)    = Leaf (x, d)
labelDepth d (Branch xs) = Branch (map (labelDepth (d+1)) xs)
```
What changes: extra accumulating parameter. Initial call uses depth 0.

### M10 — count of a value (Eq constraint)
```haskell
countBT :: Eq a => a -> BT a -> Int
countBT _ Empty        = 0
countBT v (Fork x l r) = (if x == v then 1 else 0) + countBT v l + countBT v r
```
What changes: predicate at the stored value, `Eq` constraint on `a`.

## Worked examples from this course
- Mock Q1: `isNBranching :: Int -> Rose a -> Bool` and `prune :: Int -> Rose a -> Rose a` — see M1, M2.
- Mock Q5: `circuit :: Expr -> Circuit` — A05 lives on top of this.
- Problem sheet Sets 8 & 9 (#71-90): `sizeBT`, `heightBT`, `leavesBT`, `mirror`, `flattenInOrder`, `mapBT`, `sumBT`, `maxBT`, `countBT`, `sizeRose`, `heightRose`, `flattenRose`, `evalExpr`, `depthExpr`.
- Assignment 2 (Morse): the `Tree` type with `Branch (Maybe Char) Tree Tree` is consumed structurally in `decodeTextWithTree`, `tabulate`.
- Assignment 3 Q1: `toRose`, `fromRose` are structural recursions on `Rose` and `Free [] a`.

## QuickCheck attack surface
The auto-marker will throw at you:
- **`Empty` / `Leaf x`** alone — every clause must accept the smallest tree.
- **One-sided trees** (`Fork x Empty (Fork y Empty Empty)`) — catches non-symmetric bugs like always-recurse-left.
- **Deep right-spines** length 1000+ — catches accidental quadratic structure (e.g. `flatten t ++ [x]` style).
- **Empty branch list** for Rose (`Branch []`) — `isNBranching` must return `n == 0`. Distinct from `Leaf`.
- Property checks: `length (flatten t) == size t`, `mirror (mirror t) == t`, `height (mirror t) == height t`, `size (mapBT f t) == size t`.

## Pitfalls (marks-killers)
- **Shallow check** on Rose: `isNBranching n (Branch xs) = length xs == n` forgets `&& all (isNBranching n) xs`. Symptom: passes top-level but fails any nested test.
- **Non-exhaustive patterns**: if you write `f (Fork x l r) = …` but never handled `Empty`, GHC warns and the marker crashes with `Non-exhaustive patterns in function f`.
- **Swapping l/r**: only `mirror` (and similar) needs it; copy-pasting `mirror`'s skeleton into `flatten` is a typical bug.
- **Constructor name confusion**: `Branch` (in Rose) ≠ `Branch` (in Assignment 2 Tree); the latter has a `Maybe Char` field. Read the type definition every time.
- **Forgetting the `Empty` base case** in question stems that say "a tree with at least one node" — they still test on `Empty` to force `Maybe` return or `error`.

## Combines-with deep dive

### A01 × A02 — labelling tree with State
```haskell
labelTree :: BT a -> State Int (BT (Int, a))
labelTree Empty        = return Empty
labelTree (Fork x l r) = do l' <- labelTree l
                            n  <- get; put (n+1)
                            r' <- labelTree r
                            return (Fork (n, x) l' r')
```

### A01 × A03 — `Monad m =>` mapM over a tree
```haskell
mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)
mapMTree _ Empty        = return Empty
mapMTree f (Fork x l r) = do x' <- f x
                             l' <- mapMTree f l
                             r' <- mapMTree f r
                             return (Fork x' l' r')
```

### A01 × A06 — Functor for the tree
```haskell
instance Functor BT where
  fmap _ Empty        = Empty
  fmap f (Fork x l r) = Fork (f x) (fmap f l) (fmap f r)
```

## See also

**Combines with:** [A02 state game](./A02-state-game.md) · [A03 generic monad](./A03-generic-monad.md) · [A05 ADT translation](./A05-adt-translation.md) · [A06 functor instance](./A06-functor-instance.md) · [A08 env eval](./A08-env-eval.md) · [A11 BST ops](./A11-bst-ops.md) · [A15 writer trace](./A15-writer-trace.md)
**Question families:** [tree-counting](../question-families/tree-counting-family.md) · [tree-validation](../question-families/tree-validation-family.md) · [tree-transform](../question-families/tree-transform-family.md) · [tree-extract](../question-families/tree-extract-family.md) · [rose-ops](../question-families/rose-ops-family.md)
**Cross-topic:** [tree × state](../cross-matrix/tree-x-state.md) · [tree × writer](../cross-matrix/tree-x-writer.md) · [tree × maybe](../cross-matrix/tree-x-maybe.md) · [tree × either](../cross-matrix/tree-x-either.md) · [tree × reader](../cross-matrix/tree-x-reader.md) · [tree × generic monad](../cross-matrix/tree-x-generic-monad.md) · [rose × state](../cross-matrix/rose-x-state.md) · [rose × writer](../cross-matrix/rose-x-writer.md)
**Theory:** [binary tree](../trees/binary-tree.md) · [rose tree](../trees/rose-tree.md) · [tree fold](../trees/tree-fold.md) · [tree functor](../trees/tree-functor.md) · [tree traversals](../trees/tree-traversals.md)
**Pitfalls:** [P-005 missing base case](../pitfalls/HIGH-severity.md#p-005) · [P-014 shallow recursion](../pitfalls/HIGH-severity.md#p-014) · [P-017 non-exhaustive pattern](../pitfalls/HIGH-severity.md#p-017) · [P-022 base case first](../pitfalls/HIGH-severity.md#p-022)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md) · [rose attacks](../quickcheck/rose-attacks.md)
**Mock-Q:** [Mock Q1 (isNBranching, prune)](../indexes/MOCK-Q-INDEX.md#mock-q1) · [Mock Q5 (circuit)](../indexes/MOCK-Q-INDEX.md#mock-q5)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
