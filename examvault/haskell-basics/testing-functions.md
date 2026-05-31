<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [haskell-basics](./README.md) · **Testing functions**

<!-- siblings:start -->
> **Syntax:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md) · [if-expressions](./if-expressions.md) · [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [case-expressions](./case-expressions.md) · [tuples](./tuples.md) · [local-definitions](./local-definitions.md)
> **Data:** [lists](./lists.md) · [strings](./strings.md) · [recursion](./recursion.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [sorting](./sorting.md)
> **HOFs:** [list-comprehensions](./list-comprehensions.md) · [higher-order-functions](./higher-order-functions.md) · [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)
> **Operators:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [sections](./sections.md)
> **Types:** [type-signatures](./type-signatures.md) · [polymorphism](./polymorphism.md) · [algebraic-data-types](./algebraic-data-types.md) · [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md)
> **Effects:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md) · [do-notation-basics](./do-notation-basics.md)
> **Std HOFs:** [map](./map.md) · [filter](./filter.md) · [foldr](./foldr.md) · [foldl](./foldl.md) · [zip](./zip.md) · [zipWith](./zipWith.md) · [all-any](./all-any.md)
> **Testing & tools:** **testing-functions** · [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md) · [ghci-commands](./ghci-commands.md) · [allowed-builtins](./allowed-builtins.md) · [safe-haskell](./safe-haskell.md) · [common-templates](./common-templates.md) · [ghc-error-decoder](./ghc-error-decoder.md)
<!-- siblings:end -->






# Testing functions

## What this is
How to actually call your function and see what it returns. The fastest feedback loop on vLab is `:r` + a few inputs at the GHCi prompt. This page covers pure functions; see siblings for [recursive](./testing-recursive-functions.md), [monadic](./testing-monadic-functions.md), and [tree](./testing-tree-functions.md) variants.

## Mental model
Three checks, in order:

1. **Type:** does `:t myFn` match the spec?
2. **Golden path:** does it return the right answer on the obvious input?
3. **Edge cases:** what does it return on `[]`, `0`, `Nothing`, a single element, a duplicate, a negative?

If the type is wrong, the marker probably won't even run your function — fix that first.

## Recipe: pure function

Spec: `double :: Int -> Int`, returns twice the input.

```haskell
-- in MyFile.hs
double :: Int -> Int
double n = n * 2
```

GHCi session:

```text
$ ghci MyFile.hs
ghci> :t double
double :: Int -> Int            -- matches spec ✓

ghci> double 3                  -- golden path
6

ghci> double 0                  -- edge: zero
0

ghci> double (-5)               -- edge: negative
-10

ghci> double maxBound :: Int    -- edge: huge — would overflow
-2                              -- !! sometimes a bug surface
```

## Recipe: list-returning function

Spec: `evens :: [Int] -> [Int]`, return only the even elements.

```haskell
evens :: [Int] -> [Int]
evens = filter even
```

```text
ghci> :t evens
evens :: [Int] -> [Int]

ghci> evens [1..10]              -- golden
[2,4,6,8,10]

ghci> evens []                   -- empty input
[]

ghci> evens [1,3,5]              -- no matches
[]

ghci> evens [2]                  -- one element
[2]

ghci> length (evens [1..100])    -- compute on big input
50
```

`length` after the call is a fast sanity check: did the function return roughly the right *number* of things, even before you read the values?

## Recipe: higher-order function (takes a function)

When `f :: (a -> b) -> [a] -> [b]`, you need to supply a function as the first argument. Two styles:

```text
ghci> myMap (+1) [1,2,3]
[2,3,4]

ghci> myMap (\x -> x*x) [1,2,3]      -- lambda
[1,4,9]

ghci> myMap show [1,2,3]              -- (Int -> String)
["1","2","3"]
```

Lambdas and named functions are interchangeable; pick whichever is shorter.

## Recipe: function taking a predicate

```text
ghci> myFilter (> 3) [1..6]
[4,5,6]

ghci> myFilter (\c -> c `elem` "aeiou") "hello"
"eo"

ghci> myFilter (const True) [1,2,3]    -- predicate that always says yes
[1,2,3]

ghci> myFilter (const False) [1,2,3]   -- always no
[]
```

`const True` and `const False` are universally useful for "what does this do at the boundary?" probes.

## Recipe: function returning a tuple

Spec: `divMod' :: Int -> Int -> (Int, Int)`.

```text
ghci> divMod' 17 5
(3, 2)

ghci> fst (divMod' 17 5)        -- pull out the first element
3

ghci> snd (divMod' 17 5)
2
```

For triples and bigger, pattern-bind:

```text
ghci> let (q, r) = divMod' 17 5
ghci> q
3
ghci> r
2
```

## Recipe: function returning a function (sections / curried)

Functions in Haskell are curried. `add :: Int -> Int -> Int` is really `Int -> (Int -> Int)`. Partial application returns the inner function.

```text
ghci> :t add
add :: Int -> Int -> Int

ghci> let add5 = add 5      -- partial: gave 1 of 2 args
ghci> :t add5
add5 :: Int -> Int

ghci> add5 3
8

ghci> map add5 [1,2,3]
[6,7,8]
```

This is also how the section syntax works (`(+5)` `(*2)`).

## Recipe: reading type errors

Type errors look scary but are usually one of three things.

```text
ghci> double "hi"

<interactive>:1:8: error:
    • Couldn't match expected type ‘Int’ with actual type ‘[Char]’
    • In the first argument of ‘double’, namely ‘"hi"’
```

**Translation:** "you gave a `String`, I wanted an `Int`."

```text
ghci> myFilter even
<interactive>: error:
    • No instance for (Show ([a0] -> [a0])) ...
```

**Translation:** "you only gave 1 of 2 args; the result is a function and I don't know how to print a function." Solution: supply the second arg, or pipe to `:t myFilter even` to see the type instead.

```text
ghci> head []
*** Exception: Prelude.head: empty list
```

**Translation:** runtime error — your function is *partial*. Either guard against `[]` at the call site, or use a `Maybe`-returning version (`listToMaybe`, your own `safeHead`).

## Quick edge-case checklist

For any function, ask:

| Input shape | Examples |
|---|---|
| empty | `[]`, `""`, `Nothing` |
| singleton | `[x]`, `Just x` |
| smallest meaningful | `0`, `1`, `Empty`, `Leaf` |
| duplicates | `[1,1,1]` |
| negatives | `-3`, `[-1..-5]` |
| max-out | `maxBound`, very long list |
| all-same | `replicate 100 'a'` |
| all-different | `[1..100]` |
| reverse-sorted | for sort-related |
| nesting | `[[],[1],[1,2]]` for list-of-list |

You don't need to run all of these every time — pick 3-4 that match the function's spec.

## Property tests in GHCi (without QuickCheck)

You can spot-check properties without importing QuickCheck:

```text
ghci> all (\n -> double n == n + n) [0..100]
True

ghci> all (\xs -> length (reverse xs) == length xs) (map (\n -> [1..n]) [0..20])
True
```

(Keep it on **one** physical GHCi line — splitting after `length xs` leaves line 1 as an incomplete application that evaluates to a function value, which GHCi can't `Show`, so you get a `No instance for (Show …)` error instead of `True`.)

If the result is `True` over many inputs you tried, that's *evidence* but not *proof*. The auto-marker on vLab will hit you with QuickCheck — see [PROPERTY-PATTERNS](../quickcheck/PROPERTY-PATTERNS.md) for the patterns it uses.

## Exam use

Every Q (1-5) on the exam has the same loop: `:r` → run with sample inputs → verify with property → submit. Build the habit:

1. Write the function.
2. `:r`.
3. Run the **simplest possible call** that exercises the function.
4. Run the **edge case** the spec hints at (usually `[]` or `0` or `Nothing`).
5. Run a property check if time permits.
6. Move on.

Don't read a stack trace — re-run with simpler input until the bug is obvious.

## Common mistakes
- **Forgot `:r`** after editing. You're testing the old code.
- **Tested only the golden path.** Marker will hit `[]` and you'll lose 4 marks.
- **Ignored the type error.** "It compiles in my head" doesn't count. Match `:t fn` to spec before testing.
- **Used `print` on a function value.** No `Show` instance for functions — use `:t`.
- **Tested with the wrong constructor names.** Mock Q1's `Rose` has `Leaf | Branch [Rose a]`; Assignment 2's `Tree` has `Empty | Branch (Maybe Char) ...`. Different shapes; different sample values.

## See also

**Sibling testing pages:** [testing-recursive-functions](./testing-recursive-functions.md) · [testing-monadic-functions](./testing-monadic-functions.md) · [testing-tree-functions](./testing-tree-functions.md)
**GHCi reference:** [ghci-commands](./ghci-commands.md)
**When type errors are confusing:** [ghc-error-decoder](./ghc-error-decoder.md)
**Allowed imports:** [allowed-builtins](./allowed-builtins.md)
**Property patterns:** [PROPERTY-PATTERNS](../quickcheck/PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md)
**Exam workflow:** [IN-EXAM-WORKFLOW](../exam-day/IN-EXAM-WORKFLOW.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
