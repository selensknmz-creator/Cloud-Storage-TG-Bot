from config import config
from telegram_logger import setup_telegram_logger
setup_telegram_logger()
import logging
from webApp.flask_srvr import run_thread
from managers.thread_manager import start_thread
import time

run_thread(run_flask, name="FlaskServer")

logging.info(config.id)

logging.info("Server started 🚀")
logging.error("Something failed ❌")
# Keep main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")





