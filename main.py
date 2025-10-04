import time
import pandas as pd
from binance.client import Client
from config import API_KEY, API_SECRET, PAIRS, INTERVAL_SHORT, INTERVAL_LONG, ALERTS
from strategy import multi_time_strategy
from trader import place_order, get_balance
from logger import log_trade, summary_report

client = Client(API_KEY, API_SECRET, testnet=True)

def get_klines(symbol, interval='15m', limit=100):
    """Obtém dados históricos de candles da Binance Futures Testnet"""
    candles = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(candles, columns=[
        'time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'qav', 'num_trades', 'taker_base', 'taker_quote', 'ignore'
    ])
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df

def run_bot():
    print("🤖 Bot Trader Nível 3 iniciado... Rodando em loop infinito!\n")
    while True:
        for pair in PAIRS:
            print(f"📊 Analisando {pair}...")

            # Dados curto e médio prazo
            df_short = get_klines(pair, INTERVAL_SHORT)
            df_long = get_klines(pair, INTERVAL_LONG)

            # Gerar sinal
            signal = multi_time_strategy(df_short, df_long)
            last_price = df_short['close'].iloc[-1]

            if signal in ["BUY", "SELL"]:
                order = place_order(pair, signal, last_price, df_short)
                if order:
                    balance = get_balance()
                    if ALERTS:
                        print(f"📈 Sinal: {signal} | {pair} | Preço: {last_price} | Saldo: {balance}")
                    log_trade(pair, signal, last_price, order['origQty'], "Executado", pnl=None, balance=balance)
            else:
                print(f"⏸️ Nenhum sinal em {pair}")

        # Resumo periódico no terminal
        summary_report()
        print("\n🔄 Aguardando próximo ciclo...\n")
        time.sleep(60)  # Espera 1 minuto entre ciclos; ajuste conforme necessidade

if __name__ == "__main__":
    run_bot()
