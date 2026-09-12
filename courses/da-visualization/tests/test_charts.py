"""Contract tests for the visualization challenge."""

import json
import unittest

import charts


class TestLoad(unittest.TestCase):
    def test_load_returns_rows(self):
        df = charts.load_sales(charts.SCENARIO_DIR / "sales_daily.csv")
        self.assertEqual(len(df), 135)


class TestSummary(unittest.TestCase):
    def setUp(self):
        df = charts.load_sales(charts.SCENARIO_DIR / "sales_daily.csv")
        self.result = charts.summary(df)

    def test_region_totals(self):
        expected = {"East": 12334.94, "North": 14294.7, "South": 11200.48}
        for region, value in expected.items():
            self.assertAlmostEqual(
                self.result["revenue_by_region"][region], value, places=2)

    def test_daily_count_and_total(self):
        self.assertEqual(len(self.result["daily_revenue"]), 45)
        self.assertAlmostEqual(self.result["grand_total"], 37830.12, places=2)


def _is_png(path):
    data = path.read_bytes()
    return data[:8] == b"\x89PNG\r\n\x1a\n"


class TestCharts(unittest.TestCase):
    def setUp(self):
        charts.main([])

    def test_three_pngs_exist_and_are_valid(self):
        for name in ("revenue_by_region", "daily_revenue", "revenue_histogram"):
            path = charts.OUT_DIR / f"{name}.png"
            self.assertTrue(path.exists(), name)
            self.assertTrue(_is_png(path), name)
            self.assertGreater(path.stat().st_size, 3000, name)

    def test_summary_json_written(self):
        data = json.loads((charts.OUT_DIR / "summary.json").read_text())
        self.assertAlmostEqual(data["grand_total"], 37830.12, places=2)


if __name__ == "__main__":
    unittest.main()
