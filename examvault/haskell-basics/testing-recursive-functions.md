<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Testing recursive functions**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** [testing-functions](./testing-functions.md) · **testing-recursive-functions** · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Testing recursive functions

## What this is
A recursion has two halves: a base case and a recursive case. Bugs usually live in one or the other. This page is a *recipe* for finding which one is wrong quickly.

## Mental model
For any recursive function `f`, three test points pin down 90% of bugs:

| Test | Probes |
|---|---|
| `f base` | Did the base case return the right answer? |
| `f (oneStep base)` | Does one recursion step do the right thing? |
| `f (bigInput)` | Does it scale / not blow up? |

If the base is wrong, every recursive answer will be off-by-N. If the step is wrong, the base may look right but two-element inputs fail.

## Recipe: list recursion

```haskell
myLength :: [a] -> Int
myLength []     = 0
myLength (_:xs) = 1 + myLength xs
```

```text
ghci> myLength []          -- base case
0
ghci> myLength [42]        -- one step
1
ghci> myLength [1,2,3]     -- multi-step
3
ghci> myLength [1..1000]   -- scale
1000
```

If `myLength [42]` returns `0`, base case is wrong (returns `0` even for cons).
If `myLength [42]` returns `1` but `myLength [1,2,3]` returns `2`, step is off-by-one.

## Recipe: numeric recursion

```haskell
factorial :: Int -> Int
factorial 0 = 1
factorial n = n * factorial (n - 1)
```

```text
ghci> factorial 0       -- base
1
ghci> factorial 1       -- one step: 1 * 1
1
ghci> factorial 5       -- multi-step
120
ghci> factorial (-1)    -- !! infinite loop or stack overflow
^C                      -- you hit Ctrl-C here
```

`factorial (-1)` reveals the classic bug: `n == 0` doesn't catch negatives, the recursive call goes `-1, -2, -3, …`, never reaches base.

The fix is `n <= 0` instead of `n == 0`, or a guard. See [P-008](../pitfalls/HIGH-severity.md#p-008).

## Recipe: accumulator recursion

```haskell
fastReverse :: [a] -> [a]
fastReverse xs = go xs []
  where
    go []     acc = acc
    go (x:xs) acc = go xs (x : acc)
```

Test both the outer wrapper and (mentally) the helper:

```text
ghci> fastReverse []
[]
ghci> fastReverse [1]
[1]
ghci> fastReverse [1,2,3]
[3,2,1]
```

Trace by hand:

```
go [1,2,3] []
go [2,3]   [1]
go [3]     [2,1]
go []      [3,2,1]
=> [3,2,1]
```

If your accumulator threads in the wrong order (e.g. `go xs (acc ++ [x])`), you get back the *original* list. That's a tell.

## Recipe: stop-the-world bugs

A non-terminating recursion either:
- never decreases its argument (`f n = f n + 1`), or
- decreases but skips the base case (`f 1 = ...`, then call with `f 0` is undefined / matches the recursive clause and goes negative).

When GHCi hangs:

```text
ghci> brokenFactorial 5
... (no response)
^C
Interrupted.
```

1. Hit `Ctrl+C`.
2. Test with the **smallest possible** input.

```text
ghci> brokenFactorial 0   -- if this hangs, base case is missing
... ^C
ghci> brokenFactorial 1   -- if this hangs, base is unreachable
```

Then read the equations top-to-bottom: which one matches `0`? If none, you forgot the base case.

## Recipe: off-by-one debugging

If `f [1,2,3]` returns the wrong number of things, run the smaller cases:

```text
ghci> f []
0
ghci> f [1]
1
ghci> f [1,2]
2
ghci> f [1,2,3]
3
```

Look for the first answer that doesn't follow the obvious pattern. That's where the equation is wrong.

## Recipe: structural recursion over an ADT

```haskell
data BT a = Empty | Fork a (BT a) (BT a)

sizeBT :: BT a -> Int
sizeBT Empty        = 0
sizeBT (Fork _ l r) = 1 + sizeBT l + sizeBT r
```

Build sample trees at the prompt:

```text
ghci> let t0 = Empty
ghci> let t1 = Fork 1 Empty Empty
ghci> let t2 = Fork 1 (Fork 2 Empty Empty) Empty   -- one-sided
ghci> let t3 = Fork 1 (Fork 2 Empty Empty) (Fork 3 Empty Empty)

ghci> sizeBT t0
0
ghci> sizeBT t1
1
ghci> sizeBT t2
2
ghci> sizeBT t3
3
```

The one-sided tree `t2` is the most useful test: it catches "I always recurse left" or "I always recurse right" bugs.

More tree recipes on [testing-tree-functions](./testing-tree-functions.md).

## Recipe: mutual recursion

If `f` and `g` call each other, test each entry point:

```haskell
isEven :: Int -> Bool
isEven 0 = True
isEven n = isOdd (n - 1)

isOdd :: Int -> Bool
isOdd 0  = False
isOdd n  = isEven (n - 1)
```

```text
ghci> isEven 0
True
ghci> isOdd 0
False
ghci> isEven 4
True
ghci> isOdd 7
True
ghci> isEven (-1)        -- !! infinite mutual loop
^C
```

## Recipe: testing with `take` for safety

Recursive list builders (like infinite streams or "generate all paths") can produce gigantic results. Use `take` to keep tests bounded:

```text
ghci> take 5 (myIterate (+1) 0)
[0,1,2,3,4]

ghci> take 10 (paths myTree)     -- maybe there are 10000 — only print 10
[...]
```

If `take 5` already hangs, your function is non-terminating *per element*, not just per output.

## Edge-case checklist for recursion

| Edge | What it probes |
|---|---|
| `[]` / `Empty` / `Nothing` / `0` | Base case correctness |
| singleton / one-element | First step joins base to step |
| 2-3 elements | Recursive case shape |
| Deep right-spine of length 1000+ | Stack safety / quadratic accidents |
| Negative input (numeric) | Missing `<=` guard |
| Duplicates | Eq-comparison bugs |
| All-same input | Whether output is reduced or accumulated |

## Common mistakes

- **Missing base case** — the `n == 0` trap, the `Empty` trap. [P-005](../pitfalls/HIGH-severity.md#p-005).
- **Recursive call on the same input** — `f xs = something + f xs` infinite loops. Check that the argument to the recursive call is *smaller*.
- **Wrong sub-structure** — `f (Fork x l r) = f l + f l` (typo: `l` twice). Tree gets only the left subtree counted twice. [P-014](../pitfalls/HIGH-severity.md#p-014).
- **Base-case unreachable** — `f 5 = 1 ; f n = f (n - 1)` works for `n >= 5` but loops on `n < 5`. Order matters; **base case first**. [P-022](../pitfalls/HIGH-severity.md#p-022).
- **Accumulator threaded wrong** — `go acc (x:xs) = go (acc ++ [x]) xs` quadratic; usually you want `go (x:acc) xs`.
- **Forgotten case for partial constructor** — `BT a = Empty | Fork a (BT a) (BT a)` with only the `Fork` clause matches → GHC warns `Non-exhaustive patterns`, marker crashes. [P-017](../pitfalls/HIGH-severity.md#p-017).

## Exam use

Q1 and Q5 in the mock are structural recursion. The mistakes the auto-marker hunts for are exactly the edge cases on this page — empty, singleton, deep, all-same. Always run those four before you mark a recursive function as "done".

## See also

**Sibling testing pages:** [testing-functions](./testing-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md)
**Recursion theory:** [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md)
**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)
**Pitfalls:** [P-005 missing base case](../pitfalls/HIGH-severity.md#p-005) · [P-008 `n == 0` vs `<= 0`](../pitfalls/HIGH-severity.md#p-008) · [P-014 wrong sub-structure](../pitfalls/HIGH-severity.md#p-014) · [P-017 non-exhaustive](../pitfalls/HIGH-severity.md#p-017) · [P-022 base case first](../pitfalls/HIGH-severity.md#p-022)
**QuickCheck:** [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) · [lists-attacks](../quickcheck/lists-attacks.md) · [trees-attacks](../quickcheck/trees-attacks.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
