import time
import json
from datetime import datetime
import numpy as np
import pandas as pd
from realtime.simulator import generate_batch
from realtime.model_loader import load_model_bundle
from realtime.correlation import correlate_events

# -----------------------------
# CONFIG
BATCH_SIZE = 4
CONFIDENCE_ALERT_THRESHOLD = 0.5  # min confidence to trigger alert
THREAT_SCORE_HIGH = 70
THREAT_SCORE_MEDIUM = 40
# -----------------------------

# Maintain previous predictions for trend calculation
prev_confidences = []

def compute_trend(prev, curr, delta=0.01):
    """
    Determine trend between previous and current confidence.
    """
    if prev is None:
        return "stable"
    if curr - prev > delta:
        return "rising"
    elif curr - prev < -delta:
        return "falling"
    else:
        return "stable"

def assign_severity(confidence, threat_score):
    """
    Determine severity level dynamically based on confidence + threat_score.
    """
    if threat_score >= THREAT_SCORE_HIGH or confidence >= 0.9:
        return "high"
    elif threat_score >= THREAT_SCORE_MEDIUM or confidence >= 0.7:
        return "medium"
    else:
        return "low"

def main():
    # Load model
    bundle = load_model_bundle()
    model = bundle.get("model")
    label_encoder = bundle.get("label_encoder")
    feature_names = bundle.get("feature_names")

    if model is None or label_encoder is None or feature_names is None:
        raise ValueError("Model bundle is incomplete!")

    global prev_confidences

    while True:
        # Generate simulated batch
        X_batch = generate_batch(BATCH_SIZE, feature_names)
        X_df = pd.DataFrame(X_batch, columns=feature_names)

        # Predict
        probs = model.predict_proba(X_df)
        classes = model.classes_

        events = []
        confidences = []

        for i, prob_array in enumerate(probs):
            top_idx = np.argmax(prob_array)
            attack_code = classes[top_idx]
            attack_name = label_encoder.inverse_transform([attack_code])[0]
            confidence = float(prob_array[top_idx])

            # Compute trend
            prev_conf = prev_confidences[i] if len(prev_confidences) > i else None
            trend = compute_trend(prev_conf, confidence)

            # Update previous confidence
            if len(prev_confidences) < BATCH_SIZE:
                prev_confidences.append(confidence)
            else:
                prev_confidences[i] = confidence

            events.append({
                "attack": attack_name,
                "confidence": round(confidence, 3),
                "trend": trend,
                "alert": False,  # temporarily, updated below
                "severity": "low"  # temporary
            })

            confidences.append(confidence)

        # Correlate events to get threat score & escalation
        correlation_result = correlate_events(events)

        # Assign alerts and severity dynamically
        for e, conf in zip(events, confidences):
            # Alert if confidence > threshold or threat_score high
            e["alert"] = conf >= CONFIDENCE_ALERT_THRESHOLD or correlation_result["threat_score"] >= THREAT_SCORE_MEDIUM
            e["severity"] = assign_severity(conf, correlation_result["threat_score"])

        output = {
            "events": events,
            "correlated_threat": correlation_result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        print(json.dumps(output, indent=2))
        time.sleep(1)  # simulate real-time streaming


if __name__ == "__main__":
    main()
