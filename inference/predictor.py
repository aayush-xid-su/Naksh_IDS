# inference/predictor.py

import joblib
import numpy as np

MODEL_PATH = "models/ids_model.pkl"
MASK_PATH = "models/feature_mask.npy"

model = joblib.load(MODEL_PATH)
feature_mask = np.load(MASK_PATH)


def predict_packet(feature_vector: np.ndarray):
    """
    feature_vector: shape (N_features,)
    """

    if feature_vector.ndim == 1:
        feature_vector = feature_vector.reshape(1, -1)

    selected = feature_vector[:, feature_mask]

    prediction = model.predict(selected)[0]
    confidence = max(model.predict_proba(selected)[0])

    return {
        "attack": bool(prediction),
        "confidence": round(float(confidence), 4)
    }
