"""Contract tests for the release-evidence builder."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import ship_check

COURSE_ROOT = Path(__file__).resolve().parent.parent
SCENARIO_ROOT = COURSE_ROOT / "scenario"


class RunChecksTest(unittest.TestCase):
    def test_green_project_produces_ok_check(self) -> None:
        check = ship_check.run_checks(
            ["-m", "unittest", "discover", "-s", "tests"], SCENARIO_ROOT / "green-project"
        )
        self.assertEqual(check["exit_code"], 0)
        self.assertEqual(check["ran"], 2)
        self.assertEqual(check["result"], "ok")

    def test_failing_project_is_failed(self) -> None:
        check = ship_check.run_checks(
            ["-m", "unittest", "discover", "-s", "tests"], SCENARIO_ROOT / "red-project"
        )
        self.assertNotEqual(check["exit_code"], 0)
        self.assertEqual(check["ran"], 2)
        self.assertEqual(check["result"], "failed")

    def test_no_tests_project_is_no_tests(self) -> None:
        check = ship_check.run_checks(
            ["-m", "unittest", "discover", "-s", "tests"], SCENARIO_ROOT / "no-tests"
        )
        self.assertEqual(check["ran"], 0)
        self.assertEqual(check["result"], "no-tests")


class BuildRecordTest(unittest.TestCase):
    def test_no_tests_never_counts_as_passed(self) -> None:
        record = ship_check.build_record(
            [{"command": "-m unittest", "exit_code": 0, "ran": 0, "result": "no-tests"}],
            verified_on="2026-09-12",
        )
        self.assertFalse(record["all_passed"])

    def test_record_carries_the_unverified_list(self) -> None:
        record = ship_check.build_record(
            [{"command": "-m unittest", "exit_code": 0, "ran": 2, "result": "ok"}],
            verified_on="2026-09-12",
            unverified=["production data volume", "upstream API schema stability"],
        )
        self.assertEqual(
            record["unverified"],
            ["production data volume", "upstream API schema stability"],
        )

    def test_all_passed_requires_every_check_ok(self) -> None:
        record = ship_check.build_record(
            [
                {"command": "a", "exit_code": 0, "ran": 2, "result": "ok"},
                {"command": "b", "exit_code": 1, "ran": 2, "result": "failed"},
            ],
            verified_on="2026-09-12",
        )
        self.assertFalse(record["all_passed"])


class WriteRecordTest(unittest.TestCase):
    def test_write_record_is_atomic_and_creates_parents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "evidence" / "SHIP-RECORD.json"
            ship_check.write_record({"verified_on": "2026-09-12"}, destination)
            self.assertTrue(destination.exists())
            self.assertFalse(destination.with_name(destination.name + ".tmp").exists())
            self.assertEqual(
                json.loads(destination.read_text(encoding="utf-8"))["verified_on"],
                "2026-09-12",
            )


class RunProjectTest(unittest.TestCase):
    def _copy(self, name: str) -> Path:
        target = Path(tempfile.mkdtemp(prefix="project-")) / name
        shutil.copytree(SCENARIO_ROOT / name, target)
        self.addCleanup(shutil.rmtree, target.parent, ignore_errors=True)
        return target

    def test_green_project_record_and_exit_code(self) -> None:
        project = self._copy("green-project")
        record = ship_check.run_project(project, verified_on="2026-09-12")
        written = json.loads((project / "SHIP-RECORD.json").read_text(encoding="utf-8"))
        self.assertEqual(written, record)
        self.assertTrue(record["all_passed"])
        self.assertEqual(ship_check.main([str(project), "--verified-on", "2026-09-12"]), 0)

    def test_red_project_exits_nonzero(self) -> None:
        project = self._copy("red-project")
        self.assertEqual(ship_check.main([str(project), "--verified-on", "2026-09-12"]), 1)
        written = json.loads((project / "SHIP-RECORD.json").read_text(encoding="utf-8"))
        self.assertFalse(written["all_passed"])

    def test_missing_argument_prints_usage(self) -> None:
        self.assertEqual(ship_check.main([]), 2)


if __name__ == "__main__":
    unittest.main()
