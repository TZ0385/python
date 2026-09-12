#!/usr/bin/env python3
"""Run the course contract against starter or solution.

Objective completion evidence for "One source of truth for agent rules".
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
    "test_thin_pointer_that_references_agents_md_is_a_pointer",
    "test_missing_agents_md_is_reported",
    "test_thin_pointer_is_accepted",
    "test_exact_copy_is_accepted",
    "test_diverged_file_is_flagged_with_reason",
    "test_scenario_drifted_exits_nonzero",
)



COURSE_ID = 'course-agent-rules'
# Documented constant: claim codes derive deterministically from
# (COURSE_ID, checkpoint_id, COURSE_SALT). They are spot-checkable
# self-reported evidence, not tamper-proof secrets — see
# docs/repo-plan-0.0.4.md FP-411.
COURSE_SALT = '3af23393e1911a4a'

CHECKPOINTS = [
    {"id": "l01", "gate": "attest", "title": '量化漂移 / Measure the drift'},
    {"id": "l02", "gate": "attest", "title": '确定唯一真源 / Decide the source of truth'},
    {"id": "l03", "gate": "starter-suite", "title": '有边界的变更 / Bounded change'},
    {"id": "l04", "gate": "both-suites", "title": '验证并接入流程 / Verify and wire it in'},
    {"id": "l05", "gate": "attest", "title": '应用到你的仓库 / Apply to your repository'},
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
            "Expected starter state reproduced: no pointer detection, no source "
            "requirement, no drift reporting, and CLI exit codes never signal failure."
        )
        return 0
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
