import sqlite3
from datetime import datetime

DB_NAME = "expenses.db"

def init_db():
    """ 初期テーブル作成 """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            meal TEXT,
            price REAL
        )
    """)
    conn.commit()
    conn.close()

def add_expense(meal, price):
    """ 食事と金額を保存 """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (date, meal, price) VALUES (?, ?, ?)", 
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), meal, price))
    conn.commit()
    conn.close()

def get_weekly_total():
    """ 今週の合計金額を取得 """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT SUM(price) FROM expenses
        WHERE date >= datetime('now', '-7 days')
    """)
    total = cur.fetchone()[0] or 0
    conn.close()
    return total
