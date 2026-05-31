"""Phase 2: generate the 35 haskell-basics pages with full content."""
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
BASICS = VAULT / 'haskell-basics'
BASICS.mkdir(exist_ok=True)

TEMPLATE = """> [examvault](../README.md) · [haskell-basics](./README.md) · **{title}**

# {title}

## What this is
{what}

## Mental model
{mental}

## Syntax
```haskell
{syntax}
```

## Small examples
```haskell
{examples}
```

## Exam use
{exam}

## Common mistakes
{mistakes}

## See also
{seealso}
"""

# Each entry: (filename, title, what, mental, syntax, examples, exam, mistakes, seealso)
PAGES = [
    ('pattern-matching.md', 'Pattern matching',
     "Destructure data by matching against constructors, literals, or variables, picking one equation per shape.",
     "Each equation matches in order top-to-bottom. The first one that matches wins. Variables bind; wildcards (`_`) discard.",
     "f Empty        = base\nf (Fork x l r) = combine x (f l) (f r)\nf 0       = baseInt\nf (x:xs)  = ...\nf _       = fallback",
     ">>> myLength []        ==> 0\n>>> myLength [1,2,3]   ==> 3\n>>> case Just 5 of { Just x -> x; Nothing -> 0 }   ==> 5",
     "Every ADT / list / Maybe / Either question is solved by `f <Constructor> = ...` equations. Reading the constructors IS reading the algorithm.",
     "- Missing base case → infinite loop ([P-005](../pitfalls/HIGH-severity.md#p-005)).\n- Equations in wrong order — specific pattern after general one ([P-022](../pitfalls/HIGH-severity.md#p-022)).\n- Non-exhaustive coverage with `-fwarn-incomplete-patterns` on ([P-017](../pitfalls/HIGH-severity.md#p-017)).",
     "**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md)\n**Basics:** [recursion](./recursion.md) · [guards](./guards.md) · [case-expressions](./case-expressions.md)"
    ),
    ('guards.md', 'Guards',
     "Choose an equation branch by a Boolean test on the bound variables.",
     "Inside one equation, vertical bars `|` introduce predicates. The first guard whose Bool evaluates `True` runs; `otherwise` is just `True`.",
     "classify n\n  | n < 0     = \"negative\"\n  | n == 0    = \"zero\"\n  | otherwise = \"positive\"",
     ">>> classify (-3)   ==> \"negative\"\n>>> classify 0      ==> \"zero\"\n>>> classify 42     ==> \"positive\"",
     "Anytime the result depends on a numeric comparison or a Bool predicate on a non-constructor scrutinee — use guards, not nested `if`.",
     "- Forgetting `otherwise` → non-exhaustive at runtime.\n- Re-using the same variable name shadows inputs silently.",
     "**Basics:** [pattern-matching](./pattern-matching.md) · [if-expressions](./if-expressions.md) · [where-clauses](./where-clauses.md)\n**Archetypes:** [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md)"
    ),
    ('if-expressions.md', 'if expressions',
     "Branch on a Bool in expression position.",
     "Unlike imperative `if`, Haskell `if` is an *expression* — both branches must have the same type, and you can use it inline anywhere.",
     "if cond then a else b",
     ">>> if True then 1 else 0   ==> 1\n>>> map (\\x -> if even x then x else 0) [1..5]   ==> [0,2,0,4,0]\n>>> let safe x = if x == 0 then Nothing else Just (10 `div` x)",
     "Use `if` when the test is a Bool and there's exactly two branches. Otherwise reach for guards or `case`.",
     "- Mismatched branch types — `if c then \"x\" else 0` won't compile.\n- Missing `else` — Haskell `if` has no one-armed form.",
     "**Basics:** [guards](./guards.md) · [case-expressions](./case-expressions.md)\n**Pitfalls:** see signature-pitfalls.md if `if` returns a sum type"
    ),
    ('let-in.md', 'let / in',
     "Local binding inside an expression. The binding is in scope only within the `in` body.",
     "Use `let` mid-expression to name a sub-result. Bindings are mutually recursive; later bindings see earlier ones (and vice versa) lazily.",
     "let x = 1 + 2\n    y = x * x\nin x + y",
     ">>> let x = 5 in x * x   ==> 25\n>>> let f n = n + 1; g n = n * 2 in g (f 3)   ==> 8\n>>> [let r = sqrt (fromIntegral n) in (n,r) | n <- [1..3]]",
     "Use `let` inside `do`-blocks (no `in` needed) or to name a value used twice in one expression.",
     "- Forgetting `in` outside a `do`-block.\n- Recursive `let` accidentally diverges if both bindings are unproductive.",
     "**Basics:** [where-clauses](./where-clauses.md) · [local-definitions](./local-definitions.md) · [do-notation-basics](./do-notation-basics.md)"
    ),
    ('where-clauses.md', 'where clauses',
     "Local binding attached to an *equation*. Bindings are visible to all guards and the right-hand side of that equation.",
     "Think of `where` as the structured way to name helpers and intermediate values for one definition. Style-wise preferred over `let` when the binding is used in multiple guards.",
     "bmi w h\n  | b < 18.5  = \"underweight\"\n  | b < 25    = \"normal\"\n  | otherwise = \"overweight\"\n  where b = w / h^2",
     ">>> bmi 70 1.75   ==> \"normal\"\n>>> let labelTree t = go t 0 where { go (Leaf x) n = (Leaf (n,x), n+1); ... }\n>>> -- where can introduce mutually recursive helpers",
     "Pretty much every tree/list recursion uses `where go` to thread an accumulator or state without exposing it in the signature.",
     "- Indentation is significant — `where` block must indent further than its parent.\n- Shadowing an outer name silently.",
     "**Basics:** [let-in](./let-in.md) · [local-definitions](./local-definitions.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md)"
    ),
    ('case-expressions.md', 'case expressions',
     "Pattern match in expression position. Same as multiple equations, but inline.",
     "`case scrutinee of { pat1 -> e1; pat2 -> e2; ... }` is the primitive form; multi-equation functions desugar to it. Use it when you can't (or won't) introduce a new top-level function.",
     "case x of\n  Nothing -> 0\n  Just n  -> n * 2",
     ">>> case 'a' of { 'a' -> 1; _ -> 0 }   ==> 1\n>>> map (\\m -> case m of Just n -> n; Nothing -> 0) [Just 1, Nothing]   ==> [1,0]\n>>> case lookup 'x' [('a',1),('x',5)] of { Just v -> v; _ -> -1 }   ==> 5",
     "Useful inside `do`-blocks or `where`-helpers when you need to branch on a constructor without writing a separate equation.",
     "- Forgetting `otherwise`-equivalent (wildcard `_`) → non-exhaustive.\n- Trying to write guards inside `case` — use `case x of { p | g -> e; ... }`.",
     "**Basics:** [pattern-matching](./pattern-matching.md) · [guards](./guards.md)\n**Archetypes:** [A03 generic monad](../archetypes/A03-generic-monad.md)"
    ),
    ('tuples.md', 'tuples',
     "Anonymous heterogeneous product. `(a,b)`, `(a,b,c)`, etc.",
     "A tuple's type IS its shape — `(Int, String)` is a different type from `(String, Int)`. Destructure with pattern match: `(x,y) = pair`.",
     "fst (x,y) = x\nsnd (x,y) = y\nfst3 (x,_,_) = x",
     ">>> fst (1,\"hi\")            ==> 1\n>>> let (a,b) = (3,4) in a+b   ==> 7\n>>> zip [1,2,3] \"abc\"          ==> [(1,'a'),(2,'b'),(3,'c')]",
     "Game-state archetypes (Nim) carry `(remaining, players)` as a State tuple. Codec/parser results are `(parsed, leftover)`.",
     "- Treating tuples like records — large tuples are a code smell.\n- `fst` / `snd` only work on pairs, not triples.",
     "**Basics:** [pattern-matching](./pattern-matching.md) · [recursion](./recursion.md)\n**Archetypes:** [A02 state game](../archetypes/A02-state-game.md) · [A16 parser combinators](../archetypes/A16-parser-combinators.md)"
    ),
    ('local-definitions.md', 'local definitions',
     "Naming helper values/functions inside one definition. Either `let … in …` or `where …`.",
     "Local-only bindings keep helpers out of the module's exported API and let you write `where go acc xs = ...` to thread state without polluting the signature.",
     "f x = result\n  where\n    helper a b = a + b\n    result     = helper x x",
     ">>> -- where: attached to equation\n>>> -- let: introduces expression\n>>> labelTree t = go t 0 where go (Leaf x) n = (Leaf (n,x), n+1)",
     "Every tree-recursion with an accumulator (`go t acc`) and every state-threading without the State monad uses local definitions.",
     "- Shadowing imports — naming a helper `map` or `filter` confuses readers.",
     "**Basics:** [let-in](./let-in.md) · [where-clauses](./where-clauses.md) · [accumulator-recursion](./accumulator-recursion.md)"
    ),
    ('lists.md', 'lists',
     "Singly-linked, cons-cells: `[]` (empty) and `x : xs` (head cons tail).",
     "All list operations are recursion over `(:)` and `[]`. `[1,2,3]` is sugar for `1 : 2 : 3 : []`.",
     "myLength []     = 0\nmyLength (x:xs) = 1 + myLength xs\n\n-- ranges and replication\n[1..5]   = [1,2,3,4,5]\nreplicate 3 'x' = \"xxx\"",
     ">>> [1,2,3] ++ [4,5]   ==> [1,2,3,4,5]\n>>> length \"hello\"     ==> 5\n>>> map (*2) [1,2,3]   ==> [2,4,6]",
     "Every Day-1 to Day-6 problem in the practice list. Lists are the default container; reach for them before `Data.Map`.",
     "- `head []` / `tail []` crash ([P-018](../pitfalls/HIGH-severity.md#p-018)).\n- `length` is O(n) — don't put it in a loop.",
     "**Basics:** [recursion](./recursion.md) · [pattern-matching](./pattern-matching.md) · [foldr](./foldr.md) · [map](./map.md)\n**Archetypes:** [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)"
    ),
    ('strings.md', 'strings',
     "`String` is just `[Char]`. Every list function works on strings.",
     "Backtick literals (`\"abc\"`) are sugar for `['a','b','c']`. So `map`, `filter`, `length`, `reverse` all work directly.",
     "type String = [Char]\n\nshout :: String -> String\nshout = map toUpper",
     ">>> reverse \"hello\"           ==> \"olleh\"\n>>> length \"hello\"            ==> 5\n>>> filter isUpper \"HeLLo\"    ==> \"HLL\"",
     "Caesar cipher and Morse code problems are string-list rewrites. Pretty-printers also live here.",
     "- `Char` is single-quoted; `String` double-quoted.\n- `show 'a'` returns `\"'a'\"` not `\"a\"`.",
     "**Basics:** [lists](./lists.md) · [map](./map.md) · [filter](./filter.md)\n**Archetypes:** [A07 codec pair](../archetypes/A07-codec-pair.md) · [A13 pretty printer](../archetypes/A13-pretty-printer.md)"
    ),
    ('recursion.md', 'Recursion',
     "Solve a problem by reducing it to a smaller version of itself, plus a stopping rule.",
     "Two equations: (1) base case — what to return at the smallest input; (2) recursive case — what to combine with the recursive result. Discipline: write the base case first.",
     "f base     = baseAnswer\nf (x:xs)   = combine x (f xs)\n-- or for trees\nf Empty        = base\nf (Fork x l r) = combine x (f l) (f r)",
     ">>> -- sum\n>>> let s [] = 0; s (x:xs) = x + s xs in s [1..5]   ==> 15\n>>> -- factorial\n>>> let fact 0 = 1; fact n = n * fact (n-1) in fact 5   ==> 120",
     "Every Q1 / Q5 of mock-style exams is recursion over an ADT. Get the equation skeleton down first, fill the right-hand side second.",
     "- Missing base case ([P-005](../pitfalls/HIGH-severity.md#p-005)).\n- Recursive call on the wrong sub-structure ([P-014](../pitfalls/HIGH-severity.md#p-014)).\n- `n == 0` instead of `n <= 0` for numeric recursion ([P-008](../pitfalls/HIGH-severity.md#p-008)).",
     "**Basics:** [pattern-matching](./pattern-matching.md) · [accumulator-recursion](./accumulator-recursion.md) · [helper-functions](./helper-functions.md) · [foldr](./foldr.md)\n**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)"
    ),
    ('accumulator-recursion.md', 'Accumulator recursion',
     "Pass a running result as an extra argument; the helper recurses with the accumulator updated.",
     "Lets you turn a structural recursion into a tail recursion: instead of building the answer on the way back UP, build it on the way DOWN. Common idiom: a `go` helper hidden in `where`.",
     "myReverse :: [a] -> [a]\nmyReverse xs = go xs []\n  where\n    go []     acc = acc\n    go (x:xs) acc = go xs (x:acc)",
     ">>> myReverse [1,2,3]   ==> [3,2,1]\n>>> -- foldl IS the accumulator pattern\n>>> let sumAcc = foldl (+) 0\n>>> sumAcc [1..100]    ==> 5050",
     "Whenever the problem says \"efficient\", \"linear time\", \"single pass\" — use an accumulator with `go` or `foldl'`.",
     "- `foldl` (not `foldl'`) on long lists → space leak. Use `foldl' (+) 0` with `Data.List`.\n- Forgetting to reverse the accumulator at the end when order matters.",
     "**Basics:** [recursion](./recursion.md) · [helper-functions](./helper-functions.md) · [foldl](./foldl.md)\n**Archetypes:** [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md) · [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)"
    ),
    ('helper-functions.md', 'Helper functions',
     "Inner functions defined in `where` that carry extra state (accumulator, depth, environment) the top-level signature shouldn't expose.",
     "When the public signature is `f :: T -> R` but you need to thread something extra through the recursion, introduce `go` (or `aux`) in `where` with the extra parameter. The public function calls `go t initial`.",
     "labelTree :: Tree a -> Tree (Int, a)\nlabelTree t = fst (go t 0)\n  where\n    go (Leaf x)   n = (Leaf (n,x), n+1)\n    go (Branch l r) n = let (l', n')  = go l n\n                            (r', n'') = go r n'\n                        in (Branch l' r', n'')",
     ">>> -- counting with depth tracking\n>>> let depth t = go t 0 where go Empty d = d; go (Fork _ l r) d = max (go l (d+1)) (go r (d+1))\n>>> -- BFS-style with a queue\n>>> let bfs t = go [t] where go [] = []; go (Empty:q) = go q; go (Fork x l r:q) = x : go (q++[l,r])",
     "Every tree-labelling, every depth/path question, every codec round-trip uses helpers.",
     "- Naming the helper the same as the outer function — infinite loop.\n- Forgetting to thread the state through both recursive calls.",
     "**Basics:** [where-clauses](./where-clauses.md) · [accumulator-recursion](./accumulator-recursion.md) · [local-definitions](./local-definitions.md)\n**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A02 state game](../archetypes/A02-state-game.md)"
    ),
    ('list-comprehensions.md', 'List comprehensions',
     "Generator + filter + expression syntax that desugars to `concatMap`.",
     "`[ e | g, p, let b ]` — read as: for each binding from generator `g`, keep if predicate `p` holds, possibly let-bind `b`, evaluate `e`. Multiple generators iterate left-to-right (outer is leftmost).",
     "[ (x,y) | x <- [1..3], y <- [1..3], x /= y, let s = x+y ]\n-- ==> [(1,2,3),(1,3,4),(2,1,3),(2,3,5),(3,1,4),(3,2,5)]\n--     filtered out where x == y",
     ">>> [x*x | x <- [1..5], even x]            ==> [4,16]\n>>> [(x,y) | x <- [1..3], y <- [x..3]]      ==> [(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]\n>>> [c | c <- \"Hello\", c `notElem` \"l\"]      ==> \"Heo\"",
     "Quicksort, Pythagorean triples, Cartesian product, factor lists, magic-square candidate generation — all of [A21 list-comp synthesis](../archetypes/A21-list-comp-synthesis.md).",
     "- Forgetting that generators are NESTED loops, not parallel iteration.\n- Reusing a variable name inside the comprehension shadows.",
     "**Basics:** [higher-order-functions](./higher-order-functions.md) · [map](./map.md) · [filter](./filter.md)\n**Archetypes:** [A21 list comp synthesis](../archetypes/A21-list-comp-synthesis.md)"
    ),
    ('higher-order-functions.md', 'Higher-order functions',
     "Functions that take or return other functions.",
     "Haskell functions are first-class values. `map`, `filter`, `foldr` are the canonical examples — each takes a function as one of its arguments and applies it across a structure.",
     "twice :: (a -> a) -> a -> a\ntwice f x = f (f x)\n\nflip :: (a -> b -> c) -> b -> a -> c\nflip f y x = f x y",
     ">>> twice (+3) 4         ==> 10\n>>> map (+1) [1,2,3]     ==> [2,3,4]\n>>> filter odd [1..10]   ==> [1,3,5,7,9]\n>>> foldr (+) 0 [1..5]   ==> 15",
     "Every Day-5 problem. Plus archetype [A10 fold reformulation](../archetypes/A10-fold-reformulation.md) which IS \"rewrite this recursive function as a higher-order fold\".",
     "- Reading `a -> b -> c` as \"takes two args and returns c\" — actually `a -> (b -> c)` (curried).\n- Sectioning ambiguity: `(- 3)` is negative three, not subtract-three; use `subtract 3`.",
     "**Basics:** [lambdas](./lambdas.md) · [function-composition](./function-composition.md) · [currying](./currying.md) · [partial-application](./partial-application.md)\n**Archetypes:** [A10 fold reformulation](../archetypes/A10-fold-reformulation.md) · [A03 generic monad](../archetypes/A03-generic-monad.md)"
    ),
    ('lambdas.md', 'Lambdas',
     "Anonymous functions written `\\args -> body`.",
     "`\\x -> e` is a function that takes `x` and returns `e`. Use them where you need a function in expression position and naming it would add no clarity (one-shot predicates, accumulators).",
     "\\x -> x + 1\n\\x y -> x + y      -- shorthand for \\x -> \\y -> x + y",
     ">>> map (\\x -> x*x) [1,2,3]                    ==> [1,4,9]\n>>> foldr (\\x acc -> (show x):acc) [] [1,2,3]  ==> [\"1\",\"2\",\"3\"]\n>>> filter (\\x -> x > 0 && x < 10) [-5..15]    ==> [1,2,3,4,5,6,7,8,9]",
     "Whenever `map`, `filter`, `foldr` need a tiny inline function. Also for fold accumulator step functions.",
     "- Operator backslash conflict — must escape if writing in some contexts (none in straight code).\n- Over-using lambdas when a section (`(+1)`) would be clearer.",
     "**Basics:** [higher-order-functions](./higher-order-functions.md) · [sections](./sections.md) · [function-composition](./function-composition.md)"
    ),
    ('function-composition.md', 'Function composition',
     "`(f . g) x = f (g x)` — apply `g` then `f`. Pronounce \"after\".",
     "Composition lets you build pipelines without naming intermediates. Reads right-to-left, which is the opposite of pipe operators in other languages.",
     "(.) :: (b -> c) -> (a -> b) -> (a -> c)\n(f . g) x = f (g x)",
     ">>> let shout = map toUpper . reverse\n>>> shout \"hello\"                ==> \"OLLEH\"\n>>> map (negate . (*2)) [1,2,3]  ==> [-2,-4,-6]\n>>> -- point-free style\n>>> let sumSquares = sum . map (^2)",
     "Reformulating verbose lambdas into `f . g . h` is a common A10 fold-reformulation step. Also the parser-combinator style.",
     "- Confusing `.` with `$` — `.` chains functions, `$` applies.\n- Over-eager point-free can make code unreadable.",
     "**Basics:** [dollar-operator](./dollar-operator.md) · [dot-operator](./dot-operator.md) · [higher-order-functions](./higher-order-functions.md)\n**Archetypes:** [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)"
    ),
    ('currying.md', 'Currying',
     "Multi-argument functions are actually nested single-argument functions: `f :: a -> b -> c` is `f :: a -> (b -> c)`.",
     "`add 1 2` is `(add 1) 2`. Currying enables partial application: `add 1` is a function waiting for the second argument.",
     "add :: Int -> Int -> Int\nadd x y = x + y\n\n-- same as:\nadd' :: Int -> (Int -> Int)\nadd' x = \\y -> x + y",
     ">>> let inc = (+) 1\n>>> inc 5             ==> 6\n>>> map (+10) [1,2,3] ==> [11,12,13]\n>>> -- flip swaps argument order\n>>> let subFromTen = flip (-) 10\n>>> subFromTen 25     ==> 15",
     "Used implicitly all the time: every `map (f x)` partially-applies `f`. Explicit `flip`/`curry`/`uncurry` shows up in HOF reformulations.",
     "- `curry`/`uncurry` confusion: `curry :: ((a,b) -> c) -> (a -> b -> c)`, `uncurry` the inverse.\n- Operator sections look like partial applications and they are.",
     "**Basics:** [partial-application](./partial-application.md) · [higher-order-functions](./higher-order-functions.md) · [sections](./sections.md)"
    ),
    ('partial-application.md', 'Partial application',
     "Supply some of a function's arguments to get back a function expecting the rest.",
     "Because every function is curried, omitting trailing arguments returns a new function. `map (+1)` is partial-applying `+`.",
     "addThree :: Int -> Int -> Int -> Int\naddThree x y z = x + y + z\n\nbumpBy7 = addThree 3 4         -- :: Int -> Int",
     ">>> bumpBy7 10        ==> 17\n>>> map (replicate 3) \"abc\"   ==> [\"aaa\",\"bbb\",\"ccc\"]\n>>> filter (`elem` [1,2,3]) [0..5]   ==> [1,2,3]",
     "Most folds and maps use partial application to make the step function concise (`foldr (+) 0` not `foldr (\\x acc -> x+acc) 0`).",
     "- Negative-number sections (`(- 3)`) — use `subtract 3`.\n- Over-partial-applying makes types confusing for readers.",
     "**Basics:** [currying](./currying.md) · [sections](./sections.md) · [higher-order-functions](./higher-order-functions.md)"
    ),
    ('dollar-operator.md', 'The $ operator',
     "`$ :: (a -> b) -> a -> b`, `f $ x = f x`. Right-associative, lowest precedence.",
     "Saves parentheses around the function's final argument. `f $ g x` instead of `f (g x)`. Useful when the argument expression is long.",
     "($) :: (a -> b) -> a -> b\nf $ x = f x",
     ">>> putStrLn $ \"answer is \" ++ show 42\n>>> map (*2) $ filter even [1..10]   ==> [4,8,12,16,20]\n>>> show $ 1 + 2 + 3                ==> \"6\"",
     "Anywhere you'd write `f (long expression)`. Helps readability in pipelines.",
     "- Overuse — `f $ g $ h $ x` is equivalent to `f . g . h $ x` and the latter is clearer.\n- Precedence surprises: `a $ b + c` is `a (b + c)`, not `(a b) + c`.",
     "**Basics:** [dot-operator](./dot-operator.md) · [function-composition](./function-composition.md)"
    ),
    ('dot-operator.md', 'The . operator (composition)',
     "`(.) :: (b -> c) -> (a -> b) -> (a -> c)`, `(f . g) x = f (g x)`.",
     "Function composition. Builds a pipeline of functions without naming intermediates. Reads right-to-left.",
     "(.) :: (b -> c) -> (a -> b) -> (a -> c)\n(f . g) x = f (g x)",
     ">>> (negate . abs) (-5)            ==> -5\n>>> let shout = map toUpper . reverse\n>>> shout \"hi\"                     ==> \"IH\"",
     "Point-free style and pipelines. `length . filter even` counts evens without binding the intermediate list.",
     "- Confusing with method `.` from OO languages — Haskell `.` is function composition, not member access.\n- Mistakenly using on values: `(+1) . 2` is a type error.",
     "**Basics:** [function-composition](./function-composition.md) · [dollar-operator](./dollar-operator.md)"
    ),
    ('sections.md', 'Sections',
     "Partially-applied operators: `(+1)`, `(2*)`, `` (`elem` xs) ``.",
     "`(op x)` means \"apply `op` with right argument fixed\"; `(x op)` means \"apply `op` with left argument fixed\". Both forms work for any infix operator.",
     "(+1)            -- \\x -> x + 1\n(2*)            -- \\x -> 2 * x\n(`elem` xs)     -- \\x -> x `elem` xs",
     ">>> map (+1) [1,2,3]            ==> [2,3,4]\n>>> filter (>0) [-2,-1,0,1,2]   ==> [1,2]\n>>> map (`replicate` 'x') [1..3]  ==> [\"x\",\"xx\",\"xxx\"]",
     "Universal in `map`/`filter`/`foldr` calls. Compact predicate definitions.",
     "- `(- 3)` is negative three, not subtract-three; use `subtract 3`.\n- Forgetting backticks around prefix names used infix.",
     "**Basics:** [partial-application](./partial-application.md) · [lambdas](./lambdas.md) · [higher-order-functions](./higher-order-functions.md)"
    ),
    ('type-signatures.md', 'Type signatures',
     "`name :: Type` — declare what type a function or value has.",
     "Read `a -> b -> c` as \"takes `a` and `b`, returns `c`\" (because of currying). Lowercase letters are type variables; uppercase names are concrete types or constructors.",
     "double :: Int -> Int\ndouble x = x * 2\n\n-- multi-arg\nadd :: Int -> Int -> Int\nadd x y = x + y",
     ">>> -- ::Lookup in GHCi\n>>> :t map\nmap :: (a -> b) -> [a] -> [b]\n>>> :t (.)\n(.) :: (b -> c) -> (a -> b) -> a -> c",
     "EVERY exam answer starts by writing the type signature verbatim from the template ([P-001](../pitfalls/HIGH-severity.md#p-001) — sig drift = zero marks).",
     "- Adding constraints (`Ord a =>`) the template didn't ask for.\n- Renaming type variables changes nothing semantically but looks suspicious in marker diffs.",
     "**Basics:** [polymorphism](./polymorphism.md) · [currying](./currying.md)\n**Pitfalls:** [P-001 sig changed](../pitfalls/HIGH-severity.md#p-001)"
    ),
    ('polymorphism.md', 'Polymorphism',
     "Functions that work for any type, with optional class constraints.",
     "Lowercase `a`, `b`, `c` in type signatures are universally quantified — the function works for ANY concrete type. Constraints (`Eq a =>`, `Ord a =>`, `Monad m =>`) restrict that universe.",
     "id :: a -> a\nid x = x\n\nlookup :: Eq k => k -> [(k,v)] -> Maybe v",
     ">>> id 5      ==> 5\n>>> id \"hi\"   ==> \"hi\"\n>>> -- m is constrained by Monad\n>>> -- mapM :: Monad m => (a -> m b) -> [a] -> m [b]",
     "Archetype [A03 generic monad](../archetypes/A03-generic-monad.md) — functions with `Monad m =>` are the most common Q2 shape.",
     "- Stuffing constraints when the function doesn't need them.\n- Forgetting constraints when comparing values requires `Eq` or `Ord`.",
     "**Basics:** [type-signatures](./type-signatures.md)\n**Typeclasses:** [Eq/Ord](../typeclasses/eq-ord.md) · [Monad](../typeclasses/monad.md)"
    ),
    ('algebraic-data-types.md', 'Algebraic data types',
     "`data X = A | B Int | C Y String` — sum of products. Each constructor is independent; can carry zero or more typed fields.",
     "A new type with explicit constructors. Pattern-match on the constructor to handle each case. The `data` keyword introduces a *new* type, distinct from its representation.",
     "data Color = Red | Green | Blue\ndata Shape = Circle Double | Rectangle Double Double\n\narea :: Shape -> Double\narea (Circle r)        = pi * r^2\narea (Rectangle w h)   = w * h",
     ">>> area (Circle 2.0)        ==> 12.566...\n>>> area (Rectangle 3.0 4.0)  ==> 12.0\n>>> -- can derive Show, Eq automatically\n>>> -- data X = ... deriving (Show, Eq)",
     "Half of every exam — Mock Q1 (Rose tree), Q4 (Expression tree), Q5 (Circuit). The first move is always reading the constructors.",
     "- Forgetting one constructor → non-exhaustive pattern warning + crash.\n- Constructor and type with the same name (allowed; sometimes confuses).",
     "**Basics:** [recursive-data-types](./recursive-data-types.md) · [deriving](./deriving.md) · [pattern-matching](./pattern-matching.md)\n**Archetypes:** [A05 ADT translation](../archetypes/A05-adt-translation.md)"
    ),
    ('recursive-data-types.md', 'Recursive data types',
     "An ADT that mentions itself in one or more constructor fields.",
     "Lists, trees, expression ASTs — all recursive ADTs. The recursion in the data definition mirrors the recursion in functions that consume it: one equation per constructor.",
     "data List a = Nil | Cons a (List a)\ndata BT a   = Empty | Fork a (BT a) (BT a)\ndata Rose a = Leaf a | Branch [Rose a]",
     ">>> let t = Fork 1 (Fork 2 Empty Empty) (Fork 3 Empty Empty)\n>>> -- size t = 3\n>>> -- map mentions itself: foldr (\\x rec -> ... rec ...) base xs",
     "Every Q1 / Q5 of mock-style exams. Reading the data definition tells you the structure of your function.",
     "- Missing base-case constructor → infinite type (won't typecheck).\n- Recursive call on the WRONG sub-tree.",
     "**Basics:** [algebraic-data-types](./algebraic-data-types.md) · [recursion](./recursion.md) · [pattern-matching](./pattern-matching.md)\n**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A05 ADT translation](../archetypes/A05-adt-translation.md)"
    ),
    ('deriving.md', 'Deriving',
     "Auto-generate type-class instances: `data X = ... deriving (Eq, Ord, Show, Read)`.",
     "GHC writes the boilerplate for you. Standard derivable classes: `Eq`, `Ord`, `Show`, `Read`, `Enum`, `Bounded` (some only for specific shapes).",
     "data Color = Red | Green | Blue deriving (Eq, Ord, Show, Read)",
     ">>> Red == Red             ==> True\n>>> compare Red Blue       ==> LT\n>>> show Green             ==> \"Green\"\n>>> read \"Red\" :: Color    ==> Red",
     "Useful for QuickCheck (`Eq` so the marker can compare; `Show` so it can print counterexamples). The exam forbids `deriving Functor` etc. — see [P-010](../pitfalls/HIGH-severity.md#p-010).",
     "- `deriving Functor` needs `-XDeriveFunctor`, which the assignments forbid.\n- Derived `Show` formats as code, not user-friendly — write your own if needed.",
     "**Basics:** [algebraic-data-types](./algebraic-data-types.md)\n**Typeclasses:** [Eq/Ord](../typeclasses/eq-ord.md) · [Show](../typeclasses/show.md)\n**Pitfalls:** [P-010 deriving Functor](../pitfalls/HIGH-severity.md#p-010)"
    ),
    ('maybe-basics.md', 'Maybe basics',
     "`data Maybe a = Nothing | Just a` — a value of type `a` that might be absent.",
     "Represents \"computation that can fail without an error message\". Pattern-match: `Just x` extracts; `Nothing` is the failure case. Full reference: [`../monads/maybe.md`](../monads/maybe.md).",
     "data Maybe a = Nothing | Just a\n\nsafeDiv :: Int -> Int -> Maybe Int\nsafeDiv _ 0 = Nothing\nsafeDiv x y = Just (x `div` y)",
     ">>> safeDiv 10 2            ==> Just 5\n>>> safeDiv 10 0            ==> Nothing\n>>> fromMaybe 0 (Just 5)    ==> 5\n>>> fromMaybe 0 Nothing     ==> 0",
     "Lookup functions (`lookup`, `find`), safe arithmetic, and parser results all return `Maybe`. Monadic chain via `do`-notation is in [`../monads/maybe.md`](../monads/maybe.md).",
     "- `fromJust` crashes on `Nothing` — never use without a guard.\n- Forgetting that `Just []` is a non-empty `Maybe` containing an empty list.",
     "**Basics:** [either-basics](./either-basics.md) · [pattern-matching](./pattern-matching.md) · [do-notation-basics](./do-notation-basics.md)\n**Theory:** [Maybe monad](../monads/maybe.md)\n**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md)"
    ),
    ('either-basics.md', 'Either basics',
     "`data Either e a = Left e | Right a` — success (`Right`) or failure with a message (`Left`).",
     "Like `Maybe` but the failure carries information. Convention: `Right` is the success value, `Left` carries the error. Full reference: [`../monads/either.md`](../monads/either.md).",
     "data Either e a = Left e | Right a\n\nsafeDivE :: Int -> Int -> Either String Int\nsafeDivE _ 0 = Left \"div by zero\"\nsafeDivE x y = Right (x `div` y)",
     ">>> safeDivE 10 2     ==> Right 5\n>>> safeDivE 10 0     ==> Left \"div by zero\"\n>>> case safeDivE 10 0 of { Right n -> n; Left _ -> -1 }   ==> -1",
     "Custom error types in interpreters (`Either EvalErr Value`). Used in Mock-style Q5 if the marker wants descriptive failure messages.",
     "- Bias: `fmap` and Monad instances only touch the `Right` side. `Left e` is short-circuit.\n- `Left` carries error, but the type variable `e` is on the LEFT in `Either e a` — easy to swap.",
     "**Basics:** [maybe-basics](./maybe-basics.md) · [algebraic-data-types](./algebraic-data-types.md)\n**Theory:** [Either monad](../monads/either.md) · [MonadError](../monads/monaderror.md)"
    ),
    ('do-notation-basics.md', 'do notation basics',
     "Syntactic sugar for monadic bind: `do x <- m; rest` desugars to `m >>= \\x -> rest`.",
     "Sequences monadic effects (Maybe, Either, State, IO, List). The `x <- m` extracts the value; `return x` (or `pure x`) wraps a pure value back in.",
     "do x <- Just 3\n   y <- Just 4\n   return (x + y)\n-- ==> Just 7\n\ndo x <- Nothing  -- short-circuits\n   y <- Just 4\n   return (x + y)\n-- ==> Nothing",
     ">>> do { x <- [1,2]; y <- [3,4]; return (x,y) }   ==> [(1,3),(1,4),(2,3),(2,4)]\n>>> -- IO\n>>> do { name <- getLine; putStrLn (\"hi \" ++ name) }",
     "Every interpreter, every State-monad game, every parser, every multi-effect computation uses `do`-notation.",
     "- Using `let x = ...` (no `<-`) for non-monadic binds inside `do`.\n- Forgetting `return` at the end when the do-block must produce `m a`.\n- Pattern bind `(Just x) <- m` relies on `MonadFail` — type-changes break it silently.",
     "**Basics:** [maybe-basics](./maybe-basics.md) · [either-basics](./either-basics.md)\n**Theory:** [Monad typeclass](../typeclasses/monad.md) · [State monad](../monads/state.md)\n**Archetypes:** [A03 generic monad](../archetypes/A03-generic-monad.md) · [A08 env eval](../archetypes/A08-env-eval.md)"
    ),
    ('map.md', 'map',
     "`map :: (a -> b) -> [a] -> [b]` — apply a function to every element of a list.",
     "Builds a new list by transforming each element. Pure — input list unchanged. Generalises to `fmap` for any Functor.",
     "map :: (a -> b) -> [a] -> [b]\nmap _ []     = []\nmap f (x:xs) = f x : map f xs",
     ">>> map (+1) [1,2,3]                  ==> [2,3,4]\n>>> map show [1,2,3]                 ==> [\"1\",\"2\",\"3\"]\n>>> map (\\(a,b) -> a*b) [(1,2),(3,4)]   ==> [2,12]",
     "First thing to reach for when \"do X to every element\". Reimplementing `map` is a typical [A09](../archetypes/A09-prelude-reimpl.md) question.",
     "- `map` with side effects → use `mapM` or `traverse`.\n- Confusing `map f xs` with `fmap f xs` — for lists they're identical, but `fmap` works on Trees, Maybes, etc.",
     "**Basics:** [higher-order-functions](./higher-order-functions.md) · [filter](./filter.md) · [foldr](./foldr.md)\n**Typeclasses:** [Functor](../typeclasses/functor.md)\n**Archetypes:** [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md)"
    ),
    ('filter.md', 'filter',
     "`filter :: (a -> Bool) -> [a] -> [a]` — keep elements where the predicate returns `True`.",
     "Drops elements that fail the test. Preserves the order of survivors. Often combined with `map` in a pipeline.",
     "filter :: (a -> Bool) -> [a] -> [a]\nfilter _ []     = []\nfilter p (x:xs)\n  | p x       = x : filter p xs\n  | otherwise = filter p xs",
     ">>> filter even [1..10]               ==> [2,4,6,8,10]\n>>> filter (>3) [1,4,2,5,1]          ==> [4,5]\n>>> filter (\\(_,v) -> v > 0) [(\"a\",1),(\"b\",-1)]   ==> [(\"a\",1)]",
     "Common in list-comprehension answers (the guard part). Also in fold-reformulation when the seed wraps `filter` around `map`.",
     "- `filter` then `length` — use `foldr` to count without building the intermediate list.\n- Negating the predicate by mistake.",
     "**Basics:** [higher-order-functions](./higher-order-functions.md) · [map](./map.md) · [foldr](./foldr.md)\n**Archetypes:** [A09 prelude reimpl](../archetypes/A09-prelude-reimpl.md) · [A21 list comp synthesis](../archetypes/A21-list-comp-synthesis.md)"
    ),
    ('foldr.md', 'foldr',
     "`foldr :: (a -> b -> b) -> b -> [a] -> b` — combine list elements right-to-left with a seed.",
     "Replace every `(:)` with your function and every `[]` with the seed. `foldr f z [a,b,c]` = `f a (f b (f c z))`. Right-associative — natural for list-building combinators.",
     "foldr :: (a -> b -> b) -> b -> [a] -> b\nfoldr _ z []     = z\nfoldr f z (x:xs) = f x (foldr f z xs)",
     ">>> foldr (+) 0 [1,2,3]               ==> 6\n>>> foldr (:) [] [1,2,3]              ==> [1,2,3]   -- identity\n>>> foldr (\\x acc -> if even x then x:acc else acc) [] [1..6]   ==> [2,4,6]",
     "Archetype [A10 fold reformulation](../archetypes/A10-fold-reformulation.md) — rewrite explicit recursion as a `foldr`. Used everywhere lists are reduced to a single value or a new list.",
     "- Use `foldr` when the step builds a (potentially infinite) list lazily; use `foldl'` for strict numeric reductions.\n- Argument order: step function takes `element` then `accumulator`.",
     "**Basics:** [foldl](./foldl.md) · [higher-order-functions](./higher-order-functions.md) · [recursion](./recursion.md)\n**Typeclasses:** [Foldable](../typeclasses/foldable.md)\n**Archetypes:** [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)"
    ),
    ('foldl.md', 'foldl',
     "`foldl :: (b -> a -> b) -> b -> [a] -> b` — combine list elements left-to-right with a seed.",
     "Left-associative: `foldl f z [a,b,c]` = `f (f (f z a) b) c`. For strict numeric accumulators, prefer `foldl'` from `Data.List` to avoid space leaks.",
     "foldl :: (b -> a -> b) -> b -> [a] -> b\nfoldl _ z []     = z\nfoldl f z (x:xs) = foldl f (f z x) xs\n\n-- Prefer foldl' for numeric accumulation:\n-- import Data.List (foldl')",
     ">>> foldl (+) 0 [1,2,3]               ==> 6\n>>> foldl (\\acc x -> x:acc) [] [1,2,3]    ==> [3,2,1]   -- reverses!\n>>> foldl' (*) 1 [1..5]               ==> 120",
     "Use when the seed needs to be the FIRST argument of the step function (e.g. building an accumulator with prepend). For sums/products on long lists use `foldl'`.",
     "- Lazy `foldl` on long numeric lists → stack overflow. Use `foldl'`.\n- Argument order: step takes `accumulator` then `element` (opposite of `foldr`).",
     "**Basics:** [foldr](./foldr.md) · [accumulator-recursion](./accumulator-recursion.md)\n**Archetypes:** [A10 fold reformulation](../archetypes/A10-fold-reformulation.md)"
    ),
    ('zip.md', 'zip',
     "`zip :: [a] -> [b] -> [(a,b)]` — pair up two lists positionally; stop at the shorter.",
     "Produces tuples. Common partner for `zipWith` and list comprehensions over two sources. Stops at the shorter list, no error.",
     "zip :: [a] -> [b] -> [(a,b)]\nzip []     _      = []\nzip _      []     = []\nzip (x:xs) (y:ys) = (x,y) : zip xs ys",
     ">>> zip [1,2,3] \"abc\"        ==> [(1,'a'),(2,'b'),(3,'c')]\n>>> zip [1..] [\"a\",\"b\",\"c\"]   ==> [(1,\"a\"),(2,\"b\"),(3,\"c\")]\n>>> zip3 [1,2] \"ab\" [True,False]   ==> [(1,'a',True),(2,'b',False)]",
     "Adding indices (`zip [0..] xs`), pairing parallel data (e.g. row positions in a matrix).",
     "- Silent truncation if lists have different lengths.\n- `unzip` is the inverse.",
     "**Basics:** [zipWith](./zipWith.md) · [tuples](./tuples.md)"
    ),
    ('zipWith.md', 'zipWith',
     "`zipWith :: (a -> b -> c) -> [a] -> [b] -> [c]` — `zip` + `map` in one go.",
     "Combines two lists element-wise with a binary function. Equivalent to `map (uncurry f) . zip xs`, but stops at the shorter list and avoids building the intermediate tuple list.",
     "zipWith :: (a -> b -> c) -> [a] -> [b] -> [c]\nzipWith _ []     _      = []\nzipWith _ _      []     = []\nzipWith f (x:xs) (y:ys) = f x y : zipWith f xs ys",
     ">>> zipWith (+) [1,2,3] [10,20,30]      ==> [11,22,33]\n>>> zipWith (*) [1..] [1..5]            ==> [1,4,9,16,25]\n>>> -- pair index with value\n>>> zipWith (,) [0..] \"abc\"              ==> [(0,'a'),(1,'b'),(2,'c')]",
     "Matrix dot-product step, parallel transformations, position-aware processing. Common in matrix archetype.",
     "- Truncates silently at the shorter list.\n- For three lists use `zipWith3`.",
     "**Basics:** [zip](./zip.md) · [map](./map.md) · [higher-order-functions](./higher-order-functions.md)\n**Archetypes:** [A04 matrix predicate](../archetypes/A04-matrix-predicate.md)"
    ),
    ('all-any.md', 'all / any',
     "`all :: (a -> Bool) -> [a] -> Bool` — every element satisfies. `any :: (a -> Bool) -> [a] -> Bool` — at least one does.",
     "Both short-circuit. `all p []` is `True` (vacuous); `any p []` is `False`. Built on `foldr (&&)` and `foldr (||)`.",
     "all :: (a -> Bool) -> [a] -> Bool\nall p = foldr (\\x acc -> p x && acc) True\n\nany :: (a -> Bool) -> [a] -> Bool\nany p = foldr (\\x acc -> p x || acc) False",
     ">>> all even [2,4,6]      ==> True\n>>> all even [2,3,4]      ==> False\n>>> any (> 10) [1,5,11]   ==> True\n>>> all (== 0) []         ==> True   -- vacuous truth",
     "Magic-square row/column checks, BST validation, predicate verification. The `all p children` pattern in `isNBranching`-style recursion.",
     "- `all p []` returns `True` — often the right semantics (every child of a `Leaf` satisfies `p`).\n- Using `all`/`any` where a fold with a guard would suffice (style).",
     "**Basics:** [foldr](./foldr.md) · [higher-order-functions](./higher-order-functions.md)\n**Archetypes:** [A01 tree recursion](../archetypes/A01-tree-recursion.md) · [A04 matrix predicate](../archetypes/A04-matrix-predicate.md)"
    ),
]

def main():
    n = 0
    for fname, title, what, mental, syntax, examples, exam, mistakes, seealso in PAGES:
        out = TEMPLATE.format(title=title, what=what, mental=mental, syntax=syntax, examples=examples, exam=exam, mistakes=mistakes, seealso=seealso)
        (BASICS / fname).write_text(out, encoding='utf-8', newline='')
        n += 1
        print(f'OK {fname}')
    print(f'\nTotal: {n} basics pages written')

if __name__ == '__main__':
    main()
