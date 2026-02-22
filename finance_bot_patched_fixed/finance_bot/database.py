import sqlite3

conn = sqlite3.connect("finance.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,
    category TEXT,
    subcategory TEXT,
    amount REAL,
    date TEXT
)
""")
conn.commit()


def add_record(type_, category, subcategory, amount, date):
    cursor.execute(
        """
        INSERT INTO operations (type, category, subcategory, amount, date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (type_, category, subcategory, amount, date)
    )
    conn.commit()

def get_connection():
    return sqlite3.connect("finance.db")

