import json
import os
from connectors.base import Connector

class SoftwareLogConnector(Connector):
    name = "software-logs"

    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(base, "..", "..", "logs", "all.log")

    def fetch_alerts(self):
        if not os.path.exists(self.path):
            return []
        alerts = []
        with open(self.path) as f:
            for line in f:
                entry = json.loads(line)
                if entry["level"] in ("ERROR", "WARN"):
                    alerts.append(entry)
        return alerts