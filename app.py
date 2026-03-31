from config import config
import os
import threading
import time
from webApp.flask_srvr import run_flask

# =========================
# 🚀 FLASK
# =========================
def start_flask():
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

start_flask()

print(config.id)