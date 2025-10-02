from config import QUANTITY_DEFAULT, RISK_PERCENT, MAX_DAILY_LOSS_PERCENT, STOP_LOSS_ATR_MULTIPLIER, TAKE_PROFIT_ATR_MULTIPLIER
from exchange import get_balance, get_price
from strategy import atr

def calculate_quantity(symbol, timeframe='5m', risk_percent=RISK_PERCENT):
    balance = get_balance()
    price = get_price(symbol)
    risk_amount = balance * (risk_percent / 100)
    quantity = risk_amount / price
    return max(quantity, QUANTITY_DEFAULT)

def calculate_sl_tp(symbol, side, timeframe='5m', stop_mult=STOP_LOSS_ATR_MULTIPLIER, tp_mult=TAKE_PROFIT_ATR_MULTIPLIER):
    price = get_price(symbol)
    atr_value = atr(symbol, timeframe)
    if side == "BUY":
        sl = price - atr_value * stop_mult
        tp = price + atr_value * tp_mult
    else:
        sl = price + atr_value * stop_mult
        tp = price - atr_value * tp_mult
    return round(sl, 2), round(tp, 2)

def check_daily_loss(current_loss):
    balance = get_balance()
    limit = balance * (MAX_DAILY_LOSS_PERCENT / 100)
    return current_loss >= limit
