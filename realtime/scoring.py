def decide_alert(attack, confidence):
    """
    SOC-grade alert & severity logic
    """

    if attack == "Normal":
        return False, "low"

    # Attack detected
    if confidence >= 0.55:
        return True, "high"

    if confidence >= 0.40:
        return True, "medium"

    return True, "low"
