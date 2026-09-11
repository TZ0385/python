"""Release-evidence builder for AI-written Python (starter, incomplete).

Runs a project's checks and writes a delivery record: the exact command,
its exit code, the parsed test count and outcome, an honest "unverified"
list, and an all_passed verdict. This starter reproduces the naive state:
it records only exit codes (so a project with no tests counts as passing),
never parses results, drops the unverified list, and writes non-atomically.
../TASK.md defines the contract.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

DEFAULT_COMMAND = ["-m", "unittest", "discover", "-s", "tests"]
RECORD_NAME = "SHIP-RECORD.json"


def run_checks(command: list[str], cwd: str | Path) -> dict:
    """Run *command* (python arguments) in *cwd* and record the evidence."""
    full = [sys.executable, *command]
    result = subprocess.run(full, cwd=str(cwd), capture_output=True, text=True)
    return {"command": " ".join(command), "exit_code": result.returncode}


def build_record(
    checks: list[dict],
    *,
    verified_on: str,
    unverified: list[str] | None = None,
) -> dict:
    """Assemble the delivery record from check evidence."""
    return {
        "verified_on": verified_on,
        "checks": checks,
        "all_passed": all(check["exit_code"] == 0 for check in checks),
    }


def write_record(record: dict, destination: str | Path) -> None:
    """Write the record as JSON to *destination*."""
    Path(destination).write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def run_project(project_dir: str | Path, *, verified_on: str) -> dict:
    """Read ship.json, run the checks, write SHIP-RECORD.json, return it."""
    directory = Path(project_dir)
    config = json.loads((directory / "ship.json").read_text(encoding="utf-8"))
    command = config.get("command", DEFAULT_COMMAND)
    check = run_checks(command, directory)
    record = build_record(
        [check],
        verified_on=verified_on,
        unverified=config.get("unverified"),
    )
    write_record(record, directory / RECORD_NAME)
    return record


def main(argv: list[str] | None = None) -> int:
    """Build the delivery record for one project directory."""
    arguments = sys.argv[1:] if argv is None else argv
    if not arguments or len(arguments) > 3:
        print(
            "usage: python ship_check.py <project-dir> [--verified-on YYYY-MM-DD]",
            file=sys.stderr,
        )
        return 2
    project = arguments[0]
    verified_on = date.today().isoformat()
    if len(arguments) == 3 and arguments[1] == "--verified-on":
        verified_on = arguments[2]
    record = run_project(project, verified_on=verified_on)
    print(f"all_passed={record['all_passed']} checks={len(record['checks'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
