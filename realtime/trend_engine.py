# realtime/trend_engine.py

from collections import deque

# =========================
# TREND CONFIG
# =========================
WINDOW_SIZE = 5
ESCALATION_THRESHOLD = 0.15   # 15% increase

attack_ratio_window = deque(maxlen=WINDOW_SIZE)


def update_trend(current_ratio: float) -> str:
    """
    Returns trend state:
    - STABLE
    - ESCALATING
    - DEESCALATING
    """
    if len(attack_ratio_window) > 0:
        previous = attack_ratio_window[-1]
    else:
        previous = current_ratio

    attack_ratio_window.append(current_ratio)

    if current_ratio - previous >= ESCALATION_THRESHOLD:
        return "ESCALATING"
    elif previous - current_ratio >= ESCALATION_THRESHOLD:
        return "DEESCALATING"
    else:
        return "STABLE"
