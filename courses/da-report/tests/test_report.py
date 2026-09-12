"""Contract tests for the report challenge."""

import json
import unittest

import report


class TestLoad(unittest.TestCase):
    def test_load_returns_dict(self):
        inputs = report.load_inputs(report.SCENARIO_DIR)
        self.assertEqual(inputs["total_revenue"], 33347.89)


class TestBuild(unittest.TestCase):
    def setUp(self):
        self.inputs = report.load_inputs(report.SCENARIO_DIR)
        self.report = report.build_report(self.inputs)

    def test_metrics_match_inputs(self):
        metrics = self.report["metrics"]
        self.assertEqual(metrics["total_revenue"], self.inputs["total_revenue"])
        self.assertEqual(metrics["rows_clean"], self.inputs["rows_clean"])
        self.assertEqual(metrics["top_category"], self.inputs["top_category"])

    def test_required_sections_in_order(self):
        headings = [s["heading"] for s in self.report["sections"]]
        for required in ("Data quality", "Findings", "Appendix"):
            self.assertIn(required, headings)
        self.assertLess(headings.index("Data quality"), headings.index("Findings"))
        self.assertLess(headings.index("Findings"), headings.index("Appendix"))


class TestRender(unittest.TestCase):
    def setUp(self):
        inputs = report.load_inputs(report.SCENARIO_DIR)
        self.markdown = report.render_markdown(report.build_report(inputs))

    def test_headings_present(self):
        for heading in ("# ", "## Data quality", "## Findings", "## Appendix"):
            self.assertIn(heading, self.markdown)

    def test_key_numbers_appear(self):
        self.assertIn("33347.89", self.markdown)
        self.assertIn("Books", self.markdown)


class TestMain(unittest.TestCase):
    def test_main_writes_report_files(self):
        self.assertEqual(report.main([]), 0)
        data = json.loads((report.OUT_DIR / "report.json").read_text())
        self.assertEqual(data["metrics"]["total_revenue"], 33347.89)
        self.assertIn("## Findings", (report.OUT_DIR / "report.md").read_text())


if __name__ == "__main__":
    unittest.main()
