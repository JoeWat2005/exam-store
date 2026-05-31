"""Phase 4: append structurally-distinct mutations to question-families that have headroom.

Cap 12/family. Each new mutation must change one of:
- recursion shape
- effect stack
- evaluation strategy
- data layout

Existing mutations are NOT touched. New mutations appended under '## Additional mutations'
section (created if absent).
"""
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
FAMILIES = VAULT / 'question-families'

# Mutation template — one block per item
MUTATION_TEMPLATE = """### Mutation {n} — {name}

**Spec:** {spec}

**Type sig:** `{sig}`

```haskell
{code}
```

**What changes vs seed:** {changes}

**QC trap:** {trap}

"""

ADDITIONAL_HEADER = """
## Additional mutations (Phase-4 expansion)

The seed mutations above are the canonical 10. The following add a structurally distinct shape — different recursion / effect / strategy / layout — to broaden exam coverage. Each is capped to keep the family ≤12.

"""

# (filename, [mutations]) — each mutation is (name, spec, sig, code, changes, trap)
# Number is computed (starts at 11 or 12 depending on family)
ADD = {
    'tree-counting-family.md': [
        ('countByDepth (returns assoc list)',
         "Count nodes at each depth and return the result as an association list `[(depth, count)]`.",
         'countByDepth :: BT a -> [(Int, Int)]',
         'countByDepth :: BT a -> [(Int, Int)]\ncountByDepth t = aggregate (go t 0)\n  where\n    go Empty        _ = []\n    go (Fork _ l r) d = d : go l (d+1) ++ go r (d+1)\n    aggregate ds = [(d, length (filter (==d) ds)) | d <- [0 .. maximum (0:ds)]]',
         'Result shape changes from `Int` to `[(Int, Int)]` — a structural reshape, not just a different scalar combine. Two-pass: collect depths, then aggregate.',
         '`countByDepth Empty` should be `[]` not `[(0,0)]`. The `maximum (0:ds)` guard is what saves the empty case from a crash.'),
        ('countSatisfyingWithAccumulator (single-pass strict accumulator)',
         "Count nodes whose value satisfies a predicate, using an accumulator threaded through both subtrees (no foldr).",
         'countSatisfyingAcc :: (a -> Bool) -> BT a -> Int',
         'countSatisfyingAcc :: (a -> Bool) -> BT a -> Int\ncountSatisfyingAcc p = go 0\n  where\n    go !acc Empty        = acc\n    go !acc (Fork x l r) = go (go (if p x then acc+1 else acc) l) r',
         'Different evaluation strategy: strict accumulator (`!acc`) with left-fold order. Compare with the standard structural `1 + sumL + sumR` form. Avoids deep thunks on skewed trees.',
         '`go (go acc l) r` order matters — swapping to `go (go acc r) l` traverses the tree right-first. Final count is the same but trace order differs (visible if you tee a Writer through it).'),
    ],
    'state-game-family.md': [
        ('takeTokensWithLog (State + Writer fused — tuple form)',
         "Take `n` tokens from a player; log the action; mutate the game state. Returns the action description in a log alongside the new state.",
         'takeTokensWithLog :: Int -> Player -> NimGame -> (NimGame, [String])',
         'takeTokensWithLog :: Int -> Player -> NimGame -> (NimGame, [String])\ntakeTokensWithLog n First  (a, b) =\n  let a\' = max 0 (a - n)\n  in ((a\', b), ["P1 took " ++ show n ++ " from heap A, now " ++ show a\'])\ntakeTokensWithLog n Second (a, b) =\n  let b\' = max 0 (b - n)\n  in ((a, b\'), ["P2 took " ++ show n ++ " from heap B, now " ++ show b\'])',
         'Effect stack changes: adds a Writer-style log alongside the State. Tuple form because `Control.Monad.Writer` mixed with `Control.Monad.State` is awkward without transformers.',
         'Log should reflect the CLAMPED value (`a\'`), not the requested deduction (`n`). Taking 5 from a heap of 3 should log "now 0", not "took 5".'),
        ('rewindMove (undo by replaying prefix — different data layout)',
         "Given a history list of moves and a starting state, return the state after every prefix. Lets you 'rewind' to any earlier point.",
         'rewindMoves :: [(Int, Player)] -> NimGame -> [NimGame]',
         'rewindMoves :: [(Int, Player)] -> NimGame -> [NimGame]\nrewindMoves moves s0 = scanl step s0 moves\n  where\n    step s (n, p) = case p of\n      First  -> let (a, b) = s in (max 0 (a-n), b)\n      Second -> let (a, b) = s in (a, max 0 (b-n))',
         'Data layout changes: history is `[(Int, Player)]` not a single move, and the result is a *list* of states (`scanl` pattern) rather than one.',
         '`scanl` includes the initial state; if the marker expects `[s1, s2, …]` (post-move only) you need `scanl1` or `tail . scanl …`. Off-by-one is the marker bait.'),
    ],
    'monad-combinator-family.md': [
        ('applyNTimesUntil (early-exit predicate — short-circuiting)',
         "Like `applyNTimes` but stops as soon as a predicate on the result is true; returns the prefix of results up to and including the first satisfying one.",
         'applyNTimesUntil :: Monad m => m a -> (a -> m a) -> (a -> Bool) -> Int -> m [a]',
         'applyNTimesUntil :: Monad m => m a -> (a -> m a) -> (a -> Bool) -> Int -> m [a]\napplyNTimesUntil mx _  _ 0 = do x <- mx; return [x]\napplyNTimesUntil mx mf p n = do\n  x <- mx\n  if p x\n    then return [x]\n    else do xs <- applyNTimesUntil (mf x) mf p (n-1)\n            return (x:xs)',
         'Adds a stopping predicate, changing the recursion from "always n steps" to "up to n steps". The base case logic gains a branch.',
         'When the predicate is `True` at step 0, return `[x]` (singleton) not `[]`. Counting off-by-one between "I did n steps" and "I returned n results".'),
        ('mapMWithState (Monad m + accumulator state — tuple-bound)',
         "Map a Kleisli arrow over a list while threading an accumulator pure value through. Returns the final accumulator and the mapped list.",
         'mapAcc :: Monad m => (s -> a -> m (s, b)) -> s -> [a] -> m (s, [b])',
         'mapAcc :: Monad m => (s -> a -> m (s, b)) -> s -> [a] -> m (s, [b])\nmapAcc _ s []     = return (s, [])\nmapAcc f s (x:xs) = do\n  (s\',  y)  <- f s x\n  (s\'\', ys) <- mapAcc f s\' xs\n  return (s\'\', y : ys)',
         'Carries pure state through a monadic `mapM`. Recursion shape stays list-cons but the step function takes a tuple in and out — a foldM-like pattern without using `Data.List.foldM`.',
         'Threading the *new* state `s\'` into the recursive call (not the old `s`) is the classic bug. State updates are lost if you `return (s, …)` instead of `return (s\'\', …)`.'),
    ],
    'matrix-predicate-family.md': [
        ('isMagicAntiSquare (anti-diagonal sum check — different geometric layout)',
         "Same as `isMagicSquare` but the magic constraint applies to the anti-diagonal (top-right to bottom-left) instead of the main diagonal.",
         'isMagicAntiSquare :: [[Int]] -> Bool',
         'isMagicAntiSquare :: [[Int]] -> Bool\nisMagicAntiSquare m\n  | not (square m) = False\n  | otherwise =\n      let s    = sum (head m)\n          rows = all ((== s) . sum) m\n          cols = all ((== s) . sum) (transpose m)\n          antiD = sum (zipWith (!!) m [n-1, n-2 .. 0])\n      in rows && cols && antiD == s\n  where n = length m\n\nsquare :: [[a]] -> Bool\nsquare m = let n = length m in all ((== n) . length) m',
         'Same fold shape but changes the index sequence on the diagonal extraction — `[n-1, n-2 .. 0]` instead of `[0..n-1]`. Different *data layout traversal*.',
         '`[n-1, n-2 .. 0]` for `n = 0` gives `[-1, -2 .. 0]` which is empty — but you reach the empty check earlier via `square`. Without the guard, `head m` on an empty matrix crashes.'),
        ('isLatinSquare (no repeats per row + column — different predicate kind)',
         "True iff every row and every column contains each of `1..n` exactly once. A different family of constraints than magic squares (sums vs distinctness).",
         'isLatinSquare :: [[Int]] -> Bool',
         'isLatinSquare :: [[Int]] -> Bool\nisLatinSquare m\n  | not (square m) = False\n  | otherwise =\n      let n      = length m\n          target = [1..n]\n          rowsOk = all (\\row -> sort row == target) m\n          colsOk = all (\\col -> sort col == target) (transpose m)\n      in rowsOk && colsOk\n  where square m = let n = length m in all ((== n) . length) m',
         'Different predicate family: distinctness rather than sum. Forces a `sort` (or `nub` + `length`) — a new helper not used by `isMagicSquare`.',
         '`sort xs == [1..n]` is sufficient AND necessary for "exactly `1..n` once each". `nub xs == xs` is weaker (no duplicates but might be `[5,6,7]`).'),
    ],
    'adt-translation-family.md': [
        ('exprToList (flatten Expr to inorder list — A05 × A09)',
         "Translate an arithmetic Expr into the list of its leaves in left-to-right order, dropping operator structure.",
         'exprToList :: Expr -> [Int]',
         'exprToList :: Expr -> [Int]\nexprToList (Num n)     = [n]\nexprToList (Add l r)   = exprToList l ++ exprToList r\nexprToList (Mul l r)   = exprToList l ++ exprToList r',
         'Same ADT shape as `circuit` but the target is a flat structure (`[Int]`) not another ADT. Translation flattens rather than transforms structurally — a different *data layout* than canonical ADT-to-ADT.',
         '`Add l r` and `Mul l r` produce the same list — semantically lossy. The marker may use this as a "show your function preserves the leaf ORDER" property; `r ++ l` is wrong.'),
        ('treeToBalancedList (rebalance via level-order — A05 × A12)',
         "Translate a `BT a` to its level-order (BFS) list of values. Defines an equivalence class of trees up to shape.",
         'treeToLevelList :: BT a -> [a]',
         'treeToLevelList :: BT a -> [a]\ntreeToLevelList t = go [t]\n  where\n    go []                 = []\n    go (Empty       : qs) = go qs\n    go (Fork x l r  : qs) = x : go (qs ++ [l, r])',
         'Different recursion shape: queue-based BFS (`++ [l, r]`) instead of stack-based DFS. Demonstrates that ADT translation isn\'t always structural recursion — sometimes it\'s a queue/state traversal.',
         '`qs ++ [l, r]` is O(n) per cons — total O(n²) for a balanced tree. Acceptable for exam scale but worth noting; use `Data.Sequence` if asked for efficient.'),
    ],
    'tree-validation-family.md': [
        ('isPathSumK (root-to-leaf path sum equals k — DFS with path accumulator)',
         "True iff some root-to-leaf path's sum equals `k`. Tests every path; returns True if any matches.",
         'isPathSumK :: (Num a, Eq a) => a -> BT a -> Bool',
         'isPathSumK :: (Num a, Eq a) => a -> BT a -> Bool\nisPathSumK _ Empty                       = False\nisPathSumK k (Fork x Empty Empty)        = x == k\nisPathSumK k (Fork x l r)                = isPathSumK (k-x) l || isPathSumK (k-x) r',
         'Recursion threads a numeric accumulator (the *remaining* target) DOWN the tree. Most validations sum/check UP; this one decrements down. Different recursion direction.',
         'Distinguish leaves (`Fork x Empty Empty`) from internal nodes whose subtrees are both empty after pruning. The clause order matters — must put the leaf clause before the general one.'),
        ('isBalanced (height check — single-pass returning Maybe Int)',
         "True iff every node's left and right subtree heights differ by at most 1. Returns `Maybe Int` (Just height if balanced, Nothing if not) to avoid recomputing heights.",
         'isBalanced :: BT a -> Maybe Int',
         'isBalanced :: BT a -> Maybe Int\nisBalanced Empty        = Just 0\nisBalanced (Fork _ l r) = do\n  hl <- isBalanced l\n  hr <- isBalanced r\n  if abs (hl - hr) <= 1 then Just (1 + max hl hr) else Nothing',
         'Uses the Maybe monad in `do`-notation to short-circuit AND carry the computed height — avoids the naive O(n²) "compute height at every node" approach.',
         'Returning `Just 0` for `Empty` (not `Nothing`) is correct — an empty tree IS balanced. Students often write `Nothing` for empty and then everything bubbles up as imbalanced.'),
    ],
    'bst-ops-family.md': [
        ('rangeCount (count BST entries within an inclusive range)',
         "Count how many values in the BST fall in `[lo, hi]` inclusive. Use BST ordering to prune subtrees.",
         'rangeCount :: Ord a => a -> a -> BT a -> Int',
         'rangeCount :: Ord a => a -> a -> BT a -> Int\nrangeCount _  _  Empty        = 0\nrangeCount lo hi (Fork x l r)\n  | x < lo    = rangeCount lo hi r\n  | x > hi    = rangeCount lo hi l\n  | otherwise = 1 + rangeCount lo hi l + rangeCount lo hi r',
         'Uses BST invariant to skip whole subtrees (different recursion shape than naïve "visit every node"). Time O(k + log n) for k matches.',
         'When `x` is in `[lo, hi]`, you must recurse on BOTH subtrees (because both can contain in-range values). Skipping one is the bug.'),
        ('kthSmallest (in-order traversal with early exit)',
         "Return the kth-smallest value in a BST (1-indexed), or `Nothing` if `k` exceeds size.",
         'kthSmallest :: Int -> BT a -> Maybe a',
         'kthSmallest :: Int -> BT a -> Maybe a\nkthSmallest k t\n  | k < 1 || k > sz = Nothing\n  | otherwise       = Just (inorder t !! (k - 1))\n  where sz = sizeBT t\n        inorder Empty        = []\n        inorder (Fork x l r) = inorder l ++ [x] ++ inorder r\n        sizeBT Empty        = 0\n        sizeBT (Fork _ l r) = 1 + sizeBT l + sizeBT r',
         'Combines a structural in-order traversal with list indexing — a *data layout* shift from BST to `[a]`. Adds defensive guards using `sizeBT`.',
         '`k = 0` and `k > size` both return `Nothing`. `inorder t !! (k-1)` would crash with `Prelude.!!: index too large` if you removed the guard.'),
    ],
    'functor-instance-family.md': [
        ('Functor for Phantom-Param ADT',
         "Define `Functor` for a phantom-parameter ADT like `data Const a b = Const a` — `fmap` must leave the value alone and change only the phantom type.",
         'instance Functor (Const a) where\n  fmap :: (b -> c) -> Const a b -> Const a c',
         "newtype Const a b = Const a\n\ninstance Functor (Const a) where\n  fmap _ (Const x) = Const x",
         'Phantom type: the `b` doesn\'t appear in the data — `fmap` is structurally `id` on the value. Different from canonical Functor where `b` does appear.',
         "Trying to `fmap f` over the wrapped `a` is the bug — `a` is the *first* type parameter, but Functor is over the *last*.")
    ],
    'codec-family.md': [
        ('rotN (parameterised Caesar shift — round-trip with parameter)',
         "Encode/decode with a per-call shift `n`. The decode must use the same `n`.",
         'rotEncode :: Int -> String -> String\nrotDecode :: Int -> String -> String',
         "rotEncode :: Int -> String -> String\nrotEncode n = map (shift n)\n  where shift k c\n          | isUpper c = chr ((ord c - ord 'A' + k) `mod` 26 + ord 'A')\n          | isLower c = chr ((ord c - ord 'a' + k) `mod` 26 + ord 'a')\n          | otherwise = c\n\nrotDecode :: Int -> String -> String\nrotDecode n = rotEncode (-n)",
         "Codec parameterised by an extra Int — the round-trip property must include the shift parameter. Different from Morse which is parameter-free.",
         "`mod 26` is essential: `rotEncode 27 'a' = 'b'` and `rotEncode (-1) 'a' = 'z'`. Without `mod`, negative shifts produce gibberish.")
    ],
    'env-eval-family.md': [
        ('evalMaybeWithDefault (Maybe fallback default for unknown vars)',
         "Same as canonical `eval :: Env -> Expr -> Maybe Int` but unknown variables fall back to a default value rather than failing.",
         'evalWithDefault :: Int -> Env -> Expr -> Int',
         "type Env = [(String, Int)]\ndata Expr = Num Int | Var String | Add Expr Expr | Mul Expr Expr\n\nevalWithDefault :: Int -> Env -> Expr -> Int\nevalWithDefault _ _   (Num n)   = n\nevalWithDefault d env (Var x)   = case lookup x env of\n                                    Just v  -> v\n                                    Nothing -> d\nevalWithDefault d env (Add l r) = evalWithDefault d env l + evalWithDefault d env r\nevalWithDefault d env (Mul l r) = evalWithDefault d env l * evalWithDefault d env r",
         "Drops the `Maybe` wrapper: failure becomes a default. Effect stack simplifies from `Reader + Maybe` to just `Reader`. Different effect stack.",
         "`d = 0` is sometimes implicit and sometimes wrong — for `Mul`, default 0 collapses any expression containing an unknown variable to 0. Document/clarify the default's semantics.")
    ],
    'error-handling-family.md': [
        ('safeEvalEither (Either with structured error type)',
         "Evaluate an arithmetic Expr, but instead of `Maybe Int` return `Either EvalError Int` with a typed error for unknown vars, division by zero, etc.",
         'data EvalError = UnknownVar String | DivByZero deriving (Eq, Show)\nsafeEvalE :: Env -> Expr -> Either EvalError Int',
         "data EvalError = UnknownVar String | DivByZero deriving (Eq, Show)\n\nsafeEvalE :: Env -> Expr -> Either EvalError Int\nsafeEvalE _   (Num n)   = Right n\nsafeEvalE env (Var x)   = maybe (Left (UnknownVar x)) Right (lookup x env)\nsafeEvalE env (Add l r) = (+) <$> safeEvalE env l <*> safeEvalE env r\nsafeEvalE env (Div l r) = do\n  vl <- safeEvalE env l\n  vr <- safeEvalE env r\n  if vr == 0 then Left DivByZero else Right (vl `div` vr)",
         "Effect stack changes from `Maybe Int` to `Either EvalError Int`. Same overall shape but errors carry structured information — supports diagnostics.",
         "`maybe (Left …) Right (lookup …)` is the right idiom — `fromMaybe undefined` will crash on unknown vars. Distinguish `UnknownVar` (lookup failure) from `DivByZero` (semantic failure).")
    ],
    'parser-family.md': [
        ('chainl1Parser (left-associative precedence — operator chain)',
         "Parse a list of `factor (op factor)*` items and left-bracket them with the operator's combiner.",
         'chainl1 :: Parser a -> Parser (a -> a -> a) -> Parser a',
         "chainl1 :: Parser a -> Parser (a -> a -> a) -> Parser a\nchainl1 p op = do\n  x <- p\n  rest x\n  where\n    rest x = (do\n               f <- op\n               y <- p\n               rest (f x y)\n             ) <|> return x",
         "Recursive helper accumulates the result tree by left-associativity. Different recursion shape from `many` (which only collects items, not pairs items with operators).",
         "Right-associative version uses `chainr1` — swapping `chainl1` for `chainr1` flips `(a+b)+c` to `a+(b+c)`, which the marker can distinguish via property tests.")
    ],
    'pretty-print-family.md': [
        ('showsBT (showS-style accumulator for efficiency)',
         "Implement `BT a -> ShowS` (i.e. `BT a -> String -> String`) to avoid O(n²) `++` for deeply nested trees.",
         'showsBT :: Show a => BT a -> ShowS',
         "showsBT :: Show a => BT a -> ShowS\nshowsBT Empty        = showString \"Empty\"\nshowsBT (Fork x l r) = showString \"Fork \"\n                     . showsPrec 11 x . showString \" (\"\n                     . showsBT l . showString \") (\"\n                     . showsBT r . showString \")\"",
         "Different evaluation strategy: `ShowS = String -> String` composes via `(.)`, avoiding the O(n²) string-concat blowup of naïve `show`. Same output shape, faster.",
         "`showsPrec 11 x` quotes negative numbers correctly — `show (-5)` is `\"-5\"` but inside `Fork` you need `(-5)` with parens. The `11` precedence forces parens.")
    ],
    'rose-ops-family.md': [
        ('isNBranchingOrLeaf (relaxed predicate — branches can be Leaf or n-children)',
         "A relaxed isNBranching: a `Branch` must have either 0 children (degenerate) or exactly n. Helps prune Mock-style spec ambiguity.",
         'isNBranchingRelaxed :: Int -> Rose a -> Bool',
         "isNBranchingRelaxed :: Int -> Rose a -> Bool\nisNBranchingRelaxed _ (Leaf _)            = True\nisNBranchingRelaxed n (Branch xs)\n  | k == 0 || k == n = all (isNBranchingRelaxed n) xs\n  | otherwise        = False\n  where k = length xs",
         "Same recursion shape as `isNBranching` but the predicate at each node permits two arities. Different *predicate kind*.",
         "`Branch []` — does it count as 'leaf-like' or as 'failed n-branch'? The relaxed version permits it, the strict version doesn't. Read the spec carefully.")
    ],
    'state-counter-family.md': [
        ('freshN (return n fresh integers in one shot)',
         "Return a list of n fresh counter values, incrementing state by n.",
         'freshN :: Int -> State Int [Int]',
         "freshN :: Int -> State Int [Int]\nfreshN n = do\n  start <- get\n  put (start + n)\n  return [start .. start + n - 1]",
         "Vectorised over `fresh` — one State operation produces a list, no recursion. Different recursion shape (none) from the structural `replicateM n fresh`.",
         "`[start .. start + n - 1]` for `n = 0` is `[start .. start-1]` which is `[]`. The state increments by 0 (idempotent). Correct.")
    ],
    'tree-extract-family.md': [
        ('extractMin (return min + tree without min)',
         "Return the smallest value in a `BT a` together with the tree that remains after removing it. Used by `delete`.",
         'extractMin :: Ord a => BT a -> Maybe (a, BT a)',
         "extractMin :: Ord a => BT a -> Maybe (a, BT a)\nextractMin Empty             = Nothing\nextractMin (Fork x Empty r)  = Just (x, r)\nextractMin (Fork x l r)      = do\n  (m, l') <- extractMin l\n  return (m, Fork x l' r)",
         "Returns *two* values — the minimum AND the residual tree — using the Maybe monad to bubble emptiness. Different return shape from canonical `extract :: BT a -> [a]`.",
         "When you find the leftmost Fork (`l = Empty`), return `r` as the residual (not `Empty`). Forgetting that the right subtree of the leftmost node must survive is the classic bug.")
    ],
    'tree-transform-family.md': [
        ('mirrorOnlyIf (predicate-guarded structural transform)',
         "Mirror a `BT a` left-right only at nodes whose value satisfies a predicate.",
         'mirrorOnlyIf :: (a -> Bool) -> BT a -> BT a',
         "mirrorOnlyIf :: (a -> Bool) -> BT a -> BT a\nmirrorOnlyIf _ Empty        = Empty\nmirrorOnlyIf p (Fork x l r)\n  | p x       = Fork x (mirrorOnlyIf p r) (mirrorOnlyIf p l)\n  | otherwise = Fork x (mirrorOnlyIf p l) (mirrorOnlyIf p r)",
         "Predicate-guarded mirror: same recursion shape but the swap-or-not decision is local to each node. Different from `mirror` which unconditionally swaps.",
         "Note: the mirror happens at the NODE level — children are swapped BEFORE the recursive call, but the predicate is on `x`. Swapping AFTER recursion (`flipChildren (Fork x (rec l) (rec r))`) is identical here (different operation order, same result), but won't be if your recursion depends on the parent's swap state.")
    ],
    'writer-trace-family.md': [
        ('foldWithTrace (fold over a list with each step logged)',
         "Fold a binary operation over a list, logging each step's accumulator update.",
         'foldWithTrace :: Show a => (a -> a -> a) -> a -> [a] -> Writer [String] a',
         "foldWithTrace :: Show a => (a -> a -> a) -> a -> [a] -> Writer [String] a\nfoldWithTrace _ z []     = do\n  tell [\"start: \" ++ show z]\n  return z\nfoldWithTrace f z (x:xs) = do\n  tell [\"step: combining \" ++ show z ++ \" and \" ++ show x]\n  let z' = f z x\n  tell [\"  -> \" ++ show z']\n  foldWithTrace f z' xs",
         "Effect stack: pure `foldl` becomes monadic Writer-traced. Each step contributes 2 log entries — structural change to the algorithm's logging frequency.",
         "Order of `tell` calls matters: `[step-message, result-message]` is in the order shown above. Swapping gives a confusing log. Property: number of tell entries = 2 * length + 1.")
    ],
    'applicative-monad-instance-family.md': [
        ('Applicative for ZipList (pairwise <*>)',
         "Define an Applicative instance where `(<*>)` zips lists pairwise instead of producing the Cartesian product (which `[]`s default Applicative does).",
         "newtype ZipList a = ZipList [a]\ninstance Functor ZipList where ...\ninstance Applicative ZipList where ...",
         "newtype ZipList a = ZipList [a] deriving Show\n\ninstance Functor ZipList where\n  fmap f (ZipList xs) = ZipList (map f xs)\n\ninstance Applicative ZipList where\n  pure x = ZipList (repeat x)\n  ZipList fs <*> ZipList xs = ZipList (zipWith ($) fs xs)",
         "Different Applicative on the *same* underlying data — a newtype wrap to disambiguate. `pure` returns an infinite list to maintain identity laws.",
         "`pure x = ZipList [x]` is WRONG because `pure id <*> ZipList [1,2,3]` should be `ZipList [1,2,3]` but with `pure x = ZipList [x]` you'd get `ZipList [1]`. Must be `repeat x`.")
    ],
    'lazy-infinite-family.md': [
        ('takeWhileFinite (lazy infinite generator + take prefix)',
         "Lazily generate the Fibonacci sequence and return the prefix up to (but not including) the first term exceeding `n`.",
         'fibsBelow :: Int -> [Int]',
         "fibs :: [Int]\nfibs = 0 : 1 : zipWith (+) fibs (tail fibs)\n\nfibsBelow :: Int -> [Int]\nfibsBelow n = takeWhile (< n) fibs",
         "Different evaluation strategy: relies on lazy generation of an infinite list. `fibs` is defined via `zipWith` on itself — classic Haskell idiom.",
         "If `n = 0`, result is `[]` (correctly). If `n = 1`, result is `[0]`. The strict-evaluation trap: avoid `takeWhile (< n) (take 100 fibs)` — the inner `take` forces 100 values even if you only need 5.")
    ],
    'list-comp-family.md': [
        ('perfectNumbers (list-comp with proper-divisor predicate)',
         "Return perfect numbers up to `n`. A perfect number equals the sum of its proper divisors (excluding itself).",
         'perfectsUpTo :: Int -> [Int]',
         "perfectsUpTo :: Int -> [Int]\nperfectsUpTo n = [k | k <- [1..n], sum (properDivisors k) == k]\n  where\n    properDivisors k = [d | d <- [1..k-1], k `mod` d == 0]",
         "List comprehension with a nested list comp as a predicate generator. Different shape from single-source comp.",
         "`properDivisors 1 = []` and `sum [] = 0` so `perfectsUpTo n` correctly excludes 1. Off-by-one on `[1..k-1]` (inclusive of k-1) is the typical trip-up.")
    ],
}

ADDITIONAL_HEADER_PAT = re.compile(r'^## Additional mutations \(Phase-4 expansion\)', re.MULTILINE)

def existing_mutation_count(text):
    """Count '### Mutation N' headings in the body."""
    return len(re.findall(r'^### Mutation \d+', text, flags=re.MULTILINE))

def append_section(text, mutations, start_n):
    block = ADDITIONAL_HEADER
    for i, (name, spec, sig, code, changes, trap) in enumerate(mutations):
        n = start_n + i
        block += MUTATION_TEMPLATE.format(n=n, name=name, spec=spec, sig=sig, code=code, changes=changes, trap=trap)
    # Insert before the '## See also' section (if present), else append.
    pat = re.compile(r'^## See also\b', re.MULTILINE)
    m = pat.search(text)
    if m:
        return text[:m.start()] + block + text[m.start():]
    return text.rstrip() + '\n' + block

def main():
    total_added = 0
    for fname, mutations in ADD.items():
        path = FAMILIES / fname
        if not path.exists():
            print(f'MISS {fname}'); continue
        text = path.read_text(encoding='utf-8', newline='')
        if ADDITIONAL_HEADER_PAT.search(text):
            print(f'SKIP {fname}: already has Additional mutations section')
            continue
        current_count = existing_mutation_count(text)
        if current_count + len(mutations) > 12:
            # trim to cap
            allowed = 12 - current_count
            mutations = mutations[:allowed]
            if not mutations:
                print(f'SKIP {fname}: at cap ({current_count})')
                continue
        new = append_section(text, mutations, current_count + 1)
        path.write_text(new, encoding='utf-8', newline='')
        total_added += len(mutations)
        print(f'OK   {fname}: added {len(mutations)} (now {current_count + len(mutations)} total)')
    print(f'\nTotal: {total_added} mutations added across {len(ADD)} families')

if __name__ == '__main__':
    main()
