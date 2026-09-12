#!/usr/bin/env python3
"""Run the course contract against starter or solution.

Objective completion evidence for "Exploratory data analysis" (da-eda).
Exit 0 means the selected implementation satisfies the task contract;
``--expect-failure`` reproduces the unfinished starter state and checks
that the failing tests are the intended ones. ``progress`` prints the
checkpoint claim codes for recording on flypython.com.

Dependencies (pandas) are managed with uv — run ``uv sync`` (or
``pip install -r requirements.txt``) inside this folder first.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXPECTED_STARTER_FAILURES = (
    "test_load_returns_dataframe",
    "test_load_has_expected_columns",
    "test_removes_exact_duplicates",
    "test_counts_bad_amounts",
    "test_counts_bad_dates",
    "test_clean_row_count",
    "test_clean_has_no_unparsed_amounts",
    "test_total_revenue",
    "test_revenue_by_region",
    "test_top_category",
    "test_date_range",
    "test_main_writes_results_json",
)

COURSE_ID = 'course-da-eda'
# Documented constant: claim codes derive deterministically from
# (COURSE_ID, checkpoint_id, COURSE_SALT). They are spot-checkable
# self-reported evidence, not tamper-proof secrets — see
# docs/repo-plan-0.0.4.md FP-411.
COURSE_SALT = 'e2a7c019f4d3b5aa'

CHECKPOINTS = [
    {"id": "l01", "gate": "attest", "title": 'What messy data looks like'},
    {"id": "l02", "gate": "attest", "title": 'Define the answer first'},
    {"id": "l03", "gate": "starter-suite", "title": 'Clean and summarize'},
    {"id": "l04", "gate": "both-suites", "title": 'Check against ground truth'},
    {"id": "l05", "gate": "attest", "title": 'Run it on your own data'},
]


def _deps_available():
    return importlib.util.find_spec("pandas") is not None


def _deps_hint():
    print(
        "pandas is not installed. Run `uv sync` (or "
        "`pip install -r requirements.txt`) inside this course folder first.",
        file=sys.stderr,
    )


def _claim_code(checkpoint_id):
    digest = hashlib.sha256(
        (COURSE_ID + ":" + checkpoint_id + ":" + COURSE_SALT).encode("utf-8")
    ).digest()
    return base64.b32encode(digest).decode("ascii")[:8]


def _run_suite(implementation):
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / implementation)
    return subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests")],
        env=environment, check=False, capture_output=True, text=True,
    )


def run_progress(as_json):
    if not _deps_available():
        _deps_hint()
        starter_ok = solution_ok = False
    else:
        starter = _run_suite("starter")
        solution = _run_suite("solution")
        starter_ok = starter.returncode == 0
        solution_ok = solution.returncode == 0
    rows = []
    for checkpoint in CHECKPOINTS:
        gate = checkpoint["gate"]
        if gate == "attest":
            status, kind = "attest", "attested"
        elif gate == "starter-suite":
            status = "passed" if starter_ok else "open"
            kind = "objective"
        else:
            status = "passed" if (starter_ok and solution_ok) else "open"
            kind = "objective"
        code = _claim_code(checkpoint["id"]) if status in ("passed", "attest") else None
        row = dict(checkpoint)
        row["status"] = status
        row["kind"] = kind
        row["claim_code"] = code
        rows.append(row)
    if as_json:
        print(json.dumps({"course": COURSE_ID,
            "starter_suite_passed": starter_ok,
            "solution_suite_passed": solution_ok,
            "checkpoints": rows}, ensure_ascii=False, indent=2))
    else:
        starter_state = "passed" if starter_ok else "not passed"
        solution_state = "passed" if solution_ok else "not passed"
        print("Course " + COURSE_ID)
        print("Suites: starter " + starter_state + " / solution " + solution_state)
        for row in rows:
            state = row["status"] + (" (self-attested)" if row["kind"] == "attested" else "")
            code = "claim " + row["claim_code"] if row["claim_code"] else "—"
            print("  " + row["id"] + "  " + row["title"] + "  [" + state + "]  " + code)
        print("Claim codes are self-reported evidence recorded on flypython.com — never a certificate.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("implementation", choices=("progress", "starter", "solution"))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--expect-failure", action="store_true")
    args = parser.parse_args()

    if args.implementation == "progress":
        return run_progress(args.json)

    if not _deps_available():
        _deps_hint()
        return 1

    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / args.implementation)
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests")],
        env=environment, check=False, capture_output=True, text=True,
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
            "Expected starter state reproduced: all contract tests fail "
            "because the analysis functions are not implemented."
        )
        return 0
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
