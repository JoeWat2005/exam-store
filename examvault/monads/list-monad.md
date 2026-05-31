<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [monads](./README.md) · **Monad: List `[]`**

<!-- siblings:start -->
> **Peers:** [either](./either.md) · [generic-combinators](./generic-combinators.md) · [io](./io.md) · **list-monad** · [maybe](./maybe.md) · [monad-laws](./monad-laws.md) · [monaderror](./monaderror.md) · [multi-effect](./multi-effect.md) · [reader](./reader.md) · [state](./state.md) · [transformer-stack-order](./transformer-stack-order.md) · [transformers](./transformers.md) · [writer](./writer.md)
<!-- siblings:end -->






# Monad: List `[]`

**Import:** built-in (`Prelude`); `Control.Monad` for `guard`, `MonadPlus`.
**Type:** `[a]` — the ordinary list.
**Combines with:** Maybe, State (more advanced).
**Search keywords:** non-determinism, all possible, choose, search, knight, moves, Pythagorean, triples, combinations, Cartesian product, list comprehension, guard, do-notation.

## Primitive operations

| Operation | Signature | Semantics | Pitfall |
|---|---|---|---|
| `return`/`pure x` | `a -> [a]`               | `[x]`                  | NOT `x` |
| `(>>=)`           | `[a] -> (a -> [b]) -> [b]`| `concatMap f xs`       | NOT `map f xs` |
| `[]`              | `[a]`                    | failure / no choice    | — |
| `guard`           | `Alternative f => Bool -> f ()` | `True → [()]`, `False → []` | requires `import Control.Monad` |
| `(<|>)` / `mplus` | `[a] -> [a] -> [a]`      | `(++)`                 | requires `Alternative`/`MonadPlus` |

## Run functions

No `runList`. The result IS the list. Pattern-match, use `head`/`null`/`length`, or extract the first element.

## Equivalence: do-notation ≡ list comprehension

```haskell
do x <- xs                ≡    [ f x y | x <- xs, y <- ys ]
   y <- ys
   pure (f x y)
```

Both desugar identically thanks to `MonadComprehensions`. The course material uses both interchangeably.

## When to reach for the list monad

- "List of all possible moves / positions / configurations".
- "Knight moves" (problem 105).
- "Pythagorean triples" / "all `(a,b,c)` such that...".
- "All ordered pairs" / "Cartesian product" (problem 106).
- "Search a tree breadth-first" (state-of-the-art problems).
- ANY question with the phrase "all that satisfy ...".

## Canonical templates

### Cartesian product
```haskell
pairs :: [a] -> [b] -> [(a, b)]
pairs xs ys = do
  x <- xs
  y <- ys
  pure (x, y)

-- equivalent: [ (x, y) | x <- xs, y <- ys ]
```

### Knight moves (problem 105 — CANONICAL)
```haskell
knightMoves :: (Int, Int) -> [(Int, Int)]
knightMoves (x, y) = do
  (dx, dy) <- [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
  let nx = x + dx
  let ny = y + dy
  if 1 <= nx && nx <= 8 && 1 <= ny && ny <= 8
    then pure (nx, ny)
    else []
```
Note the `else []` — that's the "filter out" behaviour you want. You could equivalently use `guard`:
```haskell
knightMoves (x, y) = do
  (dx, dy) <- offsets
  let nx = x + dx; ny = y + dy
  guard (1 <= nx && nx <= 8 && 1 <= ny && ny <= 8)
  pure (nx, ny)
 where offsets = [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
```

### All distinct ordered pairs (problem 106)
```haskell
allPairs :: [a] -> [(a, a)]
allPairs xs = [ (x, y) | (x:rest) <- tails xs, y <- rest ]

-- or via do-notation, using indexed positions:
allPairs' :: [a] -> [(a, a)]
allPairs' xs = do
  let n = length xs
  i <- [0 .. n-1]
  j <- [i+1 .. n-1]
  pure (xs !! i, xs !! j)
-- allPairs [1,2,3] == [(1,2),(1,3),(2,3)]
```

### Pythagorean triples
```haskell
triples :: Int -> [(Int, Int, Int)]
triples n = do
  a <- [1 .. n]
  b <- [a .. n]
  c <- [b .. n]
  guard (a*a + b*b == c*c)
  pure (a, b, c)
```

### `do`-style filter with `guard`
```haskell
import Control.Monad (guard)

evens :: [Int] -> [Int]
evens xs = do
  x <- xs
  guard (even x)
  pure x
```

### Cross-product-and-filter (powerset-style)
```haskell
subsets :: [a] -> [[a]]
subsets []     = [[]]
subsets (x:xs) = do
  rest <- subsets xs
  [rest, x : rest]      -- two choices each step
```

## Question families this monad belongs to

- [monad-combinator-family](../question-families/monad-combinator-family.md) — non-deterministic search via `mapM` / `filterM` / `replicateM`
- [list-comp-family](../question-families/list-comp-family.md) — combinations / all-pairs / comprehension-style generation

## QuickCheck traps

- `allPairs []` must be `[]` (not error or singleton).
- `knightMoves (1, 1)` returns ONLY in-bounds moves (e.g. 2, not 8).
- The auto-marker may sort the result; if it does, you can return any order. If it doesn't, your order must match exactly. **Check the test spec.**
- Empty Cartesian: `pairs xs []` is `[]` for any `xs`, NOT `xs` itself.

## Pitfalls

- **`xs >>= f` is `concatMap f xs`**, NOT `map f xs`. Easy to slip in instance questions.
- `pure x` for lists is `[x]`, not `x`. Type error if you forget.
- `do _ <- []; ...` produces `[]` — the WHOLE block fails to nothing. (Equivalent to short-circuit.)
- `guard False = []`, `guard True = [()]`. Order it BEFORE `pure result`.
- `(<|>)` for lists = `(++)`. Order matters: `[1,2] <|> [3,4] == [1,2,3,4]`.

## Worked examples

- Problem 105 — `knightMoves`.
- Problem 106 — `allPairs`.
- `fib2` in `monads.md` (Maybe-via-list trick).
- Lecture: list comprehensions as syntactic sugar for list monad.

## See also

**Archetypes:** [A03 generic monad](../archetypes/A03-generic-monad.md) · [A21 list comp synthesis](../archetypes/A21-list-comp-synthesis.md)
**Cross-topic:** [list × list-monad](../cross-matrix/list-x-list-monad.md) · [list × monad](../cross-matrix/list-x-monad.md)
**Question families:** [monad-combinator](../question-families/monad-combinator-family.md) · [list-comp](../question-families/list-comp-family.md)
**QuickCheck:** [monad attacks](../quickcheck/monad-attacks.md)
**Related (monads):** [generic combinators](./generic-combinators.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
