import pandas as pd
from exchange import client

def get_klines(symbol, timeframe='5m', limit=50):
    klines = client.futures_klines(symbol=symbol, interval=timeframe, limit=limit)
    closes = [float(k[4]) for k in klines]
    return pd.Series(closes)

def moving_average_crossover(symbol, timeframe='5m', short_window=5, long_window=20):
    closes = get_klines(symbol, timeframe)
    short_ma = closes.rolling(short_window).mean().iloc[-1]
    long_ma = closes.rolling(long_window).mean().iloc[-1]
    if short_ma > long_ma:
        return "BUY"
    elif short_ma < long_ma:
        return "SELL"
    return "HOLD"

def rsi(symbol, timeframe='5m', period=14):
    closes = get_klines(symbol, timeframe, period+1)
    delta = closes.diff().dropna()
    gain = delta.where(delta>0,0).mean()
    loss = -delta.where(delta<0,0).mean()
    rs = gain/loss if loss !=0 else 0
    return 100 - (100 / (1+rs))

def atr(symbol, timeframe='5m', period=14):
    klines = client.futures_klines(symbol=symbol, interval=timeframe, limit=period+1)
    highs = pd.Series([float(k[2]) for k in klines])
    lows = pd.Series([float(k[3]) for k in klines])
    closes = pd.Series([float(k[4]) for k in klines])
    tr = pd.concat([
        highs - lows,
        (highs - closes.shift(1)).abs(),
        (lows - closes.shift(1)).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean().iloc[-1]

def multi_indicator_signal(symbol, timeframe='5m'):
    ma_signal = moving_average_crossover(symbol, timeframe)
    rsi_val = rsi(symbol, timeframe)
    if ma_signal=="BUY" and rsi_val<70:
        return "BUY"
    elif ma_signal=="SELL" and rsi_val>30:
        return "SELL"
    return "HOLD"
