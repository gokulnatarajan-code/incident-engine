from connectors.software_log_connector import SoftwareLogConnector
from connectors.hardware_stub_connector import HardwareStubConnector

ACTIVE_CONNECTORS = [
    SoftwareLogConnector(),
    HardwareStubConnector(),
]

def collect_all_alerts():
    all_alerts = []
    for connector in ACTIVE_CONNECTORS:
        alerts = connector.fetch_alerts()
        print(f"[{connector.name}] fetched {len(alerts)} alerts")
        all_alerts.extend(alerts)
    return all_alerts
