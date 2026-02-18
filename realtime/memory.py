# realtime/memory.py
from collections import defaultdict, deque

class ThreatMemory:
    def __init__(self, window=10):
        self.window = window
        self.memory = defaultdict(lambda: deque(maxlen=window))

    def update(self, attack, confidence):
        self.memory[attack].append(confidence)

    def average_confidence(self, attack):
        values = self.memory.get(attack, [])
        if not values:
            return 0.0
        return round(sum(values) / len(values), 3)

    def persistence_count(self, attack, baseline=0.45):
        return sum(1 for c in self.memory.get(attack, []) if c >= baseline)

    def should_escalate(self, attack):
        avg = self.average_confidence(attack)
        persistent_hits = self.persistence_count(attack)

        if persistent_hits >= 5 and avg >= 0.50:
            return True, "Persistent malicious confidence above baseline"
        return False, None
