from binance.client import Client
from binance.enums import *
from config import API_KEY, API_SECRET, BASE_URL

client = Client(API_KEY, API_SECRET, testnet=True)
client.FUTURES_URL = BASE_URL


def get_symbol_info(symbol):
    info = client.futures_exchange_info()
    for s in info['symbols']:
        if s['symbol'] == symbol:
            return s
    return None


def adjust_quantity(symbol, quantity):
    info = get_symbol_info(symbol)
    if not info:
        return quantity
    for f in info['filters']:
        if f['filterType'] == "LOT_SIZE":
            step_size = float(f['stepSize'])
            precision = max(0, len(str(step_size).rstrip('0').split('.')[-1]))
            qty = (quantity // step_size) * step_size
            return round(qty, precision)
    return quantity


def adjust_price(symbol, price):
    info = get_symbol_info(symbol)
    if not info:
        return round(price, 2)
    for f in info['filters']:
        if f['filterType'] == "PRICE_FILTER":
            tick_size = float(f['tickSize'])
            precision = max(0, len(str(tick_size).rstrip('0').split('.')[-1]))
            adjusted = round(price - (price % tick_size), precision)
            return adjusted
    return round(price, 2)


def validate_order(symbol, quantity, price=None, debug=False):
    info = get_symbol_info(symbol)
    if not info:
        return quantity, price

    qty = float(quantity)
    px = float(price) if price else None

    for f in info['filters']:
        if f['filterType'] == "LOT_SIZE":
            step_size = float(f['stepSize'])
            min_qty = float(f['minQty'])
            if qty < min_qty:
                qty = 0
            else:
                precision = max(0, len(str(step_size).rstrip('0').split('.')[-1]))
                qty = round((qty // step_size) * step_size, precision)

        elif f['filterType'] == "PRICE_FILTER" and px:
            tick_size = float(f['tickSize'])
            precision = max(0, len(str(tick_size).rstrip('0').split('.')[-1]))
            px = round(px - (px % tick_size), precision)

        elif f['filterType'] == "MIN_NOTIONAL" and px:
            notional = qty * px
            min_notional = float(f['notional'])
            if notional < min_notional:
                if debug:
                    print(f"[VALIDATE] Ordem {symbol} rejeitada: Notional {notional} < {min_notional}")
                qty = 0

    if debug:
        print(f"[VALIDATE] {symbol} | Qty={qty} | Price={px}")

    return qty, px


def get_balance(asset="USDT"):
    try:
        balances = client.futures_account_balance()
        usdt = next((b for b in balances if b['asset'] == asset), None)
        return float(usdt['balance']) if usdt else 0.0
    except Exception as e:
        print(f"[exchange] Erro ao buscar saldo: {e}")
        return 0.0


def get_price(symbol):
    try:
        return float(client.futures_symbol_ticker(symbol=symbol)['price'])
    except Exception as e:
        print(f"[exchange] Erro ao buscar preço {symbol}: {e}")
        return 0.0


def place_order(symbol, side, quantity, stop_loss=None, take_profit=None):
    try:
        # valida quantidade antes
        quantity, _ = validate_order(symbol, quantity, get_price(symbol), debug=True)
        if quantity <= 0:
            print(f"[exchange] Ordem rejeitada: quantidade inválida para {symbol}")
            return None

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity
        )

        opposite_side = SIDE_SELL if side == SIDE_BUY else SIDE_BUY

        if stop_loss:
            _, stop_loss = validate_order(symbol, quantity, stop_loss)
            client.futures_create_order(
                symbol=symbol,
                side=opposite_side,
                type=FUTURE_ORDER_TYPE_STOP_MARKET,
                stopPrice=stop_loss,
                closePosition=True,
                reduceOnly=True
            )
        if take_profit:
            _, take_profit = validate_order(symbol, quantity, take_profit)
            client.futures_create_order(
                symbol=symbol,
                side=opposite_side,
                type=FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,
                stopPrice=take_profit,
                closePosition=True,
                reduceOnly=True
            )

        return order
    except Exception as e:
        print(f"[exchange] Erro ao criar ordem: {e}")
        return None


def check_open_orders(symbol):
    try:
        return client.futures_get_open_orders(symbol=symbol)
    except Exception as e:
        print(f"[exchange] Erro ao buscar ordens abertas: {e}")
        return []


def get_order_profit(symbol):
    try:
        trades = client.futures_account_trades(symbol=symbol)
        realized_pnl = sum(float(t['realizedPnl']) for t in trades)
        return realized_pnl
    except Exception as e:
        print(f"[exchange] Erro ao calcular PnL de {symbol}: {e}")
        return 0.0
