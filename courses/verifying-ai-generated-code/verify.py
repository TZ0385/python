#!/usr/bin/env python3
"""Run the course contract against starter or solution.

Objective completion evidence for "Verifying AI-generated code before it
ships".
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
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



COURSE_ID = 'course-verify-ship'
# Documented constant: claim codes derive deterministically from
# (COURSE_ID, checkpoint_id, COURSE_SALT). They are spot-checkable
# self-reported evidence, not tamper-proof secrets — see
# docs/repo-plan-0.0.4.md FP-411.
COURSE_SALT = '8d11b8f902b1a109'

CHECKPOINTS = [
    {"id": "l01", "gate": "attest", "title": '「能跑」不是证据 / It runs is not evidence'},
    {"id": "l02", "gate": "attest", "title": '定义发布记录 / Define the release record'},
    {"id": "l03", "gate": "starter-suite", "title": '构建 ship check / Build the ship check'},
    {"id": "l04", "gate": "both-suites", "title": '像怀疑者一样读记录 / Read the record like a skeptic'},
    {"id": "l05", "gate": "attest", "title": '发布门禁 / Gate your next release'},
]

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
        starter_state = "通过" if starter_ok else "未通过"
        solution_state = "通过" if solution_ok else "未通过"
        print("课程 " + COURSE_ID)
        print("实现状态: starter " + starter_state + " / solution " + solution_state)
        for row in rows:
            state = row["status"] + ("（自报）" if row["kind"] == "attested" else "")
            code = "认领码 " + row["claim_code"] if row["claim_code"] else "—"
            print("  " + row["id"] + "  " + row["title"] + "  [" + state + "]  " + code)
        print("认领码是自我报告的证据，在 flypython.com 记录；绝非证书。")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("implementation", choices=("progress", "starter", "solution"))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--expect-failure", action="store_true")
    args = parser.parse_args()

    if args.implementation == "progress":
        return run_progress(args.json)

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
