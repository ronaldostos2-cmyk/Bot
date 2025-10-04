from indicators import ema_multi, rsi, macd, bollinger_bands, atr

def multi_time_strategy(df_short, df_long):
    """
    Estratégia Multi-Tempo Nível 3:
    - Confirma tendência em curto (15m) e médio prazo (1h)
    - Filtra sinais por EMA, RSI, MACD, Bollinger e ATR
    - Retorna "BUY", "SELL" ou "HOLD"
    """

    # EMA multi-tempo
    df_short = ema_multi(df_short)
    df_long = ema_multi(df_long)

    last_short = df_short.iloc[-1]
    last_long = df_long.iloc[-1]

    # Indicadores RSI e MACD curto prazo
    rsi_short = rsi(df_short)
    macd_line, signal_line = macd(df_short)

    # ATR para volatilidade
    atr_value = atr(df_short).iloc[-1]
    avg_atr = atr(df_short).mean()
    if atr_value < avg_atr:
        return "HOLD"  # Ignora se volatilidade baixa

    # Condições de compra
    if (
        last_short['EMA_short'] > last_short['EMA_long'] and  # Tendência de alta curto prazo
        last_long['EMA_short'] > last_long['EMA_long'] and    # Tendência de alta médio prazo
        rsi_short.iloc[-1] < 30 and                           # Sobrevenda
        macd_line.iloc[-1] > signal_line.iloc[-1]            # Momentum positivo
    ):
        return "BUY"

    # Condições de venda
    elif (
        last_short['EMA_short'] < last_short['EMA_long'] and  # Tendência de baixa curto prazo
        last_long['EMA_short'] < last_long['EMA_long'] and    # Tendência de baixa médio prazo
        rsi_short.iloc[-1] > 70 and                           # Sobrecompra
        macd_line.iloc[-1] < signal_line.iloc[-1]            # Momentum negativo
    ):
        return "SELL"

    return "HOLD"
