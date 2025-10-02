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
        self.daily_loss = 0
        self.trailing_price = None

    def run(self):
        while self.running:
            try:
                if check_daily_loss(self.daily_loss):
                    msg = f"[{self.symbol}] Limite diário de perda atingido. Operações pausadas."
                    print(msg)
                    send_telegram(msg)
                    time.sleep(60)
                    continue

                open_orders = check_open_orders(self.symbol)
                if not open_orders:
                    signal_to_execute = None
                    tf_selected = None
                    for tf in reversed(TIMEFRAMES):
                        signal = multi_indicator_signal(self.symbol, tf)
                        if signal in ["BUY","SELL"]:
                            signal_to_execute = signal
                            tf_selected = tf
                            break

                    if signal_to_execute:
                        quantity = calculate_quantity(self.symbol, tf_selected)
                        sl, tp = calculate_sl_tp(self.symbol, signal_to_execute, tf_selected)

                        order = place_order(self.symbol, signal_to_execute, quantity, stop_loss=sl, take_profit=tp)
                        if order:
                            profit = get_order_profit(order)
                            self.daily_loss += max(0, -profit)
                            self.trailing_price = get_price(self.symbol)
                            log_order(self.symbol, order, profit)
                            record_trade(self.symbol, profit, signal_to_execute)
                            msg = f"[{self.symbol} | {tf_selected}] Ordem {signal_to_execute} enviada. SL={sl}, TP={tp}, Profit estimado={profit:.2f}"
                            print(msg)
                            send_telegram(msg)
                else:
                    current_price = get_price(self.symbol)
                    if self.trailing_price:
                        if open_orders[0]['side'] == "BUY" and current_price > self.trailing_price:
                            self.trailing_price = current_price
                        elif open_orders[0]['side'] == "SELL" and current_price < self.trailing_price:
                            self.trailing_price = current_price

                time.sleep(30)
            except Exception as e:
                print(f"[{self.symbol}] Erro na thread: {e}")
                time.sleep(10)

    def stop(self):
        self.running = False
