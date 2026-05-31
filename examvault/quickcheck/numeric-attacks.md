<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · [quickcheck](./README.md) · **QuickCheck attacks: numeric (Int, Integer, Double, divide-by-zero)**

<!-- siblings:start -->
> **Peers:** [PROPERTY-PATTERNS](./PROPERTY-PATTERNS.md) · [QUICKCHECK-ATTACKS](./QUICKCHECK-ATTACKS.md) · [bst](./bst-attacks.md) · [codec](./codec-attacks.md) · [expr](./expr-attacks.md) · [interp](./interp-attacks.md) · [lists](./lists-attacks.md) · [matrix](./matrix-attacks.md) · [maybe-either](./maybe-either-attacks.md) · [monad](./monad-attacks.md) · **numeric** · [rose](./rose-attacks.md) · [state](./state-attacks.md) · [trees](./trees-attacks.md) · [typeclass-instance](./typeclass-instance-attacks.md) · [writer](./writer-attacks.md)
<!-- siblings:end -->






# QuickCheck attacks: numeric (Int, Integer, Double, divide-by-zero)

**Search keywords:** divide by zero, div, mod, negative, overflow, Int vs Integer, Double, NaN, Infinity, sqrt, factorial, power, gcd, lcm, Bounded, maxBound

## What the marker generates

The default `Arbitrary Int` and `Arbitrary Integer` produce:
- Frequently `0`
- Often small positives `1..100`
- Often small negatives `-100..-1`
- Occasional larger values
- Both `Int` and `Integer` are tested

`NonNegative n` wrapper from QuickCheck guarantees `n >= 0`. The marker uses this sometimes:
```haskell
nonnegative :: Gen (NonNegative Integer)
nonnegativeInt = getNonNegative <$> nonnegative
smallInt = chooseInt (0, 100)
```

For `Double`, QC generates `NaN` and `Infinity` occasionally — usually marker uses `Integer` to avoid this.

## Attack surface

| # | Input class | Example | What fails if you forget it | How to fix |
|---|-------------|---------|------------------------------|------------|
| 1 | `0` | divisor in `div`, exponent base | `div _ 0` crashes; `0^0` is undefined (Haskell returns 1, mathematicians disagree) | Guard divisors with `if y == 0` |
| 2 | Negative input | `-5` for "iterate `f` `n` times" | Infinite recursion if base case is `n == 0` not `n <= 0` | Use `<=` not `==` |
| 3 | `1` | factorial base | `fact 0 = 1; fact 1 = 1` — handled by recursion only if base is correct | Standard |
| 4 | Very large `Int` | `maxBound :: Int` | `Int` overflows silently → wrong sign | Use `Integer` if spec allows; otherwise tolerate |
| 5 | `2^30` ish | typical "large" QC int | Stack overflow on naive recursion | Standard |
| 6 | `Double` `0/0` | `NaN` | `NaN /= NaN` — equality breaks | Use `isNaN` or stick to Integer |
| 7 | `Double` `1/0` | `Infinity` | `Infinity + 1 == Infinity`, etc. | Handle or avoid |
| 8 | `gcd 0 0` | `0` | Haskell defines this as 0, but some impls error | Library `gcd` is safe |
| 9 | `lcm 0 _` | `0` | Same | Same |
| 10 | `sqrt (-1)` | `NaN` for Double, error for `Integer` square root | Spec-dependent | Maybe-return |
| 11 | `mod a b` for negative `b` | Haskell: `mod (-7) 3 == 2`, `mod 7 (-3) == -2` | Confused with `rem` | `mod` rounds toward negative infinity; `rem` rounds toward zero |
| 12 | `div` and integer rounding | `div (-7) 2 == -4` (toward neg infinity) | Off-by-one if you wanted toward-zero (`quot`) | Use the right one |

## Property templates

```haskell
import Test.QuickCheck

-- gcd properties
prop_gcdCommutative :: Int -> Int -> Bool
prop_gcdCommutative a b = gcd a b == gcd b a

prop_gcdIdentity :: NonNegative Int -> Bool
prop_gcdIdentity (NonNegative n) = gcd n 0 == n

-- Power 0
prop_power0 :: Int -> Bool
prop_power0 _ = (0 :: Int) ^ (0 :: Int) == 1   -- Haskell convention

-- factorial 0
prop_fact0 :: Bool
prop_fact0 = myFact 0 == 1

prop_fact1 :: Bool
prop_fact1 = myFact 1 == 1

prop_factPos :: Property
prop_factPos = forAll (chooseInt (1, 10)) $ \n ->
  myFact n == product [1 .. n]

-- Div by zero is guarded
prop_safeDivZero :: Int -> Bool
prop_safeDivZero a = safeDiv a 0 == Nothing

prop_safeDivNonZero :: Int -> Int -> Property
prop_safeDivNonZero a b = b /= 0 ==> safeDiv a b == Just (a `div` b)
```

## Self-test before submission checklist

- [ ] Function handles `0` as input
- [ ] Function handles negative `Int` (or rejects with guard)
- [ ] Function handles `1` as input (factorial-like)
- [ ] If function divides: divisor cannot be 0 OR is explicitly handled
- [ ] If function modulos: divisor cannot be 0 OR is explicitly handled
- [ ] If function recurses on `n`: uses `<=` for base, not `==`
- [ ] If function uses `Double`: explicitly guarded against `NaN`/`Infinity` if relevant
- [ ] If function returns `Maybe`: actually returns `Nothing` for bad inputs

## Pitfalls that specifically lose QC marks

### Pitfall: `n == 0` base case allows negatives to recurse forever
```haskell
-- WRONG:
factorial 0 = 1
factorial n = n * factorial (n - 1)
-- For n = -1: -1 * factorial (-2) * factorial (-3) ... infinite
-- Fix:
factorial n | n <= 0 = 1            -- or `error` if spec disallows
            | otherwise = n * factorial (n - 1)
```

### Pitfall: `div` by zero
```haskell
-- WRONG:
divisors n = [d | d <- [1..n], n `mod` d == 0]
-- For n = 0: range [1..0] is empty, so OK actually.
-- BUT: divisors 0 returns [] (mathematically every nonzero d divides 0).
-- Spec-dependent.

-- WRONG for general division:
average xs = sum xs `div` length xs
-- For [] (empty list): div by 0
-- Fix:
average [] = 0     -- or error, spec-dependent
average xs = sum xs `div` length xs
```

### Pitfall: `div` vs `quot` rounding direction
```haskell
div (-7) 2 == -4    -- rounds toward negative infinity
quot (-7) 2 == -3   -- rounds toward zero
-- Most exam questions want `div` because it's mathematically natural.
```

### Pitfall: `Int` overflow in `factorial 20`
```haskell
factorial (20 :: Int) == 2432902008176640000   -- fits in Int64
factorial (21 :: Int) == -4249290049419214848  -- OVERFLOWED!
-- Fix: use Integer
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)
```

### Pitfall: `NaN /= NaN`
```haskell
-- WRONG:
isNaNValue x = x == (0/0 :: Double)
-- 0/0 produces NaN, but NaN /= NaN by IEEE 754.
-- Fix: isNaN is already in Prelude — just use it. NO import needed.
isNaNValue :: Double -> Bool
isNaNValue x = isNaN x        -- or: x /= x  (true only for NaN)
```
> **WARNING - not an allowed import:** `Data.Number` is NOT in base and NOT on the exam whitelist (any ad-hoc import scores 0). `isNaN` is exported by `Prelude`, so reference it directly with no import. If you don't trust the name, the self-contained test `x /= x` is `True` only for `NaN`.

### Pitfall: `1/0 == 2/0` is True!
```haskell
-- Surprising:
(1.0 / 0.0) == (2.0 / 0.0) == True
-- Both are Infinity.
-- Use comparison carefully with Doubles.
```

### Pitfall: `sum []` is 0, `product []` is 1, but `maximum []` crashes
```haskell
sum []     == 0    -- OK
product [] == 1    -- OK
maximum [] -- *** Exception: empty list
minimum [] -- same
-- Fix: check empty first or use Foldable's `maximumBy` carefully.
```

### Pitfall: integer power with negative exponent
```haskell
(2 :: Int) ^ (-1)
-- *** Exception: Negative exponent
-- Use `^^` for negative exponents (rational) or guard.
```

### Pitfall: `^` vs `**` vs `^^`
```haskell
-- ^   : non-negative integer exponent (Num base, Integral exponent)
-- ^^  : signed integer exponent (Fractional base, Integral exponent)
-- **  : real exponent (Floating base, Floating exponent)
```

## See also

- `lists-attacks.md` — for numeric lists (`sum`, `maximum`)
- `interp-attacks.md` — for div-by-zero in interpreter
- `matrix-attacks.md` — for sum-of-row overflow concerns
- `../numeric/` (parent vault) — numeric templates

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
