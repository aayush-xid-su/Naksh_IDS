from collections import defaultdict, deque

class CorrelationEngine:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.history = deque(maxlen=window_size)
        self.attack_counts = defaultdict(int)

    def update(self, attack, confidence):
        self.history.append((attack, confidence))
        self.attack_counts[attack] += 1

    def threat_score(self):
        score = 0

        unique_attacks = set(a for a, _ in self.history)
        score += len(unique_attacks) * 15

        for attack, count in self.attack_counts.items():
            if attack != "Normal":
                score += min(count * 10, 40)

        avg_conf = (
            sum(c for _, c in self.history) / len(self.history)
            if self.history else 0
        )
        score += int(avg_conf * 30)

        return min(score, 100)

    def escalation_level(self):
        score = self.threat_score()
        if score >= 75:
            return "critical"
        if score >= 55:
            return "high"
        if score >= 35:
            return "medium"
        if score >= 20:
            return "low"
        return "none"
