import unittest

from app import calculate


class CalculateTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculate(8, 3, "+"), 11)

    def test_subtraction(self):
        self.assertEqual(calculate(8, 3, "-"), 5)

    def test_multiplication(self):
        self.assertEqual(calculate(8, 3, "*"), 24)

    def test_division(self):
        self.assertEqual(calculate(8, 2, "/"), 4)

    def test_division_by_zero_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "divide by zero"):
            calculate(8, 0, "/")

    def test_unsupported_operation_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "supported operations"):
            calculate(8, 3, "%")

    def test_non_finite_result_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "supported number range"):
            calculate(1e308, 1e308, "*")


if __name__ == "__main__":
    unittest.main()