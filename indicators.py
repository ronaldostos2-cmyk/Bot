import pandas as pd

def ema(df, period=20, column='close'):
    """Média Móvel Exponencial (EMA)"""
    return df[column].ewm(span=period, adjust=False).mean()

def rsi(df, period=14, column='close'):
    """Índice de Força Relativa (RSI)"""
    delta = df[column].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(df, fast=12, slow=26, signal=9):
    """MACD e linha de sinal"""
    exp1 = df['close'].ewm(span=fast, adjust=False).mean()
    exp2 = df['close'].ewm(span=slow, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line

def bollinger_bands(df, period=20):
    """Bandas de Bollinger"""
    sma = df['close'].rolling(window=period).mean()
    std = df['close'].rolling(window=period).std()
    upper = sma + (std * 2)
    lower = sma - (std * 2)
    return upper, lower

def atr(df, period=14):
    """Average True Range (ATR) para volatilidade"""
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()

def ema_multi(df, short=20, long=50):
    """EMA curta e longa para análise multi-tempo"""
    df['EMA_short'] = ema(df, short)
    df['EMA_long'] = ema(df, long)
    return df
