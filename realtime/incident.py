from datetime import datetime, timezone

def build_incident(batch_metrics, temporal_analysis, alert):
    return {
        "incident_type": "CYBER_INTRUSION",
        "severity": alert["severity"],
        "triggered": alert["triggered"],
        "attack_ratio": batch_metrics["attack_ratio"],
        "avg_threat_score": temporal_analysis["avg_threat_score"],
        "persistence": temporal_analysis["persistence"],
        "escalation": temporal_analysis["escalation"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
