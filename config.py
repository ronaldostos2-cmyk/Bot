# =========================
# CONFIGURAÇÕES GERAIS - NÍVEL 3
# =========================

API_KEY = "d47789171a725c0b7becb283a989f44963698d6349a857a33d6e56750823f364"       # <- coloque sua API aqui
API_SECRET = "b217fe9799c0fa744c7c9703d3f6b55b09ef7c92c927cb25d8b2e890c73dbcce" # <- coloque sua SECRET aqui

BASE_URL = "https://testnet.binancefuture.com"  # Testnet URL
PAIRS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]       # Pares a operar

# Percentual base do saldo por trade
BASE_RISK_PERCENT = 0.05

# Stop Loss / Take Profit base (ajustáveis dinamicamente)
BASE_STOP_LOSS = 0.02
BASE_TAKE_PROFIT = 0.04

# Intervalos de velas
INTERVAL_SHORT = '15m'  # curto prazo
INTERVAL_LONG = '1h'    # médio prazo

# Alertas no terminal
ALERTS = True

# Sequência máxima de perdas antes do cooldown
MAX_CONSECUTIVE_LOSSES = 3

# Mínimo de volatilidade para operar (ATR)
MIN_ATR_MULTIPLIER = 1.0
