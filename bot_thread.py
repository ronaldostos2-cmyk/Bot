# bot_thread.py (revisado com novo multi-indicator)
import threading, time
from exchange import check_open_orders, place_order, get_order_profit, get_price
from strategy import multi_indicator_signal, atr
from risk_management import calculate_quantity, calculate_sl_tp, check_daily_loss
from utils import log_order
from alerts import send_telegram
from statistics import record_trade
from config import TIMEFRAMES


class BotThread(threading.Thread):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        self.running = True
        self.daily_loss = 0.0
        self.trailing_price = None
        self.current_order = None  # ordem ativa

    def run(self):
        while self.running:
            try:
                # Verifica limite diário de perdas
                if check_daily_loss(self.daily_loss):
                    msg = f"[{self.symbol}] ❌ Limite diário de perda atingido. Operações pausadas."
                    print(msg)
                    send_telegram(msg)
                    time.sleep(60)
                    continue

                open_orders = check_open_orders(self.symbol)

                # Se não houver ordens abertas → buscar novo sinal
                if not open_orders:
                    if self.current_order:
                        # Se havia ordem anterior, registra lucro/prejuízo
                        realized_pnl = get_order_profit(self.symbol)
                        if realized_pnl < 0:
                            self.daily_loss += abs(realized_pnl)

                        record_trade(self.symbol, realized_pnl, self.current_order["side"])
                        log_order(self.symbol, self.current_order, realized_pnl)

                        msg = f"[{self.symbol}] ✅ Ordem encerrada. PnL: {realized_pnl:.2f} USDT | Perda diária: {self.daily_loss:.2f}"
                        print(msg)
                        send_telegram(msg)

                        self.current_order = None

                    # Buscar sinal nos timeframes configurados
                    signal_to_execute = None
                    tf_selected = None
                    for tf in reversed(TIMEFRAMES):  # testa do maior para o menor
                        signal = multi_indicator_signal(self.symbol, tf, confirm_tf="15m")
                        if signal in ["BUY", "SELL"]:
                            signal_to_execute = signal
                            tf_selected = tf
                            break

                    # Se houver sinal válido → abre ordem
                    if signal_to_execute:
                        quantity = calculate_quantity(self.symbol, tf_selected)
                        sl, tp = calculate_sl_tp(self.symbol, signal_to_execute, tf_selected)

                        order = place_order(self.symbol, signal_to_execute, quantity, stop_loss=sl, take_profit=tp)
                        if order:
                            self.current_order = order
                            self.trailing_price = get_price(self.symbol)

                            msg = (f"[{self.symbol} | {tf_selected}] 🚀 Ordem {signal_to_execute} enviada "
                                   f"(Qtd={quantity:.4f}) SL={sl}, TP={tp}")
                            print(msg)
                            send_telegram(msg)

                else:
                    # Ajuste de trailing stop (simples)
                    current_price = get_price(self.symbol)
                    if self.trailing_price:
                        if open_orders[0]['side'] == "BUY" and current_price > self.trailing_price:
                            self.trailing_price = current_price
                            # aqui poderíamos atualizar o SL dinamicamente
                        elif open_orders[0]['side'] == "SELL" and current_price < self.trailing_price:
                            self.trailing_price = current_price
                            # idem para venda

                time.sleep(30)

            except Exception as e:
                print(f"[{self.symbol}] ⚠️ Erro na thread: {e}")
                time.sleep(10)

    def stop(self):
        self.running = False
