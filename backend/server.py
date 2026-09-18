from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/trigger-chaos")
def trigger_chaos():
    subprocess.run(["python", "../services/chaos.py"])
    return {"status": "triggered"}

@app.get("/incidents")
def get_incidents():
    from cluster import load_alerts, cluster_alerts
    from diagnose import diagnose
    from history import load_history, save_incident, find_similar

    alerts = load_alerts()
    clusters = cluster_alerts(alerts)
    results = []
    for c in clusters:
        try:
            result = diagnose(c)
        except Exception:
            continue
        history = load_history()
        similar = find_similar(result["service"], history)
        result["similar"] = similar["root_cause"] if similar else None
        result["alert_count"] = len(c)
        incident_id = save_incident(result)
        result["incident_id"] = incident_id
        results.append(result)

    return {"total_alerts": len(alerts), "incidents": results}

@app.post("/apply-fix/{service}")
def apply_fix(service: str):
    fix_map = {
        "database": "Restart connection pool / increase max_connections",
        "api": "Restart API service",
        "frontend": "No direct fix needed",
        "temp-sensor-1": "Reset sensor connection",
    }
    fix = fix_map.get(service, "Manual investigation required")
    return {"status": "applied", "action": fix}
