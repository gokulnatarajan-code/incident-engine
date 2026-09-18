from registry import collect_all_alerts

def load_alerts():
    return collect_all_alerts()

def cluster_alerts(alerts, window=30):
    alerts.sort(key=lambda a: a["ts"])
    clusters = []
    for a in alerts:
        placed = False
        for c in clusters:
            if a["ts"] - c[-1]["ts"] <= window:
                c.append(a)
                placed = True
                break
        if not placed:
            clusters.append([a])
    return clusters

if __name__ == "__main__":
    alerts = load_alerts()
    clusters = cluster_alerts(alerts)
    print(f"\nTotal alerts across all plugins: {len(alerts)}")
    print(f"Number of incident clusters: {len(clusters)}")
    for i, c in enumerate(clusters):
        services = set(a["service"] for a in c)
        print(f"  Cluster {i+1}: {len(c)} alerts across {services}")
