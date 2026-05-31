<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [trees](./README.md) · **BST delete: worked traces**

<!-- siblings:start -->
> **Peers:** [binary-tree](./binary-tree.md) · **bst-delete-trace** · [bst](./bst.md) · [expression-tree](./expression-tree.md) · [rose-tree](./rose-tree.md) · [tree-counting](./tree-counting.md) · [tree-fold](./tree-fold.md) · [tree-functor](./tree-functor.md) · [tree-traversals](./tree-traversals.md) · [tree-validation](./tree-validation.md) · [tree-zipper](./tree-zipper.md)
<!-- siblings:end -->






# BST delete — worked traces of the hard case

`delete x t` is easy in three of four sub-cases; the **two-children** case is where students lose marks. This page traces it twice — once using the **in-order successor**, once using the **predecessor** — on a concrete tree, with the call stack drawn.

The base ADT and signature used throughout (matches Birmingham course):

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

delete :: Ord a => a -> BT a -> BT a
delete _ Empty                              = Empty
delete x (Fork y l r)
  | x < y     = Fork y (delete x l) r
  | x > y     = Fork y l (delete x r)
  | otherwise = combine l r       -- the hard case lives in `combine`
```

The four-case dispatch is uncontroversial. All the difficulty hides in `combine :: BT a -> BT a -> BT a`. There are two textbook strategies.

## Strategy A — in-order successor

> When deleting a node with two children, replace its value with the smallest value in the right subtree, then delete that smallest value from the right subtree.

```haskell
combine :: BT a -> BT a -> BT a
combine Empty r = r
combine l Empty = l
combine l r     = Fork m l r'
  where (m, r') = extractMin r

extractMin :: BT a -> (a, BT a)
extractMin (Fork x Empty r) = (x, r)
extractMin (Fork x l     r) = let (m, l') = extractMin l
                              in  (m, Fork x l' r)
extractMin Empty = error "extractMin: empty tree"   -- never called from combine
```

### Trace: delete 5 from this tree

```
          5
        /   \
       3     8
      / \   / \
     2   4 6   9
              \
               7
```

The node to delete (`5`) has two children. We need `extractMin` from the right subtree:

```
extractMin (Fork 8 (Fork 6 Empty (Fork 7 Empty Empty)) (Fork 9 Empty Empty))
  -- left is NOT Empty, recurse
  = let (m, l') = extractMin (Fork 6 Empty (Fork 7 Empty Empty))
        -- inner: left IS Empty → return (6, Fork 7 Empty Empty)
        (m,  l') = (6, Fork 7 Empty Empty)
    in  (6, Fork 8 (Fork 7 Empty Empty) (Fork 9 Empty Empty))
```

So `combine l r = Fork 6 l (Fork 8 (Fork 7 Empty Empty) (Fork 9 Empty Empty))`.

After deletion:

```
          6
        /   \
       3     8
      / \   / \
     2   4 7   9
```

✓ BST invariant preserved. `6` (the smallest value > the deleted `5`) is now at the root.

## Strategy B — in-order predecessor

> Replace with the *largest* value in the *left* subtree.

```haskell
combine :: BT a -> BT a -> BT a
combine Empty r = r
combine l Empty = l
combine l r     = Fork m l' r
  where (m, l') = extractMax l

extractMax :: BT a -> (a, BT a)
extractMax (Fork x l Empty) = (x, l)
extractMax (Fork x l r    ) = let (m, r') = extractMax r
                              in  (m, Fork x l r')
extractMax Empty = error "extractMax: empty tree"
```

### Same trace: delete 5 from same tree

We need `extractMax` from the left subtree:

```
extractMax (Fork 3 (Fork 2 Empty Empty) (Fork 4 Empty Empty))
  -- right is NOT Empty, recurse
  = let (m, r') = extractMax (Fork 4 Empty Empty)
        -- right IS Empty → return (4, Empty)
        (m, r') = (4, Empty)
    in  (4, Fork 3 (Fork 2 Empty Empty) Empty)
```

So `combine l r = Fork 4 (Fork 3 (Fork 2 Empty Empty) Empty) (Fork 8 ...)`.

After deletion:

```
          4
        /   \
       3     8
      /     / \
     2     6   9
            \
             7
```

✓ Also valid. `4` (the largest value < the deleted `5`) is now at the root.

## Trace the recursive call stack

Both strategies have the same call structure: `delete` recurses down to the deleted node, calls `combine`, which calls `extractMin`/`extractMax`, which recurses down one side of the chosen subtree.

```
delete 5 (Fork 5 L R)
  → combine L R
    → extractMin R
      → extractMin (Fork 8 (Fork 6 ...) ...)
        → extractMin (Fork 6 Empty ...)
          ← returns (6, Fork 7 Empty Empty)
        ← rebuilds Fork 8 with new left
      ← (6, new-right-subtree)
    ← Fork 6 L new-right
  ← Fork 6 L new-right
```

Depth of recursion: `delete` depth + `extractMin`/`extractMax` depth = O(h) for a balanced tree, O(n) worst-case skewed.

## Choosing successor vs predecessor

Practically interchangeable. Mark to the spec — most Birmingham course material uses **in-order successor** (Strategy A). Confirm by checking your `bst.md` reference / problem statement.

## QuickCheck properties for `delete`

```haskell
prop_delete_preservesBST :: Int -> BT Int -> Property
prop_delete_preservesBST x t = isBST t ==> isBST (delete x t)

prop_delete_removes :: Int -> BT Int -> Property
prop_delete_removes x t = isBST t ==> not (member x (delete x t))

prop_delete_decreasesSize :: Int -> BT Int -> Property
prop_delete_decreasesSize x t =
  isBST t ==>
  if member x t
    then size (delete x t) == size t - 1
    else size (delete x t) == size t

prop_delete_idempotent :: Int -> BT Int -> Property
prop_delete_idempotent x t = isBST t ==> delete x (delete x t) == delete x t

prop_delete_irrelevantUnchanged :: Int -> Int -> BT Int -> Property
prop_delete_irrelevantUnchanged x y t =
  isBST t && x /= y ==>
  member y (delete x t) == member y t
```

If your implementation passes all five, you're safe.

## Common bugs

| Bug | Symptom | Fix |
|---|---|---|
| Promoting `Empty` to root in 2-children case | Lost subtrees, BST shrinks silently | Use `combine` with `extractMin`/`extractMax`, never just return `Empty`. |
| `extractMin (Fork x Empty r)` returning `(x, Empty)` | Loses `r` | Return `(x, r)`. The whole point: the right child of the min-node becomes its replacement. |
| Forgetting both `Empty` cases of `combine` | Crash or wrong tree | `combine Empty r = r` and `combine l Empty = l` are essential. |
| Using `extractMin` on the LEFT subtree | Inserts the wrong value at root | Must extract from the OPPOSITE subtree to the replacement direction. |
| Re-using `delete x` recursively instead of `combine` | Infinite loop (deletes itself forever) | The hard case is where you don't recurse with `delete x` — you destructure with `combine`. |

See [P-015 BST delete two-children case wrong](../pitfalls/HIGH-severity.md#p-015) for the canonical wrong-vs-right diff.

## See also

**Theory:** [BST](./bst.md) · [binary tree](./binary-tree.md) · [tree validation](./tree-validation.md)
**Archetypes:** [A11 BST ops](../archetypes/A11-bst-ops.md) · [A01 tree recursion](../archetypes/A01-tree-recursion.md)
**Question families:** [bst-ops](../question-families/bst-ops-family.md) · [tree-validation](../question-families/tree-validation-family.md)
**Cross-topic:** [bst × state](../cross-matrix/bst-x-state.md) · [bst × writer](../cross-matrix/bst-x-writer.md)
**QuickCheck:** [bst attacks](../quickcheck/bst-attacks.md) · [property patterns](../quickcheck/PROPERTY-PATTERNS.md)
**Pitfalls:** [P-009 isBST Empty = False](../pitfalls/HIGH-severity.md#p-009) · [P-015 BST delete two-children](../pitfalls/HIGH-severity.md#p-015) · [P-020 three different isBST impls](../pitfalls/HIGH-severity.md#p-020)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
