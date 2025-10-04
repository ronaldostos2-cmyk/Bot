from binance.client import Client
from config import API_KEY, API_SECRET, BASE_URL

client = Client(API_KEY, API_SECRET, testnet=True)
client.FUTURES_URL = BASE_URL

def get_balance():
    balances = client.futures_account_balance()
    usdt = next((b for b in balances if b['asset']=='USDT'), None)
    return float(usdt['balance']) if usdt else 0

def get_price(symbol):
    return float(client.futures_symbol_ticker(symbol=symbol)['price'])

def place_order(symbol, side, quantity, stop_loss=None, take_profit=None):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        if stop_loss:
            client.futures_create_order(
                symbol=symbol,
                side="SELL" if side=="BUY" else "BUY",
                type="STOP_MARKET",
                stopPrice=stop_loss,
                quantity=quantity
            )
        if take_profit:
            client.futures_create_order(
                symbol=symbol,
                side="SELL" if side=="BUY" else "BUY",
                type="TAKE_PROFIT_MARKET",
                stopPrice=take_profit,
                quantity=quantity
            )
        return order
    except Exception as e:
        print(f"[exchange] Erro ao criar ordem: {e}")
        return None

def check_open_orders(symbol):
    try:
        return client.futures_get_open_orders(symbol=symbol)
    except:
        return []

def get_order_profit(order):
    try:
        side = order['side']
        entry = float(order['price']) if 'price' in order else get_price(order['symbol'])
        exit_price = get_price(order['symbol'])
        quantity = float(order['origQty'])
        if side == "BUY":
            return (exit_price - entry) * quantity
        else:
            return (entry - exit_price) * quantity
    except:
        return 0
