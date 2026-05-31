"""Phase 9 link-cleanup: walk markdown files, fix broken internal links via a
name-translation map, log any unmappable broken links for manual review.

Translation map captures the old/aspirational filenames that show up in
meta/COURSE-COVERAGE.md (39 broken) and meta/VAULT-AUDIT.md (13 broken).
"""
import re, sys, io
from pathlib import Path

# Force UTF-8 stdout so unicode labels in unmappable-log print on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

VAULT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'scripts', 'graphs', '.git'}

# (broken_path, correct_path) — paths relative to vault root
TRANSLATIONS = {
    # archetype renames
    'archetypes/A21-comprehension-synthesis.md': 'archetypes/A21-list-comp-synthesis.md',
    'archetypes/A05-adt-to-adt.md':              'archetypes/A05-adt-translation.md',
    'archetypes/A22-instance-for-adt.md':        'archetypes/A22-typeclass-instance.md',
    'archetypes/A06-fam-instance.md':            'archetypes/A06-functor-instance.md',
    'archetypes/A01-tree-structural-rec.md':     'archetypes/A01-tree-recursion.md',
    'archetypes/A13-show-pretty-printer.md':     'archetypes/A13-pretty-printer.md',
    'archetypes/A02-state-mini-game.md':         'archetypes/A02-state-game.md',
    'archetypes/A14-multi-effect.md':            'archetypes/A14-multi-effect-interp.md',
    'archetypes/A19-extend-interp.md':           'archetypes/A19-extend-interpreter.md',
    'archetypes/A11-bst.md':                     'archetypes/A11-bst-ops.md',
    'archetypes/A07-codec.md':                   'archetypes/A07-codec-pair.md',
    'archetypes/A09-prelude.md':                 'archetypes/A09-prelude-reimpl.md',
    'archetypes/A10-fold.md':                    'archetypes/A10-fold-reformulation.md',
    'archetypes/A18-lazy.md':                    'archetypes/A18-lazy-memo.md',
    'archetypes/A20-iso.md':                     'archetypes/A20-laws-iso.md',
    'archetypes/A23-game.md':                    'archetypes/A23-mini-game.md',
    'archetypes/A24-applicative.md':             'archetypes/A24-applicative-instance.md',
    # tree renames
    'trees/binary-trees.md': 'trees/binary-tree.md',
    'trees/rose-trees.md':   'trees/rose-tree.md',
    'trees/expression-trees.md': 'trees/expression-tree.md',
    # monad renames
    'monads/list.md':        'monads/list-monad.md',
    'monads/free.md':        'monads/multi-effect.md',  # Free is embedded in multi-effect/A14
    # interpreter renames
    'interpreters/env-eval.md':       'interpreters/expr-reader.md',
    'interpreters/interpreter-extension.md': 'interpreters/extend-interpreter.md',
    # typeclass renames
    'typeclasses/eq-ord-num.md':    'typeclasses/eq-ord.md',
    'typeclasses/basic.md':         'typeclasses/README.md',
    'typeclasses/deriving.md':      'typeclasses/README.md',
    'typeclasses/kind-and-partial-application.md': 'typeclasses/functor.md',
    'typeclasses/custom-instances.md': 'typeclasses/README.md',
    # cross-matrix renames
    'cross-matrix/tree-x-monad.md':  'cross-matrix/tree-x-generic-monad.md',
    'cross-matrix/monad-x-error.md': 'cross-matrix/tree-x-either.md',
    # question-families
    'question-families/string-cipher.md': 'question-families/codec-family.md',
    # pitfall renames (these were never standalone; they're sections in HIGH/MEDIUM/LOW)
    'pitfalls/non-exhaustive.md':    'pitfalls/HIGH-severity.md#p-017',
    'pitfalls/foldl-vs-foldr.md':    'pitfalls/HIGH-severity.md#p-023',
    'pitfalls/three-bst-impls.md':   'pitfalls/HIGH-severity.md#p-020',
    'pitfalls/shallow-isNBranching.md': 'pitfalls/HIGH-severity.md#p-014',
    'pitfalls/isBST-Empty-False.md': 'pitfalls/HIGH-severity.md#p-009',
    'pitfalls/missing-base.md':      'pitfalls/HIGH-severity.md#p-005',
    'pitfalls/deriving-functor.md':  'pitfalls/HIGH-severity.md#p-010',
    'pitfalls/Or-with-p-not-q.md':   'pitfalls/HIGH-severity.md#p-019',
    'pitfalls/safe-pragma.md':       'pitfalls/HIGH-severity.md#p-011',
    'pitfalls/imports-forbidden.md': 'pitfalls/imports-pitfalls.md',
    # phantom files referenced from VAULT-AUDIT — point to the new homes
    'if-you-see-x.md':               'indexes/IF-YOU-SEE-X.md',
    'common-templates.md':           'haskell-basics/README.md',
    'type-signature-decoder.md':     'indexes/TYPE-SIGNATURE-DATABASE.md',
    'archetypes/00-priority.md':     'archetypes/README.md',
    'common-pitfalls.md':            'pitfalls/README.md',
    'archetypes/parser.md':          'archetypes/A16-parser-combinators.md',
    'archetypes/codec.md':           'archetypes/A07-codec-pair.md',
    'monads/transformer-stack-order.md': 'monads/transformer-stack-order.md',  # exists now — verify
    'monads/monadfail-pattern-bind.md':  'haskell-basics/do-notation-basics.md',  # MonadFail covered there
    'trees/bst-delete-walkthrough.md':   'trees/bst-delete-trace.md',
    'quickcheck/safe-pragma.md':         'pitfalls/HIGH-severity.md#p-011',
    # second-pass discoveries
    'archetypes/A08-env-evaluator.md':   'archetypes/A08-env-eval.md',
    'interpreters/expr.md':              'interpreters/simple-arith.md',
    'interpreters/arith.md':             'interpreters/simple-arith.md',
    'interpreters/imperative.md':        'interpreters/imperative-eval.md',
    'trees/rose.md':                     'trees/rose-tree.md',
    'trees/binary.md':                   'trees/binary-tree.md',
    'trees/expr.md':                     'trees/expression-tree.md',
    'trees/bst-delete.md':               'trees/bst-delete-trace.md',
    'monads/overview.md':                'monads/README.md',
    'monads/io-prime.md':                'monads/io.md',
    'monads/iomonad.md':                 'monads/io.md',
    'quickcheck/property-patterns.md':   'quickcheck/PROPERTY-PATTERNS.md',
    'quickcheck/arbitrary.md':           'quickcheck/PROPERTY-PATTERNS.md',
    'cross-matrix/parser-x-error.md':    'cross-matrix/parser-x-either.md',
    'cross-matrix/writer-x-fail.md':     'cross-matrix/writer-x-either.md',
    'haskell-basics/safe.md':            'pitfalls/HIGH-severity.md#p-011',
    'examples/morse-codec.md':           'archetypes/A07-codec-pair.md',
    'examples/env-eval-example.md':      'archetypes/A08-env-eval.md',
    'examples/minimax.md':               'archetypes/A23-mini-game.md',
    'examples/fib-memo.md':              'archetypes/A18-lazy-memo.md',
    'examples/expr-parser.md':           'interpreters/parser-chainl1.md',
    'practice/05-binary-and-rose-trees.md': 'trees/binary-tree.md',
    'patterns/lazy-memoization.md':      'archetypes/A18-lazy-memo.md',
    'templates/tree-bt.md':              'archetypes/A01-tree-recursion.md',
    'templates/tree-rose.md':            'trees/rose-tree.md',
    'templates/parser-newtype.md':       'archetypes/A16-parser-combinators.md',
    # third-pass discoveries
    'interpreters/env.md':               'interpreters/expr-reader.md',
    'interpreters/error.md':             'interpreters/expr-either.md',
    'interpreters/overview.md':          'interpreters/README.md',
    'archetypes/A18-lazy-memoisation.md':'archetypes/A18-lazy-memo.md',
    'archetypes/A18-lazy-memoization.md':'archetypes/A18-lazy-memo.md',
    'meta/INDEX.md':                     'README.md',
    'meta/NAVIGATION.md':                'README.md',
    # final pass
    'pitfalls/strictness.md':            'pitfalls/HIGH-severity.md#p-023',
    'pitfalls/proof-vs-program.md':      'pitfalls/README.md',
    'archetypes/A20-laws-iso-retract.md':'archetypes/A20-laws-iso.md',
    'archetypes/A17-zipper-navigation.md':'archetypes/A17-zipper.md',
    'quickcheck/laws.md':                'monads/monad-laws.md',
    # Old archetype filename patterns (numeric, no prefix)
    'archetypes/11-bst.md':              'archetypes/A11-bst-ops.md',
    'archetypes/01-tree-recursion.md':   'archetypes/A01-tree-recursion.md',
    'archetypes/02-state-game.md':       'archetypes/A02-state-game.md',
    'archetypes/03-generic-monad.md':    'archetypes/A03-generic-monad.md',
    # old cross-matrix and patterns refs
    'cross-matrix/expr-x-monad.md':      'cross-matrix/expr-x-multi.md',
    'patterns/tree-recursion.md':        'archetypes/A01-tree-recursion.md',
    'patterns/list-recursion.md':        'archetypes/A09-prelude-reimpl.md',
    # final pass: numeric-prefix archetype names
    'archetypes/05-adt-translation.md':  'archetypes/A05-adt-translation.md',
    'archetypes/08-env-eval.md':         'archetypes/A08-env-eval.md',
    'archetypes/16-parser.md':           'archetypes/A16-parser-combinators.md',
    'archetypes/17-zipper.md':           'archetypes/A17-zipper.md',
    'archetypes/04-matrix.md':           'archetypes/A04-matrix-predicate.md',
    'archetypes/06-functor.md':          'archetypes/A06-functor-instance.md',
    'archetypes/07-codec.md':            'archetypes/A07-codec-pair.md',
    'archetypes/09-prelude.md':          'archetypes/A09-prelude-reimpl.md',
    'archetypes/10-fold.md':             'archetypes/A10-fold-reformulation.md',
    'archetypes/13-show.md':             'archetypes/A13-pretty-printer.md',
    'archetypes/14-multi-effect.md':     'archetypes/A14-multi-effect-interp.md',
    'archetypes/15-writer.md':           'archetypes/A15-writer-trace.md',
    'archetypes/18-lazy.md':             'archetypes/A18-lazy-memo.md',
    'archetypes/19-extend.md':           'archetypes/A19-extend-interpreter.md',
    'archetypes/20-laws.md':             'archetypes/A20-laws-iso.md',
    'archetypes/21-list-comp.md':        'archetypes/A21-list-comp-synthesis.md',
    'archetypes/22-typeclass.md':        'archetypes/A22-typeclass-instance.md',
    'archetypes/23-mini-game.md':        'archetypes/A23-mini-game.md',
    'archetypes/24-applicative.md':      'archetypes/A24-applicative-instance.md',
    # other lingering refs
    'interpreters/simple-eval.md':       'interpreters/simple-arith.md',
    'monads/mapM-traverse.md':           'monads/generic-combinators.md',
    # absolute last cleanup
    'archetypes/06-functor-instance.md': 'archetypes/A06-functor-instance.md',
    'archetypes/10-fold-reformulation.md': 'archetypes/A10-fold-reformulation.md',
    'archetypes/01-tree-recursion.md':   'archetypes/A01-tree-recursion.md',
    'archetypes/02-state-game.md':       'archetypes/A02-state-game.md',
    'patterns/folds.md':                 'archetypes/A10-fold-reformulation.md',
    'exam-day/mock-q1-rose.md':          'archetypes/A01-tree-recursion.md',
}

LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)#]+)(#[^)]*)?\)')

def resolve(file_path, link_target):
    """Resolve a link target (relative to file_path's parent) to an absolute vault-relative path."""
    base = file_path.parent
    # Skip external links
    if link_target.startswith('http') or link_target.startswith('mailto'):
        return None
    # Resolve relative
    target = (base / link_target).resolve()
    try:
        rel = target.relative_to(VAULT.resolve())
        return str(rel).replace('\\', '/')
    except ValueError:
        return None

def fix_text(text, file_path):
    """For each link, if target doesn't exist and is in TRANSLATIONS, replace it."""
    n_fixed = 0
    unmappable = []

    def replace(m):
        nonlocal n_fixed
        label, url, anchor = m.group(1), m.group(2), m.group(3) or ''
        # Skip external links
        if url.startswith('http') or url.startswith('mailto') or url.startswith('#'):
            return m.group(0)
        # Compute vault-relative target
        target_rel = resolve(file_path, url)
        if target_rel is None:
            return m.group(0)
        # Check if the file (without anchor) exists
        target_path = VAULT / target_rel
        if target_path.exists():
            return m.group(0)  # link OK
        # Broken: try translation
        # Try with full path
        if target_rel in TRANSLATIONS:
            new_target = TRANSLATIONS[target_rel]
            # Recompute relative from file_path
            base_parts = file_path.parent.resolve().relative_to(VAULT.resolve()).parts
            new_parts = new_target.split('/')
            # Find common prefix
            i = 0
            while i < len(base_parts) and i < len(new_parts) - 1 and base_parts[i] == new_parts[i]:
                i += 1
            up = ['..'] * (len(base_parts) - i)
            down = new_parts[i:]
            new_url = '/'.join(up + down)
            # If new_target already contains an anchor, drop the old anchor
            if '#' in new_target:
                new_anchor = ''  # the new target's anchor wins
            else:
                new_anchor = anchor
            n_fixed += 1
            return f'[{label}]({new_url}{new_anchor})'
        # Not in map — log
        unmappable.append((target_rel, url, label))
        return m.group(0)

    new = LINK_RE.sub(replace, text)
    return new, n_fixed, unmappable

def main():
    targets = sorted(set(
        [str(p.relative_to(VAULT)).replace('\\', '/') for p in VAULT.rglob('*.md')
         if p.relative_to(VAULT).parts[0] not in ('scripts', 'graphs', '.git')]
    ))
    total_fixed = 0
    all_unmappable = []
    for rel in targets:
        path = VAULT / rel
        if not path.exists():
            print(f'MISS {rel}')
            continue
        text = path.read_text(encoding='utf-8', newline='')
        new, n, unmap = fix_text(text, path)
        if new != text:
            path.write_text(new, encoding='utf-8', newline='')
            total_fixed += n
        print(f'{rel}: {n} fixed, {len(unmap)} unmappable')
        for u in unmap[:5]:
            print(f'  ?? {u[0]}  (label: {u[2][:60]})')
        all_unmappable.extend((rel, u) for u in unmap)
    print(f'\nTOTAL: {total_fixed} links fixed across {len(targets)} files')
    print(f'TOTAL unmappable: {len(all_unmappable)}')

if __name__ == '__main__':
    main()
