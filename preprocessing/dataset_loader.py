# preprocessing/dataset_loader.py

import os
import pandas as pd
import glob


def load_multiple_datasets(data_dir="data"):
    """
    Loads and merges all CSV datasets from a directory
    """
    if not os.path.isdir(data_dir):
        raise ValueError(f"❌ Data directory not found: {data_dir}")

    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))

    if not csv_files:
        raise ValueError(f"❌ No CSV files found in {data_dir}")

    print(f"📂 Found {len(csv_files)} dataset(s):")
    for f in csv_files:
        print("   -", f)

    dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file, low_memory=False)
            df["__source_file__"] = os.path.basename(file)
            dfs.append(df)
        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")

    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"✅ Combined dataset shape: {combined_df.shape}")

    return combined_df
