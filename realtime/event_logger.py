import json
from datetime import datetime
import os

LOG_DIR = "logs"
LOG_FILE = "logs/ids_events.log"

os.makedirs(LOG_DIR, exist_ok=True)

def log_event(
    source,
    prediction,
    confidence,
    dataset
):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "source": source,
        "prediction": "ATTACK" if prediction == 1 else "BENIGN",
        "confidence": round(float(confidence), 4),
        "dataset": dataset
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
