# Computes correlated threat score and escalation
def correlate_events(events):
    """
    events: list of dicts with 'confidence' keys
    returns dict: threat_score (0-100), escalation ('low','medium','high')
    """
    if not events:
        return {"threat_score": 0, "escalation": "none"}

    avg_conf = sum(e["confidence"] for e in events) / len(events)
    max_conf = max(e["confidence"] for e in events)

    threat_score = int(avg_conf * 100)
    if max_conf > 0.8 or threat_score > 75:
        escalation = "high"
    elif max_conf > 0.5 or threat_score > 50:
        escalation = "medium"
    else:
        escalation = "low"

    return {"threat_score": threat_score, "escalation": escalation}
