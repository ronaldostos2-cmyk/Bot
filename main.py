# main.py (revisado)
import time
from bot_thread import BotThread
from config import TRADING_PAIRS
from utils import summarize_daily, init_db
from statistics import summarize_statistics
from alerts import send_telegram

threads = []


def start_bots():
    """
    Inicializa bots para cada par configurado.
    """
    init_db()  # garante que o banco está pronto
    for pair in TRADING_PAIRS:
        bot = BotThread(pair)
        bot.start()
        threads.append(bot)
        print(f"[MAIN] ✅ Bot iniciado para {pair}")
        send_telegram(f"Bot iniciado para {pair}")


def stop_bots():
    """
    Para todos os bots com segurança.
    """
    print("\n[MAIN] Encerrando bots...")
    send_telegram("⏹ Encerrando todos os bots...")

    for bot in threads:
        bot.stop()
    for bot in threads:
        bot.join()

    # Gera resumos
    summarize_daily()
    summarize_statistics()
    send_telegram("📊 Resumo diário e estatísticas enviadas. Todos os bots encerrados.")
    print("[MAIN] ✅ Todos os bots encerrados.")


if __name__ == "__main__":
    try:
        start_bots()
        print("[MAIN] Bots rodando. Pressione Ctrl+C para encerrar.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        stop_bots()

    except Exception as e:
        print(f"[MAIN] ❌ Erro crítico: {e}")
        send_telegram(f"[MAIN] ❌ Erro crítico: {e}")
        stop_bots()
