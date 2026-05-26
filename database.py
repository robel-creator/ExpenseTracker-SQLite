import sqlite3

DB_NAME = "budget_tracker.db"

class InvalidTransactionError(Exception):
    """Custom exception for business logic validation."""
    pass

def get_connection():
    """Handles database connection properly with error handling."""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    """Creates related tables if they do not exist."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        # Table 1: Categories
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                budget_limit REAL DEFAULT 0.0
            )
        """)
        # Table 2: Transactions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                category_id INTEGER,
                date TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        """)
        conn.commit()
        conn.close()

def add_category(name: str, limit: float):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categories (name, budget_limit) VALUES (?, ?)", (name, limit))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"Category '{name}' already exists.")
        finally:
            conn.close()

def add_transaction(t_type: str, amount: float, cat_id: int, date: str):
    if amount <= 0:
        raise InvalidTransactionError("Transaction amount must be positive.")
        
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (type, amount, category_id, date) VALUES (?, ?, ?, ?)",
            (t_type, amount, cat_id, date)
        )
        conn.commit()
        conn.close()

# Keep this execution block at the absolute bottom
from database import init_db, add_category, add_transaction, get_budget_report, InvalidTransactionError

def main():
    init_db()
    
    while True:
        print("\n--- Expense Tracker / Budget Manager ---")
        print("1. Add Category")
        print("2. Add Transaction")
        print("3. View Budget Report & Alerts")
        print("4. Exit")
        choice = input("Select an option: ")

        try:
            if choice == "1":
                name = input("Enter category name (e.g., Food, Utilities): ")
                limit = float(input("Enter monthly budget limit: "))
                add_category(name, limit)
                print("Category added successfully!")
                
            elif choice == "2":
                t_type = input("Type (Income/Expense): ").capitalize()
                amount = float(input("Enter amount: "))
                cat_id = int(input("Enter Category ID: "))
                date = input("Enter date (YYYY-MM-DD): ")
                
                add_transaction(t_type, amount, cat_id, date)
                print("Transaction recorded successfully!")
                
            elif choice == "3":
                print("\n--- MONTHLY BUDGET REPORT ---")
                report = get_budget_report()
                if not report:
                    print("No data available.")
                for row in report:
                    cat_name, limit, total_spent = row
                    print(f"\nCategory: {cat_name}")
                    print(f"  Budget Limit: ${limit:.2f}")
                    print(f"  Total Spent:  ${total_spent:.2f}")
                    
                    # Core Feature: Set budget limits with alerts
                    if total_spent > limit and limit > 0:
                        print(f"  ⚠️ ALERT: You have exceeded your budget for {cat_name} by ${total_spent - limit:.2f}!")
                    elif total_spent >= limit * 0.8 and limit > 0:
                        print(f"  ⚠️ WARNING: You have used {total_spent/limit*100:.1f}% of your {cat_name} budget.")
                    else:
                        print("  ✅ Status: Within Budget")
                print("-----------------------------")
                
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
                
        except ValueError:
            print("Error: Please enter a valid number for amounts or IDs.")
        except InvalidTransactionError as e:
            print(f"Validation Error: {e}")

if __name__ == "__main__":
    main()
if __name__ == "__main__":
    init_db()
