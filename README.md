# Functional programming exam vault

A cross-linked Markdown vault of Haskell revision notes for a functional programming exam, with Python search scripts and a script that drafts code notes with a local language model.

## Context

Revision material I built for the Functional Programming module at the University of Birmingham (2025/26). The vault organises the course around recurring question types, which it calls archetypes, and their variations, so that any topic can be looked up by question type, subject or type signature.

## Contents

- 24 question archetypes (`A01` to `A24`), each with recognition cues, a template, variations, worked examples, QuickCheck edge cases and pitfalls
- Question families that list many variations of each archetype
- Topic notes on trees, monads, interpreters and parsers, and type classes
- Pages on combining a data structure with an effect, such as a tree with the State monad
- Short refresher pages on Haskell basics, GHC error messages and GHCi commands
- Edge cases that QuickCheck tests tend to hit, by topic, and common mistakes ranked by severity
- Indexes for looking things up by keyword, type signature, Prelude function, lecture or practice problem
- Checklists and time plans for exam day
- JSON graphs of topics, archetypes and their dependencies, used by the search scripts
- Python scripts for searching the vault and planning revision
- A note generator that drafts Haskell code from type signatures using a local language model
- Rough practice code in `revision/`

## Tech stack

- Markdown with relative links, readable on GitHub or in any Markdown viewer
- Python 3, standard library only, for the scripts
- Bash for the vLab setup script and the note generator
- A llamafile, a single executable that bundles a language model with its runtime, stored with Git LFS
- Haskell code throughout the notes. According to `examvault/meta/FINAL-SWEEP-REPORT.md`, code changed in the vault's final review was compiled with GHC 9.6.7 and `-XSafe`.

## Building and running

There's nothing to build. Start with `examvault/README.md` or `examvault/HOME.md`. Every content page links back to these and to the master index.

### Search scripts

The scripts need Python 3 and nothing else. These examples come from `examvault/scripts/commands.txt`:

```sh
cd examvault/scripts
python3 search_by_type.py "Tree a -> Int"
python3 search_by_archetype.py A02
python3 search_by_keyword.py foldr
python3 search_by_monad.py State
python3 search_by_combo.py "Tree + State"
python3 prelude_lookup.py mapM
python3 topic_dependencies.py Functor
python3 study_planner.py 7
```

On Windows, use `py -3` instead of `python3`.

| Script | What it does |
| --- | --- |
| `search_by_type.py` | Finds the archetype, question family and pages that match a type signature |
| `search_by_archetype.py` | Shows an archetype's tier, main pages, related archetypes and where it's mentioned |
| `search_by_keyword.py` | Searches every Markdown file for a keyword and prints file and line |
| `search_by_monad.py` | Lists the pages about a monad, including the combination pages |
| `search_by_combo.py` | Finds the page for a combination such as `"Tree + State"` |
| `prelude_lookup.py` | Shows a Prelude function's signature, use and appearances in the vault |
| `topic_dependencies.py` | Shows a topic's prerequisites and the topics that build on it |
| `study_planner.py` | Prints a ranked revision plan for a given number of days |
| `mock_q_lookup.py` | Looks up the vault's notes on each mock test question |

`examvault/scripts/SCRIPTS-GUIDE.md` has worked examples with output for each script.

### vLab setup

`vlab-setup.sh` makes JupyterLab on the university's vLab open Markdown files in preview mode, so the links are clickable. Run it once, then refresh the browser tab:

```sh
bash examvault/scripts/vlab-setup.sh
```

### Note generator

`examvault/scripts/notes.sh` reads `notes.txt` at the root of the repository. Each line holds a Haskell type signature and a description of the function, separated by ` - `. For each line, the script asks the model in `examvault/models/gen.llamafile` to write the code, then writes all the results to `examvault/NOTES.md`, replacing what was there.

You need Git LFS to download the model file, which is about 940 MB. The script uses absolute paths under `/jupyter/work/exam-store`, so it only works from a clone at that location, and it exits without doing anything if `notes.txt` or the model is missing. The command, as listed in `commands.txt`, is:

```sh
bash /jupyter/work/exam-store/examvault/scripts/notes.sh
```

## How it works

- **Organisation.** `examvault/ARCHITECTURE.md` describes four axes for finding a page: question archetype, variation (the vault calls these mutations), topic and type signature. Archetype and question-family pages share a common layout, and the files in `examvault/indexes/` cross-reference pages along each axis.
- **Navigation.** Content pages carry a breadcrumb, links to their sibling pages, and links to the home page, the navigation page and the master index. Maintenance scripts in `examvault/scripts/` whose names start with `_phase` generated these blocks and the "See also" sections. Others generated the Haskell basics pages and added variations to the question families, and `_phase9_link_check.py` checks for broken internal links.
- **Search scripts.** The scripts read the JSON graphs in `examvault/graphs/` and the Markdown files directly. Each one finds the vault from its own location, so it can be run from any directory.
- **Note generator.** `notes.sh` wraps each line of `notes.txt` in a ChatML prompt and runs the llamafile in command-line mode at temperature 0, with a limit of 96 generated tokens. It then strips chat markers and stray prose from the output, keeps up to 20 lines of code, and adds the code to `NOTES.md` under a heading for the signature.

## Notes

- Some pages refer to files in the module's own course repository (`fp-learning-2025`), which isn't included here.
- The files in `revision/` are rough practice snippets rather than complete modules, and some won't compile as they are. For example, `revision/statemonad.hs` uses `State` without importing `Control.Monad.State`.

## Project structure

```text
exam-store/
├── .gitattributes        # LF line endings, and Git LFS for *.llamafile
├── commands.txt          # vLab commands for the setup script and the note generator
├── notes.txt             # input for the note generator
├── revision/             # rough Haskell practice files
└── examvault/
    ├── README.md         # entry point and directory map
    ├── HOME.md           # guided tour
    ├── HOW-TO-USE.md     # the lookup workflow
    ├── ARCHITECTURE.md   # how the vault is organised
    ├── archetypes/       # question types A01 to A24
    ├── question-families/
    ├── trees/            # binary trees, BSTs, rose trees, expression trees
    ├── monads/           # Maybe, Either, State, Writer, Reader, IO, list, transformers
    ├── interpreters/     # expression evaluators and parsers
    ├── typeclasses/      # Functor, Applicative, Monad, Foldable, Traversable and others
    ├── cross-matrix/     # data structure and effect combinations
    ├── haskell-basics/   # refresher pages
    ├── quickcheck/       # edge cases by topic
    ├── pitfalls/         # common mistakes by severity
    ├── indexes/          # cross-indexes
    ├── exam-day/         # exam-day checklists and plans
    ├── graphs/           # JSON knowledge graphs
    ├── meta/             # course coverage map, audits and build reports
    ├── models/           # gen.llamafile (Git LFS)
    └── scripts/          # search scripts, vlab-setup.sh, notes.sh and _phase maintenance scripts
```
