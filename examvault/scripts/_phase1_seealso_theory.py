"""Phase 1e: See-also blocks for theory dirs (monads, typeclasses, trees, interpreters, quickcheck)."""
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent

ARCH_NAMES = {
    'A01': 'tree recursion', 'A02': 'state game', 'A03': 'generic monad',
    'A04': 'matrix predicate', 'A05': 'ADT translation', 'A06': 'functor instance',
    'A07': 'codec pair', 'A08': 'env eval', 'A09': 'prelude reimpl',
    'A10': 'fold reformulation', 'A11': 'BST ops', 'A12': 'rep conversion',
    'A13': 'pretty printer', 'A14': 'multi-effect interp', 'A15': 'writer trace',
    'A16': 'parser combinators', 'A17': 'zipper', 'A18': 'lazy memo',
    'A19': 'extend interpreter', 'A20': 'laws / iso', 'A21': 'list comp synthesis',
    'A22': 'typeclass instance', 'A23': 'mini-game', 'A24': 'applicative instance',
}
ARCH_FILES = {a.stem.split('-',1)[0]: a.name for a in (VAULT/'archetypes').glob('A*.md')}

# Per-page mapping. Each entry: (archetypes, cross-matrix, families, qc, related-theory)
PAGES = {
    'monads/maybe.md':              (['A08','A09'], ['tree-x-maybe','expr-x-maybe'], ['env-eval-family','error-handling-family'], ['maybe-either-attacks'], ['either.md','generic-combinators.md']),
    'monads/either.md':             (['A08','A05'], ['tree-x-either','expr-x-maybe'], ['error-handling-family','env-eval-family'], ['maybe-either-attacks'], ['maybe.md','monaderror.md']),
    'monads/state.md':              (['A02','A23'], ['tree-x-state','bst-x-state','rose-x-state','expr-x-state','list-x-state','game-state'], ['state-game-family','state-counter-family'], ['state-attacks'], ['transformers.md','multi-effect.md']),
    'monads/writer.md':             (['A15'],       ['tree-x-writer','bst-x-writer','rose-x-writer','list-x-writer'], ['writer-trace-family'], ['writer-attacks'], ['transformers.md','multi-effect.md']),
    'monads/reader.md':             (['A08'],       ['tree-x-reader'], ['env-eval-family'], [], ['multi-effect.md']),
    'monads/io.md':                 ([],            [], [], [], []),
    'monads/list-monad.md':         (['A03','A21'], ['list-x-list-monad','list-x-monad'], ['monad-combinator-family','list-comp-family'], ['monad-attacks'], ['generic-combinators.md']),
    'monads/monaderror.md':         (['A08'],       [], ['error-handling-family'], ['maybe-either-attacks'], ['either.md']),
    'monads/multi-effect.md':       (['A14','A19'], ['expr-x-multi'], ['env-eval-family','writer-trace-family'], ['interp-attacks'], ['transformers.md','transformer-stack-order.md']),
    'monads/transformers.md':       (['A14','A19'], ['expr-x-multi'], ['env-eval-family','error-handling-family','writer-trace-family'], ['interp-attacks'], ['multi-effect.md','transformer-stack-order.md']),
    'monads/monad-laws.md':         (['A20','A22'], [], [], ['typeclass-instance-attacks'], []),
    'monads/generic-combinators.md':(['A03'],       ['tree-x-generic-monad','list-x-monad'], ['monad-combinator-family'], ['monad-attacks'], []),
    'typeclasses/functor.md':       (['A06','A22'], [], ['functor-instance-family'], ['typeclass-instance-attacks'], ['applicative.md','monad.md']),
    'typeclasses/applicative.md':   (['A24','A22'], [], ['applicative-monad-instance-family'], ['typeclass-instance-attacks'], ['functor.md','monad.md','alternative.md']),
    'typeclasses/monad.md':         (['A03','A22'], ['tree-x-generic-monad'], ['monad-combinator-family','applicative-monad-instance-family'], ['monad-attacks','typeclass-instance-attacks'], ['functor.md','applicative.md']),
    'typeclasses/alternative.md':   (['A16'],       [], ['parser-family'], [], ['applicative.md']),
    'typeclasses/foldable.md':      (['A10'],       [], ['list-fold-family'], [], ['traversable.md']),
    'typeclasses/traversable.md':   (['A06'],       [], [], [], ['foldable.md','functor.md']),
    'typeclasses/monoid.md':        (['A15'],       [], ['writer-trace-family'], [], []),
    'typeclasses/eq-ord.md':        (['A11'],       [], ['bst-ops-family'], ['bst-attacks'], []),
    'typeclasses/show.md':          (['A13'],       [], ['pretty-print-family'], [], []),
    'typeclasses/num.md':           ([],            [], [], ['numeric-attacks'], []),
    'trees/binary-tree.md':         (['A01'],       ['tree-x-state','tree-x-writer','tree-x-maybe','tree-x-either','tree-x-reader','tree-x-generic-monad'], ['tree-counting-family','tree-validation-family','tree-transform-family','tree-extract-family'], ['trees-attacks'], ['bst.md','rose-tree.md','tree-fold.md','tree-functor.md','tree-traversals.md']),
    'trees/bst.md':                 (['A11','A01'], ['bst-x-state','bst-x-writer'], ['bst-ops-family','tree-validation-family'], ['bst-attacks'], ['binary-tree.md']),
    'trees/rose-tree.md':           (['A01'],       ['rose-x-state','rose-x-writer'], ['rose-ops-family'], ['rose-attacks'], ['binary-tree.md','tree-fold.md']),
    'trees/expression-tree.md':     (['A05','A08'], ['expr-x-maybe','expr-x-state','expr-x-multi'], ['adt-translation-family','env-eval-family'], ['expr-attacks'], []),
    'trees/tree-counting.md':       (['A01'],       ['tree-x-state'], ['tree-counting-family'], ['trees-attacks'], ['binary-tree.md','tree-fold.md']),
    'trees/tree-fold.md':           (['A01','A10'], [], ['tree-counting-family','list-fold-family'], ['trees-attacks'], ['binary-tree.md','tree-traversals.md']),
    'trees/tree-functor.md':        (['A06','A01'], [], ['functor-instance-family','tree-transform-family'], ['typeclass-instance-attacks'], ['binary-tree.md','tree-transform.md']),
    'trees/tree-traversals.md':     (['A01'],       ['tree-x-generic-monad'], ['tree-extract-family'], ['trees-attacks'], ['binary-tree.md','tree-fold.md']),
    'trees/tree-validation.md':     (['A01','A11'], [], ['tree-validation-family','bst-ops-family'], ['trees-attacks','bst-attacks'], ['binary-tree.md','bst.md']),
    'trees/tree-zipper.md':         (['A17','A01'], [], ['tree-transform-family'], ['trees-attacks'], ['binary-tree.md']),
    'interpreters/simple-arith.md':       (['A08'],       ['expr-x-maybe'], ['env-eval-family'], ['interp-attacks'], ['expr-maybe.md']),
    'interpreters/expr-maybe.md':         (['A08'],       ['expr-x-maybe'], ['env-eval-family','error-handling-family'], ['interp-attacks','maybe-either-attacks'], ['expr-either.md','expr-state.md']),
    'interpreters/expr-either.md':        (['A08'],       [], ['error-handling-family'], ['interp-attacks','maybe-either-attacks'], ['expr-maybe.md','expr-reader-either.md']),
    'interpreters/expr-state.md':         (['A08','A02'], ['expr-x-state'], ['env-eval-family','state-game-family'], ['interp-attacks','state-attacks'], ['expr-state-either.md','imperative-storage.md']),
    'interpreters/expr-writer.md':        (['A08','A15'], [], ['env-eval-family','writer-trace-family'], ['interp-attacks','writer-attacks'], ['expr-writer-state.md','expr-state.md']),
    'interpreters/expr-reader.md':        (['A08'],       [], ['env-eval-family'], ['interp-attacks'], ['expr-reader-either.md']),
    'interpreters/expr-reader-either.md': (['A08','A19'], [], ['env-eval-family','error-handling-family'], ['interp-attacks','maybe-either-attacks'], ['expr-reader.md','expr-state-either.md']),
    'interpreters/expr-state-either.md':  (['A14','A19'], ['expr-x-multi'], ['env-eval-family','error-handling-family'], ['interp-attacks','state-attacks'], ['expr-state.md','expr-multi-effect.md']),
    'interpreters/expr-writer-state.md':  (['A14','A15'], [], ['writer-trace-family','env-eval-family'], ['interp-attacks','writer-attacks','state-attacks'], ['expr-writer.md','expr-state.md','expr-multi-effect.md']),
    'interpreters/expr-multi-effect.md':  (['A14','A19'], ['expr-x-multi'], ['env-eval-family','error-handling-family','writer-trace-family'], ['interp-attacks'], ['expr-state-either.md','expr-writer-state.md']),
    'interpreters/imperative-eval.md':    (['A08'],       [], ['env-eval-family'], ['interp-attacks'], ['imperative-storage.md']),
    'interpreters/imperative-storage.md': (['A02','A08'], ['expr-x-state'], ['env-eval-family','state-game-family'], ['interp-attacks','state-attacks'], ['imperative-eval.md','expr-state.md']),
    'interpreters/extend-interpreter.md': (['A19','A14'], [], ['env-eval-family','error-handling-family'], ['interp-attacks'], ['expr-multi-effect.md','expr-state-either.md']),
    'interpreters/desugar-pipeline.md':   (['A19'],       [], ['env-eval-family'], ['interp-attacks'], ['extend-interpreter.md']),
    'interpreters/parser-overview.md':    (['A16'],       [], ['parser-family'], ['interp-attacks'], []),
    'quickcheck/QUICKCHECK-ATTACKS.md':   ([],            [], [], [], []),
    'quickcheck/trees-attacks.md':        (['A01'],       ['tree-x-state','tree-x-writer'], ['tree-counting-family','tree-validation-family'], [], []),
    'quickcheck/bst-attacks.md':          (['A11'],       ['bst-x-state'], ['bst-ops-family'], [], []),
    'quickcheck/rose-attacks.md':         (['A01'],       ['rose-x-state','rose-x-writer'], ['rose-ops-family'], [], []),
    'quickcheck/expr-attacks.md':         (['A05','A08'], ['expr-x-maybe','expr-x-state'], ['adt-translation-family','env-eval-family'], [], []),
    'quickcheck/monad-attacks.md':        (['A03'],       ['tree-x-generic-monad','list-x-monad'], ['monad-combinator-family'], [], []),
    'quickcheck/state-attacks.md':        (['A02'],       ['tree-x-state','game-state'], ['state-game-family'], [], []),
    'quickcheck/writer-attacks.md':       (['A15'],       ['tree-x-writer','rose-x-writer'], ['writer-trace-family'], [], []),
    'quickcheck/maybe-either-attacks.md': (['A08'],       ['tree-x-maybe','expr-x-maybe'], ['env-eval-family','error-handling-family'], [], []),
    'quickcheck/codec-attacks.md':        (['A07','A05'], [], ['codec-family','adt-translation-family'], [], []),
    'quickcheck/interp-attacks.md':       (['A08','A14','A19'], ['expr-x-multi','expr-x-state'], ['env-eval-family'], [], []),
    'quickcheck/matrix-attacks.md':       (['A04'],       [], ['matrix-predicate-family'], [], []),
    'quickcheck/numeric-attacks.md':      ([],            [], [], [], []),
    'quickcheck/lists-attacks.md':        (['A09','A10','A21'], [], ['list-rewrite-family','list-fold-family','list-comp-family'], [], []),
    'quickcheck/typeclass-instance-attacks.md': (['A06','A22','A24'], [], ['functor-instance-family','applicative-monad-instance-family'], [], []),
}

def render(arch_codes, crosses, fams, qcs, related, page_path):
    lines = ['## See also', '']
    if arch_codes:
        lines.append('**Archetypes:** ' + ' · '.join(f'[{a} {ARCH_NAMES[a]}](../archetypes/{ARCH_FILES[a]})' for a in arch_codes))
    if crosses:
        lines.append('**Cross-topic:** ' + ' · '.join(f'[{c.replace("-x-"," × ")}](../cross-matrix/{c}.md)' for c in crosses))
    if fams:
        lines.append('**Question families:** ' + ' · '.join(f'[{n.replace("-family","")}](../question-families/{n}.md)' for n in fams))
    if qcs:
        lines.append('**QuickCheck:** ' + ' · '.join(f'[{q.replace("-attacks","")} attacks](../quickcheck/{q}.md)' for q in qcs))
    if related:
        # related files live in same dir as page_path
        dir_name = page_path.split('/')[0]
        rel_links = []
        for r in related:
            rel_links.append(f'[{r.replace(".md","").replace("-"," ")}](./{r})')
        lines.append(f'**Related ({dir_name}):** ' + ' · '.join(rel_links))
    return '\n'.join(lines) + '\n' if len(lines) > 2 else ''

def replace_seealso(text, new_block):
    if not new_block:
        return text
    pat = re.compile(r'## See also\b.*\Z', re.DOTALL)
    if pat.search(text):
        return pat.sub(new_block.rstrip() + '\n', text)
    return text.rstrip() + '\n\n' + new_block

def main():
    n = 0; skipped = 0
    for relpath, spec in PAGES.items():
        f = VAULT / relpath
        if not f.exists():
            print(f'MISS {relpath}'); continue
        text = f.read_text(encoding='utf-8', newline='')
        block = render(*spec, page_path=relpath)
        if not block:
            skipped += 1; continue
        new = replace_seealso(text, block)
        if new != text:
            f.write_text(new, encoding='utf-8', newline='')
            n += 1
            print(f'OK   {relpath}')
    print(f'\nTotal: {n} updated, {skipped} no-link-targets')

if __name__ == '__main__':
    main()
