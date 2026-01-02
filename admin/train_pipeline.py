# admin/train_pipeline.py

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# =========================
# PREPROCESSING IMPORTS
# =========================
from preprocessing.dataset_loader import load_multiple_datasets
from preprocessing.schema_mapper import normalize_schema
from preprocessing.data_cleaner import clean_data
from preprocessing.encoder import encode_features_safe
from preprocessing.scaler import scale_features
from preprocessing.feature_engineering import remove_low_variance

# =========================
# ML + GA IMPORTS
# =========================
from ga.ga_optimizer import run_ga
from ml_models.train_model import train_final_model


# =========================
# LABEL NORMALIZATION
# =========================
def normalize_label(row):
    """
    Binary label mapping:
    0 -> Benign / Normal
    1 -> Attack
    """
    benign_keywords = ["normal", "benign", "none", "no attack", "false", "0", "low"]

    for col in row.index:
        col_lower = col.lower()
        if any(k in col_lower for k in ["label", "attack", "severity", "class"]):
            value = str(row[col]).lower()
            if any(b in value for b in benign_keywords):
                return 0
    return 1


# =========================
# MAIN TRAINING PIPELINE
# =========================
def main():
    print("🔹 Loading datasets...")
    df = load_multiple_datasets("data")

    print("🔹 Normalizing schema...")
    df = normalize_schema(df)
    print("Columns after normalization:", df.columns.tolist())

    # -------------------------
    # LABEL CREATION
    # -------------------------
    print("🔹 Normalizing labels...")
    df["label"] = df.apply(normalize_label, axis=1)
    print("Label value counts:\n", df["label"].value_counts())

    # -------------------------
    # SPLIT FEATURES / TARGET
    # -------------------------
    y = df["label"]
    X = df.drop(columns=["label"])

    # -------------------------
    # PREPROCESSING PIPELINE
    # -------------------------
    print("🔹 Cleaning data...")
    X = clean_data(X)

    print("🔹 Encoding categorical features...")
    X, encoders = encode_features_safe(X)

    print("🔹 Scaling features...")
    X_scaled, scaler = scale_features(X)

    print("🔹 Removing low-variance features...")
    X_reduced, var_selector = remove_low_variance(X_scaled)

    # -------------------------
    # SAVE TRAINING COLUMNS
    # -------------------------
    # Save the column order AFTER preprocessing for real-time inference
    training_columns = (
        X.columns if hasattr(X, "columns") else pd.DataFrame(X).columns
    )
    os.makedirs("model", exist_ok=True)
    joblib.dump(training_columns, "model/training_columns.pkl")

    # -------------------------
    # TRAIN / TEST SPLIT
    # -------------------------
    X_np = X_reduced if isinstance(X_reduced, np.ndarray) else X_reduced.values
    y_np = y.values if hasattr(y, "values") else y

    X_train, X_test, y_train, y_test = train_test_split(
        X_np,
        y_np,
        test_size=0.2,
        stratify=y_np,
        random_state=42
    )

    # -------------------------
    # GENETIC ALGORITHM
    # -------------------------
    print("🧬 Running Genetic Algorithm...")
    best_solution = run_ga(X_train, X_test, y_train, y_test)

    feature_mask = best_solution[:-2] > 0.5
    n_estimators = int(best_solution[-2])
    max_depth = int(best_solution[-1])
    print(f"🧬 Best GA Fitness Score: {best_solution[-1]:.4f}")

    # -------------------------
    # FINAL MODEL TRAINING
    # -------------------------
    print("🔥 Final IDS model training...")
    model = train_final_model(
        X_reduced,
        y_np,
        feature_mask,
        n_estimators,
        max_depth
    )

    # -------------------------
    # SAVE ARTIFACTS
    # -------------------------
    joblib.dump(model, "model/ids_model.pkl")
    joblib.dump(scaler, "model/scaler.pkl")
    joblib.dump(encoders, "model/encoders.pkl")
    joblib.dump(var_selector, "model/variance_selector.pkl")
    joblib.dump(feature_mask, "model/selected_features.pkl")

    print("✅ Multi-dataset IDS model trained successfully")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
