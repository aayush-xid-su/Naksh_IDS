class AlertEngine:
    def __init__(self, confidence_threshold=0.6):
        self.confidence_threshold = confidence_threshold

    def evaluate(self, temporal_result):
        triggered = temporal_result["avg_threat_score"] >= self.confidence_threshold

        return {
            "triggered": triggered,
            "severity": temporal_result["escalation"],
            "reason": "above_threshold" if triggered else "below_threshold",
            "confidence_threshold": self.confidence_threshold
        }
