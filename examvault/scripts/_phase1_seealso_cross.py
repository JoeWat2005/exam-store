"""Phase 1e: See-also block for cross-matrix files (struct × monad combination pages)."""
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
CROSS = VAULT / 'cross-matrix'

# struct_file is in trees/ for tree/bst/rose, interpreters/ for expr, no theory for list/game
# monad_file is in monads/
# arch is the combined archetype(s)
# fam is the most relevant family
C = {
    'tree-x-maybe':         ('binary tree','../trees/binary-tree.md',  'Maybe','../monads/maybe.md',           ['A01','A08'],['tree-extract-family','env-eval-family'],['trees-attacks','maybe-either-attacks']),
    'tree-x-either':        ('binary tree','../trees/binary-tree.md',  'Either','../monads/either.md',         ['A01','A08'],['tree-extract-family','error-handling-family'],['trees-attacks','maybe-either-attacks']),
    'tree-x-state':         ('binary tree','../trees/binary-tree.md',  'State','../monads/state.md',           ['A01','A02'],['tree-counting-family','state-counter-family'],['trees-attacks','state-attacks']),
    'tree-x-writer':        ('binary tree','../trees/binary-tree.md',  'Writer','../monads/writer.md',         ['A01','A15'],['tree-counting-family','writer-trace-family'],['trees-attacks','writer-attacks']),
    'tree-x-reader':        ('binary tree','../trees/binary-tree.md',  'Reader','../monads/reader.md',         ['A01','A08'],['tree-extract-family','env-eval-family'],['trees-attacks']),
    'tree-x-generic-monad': ('binary tree','../trees/binary-tree.md',  'generic Monad m','../monads/generic-combinators.md',['A01','A03'],['tree-transform-family','monad-combinator-family'],['trees-attacks','monad-attacks']),
    'bst-x-state':          ('BST','../trees/bst.md',                  'State','../monads/state.md',           ['A11','A02'],['bst-ops-family','state-counter-family'],['bst-attacks','state-attacks']),
    'bst-x-writer':         ('BST','../trees/bst.md',                  'Writer','../monads/writer.md',         ['A11','A15'],['bst-ops-family','writer-trace-family'],['bst-attacks','writer-attacks']),
    'rose-x-state':         ('rose tree','../trees/rose-tree.md',      'State','../monads/state.md',           ['A01','A02'],['rose-ops-family','state-counter-family'],['rose-attacks','state-attacks']),
    'rose-x-writer':        ('rose tree','../trees/rose-tree.md',      'Writer','../monads/writer.md',         ['A01','A15'],['rose-ops-family','writer-trace-family'],['rose-attacks','writer-attacks']),
    'expr-x-maybe':         ('expression tree','../trees/expression-tree.md','Maybe','../monads/maybe.md',     ['A05','A08'],['env-eval-family','error-handling-family'],['expr-attacks','maybe-either-attacks']),
    'expr-x-state':         ('expression tree','../trees/expression-tree.md','State','../monads/state.md',     ['A08','A19'],['env-eval-family','state-game-family'],['expr-attacks','state-attacks','interp-attacks']),
    'expr-x-multi':         ('expression tree','../trees/expression-tree.md','multi-effect','../monads/multi-effect.md',['A14','A19'],['env-eval-family','error-handling-family','writer-trace-family'],['expr-attacks','interp-attacks']),
    'list-x-monad':         ('list',None,                              'generic Monad m','../monads/generic-combinators.md',['A03','A10'],['monad-combinator-family','list-fold-family'],['lists-attacks','monad-attacks']),
    'list-x-list-monad':    ('list',None,                              'List monad','../monads/list-monad.md',  ['A03','A21'],['monad-combinator-family','list-comp-family'],['lists-attacks','monad-attacks']),
    'list-x-state':         ('list',None,                              'State','../monads/state.md',           ['A02','A10'],['state-counter-family','list-fold-family'],['lists-attacks','state-attacks']),
    'list-x-writer':        ('list',None,                              'Writer','../monads/writer.md',         ['A15','A10'],['writer-trace-family','list-fold-family'],['lists-attacks','writer-attacks']),
    'game-state':           ('game (Nim, board)',None,                 'State','../monads/state.md',           ['A02','A23'],['state-game-family','state-counter-family'],['state-attacks']),
}

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

def render(struct_label, struct_path, monad_label, monad_path, archs, fams, qcs):
    lines = ['## See also', '']
    lines.append('**Combined archetypes:** ' + ' · '.join(f'[{a} {ARCH_NAMES[a]}](../archetypes/{ARCH_FILES[a]})' for a in archs))
    structlinks = []
    if struct_path:
        structlinks.append(f'[{struct_label}]({struct_path})')
    structlinks.append(f'[{monad_label}]({monad_path})')
    lines.append('**Theory:** ' + ' · '.join(structlinks))
    if fams:
        lines.append('**Question families:** ' + ' · '.join(f'[{n.replace("-family","")}](../question-families/{n}.md)' for n in fams))
    if qcs:
        lines.append('**QuickCheck:** ' + ' · '.join(f'[{q.replace("-attacks","")} attacks](../quickcheck/{q}.md)' for q in qcs))
    return '\n'.join(lines) + '\n'

def replace_seealso(text, new_block):
    pat = re.compile(r'## See also\b.*\Z', re.DOTALL)
    if pat.search(text):
        return pat.sub(new_block.rstrip() + '\n', text)
    return text.rstrip() + '\n\n' + new_block

def main():
    n = 0
    for fname, spec in C.items():
        f = CROSS / f'{fname}.md'
        if not f.exists():
            print(f'MISS {fname}'); continue
        text = f.read_text(encoding='utf-8', newline='')
        block = render(*spec)
        new = replace_seealso(text, block)
        if new != text:
            f.write_text(new, encoding='utf-8', newline='')
            n += 1
            print(f'OK   {fname}')
    print(f'\nTotal: {n} cross-matrix updated')

if __name__ == '__main__':
    main()
