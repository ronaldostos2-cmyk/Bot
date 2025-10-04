# strategy.py (revisado)
import pandas as pd
from exchange import client


def get_klines(symbol, timeframe='5m', limit=100):
    klines = client.futures_klines(symbol=symbol, interval=timeframe, limit=limit)
    df = pd.DataFrame(klines, columns=[
        "ts","open","high","low","close","volume",
        "close_time","qav","num_trades","tb_base","tb_quote","ignore"
    ])
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    return df


def moving_average_crossover(symbol, timeframe='5m', short_window=5, long_window=20):
    df = get_klines(symbol, timeframe, limit=long_window+5)
    closes = df['close']
    short_ma = closes.rolling(short_window).mean().iloc[-1]
    long_ma = closes.rolling(long_window).mean().iloc[-1]
    if pd.isna(short_ma) or pd.isna(long_ma):
        return "HOLD"
    if short_ma > long_ma:
        return "BUY"
    elif short_ma < long_ma:
        return "SELL"
    return "HOLD"


def ema(series, period=9):
    return series.ewm(span=period, adjust=False).mean()


def macd(symbol, timeframe='5m', fast=12, slow=26, signal=9):
    df = get_klines(symbol, timeframe, limit=slow+signal+5)
    closes = df['close']
    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal)
    if macd_line.iloc[-1] > signal_line.iloc[-1]:
        return "BUY"
    elif macd_line.iloc[-1] < signal_line.iloc[-1]:
        return "SELL"
    return "HOLD"


def rsi(symbol, timeframe='5m', period=14):
    df = get_klines(symbol, timeframe, limit=period+5)
    closes = df['close']
    delta = closes.diff().dropna()
    gain = delta.where(delta > 0, 0).mean()
    loss = -delta.where(delta < 0, 0).mean()
    if loss == 0:
        return 50
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def atr(symbol, timeframe='5m', period=14):
    df = get_klines(symbol, timeframe, limit=period+5)
    highs = df['high']
    lows = df['low']
    closes = df['close']
    tr = pd.concat([
        highs - lows,
        (highs - closes.shift(1)).abs(),
        (lows - closes.shift(1)).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean().iloc[-1]


def multi_indicator_signal(symbol, timeframe='5m', confirm_tf='15m'):
    """
    Estratégia combinada:
    - Confirmação MA + RSI no timeframe principal
    - Confirmação com timeframe maior (confirm_tf)
    - Filtro de volatilidade (ATR deve estar acima da média)
    - MACD usado como filtro extra
    """
    ma_signal = moving_average_crossover(symbol, timeframe)
    rsi_val = rsi(symbol, timeframe)
    macd_signal = macd(symbol, timeframe)

    # Confirmar tendência no timeframe maior
    confirm_signal = moving_average_crossover(symbol, confirm_tf)

    # Filtro de volatilidade
    atr_now = atr(symbol, timeframe)
    atr_df = get_klines(symbol, timeframe, limit=50)
    atr_series = pd.Series(
        (atr_df['high'] - atr_df['low']).rolling(14).mean()
    )
    atr_avg = atr_series.iloc[-1] if not atr_series.empty else atr_now
    volatility_ok = atr_now > atr_avg

    # Regras finais
    if ma_signal == "BUY" and rsi_val < 70 and confirm_signal == "BUY" and macd_signal == "BUY" and volatility_ok:
        return "BUY"
    elif ma_signal == "SELL" and rsi_val > 30 and confirm_signal == "SELL" and macd_signal == "SELL" and volatility_ok:
        return "SELL"
    return "HOLD"
