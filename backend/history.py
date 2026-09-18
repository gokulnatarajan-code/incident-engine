import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
HISTORY_PATH = os.path.join(BASE, "..", "logs", "history.json")

def load_history():
    if not os.path.exists(HISTORY_PATH):
        return []
    with open(HISTORY_PATH) as f:
        return json.load(f)

def save_incident(diagnosis):
    history = load_history()
    diagnosis["incident_id"] = len(history) + 1
    history.append(diagnosis)
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)
    return diagnosis["incident_id"]

def find_similar(service, history):
    matches = [h for h in history if h["service"] == service]
    return matches[-1] if matches else None