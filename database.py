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
if __name__ == "__main__":
    init_db()
