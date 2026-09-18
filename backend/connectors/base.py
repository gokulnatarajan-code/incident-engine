class Connector:
    """Every plugin must implement this shape."""

    name = "unnamed-connector"

    def fetch_alerts(self):
        """Return a list of alert dicts: {ts, service, level, message}"""
        raise NotImplementedError