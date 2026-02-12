from collections import deque, defaultdict
import numpy as np

class ConfidenceTracker:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.history = defaultdict(lambda: deque(maxlen=window_size))

    def update(self, attack, confidence):
        self.history[attack].append(confidence)

    def get_avg_confidence(self, attack):
        values = self.history.get(attack, [])
        if not values:
            return 0.0
        return float(np.mean(values))

    def get_trend(self, attack):
        values = list(self.history.get(attack, []))
        if len(values) < 2:
            return "stable"
        return "rising" if values[-1] > values[0] else "falling"
