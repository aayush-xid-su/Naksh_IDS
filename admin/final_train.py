# admin/final_train.py

import json
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from preprocessing.dataset_loader import load_multiple_datasets
from preprocessing.schema_mapper import normalize_schema
from preprocessing.encoder import encode_features


MODEL_DIR = "models"


def final_training(best_solution):
    print("\n🚀 Starting FINAL IDS training...")

    # ---------------- Load & preprocess ----------------
    df = load_multiple_datasets("data")
    df = normalize_schema(df)
    df = encode_features(df)

    X = df.drop(columns=["label"]).values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    # ---------------- GA Outputs ----------------
    feature_mask = best_solution[:-2] > 0.5
    n_estimators = int(best_solution[-2])
    max_depth = int(best_solution[-1])

    print(f"✅ Selected features: {feature_mask.sum()}/{X.shape[1]}")
    print(f"🌲 Trees: {n_estimators}, Depth: {max_depth}")

    # ---------------- Final Model ----------------
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_leaf=3,
        max_features="sqrt",
        class_weight="balanced",
        n_jobs=-1,
        random_state=42
    )

    model.fit(X_train[:, feature_mask], y_train)

    # ---------------- Evaluation ----------------
    preds = model.predict(X_test[:, feature_mask])

    print("\n📊 CONFUSION MATRIX")
    print(confusion_matrix(y_test, preds))

    print("\n📄 CLASSIFICATION REPORT")
    print(classification_report(y_test, preds))

    # ---------------- Save Artifacts ----------------
    joblib.dump(model, f"{MODEL_DIR}/ids_model.pkl")
    np.save(f"{MODEL_DIR}/feature_mask.npy", feature_mask)

    metadata = {
        "model": "RandomForestClassifier",
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "total_features": int(X.shape[1]),
        "selected_features": int(feature_mask.sum())
    }

    with open(f"{MODEL_DIR}/metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    print("\n✅ FINAL IDS MODEL SAVED SUCCESSFULLY")


if __name__ == "__main__":
    raise RuntimeError("This file must be called from train_pipeline.py")
