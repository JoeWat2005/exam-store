<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [question-families](./README.md) · **Family: functor-instance**

<!-- siblings:start -->
> **Peers:** [adt-translation](./adt-translation-family.md) · [applicative-monad-instance](./applicative-monad-instance-family.md) · [bst-ops](./bst-ops-family.md) · [codec](./codec-family.md) · [env-eval](./env-eval-family.md) · [error-handling](./error-handling-family.md) · **functor-instance** · [lazy-infinite](./lazy-infinite-family.md) · [list-comp](./list-comp-family.md) · [list-fold](./list-fold-family.md) · [list-rewrite](./list-rewrite-family.md) · [matrix-predicate](./matrix-predicate-family.md) · [monad-combinator](./monad-combinator-family.md) · [parser](./parser-family.md) · [pretty-print](./pretty-print-family.md) · [rose-ops](./rose-ops-family.md) · [state-counter](./state-counter-family.md) · [state-game](./state-game-family.md) · [string-ops](./string-ops-family.md) · [tree-counting](./tree-counting-family.md) · [tree-extract](./tree-extract-family.md) · [tree-transform](./tree-transform-family.md) · [tree-validation](./tree-validation-family.md) · [writer-trace](./writer-trace-family.md)
<!-- siblings:end -->






# Family: functor-instance

**Archetype:** A13 (Functor instance for a custom ADT)   |   **Stars:** ⭐⭐⭐   |   **Course week(s):** 9
**Search keywords:** Functor, fmap, instance Functor, Maybe, List, Tree, Pair, Reader, Either, derive

## Generator template
```haskell
instance Functor F where
  fmap :: (a -> b) -> F a -> F b
  fmap f (Cons1 x)     = Cons1 (f x)
  fmap f (Cons2 x y)   = Cons2 (f x) (f y)   -- assuming both x and y are a's
  fmap _ Empty         = Empty
```

The pattern: for every constructor of `F a`,
- replace each `a`-typed field with `f field`,
- recurse into sub-`F a` fields.

## Functor laws (always preserved)
1. `fmap id == id`
2. `fmap (f . g) == fmap f . fmap g`

These are the QC checks for *every* instance below.

## Mutations (the examiner picks one)

### Mutation 1 — Functor for MyMaybe (= problem 70 / 121)
**Sig:** `instance Functor MyMaybe`
**Solution:**
```haskell
data MyMaybe a = MyNothing | MyJust a

instance Functor MyMaybe where
  fmap _ MyNothing  = MyNothing
  fmap f (MyJust x) = MyJust (f x)
```
**QC trap:** `fmap _ MyNothing == MyNothing` — don't try to apply `f` to nothing.

### Mutation 2 — Functor for MyList (= problem 122)
**Sig:** `instance Functor MyList`
**Solution:**
```haskell
data MyList a = Nil | Cons a (MyList a)

instance Functor MyList where
  fmap _ Nil         = Nil
  fmap f (Cons x xs) = Cons (f x) (fmap f xs)
```
**QC trap:** Recurse on `xs` with the same `f`. Easy bug: writing `fmap _ xs` (passing `_` to the recursive call).

### Mutation 3 — Functor for BT (= problem 125)
**Sig:** `instance Functor BT`
**Solution:**
```haskell
data BT a = Empty | Fork a (BT a) (BT a)

instance Functor BT where
  fmap _ Empty        = Empty
  fmap f (Fork v l r) = Fork (f v) (fmap f l) (fmap f r)
```
**QC trap:** `fmap` must be the qualified one when `Fork _ l r` — see `tree-transform-family.md` mutation 8.

### Mutation 4 — Functor for Rose (= problem 126)
**Sig:** `instance Functor Rose`
**Solution (Variant A):**
```haskell
data Rose a = Branch a [Rose a]

instance Functor Rose where
  fmap f (Branch v cs) = Branch (f v) (map (fmap f) cs)
```
Note: uses the outer `map` for `[Rose a] -> [Rose b]`.
**QC trap:** `map (fmap f)` not `fmap (fmap f)` — although in fact `fmap = map` for lists, so both work.

### Mutation 5 — Functor for Pair (only the second component)
**Spec:** `Pair (b, a)` — Functor over the second slot.
**Sig:** `instance Functor (Pair b)`
**Solution:**
```haskell
data Pair b a = Pair b a

instance Functor (Pair b) where
  fmap f (Pair b a) = Pair b (f a)
```
**QC trap:** Functor takes a type constructor of kind `* -> *`. `Pair` is `* -> * -> *`, so you Functorise over `Pair b`. You can only map over the *last* type argument.

### Mutation 6 — Functor for Reader (= problem 124)
**Sig:** `instance Functor (Reader r)`
**Solution:**
```haskell
newtype Reader r a = Reader { runReader :: r -> a }

instance Functor (Reader r) where
  fmap f (Reader g) = Reader (f . g)
```
**QC trap:** `f . g` not `g . f`. Reader is "function from r to a"; fmap post-composes the result.

### Mutation 7 — Functor for Either (only Right)
**Spec:** `Either e a` — Functor maps only the Right.
**Solution:**
```haskell
-- Already in Prelude. As a teaching reimplementation:
data MyEither e a = MyLeft e | MyRight a

instance Functor (MyEither e) where
  fmap _ (MyLeft e)  = MyLeft e
  fmap f (MyRight x) = MyRight (f x)
```
**QC trap:** Just like Pair — kind `* -> *` means Functor over the last slot. Left is the "error" channel and stays put.

### Mutation 8 — Functor for Const
**Spec:** `Const a b = Const a` — phantom Functor.
**Solution:**
```haskell
newtype Const a b = Const { getConst :: a }

instance Functor (Const a) where
  fmap _ (Const x) = Const x
```
**QC trap:** `f` is *never* applied because there's no `b` value. The functor laws hold vacuously.

### Mutation 9 — Functor for Identity (= problem 123)
**Sig:** `instance Functor Identity`
**Solution:**
```haskell
newtype Identity a = Identity a

instance Functor Identity where
  fmap f (Identity x) = Identity (f x)
```
**QC trap:** Trivial — just one constructor. Useful as a starting point for State and Reader.

### Mutation 10 — Functor for Free
**Sig:** `instance Functor f => Functor (Free f)`
**Solution:**
```haskell
data Free f a = Pure a | Free (f (Free f a))

instance Functor f => Functor (Free f) where
  fmap g (Pure x)    = Pure (g x)
  fmap g (Free fxs)  = Free (fmap (fmap g) fxs)
```
**QC trap:** The outer `fmap` is on `f`'s Functor; the inner `fmap g` is the recursive call. Two `fmap`s nested — easy to confuse.

## Hidden-predicate mutations
Not really applicable — Functor instances are mechanical. The "trick" is usually:
- "implement without `deriving Functor`" (forces explicit code),
- "implement Functor *and* prove the laws" (so know how to argue both).

## Accumulator-style alternative
Not relevant — Functor is structural traversal.

## Fold-style alternative
For `Functor BT` you can express via `foldBT`:
```haskell
fmap' g = foldBT Empty (\v l r -> Fork (g v) l r)
```
Identical to mutation 3, just dressed up.

## Cross-family combinations
- this family + `applicative-monad-instance-family.md` — Functor is the prerequisite.
- this family + `tree-transform-family.md` — mapBT IS fmap.
- this family + `rose-ops-family.md` — mapRose IS fmap.
- this family + `monad-combinator-family.md` — `fmap` for the "lift pure into monad" pattern.

## QuickCheck universal attacks
- **Functor identity law:** `fmap id == id` for all instances.
- **Functor composition law:** `fmap (f . g) == fmap f . fmap g`.
- **fmap shape-preserving:** structure of the input matches structure of the output.
- **Specific instances:**
  - `fmap f Nothing == Nothing`
  - `fmap f (Just x) == Just (f x)`
  - `fmap f [] == []`
  - `fmap (+1) [1,2,3] == [2,3,4]`
  - `runReader (fmap (+1) r) 5 == 1 + runReader r 5`

## Pitfalls (per mutation)
- M1: applying `f` to Nothing.
- M2: not recursing on `xs`.
- M3: confusing in-Fork value `v` with sub-trees.
- M4: using `fmap` recursively when `map` is needed (over the children list).
- M5: trying to Functorise over the first slot.
- M6: composing in the wrong order (`g . f` vs `f . g`).
- M7: trying to map the Left case.
- M8: thinking `f` should be applied somewhere.
- M9: forgetting to wrap in `Identity`.
- M10: nested fmap confusion.
- M11: composing in the wrong order — `fmap = (.)` post-composes (`g . h`), not `h . g`.


## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

### Mutation 11 — Functor for the function type `((->) r)`

**Spec:** Make functions `r -> a` a `Functor` in their *result*. This is the "reader-as-a-plain-function" instance (no `newtype` wrapper, unlike `Reader` in M6). `fmap` is just composition.

**Type sig:**
```haskell
instance Functor ((->) r) where
  fmap :: (a -> b) -> (r -> a) -> (r -> b)
```

```haskell
instance Functor ((->) r) where
  fmap = (.)
```

**What changes vs seed:** There is **no constructor to pattern-match** — `F a` is the function type `r -> a` itself, so `fmap` can't deconstruct anything; it post-composes. Equivalently `fmap g h = g . h` (apply `h`, then `g`). This instance already lives in `Prelude`/`base`; an exam would phrase it as "show that `fmap = (.)`" or hand you a `newtype` wrapper to make the instance declarable without overlapping the built-in one.

**QC trap:** `(.)` composes *result-first*: `fmap g h = g . h`, NOT `h . g`. Test with `fmap (+1) (*2) $ 5 == 11` (double then add one), whereas the wrong `h . g` order gives `(5+1)*2 == 12`. Same post-composition direction as Reader's `f . g` in M6.

## See also

**Primary archetype:** [A06 functor instance](../archetypes/A06-functor-instance.md)
**Sibling families:** [applicative-monad-instance](./applicative-monad-instance-family.md)
**Theory:** [functor](../typeclasses/functor.md) · [tree functor](../trees/tree-functor.md)
**QuickCheck:** [typeclass-instance attacks](../quickcheck/typeclass-instance-attacks.md)
**Pitfalls:** [P-010 deriving Functor unsafe](../pitfalls/HIGH-severity.md#p-010) · [P-016 shape break](../pitfalls/HIGH-severity.md#p-016)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
