def build_explanation(metrics, temporal, threat_score):
    if metrics["attacks"] == 0:
        return "No malicious activity detected in the current observation window."

    reasons = []

    if metrics["ratio"] > 0.15:
        reasons.append("High proportion of malicious predictions")

    if temporal["persistence"] >= 2:
        reasons.append("Repeated malicious behavior across time windows")

    if threat_score >= 0.7:
        reasons.append("High combined threat score from multiple signals")

    return "; ".join(reasons)
