"""Release-evidence builder for AI-written Python (reviewed solution).

Runs a project's checks and writes a delivery record with the exact command,
its exit code, the parsed test count and outcome, the honest "unverified"
list, and an all_passed verdict that refuses to bless zero-test projects.
Writes are atomic so an interrupted run cannot leave a half-written record.
Standard library only.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

DEFAULT_COMMAND = ["-m", "unittest", "discover", "-s", "tests"]
RECORD_NAME = "SHIP-RECORD.json"
RAN_PATTERN = re.compile(r"^Ran (\d+) tests? in ", re.MULTILINE)


def run_checks(command: list[str], cwd: str | Path) -> dict:
    """Run *command* (python arguments) in *cwd* and record the evidence."""
    full = [sys.executable, *command]
    result = subprocess.run(full, cwd=str(cwd), capture_output=True, text=True)
    output = (result.stdout or "") + (result.stderr or "")
    match = RAN_PATTERN.search(output)
    ran = int(match.group(1)) if match else 0
    # "NO TESTS RAN" exits nonzero on modern Pythons; absence of tests is
    # its own verdict, not a crash, so it is classified before exit codes.
    if ran == 0:
        outcome = "no-tests"
    elif result.returncode != 0:
        outcome = "failed"
    else:
        outcome = "ok"
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "ran": ran,
        "result": outcome,
    }


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
        "all_passed": all(
            check["exit_code"] == 0 and check["result"] == "ok" for check in checks
        ),
        "unverified": list(unverified or []),
    }


def write_record(record: dict, destination: str | Path) -> None:
    """Atomically write the record as JSON, creating parent directories."""
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp")
    temporary.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, target)


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
    return 0 if record["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
