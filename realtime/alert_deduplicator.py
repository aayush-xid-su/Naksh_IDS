from datetime import datetime, timedelta

class AlertDeduplicator:
    def __init__(self, suppress_minutes=5):
        self.suppress_window = timedelta(minutes=suppress_minutes)
        self.last_alerts = {}  # attack_type -> alert metadata

    def evaluate(self, attack, severity, threat_score):
        now = datetime.utcnow()

        if attack not in self.last_alerts:
            self.last_alerts[attack] = {
                "time": now,
                "severity": severity,
                "threat_score": threat_score
            }
            return "new"

        previous = self.last_alerts[attack]

        # Escalation check
        if threat_score > previous["threat_score"] + 10:
            self.last_alerts[attack] = {
                "time": now,
                "severity": severity,
                "threat_score": threat_score
            }
            return "escalated"

        # Suppression window check
        if now - previous["time"] < self.suppress_window:
            return "suppressed"

        # Window expired → new alert
        self.last_alerts[attack] = {
            "time": now,
            "severity": severity,
            "threat_score": threat_score
        }
        return "new"
