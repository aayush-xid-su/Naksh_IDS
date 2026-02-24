from datetime import datetime
import json

def build_siem_event(batch_id, mode, model_version, metrics, temporal_analysis,
                     threat_intel, threat_score, kill_chain_phase, explanation, alert):
    event = {
        "event_type": "DETECTION_BATCH",
        "severity": "INFO",
        "runtime": {
            "mode": mode,
            "model_version": model_version
        },
        "metrics": metrics,
        "temporal_analysis": temporal_analysis,
        "threat_intel": threat_intel,
        "threat_score": threat_score,
        "kill_chain_phase": kill_chain_phase,
        "explanation": explanation,
        "alert": alert,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    print(json.dumps(event, indent=4))
    return event
