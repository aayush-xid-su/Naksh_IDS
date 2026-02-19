# realtime/model_loader.py
import joblib

MODEL_PATH = "models/rf_v1.joblib"

def load_model_bundle():
    bundle = joblib.load(MODEL_PATH)
    required_keys = ["model", "feature_names", "label_encoder", "encoders"]
    for key in required_keys:
        if key not in bundle:
            raise ValueError(f"Missing `{key}` in model bundle")
    return bundle
