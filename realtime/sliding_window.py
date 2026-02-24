from collections import deque
import numpy as np

class SlidingWindow:
    def __init__(self, size=20, attack_threshold=0.7):
        self.size = size
        self.attack_threshold = attack_threshold
        self.window = deque(maxlen=size)

    def add(self, prediction, confidence):
        self.window.append((prediction, confidence))

    def attack_ratio(self):
        if not self.window:
            return 0
        attacks = sum(1 for p, c in self.window if p == 1)
        return attacks / len(self.window)

    def is_under_attack(self):
        return self.attack_ratio() >= self.attack_threshold
