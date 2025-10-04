import pandas as pd

def volume_filter(df, threshold=1.5):
    """
    Filtra trades baseado no volume:
    - threshold = múltiplo do volume médio
    Retorna True se o volume atual for suficiente
    """
    avg_volume = df['volume'].rolling(20).mean().iloc[-1]
    last_volume = df['volume'].iloc[-1]
    return last_volume >= avg_volume * threshold

def trend_strength(df, min_diff=0.001):
    """
    Calcula força da tendência usando EMA curta e longa
    Retorna True se a diferença percentual for suficiente
    """
    df['EMA_short'] = df['close'].ewm(span=20, adjust=False).mean()
    df['EMA_long'] = df['close'].ewm(span=50, adjust=False).mean()
    last = df.iloc[-1]
    diff_pct = abs(last['EMA_short'] - last['EMA_long']) / last['close']
    return diff_pct > min_diff

def volatility_filter(df, min_atr_multiplier=1.0):
    """
    Filtra trades baseado em volatilidade (ATR)
    Retorna True se ATR atual >= média * min_atr_multiplier
    """
    df['ATR'] = (df['high'] - df['low']).rolling(14).mean()
    last_atr = df['ATR'].iloc[-1]
    avg_atr = df['ATR'].mean()
    return last_atr >= avg_atr * min_atr_multiplier
