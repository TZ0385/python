"""Agent rule-file consistency checker (reviewed solution).

Enforces the single-source-of-truth contract: AGENTS.md must exist and be
non-empty, and every other recognized rule file (CLAUDE.md, .cursorrules)
must either be a thin pointer that defers to AGENTS.md or an exact copy of
it. Anything else is reported as drifted, with a reason. Standard library
only.
"""

from __future__ import annotations

import sys
from pathlib import Path

RULE_FILE_NAMES = ("AGENTS.md", "CLAUDE.md", ".cursorrules")
SOURCE_NAME = "AGENTS.md"
POINTER_MAX_LINES = 10


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
    non_empty = [line for line in text.splitlines() if line.strip()]
    references_source = any(SOURCE_NAME in line for line in non_empty)
    return len(non_empty) <= POINTER_MAX_LINES and references_source


def check_directory(directory: str | Path) -> dict:
    """Check the single-source contract for one repository directory."""
    files = load_rule_files(directory)
    entries: list[dict] = []

    source = files.get(SOURCE_NAME)
    if source is None or not source.strip():
        entries.append(
            {
                "file": SOURCE_NAME,
                "status": "missing-source",
                "issues": [f"{SOURCE_NAME} is missing or empty"],
            }
        )
    else:
        entries.append({"file": SOURCE_NAME, "status": "source", "issues": []})

    for name, text in files.items():
        if name == SOURCE_NAME:
            continue
        if is_pointer(text):
            entries.append({"file": name, "status": "pointer", "issues": []})
        elif source is not None and source.strip() and text.strip() == source.strip():
            entries.append({"file": name, "status": "copy", "issues": []})
        else:
            entries.append(
                {
                    "file": name,
                    "status": "diverged",
                    "issues": [
                        f"contains rules that differ from {SOURCE_NAME} "
                        "and is not a thin pointer"
                    ],
                }
            )

    allowed = {"source", "pointer", "copy"}
    ok = bool(entries) and all(entry["status"] in allowed for entry in entries)
    return {"source": SOURCE_NAME, "ok": ok, "files": entries}


def main(argv: list[str] | None = None) -> int:
    """Check one directory and print a one-line summary."""
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("usage: python rules_check.py <directory>", file=sys.stderr)
        return 2
    report = check_directory(arguments[0])
    diverged = sum(1 for entry in report["files"] if entry["status"] == "diverged")
    print(
        f"ok={report['ok']} files={len(report['files'])} diverged={diverged}"
    )
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
