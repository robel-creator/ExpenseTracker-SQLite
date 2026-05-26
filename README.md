# Expense Tracker & Budget Manager

A Python command-line application using SQLite to track income/expenses, monitor budgets, and generate financial summaries.

## Core Features
* Add income and expense transactions
* Categorize spending (Food, Utilities, etc.)
* Set budget limits with automatic warning/exceeded alerts
* Maintain full transaction history using a relational SQLite database

## OOP Architecture
* **Transaction (Base Class):** Uses encapsulation with protected members and getters/setters for transaction amounts.
* **ExpenseTransaction (Derived Class):** Inherits from Transaction and overrides the `get_details()` method to track essential vs. non-essential spending.

## How to Install and Run
1. Ensure you have Python installed on your computer.
2. Clone this repository to your local machine.
3. Open a terminal/command prompt in the project directory.
4. Run the application using:
   ```bash
   python main.py
