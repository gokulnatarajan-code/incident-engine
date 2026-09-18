import json
from connectors.base import Connector

class SoftwareLogConnector(Connector):
    name = "software-logs"

    def __init__(self, path="../logs/all.log"):
        self.path = path

    def fetch_alerts(self):
        alerts = []
        with open(self.path) as f:
            for line in f:
                entry = json.loads(line)
                if entry["level"] in ("ERROR", "WARN"):
                    alerts.append(entry)
        return alerts