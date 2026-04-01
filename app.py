from config import config
from webApp.flask_srvr import run_thread
from managers.thread_manager import start_thread
import time

run_thread(run_flask, name="FlaskServer")

print(config.id)

# Keep main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")