<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **MUTATION-INDEX**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · [IF-YOU-SEE-X](./IF-YOU-SEE-X.md) · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · [MASTER-INDEX](./MASTER-INDEX.md) · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · **MUTATION-INDEX** · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# MUTATION-INDEX

Every mutation across all 24 question families on one page. **Use this when** you've matched an archetype but want to scan the *exact list* of variants the examiner might pick.

The vault carries **293 mutations** across **24 families** (235 seed + 28 Phase-4 + 30 Phase-12 expansions). Cap raised to 25 mutations per family in Phase 12. The seed list comes from the 150 practice problems and assignment archive; the Phase 4/12 additions cover *structurally different* mutations the examiner has not yet been seen to set but credibly could.

**New in Phase 12:** [string-ops-family](../question-families/string-ops-family.md) (13 mutations on string predicates / transforms / decomposition); tree-counting / tree-validation / tree-transform expanded with 5 new mutations each (M13–M17).

**Mental model:** an archetype is a question *shape*; a mutation is the *dial* the examiner turns. Read the family file to see how the mutation's code differs from the archetype template.

---

## Family count at a glance

24 families · **293 mutations** · cap raised to 25 per family in Phase 12.

| Family | Mutations | Archetype | File |
|---|---:|---|---|
| [adt-translation-family](#adt-translation-family) | 12 | A05 | [adt-translation-family](../question-families/adt-translation-family.md) |
| [applicative-monad-instance-family](#applicative-monad-instance-family) | 11 | A06 / A24 | [applicative-monad-instance-family](../question-families/applicative-monad-instance-family.md) |
| [bst-ops-family](#bst-ops-family) | 12 | A11 | [bst-ops-family](../question-families/bst-ops-family.md) |
| [codec-family](#codec-family) | 12 | A07 | [codec-family](../question-families/codec-family.md) |
| [env-eval-family](#env-eval-family) | 11 | A08 / A14 | [env-eval-family](../question-families/env-eval-family.md) |
| [error-handling-family](#error-handling-family) | 12 | A14 | [error-handling-family](../question-families/error-handling-family.md) |
| [functor-instance-family](#functor-instance-family) | 11 | A06 / A22 | [functor-instance-family](../question-families/functor-instance-family.md) |
| [lazy-infinite-family](#lazy-infinite-family) | 12 | A18 | [lazy-infinite-family](../question-families/lazy-infinite-family.md) |
| [list-comp-family](#list-comp-family) | 11 | A21 | [list-comp-family](../question-families/list-comp-family.md) |
| [list-fold-family](#list-fold-family) | 12 | A10 | [list-fold-family](../question-families/list-fold-family.md) |
| [list-rewrite-family](#list-rewrite-family) | 12 | A09 | [list-rewrite-family](../question-families/list-rewrite-family.md) |
| [matrix-predicate-family](#matrix-predicate-family) | 12 | A04 | [matrix-predicate-family](../question-families/matrix-predicate-family.md) |
| [monad-combinator-family](#monad-combinator-family) | 12 | A03 | [monad-combinator-family](../question-families/monad-combinator-family.md) |
| [parser-family](#parser-family) | 11 | A16 | [parser-family](../question-families/parser-family.md) |
| [pretty-print-family](#pretty-print-family) | 11 | A13 | [pretty-print-family](../question-families/pretty-print-family.md) |
| [rose-ops-family](#rose-ops-family) | 11 | A01 | [rose-ops-family](../question-families/rose-ops-family.md) |
| [state-counter-family](#state-counter-family) | 11 | A02 | [state-counter-family](../question-families/state-counter-family.md) |
| [state-game-family](#state-game-family) | 12 | A02 / A23 | [state-game-family](../question-families/state-game-family.md) |
| **[string-ops-family](../question-families/string-ops-family.md)** *(new in Phase 12)* | **13** | A09 / A21 | [string-ops-family](../question-families/string-ops-family.md) |
| [tree-counting-family](#tree-counting-family) | **17** *(↑12)* | A01 | [tree-counting-family](../question-families/tree-counting-family.md) |
| [tree-extract-family](#tree-extract-family) | 11 | A01 / A12 | [tree-extract-family](../question-families/tree-extract-family.md) |
| [tree-transform-family](#tree-transform-family) | **16** *(↑11)* | A01 | [tree-transform-family](../question-families/tree-transform-family.md) |
| [tree-validation-family](#tree-validation-family) | **17** *(↑12)* | A01 | [tree-validation-family](../question-families/tree-validation-family.md) |
| [writer-trace-family](#writer-trace-family) | 11 | A15 | [writer-trace-family](../question-families/writer-trace-family.md) |
| **Total** | **293** | | |

---

## How to read each row

```
### Mutation N — name (= problem M)
```

- `Mutation N` — slot number within the family. Cap 25.
- `name` — the function the examiner asks for.
- `(= problem M)` — the matching practice problem, if any, in [Haskell-Practice-Problems.md](../../fp-learning-2025/Haskell-Practice-Problems.md).
- Phase-4 additions (mutations 11 / 12 added by the wiki-upgrade pass) are *structurally* different — they exercise a recursion shape, fold variant, or invariant the others don't.

---

## Tree-axis families

Every Tree A01 question is one mutation from one of these four families. If you only revise four lists, revise these.

### tree-counting-family

> Archetype A01 · 12 mutations · "How many nodes / leaves / depths / ..."

1. **sizeBT** — total node count. Easy.
2. **leavesCount** — number of `Empty` (or `Leaf`) terminals.
3. **internalCount** — non-leaf nodes.
4. **countBT** — count occurrences of a value `x`.
5. **countBy** — hidden-predicate version (`(a -> Bool)` instead of `a == x`).
6. **countAtDepth** — slice count at exact depth.
7. **countBelowDepth** — count strictly above a threshold.
8. **countLeavesByTag** — tagged leaves (`Leaf Bool` vs `Leaf Int`).
9. **countNodesSatisfying** — predicate sees the path from root.
10. **(Int, Int) split count** — leaves and internals in *one* pass.
11. **countByDepth** — returns `[(depth, count)]` assoc list. Phase-4 addition.
12. **countSatisfyingWithAccumulator** — single-pass strict accumulator. Phase-4 addition — exercises strict folding.

Open: [tree-counting-family](../question-families/tree-counting-family.md).

### tree-validation-family

> Archetype A01 · 12 mutations · "Return `True` iff ..."

1. **isBST** — binary-search-tree invariant via bound threading.
2. **isBalanced** — AVL-style `|h(l) − h(r)| ≤ 1`.
3. **isComplete** — every level full except last; left-filled.
4. **isNBranching** — rose-tree predicate from Mock Q1.
5. **isHeap** — max-heap predicate.
6. **isMirror** — two trees structurally mirrored.
7. **isSymmetric** — single tree internally mirrored.
8. **isFull** — every node has 0 or 2 children.
9. **isAllPositive** — value-only predicate over the tree.
10. **allBT** — hidden-predicate version of 9 (takes `(a -> Bool)`).
11. **isPathSumK** — root-to-leaf path sum equals `k`. Phase-4 addition — DFS with accumulator.
12. **isBalanced (single-pass)** — height check returning `Maybe Int` so balance is decided in one pass. Phase-4 addition — short-circuit fold.

Open: [tree-validation-family](../question-families/tree-validation-family.md).

### tree-transform-family

> Archetype A01 · 11 mutations · "Return a new tree where every node ..."

1. **mapBT** — `(a -> b) -> BT a -> BT b`. The Functor instance.
2. **mirror** — swap children at every node.
3. **pruneDepth** — cut at depth `k`.
4. **pruneRose** — Mock Q1 part 2.
5. **filterBT** — keep nodes matching a predicate; collapse failures.
6. **mergeBT** — zip two shape-identical BTs.
7. **addPathSum** — annotate each node with the sum of ancestors.
8. **fmapInTree** — Functor-instance presentation of `mapBT`.
9. **reverseAtEvenDepth** — depth-conditional mirror.
10. **substituteAt** — replace a marked subtree.
11. **mirrorOnlyIf** — predicate-guarded structural transform. Phase-4 addition — combines transform + validation.

Open: [tree-transform-family](../question-families/tree-transform-family.md).

### tree-extract-family

> Archetype A01 / A12 · 11 mutations · "Return a list of ..."

1. **flattenInOrder** — left → node → right.
2. **flattenPreOrder** — node → left → right.
3. **flattenPostOrder** — left → right → node.
4. **leavesList** — only the leaves.
5. **nodesAtDepth** — slice at one level.
6. **pathsToLeaves** — list of root-to-leaf paths.
7. **flattenBFS** — level-order (breadth-first) traversal.
8. **flattenRose** — equivalent for rose trees.
9. **leafPaths-as-strings** — encode each path as a `String`.
10. **flattenWithDepth** — annotate each value with depth.
11. **extractMin** — return min + tree with min removed. Phase-4 addition — uses a Maybe pivot.

Open: [tree-extract-family](../question-families/tree-extract-family.md).

---

## BST + Rose families

### bst-ops-family

> Archetype A11 · 12 mutations · BST insert / delete / member / etc.

1. **memberBST** — `x ∈ BST?`.
2. **insertBST** — preserves BST invariant.
3. **fromList** — `[a] -> BST a` via repeated insert.
4. **bstSort** — sort by build + in-order flatten.
5. **minBST / maxBST** — leftmost / rightmost.
6. **deleteBST** — 4 cases (Empty, leaf, one child, two children with in-order successor). See [bst-delete-trace](../trees/bst-delete-trace.md).
7. **predecessorBST** — largest value `< x`.
8. **successorBST** — smallest value `> x`.
9. **toSortedList** — same as flattenInOrder for a BST.
10. **heightBST** — specialised height.
11. **rangeCount** — count entries within `[lo, hi]`. Phase-4 addition — range filter.
12. **kthSmallest** — in-order traversal with early exit. Phase-4 addition — short-circuit fold.

Open: [bst-ops-family](../question-families/bst-ops-family.md). Worked delete: [bst-delete-trace](../trees/bst-delete-trace.md).

### rose-ops-family

> Archetype A01 · 11 mutations · Rose tree operations.

1. **sizeRose** — total node count.
2. **heightRose** — max depth.
3. **flattenRose** — pre-order list.
4. **isNBranching** — Mock Q1 part 1.
5. **prune** — Mock Q1 part 2.
6. **mapRose** — Functor instance.
7. **foldRose** — generic structural fold.
8. **countLeavesRose** — nodes with no children.
9. **toRose / fromRose** — Assignment 3 Task 1 — isomorphic with `Free []`.
10. **maxDepthValue** — value at greatest depth.
11. **isNBranchingOrLeaf** — relaxed predicate. Phase-4 addition.

Open: [rose-ops-family](../question-families/rose-ops-family.md).

---

## List-axis families

### list-rewrite-family

> Archetype A09 · 12 mutations · Re-implement Prelude functions.

1. **myLength**.
2. **mySum**.
3. **myProduct**.
4. **myReverse** — naive O(n²) `xs ++ [x]`.
5. **myMap**.
6. **myFilter**.
7. **myTake**.
8. **myDrop**.
9. **myZip**.
10. **myElem**.
11. **fastReverse** — accumulator O(n).
12. **myConcat**.

Open: [list-rewrite-family](../question-families/list-rewrite-family.md). Family is **LOCKED** at 12.

### list-fold-family

> Archetype A10 · 12 mutations · "Implement X using foldr/foldl."

1. **sumWithFoldr**.
2. **lengthWithFoldr**.
3. **mapWithFoldr**.
4. **filterWithFoldr**.
5. **reverseWithFoldl**.
6. **allWithFoldr**.
7. **anyWithFoldr**.
8. **concatWithFoldr**.
9. **scanrSum** — running sums from right.
10. **scanlMax** — running max from left.
11. **composeFoldr** — `compose'` problem.
12. **foldr-via-foldl** — the bridge problem. Phase-4 addition.

Open: [list-fold-family](../question-families/list-fold-family.md). Family is **LOCKED** at 12.

### list-comp-family

> Archetype A21 · 11 mutations · List comprehension synthesis.

1. **pyths** — Pythagorean triples.
2. **factors**.
3. **perfects** — perfect numbers.
4. **positions** — indexes where predicate holds.
5. **pairs** — adjacent pairs.
6. **wordCount**.
7. **cartesian** — `[(x, y) | x <- xs, y <- ys]`.
8. **scalar / dot product**.
9. **primesUpTo**.
10. **allPairs** — ordered distinct pairs.
11. **perfectNumbers** — list-comp with proper-divisor predicate. Phase-4 addition.

Open: [list-comp-family](../question-families/list-comp-family.md).

### matrix-predicate-family

> Archetype A04 · 12 mutations · `[[Int]] -> Bool`.

1. **isMagicSquare** — Mock Q4.
2. **isSudokuRowValid**.
3. **isSudokuValid** — rows + cols + 9 sub-blocks.
4. **winner** — TicTacToe.
5. **isValidLatinSquare**.
6. **gridContains**.
7. **rowSums equal each other but not diagonals**.
8. **countLiveNeighbours** — Conway.
9. **isWinningRow** — parameterised line length.
10. **isSquareGrid**.
11. **isMagicAntiSquare** — anti-diagonal sum check. Phase-4 addition.
12. **isLatinSquare** — no repeats per row + column. Phase-4 addition.

Open: [matrix-predicate-family](../question-families/matrix-predicate-family.md).

---

## Monad-axis families

### monad-combinator-family

> Archetype A03 · 12 mutations · `Monad m =>` polymorphic combinators.

1. **applyNTimes** — Mock Q2. `(a -> m a) -> Int -> a -> m a`.
2. **mapM'** — own implementation of `mapM`.
3. **sequenceM** — own implementation of `sequence`.
4. **replicateM'** — `n` copies of one action.
5. **forM'** — `mapM'` with args flipped.
6. **foldM'** — monadic fold.
7. **filterM'** — monadic filter.
8. **mapMTree** — `mapM` lifted to BT.
9. **iterate'** — lazy infinite monadic iterate.
10. **whenM / unlessM**.
11. **applyNTimesUntil** — early-exit predicate. Phase-4 addition — short-circuiting.
12. **mapMWithState** — `Monad m` + accumulator state. Phase-4 addition — tuple bound.

Open: [monad-combinator-family](../question-families/monad-combinator-family.md).

### state-game-family

> Archetype A02 / A23 · 12 mutations · State-monad game / simulation.

1. **gameOver** — Mock Q3 part 1.
2. **takeTokens** — Mock Q3 part 2.
3. **fresh**.
4. **labelTree**.
5. **pushAll**.
6. **fibState**.
7. **evalCalc** — stack calculator.
8. **uniqueIds**.
9. **TicTacToe winner**.
10. **Conway one step**.
11. **takeTokensWithLog** — State + Writer fused. Phase-4 addition — multi-effect.
12. **rewindMove** — undo by replaying prefix. Phase-4 addition — different data layout.

Open: [state-game-family](../question-families/state-game-family.md).

### state-counter-family

> Archetype A02 · 11 mutations · State as counter / fresh-name supply.

1. **fresh** — `State Int Int`, increment-and-return.
2. **freshN** — return `n` fresh ids.
3. **countLeaves** — count leaves while traversing.
4. **labelTree (in-order)**.
5. **labelTree (pre-order)**.
6. **uniqueIds**.
7. **labelEdges** — rose-tree variant.
8. **countAtomsInTree** — counter as accumulator.
9. **relabel-by-rank** — first-occurrence position.
10. **fresh with reset**.
11. **freshN (variant)** — return `n` integers in one shot. Phase-4 addition.

Open: [state-counter-family](../question-families/state-counter-family.md).

### writer-trace-family

> Archetype A15 · 11 mutations · Writer monad tracing.

1. **logFactorial**.
2. **countSteps** — Collatz.
3. **traceEval** — log every Expr eval step.
4. **audit** — log only branches matching a predicate.
5. **numbered log** — counter + log.
6. **concurrentWriter** — two log streams.
7. **WriterT over Maybe** — log even on failure.
8. **logFib** — log calls during fib.
9. **letBindingLog** — log every let-binding in eval.
10. **log replay**.
11. **foldWithTrace** — fold list with each step logged. Phase-4 addition.

Open: [writer-trace-family](../question-families/writer-trace-family.md).

### error-handling-family

> Archetype A14 · 11 mutations · Maybe / Either.

1. **safeHead**.
2. **safeDiv**.
3. **safeSqrt**.
4. **safeIndex**.
5. **chainDivisions** — `do`-block of safeDivs.
6. **firstJust**.
7. **catMaybes' / mapMaybe'**.
8. **zipEither** — Either-typed error.
9. **parseDigit / parseNumber**.
10. **throwError variant** — MonadError.
11. **safeEvalEither** — Either with structured error type. Phase-4 addition.

Open: [error-handling-family](../question-families/error-handling-family.md).

### env-eval-family

> Archetype A08 / A14 · 11 mutations · Expression evaluation with environment.

1. **evalExpr** — no variables.
2. **evalWithEnv** — `Var` lookup, `Maybe`.
3. **evalEither** — typed errors.
4. **evalRecursiveLet** — `letrec`.
5. **evalDivision** — div-by-zero.
6. **evalReader** — Reader-monad form.
7. **evalAsString** — eval to `String`.
8. **shadowingTest** — semantics property.
9. **evalStateful** — variable mutation.
10. **evalFreeVars** — collect free variables.
11. **evalMaybeWithDefault** — Maybe fallback default. Phase-4 addition.

Open: [env-eval-family](../question-families/env-eval-family.md).

---

## Typeclass-instance families

### functor-instance-family

> Archetype A06 · 11 mutations · `instance Functor T`.

1. **Functor MyMaybe**.
2. **Functor MyList**.
3. **Functor BT**.
4. **Functor Rose**.
5. **Functor Pair** — only the second component.
6. **Functor Reader**.
7. **Functor Either** — only `Right`.
8. **Functor Const**.
9. **Functor Identity**.
10. **Functor Free**.
11. **Functor Phantom-Param ADT**. Phase-4 addition.

Open: [functor-instance-family](../question-families/functor-instance-family.md).

### applicative-monad-instance-family

> Archetype A06 / A24 · 11 mutations · `Applicative` / `Monad` instances.

1. **MyMaybe** (Applicative + Monad).
2. **MyList**.
3. **Identity**.
4. **Reader**.
5. **State** — custom version.
6. **Writer** — with `Monoid w`.
7. **Free f** — A3 setup.
8. **Either e**.
9. **Pair e** — with `Monoid e`.
10. **ZipList Applicative** — non-monad.
11. **Applicative for ZipList** (pairwise `<*>`). Phase-4 addition.

Open: [applicative-monad-instance-family](../question-families/applicative-monad-instance-family.md).

---

## ADT + Codec + Pretty + Parser families

### adt-translation-family

> Archetype A05 · 12 mutations · ADT → ADT structural translation.

1. **circuit** — Mock Q5.
2. **toNNF** — negation-normal form.
3. **exprToCalc / desugar**.
4. **exprToList** — linearise to postfix list.
5. **toCNF / pushAndOverOr**.
6. **simplifyExpr** — constant folding.
7. **exprToTree** — parse-tree visualisation.
8. **circuitInverse** — reverse direction.
9. **bracketTreeToString** — Assignment 2 Ex 6.
10. **exprToString** — pretty-print, no parens.
11. **exprToList (in-order flatten)** — A05 × A09. Phase-4 addition.
12. **treeToBalancedList (rebalance level-order)** — A05 × A12. Phase-4 addition.

Open: [adt-translation-family](../question-families/adt-translation-family.md).

### codec-family

> Archetype A07 · 12 mutations · Encode + decode pairs.

1. **shift** — Caesar single char.
2. **encode** — Caesar whole string.
3. **caesarDecode**.
4. **encodeWord** — Morse, single word (A2 Ex 1.1).
5. **encodeText** — Morse, multi-word.
6. **decodeText** — Morse via table.
7. **decodeTextWithTree** — Morse via tree.
8. **ramify** — table → tree.
9. **rle** — run-length encoding.
10. **rld** — run-length decoding.
11. **base-N conversion**. Phase-4 addition.
12. **rotN** — parameterised Caesar with round-trip parameter. Phase-4 addition.

Open: [codec-family](../question-families/codec-family.md).

### pretty-print-family

> Archetype A13 · 11 mutations · Custom `Show` / pretty-printer.

1. **show Color as hex**.
2. **pretty-print Expr** — precedence-aware.
3. **display BT** — textual.
4. **show Vec3**.
5. **show Direction**.
6. **pretty-print Logic expression**.
7. **show Rose** — indented.
8. **showsPrec implementation** — Prelude pattern.
9. **pretty-print Bracket tree** (A2 Ex 6).
10. **toJSON-like** — recursive ADT → structured string.
11. **showsBT** — `showS`-style accumulator. Phase-4 addition.

Open: [pretty-print-family](../question-families/pretty-print-family.md).

### parser-family

> Archetype A16 · 11 mutations · Parser combinators.

1. **item / sat / digit**.
2. **parseNat**.
3. **char / string**.
4. **token** — eat surrounding whitespace.
5. **sepBy / sepBy1**.
6. **chainl1** — left-associative operator chain.
7. **parseExpr** — precedence-aware.
8. **parseBool / parseKeyword**.
9. **well-bracketed** — A2 Ex 6.
10. **parseFloat / parseSigned**.
11. **chainl1Parser** — left-associative precedence variant. Phase-4 addition. See [parser-chainl1](../interpreters/parser-chainl1.md).

Open: [parser-family](../question-families/parser-family.md).

---

## Laziness family

### lazy-infinite-family

> Archetype A18 · 11 mutations · Infinite / lazy data.

1. **ones**.
2. **fibs** — Fibonacci via `zipWith`.
3. **primes via sieve**.
4. **lazy Nat** — `data Nat = Z | S Nat`.
5. **lengthNat**.
6. **memoFib via infinite tree**.
7. **fix'** — own `fix`.
8. **iterate'** — own `iterate`.
9. **repeat / cycle**.
10. **naturals / odds**.
11. **takeWhileFinite** — lazy infinite generator + take prefix. Phase-4 addition.

Open: [lazy-infinite-family](../question-families/lazy-infinite-family.md).

---

## Difficulty tiers (across families)

| Tier | Description | Example mutations |
|---|---|---|
| **Easy** | One-pattern recursion; one accumulator at most. | sizeBT · myLength · mySum · mapBT · ones · safeHead |
| **Medium** | Two recursion shapes (e.g. tree + list), one effect, one invariant. | isBalanced · labelTree · evalWithEnv · encode · isMagicSquare · mapMTree · applyNTimes |
| **Hard** | Two effects fused, or a multi-layer pattern. | takeTokensWithLog · evalRecursiveLet · chainl1 · WriterT over Maybe · transformer-stack-order |
| **Nasty** | Subtle invariant or non-obvious base case. | isBST (Empty case) · isComplete · deleteBST (two-children) · prune semantics · log order under failure |

---

## See also

**Family directory:** [question-families/](../question-families/README.md) — full enumeration with code per mutation.
**Archetype index:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) — entry points for each archetype.
**Cross-topic index:** [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) — how mutations cross axes.
**Phrase → mutation:** [IF-YOU-SEE-X](./IF-YOU-SEE-X.md).
**Type → family:** [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md).
**Problem → mutation:** [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) — 150 numbered practice problems.
**Mock-Q-by-mutation:** [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) — five mock specs verbatim.
**QuickCheck attacks:** [quickcheck/QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) — what each mutation gets attacked with.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
