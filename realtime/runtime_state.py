from collections import deque
from datetime import datetime, timedelta


class RuntimeState:
    def __init__(self, window_minutes=5):
        self.window = timedelta(minutes=window_minutes)
        self.history = deque()

    def add(self, batch_result):
        now = datetime.utcnow()
        self.history.append((now, batch_result))
        self._expire(now)

    def _expire(self, now):
        while self.history and now - self.history[0][0] > self.window:
            self.history.popleft()

    def temporal_analysis(self):
        persistence = sum(
            1 for _, r in self.history if r["metrics"]["attacks"] > 0
        )

        if persistence >= 4:
            escalation = "HIGH"
        elif persistence >= 2:
            escalation = "MEDIUM"
        else:
            escalation = "LOW"

        trend = "INCREASING" if persistence >= 2 else "NONE"

        return {
            "persistence": persistence,
            "trend": trend,
            "escalation": escalation
        }
