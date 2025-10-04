# alerts.py (revisado)
import asyncio
import aiohttp
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


async def send_telegram_async(message: str):
    """
    Envia mensagem para o Telegram (assíncrono).
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": f"[BOT] {message}"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as resp:
                if resp.status != 200:
                    print(f"[Telegram] Erro {resp.status}: {await resp.text()}")
    except Exception as e:
        print(f"[Telegram] Falha ao enviar mensagem: {e}")


def send_telegram(message: str):
    """
    Wrapper síncrono para enviar alertas sem bloquear threads.
    """
    try:
        asyncio.get_event_loop().create_task(send_telegram_async(message))
    except RuntimeError:
        # Caso não haja loop rodando (ex: execução direta no main)
        asyncio.run(send_telegram_async(message))
