MAX_QUEUE = 10_000

def check_backpressure(queue_length):
    if queue_length > MAX_QUEUE:
        return {
            "action": "DROP",
            "severity": "HIGH",
            "reason": "ingestion_overflow"
        }
    return None
