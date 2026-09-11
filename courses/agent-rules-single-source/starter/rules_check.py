"""Agent rule-file consistency checker (starter, deliberately incomplete).

Checks one repository directory for the "single source of truth" contract:
AGENTS.md exists and every other rule file (CLAUDE.md, .cursorrules) either
is a thin pointer to it or an exact copy. This starter reproduces the naive
state: it assumes everything is fine, never requires AGENTS.md, and cannot
detect pointer, copy, or drifted files. ../TASK.md defines the contract.
"""

from __future__ import annotations

import sys
from pathlib import Path

RULE_FILE_NAMES = ("AGENTS.md", "CLAUDE.md", ".cursorrules")


def load_rule_files(directory: str | Path) -> dict[str, str]:
    """Return the text of every present rule file in *directory*."""
    directory = Path(directory)
    files: dict[str, str] = {}
    for name in RULE_FILE_NAMES:
        path = directory / name
        if path.is_file():
            files[name] = path.read_text(encoding="utf-8")
    return files


def is_pointer(text: str) -> bool:
    """A thin pointer file defers to AGENTS.md instead of restating rules."""
    return False


def check_directory(directory: str | Path) -> dict:
    """Check the single-source contract for one repository directory."""
    files = load_rule_files(directory)
    entries = []
    for name, _text in files.items():
        entries.append({"file": name, "status": "ok", "issues": []})
    return {"source": "AGENTS.md", "ok": True, "files": entries}


def main(argv: list[str] | None = None) -> int:
    """Check one directory and print a one-line summary."""
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("usage: python rules_check.py <directory>", file=sys.stderr)
        return 2
    report = check_directory(arguments[0])
    print(f"ok={report['ok']} files={len(report['files'])} diverged=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
