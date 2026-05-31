<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

> [examvault](../README.md) · **typeclasses**

# Typeclasses

> **Tier-1 exam topic.** Birmingham FP exams almost always include ONE typeclass-instance question for a custom ADT (Functor / Applicative / Monad / Foldable / Traversable / Eq / Ord / Show / Monoid).

The exam pattern: a custom data type is given (a tree variant, a Pair, a parser, a Compose), and you must write the `instance` body. The marker QuickCheck-tests the laws.

## Files

| File | Class | What it gives you |
|---|---|---|
| [functor.md](functor.md) | `Functor` | `fmap` for Maybe-like, List-like, BT, Rose, Pair, Either, Reader, Compose |
| [applicative.md](applicative.md) | `Applicative` | `pure`, `<*>` for Maybe, List, Reader, Parser, ZipList, Compose |
| [monad.md](monad.md) | `Monad` | `return`, `>>=` for Maybe, List, Reader, State, Writer, Parser + Functor/Applicative trio |
| [alternative.md](alternative.md) | `Alternative` | `empty`, `<\|>` for Maybe, List, Parser |
| [foldable.md](foldable.md) | `Foldable` | `foldMap`, `foldr` for BT, Rose, Expr, Pair |
| [traversable.md](traversable.md) | `Traversable` | `traverse`, `sequenceA` for BT, Rose; relationship to `mapM` |
| [eq-ord.md](eq-ord.md) | `Eq`, `Ord` | manual instance, `compare` discipline, Ord-of-Ord |
| [show.md](show.md) | `Show` | pretty-printer with precedence |
| [num.md](num.md) | `Num` | rare but possible (Bool ring, Peano nats) |
| [monoid.md](monoid.md) | `Semigroup`, `Monoid` | `<>`, `mempty`, `Sum`/`Product`/`Max`/`Min`/`[a]` |

## Search keywords

instance Functor, instance Applicative, instance Monad, fmap, pure, <\*>, return, >>=, foldMap, traverse, Semigroup, Monoid, mempty, mappend, compare, instance Eq, instance Ord, deriving, Show, showsPrec, Num Bool, Num [()], Alternative, empty, <|>, Compose, Const, Identity, ZipList, Sum, Product

## Recognition: which class does the question want?

| Question phrasing | Class |
|---|---|
| "define `fmap` for", "make T a Functor" | Functor |
| "lift a 2-arg function", "apply wrapped fn", "pure" + "<\*>" | Applicative |
| "in do-notation over T", "make T a Monad", "bind" / `>>=` | Monad |
| "try this or that", "parser alternative", "empty/<\|>" | Alternative |
| "fold T to a sum", "any/all over T", `foldMap`, `foldr` | Foldable |
| "traverse with effects", `mapM` over T, `traverse` | Traversable |
| "compare values of T", `(==)`, `compare` | Eq / Ord |
| "pretty-print T", `show` with parens | Show |
| "integer literals 0,1 for T", `(+) (-) (*)` for T | Num |
| "combine T values", `<>`, identity element | Semigroup / Monoid |

## The Functor → Applicative → Monad hierarchy

Modern Haskell requires the trio:

```haskell
class Functor f
class Functor f     => Applicative f
class Applicative f => Monad f
```

To make `M` a Monad you MUST also declare `Functor M` and `Applicative M`. See [monad.md](monad.md) for the canonical trio template.

## Laws — stated AND as QuickCheck props

Every file gives the laws both ways. The exam often shows QC props to read; if you understand them as the law you understand the constraint.

## Cross-cutting pitfall: shape preservation

Functor's `fmap`, Traversable's `traverse`, and Monad's `mapM` ALL must **preserve the constructor count** of the input. If `fmap f Empty = Fork ...` you have a bug. If you ever lose a `Leaf` or duplicate a `Fork`, you have a bug.

## See also

- [Cross-matrix](../cross-matrix/README.md) — combining typeclass instances with monads in tree/list problems
- [Archetype 06: Functor Instance](../archetypes/) (course archetype)
- [Monads section](../monads/) — for the effect-specific instances
- Course lectures: `typeclasses.md`, `more-typeclasses.md`, `even-more-typeclasses.md`, `monads.md`

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
