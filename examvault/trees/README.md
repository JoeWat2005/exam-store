<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · **trees**

# Trees — Archetype Overview

Trees are the #1 archetype in Birmingham FP. Mock Q1 is a Rose tree. Assignment 2 was wholesale tree recursion. Lectures Data1.md / Data2.md spend most of their pages on trees. Practice problems 71–90 are all trees.

If you see ANY recursive ADT, you are doing tree recursion.

## The four tree types you must own

| Type | Declaration | Where it appears |
|------|-------------|------------------|
| **Binary tree** | `data BT a = Empty \| Fork a (BT a) (BT a)` | Data1.md, problems 71–80, Assignment 2 (`ramify`/`tabulate`) |
| **BST** (same type, sorted invariant) | same as BT | Data2.md `isBST/insert/delete`, problems 81–85 |
| **Rose A (no leaf)** | `data Rose a = Branch a [Rose a]` | Data2.md lecture, problems 86–88 |
| **Rose B (explicit leaf)** | `data Rose a = Leaf a \| Branch [Rose a]` | **Mock Q1** — `isNBranching`, `prune` |
| **Expression tree** | `data Expr = Val Int \| Add Expr Expr \| ...` | Data2.md, problems 89–90, Mock Q5 (Expr→Circuit), problem 148 (Let bindings) |

## Which file for which question

| If the question says... | Open... |
|-------------------------|---------|
| "binary tree", `Empty`/`Fork`, count, height, mirror, flatten | [binary-tree.md](binary-tree.md) |
| "binary search tree", `insert`/`member`/`delete`, sorted, `Ord a` | [bst.md](bst.md) |
| "rose tree" with `Branch a [Rose a]` (no leaf constructor) | [rose-tree.md](rose-tree.md) §A |
| "rose tree" with `Leaf a \| Branch [Rose a]` (Mock Q1 shape) | [rose-tree.md](rose-tree.md) §B |
| "expression", `Val`, `Add`, `Mul`, eval, simplify, vars | [expression-tree.md](expression-tree.md) |
| Functor / Foldable / Traversable for a tree | [tree-functor.md](tree-functor.md) |
| "generic recursor", `foldT`, build all ops from one combinator | [tree-fold.md](tree-fold.md) |
| Preorder / inorder / postorder / BFS / paths | [tree-traversals.md](tree-traversals.md) |
| Zipper / focus / edit-in-place on a tree | [tree-zipper.md](tree-zipper.md) |
| "count nodes/leaves/where p", `count :: ... -> BT a -> Int` | [tree-counting.md](tree-counting.md) |
| "is balanced / sorted / N-branching / a BST / complete / mirror" | [tree-validation.md](tree-validation.md) |

## The canonical recursion shape

Every tree function has the same skeleton:

```haskell
f :: BT a -> r
f Empty        = base                           -- stop
f (Fork x l r) = combine x (f l) (f r)          -- step

-- Rose variant A
g :: Rose a -> r
g (Branch x ts) = combine x (map g ts)

-- Rose variant B (Mock Q1)
h :: Rose a -> r
h (Leaf x)    = baseL x
h (Branch ts) = combineB (map h ts)
```

The whole exam reduces to: *which constructor stops? what does each step produce?*

## Cross-references

- Folds over trees (Foldable + custom): [tree-fold.md](tree-fold.md), [../typeclasses/foldable.md](../typeclasses/foldable.md)
- mapM / traverse over trees: [../monads/mapM-traverse.md](../monads/generic-combinators.md), [tree-functor.md](tree-functor.md)
- State-monad walks (labelTree, countLeaves): [../monads/state.md](../monads/state.md), [../cross-matrix/tree-x-state.md](../cross-matrix/tree-x-state.md)
- Expr trees as interpreter ASTs: [../interpreters/simple-eval.md](../interpreters/simple-arith.md), [../interpreters/env-eval.md](../interpreters/expr-reader.md)
- ADT-to-ADT translation (Expr → Circuit, Mock Q5): [../archetypes/05-adt-translation.md](../archetypes/A05-adt-translation.md)
- BST as an archetype: [../archetypes/11-bst.md](../archetypes/A11-bst-ops.md)
- Zipper archetype: [../archetypes/17-zipper.md](../archetypes/A17-zipper.md)

## QuickCheck attack surface (applies to every tree type)

For every operation, throw it these:
- `Empty` / smallest non-empty (single Leaf)
- one-sided (`Fork x t Empty` repeated) — *left spine* and *right spine*
- balanced / perfect binary tree of depth 4
- very deep (10⁵ nodes, careful with non-tail recursion)
- random `Arbitrary` tree via `fromList` of random list

If you write a property: *what invariant should hold after this function?* That is the property.

## Lecture-faithful naming

These are the constructor names Martín uses in lectures and assignments. Don't rename to be cute — graders match against the spec.

- **Data1.md / Data2.md / problems 71–85:** `BT a = Empty | Fork a (BT a) (BT a)`
- **Mock Q1:** `Rose a = Leaf a | Branch [Rose a]`
- **Data2 §rosetrees:** `Rose a = Branch a [Rose a]`
- **Assignment 2 (`ramify`/`tabulate`):** `Tree = Empty | Branch (Maybe Char) Tree Tree`
- **Game trees (Data2):** `GameTree b m = Node b [(m, GameTree b m)]`
- **Permutation trees (Data2):** `Tree a = EBranch [(a, Tree a)]`

Constructor names vary — when in doubt, paste the question's declaration into your editor first.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
