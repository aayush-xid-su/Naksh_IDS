# Computes trend of confidence values over batches

def compute_trend(prev_conf, current_conf):
    """
    Returns 'rising', 'falling', or 'stable'
    """
    if prev_conf is None:
        return "stable"
    if current_conf > prev_conf + 0.01:
        return "rising"
    elif current_conf < prev_conf - 0.01:
        return "falling"
    else:
        return "stable"
