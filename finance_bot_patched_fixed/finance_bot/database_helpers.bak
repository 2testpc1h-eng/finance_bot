import sqlite3
from datetime import date
from typing import Optional, Tuple

DB_PATH = "finance.db"


def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# ---------- ИНИЦИАЛИЗАЦИЯ БД ----------

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


# ---------- ДОБАВЛЕНИЕ ЗАПИСИ ----------

def add_operation(
    user_id: int,
    type_: str,
    category: str,
    subcategory: Optional[str],
    amount: float,
    date_str: str
):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO operations (user_id, type, category, subcategory, amount, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, type_, category, subcategory, amount, date_str)
    )
    conn.commit()
    conn.close()


# ---------- СУММЫ / ОТЧЁТЫ ----------

def sum_by_type_and_category(
    user_id: int,
    type_: str,
    category: Optional[str] = None,
    period: Optional[Tuple[date, date]] = None
) -> float:
    conn = get_conn()
    cur = conn.cursor()

    params = [user_id, type_]
    q = "SELECT COALESCE(SUM(amount), 0) FROM operations WHERE user_id = ? AND type = ?"

    if category:
        q += " AND category = ?"
        params.append(category)

    if period:
        start_iso = period[0].strftime("%Y-%m-%d")
        end_iso = period[1].strftime("%Y-%m-%d")
        q += " AND date BETWEEN ? AND ?"
        params.extend([start_iso, end_iso])

    cur.execute(q, params)
    val = cur.fetchone()[0] or 0.0
    conn.close()
    return float(val)


def sums_by_categories(
    user_id: int,
    type_: str,
    period: Optional[Tuple[date, date]] = None
) -> dict:
    conn = get_conn()
    cur = conn.cursor()

    if period:
        start_iso = period[0].strftime("%Y-%m-%d")
        end_iso = period[1].strftime("%Y-%m-%d")
        q = """
            SELECT category, COALESCE(SUM(amount), 0)
            FROM operations
            WHERE user_id = ? AND type = ? AND date BETWEEN ? AND ?
            GROUP BY category
        """
        params = [user_id, type_, start_iso, end_iso]
    else:
        q = """
            SELECT category, COALESCE(SUM(amount), 0)
            FROM operations
            WHERE user_id = ? AND type = ?
            GROUP BY category
        """
        params = [user_id, type_]

    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    return {r[0]: float(r[1]) for r in rows}


def get_total_by_type(
    user_id: int,
    type_: str,
    period: Optional[Tuple[date, date]] = None
) -> float:
    return sum_by_type_and_category(user_id, type_, None, period)


def get_daily_totals(
    user_id: int,
    type_: str,
    period: Optional[Tuple[date, date]] = None
):
    conn = get_conn()
    cur = conn.cursor()

    params = [user_id, type_]
    q = "SELECT date, SUM(amount) FROM operations WHERE user_id = ? AND type = ?"

    if period:
        start_iso = period[0].strftime("%Y-%m-%d")
        end_iso = period[1].strftime("%Y-%m-%d")
        q += " AND date BETWEEN ? AND ?"
        params.extend([start_iso, end_iso])

    q += " GROUP BY date ORDER BY date"

    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()

    dates = [r[0] for r in rows]
    values = [float(r[1]) for r in rows]

    return dates, values


# ---------- ОЧИСТКА ДАННЫХ ----------

def delete_by_type_all_time(user_id: int, type_: str) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM operations WHERE user_id = ? AND type = ?",
        (user_id, type_)
    )
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    return deleted


def delete_by_type_and_period(
    user_id: int,
    type_: str,
    period: Tuple[date, date]
) -> int:
    start_iso = period[0].strftime("%Y-%m-%d")
    end_iso = period[1].strftime("%Y-%m-%d")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM operations
        WHERE user_id = ? AND type = ? AND date BETWEEN ? AND ?
        """,
        (user_id, type_, start_iso, end_iso)
    )
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    return deleted


# ---------- CATEGORIES table helpers ----------
def _ensure_categories_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            name TEXT,
            UNIQUE(user_id, type, name)
        )
    """)
    conn.commit()
    conn.close()

def add_category(user_id: int, type_: str, name: str) -> bool:
    _ensure_categories_table()
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categories (user_id, type, name) VALUES (?, ?, ?)", (user_id, type_, name))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()

def get_categories(user_id: int, type_: str):
    _ensure_categories_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM categories WHERE user_id = ? AND type = ? ORDER BY name", (user_id, type_))
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]

def delete_category(user_id: int, type_: str, name: str) -> bool:
    _ensure_categories_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM categories WHERE user_id = ? AND type = ? AND name = ?", (user_id, type_, name))
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    return bool(deleted)
