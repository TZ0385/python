#!/usr/bin/env python3
"""Run the course contract against starter or solution.

Objective completion evidence for
"Hands-on Python with Claude Code". Exit 0 means the selected implementation
satisfies the task contract; ``--expect-failure`` reproduces the unfinished
starter state and checks that the failing tests are the intended ones.
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
    "test_load_json_records_returns_list_of_dicts",
    "test_unsupported_suffix_raises_value_error",
    "test_invalid_records_are_isolated_with_reasons",
    "test_group_totals_are_rounded_to_two_decimals",
    "test_write_report_creates_missing_parent_directories",
    "test_run_scenario_writes_report_file",
    "test_main_prints_summary_and_returns_zero",
)



COURSE_ID = 'course-claude-code'
# Documented constant: claim codes derive deterministically from
# (COURSE_ID, checkpoint_id, COURSE_SALT). They are spot-checkable
# self-reported evidence, not tamper-proof secrets — see
# docs/repo-plan-0.0.4.md FP-411.
COURSE_SALT = 'a54f3ce504534d68'

CHECKPOINTS = [
    {"id": "l01", "gate": "attest", "title": '复现故障 / Reproduce the failure'},
    {"id": "l02", "gate": "attest", "title": '任务契约 / Task contract'},
    {"id": "l03", "gate": "starter-suite", "title": '边界修改，按测试推进 / Bounded change, test by test'},
    {"id": "l04", "gate": "both-suites", "title": '验证与审查 / Verify and review'},
    {"id": "l05", "gate": "attest", "title": '应用到自己的项目 / Apply to your project'},
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
