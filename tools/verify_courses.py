#!/usr/bin/env python3
"""Verify every published course folder against the course contract.

Checks per course directory: COURSE.md and COURSE_cn.md exist, every English
lesson has a paired ``*_cn.md`` file (and vice versa), and the course's own
``verify.py`` reproduces the starter failure and passes the solution.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON_NAME = re.compile(r"^L\d{2,}\.md$")


def discover_courses(root: Path) -> list[Path]:
    courses_dir = root / "courses"
    if not courses_dir.exists():
        return []
    return sorted(path for path in courses_dir.iterdir() if path.is_dir())


def check_bilingual_contract(course: Path) -> list[str]:
    problems: list[str] = []
    name = course.name

    for required in ("COURSE.md", "COURSE_cn.md", "TASK.md", "TASK_cn.md", "REVIEW.md", "verify.py"):
        if not (course / required).exists():
            problems.append(f"{name}: missing {required}")

    lessons_dir = course / "lessons"
    if not lessons_dir.is_dir():
        problems.append(f"{name}: missing lessons/ directory")
        return problems

    english = {path.name.removesuffix(".md") for path in lessons_dir.iterdir() if LESSON_NAME.fullmatch(path.name)}
    chinese_stems = {
        path.name.removesuffix("_cn.md")
        for path in lessons_dir.iterdir()
        if path.name.endswith("_cn.md")
    }

    missing_pairs = sorted(english - chinese_stems)
    orphan_chinese = sorted(chinese_stems - english)
    if missing_pairs:
        problems.append(f"{name}: lessons without _cn.md pair: {', '.join(missing_pairs)}")
    if orphan_chinese:
        problems.append(f"{name}: _cn.md lessons without English pair: {', '.join(orphan_chinese)}")
    if not english:
        problems.append(f"{name}: lessons/ contains no L*.md lessons")
    return problems


def run_course_verifier(course: Path) -> list[str]:
    name = course.name
    verify = course / "verify.py"
    if not verify.exists():
        return []  # Already reported by the contract check.
    commands = (
        [sys.executable, str(verify), "starter", "--expect-failure"],
        [sys.executable, str(verify), "solution"],
    )
    problems: list[str] = []
    for command in commands:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        if result.returncode != 0:
            problems.append(
                f"{name}: verification failed: {' '.join(command[2:])}"
                f"\n{(result.stdout or '') + (result.stderr or '')}".rstrip()
            )
    problems.extend(check_progress_contract(course))
    return problems


def check_progress_contract(course: Path) -> list[str]:
    """FP-415: the progress subcommand must be deterministic and well-shaped.

    Runs ``verify.py progress --json`` twice and requires identical output,
    a valid document, five checkpoints (l01..l05), and well-formed claim
    codes wherever one is printed.
    """

    verify = course / "verify.py"
    if not verify.exists():
        return []
    name = course.name
    runs: list[str] = []
    for _ in range(2):
        result = subprocess.run(
            [sys.executable, str(verify), "progress", "--json"],
            check=False, capture_output=True, text=True,
        )
        if result.returncode != 0:
            return [f"{name}: progress failed\n{(result.stdout or '') + (result.stderr or '')}".rstrip()]
        runs.append(result.stdout)
    if runs[0] != runs[1]:
        return [f"{name}: progress output is not deterministic between runs"]
    try:
        document = json.loads(runs[0])
    except ValueError:
        return [f"{name}: progress --json did not emit valid JSON"]

    problems: list[str] = []
    for key in ("course", "starter_suite_passed", "solution_suite_passed", "checkpoints"):
        if key not in document:
            problems.append(f"{name}: progress document missing {key!r}")
    checkpoints = document.get("checkpoints")
    if not isinstance(checkpoints, list) or len(checkpoints) != 5:
        problems.append(f"{name}: progress must list exactly five checkpoints")
        return problems
    expected_ids = [f"l0{index}" for index in range(1, 6)]
    if [item.get("id") for item in checkpoints] != expected_ids:
        problems.append(f"{name}: checkpoint ids must be {expected_ids}")
    for item in checkpoints:
        code = item.get("claim_code")
        if code is not None and not re.fullmatch(r"[A-Z2-7]{8}", str(code)):
            problems.append(f"{name}: malformed claim code for {item.get('id')}: {code!r}")
    return problems


def main() -> int:
    courses = discover_courses(ROOT)
    if not courses:
        print("error: no course folders found under courses/*/", file=sys.stderr)
        return 1

    problems: list[str] = []
    for course in courses:
        problems.extend(check_bilingual_contract(course))
        problems.extend(run_course_verifier(course))

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print(f"all {len(courses)} course folder(s) satisfy the course contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
