# Python Expense Tracker

A command-line expense tracker that stores records in a local CSV file.

## Features
- Add expenses with category, amount, date, and note
- List expenses and calculate totals
- Summarize spending by category
- Use a custom CSV storage path
- Automated unit tests

## Requirements
Python 3.10+; no third-party packages required.

## Usage
```bash
python expense_tracker.py add Food 125.50 --note "Lunch"
python expense_tracker.py list
python expense_tracker.py summary
```
Custom file:
```bash
python expense_tracker.py --file data/my_expenses.csv add Travel 80
```
Dates use `YYYY-MM-DD`; amounts must be greater than zero.

## Tests
```bash
python -m unittest -v
```

## Privacy
Data stays in a local CSV file. Do not commit personal financial records to a public repository.
