import logging
import os
import threading
import time
import requests
from queue import Queue

# =========================
# ⚙️ CONFIG (ENV)
# =========================
BOT_TOKEN = os.getenv("LOGGER_BOT_TKN")
CHAT_ID = os.getenv("LOGGER_CHAT_ID")

# =========================
# 🎨 COLORS (Markdown)
# =========================
LEVEL_EMOJI = {
    "DEBUG": "⚪",
    "INFO": "🟢",
    "WARNING": "🟡",
    "ERROR": "🔴",
    "CRITICAL": "🚨"
}

# =========================
# 📦 Queue + Worker
# =========================
log_queue = Queue()
BATCH_SIZE = 10
FLUSH_INTERVAL = 5  # seconds


def telegram_worker():
    buffer = []
    last_flush = time.time()

    while True:
        try:
            log = log_queue.get(timeout=1)
            buffer.append(log)
        except:
            pass

        now = time.time()

        if len(buffer) >= BATCH_SIZE or (buffer and now - last_flush >= FLUSH_INTERVAL):
            send_batch(buffer)
            buffer.clear()
            last_flush = now


def send_batch(logs):
    try:
        text = "\n\n".join(logs)

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": text[:4000],  # Telegram limit
                "parse_mode": "Markdown"
            },
            timeout=5
        )
    except:
        pass


# =========================
# 🧠 Custom Handler
# =========================
class TelegramBatchHandler(logging.Handler):
    def emit(self, record):
        try:
            level = record.levelname
            emoji = LEVEL_EMOJI.get(level, "⚪")

            log_entry = self.format(record)

            formatted = (
                f"{emoji} *{level}*\n"
                f"`{record.threadName}`\n"
                f"{log_entry}"
            )

            log_queue.put(formatted)

        except:
            pass


# =========================
# 🚀 Setup Function
# =========================
def setup_telegram_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s\n%(message)s"
    )

    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Telegram handler
    tg_handler = TelegramBatchHandler()
    tg_handler.setFormatter(formatter)
    logger.addHandler(tg_handler)

    # Start worker thread
    t = threading.Thread(target=telegram_worker, daemon=True)
    t.start()