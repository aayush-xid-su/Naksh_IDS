import pandas as pd
import os
import random

DATA_DIR = "data"

def get_realtime_batch(batch_size=512):
    """Randomly sample rows from CSVs to simulate real-time batch"""
    csv_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    df_list = [pd.read_csv(f) for f in csv_files]
    full_df = pd.concat(df_list, ignore_index=True)

    # Random sample
    batch_df = full_df.sample(batch_size, replace=True).drop(columns=["Label"], errors="ignore")
    return batch_df
