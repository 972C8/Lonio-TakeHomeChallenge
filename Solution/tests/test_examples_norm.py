"""Example comparison: a result built from parts compares as its joined text (no LLM)."""
import unittest

from pipeline.checks.mechanical import _norm


class TestNorm(unittest.TestCase):
    def test_code_from_parts_equals_joined_text(self):
        self.assertEqual(_norm(["N", 1, "Y"]), _norm("N1Y"))
        self.assertEqual(_norm(("L", 0, "Y")), "l0y")

    def test_scalars_unchanged(self):
        self.assertEqual(_norm(True), "yes")
        self.assertEqual(_norm(" C1Y "), "c1y")


if __name__ == "__main__":
    unittest.main()
