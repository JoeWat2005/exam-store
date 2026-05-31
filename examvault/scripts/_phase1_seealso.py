"""Phase 1e: replace the prose '## See also' section in each archetype with a structured link block."""
import re
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
ARCHETYPES = VAULT / 'archetypes'

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

ARCH_FILE = {k: f"./{k}-{ARCH_NAMES[k].replace(' / ', '-').replace(' ', '-')}.md" for k in ARCH_NAMES}
# Manual overrides where actual filename differs from generated:
ARCH_FILE['A05'] = './A05-adt-translation.md'
ARCH_FILE['A11'] = './A11-bst-ops.md'
ARCH_FILE['A14'] = './A14-multi-effect-interp.md'
ARCH_FILE['A20'] = './A20-laws-iso.md'

def arch_link(code):
    return f"[{code} {ARCH_NAMES[code]}]({ARCH_FILE[code]})"

# (combines, families, cross-matrix, theory, pitfalls, qc, mock)
SEEALSO = {
    'A02': {
        'combines': ['A01','A03','A04','A23'],
        'families': [('state-game','../question-families/state-game-family.md'), ('state-counter','../question-families/state-counter-family.md')],
        'cross':    [('rose × state','../cross-matrix/rose-x-state.md'), ('tree × state','../cross-matrix/tree-x-state.md'), ('bst × state','../cross-matrix/bst-x-state.md'), ('game-state','../cross-matrix/game-state.md')],
        'theory':   [('State monad','../monads/state.md')],
        'pitfalls': [('p-006','Mock Q3 gameOver(0,0)'), ('p-008','n<=0 not n==0'), ('p-024','state action wrong type')],
        'qc':       [('state attacks','../quickcheck/state-attacks.md')],
        'mock':     [('Q3 Nim','#mock-q3')],
    },
    'A03': {
        'combines': ['A01','A24'],
        'families': [('monad-combinator','../question-families/monad-combinator-family.md'), ('applicative-monad-instance','../question-families/applicative-monad-instance-family.md')],
        'cross':    [('tree × generic monad','../cross-matrix/tree-x-generic-monad.md'), ('list × monad','../cross-matrix/list-x-monad.md')],
        'theory':   [('Monad typeclass','../typeclasses/monad.md'), ('generic combinators','../monads/generic-combinators.md')],
        'pitfalls': [('p-007','applyNTimes 0 returns [] not [x]')],
        'qc':       [('monad attacks','../quickcheck/monad-attacks.md')],
        'mock':     [('Q2 applyNTimes','#mock-q2')],
    },
    'A04': {
        'combines': ['A09','A21'],
        'families': [('matrix-predicate','../question-families/matrix-predicate-family.md')],
        'cross':    [],
        'theory':   [],
        'pitfalls': [('p-030','magic square wrong direction')],
        'qc':       [('matrix attacks','../quickcheck/matrix-attacks.md')],
        'mock':     [('Q4 magic square','#mock-q4')],
    },
    'A05': {
        'combines': ['A01','A06','A07','A20'],
        'families': [('adt-translation','../question-families/adt-translation-family.md'), ('codec','../question-families/codec-family.md')],
        'cross':    [('expr × maybe','../cross-matrix/expr-x-maybe.md'), ('tree × either','../cross-matrix/tree-x-either.md')],
        'theory':   [('expression tree','../trees/expression-tree.md')],
        'pitfalls': [('p-019','Mock Q5 p/q copy-paste'), ('p-016','functor shape break')],
        'qc':       [('codec attacks','../quickcheck/codec-attacks.md'), ('expr attacks','../quickcheck/expr-attacks.md')],
        'mock':     [('Q5 circuit','#mock-q5')],
    },
    'A06': {
        'combines': ['A01','A05','A22','A24'],
        'families': [('functor-instance','../question-families/functor-instance-family.md'), ('applicative-monad-instance','../question-families/applicative-monad-instance-family.md')],
        'cross':    [],
        'theory':   [('Functor typeclass','../typeclasses/functor.md'), ('tree functor','../trees/tree-functor.md')],
        'pitfalls': [('p-010','deriving Functor needs unsafe'), ('p-016','doesn\'t preserve shape')],
        'qc':       [('typeclass instance attacks','../quickcheck/typeclass-instance-attacks.md')],
        'mock':     [],
    },
    'A07': {
        'combines': ['A05','A12','A20'],
        'families': [('codec','../question-families/codec-family.md')],
        'cross':    [],
        'theory':   [],
        'pitfalls': [],
        'qc':       [('codec attacks','../quickcheck/codec-attacks.md')],
        'mock':     [],
    },
    'A08': {
        'combines': ['A01','A05','A14','A19'],
        'families': [('env-eval','../question-families/env-eval-family.md'), ('error-handling','../question-families/error-handling-family.md')],
        'cross':    [('expr × maybe','../cross-matrix/expr-x-maybe.md'), ('expr × state','../cross-matrix/expr-x-state.md')],
        'theory':   [('expr-reader interpreter','../interpreters/expr-reader.md'), ('expr-reader-either interpreter','../interpreters/expr-reader-either.md')],
        'pitfalls': [],
        'qc':       [('interp attacks','../quickcheck/interp-attacks.md'), ('maybe/either attacks','../quickcheck/maybe-either-attacks.md')],
        'mock':     [],
    },
    'A09': {
        'combines': ['A10','A21'],
        'families': [('list-rewrite','../question-families/list-rewrite-family.md')],
        'cross':    [],
        'theory':   [],
        'pitfalls': [('p-018','head/tail/!! without guard')],
        'qc':       [('lists attacks','../quickcheck/lists-attacks.md')],
        'mock':     [],
    },
    'A10': {
        'combines': ['A09','A21'],
        'families': [('list-fold','../question-families/list-fold-family.md')],
        'cross':    [('list × list-monad','../cross-matrix/list-x-list-monad.md')],
        'theory':   [],
        'pitfalls': [],
        'qc':       [('lists attacks','../quickcheck/lists-attacks.md')],
        'mock':     [],
    },
    'A11': {
        'combines': ['A01'],
        'families': [('bst-ops','../question-families/bst-ops-family.md')],
        'cross':    [('bst × state','../cross-matrix/bst-x-state.md'), ('bst × writer','../cross-matrix/bst-x-writer.md')],
        'theory':   [('BST','../trees/bst.md'), ('BST delete trace','../trees/bst-delete-trace.md')],
        'pitfalls': [('p-009','isBST Empty = False'), ('p-015','BST delete two-children'), ('p-020','three different isBST impls')],
        'qc':       [('bst attacks','../quickcheck/bst-attacks.md')],
        'mock':     [],
    },
    'A12': {
        'combines': ['A05','A07','A09'],
        'families': [('codec','../question-families/codec-family.md'), ('list-rewrite','../question-families/list-rewrite-family.md')],
        'cross':    [],
        'theory':   [],
        'pitfalls': [],
        'qc':       [('codec attacks','../quickcheck/codec-attacks.md')],
        'mock':     [],
    },
    'A13': {
        'combines': ['A05','A09'],
        'families': [('pretty-print','../question-families/pretty-print-family.md')],
        'cross':    [],
        'theory':   [('Show typeclass','../typeclasses/show.md')],
        'pitfalls': [('p-012','custom Show returns non-string')],
        'qc':       [('lists attacks','../quickcheck/lists-attacks.md')],
        'mock':     [],
    },
    'A14': {
        'combines': ['A08','A19','A15'],
        'families': [('env-eval','../question-families/env-eval-family.md'), ('error-handling','../question-families/error-handling-family.md'), ('writer-trace','../question-families/writer-trace-family.md')],
        'cross':    [('expr × multi','../cross-matrix/expr-x-multi.md')],
        'theory':   [('multi-effect interpreter','../interpreters/expr-multi-effect.md'), ('multi-effect monad','../monads/multi-effect.md'), ('transformer stack order','../monads/transformer-stack-order.md'), ('transformers','../monads/transformers.md')],
        'pitfalls': [],
        'qc':       [('interp attacks','../quickcheck/interp-attacks.md')],
        'mock':     [],
    },
    'A15': {
        'combines': ['A01','A02','A08','A14'],
        'families': [('writer-trace','../question-families/writer-trace-family.md')],
        'cross':    [('rose × writer','../cross-matrix/rose-x-writer.md'), ('tree × writer','../cross-matrix/tree-x-writer.md'), ('bst × writer','../cross-matrix/bst-x-writer.md'), ('list × writer','../cross-matrix/list-x-writer.md')],
        'theory':   [('Writer monad','../monads/writer.md')],
        'pitfalls': [],
        'qc':       [('writer attacks','../quickcheck/writer-attacks.md')],
        'mock':     [('Q2 (Writer variant)','#mock-q2')],
    },
    'A16': {
        'combines': ['A24','A08'],
        'families': [('parser','../question-families/parser-family.md')],
        'cross':    [],
        'theory':   [('parser overview','../interpreters/parser-overview.md'), ('chainl1 + backtracking','../interpreters/parser-chainl1.md')],
        'pitfalls': [],
        'qc':       [('interp attacks','../quickcheck/interp-attacks.md')],
        'mock':     [],
    },
    'A17': {
        'combines': ['A01','A06'],
        'families': [('tree-transform','../question-families/tree-transform-family.md')],
        'cross':    [],
        'theory':   [('tree zipper','../trees/tree-zipper.md')],
        'pitfalls': [],
        'qc':       [('trees attacks','../quickcheck/trees-attacks.md')],
        'mock':     [],
    },
    'A18': {
        'combines': ['A09'],
        'families': [('lazy-infinite','../question-families/lazy-infinite-family.md')],
        'cross':    [],
        'theory':   [],
        'pitfalls': [('p-023','deepseq exposes lazy undefined')],
        'qc':       [('lists attacks','../quickcheck/lists-attacks.md')],
        'mock':     [],
    },
    'A19': {
        'combines': ['A08','A14'],
        'families': [('env-eval','../question-families/env-eval-family.md'), ('error-handling','../question-families/error-handling-family.md')],
        'cross':    [('expr × multi','../cross-matrix/expr-x-multi.md'), ('expr × state','../cross-matrix/expr-x-state.md')],
        'theory':   [('extend interpreter','../interpreters/extend-interpreter.md')],
        'pitfalls': [],
        'qc':       [('interp attacks','../quickcheck/interp-attacks.md')],
        'mock':     [],
    },
    'A20': {
        'combines': ['A05','A06','A07'],
        'families': [('codec','../question-families/codec-family.md')],
        'cross':    [],
        'theory':   [('monad laws','../monads/monad-laws.md')],
        'pitfalls': [],
        'qc':       [('typeclass instance attacks','../quickcheck/typeclass-instance-attacks.md')],
        'mock':     [],
    },
    'A21': {
        'combines': ['A09','A10','A04'],
        'families': [('list-comp','../question-families/list-comp-family.md')],
        'cross':    [],
        'theory':   [],
        'pitfalls': [],
        'qc':       [('lists attacks','../quickcheck/lists-attacks.md')],
        'mock':     [],
    },
    'A22': {
        'combines': ['A06','A24'],
        'families': [('applicative-monad-instance','../question-families/applicative-monad-instance-family.md'), ('functor-instance','../question-families/functor-instance-family.md')],
        'cross':    [],
        'theory':   [('Monad typeclass','../typeclasses/monad.md'), ('Applicative typeclass','../typeclasses/applicative.md'), ('Functor typeclass','../typeclasses/functor.md')],
        'pitfalls': [],
        'qc':       [('typeclass instance attacks','../quickcheck/typeclass-instance-attacks.md')],
        'mock':     [],
    },
    'A23': {
        'combines': ['A02','A03'],
        'families': [('state-game','../question-families/state-game-family.md'), ('state-counter','../question-families/state-counter-family.md')],
        'cross':    [('game-state','../cross-matrix/game-state.md')],
        'theory':   [('State monad','../monads/state.md')],
        'pitfalls': [],
        'qc':       [('state attacks','../quickcheck/state-attacks.md')],
        'mock':     [],
    },
    'A24': {
        'combines': ['A03','A06','A22'],
        'families': [('applicative-monad-instance','../question-families/applicative-monad-instance-family.md')],
        'cross':    [],
        'theory':   [('Applicative typeclass','../typeclasses/applicative.md')],
        'pitfalls': [],
        'qc':       [('typeclass instance attacks','../quickcheck/typeclass-instance-attacks.md')],
        'mock':     [],
    },
}

def render(code, spec):
    lines = ['## See also', '']
    lines.append('**Combines with:** ' + ' · '.join(arch_link(c) for c in spec['combines']))
    if spec['families']:
        lines.append('**Question families:** ' + ' · '.join(f'[{n}]({p})' for n,p in spec['families']))
    if spec['cross']:
        lines.append('**Cross-topic:** ' + ' · '.join(f'[{n}]({p})' for n,p in spec['cross']))
    if spec['theory']:
        lines.append('**Theory:** ' + ' · '.join(f'[{n}]({p})' for n,p in spec['theory']))
    if spec['pitfalls']:
        lines.append('**Pitfalls:** ' + ' · '.join(f'[P-{pid[2:]} {desc}](../pitfalls/HIGH-severity.md#{pid})' for pid,desc in spec['pitfalls']))
    if spec['qc']:
        lines.append('**QuickCheck:** ' + ' · '.join(f'[{n}]({p})' for n,p in spec['qc']))
    if spec['mock']:
        lines.append('**Mock-Q:** ' + ' · '.join(f'[Mock {n}](../indexes/MOCK-Q-INDEX.md{anchor})' for n,anchor in spec['mock']))
    return '\n'.join(lines) + '\n'

def replace_seealso(text, new_block):
    pat = re.compile(r'## See also\b.*\Z', re.DOTALL)
    if pat.search(text):
        return pat.sub(new_block.rstrip() + '\n', text)
    return text.rstrip() + '\n\n' + new_block

def main():
    n = 0
    for code, spec in SEEALSO.items():
        f = ARCHETYPES / f'{code}-{ARCH_NAMES[code].replace(" / ","-").replace(" ","-")}.md'
        # Handle filename overrides
        if not f.exists():
            cands = list(ARCHETYPES.glob(f'{code}-*.md'))
            if not cands:
                print(f'MISS {code}: no file')
                continue
            f = cands[0]
        text = f.read_text(encoding='utf-8', newline='')
        block = render(code, spec)
        new = replace_seealso(text, block)
        if new != text:
            f.write_text(new, encoding='utf-8', newline='')
            n += 1
            print(f'OK   {code} -> {f.name}')
    print(f'\nTotal: {n} archetypes updated')

if __name__ == '__main__':
    main()
