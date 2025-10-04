# config.py (revisado e organizado)

# =========================
# 🔑 Binance API (Testnet ou Real)
# =========================
API_KEY = "SUA_API_KEY_TESTNET"
API_SECRET = "SEU_API_SECRET_TESTNET"

# Para futures testnet
BASE_URL = "https://testnet.binancefuture.com"
# Para produção: comente a linha acima e use:
# BASE_URL = "https://fapi.binance.com"


# =========================
# 📈 Trading (ativos e timeframes)
# =========================
TRADING_PAIRS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT"]
TIMEFRAMES = ["1m", "5m", "15m"]  


# =========================
# ⚖️ Estratégia e Indicadores
# =========================
STOP_LOSS_ATR_MULTIPLIER = 1.5   # multiplicador do ATR para SL
TAKE_PROFIT_ATR_MULTIPLIER = 3   # multiplicador do ATR para TP


# =========================
# 🛡️ Gerenciamento de risco
# =========================
RISK_PERCENT = 1.0             # % do saldo arriscado por trade
MAX_DAILY_LOSS_PERCENT = 5.0   # % máximo de perda diária antes de parar o bot
MAX_POSITION_SIZE = 2.0        # % máximo do saldo em UMA posição (protege contra alavancagem excessiva)


# =========================
# 📢 Alertas (Telegram)
# =========================
TELEGRAM_TOKEN = ""       # Coloque seu token de bot do Telegram
TELEGRAM_CHAT_ID = ""     # Seu chat_id


# =========================
# ⚙️ Outros
# =========================
QUANTITY_DEFAULT = 0.001  # quantidade mínima default para evitar zero
