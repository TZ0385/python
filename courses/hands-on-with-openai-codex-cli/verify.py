#!/usr/bin/env python3
"""Run the course contract against starter or solution.

Objective completion evidence for
"Hands-on with OpenAI Codex CLI". Exit 0 means the selected implementation
satisfies the task contract; ``--expect-failure`` reproduces the unfinished
starter state and checks that the failing tests are the intended ones.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXPECTED_STARTER_FAILURES = (
    "test_load_json_records_returns_list_of_dicts",
    "test_unsupported_suffix_raises_value_error",
    "test_invalid_records_are_isolated_with_reasons",
    "test_group_totals_are_rounded_to_two_decimals",
    "test_write_report_creates_missing_parent_directories",
    "test_run_scenario_writes_report_file",
    "test_main_prints_summary_and_returns_zero",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("implementation", choices=("starter", "solution"))
    parser.add_argument("--expect-failure", action="store_true")
    args = parser.parse_args()

    command = [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests")]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / args.implementation)
    result = subprocess.run(
        command, env=environment, check=False, capture_output=True, text=True
    )

    if args.expect_failure:
        if result.returncode == 0:
            print("Expected the starter to fail, but it passed.", file=sys.stderr)
            return 1
        output = (result.stdout or "") + (result.stderr or "")
        missing = [
            name for name in EXPECTED_STARTER_FAILURES if name not in output
        ]
        if missing:
            print(
                "Starter failed for unexpected reasons; missing expected failures:",
                file=sys.stderr,
            )
            print("\n".join(missing), file=sys.stderr)
            print(output, file=sys.stderr)
            return 1
        print(
            "Expected starter state reproduced: JSON inputs crash, invalid rows "
            "abort the run, totals are unrounded, and reports need an existing "
            "directory."
        )
        return 0
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
