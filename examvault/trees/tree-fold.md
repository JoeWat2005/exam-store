<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [trees](./README.md) · **Tree folds — `foldBT` and `foldRose`**

<!-- siblings:start -->
> **Peers:** [binary-tree](./binary-tree.md) · [bst-delete-trace](./bst-delete-trace.md) · [bst](./bst.md) · [expression-tree](./expression-tree.md) · [rose-tree](./rose-tree.md) · [tree-counting](./tree-counting.md) · **tree-fold** · [tree-functor](./tree-functor.md) · [tree-traversals](./tree-traversals.md) · [tree-validation](./tree-validation.md) · [tree-zipper](./tree-zipper.md)
<!-- siblings:end -->






# Tree folds — `foldBT` and `foldRose`

A tree fold is one combinator from which every tree recursion derives. Master this and you stop writing the same recursion ten times.

## The one definition that runs the whole show — `foldBT`

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

foldBT :: (a -> b -> b -> b)    -- f: how to combine a Fork's value with the two folded subtrees
       -> b                      -- e: what Empty becomes
       -> BT a
       -> b
foldBT _ e Empty        = e
foldBT f e (Fork x l r) = f x (foldBT f e l) (foldBT f e r)
```

The shape `(a -> b -> b -> b)` mirrors the constructor `Fork :: a -> BT a -> BT a -> BT a`. This is no coincidence — it's the *catamorphism* on BT.

## Every binary-tree operation as a one-liner

```haskell
sizeF      :: BT a -> Int
sizeF      = foldBT (\_ l r -> 1 + l + r) 0

heightF    :: BT a -> Int
heightF    = foldBT (\_ l r -> 1 + max l r) 0

sumF       :: Num a => BT a -> a
sumF       = foldBT (\x l r -> x + l + r) 0

productF   :: Num a => BT a -> a
productF   = foldBT (\x l r -> x * l * r) 1

leavesF    :: BT a -> Int
leavesF    = foldBT step 0
  where step _ 0 0 = 1                     -- both children "Empty-like"
        step _ l r = l + r

mirrorF    :: BT a -> BT a
mirrorF    = foldBT (\x l r -> Fork x r l) Empty

mapBTF     :: (a -> b) -> BT a -> BT b
mapBTF f   = foldBT (\x l r -> Fork (f x) l r) Empty

toListInF  :: BT a -> [a]
toListInF  = foldBT (\x l r -> l ++ [x] ++ r) []

toListPreF :: BT a -> [a]
toListPreF = foldBT (\x l r -> x : (l ++ r)) []

toListPostF :: BT a -> [a]
toListPostF = foldBT (\x l r -> l ++ r ++ [x]) []

anyF       :: (a -> Bool) -> BT a -> Bool
anyF p     = foldBT (\x l r -> p x || l || r) False

allF       :: (a -> Bool) -> BT a -> Bool
allF p     = foldBT (\x l r -> p x && l && r) True

elemF      :: Eq a => a -> BT a -> Bool
elemF y    = anyF (== y)

countF     :: (a -> Bool) -> BT a -> Int
countF p   = foldBT (\x l r -> (if p x then 1 else 0) + l + r) 0
```
The pattern is always: *what's the value at Empty? what's the combination at Fork?*

## Foldable from foldBT

```haskell
instance Foldable BT where
  foldr f z = foldBT (\x lAcc rAcc -> lAcc . (f x .) . rAcc $ z) (const id) -- if you wanted to
  -- in practice, just write foldr directly (see tree-functor.md), but the above shows it derives
```

## Generic Rose fold — variant A

```haskell
data Rose a = Branch a [Rose a]

foldRoseA :: (a -> [b] -> b) -> Rose a -> b
foldRoseA g (Branch x ts) = g x (map (foldRoseA g) ts)
```

```haskell
sizeRA    = foldRoseA (\_ bs -> 1 + sum bs)
heightRA  = foldRoseA (\_ bs -> if null bs then 0 else 1 + maximum bs)
sumRA     = foldRoseA (\x bs -> x + sum bs)
flattenRA = foldRoseA (\x bs -> x : concat bs)
mapRoseA f = foldRoseA (\x bs -> Branch (f x) bs)
anyRA p   = foldRoseA (\x bs -> p x || or bs)
allRA p   = foldRoseA (\x bs -> p x && and bs)
```

## Generic Rose fold — variant B (Mock Q1)

```haskell
data Rose a = Leaf a | Branch [Rose a]

foldRoseB :: (a -> b)        -- at Leaf
          -> ([b] -> b)       -- at Branch (combining children-results)
          -> Rose a
          -> b
foldRoseB lf _  (Leaf x)    = lf x
foldRoseB lf br (Branch ts) = br (map (foldRoseB lf br) ts)
```

```haskell
sizeRB     = foldRoseB (const 1) (\bs -> 1 + sum bs)
heightRB   = foldRoseB (const 0) (\bs -> if null bs then 0 else 1 + maximum bs)
leavesRB   = foldRoseB (const 1) sum
flattenRB  = foldRoseB (:[]) concat
mapRoseB f = foldRoseB (Leaf . f) Branch
sumRB      = foldRoseB id sum
anyRB p    = foldRoseB p or
allRB p    = foldRoseB p and
```

## Mutations and extensions

| Add | Change to fold |
|-----|----------------|
| depth-aware fold | wrap as `Int -> r`; pass increasing depth in the recursive calls |
| accumulator | use `b -> r` (continuation-passing) |
| Index-aware fold on Rose | use `zip [0..] ts` then fold |
| Side effects | go monadic: `foldBTM :: Monad m => (a -> b -> b -> m b) -> b -> BT a -> m b` |
| Two-argument result | `(b,c)` as `b`; project at the end |

### foldBT with depth

```haskell
foldBTd :: (Int -> a -> b -> b -> b) -> b -> BT a -> b
foldBTd f e = go 0
  where
    go _ Empty        = e
    go d (Fork x l r) = f d x (go (d+1) l) (go (d+1) r)

-- e.g. count nodes at exactly depth k:
countAtDepth :: Int -> BT a -> Int
countAtDepth k = foldBTd (\d _ l r -> (if d == k then 1 else 0) + l + r) 0
```

### Monadic fold

```haskell
foldBTM :: Monad m => (a -> b -> b -> m b) -> b -> BT a -> m b
foldBTM _ e Empty        = return e
foldBTM f e (Fork x l r) = do
    bl <- foldBTM f e l
    br <- foldBTM f e r
    f x bl br
```
Used for: counting in State, accumulating Writer logs, short-circuit failure in Either/Maybe.

## When NOT to use foldBT

- When you need to return a new `BT` *structured* like the input but with extra info (e.g. labelling) — `traverse` is usually clearer.
- When the operation depends on the *path* from the root (you'd need to thread an accumulator; use a custom recursion or pass an `Address`).
- When you want laziness in just one subtree (e.g. short-circuit `any p`). `foldBT` forces both subtree results. For lazy short-circuit you need a custom version with `||` between two recursive calls.

## QuickCheck

```haskell
-- The fold should agree with the direct definition
prop_foldSize    t = sizeF t  == size t
prop_foldHeight  t = heightF t == height t
prop_foldMap f   t = mapBTF f t == mapBT f t

-- Fusion law: foldBT f e . mapBT g == foldBT (\x l r -> f (g x) l r) e
prop_fusion g f e t = (foldBT f e . mapBT g) t
                   == foldBT (\x l r -> f (g x) l r) e t
```

## Pitfalls

- The Empty case of `foldBT f e (Fork x l r)` is *unused* if you start with `Empty` as base — you never combine an Empty with anything at the Empty level. The base `e` only matters because every Fork eventually bottoms out at Empty in its subtree recursions.
- For `mirrorF`, *swap* l and r in the continuation: `Fork x r l`. Forgetting that gives you `id` instead of `mirror`.
- For `mapBTF`, the children `l, r` are already-mapped *trees*, not the originals. Don't try to recurse manually inside the fold — that's what the fold did for you.
- `foldBT (\x l r -> ...) e` always recurses on BOTH children. If you want short-circuit (e.g. find: walk only until found), write the recursion directly.
- For `heightRA` you must guard the empty children list — `maximum []` crashes. `if null bs` or `0 : map` are the standard fixes.
- Naming: the lecture sometimes calls this a *catamorphism*; "fold" and "cata" are synonymous here.

## Cross-references

- Concrete operations on BT: [binary-tree.md](binary-tree.md)
- Concrete operations on Rose: [rose-tree.md](rose-tree.md)
- Foldable instances (where these connect to the Prelude): [tree-functor.md](tree-functor.md), [../typeclasses/foldable.md](../typeclasses/foldable.md)
- Generic fold archetype: [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)
- List foldr/foldl (for analogy): [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)
- Problem 102 — `foldr` on lists — every tree fold is the same idea

## See also

**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)
**Question families:** [tree-counting](../question-families/tree-counting-family.md) · [list-fold](../question-families/list-fold-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md)
**Related (trees):** [binary tree](./binary-tree.md) · [tree traversals](./tree-traversals.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
