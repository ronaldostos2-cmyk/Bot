import os
import csv

STAT_DIR = "statistics"
os.makedirs(STAT_DIR, exist_ok=True)

def record_trade(symbol, profit, signal):
    filename = f"{STAT_DIR}/{symbol}.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp","signal","profit"])
        from datetime import datetime
        writer.writerow([datetime.now(), signal, profit])

def summarize_statistics():
    print("\nEstatísticas por par:")
    for file in os.listdir(STAT_DIR):
        if file.endswith(".csv"):
            symbol = file.replace(".csv", "")
            total_profit, wins, losses, count = 0,0,0,0
            with open(f"{STAT_DIR}/{file}","r") as f:
                next(f)
                for row in csv.reader(f):
                    p = float(row[2])
                    total_profit += p
                    if p>0: wins+=1
                    elif p<0: losses+=1
                    count+=1
            print(f"{symbol}: Total={total_profit:.2f}, Operações={count}, Wins={wins}, Losses={losses}")
