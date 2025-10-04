from binance.client import Client
from binance.enums import *
from config import API_KEY, API_SECRET, BASE_STOP_LOSS, BASE_TAKE_PROFIT, MIN_ATR_MULTIPLIER
from risk_manager import RiskManager
from market_filter import volume_filter, trend_strength, volatility_filter

client = Client(API_KEY, API_SECRET, testnet=True)
risk_manager = RiskManager()

def get_balance(asset='USDT'):
    """Retorna saldo disponível"""
    balance = client.futures_account_balance()
    for b in balance:
        if b['asset'] == asset:
            return float(b['balance'])
    return 0.0

def calculate_qty(price, position_value):
    """Calcula quantidade de contratos a operar"""
    qty = position_value / price
    return round(qty, 3)

def place_order(symbol, side, price, df):
    """
    Executa ordens com:
    - Filtros de mercado
    - Gestão de risco avançada
    - SL/TP dinâmicos baseados em ATR
    """
    # Filtros de mercado
    if not (volume_filter(df) and trend_strength(df) and volatility_filter(df, MIN_ATR_MULTIPLIER)):
        print(f"⏸️ {symbol}: Filtros de mercado não satisfeitos. Ordem ignorada.")
        return None

    balance = get_balance()
    position_value = risk_manager.adjust_position(balance)
    if position_value == 0:
        print(f"⏸️ {symbol}: Bot em cooldown devido a perdas consecutivas.")
        return None

    qty = calculate_qty(price, position_value)

    # Criar ordem de mercado
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type=FUTURE_ORDER_TYPE_MARKET,
        quantity=qty
    )

    # SL/TP dinâmicos baseados em ATR
    atr_value = (df['high'] - df['low']).rolling(14).mean().iloc[-1]

    if side == SIDE_BUY:
        stop_price = price - atr_value
        tp_price = price + 2 * atr_value
        opposite_side = SIDE_SELL
    else:
        stop_price = price + atr_value
        tp_price = price - 2 * atr_value
        opposite_side = SIDE_BUY

    # Ordem Stop Loss
    client.futures_create_order(
        symbol=symbol,
        side=opposite_side,
        type=FUTURE_ORDER_TYPE_STOP_MARKET,
        stopPrice=round(stop_price, 2),
        quantity=qty
    )

    # Ordem Take Profit
    client.futures_create_order(
        symbol=symbol,
        side=opposite_side,
        type=FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,
        stopPrice=round(tp_price, 2),
        quantity=qty
    )

    print(f"✅ Ordem executada: {side} {symbol} | Qtd: {qty} | Preço: {price}")
    return order
