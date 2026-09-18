import time
from connectors.base import Connector

class HardwareStubConnector(Connector):
    name = "hardware-sensors"

    def fetch_alerts(self):
        # Simulated sensor data — same shape as software alerts,
        # so the pipeline treats it identically.
        now = time.time()
        return [
            {"ts": now, "service": "temp-sensor-1", "level": "WARN",
             "message": "temperature 84C exceeds threshold 75C"},
            {"ts": now + 1, "service": "temp-sensor-1", "level": "ERROR",
             "message": "sensor read timeout after 3 retries"},
        ]
    