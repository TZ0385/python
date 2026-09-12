import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from calc import add, slugify


class CalcTest(unittest.TestCase):
    def test_add_sums_two_numbers(self) -> None:
        self.assertEqual(add(2, 3), 5)

    def test_slugify_drops_empty_parts(self) -> None:
        # Deliberately wrong expectation: reproduces an unverified AI change.
        self.assertEqual(slugify("  Hello   World "), "Hello World")


if __name__ == "__main__":
    unittest.main()
