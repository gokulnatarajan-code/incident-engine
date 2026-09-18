import json
import time

def emit(service, level, message, path="logs/all.log"):
    entry = {"ts": time.time(), "service": service, "level": level, "message": message}
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")