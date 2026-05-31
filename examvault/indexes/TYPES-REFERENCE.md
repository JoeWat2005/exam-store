<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **TYPES-REFERENCE — Mock + Assignment ADTs in one place**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · [MASTER-INDEX](./MASTER-INDEX.md) · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · **TYPES-REFERENCE**
<!-- siblings:end -->





# TYPES-REFERENCE

Every Mock-Test and assignment exposes a `Types` module the student imports. Under exam pressure you don't want to hunt through 5 archetype pages to remember whether it's `Branch a [Rose a]` or `Branch [Rose a]`. This page is the **single lookup** for all the course's custom ADTs.

> **Rule of thumb:** read the exam's `Types.hs` once at the start; if your memory of it diverges from this page, **trust the file, not this page** — the question's `Types.hs` is canonical.

---

## `Rose a` — the rose tree

**Used in:** Mock Q1 (`isNBranching`, `prune`), Assignment 3 (`toRose`, `fromRose`).

```haskell
data Rose a = Leaf a | Branch [Rose a]
```

- **Value at leaves only** — `Leaf x` carries the data.
- **Branch has no value** — just a list of children.
- **`Branch []` is legal** — degenerate "empty branch"; the marker generates it. Distinct from `Leaf`.

Recursion template:
```haskell
f :: Rose a -> r
f (Leaf x)    = baseLeaf x
f (Branch xs) = combine (map f xs)
```

**WATCH OUT:** the lecture material (`Data2.md`) sometimes uses a different `Rose` definition: `data Rose a = Branch a [Rose a]` (value at every node). The Mock paper uses the `Leaf a | Branch [Rose a]` version. Use whichever the exam's `Types.hs` declares.

**Linked pages:** [rose-tree](../trees/rose-tree.md) · [rose-ops-family](../question-families/rose-ops-family.md) · [A01](../archetypes/A01-tree-recursion.md) · [Mock Q1](./MOCK-Q-INDEX.md#mock-q1)

---

## `NimGame`, `Heap`, `Player` — Mock Q3 state

**Used in:** Mock Q3 (`gameOver`, `takeTokens`).

```haskell
type NimGame = (Heap, Heap)        -- two heaps; one per player to draw from
type Heap    = Int                  -- non-negative tokens count

data Player  = First | Second
  deriving (Eq, Show)
```

Operations:
```haskell
gameOver :: State NimGame Bool
takeTokens :: Int -> Player -> State NimGame ()
```

**Critical marker quirks** (Mock Q3):
- `gameOver` must `return True` on `(0,0)` exactly — there's a hardcoded test worth **4 free marks** ([P-006](../pitfalls/HIGH-severity.md#p-006)).
- `takeTokens` must `max 0 (h - n)` — going below zero loses marks.

```haskell
gameOver :: State NimGame Bool
gameOver = do (x, y) <- get
              return (x == 0 && y == 0)         -- AND, not OR

takeTokens :: Int -> Player -> State NimGame ()
takeTokens n First  = do (x, y) <- get; put (max 0 (x - n), y)
takeTokens n Second = do (x, y) <- get; put (x, max 0 (y - n))
```

**Linked pages:** [A02](../archetypes/A02-state-game.md) · [state](../monads/state.md) · [state-game-family](../question-families/state-game-family.md) · [Mock Q3](./MOCK-Q-INDEX.md#mock-q3)

---

## `Expr` — expression tree (varies by problem)

**Used in:** Mock Q5 (`circuit`), Assignment 2, almost every interpreter problem.

The exact constructor list depends on the problem. Common variants:

### Variant A — propositional logic (Mock Q5 origin)
```haskell
data Expr = TT | FF | Var String
          | Not Expr
          | And Expr Expr | Or Expr Expr
          | Implies Expr Expr | Iff Expr Expr
  deriving (Eq, Show)
```

### Variant B — arithmetic
```haskell
data Expr = Num Int | Var String
          | Add Expr Expr | Mul Expr Expr | Sub Expr Expr
          | Let String Expr Expr      -- let binding
  deriving (Eq, Show)
```

### Variant C — minimal arithmetic (interpreter chapter)
```haskell
data Expr = Num Int | Add Expr Expr | Mul Expr Expr
  deriving (Eq, Show)
```

**Read the question's `Types.hs` to know which.** The recursion template is identical — one equation per constructor.

**Linked pages:** [expression-tree](../trees/expression-tree.md) · [A05](../archetypes/A05-adt-translation.md) · [A08](../archetypes/A08-env-eval.md) · [simple-arith](../interpreters/simple-arith.md)

---

## `Circuit` — Mock Q5 target type

**Used in:** Mock Q5 (`circuit :: Expr -> Circuit`).

```haskell
data Circuit = Wire String         -- a labelled input wire
             | Nand Circuit Circuit
  deriving (Eq, Show)
```

Mock Q5 asks you to translate `Expr` → `Circuit` using only `Wire` + `Nand`. Because `Nand` is functionally complete, every logical operator can be expressed.

**Marker quirk** (Mock Q5): The marker checks **semantic equivalence** (boolean-truth tables match), NOT structural identity. Two different `Circuit` trees that produce the same boolean output for all inputs **both pass**. Don't waste time matching the reference AST literally.

**Linked pages:** [A05](../archetypes/A05-adt-translation.md) · [adt-translation-family](../question-families/adt-translation-family.md) · [Mock Q5](./MOCK-Q-INDEX.md#mock-q5)

---

## `BT a` — binary tree (Assignment 1)

**Used in:** problem sheets, Assignment 1 grid (`GridWithAPointer`), `bst.md`, most tree archetypes.

```haskell
data BT a = Empty | Fork a (BT a) (BT a)
  deriving (Eq, Show)
```

Recursion template:
```haskell
f :: BT a -> r
f Empty        = base
f (Fork x l r) = combine x (f l) (f r)
```

**Variants seen in problems:**
- `data Tree = Empty | Node Int Tree Tree` (no type parameter)
- `data BinTree a = Leaf | Branch a (BinTree a) (BinTree a)` (Leaf instead of Empty)

**Linked pages:** [binary-tree](../trees/binary-tree.md) · [A01](../archetypes/A01-tree-recursion.md) · [A11](../archetypes/A11-bst-ops.md) · [bst-delete-trace](../trees/bst-delete-trace.md)

---

## Assignment 1 — `GridWithAPointer`

```haskell
data Grid a = Grid { rows :: [[a]] }
  deriving (Eq, Show)

data Pointer = Pointer Int Int    -- row, col

data GridWithAPointer a = GWP (Grid a) Pointer
  deriving (Eq, Show)
```

Plus a zipper-style representation (varies by assignment release). See [A17 zipper](../archetypes/A17-zipper.md).

---

## Assignment 2 — Morse codec types

```haskell
data Symbol  = Dot | Dash deriving (Eq, Show)
data MorseCode = MorseCode [Symbol]
data Tree a    = Branch (Maybe Char) (Tree a) (Tree a) | TreeLeaf
  -- the Morse decoding tree
```

Codec spec:
```haskell
encode :: String -> Maybe MorseCode
decode :: MorseCode -> Maybe String
-- prop_roundtrip: decode . encode == Just (where defined)
```

**Linked pages:** [A07 codec-pair](../archetypes/A07-codec-pair.md) · [codec-family](../question-families/codec-family.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md)

---

## Assignment 3 — Free monad + scheduler types

```haskell
data Free f a = Pure a | Free (f (Free f a))

-- Sum of functors (coproduct):
data Sum f g a = InL (f a) | InR (g a)

-- A scheduler's effect signature might be:
data Sched a = Yield a | Sleep Int a | Stop
  deriving Functor       -- may be hand-written to obey -XSafe
```

**Linked pages:** [A14 multi-effect](../archetypes/A14-multi-effect-interp.md) · [multi-effect](../monads/multi-effect.md) · [A20 laws/iso](../archetypes/A20-laws-iso.md)

---

## Quick recognition cheat-sheet

| If `Types.hs` declares… | You're in… |
|---|---|
| `Rose a = Leaf a \| Branch [Rose a]` | Mock Q1 / rose-tree archetype (A01) |
| `(Heap, Heap)` + `Player = First \| Second` | Mock Q3 / Nim state |
| `Expr` with `TT \| FF \| Not \| And…` | Mock Q5 / propositional logic |
| `Circuit = Wire String \| Nand …` | Mock Q5 target |
| `BT a = Empty \| Fork a …` | Generic binary tree |
| `Grid a` + `Pointer` | Assignment 1 |
| `Symbol = Dot \| Dash` | Assignment 2 Morse |
| `Free f a = Pure a \| Free …` | Assignment 3 Free-monad scheduler |

## See also

**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A02 state game](../archetypes/A02-state-game.md) · [A05 ADT translation](../archetypes/A05-adt-translation.md) · [A07 codec pair](../archetypes/A07-codec-pair.md) · [A11 BST ops](../archetypes/A11-bst-ops.md) · [A14 multi-effect interp](../archetypes/A14-multi-effect-interp.md)
**Mock + assignments:** [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md)
**Theory:** [binary-tree](../trees/binary-tree.md) · [rose-tree](../trees/rose-tree.md) · [expression-tree](../trees/expression-tree.md) · [state](../monads/state.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
