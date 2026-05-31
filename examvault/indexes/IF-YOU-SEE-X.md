<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [indexes](./README.md) · **IF YOU SEE X → THINK Y**

<!-- siblings:start -->
> **Peers:** [ARCHETYPE-INDEX](./ARCHETYPE-INDEX.md) · [ASSIGNMENT-INDEX](./ASSIGNMENT-INDEX.md) · [BEGINNER-INDEX](./BEGINNER-INDEX.md) · [CROSS-TOPIC-INDEX](./CROSS-TOPIC-INDEX.md) · **IF-YOU-SEE-X** · [KEYWORD-INDEX](./KEYWORD-INDEX.md) · [LECTURE-INDEX](./LECTURE-INDEX.md) · [MASTER-INDEX](./MASTER-INDEX.md) · [MOCK-Q-INDEX](./MOCK-Q-INDEX.md) · [MUTATION-INDEX](./MUTATION-INDEX.md) · [PRELUDE-INDEX](./PRELUDE-INDEX.md) · [PROBLEM-NUMBER-INDEX](./PROBLEM-NUMBER-INDEX.md) · [TYPE-SIGNATURE-DATABASE](./TYPE-SIGNATURE-DATABASE.md) · [TYPES-REFERENCE](./TYPES-REFERENCE.md)
<!-- siblings:end -->






# IF YOU SEE X → THINK Y

Phrase trigger → archetype/family/file lookup. Ctrl-F the keyword from the question.

> Format per row: `phrase in question` · `primary archetype` · `family or file` · `note`.
> Tables grouped by topic (RECURSION / MONADS / TYPECLASSES / INTERPRETERS / PARSERS / TREES / LAZY / ADTs / META / QC / GRIDS / GENERIC).

---

## RECURSION (list & general)

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "implement my…" / "reimplement" / "without using" | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | cons recursion with explicit base case |
| "for each element" / "transform each" | [A09](../archetypes/A09-prelude-reimpl.md) / [A10](../archetypes/A10-fold-reformulation.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | usually `map`, sometimes `foldr` |
| "efficient" / "single pass" / "O(n)" | [A09](../archetypes/A09-prelude-reimpl.md) (acc) | [list-rewrite-family](../question-families/list-rewrite-family.md) | accumulator `go` helper |
| "linear time" / "in one pass" | [A09](../archetypes/A09-prelude-reimpl.md) (acc) | [foldl-vs-foldr](../pitfalls/HIGH-severity.md#p-023) | use foldl' / accumulator |
| "consecutive" / "adjacent" / "alternating" / "pairs of" | [A09](../archetypes/A09-prelude-reimpl.md) / [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | `(x:y:xs)` look-ahead pattern |
| "merge two sorted lists" | [A09](../archetypes/A09-prelude-reimpl.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | dual base + Ord guard |
| "first n" / "drop n" / "take n" / "n times" | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | count-decrement recursion; handle n≤0 |
| "without recursion" / "using foldr only" / "fold form" | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) | `foldr` with `\x acc -> …` |
| "using foldl" | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) | `foldl` for tail-recursive accumulator |
| "scan" / "running total" / "prefix sum" | [A10](../archetypes/A10-fold-reformulation.md) | [list-fold-family](../question-families/list-fold-family.md) | `scanl` or manual fold variant |
| "partition" / "split" / "two lists" | [A09](../archetypes/A09-prelude-reimpl.md) / [A10](../archetypes/A10-fold-reformulation.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | pair accumulator |
| "interleave" / "zip" / "alternating from two" | [A09](../archetypes/A09-prelude-reimpl.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | dual base case |
| "merge sort" / "msort" / "split-merge" | [A09](../archetypes/A09-prelude-reimpl.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | `splitAt (length xs `div` 2)` |
| "quicksort" / "qsort" | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | three list-comprehensions |
| "sort a list" / "insertion/selection/bubble sort" / "sorting algorithm" / "write your own sort" | [sorting](../haskell-basics/sorting.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | 5 hand-rolled sorts; quicksort needs `>=` on one side; merge needs the `[x]` base case |
| "every" / "all elements satisfy" | [A10](../archetypes/A10-fold-reformulation.md) | [list-fold-family](../question-families/list-fold-family.md) | foldr-AND or `all p` |
| "any" / "exists" / "at least one" | [A10](../archetypes/A10-fold-reformulation.md) | [list-fold-family](../question-families/list-fold-family.md) | foldr-OR or `any p` |
| "remove duplicates" / "dedupe" | [A09](../archetypes/A09-prelude-reimpl.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | preserve order of first occurrence |
| "lookup in association list" | [A09](../archetypes/A09-prelude-reimpl.md) (Maybe) | [maybe](../monads/maybe.md) | reimplement `lookup :: Eq a => a -> [(a,b)] -> Maybe b` |
| "first Just" / "first matching" | [A09](../archetypes/A09-prelude-reimpl.md) (Maybe) | [maybe](../monads/maybe.md) | foldr or pattern match |
| "Pythagorean triples" / "triples (a,b,c) with…" | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | multi-generator with predicate |
| "factors of n" / "divisors" | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | `[x | x <- [1..n], n `mod` x == 0]` |
| "perfect numbers" | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | use `sum (factors n) == n` (proper divisors) |
| "all pairs" / "Cartesian product" | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | `[(x,y) | x<-xs, y<-ys]` |
| "knight moves" / "valid grid moves" | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-monad](../monads/list-monad.md) | list monad do-notation |
| "letter frequencies" / "char counts" | [A21](../archetypes/A21-list-comp-synthesis.md) (string) | [codec-family](../question-families/codec-family.md) | `[(c, length [x | x<-s, x==c]) | c<-['a'..'z']]` |

## TREES (BT / BST / Rose / Expr)

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "binary tree" / "data BT" / "Empty / Fork" | [A01](../archetypes/A01-tree-recursion.md) | [binary-tree](../trees/binary-tree.md) | `data BT a = Empty | Fork a (BT a) (BT a)` |
| "Rose tree" / "any number of children" / "[Rose a]" | [A01](../archetypes/A01-tree-recursion.md) | [rose-tree](../trees/rose-tree.md) | watch BOTH definitions! |
| "expression tree" / "data Expr" / "Add / Mul / Var" | [A05](../archetypes/A05-adt-translation.md) / [A08](../archetypes/A08-env-eval.md) | [expression-tree](../trees/expression-tree.md) | gateway to interpreter |
| "Leaf | Branch" Rose form (Mock) | [A01](../archetypes/A01-tree-recursion.md) | [rose-tree](../trees/rose-tree.md) | value at leaves only |
| "Branch a [Rose a]" Data2 form | [A01](../archetypes/A01-tree-recursion.md) | [rose-tree](../trees/rose-tree.md) | value at every node |
| "count" / "size" / "how many nodes" | [A01](../archetypes/A01-tree-recursion.md) | [tree-counting-family](../question-families/tree-counting-family.md) | additive recursion `1+ ...` |
| "height" / "depth" / "deepest path" | [A01](../archetypes/A01-tree-recursion.md) | [tree-counting-family](../question-families/tree-counting-family.md) | `1 + max (h l) (h r)` |
| "leaves" / "values at leaves" | [A01](../archetypes/A01-tree-recursion.md) | [tree-extract-family](../question-families/tree-extract-family.md) | `Fork _ Empty Empty` pattern |
| "mirror" / "flip" / "swap left/right" | [A01](../archetypes/A01-tree-recursion.md) | [tree-transform-family](../question-families/tree-transform-family.md) | swap subtrees in Fork case |
| "in-order traversal" / "left, root, right" | [A01](../archetypes/A01-tree-recursion.md) | [tree-traversals](../trees/tree-traversals.md) | `flatten l ++ [x] ++ flatten r` |
| "pre-order" / "root, left, right" | [A01](../archetypes/A01-tree-recursion.md) | [tree-traversals](../trees/tree-traversals.md) | `x : flatten l ++ flatten r` |
| "post-order" / "left, right, root" | [A01](../archetypes/A01-tree-recursion.md) | [tree-traversals](../trees/tree-traversals.md) | `flatten l ++ flatten r ++ [x]` |
| "BST" / "binary search tree" / "search tree" | [A11](../archetypes/A11-bst-ops.md) | [bst](../trees/bst.md) | `Ord a =>` |
| "isBST" / "BST invariant" | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | bound-threaded, NOT immediate-child check |
| "insert into BST" / "insertBST" | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | 3-way Ord guard |
| "delete from BST" | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | 4-case: empty/leaf/one-child/two-children |
| "BST delete two children" / "in-order successor" / "predecessor for delete" | [A11](../archetypes/A11-bst-ops.md) | [bst-delete-trace](../trees/bst-delete-trace.md) | worked trace using `extractMin`/`extractMax` — the only sub-case that loses marks |
| "Eq instance for trees" / "tree equality" / "structural equality" | [A22](../archetypes/A22-typeclass-instance.md) | [eq-ord](../typeclasses/eq-ord.md) | one equation per ctor pair, recurse on subtrees |
| "member" / "lookup in BST" | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | O(log n) average |
| "bstSort" / "sort using BST" | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | `flattenInOrder . fromList` |
| "isNBranching" | [A01](../archetypes/A01-tree-recursion.md) | [rose-ops-family](../question-families/rose-ops-family.md) | Mock Q1 — every Branch has exactly n children |
| "prune n" | [A01](../archetypes/A01-tree-recursion.md) | [rose-ops-family](../question-families/rose-ops-family.md) | Mock Q1 — keep first n children |
| "evalExpr" / "evaluate this expression" | [A08](../archetypes/A08-env-eval.md) / [A05](../archetypes/A05-adt-translation.md) | [simple-arith](../interpreters/simple-arith.md) | per-ctor case-fold |
| "depthExpr" / "expression depth" | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) | `1 + max (d e1) (d e2)` |
| "addresses in tree" / "paths to nodes" | [A01](../archetypes/A01-tree-recursion.md) | [A17-zipper](../archetypes/A17-zipper.md) | `[Direction]` accumulator |
| "label every node" / "number every node" | [A02](../archetypes/A02-state-game.md) | [tree-x-state](../cross-matrix/tree-x-state.md) | State Int + fresh |
| "every node gets fresh id" | [A02](../archetypes/A02-state-game.md) | [tree-x-state](../cross-matrix/tree-x-state.md) | State monad threading |
| "preserve structure with effect" | [A03](../archetypes/A03-generic-monad.md) | [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md) | `mapMTree :: Monad m => …` |
| "Tree of Maybes to Maybe of Tree" | [A03](../archetypes/A03-generic-monad.md) | [tree-x-generic-monad](../cross-matrix/tree-x-generic-monad.md) | `sequence` over tree |
| "expression with variables" / "Var String" | [A08](../archetypes/A08-env-eval.md) | [A08-env-eval](../archetypes/A08-env-eval.md) | env lookup |
| "Let binding" / "Let x e1 e2" | [A08](../archetypes/A08-env-eval.md) | [A08-env-eval](../archetypes/A08-env-eval.md) | extend env before body |
| "translate Expr to Circuit" / "convert to Nand-only" | [A05](../archetypes/A05-adt-translation.md) | [A05-adt-translation](../archetypes/A05-adt-translation.md) | Mock Q5 — desugar pipeline |
| "remove Implies" / "normalize to subset" | [A05](../archetypes/A05-adt-translation.md) | [adt-translation-family](../question-families/adt-translation-family.md) | per-ctor rewrite |
| "extend the interpreter" / "add new operator" | [A19](../archetypes/A19-extend-interpreter.md) | [A19-extend-interpreter](../archetypes/A19-extend-interpreter.md) | 3-layer change |
| "pretty print expression" / "Show Expr" | [A13](../archetypes/A13-pretty-printer.md) | [A13-pretty-printer](../archetypes/A13-pretty-printer.md) | showsPrec for precedence |
| "tree of forks" / "internal nodes" | [A01](../archetypes/A01-tree-recursion.md) | [tree-counting-family](../question-families/tree-counting-family.md) | predicate over Fork |
| "skewed tree" / "deep right-leaning" | [A01](../archetypes/A01-tree-recursion.md) (QC) | [trees-attacks](../quickcheck/trees-attacks.md) | stack overflow risk |
| "BST delete two children" / "in-order successor" / "predecessor replacement" | [A11](../archetypes/A11-bst-ops.md) | [bst-delete-trace](../trees/bst-delete-trace.md) | worked traces of both strategies (successor + predecessor) |
| "Eq instance for trees" / "compare two trees" | [A22](../archetypes/A22-typeclass-instance.md) | [eq-ord](../typeclasses/eq-ord.md) | structural equality per ctor |

## MONADS (recognition by phrase)

> Tier-1 phrasings live here. For transformer-order specifics see STATE/WRITER section below.

| Phrase in question | Monad | File | Note |
|---|---|---|---|
| "may fail" / "return Nothing if" / "partial" | `Maybe` | [maybe](../monads/maybe.md) | base for safe operations |
| "safe" + "div / sqrt / head" | `Maybe` | [maybe](../monads/maybe.md) | `safeDiv`, `safeHead` etc. |
| "fail with error message" / "throw error" | `Either e` or `MonadError` | [either](../monads/either.md) | `Left msg` carries message |
| "divide by zero throws" | `MonadError` | [monaderror](../monads/monaderror.md) | `throwError "div zero"` |
| "look up variable, error if missing" | `Either` or `MonadError` | [monaderror](../monads/monaderror.md) | + env eval |
| "hidden state" / "mutable" / "tracked count" | `State s` | [state](../monads/state.md) | get / put / modify |
| "track number of steps" / "counter" | `State Int` or `Writer (Sum Int)` | [state](../monads/state.md) | choose by what's primary |
| "label tree" / "fresh id per node" | `State Int` | [tree-x-state](../cross-matrix/tree-x-state.md) | + fresh / labelTree |
| "fresh names" / "unique id" / "gensym" | `State Int` | [state](../monads/state.md) | `fresh` combinator |
| "accumulate logs" / "trace messages" | `Writer [String]` | [writer](../monads/writer.md) | `tell ["msg"]` |
| "running total / metric alongside" | `Writer (Sum Int)` | [writer](../monads/writer.md) | requires `Sum` monoid |
| "log of recursive calls" | `Writer` | [writer](../monads/writer.md) | `tell` at each step |
| "interactive" / "I/O" / "side effect" / "main" | `IO` | [io](../monads/io.md) | getLine/putStrLn |
| "non-determinism" / "all possible results" / "search" | `[]` (list monad) | [list-monad](../monads/list-monad.md) | do over list = comprehension |
| "read-only environment" / "configuration" / "lookup table" | `Reader r` | [reader](../monads/reader.md) | `ask`, `local` |
| "Monad m =>" in signature | generic | [A03-generic-monad](../archetypes/A03-generic-monad.md) | [A03](../archetypes/A03-generic-monad.md) combinator |
| "for any monad" / "polymorphic monad action" | generic | [A03-generic-monad](../archetypes/A03-generic-monad.md) | use `>>=`/`pure` only |
| "state + error" / "calculator with div zero" | `(MonadState, MonadError)` | [expr-state-either](../interpreters/expr-state-either.md) | multi-effect |
| "DSL of computation to re-interpret" | `Free f` | [multi-effect](../monads/multi-effect.md) | Pure/Free constructors |
| "round-robin" / "scheduler" / "yield" | `Free + State` | [multi-effect](../monads/multi-effect.md) | Assignment 3 |
| "in `do`-notation, return…" | depends on m | [README](../monads/README.md) | use `pure x`, not `Just x` |
| "without using do" | `>>=` form | [README](../monads/README.md) | translate `do {x<-m; …}` |
| "join" / "flatten nested monad" | generic | [generic-combinators](../monads/generic-combinators.md) | `join mma = mma >>= id` |
| "sequenceM" / "[m a] → m [a]" | generic | [generic-combinators](../monads/generic-combinators.md) | fold with `liftM2 (:)` |
| "mapM" / "for-each monadic" | generic | [generic-combinators](../monads/generic-combinators.md) | `mapM = sequence . map` |
| "filterM" / "monadic filter" | generic | [generic-combinators](../monads/generic-combinators.md) | choose per element |
| "replicateM" / "n monadic actions" | generic | [generic-combinators](../monads/generic-combinators.md) | replicate then sequence |
| "applyNTimes" / "iterate monadic n" | [A03](../archetypes/A03-generic-monad.md) | [A03-generic-monad](../archetypes/A03-generic-monad.md) | Mock Q2 — n+1 values, off-by-one trap |
| "monadic fold" / "foldM" / "foldr m" | generic | [generic-combinators](../monads/generic-combinators.md) | thread the effect |
| "when / unless" (conditional effect) | generic | [generic-combinators](../monads/generic-combinators.md) | `when p m = if p then m else pure ()` |

## TYPECLASSES (instance writing)

| Phrase in question | Class | File | Note |
|---|---|---|---|
| "preserve structure, transform values" | `Functor` | [functor](../typeclasses/functor.md) | `fmap` |
| "instance Functor T" | `Functor` | [A06-functor-instance](../archetypes/A06-functor-instance.md) | one equation per ctor |
| "fmap" / "(<$>)" | `Functor` | [functor](../typeclasses/functor.md) | container preserved |
| "apply wrapped fn to wrapped value" | `Applicative` | [applicative](../typeclasses/applicative.md) | `<*>` |
| "instance Applicative T" / "pure + <*>" | `Applicative` | [A24-applicative-instance](../archetypes/A24-applicative-instance.md) | requires Functor |
| "liftA2" / "lift binary fn" | `Applicative` | [applicative](../typeclasses/applicative.md) | `f <$> ma <*> mb` |
| "chain with dependency / context" | `Monad` | [monad](../typeclasses/monad.md) | `>>=` |
| "instance Monad T" / "return + >>=" | `Monad` | [A06-functor-instance](../archetypes/A06-functor-instance.md) | requires Applicative |
| "do-notation" | `Monad` | [monad](../typeclasses/monad.md) | desugars to `>>=` |
| "alternative / fallback parser" | `Alternative` | [alternative](../typeclasses/alternative.md) | `<|>`, `empty` |
| "first try this, else that" | `Alternative` | [alternative](../typeclasses/alternative.md) | left-biased `<|>` |
| "custom equality" / "define ==" | `Eq` | [eq-ord](../typeclasses/eq-ord.md) | manual instance |
| "custom ordering" / "compare" | `Ord` | [eq-ord](../typeclasses/eq-ord.md) | requires Eq superclass |
| "natural number type" / "Peano nat" | `Num` | [num](../typeclasses/num.md) | `fromInteger` is the trap |
| "Bool as Num" | `Num` | [num](../typeclasses/num.md) | XOR/AND as +/* |
| "pretty print" / "Show instance" | `Show` | [A13-pretty-printer](../archetypes/A13-pretty-printer.md) | precedence via showsPrec |
| "auto-derived" / "deriving" | derived | [README](../typeclasses/README.md) | (Eq, Ord, Show, Enum, Bounded) |
| "Foldable" / "foldr over T" | `Foldable` | [foldable](../typeclasses/foldable.md) | minimal: foldMap or foldr |
| "Traversable" / "instance Traversable T" / "make T Traversable" / "traverse" / "mapM over T" | `Traversable` | [traversable](../typeclasses/traversable.md) | Applicative-effects; template lives HERE, **not** A06 (A06 is Functor/Applicative/Monad only) |
| "Monoid" / "<>" / "mempty" | `Monoid` | [monoid](../typeclasses/monoid.md) | identity + associative |
| "Semigroup" | `Semigroup` | [monoid](../typeclasses/monoid.md) | just `<>` |
| "MyEq class" / "custom class" | (user class) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | problem 69 pattern |
| "phantom type" / "Const a b" / "type param doesn't appear in data" | `Functor` | [functor-instance-family](../question-families/functor-instance-family.md) | `fmap _ = id` on the phantom side |
| "deriving Functor" / "deriving Monad" | (FORBIDDEN) | [P-010](../pitfalls/HIGH-severity.md#p-010) | requires `-XDeriveFunctor`; banned in Safe mode — write the instance manually |
| "newtype vs data" / "when to use newtype" | (style) | [README](../typeclasses/README.md) | newtype = single-ctor single-field, zero runtime cost; data = sum type |

## INTERPRETERS / EVAL

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "evaluate expression" / "evalExpr" | [A08](../archetypes/A08-env-eval.md) | [simple-arith](../interpreters/simple-arith.md) | per-ctor case-fold |
| "evaluate to Int" | [A08](../archetypes/A08-env-eval.md) | [simple-arith](../interpreters/simple-arith.md) | pure eval |
| "evaluate to Maybe Int" | [A08](../archetypes/A08-env-eval.md) | [expr-maybe](../interpreters/expr-maybe.md) | division can fail |
| "evaluate, may throw error" | [A14](../archetypes/A14-multi-effect-interp.md) | [expr-state-either](../interpreters/expr-state-either.md) | MonadError |
| "variables / let / env" | [A08](../archetypes/A08-env-eval.md) | [A08-env-eval](../archetypes/A08-env-eval.md) | `Env -> Expr -> Maybe Value` |
| "Let binding extends env" | [A08](../archetypes/A08-env-eval.md) | [expr-reader](../interpreters/expr-reader.md) | bind value before body |
| "Var lookup may fail" | [A08](../archetypes/A08-env-eval.md) | [expr-maybe](../interpreters/expr-maybe.md) | `lookup x env` |
| "boolean and integer expressions" | [A08](../archetypes/A08-env-eval.md) / [A19](../archetypes/A19-extend-interpreter.md) | [expr-multi-effect](../interpreters/expr-multi-effect.md) | typed `Value = BVal | IVal` |
| "while / if / block / assignment :=" | [A19](../archetypes/A19-extend-interpreter.md) | [imperative-eval](../interpreters/imperative-eval.md) | `Program -> Storage -> Storage` |
| "translate Expr to Circuit" | [A05](../archetypes/A05-adt-translation.md) | [A05-adt-translation](../archetypes/A05-adt-translation.md) | Mock Q5 |
| "remove Implies" / "normalize to subset" | [A05](../archetypes/A05-adt-translation.md) | [adt-translation-family](../question-families/adt-translation-family.md) | per-ctor rewrite |
| "extend the interpreter" | [A19](../archetypes/A19-extend-interpreter.md) | [A19-extend-interpreter](../archetypes/A19-extend-interpreter.md) | AST + parser + eval |
| "calculator with division" | [A14](../archetypes/A14-multi-effect-interp.md) | [expr-state-either](../interpreters/expr-state-either.md) | MonadError on /0 |
| "Storage" / "imperative variables" | [A19](../archetypes/A19-extend-interpreter.md) | [imperative-storage](../interpreters/imperative-storage.md) | `[(Identifier, Integer)]` |
| "parse arithmetic" | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | expr/term/factor grammar |
| "label-tree / counter during eval" | [A02](../archetypes/A02-state-game.md) + [A08](../archetypes/A08-env-eval.md) | [expr-x-state](../cross-matrix/expr-x-state.md) | state inside eval |
| "trace each step of eval" | [A15](../archetypes/A15-writer-trace.md) + [A08](../archetypes/A08-env-eval.md) | [expr-x-multi](../cross-matrix/expr-x-multi.md) | Writer log |

## PARSERS

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "parse a string into…" | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | `newtype Parser a = P (String -> [(a, String)])` |
| "Parser type" / "parser combinator" | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | Functor/Applicative/Monad/Alternative |
| "BNF / grammar" | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | recursive descent |
| "expression with precedence" | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | stratified expr/term/factor |
| "parse digit" | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | `sat isDigit` |
| "parse one or more" | [A16](../archetypes/A16-parser-combinators.md) | [alternative](../typeclasses/alternative.md) | `some p` |
| "parse zero or more" | [A16](../archetypes/A16-parser-combinators.md) | [alternative](../typeclasses/alternative.md) | `many p` |
| "balanced brackets" | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | recursive `<|>` |
| "optional whitespace" | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | `token` / `space` |
| "parse arithmetic with + and *" | [A16](../archetypes/A16-parser-combinators.md) | [A16-parser-combinators](../archetypes/A16-parser-combinators.md) | problem 140 |
| "chainl1" / "left-associative operators" / "precedence parsing" | [A16](../archetypes/A16-parser-combinators.md) | [parser-chainl1](../interpreters/parser-chainl1.md) | `chainl1 p op` — accumulator builds left-assoc tree |
| "chainr1" / "right-associative operator" / "a ^ b ^ c" | [A16](../archetypes/A16-parser-combinators.md) | [parser-chainl1](../interpreters/parser-chainl1.md) | `chainr1 p op` for right-fold operators |
| "parse with custom error" / "ParseErr" / "descriptive parse failure" / "report position" | [A16](../archetypes/A16-parser-combinators.md) | [parser × either](../cross-matrix/parser-x-either.md) | `Parser a = String -> Either ParseErr (a, String)` |
| "backtrack" / "try" / "<\|> falls through" | [A16](../archetypes/A16-parser-combinators.md) | [parser-chainl1](../interpreters/parser-chainl1.md) | implicit on Maybe; explicit `try` on Parsec |

## STATE (game / counter) and WRITER

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "Nim" / "two heaps" | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | Mock Q3 — (Int,Int) state |
| "stack calculator" / "push / pop" | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | State `[Int]` |
| "fresh integer" / "gensym" | [A02](../archetypes/A02-state-game.md) | [state](../monads/state.md) | `get >>= \n -> put (n+1) >> pure n` |
| "label a tree with State Int" | [A02](../archetypes/A02-state-game.md) | [tree-x-state](../cross-matrix/tree-x-state.md) | classic |
| "rollUntil" / "count rolls until X" | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | loop with `get`/`put` |
| "Fibonacci by state" | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | `State (prev, curr)` |
| "stack of pending operations" | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | State [a] |
| "log of factorial steps" / "logFactorial" | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | problem 107 |
| "Collatz count" / "countSteps" | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | `Writer (Sum Int)` |
| "audit trail" | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | `tell [String]` |
| "running tally" | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | `Sum`/`Product`/numeric Monoid |
| "every step appended to log" | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | `tell` per step |
| "gameOver" / "game state predicate" | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | Mock Q3 — `gameOver` has hardcoded (0,0) marker test |
| "takeTokens" | [A02](../archetypes/A02-state-game.md) | [A02-state-game](../archetypes/A02-state-game.md) | Mock Q3 — must not go below 0 |
| "modify state without read" | [A02](../archetypes/A02-state-game.md) | [state](../monads/state.md) | `modify f` not `get>>=put.f` |
| "log and fail" / "audit trail with errors" / "trace until failure" | [A15](../archetypes/A15-writer-trace.md) | [writer × either](../cross-matrix/writer-x-either.md) | Shape B = `([log], Either e a)` — log survives Left |
| "StateT ExceptT" / "transformer stack order" / "state lost on failure" | [A14](../archetypes/A14-multi-effect-interp.md) | [transformer-stack-order](../monads/transformer-stack-order.md) | order matters — `StateT s (Either e)` loses state on Left |
| "ExceptT StateT" / "state survives error" | [A14](../archetypes/A14-multi-effect-interp.md) | [transformer-stack-order](../monads/transformer-stack-order.md) | `ExceptT e (State s)` preserves state on Left |

## FREE MONAD / DSL

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "Free f a" / "free monad" / "DSL of computation" | [A14](../archetypes/A14-multi-effect-interp.md) | [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md) | Free monad is a recursive ADT carrying continuations; Assignment 3 scheduler is a Free-style pattern |
| "Pure a" / "Bind / Impure" constructors | [A14](../archetypes/A14-multi-effect-interp.md) | [A14-multi-effect-interp](../archetypes/A14-multi-effect-interp.md) | `data Free f a = Pure a \| Free (f (Free f a))` — same shape as Rose × Identity |
| "interpret a DSL" / "operational view" | [A14](../archetypes/A14-multi-effect-interp.md) | [multi-effect](../monads/multi-effect.md) | Free + fold = interpreter |
| "Rose ≅ Free []" / "Free of Rose" | [A14](../archetypes/A14-multi-effect-interp.md) | [A20-laws-iso](../archetypes/A20-laws-iso.md) | rose-tree IS the free monad of `[]` |

## MATRIX / GRIDS

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "magic square" / "rows = cols = diag" | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | Mock Q4 |
| "[[Int]] -> Bool" | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | matrix predicate via transpose |
| "transpose" / "rows ↔ cols" | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | `Data.List.transpose` |
| "diagonal" / "main diagonal" | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | `[xs!!i !! i | i<-[0..n-1]]` |
| "anti-diagonal" | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | `[xs!!i !! (n-1-i)]` |
| "tic-tac-toe winner" | [A23](../archetypes/A23-mini-game.md) | [A23-mini-game](../archetypes/A23-mini-game.md) | three-in-row predicate |
| "Sudoku-like" | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | each row/col/box constraint |
| "n × n grid" | [A04](../archetypes/A04-matrix-predicate.md) / [A23](../archetypes/A23-mini-game.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | parameterise by size |
| "Conway / Life" / "step the board" | [A23](../archetypes/A23-mini-game.md) | [A23-mini-game](../archetypes/A23-mini-game.md) | neighbour count predicate |
| "rows / cols / diagonals" all-equal | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | `all (== first) [...]` |

## CODECS / STRINGS

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "Morse" / "encode/decode pair" | [A07](../archetypes/A07-codec-pair.md) | [A07-codec-pair](../archetypes/A07-codec-pair.md) | A2 assignment |
| "Caesar cipher" / "shift letters" | [A07](../archetypes/A07-codec-pair.md) | [codec-family](../question-families/codec-family.md) | preserve non-letters |
| "RLE" / "run-length encoding" | [A07](../archetypes/A07-codec-pair.md) | [codec-family](../question-families/codec-family.md) | `[(a, Int)]` form |
| "isPalindrome" | [A09](../archetypes/A09-prelude-reimpl.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | `s == reverse s` (or case-insensitive) |
| "isVowel" / "countVowels" | [A09](../archetypes/A09-prelude-reimpl.md) | [codec-family](../question-families/codec-family.md) | `Data.Char.toLower` |
| "letterFreqs" | [A21](../archetypes/A21-list-comp-synthesis.md) | [list-comp-family](../question-families/list-comp-family.md) | comprehension over alphabet |
| "encode + decode roundtrip" | [A07](../archetypes/A07-codec-pair.md) | [codec-attacks](../quickcheck/codec-attacks.md) | QC: encode . decode = id |
| "T9-style" / "phone keypad" | [A07](../archetypes/A07-codec-pair.md) | [codec-family](../question-families/codec-family.md) | table lookup |

## ADTs / DATA TYPES

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "value or absent" | `Maybe` | [maybe](../monads/maybe.md) | partial functions |
| "error-message-or-value" | `Either String a` | [either](../monads/either.md) | error-handling pattern |
| "function-as-data" | `String -> Maybe v` | [A07-codec-pair](../archetypes/A07-codec-pair.md) | env / table-as-function |
| "focus + context for navigation" | [A17](../archetypes/A17-zipper.md) | [A17-zipper](../archetypes/A17-zipper.md) | zipper newtype |
| "two equivalent representations" | [A12](../archetypes/A12-rep-conversion.md) | [A12-rep-conversion](../archetypes/A12-rep-conversion.md) | conversion pair |
| "isomorphism" / "iso" / "f.g=id and g.f=id" | [A20](../archetypes/A20-laws-iso.md) | [A20-laws-iso](../archetypes/A20-laws-iso.md) | structural recursion both sides |
| "retract" / "f.g=id only" | [A20](../archetypes/A20-laws-iso.md) | [A20-laws-iso](../archetypes/A20-laws-iso.md) | one-sided iso |
| "newtype wrapper" | [A22](../archetypes/A22-typeclass-instance.md) / [A06](../archetypes/A06-functor-instance.md) | [README](../typeclasses/README.md) | derive Eq/Show |
| "Stack a" / "push / pop / peek" | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | problem 66 |
| "Queue a" / "enqueue / dequeue" | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | problem 67 (two-list trick) |
| "Set a" / "insertS / memberS / unionS" | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | problem 68 |
| "data Shape = …" / "area" | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | problem 61 |
| "WeekDay" / "Direction" | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | enum-style |
| "Color = Custom Int Int Int" | [A13](../archetypes/A13-pretty-printer.md) | [A13-pretty-printer](../archetypes/A13-pretty-printer.md) | hex Show |
| "Vec3 = Vec3 Double Double Double" | [A22](../archetypes/A22-typeclass-instance.md) | [A22-typeclass-instance](../archetypes/A22-typeclass-instance.md) | numeric ops |

## LAZY / INFINITE / MEMO

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "infinite list" | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | corecursive definition |
| "ones / fibs / primes" | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | knot-tying `xs = e xs` |
| "sieve of Eratosthenes" | [A18](../archetypes/A18-lazy-memo.md) | [lazy-infinite-family](../question-families/lazy-infinite-family.md) | recursive filter on stream |
| "memoise Fibonacci" / "memoFib" | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | infinite tree of values |
| "doesn't loop on infinite input" | [A18](../archetypes/A18-lazy-memo.md) | [lazy-infinite-family](../question-families/lazy-infinite-family.md) | lazy Nat comparison |
| "data Nat = Zero | Succ Nat" | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | lazy comparison via Succ chain |
| "infty = Succ infty" | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | infinite Nat |
| "lengthNat doesn't loop" | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | structural laziness |
| "fix" / "fixed-point combinator" | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | `fix f = let x = f x in x` |
| "iterate" / "[x, f x, f (f x), ...]" | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | infinite list |
| "stream" / "take from infinite" | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | `take n` from corecursion |
| "memoization" / "memoise" / "cache results" | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | infinite-tree-of-values pattern |
| "stack overflow" / "non-tail-recursive" / "use accumulator" | [A09](../archetypes/A09-prelude-reimpl.md) (acc) | [P-023](../pitfalls/HIGH-severity.md#p-023) | `go acc xs` helper; `foldl' (+) 0` not `foldl`; lazy `Writer` `<>` can OOM |
| "tail recursion" / "iterative form" / "linear in stack" | [A09](../archetypes/A09-prelude-reimpl.md) | [accumulator-recursion](../haskell-basics/accumulator-recursion.md) | `foldl'` / `where go !acc x = …` |
| "thunk" / "unevaluated expression" / "force evaluation" | [A18](../archetypes/A18-lazy-memo.md) | [A18-lazy-memo](../archetypes/A18-lazy-memo.md) | `seq`, `deepseq`, `BangPatterns` |

## QUICKCHECK / MARKER / EDGES

> For Arbitrary instance code + worked prop_ examples: [quickcheck/PROPERTY-PATTERNS](../quickcheck/PROPERTY-PATTERNS.md).

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "QuickCheck property" / "law" | [A20](../archetypes/A20-laws-iso.md) | [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) | monad/functor laws |
| "marker tries empty" | (any) | [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) | universal attack U1 |
| "marker tries singleton" | (any) | [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) | universal attack U2 |
| "what does 0 do" | [A03](../archetypes/A03-generic-monad.md) / [A09](../archetypes/A09-prelude-reimpl.md) | [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) | U9 boundary at 0 |
| "round-trip" | [A07](../archetypes/A07-codec-pair.md) / [A12](../archetypes/A12-rep-conversion.md) | [codec-attacks](../quickcheck/codec-attacks.md) | `decode . encode == id` |
| "with negative" | (numeric) | [numeric-attacks](../quickcheck/numeric-attacks.md) | U8 negative |
| "deeply skewed tree" | [A01](../archetypes/A01-tree-recursion.md) | [trees-attacks](../quickcheck/trees-attacks.md) | stack overflow risk |
| "writing Arbitrary" / "prop_ for trees" / "QuickCheck generator" | (any) | [PROPERTY-PATTERNS](../quickcheck/PROPERTY-PATTERNS.md) | `sized`/`oneof`/`frequency`, shrink with `genericShrink` |
| "Data.Map" / "Map String Int" / "M.fromList" | **NOT ALLOWED** | [P-003](../pitfalls/HIGH-severity.md#p-003) | use `[(k,v)]` assoc-list + `lookup`; `Data.Map` requires `containers` which is OUTSIDE the allowed-imports list |
| "Data.Set" / "Set a" | **NOT ALLOWED** | [P-003](../pitfalls/HIGH-severity.md#p-003) | use sorted lists + `nub`, or a hand-rolled BST |
| "Control.Monad.Reader" / "Control.Monad.Except" | **NOT ALLOWED** | [P-004](../pitfalls/HIGH-severity.md#p-004) | use plain function args (Reader) and `Either` (Except); marker enforces |

## META / TYPE-SIG ONLY (no English clue)

| Signature shape | Likely archetype | File | Note |
|---|---|---|---|
| `Monad m => … -> m …` | [A03](../archetypes/A03-generic-monad.md) | [A03-generic-monad](../archetypes/A03-generic-monad.md) | generic combinator |
| `Ord a => ...` | [A11](../archetypes/A11-bst-ops.md) / [A09](../archetypes/A09-prelude-reimpl.md) | [eq-ord](../typeclasses/eq-ord.md) | sort / compare / BST |
| `T -> X` with custom T | [A01](../archetypes/A01-tree-recursion.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) | structural recursion |
| `T -> [a]` | [A01](../archetypes/A01-tree-recursion.md) | [tree-extract-family](../question-families/tree-extract-family.md) | flatten |
| `T -> Int` | [A01](../archetypes/A01-tree-recursion.md) | [tree-counting-family](../question-families/tree-counting-family.md) | size/height/count |
| `T -> Bool` | [A01](../archetypes/A01-tree-recursion.md) | [tree-validation-family](../question-families/tree-validation-family.md) | predicate |
| `T a -> T b` | [A01](../archetypes/A01-tree-recursion.md) / [A06](../archetypes/A06-functor-instance.md) | [tree-functor](../trees/tree-functor.md) | Functor or mapBT |
| `[[Int]] -> Bool` | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | matrix predicate via transpose |
| `[[a]] -> [[a]]` | [A04](../archetypes/A04-matrix-predicate.md) | [A04-matrix-predicate](../archetypes/A04-matrix-predicate.md) | transpose / rotate |
| `[a] -> [a]` | [A09](../archetypes/A09-prelude-reimpl.md) / [A10](../archetypes/A10-fold-reformulation.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | list transformation |
| `[a] -> r` (summary) | [A10](../archetypes/A10-fold-reformulation.md) | [list-fold-family](../question-families/list-fold-family.md) | fold |
| `f a -> f b` with class | [A06](../archetypes/A06-functor-instance.md) | [A06-functor-instance](../archetypes/A06-functor-instance.md) | Functor / fmap |
| `f (a -> b) -> f a -> f b` | [A24](../archetypes/A24-applicative-instance.md) | [applicative](../typeclasses/applicative.md) | `<*>` |
| `m a -> (a -> m b) -> m b` | [A06](../archetypes/A06-functor-instance.md) | [monad](../typeclasses/monad.md) | `>>=` |
| `Expr -> Circuit` / `Logic -> Logic` | [A05](../archetypes/A05-adt-translation.md) | [A05-adt-translation](../archetypes/A05-adt-translation.md) | ADT-to-ADT translation |
| `Env -> Expr -> Maybe Value` | [A08](../archetypes/A08-env-eval.md) | [A08-env-eval](../archetypes/A08-env-eval.md) | environment evaluator |
| `State s a` | [A02](../archetypes/A02-state-game.md) | [state](../monads/state.md) | get/put combinators |
| `Writer w a` | [A15](../archetypes/A15-writer-trace.md) | [writer](../monads/writer.md) | tell-based |
| `Reader r a` | (eval) | [reader](../monads/reader.md) | ask-based |
| `Either e a` | [A06](../archetypes/A06-functor-instance.md) / [A14](../archetypes/A14-multi-effect-interp.md) | [either](../monads/either.md) | error-with-message |
| `m m a -> m a` (join) | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) | flatten |
| `(a -> b) -> [a] -> [b]` | [A09](../archetypes/A09-prelude-reimpl.md) / [A10](../archetypes/A10-fold-reformulation.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | map-shape |
| `(a -> Bool) -> [a] -> [a]` | [A09](../archetypes/A09-prelude-reimpl.md) / [A10](../archetypes/A10-fold-reformulation.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | filter-shape |
| `(a -> b -> b) -> b -> [a] -> b` | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) | foldr signature |
| `Int -> a -> [a]` | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | replicate-shape |
| `[a] -> Int` | [A09](../archetypes/A09-prelude-reimpl.md) / [A10](../archetypes/A10-fold-reformulation.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | length-shape |
| `[a] -> [a] -> [a]` | [A09](../archetypes/A09-prelude-reimpl.md) | [list-rewrite-family](../question-families/list-rewrite-family.md) | merge/append/interleave |
| `Eq a => a -> [a] -> Bool` | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | elem-shape |
| `Eq a => a -> [(a,b)] -> Maybe b` | [A09](../archetypes/A09-prelude-reimpl.md) | [maybe](../monads/maybe.md) | lookup-shape |
| `Ord a => [a] -> [a]` | [A09](../archetypes/A09-prelude-reimpl.md) / [A11](../archetypes/A11-bst-ops.md) | [bst](../trees/bst.md) | sort or BST |
| `Ord a => BT a -> Bool` | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | isBST |
| `Ord a => a -> BT a -> BT a` | [A11](../archetypes/A11-bst-ops.md) | [A11-bst-ops](../archetypes/A11-bst-ops.md) | insert/delete |
| `BT a -> BT a` | [A01](../archetypes/A01-tree-recursion.md) | [tree-transform-family](../question-families/tree-transform-family.md) | mirror-shape |
| `BT a -> [a]` | [A01](../archetypes/A01-tree-recursion.md) | [tree-extract-family](../question-families/tree-extract-family.md) | flatten-shape |
| `Rose a -> Rose a` | [A01](../archetypes/A01-tree-recursion.md) | [rose-ops-family](../question-families/rose-ops-family.md) | prune-shape |
| `Rose a -> Bool` | [A01](../archetypes/A01-tree-recursion.md) | [tree-validation-family](../question-families/tree-validation-family.md) | isNBranching-shape |
| `Int -> Rose a -> Rose a` | [A01](../archetypes/A01-tree-recursion.md) | [rose-ops-family](../question-families/rose-ops-family.md) | prune n |
| `Int -> Rose a -> Bool` | [A01](../archetypes/A01-tree-recursion.md) | [tree-validation-family](../question-families/tree-validation-family.md) | isNBranching n |
| `Expr -> Int` | [A08](../archetypes/A08-env-eval.md) | [simple-arith](../interpreters/simple-arith.md) | evalExpr |
| `Expr -> Maybe Int` | [A08](../archetypes/A08-env-eval.md) | [expr-maybe](../interpreters/expr-maybe.md) | partial eval |
| `Env -> Expr -> Maybe Int` | [A08](../archetypes/A08-env-eval.md) | [A08-env-eval](../archetypes/A08-env-eval.md) | env-based eval |
| `MonadError String m => Expr -> m Int` | [A14](../archetypes/A14-multi-effect-interp.md) | [expr-state-either](../interpreters/expr-state-either.md) | calculator with errors |
| `Monad m => (a -> m b) -> [a] -> m [b]` | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) | mapM-shape |
| `Monad m => [m a] -> m [a]` | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) | sequence-shape |
| `Monad m => m a -> (a -> m a) -> Int -> m [a]` | [A03](../archetypes/A03-generic-monad.md) | [A03-generic-monad](../archetypes/A03-generic-monad.md) | applyNTimes — Mock Q2 |
| `Monad m => m (m a) -> m a` | [A03](../archetypes/A03-generic-monad.md) | [generic-combinators](../monads/generic-combinators.md) | join |
| `Applicative f => (a -> b -> c) -> f a -> f b -> f c` | [A24](../archetypes/A24-applicative-instance.md) | [applicative](../typeclasses/applicative.md) | liftA2 |
| `Show a => …` | [A13](../archetypes/A13-pretty-printer.md) | [A13-pretty-printer](../archetypes/A13-pretty-printer.md) | pretty print |
| `Num a => …` | [A22](../archetypes/A22-typeclass-instance.md) | [num](../typeclasses/num.md) | numeric overloaded |
| `String -> Int` | [A21](../archetypes/A21-list-comp-synthesis.md) / [A07](../archetypes/A07-codec-pair.md) | [codec-family](../question-families/codec-family.md) | counting / parsing |
| `String -> String` | [A07](../archetypes/A07-codec-pair.md) / [A09](../archetypes/A09-prelude-reimpl.md) | [codec-family](../question-families/codec-family.md) | cipher / transform |

## EXAM-SPECIFIC stems (Mock Test phrasing)

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "Consider the following data type" | [A01](../archetypes/A01-tree-recursion.md) / [A05](../archetypes/A05-adt-translation.md) | [A01-tree-recursion](../archetypes/A01-tree-recursion.md) | always read the ctors first |
| "such that the following property holds" | [A20](../archetypes/A20-laws-iso.md) | [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) | examiner gives you the QC property |
| "without using any library function" | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | hand-rolled recursion |
| "using only foldr" | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) | reformulation |
| "you may use the following" | (depends) | [COURSE-MAP](../meta/COURSE-MAP.md) | allowed-imports list |
| "generic over any monad m" | [A03](../archetypes/A03-generic-monad.md) | [A03-generic-monad](../archetypes/A03-generic-monad.md) | no specialising |
| "as efficient as possible" / "O(n)" | (acc) | [foldl-vs-foldr](../pitfalls/HIGH-severity.md#p-023) | accumulator / tail rec |
| "do NOT use length" / "do NOT use !!" | [A09](../archetypes/A09-prelude-reimpl.md) | [A09-prelude-reimpl](../archetypes/A09-prelude-reimpl.md) | structural recursion only |
| "complete the following definition" | (any) | [COURSE-MAP](../meta/COURSE-MAP.md) | match the partial sig given |

## GENERIC HELPER words

| Phrase | File | Note |
|---|---|---|
| "predicate p" / "(a -> Bool)" | [tree-validation-family](../question-families/tree-validation-family.md) | hidden-predicate mutation; very common |
| "Bool-blind comparison" | [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) | use `==` if `Eq` available |
| "must compile on vLab" | [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) | Safe pragma, allowed imports only |
| "the auto-marker" / "QuickCheck-tested" | [QUICKCHECK-ATTACKS](../quickcheck/QUICKCHECK-ATTACKS.md) | sig must match exactly |
| "with `do` notation" | [README](../monads/README.md) | translate from `>>=` |
| "no explicit recursion" | [A10](../archetypes/A10-fold-reformulation.md) | [A10-fold-reformulation](../archetypes/A10-fold-reformulation.md) | fold-based |
| "structural induction" | [A20](../archetypes/A20-laws-iso.md) | [A20-laws-iso](../archetypes/A20-laws-iso.md) | base + step |
| "this lemma holds" | [A20](../archetypes/A20-laws-iso.md) | [A20-laws-iso](../archetypes/A20-laws-iso.md) | proof-style |
| "from the lecture notes" | [COURSE-MAP](../meta/COURSE-MAP.md) | search by lecture slug |
| "from a previous problem" | [PROBLEM-NUMBER-INDEX](../indexes/PROBLEM-NUMBER-INDEX.md) | look up by problem # |

## ASSIGNMENT-only stems

| Phrase in question | Archetype | File | Note |
|---|---|---|---|
| "Grid with a pointer" | [A17](../archetypes/A17-zipper.md) | [A17-zipper](../archetypes/A17-zipper.md) | A1 — focus + context |
| "uncoverable grid" | (specific) | [ASSIGNMENT-INDEX](../indexes/ASSIGNMENT-INDEX.md) | A1: hardcoded sizes (OEIS A068920) |
| "tabulate / ramify" | [A12](../archetypes/A12-rep-conversion.md) / [A20](../archetypes/A20-laws-iso.md) | [A12-rep-conversion](../archetypes/A12-rep-conversion.md) | A2 — Tree ↔ Table |
| "Free f a" / "Pure / Free" | [A14](../archetypes/A14-multi-effect-interp.md) | [multi-effect](../monads/multi-effect.md) | A3 |
| "FSum" / "sum of functors" | [A14](../archetypes/A14-multi-effect-interp.md) | [multi-effect](../monads/multi-effect.md) | A3 — multi-effect |
| "Yield" / "yield-state" | [A14](../archetypes/A14-multi-effect-interp.md) | [multi-effect](../monads/multi-effect.md) | A3 — scheduler |
| "round-robin" | [A14](../archetypes/A14-multi-effect-interp.md) | [multi-effect](../monads/multi-effect.md) | A3 — scheduler over Free programs |
| "Sleep" / "sleep counter" | [A14](../archetypes/A14-multi-effect-interp.md) | [multi-effect](../monads/multi-effect.md) | A3 — sleep-aware scheduler |
| "monadicIO + catch" | (test code) | [ASSIGNMENT-INDEX](../indexes/ASSIGNMENT-INDEX.md) | A1 — marker tests that fn THROWS |

---

## See also

- [TYPE-SIGNATURE-DATABASE](../indexes/TYPE-SIGNATURE-DATABASE.md) — same lookup grouped by sig family with the 150 practice sigs.
- [KEYWORD-INDEX](../indexes/KEYWORD-INDEX.md) — alphabetical keyword → vault files.
- [PROBLEM-NUMBER-INDEX](../indexes/PROBLEM-NUMBER-INDEX.md) — look up by problem number.
- [README](../archetypes/README.md) — full archetype priority ranking + flowchart.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
