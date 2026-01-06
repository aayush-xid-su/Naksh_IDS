# preprocessing/encoder.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder


def encode_features_safe(df):
    """
    Encodes all categorical columns safely.
    Returns:
        X_encoded (DataFrame)
        encoders (dict)
    """
    print("🔹 Encoding categorical features...")

    df = df.copy()
    encoders = {}

    categorical_cols = df.select_dtypes(include=["object", "category"]).columns

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = df[col].astype(str)
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    return df, encoders
