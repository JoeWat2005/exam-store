<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [trees](./README.md) · **Tree Zippers — focus + breadcrumbs**

<!-- siblings:start -->
> **Peers:** [binary-tree](./binary-tree.md) · [bst-delete-trace](./bst-delete-trace.md) · [bst](./bst.md) · [expression-tree](./expression-tree.md) · [rose-tree](./rose-tree.md) · [tree-counting](./tree-counting.md) · [tree-fold](./tree-fold.md) · [tree-functor](./tree-functor.md) · [tree-traversals](./tree-traversals.md) · [tree-validation](./tree-validation.md) · **tree-zipper**
<!-- siblings:end -->






# Tree Zippers — focus + breadcrumbs

A zipper lets you focus on a subtree, edit it in O(1), then reconstruct the whole tree. It's the functional equivalent of "pointer to a node + path back to the root".

## The classic binary-tree zipper

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

-- A "crumb" remembers the parent's value, the sibling subtree, and which side we descended.
data Crumb a = LeftCrumb  a (BT a)   -- went L; saved (parent value, right sibling)
             | RightCrumb a (BT a)   -- went R; saved (parent value, left sibling)
             deriving (Show, Eq)

type Breadcrumbs a = [Crumb a]            -- innermost crumb at the head
type Zipper      a = (BT a, Breadcrumbs a)  -- (current focus, path back to the root)
```
Top-of-tree:
```haskell
fromTree :: BT a -> Zipper a
fromTree t = (t, [])
```

## Navigation

```haskell
goLeft :: Zipper a -> Maybe (Zipper a)
goLeft (Empty,        _ ) = Nothing
goLeft (Fork x l r,   bs) = Just (l, LeftCrumb x r : bs)
-- descend into left subtree; remember (value, right sibling)

goRight :: Zipper a -> Maybe (Zipper a)
goRight (Empty,        _ ) = Nothing
goRight (Fork x l r,   bs) = Just (r, RightCrumb x l : bs)
-- descend into right subtree; remember (value, left sibling)

goUp :: Zipper a -> Maybe (Zipper a)
goUp (_,                       []                   ) = Nothing
goUp (t, LeftCrumb  x rSibling : bs) = Just (Fork x t rSibling, bs)
goUp (t, RightCrumb x lSibling : bs) = Just (Fork x lSibling t, bs)
-- rebuild the parent Fork using the saved sibling
```

## Reconstruction (zip back up to the root)

```haskell
toTree :: Zipper a -> BT a
toTree (t, [])     = t
toTree z           = case goUp z of
    Just z' -> toTree z'
    Nothing -> fst z

-- equivalent monadic version:
toTree' :: Zipper a -> BT a
toTree' = fst . untilNothing goUp
  where untilNothing f x = maybe x (untilNothing f) (f x)
```

## Edit (the whole point)

```haskell
modify :: (BT a -> BT a) -> Zipper a -> Zipper a
modify f (t, bs) = (f t, bs)
-- f sees only the focused subtree

setFocus :: BT a -> Zipper a -> Zipper a
setFocus t' (_, bs) = (t', bs)

getFocus :: Zipper a -> BT a
getFocus = fst
```

```haskell
-- example: replace the focused value (only on a Fork; no-op on Empty)
setRoot :: a -> Zipper a -> Zipper a
setRoot v = modify rep
  where
    rep Empty        = Fork v Empty Empty
    rep (Fork _ l r) = Fork v l r
```

## Following an address

```haskell
data Direction = L | R
goByAddr :: [Direction] -> Zipper a -> Maybe (Zipper a)
goByAddr []     z = Just z
goByAddr (L:ds) z = goLeft  z >>= goByAddr ds
goByAddr (R:ds) z = goRight z >>= goByAddr ds
```

## A worked example — increment the value at address `[L, R]`

```haskell
incrAt :: Num a => [Direction] -> BT a -> Maybe (BT a)
incrAt addr t = do
    z  <- goByAddr addr (fromTree t)
    let z' = modify incr z
    return (toTree z')
  where
    incr Empty        = Empty
    incr (Fork x l r) = Fork (x + 1) l r
```

## Why use a zipper?

For one-off edits: `incrAt` could be done by recursion through the tree (returning a new tree along the way) — O(d) where d is the depth, same as the zipper.

The win comes from **repeated, local edits**:
- "increment the focus, then move left, then increment, then move right…" — each step is O(1) with a zipper but O(d) per step with a re-traversal.
- An expression-tree editor / interpreter that walks an AST is the canonical use case.

The course rarely *requires* a zipper — it's a beautiful pattern more than an exam mainstay — but it can simplify "navigate-and-edit" problems and appears in interview questions and Assignment 3-style work.

## Rose tree zipper (variant A)

```haskell
data Rose a = Branch a [Rose a]

data RCrumb a = RCrumb a [Rose a] [Rose a]
-- (parent value, left siblings reversed, right siblings)

type RZipper a = (Rose a, [RCrumb a])

goChild :: Int -> RZipper a -> Maybe (RZipper a)
goChild i (Branch x ts, bs)
    | i < 0 || i >= length ts = Nothing
    | otherwise               = Just (ts !! i, RCrumb x ls rs : bs)
  where (ls, t:rs) = splitAt i ts

goUpR :: RZipper a -> Maybe (RZipper a)
goUpR (_, [])                       = Nothing
goUpR (t, RCrumb x ls rs : bs) = Just (Branch x (reverse ls ++ [t] ++ rs), bs)
```

## QuickCheck

```haskell
prop_zipperRoundTrip t           = (toTree . fromTree) t == t
prop_goLeftUpId t                = case goLeft (fromTree t) of
    Just z  -> fmap toTree (goUp z) == Just t
    Nothing -> True
prop_modifyIdentity t            = (toTree . modify id . fromTree) t == t
prop_setGet v t                  = case fromTree t of
    z -> case modify (const Empty) z of
        z' -> getFocus z' == Empty
prop_goByAddrValid t addr        = case goByAddr addr (fromTree t) of
    Just _  -> isValid addr t
    Nothing -> not (isValid addr t)
```

## Mutations

| Want | Add |
|------|-----|
| undo/redo | keep a stack of Zippers (a Zipper-of-Zippers) |
| typed edits at the focus | `modify :: (BT a -> Maybe (BT a)) -> Zipper a -> Maybe (Zipper a)` |
| Game-tree zipper | replace `Fork a l r` with `Node b [(m, GameTree b m)]` and adjust Crumb |
| Expression-tree zipper | one Crumb constructor per Expr constructor (e.g. `AddL Expr` for "went left in an Add") |
| Compute path on the fly | `breadcrumbs` already IS the path; map crumb→direction |

## Pitfalls

- Forgetting to reverse the breadcrumb stack: `[]` is the root, the *head* is the *innermost* crumb. `toTree` already handles this correctly via repeated `goUp`, but if you write a custom rebuilder remember which end is which.
- `goLeft (Empty, _)` returns `Nothing`. Don't accidentally return `Just (Empty, ...)` — there's no left subtree of an Empty tree.
- For the Rose zipper, `RCrumb x ls rs` stores left siblings in **reverse order** for O(1) prepend. Forgetting `reverse ls` in `goUpR` will produce a scrambled tree.
- A zipper is *not* a mutable pointer. `modify f z` returns a new zipper; `z` is unchanged.
- If you write a zipper for `Expr`, the Crumb type has one constructor per binary constructor of Expr (plus one per side). For `Add Expr Expr` you get `AddL Expr` (we're at the left, parent had right child = Expr) and `AddR Expr`. Don't try to share crumbs across constructors.

## Cross-references

- Zipper archetype: [../archetypes/A17-zipper.md](../archetypes/A17-zipper.md)
- Binary tree base ops: [binary-tree.md](binary-tree.md)
- Tree addresses (the un-zippered version): [binary-tree.md §Paths and addresses](binary-tree.md)
- General resource: Huet's "The Zipper" (1997), Journal of Functional Programming

## See also

**Archetypes:** [A17 zipper](../archetypes/A17-zipper.md) · [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Question families:** [tree-transform](../question-families/tree-transform-family.md)
**QuickCheck:** [trees attacks](../quickcheck/trees-attacks.md)
**Related (trees):** [binary tree](./binary-tree.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
