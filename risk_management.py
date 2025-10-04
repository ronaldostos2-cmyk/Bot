from config import (
    QUANTITY_DEFAULT,
    RISK_PERCENT,
    MAX_DAILY_LOSS_PERCENT,
    STOP_LOSS_ATR_MULTIPLIER,
    TAKE_PROFIT_ATR_MULTIPLIER,
    MAX_POSITION_SIZE
)
from exchange import get_balance, get_price, validate_order
from strategy import atr


def calculate_quantity(symbol, timeframe='5m', risk_percent=RISK_PERCENT, debug=False):
    balance = get_balance()
    price = get_price(symbol)
    if balance <= 0 or price <= 0:
        return QUANTITY_DEFAULT

    risk_amount = balance * (risk_percent / 100)
    quantity = risk_amount / price

    max_qty = (balance * (MAX_POSITION_SIZE / 100)) / price
    quantity = min(quantity, max_qty)

    quantity, _ = validate_order(symbol, quantity, price, debug=debug)
    return max(quantity, QUANTITY_DEFAULT)


def calculate_sl_tp(symbol, side, timeframe='5m',
                    stop_mult=STOP_LOSS_ATR_MULTIPLIER,
                    tp_mult=TAKE_PROFIT_ATR_MULTIPLIER,
                    debug=False):
    price = get_price(symbol)
    atr_value = atr(symbol, timeframe)
    if atr_value <= 0 or price <= 0:
        return None, None

    if side == "BUY":
        sl = price - atr_value * stop_mult
        tp = price + atr_value * tp_mult
    else:
        sl = price + atr_value * stop_mult
        tp = price - atr_value * tp_mult

    _, sl = validate_order(symbol, 1, sl, debug=debug)
    _, tp = validate_order(symbol, 1, tp, debug=debug)

    return sl, tp


def check_daily_loss(current_loss, debug=False):
    balance = get_balance()
    limit = balance * (MAX_DAILY_LOSS_PERCENT / 100)
    return current_loss >= limit
