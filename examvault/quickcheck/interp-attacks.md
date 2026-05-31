<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: interpreters / eval / Env**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · **interp** · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · [numeric](./numeric-attacks.md) · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: interpreters / eval / Env

**Search keywords:** interpreter, eval, Expr, Env, Storage, Identifier, Constant, Var, Op, Add, Sub, Mul, Div, Mod, Let, If, While, run, statement, opEval, missing variable, shadowing, divide by zero, recursive Let

## What the marker generates

The interpreter pattern in the lecture notes uses:
```haskell
data OpName = Add | Sub | Mul | Div | Mod | Eq | Lt | ...
data Expr = Constant Integer | Var Identifier | Op OpName [Expr]
data Statement = Identifier := Expr | If Expr Statement | IfElse Expr Statement Statement | While Expr Statement | Seq Statement Statement | Skip

type Storage = Identifier -> Integer
```

While the mock test doesn't test eval directly, **any exam interpreter question follows this pattern**, and the marker will generate:

- Arithmetic expressions of varying depth (3-7 typical).
- Storage with finite known variables.
- Programs that include assignments, if-statements, while loops.

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | `Constant n` | `Constant 0`, `Constant (-5)`, large `n` | Standard | `eval _ (Constant n) = n` |
| 2 | `Var x` where `x` is in env | `Var "x"`, env has `x ↦ 5` | Off-by-one lookup | `eval env (Var x) = env x` (or `lookup x env`) |
| 3 | `Var x` where `x` is NOT in env | `Var "missing"`, env empty | Spec: usually `0` (initial Storage). For Maybe-based: `Nothing`. | Read spec; lookup with default |
| 4 | `Op Add [a, b]` | `Op Add [Constant 1, Constant 2]` | Pattern non-exhaustive if you only handle some Op constructors | All OpName cases |
| 5 | `Op Div [a, Constant 0]` | divide by zero | `div _ 0` crashes in Haskell. If spec doesn't say, you may need to use `error` or return Maybe. | Guard against zero divisor |
| 6 | `Op Mod [a, Constant 0]` | mod by zero | Same | Same |
| 7 | `Op Sub [Constant a, Constant b]` with `b > a` | negative result | Should be `a - b` (Integer is unbounded) | Standard subtraction |
| 8 | Empty operand list `Op Add []` | should this be allowed? | Spec usually says "exactly 2 operands". If you list-pattern-match wrong, crash. | `opEval Add [x, y] = x + y`; failing on `Op Add []` is OK if not generated |
| 9 | Single-operand list `Op Add [x]` | wrong arity | Pattern-match fails | Same |
| 10 | Three-operand list `Op Add [x, y, z]` | wrong arity | Pattern-match fails | Same |
| 11 | Deeply nested expr | `Op Add [Op Mul [...], Op Sub [...]]` | Stack overflow rare | Structural recursion is fine |
| 12 | Assignment to existing var | `"x" := Constant 5` then `"x" := Constant 10` | Shadowing — new value should replace old | `update x v env = \y -> if x == y then v else env y` |
| 13 | If with false condition | `If (Constant 0) body` | Body should not execute | `boolean 0 = False`, else `True` |
| 14 | If with true condition | `If (Constant 1) body` | Body executes | Same |
| 15 | While loop that runs forever | bug-by-spec, marker may not test | If marker tests with bounded n, fine | Time limit catches this |
| 16 | While loop that runs 0 times | condition initially false | Should leave storage unchanged | Standard while semantics |
| 17 | While loop that runs many times | bounded counter | Standard | Standard |
| 18 | Let with shadowing | `Let x = 5 in Let x = 10 in x` | If you don't restore the outer env after inner Let ends, shadowing leaks | Use let-in carefully; inner scope ends with original env |
| 19 | Recursive Let | `Let x = x + 1 in x` | Should this work? Course-dependent. Most interpreters say NO (recursive defs need `letrec`). | Read spec |

## Property templates

```haskell
import Test.QuickCheck

-- Constant evaluates to itself
prop_evalConstant :: Integer -> Bool
prop_evalConstant n = eval emptyEnv (Constant n) == n

-- Var lookup with single binding
prop_evalVar :: Integer -> Bool
prop_evalVar v = eval (update "x" v emptyEnv) (Var "x") == v

-- Addition is commutative
prop_addCommutative :: Integer -> Integer -> Bool
prop_addCommutative a b =
  eval emptyEnv (Op Add [Constant a, Constant b]) ==
  eval emptyEnv (Op Add [Constant b, Constant a])

-- Division by zero: depends on spec
prop_divZero :: Integer -> Property
prop_divZero a = a /= 0 ==>
  eval emptyEnv (Op Div [Constant a, Constant a]) == 1

-- Shadowing: inner binding takes precedence
prop_shadowInner :: Integer -> Integer -> Bool
prop_shadowInner v1 v2 =
  let env = update "x" v1 emptyEnv
      env' = update "x" v2 env
  in  eval env' (Var "x") == v2

-- Update preserves OTHER variables
prop_updatePreserves :: Integer -> Integer -> Bool
prop_updatePreserves v1 v2 =
  let env = update "x" v1 emptyEnv
      env' = update "y" v2 env
  in  eval env' (Var "x") == v1
```

## Self-test before submission checklist

- [ ] `Constant n` returns `n` for `n = 0`, `n > 0`, `n < 0`
- [ ] `Var x` returns the value bound in env (using whatever Storage type the spec defines)
- [ ] `Var x` for missing `x` returns 0 (or the spec's default)
- [ ] `Op Add [a, b]` is `a + b`
- [ ] `Op Sub [a, b]` is `a - b`
- [ ] `Op Mul [a, b]` is `a * b`
- [ ] `Op Div [a, b]` handles `b == 0` (either crashes per spec or returns special value)
- [ ] All defined `OpName` constructors have a case in `opEval`
- [ ] `If condition body` does NOT execute body if condition is 0 (false)
- [ ] `update x v env` shadows any previous binding of `x`
- [ ] Other variables in env unchanged after `update`
- [ ] No `lookup` returning `Nothing` ignored — explicitly handled
- [ ] No infinite while loops without a clear termination

## Pitfalls that specifically lose QC marks

### Pitfall: divide by zero crashes
```haskell
-- WRONG (default Haskell):
opEval Div [x, y] = x `div` y
-- For y = 0: *** Exception: divide by zero
-- The marker may catch this with deepseq and treat as failure.
-- Fix:
opEval Div [x, y] | y == 0 = error "div by zero"   -- if spec allows error
                  | otherwise = x `div` y
-- Or wrap in Maybe:
opEval Div [x, y] | y == 0 = Nothing
                  | otherwise = Just (x `div` y)
-- (Spec-dependent.)
```

### Pitfall: missing variable returns wrong value
```haskell
-- WRONG: storage is Identifier -> Integer.
-- The "empty" storage should map any ident to 0 (spec).
emptyEnv :: Storage
emptyEnv = \_ -> error "undefined"
-- For Var "missing", crashes.
-- Fix:
emptyEnv = \_ -> 0
```

### Pitfall: shadowing not restored
```haskell
-- WRONG (using a global mutable concept):
let n = oldEnv "x"      -- save old
let env' = update "x" v env
... run body with env' ...
update "x" n env'       -- restore — but this is mutation thinking!
-- In Haskell, you simply don't pass the modified env down past the Let body.
-- For Let x = e in body:
runLet x e body env = run body (update x (eval env e) env)
-- After runLet returns, the calling code still has `env`, not the updated one.
```

### Pitfall: `update` overwrites instead of layering
```haskell
-- For Storage = Identifier -> Integer:
update :: Identifier -> Integer -> Storage -> Storage
update x v env = \y -> if x == y then v else env y
-- This is correct. The CALLING code is responsible for shadowing.
```

### Pitfall: not handling all `OpName` constructors
```haskell
opEval Add [x, y] = x + y
opEval Sub [x, y] = x - y
opEval Mul [x, y] = x * y
-- forgot Div, Eq, Lt — marker generates them → exception
-- Fix: handle all of them; comment out unused ones in the test if needed
```

### Pitfall: `If` returns a value instead of being a Statement
```haskell
-- If you confuse Expr-If (returns value) with Statement-If (changes state):
-- WRONG:
run (If e p) m = if boolean (eval m e) then run p m else m   -- ← OK for statement
-- WRONG:
eval m (If e t f) = if boolean (eval m e) then eval m t else eval m f
--                                                            ↑ wrong if If is a STATEMENT in your spec
```

### Pitfall: While doesn't terminate
```haskell
-- The classic:
run (While e p) m
  | boolean (eval m e) = run (While e p) (run p m)
  | otherwise          = m
-- This is correct semantics; non-termination is up to the program.
-- BUT QC won't run forever — it has a timeout. So infinite loops just fail.
```

### Pitfall: empty operator list for non-nullary op
```haskell
-- WRONG: pattern match too narrow
opEval Add []    = 0           -- ← spurious, allows Op Add [] in source
opEval Add [x]   = x           -- ← spurious
opEval Add [x,y] = x + y       -- the correct case
-- If your AST disallows wrong arity (i.e. these are unreachable), fine.
-- But don't add cases that DON'T match the AST grammar — they might mask bugs.
```

## Connection to Mock Q5 (`circuit`)

`circuit` is a "translator" not an interpreter — it translates `Expr` to `Circuit` (NAND-only). The semantic check IS effectively an interpreter test: the marker evaluates BOTH the expression and the translated circuit under every assignment and checks they agree. See `expr-attacks.md`.

## Connection to Assignment 3 Q4 schedule

`schedule [thread1, thread2, ...]` is an interpreter for a concurrent DSL with `Sleep`/`AppendChar`. The marker evaluates `execState (schedule threads) initialState` against the reference. Edge cases:
- Empty thread list — `pure ()`?
- Single thread — should equal `runSingleThread`
- Multiple threads — order of effects matters (interleaved)

## See also

**Archetypes:** [A08 env eval](../archetypes/A08-env-eval.md) · [A14 multi-effect interp](../archetypes/A14-multi-effect-interp.md) · [A19 extend interpreter](../archetypes/A19-extend-interpreter.md)
**Cross-topic:** [expr × multi](../cross-matrix/expr-x-multi.md) · [expr × state](../cross-matrix/expr-x-state.md)
**Question families:** [env-eval](../question-families/env-eval-family.md)

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
