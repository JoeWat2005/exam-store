"""Phase 1e: replace See-also section in each question-family with structured link block."""
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
FAMILIES = VAULT / 'question-families'

# Each family: primary archetype, sibling families, cross-matrix, theory, qc, pitfalls
F = {
    'adt-translation-family':       ('A05 ADT translation', './A05-adt-translation.md', ['codec-family'], ['expr-x-maybe','tree-x-either'], ['expression-tree'], ['codec-attacks','expr-attacks'], [('p-019','Mock Q5 p/q copy-paste')]),
    'applicative-monad-instance-family': ('A24 applicative instance', './A24-applicative-instance.md', ['functor-instance-family','monad-combinator-family'], [], ['applicative','monad'], ['typeclass-instance-attacks','monad-attacks'], []),
    'bst-ops-family':               ('A11 BST ops', './A11-bst-ops.md', ['tree-validation-family','tree-counting-family'], ['bst-x-state','bst-x-writer'], ['bst'], ['bst-attacks'], [('p-009','isBST Empty = False'),('p-015','BST delete two-children'),('p-020','three impls')]),
    'codec-family':                 ('A07 codec pair', './A07-codec-pair.md', ['adt-translation-family'], [], [], ['codec-attacks'], []),
    'env-eval-family':              ('A08 env eval', './A08-env-eval.md', ['error-handling-family'], ['expr-x-state','expr-x-maybe'], [], ['interp-attacks','maybe-either-attacks'], []),
    'error-handling-family':        ('A08 env eval / A05 ADT translation', './A08-env-eval.md', ['env-eval-family'], ['expr-x-maybe','tree-x-either'], [], ['maybe-either-attacks','interp-attacks'], []),
    'functor-instance-family':      ('A06 functor instance', './A06-functor-instance.md', ['applicative-monad-instance-family'], [], ['functor','tree-functor'], ['typeclass-instance-attacks'], [('p-010','deriving Functor unsafe'),('p-016','shape break')]),
    'lazy-infinite-family':         ('A18 lazy memo', './A18-lazy-memo.md', [], [], [], ['lists-attacks'], [('p-023','deepseq exposes lazy undefined')]),
    'list-comp-family':             ('A21 list comp synthesis', './A21-list-comp-synthesis.md', ['list-rewrite-family','list-fold-family'], [], [], ['lists-attacks'], []),
    'list-fold-family':             ('A10 fold reformulation', './A10-fold-reformulation.md', ['list-rewrite-family','list-comp-family'], ['list-x-list-monad'], [], ['lists-attacks'], []),
    'list-rewrite-family':          ('A09 prelude reimpl', './A09-prelude-reimpl.md', ['list-fold-family','list-comp-family'], [], [], ['lists-attacks'], [('p-018','head/tail/!! without guard')]),
    'matrix-predicate-family':      ('A04 matrix predicate', './A04-matrix-predicate.md', [], [], [], ['matrix-attacks'], [('p-030','magic square wrong direction')]),
    'monad-combinator-family':      ('A03 generic monad', './A03-generic-monad.md', ['applicative-monad-instance-family'], ['tree-x-generic-monad','list-x-monad'], ['monad','generic-combinators'], ['monad-attacks'], [('p-007','applyNTimes 0 returns [] not [x]')]),
    'parser-family':                ('A16 parser combinators', './A16-parser-combinators.md', [], [], [], ['interp-attacks'], []),
    'pretty-print-family':          ('A13 pretty printer', './A13-pretty-printer.md', [], [], ['show'], ['lists-attacks'], [('p-012','custom Show non-string')]),
    'rose-ops-family':              ('A01 tree recursion', './A01-tree-recursion.md', ['tree-counting-family','tree-validation-family','tree-transform-family','tree-extract-family'], ['rose-x-state','rose-x-writer'], ['rose-tree'], ['rose-attacks'], []),
    'state-counter-family':         ('A02 state game', './A02-state-game.md', ['state-game-family'], ['rose-x-state','tree-x-state','bst-x-state'], ['state'], ['state-attacks'], [('p-008','n<=0 not n==0')]),
    'state-game-family':            ('A02 state game', './A02-state-game.md', ['state-counter-family'], ['game-state','rose-x-state','tree-x-state'], ['state'], ['state-attacks'], [('p-006','Mock Q3 gameOver(0,0)'),('p-024','state action wrong type')]),
    'tree-counting-family':         ('A01 tree recursion', './A01-tree-recursion.md', ['tree-extract-family','tree-validation-family','rose-ops-family'], ['tree-x-state','tree-x-writer','tree-x-maybe'], ['binary-tree','tree-fold'], ['trees-attacks'], [('p-005','missing base case')]),
    'tree-extract-family':          ('A01 tree recursion', './A01-tree-recursion.md', ['tree-counting-family','tree-transform-family','rose-ops-family'], ['tree-x-maybe','tree-x-either'], ['binary-tree','tree-traversals'], ['trees-attacks'], []),
    'tree-transform-family':        ('A01 tree recursion', './A01-tree-recursion.md', ['tree-counting-family','tree-extract-family','rose-ops-family'], ['tree-x-state','tree-x-generic-monad'], ['binary-tree','tree-functor','tree-zipper'], ['trees-attacks'], [('p-016','functor doesn\'t preserve shape')]),
    'tree-validation-family':       ('A01 tree recursion', './A01-tree-recursion.md', ['bst-ops-family','tree-counting-family','rose-ops-family'], ['tree-x-maybe'], ['binary-tree','bst'], ['trees-attacks','bst-attacks'], [('p-009','isBST Empty = False'),('p-014','shallow recursion')]),
    'writer-trace-family':          ('A15 writer trace', './A15-writer-trace.md', [], ['rose-x-writer','tree-x-writer','bst-x-writer','list-x-writer'], ['writer'], ['writer-attacks'], []),
}

def render(arch_label, arch_path, siblings, crosses, theory, qcs, pitfalls):
    lines = ['## See also', '']
    lines.append(f'**Primary archetype:** [{arch_label}](../archetypes/{arch_path[2:]})')
    if siblings:
        lines.append('**Sibling families:** ' + ' · '.join(f'[{s.replace("-family","")}](./{s}.md)' for s in siblings))
    if crosses:
        lines.append('**Cross-topic:** ' + ' · '.join(f'[{c.replace("-x-"," × ")}](../cross-matrix/{c}.md)' for c in crosses))
    if theory:
        # map names to dirs
        theory_links = []
        for t in theory:
            for d in ('trees','monads','typeclasses','interpreters'):
                p = VAULT / d / f'{t}.md'
                if p.exists():
                    theory_links.append(f'[{t.replace("-"," ")}](../{d}/{t}.md)')
                    break
        if theory_links:
            lines.append('**Theory:** ' + ' · '.join(theory_links))
    if qcs:
        lines.append('**QuickCheck:** ' + ' · '.join(f'[{q.replace("-attacks","")} attacks](../quickcheck/{q}.md)' for q in qcs))
    if pitfalls:
        lines.append('**Pitfalls:** ' + ' · '.join(f'[P-{pid[2:]} {desc}](../pitfalls/HIGH-severity.md#{pid})' for pid,desc in pitfalls))
    return '\n'.join(lines) + '\n'

def replace_seealso(text, new_block):
    pat = re.compile(r'## See also\b.*\Z', re.DOTALL)
    if pat.search(text):
        return pat.sub(new_block.rstrip() + '\n', text)
    return text.rstrip() + '\n\n' + new_block

def main():
    n = 0
    for fname, (arch_label, arch_path, siblings, crosses, theory, qcs, pitfalls) in F.items():
        f = FAMILIES / f'{fname}.md'
        if not f.exists():
            print(f'MISS {fname}'); continue
        text = f.read_text(encoding='utf-8', newline='')
        block = render(arch_label, arch_path, siblings, crosses, theory, qcs, pitfalls)
        new = replace_seealso(text, block)
        if new != text:
            f.write_text(new, encoding='utf-8', newline='')
            n += 1
            print(f'OK   {fname}')
    print(f'\nTotal: {n} families updated')

if __name__ == '__main__':
    main()
