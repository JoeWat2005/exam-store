<!-- topnav:start -->
> **Quick nav:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md)
<!-- topnav:end -->

# scripts/

Python 3 (standard library only) helpers for the examvault. Each script prints helpful results, not just a file list.

**For full examples with real output:** [SCRIPTS-GUIDE.md](SCRIPTS-GUIDE.md).

## Quick start

```bash
# bash / Git Bash / WSL
cd examvault/scripts
python search_by_type.py "Tree a -> Int"
python study_planner.py 5
```

```powershell
# Windows PowerShell
cd examvault\scripts
python search_by_type.py "Tree a -> Int"
python study_planner.py 5
```

All scripts resolve the vault root as `Path(__file__).resolve().parent.parent`. You can call them from anywhere.

## Available scripts

| Script | What it does | Example |
|---|---|---|
| `search_by_type.py` | Sig → archetypes + family + files | `python search_by_type.py "Monad m => m a -> (a -> m a) -> Int -> m [a]"` |
| `search_by_archetype.py` | A## or label → all files referencing it | `python search_by_archetype.py A02` |
| `search_by_keyword.py` | Keyword → file:line grep across the vault | `python search_by_keyword.py applyNTimes` |
| `search_by_monad.py` | Monad name → files + cross-matrix entries | `python search_by_monad.py State` |
| `search_by_combo.py` | "X + Y" → cross-matrix file + archetype combo | `python search_by_combo.py "Tree + State"` |
| `study_planner.py` | N days remaining → ranked daily plan | `python study_planner.py 7` |
| `topic_dependencies.py` | Topic → prerequisites + downstream | `python topic_dependencies.py Functor` |
| `mock_q_lookup.py` | Q1..Q5 / name → Mock spec + marker quirks | `python mock_q_lookup.py Q2` |
| `prelude_lookup.py` | Function name → sig + use + appearances | `python prelude_lookup.py mapM` |

## How they work

- All scripts use ONLY the Python standard library — no `pip install` needed.
- Searches go through `graphs/*.json` (parsed with `json`) and `.md` files (read with `Path.read_text(encoding='utf-8')`).
- For `search_by_keyword.py`, a pure-Python grep walks every `.md` file. No `rg` dependency.

## Customising

Each script has a `# CONFIG` section near the top — bump constants like `MAX_RESULTS` or extend the embedded dictionaries.

## See also

- `examvault/indexes/MASTER-INDEX.md` — directory layout for everything.
- `examvault/graphs/*.json` — the data the scripts read.

<!-- footernav:start -->

---
> **Back to:** [HOME](../HOME.md) · [NAVIGATION](../NAVIGATION.md) · [MASTER-INDEX](../indexes/MASTER-INDEX.md) · [^ top](#)
<!-- footernav:end -->
