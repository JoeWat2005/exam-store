<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [trees](./README.md) · **Rose Trees — both variants**

<!-- siblings:start -->
> **Peers:** [binary-tree](./binary-tree.md) · [bst-delete-trace](./bst-delete-trace.md) · [bst](./bst.md) · [expression-tree](./expression-tree.md) · **rose-tree** · [tree-counting](./tree-counting.md) · [tree-fold](./tree-fold.md) · [tree-functor](./tree-functor.md) · [tree-traversals](./tree-traversals.md) · [tree-validation](./tree-validation.md) · [tree-zipper](./tree-zipper.md)
<!-- siblings:end -->






# Rose Trees — both variants

Rose trees branch on a list of children, not a pair. Two variants appear in the course. *Read the question's data declaration before writing anything.*

---

## Variant A — `data Rose a = Branch a [Rose a]` (lecture Data2.md, problems 86–88)

Every node carries a value; "leaf" means `Branch x []` (empty child list). There is no separate Leaf constructor. Size is always ≥ 1.

### Type
```haskell
data Rose a = Branch a [Rose a] deriving (Show, Eq)
```

### Canonical shape
```haskell
f :: Rose a -> r
f (Branch x ts) = combine x (map f ts)        -- one rule; recurse via map
```

### Core ops (Variant A)
```haskell
sizeR :: Rose a -> Int
sizeR (Branch _ ts) = 1 + sum (map sizeR ts)
-- 1 because the root always counts; empty children list ⇒ size 1
```

```haskell
heightR :: Rose a -> Int
heightR (Branch _ []) = 0
heightR (Branch _ ts) = 1 + maximum (map heightR ts)
-- The empty-list case MUST go first; otherwise `maximum []` crashes.
-- Lecture-convention: a "leaf" Branch x [] has height 0.
```

```haskell
heightR' :: Rose a -> Int
heightR' (Branch _ ts) = maximum (0 : map (\t -> 1 + heightR' t) ts)
-- alternative: seed with 0 so the empty-list case is handled without a special clause
```

```haskell
leavesR :: Rose a -> Int
leavesR (Branch _ []) = 1
leavesR (Branch _ ts) = sum (map leavesR ts)
```

```haskell
flattenR :: Rose a -> [a]
flattenR (Branch x ts) = x : concatMap flattenR ts
-- pre-order; for post-order: concatMap flattenR ts ++ [x]
```

```haskell
mapRose :: (a -> b) -> Rose a -> Rose b
mapRose f (Branch x ts) = Branch (f x) (map (mapRose f) ts)
-- this IS the Functor instance — see tree-functor.md
```

```haskell
pathsR :: Rose a -> [[a]]
pathsR (Branch x []) = [[x]]
pathsR (Branch x ts) = [x:p | t <- ts, p <- pathsR t]
-- all root-to-leaf paths as value lists
```

```haskell
sumR :: Num a => Rose a -> a
sumR (Branch x ts) = x + sum (map sumR ts)
```

### Generic fold (Variant A)
```haskell
foldRose :: (a -> [b] -> b) -> Rose a -> b
foldRose g (Branch x ts) = g x (map (foldRose g) ts)

-- one-line specialisations:
sizeR'    = foldRose (\_ bs -> 1 + sum bs)
heightR'' = foldRose (\_ bs -> if null bs then 0 else 1 + maximum bs)
flattenR' = foldRose (\x bs -> x : concat bs)
sumR'     = foldRose (\x bs -> x + sum bs)
```

---

## Variant B — `data Rose a = Leaf a | Branch [Rose a]` (Mock Q1, problem 143)

Two constructors. Values live only at `Leaf`s. `Branch` nodes carry no value, just children.

### Type (verbatim from Mock Q1 Types.hs)
```haskell
data Rose a = Leaf a
            | Branch [Rose a]
            deriving Show
```

### Canonical shape
```haskell
f :: Rose a -> r
f (Leaf x)    = baseL x
f (Branch ts) = combineB (map f ts)
```

### Mock Q1 solutions (verbatim)

```haskell
-- isNBranching n t: every Branch in t has exactly n children
isNBranching :: Int -> Rose a -> Bool
isNBranching n (Leaf _)        = True
isNBranching n (Branch forest) = length forest == n
                              && all (isNBranching n) forest

-- prune n t: keep only the first n children of every Branch
prune :: Int -> Rose a -> Rose a
prune n (Leaf x)        = Leaf x
prune n (Branch forest) = Branch $ take n $ map (prune n) forest
```
Notes on the Mock solutions:
- `isNBranching` is a *deep* predicate. Forgetting `&& all (isNBranching n) forest` is the #1 trap — checks only the root and is wrong.
- `prune` recurses *before* taking. `take n (map (prune n) forest)` and `map (prune n) (take n forest)` give different trees if children disagree on shape, but produce the same first n children either way — the lecture-solution uses `take n $ map ...`.

### Core ops (Variant B)
```haskell
sizeR :: Rose a -> Int
sizeR (Leaf _)    = 1
sizeR (Branch ts) = 1 + sum (map sizeR ts)
-- counts both Leafs and Branch nodes
```

```haskell
heightR :: Rose a -> Int
heightR (Leaf _)    = 0
heightR (Branch []) = 0
heightR (Branch ts) = 1 + maximum (map heightR ts)
```

```haskell
leavesR :: Rose a -> Int
leavesR (Leaf _)    = 1
leavesR (Branch ts) = sum (map leavesR ts)
```

```haskell
flattenR :: Rose a -> [a]
flattenR (Leaf x)    = [x]
flattenR (Branch ts) = concatMap flattenR ts
-- only leaf values; Branches carry no values
```

```haskell
mapRose :: (a -> b) -> Rose a -> Rose b
mapRose f (Leaf x)    = Leaf (f x)
mapRose f (Branch ts) = Branch (map (mapRose f) ts)
```

```haskell
pathsR :: Rose a -> [[Int]]
pathsR (Leaf _)    = [[]]
pathsR (Branch ts) = [i:p | (i,t) <- zip [0..] ts, p <- pathsR t]
-- paths as indices into the children
```

```haskell
sumR :: Num a => Rose a -> a
sumR (Leaf x)    = x
sumR (Branch ts) = sum (map sumR ts)
```

### Generic fold (Variant B)
```haskell
foldRose :: (a -> b)        -- at Leaf
         -> ([b] -> b)      -- at Branch
         -> Rose a
         -> b
foldRose leaf branch (Leaf x)    = leaf x
foldRose leaf branch (Branch ts) = branch (map (foldRose leaf branch) ts)

sizeR'      = foldRose (const 1) (\bs -> 1 + sum bs)
heightR'    = foldRose (const 0) (\bs -> if null bs then 0 else 1 + maximum bs)
flattenR'   = foldRose (:[]) concat
sumR'       = foldRose id sum
mapRose' f  = foldRose (Leaf . f) Branch
-- isNBranching' n = foldRose (const True) (\bs -> length bs == n && and bs) — not quite right since length applies to original ts not bs; you need the bs to also carry depth info
```

---

## Validation (both variants)

```haskell
-- A: every node has the same number of children (uniform branching)
isUniformA :: Rose a -> Bool
isUniformA (Branch _ ts) = all hasSameLen ts && all isUniformA ts
  where n = length (children (Branch undefined ts))
        hasSameLen t = length (children t) == n
        children (Branch _ cs) = cs

-- B: Mock Q1 isNBranching — see above
```

## Mutations (Variant B)

| Question wants | One-line change to template |
|----------------|-----------------------------|
| `isLBranching n` — at-least-n children | `length forest >= n && all ... forest` |
| `isExactlyNDeep n` — every leaf at depth n | thread depth in helper |
| `pruneIf p` — drop subtrees failing p | `Branch (filter p (map (pruneIf p) forest))` |
| `pruneDepth n` — cut at depth n | counter `0` at root, replace Branch with Leaf when out of budget |
| `replaceLeaves f` (Variant B) | recurse: `Leaf x -> f x; Branch ts -> Branch (map ... ts)` |
| `replaceAtPath p t v` | descend `p :: [Int]` via `(!!)` and `splitAt` |

## QuickCheck attack surface

```haskell
-- pathological inputs (Variant B)
mkLeaf   = Leaf 'a'
mkEmpty  = Branch []                                    -- "leaf" by structure
mkDeep n = foldr (\_ t -> Branch [t]) (Leaf 0) [1..n]   -- left spine of branches
mkWide n = Branch (replicate n (Leaf 0))                -- fan-out
mkFull d k                                              -- depth-d, k children per branch
  | d == 0    = Leaf 0
  | otherwise = Branch (replicate k (mkFull (d-1) k))

-- properties
prop_pruneSize n t       = sizeR (prune n t) <= sizeR t                  -- monotonic
prop_pruneIdempotent n t = prune n (prune n t) == prune n t              -- requires Eq
prop_isNBPrune n t       = isNBranching n (prune n (padded n t))         -- after padding
prop_flattenSize t       = length (flattenR t) == leavesR t              -- Variant B
prop_mapId t             = mapRose id t == t                             -- Functor law
prop_mapCompose f g t    = mapRose (f . g) t == mapRose f (mapRose g t)  -- Functor law
```

## Pitfalls (both variants — read these)

- **Variant A `heightR (Branch _ [])`** — `maximum []` crashes. Either special-case empty children, or seed with `0 : map ...`.
- **Variant B `flattenR (Branch _) = ...`** — Branches carry no values; don't write `x : concatMap ...`.
- **`isNBranching` MUST recurse** — shallow `length ts == n` is wrong. The Mock graders test trees where the *root* matches but a deep child doesn't.
- **`prune` recurses before taking** — `Branch (take n (map (prune n) ts))`. Mock solution uses `$` style: `Branch $ take n $ map (prune n) forest`.
- Don't confuse the variants. If you write `Leaf x` against Variant A's type you get *parse error*. Always paste the declaration first.
- Variant A's `Rose` is sometimes called a "non-empty rose tree"; Variant B is the "general" rose with explicit leaves.
- Lecture Data2.md uses Variant A. Mock Q1 uses Variant B. *Both* appear elsewhere in the wild — game trees use a third shape `Node b [(m, GameTree b m)]`.

## Cross-references

- Binary tree (for comparison): [binary-tree.md](binary-tree.md)
- Generic fold pattern: [tree-fold.md](tree-fold.md)
- Functor instances: [tree-functor.md](tree-functor.md)
- Mock Q1 walkthrough: [A01 tree recursion](../archetypes/A01-tree-recursion.md) (covers `isNBranching`/`prune`); see also the [rose-ops family](../question-families/rose-ops-family.md)
- Lecture: `fp-learning-2025/files/LectureNotes/Sections/Data2.md` §Rose trees
- Problems: 86–88 (sizeRose, heightRose, flattenRose), 126 (Functor Rose), 143 (Mock isNBranching, prune)

## See also

**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Cross-topic:** [rose × state](../cross-matrix/rose-x-state.md) · [rose × writer](../cross-matrix/rose-x-writer.md)
**Question families:** [rose-ops](../question-families/rose-ops-family.md)
**QuickCheck:** [rose attacks](../quickcheck/rose-attacks.md)
**Related (trees):** [binary tree](./binary-tree.md) · [tree fold](./tree-fold.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
