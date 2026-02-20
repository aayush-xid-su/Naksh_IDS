# realtime/preprocessing.py
import pandas as pd

def preprocess_features(df):
    # Ensure numeric columns are floats
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = df[col].astype(str)
    # Fill NaNs
    df.fillna(0, inplace=True)
    return df
