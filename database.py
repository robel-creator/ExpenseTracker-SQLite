import sqlite3

DB_NAME = "budget_tracker.db"

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

if __name__ == "__main__":
    init_db()
