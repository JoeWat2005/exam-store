<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [trees](./README.md) · **Tree Functor / Foldable / Traversable instances**

<!-- siblings:start -->
> **Peers:** [binary-tree](./binary-tree.md) · [bst-delete-trace](./bst-delete-trace.md) · [bst](./bst.md) · [expression-tree](./expression-tree.md) · [rose-tree](./rose-tree.md) · [tree-counting](./tree-counting.md) · [tree-fold](./tree-fold.md) · **tree-functor** · [tree-traversals](./tree-traversals.md) · [tree-validation](./tree-validation.md) · [tree-zipper](./tree-zipper.md)
<!-- siblings:end -->






# Tree Functor / Foldable / Traversable instances

The three big tree typeclasses. Once you have these, you get `fmap`, `foldr`, `length`, `sum`, `toList`, `mapM`, `traverse`, `sequence` *for free*.

Problems 125 and 126 ask explicitly for Functor instances on binary and rose trees. Problem 109 asks for `mapMTree`. All three are derivable from Traversable.

## Binary tree

### Functor BT

```haskell
data BT a = Empty | Fork a (BT a) (BT a) deriving Show

instance Functor BT where
  fmap :: (a -> b) -> BT a -> BT b
  fmap _ Empty        = Empty
  fmap f (Fork x l r) = Fork (f x) (fmap f l) (fmap f r)
```
This IS `mapBT` from problem 77. The functor laws:
- `fmap id == id` — by induction on BT: Empty case `fmap id Empty = Empty = id Empty`. Fork case `fmap id (Fork x l r) = Fork (id x) (fmap id l) (fmap id r) = Fork x l r` by IH.
- `fmap (f . g) == fmap f . fmap g` — same structure of induction.

### Foldable BT

```haskell
instance Foldable BT where
  foldr :: (a -> b -> b) -> b -> BT a -> b
  foldr _ z Empty        = z
  foldr f z (Fork x l r) = foldr f (f x (foldr f z r)) l
  -- in-order: leftmost element ends up innermost in the resulting f chain

  -- alternatively, derive from foldMap:
  -- foldMap :: Monoid m => (a -> m) -> BT a -> m
  -- foldMap _ Empty        = mempty
  -- foldMap f (Fork x l r) = foldMap f l <> f x <> foldMap f r
```
Once Foldable is declared you get free:
```haskell
length      :: BT a -> Int                  -- (= size)
null        :: BT a -> Bool                 -- (= isEmpty)
elem        :: Eq a => a -> BT a -> Bool    -- (= member, generic)
sum         :: Num a => BT a -> a
product     :: Num a => BT a -> a
maximum     :: Ord a => BT a -> a           -- (errors on Empty)
toList      :: BT a -> [a]                  -- (= flattenInOrder)
any, all    :: (a -> Bool) -> BT a -> Bool
```

### Traversable BT

```haskell
instance Traversable BT where
  traverse :: Applicative f => (a -> f b) -> BT a -> f (BT b)
  traverse _ Empty        = pure Empty
  traverse f (Fork x l r) = Fork <$> f x <*> traverse f l <*> traverse f r
```
Once Traversable is declared:
```haskell
mapM       :: Monad m => (a -> m b) -> BT a -> m (BT b)        -- (= mapMTree, problem 109)
sequence   :: Monad m => BT (m a) -> m (BT a)
sequenceA  :: Applicative f => BT (f a) -> f (BT a)
```

#### mapMTree (problem 109) is just traverse
```haskell
mapMTree :: Monad m => (a -> m b) -> BT a -> m (BT b)
mapMTree _ Empty        = return Empty
mapMTree f (Fork x l r) = do
    y  <- f x
    l' <- mapMTree f l
    r' <- mapMTree f r
    return (Fork y l' r')

-- equivalent (Applicative style):
mapMTree' :: Monad m => (a -> m b) -> BT a -> m (BT b)
mapMTree' f Empty        = return Empty
mapMTree' f (Fork x l r) = Fork <$> f x <*> mapMTree' f l <*> mapMTree' f r
```

#### labelTree (problem 112) via Traversable + State
```haskell
import Control.Monad.State

labelTree :: BT a -> BT (Int, a)
labelTree t = evalState (traverse label t) 0
  where
    label :: a -> State Int (Int, a)
    label x = do n <- get; put (n+1); return (n, x)
-- visits in the order traverse defines (root → left → right with the Applicative above)
-- if you want in-order: swap the order in the Applicative `<*>` calls in the Traversable instance,
-- or thread State by hand with a recursive helper
```

## Rose tree (variant A, `Branch a [Rose a]`)

### Functor Rose
```haskell
data Rose a = Branch a [Rose a]

instance Functor Rose where
  fmap f (Branch x ts) = Branch (f x) (map (fmap f) ts)
```

### Foldable Rose
```haskell
instance Foldable Rose where
  foldr f z (Branch x ts) = f x (foldr (\t acc -> foldr f acc t) z ts)
  -- pre-order traversal; the outer foldr is over the children list
```

### Traversable Rose
```haskell
instance Traversable Rose where
  traverse f (Branch x ts) = Branch <$> f x <*> traverse (traverse f) ts
  -- the outer `traverse` walks the list; the inner one walks each Rose
```

## Rose tree (variant B, `Leaf a | Branch [Rose a]`)

### Functor Rose
```haskell
data Rose a = Leaf a | Branch [Rose a]

instance Functor Rose where
  fmap f (Leaf x)    = Leaf (f x)
  fmap f (Branch ts) = Branch (map (fmap f) ts)
```
This is problem 126.

### Foldable Rose (variant B)
```haskell
instance Foldable Rose where
  foldr f z (Leaf x)    = f x z
  foldr f z (Branch ts) = foldr (\t acc -> foldr f acc t) z ts
```

### Traversable Rose (variant B)
```haskell
instance Traversable Rose where
  traverse f (Leaf x)    = Leaf <$> f x
  traverse f (Branch ts) = Branch <$> traverse (traverse f) ts
```

## Expression tree

Because `Expr` from [expression-tree.md](expression-tree.md) doesn't carry a type parameter `a`, the standard Functor instance doesn't apply. *But* if you parameterise it:

```haskell
data Expr a = Val a
            | Var String
            | Add (Expr a) (Expr a)
            | Mul (Expr a) (Expr a)
            -- ...

instance Functor Expr where
  fmap f (Val n)     = Val (f n)
  fmap _ (Var x)     = Var x
  fmap f (Add e1 e2) = Add (fmap f e1) (fmap f e2)
  fmap f (Mul e1 e2) = Mul (fmap f e1) (fmap f e2)

instance Foldable Expr where
  foldr f z (Val n)     = f n z
  foldr _ z (Var _)     = z
  foldr f z (Add e1 e2) = foldr f (foldr f z e2) e1
  foldr f z (Mul e1 e2) = foldr f (foldr f z e2) e1

instance Traversable Expr where
  traverse g (Val n)     = Val <$> g n
  traverse _ (Var x)     = pure (Var x)
  traverse g (Add e1 e2) = Add <$> traverse g e1 <*> traverse g e2
  traverse g (Mul e1 e2) = Mul <$> traverse g e1 <*> traverse g e2
```

## DeriveFunctor / DeriveFoldable / DeriveTraversable

For exam answers, **don't** use `deriving (Functor, Foldable, Traversable)` — write the instances by hand. The course expects you to know the recursion. (And `{-# LANGUAGE Safe #-}` in assignments forbids generic deriving extensions.)

## Functor laws (proofs by induction)

```
Law 1:  fmap id == id
Law 2:  fmap (g . f) == fmap g . fmap f
```

Proof of Law 1 for `BT`:
- Base: `fmap id Empty = Empty = id Empty`. ✓
- Step: assume `fmap id l == id l` and `fmap id r == id r`. Then
  ```
  fmap id (Fork x l r)
    = Fork (id x) (fmap id l) (fmap id r)     -- def of fmap
    = Fork x l r                              -- by IH and id x = x
    = id (Fork x l r)                         -- def of id
  ```

QuickCheck the laws:
```haskell
prop_fmapId    t       = fmap id t == t
prop_fmapComp  t f g   = fmap (g . f) t == fmap g (fmap f t)
prop_foldrIsToList t   = foldr (:) [] t == toList t
prop_lenIsSize t       = length t == size t
prop_sumIsSumBT t      = sum t == sumBT t
```

## Cross-references

- Generic foldT and how Foldable derives from it: [tree-fold.md](tree-fold.md)
- Functor archetype (generic): [../archetypes/06-functor-instance.md](../archetypes/A06-functor-instance.md)
- map / mapM / traverse across all containers: [../monads/mapM-traverse.md](../monads/generic-combinators.md), [../typeclasses/traversable.md](../typeclasses/traversable.md)
- Tree × State (labelTree): [../cross-matrix/tree-x-state.md](../cross-matrix/tree-x-state.md)
- Tree × Maybe (validate-then-build): [../cross-matrix/tree-x-maybe.md](../cross-matrix/tree-x-maybe.md)
- Problems: 70 (Functor Maybe), 109 (mapMTree), 112 (labelTree), 125 (Functor BT), 126 (Functor Rose)

## See also

**Archetypes:** [A06 functor instance](../archetypes/A06-functor-instance.md) · [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Question families:** [functor-instance](../question-families/functor-instance-family.md) · [tree-transform](../question-families/tree-transform-family.md)
**QuickCheck:** [typeclass-instance attacks](../quickcheck/typeclass-instance-attacks.md)
**Related (trees):** [binary tree](./binary-tree.md) · [tree transform family](../question-families/tree-transform-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
