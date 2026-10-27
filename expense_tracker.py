import argparse
import csv
from datetime import date
from pathlib import Path

FIELDS = ["date", "category", "amount", "note"]
DEFAULT_FILE = Path("expenses.csv")

def ensure_file(path):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=FIELDS).writeheader()

def load_expenses(path):
    ensure_file(path)
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def add_expense(path, category, amount, note="", day=None):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    day = day or date.today().isoformat()
    date.fromisoformat(day)
    ensure_file(path)
    with path.open("a", newline="", encoding="utf-8") as file:
        csv.DictWriter(file, fieldnames=FIELDS).writerow({
            "date": day, "category": category.strip(), "amount": f"{amount:.2f}", "note": note.strip()
        })

def show_expenses(path):
    rows = load_expenses(path)
    if not rows:
        print("No expenses recorded yet.")
        return
    print(f"{'DATE':12} {'CATEGORY':18} {'AMOUNT':>10}  NOTE")
    print("-" * 60)
    for row in rows:
        print(f"{row['date']:12} {row['category'][:18]:18} {float(row['amount']):10.2f}  {row['note']}")
    print("-" * 60)
    print(f"Total: {sum(float(row['amount']) for row in rows):.2f}")

def show_summary(path):
    rows = load_expenses(path)
    if not rows:
        print("No expenses to summarize.")
        return
    totals = {}
    for row in rows:
        totals[row["category"]] = totals.get(row["category"], 0.0) + float(row["amount"])
    print("Spending by category:")
    for category, total in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"  {category}: {total:.2f}")
    print(f"Grand total: {sum(totals.values()):.2f}")

def main():
    parser = argparse.ArgumentParser(description="Record and summarize expenses.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="CSV storage path")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="Add an expense")
    add.add_argument("category")
    add.add_argument("amount", type=float)
    add.add_argument("--note", default="")
    add.add_argument("--date", dest="day", help="Date in YYYY-MM-DD format")
    sub.add_parser("list", help="List expenses")
    sub.add_parser("summary", help="Summarize spending by category")
    args = parser.parse_args()
    try:
        if args.command == "add":
            add_expense(args.file, args.category, args.amount, args.note, args.day)
            print("Expense saved.")
        elif args.command == "list":
            show_expenses(args.file)
        else:
            show_summary(args.file)
    except (ValueError, OSError) as error:
        parser.error(str(error))

if __name__ == "__main__":
    main()
