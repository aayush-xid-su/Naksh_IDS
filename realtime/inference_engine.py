import pandas as pd
import numpy as np

def align_features(df, training_columns):
    """
    Ensures real-time batch matches training feature space
    """
    df = df.copy()

    # Add missing columns
    for col in training_columns:
        if col not in df.columns:
            df[col] = 0

    # Drop extra columns
    df = df[training_columns]

    return df


def run_inference(
    batch_df,
    model,
    encoders,
    scaler,
    var_selector,
    feature_mask,
    training_columns
):
    """
    Full preprocessing + prediction pipeline
    """

    # ---------- Encode categorical ----------
    for col, encoder in encoders.items():
        if col in batch_df.columns:
            batch_df[col] = batch_df[col].astype(str)
            batch_df[col] = batch_df[col].map(
                lambda x: encoder.transform([x])[0]
                if x in encoder.classes_ else -1
            )

    # ---------- Align features ----------
    batch_df = align_features(batch_df, training_columns)

    # ---------- Scale ----------
    X_scaled = scaler.transform(batch_df)

    # ---------- Variance selector ----------
    X_var = var_selector.transform(X_scaled)

    # ---------- Feature mask ----------
    X_final = X_var[:, feature_mask]

    # ---------- Predict ----------
    preds = model.predict(X_final)
    probs = model.predict_proba(X_final)[:, 1]

    return preds, probs
