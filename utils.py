# utils.py (revisado com SQLite + export CSV)
import os
import csv
import datetime
import sqlite3

DB_PATH = "trading.db"
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Cria DB e tabelas se não existirem
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            order_id TEXT,
            side TEXT,
            quantity REAL,
            price REAL,
            profit REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()


def log_order(symbol, order, profit=0):
    """
    Registra ordem no SQLite + salva redundância em CSV.
    """
    ts = datetime.datetime.now().isoformat()
    order_id = order.get('orderId', 'NA')
    side = order.get('side', 'NA')
    qty = float(order.get('origQty', 0))
    price = float(order.get('price', 0))

    # SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (timestamp, symbol, order_id, side, quantity, price, profit)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ts, symbol, str(order_id), side, qty, price, profit))
    conn.commit()
    conn.close()

    # Redundância em CSV (para auditoria rápida)
    filename = f"{LOG_DIR}/{symbol}.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "orderId", "side", "quantity", "price", "profit"])
        writer.writerow([ts, order_id, side, qty, price, profit])


def summarize_daily():
    """
    Resumo diário via SQLite (lucro total por símbolo).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = datetime.datetime.now().date().isoformat()
    cursor.execute("""
        SELECT symbol, SUM(profit) 
        FROM orders 
        WHERE DATE(timestamp) = ? 
        GROUP BY symbol
    """, (today,))
    rows = cursor.fetchall()
    conn.close()

    print("\nResumo diário de lucro/prejuízo:")
    for symbol, total_profit in rows:
        print(f"{symbol}: {total_profit:.4f} USDT")
