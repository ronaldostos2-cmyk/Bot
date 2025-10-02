from bot_thread import BotThread
from config import TRADING_PAIRS
import time
from utils import summarize_daily
from statistics import summarize_statistics
from alerts import send_telegram

threads = []

# Inicializa bots para cada par
for pair in TRADING_PAIRS:
    bot = BotThread(pair)
    bot.start()
    threads.append(bot)
    print(f"[MAIN] Bot iniciado para {pair}")

try:
    print("[MAIN] Bots rodando. Pressione Ctrl+C para encerrar.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[MAIN] Encerrando bots...")
    send_telegram("Bots estão sendo encerrados manualmente.")

    for bot in threads:
        bot.stop()
    for bot in threads:
        bot.join()

    summarize_daily()
    summarize_statistics()
    send_telegram("Resumo diário e estatísticas enviadas. Todos os bots encerrados.")
    print("[MAIN] Todos os bots encerrados.")
