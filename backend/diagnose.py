import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path="../.env")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def diagnose(cluster):
    log_text = "\n".join(
        f"[{a['service']}] {a['level']}: {a['message']}" for a in cluster[:30]
    )

    prompt = f"""You are an SRE assistant. Below are correlated log lines from ONE incident.

LOGS:
{log_text}

Identify:
1. service: which service failed FIRST (the root cause, not a symptom)
2. root_cause: one sentence, must quote specific evidence from the logs
3. evidence: the exact log line that proves it
4. confidence: a number 0-100

Respond with ONLY valid JSON in this exact shape, no markdown, no explanation outside the JSON:
{{"service": "...", "root_cause": "...", "evidence": "...", "confidence": 90}}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_text = response.choices[0].message.content
    return json.loads(raw_text)


if __name__ == "__main__":
    from cluster import load_alerts, cluster_alerts
    from history import load_history, save_incident, find_similar

    alerts = load_alerts()
    clusters = cluster_alerts(alerts)

    print(f"\nFound {len(clusters)} incident cluster(s). Diagnosing the first one...\n")

    result = diagnose(clusters[0])
    history = load_history()
    similar = find_similar(result["service"], history)

    print("=== DIAGNOSIS ===")
    print(f"Service:    {result['service']}")
    print(f"Root cause: {result['root_cause']}")
    print(f"Evidence:   {result['evidence']}")
    print(f"Confidence: {result['confidence']}%")

    if similar:
        print(f"\n[!] Similar past incident found: #{similar['incident_id']} - {similar['root_cause']}")
    else:
        print("\nNo similar past incident found - this is new.")

    incident_id = save_incident(result)
    print(f"\nSaved as incident #{incident_id}")
    print(f"\n=== RECOMMENDED FIX ===")
    fix_map = {
        "database": "Restart connection pool / increase max_connections",
        "api": "Restart API service",
        "frontend": "No direct fix needed - will recover once upstream is fixed",
    }
    fix = fix_map.get(result["service"], "Manual investigation required")
    print(f"Action: {fix}")

    confirm = input("Apply this fix? (y/n): ")
    if confirm.lower() == "y":
        print(f"Applying fix: {fix}...")
        print(f"[SIMULATED] {result['service']} service restarted successfully.")
        print(f"Incident #{incident_id} marked as RESOLVED.")
    else:
        print("Fix not applied. Incident remains open.")
