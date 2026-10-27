import tempfile
import unittest
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout
from expense_tracker import add_expense, load_expenses, show_summary

class ExpenseTrackerTests(unittest.TestCase):
    def test_add_and_load(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "expenses.csv"
            add_expense(path, "Food", 125.5, "Lunch", "2026-10-26")
            rows = load_expenses(path)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["category"], "Food")
            self.assertEqual(float(rows[0]["amount"]), 125.5)

    def test_reject_non_positive_amount(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                add_expense(Path(folder) / "expenses.csv", "Food", 0)

    def test_category_summary(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "expenses.csv"
            add_expense(path, "Food", 10, day="2026-10-26")
            add_expense(path, "Travel", 20, day="2026-10-26")
            output = StringIO()
            with redirect_stdout(output):
                show_summary(path)
            self.assertIn("Grand total: 30.00", output.getvalue())

if __name__ == "__main__":
    unittest.main()
