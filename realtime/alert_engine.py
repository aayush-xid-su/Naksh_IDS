from collections import deque
import random

# Maintain a sliding window for multi-batch trend analysis
BATCH_HISTORY = 5
recent_attack_ratios = deque(maxlen=BATCH_HISTORY)

def compute_severity(attack_ratio):
    """
    Compute severity based on attack ratio thresholds.
    """
    if attack_ratio > 0.5:
        return "CRITICAL"
    elif attack_ratio > 0.2:
        return "HIGH"
    elif attack_ratio > 0.05:
        return "MEDIUM"
    else:
        return "LOW"

def compute_trend(attack_ratio):
    """
    Compute trend based on recent attack ratios.
    """
    recent_attack_ratios.append(attack_ratio)
    if len(recent_attack_ratios) < 2:
        return "STABLE"

    delta = attack_ratio - recent_attack_ratios[-2]
    if delta > 0.05:
        return "INCREASING"
    elif delta < -0.05:
        return "DECREASING"
    else:
        return "STABLE"

def fetch_dynamic_threat_intel():
    """
    Return dynamic threat intelligence (stub with random example).
    """
    tactics = ["Command and Control", "Exfiltration", "Credential Access", "Lateral Movement"]
    techniques = [
        "T1071 - Application Layer Protocol",
        "T1041 - Exfiltration Over C2 Channel",
        "T1078 - Valid Accounts",
        "T1021 - Remote Services"
    ]
    return {
        "tactic": random.choice(tactics),
        "technique": random.choice(techniques),
        "category": "Active Intrusion",
        "confidence": round(random.uniform(0.7, 0.99), 2)
    }

def process_alerts(preds, severity):
    """
    Trigger alerts based on severity and recent trends.
    """
    attack_ratio = (preds == 1).sum() / len(preds) if len(preds) > 0 else 0
    trend = compute_trend(attack_ratio)
    alert_triggered = False

    if severity in ["HIGH", "CRITICAL"] and attack_ratio > 0.01:
        alert_triggered = True
        print(f"🚨 SOC ALERT [{severity}] — {trend} threat detected!")

    return alert_triggered, trend, attack_ratio
