#!/usr/bin/env python3
"""Run the course contract against starter or solution.

Objective completion evidence for "One source of truth for agent rules".
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXPECTED_STARTER_FAILURES = (
    "test_thin_pointer_that_references_agents_md_is_a_pointer",
    "test_missing_agents_md_is_reported",
    "test_thin_pointer_is_accepted",
    "test_exact_copy_is_accepted",
    "test_diverged_file_is_flagged_with_reason",
    "test_scenario_drifted_exits_nonzero",
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
            "Expected starter state reproduced: no pointer detection, no source "
            "requirement, no drift reporting, and CLI exit codes never signal failure."
        )
        return 0
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
