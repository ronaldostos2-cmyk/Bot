import os
import csv
import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_order(symbol, order, profit=0):
    filename = f"{LOG_DIR}/{symbol}.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "orderId", "side", "quantity", "price", "profit"])
        writer.writerow([
            datetime.datetime.now(),
            order['orderId'],
            order['side'],
            order['origQty'],
            order['price'] if 'price' in order else 0,
            profit
        ])

def summarize_daily():
    print("\nResumo diário de lucro/prejuízo:")
    for file in os.listdir(LOG_DIR):
        if file.endswith(".csv"):
            symbol = file.replace(".csv", "")
            total_profit = 0
            with open(f"{LOG_DIR}/{file}", "r") as f:
                next(f)  # skip header
                for row in csv.reader(f):
                    total_profit += float(row[5])
            print(f"{symbol}: {total_profit:.4f} USDT")
