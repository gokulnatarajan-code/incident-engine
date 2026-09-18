import json
import time
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "all.log")

def emit(service, level, message, path=None):
    entry = {"ts": time.time(), "service": service, "level": level, "message": message}
    target = path or LOG_FILE
    with open(target, "a") as f:
        f.write(json.dumps(entry) + "\n")