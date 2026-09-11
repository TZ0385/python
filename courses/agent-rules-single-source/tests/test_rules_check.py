"""Contract tests for the agent rule-file consistency checker."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

import rules_check

COURSE_ROOT = Path(__file__).resolve().parent.parent
SCENARIO_ROOT = COURSE_ROOT / "scenario"

RICH_AGENTS = """# Agent rules

- Make the smallest change that satisfies the task contract.
- Run the test suite before declaring work finished.
- Never edit files outside the ones the contract names.
- Record what was not verified.
"""


class IsPointerTest(unittest.TestCase):
    def test_thin_pointer_that_references_agents_md_is_a_pointer(self) -> None:
        text = "This project keeps all agent rules in AGENTS.md.\nRead it first.\n"
        self.assertTrue(rules_check.is_pointer(text))

    def test_full_ruleset_is_not_a_pointer(self) -> None:
        lines = [f"- rule {i} restated here for agents" for i in range(12)]
        lines.append("See AGENTS.md for more.\n")
        self.assertFalse(rules_check.is_pointer("\n".join(lines)))

    def test_short_file_without_reference_is_not_a_pointer(self) -> None:
        self.assertFalse(rules_check.is_pointer("Be excellent to each other.\n"))


class CheckDirectoryTest(unittest.TestCase):
    def _tmp(self, files: dict[str, str]) -> Path:
        directory = Path(tempfile.mkdtemp(prefix="rules-"))
        self.addCleanup(shutil.rmtree, directory, ignore_errors=True)
        for name, text in files.items():
            (directory / name).write_text(text, encoding="utf-8")
        return directory

    def test_missing_agents_md_is_reported(self) -> None:
        report = rules_check.check_directory(
            self._tmp({"CLAUDE.md": "Some rules that live only here.\n" * 12})
        )
        self.assertFalse(report["ok"])
        self.assertTrue(
            any(e["status"] == "missing-source" for e in report["files"])
        )

    def test_thin_pointer_is_accepted(self) -> None:
        report = rules_check.check_directory(
            self._tmp(
                {
                    "AGENTS.md": RICH_AGENTS,
                    "CLAUDE.md": "All agent rules live in AGENTS.md.\n",
                }
            )
        )
        self.assertTrue(report["ok"])
        self.assertTrue(any(e["status"] == "pointer" for e in report["files"]))

    def test_exact_copy_is_accepted(self) -> None:
        report = rules_check.check_directory(
            self._tmp({"AGENTS.md": RICH_AGENTS, "CLAUDE.md": RICH_AGENTS})
        )
        self.assertTrue(report["ok"])
        self.assertTrue(any(e["status"] == "copy" for e in report["files"]))

    def test_diverged_file_is_flagged_with_reason(self) -> None:
        drifted = RICH_AGENTS + "- Always rewrite tests to match new behavior.\n"
        report = rules_check.check_directory(
            self._tmp({"AGENTS.md": RICH_AGENTS, ".cursorrules": drifted})
        )
        self.assertFalse(report["ok"])
        diverged = [e for e in report["files"] if e["status"] == "diverged"]
        self.assertEqual(len(diverged), 1)
        self.assertIn("differ from AGENTS.md", diverged[0]["issues"][0])

    def test_only_agents_md_is_ok(self) -> None:
        report = rules_check.check_directory(self._tmp({"AGENTS.md": RICH_AGENTS}))
        self.assertTrue(report["ok"])
        self.assertEqual(len(report["files"]), 1)


class MainTest(unittest.TestCase):
    def _copy(self, name: str) -> Path:
        target = Path(tempfile.mkdtemp(prefix="scenario-")) / name
        shutil.copytree(SCENARIO_ROOT / name, target)
        self.addCleanup(shutil.rmtree, target.parent, ignore_errors=True)
        return target

    def test_scenario_drifted_exits_nonzero(self) -> None:
        self.assertEqual(rules_check.main([str(self._copy("drifted"))]), 1)

    def test_scenario_single_copy_exits_zero(self) -> None:
        self.assertEqual(rules_check.main([str(self._copy("single-copy"))]), 0)

    def test_missing_argument_prints_usage(self) -> None:
        self.assertEqual(rules_check.main([]), 2)


if __name__ == "__main__":
    unittest.main()
