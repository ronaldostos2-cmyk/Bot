import csv
from datetime import datetime

def log_trade(symbol, side, price, qty, result, pnl=None, balance=None):
    """
    Registra detalhes de cada operação em trades.csv
    - symbol: par negociado
    - side: BUY ou SELL
    - price: preço da operação
    - qty: quantidade negociada
    - result: Executado ou Ignorado
    - pnl: lucro/prejuízo do trade (opcional)
    - balance: saldo após trade (opcional)
    """
    with open("trades.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(), symbol, side, price, qty, result, pnl, balance
        ])

def summary_report():
    """
    Gera um resumo avançado das operações:
    - Total de trades
    - Lucro/prejuízo acumulado
    - % de acerto
    - Drawdown máximo
    """
    try:
        df = []
        with open("trades.csv", "r") as f:
            for row in csv.reader(f):
                df.append(row)

        if not df:
            print("⚠️ Nenhum trade registrado ainda.")
            return

        total_trades = len(df)
        wins = sum(1 for r in df if r[6] and float(r[6]) > 0)
        losses = total_trades - wins
        win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
        pnl_total = sum(float(r[6]) for r in df if r[6])

        # Cálculo simples de drawdown
        balance_history = [float(r[7]) for r in df if r[7]]
        peak = balance_history[0] if balance_history else 0
        drawdown = 0
        for b in balance_history:
            if b > peak:
                peak = b
            dd = peak - b
            if dd > drawdown:
                drawdown = dd

        print(f"📊 Resumo Trades: Total={total_trades}, Wins={wins}, Losses={losses}, WinRate={win_rate:.2f}%, PnL Total={pnl_total:.2f}, Max Drawdown={drawdown:.2f}")

    except FileNotFoundError:
        print("⚠️ Nenhum trade registrado ainda.")
