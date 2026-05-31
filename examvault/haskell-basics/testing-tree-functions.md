<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Testing tree functions**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · **testing-tree-functions** · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Testing tree functions

## What this is
Functions over `BT a`, `Rose a`, `BST a`, `Expr`, etc. need *constructed sample trees* before they can be tested. This page lists the sample trees you should build at the GHCi prompt and the typical bugs each one exposes.

## Mental model

Three sample-tree categories, in increasing strictness:

1. **Smallest** — `Empty`, `Leaf x`. Tests the base case.
2. **One-sided / asymmetric** — `Fork x (Fork y E E) E`. Tests "I only recurse left/right" bugs.
3. **Balanced** — `Fork x (Fork y E E) (Fork z E E)`. Tests the symmetric case.

Build all three at the prompt; run your function on each; cross-check counts/heights mentally.

## Binary tree (`BT`)

```haskell
data BT a = Empty | Fork a (BT a) (BT a) deriving Show
```

Sample trees:

```text
ghci> let t0 = Empty :: BT Int
ghci> let t1 = Fork 1 Empty Empty
ghci> let t2 = Fork 1 (Fork 2 Empty Empty) Empty                                   -- left-only
ghci> let t3 = Fork 1 Empty (Fork 2 Empty Empty)                                   -- right-only
ghci> let t4 = Fork 1 (Fork 2 Empty Empty) (Fork 3 Empty Empty)                    -- balanced
ghci> let t5 = Fork 1 (Fork 2 (Fork 4 Empty Empty) Empty) (Fork 3 Empty Empty)     -- deep-left
```

Tests for `sizeBT`:

```text
ghci> sizeBT t0     ==> 0
ghci> sizeBT t1     ==> 1
ghci> sizeBT t2     ==> 2
ghci> sizeBT t3     ==> 2
ghci> sizeBT t4     ==> 3
ghci> sizeBT t5     ==> 5
```

Notice the *symmetry*: `sizeBT t2 == sizeBT t3`. If only one of those equals 2, you're missing a recursive call.

Tests for `heightBT` (course convention: `Empty = 0`, `Fork _ _ _ = 1 + max …`):

```text
ghci> heightBT t0   ==> 0
ghci> heightBT t1   ==> 1
ghci> heightBT t4   ==> 2     -- balanced of depth 2
ghci> heightBT t5   ==> 3     -- left chain of length 3
```

Tests for `mirror`:

```text
ghci> mirror t0     ==> Empty
ghci> mirror t4
Fork 1 (Fork 3 Empty Empty) (Fork 2 Empty Empty)
ghci> mirror (mirror t4) == t4
True                          -- property: mirror is an involution
```

Tests for `mapBT (+10)`:

```text
ghci> mapBT (+10) t4
Fork 11 (Fork 12 Empty Empty) (Fork 13 Empty Empty)
ghci> sizeBT (mapBT (+10) t4) == sizeBT t4
True                          -- property: map preserves shape
```

## Rose tree (`Rose`)

```haskell
data Rose a = Leaf a | Branch [Rose a] deriving Show
```

Sample trees:

```text
ghci> let r0 = Leaf 1 :: Rose Int
ghci> let r1 = Branch [Leaf 1, Leaf 2, Leaf 3]
ghci> let r2 = Branch []                                       -- !! zero-child branch
ghci> let r3 = Branch [Leaf 1, Branch [Leaf 2, Leaf 3]]        -- nested
ghci> let r4 = Branch [Branch [Leaf 1], Leaf 2]                -- mixed leaves and branches
```

`r2` is the trap: a `Branch []` is a valid tree with zero subtrees. `isNBranching` on `r2` with `n == 0` must return `True`. Many bugs miss this case.

Tests for Mock Q1 `isNBranching`:

```text
ghci> isNBranching 2 r0   ==> True       -- Leaf is always n-branching
ghci> isNBranching 0 r2   ==> True       -- Branch [] is 0-branching
ghci> isNBranching 3 r1   ==> True       -- 3 children, all leaves
ghci> isNBranching 3 r3
False                                     -- top-level has 2 children, not 3
ghci> isNBranching 1 (Branch [Branch [Branch [Leaf 1]]])
True                                      -- every internal node has 1 child
```

Tests for Mock Q1 `prune n`:

```text
ghci> prune 2 r3
Branch [Leaf 1, Branch [Leaf 2, Leaf 3]]    -- already ≤2 children → unchanged
ghci> prune 1 r3
Branch [Leaf 1]                              -- trim to first child only
ghci> prune 0 r3
Branch []                                    -- chop everything
ghci> prune 5 r3
Branch [Leaf 1, Branch [Leaf 2, Leaf 3]]    -- 5 > available → unchanged
```

## BST

```haskell
data BST a = E | Node (BST a) a (BST a) deriving Show
```

Sample trees:

```text
ghci> let b0 = E
ghci> let b1 = Node E 5 E
ghci> let b2 = Node (Node E 3 E) 5 (Node E 7 E)               -- valid BST
ghci> let b3 = Node (Node E 7 E) 5 (Node E 3 E)               -- !! INVALID (out of order)
ghci> let b4 = Node (Node (Node E 1 E) 3 E) 5 (Node E 7 E)    -- deeper
```

Tests for `insertBST 4`:

```text
ghci> insertBST 4 b0       ==> Node E 4 E
ghci> insertBST 4 b2
Node (Node E 3 (Node E 4 E)) 5 (Node E 7 E)
ghci> insertBST 5 b2       ==> b2   -- duplicate: no-op (course convention)
```

Test `searchBST`:

```text
ghci> searchBST 3 b2       ==> True
ghci> searchBST 4 b2       ==> False
ghci> searchBST 7 b4       ==> True
ghci> searchBST 0 b4       ==> False
```

Test in-order is sorted:

```text
ghci> inOrder b2           ==> [3,5,7]
ghci> inOrder b4           ==> [1,3,5,7]
ghci> inOrder b3           ==> [7,5,3]      -- !! reveals b3 is invalid
ghci> let sorted xs = and (zipWith (<=) xs (drop 1 xs))
ghci> sorted (inOrder b2)  ==> True
ghci> sorted (inOrder b3)  ==> False
```

`sorted (inOrder t)` is the classic **BST validity invariant** — any operation that preserves "is a BST" must keep this `True`.

For BST delete (the hardest tree op), see [bst-delete-trace](../trees/bst-delete-trace.md).

## Expression tree (`Expr`)

```haskell
data Expr = Lit Int
          | Var String
          | Add Expr Expr
          | Mul Expr Expr
          | Let String Expr Expr
          | Div Expr Expr        -- some versions
          deriving Show
```

Sample expressions, easiest to hardest:

```text
ghci> let e1 = Lit 3
ghci> let e2 = Add (Lit 1) (Lit 2)                         -- 1 + 2
ghci> let e3 = Mul (Add (Lit 1) (Lit 2)) (Lit 4)            -- (1+2)*4
ghci> let e4 = Let "x" (Lit 5) (Add (Var "x") (Lit 1))      -- let x = 5 in x+1
ghci> let e5 = Add (Lit 10) (Div (Lit 1) (Lit 0))           -- !! div by zero
ghci> let e6 = Add (Var "x") (Lit 1)                        -- !! unbound var
```

Test pure eval (`Expr -> Int`):

```text
ghci> eval e1   ==> 3
ghci> eval e2   ==> 3
ghci> eval e3   ==> 12
```

Test `Maybe`-eval (`Expr -> Maybe Int`, where `Div _ 0 = Nothing`):

```text
ghci> evalM e2  ==> Just 3
ghci> evalM e5  ==> Nothing
```

Test env-eval (`Expr -> Env -> Maybe Int`):

```text
ghci> evalEnv e4 []           ==> Just 6
ghci> evalEnv e6 []           ==> Nothing                  -- unbound
ghci> evalEnv e6 [("x", 10)]  ==> Just 11                  -- env saves us
```

Test `Either String`-eval (`Expr -> Either String Int`):

```text
ghci> evalE e5  ==> Left "division by zero"
ghci> evalE e6  ==> Left "unbound variable: x"
```

## Sample-tree mistakes to dodge

- **Single-leaf tree only.** Catches no bugs. Always test at least one *asymmetric* tree.
- **Forgetting `Branch []`** for Rose. Common assignment failure.
- **Using `BST` for any `Ord` test.** The `b3` "invalid BST" is silently constructible — only operations that *assume* the invariant break. If your function blindly accepts `b3`, it may give silly answers. Test with valid AND invalid input.
- **Hardcoding constructor names.** Different files use `Empty`/`Lf`/`E`/`Leaf`. Match the question's spec exactly.

## Property tests on trees

```text
-- mirror is an involution
ghci> all (\t -> mirror (mirror t) == t) [t0, t1, t4, t5]
True

-- size of map equals size
ghci> all (\t -> sizeBT (mapBT (+1) t) == sizeBT t) [t0, t1, t4, t5]
True

-- in-order of a BST is sorted
ghci> all (\t -> sorted (inOrder t)) [b1, b2, b4]
True

-- height is at most size
ghci> all (\t -> heightBT t <= sizeBT t) [t1, t4, t5]
True
```

## Tree with effects — combined runners

```text
-- labelTree :: BT a -> BT (Int, a)
ghci> labelTree (Fork 'a' (Fork 'b' Empty Empty) (Fork 'c' Empty Empty))
Fork (1,'a') (Fork (0,'b') Empty Empty) (Fork (2,'c') Empty Empty)
-- in-order: label 'b' first (0), then root 'a' (1), then 'c' (2)

-- mapMTree print over IO
ghci> mapMTree print t4
1
2
3
Fork () (Fork () Empty Empty) (Fork () Empty Empty)
```

See [A01 × State](../archetypes/A01-tree-recursion.md#a01--a02--labelling-tree-with-state) and [tree-x-state](../cross-matrix/tree-x-state.md).

## Common mistakes

- **Default constructor name mismatch.** Build sample trees with the same constructors as the spec. `Branch` (Rose) ≠ `Branch (Maybe Char) ...` (Assignment 2 Tree).
- **Forgot `deriving Show`.** Without it, GHCi can't print the tree — add `deriving Show` to the ADT in your file, save, `:r`.
- **Confused list and tree.** `[Rose a]` is a list of trees (a forest); `Rose a` is one tree. Mock Q1's `prune` returns a tree, not a list.
- **Empty list in Rose's `Branch`.** Always test `Branch []` — most exam bugs hide there.
- **`maximum []` crash** when computing heights of `Branch []`. Use a guard: `if null xs then 0 else 1 + maximum (map heightR xs)`.

## Exam use

Q1 is structural recursion on a custom tree; Q5 is often "translate this tree to that tree" (A05). Both demand confident sample-tree construction. The 90-second pre-test routine: paste 3 sample trees at the prompt, run the function on each, look at the answers. If any look wrong, fix before submit.

## See also

**Sibling testing pages:** [testing-functions](./testing-functions.md) · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md)
**Tree theory:** [binary-tree](../trees/binary-tree.md) · [bst](../trees/bst.md) · [rose-tree](../trees/rose-tree.md) · [expression-tree](../trees/expression-tree.md) · [tree-traversals](../trees/tree-traversals.md) · [tree-fold](../trees/tree-fold.md) · [tree-functor](../trees/tree-functor.md) · [tree-validation](../trees/tree-validation.md) · [tree-counting](../trees/tree-counting.md) · [bst-delete-trace](../trees/bst-delete-trace.md)
**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A05 ADT translation](../archetypes/A05-adt-translation.md) · [A08 env eval](../archetypes/A08-env-eval.md) · [A11 BST ops](../archetypes/A11-bst-ops.md)
**QuickCheck:** [trees-attacks](../quickcheck/trees-attacks.md) · [rose-attacks](../quickcheck/rose-attacks.md) · [bst-attacks](../quickcheck/bst-attacks.md) · [expr-attacks](../quickcheck/expr-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
