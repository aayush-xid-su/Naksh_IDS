# realtime/temporal.py
import pandas as pd

class TemporalAnalyzer:
    def __init__(self):
        self.last_confidence = {}

    def analyze(self, attack, confidence):
        prev = self.last_confidence.get(attack, confidence)
        self.last_confidence[attack] = confidence
        return "rising" if confidence > prev else "falling" if confidence < prev else "stable"
