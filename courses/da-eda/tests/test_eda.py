"""Contract tests for the EDA challenge (run against starter or solution)."""

import unittest

import eda


class TestLoad(unittest.TestCase):
    def test_load_returns_dataframe(self):
        df = eda.load_transactions(eda.SCENARIO_DIR / "transactions.csv")
        self.assertEqual(len(df), 142)

    def test_load_has_expected_columns(self):
        df = eda.load_transactions(eda.SCENARIO_DIR / "transactions.csv")
        for column in ("order_id", "date", "region", "category", "amount", "quantity"):
            self.assertIn(column, df.columns)


class TestClean(unittest.TestCase):
    def setUp(self):
        self.df = eda.load_transactions(eda.SCENARIO_DIR / "transactions.csv")
        self.clean, self.stats = eda.clean_transactions(self.df)

    def test_removes_exact_duplicates(self):
        self.assertEqual(self.stats["duplicates_removed"], 2)

    def test_counts_bad_amounts(self):
        self.assertEqual(self.stats["missing_amount"], 2)

    def test_counts_bad_dates(self):
        self.assertEqual(self.stats["bad_dates"], 1)

    def test_clean_row_count(self):
        self.assertEqual(len(self.clean), 137)

    def test_clean_has_no_unparsed_amounts(self):
        self.assertFalse(self.clean["amount"].isna().any())
        self.assertFalse(self.clean["date"].isna().any())


class TestSummarize(unittest.TestCase):
    def setUp(self):
        df = eda.load_transactions(eda.SCENARIO_DIR / "transactions.csv")
        clean, _ = eda.clean_transactions(df)
        self.results = eda.summarize(clean)

    def test_total_revenue(self):
        self.assertAlmostEqual(self.results["total_revenue"], 33347.89, places=2)

    def test_revenue_by_region(self):
        expected = {"East": 7477.22, "North": 9401.64,
                    "South": 9140.09, "West": 7328.94}
        for region, value in expected.items():
            self.assertAlmostEqual(self.results["revenue_by_region"][region],
                                   value, places=2)

    def test_top_category(self):
        self.assertEqual(self.results["top_category"], "Books")

    def test_date_range(self):
        self.assertEqual(self.results["first_date"], "2026-01-03")
        self.assertEqual(self.results["last_date"], "2026-03-28")


class TestMain(unittest.TestCase):
    def test_main_writes_results_json(self):
        import json
        self.assertEqual(eda.main([]), 0)
        results = json.loads(
            (eda.SCENARIO_DIR / "results.json").read_text(encoding="utf-8"))
        self.assertEqual(results["rows_total"], 142)
        self.assertEqual(results["rows_clean"], 137)
        self.assertEqual(results["duplicates_removed"], 2)
        self.assertAlmostEqual(results["total_revenue"], 33347.89, places=2)


if __name__ == "__main__":
    unittest.main()
