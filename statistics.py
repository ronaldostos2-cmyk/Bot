# statistics.py (revisado com SQLite + export opcional)
import sqlite3
import csv
import os

DB_PATH = "trading.db"
STAT_DIR = "statistics"
os.makedirs(STAT_DIR, exist_ok=True)


def record_trade(symbol, profit, signal):
    """
    Salva trade no banco SQLite (tabela trades).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            symbol TEXT,
            signal TEXT,
            profit REAL
        )
    """)
    cursor.execute("""
        INSERT INTO trades (symbol, signal, profit) VALUES (?, ?, ?)
    """, (symbol, signal, profit))
    conn.commit()
    conn.close()


def summarize_statistics(export_csv=True):
    """
    Estatísticas por par: total, número de operações, wins, losses, profit factor.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT symbol, COUNT(*), SUM(profit),
               SUM(CASE WHEN profit > 0 THEN 1 ELSE 0 END) AS wins,
               SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS losses
        FROM trades
        GROUP BY symbol
    """)
    rows = cursor.fetchall()
    conn.close()

    print("\n📊 Estatísticas por par:")
    results = []
    for symbol, count, total_profit, wins, losses in rows:
        profit_factor = (wins / losses) if losses > 0 else float("inf")
        print(f"{symbol}: Total={total_profit:.2f}, Operações={count}, Wins={wins}, Losses={losses}, PF={profit_factor:.2f}")
        results.append([symbol, count, total_profit, wins, losses, profit_factor])

    # Exportar CSV opcional
    if export_csv:
        filename = f"{STAT_DIR}/statistics.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["symbol", "trades", "total_profit", "wins", "losses", "profit_factor"])
            writer.writerows(results)
        print(f"📁 Estatísticas exportadas para {filename}")
