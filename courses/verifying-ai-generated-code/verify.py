#!/usr/bin/env python3
"""Run the course contract against starter or solution.

Objective completion evidence for "Verifying AI-generated code before it
ships".
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXPECTED_STARTER_FAILURES = (
    "test_green_project_produces_ok_check",
    "test_failing_project_is_failed",
    "test_no_tests_project_is_no_tests",
    "test_no_tests_never_counts_as_passed",
    "test_record_carries_the_unverified_list",
    "test_write_record_is_atomic_and_creates_parents",
    "test_red_project_exits_nonzero",
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
        missing = [name for name in EXPECTED_STARTER_FAILURES if name not in output]
        if missing:
            print(
                "Starter failed for unexpected reasons; missing expected failures:",
                file=sys.stderr,
            )
            print("\n".join(missing), file=sys.stderr)
            print(output, file=sys.stderr)
            return 1
        print(
            "Expected starter state reproduced: exit codes only, no parsed "
            "results, no-tests projects blessed, no unverified list, and "
            "non-atomic records."
        )
        return 0
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
