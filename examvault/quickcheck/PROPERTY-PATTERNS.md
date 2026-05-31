<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **Property patterns + Arbitrary**

<!-- siblings:start -->
> **Peers:** **PROPERTY-PATTERNS** · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# Property patterns + Arbitrary instances

The 15 `*-attacks.md` files in this dir catalogue *what the marker generates*. This page catalogues *how you would write the property code yourself* — the `prop_*` declarations and the `Arbitrary` instances for the three custom ADTs the exam uses (`BT a`, `Rose a`, `Expr`).

Use this page when (a) drafting your own sanity-check before submission, (b) you want to understand what the auto-marker is doing under the hood.

## 1. `prop_*` shape

```haskell
prop_<name> :: <args with QuickCheck-derivable types> -> <Bool or Property>
prop_<name> args = lhs == rhs        -- the property
```

Common return shapes:

```haskell
prop_p1 :: [Int] -> Bool
prop_p1 xs = reverse (reverse xs) == xs

prop_p2 :: NonEmptyList Int -> Bool
prop_p2 (NonEmpty xs) = head (reverse xs) == last xs

prop_p3 :: Int -> Property
prop_p3 n = n > 0 ==> abs n == n     -- conditional, may discard

prop_p4 :: Int -> [Int] -> Property
prop_p4 x xs = classify (length xs > 10) "long" $
               x `elem` (x:xs)
```

Pick `Bool` for unconditional properties, `Property` for conditional (`==>`) or instrumented (`classify`, `cover`).

## 2. Universal property patterns by archetype

| Archetype | Canonical property shape | Example |
|---|---|---|
| A01 tree recursion | `f t == naïveSpec t` | `prop_sumBT t = sumBT t == sum (flattenBT t)` |
| A02 state game | `runState m s0 == (expectedA, expectedS)` | `prop_takeTokens n p s = let (_,s') = runState (takeTokens n p) s in s' /= s \|\| n == 0` |
| A03 generic monad | `runIdentity (mf id 0) == 0` (specialise to Identity) | `prop_applyNTimes_Identity xs n = ...` |
| A05 ADT translation | `decode . encode == id` round-trip | `prop_morse_roundtrip s = decode (encode s) == s` |
| A06 functor instance | functor laws | `prop_fmap_id t = fmap id t == t`; `prop_fmap_compose f g t = fmap (f . g) t == (fmap f . fmap g) t` |
| A07 codec pair | round-trip + injective | `prop_codec_roundtrip x = decode (encode x) == Just x` |
| A09 prelude reimpl | `myF == Prelude.f` for all inputs | `prop_myLength xs = myLength xs == length xs` |
| A11 BST ops | invariant preserved | `prop_insertBST x t = isBST (insertBST x t)` |
| A15 writer trace | log monoid law | `prop_tell_order = execWriter (tell [1] >> tell [2]) == [1,2]` |
| A20 laws / iso | both laws | functor laws OR `f . g == id && g . f == id` |

## 3. Arbitrary instances for the custom ADTs

The marker uses `sized` generation: for the `Gen` size parameter `n`, produce a tree of size ~n. Without `sized`, you'd generate unbounded trees and blow the stack.

### `Arbitrary (BT a)` — binary tree from this course

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

instance Arbitrary a => Arbitrary (BT a) where
  arbitrary = sized go
    where
      go 0 = return Empty
      go n = frequency
        [ (1, return Empty)
        , (n, do x <- arbitrary
                 l <- go (n `div` 2)
                 r <- go (n `div` 2)
                 return (Fork x l r))
        ]
  shrink Empty        = []
  shrink (Fork x l r) = [Empty, l, r] ++
                       [Fork x' l r | x' <- shrink x] ++
                       [Fork x l' r | l' <- shrink l] ++
                       [Fork x l r' | r' <- shrink r]
```

`sized` ensures the tree shrinks toward `Empty`. The `frequency` weights make `Empty` rare for large `n` (so we actually get deep trees).

### `Arbitrary (Rose a)`

```haskell
data Rose a = Leaf a | Branch [Rose a]

instance Arbitrary a => Arbitrary (Rose a) where
  arbitrary = sized go
    where
      go 0 = Leaf <$> arbitrary
      go n = oneof
        [ Leaf <$> arbitrary
        , do k  <- choose (0, min 4 n)            -- arity 0..4
             xs <- vectorOf k (go (n `div` (k+1)))
             return (Branch xs)
        ]
  shrink (Leaf _)    = []
  shrink (Branch xs) = [Leaf undefined | False] ++   -- can't shrink to Leaf without a value
                      [Branch xs' | xs' <- shrink xs]
```

Note `Branch []` is a valid value — the marker DOES generate it. If your function on `Branch []` does something silly (e.g. `head xs`), QuickCheck will find it.

### `Arbitrary Expr` — for an arithmetic Expr ADT

```haskell
data Expr = Num Int | Var String | Add Expr Expr | Mul Expr Expr

instance Arbitrary Expr where
  arbitrary = sized go
    where
      go 0 = oneof [Num <$> arbitrary, Var <$> elements ["x","y","z"]]
      go n = oneof
        [ Num <$> arbitrary
        , Var <$> elements ["x","y","z"]
        , Add <$> go (n `div` 2) <*> go (n `div` 2)
        , Mul <$> go (n `div` 2) <*> go (n `div` 2)
        ]
  shrink (Num n)   = [Num n' | n' <- shrink n]
  shrink (Var _)   = [Num 0]
  shrink (Add l r) = [l, r] ++ [Add l' r | l' <- shrink l] ++ [Add l r' | r' <- shrink r]
  shrink (Mul l r) = [l, r] ++ [Mul l' r | l' <- shrink l] ++ [Mul l r' | r' <- shrink r]
```

For `Circuit` (Mock Q5), the same pattern: generate constructors weighted by depth, shrink toward smaller variants.

## 4. `forAll`, `==>`, `classify`, `cover`

```haskell
-- forAll: use a custom generator instead of relying on Arbitrary
prop_evenList = forAll (listOf (choose (2,100) `suchThat` even)) $ \xs -> all even xs

-- ==> : discard when precondition fails (avoid bias)
prop_div :: Int -> Int -> Property
prop_div x y = y /= 0 ==> (x `div` y) * y + (x `mod` y) == x

-- classify: tag generated cases for distribution reporting
prop_listSize :: [Int] -> Property
prop_listSize xs = classify (null xs) "empty"
                 $ classify (length xs > 10) "long"
                 $ reverse (reverse xs) == xs

-- cover: REQUIRE a percentage of cases to fall in a bucket
prop_coverage :: [Int] -> Property
prop_coverage xs = cover 30 (length xs > 5) "longish" True
```

`cover` actually fails the test if generators don't produce diverse enough inputs — useful when you suspect your `Arbitrary` is degenerate.

## 5. Reading a counterexample

When QuickCheck fails it prints the smallest counterexample it could shrink to. Read it like:

```
*** Failed! Falsified (after 4 tests and 7 shrinks):
Fork 0 Empty (Fork 0 Empty Empty)
```

The shrinker has reduced to the *minimal* failing input. If you fix the bug for that case, you've probably fixed the bug for the whole class.

## 6. Universal harness — runs all properties

```haskell
main :: IO ()
main = do
  quickCheck prop_sumBT_matches_flatten
  quickCheck prop_insertBST_preserves_invariant
  quickCheck prop_applyNTimes_n0_returns_singleton
  -- etc.
```

For one-shot sanity checking in GHCi:
```
ghci> quickCheck prop_isNBranching_leaf
+++ OK, passed 100 tests.
```

## 7. Exam-day use

This page is a **safety net**, not a primary tool. The marker writes its own properties. You don't need to write yours. But if you're unsure your solution is correct, do this in 2 minutes:

1. Open this page; grab the property shape for your archetype.
2. Write 1 property in GHCi (`quickCheck`).
3. If it passes 100 random inputs, your code is probably right.

## See also

**Archetypes:** see [`../archetypes/`](../archetypes/README.md) — each archetype has a row in section 2 above.
**Cross-topic:** every `cross-matrix/*-x-*.md` file already includes `prop_*` examples for that combo.
**QuickCheck attacks:** [trees](./trees-attacks.md) · [bst](./bst-attacks.md) · [rose](./rose-attacks.md) · [expr](./expr-attacks.md) · [monad](./monad-attacks.md) · [state](./state-attacks.md) · [writer](./writer-attacks.md) · [maybe/either](./maybe-either-attacks.md) · [codec](./codec-attacks.md) · [interp](./interp-attacks.md) · [matrix](./matrix-attacks.md) · [numeric](./numeric-attacks.md) · [lists](./lists-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [master](./QUICKCHECK-ATTACKS.md)
**Pitfalls:** [P-001 sig changed](../pitfalls/HIGH-severity.md#p-001) (your prop's signature must match the marker's), [P-023 deepseq exposes lazy undefined](../pitfalls/HIGH-severity.md#p-023)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
