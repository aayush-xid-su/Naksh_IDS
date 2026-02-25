from collections import deque
import numpy as np

class TemporalAnalyzer:
    def __init__(self, max_window: int = 10):
        self.max_window = max_window
        self.window = deque(maxlen=max_window)

    def update(self, confidences):
        mean_conf = np.mean(confidences)
        self.window.append(mean_conf)
        avg_score = np.mean(self.window)
        persistence = len(self.window)
        escalation = "HIGH" if avg_score > 0.75 else "MEDIUM" if avg_score > 0.5 else "LOW"
        return {"persistence": persistence, "avg_threat_score": avg_score, "escalation": escalation}
