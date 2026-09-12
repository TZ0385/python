# Task contract: agent rule-file consistency checker

Change only `starter/rules_check.py`. Standard library only.

- `load_rule_files(directory) -> dict[str, str]`: read the text of every
  present rule file among `AGENTS.md`, `CLAUDE.md`, `.cursorrules`.
- `is_pointer(text) -> bool`: true when the file is a thin pointer — at most
  10 non-empty lines and at least one line referencing `AGENTS.md`.
- `check_directory(directory) -> dict` returning
  `{"source": "AGENTS.md", "ok": bool, "files": [...]}`:
  - `AGENTS.md` missing or empty produces a `missing-source` entry and
    `ok=False`.
  - A present, non-empty `AGENTS.md` produces a `source` entry.
  - Every other rule file is classified: `pointer` (thin pointer),
    `copy` (exact match of `AGENTS.md` content), or `diverged` (anything
    else), each with an `issues` list; `diverged` entries carry a reason
    naming the difference from `AGENTS.md`.
  - `ok=True` only when every entry is `source`, `pointer`, or `copy`.
- `main(argv=None) -> int`:
  - Exactly one argument (the directory). Otherwise print usage to stderr
    and return 2.
  - Print `ok=... files=... diverged=...` to stdout; return 0 when `ok`,
    otherwise 1.

Done means `python verify.py starter` exits 0 with all eleven tests passing.
