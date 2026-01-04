# ml_models/train_model.py

import numpy as np
from sklearn.ensemble import RandomForestClassifier

def train_final_model(X, y, feature_mask, n_estimators, max_depth):
    """
    Train the final RandomForest model using GA-selected features.
    """
    X_selected = X[:, feature_mask] if isinstance(X, np.ndarray) else X.values[:, feature_mask]

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_selected, y)
    return model


def predict_model(model, X_batch):
    """
    Predicts labels for a batch of preprocessed features.
    Returns np.ndarray of 0/1 labels.
    """
    if not isinstance(X_batch, np.ndarray):
        X_batch = X_batch.values  # fallback
    return model.predict(X_batch)
