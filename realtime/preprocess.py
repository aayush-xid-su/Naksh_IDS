import pandas as pd
import numpy as np

from preprocessing.schema_mapper import normalize_schema
from preprocessing.data_cleaner import clean_data
from preprocessing.encoder import encode_features_safe


def preprocess_batch(
    df,
    training_columns,
    encoders,
    scaler,
    var_selector,
    feature_mask
):
    # Normalize schema
    df = normalize_schema(df)

    # Align columns
    for col in training_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[training_columns]

    # Clean
    df = clean_data(df)

    # Encode (safe mode)
    df_encoded, _ = encode_features_safe(df, encoders=encoders)

    # Scale
    df_scaled = scaler.transform(df_encoded)

    # Variance filter
    df_reduced = var_selector.transform(df_scaled)

    # Feature selection (GA)
    df_final = df_reduced[:, feature_mask]

    return df_final
