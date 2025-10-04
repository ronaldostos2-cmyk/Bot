# risk_management.py (revisado)
from config import (
    QUANTITY_DEFAULT,
    RISK_PERCENT,
    MAX_DAILY_LOSS_PERCENT,
    STOP_LOSS_ATR_MULTIPLIER,
    TAKE_PROFIT_ATR_MULTIPLIER,
    MAX_POSITION_SIZE  # novo parâmetro adicionado no config.py
)
from exchange import get_balance, get_price
from strategy import atr


def calculate_quantity(symbol, timeframe='5m', risk_percent=RISK_PERCENT, debug=False):
    """
    Calcula quantidade do ativo com base no risco definido (% do saldo).
    Aplica limite máximo de posição.
    """
    balance = get_balance()
    price = get_price(symbol)

    if balance <= 0 or price <= 0:
        return QUANTITY_DEFAULT

    # risco em USDT
    risk_amount = balance * (risk_percent / 100)

    # quantidade básica
    quantity = risk_amount / price

    # aplica limite máximo de posição
    max_qty = (balance * (MAX_POSITION_SIZE / 100)) / price
    quantity = min(quantity, max_qty)

    if debug:
        print(f"[RISK] {symbol} | Balance={balance:.2f} | Risk={risk_percent:.2f}% | "
              f"Qtd calculada={quantity:.4f} | Limite={max_qty:.4f}")

    return max(quantity, QUANTITY_DEFAULT)


def calculate_sl_tp(symbol, side, timeframe='5m',
                    stop_mult=STOP_LOSS_ATR_MULTIPLIER,
                    tp_mult=TAKE_PROFIT_ATR_MULTIPLIER,
                    debug=False):
    """
    Calcula Stop Loss e Take Profit com base no ATR.
    """
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

    sl, tp = round(sl, 2), round(tp, 2)

    if debug:
        print(f"[RISK] {symbol} | Side={side} | Price={price:.2f} | ATR={atr_value:.4f} | SL={sl} | TP={tp}")

    return sl, tp


def check_daily_loss(current_loss, debug=False):
    """
    Verifica se a perda acumulada no dia ultrapassou o limite permitido (% do saldo).
    """
    balance = get_balance()
    limit = balance * (MAX_DAILY_LOSS_PERCENT / 100)

    if debug:
        print(f"[RISK] Daily Loss={current_loss:.2f} / Limit={limit:.2f} ({MAX_DAILY_LOSS_PERCENT}%)")

    return current_loss >= limit
