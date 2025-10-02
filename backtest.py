import pandas as pd
from strategy import get_klines, moving_average_crossover, rsi

def backtest(symbol, timeframe='5m', start_balance=1000):
    closes = get_klines(symbol, timeframe, limit=500)
    balance = start_balance
    position = 0
    entry_price = 0
    for i in range(20, len(closes)):
        ma_signal = moving_average_crossover(symbol, timeframe)
        rsi_val = rsi(symbol, timeframe)
        signal = None
        if ma_signal=="BUY" and rsi_val<70:
            signal = "BUY"
        elif ma_signal=="SELL" and rsi_val>30:
            signal = "SELL"

        if signal=="BUY" and position==0:
            position = balance * 0.1 / closes[i]  # 10% balance
            entry_price = closes[i]
        elif signal=="SELL" and position>0:
            profit = position * (closes[i]-entry_price)
            balance += profit
            position = 0

    print(f"Backtest {symbol} | Saldo final estimado: {balance:.2f}")
