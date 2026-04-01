import threading
import logging

# basic logging setup (ek baar hi call hona chahiye app me)
logging.basicConfig(
    level=logging.INFO,
    format="📜 %(asctime)s [%(levelname)s] (%(threadName)s) %(message)s"
)

def start_thread(func, name=None):
    def wrapper():
        thread_name = name or func.__name__
        logging.info(f"🟢 Thread started: {thread_name}")
        try:
            func()
        except Exception as e:
            logging.exception(f"⚠️ Error in thread '{thread_name}': {e}")
        finally:
            logging.info(f"🛑 Thread finished: {thread_name}")

    t = threading.Thread(
        target=wrapper,
        daemon=True,
        name=name or func.__name__
    )
    t.start()

    logging.info(f"🚀 Thread launched: {t.name}")

